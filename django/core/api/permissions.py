#   ./django/core/api/permissions.py

from rest_framework.permissions import (
    SAFE_METHODS,
    BasePermission,
)

# ===========================================
#   APENAS SUPERUSUÁRIOS
# ===========================================


class IsSuperUser(BasePermission):
    #   Permissão apenas para superusuários.

    message: str = "Apenas superusuários podem acessar este recurso."

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)


# ===========================================
#   APENAS LEITURA OU SUPERUSUÁRIOS
# ===========================================


class ReadOnlyOrSuperUser(BasePermission):
    #   Permite apenas usuários autenticados e escrita apenas para superusuários.

    message: str = "Apenas superusuários podem modificar este recurso."

    def has_permission(
        self,
        request,
        view,
    ) -> bool:
        if not request.user.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)

        return request.user.is_superuser


# ===========================================
#   APENAS PROPRIETÁRIO DO RECURSO
# ===========================================


class IsOwner(BasePermission):
    #   Permite acesso para o proprietário do objeto.

    owner_field: str = "usuario"
    message: str = "Você não possui permissão para acessar este recurso."

    def has_object_permission(
        self,
        request,
        view,
        obj,
    ) -> bool:
        if not request.user.is_authenticated:
            return False

        #   Suporta travessia de relacionamentos com "__", assim como
        #   o OwnerQuerysetMixin (ex.: "investimento__usuario").
        owner = obj
        for attribute in self.owner_field.split("__"):
            owner = getattr(owner, attribute, None)
            if owner is None:
                return False

        return bool(owner == request.user)


# ===========================================
#   PROPRIETÁRIO DO RECURSO OU SUPERUSUÁRIOS
# ===========================================


class IsOwnerOrSuperUser(IsOwner):
    #   Permite acesso para o proprietário ou superusuários.

    message: str = "Você não tem permissão para este recurso."

    def has_object_permission(
        self,
        request,
        view,
        obj,
    ) -> bool:
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        return super().has_object_permission(
            request,
            view,
            obj,
        )


# ===========================================
#   APENAS LEITURA OU PROPRIETÁRIO DO RECURSO OU SUPERUSUÁRIOS
# ===========================================


class ReadOnlyOrOwnerOrSuperUser(IsOwner):
    #   Permite apenas leitura para qualquer usuário autenticado, mas escrita
    #   apenas para o proprietário do recurso ou superusuários.

    message: str = "Apenas o proprietário do recurso ou superusuários podem modificar este recurso."

    def has_object_permission(
        self,
        request,
        view,
        obj,
    ) -> bool:
        if not request.user.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            return True

        return super().has_object_permission(
            request,
            view,
            obj,
        )
