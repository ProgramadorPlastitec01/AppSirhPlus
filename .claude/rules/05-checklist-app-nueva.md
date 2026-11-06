# 05 — Checklist: levantar una app nueva

> ## Adaptación para SIRH+
>
> Este checklist describe el ciclo de **una** aplicación. SIRH+ lo aplica **23 veces**, una por fase del plan.
>
> **Equivalencias con `claude/02-plan-de-ejecucion-sirh-plus.md`:**
>
> | Aquí | En SIRH+ |
> |---|---|
> | Fase 0 y Fase 1 | **Fase 0 — Cimientos** |
> | Fase 2 · entrevista y diseño | **Ya hecha.** Está en `docs/diseno.md` y en `claude/00`, `01`, `02` y `03`. **Validada el 5 de noviembre de 2026** |
> | Fase 3 y Fase 4 | Se repiten **dentro de cada una** de las 23 fases |
> | Fase 5 | Las **seis compuertas** del plan |
> | Fase 6 | Al salir a producción, no antes |
> | Fase 7 | Al cerrar cada fase |
>
> **No se vuelve a hacer la entrevista de dominio.** El agente `arquitecto` solo interviene cuando una fase futura necesite diseño que el plan todavía no detalla.
>
> **Cuatro desviaciones declaradas**, documentadas en `docs/diseno.md` §8 y en `claude/02` §1.2: el shell (D1), los permisos granulares (D2), el alcance del dato (D3) y la identidad diferida (D4). **No se corrigen.**

Secuencia que siguen el desarrollador y los agentes. **El orden importa**: cada paso depende del anterior.

---

> **Dos cosas que conviene no confundir.** El **esqueleto** es idéntico en toda app y se construye sin preguntar. La **lógica de negocio** es propia de cada app y no se escribe sin diseño validado. Por eso el esqueleto va antes del diseño, y el dominio después.

## Fase 0 — Crear el proyecto

En SIRH+ el repositorio ya existe y el esqueleto se construye a mano, sin el generador.

- [ ] Carpeta creada con la plantilla completa, incluidos los archivos ocultos.
- [ ] `git init` y primer commit con `.gitignore` puesto. **Antes que nada.**
- [ ] **`referencia/` dentro del `.gitignore`.** Son 140 MB con datos personales de 9.058 personas. Si se sube una vez, sacarlo del historial después es un dolor.
- [ ] `pyproject.toml` con la configuración de `ruff`.
- [ ] `CLAUDE.md` y `docs/` de la plantilla, sin llenar.

## Fase 1 — Esqueleto (sin preguntar nada)

Todo lo de esta fase está decidido por el estándar. No se consulta: se construye.

- [ ] Estructura de carpetas de `01 §1`.
- [ ] `settings.py` leyendo `.env`; PostgreSQL como única base del ORM.
- [ ] `LOGGING` configurado (04 §4).
- [ ] `.env.example` con todas las variables documentadas. `.env` real fuera de git.
- [ ] `requirements.txt` con cada dependencia justificada (02 §3).
- [ ] **Ningún paquete de identidad.** SIRH+ no gestiona usuarios, así que no se copia `cuentas/` ni se escribe nada en su lugar (ver 07, la nota del encabezado).
- [ ] `core/checks.py` con los chequeos de salud + comando + ruta `/salud/`.
- [ ] `static/css/styles.css` con los tokens de `03-sistema-de-diseno.md §1.1`.
- [ ] `templates/base.html`, `base_portal.html`, `base_publico.html`, `base_auth.html`, `macros.html`, `403.html`.
- [ ] Tipografía (Archivo e Inter) e iconos auto-hospedados en `static/vendor/`.
- [ ] `README.md`: qué hace la app, para quién, cómo se levanta en local.

### Identidad — desviación D4

El gestor de identidad está en construcción. En su lugar:

- [ ] Pantalla de ingreso **sin lógica de validación**, con el lenguaje visual de SIRH+. Durante el desarrollo es una puerta abierta.
- [ ] **Nada de autenticación local**: ni tabla de usuarios, ni contraseñas, ni «algo provisional» que después haya que desmontar.
- [ ] Los dos chequeos de salud de identidad **declarados y desactivados**, listos para encenderse.
- [ ] `PERMISOS_EXIGIR=false` en `.env`, documentado.

**Lo que se difiere hasta que el gestor exista:** el módulo `identidad/` completo —autenticar contra el gestor y avisarle de las altas y las bajas—, el registro de SIRH+ en el catálogo del gestor, y el inicio de sesión funcionando de verdad.

**Lo que no se difiere: no llega nunca.** El cambio de contraseña, la administración de usuarios y el almacenamiento de credenciales son del gestor. SIRH+ no los construye en ninguna fase.

**En este punto la app no hace nada útil todavía, pero ya se ve y se comporta como una app de Plastitec.**

- [ ] `ruff format . && ruff check .` sin hallazgos.
- [ ] `manage.py smoke_test` en verde. Commit.

## Fase 2 — Entrevista de dominio y diseño (agente Arquitecto, validación humana obligatoria)

