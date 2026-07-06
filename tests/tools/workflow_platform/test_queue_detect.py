"""Testes de detecção (W-PROTO-FILA-1.2)."""

from datetime import datetime, timedelta

import pytest

from tools.workflow_platform.models import (
    Epic,
    EpicState,
    Milestone,
    ParsedRoadmap,
)
from tools.workflow_platform.job_queue.detect import (
    WorldState,
    detect_all_items,
    detect_cleanup_items,
    detect_dispatch_items,
    detect_refine_items,
    detect_review_items,
    detect_stale_branch_items,
)
from tools.workflow_platform.job_queue.git_helper import RemoteBranch
from tools.workflow_platform.job_queue.models import (
    BranchPointer,
    CleanupPointer,
    EpicPointer,
    ItemType,
    PRPointer,
    RefinePointer,
)


_NOW = datetime(2026, 4, 30, 12, 0, 0)
_PATH = "docs/process/workflow/ROADMAP.md"


def _epic(epic_id: str, state: EpicState, **kw) -> Epic:
    defaults = dict(
        id=epic_id,
        title=f"épico {epic_id}",
        state=state,
        roadmap_path=_PATH,
        milestone_id=kw.pop("milestone_id", "M-X"),
    )
    defaults.update(kw)
    return Epic(**defaults)


def _roadmap(epics: list[Epic], milestones: list[Milestone] | None = None) -> ParsedRoadmap:
    return ParsedRoadmap(path=_PATH, epics=epics, milestones=milestones or [])


def _state(
    roadmaps: list[ParsedRoadmap] | None = None,
    branches: list[RemoteBranch] | None = None,
    now: datetime = _NOW,
) -> WorldState:
    return WorldState(
        roadmaps=roadmaps or [],
        remote_branches=branches or [],
        now=now,
    )


# ----- DISPATCH -----

def test_dispatch_with_all_detailed_generates_one_item():
    epics = [
        _epic("E1", EpicState.DETAILED, milestone_id="MIL-A"),
        _epic("E2", EpicState.DETAILED, milestone_id="MIL-A"),
    ]
    state = _state(roadmaps=[_roadmap(epics)])
    items = detect_dispatch_items(state)
    assert len(items) == 1
    item = items[0]
    assert item.type == ItemType.DISPATCH
    assert item.id == "dispatch:MIL-A"
    assert isinstance(item.source_pointer, EpicPointer)
    assert item.source_pointer.epic_ids == ["E1", "E2"]


def test_dispatch_with_one_in_progress_does_not_generate():
    epics = [
        _epic("E1", EpicState.DETAILED, milestone_id="MIL-A"),
        _epic("E2", EpicState.IN_PROGRESS, milestone_id="MIL-A"),
    ]
    state = _state(roadmaps=[_roadmap(epics)])
    assert detect_dispatch_items(state) == []


def test_dispatch_with_one_in_review_does_not_generate():
    epics = [
        _epic("E1", EpicState.DETAILED, milestone_id="MIL-A"),
        _epic("E2", EpicState.IN_REVIEW, milestone_id="MIL-A", pr_number=1),
    ]
    state = _state(roadmaps=[_roadmap(epics)])
    assert detect_dispatch_items(state) == []


def test_dispatch_with_one_done_does_not_generate():
    epics = [
        _epic("E1", EpicState.DETAILED, milestone_id="MIL-A"),
        _epic("E2", EpicState.DONE, milestone_id="MIL-A"),
    ]
    state = _state(roadmaps=[_roadmap(epics)])
    assert detect_dispatch_items(state) == []


def test_dispatch_with_one_pre_detailed_does_not_generate():
    epics = [
        _epic("E1", EpicState.DETAILED, milestone_id="MIL-A"),
        _epic("E2", EpicState.SKETCHED, milestone_id="MIL-A"),
    ]
    state = _state(roadmaps=[_roadmap(epics)])
    assert detect_dispatch_items(state) == []


