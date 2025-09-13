import uuid

def generar_id_transaccion():
    return str(uuid.uuid4())

def enviar_notificacion(preferencia, mensaje):
    if preferencia == "email":
        print(f"📧 Email enviado: {mensaje}")
    elif preferencia == "sms":
        print(f"📱 SMS enviado: {mensaje}")