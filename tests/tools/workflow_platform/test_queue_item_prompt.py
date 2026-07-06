"""Testes dos builders de prompt por tipo de QueueItem (W-PROTO-FILA-2.2)."""

from datetime import datetime
import re

import pytest

from tools.workflow_platform.models import Epic, EpicState
from tools.workflow_platform.prompts.queue_item import build_prompt_for_item
from tools.workflow_platform.job_queue.models import (
    BranchPointer,
    CleanupPointer,
    EpicPointer,
    ItemType,
    PRPointer,
    QueueItem,
    RefinePointer,
)


_NOW = datetime(2026, 4, 30, 12, 0, 0)


def _make(item_type: ItemType, pointer, **overrides) -> QueueItem:
    base = dict(
        id="x",
        type=item_type,
        title="t",
        context="c",
        expected_action="a",
        source_pointer=pointer,
        detected_at=_NOW,
    )
    base.update(overrides)
    return QueueItem(**base)


# ----- DISPATCH delega ao build_dispatch_prompt do PLAT-3.1 -----

def test_dispatch_delegates_to_build_dispatch_prompt():
    pointer = EpicPointer(
        epic_id="E1",
        milestone_id="MIL-A",
        roadmap_path="x.md",
    )
    item = _make(ItemType.DISPATCH, pointer)
    epic1 = Epic(id="E1", title="t1", state=EpicState.DETAILED, roadmap_path="x.md", milestone_id="MIL-A")
    epic2 = Epic(id="E2", title="t2", state=EpicState.DETAILED, roadmap_path="x.md", milestone_id="MIL-A")
    prompt = build_prompt_for_item(
        item,
        all_epics_by_milestone={"MIL-A": [epic1, epic2]},
        epic_lookup={"E1": epic1, "E2": epic2},
    )
    assert prompt == "implementa o épico E1"


def test_dispatch_without_lookup_falls_back_to_minimal_text():
    pointer = EpicPointer(
        epic_id="E9",
        milestone_id="MIL-X",
        roadmap_path="x.md",
    )
    item = _make(ItemType.DISPATCH, pointer)
    prompt = build_prompt_for_item(item)
    assert prompt == "implementa o épico E9"


# ----- REVIEW -----

def test_review_contains_pr_number_and_url_literally():
    pointer = PRPointer(
        pr_number=93,
        pr_url="https://github.com/gmaiarviana/paper-agent/pull/93",
        milestone_id="MIL-X",
    )
    item = _make(ItemType.REVIEW, pointer)
    prompt = build_prompt_for_item(item)
    assert "PR #93" in prompt
    assert "https://github.com/gmaiarviana/paper-agent/pull/93" in prompt
    assert "Copilot" in prompt


# ----- REFINE -----

def test_refine_delegates_to_build_refinement_prompt():
    pointer = RefinePointer(
        epic_id="W-MVP-DOC-1",
        roadmap_path="x.md",
        current_state=EpicState.SKETCHED,
        target_state=EpicState.CRITERIA,
    )
    item = _make(ItemType.REFINE, pointer)
    epic = Epic(
        id="W-MVP-DOC-1",
        title="quebrar planning_guidelines",
        state=EpicState.SKETCHED,
        roadmap_path="x.md",
        milestone_id="MVP-WORKFLOW-DOC",
    )
    prompt = build_prompt_for_item(item, epic_lookup={"W-MVP-DOC-1": epic})
    assert "W-MVP-DOC-1" in prompt
    assert "📋" in prompt or "Critérios" in prompt


def test_refine_without_lookup_falls_back():
    pointer = RefinePointer(
        epic_id="EX",
        roadmap_path="r.md",
        current_state=EpicState.SKETCHED,
        target_state=EpicState.CRITERIA,
    )
    item = _make(ItemType.REFINE, pointer)
    prompt = build_prompt_for_item(item)
    assert "EX" in prompt
    assert "r.md" in prompt


# ----- CLEANUP -----

def test_cleanup_contains_epic_id_title_and_path():
    pointer = CleanupPointer(
        epic_id="W-PROTO-PLAT-1",
        roadmap_path="docs/process/workflow/ROADMAP.md",
        title="Scaffold de plataforma",
    )
    item = _make(ItemType.CLEANUP, pointer)
    prompt = build_prompt_for_item(item)
    assert "W-PROTO-PLAT-1" in prompt
    assert "Scaffold de plataforma" in prompt
    assert "docs/process/workflow/ROADMAP.md" in prompt
    assert "skills/cleanup/skill.md" in prompt


# ----- STALE_BRANCH -----

def test_stale_branch_contains_name_days_and_three_options():
    pointer = BranchPointer(
        branch_name="claude/foo-bar",
        last_commit_at=_NOW,
        days_stale=12,
    )
    item = _make(ItemType.STALE_BRANCH, pointer)
    prompt = build_prompt_for_item(item)
    assert "claude/foo-bar" in prompt
    assert "12 dias" in prompt
    assert "(a)" in prompt
    assert "(b)" in prompt
    assert "(c)" in prompt
    assert "git push origin --delete claude/foo-bar" in prompt


# ----- regra global: nenhum placeholder pendente -----

@pytest.mark.parametrize(
    "item_type,pointer",
    [
        (ItemType.REVIEW,       PRPointer(pr_number=1, pr_url="u", milestone_id="X")),
        (ItemType.CLEANUP,      CleanupPointer(epic_id="E", roadmap_path="r", title="t")),
        (ItemType.STALE_BRANCH, BranchPointer(branch_name="b", last_commit_at=_NOW, days_stale=5)),
    ],
)
def test_no_unsubstituted_placeholder(item_type, pointer):
    item = _make(item_type, pointer)
    prompt = build_prompt_for_item(item)
    # Não deve haver tokens em <UPPER_CASE> não substituídos
    leftover = re.search(r"<[A-Z][A-Z_]+>", prompt)
    assert leftover is None, f"placeholder não substituído: {leftover.group()!r}"
