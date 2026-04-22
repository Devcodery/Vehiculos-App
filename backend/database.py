import os
from sqlmodel import create_engine, Session, SQLModel
from dotenv import load_dotenv

load_dotenv()


# En Docker, el "host" será el nombre del servicio (db)
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL no está configurada en las variables de entorno.")

# El "engine" es el que mantiene la conexión real
engine = create_engine(DATABASE_URL, echo=True)

# Función para crear las tablas al iniciar la app
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Función para obtener una sesión (se usará en los endpoints)
def get_session():
    with Session(engine) as session:
        yield session