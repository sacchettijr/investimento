# ./django/usuario/urls.py
from django.urls import path
from django.urls.resolvers import URLPattern

from usuario.views import UsuarioConfirmarEmailView

app_name = "usuario"


urlpatterns: list[URLPattern] = [
    path(
        "confirmar-email/<str:token>/",
        UsuarioConfirmarEmailView.as_view(),
        name="usuario_confirmar_email",
    ),
]
