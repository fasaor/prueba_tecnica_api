from pymongo import MongoClient
import certifi
import os

client = MongoClient(os.getenv("MONGO_URI"), tlsCAFile=certifi.where())
db = client["btg_db"]

clientes_collection = db["clientes"]
fondos_collection = db["fondos"]
transacciones_collection = db["transacciones"]
