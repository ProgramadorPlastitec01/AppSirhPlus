# Trazabilidad de decisiones

Una entrada por decisión. **No se borran ni se editan: se agregan.** Si una decisión se revierte, se escribe una entrada nueva que la reemplaza y se marca la anterior como superada.

El formato está al final. Las entradas van de la más reciente a la más antigua.

---

## 2026-11-06 · SIRH+ no gestiona usuarios: `cuentas/` no existe y no va a existir

**Fase:** 0
**Qué se decidió:** SIRH+ no crea usuarios, no guarda contraseñas y no administra credenciales. Eso es del gestor de identidad centralizado. SIRH+ es la **fuente de verdad de las personas**: el alta de un registro dispara la creación de la identidad y el retiro dispara su revocación. La relación va de SIRH+ hacia el gestor.

Los permisos sí son de SIRH+: viven en `permisos/`, se construyen de cero y el gestor no los conoce. Los módulos son dos —`identidad/` y `permisos/`— y **ninguno se llama `cuentas/`**.

Mientras el gestor no exista, la pantalla de ingreso no valida nada: es una puerta abierta durante el desarrollo. **No se construye autenticación local**, ni tabla de usuarios, ni contraseñas, ni nada provisional.

**Por qué:**
Los documentos venían diciendo dos cosas a la vez. Por un lado, que `cuentas/` se copiaba del estándar sin modificar y que un «adaptador local transitorio» viviría detrás de su interfaz, leyendo de una tabla propia de desarrollo. Por otro, que el gestor de identidad sería alimentado por SIRH+. Las dos no caben juntas: la primera convierte a SIRH+ en un consumidor más de la tabla `usuario` del estándar, y de paso le pide construir —para tirar después— un maestro de usuarios local con sus contraseñas.

Un maestro de usuarios provisional es la clase de cosa que no se desmonta nunca. Y mientras exista, hay dos sitios donde vive una credencial, que es exactamente lo que el estándar intenta evitar con una sola base de identidad.

**Qué se corrigió:**

| Dónde | Qué quedó |
|---|---|
| `CLAUDE.md` | Regla nueva, «SIRH+ no gestiona usuarios», en la sección de las reglas que no se rompen. La D4 ya no menciona el adaptador |
| `claude/02` §1.2 | La D4 dice qué se construye —una pantalla de ingreso que no valida— y qué **no**: autenticación local, tabla de usuarios, contraseñas ni nada provisional |
| `claude/02` E0.2 y E1.6 | El esqueleto no lleva paquete de identidad. E1.6 pasó de «Adaptador de identidad» a «Identidad: lo que esta fase no construye» |
| `claude/01` A.2 | El módulo es `identidad/` y se escribe cuando el gestor exista. El cambio de contraseña salió de la lista: es del gestor |
| `claude/00` §21 y el árbol | `identidad/` y `permisos/` en lugar de `cuentas/`; `permisos/roles.py` en lugar de `cuentas/roles.py` |
| `docs/diseno.md` §3 y §8 | La tabla de módulos lista `identidad/` y `permisos/`, los dos propios |
| `.claude/rules/07` | Nota en el encabezado: SIRH+ se aparta de esa regla porque es la fuente de verdad del gestor, no un consumidor más |
| `.claude/rules/05` | El checklist ya no pide copiar `cuentas/`, y separa lo que se difiere de lo que no llega nunca |
| `.env.example` | Se eliminó `IDENTIDAD_ADAPTADOR`. No queda ninguna variable de autenticación |
| `docs/pendientes.md` | La deuda D4 es ahora la pantalla de ingreso sin validación, no el adaptador |

**Qué se evaluó y se descartó:**

