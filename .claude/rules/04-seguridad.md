---
paths:
  - "**/*.py"
  - "deploy/**"
  - ".env.example"
---

# 04 — Prácticas de seguridad

Aplica a toda app interna. "Es interna" no es una excusa: la mayoría de los incidentes en aplicaciones internas vienen de suponer que nadie mal intencionado llega ahí.

---

## 1. Secretos

- **Todo secreto vive en `.env`**, en la raíz del proyecto, **nunca versionado**. Se lee con `django-environ`.
- **Nada de credenciales en el código.** Ni en settings, ni en un módulo de constantes, ni "temporalmente".
- **`.env.example` se versiona siempre**, con todas las variables, su descripción y **el comando exacto para generar cada clave**:

```
# Clave secreta de Django. Genera una con:
#   python -c "import secrets; print(secrets.token_hex(32))"
DJANGO_SECRET_KEY=cambia-esta-clave
```

- **`.gitignore` cubre desde el primer commit:** `.env`, `*.env` (con excepción de `.env.example`), `*.key`, archivos de datos locales, entornos virtuales, configuración local de herramientas.
- **Claves de producción distintas a las de desarrollo.** Siempre.
- **Usuario de base de datos con permisos mínimos**, nunca una cuenta administrativa.
- **Mantener `.env.example` al día.** Es lo primero que lee quien monta el entorno — y lo primero que un agente toma como descripción vigente del sistema. Una variable descrita según un diseño anterior desinforma a ambos.

### Claves de cifrado: la regla que suele faltar

Si la app cifra datos, la clave necesita **regla de custodia escrita**, no solo regla de uso:

- Dónde está respaldada, **fuera del servidor**.
- Quién la tiene.
- Qué se pierde si se pierde. Normalmente: **todo lo cifrado, de forma irrecuperable.**
- Rotarla invalida lo ya cifrado — no se rota sin un plan de re-cifrado.

---

## 2. Autenticación y autorización

**La identidad no se define por aplicación: vive en una base maestra compartida. Ver `07-identidad-y-acceso.md`.** Esta sección cubre lo que aplica en cualquier caso.

- **Contraseñas siempre con hash**, usando los hashers por defecto de Django. Nunca texto plano, nunca un esquema propio, nunca un hash calculado en SQL.
- **Roles explícitos y pocos.** Son dos y se llaman igual en todas las apps: `consulta` y `administra`.
- **Una credencial válida no basta.** El acceso a cada aplicación se concede por separado; sin esa concesión no se inicia sesión, aunque la clave sea correcta.
- **La protección vive en el backend.** Ocultar un enlace en el menú no es protección: es cortesía visual. Toda ruta sensible se protege con su decorador o permiso, del lado del servidor.
- **Forzar cambio de contraseña en el primer ingreso** para cuentas creadas por un administrador.
- **Negar acceso con una pantalla propia** (403) que explique qué pasó y ofrezca salida, no con un error crudo del servidor.
- Toda operación que modifica estado va por **POST con token CSRF**. Ningún cambio por enlace GET.

> **Nombres:** si se necesita un decorador propio, se le da un **nombre propio**. Reutilizar el nombre de uno de Django obliga a leer los imports para saber cuál está actuando, y un agente se equivoca ahí con facilidad.

---

## 3. Consultas a base de datos

**Los valores SIEMPRE van como parámetro. En el texto del SQL solo se interpolan identificadores de una lista blanca.**

La formulación doble importa: "usá consultas parametrizadas" sola no alcanza, porque estas apps construyen SQL dinámico de forma legítima (listas de columnas, nombre de tabla según fecha).

```python
# ✅ Correcto: el valor va como parámetro; lo interpolado es una constante
# del módulo y una condición literal con marcadores.
COLUMNAS = "OP, COD, FECHA"
condicion = "COD LIKE ? AND FECHA BETWEEN ? AND ?"
sql = f"SELECT {COLUMNAS} FROM OP WHERE {condicion}"
cursor.execute(sql, [cod, desde, hasta])

# ✅ Correcto: nombre de tabla dinámico, validado contra lista blanca
TABLAS_VALIDAS = {"MOV_ACTUAL", "MOV_MES_ANTERIOR", "MOV_HISTORICO"}
if tabla not in TABLAS_VALIDAS:
    raise ValueError(...)
sql = f"SELECT ... FROM {tabla} WHERE ID = ?"

# ❌ Prohibido: un valor dentro del texto del SQL
sql = f"SELECT ... WHERE COD = '{cod}'"
```

**El patrón `f"SELECT ... {x}"` se ve peligroso aunque sea correcto.** Por eso la regla se escribe explícita: quien revise —persona o agente— debe poder verificar en un vistazo que lo interpolado nunca viene del usuario.

