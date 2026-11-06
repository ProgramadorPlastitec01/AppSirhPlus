# SIRH+ — Diseño

**Estado: validado por el humano el 5 de noviembre de 2026.**
Versión 1.0 · Plastitec S.A.S. · Tecnología de Información

---

## Cómo leer este documento

Este archivo existe porque los agentes `developer` y `qa` lo exigen: el primero se detiene si no existe, el segundo parte de él y no del razonamiento de quien implementó.

**No repite el diseño: lo indexa.** El diseño de SIRH+ se produjo antes de crear el repositorio y vive en cuatro documentos. Este archivo recorre las nueve secciones que pide el agente `arquitecto` y apunta a dónde está cada una.

| Documento | Qué contiene |
|---|---|
| `claude/00-contexto-maestro-sirh-plus.md` | El proyecto completo y el porqué de cada decisión |
| `claude/01-inventario-y-fases-sirh-plus.md` | 28 módulos, 314 funciones, 23 fases |
| `claude/02-plan-de-ejecucion-sirh-plus.md` | **Normativo.** Reglas, compuertas, fases 0 a 3 en detalle |
| `.claude/rules/03-sistema-de-diseno.md` | **Normativo.** Tokens, componentes, patrones de pantalla |
| `mockups/mockup-sirh-plus-completo.html` | 17 pantallas de la cara de gestión |
| `mockups/mockup-portal/` | La cara de colaborador |

**Precedencia:** si este archivo contradice a uno de los cuatro, gana el otro y hay que corregir este. Si contradice al código, gana el código.

**Este diseño cubre las fases 0 a 3.** De la fase 4 en adelante, cada una se detalla en el plan de ejecución justo antes de empezarla, y entonces se amplía este documento.

---

## 1 · Problema y usuario

Plastitec tiene unas **1.100 personas** entre directos, temporales de Granservicios y aprendices SENA. Su sistema de Recursos Humanos está en Java 8 sobre JSP, sin control de versiones, con inyección SQL en 245 consultas, contraseñas en MD5 y autorización puramente cosmética. No se puede mantener ni asegurar.

SIRH+ lo reemplaza, **absorbe COPEC** (divulgación de documentos de calidad) y **absorbe BioTime** (marcaciones, turnos y cálculo de horas), y agrega la cara de autoservicio que hoy no existe.

**Tres audiencias, una sola aplicación:**

| Cara | Quién | Qué necesita |
|---|---|---|
| Pública | Cualquiera, sin sesión | Noticias, organigrama, convocatorias |
| Colaborador | 1.100 personas, entran dos minutos | Lo suyo, y solo lo suyo |
| Gestión | RH y jefes, trabajan ocho horas | Su personal, o toda la empresa según el rol |

El detalle está en `claude/00`, §1 y §2.

---

## 2 · Reglas de negocio

Las reglas están enumeradas en `claude/00` §5, §8 y §10, y en `claude/02` §1. Las que gobiernan las fases 0 a 3:

| # | Regla |
|---|---|
| RN-01 | Una persona tiene **tres identificadores distintos**: documento, código interno (el del biométrico y la firma) y código de nómina (cédula más un dígito según el vínculo) |
| RN-02 | El código de nómina **se verifica contra el histórico completo**, no contra los activos. Un temporal que pasó a directo y reingresa puede colisionar |
| RN-03 | El código de nómina **no normaliza ceros a la izquierda**. La herramienta anterior lo hacía y eso puede liquidar mal a alguien |
| RN-04 | El sufijo del código de nómina **es parametrizable**: RH puede cambiar la política sin tocar código |
| RN-05 | El registro de una persona se completa por **siete hitos**, de 10 % a 100 %, cada uno con su dueño y su consecuencia |
| RN-06 | El **umbral operativo es el 40 %**. Bajo ese nivel la persona no puede trabajar. Un registro bajo el 40 % vale 24 horas |
| RN-07 | Los pesos de los hitos **no son parametrizables**: si se movieran, el porcentaje dejaría de ser comparable entre dos momentos |
| RN-08 | El **cargo deriva seis cosas**: área, nivel, jefe, matriz de capacitación, turno habitual y punto de marcación. Se muestran, no se digitan |
| RN-09 | Un **punto de marcación es un conjunto de dispositivos**, no un equipo. Los cuatro vestieres de mujeres son un solo punto |
| RN-10 | Una marcación en un dispositivo no autorizado **nunca se descarta**: se registra y se señala como excepción |
| RN-11 | La **estructura del organigrama se resuelve a una fecha**, no a hoy. Una solicitud de hace seis meses debe saber quién era el jefe entonces |
| RN-12 | Un cargo **sin superior** no enruta solicitudes. Es un hallazgo que se señala, no un error que bloquea |
| RN-13 | La **firma se captura una vez** al ingreso y se invoca con la clave propia del colaborador. Antes bastaban cédula y código interno, que otras personas conocen |
| RN-14 | Los **datos reservados** —salario, EPS, caja, pensión— viven en tabla aparte. Si no hay permiso, el dato **no llega al navegador** |
| RN-15 | Un **parámetro legal se guarda con su vigencia**, nunca se sobrescribe. El cálculo busca el valor que regía en la fecha del hecho |
| RN-16 | Los **disparadores a sistemas externos salen por outbox**. Una caída de GLPI no impide registrar a alguien que ya llegó a trabajar |
| RN-17 | El **alcance del dato** es un eje aparte del permiso: propio, área, rama del organigrama, toda la empresa |

