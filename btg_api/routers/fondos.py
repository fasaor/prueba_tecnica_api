from fastapi import APIRouter
from database import fondos_collection

router = APIRouter()

@router.get("/")
def listar_fondos():
    return list(fondos_collection.find({}, {"_id": 0}))
