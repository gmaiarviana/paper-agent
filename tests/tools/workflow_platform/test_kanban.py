"""Testes do helper puro de agrupamento do kanban."""

from tools.workflow_platform.models import Epic, EpicState
from tools.workflow_platform.presenters import (
    NO_MILESTONE_LABEL,
    group_by_milestone,
)


def _epic(epic_id: str, milestone_id: str | None) -> Epic:
    return Epic(
        id=epic_id,
        title=f"título de {epic_id}",
        state=EpicState.DETAILED,
        roadmap_path="dummy.md",
        milestone_id=milestone_id,
    )


def test_groups_by_milestone_preserves_order():
    epics = [
        _epic("A-1", "M1"),
        _epic("B-1", "M2"),
        _epic("A-2", "M1"),
    ]
    grouped = group_by_milestone(epics)
    assert list(grouped.keys()) == ["M1", "M2"]
    assert [e.id for e in grouped["M1"]] == ["A-1", "A-2"]


def test_none_milestone_lands_in_dedicated_bucket():
    epics = [
        _epic("X-1", None),
        _epic("A-1", "M1"),
    ]
    grouped = group_by_milestone(epics)
    keys = list(grouped.keys())
    assert keys[-1] == NO_MILESTONE_LABEL
    assert grouped[NO_MILESTONE_LABEL][0].id == "X-1"


def test_empty_input_returns_empty_dict():
    assert dict(group_by_milestone([])) == {}
