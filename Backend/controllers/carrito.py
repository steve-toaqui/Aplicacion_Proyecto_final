from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from config.database import get_session
from models.models import Carrito, CarritoItem, Producto, Pedido, PedidoItem
from schemas.schemas import ItemCarrito

router = APIRouter(prefix="/compras", tags=["Carrito y Pedidos"])

@router.post("/carrito/agregar")
def agregar_al_carrito(item: ItemCarrito, db: Session = Depends(get_session)):
    carrito = db.exec(select(Carrito).where(Carrito.usuario_id == item.usuario_id)).first()
    if not carrito:
        raise HTTPException(status_code=404, detail="Carrito no encontrado")

    producto = db.get(Producto, item.producto_id)
    if not producto or producto.stock < item.cantidad:
        raise HTTPException(status_code=400, detail="No hay stock suficiente para este producto")

    item_existente = db.exec(select(CarritoItem).where(
        CarritoItem.carrito_id == carrito.id,
        CarritoItem.producto_id == item.producto_id
    )).first()

    if item_existente:
        item_existente.cantidad += item.cantidad
        db.add(item_existente)
    else:
        nuevo_item = CarritoItem(carrito_id=carrito.id, producto_id=item.producto_id, cantidad=item.cantidad)
        db.add(nuevo_item)
    
    db.commit()
    return {"mensaje": "Producto agregado al carrito exitosamente"}


@router.get("/carrito/{usuario_id}")
def ver_carrito(usuario_id: int, db: Session = Depends(get_session)):
    carrito = db.exec(select(Carrito).where(Carrito.usuario_id == usuario_id)).first()
    if not carrito:
        return {"items": [], "total": 0}
    
    total = 0
    items_detalle = []
    
    for item in carrito.items:
        subtotal = item.cantidad * item.producto.precio
        total += subtotal
        items_detalle.append({
            "producto": item.producto.nombre,
            "cantidad": item.cantidad,
            "precio_unitario": item.producto.precio,
            "subtotal": subtotal
        })
    
    return {"items": items_detalle, "total": total}


@router.post("/pedidos/generar/{usuario_id}")
def generar_pedido(usuario_id: int, db: Session = Depends(get_session)):
    carrito = db.exec(select(Carrito).where(Carrito.usuario_id == usuario_id)).first()
    if not carrito or not carrito.items:
        raise HTTPException(status_code=400, detail="Tu carrito está vacío")
    
    total_pedido = sum(item.cantidad * item.producto.precio for item in carrito.items)
    
    nuevo_pedido = Pedido(usuario_id=usuario_id, total=total_pedido, estado="procesando")
    db.add(nuevo_pedido)
    db.commit()
    db.refresh(nuevo_pedido)
    
    for item in carrito.items:
        producto = db.get(Producto, item.producto_id)
        producto.stock -= item.cantidad  
        db.add(producto)
        
        pedido_item = PedidoItem(
            pedido_id=nuevo_pedido.id,
            producto_id=item.producto_id,
            cantidad=item.cantidad,
            precio_unitario=producto.precio
        )
        db.add(pedido_item)
        db.delete(item) 
        
    db.commit()
    return {"mensaje": "Pedido generado con éxito", "pedido_id": nuevo_pedido.id}