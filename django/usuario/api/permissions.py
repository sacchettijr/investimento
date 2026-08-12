#   ./django/usuario/api/permissions.py
from rest_framework.permissions import BasePermission


class IsVerifiedEmail(BasePermission):
    #   Permissão personalizada para permitir apenas usuários com e-mail verificado.

    message: str = "Você precisa verificar seu e-mail para acessar este recurso."

    def has_permission(
        self,
        request,
        view,
    ) -> bool:

        return bool(
            request.user and request.user.is_authenticated and request.user.is_email_verified
        )
