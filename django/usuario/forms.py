#   ./django/usuario/forms.py
from typing import Any

from core.forms import FormStyleMixin
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    ReadOnlyPasswordHashField,
    SetPasswordForm,
    UserCreationForm,
)
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import HttpRequest

from django import forms
from usuario.models import UsuarioModel
from usuario.utils import normalizar_email, normalizar_nome

# ===================================================
#   MIXINS
# ===================================================


class UsuarioFormMixin:
    cleaned_data: dict[str, Any]
    instance: UsuarioModel
    fields: dict[str, forms.Field]

    def clean_nome(self) -> str:
        nome = normalizar_nome(
            self.cleaned_data["nome"],
        )

        partes = nome.split()

        if len(partes) < 2:
            raise ValidationError("Informe seu nome completo.")

        if len(nome) < 5:
            raise ValidationError("Informe um nome válido.")

        return nome

    def clean_email(self) -> str:
        email = normalizar_email(
            self.cleaned_data["email"],
        )

        queryset = UsuarioModel.objects.exclude(
            pk=self.instance.pk,
        ).filter(
            email=email,
        )

        if queryset.exists():
            raise ValidationError("Já existe um usuário cadastrado com este e-mail.")

        return email


# ===================================================
#   WIDGETS
# ===================================================


USUARIO_FORM_WIDGETS: dict[str, forms.Widget] = {
    "nome": forms.TextInput(
        attrs={
            "class": "form-control",
            "autocomplete": "name",
            "placeholder": "Nome completo",
        },
    ),
    "email": forms.EmailInput(
        attrs={
            "class": "form-control",
            "autocomplete": "email",
            "placeholder": "Digite seu e-mail",
        },
    ),
}


# ===================================================
#   CRIAÇÃO DE USUÁRIO
# ===================================================


class UsuarioCreateForm(
    FormStyleMixin,
    UsuarioFormMixin,
    UserCreationForm,
):
    class Meta:
        model = UsuarioModel
        fields = (
            "nome",
            "email",
        )
        widgets = USUARIO_FORM_WIDGETS

    def __init__(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            *args,
            **kwargs,
        )

        self.configurar_nome(
            "nome",
        )

        self.configurar_email(
            "email",
            autofocus=True,
        )

        self.configurar_password(
            "password1",
            label="Senha",
            placeholder="Digite sua senha",
        )

        self.configurar_password(
            "password2",
            label="Confirme sua senha",
            placeholder="Confirme sua senha",
        )


# =========================================================
# ATUALIZAÇÃO DE USUÁRIO
# =========================================================


class UsuarioUpdateForm(
    FormStyleMixin,
    UsuarioFormMixin,
    forms.ModelForm,
):
    class Meta:
        model = UsuarioModel
        fields = (
            "nome",
            "email",
        )
        widgets = USUARIO_FORM_WIDGETS

    def __init__(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            *args,
            **kwargs,
        )

        self.configurar_nome(
            "nome",
        )

        self.configurar_email(
            "email",
            autofocus=True,
        )


# =========================================================
#   LOGIN
# =========================================================


class UsuarioLoginForm(
    FormStyleMixin,
    AuthenticationForm,
):
    def __init__(
        self,
        request: HttpRequest | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            request,
            *args,
            **kwargs,
        )

        self.configurar_campo(
            "username",
            label="E-mail",
            autocomplete="email",
            placeholder="Digite seu email",
            help_text="",
            autofocus=True,
            spellcheck="false",
            autocapitalize="none",
        )

        self.configurar_campo(
            "password",
            label="Senha",
            autocomplete="current-password",
            placeholder="Digite sua senha",
            help_text="",
        )


# =========================================================
#   ALTERAÇÃO DE SENHA
# =========================================================


