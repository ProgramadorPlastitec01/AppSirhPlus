# SIRH+

Sistema de Información de Recursos Humanos de **Plastitec S.A.S.**

Reemplaza al SIRH antiguo e integra BioTime y COPEC en una sola plataforma. Atiende a unas 1.100 personas entre directos, temporales y aprendices SENA.

> **Estado: en construcción, fase 0.** Todavía no hay funcionalidad de negocio.

---

## Qué hace

Una sola aplicación con tres caras:

| Cara | Quién entra | Qué ve |
|---|---|---|
| **Pública** | Cualquiera, sin sesión | Noticias, organigrama, convocatorias |
| **Colaborador** | Cada persona de la nómina | Lo suyo: marcaciones, vacaciones, solicitudes, cursos |
| **Gestión** | Recursos Humanos y jefes | Su personal, o toda la empresa según su rol |

Doce módulos de negocio: personal, empresa, marcaciones, nómina, eventualidades, trámites, formación, competencias, dotación, encuestas, reservas e indicadores.

---

## Requisitos

| | Versión |
|---|---|
| Python | 3.11 o superior |
| PostgreSQL | 17 |
| Sistema | Linux, macOS o Windows para desarrollo · Rocky Linux 9 en producción |

No hace falta Node, ni npm, ni ninguna herramienta de frontend. **El proyecto no tiene build.**

---

## Levantarlo en local

```bash
# 1. Clonar
git clone <url-del-repositorio> sirh-plus
cd sirh-plus

# 2. Entorno virtual
python -m venv .venv
source .venv/bin/activate          # en Windows: .venv\Scripts\activate

# 3. Dependencias
pip install -r requirements.txt

# 4. Configuración
cp .env.example .env
```

Abre `.env` y genera la clave secreta:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Crea la base de datos y su usuario:

```sql
CREATE DATABASE sirh_plus;
CREATE USER sirh_app WITH PASSWORD 'la-que-pongas-en-el-.env';
GRANT ALL PRIVILEGES ON DATABASE sirh_plus TO sirh_app;
```

Y levanta, desde `sirh_plus/`, que es donde está `manage.py`:

```bash
cd sirh_plus
python manage.py migrate
python manage.py smoke_test          # debe salir todo en verde
python manage.py runserver
```

En `http://127.0.0.1:8000/salud/` deberías ver el estado del sistema.

---

## Comandos del día a día

```bash
ruff format .                              # formatear
ruff check .                               # revisar
python -m unittest discover -s tests       # pruebas del núcleo
python manage.py smoke_test                # chequeo de salud
python manage.py check --deploy            # revisión de seguridad
python manage.py test                      # pruebas con Django, cuando el módulo las tenga
```

**Antes de cualquier commit pasan los tres primeros:** `ruff format`, `ruff check` y las pruebas del núcleo. No se usa `--no-verify`.

`smoke_test` y `check --deploy` son compuertas de fase, no de commit: se corren al cerrar la fase. `manage.py test` no es compuerta.

---

## Cómo está organizado

```
sirh-plus/                   raíz del repositorio
├── .env                     secretos reales — NUNCA versionado
├── .env.example             la plantilla documentada — SÍ versionado
├── .gitignore
├── README.md
├── CLAUDE.md
├── requirements.txt
├── pyproject.toml
│
└── sirh_plus/               el proyecto Django
    ├── manage.py
    ├── config/              settings, urls, wsgi
    ├── core/                chequeos de salud, utilidades, base
    ├── dominio/             ★ reglas puras: sin Django, sin entrada/salida
    ├── tests/               pruebas del núcleo, sin Django
    │
    ├── personal/            personas, vínculos, historial, completitud
    ├── maestros/            áreas, cargos, estructura, puntos de marcación
    ├── identidad/           autenticación contra el gestor, altas y bajas
    ├── permisos/            catálogo granular, roles y alcance
    ├── auditoria/           bitácora inmutable
    ├── firmas/              captura, validación y estampado
    │   └── …                el resto de los módulos, por fase
    │
    ├── <fuente>_db/         conexiones de solo lectura a sistemas ajenos
    ├── templates/
    ├── static/              css y vendor; sin build
    └── deploy/
```

