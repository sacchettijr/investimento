#   ./django/PROJETO/settings.py
#   Django 6.0.7.
import os
from pathlib import Path

from dotenv import load_dotenv
from utils.env import env, env_bool, env_int, env_list

# =========================================================
# BASE
# =========================================================

BASE_DIR: Path = Path(__file__).resolve().parent.parent

load_dotenv(
    BASE_DIR.parent / ".env",
)


# =========================================================
# SEGURANÇA
# =========================================================
SECRET_KEY: str = env("SECRET_KEY")

DEBUG: bool = env_bool(
    "DEBUG",
    default=False,
)

ALLOWED_HOSTS: list[str] = env_list(
    "ALLOWED_HOSTS",
    default=[
        "localhost",
        "127.0.0.1",
    ],
)


# =========================================================
# APLICAÇÕES
# =========================================================
INSTALLED_APPS: list[str] = [
    #   DJANGO
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    #   LIBS
    "rest_framework",
    "django_filters",
    "guardian",
    #   APPS
    "core",
    "usuario",
    "investimento",
]


# =========================================================
# MIDDLEWARE
# =========================================================

MIDDLEWARE: list[str] = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    #   MIDDLEWARE PARA OBTER O USUÁRIO LOGADO
    "core.middleware.CurrentUserMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# =========================================================
# URLS
# =========================================================

ROOT_URLCONF = "PROJETO.urls"


# =========================================================
# TEMPLATES
# =========================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# =========================================================
# SERVIDORES
# =========================================================

WSGI_APPLICATION = "PROJETO.wsgi.application"


# =========================================================
# BANCO DE DADOS
# =========================================================

DATABASES: dict[str, dict[str, str]] = {
    "default": {
        "ENGINE": env("POSTGRES_ENGINE"),
        "HOST": env("POSTGRES_HOST"),
        "PORT": env("POSTGRES_PORT"),
        "NAME": env("POSTGRES_DB"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
    }
}


# =========================================================
# AUTENTICAÇÃO
# =========================================================

AUTH_USER_MODEL = "usuario.UsuarioModel"

AUTHENTICATION_BACKENDS: list[str] = [
    #   Backend padrão do Django
    "django.contrib.auth.backends.ModelBackend",
    #   Permissões por objeto do django-guardian
    "guardian.backends.ObjectPermissionBackend",
]

ANONYMOUS_USER_NAME = "anonymous"


# =========================================================
# VALIDAÇÃO DE SENHA
# =========================================================

AUTH_PASSWORD_VALIDATORS: list[dict[str, str]] = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# =========================================================
# DJANGO REST FRAMEWORK
# =========================================================

API_PAGE_SIZE: int = env_int(
    "API_PAGE_SIZE",
    default=25,
)

REST_FRAMEWORK = {
    #   AUTENTICAÇÃO
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
    #   PERMISSÕES
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    #   FILTROS
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    #   PAGINAÇÃO
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": API_PAGE_SIZE,
    #   RENDERIZAÇÃO
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
    #   EXCEÇÕES
    "EXCEPTION_HANDLER": "core.api.exceptions.exception_handler",
    #   PARSERS
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ],
    #   FORMATO DE DATA
    "DATETIME_FORMAT": "%Y-%m-%dT%H:%M:%S%z",
    "DATE_FORMAT": "%Y-%m-%d",
    #   SCHEMA
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.openapi.AutoSchema",
}


# =========================================================
# DJANGO-GUARDIAN
# =========================================================

GUARDIAN_RAISE_403 = True


# =========================================================
# INTERNACIONALIZAÇÃO
# =========================================================

LANGUAGE_CODE: str = env(
    "LANGUAGE_CODE",
    default="pt-br",
)

TIME_ZONE: str = env(
    "TIMEZONE",
    default="America/Manaus",
)

USE_I18N = True
USE_TZ = True


# =========================================================
# ARQUIVOS ESTÁTICOS
# =========================================================

STATIC_URL = "static/"

STATICFILES_DIRS = [
    os.path.join(
        BASE_DIR,
        "static",
    ),
]

STATIC_ROOT: str = os.path.join(
    BASE_DIR,
    "staticfiles",
)


# =========================================================
# ARQUIVOS DE MEDIA
# =========================================================

MEDIA_URL = "media/"

MEDIA_ROOT: str = os.path.join(
    BASE_DIR,
    "mediafiles",
)


# =========================================================
#   CONFIGURAÇÕES DE EMAIL
# =========================================================


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

SITE_URL: str = env(
    "SITE_URL",
)

EMAIL_HOST: str = env(
    "EMAIL_HOST",
)
EMAIL_PORT: int = env_int(
    "EMAIL_PORT",
    default=587,
)
EMAIL_USE_TLS: bool = env_bool(
    "EMAIL_USE_TLS",
    default=True,
)
EMAIL_HOST_USER: str = env(
    "EMAIL_HOST_USER",
)
EMAIL_HOST_PASSWORD: str = env(
    "EMAIL_HOST_PASSWORD",
)
DEFAULT_FROM_EMAIL: str = env(
    "DEFAULT_FROM_EMAIL",
)


# =========================================================
# CONFIGURAÇÕES PADRÃO
# =========================================================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
