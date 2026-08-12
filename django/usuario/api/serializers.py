#   ./django/usuario/api/serializers.py
from typing import Any, cast

from rest_framework import serializers
from usuario.api.mixins import (
    CurrentUserMixin,
    PasswordValidationMixin,
    UsuarioSerializerMixin,
)
from usuario.models import UsuarioModel

# ===================================================
#   SERIALIZER BASE
# ===================================================


class UsuarioSerializer(
    UsuarioSerializerMixin,
    serializers.ModelSerializer,
):
    class Meta:
        model = UsuarioModel

        fields = (
            "id",
            "nome",
            "email",
            "saldo",
            "criado_em",
            "modificado_em",
        )

        read_only_fields = (
            "id",
            "saldo",
            "criado_em",
            "modificado_em",
        )

        extra_kwargs = {
            "email": {
                "required": True,
            },
            "nome": {
                "required": True,
            },
        }


# ===================================================
#   SERIALIZER LISTA
# ===================================================


class UsuarioListSerializer(
    UsuarioSerializer,
):
    pass


# ===================================================
#   SERIALIZER DETALHE
# ===================================================


class UsuarioDetailSerializer(
    UsuarioSerializer,
):
    pass


# ===================================================
#   SERIALIZER DETALHE (usuário logado)
# ===================================================


class UsuarioMeSerializer(
    CurrentUserMixin,
    UsuarioSerializer,
):
    pass


# ===================================================
#   SERIALIZER CONSULTA SALDO USUÁRIO
# ===================================================


class UsuarioSaldoSerializer(
    serializers.ModelSerializer,
):
    class Meta:
        model = UsuarioModel

        fields = (
            "id",
            "saldo",
        )

        read_only_fields = fields


# ===================================================
#   SERIALIZER ADMIN
# ===================================================


class UsuarioAdminSerializer(
    UsuarioSerializer,
):
    class Meta(UsuarioSerializer.Meta):
        fields = (
            *UsuarioSerializer.Meta.fields,
            "is_active",
            "is_staff",
            "is_superuser",
            "is_email_verified",
        )


# ===================================================
#   SERIALIZER DE CRIAÇÃO
# ===================================================


class UsuarioCreateSerializer(
    PasswordValidationMixin,
    UsuarioSerializer,
):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={
            "input_type": "password",
        },
    )

    class Meta(UsuarioSerializer.Meta):
        fields = (
            "nome",
            "email",
            "password",
        )

    def create(
        self,
        validated_data: dict[str, Any],
    ) -> UsuarioModel:
        password = validated_data.pop(
            "password",
        )

        return UsuarioModel.objects.create_user(
            password=password,
            **validated_data,
        )


# ===================================================
#   SERIALIZER DE ATUALIZAÇÃO
# ===================================================


class UsuarioUpdateSerializer(
    UsuarioSerializer,
):
    class Meta(
        UsuarioSerializer.Meta,
    ):
        fields = ("nome",)


# ===================================================
#   SERIALIZER SENHA
# ===================================================


class UsuarioUpdatePasswordSerializer(
    PasswordValidationMixin,
    serializers.Serializer,
):
    current_password = serializers.CharField(
        write_only=True,
    )

    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={
            "input_type": "password",
        },
    )

    def validate_current_password(
        self,
        value: str,
    ) -> str:
        usuario = getattr(
            self,
            "instance",
            None,
        )

        if usuario is None or not usuario.check_password(value):
            raise serializers.ValidationError(
                "Senha atual incorreta.",
            )

        return value

    def save(
        self,
        **kwargs: Any,
    ) -> UsuarioModel:

        if self.instance is None:
            raise AssertionError(
                "O serializer não possui uma instância de usuário para atualizar a senha.",
            )

        usuario = cast(
            UsuarioModel,
            self.instance,
        )
        validated_data = cast(
            dict[str, str],
            self.validated_data,
        )

        usuario.set_password(
            validated_data["password"],
        )

        usuario.save(
            update_fields=[
                "password",
            ],
        )

        return usuario


# ===================================================
#   SERIALIZER CONFIRMAÇÃO DE EMAIL
# ===================================================


class UsuarioConfirmEmailSerializer(
    serializers.Serializer,
):
    token = serializers.CharField()


class UsuarioReenviarConfirmacaoEmailSerializer(
    serializers.Serializer,
):
    email = serializers.EmailField()
