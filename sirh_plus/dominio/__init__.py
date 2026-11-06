"""Nucleo de dominio de SIRH+: reglas de negocio puras.

Este paquete **no importa Django**, no toca la base de datos, no lee archivos
y no sabe quien es el usuario. Recibe datos ya consultados y devuelve
resultados. Si una regla depende del rol, el rol llega como parametro.

Decisiones que encierra:

- Es el piso de la arquitectura (`config/ -> modulos -> dominio/`): no importa
  nada del proyecto, para que sus pruebas corran en milisegundos sin levantar
  el servidor ni la base. Una suite que tarda segundos se corre en cada
  cambio; una que tarda minutos se deja de correr.
- Esta vacio en la fase 0 a proposito. El primer modulo que entra es
  `parametros.vigente_en()`, en la fase 3 (E3.9). No se crean abstracciones
  para casos que todavia no existen.

Este archivo es la fachada del paquete: lo que se exponga aqui es lo que el
resto del sistema puede importar.
"""
