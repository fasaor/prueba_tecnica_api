from fastapi import APIRouter
from models import Cliente
from database import clientes_collection

router = APIRouter()

@router.post("/")
def crear_cliente(cliente: Cliente):
    clientes_collection.insert_one(cliente.dict())
    return {"mensaje": "Cliente creado exitosamente"}
