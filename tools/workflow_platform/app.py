"""Plataforma de workflow do paper-agent — entrypoint Streamlit.

Roteiro de validação manual (W-PROTO-PLAT-1):
    1. Rodar ``streamlit run tools/workflow_platform/app.py`` a partir do repo raiz
    2. Header "Plataforma de Workflow" visível
    3. Sidebar lista os 6 ROADMAPs configurados em config.yaml
    4. Sidebar mostra contagem total de épicos parseados
    5. Expander "Avisos do parser" lista warnings (deve estar vazio com config default)
    6. Botão "🔄 Recarregar" invalida cache e re-parseia

Em W-PROTO-PLAT-2 o placeholder do kanban é substituído pela view real.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Permitir ``streamlit run tools/workflow_platform/app.py`` a partir do repo root.
_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

import streamlit as st

from tools.workflow_platform.config_loader import PlatformConfig, load_config
from tools.workflow_platform.models import ParsedRoadmap
from tools.workflow_platform.parser import parse_roadmap
from tools.workflow_platform.views.card_detail import render_card_detail
from tools.workflow_platform.views.kanban import render_kanban


st.set_page_config(
    page_title="Plataforma de Workflow",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)


def _load_state() -> tuple[PlatformConfig, list[ParsedRoadmap]]:
    if "platform_config" not in st.session_state:
        st.session_state.platform_config = load_config()
    if "parsed_roadmaps" not in st.session_state:
        st.session_state.parsed_roadmaps = [
            parse_roadmap(p) for p in st.session_state.platform_config.roadmaps
        ]
    return st.session_state.platform_config, st.session_state.parsed_roadmaps


def _reload() -> None:
    for key in ("platform_config", "parsed_roadmaps", "selected_epic_id", "selected_milestone_id"):
        st.session_state.pop(key, None)


def _render_sidebar(config: PlatformConfig, roadmaps: list[ParsedRoadmap]) -> None:
    st.sidebar.markdown("## ROADMAPs configurados")
    for r in roadmaps:
        rel = Path(r.path)
        try:
            rel = rel.relative_to(config.repo_root)
        except ValueError:
            pass
        epics_count = len(r.epics)
        st.sidebar.markdown(f"- `{rel}` — {epics_count} épicos")

    total_epics = sum(len(r.epics) for r in roadmaps)
    total_milestones = sum(len(r.milestones) for r in roadmaps)
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Total:** {total_epics} épicos · {total_milestones} milestones")

    if st.sidebar.button("🔄 Recarregar"):
        _reload()
        st.rerun()

    all_warnings: list[tuple[str, str]] = []
    for r in roadmaps:
        for w in r.warnings:
            all_warnings.append((r.path, w))
    with st.sidebar.expander(f"Avisos do parser ({len(all_warnings)})"):
        if not all_warnings:
            st.caption("sem avisos")
        else:
            for path, w in all_warnings:
                st.markdown(f"- `{Path(path).name}`: {w}")


def _find_selected_epic(roadmaps: list[ParsedRoadmap], epic_id: str | None):
    if not epic_id:
        return None
    for r in roadmaps:
        for e in r.epics:
            if e.id == epic_id:
                return e
    return None


def _render_detail_panel(
    roadmaps: list[ParsedRoadmap], config: PlatformConfig
) -> None:
    """Renderiza o painel de detalhe acima do kanban, se houver épico selecionado.

    O painel fica antes do kanban (e não depois) porque o kanban é alto — 8
    colunas com cards empilhados — e o detail abaixo ficaria fora da viewport
    após o ``st.rerun`` que acompanha cada clique.
    """
    selected_id = st.session_state.get("selected_epic_id")
    selected = _find_selected_epic(roadmaps, selected_id)
    if selected is None:
        return

    all_epics = [e for r in roadmaps for e in r.epics]
    in_milestone = [
        e for e in all_epics
        if selected.milestone_id and e.milestone_id == selected.milestone_id
    ]

    with st.container(border=True):
        cols = st.columns([6, 1])
        with cols[1]:
            if st.button("✕ Fechar", key="close-detail", use_container_width=True):
                st.session_state.pop("selected_epic_id", None)
                st.session_state.pop("selected_milestone_id", None)
                st.rerun()
        with cols[0]:
            render_card_detail(selected, in_milestone, config)
    st.markdown("---")


def main() -> None:
    config, roadmaps = _load_state()

    st.markdown("# 🧭 Plataforma de Workflow")
    st.caption(
        "Visualiza e direciona épicos de todos os ROADMAPs configurados. "
        "Markdown é fonte da verdade."
    )

    _render_sidebar(config, roadmaps)

    _render_detail_panel(roadmaps, config)

    render_kanban(roadmaps)


if __name__ == "__main__":
    main()
