#   ./django/investimento/models.py
from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING, Any

from core.models import BaseModel
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.utils.functional import cached_property
from usuario.models import UsuarioModel

from investimento.services import DemonstrativoInvestimento, InvestimentoService


class InvestimentoModel(BaseModel):
    usuario = models.ForeignKey(
        UsuarioModel,
        on_delete=models.CASCADE,
        related_name="investimentos",
    )
    descricao = models.TextField(
        blank=True,
    )
    valor_investido = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    data_inicio = models.DateField()

    class Meta:
        verbose_name = "Investimento"
        verbose_name_plural = "Investimentos"
        db_table = "investimento"
        ordering = [
            "usuario",
            "criado_em",
        ]

    if TYPE_CHECKING:
        #   APENAS PARA EVITAR FALSO POSITIVO DO PYLANCE
        resgate: "ResgateModel"

    def __str__(self) -> str:
        return f"Investimento {self.pk} - {self.usuario.email} - {self.valor_investido}"

    def clean(self) -> None:
        super().clean()
        if self.pk:
            usuario_original_id = (
                type(self)
                .objects.filter(
                    pk=self.pk,
                )
                .values_list(
                    "usuario_id",
                    flat=True,
                )
                .get()
            )
            if usuario_original_id != self.usuario.pk:
                raise ValidationError("O proprietário do investimento não pode ser alterado.")
        if self.valor_investido <= Decimal("0"):
            raise ValidationError({"valor_investido": "O investimento deve ser maior que zero."})
        if self.data_inicio > date.today():
            raise ValidationError(
                {"data_inicio": "A data do investimento não pode estar no futuro."}
            )

    @property
    def resgatado(self) -> bool:
        return hasattr(self, "resgate")

    @property
    def data_final(self) -> date:
        if self.resgatado:
            return self.resgate.data_resgate
        return date.today()

    @cached_property
    def resumo(self) -> DemonstrativoInvestimento:
        return InvestimentoService.calcular_demonstrativo(
            self.valor_investido,
            self.data_inicio,
            self.data_final,
        )

    @property
    def montante(self) -> Decimal:
        return self.resumo.montante

    @property
    def rendimento(self) -> Decimal:
        return self.resumo.rendimento

    @property
    def aliquota(self) -> Decimal:
        return self.resumo.aliquota

    @property
    def imposto(self) -> Decimal:
        return self.resumo.imposto

    @property
    def saldo_bruto(self) -> Decimal:
        return self.resumo.saldo_bruto

    @property
    def saldo_liquido(self) -> Decimal:
        return self.resumo.saldo_liquido

    def save(self, *args: Any, **kwargs: Any):
        self.full_clean()

        with transaction.atomic():
            resultado = super().save(*args, **kwargs)
            self.usuario.atualizar_saldo()
        return resultado

    def delete(self, *args: Any, **kwargs: Any):
        usuario = self.usuario
        with transaction.atomic():
            resultado = super().delete(*args, **kwargs)
            usuario.atualizar_saldo()
        return resultado


class ResgateModel(BaseModel):
    investimento = models.OneToOneField(
        InvestimentoModel,
        on_delete=models.CASCADE,
        related_name="resgate",
    )
    data_resgate = models.DateField()
    aliquota = models.DecimalField(
        "Alíquota",
        max_digits=5,
        decimal_places=2,
        editable=False,
    )
    imposto = models.DecimalField(
        "Imposto",
        max_digits=10,
        decimal_places=2,
        editable=False,
    )
    saldo_bruto = models.DecimalField(
        "Saldo bruto",
        max_digits=10,
        decimal_places=2,
        editable=False,
    )
    saldo_liquido = models.DecimalField(
        "Saldo líquido",
        max_digits=10,
        decimal_places=2,
        editable=False,
    )

    class Meta:
        verbose_name = "Resgate"
        verbose_name_plural = "Resgates"
        db_table = "resgate"
        ordering = [
            "investimento",
        ]

    def __str__(self) -> str:
        return f"Resgate {self.pk} - {self.investimento.usuario.email}"

    def clean(self):
        if self.investimento.resgatado:
            raise ValidationError(
                {
                    "investimento": "Este investimento já foi resgatado.",
                }
            )
        if self.data_resgate < self.investimento.data_inicio:
            raise ValidationError(
                {
                    "data_resgate": "O resgate não pode ocorrer antes do investimento.",
                }
            )
        if self.data_resgate > date.today():
            raise ValidationError(
                {
                    "data_resgate": "O resgate não pode ocorrer no futuro.",
                }
            )
        return super().clean()

    def save(self, *args, **kwargs):

        if self.pk and type(self).objects.filter(pk=self.pk).exists():
            raise ValidationError("Um resgate não pode ser alterado após ser criado.")
        self.full_clean()

        resumo: DemonstrativoInvestimento = InvestimentoService.calcular_demonstrativo(
            self.investimento.valor_investido,
            self.investimento.data_inicio,
            self.data_resgate,
        )

        self.aliquota = resumo.aliquota
        self.imposto = resumo.imposto
        self.saldo_bruto = resumo.saldo_bruto
        self.saldo_liquido = resumo.saldo_liquido

        with transaction.atomic():
            resultado = super().save(*args, **kwargs)
            self.investimento.usuario.atualizar_saldo()
        return resultado

    def delete(self, *args, **kwargs):
        usuario = self.investimento.usuario
        with transaction.atomic():
            resultado = super().delete(*args, **kwargs)
            usuario.atualizar_saldo()
        return resultado
