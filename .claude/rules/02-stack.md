---
paths:
  - "**/*.py"
  - "requirements*.txt"
  - "pyproject.toml"
---

# 02 — Stack tecnológico y política de dependencias

## 1. Stack fijo

Toda app interna de Plastitec se construye con esto. No se evalúan alternativas por proyecto.

| Capa | Tecnología | Nota |
|---|---|---|
| Lenguaje | **Python 3.11+** | |
| Framework web | **Django 5.2 LTS** | Server-rendered |
| Base propia | **PostgreSQL** vía `psycopg[binary]` | Una por app. Guarda el dominio, nunca usuarios |
| Identidad | **MySQL** vía `mysqlclient` — previsto PostgreSQL | **Una sola, compartida por todas las apps** (ver 07) |
| Sistemas ajenos | **SQL Server** vía `pyodbc` + ODBC Driver 17 | Solo lectura (ver 01 §4) |
| Configuración | **django-environ** leyendo `.env` | |
| Plantillas | **Django Template Language (DTL)** | Ver §4 |
| Frontend | **CSS plano + JavaScript vanilla** | Sin build, sin Node |
| Exportación | `openpyxl` (Excel) · `reportlab` (PDF) | |
| Servidor | **Gunicorn** tras **Nginx**, bajo **systemd** | Rocky Linux 9 |
| Pruebas | `unittest` de la stdlib | Sin dependencia extra |

## 2. Qué está prohibido, y por qué

| Prohibido | Razón |
|---|---|
| **Build de frontend** (Node, Tailwind, webpack, npm) | Agrega una cadena de herramientas completa que hay que instalar, versionar y reproducir en el servidor, para una app interna que se sirve con HTML y CSS. El costo de mantenimiento no se justifica. |
| **Librerías JS de terceros** (jQuery, frameworks SPA) | Lo que hacen estas apps —mostrar tablas, filtrar, abrir modales— se resuelve con JS plano en decenas de líneas. |
| **CDN para cualquier recurso** | El servidor está en la red interna. Un recurso remoto es una dependencia de internet para que la app se vea bien, y una fuga de tráfico hacia afuera. Todo se auto-hospeda en `static/vendor/`. |
| **Escribir en la base de un sistema ajeno** | La app es invitada, no dueña. |
| **Duplicar la regla de negocio en JS** | Ver §5. |

## 3. Política de dependencias

**Ninguna dependencia nueva sin justificación escrita.** El `requirements.txt` no lleva una sola línea sin comentario que responda tres cosas:

1. **Para qué** se usa, con el archivo concreto que la importa.
2. **Qué pasa si falta** (¿la app no arranca? ¿se degrada una función?).
3. **Si es transitoria**, cuándo se podrá quitar.

```
# Acceso de solo lectura a <sistema ajeno>. Sin esto, <módulo> no puede
# consultar nada. Dependencia permanente.
pyodbc==5.3.0

# Exportación a Excel en <modulo>/exportacion.py. Sin esto, el botón de
# descarga deja de funcionar; el resto de la app sigue operando.
openpyxl==3.1.5
```

**Versiones siempre fijas** (`==`), nunca rangos. Y confirmadas contra `pip freeze` del entorno real: los pines escritos a mano se desfasan en silencio.

**No arrastrar paquetes "por si acaso".** Una dependencia instalada y no usada es superficie de ataque, peso de instalación y ruido para quien lee el archivo. Si no se usa hoy, se saca.

## 4. Plantillas: Django Template Language

**Se usa DTL, el sistema de plantillas propio de Django. Sin excepciones y sin evaluar alternativas.**

No se instala ni se configura ningún otro motor de plantillas. Un motor alternativo obliga a mantener adaptadores, divide los ejemplos del equipo en dos dialectos y hace que la documentación de Django deje de aplicar tal cual.

Las herramientas de plantilla que una app necesita —filtros, etiquetas, componentes reutilizables— se resuelven con los mecanismos de DTL: `{% include %}`, `{% extends %}`, bloques, y filtros propios en `templatetags/` cuando haga falta.

## 5. Dónde vive la lógica: una sola vez, en Python

La regla de negocio vive en `dominio/` (ver 01 §3) y **no se reimplementa en JavaScript**.

Cuando se necesite interactividad en el cliente (filtrar, ordenar, paginar una tabla ya cargada), el JS puede **reordenar y filtrar datos que el servidor ya calculó**, pero no recalcularlos.

**Por qué la regla es absoluta:** una divergencia entre dos implementaciones de la misma fórmula es silenciosa. Nadie ve un error ni una excepción: solo un número distinto según dónde se mire. Y como las dos implementaciones viven en lenguajes distintos, ningún cambio en una obliga a tocar la otra.

> **Ante la duda, una consulta más al servidor es más barata que dos implementaciones de la misma regla.**

Si la interactividad en vivo es un requisito real del usuario, la respuesta correcta es que el servidor devuelva los datos ya calculados en todas las agrupaciones que el usuario pueda elegir, no que el navegador los recalcule.

## 6. Control de versiones

**Git desde el primer commit, antes de la primera línea de código.** No es negociable y no es opcional para apps pequeñas.

Sin git no hay diff, y sin diff:

- no se puede revisar un cambio, ni humano ni de un agente;
- no hay reversa cuando algo se rompe;
- no se puede verificar "esto no cambió lo demás".

Todo el flujo de trabajo con agentes se apoya en poder leer un diff. Es el requisito previo a todo lo demás.

## 7. Calidad automática

Lo que puede verificar una máquina no se deja a criterio de nadie:

**El formateador y el linter son `ruff`.** Una sola herramienta cubre los dos roles, se instala con `pip` y no arrastra dependencias. La configuración vive en `pyproject.toml`, versionada, y viene en la plantilla:

```toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "W", "I", "UP", "B", "S"]
ignore = ["S101"]            # assert: se usa en las pruebas

[tool.ruff.lint.per-file-ignores]
"*/migrations/*" = ["E501"]  # migraciones generadas por Django
"config/settings.py" = ["E501"]
```

Los tres comandos que son compuerta, en este orden:

```bash
ruff format .                           # formatea
ruff check .                            # lint
python -m unittest discover -s tests    # pruebas del núcleo
python manage.py check --deploy         # antes de desplegar (ver 04 §6)
```

**Un agente acierta el estilo cuando una herramienta se lo corrige, no cuando lo lee en un documento.** Por eso el formateador se corre, no se pide.

La regla `S` de ruff (bandit) detecta parte de lo que cubre `04-seguridad`: SQL construido con interpolación, secretos literales, uso de `subprocess` sin control. No reemplaza la revisión, pero atrapa lo evidente antes de que llegue a una persona.
