"""View Kanban — 8 colunas por estado, cards agrupados por milestone.

Card clicado salva ``selected_epic_id`` em ``st.session_state``; o painel
de detalhe é renderizado em ``app._render_detail_panel`` acima do kanban
(não abaixo) — o kanban é alto e o detail abaixo ficaria fora da viewport
após o ``st.rerun`` que segue o clique.

Roteiro de validação manual:
    1. Abrir o app com config default; verificar 8 colunas visíveis
    2. Verificar épicos do workflow ROADMAP em "PROTO-WORKFLOW-PLATAFORMA"
    3. Épicos sem campo **Milestone:** aparecem em "Sem milestone"
    4. Carregar fixture com 25+ épicos e confirmar layout legível
"""

from __future__ import annotations

from collections import OrderedDict

import streamlit as st

from tools.workflow_platform.models import Epic, EpicState, ParsedRoadmap


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

_STATE_LABELS: dict[EpicState, str] = {
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
    """Constrói o label do st.button para o card.

    Mantém uma única linha legível: ``id — title``, eventualmente truncado.
    Evitamos `**bold**` e quebras de parágrafo no label porque st.button
    preserva esses caracteres literais em algumas versões do Streamlit.
    """
    title = epic.title
    if len(title) > CARD_TITLE_MAX_LEN:
        title = title[: CARD_TITLE_MAX_LEN - 1].rstrip() + "…"
    prefix = "● " if selected else ""
    return f"{prefix}{epic.id} — {title}"


def _render_card(epic: Epic, column_index: int, position: int, selected_id: str | None) -> None:
    is_selected = (selected_id == epic.id)
    key = f"epic-card-{column_index}-{position}-{epic.id}"
    label = card_button_label(epic, selected=is_selected)
    button_type = "primary" if is_selected else "secondary"
    if st.button(label, key=key, use_container_width=True, type=button_type):
        st.session_state["selected_epic_id"] = epic.id
        st.session_state["selected_milestone_id"] = epic.milestone_id
        st.rerun()


def render_kanban(roadmaps: list[ParsedRoadmap]) -> None:
    """Renderiza 8 colunas; em cada coluna agrupa epics por ``milestone_id``."""
    all_epics: list[Epic] = [e for r in roadmaps for e in r.epics]
    selected_id = st.session_state.get("selected_epic_id")

    columns = st.columns(len(KANBAN_COLUMN_ORDER))

    for col_idx, state in enumerate(KANBAN_COLUMN_ORDER):
        with columns[col_idx]:
            st.markdown(f"### {_STATE_LABELS[state]}")
            epics_in_state = [e for e in all_epics if e.state == state]
            st.caption(f"{len(epics_in_state)} épicos")

            grouped = group_by_milestone(epics_in_state)
            if not grouped:
                st.caption("_(vazio)_")
                continue

            position = 0
            for milestone_id, epics in grouped.items():
                st.markdown(f"**{milestone_id}**")
                for epic in epics:
                    _render_card(epic, col_idx, position, selected_id)
                    position += 1