> **En SIRH+ esta fase ya está cerrada.** El diseño está en `docs/diseno.md`, validado el 5 de noviembre de 2026, y se apoya en `claude/00`, `01`, `02` y `03` más los mockups.
>
> **No se repite la entrevista.** Este bloque se reactiva solo cuando una fase futura necesite diseño que el plan todavía no detalla; entonces se amplía `docs/diseno.md`, no se reescribe.

Primero se llena el `CLAUDE.md` con lo que diga el negocio. Después se produce `docs/diseno.md`, **antes de una sola línea de lógica de negocio**:

- [x] Qué problema resuelve y quién lo va a usar.
- [x] Reglas de negocio identificadas — en lenguaje del negocio, no técnico.
- [x] Módulos funcionales (una app Django por módulo).
- [x] Modelo de datos propio · qué sistemas ajenos se consultan y en modo lectura.
- [x] Pantallas, y a cuál patrón de `03-sistema-de-diseno.md §5` corresponde cada una.
- [x] Roles y qué puede hacer cada uno.
- [x] **Desviaciones del estándar, con justificación escrita.** Son cuatro: D1 a D4.
- [x] **Preguntas abiertas registradas**, en `docs/pendientes.md`.

> ⛔ **No se pasa a la Fase 3 sin validación humana explícita de `docs/diseno.md`.** Es donde los errores cuestan minutos en vez de días.

## Fase 3 — Núcleo de dominio (agente Developer)

- [ ] `dominio/` con las reglas, **sin importar Django ni I/O**.
- [ ] `tests/` cubriendo cada regla y cada caso límite.
- [ ] Las pruebas corren con un comando y sin levantar Django.

> Se hace **antes** que las vistas. Es la capa que se puede verificar de verdad; construirla primero da una base sobre la que el resto se apoya.

## Fase 4 — Módulos

Por cada módulo, en este orden:

- [ ] Migración del modelo de datos.
- [ ] `consultas.py` — acceso a datos, parametrizado (04 §3), con troceo por lotes si aplica.
- [ ] `presentacion.py` — arma lo que la plantilla necesita.
- [ ] `views.py` — delgado: recibe, delega, responde.
- [ ] Plantillas con **los cuatro estados** de `03-sistema-de-diseno.md §4.8`.
- [ ] `exportacion.py` si hay salidas a archivo.
- [ ] **Ayuda contextual del módulo** en `templates/ayuda/<modulo>.html`.

## Fase 5 — Verificación

En SIRH+ estas son **las seis compuertas**. Ninguna es opcional.

- [ ] `ruff format .` y `ruff check .` sin hallazgos.
- [ ] Pruebas del núcleo en verde: `python -m unittest discover -s tests`.
- [ ] `manage.py smoke_test` en verde y la ruta `/salud/` respondiendo.
- [ ] **Seguridad** (agente + herramientas): `check --deploy`, rutas protegidas, secretos, errores expuestos.
- [ ] **QA** (agente, partiendo de `docs/diseno.md`, **no** del razonamiento del developer): casos límite, reglas de negocio, datos ausentes, entradas inválidas.
- [ ] Revisión de cierre de `03-sistema-de-diseno.md §9`: sin CDN, sin valores fuera de `:root`, cuatro estados resueltos, recorrido completo con teclado, cifras con `tabular-nums`, cada dato ajeno con su origen.
- [ ] **Validación humana contra el problema real.** Nadie más puede hacer esta.

Al menos una vez por fase, además:

- [ ] Correr la aplicación con `PERMISOS_EXIGIR=true` y revisar el registro de verificaciones que habrían fallado. **Es la salvaguarda contra repetir la autorización cosmética del sistema viejo.**

## Fase 6 — Despliegue

- [ ] `deploy/` con la unit de systemd, la conf de Nginx y el runbook.
- [ ] `DEBUG=False`, `ALLOWED_HOSTS` explícito, usuario dedicado.
- [ ] Particularidades del servidor documentadas en el repo (04 §6).
- [ ] Secretos de producción distintos, y respaldados fuera del servidor.
- [ ] **El gestor de identidad funcionando.** SIRH+ no sale a producción sin él (D4).

## Fase 7 — Cerrar el ciclo

- [ ] **Agente Documentador**: documentación técnica y funcional al día.
- [ ] `CLAUDE.md`: actualizar la tabla de estado y la de módulos construidos.
- [ ] `docs/trazabilidad.md`: una entrada por cada decisión tomada en la fase.
- [ ] `docs/pendientes.md`: mover lo resuelto, subir lo que se volvió bloqueante.
- [ ] `docs/glosario.md`: los términos nuevos que introdujo la fase.
- [ ] Desviaciones del estándar que resultaron buenas → propuestas como regla nueva aquí.
- [ ] Lo que salió mal → `06-lecciones.md`.

---

## La regla que mantiene vivo el estándar

> Cada bug que llega a producción termina en una línea de `06-lecciones.md`.
> Cada desviación que se repite en tres apps deja de ser desviación y se promueve a regla.

Sin esto, el estándar es una foto que envejece. Con esto, el conocimiento deja de vivir solo en la cabeza del programador.
