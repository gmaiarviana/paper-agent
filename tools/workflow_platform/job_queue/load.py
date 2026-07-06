"""Auto-regulação da fila reativa (W-PROTO-FILA-3).

Computa estado de carga em 3 faixas a partir do número de itens detectados
e mapeia para cores de fundo. Limite alvo declarado em vision §"Fila"
(20 itens); aproximação em 75% (15 itens — buffer cognitivo de 5).

Constantes nomeadas e função pura — espelha
``tools/workflow_platform/presenters.py::KANBAN_COLUMN_ORDER``.
"""

from __future__ import annotations

from enum import Enum


QUEUE_TARGET_LIMIT = 20
QUEUE_APPROACHING_THRESHOLD = 15


class QueueLoadState(Enum):
    OK = "ok"
    APPROACHING = "approaching"
    OVER_LIMIT = "over_limit"


LOAD_STATE_COLORS: dict[QueueLoadState, str] = {
    QueueLoadState.OK:          "#d4edda",
    QueueLoadState.APPROACHING: "#fff3cd",
    QueueLoadState.OVER_LIMIT:  "#f8d7da",
}


def compute_load_state(count: int) -> QueueLoadState:
    """Mapeia contagem → estado de carga.

    Faixas:
        - count <  15 → OK (verde)
        - count <  20 → APPROACHING (amarelo)
        - count >= 20 → OVER_LIMIT (vermelho)
    """
    if count >= QUEUE_TARGET_LIMIT:
        return QueueLoadState.OVER_LIMIT
    if count >= QUEUE_APPROACHING_THRESHOLD:
        return QueueLoadState.APPROACHING
    return QueueLoadState.OK
