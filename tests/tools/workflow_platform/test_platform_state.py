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
from tools.workflow_platform.web.state import PlatformState, github_pr_url


_ROADMAP_PATH = "docs/process/workflow/ROADMAP.md"
_FIXED_NOW = datetime(2026, 7, 4, 12, 0, 0)


def _default_epics() -> list[Epic]:
    """Milestone com 3 épicos em 🔍 → apto a DISPATCH."""
    return [
        Epic(
            id=f"W-FAKE-{n}",
            title=f"épico fake {n}",
            state=EpicState.DETAILED,
            roadmap_path="",  # preenchido pelo factory com o path da fixture
            milestone_id="FAKE-MILESTONE",
        )
        for n in (1, 2, 3)
    ]


@pytest.fixture
def make_state(monkeypatch, tmp_path):
    """Factory: monta um ``PlatformState`` carregado a partir de uma lista de
    épicos (via monkeypatch — sem disco nem git). O ``roadmap_path`` de cada
    épico é normalizado para o path do ROADMAP fixture.
    """
    repo_root = tmp_path
    path = str(repo_root / _ROADMAP_PATH)

    def _make(epics: list[Epic]) -> PlatformState:
        for e in epics:
            e.roadmap_path = path
        parsed = ParsedRoadmap(path=path, epics=epics, warnings=[])

        def fake_load_config() -> PlatformConfig:
            return PlatformConfig(
                github_owner="gmaiarviana",
                github_repo="paper-agent",
                roadmaps=[path],
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

    return _make


@pytest.fixture
def state(make_state) -> PlatformState:
    return make_state(_default_epics())


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


# ---------------------------------------------------------------------------
# Roteamento de _build_kanban_detail por estado do épico (os 5 kinds).
# "dispatch" já é coberto por test_select_epic_builds_dispatch_detail.
# ---------------------------------------------------------------------------


def _epic(state: EpicState, **kwargs) -> Epic:
    base = dict(
        id="W-KIND-1",
        title="épico kind",
        state=state,
        roadmap_path="",
        milestone_id="FAKE-MILESTONE",
    )
    base.update(kwargs)
    return Epic(**base)


def test_kanban_detail_in_progress(make_state):
    # Com branch declarada → link_md aponta pra branch.
    s = make_state([_epic(EpicState.IN_PROGRESS, branch="feat/x")])
    s.select_epic("W-KIND-1")
    assert s.kanban_detail.kind == "in_progress"
    assert "feat/x" in s.kanban_detail.link_md
    assert s.kanban_detail.warn == ""

    # Sem branch → warn não vazio, sem link.
    s2 = make_state([_epic(EpicState.IN_PROGRESS, branch=None)])
    s2.select_epic("W-KIND-1")
    assert s2.kanban_detail.kind == "in_progress"
    assert s2.kanban_detail.warn != ""
    assert s2.kanban_detail.link_md == ""


def test_kanban_detail_in_review_fallback(make_state):
    # pr_url vazio + pr_number presente → FALLBACK monta a URL via github_pr_url.
    s = make_state([_epic(EpicState.IN_REVIEW, pr_url="", pr_number=7)])
    s.select_epic("W-KIND-1")
    assert s.kanban_detail.kind == "in_review"
    assert github_pr_url("gmaiarviana", "paper-agent", 7) in s.kanban_detail.link_md

    # Sem pr_url e sem pr_number → warn não vazio.
    s2 = make_state([_epic(EpicState.IN_REVIEW, pr_url=None, pr_number=None)])
    s2.select_epic("W-KIND-1")
    assert s2.kanban_detail.kind == "in_review"
    assert s2.kanban_detail.warn != ""
    assert s2.kanban_detail.link_md == ""


def test_kanban_detail_pre(make_state):
    s = make_state([_epic(EpicState.CRITERIA)])
    s.select_epic("W-KIND-1")
    assert s.kanban_detail.kind == "pre"
    # CRITERIA → get_next_step traz guidance e build_refinement_prompt traz prompt.
    assert s.kanban_detail.guidance != ""
    assert s.kanban_detail.refine_prompt != ""


def test_kanban_detail_done(make_state):
    s = make_state([_epic(EpicState.DONE, body_excerpt="resumo…")])
    s.select_epic("W-KIND-1")
    assert s.kanban_detail.kind == "done"
    assert s.kanban_detail.excerpt == "resumo…"
