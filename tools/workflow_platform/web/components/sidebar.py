"""Sidebar da plataforma em Reflex (W-PILOTO-UX-1.4).

Paridade com ``app._render_sidebar`` — filtro por ROADMAP visível, badge de
carga da fila, botão recarregar e painel de avisos do parser.
"""

from __future__ import annotations

import reflex as rx

from tools.workflow_platform.web.state import PlatformState


def _visible_checkbox(r) -> rx.Component:
    return rx.checkbox(
        r.display,
        checked=r.checked,
        on_change=lambda _v: PlatformState.toggle_roadmap(r.rel),
        size="1",
        margin_y="2px",
    )


def _load_badge() -> rx.Component:
    return rx.box(
        rx.text(
            PlatformState.queue_badge_text,
            weight="bold",
            size="1",
            text_align="center",
        ),
        background=PlatformState.queue_badge_color,
        padding="8px",
        border_radius="6px",
        width="100%",
    )


def _warnings_panel() -> rx.Component:
    return rx.box(
        rx.cond(
            PlatformState.warnings_count > 0,
            rx.foreach(
                PlatformState.warning_lines,
                lambda line: rx.text(line, size="1"),
            ),
            rx.text("sem avisos", size="1", color_scheme="gray"),
        ),
        margin_top="8px",
        padding="8px",
        background="var(--gray-2)",
        border_radius="6px",
        width="100%",
    )


def sidebar() -> rx.Component:
    return rx.box(
        rx.heading("👁️ Visíveis", size="3", margin_bottom="4px"),
        rx.foreach(PlatformState.sidebar_roadmaps, _visible_checkbox),
        rx.divider(margin_y="10px"),
        _load_badge(),
        rx.button(
            "🔄 Recarregar",
            on_click=PlatformState.reload,
            variant="soft",
            width="100%",
            margin_top="8px",
        ),
        rx.divider(margin_y="10px"),
        rx.button(
            "⚠️ Avisos (" + PlatformState.warnings_count.to_string() + ")",
            on_click=PlatformState.toggle_warnings,
            variant="soft",
            width="100%",
        ),
        rx.cond(PlatformState.show_warnings, _warnings_panel(), rx.fragment()),
        width="280px",
        min_width="280px",
        height="100vh",
        overflow_y="auto",
        padding="16px",
        border_right="1px solid var(--gray-4)",
    )
