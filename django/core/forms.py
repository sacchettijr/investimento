#   ./django/usuario/forms.py
from typing import Any

from django import forms


class FormStyleMixin:
    fields: dict[str, forms.Field]

    def configurar_campo(
        self,
        nome: str,
        *,
        label: str | None = None,
        help_text: str | None = None,
        **attrs: Any,
    ) -> None:
        campo = self.fields[nome]

        classes = campo.widget.attrs.get("class", "")
        campo.widget.attrs["class"] = f"{classes} form-control".strip()

        if label is not None:
            campo.label = label

        if help_text is not None:
            campo.help_text = help_text

        campo.widget.attrs.update(attrs)

    def configurar_password(
        self,
        campo: str,
        *,
        label: str,
        placeholder: str,
        **attrs: Any,
    ) -> None:
        self.configurar_campo(
            campo,
            label=label,
            placeholder=placeholder,
            autocomplete="new-password",
            help_text="",
            spellcheck=False,
            **attrs,
        )

    def configurar_email(
        self,
        campo: str = "email",
        **attrs: Any,
    ) -> None:
        self.configurar_campo(
            campo,
            label="E-mail",
            placeholder="Digite seu e-mail",
            autocomplete="email",
            help_text="",
            spellcheck=False,
            autocapitalize="none",
            **attrs,
        )

    def configurar_nome(
        self,
        campo: str = "nome",
        **attrs: Any,
    ) -> None:
        self.configurar_campo(
            campo,
            label="Nome completo",
            placeholder="Digite seu nome completo",
            autocomplete="name",
            help_text="",
            **attrs,
        )
