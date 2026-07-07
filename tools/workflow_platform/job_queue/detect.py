"""Detecção determinística de itens de fila a partir do estado-do-mundo.

Função pura ``detect_all_items(state) -> list[QueueItem]``. Sem efeitos
colaterais; sem cache. Cada render da view reconstrói a fila do zero,
materializando o princípio "markdown é fonte da verdade".

Cobre 5 tipos no Protótipo:
    - DISPATCH       épico em 🔍 com predecessores todos ✅ (1 item por épico)
    - REVIEW         PR aberta (épicos em 🔀, agrupados por pr_number)
    - REFINE         épico em 📐 ou 📋 com predecessores todos ✅ (alvo via NEXT_STEP_MAP)
    - CLEANUP        épico em ✅ de milestone inteiro fechado (todos ✅)
    - STALE_BRANCH   branch parada > threshold dias, sem PR e sem épico em 🏗️/🔀
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from tools.workflow_platform.models import (
    Epic,
    EpicState,
    ParsedRoadmap,
    is_blocked_by_predecessor,
)
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


def _epics_by_id(state: WorldState) -> dict[str, Epic]:
    return {e.id: e for e in _all_epics(state)}


def detect_dispatch_items(state: WorldState) -> list[QueueItem]:
    """1 item por épico em 🔍 cujos predecessores estão **todos ✅**.

    Detecção **por épico** (substitui a antiga lógica atômica por milestone): um
    milestone parcialmente entregue passa a surfaçar as fatias 🔍 restantes. Épico
    🔍 com predecessor não-✅ **não** gera item (suprimido pelo gate). Épico sem
    milestone não é despachável (fica fora do ciclo de milestone).
    """
    items: list[QueueItem] = []
    by_id = _epics_by_id(state)
    by_milestone = _epics_by_milestone(state)
    for epic in _all_epics(state):
        if epic.state != EpicState.DETAILED:
            continue
        if epic.milestone_id is None:
            continue
        if is_blocked_by_predecessor(epic, by_id, by_milestone):
            continue
        pointer = EpicPointer(
            epic_id=epic.id,
            milestone_id=epic.milestone_id,
            roadmap_path=epic.roadmap_path,
        )
        items.append(
            QueueItem(
                id=f"dispatch:{epic.id}",
                type=ItemType.DISPATCH,
                title=f"Despachar {epic.id}",
                context=f"🔍 — apto a dispatch (épico de {epic.milestone_id})",
                expected_action=(
                    f"Copie o prompt e rode em sessão autônoma: "
                    f'"implementa o épico {epic.id}"'
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
    by_id = _epics_by_id(state)
    by_milestone = _epics_by_milestone(state)
    for epic in _all_epics(state):
        if epic.state not in refinable:
            continue
        if is_blocked_by_predecessor(epic, by_id, by_milestone):
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
    """1 item por épico em ✅ cujo milestone está inteiro fechado (todos ✅).

    Épico ✅ num milestone ainda aberto (com irmão em estado != ✅) é progresso
    intra-milestone visível — não gera faxina até o milestone fechar. Épico sem
    milestone não gera faxina (fora do ciclo de milestone).
    """
    items: list[QueueItem] = []
    by_milestone = _epics_by_milestone(state)
    for epic in _all_epics(state):
        if epic.state != EpicState.DONE:
            continue
        siblings = by_milestone.get(epic.milestone_id) if epic.milestone_id else None
        if not siblings or any(s.state != EpicState.DONE for s in siblings):
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
