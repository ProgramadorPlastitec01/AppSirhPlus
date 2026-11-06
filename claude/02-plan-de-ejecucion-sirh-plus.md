# SIRH+ — Plan de ejecución

**Plastitec S.A.S. · Tecnología de Información**
Versión 1.0 · 5 de noviembre de 2026
**Documento normativo del proyecto. Se lee completo antes de escribir la primera línea de código.**

---

# 0 · Cómo se usa este documento

## 0.1 Qué es y qué no es

Este documento es **el contrato de ejecución**. Dice qué se construye, en qué orden, con qué reglas y cómo se verifica.

| Dónde vive qué | Documento |
|---|---|
| El contexto del proyecto y las decisiones | `claude/00-contexto-maestro-sirh-plus.md` |
| Todos los módulos y todas sus opciones | `claude/01-inventario-y-fases-sirh-plus.md` |
| **Cómo se ejecuta** | **Este documento** |
| El diseño visual y de interacción | `.claude/rules/03-sistema-de-diseno.md` |
| El detalle del módulo de marcaciones | **Por escribir.** El documento del módulo de marcaciones se escribe antes de la fase 6 |

**Los artboards son ids dentro de un solo archivo.** Las pantallas de la cara de gestión viven como secciones con id —`v-permisos`, `v-cargos`, `v-hoja`…— dentro de `mockups/mockup-sirh-plus-completo.html`. No son archivos sueltos. La correspondencia completa de pantalla a id está en `docs/diseno.md` §5. La cara de colaborador sí está en archivos, en `mockups/mockup-portal/`.

Si este documento contradice al código, gana el código y hay que corregir este documento. Si contradice al estándar de Plastitec, gana el estándar, salvo donde aquí se declare una desviación.

## 0.2 La regla que gobierna todo

> **No se avanza a la fase siguiente hasta que la fase actual esté construida, probada, verificada y validada por una persona.**

Existe por una razón concreta: un proyecto que construye diez módulos en paralelo termina con diez módulos a medias que nadie puede probar. Uno que construye uno, lo pone a funcionar y luego sigue, tiene valor desde la primera semana.

## 0.3 Las seis compuertas

Una fase está terminada cuando las seis pasan. **Ninguna es opcional.**

| # | Compuerta | Cómo se verifica |
|---|---|---|
| 1 | **Formato y lint en verde** | `ruff format .` y `ruff check .` sin hallazgos |
| 2 | **Pruebas del núcleo en verde** | `python -m unittest discover -s tests` sin fallos |
| 3 | **Chequeo de salud en verde** | `python manage.py smoke_test` y la ruta `/salud/` |
| 4 | **Revisión de seguridad** | `python manage.py check --deploy` sin hallazgos, más la revisión del agente de seguridad. Qué avisos se aceptan en local y cuáles no: ver «Postura sobre HTTPS y `check --deploy`» en `CLAUDE.md` |
| 5 | **Revisión visual y los cuatro estados** | Cada pantalla contra su artboard, con datos, vacía, con error y cargando |
| 6 | **Validación humana** | Sebastián usa la fase contra un caso real; después el QA la revisa y envía su informe. **Nadie más puede dar esta compuerta** |

Si una compuerta falla, la fase **no** está terminada. No se empieza la siguiente.

## 0.4 Qué no hacer

- **No construir algo de una fase posterior** porque «ya que estamos».
- **No agregar campos al modelo** «por si acaso».
- **No crear una abstracción** para un caso que todavía no existe.
- **No tocar código de una fase ya cerrada** salvo para corregir un defecto, y entonces se anota en `docs/trazabilidad.md`.
- Si aparece una idea buena que no es de esta fase, va a `docs/pendientes.md`, **no al código**.

## 0.5 Orden de construcción dentro de una fase

Siempre de adentro hacia afuera. Nunca al revés.

```
1. Migración del modelo de datos
2. dominio/            funciones puras, sin Django ni entrada/salida
3. tests/              pruebas de esas funciones, con casos límite
4. consultas.py        acceso a datos, parametrizado
5. presentacion.py     arma lo que la plantilla necesita
6. views.py            delgada: recibe, delega, responde
7. templates/          con los cuatro estados resueltos
8. Verificación        las seis compuertas
```

**Regla verificable:** una función de `views.py` no debería pasar de 30 líneas. Si crece, la lógica pertenece a una capa de abajo.

## 0.6 Cómo se trabaja con Claude Code

| Regla | Por qué |
|---|---|
| **Una fase por sesión larga, un entregable por tanda** | El contexto se degrada; es mejor cerrar piezas pequeñas |
| **Leer `docs/pendientes.md` al empezar cada sesión** | Es lo primero que dice dónde quedó todo |
| **Un commit por entregable, con mensaje que diga el porqué** | Sin diff no hay revisión |
| **Nunca `--no-verify`** | Las compuertas existen para fallar |
| **Al cerrar una fase, actualizar `CLAUDE.md` y `trazabilidad.md`** | Si no, la próxima sesión arranca a ciegas |
| **Ante una duda de negocio, preguntar. No inventar** | Un supuesto no verificado es deuda que estalla en producción |

---

# 1 · No negociables

Estos aplican a todas las fases, desde la primera línea.

## 1.1 Stack

