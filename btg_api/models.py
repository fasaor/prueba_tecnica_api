from pydantic import BaseModel
from typing import Optional

class Cliente(BaseModel):
    nombre: str
    email: str
    password: str
    preferencia_notificacion: Optional[str]
    saldo: float = 500000
    rol: str = "cliente"

class Fondo(BaseModel):
    id: int
    nombre: str
    monto_minimo: float
    categoria: str

class Transaccion(BaseModel):
    cliente_email: str
    fondo_id: int
    tipo: str  # apertura o cancelacion
    monto: float
    categoria: str
    fecha: str
    transaccion_id: str