**Son dos niveles, como manda `.claude/rules/01-estructura-y-capas.md` §1:** la carpeta del repositorio, con la configuración y los documentos, y dentro el proyecto Django autocontenido. `manage.py` vive junto a `config/`, dentro de `sirh_plus/`, y desde ahí se corren todos los comandos de `manage.py`.

**La regla de dependencias:** `config/ → módulos → dominio/`. Nunca hacia arriba, nunca circular.

`dominio/` es el corazón: no importa Django, no toca la base, y sus pruebas corren en milisegundos. Ahí viven el cálculo de jornada, la causación de vacaciones, la ponderación de competencias y los indicadores.

---

## Documentación

Léela en este orden antes de tocar código:

| | Documento | Para qué |
|---|---|---|
| 1 | `claude/02-plan-de-ejecucion-sirh-plus.md` | **Normativo.** Reglas, compuertas y fases |
| 2 | `claude/00-contexto-maestro-sirh-plus.md` | El proyecto y el porqué de cada decisión |
| 3 | `.claude/rules/03-sistema-de-diseno.md` | **Normativo.** Tokens, componentes, patrones |
| 4 | `claude/01-inventario-y-fases-sirh-plus.md` | Todos los módulos y sus funciones |
| 5 | `CLAUDE.md` | Resumen operativo y estado actual |

Los mockups navegables están en `mockups/`. Ábrelos en el navegador: son archivos autónomos.

**Documentos vivos**, en `docs/`: `pendientes.md` (lo primero que se lee al retomar), `trazabilidad.md` y `glosario.md`.

---

## Cómo se trabaja

El proyecto avanza por **fases**, no por módulos sueltos. Cada fase entrega algo usable y no se avanza hasta que seis compuertas pasen:

1. Formato y lint en verde
2. Pruebas del núcleo en verde
3. Chequeo de salud en verde
4. Revisión de seguridad sin hallazgos
5. Revisión visual y los cuatro estados en cada pantalla
6. **Validación humana** contra un caso real, más revisión del QA

La sexta no la puede dar una máquina.

Dentro de una fase se construye de adentro hacia afuera: modelo → dominio → pruebas → consultas → presentación → vistas → plantillas → verificación.

---

## Qué no se hace aquí

- No hay build de frontend, ni Node, ni librerías de JavaScript de terceros
- No se cargan recursos desde un CDN: todo se auto-hospeda en `static/vendor/`
- No se escribe en la base de datos de un sistema ajeno
- No se duplica una regla de negocio en JavaScript
- No se escriben valores visuales fuera de `:root`
- No entran secretos al repositorio

---

## Seguridad

| Qué | Cómo |
|---|---|
| Secretos | Solo en `.env`, nunca en el código ni en la base |
| Consultas | ORM o SQL parametrizado. Nunca concatenación |
| Validación | En el servidor, siempre |
| Autorización | Verificada en cada ruta y cada acción, no solo en el menú |
| Datos sensibles | Permiso explícito y registro de cada consulta |
| Errores | El detalle al log; al usuario, un mensaje que entienda |

El sistema maneja datos de salud ocupacional, incapacidades y salarios. Aplica la **Ley 1581 de 2012**: cinco años de retención en línea y derecho de corrección.

**Si encuentras una vulnerabilidad**, no abras un ticket público: avisa directamente a Tecnología de Información.

---

## Despliegue

Gunicorn tras Nginx, bajo systemd, en Rocky Linux 9. Los archivos de `deploy/` y el procedimiento completo están en `docs/instalacion-despliegue.md` **(se escribe en la fase 6)**.

El sistema sale **solo a la red interna** en su primera etapa, y no sale a producción sin el gestor de identidad funcionando.

---

## Equipo

Tecnología de Información · Plastitec S.A.S.
Para dudas sobre el dominio: Recursos Humanos.
