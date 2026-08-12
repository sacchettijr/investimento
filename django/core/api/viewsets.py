#   ./django/core/api/viewsets.py

from core.api import permissions
from core.api.pagination import DefaultPagination
from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated


class BaseModelViewSet(viewsets.ModelViewSet):
    # Um viewset base que fornece ações padrão.

    serializer_action_classes = {}
    permission_action_classes = {}

    pagination_class = DefaultPagination

    def get_serializer_class(
        self,
    ) -> type[serializers.BaseSerializer]:
        # Retorna a classe do serializer apropriada para a ação atual.
        return self.serializer_action_classes.get(
            self.action,
            serializers.ModelSerializer,
        )

    def get_permissions(
        self,
    ) -> list[permissions.BasePermission]:
        # Retorna a lista de permissões apropriadas para a ação atual.
        permission_classes = self.permission_action_classes.get(
            self.action,
            [IsAuthenticated],
        )
        return [permission() for permission in permission_classes]
