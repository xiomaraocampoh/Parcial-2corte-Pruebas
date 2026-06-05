# pasos parciales (solo mío, para repasar)

> apuntes míos antes del parcial. lo escribí yo para entenderlo paso a paso.
> si algo no cuadra, vuelvo a leer esto con el proyecto abierto hasta que de eeee

---

## 0. antes de tocar código — qué necesito tener

1. pc encendida, obvio jaja
2. **cursor** abierto (o vscode, da igual)
3. **git** instalado (para commits y github)
4. **python** instalado ( 3.14)
5. **uv** instalado → es como el "instalador de cosas (paquetes dependencias)" de python. sin uv toca pelear con pip a mano y no gracias

instalar uv (ya esta ):
- voy a https://docs.astral.sh/uv/getting-started/installation/
- en windows suele ser un comando en powershell, lo copio y listo

---

## 1. crear el proyecto desde CERO (primera vez)

### 1.1 crear la carpeta

```powershell
mkdir D:\parqueadero
cd D:\parqueadero
```

o desde cursor: file → open folder → creo carpeta parqueadero

### 1.2 inicializar proyecto con uv

```powershell
uv init
```

esto crea archivos base:
- `pyproject.toml` → lista de dependencias y config del proyecto
- `main.py` → archivo suelto (nosotros casi no lo usamos)
- `.python-version` → qué versión de python usa

### 1.3 crear la estructura de carpetas A MANO

click derecho en el explorador de archivos de cursor → new folder:

```
parqueadero/
├── src/              ← aquí va el código "de verdad" (la lógica)
├── test/             ← aquí van las pruebas unitarias (pytest)
├── features/         ← aquí va el BDD (gherkin + steps)
│   └── steps/        ← OBLIGATORIO para behave, si no existe → error
└── .github/
    └── workflows/    ← aquí va el pipeline de github actions
```

**por qué así:**
- `src/` = código de producción
- `test/` = pruebas que corren con pytest
- `features/` = pruebas en lenguaje humano (behave/gherkin)

### 1.4 agregar dependencias según vayamos necesitando

en `pyproject.toml` van las librerías. nosotros terminamos con:

| librería | para qué |
|----------|----------|
| pytest | tests unitarios (TDD) |
| behave | tests BDD (gherkin) |
| flask + waitress | API web para locust |
| locust | pruebas de rendimiento / carga |
| bandit | seguridad básica |

instalar todo de una vez:
```powershell
uv add pytest behave flask waitress locust bandit
```

o si ya están en pyproject.toml:
```powershell
uv sync
```

`uv sync` = "lee pyproject.toml e instala lo que falte"

---

## 2. TDD — la parte que más me confundía al principio

TDD = **Test Driven Development** = primero la prueba, después el código.

hay 3 fases que el profe quiere ver en los **commits**:

| fase | color | qué hago | mensaje commit ejemplo |
|------|-------|----------|------------------------|
| RED | rojo | escribo test que FALLA | `test: prueba roja de los 30 minutos gratis` |
| GREEN | verde | escribo código mínimo para que pase | `feat: implementar calcular_tarifa` |
| REFACTOR | azul/refactor | limpio sin romper tests | `refactor: simplificar condicion VIP` |

---

## 3. RED — escribir la prueba ANTES de la función

### 3.1 cómo se define una función en python (repaso rápido)

en python una función se ve así:

```python
def nombre_de_la_funcion(parametro1, parametro2=False):
    # cuerpo: lo que hace la función
    return algo
```

partes importantes:
- **`def`** → palabra reservada. SIEMPRE va al inicio. significa "defino una función"
- **`nombre_de_la_funcion`** → cómo la llamo después. en python se usa snake_case (minúsculas_con_guion_bajo)
- **`(parametro1, parametro2=False)`** → lo que recibe. el `=False` es valor por defecto (opcional)
- **`:`** → dos puntos al final de la línea del def. obligatorio
- indentación (tab o 4 espacios) → todo lo de adentro pertenece a la función
- **`return`** → devuelve un valor. si no hay return, devuelve None

