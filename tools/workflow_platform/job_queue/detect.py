"""Detecção determinística de itens de fila a partir do estado-do-mundo.

Função pura ``detect_all_items(state) -> list[QueueItem]``. Sem efeitos
colaterais; sem cache. Cada render da view reconstrói a fila do zero,
materializando o princípio "markdown é fonte da verdade".

Cobre 5 tipos no Protótipo:
    - DISPATCH       milestone com todos épicos em 🔍, sem nenhum em 🏗️/🔀/✅
    - REVIEW         PR aberta (épicos em 🔀, agrupados por pr_number)
    - REFINE         épico em 📐 ou 📋 (alvo via NEXT_STEP_MAP)
    - CLEANUP        épico em ✅ (Cleanup skill ainda não rodou)
    - STALE_BRANCH   branch parada > threshold dias, sem PR e sem épico em 🏗️/🔀
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from tools.workflow_platform.models import Epic, EpicState, ParsedRoadmap
from tools.workflow_platform.prompts.refinement import NEXT_STEP_MAP
from tools.workflow_platform.job_queue.git_helper import RemoteBranch
from tools.workflow_platform.job_queue.models import (
    BranchPointer,
    CleanupPointer,
    EpicPointer,
    ItemType,
    PRPointer,
    QueueItem,
    RefinePointer,
)


DEFAULT_STALE_THRESHOLD_DAYS = 7

_EXECUTION_STATES: set[EpicState] = {
    EpicState.IN_PROGRESS,
    EpicState.IN_REVIEW,
    EpicState.DONE,
}

_TYPE_PRIORITY: dict[ItemType, int] = {
    ItemType.DISPATCH:     0,
    ItemType.REVIEW:       1,
    ItemType.REFINE:       2,
    ItemType.CLEANUP:      3,
    ItemType.STALE_BRANCH: 4,
}


@dataclass(frozen=True)
class WorldState:
    roadmaps: list[ParsedRoadmap]
    remote_branches: list[RemoteBranch]
    now: datetime


def _all_epics(state: WorldState) -> list[Epic]:
    return [e for r in state.roadmaps for e in r.epics]


def _epics_by_milestone(state: WorldState) -> dict[str, list[Epic]]:
    grouped: dict[str, list[Epic]] = {}
    for epic in _all_epics(state):
        if epic.milestone_id is None:
            continue
        grouped.setdefault(epic.milestone_id, []).append(epic)
    return grouped


def detect_dispatch_items(state: WorldState) -> list[QueueItem]:
    """1 item por milestone com todos épicos em 🔍 e nenhum em 🏗️/🔀/✅."""
    items: list[QueueItem] = []
    grouped = _epics_by_milestone(state)
    for milestone_id, epics in grouped.items():
        if not epics:
            continue
        if any(e.state in _EXECUTION_STATES for e in epics):
            continue
        if not all(e.state == EpicState.DETAILED for e in epics):
            continue
        # Todos em 🔍.
        roadmap_path = epics[0].roadmap_path
        epic_ids = sorted(e.id for e in epics)
        pointer = EpicPointer(
            milestone_id=milestone_id,
            roadmap_path=roadmap_path,
            epic_ids=epic_ids,
        )
        items.append(
            QueueItem(
                id=f"dispatch:{milestone_id}",
                type=ItemType.DISPATCH,
                title=f"Despachar {milestone_id}",
                context=f"{len(epics)} épicos em 🔍 — apto a dispatch",
                expected_action=(
                    f"Copie o prompt e rode em sessão autônoma: "
                    f'"implementa o {milestone_id}"'
                ),
                source_pointer=pointer,
                detected_at=state.now,
            )
        )
    return items


def detect_review_items(state: WorldState) -> list[QueueItem]:
    """1 item por pr_number distinto encontrado em épicos no estado 🔀."""
    by_pr: dict[int, list[Epic]] = {}
    for epic in _all_epics(state):
        if epic.state != EpicState.IN_REVIEW or epic.pr_number is None:
            continue
        by_pr.setdefault(epic.pr_number, []).append(epic)

    items: list[QueueItem] = []
    for pr_number, epics in by_pr.items():
        # Pega URL do primeiro épico que tiver, fallback vazio.
        pr_url = next((e.pr_url for e in epics if e.pr_url), "") or ""
        # milestone_id se todos os épicos do PR concordarem
        milestone_ids = {e.milestone_id for e in epics if e.milestone_id}
        milestone_id = next(iter(milestone_ids)) if len(milestone_ids) == 1 else None
        epic_ids = sorted(e.id for e in epics)

        pointer = PRPointer(
            pr_number=pr_number,
            pr_url=pr_url,
            milestone_id=milestone_id,
        )
        ms_label = milestone_id or "milestone"
        items.append(
            QueueItem(
                id=f"review:pr-{pr_number}",
                type=ItemType.REVIEW,
                title=f"Revisar PR #{pr_number}",
                context=(
                    f"{ms_label} em 🔀 — épicos: {', '.join(epic_ids)}"
                ),
                expected_action=(
                    "Abra a PR, copie a Seção 🎯 Validação do body, cole no "
                    "GitHub Copilot, e decida merge."
                ),
                source_pointer=pointer,
                detected_at=state.now,
            )
        )
    return items


def detect_refine_items(state: WorldState) -> list[QueueItem]:
    """1 item por épico em 📐 ou 📋. Estados 🌱/🧭 ficam fora."""
    items: list[QueueItem] = []
    refinable = {EpicState.SKETCHED, EpicState.CRITERIA}
    for epic in _all_epics(state):
        if epic.state not in refinable:
            continue
        info = NEXT_STEP_MAP.get(epic.state)
        if info is None or not info.target_states:
            continue
        target = info.target_states[0]
        pointer = RefinePointer(
            epic_id=epic.id,
            roadmap_path=epic.roadmap_path,
            current_state=epic.state,
            target_state=target,
        )
        items.append(
            QueueItem(
                id=f"refine:{epic.id}",
                type=ItemType.REFINE,
                title=f"Refinar {epic.id}",
                context=f"{epic.state.value} → {target.value}",
                expected_action=(
                    "Copie o prompt de refinamento e rode em sessão de "
                    "refinamento."
                ),
                source_pointer=pointer,
                detected_at=state.now,
            )
        )
    return items


def detect_cleanup_items(state: WorldState) -> list[QueueItem]:
    """1 item por épico em ✅ (Cleanup skill ainda não rodou)."""
    items: list[QueueItem] = []
    for epic in _all_epics(state):
        if epic.state != EpicState.DONE:
            continue
        pointer = CleanupPointer(
            epic_id=epic.id,
            roadmap_path=epic.roadmap_path,
            title=epic.title,
        )
        items.append(
            QueueItem(
                id=f"cleanup:{epic.id}",
                type=ItemType.CLEANUP,
                title=f"Limpar {epic.id}",
                context=f'✅ aguardando faxina — "{epic.title}"',
                expected_action=(
                    "Carregue skills/cleanup/skill.md e siga o protocolo. "
                    "Cleanup move conteúdo histórico do épico pra fora do "
                    "ROADMAP; coluna ✅ do kanban volta a ficar vazia."
                ),
                source_pointer=pointer,
                detected_at=state.now,
            )
        )
    return items


def _branches_in_use(state: WorldState) -> set[str]:
    """Branches referenciadas por épicos em 🏗️/🔀."""
    in_use: set[str] = set()
    active_states = {EpicState.IN_PROGRESS, EpicState.IN_REVIEW}
    for epic in _all_epics(state):
        if epic.state in active_states and epic.branch:
            in_use.add(epic.branch)
    return in_use


def detect_stale_branch_items(
    state: WorldState,
    threshold_days: int = DEFAULT_STALE_THRESHOLD_DAYS,
) -> list[QueueItem]:
    """Branches paradas > threshold_days sem épico em 🏗️/🔀 referenciando.

    Exclui ``main``. Caller decide o threshold (lê de preferences.json
    em FILA-4.1; default 7).
    """
    items: list[QueueItem] = []
    in_use = _branches_in_use(state)
    for branch in state.remote_branches:
        if branch.name == "main":
            continue
        if branch.name in in_use:
            continue
        delta = state.now - branch.last_commit_at
        days = delta.days
        if days <= threshold_days:
            continue
        pointer = BranchPointer(
            branch_name=branch.name,
            last_commit_at=branch.last_commit_at,
            days_stale=days,
        )
        items.append(
            QueueItem(
                id=f"stale:{branch.name}",
                type=ItemType.STALE_BRANCH,
                title=f"Branch {branch.name} parada",
                context=f"{days} dias sem commit, sem PR aberta",
                expected_action=(
                    "Decida: (a) abrir PR (b) git push origin --delete "
                    f"{branch.name} (c) resgatar contexto e seguir"
                ),
                source_pointer=pointer,
                detected_at=state.now,
            )
        )
    return items


def detect_all_items(
    state: WorldState,
    threshold_days: int = DEFAULT_STALE_THRESHOLD_DAYS,
) -> list[QueueItem]:
    """União ordenada por (detected_at desc, type priority asc, id asc)."""
    items: list[QueueItem] = []
    items.extend(detect_dispatch_items(state))
    items.extend(detect_review_items(state))
    items.extend(detect_refine_items(state))
    items.extend(detect_cleanup_items(state))
    items.extend(detect_stale_branch_items(state, threshold_days=threshold_days))

    items.sort(
        key=lambda i: (
            -i.detected_at.timestamp(),
            _TYPE_PRIORITY[i.type],
            i.id,
        )
    )
    return items
