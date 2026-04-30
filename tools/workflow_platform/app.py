"""Plataforma de workflow do paper-agent — entrypoint Streamlit.

Layout:
    - Tab "📋 Fila"   (default) — fila reativa de itens (W-PROTO-FILA-2)
    - Tab "🗂️ Kanban"            — kanban por estado (W-PROTO-PLAT-2)

Sidebar: filtros por ROADMAP visível (FILA-4.3), badge de carga da fila
(FILA-3.1), botão recarregar e diálogo de avisos do parser.
"""

from __future__ import annotations

import sys
from dataclasses import replace
from pathlib import Path

# Permitir ``streamlit run tools/workflow_platform/app.py`` a partir do repo root.
_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

import streamlit as st

from tools.workflow_platform.config_loader import PlatformConfig, load_config
from tools.workflow_platform.models import ParsedRoadmap
from tools.workflow_platform.parser import parse_roadmap
from tools.workflow_platform.preferences import (
    Preferences,
    PreferencesLoadError,
    apply_visibility_filter,
    load_preferences,
    save_preferences,
)
from tools.workflow_platform.queue.detect import detect_all_items
from tools.workflow_platform.queue.load import (
    LOAD_STATE_COLORS,
    QUEUE_TARGET_LIMIT,
    QueueLoadState,
    compute_load_state,
)
from tools.workflow_platform.queue.models import QueueItem
from tools.workflow_platform.views.card_detail import render_card_detail
from tools.workflow_platform.views.kanban import render_kanban
from tools.workflow_platform.views.queue import (
    build_world_state,
    render_queue,
    render_queue_item_detail,
)


st.set_page_config(
    page_title="Plataforma de Workflow",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)


LABEL_OVERRIDES = {
    "docs/ROADMAP.md": "Core",
    "docs/process/workflow/ROADMAP.md": "Workflow",
}


def _label_for_roadmap(path: str, repo_root: Path) -> str:
    """Deriva label legível do path de ROADMAP.

    Mapeamento:
        - docs/ROADMAP.md                        → "Core"
        - docs/process/workflow/ROADMAP.md       → "Workflow"
        - products/<name>/ROADMAP.md             → <Name>
        - fallback: parent name title-cased ou stem
    """
    try:
        rel = str(Path(path).relative_to(repo_root))
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


def _load_preferences(config: PlatformConfig) -> Preferences:
    if "preferences" not in st.session_state:
        try:
            st.session_state.preferences = load_preferences(config.repo_root)
            st.session_state.preferences_error = None
        except PreferencesLoadError as exc:
            st.session_state.preferences = Preferences()
            st.session_state.preferences_error = str(exc)
    return st.session_state.preferences


def _load_state() -> tuple[PlatformConfig, list[ParsedRoadmap], Preferences]:
    if "platform_config" not in st.session_state:
        st.session_state.platform_config = load_config()
    config: PlatformConfig = st.session_state.platform_config
    if "parsed_roadmaps_all" not in st.session_state:
        st.session_state.parsed_roadmaps_all = [
            parse_roadmap(p) for p in config.roadmaps
        ]
    prefs = _load_preferences(config)
    visible = apply_visibility_filter(
        st.session_state.parsed_roadmaps_all,
        prefs,
        config.repo_root,
    )
    return config, visible, prefs


def _reload() -> None:
    keys = (
        "platform_config",
        "parsed_roadmaps_all",
        "preferences",
        "preferences_error",
        "queue_world_state",
        "queue_items",
        "queue_fetch_warning",
        "selected_epic_id",
        "selected_milestone_id",
        "selected_queue_item_id",
    )
    for key in keys:
        st.session_state.pop(key, None)


def _ensure_queue_items(
    roadmaps: list[ParsedRoadmap],
    prefs: Preferences,
) -> tuple[list[QueueItem], str | None]:
    if "queue_items" in st.session_state and "queue_fetch_warning" in st.session_state:
        return (
            st.session_state.queue_items,
            st.session_state.queue_fetch_warning,
        )
    state, warning = build_world_state(
        roadmaps,
        threshold_days=prefs.stale_branch_threshold_days,
    )
    items = detect_all_items(state, threshold_days=prefs.stale_branch_threshold_days)
    st.session_state.queue_world_state = state
    st.session_state.queue_items = items
    st.session_state.queue_fetch_warning = warning
    return items, warning


def render_queue_load_badge(items: list[QueueItem]) -> None:
    n = len(items)
    state = compute_load_state(n)
    color = LOAD_STATE_COLORS[state]
    if n == 0:
        text = f"📋 Fila: 0/{QUEUE_TARGET_LIMIT} — sem itens"
    else:
        text = f"📋 Fila: {n}/{QUEUE_TARGET_LIMIT}"
    st.sidebar.markdown(
        f"<div style='background-color:{color};padding:8px;"
        f"border-radius:6px;font-weight:600;text-align:center;'>{text}</div>",
        unsafe_allow_html=True,
    )


