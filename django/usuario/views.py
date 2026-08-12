# ./django/usuario/views.py

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views import View

from django.core import signing
from usuario.models import UsuarioModel


class UsuarioConfirmarEmailView(View):
    def get(
        self,
        request: HttpRequest,
        token: str,
    ) -> HttpResponse:
        try:
            dados = signing.loads(
                token,
                salt="usuario-confirmacao-email",
            )
        except signing.BadSignature:
            messages.error(
                request,
                "O link de confirmação é inválido ou foi alterado.",
            )
            return redirect(
                "admin:login",
            )

        try:
            usuario = UsuarioModel.objects.get(
                pk=dados["usuario_id"],
                email=dados["email"],
            )
        except UsuarioModel.DoesNotExist:
            messages.error(
                request,
                "Usuário não encontrado.",
            )
            return redirect(
                "admin:login",
            )

        if usuario.is_email_verified:
            messages.info(
                request,
                "Seu endereço de e-mail já foi confirmado.",
            )
            return redirect(
                "admin:login",
            )

        usuario.is_email_verified = True

        usuario.save(
            update_fields=[
                "is_email_verified",
            ],
        )

        messages.success(
            request,
            "E-mail confirmado com sucesso! Agora você pode acessar o sistema.",
        )
        return redirect(
            "admin:login",
        )