| Opción | Por qué no |
|---|---|
| Conservar el adaptador local «por si el gestor se demora» | Es construir un maestro de usuarios para desmontarlo. Mientras exista, hay dos sitios donde vive una credencial |
| Llamar `cuentas/` al módulo propio, para no separarse del nombre del estándar | El nombre del estándar trae su contenido: un paquete idéntico en todas las apps, conectado por ORM a la base de identidad. SIRH+ no hace eso |
| Reescribir `.claude/rules/07` para que no hable de `cuentas/` | Es el estándar, y la desviación solo se entiende contra él. Se le puso una nota al encabezado, no se le cambió el cuerpo |
| Dejar la autenticación fuera de todo módulo y resolverla en `core/` | La autenticación tiene un sistema ajeno al otro lado. Merece su capa, como `glpi_api/` o `daruma_db/` |

**Qué cambia si esto resulta equivocado:**
Si el gestor se demora más allá de la fase 3, SIRH+ llega a producción sin poder salir —no sale sin él— y hay que decidir entonces. La decisión de hoy hace que ese día no haya nada que desmontar: lo que falta es escribir `identidad/`, no deshacer un provisional. El riesgo que sí corre es de desarrollo: una pantalla de ingreso que no valida nada da acceso a cualquiera que alcance el servidor, y por eso **nunca sale de la red de desarrollo**.

---

## 2026-11-06 · Corrección documental previa a la fase 0

**Fase:** 0
**Qué se decidió:** corregir nueve contradicciones entre los documentos **antes** de escribir la primera línea de código, y cerrar con una decisión escrita las cinco que no eran solo una referencia rota.

**Por qué:**
Una lectura completa de los dieciséis documentos, hecha para arrancar la fase 0, encontró que los documentos se contradecían entre sí en cosas que cambian lo que se construye. La lección L7 del estándar dice que una afirmación que el código contradice desinforma a quien la lee después; aquí todavía no hay código, así que lo barato era corregir los documentos ahora.

**Qué se corrigió:**

| # | Qué estaba mal | Qué quedó |
|---|---|---|
| 1 | `claude/02` §1.2 declaraba **tres** desviaciones; `docs/diseno.md` §8 y el checklist declaraban cuatro, y citaban §1.2 como fuente de la D4 | La D4 —la identidad diferida— se declaró en el documento normativo, con el mismo formato que las otras tres. `CLAUDE.md` pasó a cuatro |
| 2 | Las seis compuertas eran distintas en tres documentos: `claude/00` §23.1 y `claude/01` no incluían el lint y separaban visual de cuatro estados | `claude/00` y `claude/01` ahora dicen lo mismo que `claude/02` §0.3, y remiten a él como versión normativa |
| 3 | Seis archivos citaban `claude/03-sistema-de-diseno.md`, que no existe; y se citaban `03-frontend-ux.md`, `04-modulo-marcaciones.md`, `08-modulo-marcaciones.md`, `13-sistema-de-diseno.md` y un mapa de documentos con la numeración vieja completa | Todas las rutas apuntan a `.claude/rules/03-sistema-de-diseno.md`. El mapa de `claude/00` §27 lista los archivos que existen. El documento de marcaciones se nombra por lo que es: por escribir, antes de la fase 6 |
| 4 | `claude/02` citaba seis artboards como archivos `*.dc.html` que no existen | Se reemplazaron por los ids reales (`v-permisos`, `v-usuarios`, `v-cargos`, `v-estructura`, `v-organigrama`, `v-hoja`) y §0.1 aclara que los artboards de gestión son secciones con id dentro de `mockups/mockup-sirh-plus-completo.html` |
| 5 | `parametros/` estaba en la fase 5, pero la fase 3 necesita dos parámetros: el plazo del registro incompleto y los sufijos del código de nómina | Se partió en dos. **E3.9** crea el modelo `Parametro`, su vigencia y `dominio/parametros.vigente_en()`, sin pantalla. La fase 5 entrega la administración, el catálogo por módulo, el historial y los festivos |
| 6 | La compuerta 4 exige `check --deploy` **sin hallazgos**, y en local eso es inalcanzable con `DEBUG=True` y sin HTTPS. El estándar exige además que la postura sobre HTTPS en red interna quede escrita, y no estaba | `CLAUDE.md` tiene una sección con los cuatro avisos que se aceptan en local y la regla de que cualquier otro se arregla. En producción, HTTPS obligatorio y cero hallazgos: la red interna no exime del certificado |
| 7 | E0.2 pedía `base_auth.html` y el sistema de diseño definía tres caras, sin decir qué shell usa el ingreso | El ingreso **hereda de `base_publico.html`**, centrado y sin navegación. Es la puerta de entrada de las tres caras, no una cuarta. Quedó como §2.4 del sistema de diseño, y su referencia visual es `mockups/mockup-portal/Login.dc.html` |
| 8 | El árbol del `README.md` aplanaba los dos niveles de `.claude/rules/01-estructura-y-capas.md` §1 y no mostraba `manage.py` | Dos niveles, como el estándar: la carpeta del repositorio con la configuración y los documentos, y dentro `sirh_plus/` con `manage.py` junto a `config/` |
| 9 | `README.md` pedía cuatro comandos antes de cada commit, incluyendo `manage.py test`, que no es compuerta, y dejando fuera `check --deploy`, que sí lo es. `docs/diseno.md` §4 titulaba «en modo lectura» una tabla con dos capas de escritura | Antes de un commit van tres: `ruff format`, `ruff check` y las pruebas del núcleo. La tabla de sistemas ajenos tiene columna de modo, y queda dicho que lo prohibido es escribir en la **base** de un sistema ajeno, no llamar a su API |

