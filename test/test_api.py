from fastapi.testclient import TestClient

from src.api import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_recarga_get_valida():
    response = client.get("/recarga?monto=10000&es_premium=false")
    assert response.status_code == 200
    assert response.json()["bono_porcentaje"] == 10
    assert response.json()["bono_datos"] == 1000


def test_recarga_get_rechazada():
    response = client.get("/recarga?monto=999&es_premium=false")
    assert response.status_code == 400
    assert "El monto debe estar entre" in response.json()["detail"]


def test_recarga_post_premium():
    response = client.post("/recarga", json={"monto": 30000, "es_premium": True})
    assert response.status_code == 200
    assert response.json()["bono_porcentaje"] == 30
    assert response.json()["bono_datos"] == 9000
