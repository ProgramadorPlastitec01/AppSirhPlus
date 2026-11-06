# SIRH+ — Documento maestro de contexto

**Plastitec S.A.S. · Tecnología de Información**
Versión 1.0 · 5 de noviembre de 2026
Estado del proyecto: **planeación avanzada. No hay una sola línea de código escrita.**

---

## 0. Para qué sirve este archivo

Este documento existe para que cualquier persona —o cualquier sesión nueva de Claude, sin memoria de las conversaciones anteriores— entienda **el proyecto completo** sin leer los ocho documentos de diseño anteriores.

Reemplaza a `claude/context.md`, que quedó desactualizado en cifras y en alcance.

Contiene tres cosas, en este orden:

1. **Qué existe hoy** — la organización, los sistemas, el diagnóstico del sistema viejo.
2. **Qué se decidió** — stack, arquitectura, principios, y el porqué de cada uno.
3. **Qué se va a construir** — cada módulo, con el detalle funcional que se levantó con el área.

**Regla de precedencia:** si este documento contradice a un documento más específico (por ejemplo `08-modulo-marcaciones.md`), gana el específico — y entonces este archivo está desactualizado y hay que corregirlo. Si este documento contradice al código, gana el código y hay que corregir este archivo.

---

# PARTE I · EL CONTEXTO

---

## 1. El proyecto en una página

Plastitec S.A.S. es una empresa manufacturera colombiana con **alrededor de 1.100 personas** entre personal directo, temporal y aprendices SENA, repartidas en producción farmacéutica, producción de insumos, mantenimiento, almacén y áreas administrativas.

Su sistema de Recursos Humanos se llama **SIRH**. Está escrito en Java 8 sobre JSP, no tiene control de versiones, tiene inyección SQL sistémica, guarda contraseñas en MD5 sin salt con retroceso a texto plano, y su autorización es puramente cosmética. No se puede mantener ni asegurar.

**SIRH+** es su reemplazo. No es una migración ni un refactor: es una reingeniería que conserva el conocimiento funcional y descarta el código.

Además, SIRH+ **absorbe otros dos sistemas**:

- **COPEC**, el aplicativo que hoy controla que cada jefe divulgue a tiempo los documentos de calidad de su área.
- **BioTime**, el software del fabricante de los biométricos, del que hoy depende todo el control de tiempo y asistencia.

Y **extiende** el alcance con un **Portal del Colaborador**: la cara de autoservicio que hoy no existe, donde cada persona consulta su información y radica sus solicitudes sin interrumpir a Recursos Humanos.

El objetivo no es una versión más bonita del sistema actual. Es construir la plataforma de Recursos Humanos de la organización para los próximos diez años: robusta, segura, escalable, mantenible y preparada para evolucionar.

---

## 2. La organización, en los datos que importan

| Dimensión | Dato |
|---|---|
| Personal total | ~1.100 personas |
| Reparto por empresa | ~600 Plastitec S.A. · ~500 Granservicios (temporal) |
| Personal que rota turno | 65 %–70 % del total |
| Tipos de vínculo | Directo, temporal (Granservicios), aprendiz SENA. **Los contratistas no se registran** |
| Niveles del organigrama | 9: operativo, auxiliar, técnico, asistente, coordinador, jefatura, dirección, gerencia, junta directiva |
| Sedes | Planta 1 y Planta 2 (no se manejan como dimensión de reporte) |
| Biométricos | 10 dispositivos: 4 vestieres, 2 porterías, almacén, extrusión, recepción, producción insumos |
| Volumen de marcaciones | ~71.000 registros en un mes |
| Equipo de desarrollo | **Una persona**, con apoyo de Claude Code y un QA ocasional |
| Dedicación | ~5 horas diarias |
| Infraestructura | On-premise, red interna `172.16.x.x` |
| Datos sensibles | Salud ocupacional, incapacidades, exámenes médicos, salarios → **Ley 1581 de 2012** |
| Retención | 5 años en línea; lo anterior pasa a un módulo de consulta histórica |

### 2.1 Lo que esto implica

**Este sistema no necesita microservicios, ni Kafka, ni Kubernetes, ni CQRS.** El volumen es bajo y predecible; la complejidad está en las reglas de negocio, no en la escala. El cuello de botella real es la **mantenibilidad**, porque quien lo mantenga va a ser una sola persona.

Necesita un monolito bien construido, con módulos claros, seguridad real, un núcleo de dominio probado y capacidad de evolucionar.

---

## 3. El sistema actual: diagnóstico

Análisis estático del 29 de septiembre de 2026 sobre el código fuente de SIRH, sin acceso a la base de datos.

### 3.1 Qué hay

| Aspecto | Dato |
|---|---|
| Lenguaje y plataforma | Java 8, Tomcat, NetBeans + Ant, EclipseLink 2.5 |
| Base de datos | MySQL en `172.16.2.111/sirh` |
| Java | 111 archivos, 29.116 líneas |
| JavaScript | 247 archivos, 130.307 líneas |
| JSP | 17 archivos |
| **Procedimientos almacenados** | **207** |

### 3.2 Los cinco hallazgos que deciden el proyecto

1. **La lógica de negocio vive en la base de datos.** Los 207 procedimientos almacenados contienen las reglas reales; la capa Java es un orquestador delgado. **Ese es el activo a rescatar, y el entregable más valioso de toda la etapa de análisis.**

2. **La vista se genera desde Java.** `Tag_seguimiento.java` tiene 3.394 líneas en un solo método `doStartTag()`, concatenando HTML con `out.print`. No es mantenible por nadie.

3. **Inyección SQL sistémica.** 245 llamadas a `createNativeQuery` por concatenación de cadenas. **Cero `setParameter`.**

4. **La autorización es cosmética.** Los permisos solo se consultan para decidir qué pintar en el menú. Ningún filtro protege las rutas: quien conozca una URL entra.

5. **Contraseñas en MD5 sin salt**, con retroceso a texto plano para claves de menos de 8 caracteres. Credenciales de base de datos escritas en el código fuente.

Sumado a eso: sin git, sin gestión de dependencias (20 JAR sueltos), sin pruebas, sin logs, sin auditoría, y un `sirh.json` con datos personales de cientos de empleados dentro del proyecto.

### 3.3 Conclusión

No es un sistema viejo pero sano. Refactorizar en sitio cuesta más que reconstruir y deja intactos los problemas estructurales. **Se reconstruye la capa de aplicación, se rediseña el modelo de datos, y el sistema viejo opera en paralelo hasta que cada módulo esté reemplazado.**

Lo que se conserva no es el código: es el **conocimiento funcional** —los 207 procedimientos, el modelo de datos, el mapa de módulos y los datos históricos.

### 3.4 Acciones urgentes sobre el sistema actual

Independientes de SIRH+, porque el riesgo es hoy:

1. Git ya. No existe respaldo del código fuente.
2. Sacar las credenciales del repositorio y **rotarlas todas**.
3. Quitar `schema-generation.database.action=create` de `persistence.xml`.
4. Eliminar el retroceso a contraseña en texto plano.
5. Agregar un filtro que exija sesión válida en todas las rutas salvo login.
6. Desactivar los servlets de FCKeditor si no se usan.
7. Sacar `sirh.json` del proyecto.

Los puntos 1 a 5 son días de trabajo y cierran las exposiciones más graves.

---

## 4. El ecosistema: seis sistemas externos

SIRH+ no vive solo. Esta es la relación con cada sistema vecino, y hacia dónde va.

| Sistema | Qué es | Relación hoy | Relación objetivo |
|---|---|---|---|
| **BioTime** | Software del fabricante de los biométricos | Fuente de marcaciones y de todo el cálculo de horas | **Desaparece.** SIRH+ se conecta directo a los dispositivos en LAN |
| **SINERGY** | Sistema de nómina | Sin conexión. Se le carga un archivo plano al cierre de mes | Igual, hasta que exponga API |
| **Daruma** | Gestor documental de calidad | Lectura directa a su base MySQL (lo hace COPEC) | Lectura directa desde SIRH+ |
| **MANT** | SQL Server de dotación | Catálogo de elementos de dotación | Lectura para asignar dotación |
| **GLPI** | Mesa de ayuda / tickets | SIRH crea usuarios por API al registrar personal | **Se conserva tal cual.** Funciona bien |
| **IAM / Maestro** | Gestor de identidad centralizado | En construcción por otro desarrollador | SIRH+ es su fuente de verdad de personas |

### 4.1 La relación con el IAM es asimétrica, y eso es lo importante

```
SIRH+  ──── ciclo de vida de la persona ────▶  IAM
       (ingresó, cambió de área, se retiró)   (crea / ajusta / revoca identidad)

SIRH+  ◀─── autenticación y sesión ─────────  IAM
       (¿quién es? ¿sigue activo?)
```

**SIRH+ es el único sistema de la organización que sabe quién trabaja aquí.** Ningún otro aplicativo se entera de un ingreso, un cambio de cargo o un retiro. Eso lo convierte en el origen del ciclo de vida de la identidad, no en un consumidor más.

