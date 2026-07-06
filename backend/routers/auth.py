from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from database import get_session
from models import User
from security import verificar_password, create_access_token
from services.audit_logger import log_action

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    statement = select(User).where(User.email == form_data.username)
    user = session.exec(statement).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales invalidas")
    
    if not verificar_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales invalidas")
    
    access_token = create_access_token(data={"sub": user.email, "id": user.user_id})
    log_action("auth", "inicio_sesion", user.email, f"Usuario {user.nombre} inició sesión correctamente")
    
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user_data": {
            "id": user.user_id,
            "email": user.email,
            "nombre": user.nombre,
            "rol": user.rol
        }
    }
