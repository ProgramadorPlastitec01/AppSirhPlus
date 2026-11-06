# SIRH+ — Contexto para los agentes

Sistema de Información de Recursos Humanos de **Plastitec S.A.S.**
Reemplaza al SIRH antiguo e integra BioTime y COPEC.

> **Este documento es normativo.** No es una guía de sugerencias ni una lista de buenas intenciones: lo que dice se cumple. Una regla no se pondera contra la prisa del momento. Si una regla parece equivocada, se discute y se corrige aquí —y queda en `docs/trazabilidad.md`—, pero no se ignora en silencio ni se deja «para esta vez».

---

## Lo primero que se lee al retomar

1. `docs/pendientes.md` — qué quedó abierto, bloqueado o a medias
2. La sección de la fase en curso en `claude/02-plan-de-ejecucion-sirh-plus.md`
3. La sección «Estado actual» de este archivo

---

## Estado actual

| | |
|---|---|
| **Fase en curso** | 0 — Cimientos |
| **Entregable en curso** | E0.1 — Repositorio |
| **Última fase cerrada** | ninguna |
| **Fecha de esta nota** | 5 de noviembre de 2026 |

> Al cerrar cada entregable se actualiza esta tabla. Al cerrar una fase se actualiza además la tabla de módulos y las decisiones de dominio.

---

## Qué es este sistema

Una plataforma de Recursos Humanos para **~1.100 personas**: directos, temporales de Granservicios y aprendices SENA. Los contratistas no se registran.

**Una sola aplicación con tres caras:**

| Cara | Quién | Shell |
|---|---|---|
| Pública | Cualquiera, sin sesión | Cabecera superior |
| Colaborador | 1.100 personas, entran dos minutos | Cabecera superior |
| Gestión | RH y jefes, trabajan ocho horas | Barra lateral de 244 px |

El Portal **no es una aplicación aparte**: es la capa de visibilidad de colaborador sobre los mismos módulos. Un módulo, tres vistas.

**SIRH+ absorbe tres sistemas:** el SIRH antiguo, COPEC (divulgación de documentos) y BioTime (marcaciones y turnos).

---

## Las reglas que no se rompen

1. **`dominio/` no importa Django ni hace entrada/salida.** Recibe datos, devuelve resultados. Sus pruebas corren en milisegundos.
2. **El permiso se verifica en el SERVIDOR.** Ocultar un enlace del menú es cortesía visual, no protección.
3. **Los valores van como parámetro** en toda consulta. En el texto del SQL solo se interpolan identificadores de una lista blanca.
4. **Un parámetro legal se guarda con su VIGENCIA**, nunca se sobrescribe. El cálculo busca el valor que regía en la fecha del hecho.
5. **El salario vive en una tabla aparte** (`DatosReservados`) y su consulta se audita. Si no hay permiso, el dato no llega al navegador.
6. **El código de nómina se verifica contra el histórico completo**, no contra los activos. Y no se normalizan los ceros a la izquierda.
7. **La estructura del organigrama se resuelve a una FECHA**, no a hoy. Una solicitud de hace seis meses debe seguir sabiendo quién era el jefe entonces.
8. **Una marcación en un dispositivo no autorizado nunca se descarta.** Se registra y se señala como excepción.
9. **Ningún valor visual fuera de `:root`.** Ni un color, ni un radio, ni un espaciado.
10. **Ningún modelo propio tiene llave foránea hacia el usuario.** Se guarda el identificador y el nombre como texto.

### SIRH+ no gestiona usuarios

**SIRH+ no crea usuarios, no guarda contraseñas y no administra credenciales.** Eso es del gestor de identidad centralizado.

**SIRH+ es la fuente de verdad de las personas.** Cuando RH registra a alguien, SIRH+ le dispara al gestor para que cree la identidad; cuando registra un retiro, le dispara para que la revoque. La relación va de SIRH+ hacia el gestor, no al revés.

**Lo que sí es de SIRH+ son los permisos:** qué puede hacer cada quien dentro de este sistema. Viven en `permisos/`, se construyen de cero, y el gestor no los conoce.

**Dos módulos, no tres:** `identidad/` —autenticar contra el gestor y avisarle de las altas y las bajas— y `permisos/` —catálogo, roles y alcance—. **No existe un módulo `cuentas/` y no va a existir.** No hay nada que copiar del estándar: los dos módulos son propios.

**Mientras el gestor no exista:** la pantalla de ingreso no valida nada. Es una puerta abierta que da acceso durante el desarrollo. **No se construye autenticación local**, ni tabla de usuarios, ni contraseñas, ni «algo provisional» que después haya que desmontar. Cuando el gestor esté listo se escribe `identidad/` y se conecta.

---

## Arquitectura

```
config/  ──▶  módulos  ──▶  dominio/
                  │
                  └──────▶  <fuente>_db/     (solo lectura)
```

Nunca hacia arriba. Nunca circular.

**Orden de construcción dentro de un módulo**, siempre de adentro hacia afuera:

