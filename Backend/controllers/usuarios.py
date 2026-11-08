from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from config.database import get_session
from models.models import Usuario, Carrito
from schemas.schemas import UsuarioRegistro, UsuarioLogin, Token
from dependencias.seguridad import obtener_hash_password, verificar_password, crear_token_acceso


router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.post("/registro")
def registrar_usuario(usuario_data: UsuarioRegistro, db: Session = Depends(get_session)):
  
    usuario_existente = db.exec(select(Usuario).where(Usuario.correo == usuario_data.correo)).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="El correo ya esta registrado")

   
    password_encriptada = obtener_hash_password(usuario_data.password)

    
    nuevo_usuario = Usuario(
        nombre=usuario_data.nombre,
        correo=usuario_data.correo,
        password_hash=password_encriptada
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

   
    nuevo_carrito = Carrito(usuario_id=nuevo_usuario.id)
    db.add(nuevo_carrito)
    db.commit()

    return {"mensaje": "Usuario registrado exitosamente"}


@router.post("/login", response_model=Token)
def iniciar_sesion(usuario_data: UsuarioLogin, db: Session = Depends(get_session)):
  
    usuario = db.exec(select(Usuario).where(Usuario.correo == usuario_data.correo)).first()
    
    if not usuario or not verificar_password(usuario_data.password, usuario.password_hash):
        raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")

    token = crear_token_acceso(data={"sub": usuario.correo})
    
    return {
        "access_token": token, 
        "token_type": "bearer",
        "usuario_id": usuario.id,
        "nombre": usuario.nombre
    }

