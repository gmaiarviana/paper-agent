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
