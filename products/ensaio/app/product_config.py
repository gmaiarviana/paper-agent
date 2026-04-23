"""Loader do contexto de produto do Ensaio (E-POC-2.2).

Lê ``products/ensaio/config/product.yaml`` e retorna a string do campo
``focus``, pronta para ser injetada nos agentes do core via
``config.configurable.product_context``.

Este módulo NÃO importa nada de ``core/``; é responsabilidade do produto
conhecer seu próprio foco.
"""

from __future__ import annotations

from pathlib import Path

import yaml


class ProductConfigError(Exception):
    """Erro ao carregar ou validar o product.yaml do Ensaio."""


_CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "product.yaml"


def _resolve_config_path(path: Path | None = None) -> Path:
    return Path(path) if path is not None else _CONFIG_PATH


def load_product_context(path: Path | None = None) -> str:
    """Retorna a string do campo ``focus`` do product.yaml do Ensaio.

    Args:
        path: caminho alternativo ao ``product.yaml`` (usado por testes).

    Returns:
        String não-vazia com o foco do produto.

    Raises:
        ProductConfigError: quando o arquivo está ausente, é YAML inválido,
            não contém o campo ``focus`` ou o campo está vazio.
    """
    config_path = _resolve_config_path(path)

    if not config_path.exists():
        raise ProductConfigError(
            "Arquivo de configuração do produto Ensaio não encontrado: "
            f"{config_path}. Crie o arquivo com o campo obrigatório 'focus'."
        )

    try:
        with config_path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        raise ProductConfigError(
            f"YAML do produto Ensaio está malformado ({config_path}): {exc}"
        ) from exc

    if not isinstance(data, dict):
        raise ProductConfigError(
            f"YAML do produto Ensaio deve ser um mapeamento de chaves ({config_path})."
        )

    focus = data.get("focus")
    if not isinstance(focus, str) or not focus.strip():
        raise ProductConfigError(
            "Campo obrigatório 'focus' ausente ou vazio no product.yaml do Ensaio "
            f"({config_path})."
        )

    return focus.strip()