```
1. Migración del modelo
2. dominio/            funciones puras
3. tests/              pruebas con casos límite
4. consultas.py        acceso a datos, parametrizado
5. presentacion.py     arma lo que la plantilla necesita
6. views.py            delgada: recibe, delega, responde
7. templates/          con los cuatro estados
8. Las seis compuertas
```

Una función de `views.py` no pasa de 30 líneas. Si crece, la lógica pertenece abajo.

---

## Stack

Python 3.11+ · Django 5.2 LTS · PostgreSQL 17 · CSS plano y JavaScript vanilla · `unittest` · `ruff` · `django-environ` · Gunicorn tras Nginx en Rocky Linux 9.

**Prohibido:** build de frontend, librerías JavaScript de terceros, recursos desde CDN, escribir en la base de un sistema ajeno, duplicar una regla de negocio en JavaScript.

---

## Las cuatro desviaciones declaradas del estándar

Están justificadas en `claude/02-plan-de-ejecucion-sirh-plus.md` §1.2 y en `docs/diseno.md` §8. **No se corrigen.**

| # | Desviación | Por qué |
|---|---|---|
| **D1** | Cabecera superior en la cara de colaborador, no sidebar | Dos audiencias distintas: ocho horas contra dos minutos |
| **D2** | Permisos granulares por módulo y acción, no dos roles | El sistema maneja salarios, descargos y datos de salud |
| **D3** | El alcance del dato como eje aparte del permiso | Dos roles con el mismo permiso ven conjuntos distintos |
| **D4** | La identidad llega después: ingreso sin validación y `PERMISOS_EXIGIR=false` | El gestor de identidad está en construcción y SIRH+ será su fuente de verdad. Se mitiga corriendo con la verificación exigida una vez por fase |

En las cuatro, **el acceso no se resuelve con el paquete `cuentas/` del estándar**: SIRH+ no gestiona usuarios. La autenticación vive en `identidad/`, contra el gestor, y la autorización dentro del sistema en `permisos/`. Los dos son propios y se construyen de cero. Ver «SIRH+ no gestiona usuarios», arriba.

La regla de frontend del estándar está **reemplazada** por `.claude/rules/03-sistema-de-diseno.md`.

---

## Decisiones de dominio que hay que conocer

**Los tres identificadores de una persona son distintos y no se mezclan:** documento, código interno (= el del biométrico y la firma) y código de nómina (cédula + un dígito según el vínculo, parametrizable).

**El registro se completa por hitos, no por campos.** De 10 % a 100 %, cada hito con su dueño y su consecuencia. El umbral operativo es el **40 %**: bajo eso la persona no puede trabajar. Un registro bajo el 40 % vale 24 horas.

**El cargo deriva seis cosas:** área, nivel, jefe, matriz de capacitación, turno habitual y punto de marcación. Se muestran para confirmar, no se digitan.

**Un punto de marcación es un conjunto de dispositivos**, no un equipo. Los cuatro vestieres de mujeres son un solo punto.

**El motor de registros firmados es uno solo** para siete documentos: formato versionado → diligenciar → firmas en orden → folio → cierre inmutable → PDF.

**La firma se captura una vez y se invoca con la clave propia del colaborador.** Antes se usaban cédula y código interno, que otras personas conocen.

**El ciclo de nómina va del 11 al 10.** La semana operativa arranca el domingo a las 22:00.

---

## Vocabulario

Términos fijos. Se usan en la interfaz **y en el código**.

| Término | Nombre en código |
|---|---|
| Colaborador | — |
| Eventualidad | `Eventualidad` |
| Trámite | `Tramite` |
| Divulgación | `Divulgacion` |
| Constancia | `ConstanciaLectura` |
| Registro (formato con folio) | `Registro` |
| Marcación | `Marcacion` |
| Jornada | `Jornada` |
| Turno · bloque | `Turno`, `BloqueTurno` |
| Punto de marcación | `PuntoMarcacion` |
| Programación | `Programacion` |
| Período | `Periodo` |
| Horas pendientes | `pendiente_min` |

**No se usa** «evento», «seguimiento» ni «empleado» en la interfaz.

---

## Módulos construidos

| Módulo | Fase | Qué hace |
|---|---|---|
| _ninguno todavía_ | — | — |

---

## Las seis compuertas

Una fase está terminada cuando las seis pasan. Ninguna es opcional.

| # | Compuerta | Cómo |
|---|---|---|
| 1 | Formato y lint | `ruff format .` y `ruff check .` |
| 2 | Pruebas del núcleo | `python -m unittest discover -s tests` |
| 3 | Chequeo de salud | `python manage.py smoke_test` y `/salud/` |
| 4 | Seguridad | `python manage.py check --deploy` |
| 5 | Visual y cuatro estados | Cada pantalla contra su mockup |
| 6 | **Validación humana** | Sebastián la usa contra un caso real, luego el QA |

---

## Nada se acumula

