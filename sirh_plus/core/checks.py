"""Chequeos de salud del sistema: una sola definicion.

La misma tupla alimenta el comando `manage.py smoke_test` y la ruta `/salud/`,
de modo que los dos no puedan contradecirse
(`.claude/rules/01-estructura-y-capas.md` seccion 6).

Decisiones que encierra:

- Cada chequeo devuelve `(ok, mensaje)` y nunca lanza: un chequeo que revienta
  deja sin diagnostico a los demas, que es justo lo contrario de lo que se
  busca. El error se atrapa y se convierte en el mensaje.
- `obligatorio=False` marca lo informativo: no tumba el resultado global.
- Los dos chequeos de identidad estan **declarados y apagados** (desviacion
  D4). Se declaran desde ahora para que el dia que el gestor exista se
  enciendan, no se inventen.
"""

from pathlib import Path

from django.conf import settings
from django.db import connection


def chequear_bd():
    """La base propia responde."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
    except Exception as exc:  # noqa: BLE001 - cualquier fallo es un fallo de salud
        return False, f"No responde: {exc.__class__.__name__}"
    return True, f"Responde · {connection.settings_dict['NAME']}"


def chequear_migraciones():
    """No quedan migraciones sin aplicar."""
    try:
        from django.db.migrations.executor import MigrationExecutor

        executor = MigrationExecutor(connection)
        objetivos = executor.loader.graph.leaf_nodes()
        plan = executor.migration_plan(objetivos)
    except Exception as exc:  # noqa: BLE001
        return False, f"No se pudo verificar: {exc.__class__.__name__}"
    if plan:
        nombres = ", ".join(f"{m.app_label}.{m.name}" for m, _ in plan[:3])
        return False, f"Faltan {len(plan)} por aplicar: {nombres}"
    return True, "Al dia"


def chequear_estaticos():
    """La hoja de estilos con los design tokens esta donde se espera."""
    hoja = Path(settings.BASE_DIR) / "static" / "css" / "styles.css"
    if not hoja.is_file():
        return False, "Falta static/css/styles.css"
    if ":root" not in hoja.read_text(encoding="utf-8"):
        return False, "styles.css no declara los tokens en :root"
    return True, "Hoja de estilos con tokens en :root"


def chequear_identidad_conexion():
    """Declarado y apagado: el gestor de identidad todavia no existe (D4)."""
    return True, "Apagado hasta que exista el gestor de identidad"


def chequear_identidad_registro():
    """Declarado y apagado: SIRH+ aun no esta registrada en el gestor (D4)."""
    return True, "Apagado hasta que exista el gestor de identidad"


# (nombre, funcion, obligatorio)
CHEQUEOS = (
    ("base_de_datos", chequear_bd, True),
    ("migraciones_al_dia", chequear_migraciones, True),
    ("estaticos", chequear_estaticos, False),
)

# Declarados y desactivados. No entran en el resultado global: se muestran
# para que se vea que existen y que estan apagados a proposito.
CHEQUEOS_APAGADOS = (
    ("identidad_conexion", chequear_identidad_conexion, False),
    ("identidad_registro", chequear_identidad_registro, False),
)


def correr():
    """Corre los chequeos activos.

    Devuelve `(todo_bien, filas)`, donde cada fila es
    `(nombre, ok, mensaje, obligatorio)`.
    """
    filas = []
    todo_bien = True
    for nombre, funcion, obligatorio in CHEQUEOS:
        try:
            ok, mensaje = funcion()
        except Exception as exc:  # noqa: BLE001
            ok, mensaje = False, f"El chequeo fallo: {exc.__class__.__name__}"
        if obligatorio and not ok:
            todo_bien = False
        filas.append((nombre, ok, mensaje, obligatorio))
    return todo_bien, filas


def apagados():
    """Los chequeos declarados pero desactivados, para mostrarlos como tales."""
    return [(nombre, funcion()[1]) for nombre, funcion, _ in CHEQUEOS_APAGADOS]
