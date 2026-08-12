#   ./django/usuari/admin.py

from core.admin.base import BaseModelAdmin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.http import HttpRequest

from usuario.forms import (
    UsuarioAdminChangeForm,
    UsuarioAdminCreationForm,
)
from usuario.models import UsuarioModel


@admin.register(UsuarioModel)
class UsuarioAdmin(
    BaseModelAdmin,
    UserAdmin,
):
    # =========================================================
    #   LISTAGEM
    # =========================================================

    list_display = (
        "nome",
        "email",
        "saldo",
        "is_active",
        "is_email_verified",
        "is_staff",
        "criado_em",
    )

    list_display_links = (
        "nome",
        "email",
    )

    list_filter = (
        "is_active",
        "is_staff",
        "is_superuser",
        "is_email_verified",
        "criado_em",
    )

    ordering = ("nome",)

    search_fields = (
        "email",
        "nome",
    )

    # =========================================================
    #   CAMPOS IMUTÁVEIS
    # =========================================================

    immutable_fields = ("email",)

    # =========================================================
    #   CAMPOS SOMENTE LEITURA
    # =========================================================

    readonly_fields = (
        *BaseModelAdmin.readonly_fields,
        "saldo",
        "password",
    )

    # =========================================================
    #   FORMULÁRIO DE ALTERAÇÃO
    # =========================================================

    form = UsuarioAdminChangeForm

    fieldsets = (
        (
            "Dados do usuário",
            {
                "fields": (
                    "nome",
                    "email",
                    "saldo",
                    "password",
                ),
            },
        ),
        (
            "Permissões",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_email_verified",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            "Auditoria",
            {
                "fields": (
                    "criado_em",
                    "modificado_em",
                    "criado_por",
                    "modificado_por",
                ),
            },
        ),
    )

    # =========================================================
    #   FORMULÁRIO DE CRIAÇÃO
    # =========================================================
    add_form = UsuarioAdminCreationForm

    add_fieldsets = (
        (
            "Dados do usuário",
            {
                "fields": (
                    "nome",
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
        (
            "Permissões",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_email_verified",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )

    # =========================================================
    #   FORMULÁRIO DINÂMICO
    # =========================================================

    def get_form(
        self,
        request,
        obj=None,
        **kwargs,
    ):
        if obj is None:
            kwargs["form"] = self.add_form
        return super().get_form(
            request,
            obj,
            **kwargs,
        )

    def save_model(
        self,
        request: HttpRequest,
        obj: UsuarioModel,
        form,
        change=bool,
    ) -> None:
        is_new = not obj.pk

        print(
            f"→ save_model chamado | novo usuário: {is_new} | email: {obj.email}",
        )

        super().save_model(
            request,
            obj,
            form,
            change,
        )

        if is_new:
            print(
                "→ Chamando enviar_email_confirmacao()",
            )
            obj.enviar_email_confirmacao()
            print(
                "→ enviar_email_confirmacao() concluído",
            )
