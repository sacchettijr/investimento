#   ./django/core/admin/base.py
from typing import Any

from django.contrib import admin
from django.http import HttpRequest

from core.admin.mixins import (
    AuditoriaFieldsMixin,
    ImmutableFieldsMixin,
)
from core.models import BaseModel


class BaseAdmin(admin.ModelAdmin):
    save_on_top = True
    list_per_page = 25
    ordering = ("id",)


class BaseModelAdmin(
    ImmutableFieldsMixin,
    AuditoriaFieldsMixin,
    BaseAdmin,
):
    readonly_fields = (
        "criado_em",
        "modificado_em",
        "criado_por",
        "modificado_por",
    )

    def get_fieldsets(
        self,
        request: HttpRequest,
        obj: Any | None = None,
    ):
        fieldsets = list(
            super().get_fieldsets(
                request,
                obj,
            ),
        )
        fieldsets.append(
            (
                "Auditoria",
                {
                    "classes": ("collapse",),
                    "fields": (
                        "criado_em",
                        "modificado_em",
                        "criado_por",
                        "modificado_por",
                    ),
                },
            ),
        )
        return fieldsets

    def save_model(
        self,
        request: HttpRequest,
        obj: BaseModel,
        form: Any,
        change: bool,
    ) -> None:

        if not change:
            obj.criado_por = request.user
        obj.modificado_por = request.user
        super().save_model(
            request,
            obj,
            form,
            change,
        )
