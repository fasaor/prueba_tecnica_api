from fastapi import APIRouter, HTTPException
from database import clientes_collection
from models import Cliente
from auth import hash_password, verify_password, create_access_token

router = APIRouter()

@router.post("/registro")
def registrar(cliente: Cliente):
    if clientes_collection.find_one({"email": cliente.email}):
        raise HTTPException(status_code=400, detail="Email ya registrado")
    cliente_dict = cliente.dict()
    cliente_dict["password"] = hash_password(cliente.password)
    clientes_collection.insert_one(cliente_dict)
    return {"mensaje": "Cliente registrado"}

@router.post("/login")
def login(email: str, password: str):
    cliente = clientes_collection.find_one({"email": email})
    if not cliente or not verify_password(password, cliente["password"]):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    token = create_access_token({"sub": cliente["email"], "rol": cliente["rol"]})
    return {"access_token": token}