Si esto se implementa bien, la organización gana algo que hoy no tiene:

> **Cuando RH registra un retiro, el acceso a *todos* los aplicativos se revoca automáticamente, el mismo día.**

Hoy eso depende de que alguien se acuerde de avisar, aplicativo por aplicativo. Es, probablemente, el mayor riesgo de seguridad abierto de la organización.

### 4.2 La frontera entre identidad y permisos

El error más común al centralizar identidad es meter todo en la maestra. Hay cuatro conceptos distintos:

| Concepto | Qué es | Dueño |
|---|---|---|
| **Persona / Empleado** | Un ser humano con documento, nombre, cargo, área | **SIRH+** |
| **Identidad** | Una cuenta que puede autenticarse | **IAM** |
| **Acceso a aplicativo** | El vínculo identidad ↔ aplicativo, con su rol de alto nivel | **IAM** |
| **Permisos** | Qué puede hacer *dentro* del aplicativo | **Cada aplicativo** |

**La regla crítica: el IAM no debe conocer los permisos internos de SIRH+.** Si los conociera, cada funcionalidad nueva obligaría a modificar el sistema del que dependen todos los demás.

- **El IAM dice:** «esta identidad existe, está activa, y tiene acceso a SIRH+ con el rol `ANALISTA_RRHH`».
- **SIRH+ dice:** «el rol `ANALISTA_RRHH` significa estos 14 permisos».

---

## 5. Los tres identificadores de una persona

Esto parece un detalle y es una de las piezas más delicadas del modelo.

| Identificador | Qué es | Quién lo asigna | Dónde se usa |
|---|---|---|---|
| **Documento (cédula)** | Identificación legal | El Estado | Trámites, certificados, firma |
| **Código interno** | Consecutivo de 4 dígitos al ingresar | SIRH+ | Biométricos, firma digital, llave operativa |
| **Código de nómina (`COD_SINER`)** | Cédula + un dígito según el vínculo | SIRH+, por regla parametrizada | **Archivo plano de nómina** |

### 5.1 La regla del código de nómina

Se construye a partir de la cédula más un dígito que depende del tipo de vínculo:

| Vínculo | Sufijo | Ejemplo |
|---|---|---|
| Aprendiz SENA | `1` | `10216724331` |
| Temporal | `2` | — |
| Directo | según política | — |
| Reingreso | otro dígito | — |

**Los sufijos son parametrizables desde el módulo de configuración**, porque RH puede cambiar la política.

**Reglas inviolables del campo:**

- **No es editable** por quien registra al personal. Se genera.
- **Es único contra el histórico completo**, no contra los activos. Un temporal que pasa a directo y luego reingresa puede colisionar con un código ya usado.
- **No se normalizan los ceros a la izquierda** al exportar. La herramienta actual los quita, y eso puede liquidar mal a alguien.
- **Sin código de nómina no se cierra el período.** Hoy esas personas desaparecen del archivo en silencio.

> **Riesgo medido hoy:** el maestro tiene 1.108 empleados. El Excel que mantiene los códigos de nómina tiene 437 filas. El archivo plano de septiembre salió con 297 personas. El resto, sencillamente, no se liquida por esa vía y nadie recibe un aviso.

---

# PARTE II · LAS DECISIONES

---

## 6. Decisiones cerradas

No se reabren sin razón nueva. Si al implementar algo de aquí no se sostiene, va a `docs/pendientes.md` como decisión a revisar; no se cambia sobre la marcha.

### 6.1 Stack — el del estándar de Plastitec, sin modificaciones

| Capa | Tecnología |
|---|---|
| Lenguaje | Python 3.11+ |
| Framework | Django 5.2 LTS, renderizado en servidor |
| Base propia | PostgreSQL 17 vía `psycopg[binary]` |
| Sistemas ajenos | Solo lectura, en capa aislada, **nunca** en `DATABASES` |
| Plantillas | Django Template Language |
| Frontend | **CSS plano + JavaScript vanilla** |
| Exportación | `openpyxl` (Excel), `reportlab` (PDF) |
| Servidor | Gunicorn tras Nginx, bajo systemd, Rocky Linux 9 |
| Pruebas | `unittest` de la biblioteca estándar |
| Configuración | `django-environ` leyendo `.env` |
| Control de versiones | Git, en GitHub |

**Prohibido, sin excepción:**

- Build de frontend (Node, npm, webpack, Tailwind)
- Librerías JavaScript de terceros
- Recursos desde CDN — todo se auto-hospeda en `static/vendor/`
- Escribir en la base de un sistema ajeno
- Duplicar una regla de negocio en JavaScript

### 6.2 Por qué este stack y no otro

La primera recomendación de este proyecto fue Java 21 + Spring Boot, con el argumento de la continuidad: «el equipo ya sabe Java».

**Ese argumento era incorrecto, porque identificó mal cuál es el activo de continuidad.** El activo no es el código Java de SIRH —ese se descarta completo—. El activo es **el estándar de desarrollo de Plastitec y las aplicaciones que ya corren sobre él**: reglas escritas, agentes configurados, un protocolo de arranque y lecciones acumuladas de código real.

Construir SIRH+ en Java significaría ser la única aplicación Java de la organización, mantenida por una sola persona, con los agentes y las reglas del estándar sin aplicar. A cambio de reutilizar conocimiento de un código que de todas formas se va a botar. Es un mal negocio.

| Opción evaluada | Por qué no |
|---|---|
| Java 21 + Spring Boot | Sería la única app Java de la empresa; el estándar no aplicaría |
| Mantener Java 8 + JSP | Fuera de soporte. Nacería obsoleto |
| Microservicios | Resuelven escalado independiente y equipos separados. Aquí no existe ninguno de los dos problemas |
| SPA (React + API) | Dos aplicaciones para mantener por una persona, sobre pantallas que son formularios, tablas y filtros |
| Low-code (Mendix, OutSystems) | Licenciamiento recurrente, dependencia del proveedor, y techo al llegar a lógica compleja como la de nómina |
| HTMX | Lo que el sistema necesita está cubierto por CSS y JS plano. Si una pantalla demuestra lo contrario, esa es la evidencia para pedir la desviación |
| Tailwind | Los design tokens cumplen la misma función sin build |
| LMS comercial | Se evaluó para cursos. Se decidió construir |

### 6.3 Núcleo de dominio puro

`dominio/` es un paquete Python **sin Django y sin entrada/salida**: recibe datos, devuelve resultados, y sus pruebas corren en milisegundos.

Ahí van las reglas que hoy están enterradas en los procedimientos almacenados y en un archivo HTML: horas extra, recargos, rotación, indicadores SST, vigencias, calificación de competencias, causación de vacaciones.

Es la regla más importante del estándar, y para este proyecto es también la que más valor entrega: **es lo que permite probar la lógica de nómina sin levantar una base de datos.**

### 6.4 Regla de dependencias entre capas

```
config/  →  módulos  →  dominio/
```

Nunca hacia arriba. Nunca circular.

### 6.5 Una sola fuente por dato

Cada dato tiene un dueño y uno solo. Si dos módulos llevan su propia cuenta de lo mismo, en pocos meses hay dos cifras distintas y nadie sabe cuál vale.

> **Excepción documentada, octubre de 2026.** Los datos contractuales que necesita el certificado laboral —cargo, fecha de ingreso, tipo de contrato, salario— se sostienen en SIRH+, porque SINERGY no expone API. Van con una fecha de corte visible que se imprime en el certificado, y la excepción desaparece sola cuando SINERGY se conecte.

### 6.6 El Portal no es una aplicación aparte

Esta decisión se tomó en noviembre de 2026 y cambia el diseño original.

El Portal del Colaborador **no se construye como un sistema separado**. Es la **capa de visibilidad de colaborador** sobre los mismos módulos de SIRH+.

Trámites aparece dos veces en el alcance (solicitar / aprobar). Igual capacitaciones, encuestas, marcaciones y competencias. Si eso se construye dos veces, se duplica la regla de negocio y diverge en seis meses.

**La regla es: un módulo, tres vistas.**

| Vista | Quién | Qué ve |
|---|---|---|
| **Pública** | Cualquiera, sin sesión | Noticias, organigrama, convocatorias |
| **Colaborador** | Persona autenticada | Lo suyo, y solo lo suyo |
| **Gestión** | Jefes y RH | Su personal (jefe) o todo (RH) |

La aplicación tiene una sola puerta. Al validar la sesión aparece la información personal; quien tenga rol de gestión ve además una entrada a «Recursos Humanos» que lleva a la administración del módulo.

---

## 7. Arquitectura de la aplicación

