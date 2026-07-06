"""Aba Kanban da plataforma em Reflex (W-PILOTO-UX-1.3).

Paridade com ``views/kanban.py`` — 8 colunas por estado, cards agrupados por
milestone, painel de detalhe (ações contextuais por estado) acima do board.
Estrutura vem serializada de ``PlatformState.kanban_columns``.
"""

from __future__ import annotations

import reflex as rx

from tools.workflow_platform.web.components.detail import kanban_detail_panel
from tools.workflow_platform.web.state import PlatformState


def _kanban_card(epic) -> rx.Component:
    return rx.button(
        epic.label,
        on_click=PlatformState.select_epic(epic.id),
        variant=rx.cond(epic.selected, "solid", "surface"),
        size="1",
        width="100%",
        justify_content="start",
        white_space="normal",
        height="auto",
        padding_y="6px",
        margin_bottom="4px",
    )


def _kanban_group(group) -> rx.Component:
    return rx.box(
        rx.text(group.milestone_id, weight="bold", size="1", margin_top="6px"),
        rx.foreach(group.epics, _kanban_card),
        width="100%",
    )


def _kanban_column(col) -> rx.Component:
    return rx.box(
        rx.heading(col.state_label, size="2"),
        rx.text(col.count_label, size="1", color_scheme="gray"),
        rx.cond(
            col.groups.length() > 0,
            rx.foreach(col.groups, _kanban_group),
            rx.text("(vazio)", size="1", color_scheme="gray", font_style="italic"),
        ),
        min_width="220px",
        width="220px",
        padding="8px",
        border_right="1px solid var(--gray-3)",
    )


def kanban_tab() -> rx.Component:
    return rx.box(
        kanban_detail_panel(),
        rx.hstack(
            rx.foreach(PlatformState.kanban_columns, _kanban_column),
            align="start",
            spacing="1",
            width="100%",
            overflow_x="auto",
        ),
        width="100%",
    )
