#   ./django./investimento/services.py
from dataclasses import dataclass
from datetime import date
from decimal import ROUND_HALF_UP, Decimal


@dataclass(
    frozen=True,
)
class DemonstrativoInvestimento:
    montante: Decimal
    rendimento: Decimal
    aliquota: Decimal
    imposto: Decimal
    saldo_bruto: Decimal
    saldo_liquido: Decimal


class InvestimentoService:
    TAXA = Decimal("0.0052")
    FATOR_RENDIMENTO: Decimal = Decimal("1.00") + TAXA
    ALIQUOTA_MENOR_1_ANO = Decimal("22.5")
    ALIQUOTA_1_A_2_ANOS = Decimal("18.5")
    ALIQUOTA_MAIOR_2_ANOS = Decimal("15.0")
    CENTO = Decimal("100")
    CENTAVOS = Decimal("0.01")

    @staticmethod
    def meses_rendidos(
        data_inicio: date,
        data_final: date,
    ) -> int:
        meses = (data_final.year - data_inicio.year) * 12 + data_final.month - data_inicio.month

        if data_final.day < data_inicio.day:
            meses -= 1

        return max(meses, 0)

    @classmethod
    def aliquota(
        cls,
        data_inicio: date,
        data_final: date,
    ) -> Decimal:
        dias = (data_final - data_inicio).days
        if dias < 365:
            return cls.ALIQUOTA_MENOR_1_ANO
        if dias < 730:
            return cls.ALIQUOTA_1_A_2_ANOS
        return cls.ALIQUOTA_MAIOR_2_ANOS

    @classmethod
    def calcular_demonstrativo(
        cls,
        valor_investido: Decimal,
        data_inicio: date,
        data_final: date,
    ) -> DemonstrativoInvestimento:

        meses: int = cls.meses_rendidos(
            data_inicio,
            data_final,
        )

        montante: Decimal = (valor_investido * (cls.FATOR_RENDIMENTO**meses)).quantize(
            cls.CENTAVOS, rounding=ROUND_HALF_UP
        )

        rendimento: Decimal = (montante - valor_investido).quantize(
            cls.CENTAVOS,
            rounding=ROUND_HALF_UP,
        )

        aliquota: Decimal = cls.aliquota(
            data_inicio,
            data_final,
        )

        imposto: Decimal = (rendimento * aliquota / cls.CENTO).quantize(
            cls.CENTAVOS,
            rounding=ROUND_HALF_UP,
        )

        saldo_liquido: Decimal = (montante - imposto).quantize(
            cls.CENTAVOS,
            rounding=ROUND_HALF_UP,
        )

        return DemonstrativoInvestimento(
            montante=montante,
            rendimento=rendimento,
            aliquota=aliquota,
            imposto=imposto,
            saldo_bruto=montante,
            saldo_liquido=saldo_liquido,
        )
