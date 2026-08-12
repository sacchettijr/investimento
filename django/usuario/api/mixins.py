#   ./django/usuario/api/mixins.py


from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.request import Request
from usuario.models import UsuarioModel
from usuario.utils import (
    normalizar_email,
    normalizar_nome,
)


# ===================================================
#   MIXIN DE DADOS DO USUÁRIO
# ===================================================
class UsuarioSerializerMixin:
    #   Métodos compartilhados entre os serializers de usuário.

    def validate_nome(
        self,
        value: str,
    ) -> str:
        nome = normalizar_nome(value)

        partes = nome.split()

        if len(nome) < 5:
            raise serializers.ValidationError("Informe um nome válido.")
        if len(partes) < 2:
            raise serializers.ValidationError("Informe seu nome completo.")
        return nome

    def validate_email(
        self,
        value: str,
    ) -> str:
        email = normalizar_email(value)

        if not email:
            raise serializers.ValidationError(
                "Informe um e-mail válido.",
            )

        queryset = UsuarioModel.objects.filter(
            email=email,
        )

        instance = getattr(
            self,
            "instance",
            None,
        )

        if instance is not None:
            queryset = queryset.exclude(
                pk=instance.pk,
            )

        if queryset.exists():
            raise serializers.ValidationError(
                "Já existe um usuário cadastrado com este e-mail.",
            )

        return email


# ===================================================
#   MIXIN DE SENHA
# ===================================================
class PasswordValidationMixin:
    #   Validações relacionadas à senha.

    def validate_password(
        self,
        value: str,
    ) -> str:
        validate_password(
            password=value,
            user=getattr(
                self,
                "instance",
                None,
            ),
        )
        return value


# ===================================================
#   MIXIN DE USUÁRIO ATUAL
# ===================================================


class CurrentUserMixin:
    #   Retorna o usuário autenticado atual.

    @property
    def current_user(self) -> UsuarioModel | None:
        context = getattr(
            self,
            "context",
            {},
        )

        request: Request | None = context.get(
            "request",
        )

        if request is None:
            return None

        user = getattr(
            request,
            "user",
            None,
        )

        return user if user is not None and user.is_authenticated else None
