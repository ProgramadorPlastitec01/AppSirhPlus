"""Libreria de componentes del sistema de diseno.

**Ningun modulo escribe su propio boton.** Todo lo visual sale de aqui, y los
valores visuales salen de los tokens de `static/css/styles.css`.

Decisiones que encierra:

- El sistema de diseno (seccion 3.16) describe los componentes con firmas de
  macro: `btn(texto, variante, icono, href)`. **El Django Template Language no
  tiene macros**, y el estandar prohibe cambiar de motor de plantillas
  (`02-stack.md` seccion 4). La forma nativa equivalente es una etiqueta de
  inclusion, que conserva la misma firma: `{% btn "Guardar" "primario" %}`.
  Las plantillas de cada componente viven en `templates/macros/`.
- Intento descartado: resolver los componentes con `{% include %}` suelto y
  `with`. Funciona, pero no valida argumentos, no permite valores por defecto
  y obliga a repetir el nombre del archivo en cada llamada. Un error de
  escritura ahi falla en silencio, mostrando nada.
- El grosor del trazo de los iconos depende del tamano (1.8 en 17 px, 2 en
  15 px o menos, 1.9 en 20 px o mas). Se calcula aqui para que ninguna
  plantilla tenga que recordarlo.
"""

from django import template

register = template.Library()


def _trazo(tam):
    if tam <= 15:
        return "2"
    if tam >= 20:
        return "1.9"
    return "1.8"


@register.inclusion_tag("macros/icon.html")
def icon(nombre, tam=17):
    """Un icono de linea. Siempre decorativo: el significado va en el texto."""
    return {"nombre": nombre, "tam": tam, "trazo": _trazo(tam)}


@register.inclusion_tag("macros/btn.html")
def btn(texto, variante="secundario", icono=None, href=None, tipo="button", extra=""):
    """Boton o enlace con forma de boton. Una accion primaria por pantalla."""
    return {
        "texto": texto,
        "variante": variante,
        "icono": icono,
        "href": href,
        "tipo": tipo,
        "extra": extra,
    }


@register.inclusion_tag("macros/badge.html")
def badge(texto, estado="neutro"):
    """Etiqueta de estado. El texto dice el estado, no lo insinua."""
    return {"texto": texto, "estado": estado}


@register.inclusion_tag("macros/kpi.html")
def kpi(etiqueta, valor, detalle=None, fuente=None):
    """Tarjeta de cifra. La linea de fuente es obligatoria si el dato es ajeno."""
    return {"etiqueta": etiqueta, "valor": valor, "detalle": detalle, "fuente": fuente}


@register.inclusion_tag("macros/campo.html")
def field(tipo, nombre, etiqueta, ayuda=None, error=None, valor="", opcional=False, extra=""):
    """Campo de formulario con su etiqueta, su ayuda y su error."""
    return {
        "tipo": tipo,
        "nombre": nombre,
        "etiqueta": etiqueta,
        "ayuda": ayuda,
        "error": error,
        "valor": valor,
        "opcional": opcional,
        "extra": extra,
    }


@register.inclusion_tag("macros/alert.html")
def alert(texto, estado="info", icono=None):
    """Aviso en linea. No se usa para felicitar: interrumpe la lectura."""
    iconos = {"ok": "check", "aviso": "alerta", "error": "error", "info": "info"}
    return {
        "texto": texto,
        "estado": estado,
        "icono": icono or iconos.get(estado, "info"),
        "rol": "alert" if estado == "error" else "status",
    }


@register.inclusion_tag("macros/vacio.html")
def empty_state(titulo, texto, accion=None, href=None, icono="caja"):
    """Estado vacio. Nunca dice solo «No hay datos»."""
    return {"titulo": titulo, "texto": texto, "accion": accion, "href": href, "icono": icono}


@register.inclusion_tag("macros/migas.html")
def migas(ruta):
    """Ruta de navegacion. El ultimo elemento no es enlace."""
    return {"ruta": ruta}


@register.inclusion_tag("macros/paginacion.html")
def paginacion(pagina, total, por_pagina=9):
    """Paginacion con el conteo a la izquierda."""
    desde = (pagina - 1) * por_pagina + 1 if total else 0
    hasta = min(pagina * por_pagina, total)
    paginas = max(1, -(-total // por_pagina)) if total else 1
    return {
        "pagina": pagina,
        "total": total,
        "desde": desde,
        "hasta": hasta,
        "paginas": range(1, paginas + 1),
    }


@register.inclusion_tag("macros/avatar.html")
def avatar(iniciales, tono="claro", tam="normal"):
    """Avatar con iniciales. No carga imagenes en la fase 0."""
    return {"iniciales": iniciales, "tono": tono, "tam": tam}


@register.inclusion_tag("macros/fuente.html")
def fuente(origen, corte=None):
    """La linea de origen de un dato que no nace en SIRH+ (patron 4.1).

    Es una etiqueta de inclusion y no una que devuelva HTML armado a mano:
    asi el origen y la fecha de corte los escapa la plantilla. Un dato que
    viene de un sistema ajeno no se concatena nunca dentro de una cadena
    marcada como segura.
    """
    return {"origen": origen, "corte": corte}
