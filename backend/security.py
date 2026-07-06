import os
import hashlib
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from database import get_session
from models import User

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
MEDIA_ROOT = "/media_files"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

SECRET_KEY = os.getenv("SECRET_KEY", "MessiLoversGatusoOnlyFans20")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "")
ADMIN_FULLNAME = os.getenv("ADMIN_FULLNAME", "Admin AutoCare Pro")
ADMIN_ROLE = os.getenv("ADMIN_ROLE", "admin")

def verify_env_variables():
    missing_vars = []
    
    if not SECRET_KEY:
        missing_vars.append("SECRET_KEY")
    if not ALGORITHM:
        missing_vars.append("ALGORITHM")
    if not ACCESS_TOKEN_EXPIRE_MINUTES:
        missing_vars.append("ACCESS_TOKEN_EXPIRE_MINUTES")

    if missing_vars:
        raise RuntimeError(f"Variables de entorno faltantes: {', '.join(missing_vars)}")
    
verify_env_variables()

def create_access_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

def get_password_prehash(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def verificar_password(password_plana, password_hasheada_db):
    pre_hashed = get_password_prehash(password_plana)
    
    return pwd_context.verify(pre_hashed, password_hasheada_db)

async def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        token_data = payload.get("sub")
        
        if token_data is None:
            raise HTTPException(status_code=401, detail="Token inválido: falta 'sub'")
    except JWTError:
        raise HTTPException(status_code=401, detail="No se pudo validar el token")
    
    statement = select(User).where(User.email == token_data)
    user = session.exec(statement).first()
    
    if user is None:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    
    return user
