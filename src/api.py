import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.recarga import calcular_recarga

app = FastAPI(title="RecargaYa API")


class RecargaRequest(BaseModel):
    monto: int
    es_premium: bool = False


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/recarga")
def recargar_get(monto: int, es_premium: bool = False):
    resultado = calcular_recarga(monto, es_premium=es_premium)
    if resultado["rechazado"]:
        raise HTTPException(status_code=400, detail=resultado["motivo"])
    return resultado


@app.post("/recarga")
def recargar_post(body: RecargaRequest):
    resultado = calcular_recarga(body.monto, es_premium=body.es_premium)
    if resultado["rechazado"]:
        raise HTTPException(status_code=400, detail=resultado["motivo"])
    return resultado
