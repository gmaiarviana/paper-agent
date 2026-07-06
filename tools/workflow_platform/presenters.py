"""Lógica de apresentação stack-independente da plataforma de workflow.

Reúne os helpers puros que antes viviam nos módulos de view Streamlit
(``app.py``, ``views/queue.py``, ``views/kanban.py``) — agrupamentos,
labels e serialização de/para dict. Nenhum import de framework de UI
aqui: a camada Reflex (``web/``) consome estas funções, e os testes as
exercitam diretamente.

W-PILOTO-UX-1 (migração Streamlit → Reflex): a view muda, o miolo não.
"""

from __future__ import annotations

from collections import OrderedDict
from pathlib import Path

from tools.workflow_platform.models import Epic, EpicState, ParsedRoadmap
from tools.workflow_platform.job_queue.models import ItemType, QueueItem


# ---------------------------------------------------------------------------
# Labels de ROADMAP na sidebar (movido de app.py::_label_for_roadmap)
# ---------------------------------------------------------------------------

LABEL_OVERRIDES = {
    "docs/ROADMAP.md": "Core",
    "docs/process/workflow/ROADMAP.md": "Workflow",
}


def label_for_roadmap(path: str, repo_root: Path) -> str:
    """Deriva label legível do path de ROADMAP.

    Mapeamento:
        - docs/ROADMAP.md                        → "Core"
        - docs/process/workflow/ROADMAP.md       → "Workflow"
        - products/<name>/ROADMAP.md             → <Name>
        - fallback: parent name title-cased ou stem
    """
    try:
        rel = Path(path).relative_to(repo_root).as_posix()
    except ValueError:
        return Path(path).stem.title() or path
    if rel in LABEL_OVERRIDES:
        return LABEL_OVERRIDES[rel]
    parts = Path(rel).parts
    if len(parts) >= 2 and parts[0] == "products":
        return parts[1].replace("-", " ").title()
    parent_name = Path(rel).parent.name
    if parent_name:
        return parent_name.title()
    return Path(rel).stem.title() or rel


def relative_path(path: str, repo_root: Path) -> str:
    """Path relativo ao repo root (POSIX); fallback para o path cru."""
    try:
        return Path(path).relative_to(repo_root).as_posix()
    except ValueError:
        return path


# ---------------------------------------------------------------------------
# Fila — agrupamento por tipo (movido de views/queue.py)
# ---------------------------------------------------------------------------

TYPE_HEADERS: dict[ItemType, tuple[str, str]] = {
    ItemType.DISPATCH:     ("📤", "Dispatch"),
    ItemType.REVIEW:       ("🔀", "Review"),
    ItemType.REFINE:       ("📐", "Refine"),
    ItemType.CLEANUP:      ("✅", "Cleanup"),
    ItemType.STALE_BRANCH: ("🌱", "Stale branches"),
}

TYPE_ORDER: list[ItemType] = [
    ItemType.DISPATCH,
    ItemType.REVIEW,
    ItemType.REFINE,
    ItemType.CLEANUP,
    ItemType.STALE_BRANCH,
]


def group_by_type(items: list[QueueItem]) -> "OrderedDict[ItemType, list[QueueItem]]":
    """Agrupa items por tipo, preservando a ordem interna do input.

    Sempre devolve as 5 chaves do enum (mesmo se vazias), na ordem fixa
    DISPATCH → REVIEW → REFINE → CLEANUP → STALE_BRANCH.
    """
    grouped: "OrderedDict[ItemType, list[QueueItem]]" = OrderedDict()
    for t in TYPE_ORDER:
        grouped[t] = []
    for item in items:
        grouped.setdefault(item.type, []).append(item)
    return grouped


# ---------------------------------------------------------------------------
# Kanban — colunas e agrupamento por milestone (movido de views/kanban.py)
# ---------------------------------------------------------------------------

KANBAN_COLUMN_ORDER: list[EpicState] = [
    EpicState.VISION,
    EpicState.ALIGNED,
    EpicState.SKETCHED,
    EpicState.CRITERIA,
    EpicState.DETAILED,
    EpicState.IN_PROGRESS,
    EpicState.IN_REVIEW,
    EpicState.DONE,
]

