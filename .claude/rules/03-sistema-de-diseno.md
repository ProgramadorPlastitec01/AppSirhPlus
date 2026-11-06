# SIRH+ — Sistema de diseño

**Plastitec S.A.S. · Tecnología de Información**
Versión 1.0 · 5 de noviembre de 2026
**Documento normativo. Reemplaza íntegramente a `.claude/rules/03-frontend-ux.md`.**

---

# 0 · Cómo se usa este documento

## 0.1 La regla que lo gobierna todo

> **Ningún valor visual se escribe a mano fuera de `:root`.**

Ni un color, ni un radio, ni una sombra, ni un espaciado, ni un tamaño de letra. Si lo que necesitas no está en los tokens, la respuesta no es escribir el valor: es discutir si falta un token.

Esa regla es la que hace que un sistema de 28 módulos construido durante años se vea como una sola cosa. Sin ella, para el módulo doce ya habrá cuatro azules distintos y nadie sabrá cuál es el correcto.

## 0.2 Las tres caras del sistema

SIRH+ es una sola aplicación con tres audiencias. Comparten tokens, tipografía y componentes; cambian el shell y la densidad.

| Cara | Quién | Shell | Densidad | Plantilla |
|---|---|---|---|---|
| **Pública** | Cualquiera, sin sesión | Cabecera superior | Amplia | `base_publico.html` |
| **Colaborador** | 1.100 personas, entran dos minutos | Cabecera superior | Amplia | `base_portal.html` |
| **Gestión** | RH y jefes, trabajan ocho horas | Barra lateral | Compacta | `base.html` |

La diferencia no es estética. Alguien que entra dos minutos al mes necesita respirar y que todo esté evidente; alguien que pasa la jornada dentro necesita ver más en menos espacio y no perder tiempo en movimientos.

## 0.3 Qué se hereda del estándar y qué no

| Del estándar | Estado |
|---|---|
| Tokens en `:root`, sin valores sueltos | Se conserva |
| CSS plano y JavaScript vanilla, sin build | Se conserva |
| Recursos auto-hospedados, sin CDN | Se conserva |
| Los cuatro estados en cada pantalla | Se conserva y se amplía |
| Una sola hoja de estilos | Se conserva |
| **Sidebar de 220 px para toda pantalla con sesión** | **Desviación D1** — justificada en `docs/diseno.md` §8 |

---

# 1 · Fundamentos

## 1.1 Color

### La paleta y su porqué

El azul marca `#16163A` es casi negro con temperatura. Sostiene la barra lateral y los bloques de énfasis sin competir con el contenido.

El índigo `#4F46E5` es la acción: lo que se puede pulsar, lo que está activo, lo que el sistema propone.

El dorado `#D9B06A` es el acento de la marca. **No es un color de estado.** Marca la pestaña activa, la etiqueta de sección y el borde de una cita. Nunca significa «cuidado» por sí solo.

### Tokens

```css
:root {
  color-scheme: light;

  /* ——— Marca ——— */
  --marca:        #16163A;   /* barra lateral, bloques de énfasis */
  --marca-2:      #1E1E4A;   /* superficie sobre marca */
  --marca-3:      #2E2E5E;   /* elemento activo sobre marca */
  --marca-linea:  #3A3A72;   /* separador sobre marca */
  --marca-txt:    #FFFFFF;
  --marca-txt-2:  #C3C5E8;
  --marca-txt-3:  #8A8CBE;

  /* ——— Acción ——— */
  --accion:       #4F46E5;
  --accion-2:     #3730A3;   /* al pasar el cursor, y texto sobre claro */
  --accion-suave: #EEF0FE;   /* fondo de estado activo */
  --accion-borde: #B9BCF5;

  /* ——— Acento ——— */
  --acento:       #D9B06A;   /* solo sobre fondo oscuro */
  --acento-txt:   #7A4F00;   /* el mismo acento, legible sobre claro */
  --acento-suave: #FAF0DC;

  /* ——— Superficies ——— */
  --fondo:        #F5F5F8;
  --sup:          #FFFFFF;
  --sup-2:        #FBFBFD;   /* cabecera de tabla, fila alterna */
  --sup-3:        #F0F0F5;   /* elemento deshabilitado */
  --linea:        #E7E7EE;   /* separador interno */
  --linea-2:      #D7D8E2;   /* borde de control */

  /* ——— Texto ——— */
  --txt:          #14141F;   /* principal */
  --txt-2:        #4A4F5E;   /* secundario */
  --txt-3:        #6B7080;   /* etiqueta, ayuda */
  --txt-4:        #8A8FA3;   /* metadato, marca de agua */

  /* ——— Estados ——— */
  --ok:           #0B5A48;  --ok-s:   #E8F3EF;  --ok-b:   #A9D4C4;
  --aviso:        #7A4F00;  --aviso-s:#FAF0DC;  --aviso-b:#E6CD96;
  --error:        #A62E1A;  --error-s:#FBE9E5;  --error-b:#F0C4BA;
  --info:         #3730A3;  --info-s: #EEF0FE;  --info-b: #B9BCF5;

  /* ——— Datos ——— */
  --d1: #4F46E5;  --d2: #0B5A48;  --d3: #7A4F00;
  --d4: #A62E1A;  --d5: #2E2E5E;  --d6: #8A8FA3;
}
```

