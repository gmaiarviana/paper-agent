"""Construção do WorldState para a detecção da fila (stack-independent).

Movido de ``views/queue.py`` na migração Streamlit → Reflex (W-PILOTO-UX-1).
A função é view-agnóstica — faz ``git fetch``, lista branches remotas e monta
o ``WorldState`` que ``queue/detect.py`` consome. Sem import de framework de UI.
"""

from __future__ import annotations

import subprocess
from datetime import datetime

from tools.workflow_platform.models import ParsedRoadmap
from tools.workflow_platform.queue.detect import (
    DEFAULT_STALE_THRESHOLD_DAYS,
    WorldState,
)
from tools.workflow_platform.queue.git_helper import (
    RemoteBranch,
    list_remote_branches,
)


def _git_fetch_with_warning() -> str | None:
    """``git fetch origin --prune``. Retorna None em sucesso, mensagem em falha."""
    try:
        subprocess.run(
            ["git", "fetch", "origin", "--prune"],
            capture_output=True,
            text=True,
            check=True,
            timeout=15,
        )
    except subprocess.CalledProcessError as exc:
        return f"git fetch falhou: {exc.stderr.strip() or exc}"
    except subprocess.TimeoutExpired:
        return "git fetch atingiu timeout (15s)"
    except FileNotFoundError:
        return "git não encontrado no PATH"
    return None


def build_world_state(
    roadmaps: list[ParsedRoadmap],
    threshold_days: int = DEFAULT_STALE_THRESHOLD_DAYS,
    *,
    do_fetch: bool = True,
) -> tuple[WorldState, str | None]:
    """Constrói WorldState para ``detect_all_items``.

    Retorna ``(state, fetch_warning)``. ``do_fetch=False`` nos testes evita
    chamar subprocess. ``threshold_days`` é injetado pelo caller (lido de
    ``preferences.json``).
    """
    fetch_warning = _git_fetch_with_warning() if do_fetch else None
    branches: list[RemoteBranch]
    try:
        branches = list_remote_branches()
    except Exception as exc:  # noqa: BLE001 - render-time defensive
        branches = []
        fetch_warning = (fetch_warning or "") + f" | list_remote_branches falhou: {exc}"
    state = WorldState(
        roadmaps=roadmaps,
        remote_branches=branches,
        now=datetime.now(),
    )
    return state, fetch_warning
