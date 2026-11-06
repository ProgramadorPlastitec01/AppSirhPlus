# SIRH+ — Inventario completo de módulos y plan de fases

**Plastitec S.A.S. · Tecnología de Información**
Versión 1.0 · 5 de noviembre de 2026

Documento de alcance. Lista **todos** los módulos, **todas** sus opciones y el orden en que se construyen. Es el insumo para la propuesta a gerencia y el esqueleto del plan de ejecución.

---

## Cómo leer este documento

- **Parte I — Inventario**: qué hace el sistema, módulo por módulo, opción por opción.
- **Parte II — Fases**: en qué orden se construye y qué entrega cada fase.
- **Parte III — Lo que se reemplaza**: qué sistemas desaparecen y qué se gana.

**Módulo** = una app de Django con su dominio. Unidad de código.
**Fase** = un bloque de trabajo que entrega algo usable y verificable. Puede tocar varios módulos.

---

# PARTE I · INVENTARIO DE MÓDULOS

## Resumen

| Grupo | Módulos | Opciones |
|---|---|---|
| **Transversales** | 9 | 58 |
| **Negocio** | 12 | 225 |
| **Integraciones** | 7 | 31 |
| **TOTAL** | **28** | **314** |

---

# A · MÓDULOS TRANSVERSALES

Infraestructura de la que depende casi todo. Se construyen una vez.

## A.1 · Núcleo de dominio — `dominio/`

Paquete Python puro, sin Django, sin entrada ni salida. Todas las reglas de negocio calculables viven aquí y se prueban en milisegundos.

| # | Pieza | Qué calcula |
|---|---|---|
| 1 | `festivos.py` | Festivos de Colombia por algoritmo, sin tabla que mantener |
| 2 | `jornada/marcaciones.py` | Limpieza, deduplicación y emparejamiento de marcaciones |
| 3 | `jornada/turnos.py` | Ventana del turno, café, almuerzo, roles de dispositivo |
| 4 | `jornada/segmentacion.py` | Partición del tiempo en tramos atómicos |
| 5 | `jornada/clasificacion.py` | Matriz de conceptos, escalera, umbral semanal |
| 6 | `jornada/conceptos.py` | Agregación por concepto y generación del archivo plano |
| 7 | `vacaciones.py` | Causación, saldo, días hábiles, fraccionamiento |
| 8 | `competencias.py` | Ponderación por grupo y nota final |
| 9 | `indicadores.py` | Rotación, ausentismo, incapacidades, indicadores SST |
| 10 | `vencimientos.py` | Al día, próximo a vencer, vencido |
| 11 | `codigos.py` | Construcción y validación del código de nómina |
| 12 | `parametros.py` | Resolución del valor vigente en una fecha |

## A.2 · Identidad y acceso — `identidad/`

**Se escribe cuando el gestor de identidad exista.** SIRH+ no gestiona usuarios: no crea cuentas, no guarda contraseñas y no administra credenciales. Mientras tanto la pantalla de ingreso no valida nada, y **no se construye autenticación local de ninguna clase**. Ver `CLAUDE.md`, «SIRH+ no gestiona usuarios».

| # | Opción |
|---|---|
| 1 | Inicio de sesión contra el gestor de identidad central |
| 2 | Aviso al gestor del alta de una persona, por la outbox |
| 3 | Aviso al gestor de la baja por retiro, por la outbox |
| 4 | Verificación del acceso a SIRH+ por aplicación |
| 5 | Gestión de la sesión: expiración, renovación, cierre |
| 6 | Pantalla propia de acceso denegado |
| 7 | Chequeo de salud de la conexión de identidad |

**El cambio de contraseña no está en la lista.** Es del gestor, no de SIRH+.

## A.3 · Permisos — `permisos/`

**Se construye de cero.** El modelo del sistema anterior (permisos por usuario, HTML del menú dentro de la base) no se reutiliza.

| # | Opción |
|---|---|
| 1 | Catálogo de permisos, declarado en código por módulo |
| 2 | Administración de roles: crear, editar, duplicar, desactivar |
| 3 | Matriz de permisos por rol, con buscador y agrupación por módulo |
| 4 | Marca de permiso sensible, con auditoría obligatoria de su uso |
| 5 | Alcance del dato como eje aparte: propio · área · rama del organigrama · toda la empresa |
| 6 | Asignación de rol y alcance por usuario |
| 7 | Simulador: «ver el sistema como lo vería este rol» |
| 8 | Verificación en el servidor, en cada ruta y cada acción |
| 9 | Interruptor de exigencia, por configuración, para probar antes del final |
| 10 | Informe de quién tiene cada permiso |

## A.4 · Firmas — `firmas/`

| # | Opción |
|---|---|
| 1 | Captura de la firma en tableta, una sola vez al ingreso |
| 2 | Almacenamiento como coordenadas, ligado a documento y código interno |
| 3 | Creación de la clave propia del colaborador |
| 4 | Restablecimiento de clave desde el gestor de identidad |
| 5 | Invocación de la firma con validación de clave |
| 6 | Estampado de la firma en el documento |
| 7 | Generación del PDF firmado |
| 8 | Migración de las ~8.200 firmas existentes por código interno |
| 9 | Consulta de dónde se ha usado cada firma |

## A.5 · Registros firmados — `registros/`

Motor común a siete documentos distintos.

| # | Opción |
|---|---|
| 1 | Definición de formatos, versionados |
| 2 | Diligenciamiento del formato |
| 3 | Flujo de firmas en orden, con estado por firmante |
| 4 | Asignación de folio consecutivo que no se reinicia |
| 5 | Cierre inmutable |
| 6 | Exportación a PDF con las firmas estampadas |
| 7 | Consulta y búsqueda de registros por folio, fecha o persona |
| 8 | Anulación con motivo, que emite un registro nuevo y no borra el anterior |