### Reglas de color

| Regla | Detalle |
|---|---|
| **El color nunca es la única señal** | Un estado lleva color, texto y, cuando aplica, icono o forma |
| **El dorado no es un estado** | Para «cuidado» va `--aviso` |
| **`--acento` solo sobre oscuro** | Sobre claro no alcanza contraste; ahí va `--acento-txt` |
| **Los colores de datos van en orden** | Primera serie `--d1`, segunda `--d2`. No se eligen por gusto |
| **Contraste mínimo 4.5:1 en texto** | 3:1 en texto de 18 px o mayor y en bordes de control |

### Qué significa cada estado

| Estado | Cuándo | Ejemplo real |
|---|---|---|
| `--ok` | Está como debe estar | Activo · al día · aprobado |
| `--aviso` | Requiere atención, no está roto | Próximo a vencer · datos incompletos · tope superado |
| `--error` | Está mal o bloquea | Sin código de nómina · acceso denegado · vencido |
| `--info` | El sistema informa o propone | Por validar · sugerencia · explicación |

## 1.2 Tipografía

**Archivo** para títulos y cifras. **Inter** para todo lo demás. Ambas auto-hospedadas en `static/vendor/`.

```css
:root {
  --disp: 'Archivo', system-ui, -apple-system, 'Segoe UI', sans-serif;
  --sans: 'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
  --mono: ui-monospace, 'SF Mono', SFMono-Regular, Consolas, monospace;

  --t-xs:   11px;   --lh-xs:   1.45;
  --t-sm:   12.5px; --lh-sm:   1.5;
  --t-base: 13.5px; --lh-base: 1.55;   /* texto de gestión */
  --t-md:   15px;   --lh-md:   1.6;    /* texto de portal */
  --t-lg:   17px;   --lh-lg:   1.4;
  --t-xl:   20px;   --lh-xl:   1.25;
  --t-2xl:  25px;   --lh-2xl:  1.15;
  --t-3xl:  32px;   --lh-3xl:  1.1;
  --t-4xl:  42px;   --lh-4xl:  1.05;

  --p-400: 400; --p-500: 500; --p-600: 600; --p-700: 700; --p-800: 800;
  --ls-t: -0.025em;   /* títulos */
  --ls-e: 0.1em;      /* etiqueta en versalitas */
}
```

### Escala por rol

| Rol | Familia | Tamaño | Peso | Tracking |
|---|---|---|---|---|
| Título de pantalla | Archivo | `--t-xl` | 700 | `--ls-t` |
| Título de persona | Archivo | `--t-2xl` | 700 | `--ls-t` |
| Título de sección | Archivo | `--t-lg` | 700 | `--ls-t` |
| Cifra destacada | Archivo | `--t-3xl` | 700 | `-0.035em` |
| Texto de gestión | Inter | `--t-base` | 400 | — |
| Texto de portal | Inter | `--t-md` | 400 | — |
| Etiqueta de campo | Inter | `--t-sm` | 600 | — |
| Ayuda bajo campo | Inter | `--t-xs` | 400 | — |
| Encabezado de tabla | Inter | `--t-xs` | 700 | `0.05em`, versalitas |
| Etiqueta de sección | Inter | `--t-xs` | 700 | `--ls-e`, versalitas |
| Código técnico | Mono | `--t-sm` | 400 | — |

### Reglas tipográficas

- **Toda cifra lleva `font-variant-numeric: tabular-nums`.** Sin excepción: montos, horas, documentos, códigos, conteos, fechas. Una columna de números que baila es ilegible.
- **Máximo 75 caracteres por línea** en texto corrido.
- **No se usa cursiva** para énfasis. Se usa peso.
- **Ni mayúsculas sostenidas** fuera de las etiquetas en versalitas, que llevan su tracking.
- **Puntuación tipográfica** en todo texto visible: `’` para el apóstrofo, `«»` o `“”` según corresponda. Las comillas rectas quedan para el código.

## 1.3 Espacio

Escala de 4 px. Nada entre medias.