def _all_warnings_for(roadmaps: list[ParsedRoadmap]) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    for r in roadmaps:
        for w in r.warnings:
            out.append((r.path, w))
    return out


@st.dialog("Avisos do parser")
def _render_warnings_dialog(all_warnings: list[tuple[str, str]]) -> None:
    if not all_warnings:
        st.caption("sem avisos")
    else:
        for path, w in all_warnings:
            st.markdown(f"- `{Path(path).name}`: {w}")
    if st.button("Fechar", key="close-warnings-dialog"):
        st.session_state["show_warnings_dialog"] = False
        st.rerun()


def _render_sidebar(
    config: PlatformConfig,
    all_roadmaps: list[ParsedRoadmap],
    prefs: Preferences,
    queue_items: list[QueueItem],
) -> None:
    """W-PROTO-FILA-4.3 — sidebar como painel de filtros + status."""
    st.sidebar.markdown("## 👁️ Visíveis")

    selected_paths: list[str] = []
    for r in all_roadmaps:
        try:
            rel = str(Path(r.path).relative_to(config.repo_root))
        except ValueError:
            rel = r.path
        label = _label_for_roadmap(r.path, config.repo_root)
        checked = (prefs.visible_roadmaps is None) or (rel in prefs.visible_roadmaps)
        if st.sidebar.checkbox(
            f"{label} ({len(r.epics)})",
            value=checked,
            key=f"visible_{rel}",
        ):
            selected_paths.append(rel)

    new_visible = sorted(selected_paths)
    current = (
        sorted(prefs.visible_roadmaps) if prefs.visible_roadmaps is not None else None
    )
    # Estado "todos marcados" em current=None equivale a new_visible com todos os paths.
    all_paths = []
    for r in all_roadmaps:
        try:
            all_paths.append(str(Path(r.path).relative_to(config.repo_root)))
        except ValueError:
            all_paths.append(r.path)

    representative_current = current if current is not None else sorted(all_paths)
    if representative_current != new_visible:
        new_value = (
            None if new_visible == sorted(all_paths) else new_visible
        )
        save_preferences(replace(prefs, visible_roadmaps=new_value), config.repo_root)
        st.session_state.pop("preferences", None)
        st.rerun()

    st.sidebar.markdown("---")
    render_queue_load_badge(queue_items)
    if st.sidebar.button("🔄 Recarregar", key="reload-platform"):
        _reload()
        st.rerun()

    st.sidebar.markdown("---")
    all_warnings = _all_warnings_for(all_roadmaps)
    error = st.session_state.get("preferences_error")
    if error:
        all_warnings = [("preferences.json", error), *all_warnings]
    if st.sidebar.button(
        f"⚠️ Avisos ({len(all_warnings)})", key="open-warnings-button"
    ):
        st.session_state["show_warnings_dialog"] = True
    if st.session_state.get("show_warnings_dialog"):
        _render_warnings_dialog(all_warnings)


def _find_selected_epic(roadmaps: list[ParsedRoadmap], epic_id: str | None):
    if not epic_id:
        return None
    for r in roadmaps:
        for e in r.epics:
            if e.id == epic_id:
                return e
    return None


def _find_selected_queue_item(items: list[QueueItem], item_id: str | None):
    if not item_id:
        return None
    for i in items:
        if i.id == item_id:
            return i
    return None


def _render_kanban_detail_panel(
    roadmaps: list[ParsedRoadmap], config: PlatformConfig
) -> None:
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
    config, visible_roadmaps, prefs = _load_state()
    queue_items, fetch_warning = _ensure_queue_items(visible_roadmaps, prefs)

    st.markdown("# 🧭 Plataforma de Workflow")
    st.caption(
        "Visualiza e direciona épicos de todos os ROADMAPs configurados. "
        "Markdown é fonte da verdade."
    )

    _render_sidebar(config, st.session_state.parsed_roadmaps_all, prefs, queue_items)

    if fetch_warning:
        st.warning(f"git fetch: {fetch_warning}")

    tab_queue, tab_kanban = st.tabs(["📋 Fila", "🗂️ Kanban"])

    with tab_queue:
        render_queue(queue_items)
        selected_item = _find_selected_queue_item(
            queue_items,
            st.session_state.get("selected_queue_item_id"),
        )
        if selected_item is not None:
            with st.container(border=True):
                render_queue_item_detail(selected_item, config, visible_roadmaps)

    with tab_kanban:
        _render_kanban_detail_panel(visible_roadmaps, config)
        render_kanban(visible_roadmaps)


if __name__ == "__main__":
    main()