def test_dispatch_skips_epics_without_milestone():
    epics = [_epic("E1", EpicState.DETAILED, milestone_id=None)]
    state = _state(roadmaps=[_roadmap(epics)])
    assert detect_dispatch_items(state) == []


# ----- REVIEW -----

def test_review_groups_by_pr_number():
    epics = [
        _epic("E1", EpicState.IN_REVIEW, milestone_id="MIL-A", pr_number=93,
              pr_url="https://example.com/pr/93"),
        _epic("E2", EpicState.IN_REVIEW, milestone_id="MIL-A", pr_number=93,
              pr_url="https://example.com/pr/93"),
    ]
    state = _state(roadmaps=[_roadmap(epics)])
    items = detect_review_items(state)
    assert len(items) == 1
    item = items[0]
    assert item.type == ItemType.REVIEW
    assert item.id == "review:pr-93"
    assert isinstance(item.source_pointer, PRPointer)
    assert item.source_pointer.pr_number == 93
    assert item.source_pointer.milestone_id == "MIL-A"


def test_review_distinct_pr_numbers_generate_distinct_items():
    epics = [
        _epic("E1", EpicState.IN_REVIEW, milestone_id="A", pr_number=10, pr_url="u/10"),
        _epic("E2", EpicState.IN_REVIEW, milestone_id="B", pr_number=11, pr_url="u/11"),
    ]
    state = _state(roadmaps=[_roadmap(epics)])
    items = detect_review_items(state)
    assert len(items) == 2


def test_review_skips_epics_without_pr_number():
    epics = [_epic("E1", EpicState.IN_REVIEW, milestone_id="A", pr_number=None)]
    state = _state(roadmaps=[_roadmap(epics)])
    assert detect_review_items(state) == []


# ----- REFINE -----

def test_refine_generates_for_sketched():
    epics = [_epic("E1", EpicState.SKETCHED)]
    state = _state(roadmaps=[_roadmap(epics)])
    items = detect_refine_items(state)
    assert len(items) == 1
    item = items[0]
    assert item.type == ItemType.REFINE
    assert isinstance(item.source_pointer, RefinePointer)
    assert item.source_pointer.current_state == EpicState.SKETCHED
    assert item.source_pointer.target_state == EpicState.CRITERIA


def test_refine_generates_for_criteria():
    epics = [_epic("E1", EpicState.CRITERIA)]
    state = _state(roadmaps=[_roadmap(epics)])
    items = detect_refine_items(state)
    assert len(items) == 1
    assert items[0].source_pointer.target_state == EpicState.DETAILED


def test_refine_excludes_vision_and_aligned():
    epics = [
        _epic("V", EpicState.VISION),
        _epic("A", EpicState.ALIGNED),
    ]
    state = _state(roadmaps=[_roadmap(epics)])
    assert detect_refine_items(state) == []


def test_refine_excludes_detailed_and_execution_states():
    epics = [
        _epic("D", EpicState.DETAILED),
        _epic("P", EpicState.IN_PROGRESS),
        _epic("R", EpicState.IN_REVIEW, pr_number=1),
        _epic("X", EpicState.DONE),
    ]
    state = _state(roadmaps=[_roadmap(epics)])
    assert detect_refine_items(state) == []


# ----- CLEANUP -----

def test_cleanup_generates_for_done_epics():
    epics = [_epic("E1", EpicState.DONE)]
    state = _state(roadmaps=[_roadmap(epics)])
    items = detect_cleanup_items(state)
    assert len(items) == 1
    assert items[0].type == ItemType.CLEANUP
    assert isinstance(items[0].source_pointer, CleanupPointer)
    assert items[0].source_pointer.title == "épico E1"


def test_cleanup_excludes_non_done():
    epics = [_epic("E1", EpicState.IN_REVIEW, pr_number=1)]
    state = _state(roadmaps=[_roadmap(epics)])
    assert detect_cleanup_items(state) == []


# ----- STALE_BRANCH -----

def test_stale_branch_generates_for_old_branch():
    branches = [RemoteBranch(name="claude/old", last_commit_at=_NOW - timedelta(days=10))]
    state = _state(branches=branches)
    items = detect_stale_branch_items(state, threshold_days=7)
    assert len(items) == 1
    item = items[0]
    assert item.type == ItemType.STALE_BRANCH
    assert isinstance(item.source_pointer, BranchPointer)
    assert item.source_pointer.days_stale == 10


def test_stale_branch_skips_recent_branch():
    branches = [RemoteBranch(name="claude/new", last_commit_at=_NOW - timedelta(days=3))]
    state = _state(branches=branches)
    assert detect_stale_branch_items(state, threshold_days=7) == []


def test_stale_branch_excludes_branch_referenced_by_in_progress_epic():
    epics = [_epic("E1", EpicState.IN_PROGRESS, branch="claude/working")]
    branches = [RemoteBranch(name="claude/working", last_commit_at=_NOW - timedelta(days=10))]
    state = _state(roadmaps=[_roadmap(epics)], branches=branches)
    assert detect_stale_branch_items(state, threshold_days=7) == []


def test_stale_branch_excludes_branch_referenced_by_in_review_epic():
    epics = [_epic("E1", EpicState.IN_REVIEW, branch="claude/r", pr_number=1)]
    branches = [RemoteBranch(name="claude/r", last_commit_at=_NOW - timedelta(days=20))]
    state = _state(roadmaps=[_roadmap(epics)], branches=branches)
    assert detect_stale_branch_items(state, threshold_days=7) == []


def test_stale_branch_always_excludes_main():
    branches = [RemoteBranch(name="main", last_commit_at=_NOW - timedelta(days=999))]
    state = _state(branches=branches)
    assert detect_stale_branch_items(state, threshold_days=7) == []


def test_stale_branch_threshold_is_strict_greater():
    # Exatamente threshold_days NÃO conta como stale (CA exige > threshold).
    branches = [RemoteBranch(name="claude/edge", last_commit_at=_NOW - timedelta(days=7))]
    state = _state(branches=branches)
    assert detect_stale_branch_items(state, threshold_days=7) == []


# ----- detect_all_items: ordenação -----

def test_detect_all_orders_dispatch_before_review_before_stale():
    epics = [
        _epic("D1", EpicState.DETAILED, milestone_id="MD"),
        _epic("R1", EpicState.IN_REVIEW, milestone_id="MR", pr_number=42, pr_url="u"),
    ]
    branches = [RemoteBranch(name="claude/old", last_commit_at=_NOW - timedelta(days=10))]
    state = _state(roadmaps=[_roadmap(epics)], branches=branches)
    items = detect_all_items(state, threshold_days=7)
    types = [i.type for i in items]
    assert types.index(ItemType.DISPATCH) < types.index(ItemType.REVIEW) < types.index(ItemType.STALE_BRANCH)


def test_detect_all_orders_review_before_refine_before_cleanup():
    epics = [
        _epic("R1", EpicState.IN_REVIEW, milestone_id="MR", pr_number=42, pr_url="u"),
        _epic("F1", EpicState.SKETCHED, milestone_id="MF"),
        _epic("C1", EpicState.DONE, milestone_id="MC"),
    ]
    state = _state(roadmaps=[_roadmap(epics)])
    items = detect_all_items(state)
    types = [i.type for i in items]
    assert types == [ItemType.REVIEW, ItemType.REFINE, ItemType.CLEANUP]


def test_detect_all_idempotent():
    epics = [_epic("E1", EpicState.DETAILED, milestone_id="MIL-A")]
    state = _state(roadmaps=[_roadmap(epics)])
    a = detect_all_items(state)
    b = detect_all_items(state)
    assert a == b


def test_detect_all_returns_empty_for_empty_state():
    state = _state()
    assert detect_all_items(state) == []
