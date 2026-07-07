"""Modelos da plataforma de workflow.

Estados de épico, Epic, Milestone e ParsedRoadmap. Os emojis em
``EpicState`` espelham os 8 estados declarados em
``docs/process/refinement/planning_guidelines.md`` — qualquer mudança ali
exige acompanhar este enum.
"""

from dataclasses import dataclass, field
from enum import Enum


class EpicState(Enum):
    VISION = "🌱"          # 🌱 Visão
    ALIGNED = "🧭"         # 🧭 Jornada alinhada
    SKETCHED = "📐"        # 📐 Funcionalidades esboçadas
    CRITERIA = "📋"        # 📋 Critérios definidos
    DETAILED = "🔍"        # 🔍 Detalhes definidos
    IN_PROGRESS = "🏗️"     # 🏗️ Em andamento
    IN_REVIEW = "🔀"       # 🔀 Em revisão
    DONE = "✅"            # ✅ Implementado


@dataclass
class Epic:
    id: str
    title: str
    state: EpicState
    roadmap_path: str
    milestone_id: str | None = None
    branch: str | None = None
    pr_number: int | None = None
    pr_url: str | None = None
    raw_status_line: str = ""
    body_excerpt: str = ""
    blocking_predecessors: list[str] = field(default_factory=list)


@dataclass
class Milestone:
    id: str
    roadmap_path: str
    objective: str | None = None
    epic_ids: list[str] = field(default_factory=list)


@dataclass
class ParsedRoadmap:
    path: str
    epics: list[Epic] = field(default_factory=list)
    milestones: list[Milestone] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Predecessor bloqueante (W-PILOTO-DISP-1)
# ---------------------------------------------------------------------------
#
# Regra compartilhada por dispatch e refino: um épico com predecessor declarado
# ainda não `✅` (DONE) está bloqueado — não é oferecido como ação. Um predecessor
# pode ser um id de épico ou de milestone; milestone conta como satisfeito quando
# todos os seus épicos estão `✅`.


def _predecessor_satisfied(
    pred_id: str,
    epics_by_id: dict[str, Epic],
    epics_by_milestone: dict[str, list[Epic]],
) -> bool:
    """True se ``pred_id`` (épico ou milestone) está concluído (`✅`).

    Épico → satisfeito quando ``state == DONE``. Milestone → satisfeito quando
    todos os seus épicos estão `✅`.

    Predecessor não encontrado no conjunto parseado é tratado como **satisfeito**.
    A causa dominante de "não encontrado" é predecessor concluído e podado do
    ROADMAP (a faxina remove blocos `✅` ao fechar o milestone) — bloquear para
    sempre um dependente cujo predecessor já foi entregue é o pior modo de falha.
    Um id digitado errado aparece como item acionável (revisável em uso), não
    some silenciosamente. Grafo de dependências rico está fora do escopo do épico.
    """
    epic = epics_by_id.get(pred_id)
    if epic is not None:
        return epic.state == EpicState.DONE
    siblings = epics_by_milestone.get(pred_id)
    if siblings:
        return all(e.state == EpicState.DONE for e in siblings)
    return True


def blocking_predecessors_of(
    epic: Epic,
    epics_by_id: dict[str, Epic],
    epics_by_milestone: dict[str, list[Epic]],
) -> list[str]:
    """IDs de predecessores de ``epic`` que ainda **não** estão `✅`.

    Lista vazia = épico desbloqueado. Preserva a ordem declarada no ROADMAP.
    """
    return [
        pred_id
        for pred_id in epic.blocking_predecessors
        if not _predecessor_satisfied(pred_id, epics_by_id, epics_by_milestone)
    ]


def is_blocked_by_predecessor(
    epic: Epic,
    epics_by_id: dict[str, Epic],
    epics_by_milestone: dict[str, list[Epic]],
) -> bool:
    """True se ``epic`` tem ao menos um predecessor não-`✅`."""
    return bool(blocking_predecessors_of(epic, epics_by_id, epics_by_milestone))
