#   ./django/investimento/api/permissions.py
from core.api.permissions import IsOwnerOrSuperUser


class ResgateIsOwnerOrSuperUser(IsOwnerOrSuperUser):
    #   O proprietário de um resgate é o dono do investimento associado.
    owner_field: str = "investimento__usuario"
