import os
import shutil
from typing import Optional
from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException
from sqlmodel import Session, select
from database import get_session
from models import Product, User
from security import get_current_user, MEDIA_ROOT

router = APIRouter(prefix="/productos", tags=["Productos"])

@router.post("/")
async def create_product(marca: str = Form(...),
                         nombre: str = Form(...),
                         detalles: Optional[str] = Form(None),
                         referencia: Optional[str] = Form(None),
                         categoria: Optional[str] = Form(None),
                         archivo_foto: Optional[UploadFile] = File(None),
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

    new_product = Product(
        marca=marca, 
        nombre=nombre, 
        detalles=detalles, 
        referencia=referencia, 
        categoria=categoria, 
        imagen=db_path
    )
    
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

@router.patch("/{producto_id}")
async def update_product(producto_id: int,
                         marca: Optional[str] = Form(None),
                         nombre: Optional[str] = Form(None),
                         detalles: Optional[str] = Form(None),
                         referencia: Optional[str] = Form(None),
                         categoria: Optional[str] = Form(None),
                         archivo_foto: Optional[UploadFile] = File(None),
                         session: Session = Depends(get_session)):
    product = session.get(Product, producto_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
        
    if marca is not None:
        product.marca = marca
    if nombre is not None:
        product.nombre = nombre
    if detalles is not None:
        product.detalles = detalles
    if referencia is not None:
        product.referencia = referencia
    if categoria is not None:
        product.categoria = categoria
        
    if archivo_foto and archivo_foto.filename:
        product_folder = os.path.join(MEDIA_ROOT, "products")
        os.makedirs(product_folder, exist_ok=True)
        clean_name = archivo_foto.filename.replace(" ", "_")
        file_name = f"{product.marca}_{product.nombre}_{clean_name}"
        full_path = os.path.join(product_folder, file_name)
        
        with open(full_path, "wb") as buffer:
            shutil.copyfileobj(archivo_foto.file, buffer)
            
        product.imagen = f"products/{file_name}"
        
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

@router.delete("/{producto_id}")
async def delete_product(producto_id: int, session: Session = Depends(get_session)):
    product = session.get(Product, producto_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    session.delete(product)
    session.commit()
    return {"mensaje": "Producto eliminado con éxito"}