**Qué se evaluó y se descartó:**

| Opción | Por qué no |
|---|---|
| Quitar la D4 de `docs/diseno.md` para que fueran tres | La D4 es la desviación de mayor impacto operativo: es la que apaga la verificación de permisos. Borrarla del papel no la quita del sistema |
| Dejar las tres versiones de las compuertas y confiar en la regla de precedencia | Un agente que lea el maestro primero correría cinco compuertas creyendo que corrió seis |
| Mover `parametros/` entero a la fase 3 | La fase 3 necesita dos parámetros, no un módulo de administración. Adelantarlo completo contradice «no construir algo de una fase posterior» |
| Guardar los dos parámetros de la fase 3 como constantes en código | RN-04 dice que el sufijo del código de nómina es parametrizable por RH. Una constante hoy es una migración de datos mañana |
| Darle al ingreso su propio shell | Son tres caras, no cuatro. Un cuarto shell es un cuarto sitio donde divergir |
| Aplanar el árbol y poner `manage.py` en la raíz | Habría sido una quinta desviación del estándar, sin más razón que la comodidad |

**Qué cambia si esto resulta equivocado:**
Bajo, salvo en dos puntos. El **E3.9** es la única corrección que mueve alcance: si resulta que la fase 3 no necesitaba el modelo de parámetros, sobra un modelo de dos tablas y se arrastra a la fase 5, que es donde iba. Y la **postura sobre HTTPS**: si se decide que la red interna sí exime del certificado, hay que reescribirla y decir por qué — pero escrita, porque el estándar no admite el silencio.

**Lo que esta corrección no tocó:** ninguna regla de negocio, ninguna decisión de diseño, ningún mockup. Las cuatro desviaciones no se corrigen: se declaran.

---

## 2026-11-05 · Un punto de marcación es un conjunto de dispositivos

**Fase:** 2
**Qué se decidió:** el cargo apunta a un **punto de marcación**, que agrupa varios dispositivos, no a un biométrico concreto.

**Por qué:**
En los datos reales hay cuatro dispositivos llamados «Vestier Mujeres 1 a 4». Para una operaria son el mismo punto: entra por el que esté libre. Si el cargo apuntara a un dispositivo, el sistema marcaría como irregular algo perfectamente normal.

Además se decidió que **una marcación en un dispositivo no autorizado nunca se descarta**: se registra y se señala como excepción. Descartarla sería perder un dato que vale dinero, y el sistema no debe decidir quién trabajó.

