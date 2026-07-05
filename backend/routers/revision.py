from typing import Optional, List
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models import RevisionType, Revision, RevisionProducts, Vehicle, User
from security import get_current_user

router = APIRouter(prefix="/revisiones", tags=["Revisiones"])

# --- ESQUEMAS PARA RECIBIR DATOS DESDE VUE ---

class ProductoUtilizadoIn(BaseModel):
    producto_id: int
    cantidad: int

class RevisionCreateIn(BaseModel):
    vehiculo_id: str # Es str porque tu clave primaria es la matrícula
    tipo_revision_id: int
    kilometro_servicio: int
    precio: Optional[float] = None
    nota: Optional[str] = None
    productos_utilizados: List[ProductoUtilizadoIn] = []

@router.post("/tipos/", response_model=RevisionType)
async def create_revision_type(revision_type: RevisionType,
                               session: Session = Depends(get_session)):
    session.add(revision_type)
    session.commit()
    session.refresh(revision_type)
    return revision_type

@router.post("/")
async def create_revision(revision_data: RevisionCreateIn,
                          current_user: User = Depends(get_current_user),
                          session: Session = Depends(get_session)):
    
    # 1. Verificamos que el coche es de este usuario
    vehicle = session.exec(
        select(Vehicle).where(Vehicle.matricula == revision_data.vehiculo_id, Vehicle.user_id == current_user.user_id)
    ).first()
    
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado o acceso denegado")

    # 2. Buscamos el tipo de revisión para calcular el próximo servicio
    rev_type = session.get(RevisionType, revision_data.tipo_revision_id)
    if not rev_type:
        raise HTTPException(status_code=404, detail="Tipo de revisión no encontrado")

    # 3. CREAMOS LA REVISIÓN REAL
    nueva_revision = Revision(
        vehiculo_id=revision_data.vehiculo_id,
        tipo_revision_id=revision_data.tipo_revision_id,
        kilometro_servicio=revision_data.kilometro_servicio,
        precio=revision_data.precio,
        nota=revision_data.nota
    )
    
    session.add(nueva_revision)
    session.commit()
    session.refresh(nueva_revision) # Aquí Postgres le asigna su revision_id
    
    # 4. AÑADIMOS LOS PRODUCTOS A LA TABLA INTERMEDIA
    if revision_data.productos_utilizados:
        for prod in revision_data.productos_utilizados:
            # Creamos la fila que une la revisión con el producto y su cantidad
            link = RevisionProducts(
                revision_id=nueva_revision.revision_id,
                producto_id=prod.producto_id,
                cantidad=prod.cantidad
            )
            session.add(link)
        
        # Guardamos todos los productos vinculados
        session.commit()
    
    # Lógica: Calcular próximo servicio
    next_service_km = nueva_revision.kilometro_servicio + rev_type.cada_cuantos_Km
    
    return {
        "message": "Revisión registrada con éxito",
        "revision_id": nueva_revision.revision_id,
        "reminder": f"Tu próximo/a {rev_type.nombre} debería ser a los {next_service_km} km"
    }

@router.get("/tipos/mis/", response_model=list[RevisionType])
async def list_revision_type(current_user: User = Depends(get_current_user),
                             session: Session = Depends(get_session)):
    statement = select(RevisionType).where(RevisionType.tipo_revision_id == current_user.user_id)
    
    revision_type = session.exec(statement).all()
    return revision_type
