import os
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["btg_db"]

clientes_collection = db["clientes"]
fondos_collection = db["fondos"]
transacciones_collection = db["transacciones"]