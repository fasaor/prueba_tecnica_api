from fastapi import APIRouter, HTTPException, Depends, Header
from models import Transaccion
from database import clientes_collection, fondos_collection, transacciones_collection
from utils import generar_id_transaccion, enviar_notificacion, decodificar_token
from datetime import datetime

router = APIRouter()

# 🔒 Middleware para validar token y extraer datos del usuario
def validar_token(authorization: str = Header(...)):
    try:
        token = authorization.split(" ")[1]
        datos = decodificar_token(token)
        return datos
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

# 📥 Apertura de fondo (suscripción)
@router.post("/apertura")
def suscribir_fondo(transaccion: Transaccion, usuario=Depends(validar_token)):
    if usuario["rol"] != "cliente":
        raise HTTPException(status_code=403, detail="Acceso denegado")

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

    return {
        "mensaje": "Suscripción realizada",
        "transaccion_id": transaccion.transaccion_id,
        "nuevo_saldo": nuevo_saldo
    }

# 📤 Cancelación de fondo
@router.post("/cancelacion")
def cancelar_fondo(transaccion: Transaccion, usuario=Depends(validar_token)):
    if usuario["rol"] != "cliente":
        raise HTTPException(status_code=403, detail="Acceso denegado")

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

    return {
        "mensaje": "Cancelación realizada",
        "transaccion_id": transaccion.transaccion_id,
        "nuevo_saldo": nuevo_saldo
    }

# 📜 Historial de transacciones por cliente
@router.get("/historial/{email}")
def historial_transacciones(email: str, usuario=Depends(validar_token)):
    if usuario["rol"] not in ["cliente", "admin"]:
        raise HTTPException(status_code=403, detail="Acceso denegado")

    if usuario["rol"] == "cliente" and usuario["sub"] != email:
        raise HTTPException(status_code=403, detail="No puede consultar el historial de otro cliente")

    historial = list(transacciones_collection.find({"cliente_email": email}, {"_id": 0}))
    return {"transacciones": historial}