Las compuertas dicen cuándo termina una fase. Esta sección dice cuándo termina un entregable, que es donde empieza la deuda. Un sistema de 28 módulos no se degrada de golpe: se degrada por un aviso que nadie cerró, repetido cien veces.

**1 · Un aviso es un error.** Si `ruff`, Django, Python o el navegador emiten un aviso, se arregla antes de seguir. No se reporta: se cierra. Un aviso que sobrevive a una sesión ya es deuda, y la deuda que nadie escribió es la que nunca se paga.

**2 · No se entrega nada con pendientes pequeños.** Si al terminar un entregable quedan tres cosas menores, el entregable **no está terminado**. Se cierran, y después se reporta. «Listo, salvo dos detalles» no es listo.

**3 · Si un arreglo abre otro problema, se para.** No se encadenan correcciones. Se deshace lo que se tocó, se explica qué pasó y se pregunta. Una bola de nieve de errores cuesta más que una sesión perdida.

**4 · Lo que no se puede cerrar va a `docs/pendientes.md` el mismo día**, con qué es, por qué no se cerró y quién lo destraba. No se menciona de pasada en una respuesta y se olvida: lo que solo vive en una conversación desaparece con ella.

**5 · No se inventan problemas.** Si algo funciona y cumple el plan, está bien. No se abren frentes que nadie pidió, ni se «mejora de paso» lo que ya estaba cerrado.

**6 · Una cosa a la vez.** Si en medio de un entregable aparece algo bueno que no es de ese entregable, va a `docs/pendientes.md`. **No al código.**

El objetivo de estas reglas es que al terminar cada entregable el repositorio esté limpio: sin avisos, sin cabos sueltos, sin «lo vemos después». Si eso no se puede, el entregable no está listo y **hay que decirlo claramente**, no entregarlo con notas al pie.

---

## Postura sobre HTTPS y `check --deploy`

El estándar (`.claude/rules/04-seguridad.md` §6) exige que esto quede escrito. Un silencio aquí no es una postura.

**En desarrollo local** se aceptan los avisos que se derivan de `DEBUG=True` y de la ausencia de HTTPS, y solo esos:

- `security.W004` — `SECURE_HSTS_SECONDS` sin definir
- `security.W008` — `SECURE_SSL_REDIRECT` en falso
- `security.W012` — `SESSION_COOKIE_SECURE` en falso
- `security.W016` — `CSRF_COOKIE_SECURE` en falso

**Cualquier otro hallazgo de `check --deploy` se arregla.** No se silencia con `SILENCED_SYSTEM_CHECKS` ni se deja «para después».

**En producción, HTTPS es obligatorio y `check --deploy` debe salir sin ningún hallazgo.** El sistema sale solo a la red interna en su primera etapa, y eso **no** exime del certificado: la red interna es donde están las 1.100 personas cuyos salarios y datos de salud viajan por ese cable.

---

## Qué no hacer

- No construir algo de una fase posterior porque «ya que estamos»
- No agregar campos al modelo «por si acaso»
- No crear una abstracción para un caso que todavía no existe
- No tocar código de una fase cerrada salvo para corregir un defecto
- No usar `--no-verify`
- Si aparece una idea buena que no es de esta fase, va a `docs/pendientes.md`, **no al código**
- Ante una duda de negocio, preguntar. **No inventar**

---

## Intentos fallidos y por qué

Decisiones que se tomaron y se revirtieron. Están aquí para no repetirlas.

| Qué se probó | Por qué no funcionó |
|---|---|
| Java 21 + Spring Boot | Sería la única app Java de la empresa; el estándar no aplicaría |
| El Portal como aplicación aparte | Habría duplicado la regla de negocio de cinco módulos |
| Porcentaje de completitud por campos contados | Promedia cosas que no pesan igual y da tranquilidad falsa |
| Firma invocada con cédula y código interno | Los dos datos los conocen otras personas |
| Dimensionar sobre 500 personas | Son ~1.100. Verificar las cifras que fundamentan decisiones |

---

## Mapa de documentos

| Archivo | Para qué |
|---|---|
| `claude/00-contexto-maestro-sirh-plus.md` | El proyecto completo y el porqué de cada decisión |
| `claude/01-inventario-y-fases-sirh-plus.md` | 28 módulos, 314 funciones, 23 fases |
| `claude/02-plan-de-ejecucion-sirh-plus.md` | **Normativo.** Reglas, compuertas, fases 0 a 3 en detalle |
| `.claude/rules/03-sistema-de-diseno.md` | **Normativo.** Tokens, componentes, patrones |
| `mockups/mockup-sirh-plus-completo.html` | 17 pantallas de la cara de gestión |
| `mockups/mockup-portal/` | La cara de colaborador |
| `docs/trazabilidad.md` | Cada decisión con su porqué |
| `docs/pendientes.md` | Lo abierto, lo bloqueado, la deuda asumida |
| `docs/glosario.md` | Vocabulario, en interfaz y en código |

**Precedencia:** si un documento contradice al código, gana el código y hay que corregir el documento. Si contradice al estándar, gana el estándar, salvo donde aquí se declare una desviación.