El punto lo define el cargo, puede cambiarse por persona con motivo y vigencia, y lo que no encaje sale como excepción.

**Qué se evaluó y se descartó:**

| Opción | Por qué no |
|---|---|
| Cargo → un dispositivo | Los cuatro vestieres son intercambiables para la misma persona |
| Persona → dispositivos, sin pasar por el cargo | Se vuelve inmanejable con 1.100 personas y no expresa la regla real |
| Rechazar la marcación fuera de punto | Se pierde un dato que vale dinero |

**Qué cambia si esto resulta equivocado:**
Bajo. El modelo de punto puede colapsarse a un dispositivo si resulta que cada cargo tiene uno solo, sin tocar nada más.

---

## 2026-11-05 · La completitud se mide por hitos, no por campos

**Fase:** 3
**Qué se decidió:** el registro de una persona se completa por siete hitos con nombre, de 10 % a 100 %, cada uno con su dueño y su consecuencia.

**Por qué:**
Un porcentaje calculado contando campos promedia cosas que no son comparables: el número de hijos y el código de nómina no pesan igual. Y da tranquilidad falsa — un 92 % se siente terminado, y lo que falta puede ser justo lo que bloquea la nómina.

Con hitos, el 70 % deja de ser un número y pasa a significar «le falta liquidación», con un dueño concreto.

Se fijó además que **el umbral operativo es el 40 %**: bajo ese nivel la persona no puede trabajar, porque el biométrico no la reconoce y nadie puede aprobarle nada. Un registro bajo el 40 % vale 24 horas, parámetro `personal.plazo_incompleto`.

**Qué se evaluó y se descartó:**

| Opción | Por qué no |
|---|---|
| Porcentaje por campos llenos | Iguala lo que no pesa igual |
| Solo dos estados: completo o incompleto | No dice qué falta ni a quién le toca |
| Hitos parametrizables por RH | El porcentaje dejaría de ser comparable entre dos momentos |

**Qué cambia si esto resulta equivocado:**
Medio. Los pesos se pueden recalibrar, pero cambiarlos invalida la comparación histórica. Por eso no son parametrizables.

---

## 2026-11-05 · La captura rápida es una pantalla aparte de la carga masiva

**Fase:** 3
**Qué se decidió:** dos pantallas distintas. Captura rápida de cinco campos con guardado sin recarga, y carga masiva desde planilla. La foto va a una cola propia.

**Por qué:**
Son necesidades diferentes. La captura rápida resuelve «hay quince personas esperando con su cédula en la mano»; la carga masiva resuelve «Granservicios envió una planilla». Una importación de Excel no sirve si estás en el salón tomando fotos.

El cargo deriva seis cosas —área, nivel, jefe, matriz, turno y punto de marcación—, así que no se preguntan. Eso baja la captura a cinco campos, y tres salen del documento que la persona tiene en la mano.

**La foto no pesa en la completitud.** Si pesara, media planta quedaría atascada por algo que no depende de quien registra.

**Qué cambia si esto resulta equivocado:**
Bajo. Son dos pantallas sobre el mismo modelo.

---

## 2026-11-05 · El código interno lo propone el sistema y se puede sobrescribir

**Fase:** 3
**Qué se decidió:** el campo se precarga con el siguiente consecutivo libre y admite edición, con validación de unicidad al escribir.

**Por qué:**
Estaba definido como generado por el sistema. Pero hay personas que llegan con un código ya asignado. Proponer y permitir sobrescribir cubre los dos casos sin ramificar la lógica.

**Supera a:** la decisión original de generarlo sin posibilidad de edición.

---

## 2026-11-05 · El sistema de diseño se escribe de cero

**Fase:** 0
**Qué se decidió:** vaciar `.claude/rules/03-frontend-ux.md` y reemplazarla por un sistema de diseño propio, derivado del mockup del Portal.

**Por qué:**
El estándar fija un sidebar de 220 px para toda pantalla con sesión. El mockup del Portal se construyó con cabecera superior, deliberadamente: un portal para 1.100 personas que no quieren entrar a un sistema no se ve como una herramienta interna de RH.

