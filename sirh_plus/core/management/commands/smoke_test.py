"""Compuerta 3: el chequeo de salud desde la consola.

Lee la **misma tupla** que la ruta `/salud/` (`core/checks.py`), asi que los
dos no pueden contradecirse. Devuelve codigo de salida 1 si algo obligatorio
falla, para que sirva en un script de despliegue.
"""

from django.core.management.base import BaseCommand

from core import checks


class Command(BaseCommand):
    help = "Verifica que el sistema este en condiciones de atender."

    def handle(self, *args, **opciones):
        todo_bien, filas = checks.correr()

        for nombre, ok, mensaje, obligatorio in filas:
            marca = "OK " if ok else "FALLA"
            etiqueta = "" if obligatorio else "  (informativo)"
            linea = f"[{marca}] {nombre}: {mensaje}{etiqueta}"
            estilo = self.style.SUCCESS if ok else self.style.ERROR
            self.stdout.write(estilo(linea))

        for nombre, mensaje in checks.apagados():
            self.stdout.write(self.style.WARNING(f"[ -- ] {nombre}: {mensaje}"))

        if todo_bien:
            self.stdout.write(self.style.SUCCESS("\nTodo en verde."))
            return

        self.stderr.write(self.style.ERROR("\nHay chequeos obligatorios en rojo."))
        raise SystemExit(1)
