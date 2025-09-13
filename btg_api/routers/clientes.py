from fastapi import APIRouter, HTTPException
from models import Cliente
from database import clientes_collection
from utils import hash_password, verify_password, crear_token

router = APIRouter()

@router.post("/registro")
def registrar_cliente(cliente: Cliente):
    if clientes_collection.find_one({"email": cliente.email}):
        raise HTTPException(status_code=400, detail="El cliente ya existe")
    cliente.password = hash_password(cliente.password)
    clientes_collection.insert_one(cliente.dict())
    return {"mensaje": "Cliente registrado"}

@router.post("/login")
def login(email: str, password: str):
    cliente = clientes_collection.find_one({"email": email})
    if not cliente or not verify_password(password, cliente["password"]):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    token = crear_token(email, cliente["rol"])
    return {"access_token": token}