**Documentos que lo usan:** R-RH-009 capacitación · R-RH-053 competencias · solicitud de vacaciones · solicitud de permiso · divulgación de documento · entrega de dotación · paz y salvo de retiro.

## A.6 · Vencimientos — `vencimientos/`

| # | Opción |
|---|---|
| 1 | Definición de reglas de vencimiento por tipo |
| 2 | Cálculo de estado: al día, próximo a vencer, vencido |
| 3 | Panel de vencimientos por área y por persona |
| 4 | Generación de avisos |
| 5 | Parametrización del plazo por cargo |

**Qué vigila:** exámenes médicos · evaluaciones de competencias · documentos de la matriz de capacitación · contratos a término fijo.

## A.7 · Parámetros — `parametros/`

| # | Opción |
|---|---|
| 1 | Catálogo organizado por módulo |
| 2 | Parámetro legal con vigencia: valor más fecha desde, nunca se sobrescribe |
| 3 | Parámetro de política interna, con vigencia |
| 4 | Parámetro operativo, editable |
| 5 | Resolución del valor vigente en una fecha dada |
| 6 | Historial completo de vigencias de cada parámetro |
| 7 | Calendario de festivos: cálculo automático más ajustes manuales |
| 8 | Reglas del código de nómina: qué dígito corresponde a qué vínculo |
| 9 | Fechas de corte y cierre de período |
| 10 | Auditoría de cada cambio |

## A.8 · Notificaciones — `notificaciones/`

| # | Opción |
|---|---|
| 1 | Bandeja unificada de pendientes, por usuario |
| 2 | Avisos en la portada del sistema |
| 3 | Envío por correo a quien lo tenga |
| 4 | Plantillas de mensaje, editables |
| 5 | Preferencias de notificación por usuario |
| 6 | Registro de qué se envió y a quién |

## A.9 · Auditoría — `auditoria/`

| # | Opción |
|---|---|
| 1 | Registro inmutable de creación, modificación y borrado |
| 2 | Registro de consulta de datos sensibles |
| 3 | Valor anterior y valor nuevo en cada cambio |
| 4 | Usuario, fecha, hora, dirección y equipo |
| 5 | Consulta con filtros por módulo, acción, usuario y rango de fechas |
| 6 | Exportación de la bitácora |
| 7 | Registro de intentos de acceso denegados |
| 8 | Trazabilidad de un registro: toda su historia en una vista |

---

# B · MÓDULOS DE NEGOCIO

## B.1 · Personal — `personal/`

El módulo del que dependen todos los demás.

### Registro y datos

| # | Opción |
|---|---|
| 1 | **Captura rápida**: cinco campos, guardar y siguiente, sin recargar |
| 1b | **Carga masiva** desde planilla, para personal temporal |
| 1c | **Cola de fotos**: disparar y avanzar, para cuando la persona llega |
| 1d | **Completitud por hitos**, de 10 % a 100 %, con dueño y consecuencia por hito |
| 1e | Plazo de 24 horas para los registros bajo el 40 % |
| 1f | Validación de unicidad **al escribir**, contra el histórico completo |
| 2 | Identificación: tipo y número de documento, nombres, apellidos, género, fecha de nacimiento |
| 3 | Fotografía del colaborador |
| 4 | Perfil: grupo sanguíneo, nivel educativo, número de hijos, especialidad |
| 5 | Vínculo: directo, temporal o aprendiz SENA; estado; fechas de ingreso y contrato |
| 6 | Empresa: Plastitec o Granservicios |
| 7 | Códigos: interno, de nómina y de firma, generados y no editables |
| 8 | Ubicación: cargo y área |
| 9 | Contacto: correo, teléfonos, contacto de urgencia, localidad |
| 10 | SST: brigadista, restricciones físicas, restricciones médicas |
| 11 | Datos reservados: salario, EPS, caja de compensación, fondo de pensión, cesantías, nivel de riesgo |
| 12 | Sindicalizado |

### Consulta y gestión

| # | Opción |
|---|---|
| 13 | Listado con filtros avanzados y columnas configurables |
| 14 | Atajos de filtro: sin código de nómina, datos incompletos, examen vencido, sin firma |
| 15 | Búsqueda por documento, nombre o código |
| 16 | Exportación a Excel, respetando permisos |
| 17 | **Hoja de vida**: todo el recorrido histórico en una línea de tiempo |
| 18 | Pestañas de la hoja de vida: datos, contrato, eventualidades, formación, competencias, dotación, documentos |
| 19 | Historial temporal: qué cargo, área y salario tenía en cualquier fecha pasada |
| 20 | Edición con registro de cambios |
| 21 | Solicitudes de actualización de datos: bandeja, comparación antes y después, aprobación campo por campo |
| 22 | Reingreso: reactivación con trazabilidad y código de nómina nuevo |
| 23 | Documentos adjuntos de la persona |
| 24 | Validación del código de nómina como único contra el histórico completo |

### Retiro

| # | Opción |
|---|---|
| 25 | Registro del retiro con motivo y tipo |
| 26 | Generación del paz y salvo |
| 27 | Verificación por área: TI, Seguridad, Jefe inmediato, Recursos Humanos |
| 28 | Firma del trabajador, el jefe y RH |
| 29 | Revocación de accesos en los sistemas conectados |
| 30 | Entrevista de retiro |

## B.2 · Empresa — `maestros/`