```
sirh_plus/
├── dominio/                 ★ reglas puras, sin Django, sin I/O
│   ├── jornada/             horas extra, recargos, escalera, semana
│   │   ├── festivos.py
│   │   ├── marcaciones.py
│   │   ├── turnos.py
│   │   ├── segmentacion.py
│   │   ├── clasificacion.py
│   │   ├── parametros.py    ★ vigencia por fecha
│   │   └── conceptos.py     archivo plano
│   ├── vacaciones.py        causación, saldo, fraccionamiento
│   ├── competencias.py      ponderación y nota final
│   ├── indicadores.py       rotación, ausentismo, SST
│   └── vencimientos.py      motor de vigencias
├── tests/                   pruebas del núcleo, sin Django
│
├── config/                  settings, urls, wsgi
├── core/                    checks, utilidades, base
├── cuentas/                 adaptador de identidad, roles, permisos
│
├── personal/                personas, vínculos, historial temporal
├── maestros/                áreas, cargos, dependencias, calendario
├── firmas/                  ★ transversal: captura, validación, estampado
├── registros/               ★ transversal: motor de registros firmados
├── parametros/              ★ transversal: configuración con vigencia
├── notificaciones/          ★ transversal: correo, cartelera, bandeja
├── auditoria/               ★ transversal: quién hizo qué y cuándo
│
├── marcaciones/             dispositivos, turnos, programación, cálculo
├── nomina/                  conceptos, períodos, cierre, archivo plano
├── eventualidades/          modelo unificado de novedades
├── tramites/                solicitudes, aprobaciones, certificados, PQR
├── formacion/               inducción, cursos, divulgaciones, matriz
├── competencias/            formatos, evaluaciones, histórico
├── dotacion/                catálogo, asignación, entrega
├── encuestas/               constructor, publicación, análisis
├── reservas/                salas y recursos
├── reportes/                informes, indicadores, exportación
│
├── biometricos_api/         ← conexión LAN a los dispositivos
├── daruma_db/               ← solo lectura: MySQL de calidad
├── mant_db/                 ← solo lectura: SQL Server de dotación
├── glpi_api/                ← cliente GLPI (se conserva)
├── identidad_api/           ← cliente IAM + outbox
├── sirh_legacy_db/          ← solo lectura: MySQL viejo, migración
│
├── templates/
├── static/
└── deploy/
```

Cada módulo con sus `views.py` / `consultas.py` / `presentacion.py` / `exportacion.py`, según la regla del estándar.

---

## 8. Los seis componentes transversales

Estos no son módulos funcionales. Son infraestructura que **se construye una vez** y de la que dependen casi todos los demás. Construirlos tarde obliga a rehacer medio sistema.

### 8.1 Firmas

Una persona que ingresa a la empresa crea **una firma digital** que es válida durante toda su estancia. Se dibuja en una tableta al momento del registro, y se guarda como coordenadas que se trazan en negro.

| Aspecto | Decisión |
|---|---|
| Captura | Una sola vez, al ingreso, en tableta |
| Almacenamiento | Coordenadas + cédula + código interno |
| Uso | Se estampa en el documento invocando el id de la firma |
| **Autorización de uso** | **Contraseña propia del colaborador**, creada en la inducción |
| Restablecimiento | TI, desde el gestor de identidades |
| Migración | Las firmas existentes se migran por código interno |
| Salida | El documento firmado se descarga en PDF con las firmas estampadas |

**Por qué contraseña y no cédula + código interno**, que es lo que se usa hoy: ambos datos son conocidos por terceros. Cualquiera que sepa la cédula y el código de un compañero puede firmar por él. Dado que no se puede usar correo ni celular como segundo factor —no todos tienen—, la contraseña propia es la única opción robusta.

**Dónde se usa:** solicitud de vacaciones, permisos, divulgación de documentos, R-RH-009, R-RH-053, entrega de dotación, paz y salvo de retiro.

### 8.2 Motor de registros firmados

Seis procesos distintos resultaron ser el mismo patrón. Se construye una vez:

```
formato versionado → diligenciar → firmas en orden → folio → cierre inmutable → PDF
```

| Registro | Quiénes firman | Quién cierra |
|---|---|---|
| R-RH-009 · Capacitación | Instructor + asistentes | RH (asigna folio) |
| R-RH-053 · Competencias | Jefe (y el evaluado, por definir) | RH |
| Solicitud de vacaciones | Colaborador → jefe → RH | RH |
| Solicitud de permiso | Colaborador → jefe → RH | RH |
| Divulgación de documento | Colaborador | Automático |
| Entrega de dotación | Colaborador | RH |
| Paz y salvo de retiro | Trabajador + jefe + RH | RH |

**Propiedades obligatorias del motor:**

- El formato se **versiona**. Un registro histórico conserva la versión con la que se diligenció.
- El folio es un **consecutivo que no se reinicia**.
- Cerrado es **inmutable**. Ninguna corrección posterior modifica el documento; se emite uno nuevo.
- Todo queda en auditoría: quién firmó, cuándo, desde dónde.

### 8.3 Motor de vencimientos

Cuatro necesidades distintas, un solo mecanismo:

| Qué vence | Plazo | Alerta |
|---|---|---|
| Examen médico periódico | 12 meses (parametrizable por cargo) | Al cumplirse |
| Evaluación de competencias | 12 meses | A los 10 meses |
| Documento de la matriz de capacitación | Al publicarse una versión nueva en Daruma | Inmediata |
| Contrato a término fijo | Según fecha de fin | Configurable |

Estados: **al día · próximo a vencer · vencido**. El sistema avisa, no bloquea.

### 8.4 Parámetros con vigencia

**Este es el componente que más veces se subestima y más caro sale.**

Un parámetro legal no se guarda como un valor. Se guarda como **valor + fecha desde la que rige**, y el cálculo busca el que estaba vigente en la fecha del hecho.

Sin esto, recalcular un mes ya cerrado da un resultado distinto al que se pagó, y no hay forma de defenderlo ante una auditoría.

**No es una hipótesis.** La jornada semanal viene bajando por etapas, el recargo dominical viene subiendo por etapas, y la hora de inicio de la jornada nocturna cambió por reforma. En los archivos reales del sistema actual conviven tres escalones distintos de la misma norma al mismo tiempo.

Tres clases de parámetro, las tres con auditoría de quién las cambió:

| Clase | Ejemplos | Comportamiento |
|---|---|---|
| **Legal con vigencia** | Jornada semanal, inicio de franja nocturna, porcentajes de recargo, códigos de concepto | Valor + fecha desde. **Nunca se sobrescribe** |
| **Política interna** | Tolerancia de puntualidad, tope de extras, nota mínima de competencias, mínimo de días de vacaciones, sufijos del código de nómina | Valor + fecha desde |
| **Operativo** | Festivos, fechas de corte, salas, roles de dispositivo | Editable, con auditoría |

El módulo de configuración se organiza **por módulo**, es exclusivo del administrador, y cada parámetro lleva su descripción y su fundamento.

### 8.5 Notificaciones

| Canal | Alcance | Validez |
|---|---|---|
| **Cartelera en papel** | Todos | Es el aviso con validez legal hoy |
| **Correo** | Quien tenga | Complementario |
| **Portada del portal** | Todos los autenticados | Anuncios de RH y del Fondo de Empleados |
| **Bandeja de pendientes** | Jefes y RH | Lo que requiere su acción |

**La bandeja unificada de pendientes es crítica.** Si cada módulo tiene su propia bandeja, los jefes no van a entrar. Un jefe debe tener un solo lugar donde ve todo lo que espera por él: horas extra por aprobar, solicitudes de su gente, evaluaciones vencidas, divulgaciones sin leer de su área.

### 8.6 Auditoría y trazabilidad

Obligatoria por Ley 1581 y por el módulo de nómina.

Todo cambio sobre un dato sensible registra **quién, qué, cuándo, desde dónde y el valor anterior**. Con prioridad absoluta en: marcaciones corregidas, horas aprobadas, salarios, descargos, firmas usadas, parámetros modificados y cierres de período.

Esta es, además, una capacidad que el sistema debe **exhibir**: poder abrir la hoja de vida de una persona y ver su recorrido completo —cargos, capacitaciones, eventualidades, evaluaciones, dotación— es uno de los objetivos declarados del proyecto.

---

# PARTE III · LOS MÓDULOS

---

## 9. Mapa de módulos

| # | Módulo | Vista colaborador | Vista jefe | Vista RH |
|---|---|---|---|---|
| 1 | Personal | Mis datos, solicitar actualización | Su personal | Todo |
| 2 | Empresa y organigrama | Ver (público) | Ver | Administrar |
| 3 | Marcaciones | Mis marcaciones | Programar, corregir, aprobar | Todo + cierre |
| 4 | Nómina | — | — | Archivo plano, períodos |
| 5 | Eventualidades | Las mías | Las de su personal | Todo |
| 6 | Trámites | Solicitar | Aprobar | Aprobar y aplicar |
| 7 | Formación | Hacer, leer, firmar | Programar su área | Todo + folios |
| 8 | Competencias | Ver la propia | Evaluar su personal | Todo + formatos |
| 9 | Dotación | Mis entregas | — | Asignar y entregar |
| 10 | Encuestas | Responder | — | Crear y analizar |
| 11 | Reservas de salas | Reservar | — | Administrar |
| 12 | Indicadores e informes | — | Los de su área | Todo |

