# 06 — Lecciones

Cosas que costaron tiempo real. Cada entrada existe para que no vuelvan a costarlo.

**Formato:** qué pasó · qué lo causó · qué se hace ahora.

---

### L1 — Comparar el campo candidato contra el que reemplaza, no contra un tercero

Se evaluó si un campo podía sustituir a otro comparándolo con un **tercer** campo relacionado. Resultaron iguales, y se concluyó que era una copia redundante. La comparación correcta —el campo candidato contra el que efectivamente reemplaza, en la misma fila— dio el resultado opuesto, y esa fue la que se implementó.

**Ahora:** al evaluar un dato de reemplazo, se compara **exactamente contra el campo que va a reemplazar**, fila por fila.

---

### L2 — Verificar índices antes de unir tablas históricas

Una consulta que unía tres tablas históricas tardaba más de dos minutos: la más grande (~4M filas) no tenía índice en la columna de filtro.

**Ahora:** antes de consultar una tabla histórica grande, se verifica su tamaño y sus índices. Si no hay índice, se elige **una sola tabla según el criterio del negocio** en vez de unirlas.

---

### L3 — Los límites del driver no aparecen en pruebas pequeñas

Una consulta con `IN (?, ?, …)` funcionaba perfecto en desarrollo y devolvía error 500 en producción con rangos amplios: el driver ODBC corta cerca de 2.100 parámetros.

**Ahora:** toda consulta con lista de parámetros variable se trocea en lotes desde el primer día, no cuando falla. Ver 04 §3.

---

### L4 — Un patrón de datos no se asume: se verifica con una muestra real

Varias decisiones tuvieron que revertirse por haberse basado en un diagnóstico anterior o en una muestra pequeña, en vez de verificar contra datos reales en el momento.

**Ahora:** antes de aceptar o descartar una regla sobre los datos, se verifica con una muestra real. La memoria de un diagnóstico previo no cuenta como evidencia.

---

### L5 — Un dato de infraestructura no escrito cuesta un día cada vez

Conectar a SQL Server 2012 desde Rocky Linux 9 requiere una configuración específica de OpenSSL, declarada como variable de entorno en la unit de systemd. Sin ella la app **arranca sin error** y falla al conectar a la base — un síntoma que no señala la causa.

**Ahora:** toda particularidad del servidor se documenta en el repo, junto al archivo de despliegue que la necesita.

---

### L6 — Documentar también lo que NO funcionó

Un intento de resolver el token CSRF por una vía razonable fallaba por una colisión de nombres nada obvia. Quedó escrito en el módulo, con el error exacto.

**Ahora:** cuando un intento razonable falla por un motivo no evidente, se deja escrito en el docstring del módulo. Sin eso, la siguiente persona —o el siguiente agente— lo intenta de nuevo.

---

### L7 — Una afirmación en la documentación que el código contradice desinforma a los agentes

El `CLAUDE.md` de una app afirmaba dos veces que cierto paquete solo lo usaban unos comandos de importación. Dos módulos del camino normal lo importaban. La *intención* se cumplía, pero la afirmación literal era falsa — y un agente que la lea podría borrar ese paquete.

**Ahora:** las afirmaciones absolutas ("solo", "nunca", "ya no se usa") se verifican contra el código antes de escribirlas, y se revisan cuando el código cambia.
