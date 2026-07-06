"""Testes do shape de QueueItem (W-PROTO-FILA-1.1)."""

from datetime import datetime

import pytest

from tools.workflow_platform.models import EpicState
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


def _epic_pointer() -> EpicPointer:
    return EpicPointer(
        milestone_id="PROTO-WORKFLOW-FAXINA",
        roadmap_path="docs/process/workflow/ROADMAP.md",
        epic_ids=["W-PROTO-10", "W-PROTO-11"],
    )


def _pr_pointer() -> PRPointer:
    return PRPointer(pr_number=93, pr_url="https://example.com/pr/93", milestone_id="X-Y")


def _branch_pointer() -> BranchPointer:
    return BranchPointer(branch_name="claude/foo", last_commit_at=_NOW, days_stale=12)


def _refine_pointer() -> RefinePointer:
    return RefinePointer(
        epic_id="W-MVP-DOC-1",
        roadmap_path="docs/process/workflow/ROADMAP.md",
        current_state=EpicState.SKETCHED,
        target_state=EpicState.CRITERIA,
    )


def _cleanup_pointer() -> CleanupPointer:
    return CleanupPointer(
        epic_id="W-PROTO-PLAT-1",
        roadmap_path="docs/process/workflow/ROADMAP.md",
        title="Scaffold de plataforma",
    )


# ----- shape coerente: cada tipo aceita seu pointer -----

def test_dispatch_with_epic_pointer_instantiates():
    item = QueueItem(
        id="dispatch:PROTO-WORKFLOW-FAXINA",
        type=ItemType.DISPATCH,
        title="Despachar PROTO-WORKFLOW-FAXINA",
        context="2 épicos em 🔍",
        expected_action="copiar prompt e rodar em sessão autônoma",
        source_pointer=_epic_pointer(),
        detected_at=_NOW,
    )
    assert item.type == ItemType.DISPATCH
    assert isinstance(item.source_pointer, EpicPointer)


def test_review_with_pr_pointer_instantiates():
    item = QueueItem(
        id="review:pr-93",
        type=ItemType.REVIEW,
        title="Revisar PR #93",
        context="milestone X em 🔀",
        expected_action="abrir PR + Copilot",
        source_pointer=_pr_pointer(),
        detected_at=_NOW,
    )
    assert isinstance(item.source_pointer, PRPointer)


def test_refine_with_refine_pointer_instantiates():
    item = QueueItem(
        id="refine:W-MVP-DOC-1",
        type=ItemType.REFINE,
        title="Refinar W-MVP-DOC-1",
        context="📐 → 📋",
        expected_action="rodar PM/sessão de refinamento",
        source_pointer=_refine_pointer(),
        detected_at=_NOW,
    )
    assert isinstance(item.source_pointer, RefinePointer)


def test_cleanup_with_cleanup_pointer_instantiates():
    item = QueueItem(
        id="cleanup:W-PROTO-PLAT-1",
        type=ItemType.CLEANUP,
        title="Limpar W-PROTO-PLAT-1",
        context="✅ aguardando faxina",
        expected_action="rodar Cleanup skill",
        source_pointer=_cleanup_pointer(),
        detected_at=_NOW,
    )
    assert isinstance(item.source_pointer, CleanupPointer)


def test_stale_branch_with_branch_pointer_instantiates():
    item = QueueItem(
        id="stale:claude/foo",
        type=ItemType.STALE_BRANCH,
        title="Branch claude/foo parada",
        context="12 dias sem commit",
        expected_action="abrir PR / deletar / resgatar",
        source_pointer=_branch_pointer(),
        detected_at=_NOW,
    )
    assert isinstance(item.source_pointer, BranchPointer)


# ----- shape incoerente: __post_init__ rejeita -----

@pytest.mark.parametrize(
    "item_type,wrong_pointer",
    [
        (ItemType.DISPATCH, _branch_pointer()),
        (ItemType.DISPATCH, _pr_pointer()),
        (ItemType.REVIEW, _epic_pointer()),
        (ItemType.REFINE, _epic_pointer()),
        (ItemType.CLEANUP, _branch_pointer()),
        (ItemType.STALE_BRANCH, _epic_pointer()),
    ],
)
def test_inconsistent_pointer_raises(item_type, wrong_pointer):
    with pytest.raises(TypeError):
        QueueItem(
            id="x",
            type=item_type,
            title="t",
            context="c",
            expected_action="a",
            source_pointer=wrong_pointer,
            detected_at=_NOW,
        )


# ----- igualdade -----

def test_two_items_with_same_fields_are_equal():
    a = QueueItem(
        id="dispatch:M",
        type=ItemType.DISPATCH,
        title="t",
        context="c",
        expected_action="a",
        source_pointer=_epic_pointer(),
        detected_at=_NOW,
    )
    b = QueueItem(
        id="dispatch:M",
        type=ItemType.DISPATCH,
        title="t",
        context="c",
        expected_action="a",
        source_pointer=_epic_pointer(),
        detected_at=_NOW,
    )
    assert a == b
