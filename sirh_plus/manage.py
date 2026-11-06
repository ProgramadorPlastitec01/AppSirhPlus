#!/usr/bin/env python
"""Punto de entrada de los comandos de Django.

Vive junto a `config/`, dentro de `sirh_plus/`, como manda
`.claude/rules/01-estructura-y-capas.md` seccion 1. Todos los comandos de
`manage.py` se corren desde esta carpeta, no desde la raiz del repositorio.
"""

import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "No se pudo importar Django. Verifica que el entorno virtual este "
            "activo y que las dependencias de requirements.txt esten instaladas."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
