#   ./django/investimento/api/urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from investimento.api.viewsets import InvestimentoViewSet, ResgateViewSet

router = DefaultRouter()

router.register(
    "investimentos",
    InvestimentoViewSet,
    basename="investimento",
)

router.register(
    "resgates",
    ResgateViewSet,
    basename="resgate",
)

urlpatterns = [
    path(
        "",
        include(router.urls),
    ),
]
