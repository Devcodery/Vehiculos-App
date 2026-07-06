import os
import shutil
from typing import Optional
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, Form
from pydantic import BaseModel
from sqlmodel import Session, select
from database import get_session
from models import Vehicle, User
from security import get_current_user, MEDIA_ROOT

router = APIRouter(prefix="/vehiculos", tags=["Vehículos"])

class VehicleUpdate(BaseModel):
    alias: Optional[str] = None
    marca: Optional[str] = None
    modelo: Optional[str] = None
    kilometraje: Optional[int] = None
    imagen: Optional[str] = None
    matricula: Optional[str] = None

@router.post("/")
async def create_vehicle(matricula: str = Form(...),
                         alias: str = Form(...),
                         marca: str = Form(...),
                         modelo: str = Form(...),
                         kilometraje: int = Form(...),
                         archivo_foto: UploadFile = File(None),
                         session: Session = Depends(get_session),
                         current_user: User = Depends(get_current_user)):
    
    user_id = current_user.user_id
    db_path = None
    
    if archivo_foto:
        user_subfolder = f"vehicles/user{current_user.user_id}"
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

@router.get("/", response_model=list[Vehicle])
async def list_vehicles(current_user: User = Depends(get_current_user),
                        session: Session = Depends(get_session)):
    statement = select(Vehicle).where(Vehicle.user_id == current_user.user_id)
    vehiculos = session.exec(statement).all()
    return vehiculos

@router.get("/{vehiculo_id}", response_model=Vehicle)
async def get_vehicle(vehiculo_id: str,
                      current_user: User = Depends(get_current_user),
                      session: Session = Depends(get_session)):
    vehicle = session.exec(
        select(Vehicle).where(Vehicle.matricula == vehiculo_id, Vehicle.user_id == current_user.user_id)
    ).first()
    
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado o acceso denegado")
    return vehicle

@router.patch("/{vehiculo_id}")
async def actualizar_vehiculo(
    vehiculo_id: str,
    alias: Optional[str] = Form(None),
    marca: Optional[str] = Form(None),
    modelo: Optional[str] = Form(None),
    kilometraje: Optional[int] = Form(None),
    archivo_foto: Optional[UploadFile] = File(None),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    coche = session.exec(
        select(Vehicle).where(Vehicle.matricula == vehiculo_id, Vehicle.user_id == current_user.user_id)
    ).first()
    
    if not coche:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado o acceso denegado")
    
    if alias is not None:
        coche.alias = alias
    if marca is not None:
        coche.marca = marca
    if modelo is not None:
        coche.modelo = modelo
    if kilometraje is not None:
        coche.kilometraje = kilometraje
        
    if archivo_foto and archivo_foto.filename:
        user_subfolder = f"vehicles/user{current_user.user_id}"
        destination_folder = os.path.join(MEDIA_ROOT, user_subfolder)
        os.makedirs(destination_folder, exist_ok=True)
        
        clean_name = archivo_foto.filename.replace(" ", "_")
        final_name = f"{coche.matricula}_{clean_name}"
        file_path = os.path.join(destination_folder, final_name)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(archivo_foto.file, buffer)
            
        coche.imagen = f"{user_subfolder}/{final_name}"
        
    session.add(coche)
    session.commit()
    session.refresh(coche)
    return coche
