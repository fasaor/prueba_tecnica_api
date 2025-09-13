from fastapi import APIRouter
from models import Fondo
from database import fondos_collection

router = APIRouter()

@router.get("/")
def listar_fondos():
    fondos = list(fondos_collection.find({}, {"_id": 0}))
    return fondos