| # | Opción |
|---|---|
| 1 | Áreas: crear, editar, desactivar; sigla, jefe, correo |
| 2 | Cargos: crear, editar, desactivar; área, nivel, especialidad |
| 3 | Los nueve niveles jerárquicos |
| 4 | Estructura: qué cargo reporta a qué cargo |
| 5 | Versionado de la estructura con fecha de vigencia |
| 6 | Detección de cargos sin superior |
| 7 | Vista del impacto de un cambio: a cuántas personas afecta |
| 8 | **Matriz de capacitación por cargo**: qué documentos le aplican |
| 9 | Formato de competencias asignado al cargo |
| 10 | **Organigrama navegable**, público, con búsqueda |
| 11 | Vista por cargo y vista por persona |
| 12 | Vacantes: cargos sin asignación vigente |
| 13 | Exportación del organigrama a PDF |
| 14 | Catálogos: tipos de categoría, motivos, calendario de actividades |
| 15 | **Catálogo de puntos de marcación**: un punto agrupa varios dispositivos |
| 16 | Punto de marcación por omisión de cada cargo |
| 17 | Excepción de punto por persona, con motivo, vigencia y autorizador |
| 18 | Rol de los dispositivos del punto: portería, descanso o interior |
| 19 | Detección de cargos sin punto asignado |

## B.3 · Marcaciones — `marcaciones/`

**Reemplaza a BioTime por completo.** El módulo más grande del proyecto.

### Dispositivos y captura

| # | Opción |
|---|---|
| 1 | Catálogo de biométricos: nombre, dirección, ubicación |
| 2 | **Rol de cada dispositivo**: portería, descanso o interior |
| 3 | Conexión directa a los dispositivos en la red |
| 4 | Recolección programada de marcaciones |
| 5 | **Monitor de salud**: detecta un dispositivo caído y avisa a soporte |
| 6 | Registro del estado histórico de cada dispositivo |
| 7 | Control de reloj desfasado y marcaciones rezagadas |
| 8 | Deduplicación y agrupación de doble toque |
| 9 | Consulta de la marcación cruda, sin procesar |
| 10 | Carga manual de respaldo, por si falla la conexión |

### Turnos

| # | Opción |
|---|---|
| 11 | Catálogo de turnos |
| 12 | Bloques por día de la semana dentro de un mismo turno |
| 13 | Turnos gemelos para semanas con festivo |
| 14 | Ventana válida de marcación, antes y después, por turno |
| 15 | Descanso de café y descanso de almuerzo, con su hora |
| 16 | Turnos que cruzan medianoche |
| 17 | Turnos de solo extras |
| 18 | Turnos administrativos |
| 19 | Duplicar y versionar un turno |

### Programación

| # | Opción |
|---|---|
| 20 | Programación semanal por área |
| 21 | Vista de matriz: personas por días |
| 22 | Vista de calendario mensual por persona |
| 23 | **Selección masiva** por área, turno actual, grupo o cuadrilla |
| 24 | **Rotación en bloque**: todos los de turno 1 pasan a turno 2 |
| 25 | Patrones de rotación por área, hacia adelante o hacia atrás |
| 26 | Detección de festivos con propuesta de turno, que el jefe acepta |
| 27 | Cambios puntuales sobre la programación, con trazabilidad |
| 28 | Copiar la programación de una semana a otra |
| 29 | Detección de persona sin turno y de doble turno |
| 30 | Publicación de la programación al personal |

### Cálculo

| # | Opción |
|---|---|
| 31 | Jornada fija del turno, acreditada completa |
| 32 | Horas pendientes, reportadas sin descontar del pago |
| 33 | Escalera de sobretiempo, con parámetros |
| 34 | Segmentación por minuto |
| 35 | Tipo de día evaluado por tramo, no por turno |
| 36 | Clasificación en los siete conceptos, mutuamente excluyente |
| 37 | Umbral semanal para personal rotativo |
| 38 | Semana operativa que arranca el domingo a las 22:00 |
| 39 | Café pagado, por rol de dispositivo |
| 40 | Tránsito interior, que no genera deuda |
| 41 | Lactancia, con tope diario por etapa |
| 42 | Personal de dirección y confianza, excluido de jornada máxima |
| 43 | Vigencia del empleado: ingreso, retiro y marcaciones posteriores |
| 44 | Invariantes de integridad verificados en cada cálculo |

### Excepciones y corrección

| # | Opción |
|---|---|
| 45 | Consola de excepciones por severidad |
| 46 | Marcación faltante señalada en pantalla |
| 47 | Número impar de marcaciones, con resolución propuesta |
| 48 | Corrección de una marcación por el jefe, con auditoría |
| 49 | Vista en vivo de quién está en turno y quién no ha llegado |
| 50 | Tolerancia de puntualidad parametrizable |

### Aprobación y cierre

| # | Opción |
|---|---|
| 51 | Bandeja de horas extra por aprobar, del jefe |
| 52 | Aprobación o rechazo con motivo |
| 53 | Alerta de tope semanal de 12 horas |
| 54 | Contador mensual de 48 horas, con alerta |
| 55 | Período con estados: abierto, en cierre, cerrado |
| 56 | Cierre inmutable, con foto histórica |
| 57 | Bloqueo del cierre si hay excepciones sin resolver o personas sin código de nómina |
| 58 | Reapertura con rol elevado, que genera un cálculo nuevo |
| 59 | Recálculo histórico con los parámetros vigentes en la fecha |

### Reportes

| # | Opción |
|---|---|
| 60 | Consolidado por empleado |
| 61 | Detalle día a día |
| 62 | Asistencia con semáforo |
| 63 | Calidad de marcación por área |
| 64 | Cobertura de programación y de datos |
| 65 | Indicadores de cumplimiento |
| 66 | Consulta de sus propias marcaciones, para el colaborador |
| 67 | Exportación de todo lo anterior a Excel |

## B.4 · Nómina — `nomina/`

