"""Testes do builder de prompt de dispatch (por épico — W-PILOTO-DISP-1)."""

from tools.workflow_platform.models import Epic, EpicState
from tools.workflow_platform.prompts.dispatch import build_dispatch_prompt


def _epic(
    epic_id: str,
    state: EpicState,
    milestone_id: str | None = "M-1",
    blocking_predecessors: list[str] | None = None,
) -> Epic:
    return Epic(
        id=epic_id,
        title=f"título de {epic_id}",
        state=state,
        roadmap_path="dummy.md",
        milestone_id=milestone_id,
        blocking_predecessors=blocking_predecessors or [],
    )


def _by_id(*epics: Epic) -> dict[str, Epic]:
    return {e.id: e for e in epics}


def test_detailed_epic_emits_per_epic_prompt():
    epic = _epic("X-1", EpicState.DETAILED)
    result = build_dispatch_prompt(epic, _by_id(epic))
    assert result.prompt_text == "implementa o épico X-1"
    assert result.blocked is False
    assert result.warnings == []


def test_sibling_in_execution_no_longer_blocks():
    # Irmão em 🏗️/🔀/✅ NÃO bloqueia mais o dispatch do épico-alvo.
    target = _epic("X-1", EpicState.DETAILED)
    sibling_prog = _epic("X-2", EpicState.IN_PROGRESS)
    sibling_done = _epic("X-3", EpicState.DONE)
    result = build_dispatch_prompt(
        target, _by_id(target, sibling_prog, sibling_done)
    )
    assert result.blocked is False
    assert result.prompt_text == "implementa o épico X-1"


def test_non_done_predecessor_blocks_with_reason():
    pred = _epic("PRED", EpicState.IN_REVIEW)
    dep = _epic("DEP", EpicState.DETAILED, blocking_predecessors=["PRED"])
    result = build_dispatch_prompt(dep, _by_id(pred, dep))
    assert result.blocked is True
    assert result.prompt_text is None
    assert any("PRED" in w and "✅" in w for w in result.warnings)


def test_done_predecessor_does_not_block():
    pred = _epic("PRED", EpicState.DONE)
    dep = _epic("DEP", EpicState.DETAILED, blocking_predecessors=["PRED"])
    result = build_dispatch_prompt(dep, _by_id(pred, dep))
    assert result.blocked is False
    assert result.prompt_text == "implementa o épico DEP"


def test_milestone_predecessor_all_done_does_not_block():
    a = _epic("A", EpicState.DONE, milestone_id="MIL-PRED")
    b = _epic("B", EpicState.DONE, milestone_id="MIL-PRED")
    dep = _epic("DEP", EpicState.DETAILED, milestone_id="MIL-DEP",
                blocking_predecessors=["MIL-PRED"])
    by_ms = {"MIL-PRED": [a, b], "MIL-DEP": [dep]}
    result = build_dispatch_prompt(dep, _by_id(a, b, dep), by_ms)
    assert result.blocked is False
    assert result.prompt_text == "implementa o épico DEP"


def test_no_milestone_id_returns_none_with_warning():
    epic = _epic("X-1", EpicState.DETAILED, milestone_id=None)
    result = build_dispatch_prompt(epic, _by_id(epic))
    assert result.prompt_text is None
    assert result.blocked is True
    assert any("sem milestone" in w for w in result.warnings)