| Capa | Tecnología |
|---|---|
| Lenguaje | Python 3.11+ |
| Framework | Django 5.2 LTS, renderizado en servidor |
| Base propia | PostgreSQL 17 vía `psycopg[binary]` |
| Sistemas ajenos | Solo lectura, en capa aislada, **nunca** en `DATABASES` |
| Plantillas | Django Template Language |
| Frontend | CSS plano y JavaScript vanilla |
| Exportación | `openpyxl` y `reportlab` |
| Pruebas | `unittest` de la biblioteca estándar |
| Formato y lint | `ruff` |
| Configuración | `django-environ` leyendo `.env` |
| Servidor | Gunicorn tras Nginx, bajo systemd, Rocky Linux 9 |

**Prohibido sin excepción:** build de frontend, librerías JavaScript de terceros, recursos desde CDN, escribir en la base de un sistema ajeno, duplicar una regla de negocio en JavaScript.

## 1.2 Las cuatro desviaciones declaradas del estándar

Se declaran aquí, con su justificación, porque el estándar exige que toda desviación se escriba.

### D1 · El shell no es el del estándar

**El estándar fija** un sidebar fijo de 220 px a la izquierda para toda pantalla con sesión.

**SIRH+ usa:** sidebar de 244 px para la cara de gestión, y **cabecera superior** para la cara pública y la de colaborador.

**Por qué:** el estándar está escrito para herramientas internas de consulta, que usan decenas de personas. La cara de colaborador la usan 1.100 personas que no quieren entrar a un sistema. Son dos audiencias con necesidades distintas. El detalle está en `.claude/rules/03-sistema-de-diseno.md`.

### D2 · Los permisos no son dos roles

**El estándar fija** dos roles, `consulta` y `administra`, iguales en todas las aplicaciones, y dice que un tercero es una desviación.

**SIRH+ usa:** un catálogo granular de permisos por módulo y acción, agrupados en roles que define TI, con el alcance del dato como eje aparte.

**Por qué:** SIRH+ maneja salarios, procesos disciplinarios y datos de salud ocupacional. Dos roles no pueden expresar que un analista vea el salario pero no lo edite, ni que un jefe vea solo su rama del organigrama.

**Cómo se respeta el estándar:** la frontera se mantiene. El gestor de identidad resuelve el acceso a la aplicación —quién entra y con qué rol de alto nivel—; SIRH+ resuelve la autorización dentro de la aplicación, en un módulo `permisos/` propio. El rol que entrega el gestor se traduce a permisos internos en `permisos/roles.py`.

### D3 · Más de dos niveles de alcance

**SIRH+ añade** el alcance del dato: propio, área, rama del organigrama, toda la empresa.

**Por qué:** dos usuarios con el mismo permiso `personal.ver` deben ver conjuntos de personas distintos. Eso no es un permiso: es una dimensión aparte, y mezclarla con el permiso multiplicaría el catálogo por cuatro.

### D4 · La identidad llega después, no en la fase 1

**El estándar exige**, en la fase 1 de su checklist: la conexión `identidad` con su router, la aplicación registrada en la tabla `aplicacion`, un usuario de MySQL propio, los dos chequeos de salud de identidad, y login y cambio de contraseña funcionando de verdad.

**SIRH+ construye** en su lugar: pantalla de ingreso **sin lógica de validación** —una puerta abierta durante el desarrollo—, catálogo de permisos completo pero con `PERMISOS_EXIGIR=false`, y los dos chequeos de salud de identidad declarados y desactivados, listos para encenderse.

**Lo que SIRH+ no construye, y conviene que quede escrito:** autenticación local, tabla de usuarios, contraseñas, ni «algo provisional» mientras tanto. Construirlo significaría desmontarlo después y, peor, tener dos sitios donde vive una credencial.

**Por qué:** el gestor de identidad está en construcción y SIRH+ va a ser su fuente de verdad de personas. Esperar a que exista detendría el proyecto; construir sin pensar en él obligaría a rehacerlo.

**Cómo se respeta el estándar:** no se toca el paquete `cuentas/` del estándar porque **SIRH+ no lo usa**. SIRH+ no gestiona usuarios: es la fuente de verdad de las personas del gestor, no un consumidor más de su tabla. La autenticación se escribe en un módulo propio, `identidad/`, el día que el gestor exista. Ver «SIRH+ no gestiona usuarios» en `CLAUDE.md`.

**Cómo se mitiga el riesgo:** el catálogo de permisos existe desde la fase 1 y se corre con `PERMISOS_EXIGIR=true` **al menos una vez por fase**, revisando el registro de las verificaciones que habrían fallado. Esa es la salvaguarda contra repetir la autorización cosmética del sistema viejo.

**Cuándo se paga:** al conectar el gestor. SIRH+ no sale a producción sin él.

## 1.3 Reglas de arquitectura

```
config/  ──▶  módulos  ──▶  dominio/
                  │
                  └──────▶  <fuente>_db/
```

- `dominio/` no importa **nada** del proyecto. Es el piso.
- `dominio/` no sabe quién es el usuario. Si una regla depende del rol, el rol llega como parámetro.
- `views.py` no habla con la base: pasa por `consultas.py`.
- `templates/` no consulta nada: recibe lo que `presentacion.py` armó.
- **Ningún modelo de la base propia tiene llave foránea hacia el usuario.** Se guarda el identificador y el nombre como texto.

## 1.4 Reglas de seguridad

| Regla | Detalle |
|---|---|
| **Valores siempre como parámetro** | En el texto del SQL solo se interpolan identificadores de una lista blanca |
| **Validación en el servidor, siempre** | La del navegador es cortesía |
| **Toda operación que modifica estado va por POST con token** | Ningún cambio por enlace |
| **El detalle técnico va al registro de eventos** | Al usuario, un mensaje que entienda. Nunca un traceback en pantalla |
| **Secretos solo en `.env`** | Nunca en el código, nunca en la base, nunca «temporalmente» |
| **El permiso se verifica en el servidor** | Ocultar un enlace del menú es cortesía visual, no protección |
| **Todo dato sensible registra su consulta** | Salario, descargos, restricciones médicas, exámenes |

