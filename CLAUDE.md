# SIRH+ — Contexto para los agentes

Sistema de Información de Recursos Humanos de **Plastitec S.A.S.**
Reemplaza al SIRH antiguo e integra BioTime y COPEC.

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

Una función de `views.py` no debería pasar de 30 líneas. Si crece, la lógica pertenece abajo.

---

## Stack

Python 3.11+ · Django 5.2 LTS · PostgreSQL 17 · CSS plano y JavaScript vanilla · `unittest` · `ruff` · `django-environ` · Gunicorn tras Nginx en Rocky Linux 9.

**Prohibido:** build de frontend, librerías JavaScript de terceros, recursos desde CDN, escribir en la base de un sistema ajeno, duplicar una regla de negocio en JavaScript.

---

## Las tres desviaciones declaradas del estándar

Están justificadas en `claude/02-plan-de-ejecucion-sirh-plus.md` §1.2. **No se corrigen.**

| # | Desviación | Por qué |
|---|---|---|
| **D1** | Cabecera superior en la cara de colaborador, no sidebar | Dos audiencias distintas: ocho horas contra dos minutos |
| **D2** | Permisos granulares por módulo y acción, no dos roles | El sistema maneja salarios, descargos y datos de salud |
| **D3** | El alcance del dato como eje aparte del permiso | Dos roles con el mismo permiso ven conjuntos distintos |

En las tres, **`cuentas/` no se modifica**. El estándar resuelve el acceso a la aplicación; SIRH+ resuelve la autorización dentro, en un módulo `permisos/` propio.

`.claude/rules/03-frontend-ux.md` está **reemplazada** por `claude/03-sistema-de-diseno.md`.

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
| `claude/03-sistema-de-diseno.md` | **Normativo.** Tokens, componentes, patrones |
| `mockups/mockup-sirh-plus-completo.html` | 17 pantallas de la cara de gestión |
| `mockups/mockup-portal/` | La cara de colaborador |
| `docs/trazabilidad.md` | Cada decisión con su porqué |
| `docs/pendientes.md` | Lo abierto, lo bloqueado, la deuda asumida |
| `docs/glosario.md` | Vocabulario, en interfaz y en código |

**Precedencia:** si un documento contradice al código, gana el código y hay que corregir el documento. Si contradice al estándar, gana el estándar, salvo donde aquí se declare una desviación.