---

## 10. Personal

**Dueño de:** la persona y su historia laboral dentro de la empresa.

### 10.1 Qué registra

| Grupo | Campos |
|---|---|
| **Identificación** | Documento, nombres, apellidos, género, fecha de nacimiento, foto |
| **Perfil** | Grupo sanguíneo, nivel educativo, número de hijos |
| **Vínculo** | Tipo (directo / temporal / aprendiz), estado, fecha de ingreso, fecha de contrato |
| **Códigos** | Código interno, código de nómina, código de firma |
| **Ubicación** | Cargo, área, empresa (Plastitec / Granservicios) |
| **Contacto** | Correo, teléfonos, contacto de urgencia, localidad |
| **SST** | Brigadista, restricciones físicas, restricciones médicas |

La foto del empleado **no existe hoy y se incorpora**.

### 10.2 Completitud por hitos

El registro **no se completa de una vez**. Se completa por etapas, cada una con su dueño y su consecuencia.

| % | Hito | Qué habilita | Quién |
|---|---|---|---|
| 10 | **Identificada** — documento, nombres, código interno | Existe en el sistema. Nada más | Quien recibe |
| 25 | **Vinculada** — tipo, empresa, fecha de ingreso | Se genera su código de nómina | Quien recibe |
| 40 | **Ubicada** — cargo y punto de marcación | Tiene jefe, hereda matriz, puede marcar | Quien recibe |
| 55 | **Habilitada** — firma y clave | Puede firmar y entrar al portal | Quien recibe |
| 70 | **Liquidable** — salario, EPS, caja, pensión | Entra al archivo de nómina | Permiso reservado |
| 85 | **Completa** — contacto, urgencia, SST | Cumple el perfil para SST y emergencias | RH |
| 100 | **Al día** — examen de ingreso e inducción | Sin pendientes de apertura | SST y Formación |

**Por qué hitos y no campos contados.** Un porcentaje por campos promedia cosas que no son comparables: el número de hijos y el código de nómina no pesan igual. Peor aún, da tranquilidad falsa — un 92 % se siente terminado, y lo que falta puede ser justo lo que bloquea la nómina.

**El umbral operativo es el 40 %, no el 10 %.** Bajo ese nivel la persona no puede trabajar: sin código el biométrico no la reconoce, y sin cargo nadie puede aprobarle nada. Por eso **un registro bajo el 40 % vale 24 horas**; pasado el plazo aparece en rojo, porque alguien está trabajando sin estar en el sistema.

**Los hitos los declara cada módulo.** `personal/` solo suma los declarados, sin importar de eventualidades ni de formación. Durante la fase 3 el tope real es 85 %, y los dos hitos finales aparecen cuando sus módulos existan.

**Los pesos y los hitos no son parametrizables.** Si RH pudiera moverlos, el porcentaje dejaría de significar lo mismo entre dos momentos y los informes históricos no se podrían comparar.

### 10.3 Captura rápida y cola de fotos

Dos necesidades distintas que el diseño separa:

| | Captura rápida | Carga masiva |
|---|---|---|
| Situación | Varias personas esperando, con su cédula en la mano | Granservicios envía una planilla |
| Entrada | Una pantalla, cinco campos, guardar y siguiente | Un archivo |
| Qué optimiza | Segundos por persona, sin perder el foco | Volumen de una vez |

**La captura rápida pide cinco campos:** documento, nombres, apellidos, código interno y cargo. El área, el nivel, el jefe, la matriz, el turno y el punto de marcación **los trae el cargo**: se muestran para confirmar, no se digitan.

**El código interno lo propone el sistema y se puede sobrescribir.** Quien tenga uno asignado lo escribe; quien no, acepta el siguiente consecutivo. En ambos casos se valida unicidad al escribir.

**La foto es una cola, no un campo.** La información suele llegar antes que la persona. Cuando llega, se dispara y se pasa a la siguiente. **La foto no pesa en la completitud**, porque no depende de quien registra.

**Unicidad verificada al escribir, no al guardar.** Documento y código interno son únicos contra el histórico completo. Un documento ya existente se avisa de inmediato, distinguiendo el duplicado del reingreso.

### 10.4 Punto de marcación

| Nivel | Regla |
|---|---|
| **Catálogo** | Un punto es un **conjunto de dispositivos**, no un equipo. Los cuatro vestieres de mujeres son un solo punto |
| **Cargo** | Define el punto por omisión. Un cargo sin punto deja todas sus marcaciones como excepción |
| **Persona** | Puede tener una excepción, con motivo, vigencia y autorizador, que queda en la bitácora |
| **Marcación** | Una marcación en un dispositivo no autorizado **nunca se descarta**: se registra y se señala como excepción |

La última regla es la más importante. Descartar una marcación sería perder un dato que vale dinero. El sistema no decide quién trabajó: lo registra y avisa que algo no cuadra.

### 10.5 Reglas

- **El salario y el contrato formal son de SINERGY.** SIRH+ sostiene la fecha de contrato porque la necesita para calcular, y los datos del certificado laboral por la excepción del §6.5.
- **Los contratistas no se registran.**
- **Historial temporal:** se debe poder saber qué cargo tenía una persona en una fecha pasada, no solo hoy. Esto no es opcional: la evaluación de competencias, la matriz de capacitación y el enrutamiento de aprobaciones dependen de la estructura vigente *en la fecha del hecho*.
- **Reingreso:** el registro se reactiva y queda la trazabilidad del reintegro. El código de nómina cambia, porque así lo exige la gestión en SINERGY.
- **El colaborador no edita sus datos.** Solicita una actualización que RH valida.
- **El registro es de dos manos como mínimo**, y puede ser de más: cada hito tiene su dueño.

### 10.6 Disparadores al registrar una persona

| Destino | Qué pasa |
|---|---|
| GLPI | Se crea el usuario por API. **Lógica existente, se conserva** |
| IAM | Se crea la identidad. **Código listo, apagado hasta que el IAM exista** |
| Firmas | Se captura la firma en tableta |
| Formación | Se le asigna la matriz de capacitación de su cargo |

### 10.7 El retiro dispara un proceso completo

1. Se registra la eventualidad de retiro.
2. Se genera el **paz y salvo**, que recorre cuatro áreas:

| Área | Qué verifica |
|---|---|
| Tecnología de Información | Computador, tablet, celular, impresora, claves, desactivación de cuentas de dominio, correo y conexiones externas |
| Seguridad | Tarjeta de acceso, lockers |
| Jefe inmediato | Información del PC, implementos de oficina, puesto de trabajo, herramientas |
| Recursos Humanos | Dotación, carné, EPP, consumo de restaurante, recargo nocturno, horas extra, descuento sindical, otros descuentos, **inactivación en SIRH, PAYFLOW y BIOTIME** |

3. Firman trabajador, jefe inmediato y RH.
4. Se revocan los accesos en los sistemas conectados.

---

## 11. Empresa y organigrama

**Dueño de:** áreas, cargos y la estructura de dependencias.

### 11.1 Por qué no es un CRUD de catálogos

El organigrama **es la tabla de enrutamiento del sistema**. De él dependen:

- Quién aprueba una solicitud de vacaciones o una hora extra
- Qué personal ve un jefe
- Quién evalúa las competencias de quién
- Quién programa las divulgaciones de un área

### 11.2 Reglas

- La jerarquía es **cargo reporta a cargo**, no persona a persona. Se configura al crear áreas y cargos, y de ahí sale tanto el organigrama como la cadena de aprobación.
- **Nueve niveles**, de abajo hacia arriba: operativo, auxiliar, técnico, asistente, coordinador, jefatura, dirección, gerencia, junta directiva.
- **El evaluador de competencias es el superior inmediato en la rama.** Un director financiero evalúa al jefe de compras; el jefe de compras evalúa al asistente de compras.
- **Un jefe por persona.** No se ha presentado la necesidad de jefes múltiples ni de encargados temporales, pero el modelo no debe cerrarse a ello.
- **La estructura se versiona.** Hay que poder saber quién era el jefe de quién en la fecha de una solicitud.
- **El organigrama es público.** Se puede ver sin iniciar sesión.

---

## 12. Marcaciones

Es el módulo **más grande, más riesgoso y mejor documentado** del proyecto. Tiene su propio documento: `08-modulo-marcaciones.md`.

### 12.1 Qué hace

Reemplaza por completo a BioTime:

1. **Recoge** las marcaciones crudas directamente de los biométricos en LAN.
2. **Vigila** que los dispositivos estén vivos y avisa a soporte cuando uno se cae.
3. **Programa** los turnos semanalmente, por área.
4. **Calcula** jornada ordinaria, horas extra y recargos según la ley colombiana.
5. **Somete** las horas extra a aprobación del jefe.
6. **Cierra** el período de forma inmutable.
7. **Genera** el archivo plano que se carga a SINERGY.
8. **Reporta** asistencia, puntualidad, calidad de marcación y cobertura.