## 1.5 Vocabulario

Términos fijos. Se usan en la interfaz **y en el código**.

| Término | Significado | Nombre en código |
|---|---|---|
| Colaborador | El empleado como usuario del sistema | — |
| Eventualidad | Lo que le pasa a una persona en una fecha | `Eventualidad` |
| Trámite | Solicitud con radicado y estado | `Tramite` |
| Divulgación | Documento que debe leerse y firmarse | `Divulgacion` |
| Constancia | Evidencia de lectura | `ConstanciaLectura` |
| Curso | Secciones más evaluación | `Curso` |
| Certificado | Resultado de aprobar un curso | `Certificado` |
| Registro | Formato de RH con folio y firmas | `Registro` |
| Marcación | Un golpe en un biométrico | `Marcacion` |
| Jornada | Un día calculado de una persona | `Jornada` |
| Turno | Catálogo con bloques por día | `Turno`, `BloqueTurno` |
| Programación | Asignación de turno a persona y fecha | `Programacion` |
| Período | Ciclo de nómina, del 11 al 10 | `Periodo` |
| Horas pendientes | Tiempo de turno no cumplido, **no se descuenta** | `pendiente_min` |

**No se usa** «evento», «seguimiento» ni «empleado» en la interfaz.

---

# 2 · FASE 0 · Cimientos

> **Objetivo:** la aplicación arranca, se despliega y se ve como SIRH+. No hace nada útil todavía.

## 2.1 Entregables

### E0.1 · Repositorio

```
git init
```

Primer commit **antes** de la primera línea de código, con la plantilla del estándar copiada tal cual.

| Archivo | Contenido |
|---|---|
| `.gitignore` | `.env`, `*.env` salvo `.env.example`, `*.key`, entornos virtuales, `*.sqlite3`, datos locales |
| `.env.example` | Todas las variables, documentadas, con el comando para generar cada clave |
| `README.md` | Qué es la app y cómo se levanta en local |
| `CLAUDE.md` | Plantilla, se llena en E0.8 |
| `pyproject.toml` | Configuración de `ruff`, de la plantilla |
| `requirements.txt` | Con versión fija y comentario justificando cada línea |
| `.claude/rules/` | Los estándares, copiados |
| `.claude/agents/` | Los cinco agentes, copiados |

**Nota: ya hecho.** La regla de frontend del estándar fue reemplazada por `.claude/rules/03-sistema-de-diseno.md`. El shell del estándar no aplica a SIRH+ — ver D1.

### E0.2 · Esqueleto de Django

```
sirh_plus/
├── manage.py
├── config/           settings, urls, wsgi, asgi
├── core/             checks.py, vistas base, utilidades
├── dominio/          vacío por ahora, con su __init__.py
├── tests/            vacío por ahora
├── templates/
│   ├── base.html             cara de gestión
│   ├── base_portal.html      cara de colaborador
│   ├── base_publico.html     sin sesión
│   ├── base_auth.html        ingreso, hereda de base_publico.html
│   └── macros.html
├── static/
│   ├── css/styles.css
│   └── vendor/               tipografías auto-hospedadas
└── deploy/
```

**No hay paquete de identidad en el esqueleto.** SIRH+ no gestiona usuarios, así que no se copia el `cuentas/` del estándar ni se escribe nada en su lugar. El módulo `identidad/` nace el día que exista el gestor; hasta entonces la pantalla de ingreso no valida nada.

**El ingreso no tiene shell propio.** `base_auth.html` hereda de `base_publico.html`, con el contenido centrado y sin navegación: es la puerta de entrada de las tres caras, no una cuarta. Su referencia visual es `mockups/mockup-portal/Login.dc.html`.

### E0.3 · Base de datos

- PostgreSQL 17 local, con un usuario propio de permisos mínimos.
- `DATABASES` con `default` solamente. La conexión `identidad` se agrega en la fase 1.
- Primera migración de Django, sin modelos propios todavía.

### E0.4 · Sistema de diseño

| Qué | Dónde |
|---|---|
| Design tokens en `:root` | `static/css/styles.css` |
| Las cuatro plantillas base | `templates/` — `base.html`, `base_portal.html`, `base_publico.html` y `base_auth.html`, que hereda de `base_publico.html` |
| Librería de componentes | `templates/macros.html` |
| Tipografías Archivo e Inter | `static/vendor/`, **auto-hospedadas** |
| Juego de iconos, uno solo, SVG en línea | `templates/macros.html` |

**Los tokens salen de `.claude/rules/03-sistema-de-diseno.md`.** Ningún color, radio, sombra o espaciado se escribe a mano fuera de `:root`.

El shell de ingreso está en §2.4 de ese documento: contenido centrado sobre `base_publico.html`, sin navegación, con `mockups/mockup-portal/Login.dc.html` como referencia visual.

Componentes mínimos de la fase 0: `icon`, `btn`, `card`, `kpi`, `badge`, `field`, `tabla`, `empty_state`, `alert`, `modal`, `paginacion`, `migas`, `ayuda`.

### E0.5 · Chequeos de salud

```python
# core/checks.py
CHEQUEOS = (
    ("base_de_datos", chequear_bd, True),
    ("migraciones_al_dia", chequear_migraciones, True),
    ("estaticos", chequear_estaticos, False),
)
```

