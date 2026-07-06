"""View models tipados para o ``rx.State`` da plataforma (W-PILOTO-UX-1).

Reflex exige tipos concretos para iterar (``rx.foreach``) e acessar campos no
render — dicts ``Any`` não bastam (o item aninhado vira ``Any`` e quebra o
``foreach``). Estes dataclasses descrevem os shapes serializáveis derivados do
miolo. Todos os campos têm default para permitir instâncias vazias (estado
"nada selecionado").

Nomes de campo evitam colisão com métodos de ``ObjectVar`` do Reflex
(``items``/``keys``/``values``) — daí ``cards`` em vez de ``items`` e
``item_type`` em vez de ``type``.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class QueueItemView:
    id: str = ""
    item_type: str = ""
    emoji: str = ""
    type_label: str = ""
    title: str = ""
    context: str = ""
    expected_action: str = ""
    pointer_md: str = ""
    prompt: str = ""
    card_label: str = ""
    title_label: str = ""
    action_label: str = ""
    meta: str = ""


@dataclass
class QueueGroup:
    emoji: str = ""
    label: str = ""
    count: int = 0
    header: str = ""
    cards: list[QueueItemView] = field(default_factory=list)


@dataclass
class EpicCard:
    id: str = ""
    label: str = ""
    selected: bool = False
    blocked: bool = False
    blocked_note: str = ""    # "🔒 aguardando <ID>" quando bloqueado


@dataclass
class KanbanGroup:
    milestone_id: str = ""
    epics: list[EpicCard] = field(default_factory=list)


@dataclass
class KanbanColumn:
    state_label: str = ""
    count: int = 0
    count_label: str = ""
    groups: list[KanbanGroup] = field(default_factory=list)


@dataclass
class SidebarRoadmap:
    rel: str = ""
    label: str = ""
    count: int = 0
    checked: bool = False
    display: str = ""


@dataclass
class DispatchWarning:
    text: str = ""
    blocked: bool = False


@dataclass
class KanbanDetail:
    id: str = ""
    title: str = ""
    header: str = ""
    meta: str = ""
    state_label: str = ""
    milestone: str = ""
    roadmap: str = ""
    kind: str = ""          # "" = nenhum épico selecionado; "blocked" = predecessor não-✅
    blocked_by: str = ""    # IDs de predecessores não-✅ (separados por vírgula)
    guidance: str = ""
    show_readiness: bool = False
    refine_prompt: str = ""
    dispatch_prompt: str = ""
    dispatch_warnings: list[DispatchWarning] = field(default_factory=list)
    link_md: str = ""
    warn: str = ""
    excerpt: str = ""