### 12.2 El activo que ya existe

Existe una herramienta llamada **MOD_BIO** —dos archivos HTML autónomos— que ya implementa el motor de cálculo, validado contra 111.356 marcaciones reales y 1.095 empleados.

Viene con un **catálogo de 167 condiciones de negocio** verificadas línea por línea contra el código. De ellas, 102 están implementadas, 12 reemplazadas por un mecanismo mejor y 2 son decisiones conscientes de diseño.

**Ese catálogo es la suite de pruebas de `dominio/jornada/`.** No es común arrancar un módulo con los criterios de aceptación ya escritos y verificados.

Lo que MOD_BIO **no** puede hacer, por ser una herramienta local sin servidor, son 47 condiciones agrupadas en tres bloques: **aprobación con roles**, **cierre de período** y **conciliación**. Eso es exactamente lo que SIRH+ aporta.

### 12.3 Los conceptos de nómina

| Código | Concepto | Clave interna |
|---|---|---|
| `0200` | Hora extra diurna ordinaria | `EXT_D` |
| `0210` | Hora extra nocturna ordinaria | `EXT_N` |
| `0250` | Hora extra festiva diurna | `EXT_FD` |
| `0260` | Hora extra festiva nocturna | `EXT_FN` |
| `0220` | Recargo nocturno | `REC_N` |
| `0253` → `0252` | Recargo dominical / festivo | `REC_F` |
| `0259` → `0258` | Recargo nocturno festivo | `REC_FN` |

Los códigos de recargo dominical cambian por escalones de la ley. **Van en la tabla de vigencias, no en una fecha de corte única.**

Hay además conceptos que **no vienen de marcaciones** y que el archivo de nómina también lleva: `001` hora ordinaria diurna, `1670` calamidad, `VAC` vacaciones, `INCAP` incapacidad, `PERREM` y `PERNOREM` permisos. Esos los alimentan **eventualidades** y **trámites**, no marcaciones.

### 12.4 El modelo de turnos

Un turno **no es un horario**: es un conjunto de bloques por día de la semana.

```
T_NORMAL1   bloque 1   Lun          06:00 – 14:00
            bloque 2   Mar a Vie    06:00 – 13:00
            bloque 3   Sáb          06:00 – 12:00
```

Y para las semanas con festivo existe un turno **gemelo** que corre los horarios:

```
T_FESTIVO1  bloque 1   Mar a Sáb    06:00 – 14:00
```

El jefe no «arma una semana»: cambia a su gente de `T_NORMAL1` a `T_FESTIVO1`. Así es como se cumple el tope de la jornada semanal legal.

Cada turno declara además:

| Atributo | Para qué |
|---|---|
| Ventana válida de marcación, antes y después | Cuánto antes del turno se acepta una entrada. **Es por turno, no global** |
| Descanso | `0,333 h` = los 20 min de café de planta · `1,0 h` = la hora de almuerzo administrativa |
| Hora del descanso | Dónde cae dentro de la jornada |
| Horas hábiles y horas por día | Jornada fija acreditada |

**El café lo paga la empresa y no se descuenta. El almuerzo sí se descuenta, y solo aplica a administrativos.**

### 12.5 La programación de turnos: el reto de UX del proyecto

Entre 700 y 800 personas rotan turno. Se programa semanalmente, usualmente el jueves anterior. La rotación puede ir hacia adelante o hacia atrás según el área, y cualquier caso particular es posible: alguien repite turno para cubrir, alguien vuelve de incapacidad y entra a otro turno.

**Si la pantalla obliga a asignar persona por persona, el módulo fracasa.** Tiene que ofrecer:

- Selección masiva por área, por turno actual, por grupo o cuadrilla
- Rotación en bloque: «todos los de turno 1 pasan a turno 2»
- Aplicar el patrón de rotación del área con un clic
- Detección automática de festivos, con propuesta de la semana que corresponde —**que el jefe acepta, no que el sistema impone**, porque puede decidirse trabajar el festivo
- Cambios puntuales sobre la programación, con trazabilidad
- Vista de calendario mensual por persona y vista de matriz por área

### 12.6 Reglas de cálculo

| Regla | Contenido |
|---|---|
| **Jornada fija** | El día acredita las horas del turno aunque falten minutos. El faltante se registra aparte como *horas pendientes*, no se descuenta del pago |
| **Escalera de sobretiempo** | La primera media hora exige 25 min; cada media hora siguiente se acredita con 10 min de gracia. Medida siempre desde el fin del turno |
| **Segmentación por minuto** | Cada minuto se clasifica contra el calendario y la franja en que realmente ocurre |
| **Tipo de día por tramo** | Un turno nocturno que empieza en festivo deja de cobrar recargo festivo al cruzar la medianoche. Y al revés |
| **Exclusión mutua** | Un minuto genera un solo concepto. El recargo nocturno festivo ya lleva ambos porcentajes sumados |
| **Semana operativa** | Arranca el domingo a las 22:00, con la entrada del turno 3. No a medianoche del lunes |
| **Café pagado** | Los huecos entre marcaciones se clasifican por el rol del dispositivo donde abren y cierran |
| **Tránsito interior** | Quien pasa por un lector interior no salió de la planta. No genera deuda de horas |
| **Lactancia** | Derecho con tope diario por etapa. Se acredita como ordinario **sin recargo** |
| **Personal de dirección y confianza** | Excluido de jornada máxima. Conserva recargos, no genera extras ni pendientes |

### 12.7 Roles de dispositivo

| Rol | Significa | Efecto del hueco |
|---|---|---|
| `PORTERIA` | Salió de la empresa | Pesa completo como ausencia |
| `DESCANSO` | Vestier, cafetería, casino | Se perdona hasta el tope de café |
| `INTERIOR` | Tránsito entre áreas | No genera deuda |

Si cualquiera de los dos extremos de un hueco es portería, el hueco completo es ausencia. **Ante la duda se cobra al empleado, nunca a la empresa.**

Esto deja de vivir en el navegador de una persona y pasa a ser **tabla maestra con auditoría**: junto con la escalera, es lo que más pesa sobre las horas reportadas.

### 12.8 Marcaciones y correcciones

- Tolerancia de llegada tarde parametrizable.
- Una marcación faltante se marca **«Sin marcación»** en naranja, visible y llamativa.
- El jefe puede **corregir** una marcación a solicitud del colaborador, con auditoría completa.
- El jefe debe poder ver **en vivo** quiénes ya están en turno y quiénes no han llegado.
- Número impar de marcaciones: el sistema propone una resolución descartando una marcación, nunca inventa una hora, y exige aprobación.

### 12.9 Horas extra: topes y aprobación

| Regla | Valor |
|---|---|
| Tope semanal | 12 horas — **alerta, no bloqueo** |
| Contador mensual | 48 horas — **alerta, no bloqueo** |
| Quién aprueba | Solo el jefe o el director del área |
| Cuándo | Después de trabajadas |
| Plazo | Un par de días después del cierre |

Por fuerza mayor alguien puede superar el tope. El sistema avisa y lo deja registrado.

### 12.10 Período y cierre

- El ciclo va del **11 de un mes al 10 del siguiente**.
- Las fechas de cierre son **parametrizables**.
- Al cerrar, las horas se congelan en una foto inmutable.
- Una reapertura exige rol elevado y genera un cálculo nuevo con identificador propio.
- Una corrección posterior se ajusta y se vuelve a emitir el archivo.
- **El cierre se bloquea** si hay empleados con conceptos y sin código de nómina, o si quedan excepciones bloqueantes sin resolver.

### 12.11 El archivo plano de SINERGY

Formato confirmado contra un archivo real de producción:

```
codSinergy ⇥ concepto ⇥ + ⇥ fechaInicio ⇥ horas ⇥ fechaFin ⇥ ⇥ ⇥ ⇥ ⇥ ⇥
```

| Aspecto | Regla |
|---|---|
| Campos | 12, separados por tabulación |
| Encabezado | No lleva |
| Codificación | UTF-8, saltos `\n`, **sin salto al final** |
| Fecha | `D/MM/AAAA` — día sin cero, mes con cero |
| Signo | `+` fijo |
| Horas | 2 decimales máximo, **sin ceros de relleno**: `45`, `57.5`, nunca `45.00` |
| Agregación | Una línea por empleado y concepto, con el total del período |
| Campos 7 a 12 | Vacíos pero presentes |
| Nombre | `FINAL_SINER_<inicio>_<fin>.txt` |
| Cero | Un concepto en cero no emite línea |

### 12.12 La brecha que justifica el proyecto

Un dato del archivo real de septiembre de 2026, que vale la pena verificar y luego poner en pesos:

| Concepto | Archivo enviado a nómina | Lo que calcula el motor validado |
|---|---|---|
| Horas extra del período | **31 horas** | del orden de **9.700 horas** |

El archivo que hoy se sube a nómina no lo produce el motor corregido: lo produce BioTime, cuyo redondeo plano sobre el total del día se come prácticamente todo el sobretiempo. **El motor que corrige el cálculo existe y está validado, pero el archivo que se sube no lo usa.**

Cerrar esa brecha —una sola ruta al archivo de nómina— es el argumento para gerencia más fuerte de todo el proyecto.

---

## 13. Eventualidades

**Dueño de:** todo lo que le pasa a una persona en una fecha.

Diez módulos del sistema viejo se consolidan en uno solo, parametrizado por tipo. Diez módulos casi idénticos serían un olor a diseño; un módulo con su catálogo de tipos es el módulo funcional real.

### 13.1 Tipos

| Tipo | Particularidades |
|---|---|
| Accidente de trabajo | Investigación, causas, plan de acción, responsable, seguimiento post-evento, cierre |
| Enfermedad profesional | Seguimiento |
| Incapacidad | Días, origen. **Sin seguimiento de recobro ante EPS/ARL por ahora** |
| Ausencia | Con causal |
| Descargo | **Acceso restringido**: solo jefe y RH |
| Retiro | Dispara paz y salvo y revocación de accesos |
| Examen médico | De ingreso y periódico |

### 13.2 Reglas

- **Ausentismo es el mismo hecho visto dos veces.** El biométrico ve que no marcó; la eventualidad explica por qué. La marcación es el hecho, la novedad es la causa, y el indicador de ausentismo nace de cruzar ambas. Si cada módulo lleva su propio conteo, los indicadores nunca cuadran.
- **Los exámenes periódicos son anuales**, parametrizables por cargo. El sistema alerta cuando alguien pasa de un año sin registro.
- **Del examen se guarda fecha y concepto** (apto / apto con restricciones / no apto), y **se incorpora adjuntar el documento de evidencia**.
- Las eventualidades alimentan conceptos del archivo de nómina: incapacidad, calamidad, permisos.
- Todas las eventualidades de una persona forman su **hoja de vida**.

---

## 14. Trámites

**Dueño de:** las solicitudes con radicado y estado.

### 14.1 Tipos de solicitud

Vacaciones · Permiso · Certificado laboral · PQR

Con los motivos de permiso ya catalogados: ARL, calamidad doméstica, diligencia personal, examen periódico, licencia no remunerada, licencia de paternidad, licencia por luto, llegada tarde, permiso EPS, permiso sindical, sanción, tiempo por votación.

### 14.2 Flujo de vacaciones y permisos

```
Colaborador radica y firma
        ↓  notificación
Jefe revisa, aprueba y firma
        ↓  notificación
RH firma, registra en SINERGY a mano, y notifica la aprobación en SIRH+
```

RH no debería devolver una solicitud que el jefe ya aprobó, salvo error del sistema. Por eso el saldo tiene que validarse **antes** de radicar.

### 14.3 Vacaciones

| Regla | Contenido |
|---|---|
| Causación | 15 días hábiles por año cumplido. **Solo personal directo** |
| Primer período | Se habilita al cumplir un año |
| Días hábiles | Excluyen sábados, domingos y festivos |
| Mínimo del primer período | 6 días |
| Mínimo posterior | 3 días |
| Acumulación | Política: 2 períodos. Hay excepciones de hecho en jefaturas → **alerta, no bloqueo** |
| Temporales y aprendices | No causan |
| Saldo | **Pozo único**: «2 períodos — 30 días». No se lleva contabilidad por período |
| Bloqueo | No se puede solicitar más de lo disponible. La alternativa es permiso o licencia no remunerada |
| Solicitud | En rango de fechas, con cálculo automático de días hábiles |

Mientras no haya conexión con SINERGY, el saldo lo calcula SIRH+ desde la fecha de contrato menos los días aprobados.

### 14.4 Certificado laboral

Se genera al instante, con o sin salario. Mientras no haya conexión con SINERGY, RH registra el salario. Lleva fecha de corte visible y código verificable.

### 14.5 PQR

Llegan a su módulo. RH decide si las escala a otro comité, como el COPASST.

---

## 15. Formación

**Dueño de:** inducción, cursos, divulgaciones y la matriz de capacitación.

Este módulo absorbe COPEC.

### 15.1 Inducción

- **Es la misma para todo el personal.**
- Hoy se dicta presencialmente en un salón, durante dos o tres días, antes de entrar a planta.
- El objetivo es poder enviarla por enlace para que se haga desde casa antes del primer día. **Eso exige la cuenta de pre-ingreso**: alguien que todavía no es empleado y ya debe entrar.
- Al completarla, la persona pasa a recibir las divulgaciones de los documentos de su área.
- Deja constancia verificable con consecutivo, horas y código, por exigencia del SG-SST.

### 15.2 Divulgación de documentos

El proceso que hoy hace COPEC:

1. Daruma publica una versión nueva de un documento de calidad.
2. El sistema compara su versión contra la de Daruma. Si la suya es inferior, marca que hay que divulgar.
3. Se notifica a todo el personal cuya matriz de cargo incluye ese documento.
4. Cada persona abre el documento, lo lee y **firma** confirmando que está enterada del cambio.

Daruma **no expone API**: el enlace se registra a mano y la detección de versión se hace leyendo su base de datos directamente.

### 15.3 Matriz de capacitación por cargo

- El jefe define, por cargo, qué documentos aplican.
- En la primera divulgación, la persona debe revisar todos los documentos de su matriz.
- **Si cambia de cargo**, hereda la matriz nueva y debe divulgarse. La matriz anterior queda como historial en su hoja de vida: en algún momento leyó y aplicó esos documentos.
- No hay plazo límite hoy, pero toda versión nueva debe divulgarse a quien le aplique.

### 15.4 Cursos

Un constructor de evaluaciones equivalente a un formulario en modo examen: se crea la pregunta, se ponen las respuestas y se marca cuál vale.

Hoy no hay nota mínima; **incorporarla es una mejora prevista**, junto con el número de reintentos.

### 15.5 R-RH-009 · Registro de capacitación

Toda capacitación —virtual, presencial, interna o dictada por un externo— genera este registro.

**Cómo funciona hoy:** el instructor entra a un módulo público con cédula y código interno, crea el formato con los datos de cabecera (nombre, duración, motivo, observaciones), agrega a los asistentes y pasa la tableta para que cada uno firme. RH revisa, asigna folio y cierra.

**Qué mejora:** la autenticación pasa a contraseña propia, el instructor externo puede registrarse sin ser empleado, y el registro entra al motor de registros firmados del §8.2.

Puede ser grupal o individual. El folio es un consecutivo que no se reinicia. Solo RH —analistas, asistentes o auxiliares— puede cerrar.

---

## 16. Competencias

**Dueño de:** la evaluación de desempeño y su histórico.

### 16.1 El formato R-RH-053

RH crea un formato por cargo. Cada formato tiene grupos con un peso porcentual que suma 100 %:

| Grupo | Peso de ejemplo |
|---|---|
| Genéricas | 15 % |
| Técnicas | 20 % |
| Humanas | 10 % |
| Educación | 15 % |
| Formación | 5 % |
| Experiencia | 20 % |
| SG-SST | 15 % |

Dentro de cada grupo hay conductas, cada una con su definición y su calificación de 1 a 5, más una observación.

**La nota final** se obtiene ponderando la calificación de cada grupo por su peso. **La mínima para aprobar es 80 %, parametrizable.**

Los grupos son fijos hoy, pero el sistema debe permitir crear grupos nuevos.

### 16.2 Reglas

- El formato se asigna **a un cargo**, no a una persona.
- **Evalúa el jefe inmediato**, al menos una vez al año.
- Por política interna, la calificación se hace **junto con la persona**. Hoy no firma ninguno de los dos: queda el registro de auditoría del usuario del jefe. Que ambos firmen es una mejora a evaluar.
- Si se pierde la evaluación, se rehace a los 3 meses.
- Deja observaciones, no plan de acción formal.
- **Alerta a los 10 meses** sin evaluación; vencida a los 12.
- Si el formato se modifica, las evaluaciones históricas conservan la versión con la que se hicieron, junto con su resultado.
- Que el colaborador vea su propia calificación en el portal **está por definir con RH**.

---

## 17. Dotación y EPP

**Dueño de:** la entrega de dotación y elementos de protección personal.

- **No hay control de inventario.** Solo registro de entrega.
- El catálogo de elementos se consulta de la base SQL Server de MANT.
- La empresa hace **tres jornadas de entrega al año**.
- La entrega **requiere firma** del colaborador.
- Las entregas pendientes de devolución entran al paz y salvo de retiro.

Es un módulo propio, no un tipo de eventualidad: tiene catálogo, tallas, ciclos de reposición y firma. La entrega sí genera un registro en la hoja de vida.

---

## 18. Encuestas

