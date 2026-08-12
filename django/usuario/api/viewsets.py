#   ./django/usuario/api/viewsets.py
from core.api.permissions import (
    IsOwnerOrSuperUser,
)
from core.api.viewsets import BaseModelViewSet
from rest_framework import permissions, serializers
from rest_framework.decorators import action
from rest_framework.filters import (
    OrderingFilter,
    SearchFilter,
)
from rest_framework.response import Response
from usuario.api.permissions import (
    IsVerifiedEmail,
)
from usuario.api.serializers import (
    UsuarioAdminSerializer,
    UsuarioConfirmEmailSerializer,
    UsuarioCreateSerializer,
    UsuarioDetailSerializer,
    UsuarioListSerializer,
    UsuarioMeSerializer,
    UsuarioReenviarConfirmacaoEmailSerializer,
    UsuarioSaldoSerializer,
    UsuarioSerializer,
    UsuarioUpdatePasswordSerializer,
    UsuarioUpdateSerializer,
)
from usuario.models import UsuarioModel


class UsuarioViewSet(BaseModelViewSet):
    queryset = UsuarioModel.objects.all()

    http_method_names = [
        "get",
        "post",
        "put",
        "patch",
        "delete",
    ]

    filter_backends = [
        SearchFilter,
        OrderingFilter,
    ]

    search_fields = (
        "nome",
        "email",
    )

    ordering_fields = (
        "nome",
        "email",
        "criado_em",
        "modificado_em",
    )

    ordering = ("nome",)

    serializer_action_classes = {
        "list": UsuarioListSerializer,
        "retrieve": UsuarioDetailSerializer,
        "create": UsuarioCreateSerializer,
        "update": UsuarioUpdateSerializer,
        "partial_update": UsuarioUpdateSerializer,
        "me": UsuarioMeSerializer,
        "saldo": UsuarioSaldoSerializer,
        "change_password": UsuarioUpdatePasswordSerializer,
        "confirm_email": UsuarioConfirmEmailSerializer,
        "resend_confirmation_email": UsuarioReenviarConfirmacaoEmailSerializer,
    }

    permission_action_classes = {
        "create": [
            permissions.AllowAny,
        ],
        "list": [
            permissions.IsAuthenticated,
        ],
        "retrieve": [
            permissions.IsAuthenticated,
            IsOwnerOrSuperUser,
        ],
        "update": [
            permissions.IsAuthenticated,
            IsOwnerOrSuperUser,
        ],
        "partial_update": [
            permissions.IsAuthenticated,
            IsOwnerOrSuperUser,
        ],
        "destroy": [
            permissions.IsAuthenticated,
            IsOwnerOrSuperUser,
        ],
        "saldo": [
            permissions.IsAuthenticated,
            IsVerifiedEmail,
        ],
        "me": [
            permissions.IsAuthenticated,
        ],
    }

    def get_queryset(
        self,
    ):
        queryset = super().get_queryset()

        if self.request.user.is_superuser:
            return queryset

        return queryset.filter(
            pk=self.request.user.pk,
        )

    def get_serializer_class(
        self,
    ) -> type[serializers.BaseSerializer]:
        if self.request.user.is_superuser and self.action in {
            "list",
            "retrieve",
        }:
            return UsuarioAdminSerializer

        return self.serializer_action_classes.get(
            self.action,
            UsuarioSerializer,
        )

    def get_permissions(
        self,
    ) -> list[permissions.BasePermission]:
        permission_classes = self.permission_action_classes.get(
            self.action,
            [
                permissions.IsAuthenticated,
            ],
        )
        return [permission() for permission in permission_classes]

    def perform_create(
        self,
        serializer: serializers.BaseSerializer,
    ) -> None:
        serializer.save()

    def perform_update(
        self,
        serializer: serializers.BaseSerializer,
    ) -> None:
        serializer.save()

    def perform_destroy(
        self,
        instance: UsuarioModel,
    ) -> None:
        instance.delete()

    @action(
        detail=False,
        methods=["get"],
        url_path="saldo",
    )
    def saldo(
        self,
        request,
    ) -> Response:
        #   Retorna o saldo do usuário autenticado.
        serializer = self.get_serializer(
            request.user,
        )
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["get"],
        url_path="me",
    )
    def me(
        self,
        request,
    ) -> Response:
        #   Retorna os dados do usuário autenticado.
        serializer = self.get_serializer(
            request.user,
        )
        return Response(serializer.data)
