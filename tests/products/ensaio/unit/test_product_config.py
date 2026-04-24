"""Unit tests for the Ensaio product_config loader (E-POC-2.2)."""

from pathlib import Path

import pytest

from products.ensaio.app.product_config import (
    ProductConfigError,
    load_product_context,
)


def test_loads_focus_from_valid_yaml(tmp_path: Path) -> None:
    config = tmp_path / "product.yaml"
    config.write_text("focus: |\n  Experimentos em IA agêntica.\n", encoding="utf-8")

    result = load_product_context(config)

    assert result == "Experimentos em IA agêntica."


def test_raises_when_file_missing(tmp_path: Path) -> None:
    missing = tmp_path / "does-not-exist.yaml"

    with pytest.raises(ProductConfigError) as excinfo:
        load_product_context(missing)

    assert "não encontrado" in str(excinfo.value)


def test_raises_when_yaml_malformed(tmp_path: Path) -> None:
    config = tmp_path / "product.yaml"
    config.write_text("focus: [unterminated\n  - item", encoding="utf-8")

    with pytest.raises(ProductConfigError) as excinfo:
        load_product_context(config)

    assert "malformado" in str(excinfo.value)


def test_raises_when_focus_missing(tmp_path: Path) -> None:
    config = tmp_path / "product.yaml"
    config.write_text("other_field: something\n", encoding="utf-8")

    with pytest.raises(ProductConfigError) as excinfo:
        load_product_context(config)

    assert "focus" in str(excinfo.value)


def test_raises_when_focus_empty(tmp_path: Path) -> None:
    config = tmp_path / "product.yaml"
    config.write_text("focus: '   '\n", encoding="utf-8")

    with pytest.raises(ProductConfigError):
        load_product_context(config)


def test_default_path_loads_real_product_yaml() -> None:
    """Garante que o product.yaml do Ensaio (shipped no repo) é carregável."""
    result = load_product_context()

    assert isinstance(result, str)
    assert result.strip(), "focus do product.yaml não pode ser vazio"
    assert "ICT" in result or "pesquisador" in result.lower()


def test_product_config_does_not_import_core() -> None:
    """E-POC-2.2 exige que o loader não importe do core."""
    import products.ensaio.app.product_config as module

    source = Path(module.__file__).read_text(encoding="utf-8")
    for line in source.splitlines():
        stripped = line.strip()
        if stripped.startswith("import core") or stripped.startswith("from core"):
            pytest.fail(f"product_config importou do core: {line}")