```css
:root {
  --e0: 0;     --e1: 4px;   --e2: 8px;   --e3: 12px;
  --e4: 16px;  --e5: 20px;  --e6: 24px;  --e8: 32px;
  --e10: 40px; --e12: 48px; --e16: 64px;
}
```

| Relación | Gestión | Portal |
|---|---|---|
| Etiqueta a su campo | `--e2` | `--e2` |
| Entre campos de un grupo | `--e4` | `--e5` |
| Entre secciones de un formulario | `--e5` | `--e6` |
| Entre tarjetas | `--e4` | `--e5` |
| Relleno de tarjeta | `--e5` | `--e6` |
| Relleno de la zona de contenido | `--e6` lateral `--e8` | `--e8` |

**El espacio es una señal de jerarquía.** Lo que está junto se lee junto. Un campo separado de su etiqueta por `--e4` ya parece de otro grupo.

## 1.4 Forma, sombra y borde

```css
:root {
  --r-xs: 5px;    /* código en línea, etiqueta pequeña */
  --r-sm: 8px;    /* icono, botón secundario pequeño */
  --r:    9px;    /* control, botón, campo */
  --r-md: 11px;   /* contenedor pequeño, aviso */
  --r-lg: 14px;   /* tarjeta, panel */
  --r-xl: 16px;   /* ventana modal */
  --r-full: 999px;/* píldora, punto */

  --s-0: none;
  --s-1: 0 1px 2px rgba(20,21,25,.04), 0 2px 6px rgba(20,21,25,.05);
  --s-2: 0 2px 4px rgba(20,21,25,.05), 0 6px 16px rgba(20,21,25,.07);
  --s-3: 0 8px 24px rgba(20,21,25,.10), 0 24px 56px rgba(20,21,25,.14);
}
```

| Elevación | Sombra | Dónde |
|---|---|---|
| Plana | `--s-0` | Dentro de otra tarjeta, fila de tabla |
| Base | `--s-1` | Tarjeta, panel |
| Flotante | `--s-2` | Menú desplegable, sugerencias |
| Modal | `--s-3` | Ventana modal, confirmación |

**La sombra nunca reemplaza al borde.** Toda tarjeta lleva `1px solid var(--linea)` además de su sombra: el borde es lo que la define cuando la sombra no se percibe.

Un elemento seleccionado se marca con **borde de 2 px en `--accion`**, no con una sombra más fuerte.

## 1.5 Movimiento

```css
:root {
  --m-rapido: 120ms;
  --m-base:   180ms;
  --m-lento:  260ms;
  --m-curva:  cubic-bezier(.2,.7,.3,1);
}
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: .01ms !important;
    transition-duration: .01ms !important;
  }
}
```

| Qué | Duración | Qué se anima |
|---|---|---|
| Cursor sobre un control | `--m-rapido` | `background`, `border-color`, `color` |
| Apertura de panel o acordeón | `--m-base` | `opacity`, `transform` |
| Apertura de modal | `--m-lento` | `opacity`, `transform: translateY(12px)` |
| Entrada de fila nueva | `--m-base` | `opacity`, `transform` |

**Nunca se anima `width`, `height`, `top` ni `left`.** Solo `opacity` y `transform`, que no provocan reflujo.

**Nada se mueve sin que el usuario lo haya provocado.** Ningún carrusel, ninguna animación en bucle, ningún elemento que entre por sí solo. En un sistema donde la gente trabaja ocho horas, el movimiento gratuito cansa.

## 1.6 Iconografía

Un solo juego, dibujado en línea como SVG. Trazo `1.8` en 17 px, `2` en 15 px o menos, `1.9` en 20 px o más.

| Regla | Detalle |
|---|---|
| `stroke="currentColor"` siempre | Hereda el color del contexto |
| `fill="none"` siempre | Son iconos de línea, no sólidos |
| `aria-hidden="true"` siempre | Son decorativos; el significado va en el texto |
| `viewBox="0 0 24 24"` siempre | Para que el trazo sea consistente |
| **Nunca un icono solo** sin texto ni `aria-label` | Un icono sin nombre no se entiende igual para todos |

## 1.7 Enfoque

```css
:where(a, button, input, select, textarea, [tabindex]):focus-visible {
  outline: 2px solid var(--accion);
  outline-offset: 2px;
  border-radius: var(--r-sm);
}
```

**Nunca `outline: none` sin reemplazo.** Quien navega con teclado necesita ver dónde está. Sobre fondo oscuro el anillo va en `--acento`.

---

# 2 · Los shells

## 2.1 Shell de gestión — `base.html`

