#   ./django/core/management/commands/create_admin.py

from typing import Type, cast

from django.core.management.base import BaseCommand
from usuario.models import UsuarioModel
from utils.env import env


class Command(BaseCommand):
    help = "Cria um superusuário caso ele não exista."

    def handle(self, *args, **options):

        User = cast(Type[UsuarioModel], UsuarioModel)

        nome = env("DJANGO_SUPERUSER_NAME")
        email = env("DJANGO_SUPERUSER_EMAIL")
        password = env("DJANGO_SUPERUSER_PASSWORD")

        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING(f"Superusuário '{email}' já existe."))
            return

        User.objects.create_superuser(
            nome=nome,
            email=email,
            password=password,
        )

        self.stdout.write(self.style.SUCCESS(f"Superusuário '{email}' criado com sucesso."))
