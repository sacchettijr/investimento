#   ./django/core/admin/mixins.py
from django.contrib import admin
from django.db.models import Model
from django.http import HttpRequest


class SearchByNameMixin:
    search_fields = ("nome",)


class SearchByEmailMixin:
    search_fields = ("email",)


class ReadOnlyAuditMixin:
    readonly_fields = (
        "criado_em",
        "modificado_em",
    )


class AuditoriaFieldsMixin(admin.ModelAdmin):
    #   Torna os campos de auditoria somente leitura.

    readonly_fields = (
        "criado_em",
        "modificado_em",
        "criado_por",
        "modificado_por",
    )


class ImmutableFieldsMixin(admin.ModelAdmin):
    #   Torna campos imutáveis após a criação do registro.

    immutable_fields: tuple[str, ...] = ()

    def get_readonly_fields(
        self,
        request: HttpRequest,
        obj: Model | None = None,
    ) -> tuple[str, ...]:
        fields = list(
            super().get_readonly_fields(
                request,
                obj,
            )
        )

        if obj is not None:
            fields.extend(
                self.immutable_fields,
            )

        return tuple(
            dict.fromkeys(fields),
        )