```
┌──────────────┬────────────────────────────────────────────┐
│              │  migas                            buscar   │
│   244 px     │  Título                         [acción]   │
│   lateral    ├────────────────────────────────────────────┤
│   --marca    │                                            │
│              │  contenido                                 │
│              │  máx 1180 px, relleno --e6 / --e8          │
└──────────────┴────────────────────────────────────────────┘
```

**Barra lateral: 244 px, fondo `--marca`.**

| Zona | Contenido |
|---|---|
| Arriba | Logotipo, nombre y la palabra «Gestión» |
| Grupos | Etiqueta en versalitas, luego los enlaces |
| Enlace activo | Fondo `--marca-3`, texto blanco, peso 600, **barra de 3 px en `--acento` al borde izquierdo** |
| Abajo | Usuario, su rol y el botón de salir |

**Cabecera: 1 px de línea, fondo `--sup`.**
Migas en `--t-sm` sobre el título. La acción principal a la derecha, una sola. Las demás son secundarias.

**Los grupos de la lateral son dos, siempre:** Operación y Administración. Administración solo aparece para quien tiene permisos de ese grupo.

## 2.2 Shell de portal — `base_portal.html`

Cabecera superior, fondo `--marca`, con pestañas. La activa lleva texto blanco y **subrayado de 3 px en `--acento`**.

A la derecha: nombre del colaborador, temporizador de sesión visible y botón de salir, siempre presente.

**El temporizador de sesión se muestra.** Viene del mockup del portal y es una buena decisión: quien va a radicar unas vacaciones necesita saber cuánto tiempo le queda.

## 2.3 Shell público — `base_publico.html`

El mismo de portal, sin datos de usuario y con un botón de acceso. Lo que se ve aquí es solo: noticias, organigrama, convocatorias y el espacio del Fondo de Empleados.

## 2.4 Shell de ingreso — `base_auth.html`

**Hereda de `base_publico.html`**, con el contenido centrado y sin navegación. El ingreso no tiene shell propio: es la puerta de entrada de las tres caras, no una cuarta cara.

Su referencia visual es `mockups/mockup-portal/Login.dc.html`.

## 2.5 Ancho y rejilla

| Contexto | Ancho máximo |
|---|---|
| Contenido de gestión | 1.180 px |
| Contenido de portal | 1.080 px |
| Formulario de una columna | 680 px |
| Texto corrido | 75 caracteres |

La rejilla es flexbox o grid, en fracciones. **Nunca anchos fijos en píxeles para el contenido.**

## 2.6 Adaptación

Tres puntos de quiebre, y solo tres:

```css
/* ≥ 1100px  — base, sin consulta */
@media (max-width: 1100px) { /* la lateral se colapsa a iconos */ }
@media (max-width: 760px)  { /* una columna; la lateral pasa a cajón */ }
@media (max-width: 480px)  { /* ajustes de relleno y tamaño */ }
```

| Qué | Cómo se adapta |
|---|---|
| Rejillas de 3 y 4 | A 2 bajo 900 px, a 1 bajo 620 px |
| Tabla ancha | Scroll horizontal **dentro de su contenedor**, nunca en el cuerpo |
| Barra lateral | Iconos bajo 1100 px, cajón bajo 760 px |
| Objetivo táctil | Mínimo 44 × 44 px en todo lo pulsable |

La cara de gestión **se diseña para escritorio** y se adapta para no romperse. La cara de colaborador **se diseña para teléfono** y crece.

---

# 3 · Componentes

Todos viven en `templates/macros.html` y se invocan desde las plantillas. **Ningún módulo escribe su propio botón.**

## 3.1 Botón

| Variante | Fondo | Borde | Texto | Cuándo |
|---|---|---|---|---|
| `primario` | `--accion` | — | blanco | La acción principal. **Una por pantalla** |
| `secundario` | `--sup` | `--linea-2` | `--txt-2` | Acciones de apoyo |
| `oscuro` | `--marca` | — | blanco | Aplicar un filtro, confirmar un paso |
| `sutil` | transparente | — | `--accion` | Acción terciaria dentro de una tarjeta |
| `peligro` | `--error-s` | `--error-b` | `--error` | Borrar, anular, revocar |

Altura mínima 44 px. Relleno `0 var(--e4)`. Radio `--r`. Peso 600.

Un botón con icono lleva `--e2` de separación y el icono a 16 px.

## 3.2 Campo de formulario

```html
<div class="campo">
  <label class="campo__etiqueta" for="x">Etiqueta</label>
  <input class="campo__control" id="x" type="text">
  <p class="campo__ayuda">Qué se espera aquí.</p>
  <p class="campo__error" role="alert">Qué está mal y cómo se arregla.</p>
</div>
```