**Reglas marcadas como no resueltas:** ninguna de las anteriores. Las dudas abiertas están en la sección 9.

---

## 3 · Módulos funcionales

Una app de Django por módulo. El inventario completo está en `claude/01`; estos son los de las fases 0 a 3.

**No hay un módulo `cuentas/`.** SIRH+ no gestiona usuarios: no crea cuentas, no guarda contraseñas y no administra credenciales. Eso es del gestor de identidad, del que SIRH+ es la fuente de verdad de las personas. La regla completa está en `CLAUDE.md`, «SIRH+ no gestiona usuarios».

| App | Responsabilidad |
|---|---|
| `core/` | Chequeos de salud, utilidades y plantillas base |
| `identidad/` | Autenticación contra el gestor y aviso de altas y bajas. **Se escribe cuando el gestor exista** |
| `permisos/` | Catálogo granular, roles y resolución del alcance. **Propio, de cero** |
| `auditoria/` | Bitácora inmutable de cambios y consultas sensibles |
| `maestros/` | Áreas, cargos, estructura, organigrama y puntos de marcación |
| `personal/` | Personas, vínculos, historial temporal y completitud |
| `firmas/` | Captura, validación y estampado |
| `parametros/` | Configuración con vigencia por fecha |
| `dominio/` | **No es una app.** Reglas puras, sin Django ni entrada/salida |

---

## 4 · Datos

### Modelo propio

El detalle de cada modelo está en `claude/02`, §3 a §5. Resumen:

| Modelo | App | Nota |
|---|---|---|
| `Rol`, `PermisoRol`, `AsignacionUsuario` | permisos | El catálogo de permisos se declara **en código**, no en la base |
| `RegistroAuditoria` | auditoria | **Sin vistas de edición ni de borrado.** Ni para el administrador |
| `Area`, `Nivel`, `Cargo` | maestros | |
| `Dependencia` | maestros | **Versionada por fecha.** No se borra: se cierra su vigencia |
| `PuntoMarcacion`, `Dispositivo` | maestros | Un punto agrupa dispositivos |
| `Persona` | personal | La identificación. Lo que no cambia |
| `Vinculo` | personal | La relación laboral. Una persona puede tener varios en el tiempo |
| `AsignacionCargo` | personal | **Versionada por fecha** |
| `DatosContacto`, `DatosSST` | personal | |
| `DatosReservados` | personal | **Tabla aparte a propósito**, para que el permiso se aplique en la consulta |
| `SolicitudActualizacion` | personal | El colaborador no edita: solicita |
| `Firma`, `UsoFirma` | firmas | |
| `Parametro`, `Vigencia` | parametros | |

**Ningún modelo propio tiene llave foránea hacia el usuario.** Se guarda el identificador y el nombre como texto.

### Sistemas ajenos

