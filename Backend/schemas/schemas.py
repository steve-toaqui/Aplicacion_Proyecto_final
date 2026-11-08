from pydantic import BaseModel


class UsuarioRegistro(BaseModel):
    nombre: str
    correo: str
    password: str


class UsuarioLogin(BaseModel):
    correo: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    usuario_id: int
    nombre: str

class ItemCarrito(BaseModel):
    usuario_id: int
    producto_id: int
    cantidad: int