operadores básicos que usamos en el parcial:
- `<=` menor o igual
- `>` mayor que
- `==` igual a (comparar, NO es asignar)
- `=` asignar valor a variable
- `*` multiplicar
- `/` dividir

### 3.2 cómo se define un TEST en pytest

un test también es una función, pero con reglas:

```python
def test_algo_descriptivo():
    assert resultado == valor_esperado
```

- el nombre **DEBE** empezar con `test_` → pytest busca funciones así
- **`assert`** → palabra reservada. dice "esto TIENE que ser verdad, si no → falla la prueba"
- si assert falla → pytest muestra ROJO (FAILED)
- si assert pasa → VERDE (PASSED)

### 3.3 ejemplo RED real de nuestro proyecto

**paso 1:** creo `test/test_cobro.py` (el archivo puede no existir aún el código fuente)

```python
from src.cobro import calcular_tarifa   # importo la función (AÚN NO EXISTE → error)

def test_gratis_30_minutos():
    assert calcular_tarifa(30) == 0
```

**qué significa cada línea:**
- `from src.cobro import calcular_tarifa` → "de la carpeta src, archivo cobro.py, trae la función calcular_tarifa"
- `calcular_tarifa(30)` → llamo la función con 30 minutos
- `== 0` → espero que devuelva cero pesos (regla: 30 min gratis)

**paso 2:** corro la prueba y DEBE fallar (eso es RED, está bien que falle)

```powershell
cd D:\parqueadero
uv run python -m pytest test/ -v
```

> ojo: en windows a veces `uv run pytest` da error raro. uso `uv run python -m pytest test/ -v`

**qué veo cuando está en rojo:**
```
FAILED test/test_cobro.py - ModuleNotFoundError: No module named 'src.cobro'
```
o
```
FAILED - assert None == 0
```

**eso está BIEN en fase red.** significa "todavía no hay código, la prueba reclama"

**paso 3:** hago commit del test rojo
```powershell
git add test/test_cobro.py
git commit -m "test: prueba roja de los 30 minutos gratis"
```

---

## 4. GREEN — escribir el código mínimo para que pase

### 4.1 creo el archivo de la función

`src/cobro.py`:

```python
def calcular_tarifa(minutos, es_vip=False):
    if minutos <= 30:
        return 0
    return 0   # al principio hasta que agregue más reglas
```

**estructura:**
- recibe `minutos` (número entero)
- recibe `es_vip` (True/False, por defecto False)
- devuelve un número (el cobro en pesos)

### 4.2 vuelvo a correr pytest

```powershell
uv run python -m pytest test/ -v
```

**ahora debo ver:**
```
test_gratis_30_minutos PASSED
```

**commit green:**
```powershell
git add src/cobro.py
git commit -m "feat: implementar calcular_tarifa con 30 min gratis"
```

### 4.3 voy agregando reglas de a una (siempre red-green)

| orden | test nuevo (red) | código (green) |
|-------|------------------|----------------|
| 1 | 30 min → $0 | `if minutos <= 30: return 0` |
| 2 | 31 min → $500 | `horas = math.ceil(minutos/60); tarifa = horas * 500` |
| 3 | 1440 min → $12000 | `if tarifa > 12000: return 12000` |
| 4 | 1440 min VIP → $9600 | `if es_vip: tarifa = tarifa * 0.80` |

**import math** → porque usamos `math.ceil()` que redondea hacia arriba.
ejemplo: 31 minutos / 60 = 0.516... → ceil = 1 hora → $500

**orden VIP vs tope:** primero descuento VIP, DESPUÉS tope de $12000. el profe puede preguntar eso.

### 4.4 todos nuestros tests unitarios (para memorizar)

```python
from src.cobro import calcular_tarifa

def test_gratis_30_minutos():
    assert calcular_tarifa(30) == 0

def test_fraccion_hora():
    assert calcular_tarifa(31) == 500
    assert calcular_tarifa(60) == 500

def test_tope_maximo():
    assert calcular_tarifa(1440) == 12000

def test_descuento_vip():
    assert calcular_tarifa(1440, es_vip=True) == 9600
```

