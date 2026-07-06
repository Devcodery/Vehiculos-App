from datetime import date, datetime, timezone
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

# --- 1. ENTIDAD USUARIO ---
class User(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    email: str = Field(unique=True, index=True)
    rol: str = Field(default="usuario")
    password_hash: str

    # Relación: Un usuario tiene muchos vehículos
    vehiculos: List["Vehicle"] = Relationship(back_populates="owner")
    my_revision_type: List["RevisionType"] = Relationship(back_populates="creator")

# --- 2. ENTIDAD VEHÍCULO ---
class Vehicle(SQLModel, table=True):
    matricula: str = Field(primary_key=True, index=True)
    alias: str
    marca: str
    modelo: str
    kilometraje: int
    imagen: Optional[str] = None
    
    user_id: Optional[int] = Field(default=None, foreign_key="user.user_id")
    
    # Relaciones
    owner: Optional[User] = Relationship(back_populates="vehiculos")
    revisiones: List["Revision"] = Relationship(back_populates="vehicle")
    
# --- 3. ENTIDAD REVISIÓN-PRODUCTOS ---
class RevisionProducts(SQLModel, table=True):
    revision_id: Optional[int] = Field(default=None, foreign_key="revision.revision_id", primary_key=True)
    producto_id: Optional[int] = Field(default=None, foreign_key="product.producto_id", primary_key=True)
    
    cantidad: int = Field(default=1)

# --- 4. ENTIDAD PRODUCTO ---
class Product(SQLModel, table=True):
    producto_id: Optional[int] = Field(default=None, primary_key=True)
    marca: str = Field(index=True)
    nombre: str
    detalles: Optional[str] = None
    imagen: Optional[str] = None # Ruta de la foto del producto
    referencia: Optional[str] = None
    categoria: Optional[str] = None
    
    revisiones: List["Revision"] = Relationship(
        back_populates="products",
        link_model=RevisionProducts
    )

# --- 5. ENTIDAD TIPO DE REVISIÓN ---
class RevisionType(SQLModel, table=True):
    tipo_revision_id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(unique=True)
    detalles: str
    cada_cuantos_Km: int
    cada_cuantos_Meses: int
    user_id: Optional[int] = Field(default=None, foreign_key="user.user_id")
    
    creator: Optional[User] = Relationship(back_populates="my_revision_type")
    revisiones: List["Revision"] = Relationship(back_populates="revision_type")

# --- 6. ENTIDAD REVISIÓN (Relación Ternaria) ---
class Revision(SQLModel, table=True):
    revision_id: Optional[int] = Field(default=None, primary_key=True)
    
    # Claves foráneas (Conexión ternaria)
    vehiculo_id: str = Field(foreign_key="vehicle.matricula")
    tipo_revision_id: int = Field(foreign_key="revisiontype.tipo_revision_id")
    
    # Datos específicos del servicio
    fecha: date = Field(default_factory=date.today)
    precio: Optional[float] = None
    nota: Optional[str] = None
    kilometro_servicio: int
    
    # Relaciones para acceder a los datos fácilmente
    vehicle: Vehicle = Relationship(back_populates="revisiones")
    revision_type: RevisionType = Relationship(back_populates="revisiones")
    
    # RELACIÓN MUCHOS A MUCHOS: Conecta esta revisión real con los productos usados
    products: List["Product"] = Relationship(
        back_populates="revisiones", 
        link_model=RevisionProducts
    )

# --- 7. ENTIDAD ALERTA DE SERVICIO (Para controlar notificaciones recurrentes) ---
class ServiceAlert(SQLModel, table=True):
    alert_id: Optional[int] = Field(default=None, primary_key=True)
    vehiculo_id: str = Field(index=True)
    tipo_revision_id: int = Field(index=True)
    estado: str  # "PRÓXIMO" o "VENCIDO"
    ultimo_envio: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))