| # | Opción |
|---|---|
| 1 | Catálogo de conceptos con su código |
| 2 | Vigencia de los códigos, para cuando la ley cambia los porcentajes |
| 3 | Conceptos habilitados por empleado |
| 4 | Consolidación de conceptos desde marcaciones, eventualidades y trámites |
| 5 | **Generación del archivo plano**, con su formato exacto |
| 6 | Separación por empresa, Plastitec y Granservicios |
| 7 | Vista previa antes de generar |
| 8 | Validación previa: códigos de nómina faltantes, excepciones abiertas |
| 9 | Registro de qué archivo se generó, cuándo y quién |
| 10 | Reproceso y ajuste del período |
| 11 | Contraste contra el período anterior |
| 12 | Conciliación con lo liquidado |

## B.5 · Eventualidades — `eventualidades/`

Modelo unificado, parametrizado por tipo.

| # | Opción |
|---|---|
| 1 | Catálogo de tipos y de motivos |
| 2 | Registro de la eventualidad con sus campos por tipo |
| 3 | Documentos adjuntos |
| 4 | **Accidente de trabajo**: investigación, causas, plan de acción, responsable, seguimiento, cierre |
| 5 | **Enfermedad profesional**, con seguimiento |
| 6 | **Incapacidad**: días, origen, entidad |
| 7 | **Ausencia**, con causal |
| 8 | **Descargo**, con acceso restringido a jefe y RH |
| 9 | **Examen médico**: ingreso y periódico; concepto y adjunto |
| 10 | **Retiro**, que dispara el paz y salvo |
| 11 | Consulta y listado con filtros |
| 12 | Vista por persona dentro de la hoja de vida |
| 13 | Aporte de conceptos al archivo de nómina |
| 14 | Cruce con marcaciones para el indicador de ausentismo |
| 15 | Alertas de examen periódico vencido |
| 16 | Exportación |

## B.6 · Trámites — `tramites/`

| # | Opción |
|---|---|
| 1 | Catálogo de tipos de solicitud |
| 2 | Radicación con número consecutivo |
| 3 | Estados y seguimiento |
| 4 | Enrutamiento al jefe según el organigrama vigente |
| 5 | Flujo de firmas: colaborador, jefe, RH |
| 6 | Bandeja de aprobación del jefe |
| 7 | Bandeja de RH |
| 8 | Notificación en cada paso |
| 9 | **Vacaciones**: causación, saldo, días hábiles, mínimos por política, acumulación |
| 10 | Bloqueo si no hay saldo suficiente |
| 11 | Solicitud en rango de fechas, excluyendo sábados, domingos y festivos |
| 12 | **Permisos**: los doce motivos del catálogo, remunerados y no remunerados |
| 13 | **Certificado laboral** con y sin salario, con código verificable |
| 14 | **PQR**, con escalamiento a comité |
| 15 | Histórico de trámites por persona |
| 16 | Indicadores: tiempos de respuesta, volumen por tipo |

## B.7 · Formación — `formacion/`

**Reemplaza a COPEC por completo.**

### Divulgación de documentos

| # | Opción |
|---|---|
| 1 | Conexión de solo lectura a Daruma |
| 2 | Catálogo de documentos con su versión |
| 3 | **Detección de versión nueva** comparando contra Daruma |
| 4 | Programación de la divulgación por el jefe del área |
| 5 | Disparo automático a quienes tienen el documento en su matriz |
| 6 | Lectura del documento dentro del sistema |
| 7 | Firma de la constancia de lectura |
| 8 | Seguimiento de quién leyó y quién no |
| 9 | Control por área y por jefe |
| 10 | Alerta de divulgación pendiente |
| 11 | Reasignación de matriz al cambiar de cargo, conservando el historial |
| 12 | Historial de versiones leídas por persona |

### Inducción

| # | Opción |
|---|---|
| 13 | Contenido de la inducción, por secciones |
| 14 | Cuenta de pre-ingreso, para quien todavía no es empleado |
| 15 | Seguimiento del avance |
| 16 | Evaluación final |
| 17 | **Constancia verificable**: consecutivo, horas y código |
| 18 | Panel de ingresos nuevos y su estado de inducción |

### Cursos

| # | Opción |
|---|---|
| 19 | Catálogo de cursos |
| 20 | Constructor de curso por secciones |
| 21 | **Constructor de evaluación**: pregunta, opciones y respuesta correcta |
| 22 | Nota mínima y número de reintentos |
| 23 | Asignación por cargo, área o persona |
| 24 | Realización del curso por el colaborador |
| 25 | Certificado al aprobar |
| 26 | Seguimiento de avance y aprobación |

### R-RH-009 · Registro de capacitación

| # | Opción |
|---|---|
| 27 | Creación del registro con sus datos de cabecera |
| 28 | Capacitación individual o grupal |
| 29 | Instructor interno o externo |
| 30 | Carga de asistentes |
| 31 | Firma de cada asistente en la tableta |
| 32 | Revisión por RH y asignación de folio |
| 33 | Cierre del registro |
| 34 | Consulta por folio, fecha, instructor o asistente |
| 35 | Exportación a PDF |

### Transversal

| # | Opción |
|---|---|
| 36 | Horas de formación por persona y por año |
| 37 | Cumplimiento de la matriz por cargo y por área |
| 38 | Indicadores de formación |

## B.8 · Competencias — `competencias/`

| # | Opción |
|---|---|
| 1 | Constructor del formato R-RH-053 |
| 2 | Grupos con peso porcentual que suma 100 |
| 3 | Conductas con definición y escala de 1 a 5 |
| 4 | Observación por conducta |
| 5 | Versionado del formato |
| 6 | Asignación del formato a un cargo |
| 7 | Evaluación por el jefe inmediato |
| 8 | Cálculo de la nota ponderada |
| 9 | Nota mínima parametrizable |
| 10 | Resultado: aprobada o por repetir a los tres meses |
| 11 | Histórico de evaluaciones con la versión del formato usada |
| 12 | Alerta a los diez meses sin evaluación |
| 13 | Panel de cumplimiento por área |
| 14 | Vista del colaborador, por definir con RH |
| 15 | Matriz SST, con su propio formato |
| 16 | Exportación |

