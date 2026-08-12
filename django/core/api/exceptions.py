#   ./django/core/api/exceptions.py
from typing import Any

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler


def exception_handler(
    exc: Exception,
    context: dict[str, Any],
) -> Response | None:
    #   Converte ValidationError do Django (levantada em Model.full_clean)
    #   para o formato de erro padrão do DRF, evitando 500 em regras de
    #   integridade validadas nos models.
    if isinstance(exc, DjangoValidationError):
        exc = DRFValidationError(_as_error_detail(exc))

    return drf_exception_handler(exc, context)


def _as_error_detail(exc: DjangoValidationError) -> Any:
    if hasattr(exc, "message_dict"):
        return exc.message_dict
    return exc.messages
