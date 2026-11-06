---
paths:
  - "**/*.py"
---

# 01 — Estructura de carpetas y capas

## 1. Árbol obligatorio

Toda app nueva arranca con esta estructura. Los nombres no se cambian por gusto.

```
<nombre-app>/
├── .env                      secretos reales — NUNCA versionado
├── .env.example              plantilla documentada de .env — SÍ versionado
├── .gitignore
├── README.md                 qué es la app, cómo se levanta en local
├── CLAUDE.md                 contexto para los agentes (ver README del estándar)
├── requirements.txt          dependencias con versión fija y comentario
│
└── <nombre_proyecto>/        proyecto Django autocontenido
    ├── manage.py
    │
    ├── dominio/              ★ NÚCLEO: paquete Python PURO (ver §3)
    │   ├── __init__.py       fachada: qué expone el paquete
    │   └── <reglas>.py
    │
    ├── tests/                pruebas del núcleo — corren SIN levantar Django
    │   └── test_<dominio>.py
    │
    ├── config/               settings, urls, wsgi, asgi
    ├── core/                 vistas base, salud del sistema, utilidades compartidas
    │   └── checks.py         chequeos de salud (ver §5)
    ├── cuentas/              ★ identidad compartida — IDÉNTICO en toda app (ver 07)
    ├── <fuente_externa>_db/  acceso a bases ajenas de solo lectura (ver §4)
    ├── <modulo_1>/           una app Django por módulo funcional
    │
    ├── templates/            plantillas (base, macros, una por pantalla)
    ├── static/
    │   ├── css/styles.css    hoja única con los design tokens en :root
    │   └── vendor/           tipografías e iconos auto-hospedados
    │
    └── deploy/               unit de systemd, conf de nginx, runbook
```

**Una app Django por módulo funcional.** Si el módulo consulta, calcula y exporta, eso son archivos dentro de esa app — no apps separadas.

## 2. Responsabilidad de cada archivo dentro de un módulo

Un módulo funcional se parte siempre igual. Esto es lo que impide que las vistas crezcan sin control.

```
<modulo>/
├── views.py           SOLO orquesta: recibe request, delega, responde
├── consultas.py       acceso a datos: SQL / ORM. No calcula, no formatea
├── presentacion.py    agrupa y arma lo que la plantilla necesita
├── exportacion.py     salidas a archivo (Excel, PDF)
├── models.py          modelos propios (vacío si el módulo no tiene datos propios)
└── urls incluidas en config/urls.py
```

**Regla verificable:** una función de `views.py` no debería pasar de ~30 líneas. Si crece, la lógica pertenece a una capa de abajo.

> Evidencia del patrón: en `AppConsultasFact`, `ordenes/views.py` tiene 270 líneas para 9 vistas, mientras `consultas.py` tiene 1.081 y `presentacion.py` 525. Las vistas se mantuvieron delgadas porque cada capa tenía dueño.

## 3. ★ El núcleo de dominio es un paquete Python puro

**La regla más importante del estándar.**

El paquete `dominio/` contiene las reglas de negocio y **no importa Django, ni el framework web, ni el driver de base de datos, ni nada de I/O**. Recibe datos ya consultados y devuelve resultados.

```python
# dominio/reglas.py — así se ve
def calcular_algo(valor, base):
    """Recibe números, devuelve números. No sabe de dónde vinieron."""
    ...
```

**Por qué es innegociable:**

- **Las reglas de negocio se prueban en milisegundos**, sin levantar servidor, sin base de datos y sin red. Una suite que tarda segundos se corre en cada cambio; una que tarda minutos se deja de correr.
- **El cálculo queda aislado de todo lo que puede fallar por otra razón.** Cuando un número sale mal, el defecto está en `dominio/` o en los datos que recibió — no hay una tercera opción que investigar.
- **Es la única capa donde un agente de IA trabaja contra una compuerta real:** o las pruebas pasan, o no. En el resto del código la verificación depende de que alguien lea; aquí la hace la máquina.

**Qué NO va en `dominio/`:** nada que sepa de `request`, de plantillas, de conexiones, de archivos, de formato de presentación.

### El paquete `cuentas/` no es de la app

`cuentas/` viene resuelto en la plantilla y **es el mismo archivo por archivo en todas las aplicaciones**. Conecta con la base de identidad compartida, autentica y resuelve el rol. Lo único que cambia entre apps es `CODIGO_APLICACION` en el `.env`.

Modificarlo en una app es una desviación del estándar y se declara. Casi siempre, lo que hay que cambiar es el estándar — y entonces el cambio se hace en la plantilla y se propaga a todas.

## 4. Datos propios vs. datos ajenos

| | Datos propios de la app | Datos de un sistema ajeno (ERP, otro servicio) |
|---|---|---|
| Acceso | ORM de Django | SQL parametrizado en una capa aislada |
| Registro | En `DATABASES` de `settings.py` | **Nunca** en `DATABASES` |
| Modelado | `models.py` + migraciones | **Nunca** se modela |
| Escritura | Permitida | **Prohibida** — solo lectura, siempre |
| Ubicación | El módulo que los usa | App propia: `<fuente>_db/conexion.py` |

**Por qué no se modelan los datos ajenos:** modelarlos da una falsa sensación de propiedad sobre tablas que la app no controla y que otro sistema puede cambiar sin avisar. La app es un invitado ahí.

La app de acceso expone **solo funciones de conexión**, una por base:

```python
# <fuente>_db/conexion.py
def get_<fuente>_connection():
    """Conexión de SOLO LECTURA a <fuente>."""
```

## 5. Regla de dependencias entre capas

Las flechas van **hacia abajo**. Nunca hacia arriba, nunca en círculo.

```
config/  ──▶  módulos  ──▶  dominio/
                  │
                  └──────▶  <fuente>_db/  (solo la capa de consultas)
```

- `dominio/` no importa **nada** del proyecto. Es el piso.
- `dominio/` tampoco sabe quién es el usuario. Si una regla depende del rol, el rol llega como parámetro.
- `consultas.py` puede importar `dominio/` y `<fuente>_db/`.
- `views.py` no habla con la base directamente: pasa por `consultas.py`.
- `templates/` no consulta nada: recibe lo que `presentacion.py` ya armó.

Si un import rompe estas flechas, el diseño está mal — no el import.

## 6. Chequeos de salud: una sola definición

Cada app expone su estado de forma verificable, y **la misma definición** alimenta tanto un comando de consola como una ruta HTTP.

```python
# core/checks.py
CHEQUEOS = (
    ("<nombre>", funcion_que_devuelve_(ok, mensaje), obligatorio_bool),
    ...
)
```

- Un comando de gestión (`manage.py smoke_test`) para verificar antes de desplegar.
- Una ruta `/salud/` para verificar en caliente.
- `obligatorio=False` marca chequeos informativos que no tumban el resultado global.

Ambos leen la misma tupla, así que **no pueden contradecirse**.

## 7. Documentar la decisión, no el código

Todo módulo abre con un docstring que explica **por qué** existe y qué decisión encierra — no qué hace línea por línea.

```python
"""
Qué resuelve este módulo y por qué está separado.

Decisiones que encierra:
- <decisión> porque <razón>.
- Intento fallido documentado: <qué se probó y por qué no funcionó>.
"""
```

Incluir los **intentos fallidos** es parte de la regla. Un agente (o un compañero) que no sepa que algo ya se probó, lo va a volver a probar.
