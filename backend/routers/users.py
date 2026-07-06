from typing import Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlmodel import Session, select
from database import get_session
from models import User
from security import get_current_user, get_password_prehash, pwd_context
from services.email_services import enviar_correo_real
from services.audit_logger import log_action

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

class UserCreate(BaseModel):
    nombre: str
    email: EmailStr
    password: str
    rol: str
    
class UserUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[str] = None

class PasswordUpdate(BaseModel):
    password_actual: str
    password_nueva: str

@router.post("/", response_model=User)
async def create_user(user: UserCreate, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    statement = select(User).where(User.email == user.email)
    existing_user = session.exec(statement).first()
    
    if current_user.rol != "admin":
        raise HTTPException(status_code=403, detail="Solo los administradores pueden crear nuevos usuarios")
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    pre_hashed = get_password_prehash(user.password)
     
    user.password = pwd_context.hash(pre_hashed)
    
    finalUser  = User(
        nombre=user.nombre,
        email=user.email,
        rol=user.rol,
        password_hash=user.password
    )
    
    session.add(finalUser)
    session.commit()
    session.refresh(finalUser)
    log_action("auth", "creacion_usuario", current_user.email, f"Creado usuario {finalUser.email} con rol {finalUser.rol}")
    return finalUser

@router.patch("/change", response_model=User)
async def actualizar_mi_perfil(
    datos: UserUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    datos_nuevos = datos.model_dump(exclude_unset=True)
    
    for clave, valor in datos_nuevos.items():
        setattr(current_user, clave, valor)
        
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    log_action("auth", "actualizacion_perfil", current_user.email, f"Actualizados datos: {datos_nuevos}")
    return current_user

@router.patch("/change/password")
async def cambiar_mi_password(
    datos: PasswordUpdate,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    pre_hashed_actual = get_password_prehash(datos.password_actual)
    if not pwd_context.verify(pre_hashed_actual, current_user.password_hash):
        raise HTTPException(status_code=400, detail="La contraseña actual es incorrecta.")
    
    pre_hashed_nueva = get_password_prehash(datos.password_nueva)
    current_user.password_hash = pwd_context.hash(pre_hashed_nueva)
    
    session.add(current_user)
    session.commit()
    log_action("auth", "cambio_password", current_user.email, "Modificó su contraseña de acceso")
    
    cuerpo_del_correo = f"""
    <div style="font-family: sans-serif; background-color: #111; color: #fff; padding: 20px; border: 4px solid #ff3333;">
        <h2 style="color: #ff3333;">ALERTA DE SEGURIDAD - AUTOCARE</h2>
        <p>Hola <strong>{current_user.nombre}</strong>,</p>
        <p>Te informamos que la contraseña de tu cuenta ha sido modificada recientemente.</p>
        <p>Si has sido tú, puedes ignorar este mensaje.</p>
        <p style="background-color: #ffcc00; color: #000; padding: 10px; font-weight: bold;">
           Si no has autorizado este cambio, contacta con el administrador del taller de inmediato.
        </p>
    </div>
    """
    
    background_tasks.add_task(
        enviar_correo_real, 
        email_destinatario=current_user.email,
        nombre_destinatario=current_user.nombre,
        asunto="Cambio de Contraseña - AutoCare", 
        cuerpo_html=cuerpo_del_correo
    )
    
    return {"mensaje": "Contraseña actualizada con éxito."}