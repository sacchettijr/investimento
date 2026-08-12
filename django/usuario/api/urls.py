#   ./django/usuario/api/urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from usuario.api.viewsets import UsuarioViewSet

router = DefaultRouter()

router.register(
    "",
    UsuarioViewSet,
    basename="usuario",
)

urlpatterns = [
    path(
        "",
        include(router.urls),
    ),
]
