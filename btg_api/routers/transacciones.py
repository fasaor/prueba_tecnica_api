from fastapi import APIRouter, HTTPException
from database import clientes_collection, fondos_collection, transacciones_collection
from uuid import uuid4
from datetime import datetime

router = APIRouter()

@router.post("/suscribir")
def suscribir(cliente_email: str, fondo_nombre: str):
    cliente = clientes_collection.find_one({"email": cliente_email})
    fondo = fondos_collection.find_one({"nombre": fondo_nombre})
    if not cliente or not fondo:
        raise HTTPException(status_code=404, detail="Cliente o fondo no encontrado")
    if cliente["saldo"] < fondo["monto_minimo"]:
        raise HTTPException(status_code=400, detail=f"No tiene saldo disponible para vincularse al fondo {fondo['nombre']}")
    
    clientes_collection.update_one(
        {"email": cliente_email},
        {"$inc": {"saldo": -fondo["monto_minimo"]}}
    )
    
    transacciones_collection.insert_one({
        "_id": str(uuid4()),
        "cliente_id": cliente_email,
        "fondo_id": fondo_nombre,
        "tipo": "apertura",
        "monto": fondo["monto_minimo"],
        "fecha": datetime.utcnow(),
        "categoria": fondo["categoria"]
    })
    return {"mensaje": "Suscripción exitosa"}

@router.post("/cancelar")
def cancelar(cliente_email: str, fondo_nombre: str):
    fondo = fondos_collection.find_one({"nombre": fondo_nombre})
    cliente = clientes_collection.find_one({"email": cliente_email})
    if not cliente or not fondo:
        raise HTTPException(status_code=404, detail="Datos no encontrados")
    
    clientes_collection.update_one(
        {"email": cliente_email},
        {"$inc": {"saldo": fondo["monto_minimo"]}}
    )
    
    transacciones_collection.insert_one({
        "_id": str(uuid4()),
        "cliente_id": cliente_email,
        "fondo_id": fondo_nombre,
        "tipo": "cancelacion",
        "monto": fondo["monto_minimo"],
        "fecha": datetime.utcnow(),
        "categoria": fondo["categoria"]
    })
    return {"mensaje": "Cancelación exitosa"}

@router.get("/historial")
def historial(cliente_email: str):
    return list(transacciones_collection.find({"cliente_id": cliente_email}, {"_id": 0}))