"""Rutas del nucleo: la cara publica, el ingreso y la salud del sistema."""

from django.conf import settings
from django.urls import path

from core import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("ingreso/", views.ingreso, name="ingreso"),
    path("salud/", views.salud, name="salud"),
]

# Catalogo de componentes del sistema de diseno. Es una herramienta de
# desarrollo: se usa para revisar los componentes contra el mockup y para que
# ningun modulo escriba su propio boton. No existe fuera de desarrollo.
if settings.DEBUG:
    urlpatterns += [path("componentes/", views.componentes, name="componentes")]
