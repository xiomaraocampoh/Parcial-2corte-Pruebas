Feature: Calculo de recargas moviles RecargaYa
  Como gerente de RecargaYa
  Quiero calcular bonos de datos segun el monto recargado
  Para ofrecer beneficios claros a los clientes

  Scenario: Monto por debajo del minimo permitido
    Given un cliente normal
    And un cliente quiere recargar 999 pesos
    When se calcula la recarga
    Then la recarga es rechazada

  Scenario: Recarga minima valida sin bono
    Given un cliente normal
    And un cliente quiere recargar 1000 pesos
    When se calcula la recarga
    Then la recarga es aceptada
    And el bono de datos es del 0 por ciento

  Scenario: Recarga con bono del diez por ciento
    Given un cliente normal
    And un cliente quiere recargar 10000 pesos
    When se calcula la recarga
    Then la recarga es aceptada
    And el bono de datos es del 10 por ciento
    And el bono en pesos es 1000

  Scenario: Recarga premium con bono adicional
    Given un cliente premium
    And un cliente quiere recargar 30000 pesos
    When se calcula la recarga
    Then la recarga es aceptada
    And el bono de datos es del 30 por ciento
    And el bono en pesos es 9000

  Scenario Outline: Validacion de montos en los limites del rango
    Given un cliente normal
    And un cliente quiere recargar <monto> pesos
    When se calcula la recarga
    Then <resultado>

    Examples:
      | monto | resultado            |
      | 999   | la recarga es rechazada |
      | 1000  | la recarga es aceptada  |
      | 50000 | la recarga es aceptada  |
      | 50001 | la recarga es rechazada |
