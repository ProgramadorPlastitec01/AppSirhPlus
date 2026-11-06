# Glosario

Vocabulario del proyecto. **Estos términos se usan en la interfaz y en el código.** Si la pantalla dice «eventualidad», el modelo se llama `Eventualidad`.

Un sistema donde el mismo concepto se llama de tres maneras es un sistema que nadie puede mantener.

---

## 1 · Personas

| Término | Qué es | En código |
|---|---|---|
| **Colaborador** | El empleado visto como usuario del sistema. Es como se le nombra en la interfaz | — |
| **Persona** | La identificación: documento, nombres, fecha de nacimiento. Lo que no cambia | `Persona` |
| **Vínculo** | La relación laboral. Una persona puede tener varios en el tiempo: ingresó, se retiró, reingresó | `Vinculo` |
| **Documento** | La cédula. Identificación legal | `documento` |
| **Código interno** | Consecutivo de 4 dígitos que se asigna al ingresar. **Es el mismo del biométrico y de la firma** | `codigo_interno` |
| **Código de nómina** | Cédula más un dígito según el vínculo. Es el que viaja en el archivo plano | `codigo_nomina` |
| **Datos reservados** | Salario, EPS, caja, pensión, cesantías. Viven en tabla aparte y su consulta se audita | `DatosReservados` |
| **Completitud** | El porcentaje de hitos cumplidos en el registro de una persona, de 10 % a 100 % | `completitud` |
| **Hito** | Cada una de las siete etapas del registro, con su peso, su dueño y lo que habilita | `Hito` |

**No se usa «empleado» en la interfaz.** Se usa «colaborador».

---

## 2 · Organización

| Término | Qué es | En código |
|---|---|---|
| **Área** | Unidad organizativa. Hay 32 | `Area` |
| **Cargo** | Posición dentro de un área. Hay 198 | `Cargo` |
| **Nivel** | Uno de los nueve escalones, de operativo a junta directiva | `Nivel` |
| **Dependencia** | Qué cargo reporta a qué cargo. **Versionada por fecha** | `Dependencia` |
| **Estructura** | El conjunto de dependencias vigentes en una fecha | — |
| **Rama** | Todos los cargos que dependen de uno, directa o indirectamente | `rama_de()` |
| **Organigrama** | La representación visual de la estructura. Es público | — |
| **Vacante** | Un cargo sin asignación vigente | — |
| **Alcance** | Qué conjunto de personas ve un usuario: propio, área, rama o todo | `alcance` |

---

## 3 · Marcaciones y jornada

| Término | Qué es | En código |
|---|---|---|
| **Marcación** | Un golpe en un biométrico. El hecho crudo | `Marcacion` |
| **Dispositivo** | Un biométrico concreto. Hay 10 | `Dispositivo` |
| **Punto de marcación** | Un **conjunto** de dispositivos donde un cargo puede marcar | `PuntoMarcacion` |
| **Rol del punto** | Portería, descanso o interior. Decide si el hueco se cobra al empleado | `rol` |
| **Excepción de punto** | Una persona marca en un punto distinto al de su cargo, con motivo y vigencia | `ExcepcionPunto` |
| **Turno** | Catálogo con bloques por día de la semana | `Turno` |
| **Bloque** | Un tramo del turno para un rango de días | `BloqueTurno` |
| **Programación** | La asignación de turno a una persona en una fecha | `Programacion` |
| **Jornada** | Un día calculado de una persona | `Jornada` |
| **Tramo** | Un segmento de tiempo con un mismo tipo de día y una misma franja | `Tramo` |
| **Horas pendientes** | Tiempo de turno no cumplido. **Se reporta, no se descuenta del pago** | `pendiente_min` |
| **Escalera** | La regla de acreditación del sobretiempo por medias horas | — |
| **Semana operativa** | Arranca el domingo a las 22:00, no a medianoche del lunes | — |
| **Café pagado** | El descanso de 20 minutos que la empresa asume | — |
| **Excepción** | Algo que no cuadra y que alguien debe revisar. **No es un rechazo** | `Excepcion` |

---

## 4 · Nómina

| Término | Qué es | En código |
|---|---|---|
| **Concepto** | Un tipo de pago con su código: extra diurna, recargo nocturno | `Concepto` |
| **Período** | El ciclo de nómina, del 11 al 10 | `Periodo` |
| **Cierre** | El momento en que un período se congela y no admite cambios | — |
| **Archivo plano** | El `FINAL_SINER_*.txt` que se carga a SINERGY | — |
| **Conciliación** | Contrastar lo calculado contra lo liquidado | — |

---

## 5 · Eventualidades y trámites