## B.9 · Dotación y EPP — `dotacion/`

| # | Opción |
|---|---|
| 1 | Catálogo de elementos, leído de la base de dotación |
| 2 | Tallas por persona |
| 3 | Ciclos de entrega, tres al año |
| 4 | Asignación por cargo |
| 5 | Jornada de entrega: lista, marcación de entregados |
| 6 | Firma del colaborador |
| 7 | Entrega de EPP, por separado |
| 8 | Histórico por persona |
| 9 | Pendientes de devolución para el paz y salvo |
| 10 | Indicadores de entrega |

## B.10 · Encuestas — `encuestas/`

| # | Opción |
|---|---|
| 1 | Constructor de encuesta |
| 2 | Tipos de pregunta: opción múltiple, escala, texto libre corto |
| 3 | Marca de anónima |
| 4 | Segmentación: toda la empresa o por cargos |
| 5 | Fecha de cierre opcional |
| 6 | Publicación y notificación |
| 7 | Respuesta por el colaborador |
| 8 | Control de respuesta única, en tabla separada de las respuestas |
| 9 | Conteo de quiénes faltan; los nombres solo si no es anónima |
| 10 | Análisis con gráficas y promedios |
| 11 | Exportación a Excel |
| 12 | Histórico de encuestas |

## B.11 · Reservas — `reservas/`

| # | Opción |
|---|---|
| 1 | Catálogo de recursos reservables |
| 2 | Calendario de disponibilidad |
| 3 | Reserva con tope de seis horas |
| 4 | Cancelación |
| 5 | Mis reservas |
| 6 | Vista de ocupación |

## B.12 · Indicadores e informes — `reportes/`

Capa de lectura sobre los demás módulos. Se construye al final.

| # | Opción |
|---|---|
| 1 | **Rotación de personal**, con desglose |
| 2 | **Índice de ausentismo**, cruzando marcaciones y eventualidades |
| 3 | **Índice de incapacidades**, por motivo y área |
| 4 | Indicadores de accidentalidad y SST |
| 5 | Indicadores de formación |
| 6 | Indicadores de competencias |
| 7 | Indicadores de trámites |
| 8 | Consulta por rango de fechas libre |
| 9 | Desglose por área, cargo, vínculo y período |
| 10 | Panel configurable |
| 11 | Exportación a Excel y PDF |
| 12 | **Módulo de consulta histórica**, para lo anterior a cinco años |

---

# C · LA CARA DEL COLABORADOR

No es un módulo aparte: es la capa de visibilidad sobre los mismos módulos.

## C.1 · Vista pública, sin sesión

| # | Opción |
|---|---|
| 1 | Portada con noticias |
| 2 | Organigrama |
| 3 | Convocatorias internas |
| 4 | Espacio del Fondo de Empleados |
| 5 | Acceso |

## C.2 · Vista del colaborador

| # | Opción | Módulo que la sirve |
|---|---|---|
| 1 | Mi información y solicitud de actualización | Personal |
| 2 | Mis marcaciones y mis horas | Marcaciones |
| 3 | Mi saldo de vacaciones | Trámites |
| 4 | Solicitar vacaciones y permisos | Trámites |
| 5 | Mis solicitudes y su estado | Trámites |
| 6 | Descargar certificado laboral | Trámites |
| 7 | Radicar una PQR | Trámites |
| 8 | Mi inducción | Formación |
| 9 | Divulgaciones pendientes y firma | Formación |
| 10 | Catálogo de cursos y mis certificados | Formación |
| 11 | Mis encuestas pendientes | Encuestas |
| 12 | Reservar sala | Reservas |
| 13 | Mi dotación recibida | Dotación |
| 14 | Mis competencias, por definir | Competencias |
| 15 | Mi hoja de vida resumida | Personal |

## C.3 · Vista del jefe

| # | Opción |
|---|---|
| 1 | Bandeja unificada de pendientes de su personal |
| 2 | Su personal, con alcance de su rama |
| 3 | Programación de turnos de su área |
| 4 | Aprobación de horas extra |
| 5 | Aprobación de permisos y vacaciones |
| 6 | Evaluación de competencias de su personal |
| 7 | Programación de divulgaciones de su área |
| 8 | Indicadores de su área |

## C.4 · Contenido corporativo — `contenido/`

| # | Opción |
|---|---|
| 1 | Noticias: crear, publicar, programar, archivar |
| 2 | Categorías de noticia |
| 3 | Convocatorias internas, solo como anuncio |
| 4 | Beneficios |
| 5 | Espacio del Fondo de Empleados, con usuario propio |
| 6 | Moderación por RH de lo que publica el Fondo |
| 7 | Directorio por área |
| 8 | Cumpleaños del mes |

---

# D · INTEGRACIONES

| # | Sistema | Dirección | Qué hace |
|---|---|---|---|
| 1 | **Biométricos** | Lectura | Recolección de marcaciones en la red |
| 2 | **Biométricos** | Lectura | Monitoreo de salud y aviso a soporte |
| 3 | **GLPI** | Escritura | Creación del usuario al registrar personal |
| 4 | **GLPI** | Escritura | Inactivación al retiro |
| 5 | **Gestor de identidad** | Escritura | Alta, cambio y baja de la identidad |
| 6 | **Gestor de identidad** | Lectura | Autenticación y verificación de acceso |
| 7 | **Daruma** | Lectura | Catálogo de documentos y detección de versión |
| 8 | **Base de dotación** | Lectura | Catálogo de elementos |
| 9 | **SINERGY** | Archivo | Generación del archivo plano de nómina |
| 10 | **SIRH antiguo** | Lectura | Migración y conciliación |
| 11 | **Correo** | Escritura | Notificaciones |

---

# PARTE II · PLAN DE FASES

