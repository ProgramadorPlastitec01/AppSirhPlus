# Pendientes

**Lo primero que se lee al retomar el proyecto.**

Actualizado: 6 de noviembre de 2026 · Fase en curso: 0 — Cimientos

---

## Bloqueado

Nada avanza hasta que alguien de fuera del proyecto lo resuelva.

| # | Qué | Quién lo destraba | Bloquea | Desde |
|---|---|---|---|---|
| B1 | Rotar los tokens de GLPI y las credenciales que están en texto plano en la tabla `configuracion` del SIRH viejo | TI | **Fase 0** · es riesgo de hoy, no del proyecto | 29/09/2026 |
| B2 | Poner el código del SIRH viejo y el de COPEC bajo control de versiones | TI | **Fase 0** · hoy no hay respaldo del código fuente | 29/09/2026 |
| B3 | Construir con RH la estructura de dependencias de los 198 cargos | RH | **Fase 2** · no existe hoy en ningún sistema | 05/11/2026 |
| B4 | Documentación de la API de los biométricos | Compañero de TI | Fase 6 | — |
| B5 | Acceso de lectura a Daruma y nombres de las tablas que usa COPEC | TI | Fase 14 | — |
| B6 | Gestor de identidad en producción | TI | Salida a producción, no el desarrollo | — |
| B7 | Máquina de producción | TI | Puesta en marcha | — |

---

## Abierto

Decisiones de negocio sin tomar. No bloquean todavía, pero sí a su fase.

| # | Qué | Quién decide | Se necesita en |
|---|---|---|---|
| A1 | Código y porcentaje vigente del recargo dominical. ¿`0253` sigue vigente con tarifa nueva, o nómina creó un código? | Nómina | Fase 10 |
| A2 | Tratamiento de Granservicios en el archivo de nómina: ¿un archivo o dos? Son ~493 personas | RH + Granservicios | Fase 10 |
| A3 | ¿El colaborador ve su propia calificación de competencias? | RH | Fase 17 |
| A4 | ¿El evaluado firma el R-RH-053, o basta el registro de auditoría del jefe? | RH | Fase 17 |
| A5 | ¿La autorización de tratamiento de datos debe firmarse en el hito del 10 % o puede esperar al 55 %? | RH + jurídico | Fase 3 |
| A6 | Nota mínima y número de reintentos en los cursos | RH | Fase 15 |
| A7 | Plazo límite para que una divulgación se lea y se firme | RH | Fase 14 |
| A8 | Quién mantiene el maestro de códigos de nómina y por qué cubre 437 de 1.094 personas | RH | Fase 10 |
| A9 | Dueño definitivo de contrato y salario cuando SINERGY exponga API | RH + Nómina | Sin fecha |
| A10 | Dónde se guarda la foto del colaborador y con qué compresión. Mil fotos sin comprimir son un problema de disco y de velocidad | TI | Fase 3 |
| A11 | **Cuánto dura la sesión.** Hoy son 30 minutos, un valor provisional puesto en la fase 0 porque el portal muestra el temporizador y el número tenía que existir. Se cambia con `SESION_MINUTOS` en el `.env`, sin tocar código. El equipo de vestier marca y se va; RH pasa la jornada dentro: puede que no sea un solo número | RH + TI | Fase 1 |

---

## Deuda asumida a conciencia

Cosas que se hacen mal **a propósito**, con su fecha de pago.

| # | Qué | Por qué se asumió | Cuándo se paga |
|---|---|---|---|
| D1 | SIRH+ sostiene salario, cargo y fecha de ingreso para el certificado laboral, aunque el dueño sea SINERGY | SINERGY no expone API. Sin esto no hay certificado | Cuando SINERGY se conecte. El certificado lleva fecha de corte visible |
| D2 | El saldo de vacaciones se calcula en SIRH+ desde la fecha de contrato | Mismo motivo | Igual |
| D3 | Los permisos se declaran pero no se verifican por defecto | El gestor de identidad no existe todavía | Al conectar el gestor. Mientras tanto, `PERMISOS_EXIGIR=true` al menos una vez por fase |
| D4 | La pantalla de ingreso no valida nada: durante el desarrollo es una puerta abierta | Igual. **No se construye autenticación local en su lugar**: SIRH+ no gestiona usuarios | Al conectar el gestor. **Así nunca sale a producción** |
| D5 | Los enlaces a documentos de Daruma se registran a mano | Daruma no expone API | Si Daruma algún día la expone |

---

## Ideas que no son de esta fase

Buenas ideas que aparecieron fuera de lugar. **Van aquí, no al código.**

| # | Idea | Fase candidata |
|---|---|---|
| I1 | Enviar la inducción por enlace para hacerla desde casa antes del primer día. Exige la cuenta de pre-ingreso y salir a internet | 15 |
| I2 | Adjuntar el documento de evidencia del examen médico, no solo la fecha y el concepto | 11 |
| I3 | Nota mínima en los cursos de inducción. Hoy no existe | 15 |
| I4 | Que el manual de usuario se adapte por cargo, de modo que cada persona vea solo lo suyo | Posterior a la 22 |
| I5 | Seguimiento de recobro de incapacidades ante EPS y ARL | Sin asignar |
| I6 | Jefes suplentes para cuando el titular está de vacaciones | Sin asignar. No se ha presentado la necesidad |
| I7 | Sacar las marcaciones directamente de los dispositivos sin ninguna capa intermedia | Ya es el plan de la fase 6 |

---

## Riesgos abiertos del sistema actual

No son del proyecto, pero existen hoy y conviene no perderlos de vista.

| # | Riesgo | Estado |
|---|---|---|
| R1 | Inyección SQL en 245 consultas | Se cierra al apagar el SIRH viejo, fase 22 |
| R2 | Contraseñas en MD5 con retroceso a texto plano | Igual |
| R3 | Autorización puramente cosmética: quien conozca una URL entra | Igual |
| R4 | Credenciales y tokens legibles en la tabla `configuracion` | **B1** · se rota ya |
| R5 | Un retiro no revoca accesos en ningún aplicativo | Se cierra en la fase 3 |
| R6 | 657 personas no aparecen en el archivo de nómina y nadie recibe aviso | Se cierra en la fase 10 |
| R7 | Sin respaldo del código fuente | **B2** · se resuelve ya |
| R8 | `sirh.json` con datos personales de cientos de empleados dentro del proyecto | Pendiente de sacar |

---

## Cómo se usa este archivo

- Se lee **al empezar cada sesión**, antes del plan.
- Cuando algo se resuelve, se mueve a una sección «Resuelto» al final con su fecha, **no se borra**.
- Una idea que aparece en medio de una fase se anota aquí y se sigue con lo que estaba.
- Si un pendiente bloquea de verdad, sube a la tabla de **Bloqueado** y se avisa a quien lo destraba.
