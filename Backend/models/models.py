from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional

class Categoria(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    descripcion: str
    
    productos: List["Producto"] = Relationship(back_populates="categoria")


class Producto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    descripcion: str
    precio: float
    stock: int
    imagen: str  
    
    categoria_id: Optional[int] = Field(default=None, foreign_key="categoria.id")
    categoria: Optional[Categoria] = Relationship(back_populates="productos")


class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    correo: str = Field(unique=True) 
    password_hash: str 
    
    carrito: Optional["Carrito"] = Relationship(back_populates="usuario")
    pedidos: List["Pedido"] = Relationship(back_populates="usuario")


class Carrito(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id")
    
    usuario: Optional[Usuario] = Relationship(back_populates="carrito")
    items: List["CarritoItem"] = Relationship(back_populates="carrito")

class CarritoItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cantidad: int
    
    carrito_id: int = Field(foreign_key="carrito.id")
    producto_id: int = Field(foreign_key="producto.id")
    
    carrito: Optional[Carrito] = Relationship(back_populates="items")
    producto: Optional[Producto] = Relationship()


class Pedido(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    estado: str = Field(default="pendiente") # pendiente, procesando, enviado, entregado
    total: float
    
    usuario_id: int = Field(foreign_key="usuario.id")
    usuario: Optional[Usuario] = Relationship(back_populates="pedidos")
    items: List["PedidoItem"] = Relationship(back_populates="pedido")

class PedidoItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cantidad: int
    precio_unitario: float
    
    pedido_id: int = Field(foreign_key="pedido.id")
    producto_id: int = Field(foreign_key="producto.id")
    
    pedido: Optional[Pedido] = Relationship(back_populates="items")
    producto: Optional[Producto] = Relationship()