Alimentan **la misma tupla** para el comando `manage.py smoke_test` y para la ruta `/salud/`, de modo que no puedan contradecirse.

### E0.6 · Registro de eventos

`LOGGING` configurado en `settings.py` desde el inicio. Sin esto, los errores no quedan en ningún lado y mostrárselos al usuario se vuelve la única forma de verlos — que es justo lo que la regla de seguridad prohíbe.

### E0.7 · Pantalla de ingreso, sin lógica

Una pantalla de acceso con el lenguaje visual de SIRH+. **No valida nada todavía.** Es una capa visual que la fase 1 conecta.

### E0.8 · Documentos vivos

Se crean los cuatro, con las plantillas de la sección 7 de este documento:

- `CLAUDE.md`
- `docs/trazabilidad.md`
- `docs/pendientes.md`
- `docs/glosario.md`

## 2.2 Fuera de alcance de la fase 0

- Cualquier modelo de negocio
- Cualquier lógica de autenticación o de permisos
- Cualquier conexión a un sistema externo
- Despliegue en servidor

## 2.3 Criterio de aceptación

| # | Se verifica así |
|---|---|
| 1 | `ruff format .` y `ruff check .` sin hallazgos |
| 2 | `python -m unittest discover -s tests` corre, aunque no haya pruebas |
| 3 | `python manage.py smoke_test` en verde y `/salud/` responde |
| 4 | `python manage.py check --deploy` sin hallazgos distintos de los aceptados en la postura de `CLAUDE.md` |
| 5 | La pantalla de ingreso coincide con su artboard: `mockups/mockup-portal/Login.dc.html` |
| 6 | Sebastián levanta el proyecto en su máquina siguiendo solo el `README.md` |

---

# 3 · FASE 1 · Identidad, permisos y auditoría

> **Objetivo:** se entra al sistema con un rol y un alcance, y todo lo que se hace queda registrado. **El catálogo de permisos existe completo desde ahora, aunque la verificación esté apagada.**

## 3.1 Por qué esta fase va primero

El SIRH actual tiene autorización cosmética porque los permisos se agregaron al final, sobre un sistema ya construido. Si repetimos ese orden, llegamos al mismo lugar.

Por eso: **el catálogo se declara en la fase 1 y crece con cada módulo**, con un interruptor que lo hace exigible en cualquier momento.

## 3.2 Entregables

### E1.1 · Modelo de permisos

```
permisos/
├── models.py          Rol, PermisoRol, AsignacionUsuario
├── catalogo.py        el catálogo, declarado en código
├── roles.py           traducción del rol del gestor a permisos internos
├── decoradores.py     @permiso_requerido, @alcance
├── consultas.py
├── presentacion.py
├── views.py
└── alcance.py         resolución del conjunto de personas visible
```

**El catálogo se declara en código, no en la base.** La base guarda qué rol tiene qué permiso; el catálogo de permisos posibles es parte del código y se versiona con él.

```python
# permisos/catalogo.py
CATALOGO = {
    "personal": {
        "titulo": "Personal",
        "permisos": [
            ("personal.ver",              "Ver personal",            "Listado y ficha, dentro de su alcance",        False),
            ("personal.crear",            "Registrar persona",       "Paso 1 del registro: datos básicos",           False),
            ("personal.editar",           "Editar datos básicos",    "Y aprobar solicitudes de actualización",       False),
            ("personal.salario.ver",      "Ver el salario",          "Cada consulta queda en la bitácora",           True),
            ("personal.salario.editar",   "Editar datos reservados", "Salario, EPS, caja, pensión y cesantías",      True),
            ("personal.retirar",          "Registrar un retiro",     "Dispara el paz y salvo y revoca accesos",      True),
            ("personal.exportar",         "Exportar el listado",     "Respeta los permisos de cada columna",         False),
        ],
    },
    # ... un bloque por módulo, que crece con cada fase
}
```

El cuarto valor marca el permiso como **sensible**: su uso se audita obligatoriamente.

### E1.2 · Alcance del dato

Cuatro niveles, modelados aparte del permiso:

| Nivel | Qué ve |
|---|---|
| `propio` | Solo sus propios datos |
| `area` | Las personas de su área |
| `rama` | Las personas que dependen de su cargo en el organigrama |
| `todo` | Toda la empresa |

```python
# permisos/alcance.py
def personas_visibles(usuario, fecha=None):
    """Devuelve el conjunto de documentos que este usuario puede ver.

    El alcance 'rama' se resuelve contra la estructura VIGENTE en `fecha`,
    no contra la actual: una solicitud de hace seis meses debe seguir
    sabiendo quién era el jefe entonces.
    """
```

**Hasta la fase 2 el alcance `rama` y `area` devuelven el conjunto vacío**, porque el organigrama todavía no existe. Eso se documenta y se completa en la fase 2.

### E1.3 · Administración de roles

| Pantalla | Contenido |
|---|---|
| Roles y permisos | Lista de roles, matriz de permisos por módulo, buscador, alcance |
| Usuarios | Quién tiene acceso, con qué rol y qué alcance |
| Simulador | Ver el sistema como lo vería un rol |

Artboards: `v-permisos` y `v-usuarios`.

### E1.4 · El interruptor

```
# .env
PERMISOS_EXIGIR=false     # en desarrollo, hasta que el gestor exista
```

Con `false`, el decorador registra en el log cada verificación que habría fallado, pero deja pasar. Con `true`, bloquea.

**Esto permite probar el control de acceso completo antes del final.** Al menos una vez por fase se corre la aplicación con `PERMISOS_EXIGIR=true` y se revisa el registro.

### E1.5 · Auditoría