**Dueño de:** la creación, publicación y análisis de encuestas internas.

| Aspecto | Decisión |
|---|---|
| Quién las crea | Solo RH |
| Tipos de pregunta | Opción múltiple, escala, texto libre corto |
| Segmentación | Toda la empresa, o por cargos seleccionados |
| Entrega | Al autenticarse, el colaborador ve sus formularios pendientes |
| Fecha de cierre | Opcional, la define quien la crea |
| Análisis | Gráficas, promedios y exportación a Excel |

### 18.1 Anonimato

El anonimato es una opción que RH marca al crear la encuesta.

**El mecanismo correcto no es el caché del navegador** —se borra y se responde otra vez—. Es guardar **en una tabla separada** que la persona X ya respondió, sin ningún vínculo con el contenido de su respuesta.

Con ese diseño:

- En una encuesta anónima, RH ve **cuántos** faltan, nunca **quiénes**.
- En una encuesta no anónima, RH ve quiénes faltan.

---

## 19. Reservas de salas

**Dueño de:** la reserva de espacios.

Es el módulo más pequeño y más independiente del sistema, y por eso un buen candidato a piloto.

- Hay 2 salas de capacitación, pero el modelo permite crear más recursos.
- Cualquiera puede reservar, sin aprobación.
- Se ve un calendario, se elige la sala y el tiempo, **con un máximo de 6 horas**.

---

## 20. Indicadores e informes

**No es un módulo: es una capa de lectura.**

Construirlo como aplicación propia lleva a tablas de resumen que se desincronizan de la realidad. El cálculo va en `dominio/indicadores.py` con sus pruebas; la presentación va en `reportes/`.

**Se construye al final**, cuando los módulos que lo alimentan ya existen.

### 20.1 Indicadores principales

| Indicador | Se alimenta de |
|---|---|
| Rotación de personal | Personal + eventualidades de retiro |
| Índice de ausentismo | Marcaciones × eventualidades |
| Índice de incapacidades | Eventualidades |

Cada uno se despliega en detalle: por área, por cargo, por motivo, por período.

### 20.2 Reglas

- Consultables bajo **rango de fechas libre**, no en períodos fijos.
- Los informes del sistema viejo no hay que replicarlos exactamente: como los datos se migran, se presentan en el formato nuevo.
- Lo que sí hay que hacer es **conciliar**: los indicadores del sistema nuevo deben dar lo mismo que los del viejo sobre los mismos períodos. Esa es la prueba de aceptación real de la migración.

---

# PARTE IV · CÓMO SE CONSTRUYE

---

## 21. Seguridad

| Frente | Decisión |
|---|---|
| Autenticación | IAM centralizado. Adaptador local transitorio **detrás de una interfaz**, reemplazable por configuración |
| Credenciales viejas | **Las contraseñas MD5 del SIRH no se migran.** Se crean identidades nuevas con cambio forzado al primer ingreso |
| Autorización | Roles de alto nivel del IAM, traducidos a permisos internos en `cuentas/roles.py`. **Verificada en cada ruta, no solo en el menú** |
| Consultas | ORM de Django o SQL parametrizado. Nunca concatenación |
| Entradas | Validación en servidor **siempre**. La del navegador es cortesía |
| Sesiones | Expiración, renovación, cierre explícito |
| Secretos | En `.env`, nunca en el repositorio |
| Transporte | HTTPS obligatorio |
| Datos sensibles | Acceso por permiso explícito: salarios, descargos, salud ocupacional |
| Auditoría | Registro inmutable de accesos y cambios sensibles |
| Errores | Detalle técnico al log; mensaje entendible al usuario. Nunca un traceback en pantalla |
| Habeas data | Ley 1581: 5 años en línea, consentimiento, derecho de corrección vía solicitud de actualización |

### 21.1 Alcance de red

El sistema sale **solo a la red interna** en su primera etapa. Debe poderse entrar desde cualquier computador de la planta, sin restricción por equipo.

Salir a internet se contempla más adelante, y es lo que haría posible la inducción desde casa. **No sale a producción pública sin el IAM funcionando.**

---

## 22. Experiencia de usuario

El diseño no es un acabado: es lo que vende el sistema y lo que decide si la gente lo usa. Se trata como requisito.

### 22.1 Principios

| Principio | Qué significa en la práctica |
|---|---|
| **El sistema ayuda** | Cada módulo tiene un icono de ayuda que abre una ventana con cómo funciona y qué tener en cuenta |
| **Todo formulario validado** | En servidor, con mensajes claros y específicos |
| **Formularios en ventana modal** | Patrón consistente en todo el sistema |
| **Los cuatro estados** | Cada pantalla resuelve: con datos, vacío, error y cargando |
| **Coherencia** | Mismos patrones, mismos nombres, mismos lugares en todos los módulos |
| **Accesibilidad** | Contraste, navegación por teclado, etiquetas |
| **Responsive** | Funciona en computador de planta y en pantallas pequeñas |
| **Alertas adecuadas** | Ni ruido ni silencio. Lo urgente se ve; lo informativo no interrumpe |

### 22.2 Más allá del CRUD

El alcance explícito del proyecto es no construir «formularios de guardar». Según el caso, la interfaz debe usar: asistentes por etapas, vistas de detalle, acciones contextuales, historiales, paneles, filtros avanzados, bandejas, calendarios y matrices.

### 22.3 Sistema de diseño

Design tokens en `:root`, componentes reutilizables en plantillas, y un documento `13-sistema-de-diseno.md` que define la tipografía, el color, el espaciado y los patrones de pantalla.

El portal público no se ve como una herramienta interna de RH. Es la cara de la empresa hacia 1.100 personas que no tienen ninguna gana de entrar a un sistema.

---

## 23. Calidad

### 23.1 Las seis compuertas

Un módulo está terminado cuando las seis pasan. Ninguna es opcional.

| # | Compuerta | Cómo se verifica |
|---|---|---|
| 1 | Pruebas del núcleo en verde | `python -m unittest discover -s tests` |
| 2 | Chequeo de salud en verde | `python manage.py smoke_test` y la ruta `/salud/` |
| 3 | Revisión de seguridad | `python manage.py check --deploy` sin hallazgos |
| 4 | Revisión visual contra el diseño | Cada pantalla comparada con su referencia |
| 5 | Los cuatro estados resueltos | En cada pantalla |
| 6 | Validación humana | Contra un caso real. Nadie más puede dar esta |

### 23.2 Orden de construcción dentro de un módulo

Siempre de adentro hacia afuera:

1. Migración del modelo de datos
2. `dominio/` — funciones puras
3. `tests/` — pruebas de esas funciones, con casos límite
4. `consultas.py` — acceso a datos, parametrizado
5. `presentacion.py` — arma lo que la plantilla necesita
6. `views.py` — delgada: recibe, delega, responde
7. Plantillas — con los cuatro estados
8. Verificación — las seis compuertas

### 23.3 Qué no hacer

- No construir «de una vez» algo de un módulo posterior porque «ya que estamos».
- No agregar campos al modelo «por si acaso».
- No crear una abstracción para un caso que todavía no existe.
- Si aparece una idea buena que no es de este módulo, va a `docs/pendientes.md`, no al código.

### 23.4 Documentación

| Documento | Para quién | Cuándo |
|---|---|---|
| Ayuda contextual en la app | Usuario final | Con cada módulo |
| Manual de usuario en PDF | RH y jefes | Al cerrar cada módulo |
| Manual técnico | Quien mantenga el sistema | Continuo |
| `docs/trazabilidad.md` | El proyecto | En cada decisión |
| `docs/pendientes.md` | El proyecto | Continuo. Lo primero que se lee al retomar |
| `CLAUDE.md` | Los agentes | Al cerrar cada módulo |
| Registro de errores | QA | El QA prueba y envía informe por correo |

---

## 24. Orden de construcción

**El principio:** cada módulo se entrega funcional de punta a punta —backend, frontend, pruebas— y se prueba contra casos reales antes de pasar al siguiente. Nada de diez módulos a medias.

| Orden | Módulo | Por qué va aquí |
|---|---|---|
| **0** | Cimientos | Git, esqueleto Django, despliegue, chequeos de salud, design tokens |
| **1** | **Personal + Empresa + Firmas** | Todo lo demás se para encima. Sin personas con código, sin cargos y sin firmas no hay nada |
| **2** | Parámetros, auditoría, notificaciones | Los transversales que el resto necesita |
| **3** | **Marcaciones** | El más grande y el de mayor valor demostrable |
| **4** | Nómina y archivo plano | Cierra el caso de negocio |
| **5** | Eventualidades | Alimenta indicadores y nómina |
| **6** | Trámites + vista de colaborador | La autoconsulta que RH pidió |
| **7** | Formación | Absorbe COPEC |
| **8** | Competencias | |
| **9** | Dotación, encuestas, reservas | Los más pequeños |
| **10** | Indicadores e informes | Al final, cuando hay con qué alimentarlos |

