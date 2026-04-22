"""
Loader do contexto de produto do Ensaio (E-POC-2.2).

Responsabilidade única: ler products/ensaio/config/product.yaml e retornar
a string do campo `focus`, pronta para ser injetada nos agentes do core via
`config.configurable.product_context`.

Contratos (ROADMAP E-POC-2.2):
- Expõe função `load_product_context() -> str`.
- Lança exceção com mensagem clara em PT-BR quando YAML ausente ou malformado.
- NÃO importa nada de `core/`.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import yaml


class ProductConfigError(Exception):
    """Erro ao carregar ou validar o product.yaml do Ensaio."""


_DEFAULT_CONFIG_PATH = Path(__file__).parent.parent / "config" / "product.yaml"


def load_product_context(config_path: Optional[Path] = None) -> str:
    """
    Lê o product.yaml do Ensaio e retorna o conteúdo do campo `focus`.

    Args:
        config_path: Caminho opcional para o YAML (útil em testes). Quando None,
            usa `products/ensaio/config/product.yaml`.

    Returns:
        String do campo `focus` (já com `strip()` aplicado).

    Raises:
        ProductConfigError: Quando o arquivo não existe, é YAML inválido, está
            vazio, ou não contém o campo `focus` como string não-vazia.
    """
    path = Path(config_path) if config_path is not None else _DEFAULT_CONFIG_PATH

    if not path.exists():
        raise ProductConfigError(
            f"Arquivo de contexto do produto não encontrado: {path}\n"
            "Esperado: products/ensaio/config/product.yaml"
        )

    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ProductConfigError(
            f"Não foi possível ler o arquivo de contexto do produto ({path}): {exc}"
        ) from exc

    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        raise ProductConfigError(
            f"YAML do produto malformado em {path}: {exc}"
        ) from exc

    if data is None:
        raise ProductConfigError(
            f"YAML do produto está vazio: {path}"
        )

    if not isinstance(data, dict):
        raise ProductConfigError(
            f"YAML do produto deve ter estrutura de objeto no nível raiz, "
            f"mas recebeu {type(data).__name__}: {path}"
        )

    focus = data.get("focus")
    if not isinstance(focus, str) or not focus.strip():
        raise ProductConfigError(
            f"Campo 'focus' obrigatório e deve ser string não-vazia em {path}"
        )

    return focus.strip()