```
auditoria/
├── models.py          RegistroAuditoria
├── servicios.py       registrar_cambio(), registrar_consulta()
├── mixins.py          para modelos auditables
├── consultas.py
├── presentacion.py
└── views.py
```

| Campo | Contenido |
|---|---|
| `momento` | Fecha y hora |
| `usuario_id`, `usuario_nombre` | El identificador y el nombre como texto |
| `accion` | crear, modificar, borrar, consultar, denegar |
| `modulo`, `objeto`, `objeto_id` | Qué se tocó |
| `campo`, `valor_anterior`, `valor_nuevo` | Qué cambió |
| `direccion`, `equipo` | Desde dónde |

**La tabla no tiene vistas de edición ni de borrado.** Ni para el administrador.

### E1.6 · Identidad: lo que esta fase **no** construye

**SIRH+ no gestiona usuarios.** La fase 1 entrega el rol y el alcance, no la autenticación.

| Qué | Estado en esta fase |
|---|---|
| Pantalla de ingreso | Existe desde E0.7 y **no valida nada**. Puerta abierta durante el desarrollo |
| Módulo `identidad/` | **No se escribe.** Nace cuando el gestor exista |
| Autenticación local, tabla de usuarios, contraseñas | **No se construyen.** Ni como algo provisional |
| Chequeos de salud de identidad | Declarados y desactivados, listos para encenderse |
| Pantalla propia de 403 | Sí, y se usa en cuanto `PERMISOS_EXIGIR=true` |

Lo que sí es de SIRH+ en esta fase son los permisos, y están en E1.1 a E1.4. La regla completa está en `CLAUDE.md`, «SIRH+ no gestiona usuarios».

## 3.3 Fuera de alcance de la fase 1

- Conexión real al gestor de identidad
- Verificación de permisos **exigida** por defecto
- Cualquier modelo de negocio

## 3.4 Criterio de aceptación

| # | Se verifica así |
|---|---|
| 1 | El catálogo declara todos los permisos de los módulos de las fases 0 a 3 |
| 2 | Un rol con `personal.ver` y sin `personal.salario.ver` no recibe el salario en la respuesta del servidor, no solo oculto en pantalla |
| 3 | Con `PERMISOS_EXIGIR=true`, una ruta sin permiso devuelve la pantalla propia de 403 |
| 4 | Toda modificación deja un registro con valor anterior y nuevo |
| 5 | Un intento de acceso denegado queda registrado |
| 6 | Sebastián crea un rol, le asigna permisos y verifica el comportamiento con el simulador |

---

# 4 · FASE 2 · Empresa

> **Objetivo:** la estructura de la organización, de la que depende todo el enrutamiento del sistema.

## 4.1 Por qué va antes que Personal

Una persona necesita un cargo que exista, y ese cargo necesita saber a quién reporta. Sin eso no hay a quién enrutar una solicitud, ni quién evalúa a quién, ni qué personal ve cada jefe.

## 4.2 Entregables

### E2.1 · Modelo

```python
# maestros/models.py

class Area(models.Model):
    nombre, sigla, correo, estado

class Nivel(models.Model):
    """Los nueve niveles, de operativo a junta directiva."""
    nombre, orden

class Cargo(models.Model):
    nombre, area, nivel, especialidad, estado

class Dependencia(models.Model):
    """Qué cargo reporta a qué cargo, VERSIONADO por fecha.

    Decisiones que encierra:
    - Se versiona porque una solicitud de hace seis meses debe seguir
      sabiendo quién era el jefe entonces.
    - No se borra una dependencia: se cierra su vigencia y se abre otra.
    """
    cargo, cargo_superior, vigente_desde, vigente_hasta
```

### E2.2 · Resolución de la estructura en una fecha

```python
# dominio/estructura.py  — puro, sin Django

def superior_de(cargo_id, dependencias, fecha):
    """El cargo superior vigente en `fecha`. None si no hay."""

def rama_de(cargo_id, dependencias, fecha):
    """Todos los cargos que dependen de este, directa o indirectamente."""

def cargos_sin_superior(cargos, dependencias, fecha):
    """Los que no pueden enrutar nada. Es un hallazgo, no un error."""
```

Pruebas obligatorias: cadena de tres niveles · cargo raíz · cargo huérfano · ciclo (debe detectarse y rechazarse) · estructura en dos fechas distintas.

### E2.3 · Pantallas

| Artboard | Qué resuelve |
|---|---|
| `v-cargos` | Catálogo de áreas y cargos |
| `v-estructura` | Editor de dependencias, con impacto visible |
| `v-organigrama` | Navegable, público |

### E2.4 · Puntos de marcación

```python
# maestros/models.py

class PuntoMarcacion(models.Model):
    """Un conjunto de dispositivos, no un equipo.

    Los cuatro vestieres de mujeres son un solo punto: para una operaria
    son intercambiables. Amarrar el cargo a un dispositivo marcaría como
    irregular algo perfectamente normal.
    """
    nombre, rol  # PORTERIA | DESCANSO | INTERIOR

class Dispositivo(models.Model):
    punto, nombre, direccion, estado

class Cargo(models.Model):
    # ...
    punto_marcacion   # por omisión; puede quedar nulo, y entonces se señala
```

**El rol del punto decide el cálculo de horas**, no solo el permiso: es lo que determina si el tiempo entre dos marcaciones se cobra al empleado o lo asume la empresa. Cambiarlo es una acción que muestra su impacto antes de confirmarse.

**Regla inviolable:** una marcación en un dispositivo no autorizado **nunca se descarta**. Se registra y se clasifica como excepción. Descartarla sería perder un dato que vale dinero.

