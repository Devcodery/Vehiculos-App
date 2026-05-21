from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session, select
from database import create_db_and_tables, get_session, engine
from passlib.context import CryptContext
import hashlib
from models import User, Vehicle, Product, RevisionType, Revision
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
import os
from dotenv import load_dotenv
import shutil
from typing import Optional


load_dotenv()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
MEDIA_ROOT = "/media_files"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

origins = [
    "http://localhost:5173", # Puerto por defecto de Vite/Vue
    "http://127.0.0.1:5173",
]

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

# --- SECURITY UTILS ---

def create_access_token(data: dict):
    to_encode = data.copy()
    
    # Ponemos fecha de caducidad
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    # Firmamos el token con nuestra SECRET_KEY
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

def get_password_prehash(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def verificar_password(password_plana, password_hasheada_db):
    
    # Primero pre-hasheas lo que el usuario acaba de escribir
    pre_hashed = get_password_prehash(password_plana)
    
    # Luego comparas ese pre-hash con el hash de bcrypt de la DB
    return pwd_context.verify(pre_hashed, password_hasheada_db)


async def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    try:
        # 1. Decodificamos el JWT con nuestra SECRET_KEY
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        token_data = payload.get("sub")
        
        if token_data is None:
            raise HTTPException(status_code=401, detail="Token inválido: falta 'sub'")
    except JWTError:
        raise HTTPException(status_code=401, detail="No se pudo validar el token")
    
    # 2. Buscamos al usuario en la DB
    statement = select(User).where(User.email == token_data)
    user = session.exec(statement).first()
    
    if user is None:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    
    return user # Devolvemos el objeto usuario completo   


# --- LIFESPAN ---

# 1. Definimos el ciclo de vida (lifespan)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- ACCIONES AL ARRANCAR (STARTUP) ---
    print("Arrancando la API y verificando tablas...")
    create_db_and_tables()
    
    with Session(engine) as session:
        # Preguntamos: ¿Hay algún usuario en la tabla?
        primer_usuario = session.exec(select(User)).first()
        
        # Si la respuesta es NO (None), lo creamos nosotros
        if not primer_usuario:
            print("Base de datos vacía. Creando Administrador por defecto...")
            
            # Hasheamos la contraseña que queramos ponerle 
            pre_hashed = get_password_prehash(ADMIN_PASSWORD)
            hashed_password = pwd_context.hash(pre_hashed)
            
            admin_user = User(
                email=ADMIN_EMAIL,
                nombre=ADMIN_FULLNAME,
                password_hash=hashed_password,
                rol=ADMIN_ROLE
            )
            
            session.add(admin_user)
            session.commit()
        else:
            print("👍 La base de datos ya contiene usuarios.")
    
    yield  # Aquí es donde la aplicación "vive" y atiende peticiones
    
    # --- ACCIONES AL CERRAR (SHUTDOWN) ---
    print("Apagando la API...")

# 2. Pasamos el lifespan a la instancia de FastAPI
app = FastAPI(
    title="AutoCare Pro API",
    lifespan=lifespan
)

app.mount("/media", StaticFiles(directory=MEDIA_ROOT), name="media")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"], # Permite todas las cabeceras (incluyendo tu Token JWT)
)

# --- ROUTES ---

@app.get("/")
async def read_root():
    return {"message": "Bienvenido a AutoCare Pro API", "status": "Ready"}

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    # 1. Buscar al usuario por email (OAuth2 usa 'username' por defecto)
    statement = select(User).where(User.email == form_data.username)
    user = session.exec(statement).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales invalidas")
    
    if not verificar_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales invalidas")
    
    access_token = create_access_token(data={"sub": user.email, "id": user.id})
    
    return {
        "access_token": access_token, 
        "token_type": "bearer"
    }
    

@app.post("/usuarios/", response_model=User)
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

