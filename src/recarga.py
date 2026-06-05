MONTO_MINIMO = 1000
MONTO_MAXIMO = 50000


def calcular_recarga(monto, es_premium=False):
    if monto < MONTO_MINIMO or monto > MONTO_MAXIMO:
        return {
            "rechazado": True,
            "motivo": "El monto debe estar entre $1.000 y $50.000",
        }

    if monto >= 30000:
        bono = 0.25
    elif monto >= 10000:
        bono = 0.10
    else:
        bono = 0.0

    if es_premium:
        bono += 0.05

    return {
        "rechazado": False,
        "monto": monto,
        "bono_porcentaje": round(bono * 100),
        "bono_datos": round(monto * bono),
        "es_premium": es_premium,
    }