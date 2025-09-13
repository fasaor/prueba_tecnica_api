from pydantic import BaseModel, EmailStr
from typing import Optional, List

# 🧍 Modelo de Cliente
class Cliente(BaseModel):
    nombre: str
    email: EmailStr
    password: str
    preferencia_notificacion: str  # email o sms
    saldo: Optional[int] = 500000  # Saldo inicial por regla de negocio
    rol: Optional[str] = "cliente"  # Rol por defecto

# 🏦 Modelo de Fondo
class Fondo(BaseModel):
    nombre: str
    monto_minimo: int
    categoria: str  # "FPV" o "FIC"

# 🔄 Modelo de Transacción
class Transaccion(BaseModel):
    cliente_id: str
    fondo_id: str
    tipo: str  # "apertura" o "cancelacion"
    monto: int
    categoria: str
    fecha: Optional[str] = None  # Se asigna automáticamente en el backend

# 📋 Fondos iniciales
fondos_iniciales: List[dict] = [
    {
        "nombre": "FPV_BTG_PACTUAL_RECAUDADORA",
        "monto_minimo": 75000,
        "categoria": "FPV"
    },
    {
        "nombre": "FPV_BTG_PACTUAL_ECOPETROL",
        "monto_minimo": 125000,
        "categoria": "FPV"
    },
    {
        "nombre": "DEUDAPRIVADA",
        "monto_minimo": 50000,
        "categoria": "FIC"
    },
    {
        "nombre": "FDO-ACCIONES",
        "monto_minimo": 250000,
        "categoria": "FIC"
    },
    {
        "nombre": "FPV_BTG_PACTUAL_DINAMICA",
        "monto_minimo": 100000,
        "categoria": "FPV"
    }
]