STATE_LABELS: dict[EpicState, str] = {
    EpicState.VISION: "🌱 Visão",
    EpicState.ALIGNED: "🧭 Jornada alinhada",
    EpicState.SKETCHED: "📐 Esboçados",
    EpicState.CRITERIA: "📋 Critérios",
    EpicState.DETAILED: "🔍 Detalhes",
    EpicState.IN_PROGRESS: "🏗️ Em andamento",
    EpicState.IN_REVIEW: "🔀 Em revisão",
    EpicState.DONE: "✅ Implementado",
}

NO_MILESTONE_LABEL = "Sem milestone"

CARD_TITLE_MAX_LEN = 60


def group_by_milestone(epics: list[Epic]) -> "OrderedDict[str, list[Epic]]":
    """Agrupa épicos por ``milestone_id`` preservando a ordem de aparição.

    Épicos com ``milestone_id=None`` ficam num grupo final ``"Sem milestone"``.
    """
    grouped: "OrderedDict[str, list[Epic]]" = OrderedDict()
    no_milestone: list[Epic] = []

    for epic in epics:
        if epic.milestone_id is None:
            no_milestone.append(epic)
            continue
        grouped.setdefault(epic.milestone_id, []).append(epic)

    if no_milestone:
        grouped[NO_MILESTONE_LABEL] = no_milestone

    return grouped


def card_button_label(epic: Epic, *, selected: bool = False) -> str:
    """Constrói o label de card do kanban: ``id — title`` truncado.

    Mantém uma única linha legível, sem markdown de ênfase.
    """
    title = epic.title
    if len(title) > CARD_TITLE_MAX_LEN:
        title = title[: CARD_TITLE_MAX_LEN - 1].rstrip() + "…"
    prefix = "● " if selected else ""
    return f"{prefix}{epic.id} — {title}"


# ---------------------------------------------------------------------------
# Serialização de/para dict (objetos ricos ⇄ vars serializáveis do rx.State)
# ---------------------------------------------------------------------------
#
# Reflex exige vars serializáveis (JSON-able); Epic/ParsedRoadmap carregam
# um Enum (EpicState) e não entram crus no rx.State. Serializamos para dict
# com a string do estado (``EpicState.value``) e reconstruímos sob demanda
# nos event handlers, onde os builders de prompt precisam dos objetos ricos.


def epic_to_dict(epic: Epic) -> dict:
    return {
        "id": epic.id,
        "title": epic.title,
        "state": epic.state.value,
        "roadmap_path": epic.roadmap_path,
        "milestone_id": epic.milestone_id,
        "branch": epic.branch,
        "pr_number": epic.pr_number,
        "pr_url": epic.pr_url,
        "raw_status_line": epic.raw_status_line,
        "body_excerpt": epic.body_excerpt,
        "blocking_predecessors": list(epic.blocking_predecessors),
    }


def epic_from_dict(data: dict) -> Epic:
    return Epic(
        id=data["id"],
        title=data["title"],
        state=EpicState(data["state"]),
        roadmap_path=data["roadmap_path"],
        milestone_id=data.get("milestone_id"),
        branch=data.get("branch"),
        pr_number=data.get("pr_number"),
        pr_url=data.get("pr_url"),
        raw_status_line=data.get("raw_status_line", ""),
        body_excerpt=data.get("body_excerpt", ""),
        blocking_predecessors=list(data.get("blocking_predecessors", [])),
    )


def roadmap_to_dict(roadmap: ParsedRoadmap, repo_root: Path) -> dict:
    """Serializa um ParsedRoadmap para o rx.State.

    Inclui ``rel`` e ``label`` derivados (usados pela sidebar) para evitar
    recomputar path relativo no render. Milestones não são serializados —
    o agrupamento por milestone deriva de ``epic.milestone_id``.
    """
    return {
        "path": roadmap.path,
        "rel": relative_path(roadmap.path, repo_root),
        "label": label_for_roadmap(roadmap.path, repo_root),
        "epics": [epic_to_dict(e) for e in roadmap.epics],
        "warnings": list(roadmap.warnings),
    }


def roadmap_from_dict(data: dict) -> ParsedRoadmap:
    return ParsedRoadmap(
        path=data["path"],
        epics=[epic_from_dict(e) for e in data.get("epics", [])],
        warnings=list(data.get("warnings", [])),
    )