correr todos:
```powershell
uv run python -m pytest test/ -v
```
espero: **4 passed**

---

## 5. tabla de casos (partición de equivalencia + valores límite)

esto es aparte de pytest pero el profe la pide en el README.

**partición de equivalencia** = agrupar entradas que se comportan igual

**valores límite** = probar justo en el borde del grupo

### regla "30 min gratis"

| grupo | rango | caso límite | resultado |
|-------|-------|-------------|-----------|
| gratis | 0 a 30 | **30** (último gratis) | $0 |
| cobro | 31 en adelante | **31** (primer cobro) | $500 |

### regla "tope diario"

| grupo | caso | resultado |
|-------|------|-----------|
| normal | 120 min | $1000 |
| tope 24h | **1440** min | $12000 |
| VIP tope | **1440** min VIP | $9600 |

---

## 6. BDD — behave + gherkin (la que menos entendía)

### 6.1 qué es esto en palabras simples

- **pytest** = pruebas para programadores (`assert calcular_tarifa(30) == 0`)
- **BDD** = pruebas que un **gerente** puede leer sin saber python

el gerente lee un archivo `.feature` escrito en **Gherkin** (casi español).
python no entiende gherkin solo → necesitamos **steps** que traduzcan cada frase.

### 6.2 estructura de carpetas BDD (importantísimo)

```
features/
├── parqueadero.feature    ← el "cuento" en gherkin
├── environment.py         ← config antes/después de escenarios
└── steps/
    └── cobro_steps.py     ← traduce gherkin a python
```

**si falta `features/steps/` → behave dice:**
`ConfigError: No steps directory in '...\features'`

### 6.3 qué es el archivo `.feature` (gherkin)

extensión: `.feature`
no es python. es un mini-lenguaje con palabras clave:

| palabra | significado | cuándo la uso |
|---------|-------------|---------------|
| **Feature:** | título del módulo / funcionalidad | una vez al inicio |
| **Scenario:** | un caso concreto | uno por situación |
| **Given** | situación inicial ("dado que...") | preparar el contexto |
| **When** | acción ("cuando...") | lo que pasa |
| **Then** | resultado esperado ("entonces...") | qué debe pasar |

ejemplo nuestro:

```gherkin
Feature: Cobro del parqueadero ParkingUV

  Scenario: Cliente sale dentro del tiempo gratis
    Given un cliente aparca
    When han pasado 30 minutos
    Then el cobro debe ser 0 pesos
```

**cómo lo lee el gerente:**
"un cliente aparca, pasan 30 minutos, debe cobrar 0 pesos" → suena a regla de negocio, no a código.

### 6.4 qué es `environment.py` y para qué sirve

archivo: `features/environment.py`

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
```

**en criollo:** behave corre desde la carpeta `features/`, y python a veces no encuentra `src/`. environment.py le dice a python: "oye, también busca en la carpeta padre del proyecto".

**sin environment.py** → al importar `from src.cobro import calcular_tarifa` en los steps puede fallar.

no es obligatorio en todos los proyectos, pero en el nuestro sí lo necesitamos.

behave también usa environment.py para hooks opcionales:
- `before_all` → antes de todos los escenarios
- `before_scenario` → antes de cada uno
- `after_scenario` → después

nosotros solo usamos el arreglo de path. suficiente.

### 6.5 qué son los STEPS y cómo se crean

archivo: `features/steps/cobro_steps.py`

cada frase del `.feature` se conecta a una función python con un **decorador**:

| decorador | conecta con línea |
|-----------|-------------------|
| `@given("texto exacto")` | Given ... |
| `@when("texto exacto")` | When ... |
| `@then("texto exacto")` | Then ... |

**regla de oro:** el texto entre comillas debe coincidir EXACTO con el .feature (mayúsculas, tildes, todo).

nuestro código de steps:

```python
from behave import given, then, when
from src.cobro import calcular_tarifa


@given("un cliente aparca")
def cliente_aparca(context):
    context.es_vip = False


