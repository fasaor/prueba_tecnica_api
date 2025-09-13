import bcrypt
from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "clave_secreta_super_segura"
ALGORITHM = "HS256"

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def crear_token(email: str, rol: str) -> str:
    payload = {
        "sub": email,
        "rol": rol,
        "exp": datetime.utcnow() + timedelta(hours=2)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decodificar_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