Mantener las dos reglas en el repositorio habría dejado a los agentes eligiendo entre dos verdades.

**Es la desviación D1**, declarada en el plan de ejecución §1.2.

---

## 2026-11-05 · Permisos granulares con el alcance como eje aparte

**Fase:** 1
**Qué se decidió:** catálogo de permisos por módulo y acción, declarado en código, agrupado en roles que define TI. El alcance del dato —propio, área, rama, todo— se modela aparte del permiso.

**Por qué:**
El estándar fija dos roles iguales en todas las aplicaciones. SIRH+ maneja salarios, procesos disciplinarios y datos de salud ocupacional: dos roles no pueden expresar que un analista vea el salario pero no lo edite.

El alcance va aparte porque dos usuarios con el mismo `personal.ver` deben ver conjuntos de personas distintos. Mezclarlo con el permiso multiplicaría el catálogo por cuatro.

**Cómo se respeta el estándar:** `cuentas/` no se modifica. El estándar resuelve el acceso a la aplicación; SIRH+ resuelve la autorización dentro, en un módulo `permisos/` propio.

> **Esta última frase quedó superada** el 6 de noviembre de 2026: SIRH+ no usa `cuentas/` en absoluto. El resto de la entrada sigue vigente. Ver «SIRH+ no gestiona usuarios», arriba.

**Qué se evaluó y se descartó:**

| Opción | Por qué no |
|---|---|
| Dos roles, como el estándar | No expresa ver-sin-editar sobre datos sensibles |
| Permisos por usuario, como el SIRH viejo | 1.143 filas para 56 usuarios, replicadas a mano |
| El alcance como un permiso más | Multiplica el catálogo por cuatro |

**Son las desviaciones D2 y D3.**

---

## 2026-11-05 · El catálogo de permisos existe desde la fase 1, con interruptor

**Fase:** 1
**Qué se decidió:** el catálogo completo se declara en la fase 1 aunque la verificación esté apagada, con un parámetro `PERMISOS_EXIGIR` que la hace exigible.

**Por qué:**
El SIRH actual tiene autorización cosmética porque los permisos se agregaron al final, sobre un sistema ya construido. Si repetimos ese orden, llegamos al mismo lugar.

Con el interruptor se puede correr la aplicación con la verificación exigida al menos una vez por fase y revisar el registro, antes de que sea tarde.

---

## 2026-11-05 · El salario vive en una tabla aparte

**Fase:** 3
**Qué se decidió:** `DatosReservados` es un modelo propio, no columnas de `Vinculo`.

**Por qué:**
Así el permiso se aplica a nivel de consulta y el dato **no viaja al navegador** de quien no debe verlo. Ocultarlo con CSS no es protección: basta abrir las herramientas del navegador.

---

## 2026-11-05 · Los disparadores salen por outbox

**Fase:** 3
**Qué se decidió:** al registrar una persona se escribe la intención en una tabla y un proceso aparte la ejecuta contra GLPI y el gestor de identidad.

**Por qué:**
Si GLPI está caído, RH igual tiene que poder registrar a alguien que ya llegó a trabajar. Llamar la API en línea haría que un sistema externo bloqueara el ingreso.

---

## 2026-11-04 · Empresa se construye antes que Personal

**Fase:** 2 antes que 3
**Qué se decidió:** áreas, cargos y estructura van en la fase 2; personas en la fase 3.

**Por qué:**
Una persona necesita un cargo que exista, y ese cargo necesita saber a quién reporta. Sin eso no hay a quién enrutar una solicitud, ni quién evalúa a quién, ni qué personal ve cada jefe.

Suena al revés, pero son dos semanas antes que evitan rehacer el enrutamiento después.

---

## 2026-11-04 · El Portal no es una aplicación aparte

**Fase:** transversal
**Qué se decidió:** el Portal del Colaborador es la capa de visibilidad de colaborador sobre los mismos módulos. Un módulo, tres vistas.

