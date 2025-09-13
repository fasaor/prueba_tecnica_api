from fastapi import FastAPI
from routers import clientes, fondos, transacciones

app = FastAPI()

app.include_router(clientes.router, prefix="/clientes", tags=["Clientes"])
app.include_router(fondos.router, prefix="/fondos", tags=["Fondos"])
app.include_router(transacciones.router, prefix="/transacciones", tags=["Transacciones"])