| Estado | Señal |
|---|---|
| Normal | Borde `--linea-2` |
| Con foco | Anillo `--accion` de 2 px |
| Con error | Borde `--error-b`, mensaje en `--error` con `role="alert"` |
| Solo lectura | Fondo `--sup-3`, texto `--txt-3`, con ayuda que diga por qué |
| Deshabilitado | Opacidad 0.5 y `aria-disabled` |

**Reglas:**
- Toda etiqueta tiene su `for`. Un `placeholder` **no es** una etiqueta.
- El mensaje de error dice **qué hacer**, no «campo inválido».
- Un campo de solo lectura explica por qué lo es: «lo genera el sistema», «viene de SINERGY».
- Un campo opcional se marca «(opcional)». No se marcan los obligatorios: son la mayoría.

## 3.3 Tarjeta

Fondo `--sup`, borde `--linea`, radio `--r-lg`, sombra `--s-1`, relleno `--e5`.

Variantes: `destacada` (borde 2 px en `--accion`), `oscura` (fondo `--marca`), `discreta` (sin sombra, fondo `--sup-2`).

## 3.4 Tarjeta de cifra

```
┌──────────────────────┐
│ Etiqueta             │   --t-sm, --txt-3, peso 600
│ 1.094                │   Archivo, --t-3xl, peso 700
│ 601 directos · 493…  │   --t-xs, --txt-2
│ FUENTE: SIRH+        │   --t-xs, --txt-4, versalitas
└──────────────────────┘
```

**La línea de fuente es obligatoria** en toda cifra que no nazca en SIRH+. Ver §4.1.

## 3.5 Etiqueta de estado

Píldora: `--r-full`, relleno `3px var(--e2)`, `--t-xs`, peso 700.

```html
{{ badge("Activo", "ok") }}
{{ badge("Próximo a vencer", "aviso") }}
{{ badge("Sin código de nómina", "error") }}
{{ badge("Por validar", "info") }}
{{ badge("Directo", "neutro") }}
```

**El texto de la etiqueta dice el estado, no lo insinúa.** «Sin código de nómina», no «Incompleto».

## 3.6 Tabla

| Parte | Regla |
|---|---|
| Encabezado | `--t-xs`, peso 700, versalitas, `--txt-3`, línea `--linea-2` abajo |
| Celda | `--e3 var(--e4)`, `--t-base`, línea `--linea` abajo |
| Fila al pasar el cursor | Fondo `--sup-2` |
| Cifras | Alineadas a la derecha, con `tabular-nums` |
| Acciones | Última columna, alineada a la derecha |
| Ancho | `min-width` y scroll dentro de un contenedor con `overflow-x: auto` |

**Obligatorio:** `<caption>` visualmente oculto y `scope="col"` en cada `<th>`.

**Nunca más de 8 columnas visibles.** Si hacen falta más, se usa el selector de columnas y la vista de detalle.

## 3.7 Ventana modal

```html
<div role="dialog" aria-modal="true" aria-labelledby="t">
  <header>icono · título · descripción · cerrar</header>
  <div>contenido</div>
  <footer>cancelar ··· confirmar</footer>
</div>
```

| Regla | Detalle |
|---|---|
| Ancho máximo 620 px; 760 px si lleva formulario de dos columnas |
| El foco entra al abrir y **vuelve al disparador** al cerrar |
| El foco queda atrapado dentro mientras está abierta |
| `Esc` cierra, salvo si hay cambios sin guardar: entonces pregunta |
| Cancelar a la izquierda, confirmar a la derecha |
| **Nunca un modal dentro de otro** |

**Los formularios van en modal** en la cara de gestión. Es el patrón del sistema y no se alterna con páginas aparte.

## 3.8 Confirmación destructiva

Modal con icono en `--error`, el nombre exacto de lo que se va a afectar, y **el conteo de lo que arrastra**: «Esto afecta a 94 personas». El botón de confirmar es `peligro` y dice el verbo: «Anular el registro», no «Aceptar».

## 3.9 Aviso en línea

Franja con fondo `--*-s`, radio `--r-md`, icono a la izquierda, texto en el color del estado. Lleva `role="status"`, o `role="alert"` si es un error.

**No se usa para felicitar.** Un aviso interrumpe la lectura; se reserva para lo que cambia lo que la persona va a hacer.

## 3.10 Estado vacío

```
       ⬡          icono en caja de 52 px, fondo --sup-3
  Título          Archivo, --t-lg, 700
  Explicación     --t-base, --txt-3, máx 44ch
  [Acción]        si hay algo que hacer
```

**Un estado vacío nunca dice solo «No hay datos».** Dice por qué está vacío y qué se puede hacer.

## 3.11 Ayuda contextual

Un botón con signo de interrogación junto al título de cada módulo. Abre un modal con tres bloques fijos:

1. **Para qué sirve este módulo** — dos o tres frases
2. **Qué tener en cuenta** — las reglas que no son obvias
3. **Qué hacer si algo sale mal** — a quién acudir

El contenido vive en `templates/ayuda/<modulo>.html`. **Un módulo sin ayuda contextual no pasa la compuerta 5.**

## 3.12 Migas

`--t-sm`, `--txt-3`, separador `›`. El último elemento no es enlace. Dentro de `<nav aria-label="Ruta">`.

## 3.13 Paginación

Botones de 36 px mínimo, el actual con `aria-current="page"`. A la izquierda, el conteo: «Mostrando 1–9 de 1.094».

## 3.14 Filtros

Tres partes, en este orden:

1. **Buscador libre** — ocupa el espacio flexible
2. **Selectores** — anchos fijos, los más usados primero
3. **Atajos** — píldoras con el conteo: «Sin código de nómina · 31»

Los atajos son filtros guardados que resuelven la pregunta real que la gente tiene. Valen más que diez selectores.

## 3.15 Línea de tiempo

Columna de 34 px con el indicador y la línea vertical, luego el contenido. Cada hito lleva: tipo con su color, título, detalle, fecha a la derecha y quién lo registró.

Es el componente de la hoja de vida y el de la bitácora de auditoría.

## 3.16 Catálogo completo

| Componente | Macro |
|---|---|
| Icono | `icon(nombre, tam)` |
| Botón | `btn(texto, variante, icono, href)` |
| Campo | `field(tipo, nombre, etiqueta, ayuda, error)` |
| Selector | `select(nombre, etiqueta, opciones)` |
| Tarjeta | `card(variante)` |
| Tarjeta de cifra | `kpi(etiqueta, valor, detalle, fuente)` |
| Etiqueta de estado | `badge(texto, estado)` |
| Tabla | `tabla(columnas, filas, caption)` |
| Modal | `modal(id, titulo, descripcion)` |
| Confirmación | `confirmar(titulo, objeto, impacto, verbo)` |
| Aviso | `alert(texto, estado)` |
| Estado vacío | `empty_state(titulo, texto, accion)` |
| Ayuda | `ayuda(modulo)` |
| Migas | `migas(ruta)` |
| Paginación | `paginacion(pagina, total)` |
| Filtros | `filtros(buscador, selectores, atajos)` |
| Línea de tiempo | `timeline(hitos)` |
| Avatar | `avatar(iniciales, tono, tam)` |
| Pestañas | `tabs(items, activa)` |
| Interruptor | `switch(nombre, activo, etiqueta)` |
| Pasos | `pasos(lista, actual)` |

---

# 4 · Patrones propios de SIRH+

Estos son los que distinguen a este sistema. No vienen de ninguna librería.

## 4.1 Cada dato dice de dónde viene

**Todo dato que no nace en SIRH+ muestra su origen y su fecha de corte.**

```
Salario                    $ 2.340.000
FUENTE: SINERGY · corte 31/10/2026
```

Viene del mockup del portal, donde una cifra decía «Fuente: BITIOME». Es la respuesta a la pregunta que la gente siempre hace frente a un número que no cuadra: ¿de dónde salió esto?

| Origen | Etiqueta |
|---|---|
| Propio | `SIRH+` |
| Nómina | `SINERGY · corte DD/MM/AAAA` |
| Documental | `DARUMA` |
| Inventario | `MANT` |
| Identidad | `GESTOR DE IDENTIDAD` |

En una pantalla con muchos datos de un mismo origen, basta con un bloque que lo diga una vez.

## 4.2 El dato sensible se anuncia

Cuando alguien ve un dato reservado, el sistema le dice por qué lo está viendo:

> Ves esta sección porque tu rol incluye `personal.salario.ver`. Cada consulta queda en la bitácora.

Fondo `--aviso-s`, texto `--aviso`, `--t-xs`.

**No es una advertencia: es una cortesía y un recordatorio.** Quien sabe que su consulta queda registrada consulta con criterio.

Y la regla técnica detrás: **si no tiene el permiso, el dato no llega al navegador.** No se oculta con CSS.

## 4.3 La acción muestra su impacto antes de ejecutarse

Antes de confirmar algo que arrastra consecuencias, el sistema las enumera:

> **Qué cambia si mueves este cargo**
> - 94 personas cambian de aprobador de permisos y vacaciones
> - 94 personas cambian de evaluador de competencias
> - Las horas extra pasan a aprobarse por el nuevo superior
>
> Las solicitudes ya radicadas conservan su aprobador.

Aplica a: mover un cargo en la estructura, cambiar un permiso de un rol, cerrar un período, anular un registro con folio, aprobar horas extra por encima del tope.

