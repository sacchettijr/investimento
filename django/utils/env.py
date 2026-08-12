#   ./django/utils/env.py
import os


def env(
    name: str,
    default: str | None = None,
) -> str:
    value: str | None = os.getenv(name)
    if value is None:
        if default is not None:
            return default
        raise RuntimeError(f"Variável de ambiente '{name}' não definida.")
    return value


def env_bool(
    name: str,
    default: bool = False,
) -> bool:
    value = (
        env(
            name,
            default=str(default),
        )
        .strip()
        .lower()
    )

    if value in {
        "true",
        "1",
        "yes",
        "y",
        "on",
    }:
        return True

    if value in {
        "false",
        "0",
        "no",
        "n",
        "off",
    }:
        return False

    raise ValueError(
        f"Valor inválido para a variável de ambiente '{name}': {value!r}. Use true ou false."
    )


def env_int(
    name: str,
    default: int | None = None,
) -> int:
    value = env(
        name,
        default=(str(default) if default is not None else None),
    )

    try:
        return int(value)
    except ValueError as exc:
        raise ValueError(
            f"Valor inválido para a variável de ambiente "
            f"'{name}': {value!r}. "
            f"Esperado um número inteiro."
        ) from exc


def env_list(
    name: str,
    default: list[str] | None = None,
    separator: str = ",",
) -> list[str]:
    default_value = separator.join(default) if default is not None else None

    value = env(
        name,
        default=default_value,
    )

    return [item.strip() for item in value.split(separator) if item.strip()]
