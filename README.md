## Tabla de casos de prueba (campo monto)

Particion de equivalencia y valores limite sobre el **monto**:

| Grupo | Rango | Caso limite | Resultado esperado |
|-------|-------|-------------|-------------------|
| Invalido bajo | < 1000 | **999** | Rechazado |
| Valido sin bono | 1000 - 9999 | **1000** (minimo) | Aceptado, 0% bono |
| Bono 10% | 10000 - 29999 | **10000** | Aceptado, 10% bono |
| Bono 25% | 30000 - 50000 | **30000** | Aceptado, 25% bono |
| Invalido alto | > 50000 | **50001** | Rechazado |

Casos premium (bono base + 5%):

| Monto | Premium | Bono total |
|-------|---------|------------|
| 10000 | Si | 15% |
| 30000 | Si | 30% |
| 50000 | Si | 30% |

---
## Reglas de negocio

| Regla | Detalle |
|-------|---------|
| Rango valido | Monto entre **$1.000** y **$50.000**. Fuera de rango = rechazado |
| Bono 10% | Recargas de **$10.000** o mas |
| Bono 25% | Recargas de **$30.000** o mas (reemplaza el 10%) |
| Premium | **+5%** adicional sobre el bono que ya tenga |

## Instalacion

```powershell
cd D:\recargaya
uv sync
```

## 1. Tests unitarios (pytest / TDD)

```powershell
uv run python -m pytest test/ -v
```

Resultado esperado: **7 passed**

Ciclo TDD usado: commits con `test:` (red), `feat:` (green), `refactor:` (limpieza).

---

## 2. Tests BDD (behave / Gherkin)

Escenarios en `features/recarga.feature` (incluye un **Scenario Outline**).

```powershell
uv run behave
```

Resultado esperado: **8 scenarios passed** (4 fijos + 4 del outline)


---

## 3. API FastAPI

Levantar servidor:

```powershell
uv run uvicorn src.api:app --host 127.0.0.1 --port 8000
```

Probar manualmente:

```powershell
curl "http://127.0.0.1:8000/recarga?monto=10000&es_premium=false"
curl "http://127.0.0.1:8000/recarga?monto=999"
```

Documentacion interactiva: http://127.0.0.1:8000/docs

---

## 4. Rendimiento (Locust, 30 usuarios, P95 < 300ms)

Terminal 1 (API):

```powershell
uv run uvicorn src.api:app --host 127.0.0.1 --port 8000
```

Terminal 2 (Locust):

```powershell
uv run locust -f locustfile.py --headless -u 30 -r 10 -t 20s --host http://127.0.0.1:8000
```

Al final debe aparecer: `OK: P95=XXms dentro del limite de 300ms`

---

## 5. Pipeline CI (GitHub Actions)

En **cada push** corre: pytest + behave + bandit + Locust con 30 usuarios.


## Estructura

```
recargaya/
├── src/
│   ├── recarga.py       # logica de negocio
│   └── api.py           # FastAPI
├── test/
│   └── test_recarga.py
├── features/
│   ├── recarga.feature
│   └── steps/
│       └── recarga_steps.py
├── locustfile.py
└── .github/workflows/ci.yml
```
