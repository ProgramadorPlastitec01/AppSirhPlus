"""Configuracion de Django para SIRH+.

Decisiones que encierra:

- **No se instala `django.contrib.auth` ni `django.contrib.admin`.** SIRH+ no
  gestiona usuarios: no crea cuentas, no guarda contrasenas y no administra
  credenciales. Instalar `auth` crearia una tabla de usuarios propia —
  exactamente lo que la regla de `CLAUDE.md` prohibe— y `admin` abriria una
  puerta de administracion que nadie diseno ni audito. La autenticacion llega
  en el modulo `identidad/`, contra el gestor, cuando exista (desviacion D4).
- **Sin `auth` no hay `AUTH_PASSWORD_VALIDATORS` ni `AuthenticationMiddleware`.**
  No es un olvido: no hay contrasenas que validar en este sistema.
- **Una sola conexion, `default`.** La base de un sistema ajeno nunca entra en
  `DATABASES`: va en su capa `<fuente>_db/`, de solo lectura
  (`.claude/rules/01-estructura-y-capas.md` seccion 4).
- **`LOGGING` queda configurado desde el primer dia.** Sin el, los errores no
  quedan en ningun lado y mostrarselos al usuario se vuelve la unica forma de
  verlos, que es lo que `04-seguridad.md` seccion 4 prohibe.
- **Las banderas de HTTPS se leen del entorno y por defecto estan en falso.**
  En local eso produce cuatro avisos de `check --deploy` que estan aceptados
  por escrito en `CLAUDE.md`, seccion «Postura sobre HTTPS y check --deploy».
  En produccion las cuatro van en verdadero y no se acepta ningun hallazgo.
"""

from pathlib import Path

import environ

# sirh_plus/config/settings.py -> sirh_plus/
BASE_DIR = Path(__file__).resolve().parent.parent

# La raiz del repositorio, un nivel arriba: ahi viven .env y requirements.txt.
RAIZ_REPOSITORIO = BASE_DIR.parent

env = environ.Env()
environ.Env.read_env(RAIZ_REPOSITORIO / ".env")


# --- Nucleo ------------------------------------------------------------------

SECRET_KEY = env("DJANGO_SECRET_KEY")
DEBUG = env.bool("DJANGO_DEBUG", default=False)
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=[])

# Codigo con el que SIRH+ queda registrada en el gestor de identidad.
# Todavia no tiene efecto: ver la desviacion D4.
CODIGO_APLICACION = env("CODIGO_APLICACION", default="sirh_plus")

# Interruptor de la verificacion de permisos. En falso, el decorador deja pasar
# y anota en el registro cada verificacion que habria fallado. Se corre con
# PERMISOS_EXIGIR=true al menos una vez por fase.
PERMISOS_EXIGIR = env.bool("PERMISOS_EXIGIR", default=False)


# --- Aplicaciones -------------------------------------------------------------

INSTALLED_APPS = [
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"


# --- Plantillas ---------------------------------------------------------------
# Django Template Language, sin alternativas (02-stack.md seccion 4).

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.messages.context_processors.messages",
                "core.context.marca",
            ],
        },
    },
]


# --- Base de datos ------------------------------------------------------------
# PostgreSQL 17. Una sola conexion: la propia.

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("BD_NAME"),
        "USER": env("BD_USER"),
        "PASSWORD": env("BD_PASSWORD"),
        "HOST": env("BD_HOST", default="localhost"),
        "PORT": env("BD_PORT", default="5432"),
        # Conexiones persistentes: Gunicorn abre pocas y las reusa.
        "CONN_MAX_AGE": env.int("BD_CONN_MAX_AGE", default=60),
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# --- Sesiones -----------------------------------------------------------------
# Viven en la base propia: una caida del gestor de identidad no expulsa a quien
# ya esta trabajando. La cara de colaborador muestra el tiempo restante, asi que
# el valor tiene que ser explicito y no el de fabrica, que son dos semanas.

SESSION_ENGINE = "django.contrib.sessions.backends.db"
SESSION_COOKIE_AGE = env.int("SESION_MINUTOS", default=30) * 60
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"


# --- Internacionalizacion -----------------------------------------------------

LANGUAGE_CODE = "es-co"
TIME_ZONE = "America/Bogota"
USE_I18N = True
USE_TZ = True


# --- Archivos estaticos -------------------------------------------------------
# Sin build y sin CDN: todo se auto-hospeda en static/vendor/.

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"


# --- Seguridad ----------------------------------------------------------------
# Por defecto en falso para que el proyecto levante en local sin HTTPS.
# En produccion las cuatro van en verdadero, y entonces check --deploy sale
# sin ningun hallazgo. La postura escrita esta en CLAUDE.md.

SECURE_SSL_REDIRECT = env.bool("SEGURIDAD_SSL_REDIRECT", default=False)
SESSION_COOKIE_SECURE = env.bool("SEGURIDAD_COOKIE_SEGURA", default=False)
CSRF_COOKIE_SECURE = env.bool("SEGURIDAD_COOKIE_SEGURA", default=False)
SECURE_HSTS_SECONDS = env.int("SEGURIDAD_HSTS_SEGUNDOS", default=0)
SECURE_HSTS_INCLUDE_SUBDOMAINS = SECURE_HSTS_SECONDS > 0
SECURE_HSTS_PRELOAD = SECURE_HSTS_SECONDS > 0

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "same-origin"
X_FRAME_OPTIONS = "DENY"
CSRF_COOKIE_HTTPONLY = False  # el token se lee por JavaScript en los formularios
CSRF_COOKIE_SAMESITE = "Lax"

# Detras de Nginx, que es quien termina el TLS.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


# --- Registro de eventos ------------------------------------------------------

LOG_NIVEL = env("LOG_NIVEL", default="INFO").upper()
LOG_ARCHIVO = Path(env("LOG_ARCHIVO", default="logs/app.log"))
if not LOG_ARCHIVO.is_absolute():
    LOG_ARCHIVO = BASE_DIR / LOG_ARCHIVO
LOG_ARCHIVO.parent.mkdir(parents=True, exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "detallado": {
            "format": "{asctime} {levelname} {name} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "consola": {
            "class": "logging.StreamHandler",
            "formatter": "detallado",
        },
        "archivo": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": str(LOG_ARCHIVO),
            "maxBytes": 5 * 1024 * 1024,
            "backupCount": 5,
            "encoding": "utf-8",
            "formatter": "detallado",
        },
    },
    "root": {
        "handlers": ["consola", "archivo"],
        "level": LOG_NIVEL,
    },
    "loggers": {
        "django.request": {
            "handlers": ["consola", "archivo"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}