| Capa | Sistema | Modo | Qué se lee o se escribe | Desde |
|---|---|---|---|---|
| `sirh_legacy_db/` | MySQL del SIRH viejo | Lectura | Migración y conciliación | Fase 2 |
| `glpi_api/` | GLPI | **Escritura**, por API | Creación de usuario. Lógica existente que se conserva | Fase 3 |
| `identidad_api/` | Gestor de identidad | **Escritura**, por API | Autenticación y ciclo de vida de la persona | Cuando exista |
| `biometricos_api/` | Dispositivos en LAN | Lectura | Marcaciones crudas | Fase 6 |
| `daruma_db/` | MySQL de calidad | Lectura | Documentos y versiones | Fase 14 |
| `mant_db/` | SQL Server de dotación | Lectura | Catálogo de elementos | Fase 18 |

**Lo que el estándar prohíbe es escribir en la BASE de un sistema ajeno, no llamar a su API.** Las dos capas que escriben lo hacen por la interfaz pública del otro sistema, que es su contrato y lo que ese sistema puede validar. A ninguna base ajena se le escribe.

**Nunca en `DATABASES`.** Cada una en su capa aislada.

---

## 5 · Pantallas

Cada pantalla corresponde a uno de los **cinco arquetipos** de `.claude/rules/03-sistema-de-diseno.md` §5, y todas resuelven los **cuatro estados** de §4.8.

| Pantalla | Arquetipo | Fase | Artboard |
|---|---|---|---|
| Tablero de RH | Panel | 1 | `v-tablero` |
| Roles y permisos | Editor | 1 | `v-permisos` |
| Usuarios, rol y alcance | Listado | 1 | `v-usuarios` |
| Bitácora de auditoría | Listado | 1 | `v-auditoria` |
| Áreas y cargos | Listado | 2 | `v-cargos` |
| Estructura y dependencias | Editor | 2 | `v-estructura` |
| Organigrama | Detalle | 2 | `v-organigrama` |
| Puntos de marcación | Listado + editor | 2 | `v-puntos` |
| Parámetros con vigencia | Listado | 2 | `v-parametros` |
| Captura rápida | Formulario por pasos | 3 | `v-captura` |
| Cola de fotos | Editor | 3 | `v-fotos` |
| Listado de personal | Listado | 3 | `v-listado` |
| Hoja de vida | Detalle | 3 | `v-hoja` |
| Completitud | Panel | 3 | `v-completitud` |
| Bandeja de pendientes | Listado | 3 | `v-pendientes` |
| Captura de firma | Formulario | 3 | `v-firmacap` |
| Firmar documento | Modal | 3 | `v-firmaconf` |

Los artboards están en `mockups/mockup-sirh-plus-completo.html`. **El mockup es la referencia visual**; la coincidencia se verifica en estructura, no píxel a píxel.

---

## 6 · Roles y permisos

### Roles

Los define TI, no RH. Siete al arrancar: administrador del sistema, coordinador de RRHH, analista de RRHH, auxiliar de RRHH, jefe de área, director, y seguridad y salud.

### Catálogo de permisos

Se declara **en código**, en `permisos/catalogo.py`, y crece con cada fase. La base guarda qué rol tiene qué permiso; el catálogo de permisos posibles se versiona con el código.

Cada permiso lleva una marca de **sensible**: su uso se audita obligatoriamente.

### Alcance

Eje aparte del permiso: `propio` · `area` · `rama` · `todo`. El alcance `rama` se resuelve contra la estructura **vigente en la fecha**, no contra la actual.

### Verificación

**En el servidor, en cada ruta y cada acción.** Ocultar un enlace del menú es cortesía visual, no protección.

Mientras el gestor de identidad no exista, la verificación se declara pero no se exige por defecto, con el parámetro `PERMISOS_EXIGIR`. Ver la desviación **D4**.

---

## 7 · Núcleo de dominio

Funciones puras en `dominio/`, sin Django y sin entrada/salida. Las de las fases 0 a 3:

| Función | Recibe | Devuelve |
|---|---|---|
| `codigos.codigo_nomina()` | documento, tipo de vínculo, reglas, códigos usados | el código, o el motivo del rechazo |
| `estructura.superior_de()` | cargo, dependencias, fecha | el cargo superior vigente, o `None` |
| `estructura.rama_de()` | cargo, dependencias, fecha | todos los cargos que dependen de él |
| `estructura.cargos_sin_superior()` | cargos, dependencias, fecha | los que no pueden enrutar |
| `parametros.vigente_en()` | clave, vigencias, fecha | el valor que regía en esa fecha |
| `completitud.calcular()` | hitos declarados, estado de la persona | el porcentaje y qué falta |
| `vencimientos.estado()` | fecha base, plazo, hoy | al día · próximo a vencer · vencido |

