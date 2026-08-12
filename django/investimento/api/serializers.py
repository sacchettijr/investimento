#   ./django/investimento/api/serializers.py
from datetime import date
from typing import Any

from rest_framework import serializers

from investimento.models import InvestimentoModel, ResgateModel

# ===================================================
#   SERIALIZER DE INVESTIMENTO
# ===================================================


class InvestimentoSerializer(serializers.ModelSerializer):
    #   Campos calculados pelo InvestimentoService (via propriedades do model).
    resgatado = serializers.BooleanField(read_only=True)
    data_final = serializers.DateField(read_only=True)
    montante = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    rendimento = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    aliquota = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)
    imposto = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    saldo_bruto = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    saldo_liquido = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = InvestimentoModel

        fields = (
            "id",
            "usuario",
            "descricao",
            "valor_investido",
            "data_inicio",
            "resgatado",
            "data_final",
            "montante",
            "rendimento",
            "aliquota",
            "imposto",
            "saldo_bruto",
            "saldo_liquido",
            "criado_em",
            "modificado_em",
        )

        read_only_fields = (
            "id",
            "usuario",
            "criado_em",
            "modificado_em",
        )


# ===================================================
#   SERIALIZER DE RESGATE
# ===================================================


class ResgateSerializer(serializers.ModelSerializer):
    #   Quando não informada, o resgate ocorre na data atual.
    data_resgate = serializers.DateField(
        required=False,
        default=date.today,
    )

    class Meta:
        model = ResgateModel

        fields = (
            "id",
            "investimento",
            "data_resgate",
            "aliquota",
            "imposto",
            "saldo_bruto",
            "saldo_liquido",
            "criado_em",
        )

        read_only_fields = (
            "id",
            "aliquota",
            "imposto",
            "saldo_bruto",
            "saldo_liquido",
            "criado_em",
        )

    def __init__(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)

        request = self.context.get("request")

        #   Isolamento por proprietário: um usuário só pode resgatar
        #   os próprios investimentos.
        if request is not None and not request.user.is_superuser:
            self.fields["investimento"].queryset = InvestimentoModel.objects.filter(
                usuario=request.user,
            )
