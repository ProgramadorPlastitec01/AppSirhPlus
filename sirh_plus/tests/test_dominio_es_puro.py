"""La regla mas importante del estandar, verificada por una maquina.

`dominio/` no importa Django, ni el driver de base de datos, ni nada del
proyecto, ni nada de entrada/salida. Hasta ahora eso era una regla escrita;
aqui es una prueba que falla.

Por que existe esta prueba en la fase 0, cuando `dominio/` todavia esta vacio:

- La compuerta 2 es `python -m unittest discover -s tests`. Sin una sola
  prueba, `unittest` termina con **codigo de salida 5** ("NO TESTS RAN"), que
  en un hook de commit o en un script de despliegue es un fallo. Una compuerta
  que sale en rojo cuando todo esta bien se termina ignorando, y una compuerta
  que se ignora no es una compuerta.
- La regla que protege es la que mas cuesta recuperar si se rompe: el dia que
  `dominio/` importe Django, las pruebas dejan de correr en milisegundos y
  dejan de correrse.

Corre sin levantar Django: lee los archivos y mira sus imports con `ast`. No
los ejecuta.
"""

import ast
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DOMINIO = RAIZ / "dominio"

# Lo que `dominio/` no puede importar, con el motivo.
PROHIBIDOS = {
    "django": "es el framework web",
    "psycopg": "es el driver de la base de datos",
    "config": "es la capa de arriba",
    "core": "es la capa de arriba",
    "os": "es entrada/salida",
    "io": "es entrada/salida",
    "pathlib": "es entrada/salida",
    "socket": "es entrada/salida",
    "subprocess": "es entrada/salida",
    "sqlite3": "es acceso a datos",
    "urllib": "es acceso a la red",
    "requests": "es acceso a la red",
}


def _modulos_importados(archivo):
    """Los nombres de primer nivel que importa un archivo."""
    # utf-8-sig y no utf-8: en Windows es facil guardar un archivo con BOM, y
    # con utf-8 a secas `ast.parse` revienta con «invalid non-printable
    # character U+FEFF», un mensaje que no dice que el problema es el BOM.
    arbol = ast.parse(archivo.read_text(encoding="utf-8-sig"), filename=str(archivo))
    nombres = set()
    for nodo in ast.walk(arbol):
        if isinstance(nodo, ast.Import):
            for alias in nodo.names:
                nombres.add(alias.name.split(".")[0])
        elif isinstance(nodo, ast.ImportFrom):
            if nodo.level:  # un import relativo, dentro del propio paquete
                continue
            if nodo.module:
                nombres.add(nodo.module.split(".")[0])
    return nombres


class DominioEsPuro(unittest.TestCase):
    def test_la_carpeta_dominio_existe(self):
        self.assertTrue(DOMINIO.is_dir(), "Falta la carpeta dominio/")

    def test_no_importa_django_ni_entrada_salida(self):
        for archivo in sorted(DOMINIO.rglob("*.py")):
            with self.subTest(archivo=archivo.name):
                for modulo in _modulos_importados(archivo):
                    motivo = PROHIBIDOS.get(modulo)
                    self.assertIsNone(
                        motivo,
                        f"dominio/{archivo.name} importa «{modulo}», y {motivo}. "
                        f"El dominio recibe datos y devuelve resultados: "
                        f"lo que necesite de afuera llega como parametro.",
                    )


if __name__ == "__main__":
    unittest.main()
