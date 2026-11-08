
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.database import create_db_and_tables
from controllers import usuarios, productos, carrito
import models.models 

from controllers import usuarios, productos 

app = FastAPI(title="API Tienda Gamer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    print("Creando las tablas en la base de datos...")
    create_db_and_tables()

app.include_router(usuarios.router)
app.include_router(productos.router) 
app.include_router(carrito.router)

@app.get("/")
def ruta_principal():
    return {"mensaje": "Servidor de Tienda Gamer funcionando"}