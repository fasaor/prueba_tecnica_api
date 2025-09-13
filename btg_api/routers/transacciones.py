from fastapi import APIRouter, HTTPException
from models import Transaccion
from database import clientes_collection, fondos_collection, transacciones_collection
from utils import generar_id_transaccion, enviar_notificacion
from datetime import datetime

router = APIRouter()

@router.post("/apertura")
def suscribir_fondo(transaccion: Transaccion):
    cliente = clientes_collection.find_one({"email": transaccion.cliente_email})
    fondo = fondos_collection.find_one({"id": transaccion.fondo_id})

    if not cliente or not fondo:
        raise HTTPException(status_code=404, detail="Cliente o fondo no encontrado")

    if cliente["saldo"] < fondo["monto_minimo"]:
        raise HTTPException(
            status_code=400,
            detail=f"No tiene saldo disponible para vincularse al fondo {fondo['nombre']}"
        )

    nuevo_saldo = cliente["saldo"] - fondo["monto_minimo"]
    clientes_collection.update_one(
        {"email": cliente["email"]},
        {"$set": {"saldo": nuevo_saldo}}
    )

    transaccion.transaccion_id = generar_id_transaccion()
    transaccion.monto = fondo["monto_minimo"]
    transaccion.categoria = fondo["categoria"]
    transaccion.tipo = "apertura"
    transaccion.fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    transacciones_collection.insert_one(transaccion.dict())
    enviar_notificacion(cliente.get("preferencia_notificacion"), f"Suscripción exitosa al fondo {fondo['nombre']}")

    return {"mensaje": "Suscripción realizada", "transaccion_id": transaccion.transaccion_id}

@router.post("/cancelacion")
def cancelar_fondo(transaccion: Transaccion):
    cliente = clientes_collection.find_one({"email": transaccion.cliente_email})
    fondo = fondos_collection.find_one({"id": transaccion.fondo_id})

    if not cliente or not fondo:
        raise HTTPException(status_code=404, detail="Cliente o fondo no encontrado")

    transaccion.transaccion_id = generar_id_transaccion()
    transaccion.monto = fondo["monto_minimo"]
    transaccion.categoria = fondo["categoria"]
    transaccion.tipo = "cancelacion"
    transaccion.fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    nuevo_saldo = cliente["saldo"] + fondo["monto_minimo"]
    clientes_collection.update_one(
        {"email": cliente["email"]},
        {"$set": {"saldo": nuevo_saldo}}
    )

    transacciones_collection.insert_one(transaccion.dict())
    enviar_notificacion(cliente.get("preferencia_notificacion"), f"Cancelación exitosa del fondo {fondo['nombre']}")

    return {"mensaje": "Cancelación realizada", "transaccion_id": transaccion.transaccion_id}

@router.get("/historial/{email}")
def historial_transacciones(email: str):
    historial = list(transacciones_collection.find({"cliente_email": email}, {"_id": 0}))
    return historial
