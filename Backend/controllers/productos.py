from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from sqlalchemy.sql.expression import func 
from config.database import get_session
from models.models import Categoria, Producto

router = APIRouter(prefix="/productos", tags=["Productos y Categorías"])

@router.post("/categorias")
def crear_categoria(categoria: Categoria, db: Session = Depends(get_session)):
    db.add(categoria)
    db.commit()
    db.refresh(categoria)
    return {"mensaje": "Categoria creada exitosamente", "categoria": categoria}

@router.get("/categorias")
def obtener_categorias(db: Session = Depends(get_session)):
    return db.exec(select(Categoria)).all()


@router.post("/")
def crear_producto(producto: Producto, db: Session = Depends(get_session)):
    db.add(producto)
    db.commit()
    db.refresh(producto)
    return {"mensaje": "Producto creado exitosamente", "producto": producto}

@router.get("/")
def obtener_todos_los_productos(db: Session = Depends(get_session)):
    return db.exec(select(Producto)).all()

@router.get("/aleatorios")
def obtener_productos_aleatorios(limite: int = 4, db: Session = Depends(get_session)):
    productos = db.exec(select(Producto).order_by(func.random()).limit(limite)).all()
    return productos

@router.get("/{producto_id}")
def obtener_detalle_producto(producto_id: int, db: Session = Depends(get_session)):
    producto = db.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto