"""Painéis de detalhe (Fila e Kanban) da plataforma em Reflex.

Paridade com ``views/card_detail.py`` + ``views/queue.py::render_queue_item_detail``
da versão Streamlit. O painel da Fila fica no rodapé da aba (paridade de
posição — o reposicionamento na co-visibilidade é W-PILOTO-UX-2); o painel do
Kanban fica acima do board (que é alto).
"""

from __future__ import annotations

import reflex as rx

from tools.workflow_platform.web.state import PlatformState


def prompt_block(label: str, text) -> rx.Component:
    """Bloco de prompt clipboard-ready: rótulo + botão copiar + texto mono."""
    return rx.box(
        rx.hstack(
            rx.text(label, weight="bold", size="1"),
            rx.spacer(),
            rx.button(
                "📋 Copiar",
                size="1",
                variant="soft",
                on_click=rx.set_clipboard(text),
            ),
            width="100%",
            align="center",
        ),
        rx.box(
            rx.text(text, white_space="pre-wrap", font_family="monospace", size="1"),
            background="var(--gray-3)",
            padding="12px",
            border_radius="6px",
            overflow_x="auto",
            margin_top="4px",
            width="100%",
        ),
        width="100%",
        margin_top="8px",
    )


def queue_detail_panel() -> rx.Component:
    item = PlatformState.selected_queue_item
    return rx.cond(
        PlatformState.has_selected_item,
        rx.box(
            rx.hstack(
                rx.heading(item.title_label, size="4"),
                rx.spacer(),
                rx.button(
                    "✕ Fechar",
                    size="1",
                    variant="soft",
                    on_click=PlatformState.close_item,
                ),
                width="100%",
                align="center",
            ),
            rx.text(
                item.meta,
                size="1",
                color_scheme="gray",
            ),
            rx.cond(
                item.pointer_md != "",
                rx.markdown(item.pointer_md),
                rx.fragment(),
            ),
            prompt_block("Prompt (clipboard-ready):", item.prompt),
            border="1px solid var(--gray-4)",
            border_radius="8px",
            padding="16px",
            margin_top="12px",
            width="100%",
        ),
        rx.fragment(),
    )


def _detail_pre(d) -> rx.Component:
    return rx.box(
        rx.callout(d.guidance, icon="info", size="1", margin_top="8px"),
        rx.cond(
            d.show_readiness,
            rx.markdown(
                "Checklist do alvo `🔍`: "
                "`docs/process/refinement/autonomous_readiness.md`"
            ),
            rx.fragment(),
        ),
        rx.cond(
            d.refine_prompt != "",
            prompt_block("Prompt de refinamento (clipboard-ready):", d.refine_prompt),
            rx.fragment(),
        ),
        width="100%",
    )


def _detail_dispatch(d) -> rx.Component:
    return rx.box(
        rx.foreach(
            d.dispatch_warnings,
            lambda w: rx.callout(
                w.text,
                icon="triangle-alert",
                size="1",
                color_scheme=rx.cond(w.blocked, "red", "blue"),
                margin_top="4px",
            ),
        ),
        rx.cond(
            d.dispatch_prompt != "",
            prompt_block("Prompt de dispatch (clipboard-ready):", d.dispatch_prompt),
            rx.fragment(),
        ),
        width="100%",
    )


def _detail_link(d) -> rx.Component:
    return rx.box(
        rx.cond(
            d.warn != "",
            rx.callout(d.warn, icon="triangle-alert", color_scheme="orange", size="1", margin_top="8px"),
            rx.fragment(),
        ),
        rx.cond(d.link_md != "", rx.markdown(d.link_md), rx.fragment()),
        width="100%",
    )


def _detail_blocked(d) -> rx.Component:
    return rx.box(
        rx.callout(
            "🔒 Bloqueado por " + d.blocked_by + " (precisa estar ✅)",
            icon="lock",
            color_scheme="gray",
            size="1",
            margin_top="8px",
        ),
        width="100%",
    )


def _detail_done(d) -> rx.Component:
    return rx.box(
        rx.callout("Épico implementado.", icon="circle-check", color_scheme="green", size="1", margin_top="8px"),
        rx.text("Resumo do bloco:", weight="bold", size="1", margin_top="8px"),
        rx.box(
            rx.text(d.excerpt, white_space="pre-wrap", font_family="monospace", size="1"),
            background="var(--gray-3)",
            padding="12px",
            border_radius="6px",
        ),
        width="100%",
    )


def kanban_detail_panel() -> rx.Component:
    d = PlatformState.kanban_detail
    return rx.cond(
        PlatformState.has_kanban_detail,
        rx.box(
            rx.hstack(
                rx.heading(d.header, size="4"),
                rx.spacer(),
                rx.button("✕ Fechar", size="1", variant="soft", on_click=PlatformState.close_epic),
                width="100%",
                align="center",
            ),
            rx.text(
                d.meta,
                size="1",
                color_scheme="gray",
            ),
            rx.match(
                d.kind,
                ("pre", _detail_pre(d)),
                ("dispatch", _detail_dispatch(d)),
                ("blocked", _detail_blocked(d)),
                ("in_progress", _detail_link(d)),
                ("in_review", _detail_link(d)),
                ("done", _detail_done(d)),
                rx.fragment(),
            ),
            border="1px solid var(--gray-4)",
            border_radius="8px",
            padding="16px",
            margin_bottom="12px",
            width="100%",
        ),
        rx.fragment(),
    )
