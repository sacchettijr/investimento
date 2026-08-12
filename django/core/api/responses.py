#   ./django/core/api/responses.py
from rest_framework.response import Response


def success_response(data, status=200):
    # Retorna uma resposta de sucesso com os dados fornecidos.
    return Response(
        data,
        status=status,
    )


def error_response(message, status=400):
    # Retorna uma resposta de erro com a mensagem fornecida.
    return Response(
        {
            "success": False,
            "message": message,
        },
        status=status,
    )


def created_response(data):
    # Retorna uma resposta de sucesso com os dados fornecidos e status 201.
    return Response(
        data,
        status=201,
    )
