from pydantic import BaseModel
from typing import Optional

class Cliente(BaseModel):
    nombre: str
    email: str
    password: str
    preferencia_notificacion: Optional[str]
    saldo: float
    rol: str

class Fondo(BaseModel):
    nombre: str
    monto_minimo: float
    categoria: str

class Transaccion(BaseModel):
    cliente_id: str
    fondo_id: str
    tipo: str
    monto: float
    categoria: str
    fecha: str