| Término | Qué es | En código |
|---|---|---|
| **Eventualidad** | Lo que le pasa a una persona en una fecha: accidente, incapacidad, ausencia, descargo, examen, retiro | `Eventualidad` |
| **Trámite** | Una solicitud con radicado y estado | `Tramite` |
| **Radicado** | El número consecutivo de un trámite | `radicado` |
| **Paz y salvo** | El documento de retiro que recorre cuatro áreas | `PazYSalvo` |
| **Hoja de vida** | El recorrido completo de una persona en la empresa | — |

**No se usa «evento» ni «seguimiento»** en la interfaz.

---

## 6 · Formación

| Término | Qué es | En código |
|---|---|---|
| **Divulgación** | La publicación de un documento que debe leerse y firmarse | `Divulgacion` |
| **Constancia** | La evidencia de que alguien leyó un documento | `ConstanciaLectura` |
| **Matriz de capacitación** | Qué documentos aplican a cada cargo | `MatrizCargo` |
| **Curso** | Secciones más evaluación. Deja certificado | `Curso` |
| **Sección** | Una parte de un curso | `Seccion` |
| **Certificado** | El resultado de aprobar un curso | `Certificado` |
| **Inducción** | El curso único para todo ingreso nuevo | — |
| **R-RH-009** | El registro de capacitación, con folio y firmas | — |

---

## 7 · Registros y firmas

| Término | Qué es | En código |
|---|---|---|
| **Registro** | Un formato de RH con folio y firmas, que se cierra y no se modifica | `Registro` |
| **Folio** | El consecutivo de un registro. **No se reinicia** | `folio` |
| **Formato** | La plantilla de un registro. Se versiona | `Formato` |
| **Firma** | El trazo que el colaborador dibuja una vez al ingresar | `Firma` |
| **Clave de firma** | La contraseña propia del colaborador que autoriza su uso | — |
| **Cierre** | El momento en que un registro se vuelve inmutable | — |

---

## 8 · Competencias

| Término | Qué es | En código |
|---|---|---|
| **Formato de competencias** | El R-RH-053, definido por cargo | `FormatoCompetencias` |
| **Grupo** | Una sección del formato con su peso porcentual | `GrupoCompetencia` |
| **Conducta** | Un ítem evaluable dentro de un grupo, de 1 a 5 | `Conducta` |
| **Evaluación** | Una aplicación del formato a una persona | `Evaluacion` |

---

## 9 · Sistema

| Término | Qué es | En código |
|---|---|---|
| **Parámetro** | Un valor configurable. Los legales llevan vigencia | `Parametro` |
| **Vigencia** | El período en que un valor rige. Un parámetro legal no se sobrescribe | `Vigencia` |
| **Permiso** | Una acción concreta sobre un módulo: `personal.salario.ver` | `Permiso` |
| **Rol** | Un conjunto de permisos. Lo define TI | `Rol` |
| **Bitácora** | El registro inmutable de todo lo que pasa | `RegistroAuditoria` |
| **Bandeja** | El lugar donde cada usuario ve lo que espera por él | — |
| **Compuerta** | Cada una de las seis verificaciones para cerrar una fase | — |
| **Fase** | Un bloque de trabajo que entrega algo usable | — |
| **Módulo** | Una app de Django con su dominio | — |

---

## 10 · Sistemas externos

| Término | Qué es |
|---|---|
| **SIRH** | El sistema antiguo, en Java 8 y JSP. Se apaga en la fase 22 |
| **SIRH+** | Este sistema |
| **BioTime** | El software del fabricante de los biométricos. Se integra en la fase 10 |
| **COPEC** | El aplicativo de divulgación de documentos. Se integra en la fase 14 |
| **SINERGY** | El sistema de nómina. Sin conexión: se le carga un archivo plano |
| **Daruma** | El gestor documental de calidad. Solo lectura a su base |
| **GLPI** | La mesa de ayuda. SIRH+ le crea usuarios por API |
| **Gestor de identidad** | El sistema central de identidad, en construcción |
| **Granservicios** | La empresa temporal. Unas 493 personas |

---

## 11 · Cómo se escribe

Reglas de redacción para la interfaz. El detalle está en `.claude/rules/03-sistema-de-diseno.md` §7.

| Regla | Mal | Bien |
|---|---|---|
| Decir qué hacer | «Campo inválido» | «El documento debe tener entre 6 y 11 dígitos» |
| Nombrar lo que pasó | «Operación exitosa» | «Se registró a Andrés Mora» |
| El verbo en el botón | «Aceptar» | «Anular el registro» |
| Sin jerga | «Error 500» | «No pudimos guardar. Intenta de nuevo o avisa a TI» |
| Sin admiraciones | «¡Listo!» | «Listo» |
| Segunda persona | «El usuario debe…» | «Necesitas…» |
| Cifras con separador | `1094` | `1.094` |
| Moneda sin decimales | `$ 2.340.000,00` | `$ 2.340.000` |

---

## Cómo se agrega un término

Cuando un módulo nuevo introduce un concepto, se agrega aquí **antes** de escribir el modelo. Si el término no está en el glosario, todavía no existe.
