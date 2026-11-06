"""Punto de entrada ASGI.

SIRH+ se sirve por WSGI con Gunicorn. Este archivo existe porque Django lo
espera, no porque haya algo asincrono en el sistema.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_asgi_application()
