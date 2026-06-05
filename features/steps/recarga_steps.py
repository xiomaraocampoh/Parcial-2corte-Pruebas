from behave import given, then, when, use_step_matcher

from src.recarga import calcular_recarga

use_step_matcher("parse")


@given("un cliente normal")
def cliente_normal(context):
    context.es_premium = False


@given("un cliente premium")
def cliente_premium(context):
    context.es_premium = True


@given("un cliente quiere recargar {monto:d} pesos")
def cliente_quiere_recargar(context, monto):
    context.monto = monto


@when("se calcula la recarga")
def calcular(context):
    context.resultado = calcular_recarga(context.monto, es_premium=context.es_premium)


@then("la recarga es rechazada")
def recarga_rechazada(context):
    assert context.resultado["rechazado"] is True


@then("la recarga es aceptada")
def recarga_aceptada(context):
    assert context.resultado["rechazado"] is False


@then("el bono de datos es del {porcentaje:d} por ciento")
def verificar_bono(context, porcentaje):
    assert context.resultado["bono_porcentaje"] == porcentaje


@then("el bono en pesos es {valor:d}")
def verificar_bono_pesos(context, valor):
    assert context.resultado["bono_datos"] == valor
