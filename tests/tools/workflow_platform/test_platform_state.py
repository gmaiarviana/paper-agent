"""Teste automatizável do ``PlatformState`` Reflex (W-PILOTO-UX-1.1/1.2).

Instancia o estado, roda ``on_load`` contra um ROADMAP fixture (via
monkeypatch — sem disco nem git) e assevera que ``roadmaps_all``/``queue_items``
são populados e que ``select_item``/``select_epic``/``toggle_roadmap`` mutam o
estado como esperado. Não sobe o frontend Reflex.

A paridade de ``detect_all`` com a versão Streamlit é garantida por construção
(mesma função ``queue.detect.detect_all_items``) e coberta por
``test_queue_detect.py`` / ``test_queue_determinism.py``.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pytest

from tools.workflow_platform.config_loader import PlatformConfig
from tools.workflow_platform.models import Epic, EpicState, ParsedRoadmap
from tools.workflow_platform.preferences import Preferences
from tools.workflow_platform.queue.detect import WorldState
from tools.workflow_platform.web.state import PlatformState


_ROADMAP_PATH = "docs/process/workflow/ROADMAP.md"
_FIXED_NOW = datetime(2026, 7, 4, 12, 0, 0)


def _fixture_roadmap(repo_root: Path) -> ParsedRoadmap:
    """Milestone com 3 épicos em 🔍 → apto a DISPATCH."""
    path = str(repo_root / _ROADMAP_PATH)
    epics = [
        Epic(
            id=f"W-FAKE-{n}",
            title=f"épico fake {n}",
            state=EpicState.DETAILED,
            roadmap_path=path,
            milestone_id="FAKE-MILESTONE",
        )
        for n in (1, 2, 3)
    ]
    return ParsedRoadmap(path=path, epics=epics, warnings=[])


@pytest.fixture
def state(monkeypatch, tmp_path) -> PlatformState:
    repo_root = tmp_path
    parsed = _fixture_roadmap(repo_root)

    def fake_load_config() -> PlatformConfig:
        return PlatformConfig(
            github_owner="gmaiarviana",
            github_repo="paper-agent",
            roadmaps=[parsed.path],
            repo_root=repo_root,
        )

    def fake_build_world_state(roadmaps, threshold_days=7, *, do_fetch=True):
        return WorldState(roadmaps=roadmaps, remote_branches=[], now=_FIXED_NOW), None

    monkeypatch.setattr("tools.workflow_platform.web.state.load_config", fake_load_config)
    monkeypatch.setattr(
        "tools.workflow_platform.web.state.parse_roadmap", lambda _p: parsed
    )
    monkeypatch.setattr(
        "tools.workflow_platform.web.state.load_preferences", lambda _root: Preferences()
    )
    monkeypatch.setattr(
        "tools.workflow_platform.web.state.build_world_state", fake_build_world_state
    )

    s = PlatformState(_reflex_internal_init=True)
    s.on_load()
    return s


def test_on_load_populates_roadmaps_and_queue(state: PlatformState):
    assert len(state.roadmaps_all) == 1
    assert len(state.roadmaps_all[0]["epics"]) == 3
    # 3 épicos 🔍 no mesmo milestone → exatamente 1 item DISPATCH.
    assert len(state.queue_items) == 1
    assert state.queue_items[0].item_type == "dispatch"
    assert "implementa" in state.queue_items[0].prompt.lower()


def test_grouped_queue_has_dispatch_bucket(state: PlatformState):
    groups = state.grouped_queue
    assert len(groups) == 1
    assert groups[0].label == "Dispatch"
    assert len(groups[0].cards) == 1


def test_select_item_sets_selection_and_detail(state: PlatformState):
    item_id = state.queue_items[0].id
    assert state.has_selected_item is False
    state.select_item(item_id)
    assert state.selected_item_id == item_id
    assert state.has_selected_item is True
    assert state.selected_queue_item.id == item_id
    state.close_item()
    assert state.selected_item_id == ""


def test_select_epic_builds_dispatch_detail(state: PlatformState):
    assert state.has_kanban_detail is False
    state.select_epic("W-FAKE-1")
    assert state.selected_epic_id == "W-FAKE-1"
    assert state.has_kanban_detail is True
    assert state.kanban_detail.kind == "dispatch"
    state.close_epic()
    assert state.kanban_detail.kind == ""


def test_kanban_columns_place_detailed_epics(state: PlatformState):
    columns = state.kanban_columns
    detailed = [c for c in columns if c.state_label.startswith("🔍")]
    assert detailed and detailed[0].count == 3


def test_toggle_roadmap_hides_and_reshows(state: PlatformState):
    rel = _ROADMAP_PATH
    assert rel in state.visible_roadmaps
    state.toggle_roadmap(rel)
    assert rel not in state.visible_roadmaps
    assert state.queue_items == []          # nada visível → nada detectado
    state.toggle_roadmap(rel)
    assert rel in state.visible_roadmaps
    assert len(state.queue_items) == 1
