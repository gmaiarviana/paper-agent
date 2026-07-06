"""Entrypoint Reflex da plataforma de workflow (W-PILOTO-UX-1).

Substitui ``tools/workflow_platform/app.py`` (Streamlit). Layout: sidebar de
filtros/status à esquerda + área principal com título e abas Fila/Kanban.

Executar (a partir de ``tools/workflow_platform/``):
    reflex run
"""

from __future__ import annotations

import reflex as rx

from tools.workflow_platform.web.components.kanban import kanban_tab
from tools.workflow_platform.web.components.queue import queue_tab
from tools.workflow_platform.web.components.sidebar import sidebar
from tools.workflow_platform.web.state import PlatformState


def index() -> rx.Component:
    return rx.hstack(
        sidebar(),
        rx.box(
            rx.heading("🧭 Plataforma de Workflow", size="6"),
            rx.text(
                "Visualiza e direciona épicos de todos os ROADMAPs configurados. "
                "Markdown é fonte da verdade.",
                size="2",
                color_scheme="gray",
                margin_bottom="8px",
            ),
            rx.cond(
                PlatformState.fetch_warning != "",
                rx.callout(
                    "git fetch: " + PlatformState.fetch_warning,
                    icon="triangle-alert",
                    color_scheme="orange",
                    size="1",
                    margin_y="8px",
                ),
                rx.fragment(),
            ),
            rx.tabs.root(
                rx.tabs.list(
                    rx.tabs.trigger("📋 Fila", value="fila"),
                    rx.tabs.trigger("🗂️ Kanban", value="kanban"),
                ),
                rx.tabs.content(queue_tab(), value="fila", padding_top="12px"),
                rx.tabs.content(kanban_tab(), value="kanban", padding_top="12px"),
                value=PlatformState.active_tab,
                on_change=PlatformState.set_active_tab,
                default_value="fila",
                width="100%",
            ),
            padding="16px",
            width="100%",
            height="100vh",
            overflow_y="auto",
        ),
        align="start",
        spacing="0",
        width="100vw",
        height="100vh",
    )


app = rx.App(theme=rx.theme(appearance="light", accent_color="blue"))
app.add_page(index, on_load=PlatformState.on_load, route="/")