@given("un cliente VIP aparca")
def cliente_vip_aparca(context):
    context.es_vip = True


@when("han pasado {minutos:d} minutos")
def han_pasado_minutos(context, minutos):
    context.minutos = minutos


@then("el cobro debe ser {monto:d} pesos")
def verificar_cobro(context, monto):
    resultado = calcular_tarifa(context.minutos, es_vip=context.es_vip)
    assert resultado == monto
```

### 6.6 qué es `context` (otra duda que tenía)

`context` es una **mochila** que behave pasa a cada step.

- en Given guardo datos: `context.es_vip = False`
- en When guardo más: `context.minutos = 30`
- en Then uso todo: `calcular_tarifa(context.minutos, es_vip=context.es_vip)`

los steps se hablan a través de `context` porque cada step es una función separada.

### 6.7 parámetros en steps `{minutos:d}`

`{minutos:d}` = behave captura un número de la frase y lo pasa como variable `minutos`.

- `{minutos:d}` → entero (d = digit)
- `{monto:d}` → entero

"As han pasado **31** minutos" → minutos = 31 automáticamente.

### 6.8 correr BDD

```powershell
uv run behave
```

espero:
```
5 scenarios passed, 0 failed
15 steps passed, 0 failed
```

cada scenario tiene 3 steps (Given, When, Then) → 5 × 3 = 15 steps.

### 6.9 resumen mental BDD

```
.feature (gerente lee)  →  steps (programador traduce)  →  calcular_tarifa (código real)
```

---

## 7. Locust — pruebas de rendimiento (no confundir con gherkin)

**gherkin** = archivo `.feature` para behave
**locust** = simula muchos usuarios pegándole a la API al mismo tiempo

### 7.1 por qué necesitamos API

locust no llama funciones python directo (bueno, puede, pero el parcial pide HTTP concurrente).
por eso creamos `src/api.py` con flask + waitress.

endpoints:
- `GET /health` → "¿estás vivo?"
- `GET /calcular?minutos=31&vip=false` → devuelve JSON con la tarifa

### 7.2 correr locust (2 terminales)

terminal 1:
```powershell
uv run python src/api.py
```

terminal 2:
```powershell
uv run locust -f locustfile.py --headless -u 20 -r 5 -t 15s --host http://127.0.0.1:8000
```

parámetros:
- `-u 20` → 20 usuarios ficticios
- `-r 5` → suben de a 5 por segundo
- `-t 15s` → dura 15 segundos
- `--headless` → sin ventana gráfica
- `--host` → dónde está la API

### 7.3 qué es P95

**P95** = el 95% de las respuestas fueron más rápidas que X milisegundos.

el parcial pide **P95 < 300ms**.

al final locust imprime algo como:
```
OK: P95=18ms dentro del limite de 300ms
```

**truco windows:** usar `127.0.0.1` NO `localhost`. y no dejar dos servidores en puerto 8000.

---

## 8. seguridad — bandit

```powershell
uv run bandit -r src/ -ll
```

- `-r src/` → revisa carpeta src
- `-ll` → solo reporta cosas medias/graves

espero: `No issues identified.`

nosotros tuvimos un warning por `host="0.0.0.0"` → lo cambiamos a `127.0.0.1`.

---

## 9. pipeline de GitHub Actions — qué es y qué significa cada parte

**pipeline** = robot en la nube que corre mis pruebas cada vez que hago push.

archivo: `.github/workflows/ci.yml`

### 9.1 qué debo ver en github cuando funciona

1. voy a mi repo en github.com
2. pestaña **Actions**
3. veo una fila verde con check con el nombre del workflow "CI"
4. click → veo los jobs:
   - **tests** (ok) (pytest + behave + bandit)
   - **performance** (ok) (solo en rama master/main, locust)

si algo falla → círculo rojo, click y leo en qué step murió.

### 9.2 explicación línea por línea de nuestro pipeline

```yaml
name: CI
```
nombre que aparece en la pestaña Actions

```yaml
on:
  push:
    branches: [master, main]
  pull_request:
```
**cuándo se dispara:** cada push a master/main, y también en pull requests

```yaml
jobs:
  tests:
    runs-on: ubuntu-latest
```
**job tests** corre en un servidor linux limpio de github (no mi pc)

```yaml
    steps:
      - uses: actions/checkout@v4
```
**checkout** = descarga mi código al servidor

```yaml
      - uses: astral-sh/setup-uv@v5
```
instala **uv** en el servidor

```yaml
      - run: uv sync
```
instala dependencias del pyproject.toml

```yaml
      - run: uv run python -m pytest test/ -v
      - run: uv run behave
      - run: uv run bandit -r src/ -ll
```
corre las 3 pruebas "ligeras" en CADA push

```yaml
  performance:
    if: github.ref == 'refs/heads/master' || github.ref == 'refs/heads/main'
```
**job performance** SOLO corre en rama principal (master o main), no en ramas de experimento

```yaml
      - run: uv run python src/api.py &
```
levanta la API en background (`&`)

```yaml
      - run: |
          for i in $(seq 1 30); do
            curl -sf http://127.0.0.1:8000/health && exit 0
            sleep 1
          done
```
espera hasta 30 segundos a que la API responda

```yaml
      - run: uv run locust -f locustfile.py --headless ...
```
corre locust y verifica P95

---

## 10. git y github — commits que el profe quiere ver

mínimo **10 commits** que muestren el proceso.

```powershell
git log --oneline
```

nuestro historial:
```
refactor: simplificar condicion VIP...
docs: README completo...
ci: pipeline GitHub Actions...
feat: API de cobro con Locust...
test: escenarios BDD en Gherkin...
...
test: prueba roja de los 30 minutos gratis   ← el primero, RED
```

subir a github (una vez):
```powershell
git remote add origin https://github.com/MI_USUARIO/parqueadero.git
git push -u origin master
```

repo debe ser **público** para la entrega.

---

## 11. cheat sheet — comandos que debo saber de memoria

```powershell
cd D:\parqueadero
uv sync                                          # instalar deps
uv run python -m pytest test/ -v                 # unitarios
uv run behave                                    # BDD
uv run bandit -r src/ -ll                        # seguridad
uv run python src/api.py                         # levantar API
uv run locust -f locustfile.py --headless -u 20 -r 5 -t 15s --host http://127.0.0.1:8000
git add .
git commit -m "mensaje"
git push
```

---

## 12. cosas que casi se me olvidan (checklist parcial)

- [ ] 30 min gratis → 30=$0, 31=$500 (límites)
- [ ] ceil = redondea hora hacia arriba (fracción cuenta)
- [ ] tope $12000 en 1440 min
- [ ] VIP 20% ANTES del tope → 1440 VIP = $9600
- [ ] TDD: red → green → refactor en commits separados
- [ ] behave necesita `features/steps/`
- [ ] environment.py arregla imports de src
- [ ] texto en steps = EXACTO al .feature
- [ ] context es la mochila entre steps
- [ ] pipeline: tests en todo push, locust solo en main
- [ ] P95 < 300ms
- [ ] README público explica cómo correr cada prueba
- [ ] mínimo 10 commits
- [ ] repo público en github con pipeline verde

---

## 13. si algo falla — qué hice mal (yo conmigo mismo)

| error | probable causa | qué hago |
|-------|----------------|----------|
| ModuleNotFoundError src | no estoy en raíz del proyecto | `cd D:\parqueadero` |
| pytest 0 tests | carpeta mal | `uv run python -m pytest test/ -v` |
| behave no steps | falta carpeta steps | crear `features/steps/cobro_steps.py` |
| step undefined | texto no coincide con .feature | copiar texto exacto |
| locust P95 altísimo | 2 servidores en puerto 8000 | cerrar procesos, uno solo |
| bandit B104 | host 0.0.0.0 | usar 127.0.0.1 |
| pipeline rojo en github | ver log del step que falló | click en la X roja y leer error |

---

*fin de apuntes. suerte en el parcial. si leo esto la noche antes, me acuerdo de casi todo.*
