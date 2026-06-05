import pytest
from recarga import calcular_recarga
from api import app


def test_rechaza_monto_bajo():
    resultado = calcular_recarga(999)
    assert resultado["rechazado"] is True

def test_acepta_monto_minimo():
    resultado = calcular_recarga(1000)
    assert resultado["rechazado"] is False
    assert resultado["bono_porcentaje"] == 0


def test_rechaza_monto_alto():
    resultado = calcular_recarga(50001)
    assert resultado["rechazado"] is True


def test_bono_diez_por_ciento():
    resultado = calcular_recarga(10000)
    assert resultado["bono_porcentaje"] == 10
    assert resultado["bono_datos"] == 1000


def test_bono_veinticinco_por_ciento():
    resultado = calcular_recarga(30000)
    assert resultado["bono_porcentaje"] == 25
    assert resultado["bono_datos"] == 7500


def test_premium_suma_cinco_por_ciento():
    resultado = calcular_recarga(10000, es_premium=True)
    assert resultado["bono_porcentaje"] == 15
    assert resultado["bono_datos"] == 1500


def test_premium_en_tope_maximo():
    resultado = calcular_recarga(50000, es_premium=True)
    assert resultado["bono_porcentaje"] == 30
    assert resultado["bono_datos"] == 15000
