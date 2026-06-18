"""Testes do helper puro de FILA-2.1 (group_by_type).

A camada de render Streamlit (``render_queue``, ``render_card``,
``render_over_limit_banner``) é validada manualmente via fixture sintética
— mesmo padrão de PLAT-2 (kanban).
"""

from datetime import datetime

import pytest

from tools.workflow_platform.queue.models import (
    EpicPointer,
    ItemType,
    PRPointer,
    QueueItem,
)
from tools.workflow_platform.views.queue import group_by_type


_NOW = datetime(2026, 4, 30, 12, 0, 0)


def _dispatch_item(suffix: str) -> QueueItem:
    return QueueItem(
        id=f"dispatch:{suffix}",
        type=ItemType.DISPATCH,
        title=f"Despachar {suffix}",
        context="3 épicos em 🔍",
        expected_action="rodar em sessão autônoma",
        source_pointer=EpicPointer(
            milestone_id=suffix,
            roadmap_path="x.md",
            epic_ids=["E1", "E2", "E3"],
        ),
        detected_at=_NOW,
    )


def _review_item(pr_number: int) -> QueueItem:
    return QueueItem(
        id=f"review:pr-{pr_number}",
        type=ItemType.REVIEW,
        title=f"Revisar PR #{pr_number}",
        context="milestone X em 🔀",
        expected_action="abrir + Copilot",
        source_pointer=PRPointer(
            pr_number=pr_number,
            pr_url=f"https://example/pr/{pr_number}",
            milestone_id="X",
        ),
        detected_at=_NOW,
    )


def test_group_by_type_returns_all_five_keys_even_when_empty():
    grouped = group_by_type([])
    assert set(grouped.keys()) == set(ItemType)
    assert all(v == [] for v in grouped.values())


def test_group_by_type_preserves_internal_order_per_bucket():
    a = _dispatch_item("MIL-A")
    b = _dispatch_item("MIL-B")
    c = _review_item(10)
    d = _review_item(11)
    items = [a, c, b, d]
    grouped = group_by_type(items)
    assert grouped[ItemType.DISPATCH] == [a, b]
    assert grouped[ItemType.REVIEW] == [c, d]
    assert grouped[ItemType.STALE_BRANCH] == []


def test_group_by_type_keys_are_in_fixed_order():
    grouped = group_by_type([_review_item(1), _dispatch_item("M")])
    keys = list(grouped.keys())
    assert keys == [
        ItemType.DISPATCH,
        ItemType.REVIEW,
        ItemType.REFINE,
        ItemType.CLEANUP,
        ItemType.STALE_BRANCH,
    ]
