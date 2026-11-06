---
paths:
  - "cuentas/**"
  - "config/settings.py"
  - "**/models.py"
  - "**/views.py"
  - ".env.example"
---

# 07 — Identidad y control de acceso

Toda app interna de Plastitec autentica contra **una sola base de datos maestra de identidad**, compartida por todas las aplicaciones. Ningún aplicativo define su propio maestro de usuarios.

Esto significa que una persona tiene **una credencial** para todas las apps internas, que darla de baja en un solo lugar la deja sin acceso a todo, y que el área de TI tiene un único sitio donde auditar quién entra a qué.

---

## 1. Las dos bases de cada app

| | Base de identidad | Base propia de la app |
|---|---|---|
| Nombre de la conexión | `identidad` | `default` |
| Motor hoy | MySQL | PostgreSQL |
| Motor previsto | PostgreSQL | PostgreSQL |
| Qué guarda | Usuarios, aplicaciones registradas, qué rol tiene cada usuario en cada app | Todo lo del dominio de la app |
| Quién la modela | **Una sola app, la propietaria** | Cada app, la suya |
| Quién corre sus migraciones | **Solo la propietaria** | Cada app, las suyas |

**La base de identidad no es "la base de la app".** Es un servicio compartido al que la app se conecta, igual que se conecta a un ERP: con su propio usuario, con permisos mínimos y sin asumir que puede cambiarle la estructura.

### La app propietaria

Exactamente **una** aplicación del parque declara `IDENTIDAD_ES_PROPIETARIA=True` en su `.env`. Solo esa corre `migrate` sobre la conexión `identidad`; en todas las demás el router lo bloquea.

Si dos aplicaciones se declaran propietarias, la segunda que migre puede alterar tablas que la primera ya está usando. El router impide el accidente, pero la decisión de quién es propietaria es administrativa y se escribe en el `CLAUDE.md` de esa app.

---

## 2. Modelo de datos

Tres tablas. Nada más.

```
usuario                 quién es la persona y cómo se autentica
aplicacion              catálogo de las apps internas
acceso_aplicacion       qué rol tiene cada usuario en cada aplicación
```

**El rol no vive en el usuario, vive en el cruce.** La misma persona puede administrar una app y solo consultar otra. Un usuario sin fila en `acceso_aplicacion` para una app **no entra a esa app**, aunque su credencial sea válida.

Los roles son dos y se llaman igual en todas partes:

| Rol | Puede |
|---|---|
| `consulta` | Ver y exportar |
| `administra` | Lo anterior, más crear, editar y configurar |

Si una app necesita un tercer rol, eso es una **desviación del estándar** y se declara con su justificación.

---

## 3. La restricción que no se puede violar

**Ningún modelo de la base `default` puede tener una llave foránea hacia `Usuario`.**

Django no cruza bases de datos en una llave foránea. Si se declara, las migraciones pasan y las consultas fallan en tiempo de ejecución con errores que no señalan la causa.

```python
# ❌ PROHIBIDO — Usuario vive en otra base
class Causacion(models.Model):
    revisado_por = models.ForeignKey("cuentas.Usuario", on_delete=models.PROTECT)

# ✅ Correcto — se guarda el identificador, sin relación declarada
class Causacion(models.Model):
    revisado_por_id = models.IntegerField(null=True, blank=True)
    revisado_por_usuario = models.CharField(max_length=150, blank=True)
```

Se guardan **las dos cosas**: el id para relacionar, y el nombre de usuario como texto para que el registro siga siendo legible aunque la persona se dé de baja. Un histórico que depende de una consulta a otra base para mostrar un nombre deja de ser un histórico.

Para mostrar nombres completos en una pantalla, `presentacion.py` resuelve los ids en una sola consulta a `identidad` y arma un diccionario. **Nunca una consulta por fila.**

### Por qué el usuario no usa el sistema de permisos de Django

`Usuario` hereda de `AbstractBaseUser`, **no** de `PermissionsMixin`, y la app no instala `django.contrib.admin`.

