#   ./django/investimento/admin.py
from core.admin.base import BaseModelAdmin
from django.contrib import admin

from investimento.models import InvestimentoModel, ResgateModel


@admin.register(InvestimentoModel)
class InvestimentoAdmin(BaseModelAdmin):
    list_display = (
        "id",
        "usuario",
        "valor_investido",
        "data_inicio",
        "saldo_bruto",
        "saldo_liquido",
        "resgatado",
        "criado_em",
    )

    list_display_links = (
        "id",
        "usuario",
    )

    list_filter = (
        "data_inicio",
        "criado_em",
    )

    search_fields = (
        "usuario__nome",
        "usuario__email",
        "descricao",
    )

    autocomplete_fields = ("usuario",)

    list_select_related = ("usuario",)

    ordering = ("-criado_em",)

    fieldsets = (
        (
            "Dados do investimento",
            {
                "fields": (
                    "usuario",
                    "descricao",
                    "valor_investido",
                    "data_inicio",
                ),
            },
        ),
        (
            "Demonstrativo",
            {
                "classes": ("collapse",),
                "fields": (
                    "montante",
                    "rendimento",
                    "aliquota",
                    "imposto",
                    "saldo_bruto",
                    "saldo_liquido",
                ),
            },
        ),
    )

    immutable_fields = ("usuario",)

    readonly_fields = (
        *BaseModelAdmin.readonly_fields,
        "montante",
        "rendimento",
        "aliquota",
        "imposto",
        "saldo_bruto",
        "saldo_liquido",
    )


@admin.register(ResgateModel)
class ResgateAdmin(BaseModelAdmin):
    list_display = (
        "id",
        "investimento",
        "data_resgate",
        "saldo_bruto",
        "saldo_liquido",
        "criado_em",
    )

    list_display_links = (
        "id",
        "investimento",
    )

    list_filter = (
        "data_resgate",
        "criado_em",
    )

    search_fields = (
        "investimento__usuario__nome",
        "investimento__usuario__email",
    )

    autocomplete_fields = ("investimento",)

    list_select_related = (
        "investimento",
        "investimento__usuario",
    )

    ordering = ("-data_resgate",)

    fieldsets = (
        (
            "Resgate",
            {
                "fields": (
                    "investimento",
                    "data_resgate",
                ),
            },
        ),
        (
            "Resultado",
            {
                "fields": (
                    "aliquota",
                    "imposto",
                    "saldo_bruto",
                    "saldo_liquido",
                ),
            },
        ),
    )

    immutable_fields = (
        "investimento",
        "aliquota",
        "imposto",
        "saldo_bruto",
        "saldo_liquido",
    )

    readonly_fields = (
        *BaseModelAdmin.readonly_fields,
        "aliquota",
        "imposto",
        "saldo_bruto",
        "saldo_liquido",
    )