### 24.1 Migración

**Cada módulo migra lo suyo al terminarse**, no todo al final. El esquema actual es sencillo y los datos se adaptan bien al modelo nuevo.

Pasos para cada módulo:

1. Extraer el DDL y los procedimientos relevantes
2. Documentar las reglas de negocio embebidas — **este es el entregable más valioso del análisis**
3. Mapear modelo viejo → modelo nuevo, tabla por tabla
4. Escribir las migraciones como **código repetible**, no scripts de una sola vez
5. **Conciliar**: los reportes del sistema nuevo deben dar exactamente lo mismo que los del viejo sobre los mismos períodos

### 24.2 Paralelo

La norma interna exige **3 meses de pruebas** antes de oficializar. Durante ese período se digita en los dos sistemas. **No se construye ninguna conexión al sistema viejo más allá de la migración de datos.**

Los datos capturados durante las pruebas probablemente se borran al oficializar.

---

## 25. Decisiones abiertas

| # | Pendiente | Impacto | Quién decide |
|---|---|---|---|
| 1 | Código y porcentaje vigente del recargo dominical | Alto — afecta lo que se paga | Nómina |
| 2 | ¿El colaborador ve su calificación de competencias? | Medio | RH |
| 3 | ¿El evaluado firma el R-RH-053? | Medio | RH |
| 4 | Tratamiento de Granservicios en el archivo de nómina: ¿un archivo o dos? | Alto | RH + Granservicios |
| 5 | Quién mantiene el maestro de códigos de nómina y por qué cubre menos de la mitad | Alto | RH |
| 6 | Dueño definitivo de contrato y salario cuando SINERGY exponga API | Medio | RH + Nómina |
| 7 | Nota mínima y reintentos en cursos | Bajo | RH |
| 8 | Plazo límite para divulgaciones | Bajo | RH |
| 9 | Fecha del IAM y cierre del contrato de integración | Alto | TI |
| 10 | Máquina de producción | Medio | TI |

---

## 26. Vocabulario

Términos fijos. Se usan en la interfaz **y en el código**.

| Término | Significado | Nombre en código |
|---|---|---|
| **Colaborador** | El empleado como usuario del sistema | — |
| **Eventualidad** | Lo que le pasa a una persona en una fecha | `Eventualidad`, app `eventualidades/` |
| **Trámite** | Solicitud con radicado y estado | `Tramite`, app `tramites/` |
| **Divulgación** | Publicación de un documento que debe leerse y firmarse | `Divulgacion` |
| **Constancia** | Evidencia de lectura de un documento | `ConstanciaLectura` |
| **Curso** | Secciones más evaluación, deja certificado | `Curso`, `Seccion` |
| **Certificado** | Resultado de aprobar un curso | `Certificado` |
| **Registro** | Formato de RH con folio y firmas | `Registro` |
| **Folio** | Consecutivo que no se reinicia | `folio` |
| **Marcación** | Un golpe en un biométrico | `Marcacion` |
| **Jornada** | Un día calculado de una persona | `Jornada` |
| **Turno** | Catálogo con bloques por día de semana | `Turno`, `BloqueTurno` |
| **Programación** | Asignación de turno a persona y fecha | `Programacion` |
| **Período** | Ciclo de nómina, del 11 al 10 | `Periodo` |
| **Horas pendientes** | Tiempo de turno no cumplido. **No se descuenta del pago** | `pendiente_min` |
| **Vacante** | Cargo sin asignación vigente | — |
| **IAM / Maestro** | El aplicativo central de identidad | — |

No se usa «evento», «seguimiento» ni «empleado» en la interfaz.

---

## 27. Mapa de documentos

| Documento | Para qué | Vigencia |
|---|---|---|
| `claude/00-contexto-maestro-sirh-plus.md` | **Este archivo.** El mapa completo | Vigente |
| `claude/01-diagnostico-sistema-actual.md` | Qué hay hoy y por qué no se refactoriza | Vigente |
| `claude/02-propuesta-stack-y-arquitectura.md` | Diseño general | ⚠️ Stack y frontend obsoletos, corregidos por el 05 |
| `claude/03-arquitectura-de-identidad-centralizada.md` | Cómo se separa identidad de permisos | Vigente |
| `claude/04-contrato-integracion-app-maestra.md` | Para entregar al desarrollador del IAM | Vigente, falta acordarlo |
| `claude/05-alineacion-con-el-estandar-plastitec.md` | La corrección del stack, razonada | Vigente |
| `claude/06-propuesta-portal-colaborador.md` | Propuesta funcional del Portal | ⚠️ El Portal ya no es app aparte — ver §6.6 |
| `claude/07-plan-de-ejecucion-portal.md` | 14 fases del Portal | ⚠️ A reescribir dentro del plan general |
| `claude/08-modulo-marcaciones.md` | **Por escribir.** El módulo en detalle | — |
| `claude/09-modelo-de-datos.md` | **Por escribir.** Esquema completo | — |
| `claude/10-plan-de-ejecucion-sirh-plus.md` | **Por escribir.** Fases y compuertas | — |
| `claude/11-plan-de-migracion.md` | **Por escribir.** Mapeo y conciliación | — |
| `claude/12-sistema-de-diseno.md` | **Por escribir.** Tokens, componentes, patrones | — |

### 27.1 Insumos pendientes

| # | Qué | Para qué | Bloquea |
|---|---|---|---|
| 1 | `reporte-horas.html` (versión auditoría) | Excepciones y Glosario | Módulo de marcaciones |
| 2 | `CLAUDE.md` de MOD_BIO | El razonamiento de cada decisión | Módulo de marcaciones |
| 3 | `scripts/pruebas_motor/` | Se traducen a `unittest` | Módulo de marcaciones |
| 4 | Dump del esquema MySQL del SIRH | Modelo de datos | **Todo lo demás** |
| 5 | Cuerpo de los 207 procedimientos | Reglas de negocio reales | **Todo lo demás** |
| 6 | Lista de áreas y cargos con jerarquía | Organigrama | Módulo 1 |
| 7 | Plantilla del estándar de Plastitec | Define cómo se escribe el código | Fase 0 |
| 8 | Código de COPEC | El módulo que se absorbe | Formación |
| 9 | Formatos R-RH-009, R-RH-053, paz y salvo, certificado | Motor de registros | Transversales |
| 10 | API de los biométricos | Conexión LAN | Marcaciones |
| 11 | Acceso de lectura a Daruma | Divulgaciones | Formación |
| 12 | Esquema de la base de dotación | Catálogo | Dotación |

---

## 28. Lo que se aprendió en el camino

Errores reales de este proyecto. Están aquí porque evitan repetirlos.

1. **Se recomendó un stack antes de conocer el estándar de la empresa.** La recomendación era defendible en abstracto y equivocada en contexto. Antes de decidir tecnología, preguntar qué corre ya en la organización y con qué se mantiene.

2. **Se escribió un plan de ejecución antes de definir qué hacía el aplicativo.** Hubo que parar y producir primero el alcance funcional. El orden es **alcance → diseño → plan**, nunca al revés.

3. **El primer mockup era un panel administrativo genérico.** Se rehízo con identidad propia. Un portal para 1.100 personas que no quieren entrar a un sistema no se ve como una herramienta interna de RH.

4. **Se dio por hablada una decisión que nunca se tomó.** Conviene revisar el historial antes de afirmar que algo ya se acordó.

5. **La documentación que contradice al código desinforma a quien la lee después.** Por eso los documentos obsoletos llevan cabecera de advertencia en vez de borrarse o corregirse en silencio.

6. **El Portal se diseñó como aplicación aparte y no lo es.** Habría duplicado la regla de negocio de cinco módulos. Se corrigió antes de escribir código, que es el único momento barato para corregirlo.

7. **La cifra de personal estaba mal por un factor de dos.** Se dimensionó medio proyecto sobre 500 personas cuando son 1.100. Verificar las cifras que fundamentan decisiones de diseño, aunque vengan de un documento propio.

8. **Existían tres herramientas haciendo lo mismo de maneras distintas**, y nadie lo había notado junto. Antes de construir, inventariar qué hay funcionando en las orillas del sistema.

---

## 29. Qué sigue

En este orden. Los primeros no dependen de TI y pueden arrancar ya.

1. **Preguntar a nómina** cuál es el código y el porcentaje vigente del recargo dominical.
2. **Averiguar quién mantiene el maestro de códigos de nómina** y por qué cubre menos de la mitad del personal.
3. **Conseguir el esquema MySQL y los 207 procedimientos.** Es el cuello de botella de todo lo que no sea marcaciones.
4. **Poner bajo control de versiones** el código del SIRH viejo, el de COPEC y la plantilla del estándar.
5. **Correr el motor validado sobre septiembre** y comparar su archivo contra el que se envió. Si la brecha se confirma, hay caso de negocio medido en pesos.
6. **Escribir `08-modulo-marcaciones.md`** y empezar por los cimientos.