## 4.4 La vigencia es visible

Todo lo que se versiona por fecha lo muestra:

```
42 h   Desde el 16 de julio de 2025 · vigente     [Vigente]
44 h   Del 16/07/2024 al 15/07/2025               [Histórico]
```

La vigente lleva barra en `--ok`; las históricas en `--linea-2`, con texto `--txt-3`.

Aplica a parámetros legales, estructura del organigrama, formatos de competencias, cargo de una persona, datos reservados.

## 4.5 El pendiente tiene dueño, plazo y consecuencia

Una fila de bandeja lleva siempre cuatro cosas:

```
▌ Completar datos reservados — Andrés Mora        [Bloquea nómina]  hace 2 d
  Registrado hace 2 días · falta salario, EPS y caja
```

Barra de color según urgencia · qué es · qué falta · **qué pasa si no se hace** · desde cuándo.

La etiqueta de consecuencia es lo que convierte una lista en una prioridad.

## 4.6 El estado incompleto es un estado, no un error

Una persona registrada sin datos reservados no está mal: está a medias, y eso es correcto en el flujo. Se muestra en `--aviso`, no en `--error`, y con una explicación de qué falta y a quién le toca.

`--error` se reserva para lo que **bloquea** algo: sin código de nómina, cargo sin superior, acceso denegado.

## 4.7 La ayuda está donde surge la duda

Tres niveles:

1. **Ayuda bajo el campo** — qué se espera ahí
2. **Nota al pie de sección** — la regla que no es obvia
3. **Modal de ayuda del módulo** — cómo funciona todo

Nunca un manual aparte como única fuente. El manual en PDF existe, pero la ayuda vive dentro.

## 4.8 Los cuatro estados, siempre

| Estado | Qué se muestra |
|---|---|
| **Con datos** | Lo normal |
| **Vacío** | Por qué está vacío y qué hacer |
| **Error** | Qué falló, en lenguaje del usuario, y cómo reintentar |
| **Cargando** | Esqueleto con la forma del contenido, nunca un giro genérico |

**Una pantalla sin los cuatro no pasa la compuerta 5.**

El esqueleto respeta la forma real: si van a llegar nueve filas, se muestran nueve barras de la altura de una fila.

---

# 5 · Arquetipos de pantalla

Cinco formas. Toda pantalla del sistema es una de ellas.

## 5.1 Listado

`migas → título → acción principal → filtros → tabla → paginación`

Reglas: atajos antes que selectores · máximo 8 columnas · cada fila lleva a su detalle · la exportación respeta los permisos de cada columna.

## 5.2 Detalle

`migas → cabecera de la entidad → pestañas → contenido + columna lateral`

La cabecera lleva: avatar, nombre, estado, datos clave en fila e identificadores. Las acciones a la derecha, la principal en `oscuro`.

La columna lateral es para lo que se consulta, no para lo que se edita.

## 5.3 Formulario por pasos

`pasos → secciones en tarjetas → acciones al pie`

Cada paso es una unidad que se guarda sola. El indicador muestra quién hace cada paso cuando son personas distintas. La columna lateral explica qué pasa al guardar.

## 5.4 Editor

`cabecera → lienzo → panel de propiedades → acciones`

Para estructura, formatos de competencias, constructor de encuestas y programación de turnos. El panel muestra el impacto antes de guardar (§4.3).

## 5.5 Panel

`cifras → bandeja → columna de vencimientos y estado`

Las cifras arriba, la bandeja de pendientes como contenido principal, lo informativo a la derecha. **Un panel no es un muro de gráficas:** es lo que hay que hacer hoy.

---

# 6 · Accesibilidad

No es una capa final. Es parte de la compuerta 5.

| Requisito | Verificación |
|---|---|
| Contraste 4.5:1 en texto, 3:1 en bordes | Medido, no estimado |
| Todo control alcanzable con teclado, en orden lógico | Se recorre con tabulador |
| Anillo de foco visible en todo control | Nunca `outline: none` sin reemplazo |
| Toda imagen y todo icono con significado, con texto | `alt` o `aria-label` |
| Toda etiqueta con su `for` | Verificado |
| Todo error con `role="alert"` | Verificado |
| Modal con foco atrapado y devuelto | Probado |
| Tabla con `<caption>` y `scope` | Verificado |
| Color nunca como única señal | Revisado en escala de grises |
| Objetivo táctil de 44 px | Medido |
| Jerarquía de encabezados sin saltos | Un `h1` por pantalla |
| `prefers-reduced-motion` respetado | Probado |

**Prueba rápida de la compuerta 5:** recorrer la pantalla completa con el tabulador, sin tocar el ratón, y poder hacer todo lo que la pantalla permite.

