"""
Unit tests de load_product_context (E-POC-2.2).

Cobre:
- YAML válido (o padrão em products/ensaio/config/product.yaml)
- YAML ausente
- YAML malformado (inclui: campo focus vazio, YAML sintaticamente quebrado)
"""

from __future__ import annotations

from pathlib import Path

import pytest

from products.ensaio.app.product_config import (
    ProductConfigError,
    load_product_context,
)


def test_load_product_context_default_yaml_returns_non_empty_string():
    """O YAML canônico do Ensaio carrega e devolve string não-vazia."""
    context = load_product_context()
    assert isinstance(context, str)
    assert context.strip() != ""
    # Valor semântico: deve mencionar pesquisador/experimento/IMRaD.
    assert "pesquisador" in context.lower()
    assert "imrad" in context.lower()


def test_load_product_context_missing_file_raises(tmp_path: Path):
    missing = tmp_path / "does_not_exist.yaml"
    with pytest.raises(ProductConfigError) as exc:
        load_product_context(config_path=missing)
    assert "não encontrado" in str(exc.value)


def test_load_product_context_invalid_yaml_raises(tmp_path: Path):
    broken = tmp_path / "broken.yaml"
    broken.write_text("focus: [unterminated", encoding="utf-8")
    with pytest.raises(ProductConfigError) as exc:
        load_product_context(config_path=broken)
    assert "malformado" in str(exc.value)


def test_load_product_context_missing_focus_raises(tmp_path: Path):
    no_focus = tmp_path / "no_focus.yaml"
    no_focus.write_text("other: value\n", encoding="utf-8")
    with pytest.raises(ProductConfigError) as exc:
        load_product_context(config_path=no_focus)
    assert "focus" in str(exc.value)


def test_load_product_context_empty_focus_raises(tmp_path: Path):
    empty_focus = tmp_path / "empty_focus.yaml"
    empty_focus.write_text("focus: ''\n", encoding="utf-8")
    with pytest.raises(ProductConfigError):
        load_product_context(config_path=empty_focus)