### E2.5 · Matriz de capacitación por cargo

Solo la **definición**: qué documentos aplican a cada cargo. El uso llega en la fase 14.

### E2.6 · Completar el alcance

Con el organigrama existiendo, `permisos/alcance.py` deja de devolver el conjunto vacío:

```python
def personas_visibles(usuario, fecha=None):
    # 'rama' ahora resuelve contra dominio.estructura.rama_de()
```

### E2.7 · Migración

32 áreas y 198 cargos del sistema actual. La estructura de dependencias **no existe hoy** y hay que construirla con RH. Es trabajo de ellos, no de TI.

## 4.3 Fuera de alcance

- Asignar personas a cargos, que es la fase 3
- Usar la matriz de capacitación

## 4.4 Criterio de aceptación

| # | Se verifica así |
|---|---|
| 1 | La estructura resuelve el superior correcto en dos fechas distintas |
| 2 | Un ciclo en la estructura se rechaza con un mensaje claro |
| 3 | Los cargos sin superior aparecen señalados |
| 4 | El organigrama se ve sin iniciar sesión |
| 5 | Un usuario con alcance `rama` ve exactamente los cargos de su rama |
| 6 | RH revisa la estructura cargada y confirma que refleja la realidad |

---

# 5 · FASE 3 · Personal y firmas

> **Objetivo:** registrar una persona de punta a punta, con su firma, y ver su hoja de vida.

## 5.1 Entregables

### E3.1 · Modelo

```python
# personal/models.py

class Persona(models.Model):
    """Identificación. Lo que no cambia."""
    documento (llave), tipo_documento, nombres, apellidos, genero,
    fecha_nacimiento, foto, grupo_sanguineo, nivel_educativo

class Vinculo(models.Model):
    """La relación laboral, VERSIONADA.

    Una persona puede tener varios vínculos en el tiempo: ingresó,
    se retiró, reingresó. Cada uno con su código de nómina propio.
    """
    persona, tipo, empresa, codigo_interno, codigo_nomina,
    fecha_ingreso, fecha_contrato, fecha_retiro, estado

class AsignacionCargo(models.Model):
    """Qué cargo tiene, VERSIONADO por fecha."""
    vinculo, cargo, vigente_desde, vigente_hasta

class DatosContacto(models.Model):
    correo, telefonos, contacto_urgencia, localidad

class DatosSST(models.Model):
    brigadista, restriccion_fisica, restriccion_medica

class DatosReservados(models.Model):
    """Separado a propósito: su acceso se controla aparte."""
    vinculo, salario, eps, caja, pension, cesantias, nivel_riesgo,
    vigente_desde, vigente_hasta

class SolicitudActualizacion(models.Model):
    persona, campo, valor_actual, valor_solicitado, estado, observacion
```

**`DatosReservados` es una tabla aparte, no columnas de `Vinculo`.** Así el permiso se aplica a nivel de consulta y el dato no viaja al navegador de quien no debe verlo.

### E3.2 · El código de nómina

```python
# dominio/codigos.py  — puro

def codigo_nomina(documento, tipo_vinculo, reglas, usados):
    """Construye el código y verifica que sea único.

    Decisiones que encierra:
    - El sufijo depende del tipo de vínculo y es PARAMETRIZABLE: RH puede
      cambiar la política sin tocar código.
    - La unicidad se verifica contra el HISTÓRICO COMPLETO, no contra los
      activos: un temporal que pasó a directo y reingresa puede colisionar.
    - NO se normalizan ceros a la izquierda. La herramienta anterior lo
      hacía y eso puede liquidar mal a alguien.
    """
```

Pruebas: cada tipo de vínculo · colisión con un código histórico · documento de seis dígitos · reingreso.

### E3.3 · Completitud por hitos

El registro se completa por etapas. Cada hito tiene su peso, su dueño y su consecuencia.

```python
# personal/hitos.py

HITOS = [
    ("identificada", 10,  "Documento, nombres y código interno"),
    ("vinculada",    25,  "Tipo de vínculo, empresa y fecha de ingreso"),
    ("ubicada",      40,  "Cargo asignado y punto de marcación"),
    ("habilitada",   55,  "Firma capturada y clave creada"),
    ("liquidable",   70,  "Salario, EPS, caja y pensión"),
    ("completa",     85,  "Contacto, urgencia y datos de SST"),
    ("al_dia",      100,  "Examen de ingreso e inducción"),
]
```

| Regla | Detalle |
|---|---|
| **Hitos, no campos contados** | Un promedio de campos iguala cosas que no pesan igual y da tranquilidad falsa |
| **El umbral operativo es 40 %** | Bajo eso la persona no puede trabajar: el biométrico no la reconoce y nadie puede aprobarle nada |
| **Plazo de 24 horas bajo el 40 %** | Parámetro `personal.plazo_incompleto`. Pasado el plazo, rojo en la bandeja |
| **Cada módulo declara su hito** | `personal/` solo suma los declarados. No importa de eventualidades ni de formación |
| **No son parametrizables** | Si se movieran, el porcentaje dejaría de ser comparable entre dos momentos |

Durante esta fase el tope real es **85 %**: los dos hitos finales aparecen con sus módulos.

### E3.4 · Captura rápida

Una pantalla para registrar a varias personas seguidas, mientras otras esperan.

