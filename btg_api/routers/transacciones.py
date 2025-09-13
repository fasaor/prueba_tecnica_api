from fastapi import APIRouter
from models import Transaccion
from database import transacciones_collection

router = APIRouter()

@router.post("/")
def registrar_transaccion(transaccion: Transaccion):
    transacciones_collection.insert_one(transaccion.dict())
    return {"mensaje": "Transacción registrada"}
