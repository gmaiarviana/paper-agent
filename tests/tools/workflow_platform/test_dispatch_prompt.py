"""Testes do builder de prompt de dispatch."""

from tools.workflow_platform.models import Epic, EpicState
from tools.workflow_platform.prompts.dispatch import build_dispatch_prompt


def _epic(epic_id: str, state: EpicState, milestone_id: str | None = "M-1") -> Epic:
    return Epic(
        id=epic_id,
        title=f"título de {epic_id}",
        state=state,
        roadmap_path="dummy.md",
        milestone_id=milestone_id,
    )


def test_milestone_all_detailed_emits_simple_prompt():
    epics = [
        _epic("X-1", EpicState.DETAILED),
        _epic("X-2", EpicState.DETAILED),
    ]
    result = build_dispatch_prompt(epics[0], epics)
    assert result.prompt_text == "implementa o M-1"
    assert result.blocked is False
    assert result.warnings == []


def test_milestone_with_criteria_epic_appends_pm_note():
    epics = [
        _epic("X-1", EpicState.DETAILED),
        _epic("X-2", EpicState.CRITERIA),
    ]
    result = build_dispatch_prompt(epics[0], epics)
    assert result.blocked is False
    assert "implementa o M-1" in result.prompt_text
    assert "PM skill refinará" in result.prompt_text
    assert "X-2" in result.prompt_text
    assert any("X-2" in w for w in result.warnings)


def test_milestone_with_in_progress_epic_blocks():
    epics = [
        _epic("X-1", EpicState.DETAILED),
        _epic("X-2", EpicState.IN_PROGRESS),
    ]
    result = build_dispatch_prompt(epics[0], epics)
    assert result.blocked is True
    assert result.prompt_text is None
    assert any("X-2" in w for w in result.warnings)


def test_milestone_with_done_epic_blocks():
    epics = [
        _epic("X-1", EpicState.DETAILED),
        _epic("X-2", EpicState.DONE),
    ]
    result = build_dispatch_prompt(epics[0], epics)
    assert result.blocked is True
    assert result.prompt_text is None


def test_no_milestone_id_returns_none_with_warning():
    epic = _epic("X-1", EpicState.DETAILED, milestone_id=None)
    result = build_dispatch_prompt(epic, [epic])
    assert result.prompt_text is None
    assert result.blocked is True
    assert any("sem milestone" in w for w in result.warnings)


def test_multiple_pre_refinement_epics_are_listed():
    epics = [
        _epic("X-1", EpicState.DETAILED),
        _epic("X-2", EpicState.SKETCHED),
        _epic("X-3", EpicState.VISION),
    ]
    result = build_dispatch_prompt(epics[0], epics)
    assert result.blocked is False
    assert "X-2" in result.prompt_text
    assert "X-3" in result.prompt_text