@app.post("/vehiculos/")
async def create_vehicle(matricula: str = Form(...),
                            alias: str = Form(...),
                            marca: str = Form(...),
                            modelo: str = Form(...),
                            kilometraje: int = Form(...),
                            archivo_foto: UploadFile = File(None),
                            session: Session = Depends(get_session),
                            current_user: User = Depends(get_current_user)):
    
    user_id = current_user.id
    db_path = None
    
    if archivo_foto:
        # Guardamos la foto en el servidor
        
        user_subfolder = f"vehicles/user{current_user.id}"
        destination_folder = os.path.join(MEDIA_ROOT, user_subfolder)
        os.makedirs(destination_folder, exist_ok=True)
        
        print(f"Guardando foto en: {destination_folder}")
        
        if archivo_foto and archivo_foto.filename:
            
            clean_name = archivo_foto.filename.replace(" ", "_")
            final_name = f"{matricula}_{clean_name}"
            file_path = os.path.join(destination_folder, final_name)
            
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(archivo_foto.file, buffer)
            
            db_path = f"{user_subfolder}/{final_name}"
    
    # Creamos una instancia del modelo Vehicle con los datos recibidos
    vehicle = Vehicle(
        matricula=matricula,
        alias=alias,
        marca=marca,
        modelo=modelo,
        kilometraje=kilometraje,
        user_id=user_id,
        imagen=db_path
    )
    
    session.add(vehicle)
    session.commit()
    session.refresh(vehicle)
    return vehicle

@app.get("/mis-vehiculos/", response_model=list[Vehicle])
async def list_vehicles(current_user: User = Depends(get_current_user),
                                session: Session = Depends(get_session)):
    # Solo buscamos los vehículos donde el user_id coincida con el del Token
    statement = select(Vehicle).where(Vehicle.user_id == current_user.id)
    vehiculos = session.exec(statement).all()
    return vehiculos

@app.post("/productos/")
async def create_product(marca: str = Form(...),
                            nombre: str = Form(...),
                            detalles: Optional[str] = Form(None),
                            archivo_foto: UploadFile = File(None),
                            session: Session = Depends(get_session)):
    
    db_path = None
    
    product_folder = os.path.join(MEDIA_ROOT, "products")
    os.makedirs(product_folder, exist_ok=True)
        
    if archivo_foto and archivo_foto.filename:
        clean_name = archivo_foto.filename.replace(" ", "_")
        file_name = f"{marca}_{nombre}_{clean_name}"
        full_path = os.path.join(product_folder, file_name)
        
        with open(full_path, "wb") as buffer:
            shutil.copyfileobj(archivo_foto.file, buffer)
        
        db_path = f"products/{file_name}"

    new_product = Product(marca=marca, nombre=nombre, detalles=detalles, imagen=db_path)
    
    session.add(new_product)
    session.commit()
    session.refresh(new_product)
    return new_product

@app.post("/tipos-revision/", response_model=RevisionType)
async def create_revision_type(revision_type: RevisionType,
                                session: Session = Depends(get_session)):
    

    
    session.add(revision_type)
    session.commit()
    session.refresh(revision_type)
    return revision_type

@app.post("/revisiones/")
async def create_revision(revision: Revision,
                            current_user: User = Depends(get_current_user),
                            session: Session = Depends(get_session)):
    
    # Verify vehicle ownership
    vehicle = session.exec(
        select(Vehicle).where(Vehicle.matricula == revision.vehiculo_id, Vehicle.user_id == current_user.id)
    ).first()
    
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found or access denied")

    # Get revision type for km calculation
    rev_type = session.get(RevisionType, revision.tipo_revision_id)
    if not rev_type:
        raise HTTPException(status_code=404, detail="Revision type not found")

    session.add(revision)
    
    # Logic: Calculate next service reminder
    next_service_km = revision.kilometro_servicio + rev_type.cada_cuantos_Km
    
    session.commit()
    session.refresh(revision)
    
    return {
        "message": "Revision recorded successfully",
        "revision": revision,
        "reminder": f"Your next {rev_type.nombre} should be at {next_service_km} km"
    }