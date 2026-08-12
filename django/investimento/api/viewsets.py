#   ./django/investimento/api/viewsets.py
from core.api.mixins import OwnerQuerysetMixin, SearchOrderingMixin
from core.api.permissions import IsOwnerOrSuperUser
from core.api.viewsets import BaseModelViewSet
from django.db.models import QuerySet
from rest_framework import permissions, serializers

from investimento.api.permissions import ResgateIsOwnerOrSuperUser
from investimento.api.serializers import InvestimentoSerializer, ResgateSerializer
from investimento.models import InvestimentoModel, ResgateModel

# ===================================================
#   VIEWSET DE INVESTIMENTO
# ===================================================


class InvestimentoViewSet(
    OwnerQuerysetMixin,
    SearchOrderingMixin,
    BaseModelViewSet,
):
    #   Criação, consulta e listagem de investimentos do usuário autenticado.

    queryset = InvestimentoModel.objects.select_related(
        "usuario",
        "resgate",
    ).all()

    #   Investimentos não são editados nem removidos pela API.
    http_method_names = [
        "get",
        "post",
    ]

    search_fields = ("descricao",)

    ordering_fields = (
        "data_inicio",
        "valor_investido",
        "criado_em",
    )

    ordering = ("-criado_em",)

    serializer_action_classes = {
        "list": InvestimentoSerializer,
        "retrieve": InvestimentoSerializer,
        "create": InvestimentoSerializer,
    }

    permission_action_classes = {
        "list": [
            permissions.IsAuthenticated,
        ],
        "create": [
            permissions.IsAuthenticated,
        ],
        "retrieve": [
            permissions.IsAuthenticated,
            IsOwnerOrSuperUser,
        ],
    }

    def get_queryset(
        self,
    ) -> QuerySet[InvestimentoModel]:
        return self.filter_queryset_by_owner(
            super().get_queryset(),
        )

    def get_serializer_class(
        self,
    ) -> type[serializers.BaseSerializer]:
        return self.serializer_action_classes.get(
            self.action,
            InvestimentoSerializer,
        )

    def get_permissions(
        self,
    ) -> list[permissions.BasePermission]:
        permission_classes = self.permission_action_classes.get(
            self.action,
            [permissions.IsAuthenticated],
        )
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer: serializers.BaseSerializer) -> None:
        serializer.save(usuario=self.request.user)


# ===================================================
#   VIEWSET DE RESGATE
# ===================================================


class ResgateViewSet(
    OwnerQuerysetMixin,
    SearchOrderingMixin,
    BaseModelViewSet,
):
    #   Criação e consulta de resgates dos investimentos do usuário autenticado.

    queryset = ResgateModel.objects.select_related(
        "investimento",
        "investimento__usuario",
    ).all()

    #   Resgates não são editados nem removidos pela API (imutáveis).
    http_method_names = ["get", "post"]

    #   O proprietário do resgate é acessado através do investimento.
    owner_field = "investimento__usuario"

    ordering_fields = (
        "data_resgate",
        "criado_em",
    )

    ordering = ("-criado_em",)

    serializer_action_classes = {
        "list": ResgateSerializer,
        "retrieve": ResgateSerializer,
        "create": ResgateSerializer,
    }

    permission_action_classes = {
        "list": [permissions.IsAuthenticated],
        "create": [permissions.IsAuthenticated],
        "retrieve": [permissions.IsAuthenticated, ResgateIsOwnerOrSuperUser],
    }

    def get_queryset(self) -> QuerySet[ResgateModel]:
        return self.filter_queryset_by_owner(super().get_queryset())

    def get_serializer_class(self) -> type[serializers.BaseSerializer]:
        return self.serializer_action_classes.get(
            self.action,
            ResgateSerializer,
        )

    def get_permissions(self) -> list[permissions.BasePermission]:
        permission_classes = self.permission_action_classes.get(
            self.action,
            [permissions.IsAuthenticated],
        )
        return [permission() for permission in permission_classes]