## Principio

**Cada fase entrega algo usable y verificado.** No se avanza hasta que las seis compuertas pasen y el QA revise. Nada depende de algo que todavía no existe.

## Las seis compuertas

| # | Compuerta |
|---|---|
| 1 | Formato y lint en verde |
| 2 | Pruebas del núcleo en verde |
| 3 | Chequeo de salud en verde |
| 4 | Revisión de seguridad sin hallazgos |
| 5 | Revisión visual y los cuatro estados en cada pantalla |
| 6 | Validación humana contra un caso real, más revisión del QA |

La versión normativa está en `claude/02-plan-de-ejecucion-sirh-plus.md` §0.3. Si las dos se separan, gana el plan de ejecución.

## Resumen de las fases

| # | Fase | Módulos que toca | Qué se puede hacer al terminar |
|---|---|---|---|
| **0** | Cimientos | — | La aplicación arranca, se despliega y se ve como SIRH+ |
| **1** | Identidad, permisos y auditoría | permisos, auditoría | Entrar, con rol y alcance; todo cambio queda registrado |
| **2** | Empresa | maestros | Áreas, cargos, estructura y organigrama funcionando |
| **3** | Personal y firmas | personal, firmas | Registrar personal de punta a punta, con hoja de vida |
| **4** | Migración del maestro | sirh_legacy_db | Las 1.094 personas y sus 8.200 firmas, dentro |
| **5** | Parámetros y vencimientos | parámetros, vencimientos | Configuración con vigencia administrable y alertas funcionando |
| **6** | Marcaciones · captura | marcaciones, biométricos | Las marcaciones entran solas y los dispositivos se vigilan |
| **7** | Marcaciones · turnos y programación | marcaciones | Los jefes programan turnos sin BioTime |
| **8** | Marcaciones · motor de cálculo | dominio/jornada | El cálculo reproduce exactamente el ciclo de referencia |
| **9** | Marcaciones · aprobación y cierre | marcaciones | Horas aprobadas por el jefe y período cerrado |
| **10** | Nómina · archivo plano | nómina | **BioTime se apaga** |
| **11** | Eventualidades | eventualidades | Toda la hoja de vida se llena |
| **12** | Registros firmados y notificaciones | registros, notificaciones | El motor común, listo para cinco módulos |
| **13** | Trámites y vista del colaborador | trámites, cara de colaborador | Autoconsulta y solicitudes en línea |
| **14** | Formación · divulgaciones | formación, Daruma | **COPEC se apaga** |
| **15** | Formación · inducción y cursos | formación | Inducción desde casa y catálogo de cursos |
| **16** | Formación · R-RH-009 | formación | Registro de capacitación digital |
| **17** | Competencias | competencias | Evaluación anual completa |
| **18** | Dotación y EPP | dotación | Jornadas de entrega con firma |
| **19** | Encuestas y reservas | encuestas, reservas | Los dos módulos menores |
| **20** | Contenido y portal público | contenido | Noticias, convocatorias y Fondo de Empleados |
| **21** | Indicadores e informes | reportes | Los indicadores de RH, conciliados |
| **22** | Histórico y cierre | reportes | Consulta histórica y apagado del SIRH viejo |

---

## Detalle de cada fase

### Fase 0 · Cimientos

**Entrega:** la aplicación arranca, se despliega y tiene el lenguaje visual de SIRH+. No hace nada útil todavía.

| Contenido |
|---|
| Repositorio en Git, con la plantilla del estándar |
| Esqueleto de Django y estructura de carpetas |
| PostgreSQL local, configuración por `.env` |
| Design tokens y hoja de estilos única |
| Plantillas base y librería de componentes |
| Tipografías auto-hospedadas |
| Chequeos de salud y ruta de estado |
| Registro de eventos configurado |
| `ruff` como formateador y linter |
| Documentos vivos del proyecto |

**Fuera de alcance:** cualquier funcionalidad de negocio.

---

### Fase 1 · Identidad, permisos y auditoría

**Entrega:** se entra al sistema con un rol y un alcance, y todo lo que se hace queda registrado.

| Contenido |
|---|
| Pantalla de acceso, sin lógica de validación todavía |
| **Ninguna autenticación.** `identidad/` se escribe cuando el gestor exista |
| **Catálogo de permisos completo, declarado** |
| Administración de roles y matriz de permisos |
| Alcance del dato como eje aparte |
| Asignación de rol y alcance por usuario |
| Interruptor de exigencia, por configuración |
| Módulo de auditoría completo |
| Pantalla propia de acceso denegado |

**Fuera de alcance:** conexión real al gestor de identidad, que llega cuando exista.

---

### Fase 2 · Empresa

**Entrega:** la estructura de la organización, de la que depende todo el enrutamiento.

| Contenido |
|---|
| Áreas y cargos, con su catálogo |
| Los nueve niveles |
| Estructura de dependencias, versionada |
| Detección de cargos sin superior |
| Organigrama navegable, público |
| Matriz de capacitación por cargo, como definición |
| **Catálogo de puntos de marcación y su rol** |
| **Punto por omisión de cada cargo**, con detección de cargos sin punto |
| Migración de las 32 áreas y los 198 cargos |

---

### Fase 3 · Personal y firmas

**Entrega:** registrar una persona de punta a punta y ver su hoja de vida.

| Contenido |
|---|
| **Captura rápida**, con validación de unicidad al escribir |
| **Cola de fotos**, con disparo y avance |
| **Completitud por hitos**, con su registro declarativo por módulo |
| Excepción de punto de marcación por persona |
| Registro completo, por hitos y con dueño distinto por tramo |
| Todos los campos del inventario |
| Códigos generados, con validación de unicidad |
| Listado con filtros y exportación |
| Hoja de vida con su línea de tiempo |
| Historial temporal de cargo, área y salario |
| Solicitudes de actualización |
| Captura de firma y creación de la clave |
| Uso de la firma con validación |
| Disparadores a GLPI |
| Disparadores al gestor de identidad, listos y apagados |

