"""Testes do mapa de próximo passo + prompt de refinamento."""

from tools.workflow_platform.models import Epic, EpicState
from tools.workflow_platform.prompts.refinement import (
    AUTONOMOUS_READINESS_PATH,
    NEXT_STEP_MAP,
    build_refinement_prompt,
    get_next_step,
)


def _epic(state: EpicState, *, epic_id: str = "X-1", title: str = "título de X") -> Epic:
    return Epic(
        id=epic_id,
        title=title,
        state=state,
        roadmap_path="docs/process/workflow/ROADMAP.md",
        milestone_id="M-1",
    )


def test_next_step_for_criteria_targets_detailed_with_checklist():
    info = get_next_step(_epic(EpicState.CRITERIA))
    assert info is not None
    assert info.target_states == [EpicState.DETAILED]
    assert info.readiness_checklist is True


def test_next_step_for_in_progress_returns_none():
    assert get_next_step(_epic(EpicState.IN_PROGRESS)) is None


def test_next_step_map_covers_four_pre_execution_states():
    expected = {
        EpicState.VISION,
        EpicState.ALIGNED,
        EpicState.SKETCHED,
        EpicState.CRITERIA,
    }
    assert set(NEXT_STEP_MAP.keys()) == expected


def test_refinement_prompt_for_criteria_mentions_readiness():
    prompt = build_refinement_prompt(_epic(EpicState.CRITERIA))
    assert prompt is not None
    assert AUTONOMOUS_READINESS_PATH in prompt
    assert "X-1" in prompt
    assert "título de X" in prompt
    assert "docs/process/workflow/ROADMAP.md" in prompt


def test_refinement_prompt_for_vision_omits_readiness():
    prompt = build_refinement_prompt(_epic(EpicState.VISION))
    assert prompt is not None
    assert AUTONOMOUS_READINESS_PATH not in prompt


def test_refinement_prompt_for_execution_state_returns_none():
    assert build_refinement_prompt(_epic(EpicState.IN_PROGRESS)) is None
    assert build_refinement_prompt(_epic(EpicState.DETAILED)) is None
    assert build_refinement_prompt(_epic(EpicState.DONE)) is None
