#   ./django/PROJETO/api/urls.py
from django.urls import include, path

urlpatterns = [
    #   API de usuários
    path(
        "usuario/",
        include("usuario.api.urls"),
    ),
    #   API de investimentos e resgates
    path(
        "",
        include("investimento.api.urls"),
    ),
]
