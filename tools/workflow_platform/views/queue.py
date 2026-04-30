"""View da fila reativa (W-PROTO-FILA-2.1 + 3.2).

Tab "📋 Fila" default no app. Renderiza QueueItems detectados em FILA-1
como cards clicáveis agrupados por tipo (DISPATCH > REVIEW > REFINE >
CLEANUP > STALE_BRANCH). Clique grava ``selected_queue_item_id`` em
``st.session_state``; painel de detalhe (FILA-2.2) é renderizado pelo
chamador.

Padrão herdado de ``views/kanban.py`` (PLAT-2.1) — ``render_*`` puros,
estado via ``st.session_state``.
"""

from __future__ import annotations

import subprocess
from collections import OrderedDict
from datetime import datetime

import streamlit as st

from tools.workflow_platform.models import ParsedRoadmap
from tools.workflow_platform.queue.detect import (
    DEFAULT_STALE_THRESHOLD_DAYS,
    WorldState,
    detect_all_items,
)
from tools.workflow_platform.queue.git_helper import (
    RemoteBranch,
    list_remote_branches,
)
from tools.workflow_platform.queue.load import (
    QueueLoadState,
    compute_load_state,
)
from tools.workflow_platform.queue.models import ItemType, QueueItem


TYPE_HEADERS: dict[ItemType, tuple[str, str]] = {
    ItemType.DISPATCH:     ("📤", "Dispatch"),
    ItemType.REVIEW:       ("🔀", "Review"),
    ItemType.REFINE:       ("📐", "Refine"),
    ItemType.CLEANUP:      ("✅", "Cleanup"),
    ItemType.STALE_BRANCH: ("🌱", "Stale branches"),
}

_TYPE_ORDER: list[ItemType] = [
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
    for t in _TYPE_ORDER:
        grouped[t] = []
    for item in items:
        grouped.setdefault(item.type, []).append(item)
    return grouped


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
    """Constrói WorldState para detect_all_items.

    Retorna (state, fetch_warning). ``do_fetch=False`` nos testes evita
    chamar subprocess. ``threshold_days`` é injetado pelo caller (FILA-4.2
    lê de preferences.json).
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


def render_over_limit_banner(items: list[QueueItem]) -> None:
    """W-PROTO-FILA-3.2 — alerta quando OVER_LIMIT.

    Renderiza ``st.warning`` no topo da tab quando ``len(items) >= 20``.
    Não bloqueia clique nem renderização — sinalização cognitiva.
    """
    n = len(items)
    state = compute_load_state(n)
    if state != QueueLoadState.OVER_LIMIT:
        return
    st.warning(
        f"⚠️ Fila com {n} itens (limite alvo: 20). Considere fechar itens "
        "antes de iniciar novos. No MVP, o proponente vai pausar criação "
        "automaticamente."
    )


def _render_card(item: QueueItem) -> None:
    emoji, _label = TYPE_HEADERS[item.type]
    card_label = f"{emoji} {item.title}"
    key = f"queue_card_{item.id}"
    selected = st.session_state.get("selected_queue_item_id") == item.id
    button_type = "primary" if selected else "secondary"
    if st.button(
        card_label, key=key, use_container_width=True, type=button_type
    ):
        st.session_state["selected_queue_item_id"] = item.id
        st.rerun()
    st.caption(item.context)
    st.markdown(f"**Ação esperada:** {item.expected_action}")


def render_queue(items: list[QueueItem]) -> None:
    """Renderiza a tab "📋 Fila".

    Banner OVER_LIMIT (FILA-3.2) → cabeçalhos por tipo com contagem →
    cards. Clique no card grava ``selected_queue_item_id``.
    """
    render_over_limit_banner(items)

    if not items:
        st.info("Sem itens na fila — nada esperando ação no momento.")
        return

    grouped = group_by_type(items)
    for item_type in _TYPE_ORDER:
        bucket = grouped.get(item_type, [])
        if not bucket:
            continue
        emoji, label = TYPE_HEADERS[item_type]
        st.subheader(f"{emoji} {label} ({len(bucket)})")
        for item in bucket:
            _render_card(item)
        st.markdown("---")


def render_queue_item_detail(
    item: QueueItem,
    config,
    parsed_roadmaps: list[ParsedRoadmap],
) -> None:
    """Painel de detalhe do item selecionado (consumido pelo app.py).

    Implementação da renderização do prompt vive em FILA-2.2; este shim
    importa lazy para evitar ciclo entre views/queue.py e
    prompts/queue_item.py.
    """
    from tools.workflow_platform.prompts.queue_item import (
        build_prompt_for_item,
    )
    from tools.workflow_platform.views.card_detail import (
        github_branch_url,
        github_pr_url,
    )
    from tools.workflow_platform.queue.models import (
        BranchPointer,
        EpicPointer,
        PRPointer,
        RefinePointer,
    )

    # Construir lookups para builders DISPATCH e REFINE
    all_epics_by_milestone: dict[str, list] = {}
    epic_lookup: dict[str, object] = {}
    for r in parsed_roadmaps:
        for e in r.epics:
            epic_lookup[e.id] = e
            if e.milestone_id:
                all_epics_by_milestone.setdefault(e.milestone_id, []).append(e)

    cols = st.columns([6, 1])
    with cols[1]:
        if st.button("✕ Fechar", key="close-queue-detail", use_container_width=True):
            st.session_state.pop("selected_queue_item_id", None)
            st.rerun()
    with cols[0]:
        emoji, label = TYPE_HEADERS[item.type]
        st.markdown(f"## {emoji} {item.title}")
        st.caption(f"Tipo: **{label}** · ID: `{item.id}`")

    # Link contextual do ponteiro
    pointer = item.source_pointer
    if isinstance(pointer, PRPointer) and pointer.pr_url:
        st.markdown(f"**PR:** [#{pointer.pr_number}]({pointer.pr_url})")
    elif isinstance(pointer, BranchPointer):
        url = github_branch_url(config.github_owner, config.github_repo, pointer.branch_name)
        st.markdown(f"**Branch:** [`{pointer.branch_name}`]({url}) · {pointer.days_stale} dias")
    elif isinstance(pointer, EpicPointer):
        st.markdown(f"**Milestone:** `{pointer.milestone_id}` · ROADMAP `{pointer.roadmap_path}`")
    elif isinstance(pointer, RefinePointer):
        st.markdown(
            f"**Épico:** `{pointer.epic_id}` · "
            f"{pointer.current_state.value} → {pointer.target_state.value}"
        )

    prompt = build_prompt_for_item(
        item,
        all_epics_by_milestone=all_epics_by_milestone,
        epic_lookup=epic_lookup,
    )
    st.markdown("**Prompt (clipboard-ready):**")
    st.code(prompt, language="text")
