"""Determinismo da detecção (W-PROTO-FILA-1.3).

Snapshot fixo prova que ``detect_all_items`` é função pura do estado.
Mudança no código que altera shape/regra quebra ``test_detect_snapshot``.
Atualizar snapshot é decisão consciente: rodar o helper de regeneração
documentado abaixo.
"""

from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path

from tools.workflow_platform.job_queue.detect import detect_all_items
from tools.workflow_platform.job_queue.models import QueueItem

from tests.tools.workflow_platform.fixtures.world_state import (
    SNAPSHOT_THRESHOLD_DAYS,
    make_world_state_fixture,
)


SNAPSHOT_PATH = (
    Path(__file__).parent / "fixtures" / "expected_queue_snapshot.json"
)


def _serialize(obj):
    """Serializa QueueItem (e ponteiros) num dict JSON-friendly determinístico."""
    if isinstance(obj, list):
        return [_serialize(x) for x in obj]
    if isinstance(obj, Enum):
        return obj.value
    if isinstance(obj, datetime):
        return obj.isoformat()
    if is_dataclass(obj):
        out = {}
        for k, v in asdict(obj).items():
            out[k] = _serialize_value(v)
        if isinstance(obj, QueueItem):
            # asdict já transformou source_pointer num dict simples;
            # adicionamos o nome da classe pra distinguir tipos no snapshot
            out["source_pointer_kind"] = type(obj.source_pointer).__name__
        return out
    return obj


def _serialize_value(v):
    if isinstance(v, Enum):
        return v.value
    if isinstance(v, datetime):
        return v.isoformat()
    if isinstance(v, list):
        return [_serialize_value(x) for x in v]
    if isinstance(v, dict):
        return {kk: _serialize_value(vv) for kk, vv in v.items()}
    return v


def _serialize_items(items: list[QueueItem]) -> list[dict]:
    return [_serialize(i) for i in items]


def test_detect_is_deterministic():
    """Detecção é função pura: duas chamadas no mesmo estado dão lista idêntica."""
    state = make_world_state_fixture()
    a = detect_all_items(state, threshold_days=SNAPSHOT_THRESHOLD_DAYS)
    b = detect_all_items(state, threshold_days=SNAPSHOT_THRESHOLD_DAYS)
    assert a == b


def test_detect_snapshot():
    """Saída casa exatamente com snapshot persistido em fixtures/.

    Para regenerar conscientemente:
        python -m tests.tools.workflow_platform.fixtures.regenerate_snapshot
    (ou rodar o trecho abaixo em REPL e gravar)::
        from tests.tools.workflow_platform.fixtures.world_state \\
            import make_world_state_fixture
        from tools.workflow_platform.job_queue.detect import detect_all_items
        items = detect_all_items(make_world_state_fixture(), threshold_days=7)
        # serializar via _serialize_items deste arquivo
    """
    state = make_world_state_fixture()
    actual = _serialize_items(
        detect_all_items(state, threshold_days=SNAPSHOT_THRESHOLD_DAYS)
    )
    expected = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
    assert actual == expected


def test_snapshot_has_three_items_one_of_each_relevant_type():
    """Snapshot atual tem exatamente 1 DISPATCH, 1 REVIEW, 1 STALE_BRANCH.

    REFINE/CLEANUP não estão no snapshot porque os épicos sintéticos não
    cobrem 📐/📋/✅ — esses tipos têm cobertura unitária em
    ``test_queue_detect.py``.
    """
    expected = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
    types = sorted(item["type"] for item in expected)
    assert types == ["dispatch", "review", "stale_branch"]
