"""Rutas de SIRH+.

Decisiones que encierra:

- **No hay ruta de administracion de Django.** `django.contrib.admin` no esta
  instalado: SIRH+ no gestiona usuarios y no expone una puerta de
  administracion que nadie diseno ni audito.
- Cada modulo trae sus rutas en su propio `urls.py` y se incluyen aqui. En la
  fase 0 el unico modulo es `core`.
"""

from django.urls import include, path

urlpatterns = [
    path("", include("core.urls")),
]

handler403 = "core.views.error_403"
handler404 = "core.views.error_404"
handler500 = "core.views.error_500"