**La hoja de vida nace aquí y se llena en las fases siguientes.**

---

### Fase 4 · Migración del maestro

**Entrega:** los datos reales dentro del sistema nuevo.

| Contenido |
|---|
| Mapeo de `personal` y `personal_datos` al modelo nuevo |
| Migración del historial temporal |
| Migración de las ~8.200 firmas |
| Generación del código de nómina para quien no lo tenga |
| Informe de inconsistencias |
| Conciliación de conteos |
| Migraciones escritas como código repetible |

---

### Fase 5 · Parámetros y vencimientos

**Entrega:** la configuración con vigencia administrable y las alertas funcionando.

**El modelo `Parametro` y `dominio/parametros.vigente_en()` ya existen desde la fase 3** (entregable E3.9 del plan de ejecución), porque el registro de personal necesita dos parámetros: el plazo del registro incompleto y las reglas del sufijo del código de nómina. Esta fase **no** crea el modelo: le pone administración y lo generaliza.

| Contenido |
|---|
| Pantalla de administración de parámetros |
| Catálogo de parámetros por módulo |
| Las tres clases de parámetro |
| Historial de vigencias |
| Calendario de festivos |
| Motor de vencimientos |
| Primer uso: examen médico y contrato a término fijo |

---

### Fase 6 · Marcaciones · captura

**Entrega:** las marcaciones entran solas y los dispositivos se vigilan.

| Contenido |
|---|
| Catálogo de dispositivos con su rol |
| Conexión a los biométricos |
| Recolección programada |
| Monitor de salud y aviso a soporte |
| Almacenamiento de la marcación cruda |
| Deduplicación y doble toque |
| Consulta de marcaciones crudas |
| Carga manual de respaldo |
| Migración del histórico de marcaciones |

---

### Fase 7 · Marcaciones · turnos y programación

**Entrega:** los jefes programan turnos sin entrar a BioTime.

| Contenido |
|---|
| Catálogo de turnos con sus bloques |
| Turnos gemelos para semanas con festivo |
| Todos los atributos del turno |
| Programación semanal por área |
| Selección masiva y rotación en bloque |
| Patrones de rotación |
| Detección de festivos con propuesta |
| Cambios puntuales con trazabilidad |
| Vista de matriz y vista de calendario |
| Migración de los turnos y la programación vigente |

**Es la fase con más riesgo de interfaz del proyecto.**

---

### Fase 8 · Marcaciones · motor de cálculo

**Entrega:** el cálculo reproduce exactamente un ciclo ya liquidado.

| Contenido |
|---|
| Las 167 condiciones del catálogo, portadas a `dominio/jornada/` |
| Pruebas, una por condición |
| Jornada fija y escalera |
| Segmentación y clasificación |
| Umbral y semana operativa |
| Café, tránsito y lactancia |
| Dirección y confianza |
| Invariantes de integridad |
| Consola de excepciones |

**Criterio de aceptación:** reproducir el ciclo de referencia con sus cifras exactas.

---

### Fase 9 · Marcaciones · aprobación y cierre

**Entrega:** horas aprobadas por el jefe y período cerrado de forma inmutable.

| Contenido |
|---|
| Bandeja de horas extra del jefe |
| Aprobación y rechazo con motivo |
| Topes semanal y mensual, con alerta |
| Corrección de marcación con auditoría |
| Vista en vivo de quién está en turno |
| Período con estados |
| Cierre inmutable y reapertura con rol elevado |
| Recálculo histórico con parámetros vigentes |
| Reportes de asistencia, calidad y cobertura |

---

### Fase 10 · Nómina · archivo plano

**Entrega:** el archivo que se carga a SINERGY sale de SIRH+. **BioTime se apaga.**

| Contenido |
|---|
| Catálogo de conceptos con vigencia de códigos |
| Consolidación por empleado y concepto |
| Generación del archivo plano con su formato exacto |
| Separación por empresa |
| Validación previa y bloqueo del cierre |
| Registro de exportaciones |
| Reproceso y ajuste |
| Contraste contra el período anterior |
| **Conciliación: tres meses en paralelo** |

---

### Fase 11 · Eventualidades

**Entrega:** la hoja de vida se llena con todo lo que le pasa a una persona.

| Contenido |
|---|
| Modelo unificado y catálogo de tipos |
| Los siete tipos con sus campos |
| Seguimiento de accidentes |
| Descargos con acceso restringido |
| Exámenes médicos con adjunto |
| Retiro, que dispara el paz y salvo |
| Cruce con marcaciones para ausentismo |
| Migración de 1.524 accidentes, 98.101 ausencias, 36.604 incapacidades, 4.296 descargos, 2.672 exámenes y 8.502 retiros |

---

### Fase 12 · Registros firmados y notificaciones

**Entrega:** el motor común del que dependen cinco módulos.

| Contenido |
|---|
| Formatos versionados |
| Flujo de firmas en orden |
| Folio consecutivo |
| Cierre inmutable y PDF |
| Primer uso: paz y salvo de retiro |
| Bandeja unificada de pendientes |
| Notificación por correo y en portada |

---

### Fase 13 · Trámites y vista del colaborador

**Entrega:** la autoconsulta y las solicitudes en línea. **El colaborador entra al sistema por primera vez.**

| Contenido |
|---|
| Catálogo de tipos de solicitud |
| Radicación, estados y enrutamiento |
| Flujo de firmas |
| Vacaciones con causación y saldo |
| Permisos con sus doce motivos |
| Certificado laboral |
| PQR |
| Bandejas del jefe y de RH |
| Primera versión de la cara de colaborador |

---

### Fase 14 · Formación · divulgaciones

