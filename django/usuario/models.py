#   ./django/usuario/models.py
from decimal import ROUND_HALF_UP, Decimal
from typing import TYPE_CHECKING, Any, ClassVar

from core.models import BaseModel
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.db.models import Manager
from django.urls import reverse

from django.core import signing
from usuario.utils import normalizar_email, normalizar_nome


class UsuarioManagerModel(BaseUserManager["UsuarioModel"]):
    def create_user(
        self,
        nome: str,
        email: str,
        password: str | None = None,
        saldo: Decimal = Decimal("0.00"),
    ) -> "UsuarioModel":
        model = self.model

        nome = normalizar_nome(nome)
        email = normalizar_email(email)

        if not nome:
            raise ValueError("O nome do usuário deve ser fornecido.")
        if not email:
            raise ValueError("O e-mail do usuário deve ser fornecido.")
        if not password:
            raise ValueError("A senha do usuário deve ser fornecida.")

        usuario = model(
            nome=nome,
            email=email,
            saldo=saldo,
        )
        usuario.set_password(password)
        usuario.save(
            using=self._db,
        )
        usuario.enviar_email_confirmacao()
        return usuario

    def create_superuser(
        self,
        nome: str,
        email: str,
        password: str,
        saldo: Decimal = Decimal("0.00"),
    ) -> "UsuarioModel":
        model = self.model

        nome = normalizar_nome(nome)
        email = normalizar_email(email)

        usuario = model(
            nome=nome,
            email=email,
            saldo=saldo,
            is_superuser=True,
            is_staff=True,
            is_active=True,
            is_email_verified=True,
        )

        usuario.set_password(password)

        if not usuario.is_superuser:
            raise ValueError("O superusuário deve ter is_superuser=True.")
        if not usuario.is_staff:
            raise ValueError("O superusuário deve ter is_staff=True.")

        usuario.save(
            using=self._db,
        )
        return usuario


class UsuarioModel(BaseModel, AbstractBaseUser, PermissionsMixin):
    #   Dados
    nome = models.CharField(
        "Nome",
        max_length=150,
    )
    email = models.EmailField(
        "E-mail",
        unique=True,
        db_index=True,
        max_length=255,
    )
    saldo = models.DecimalField(
        "Saldo",
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text="Valor atualmente investido, incluindo os rendimentos dos investimentos ativos.",
    )

    #   Permissões
    is_staff = models.BooleanField(
        "Membro da equipe",
        default=False,
    )
    is_active = models.BooleanField(
        "Ativo",
        default=True,
    )
    is_email_verified = models.BooleanField(
        "E-mail verificado",
        default=False,
    )

    objects: ClassVar[UsuarioManagerModel] = UsuarioManagerModel()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "nome",
    ]

    if TYPE_CHECKING:
        #   CORRIGIR FALSO POSITIVO PYLANCE
        from investimento.models import InvestimentoModel

        investimentos: Manager["InvestimentoModel"]

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        db_table = "usuario"
        ordering = ["email"]

    def __str__(self):
        return f"{self.nome} <{self.email}>"

    def get_full_name(self) -> str:
        return self.nome

    def get_short_name(self) -> str:
        return self.nome.split(" ")[0] if self.nome else ""

    def email_user(
        self,
        subject: str,
        message: str,
        from_email: str | None = None,
        **kwargs: Any,
    ) -> None:
        send_mail(
            subject,
            message,
            from_email,
            [
                self.email,
            ],
            **kwargs,
        )

    def atualizar_saldo(self) -> None:
        investimentos = self.investimentos.filter(resgate__isnull=True).iterator()

        novo_saldo = sum(
            (investimento.saldo_bruto for investimento in investimentos),
            start=Decimal("0.00"),
        ).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

        if self.saldo != novo_saldo:
            type(self).objects.filter(pk=self.pk).update(
                saldo=novo_saldo,
            )
            self.saldo = novo_saldo

    def gerar_token_confirmacao_email(self) -> str:
        return signing.dumps(
            {
                "usuario_id": self.pk,
                "email": self.email,
            },
            salt="usuario-confirmacao-email",
        )

    def enviar_email_confirmacao(self) -> None:
        if self.is_email_verified:
            return

        if not self.pk:
            raise ValueError(
                "O usuário precisa ser salvo antes de enviar o e-mail de confirmação.",
            )

        token: str = self.gerar_token_confirmacao_email()

        url_confirmacao: str = reverse(
            "usuario:usuario_confirmar_email",
            kwargs={
                "token": token,
            },
        )

        link_confirmacao: str = f"{settings.SITE_URL}{url_confirmacao}"

        self.email_user(
            subject="Confirme seu cadastro",
            message=(
                f"Olá, {self.get_short_name()}!\n\n"
                "Seu cadastro foi realizado com sucesso.\n\n"
                "Para confirmar seu endereço de e-mail, "
                "acesse o link abaixo:\n\n"
                f"{link_confirmacao}\n\n"
                "Se você não realizou este cadastro, "
                "ignore este e-mail."
            ),
        )

    def save(
        self,
        *args: Any,
        **kwargs: Any,
    ):

        if self.nome:
            self.nome = normalizar_nome(
                self.nome,
            )

        if self.email:
            self.email = normalizar_email(
                self.email,
            )

        return super().save(*args, **kwargs)
