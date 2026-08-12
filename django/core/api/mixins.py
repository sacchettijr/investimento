#   ./django/core/api/mixins.py

from django.db.models import QuerySet
from rest_framework.filters import (
    OrderingFilter,
    SearchFilter,
)
from rest_framework.request import Request

# ============================================
#   MIXIN DE FILTRO POR PROPRIETÁRIO
# ============================================


class OwnerQuerysetMixin:
    #   Um mixin que filtra o queryset para retornar apenas
    #   os objetos pertencentes ao usuário autenticado.

    owner_field: str = "usuario"

    request: Request

    def filter_queryset_by_owner(
        self,
        queryset: QuerySet,
    ) -> QuerySet:
        # Retorna o queryset filtrado para o usuário autenticado.

        if self.request.user.is_superuser:
            return queryset

        return queryset.filter(
            **{
                self.owner_field: self.request.user,
            },
        )


# ============================================
#   MIXIN DE PESQUISA E ORDENAÇÃO
# ============================================


class SearchOrderingMixin:
    # Um mixin que adiciona suporte a pesquisa e ordenação para viewsets.

    filter_backends = [
        SearchFilter,
        OrderingFilter,
    ]

    search_fields: tuple[str, ...] = ()
    ordering_fields: tuple[str, ...] = ()
    ordering: tuple[str, ...] = ()
