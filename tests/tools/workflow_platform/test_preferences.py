"""Testes de preferences.py (W-PROTO-FILA-4.1)."""

import json
from pathlib import Path

import pytest

from tools.workflow_platform.preferences import (
    DEFAULT_STALE_THRESHOLD_DAYS,
    PREFERENCES_FILENAME,
    Preferences,
    PreferencesLoadError,
    _preferences_path,
    load_preferences,
    save_preferences,
)


def _make_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    (repo / "tools" / "workflow_platform").mkdir(parents=True)
    return repo


def test_load_returns_defaults_when_file_missing(tmp_path: Path):
    repo = _make_repo(tmp_path)
    prefs = load_preferences(repo)
    assert prefs == Preferences()
    assert prefs.visible_roadmaps is None
    assert prefs.stale_branch_threshold_days == DEFAULT_STALE_THRESHOLD_DAYS


def test_save_then_load_roundtrip(tmp_path: Path):
    repo = _make_repo(tmp_path)
    original = Preferences(
        visible_roadmaps=["docs/ROADMAP.md", "products/x/ROADMAP.md"],
        stale_branch_threshold_days=14,
    )
    save_preferences(original, repo)
    loaded = load_preferences(repo)
    assert loaded == original


def test_save_writes_to_expected_path(tmp_path: Path):
    repo = _make_repo(tmp_path)
    save_preferences(Preferences(), repo)
    expected_path = _preferences_path(repo)
    assert expected_path.name == PREFERENCES_FILENAME
    assert expected_path.exists()


def test_load_malformed_json_raises(tmp_path: Path):
    repo = _make_repo(tmp_path)
    _preferences_path(repo).write_text("{{{not-json", encoding="utf-8")
    with pytest.raises(PreferencesLoadError):
        load_preferences(repo)


def test_load_top_level_array_raises(tmp_path: Path):
    repo = _make_repo(tmp_path)
    _preferences_path(repo).write_text("[]", encoding="utf-8")
    with pytest.raises(PreferencesLoadError):
        load_preferences(repo)


def test_load_visible_roadmaps_wrong_type_raises(tmp_path: Path):
    repo = _make_repo(tmp_path)
    _preferences_path(repo).write_text(
        json.dumps({"visible_roadmaps": "string-instead-of-list"}),
        encoding="utf-8",
    )
    with pytest.raises(PreferencesLoadError):
        load_preferences(repo)


def test_load_visible_roadmaps_with_non_string_element_raises(tmp_path: Path):
    repo = _make_repo(tmp_path)
    _preferences_path(repo).write_text(
        json.dumps({"visible_roadmaps": ["docs/ROADMAP.md", 42]}),
        encoding="utf-8",
    )
    with pytest.raises(PreferencesLoadError):
        load_preferences(repo)


def test_load_threshold_zero_raises(tmp_path: Path):
    repo = _make_repo(tmp_path)
    _preferences_path(repo).write_text(
        json.dumps({"stale_branch_threshold_days": 0}),
        encoding="utf-8",
    )
    with pytest.raises(PreferencesLoadError):
        load_preferences(repo)


def test_load_threshold_negative_raises(tmp_path: Path):
    repo = _make_repo(tmp_path)
    _preferences_path(repo).write_text(
        json.dumps({"stale_branch_threshold_days": -3}),
        encoding="utf-8",
    )
    with pytest.raises(PreferencesLoadError):
        load_preferences(repo)


def test_load_threshold_non_int_raises(tmp_path: Path):
    repo = _make_repo(tmp_path)
    _preferences_path(repo).write_text(
        json.dumps({"stale_branch_threshold_days": "seven"}),
        encoding="utf-8",
    )
    with pytest.raises(PreferencesLoadError):
        load_preferences(repo)


def test_save_atomicity_keeps_existing_file_intact_on_write_failure(
    tmp_path: Path, monkeypatch
):
    """Mock ``Path.write_text`` no .tmp para falhar; arquivo final fica intacto."""
    repo = _make_repo(tmp_path)
    initial = Preferences(visible_roadmaps=["a"], stale_branch_threshold_days=5)
    save_preferences(initial, repo)
    intact_content = _preferences_path(repo).read_text(encoding="utf-8")

    # Forçar exceção dentro de save_preferences durante o write_text do tmp.
    original_write = Path.write_text

    def fail_on_tmp(self, *a, **kw):
        if self.suffix == ".tmp":
            raise OSError("simulated disk full")
        return original_write(self, *a, **kw)

    monkeypatch.setattr(Path, "write_text", fail_on_tmp)

    new = Preferences(visible_roadmaps=["b"], stale_branch_threshold_days=99)
    with pytest.raises(OSError):
        save_preferences(new, repo)

    # Arquivo final permanece como estava antes da chamada falha
    assert _preferences_path(repo).read_text(encoding="utf-8") == intact_content


def test_load_empty_visible_roadmaps_list_is_valid(tmp_path: Path):
    """Lista vazia (operador desmarcou tudo) é estado válido — não levanta."""
    repo = _make_repo(tmp_path)
    _preferences_path(repo).write_text(
        json.dumps({"visible_roadmaps": []}),
        encoding="utf-8",
    )
    prefs = load_preferences(repo)
    assert prefs.visible_roadmaps == []