| Regla | Detalle |
|---|---|
| **Cinco campos** | Documento, nombres, apellidos, código interno, cargo |
| **El cargo deriva seis cosas** | Área, nivel, jefe, matriz, turno y punto de marcación. Se muestran, no se digitan |
| **El código interno se propone** | El siguiente consecutivo, sobrescribible |
| **Unicidad al escribir** | Documento y código, contra el histórico completo, distinguiendo duplicado de reingreso |
| **Guardar devuelve el foco** | Al documento, sin recargar. Ahí está la diferencia entre diez minutos y cuarenta |
| **La foto va a una cola** | No es un campo del registro, y no pesa en la completitud |

**La cola de fotos** es su propia pantalla: disparar y avanzar, con la barra espaciadora.

### E3.5 · Excepción de punto de marcación

El punto lo define el cargo. Una persona puede tener uno distinto, con **motivo, vigencia y autorizador**, registrado en la bitácora. Cerrar la excepción la devuelve al punto de su cargo.

**Al guardar el primer hito salen los disparadores.** Que falten datos posteriores no detiene nada: la persona ya tiene acceso. Lo único bloqueado es lo que cada hito habilita.

### E3.6 · Firmas

```
firmas/
├── models.py          Firma, UsoFirma
├── servicios.py       capturar(), invocar(), estampar()
├── pdf.py             generación del documento firmado
└── views.py
```

| Regla | Detalle |
|---|---|
| Se captura **una vez**, al ingreso, en tableta |
| Se guarda como coordenadas, con documento y código interno |
| Para usarla se exige **la clave propia del colaborador** |
| Cada uso registra quién, cuándo, desde dónde y sobre qué documento |
| El restablecimiento de clave lo hace TI, no RH |

**Por qué clave y no cédula más código interno:** ambos datos los conocen otras personas. Cualquiera podía firmar por un compañero.

### E3.7 · Hoja de vida

La vista más importante del módulo. Nace aquí con lo que existe —cargos, firma, datos— y **se llena sola** a medida que llegan eventualidades, formación, competencias y dotación.

Artboard: `v-hoja`.

### E3.8 · Disparadores

| Destino | Cuándo | Estado en esta fase |
|---|---|---|
| GLPI | Al guardar el paso 1 | **Activo.** La lógica existente se conserva |
| Gestor de identidad | Al guardar el paso 1 | **Listo y apagado.** La intención se escribe en la outbox; nadie la consume hasta que el gestor exista |
| Formación | Al asignar el cargo | Se registra la matriz; el uso llega en la fase 14 |

Los disparadores van por **outbox**: se escribe la intención en una tabla y un proceso aparte la ejecuta. Así una caída de GLPI no impide registrar a una persona.

### E3.9 · `parametros/` mínimo

La fase 3 necesita dos parámetros y el plan pone `parametros/` en la fase 5. Se parte en dos: **aquí nace el modelo, en la fase 5 nace la administración.**

```
parametros/
├── models.py          Parametro, Vigencia
└── consultas.py
```

```python
# dominio/parametros.py  — puro

def vigente_en(clave, vigencias, fecha):
    """El valor que regía en `fecha`.

    Un parámetro no se sobrescribe: se cierra su vigencia y se abre otra.
    El cálculo busca el valor que regía en la fecha del hecho, no el de hoy.
    """
```

Los dos parámetros que esta fase necesita:

| Clave | Para qué |
|---|---|
| `personal.plazo_incompleto` | Las 24 horas que vale un registro bajo el 40 % — ver E3.3 |
| `personal.codigo_nomina.sufijos` | Qué dígito corresponde a qué tipo de vínculo — ver E3.2 |

**Fuera de alcance aquí:** la pantalla de administración, el catálogo por módulo, el historial de vigencias y el calendario de festivos. Todo eso es de la fase 5.

Pruebas: fecha anterior a toda vigencia · fecha entre dos vigencias · fecha dentro de la vigente · clave inexistente.

## 5.2 Fuera de alcance

- Migrar los datos reales, que es la fase 4
- El paz y salvo de retiro, que necesita el motor de registros de la fase 12

## 5.3 Criterio de aceptación

| # | Se verifica así |
|---|---|
| 1 | Un usuario sin `personal.salario.ver` **no recibe el salario en la respuesta del servidor** |
| 2 | El código de nómina rechaza una colisión con un código histórico |
| 3 | El paso 1 guardado dispara GLPI aunque falten los datos reservados |
| 4 | La firma no se puede invocar sin la clave |
| 5 | Cada uso de firma deja registro |
| 6 | La hoja de vida muestra el cargo correcto en una fecha pasada |
| 7 | La captura rápida registra 10 personas seguidas sin recargar ni perder el foco |
| 8 | El porcentaje refleja hitos, y un registro bajo el 40 % con más de 24 horas sale en rojo |
| 9 | Una excepción de punto queda con motivo, vigencia y autorizador en la bitácora |
| 10 | Sebastián registra una persona de prueba completa, de punta a punta |

---

# 6 · FASES 4 A 22

El contenido de cada una está en `01-inventario-y-fases-sirh-plus.md`, sección «Detalle de cada fase».

**Cada fase se detalla en este documento al estilo de las anteriores, justo antes de empezarla**, no ahora. Escribir hoy el detalle de la fase 17 es inventar: para entonces habremos aprendido cosas que cambiarían lo escrito.

Lo que sí está fijo desde ahora:

