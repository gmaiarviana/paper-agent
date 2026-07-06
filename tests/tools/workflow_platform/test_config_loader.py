"""Testes do carregador de config da plataforma."""

from pathlib import Path

import pytest

from tools.workflow_platform.config_loader import load_config


VALID_YAML = """github:
  owner: someone
  repo: somerepo
roadmaps:
  - docs/ROADMAP.md
  - products/ensaio/ROADMAP.md
"""


def test_loads_valid_config(tmp_path: Path):
    repo_root = tmp_path
    (repo_root / "tools" / "workflow_platform").mkdir(parents=True)
    (repo_root / "docs").mkdir()
    (repo_root / "products" / "ensaio").mkdir(parents=True)
    cfg = repo_root / "tools" / "workflow_platform" / "config.yaml"
    cfg.write_text(VALID_YAML, encoding="utf-8")

    result = load_config(repo_root=repo_root, config_path=cfg)

    assert result.github_owner == "someone"
    assert result.github_repo == "somerepo"
    assert len(result.roadmaps) == 2
    for path in result.roadmaps:
        assert Path(path).is_absolute()
    assert Path(result.roadmaps[0]).as_posix().endswith("docs/ROADMAP.md")


def test_missing_field_raises(tmp_path: Path):
    repo_root = tmp_path
    cfg_dir = repo_root / "tools" / "workflow_platform"
    cfg_dir.mkdir(parents=True)
    cfg = cfg_dir / "config.yaml"
    cfg.write_text("github:\n  owner: foo\n", encoding="utf-8")

    with pytest.raises(ValueError) as exc:
        load_config(repo_root=repo_root, config_path=cfg)
    assert "github.repo" in str(exc.value) or "roadmaps" in str(exc.value)


def test_missing_file_raises(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        load_config(repo_root=tmp_path, config_path=tmp_path / "ausente.yaml")


def test_real_repo_config_loads():
    """Garante que o config.yaml versionado é válido."""
    result = load_config()
    assert result.github_owner == "gmaiarviana"
    assert result.github_repo == "paper-agent"
    assert len(result.roadmaps) >= 2