`Group` y `Permission` tienen relaciones muchos-a-muchos con el usuario. Con el usuario en otra base, esas tablas intermedias quedan rotas por el mismo motivo del punto anterior. El control de acceso se resuelve con `acceso_aplicacion`, que es explícito, cabe en una tabla y se audita leyéndola.

---

## 4. Portabilidad MySQL → PostgreSQL

La base de identidad hoy es MySQL y va a ser PostgreSQL. Estas cuatro reglas evitan que la migración rompa inicios de sesión.

**Sin SQL crudo sobre `identidad`.** Solo el ORM. Es la única capa que traduce sola entre los dos motores.

**Nombres de usuario y correos siempre en minúscula.** MySQL compara texto sin distinguir mayúsculas por defecto; PostgreSQL sí distingue. Una cuenta creada como `JPerez` entra hoy escribiendo `jperez` y **dejaría de entrar** después de migrar. El modelo normaliza a minúsculas al guardar, y la autenticación también normaliza lo que recibe.

**`max_length` explícito en todo campo indexado**, y nunca por encima de 191 caracteres si el campo lleva índice único. MySQL con `utf8mb4` limita el índice a 191 caracteres; PostgreSQL no tiene ese límite, pero respetarlo no cuesta nada y evita que la tabla no se pueda crear hoy.

**Sin tipos ni funciones propias de un motor.** Nada de `JSONField` con operadores específicos, nada de funciones SQL nativas. Los tipos que se usan son los que ambos motores tienen: entero, texto, booleano, fecha-hora.

---

## 5. Seguridad de la conexión

**Cada aplicación tiene su propio usuario de MySQL**, nunca uno compartido entre apps y nunca el administrador.

Permisos mínimos para una app **no propietaria**:

```sql
GRANT SELECT ON identidad.usuario            TO 'app_<nombre>'@'%';
GRANT SELECT ON identidad.aplicacion         TO 'app_<nombre>'@'%';
GRANT SELECT ON identidad.acceso_aplicacion  TO 'app_<nombre>'@'%';
-- El inicio de sesion actualiza la fecha; el cambio de clave, el hash
GRANT UPDATE (last_login, password) ON identidad.usuario TO 'app_<nombre>'@'%';
```

La app propietaria necesita además `INSERT`, `DELETE` y `ALTER` para administrar usuarios y correr migraciones.

**Las credenciales van en `.env`**, nunca en el código. Las variables están documentadas en `.env.example`.

**La contraseña se guarda con los hashers de Django.** Nunca texto plano, nunca un esquema propio, nunca un hash calculado a mano en SQL.

---

## 6. Qué pasa cuando la base de identidad no responde

Es un punto único de falla: si se cae, nadie entra a ninguna app. Eso se asume, pero no se ignora.

- **Un chequeo de salud propio**, obligatorio, en `core/checks.py`. La ruta `/salud/` debe decir si la identidad responde, separada del resto.
- **Tiempo de espera corto y explícito** en la conexión, como cualquier sistema ajeno (ver `04-seguridad.md §3`). Un login que cuelga treinta segundos es peor que un login que falla en tres.
- **Mensaje propio al usuario**: "No se pudo verificar tu acceso. Intenta de nuevo o avisa a TI." Nunca el error del driver.
- **Las sesiones ya iniciadas viven en la base propia de la app**, no en la de identidad. Una caída corta no expulsa a quien ya está trabajando.

---

## 7. Qué trae la plantilla

El paquete `cuentas/` viene resuelto y **no se modifica por app**:

| Archivo | Qué hace |
|---|---|
| `models.py` | `Usuario`, `Aplicacion`, `AccesoAplicacion` |
| `routers.py` | Manda `cuentas` a `identidad` y bloquea migraciones si no es propietaria |
| `backends.py` | Autenticación contra `identidad` y verificación del acceso a esta app |
| `decoradores.py` | `@rol_requerido("administra")` |
| `checks.py` | Chequeo de salud de la conexión de identidad |

Lo único que cambia entre apps es el valor de `CODIGO_APLICACION` en `.env`, que identifica a la app dentro de `acceso_aplicacion`.

**Si una app necesita cambiar algo de `cuentas/`, eso es una desviación del estándar** y se declara. Lo más probable es que el cambio corresponda al estándar y no a la app.
