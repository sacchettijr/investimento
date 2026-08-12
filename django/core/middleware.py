#   ./django/core/middleware.py
from typing import cast

from django.http import HttpRequest, HttpResponse
from usuario.models import UsuarioModel

from core.current_user import set_current_user


class CurrentUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(
        self,
        request: HttpRequest,
    ) -> HttpResponse:
        if request.user.is_authenticated:
            set_current_user(
                cast(
                    UsuarioModel,
                    request.user,
                )
            )
        else:
            set_current_user(None)

        try:
            response = self.get_response(request)
        finally:
            set_current_user(None)

        return response