**Sobre sistemas ajenos: solo lectura, siempre.** Ningún `INSERT`/`UPDATE`/`DELETE`. Y el usuario de conexión debería tener únicamente permiso de lectura, para que la regla no dependa solo de la disciplina.

**Límite de parámetros por consulta:** los drivers ODBC cortan alrededor de 2.100. Toda consulta con `IN (?, ?, …)` sobre un conjunto que pueda crecer debe trocearse en lotes (500 es un tamaño seguro). Es un error que no aparece en pruebas con pocos datos y estalla en producción con un rango amplio.

### Tiempos de espera y consultas largas

Una consulta sin límite de tiempo contra un sistema ajeno bloquea un worker de Gunicorn hasta que el otro extremo responda o se caiga la conexión. Con pocos workers, dos consultas lentas dejan la aplicación sin atender a nadie.

**Toda conexión a un sistema ajeno declara su tiempo de espera, en dos niveles:**

```python
# <fuente>_db/conexion.py
conexion = pyodbc.connect(cadena, timeout=SEGUNDOS_CONEXION)  # abrir la conexión
conexion.timeout = SEGUNDOS_CONSULTA                          # ejecutar cada consulta
```

Los dos valores se leen de `.env`, con un valor por defecto conservador, y se documentan en `.env.example`. Nunca se dejan en infinito, que es el comportamiento por defecto de la mayoría de los drivers.

**Cuando una consulta supera el tiempo:** se registra en el log con los parámetros de la búsqueda y se le devuelve al usuario un mensaje que diga qué hacer — acotar el rango de fechas, filtrar por menos elementos. Nunca un error crudo ni una pantalla en blanco.

**Si una consulta necesita de verdad más tiempo del razonable**, el problema no es el límite: es la consulta. Antes de subir el valor se verifica el tamaño y los índices de las tablas involucradas (ver `06-lecciones.md`, L2).

---

## 4. Manejo de errores

**El detalle técnico va al log. Al usuario va un mensaje que pueda entender.**

```python
# ❌ Prohibido
return render(request, "resultado.html", {"traceback": traceback.format_exc()})

# ✅ Correcto
logger.exception("Falló la consulta a <sistema>")
return render(request, "resultado.html",
              {"error": "No se pudo consultar <sistema>. Intenta de nuevo o avisa a TI."},
              status=500)
```

Esto **no depende de `DEBUG`**: una plantilla que imprime el traceback lo imprime también en producción, y expone rutas del servidor, nombres de tabla y fragmentos de SQL a cualquiera que provoque un error.

> Encontrado en `AppConsultasFact`: dos plantillas imprimen `{{ traceback }}` cuando la vista lo pasa al contexto.

**Logging configurado desde el inicio.** Sin `LOGGING` en settings, los errores no quedan en ningún lado — y entonces mostrárselos al usuario se vuelve la única forma de verlos, que es justo lo que esta regla prohíbe. **Las dos cosas van juntas o ninguna funciona.**

---

## 5. Dependencias

- Versiones fijas y justificadas (ver 02 §3).
- **Cero paquetes instalados y sin usar**: cada uno es superficie de ataque que nadie está vigilando.
- Las dependencias transitorias se marcan con su condición de salida, y se revisan.

---

## 6. Despliegue

- **`DEBUG` desactivado en producción.** Sin excepción.
- **`ALLOWED_HOSTS` explícito**, nunca `*`.
- **Gunicorn detrás de Nginx**, gestionado por systemd, escuchando solo en localhost.
- **Servicio bajo un usuario dedicado**, no `root`.
- **Cookies de sesión y CSRF marcadas como seguras** cuando hay HTTPS; si la app se sirve sin HTTPS en la red interna, **eso se escribe como decisión consciente** en el `CLAUDE.md` de la app, con su razón. Un silencio aquí no es una postura.
- **`python manage.py check --deploy` es compuerta de despliegue.** Django ya lista lo que falta; correrlo es gratis.
- **Las particularidades del servidor se documentan en el repo**, no en la memoria de quien desplegó. Ejemplo real: conectar a SQL Server 2012 desde Rocky Linux 9 exige una configuración de OpenSSL específica vía variable de entorno en la unit de systemd — sin ella la app arranca pero no conecta a la base. Un dato así, no escrito, cuesta un día de diagnóstico cada vez.

---

## 7. Revisión de seguridad: qué hace un agente y qué no

El agente de seguridad revisa **lógica**: permisos mal aplicados, validaciones ausentes, datos sensibles en respuestas o logs, rutas sin proteger, secretos filtrados en el código.

Lo **determinístico** lo hacen herramientas: `check --deploy`, escaneo de dependencias, linter.

> **Un agente que dice "se ve bien" no es una compuerta.** Las compuertas son las máquinas; los agentes encuentran lo que las máquinas no ven.
