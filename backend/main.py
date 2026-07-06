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


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Arrancando la API y verificando tablas...")
    create_db_and_tables()
    asyncio.create_task(start_alert_scheduler())
    
    with Session(engine) as session:
        primer_usuario = session.exec(select(User)).first()
        
        if not primer_usuario:
            print("Base de datos vacía. Creando Administrador por defecto...")
            
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
    
    yield
    
    print("Apagando la API...")

app = FastAPI(
    title="AutoCare Pro API",
    lifespan=lifespan
)

os.makedirs(MEDIA_ROOT, exist_ok=True)
app.mount("/media", StaticFiles(directory=MEDIA_ROOT), name="media")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://autocare.devcodery.duckdns.org",
    "https://api-autocare.devcodery.duckdns.org",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(vehicles_router)
app.include_router(products_router)
app.include_router(revision_router)


@app.get("/")
async def read_root():
    return {"message": "Bienvenido a AutoCare Pro API", "status": "Ready"}