**Por qué:**
Trámites aparecía dos veces en el alcance —solicitar y aprobar—, y lo mismo capacitaciones, encuestas, marcaciones y competencias. Construirlo dos veces habría duplicado la regla de negocio de cinco módulos y las dos versiones habrían divergido en seis meses.

**Supera a:** el diseño del documento 06, que planteaba el Portal como sistema separado.

---

## 2026-11-03 · Parámetros legales con vigencia por fecha

**Fase:** 5, aplicado desde la 1
**Qué se decidió:** un parámetro legal se guarda como valor más fecha desde la que rige. Nunca se sobrescribe. El cálculo busca el vigente en la fecha del hecho.

**Por qué:**
No es una hipótesis: la jornada semanal viene bajando por etapas, el recargo dominical viene subiendo por etapas, y la hora de inicio de la franja nocturna cambió por reforma. En los archivos reales del sistema actual conviven tres escalones distintos de la misma norma al mismo tiempo.

Sin vigencia, recalcular un mes ya cerrado da un resultado distinto al que se pagó y no hay forma de defenderlo ante una auditoría.

---

## 2026-10-28 · El stack es el estándar de Plastitec

**Fase:** 0
**Qué se decidió:** Python 3.11, Django 5.2 LTS, PostgreSQL 17, CSS plano y JavaScript vanilla, sin build de frontend.

**Por qué:**
La primera recomendación de este proyecto fue Java 21 con Spring Boot, por continuidad con el SIRH actual. **Ese argumento identificaba mal el activo.** El activo no es el código Java del SIRH —ese se descarta completo—: es el estándar de desarrollo de Plastitec y las aplicaciones que ya corren sobre él.

Construir en Java significaría ser la única aplicación Java de la organización, mantenida por una sola persona, con los agentes y las reglas del estándar sin aplicar, a cambio de reutilizar conocimiento de un código que de todas formas se bota.

**Qué se evaluó y se descartó:**

| Opción | Por qué no |
|---|---|
| Java 21 + Spring Boot | Única app Java; el estándar no aplicaría |
| Mantener Java 8 + JSP | Fuera de soporte. Nacería obsoleto |
| Microservicios | Resuelven escalado independiente y equipos separados. No existe ninguno de los dos problemas |
| SPA con React y API | Dos aplicaciones para una persona, sobre pantallas que son formularios y tablas |
| Low-code | Licencia recurrente, dependencia del proveedor y techo en la lógica de nómina |
| HTMX | Lo que el sistema necesita está cubierto por CSS y JS plano |

**Supera a:** la recomendación del documento 02.

---

## 2026-09-29 · Se reconstruye, no se refactoriza

**Fase:** decisión fundacional
**Qué se decidió:** se reconstruye la capa de aplicación y se rediseña el modelo de datos. El SIRH antiguo opera en paralelo hasta que cada módulo esté reemplazado.

**Por qué:**
El diagnóstico encontró inyección SQL en 245 consultas sin una sola parametrizada, contraseñas en MD5 con retroceso a texto plano, autorización puramente cosmética, 3.394 líneas de HTML concatenado en un solo método, y ningún control de versiones.

No es un sistema viejo pero sano. Refactorizar en sitio cuesta más que reconstruir y deja los problemas estructurales intactos.

Lo que se conserva no es el código: es el **conocimiento funcional** —los 211 procedimientos almacenados, el modelo de datos, el mapa de módulos y los datos históricos.

---

## Formato de una entrada

```markdown
## <AAAA-MM-DD> · <título de la decisión>

**Fase:** <N>
**Qué se decidió:** <una frase>

**Por qué:**
<el razonamiento, no la conclusión>

**Qué se evaluó y se descartó:**
| Opción | Por qué no |
|---|---|

**Qué cambia si esto resulta equivocado:**
<el costo de revertirla>
```

Campos opcionales: **Supera a:** cuando reemplaza una decisión anterior.
