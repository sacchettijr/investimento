#   ./django/core/models.py
from typing import Any

from django.conf import settings
from django.db import models

from core.current_user import get_current_user


class BaseModel(models.Model):
    #   CLASSE ABSTRATA PARA HERANÇA DE MODELOS
    criado_em = models.DateTimeField(
        auto_now_add=True,
    )
    modificado_em = models.DateTimeField(
        auto_now=True,
    )
    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        editable=False,
        related_name="%(class)s_criados",
        db_index=True,
    )
    modificado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        editable=False,
        related_name="%(class)s_modificados",
        db_index=True,
    )

    class Meta:
        abstract = True

    def save(
        self,
        *args: Any,
        **kwargs: Any,
    ):
        user = get_current_user()
        if user:
            self.criado_por = self.criado_por or user
            self.modificado_por = user
        return super().save(*args, **kwargs)
