# Trazabilidad de decisiones

Una entrada por decisión. **No se borran ni se editan: se agregan.** Si una decisión se revierte, se escribe una entrada nueva que la reemplaza y se marca la anterior como superada.

El formato está al final. Las entradas van de la más reciente a la más antigua.

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