**Entrega:** la divulgación de documentos de calidad. **COPEC se apaga.**

| Contenido |
|---|
| Conexión de solo lectura a Daruma |
| Catálogo de documentos y detección de versión |
| Matriz de capacitación operativa |
| Programación de divulgación por el jefe |
| Lectura y firma de la constancia |
| Seguimiento de quién leyó |
| Reasignación de matriz al cambiar de cargo |
| Migración del histórico de COPEC |

---

### Fase 15 · Formación · inducción y cursos

| Contenido |
|---|
| Contenido de la inducción por secciones |
| Cuenta de pre-ingreso |
| Evaluación y constancia verificable |
| Catálogo de cursos |
| Constructor de curso y de evaluación |
| Nota mínima y reintentos |
| Certificado al aprobar |
| Seguimiento de avance |

---

### Fase 16 · Formación · R-RH-009

| Contenido |
|---|
| Registro de capacitación con su cabecera |
| Individual o grupal |
| Instructor externo sin usuario |
| Carga de asistentes y firma en tableta |
| Revisión, folio y cierre por RH |
| Consulta y exportación |
| Migración de 29.171 capacitaciones y 396.564 asistencias |

---

### Fase 17 · Competencias

| Contenido |
|---|
| Constructor del formato R-RH-053 |
| Grupos, pesos y conductas |
| Versionado del formato |
| Evaluación por el jefe |
| Cálculo de la nota ponderada |
| Histórico con la versión usada |
| Alerta a los diez meses |
| Matriz SST |
| Migración de 4.750 calificaciones y 6.779 definiciones |

---

### Fase 18 · Dotación y EPP

| Contenido |
|---|
| Catálogo leído de la base de dotación |
| Tallas y ciclos |
| Jornada de entrega |
| Firma del colaborador |
| EPP por separado |
| Pendientes para el paz y salvo |
| Migración de 171.860 entregas y 9.816 registros de EPP |

---

### Fase 19 · Encuestas y reservas

| Contenido |
|---|
| Constructor de encuesta y tipos de pregunta |
| Anonimato con tabla separada |
| Segmentación y publicación |
| Análisis y exportación |
| Catálogo de recursos y calendario |
| Reserva con tope de seis horas |

---

### Fase 20 · Contenido y portal público

| Contenido |
|---|
| Noticias con categorías y programación |
| Convocatorias internas |
| Beneficios |
| Espacio del Fondo de Empleados, con usuario propio |
| Moderación por RH |
| Directorio y cumpleaños |
| Portada pública |

---

### Fase 21 · Indicadores e informes

| Contenido |
|---|
| Rotación, ausentismo e incapacidades |
| Indicadores de SST, formación, competencias y trámites |
| Consulta por rango libre |
| Desglose por área, cargo, vínculo y período |
| Panel configurable |
| Exportación |
| **Conciliación contra los informes del sistema viejo** |

---

### Fase 22 · Histórico y cierre

| Contenido |
|---|
| Módulo de consulta histórica, para lo anterior a cinco años |
| Política de retención |
| Verificación final de migración |
| Documentación de cierre |
| **Apagado del SIRH antiguo** |

---

# PARTE III · LO QUE SE REEMPLAZA

Esto es lo que se lleva a gerencia.

| Sistema | Qué hace hoy | Cuándo se apaga | Qué se gana |
|---|---|---|---|
| **BioTime** | Marcaciones, turnos y cálculo de horas | Fase 10 | Cálculo correcto de horas extra, programación de turnos propia, y una sola ruta al archivo de nómina |
| **COPEC** | Divulgación de documentos de calidad | Fase 14 | Un sistema menos que mantener, integrado a la hoja de vida |
| **SIRH antiguo** | Personal, eventualidades, formación, competencias, dotación | Fase 22 | Sin inyección SQL, sin contraseñas en MD5, con autorización real y auditoría |
| **Excel de códigos de nómina** | Cruce manual, 437 de 1.094 personas | Fase 3 | Nadie se pierde del archivo de nómina en silencio |
| **Herramienta de horas en HTML** | Cálculo correcto, pero sin aprobación ni cierre | Fase 9 | Aprobación con roles, cierre inmutable y trazabilidad |

## Riesgos que el proyecto cierra

| Riesgo abierto hoy | Cómo se cierra |
|---|---|
| Inyección SQL en 245 consultas | Fase 0: ORM y SQL parametrizado |
| Contraseñas en MD5 con retroceso a texto plano | Fase 1: identidad centralizada, credenciales nuevas |
| Autorización puramente cosmética | Fase 1: verificación en el servidor en cada ruta |
| Credenciales y tokens legibles en la base | Fase 0: `.env`, y rotación inmediata de los actuales |
| Un retiro no revoca accesos | Fase 3: disparador al gestor de identidad |
| Sin auditoría de quién hizo qué | Fase 1: bitácora inmutable |
| Sin respaldo del código fuente | Fase 0: Git |
| Personas que no entran al archivo de nómina sin aviso | Fase 10: bloqueo del cierre |
| Horas extra calculadas con redondeo incorrecto | Fase 8: motor validado |

---

## Dependencias externas al proyecto

| # | Qué hace falta | Bloquea |
|---|---|---|
| 1 | API de los biométricos | Fase 6 |
| 2 | Acceso de lectura a Daruma | Fase 14 |
| 3 | Gestor de identidad en producción | Salida a producción |
| 4 | Máquina de producción | Puesta en marcha |
| 5 | Código y porcentaje vigente del recargo dominical | Fase 10 |
| 6 | Decisión sobre Granservicios en el archivo de nómina | Fase 10 |
| 7 | Formatos en blanco de R-RH-009, R-RH-053 y paz y salvo | Fases 12, 16 y 17 |
| 8 | Contenido de la inducción | Fase 15 |