---

# 7 · Reglas de escritura

El texto es parte del diseño. Las mismas reglas de voz del resto del proyecto.

| Regla | Mal | Bien |
|---|---|---|
| Decir qué hacer, no qué pasó | «Campo inválido» | «El documento debe tener entre 6 y 11 dígitos» |
| Nombrar lo que ocurre | «Operación exitosa» | «Se registró a Andrés Mora» |
| El verbo en el botón | «Aceptar» | «Anular el registro» |
| Sin jerga técnica | «Error 500» | «No pudimos guardar. Intenta de nuevo o avisa a TI» |
| Sin signos de admiración | «¡Listo!» | «Listo» |
| Segunda persona, sin usted | «El usuario debe…» | «Necesitas…» |
| Fechas en palabras cuando hay espacio | `05/11/2026` | `5 de noviembre de 2026` |
| Cifras con separador de miles | `1094` | `1.094` |
| Moneda sin decimales | `$ 2.340.000,00` | `$ 2.340.000` |

**El vocabulario del §1.5 del plan de ejecución es obligatorio.** Si la interfaz dice «eventualidad», el código dice `Eventualidad`.

---

# 8 · Qué está prohibido

| Prohibido | Por qué |
|---|---|
| Un valor de color, radio, sombra o espacio fuera de `:root` | Es cómo un sistema se desintegra |
| Una librería de JavaScript de terceros | Regla del estándar |
| Un recurso desde CDN | Regla del estándar |
| Un build de frontend | Regla del estándar |
| Un componente propio de un módulo que duplique uno existente | Divergencia garantizada |
| `outline: none` sin reemplazo | Deja a la gente sin saber dónde está |
| Un icono solo, sin texto ni `aria-label` | No se entiende igual para todos |
| Animar `width`, `height`, `top` o `left` | Provoca reflujo |
| Movimiento no provocado por el usuario | Cansa en ocho horas |
| Un modal dentro de otro | No hay forma de salir con sentido |
| Más de una acción primaria por pantalla | Si todo es primario, nada lo es |
| Ocultar un dato sensible solo con CSS | No es protección |
| Scroll horizontal en el cuerpo de la página | Rompe la lectura |
| Un estado vacío que solo diga «No hay datos» | Deja a la persona sin salida |
| Una pantalla sin sus cuatro estados | No pasa la compuerta 5 |
| Una pantalla de módulo sin ayuda contextual | No pasa la compuerta 5 |

---

# 9 · Cómo se verifica la compuerta 5

Lista que se recorre pantalla por pantalla. Las doce.

| # | Verificación |
|---|---|
| 1 | Coincide con su artboard en estructura, no necesariamente píxel a píxel |
| 2 | Ningún valor visual fuera de los tokens |
| 3 | Los cuatro estados existen y se ven bien |
| 4 | Se recorre completa con el tabulador |
| 5 | El anillo de foco es visible en todo control |
| 6 | Contraste medido en texto y bordes |
| 7 | En escala de grises se entiende todo |
| 8 | Funciona a 1100, 760 y 480 px |
| 9 | Ninguna tabla desborda el cuerpo |
| 10 | Toda cifra lleva `tabular-nums` |
| 11 | Todo dato ajeno muestra su origen |
| 12 | El módulo tiene su ayuda contextual |

---

# 10 · Decisiones de este sistema y su porqué

Para que la próxima persona entienda, y para que no se reabran sin motivo.

| Decisión | Por qué |
|---|---|
| **Barra lateral en gestión, cabecera en portal** | Son dos audiencias: ocho horas contra dos minutos |
| **Densidad distinta por cara** | Misma razón. Los tokens son los mismos; el relleno cambia |
| **El dorado no es un estado** | Es la marca. Mezclarlo con «cuidado» rompe ambas lecturas |
| **Formularios en modal en gestión** | Mantiene el contexto del listado. Alternar con páginas aparte desorienta |
| **Cada dato dice su origen** | Viene del mockup y responde la pregunta real de la gente |
| **El dato sensible se anuncia** | Quien sabe que queda registrado consulta con criterio |
| **El impacto antes de confirmar** | En un sistema que enruta aprobaciones, mover un cargo afecta a cientos |
| **Incompleto es `--aviso`, no `--error`** | Es un estado válido del flujo, no una falla |
| **Esqueleto en vez de giro genérico** | Reduce el salto visual cuando el contenido llega |
| **Nada se mueve solo** | El movimiento gratuito cansa en una jornada |
| **Un solo juego de iconos, en línea** | Sin CDN, sin build, y heredan el color |
| **La ayuda vive dentro de la aplicación** | Un manual aparte no se lee en el momento de la duda |
