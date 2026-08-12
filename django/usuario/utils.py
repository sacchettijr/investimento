#   ./django/usuario.utils.py
from django.contrib.auth.models import BaseUserManager


def normalizar_nome(nome: str) -> str:
    return " ".join(nome.split())


def normalizar_email(email: str) -> str:
    return BaseUserManager.normalize_email(
        email.strip(),
    ).lower()
