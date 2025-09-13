def test_monto_minimo():
    fondo = {"nombre": "FPV_BTG_PACTUAL_RECAUDADORA", "monto_minimo": 75000}
    cliente = {"saldo": 50000}
    assert cliente["saldo"] < fondo["monto_minimo"]

def test_transaccion_id_unico():
    from uuid import uuid4
    ids = {str(uuid4()) for _ in range(100)}
    assert len(ids) == 100