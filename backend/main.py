from contextlib import asynccontextmanager
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session, select
from database import create_db_and_tables, engine
from models import User
import os
from security import (
    MEDIA_ROOT,
    ADMIN_PASSWORD,
    ADMIN_EMAIL,
    ADMIN_FULLNAME,
    ADMIN_ROLE,
    get_password_prehash,
    pwd_context
)
from routers.auth import router as auth_router
from routers.users import router as users_router
from routers.vehicles import router as vehicles_router
from routers.products import router as products_router
from routers.revision import router as revision_router
from services.alert_scheduler import start_alert_scheduler

# --- LIFESPAN ---

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- ACCIONES AL ARRANCAR (STARTUP) ---
    print("Arrancando la API y verificando tablas...")
    create_db_and_tables()
    asyncio.create_task(start_alert_scheduler())
    
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
            print("La base de datos ya contiene usuarios.")
    
    yield  # Aquí es donde la aplicación "vive" y atiende peticiones
    
    # --- ACCIONES AL CERRAR (SHUTDOWN) ---
    print("Apagando la API...")

# 2. Pasamos el lifespan a la instancia de FastAPI
app = FastAPI(
    title="AutoCare Pro API",
    lifespan=lifespan
)

os.makedirs(MEDIA_ROOT, exist_ok=True)
app.mount("/media", StaticFiles(directory=MEDIA_ROOT), name="media")

origins = [
    "http://localhost:5173", # Puerto por defecto de Vite/Vue
    "http://127.0.0.1:5173",
    "https://autocare.devcodery.duckdns.org", # Dominio de producción frontend
    "https://api.devcodery.duckdns.org",      # Dominio de producción backend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"], # Permite todas las cabeceras (incluyendo tu Token JWT)
)

# --- REGISTRO DE ROUTERS ---
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(vehicles_router)
app.include_router(products_router)
app.include_router(revision_router)

# --- ROUTES ---

@app.get("/")
async def read_root():
    return {"message": "Bienvenido a AutoCare Pro API", "status": "Ready"}