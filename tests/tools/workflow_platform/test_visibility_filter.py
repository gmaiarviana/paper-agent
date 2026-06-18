"""Testes do helper de filtro por ROADMAP visível (W-PROTO-FILA-4.2)."""

from pathlib import Path

import pytest

from tools.workflow_platform.models import ParsedRoadmap
from tools.workflow_platform.preferences import (
    Preferences,
    apply_visibility_filter,
)


def _roadmap(rel_path: str, repo_root: Path) -> ParsedRoadmap:
    return ParsedRoadmap(path=str(repo_root / rel_path))


def test_none_returns_input_intact(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    roadmaps = [
        _roadmap("docs/ROADMAP.md", repo),
        _roadmap("products/x/ROADMAP.md", repo),
    ]
    prefs = Preferences(visible_roadmaps=None)
    result = apply_visibility_filter(roadmaps, prefs, repo)
    assert result == roadmaps


def test_list_filters_to_matching_paths(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    a = _roadmap("docs/ROADMAP.md", repo)
    b = _roadmap("products/x/ROADMAP.md", repo)
    c = _roadmap("products/y/ROADMAP.md", repo)
    d = _roadmap("docs/process/workflow/ROADMAP.md", repo)
    prefs = Preferences(
        visible_roadmaps=["docs/ROADMAP.md", "products/y/ROADMAP.md"],
    )
    result = apply_visibility_filter([a, b, c, d], prefs, repo)
    assert result == [a, c]


def test_path_not_in_configured_is_silently_ignored(tmp_path: Path):
    """Path em ``prefs`` que não casa com nenhum ROADMAP é ignorado sem erro."""
    repo = tmp_path / "repo"
    repo.mkdir()
    a = _roadmap("docs/ROADMAP.md", repo)
    prefs = Preferences(
        visible_roadmaps=["docs/ROADMAP.md", "phantom/ROADMAP.md"],
    )
    result = apply_visibility_filter([a], prefs, repo)
    assert result == [a]


def test_empty_list_returns_empty(tmp_path: Path):
    """Operador desmarcou tudo — kanban/fila ficam vazios, é estado válido."""
    repo = tmp_path / "repo"
    repo.mkdir()
    a = _roadmap("docs/ROADMAP.md", repo)
    b = _roadmap("products/x/ROADMAP.md", repo)
    prefs = Preferences(visible_roadmaps=[])
    result = apply_visibility_filter([a, b], prefs, repo)
    assert result == []


def test_path_outside_repo_root_is_ignored(tmp_path: Path):
    """ROADMAP cujo path é absoluto fora do repo_root → ignorado silenciosamente."""
    repo = tmp_path / "repo"
    repo.mkdir()
    other = tmp_path / "other"
    other.mkdir()
    inside = _roadmap("docs/ROADMAP.md", repo)
    outside = ParsedRoadmap(path=str(other / "X.md"))
    prefs = Preferences(visible_roadmaps=["docs/ROADMAP.md"])
    result = apply_visibility_filter([inside, outside], prefs, repo)
    assert result == [inside]
