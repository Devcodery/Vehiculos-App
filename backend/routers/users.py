from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models import User
from security import get_current_user, get_password_prehash, pwd_context

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.post("/", response_model=User)
async def create_user(user: User, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    # Comprobamos si el email ya existe
    statement = select(User).where(User.email == user.email)
    existing_user = session.exec(statement).first()
    
    if current_user.rol != "admin":
        raise HTTPException(status_code=403, detail="Solo los administradores pueden crear nuevos usuarios")
    
    # Si existe lanzamos la excepcion
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Pre-hash de la contraseña antes de aplicar bcrypt
    pre_hashed = get_password_prehash(user.password_hash)
    
    # Ahora aplicamos bcrypt al pre-hash
    user.password_hash = pwd_context.hash(pre_hashed)
    
    # Guardamos el usuario en la base de datos
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