| Fase | Hito |
|---|---|
| 4 | Migración del maestro: 1.094 personas y 8.214 firmas |
| 5 | Administración de parámetros y motor de vencimientos. **El modelo `Parametro` ya existe desde la fase 3** (E3.9): aquí llegan la pantalla, el catálogo por módulo, el historial de vigencias y el calendario de festivos |
| 6–9 | Marcaciones: captura, turnos, cálculo, cierre |
| 10 | **Archivo plano de nómina. BioTime se integra** |
| 11 | Eventualidades |
| 12 | Motor de registros firmados y notificaciones |
| 13 | **Trámites. El colaborador entra al sistema** |
| 14 | **Divulgaciones. COPEC se integra** |
| 15–16 | Inducción, cursos y R-RH-009 |
| 17 | Competencias |
| 18 | Dotación y EPP |
| 19 | Encuestas y reservas |
| 20 | Contenido corporativo y portal público |
| 21 | Indicadores e informes |
| 22 | **Histórico. El SIRH antiguo se apaga** |

---

# 7 · Plantillas de los documentos vivos

## 7.1 `CLAUDE.md`

```markdown
# SIRH+ — Contexto para los agentes

Sistema de Información de Recursos Humanos de Plastitec S.A.S.
Reemplaza al SIRH antiguo, e integra BioTime y COPEC.

## Qué es este sistema

~1.100 personas entre directos, temporales de Granservicios y aprendices SENA.
Una sola aplicación con tres caras: pública, colaborador y gestión.

## Las reglas que no se rompen

1. `dominio/` no importa Django ni hace entrada/salida.
2. El permiso se verifica en el SERVIDOR. Ocultar un enlace no es protección.
3. Los valores van como parámetro en toda consulta.
4. Un parámetro legal se guarda con su VIGENCIA, nunca se sobrescribe.
5. El salario vive en una tabla aparte y su consulta se audita.
6. El código de nómina se verifica contra el histórico completo.
7. La estructura del organigrama se resuelve a una FECHA, no a hoy.

## Estado actual

Fase en curso: <N> — <nombre>
Última fase cerrada: <N> — <fecha>

## Módulos construidos

| Módulo | Fase | Qué hace |
|---|---|---|
| ... | ... | ... |

## Decisiones de dominio que hay que conocer

- <decisión> porque <razón>
- Intento fallido: <qué se probó y por qué no funcionó>

## Lo primero que se lee al retomar

`docs/pendientes.md`
```

## 7.2 `docs/trazabilidad.md`

```markdown
# Trazabilidad de decisiones

Una entrada por decisión. No se borran ni se editan: se agregan.

---

## <AAAA-MM-DD> · <título de la decisión>

**Fase:** <N>
**Qué se decidió:** <una frase>

**Por qué:**
<el razonamiento>

**Qué se evaluó y se descartó:**
| Opción | Por qué no |
|---|---|

**Qué cambia si esto resulta equivocado:**
<el costo de revertirla>
```

## 7.3 `docs/pendientes.md`

```markdown
# Pendientes

Lo primero que se lee al retomar el proyecto.

## Bloqueado

| # | Qué | Quién lo destraba | Desde |
|---|---|---|---|

## Abierto

| # | Qué | Fase en que se resuelve |
|---|---|---|

## Deuda asumida a conciencia

| # | Qué | Por qué se asumió | Cuándo se paga |
|---|---|---|---|

## Ideas que no son de esta fase

| # | Idea | Fase candidata |
|---|---|---|
```

## 7.4 `docs/glosario.md`

El vocabulario de la sección 1.5, más los términos que cada módulo agregue.

---

# 8 · Lo que se aprendió y no se repite

Errores reales de este proyecto, antes de escribir código.

1. **Se recomendó un stack antes de conocer el estándar de la empresa.** Antes de decidir tecnología, preguntar qué corre ya en la organización.
2. **Se escribió un plan antes de definir qué hacía el aplicativo.** El orden es alcance → diseño → plan.
3. **El primer mockup era un panel administrativo genérico.** Un portal para 1.100 personas no se ve como una herramienta interna.
4. **Se dio por hablada una decisión que nunca se tomó.** Revisar el historial antes de afirmar que algo ya se acordó.
5. **La documentación que contradice al código desinforma.** Los documentos obsoletos llevan advertencia, no se borran en silencio.
6. **El Portal se diseñó como aplicación aparte y no lo es.** Se corrigió antes de escribir código, que es el único momento barato.
7. **La cifra de personal estaba mal por un factor de dos.** Verificar las cifras que fundamentan decisiones, aunque vengan de un documento propio.
8. **Existían tres herramientas haciendo lo mismo y nadie lo había notado junto.** Antes de construir, inventariar qué hay funcionando en las orillas.
9. **Se iba a llevar a gerencia una cifra sin verificar.** Un argumento fuerte sin comprobar es un argumento que se cae en la reunión.

---

# 9 · Qué hace falta antes de la fase 0

| # | Qué | Quién |
|---|---|---|
| 1 | ~~Escribir el sistema de diseño desde el mockup aprobado~~ · **Hecho el 5 de noviembre de 2026**, en `.claude/rules/03-sistema-de-diseno.md` | TI |
| 2 | Rotar los tokens de GLPI y las credenciales que están en la base | TI |
| 3 | Poner el código del SIRH viejo y el de COPEC bajo control de versiones | TI |
| 4 | Construir con RH la estructura de dependencias de los 198 cargos | RH |
| 5 | Confirmar el código y el porcentaje vigente del recargo dominical | Nómina |
| 6 | Definir el tratamiento de Granservicios en el archivo de nómina | RH |
| 7 | Conseguir los formatos en blanco R-RH-009, R-RH-053 y paz y salvo | RH |

**Los puntos 2 y 3 bloquean la fase 0** — son B1 y B2 de `docs/pendientes.md`. El punto 1 ya está resuelto. Los demás se pueden resolver en paralelo.
