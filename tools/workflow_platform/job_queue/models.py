"""Modelos da fila reativa.

QueueItem com 5 tipos (DISPATCH, REVIEW, REFINE, CLEANUP, STALE_BRANCH)
e tagged union de SourcePointer discriminado por tipo. Shape único pra
todos os tipos do Protótipo; runtime check em ``__post_init__`` impede
inconsistência tipo↔ponteiro.

Espelha o padrão de ``tools/workflow_platform/models.py`` — dataclasses
imutáveis (``frozen=True``), stdlib only.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from tools.workflow_platform.models import EpicState


class ItemType(Enum):
    DISPATCH = "dispatch"
    REVIEW = "review"
    REFINE = "refine"
    CLEANUP = "cleanup"
    STALE_BRANCH = "stale_branch"


@dataclass(frozen=True)
class EpicPointer:
    milestone_id: str
    roadmap_path: str
    epic_ids: list[str]


@dataclass(frozen=True)
class PRPointer:
    pr_number: int
    pr_url: str
    milestone_id: str | None = None


@dataclass(frozen=True)
class BranchPointer:
    branch_name: str
    last_commit_at: datetime
    days_stale: int


@dataclass(frozen=True)
class RefinePointer:
    epic_id: str
    roadmap_path: str
    current_state: EpicState
    target_state: EpicState


@dataclass(frozen=True)
class CleanupPointer:
    epic_id: str
    roadmap_path: str
    title: str


SourcePointer = EpicPointer | PRPointer | BranchPointer | RefinePointer | CleanupPointer


_EXPECTED_POINTER: dict[ItemType, type] = {
    ItemType.DISPATCH:     EpicPointer,
    ItemType.REVIEW:       PRPointer,
    ItemType.REFINE:       RefinePointer,
    ItemType.CLEANUP:      CleanupPointer,
    ItemType.STALE_BRANCH: BranchPointer,
}


@dataclass(frozen=True)
class QueueItem:
    id: str
    type: ItemType
    title: str
    context: str
    expected_action: str
    source_pointer: SourcePointer
    detected_at: datetime

    def __post_init__(self) -> None:
        expected = _EXPECTED_POINTER[self.type]
        if not isinstance(self.source_pointer, expected):
            raise TypeError(
                f"{self.type} expects {expected.__name__}, "
                f"got {type(self.source_pointer).__name__}"
            )