Cada una con sus pruebas en `tests/`, **incluyendo los casos límite**: ciclos en la estructura, cargo raíz, cargo huérfano, colisión de códigos, documento de seis dígitos, reingreso, fecha anterior a toda vigencia.

---

## 8 · Desviaciones del estándar

Cuatro, todas declaradas con su justificación. **No se corrigen.**

### D1 · El shell no es el del estándar

**El estándar fija** un sidebar de 220 px para toda pantalla con sesión.

**SIRH+ usa** sidebar de 244 px en la cara de gestión y **cabecera superior** en la pública y la de colaborador.

**Por qué:** el estándar está escrito para herramientas internas que usan decenas de personas. La cara de colaborador la usan 1.100 personas que no quieren entrar a un sistema. Son dos audiencias con necesidades distintas.

**Alcance:** `.claude/rules/03-sistema-de-diseno.md` reemplaza íntegramente a la regla de frontend del estándar.

### D2 · Permisos granulares, no dos roles

**El estándar fija** dos roles, `consulta` y `administra`, iguales en todas las aplicaciones.

**SIRH+ usa** un catálogo granular por módulo y acción, agrupado en roles que define TI.

**Por qué:** SIRH+ maneja salarios, procesos disciplinarios y datos de salud ocupacional. Dos roles no pueden expresar que un analista vea el salario pero no lo edite.

**Cómo se respeta el estándar:** la frontera se mantiene. El gestor de identidad resuelve el acceso a la aplicación; SIRH+ resuelve la autorización dentro, en un módulo `permisos/` propio.

### D3 · El alcance del dato como eje aparte

**SIRH+ añade** cuatro niveles de alcance, modelados aparte del permiso.

**Por qué:** dos usuarios con el mismo `personal.ver` deben ver conjuntos de personas distintos. Eso no es un permiso: es una dimensión aparte, y mezclarla multiplicaría el catálogo por cuatro.

### D4 · La identidad llega después, no en la fase 1

**El estándar exige**, en la fase 1 de su checklist: conexión `identidad` con su router, la app registrada en la tabla `aplicacion`, un usuario de MySQL propio, los dos chequeos de salud de identidad, y login y cambio de contraseña funcionando.

**SIRH+ construye** en su lugar: pantalla de ingreso sin lógica de validación, catálogo de permisos completo pero con `PERMISOS_EXIGIR=false`, y los dos chequeos de salud declarados y desactivados.

**Y no construye:** autenticación local, tabla de usuarios, contraseñas, ni nada provisional en su lugar. SIRH+ no gestiona usuarios. El módulo `identidad/` se escribe cuando el gestor exista.

**Por qué:** el gestor de identidad está en construcción y SIRH+ va a ser su fuente de verdad de personas. Esperar a que exista detendría el proyecto; construir sin pensar en él obligaría a rehacerlo.

**Cómo se mitiga el riesgo:** no queda nada que desmontar, porque no se construye nada en lugar del gestor. El catálogo de permisos existe desde la fase 1 y **se corre con la verificación exigida al menos una vez por fase**, revisando el registro. Esa es la salvaguarda contra repetir la autorización cosmética del sistema viejo.

**Cuándo se paga:** al conectar el gestor. **La pantalla de ingreso sin validación nunca sale a producción**, y el sistema no sale a producción sin el gestor funcionando.

---

## 9 · Preguntas abiertas

Están en `docs/pendientes.md`, con quién decide cada una y en qué fase se necesita. Las que afectan a las fases 0 a 3:

| # | Pregunta | Quién decide |
|---|---|---|
| A5 | ¿La autorización de tratamiento de datos se firma en el hito del 10 % o puede esperar al 55 %? | RH y jurídico |
| A10 | ¿Dónde se guarda la foto del colaborador y con qué compresión? Mil fotos sin comprimir son un problema de disco y de velocidad | TI |
| B3 | La estructura de dependencias de los 198 cargos **no existe hoy en ningún sistema** y hay que construirla con RH | RH |

**Ninguna de las tres bloquea la fase 0 ni la 1.** B3 bloquea la migración de la fase 2.