class UsuarioPasswordChangeForm(
    FormStyleMixin,
    PasswordChangeForm,
):
    def __init__(
        self,
        user: UsuarioModel,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            user,
            *args,
            **kwargs,
        )

        self.configurar_campo(
            "old_password",
            label="Senha atual",
            placeholder="Digite sua senha atual",
            autocomplete="current-password",
        )

        self.configurar_password(
            "new_password1",
            label="Confirme sua nova senha",
            placeholder="Confirme sua nova senha",
        )


# =========================================================
#   RECUPERAÇÃO DE SENHA
# =========================================================


class UsuarioPasswordResetForm(
    FormStyleMixin,
    PasswordResetForm,
):
    def __init__(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            *args,
            **kwargs,
        )

        self.configurar_email(
            "email",
            autofocus=True,
        )


# =========================================================
#   DEFINIÇÃO DE NOVA SENHA
# =========================================================


class UsuarioNovaSenhaForm(
    FormStyleMixin,
    SetPasswordForm,
):
    def __init__(
        self,
        user: UsuarioModel,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            user,
            *args,
            **kwargs,
        )

        self.configurar_password(
            "new_password1",
            label="Senha",
            placeholder="Digite sua senha",
        )

        self.configurar_password(
            "new_password2",
            label="Confirmação de senha",
            placeholder="Confirme sua senha",
        )


# =========================================================
#   ADMIN - CRIAÇÃO DE USUÁRIO
# =========================================================


class UsuarioAdminCreationForm(
    FormStyleMixin,
    UsuarioFormMixin,
    forms.ModelForm,
):
    password1 = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
            },
        ),
        strip=False,
        help_text="Informe uma senha segura para o usuário.",
    )

    password2 = forms.CharField(
        label="Confirmação da senha",
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
            },
        ),
        strip=False,
    )

    class Meta:
        model = UsuarioModel
        fields = (
            "nome",
            "email",
            "password1",
            "password2",
            "saldo",
            "is_active",
            "is_staff",
            "is_superuser",
            "is_email_verified",
            "groups",
            "user_permissions",
        )

    def __init__(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            *args,
            **kwargs,
        )

        self.configurar_nome(
            "nome",
        )

        self.configurar_email(
            "email",
        )

        self.configurar_password(
            "password1",
            label="Senha",
            placeholder="Digite uma senha segura",
        )

        self.configurar_password(
            "password2",
            label="Confirmar a senha",
            placeholder="Confirmar a senha",
        )

    def clean_password1(self) -> str:
        password = self.cleaned_data.get(
            "password1",
        )

        if not password:
            raise ValidationError(
                "A senha é obrigatória.",
            )

        validate_password(
            password,
            self.instance,
        )

        return password

    def clean(
        self,
    ) -> dict[str, Any]:
        cleaned_data = super().clean()

        password1 = cleaned_data.get("password1")

        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error(
                "password2",
                "As senhas não coincidem.",
            )

        return cleaned_data

    def save(
        self,
        commit: bool = True,
    ) -> UsuarioModel:
        usuario = super().save(
            commit=False,
        )

        usuario.set_password(
            self.cleaned_data["password1"],
        )

        if commit:
            usuario.save()
            self.save_m2m()

        return usuario


# =========================================================
#   ADMIN - ALTERAÇÃO DE USUÁRIO
# =========================================================


class UsuarioAdminChangeForm(
    FormStyleMixin,
    UsuarioFormMixin,
    forms.ModelForm,
):
    password = ReadOnlyPasswordHashField(
        label="Senha",
        help_text=(
            "As senhas são armazenadas de forma segura e não podem ser vizualizadas. "
            "Para alterar a senha, utilize o formulário de alteração de senha."
        ),
    )

    class Meta:
        model = UsuarioModel
        fields = (
            "nome",
            "email",
            "password",
            "saldo",
            "is_active",
            "is_staff",
            "is_superuser",
            "is_email_verified",
            "groups",
            "user_permissions",
        )

    def __init__(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            *args,
            **kwargs,
        )

        self.configurar_nome(
            "nome",
        )
