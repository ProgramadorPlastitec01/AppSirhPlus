"""Lo que toda plantilla necesita saber, sin que cada vista lo repita.

Decisiones que encierra:

- Aqui solo entra lo que es igual en todas las pantallas: el nombre del
  sistema, la empresa y la duracion de la sesion. **Nada que dependa de una
  consulta**: un procesador de contexto corre en cada peticion, y una consulta
  aqui es una consulta en cada pantalla del sistema.
"""

from django.conf import settings


def marca(request):
    return {
        "SISTEMA": "SIRH+",
        "EMPRESA": "Plastitec S.A.S.",
        "SESION_MINUTOS": settings.SESSION_COOKIE_AGE // 60,
        "ES_DESARROLLO": settings.DEBUG,
    }
