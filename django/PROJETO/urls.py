#   ./django/PROJETO/urls.py

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path(
        "admin/",
        admin.site.urls,
    ),
    path(
        "api/",
        include("PROJETO.api.urls"),
    ),
    path(
        "usuario/",
        include("usuario.urls"),
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
