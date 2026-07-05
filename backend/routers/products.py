import os
import shutil
from typing import Optional
from fastapi import APIRouter, Depends, File, UploadFile, Form
from sqlmodel import Session, select
from database import get_session
from models import Product, User
from security import get_current_user, MEDIA_ROOT

router = APIRouter(prefix="/productos", tags=["Productos"])

@router.post("/")
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

@router.get("/", response_model=list[Product])
async def list_products(current_user: User = Depends(get_current_user),
                        session: Session = Depends(get_session)):
    statement = select(Product)
    products = session.exec(statement).all()
    return products
