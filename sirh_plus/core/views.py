"""Vistas del nucleo: la cara publica, el ingreso, la salud y los errores.

Decisiones que encierra:

- **La pantalla de ingreso no valida nada.** Es una capa visual que la fase 1
  conecta contra el gestor de identidad. No hay formulario que procesar, no
  hay contrasena que comparar y no hay usuario que buscar: SIRH+ no gestiona
  usuarios (ver `CLAUDE.md`).
- `/salud/` responde JSON y cambia el codigo HTTP segun el resultado, para que
  un monitor pueda leerlo sin interpretar texto.
- Las vistas de error no muestran detalle tecnico. El detalle va al registro
  de eventos; al usuario le llega un mensaje que entienda.
"""

import logging

from django.http import JsonResponse
from django.shortcuts import render

from core import checks

logger = logging.getLogger(__name__)


def inicio(request):
    """La cara publica. Sin sesion, sin datos de nadie."""
    return render(request, "publico/inicio.html")


def ingreso(request):
    """Pantalla de acceso. **No valida nada todavia** (desviacion D4).

    Si alguien envia el formulario, la pantalla lo dice en lugar de quedarse
    muda: una pantalla que no responde parece rota. El POST existe para que el
    token CSRF este puesto desde ahora, no para procesar nada.
    """
    return render(request, "publico/ingreso.html", {"intento": request.method == "POST"})


def salud(request):
    """Estado del sistema, leyendo la misma tupla que `smoke_test`."""
    todo_bien, filas = checks.correr()
    cuerpo = {
        "estado": "ok" if todo_bien else "falla",
        "chequeos": [
            {
                "nombre": nombre,
                "ok": ok,
                "mensaje": mensaje,
                "obligatorio": obligatorio,
            }
            for nombre, ok, mensaje, obligatorio in filas
        ],
        "apagados": [
            {"nombre": nombre, "mensaje": mensaje} for nombre, mensaje in checks.apagados()
        ],
    }
    if not todo_bien:
        logger.error("Chequeo de salud en rojo: %s", cuerpo)
    return JsonResponse(cuerpo, status=200 if todo_bien else 503)


ICONOS = (
    "check",
    "cerrar",
    "info",
    "alerta",
    "error",
    "ayuda",
    "candado",
    "buscar",
    "usuario",
    "salir",
    "menu",
    "flecha-derecha",
    "reloj",
    "panel",
    "personas",
    "estructura",
    "documento",
    "reloj-marcacion",
    "caja",
    "engranaje",
)


def componentes(request):
    """Catalogo del sistema de diseno. Solo existe en desarrollo."""
    contexto = {
        "iconos": ICONOS,
        "ruta": [
            {"texto": "Administración", "href": "#"},
            {"texto": "Sistema de diseño"},
        ],
    }
    return render(request, "desarrollo/componentes.html", contexto)


def error_403(request, exception=None):
    return render(request, "403.html", status=403)


def error_404(request, exception=None):
    return render(request, "404.html", status=404)


def error_500(request):
    return render(request, "500.html", status=500)
