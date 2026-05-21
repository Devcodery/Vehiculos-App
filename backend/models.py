from datetime import date
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

# --- 1. ENTIDAD USUARIO ---
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    email: str = Field(unique=True, index=True)
    rol: str = Field(default="usuario")
    password_hash: str

    # Relación: Un usuario tiene muchos vehículos
    vehiculos: List["Vehicle"] = Relationship(back_populates="owner")

# --- 2. ENTIDAD VEHÍCULO ---
class Vehicle(SQLModel, table=True):
    matricula: str = Field(primary_key=True, index=True)
    alias: str
    marca: str
    modelo: str
    kilometraje: int
    imagen: Optional[str] = None
    
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    
    # Relaciones
    owner: Optional[User] = Relationship(back_populates="vehiculos")
    revisiones: List["Revision"] = Relationship(back_populates="vehicle")

# --- 3. ENTIDAD PRODUCTO ---
class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    marca: str = Field(index=True)
    nombre: str
    detalles: Optional[str] = None
    imagen: Optional[str] = None # Ruta de la foto del producto
    
    revisiones: List["Revision"] = Relationship(back_populates="product")

# --- 4. ENTIDAD TIPO DE REVISIÓN ---
class RevisionType(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(unique=True)
    detalles: str
    cada_cuantos_Km: int
    cada_cuantos_Meses: int
    
    revisiones: List["Revision"] = Relationship(back_populates="revision_type")

# --- 5. ENTIDAD REVISIÓN (Relación Ternaria) ---
class Revision(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Claves foráneas (Conexión ternaria)
    vehiculo_id: str = Field(foreign_key="vehicle.matricula")
    producto_id: int = Field(foreign_key="product.id")
    tipo_revision_id: int = Field(foreign_key="revisiontype.id")
    
    # Datos específicos del servicio
    fecha: date = Field(default_factory=date.today)
    precio: Optional[float] = None
    nota: Optional[str] = None
    kilometro_servicio: int
    
    # Relaciones para acceder a los datos fácilmente
    vehicle: Vehicle = Relationship(back_populates="revisiones")
    product: Product = Relationship(back_populates="revisiones")
    revision_type: RevisionType = Relationship(back_populates="revisiones")