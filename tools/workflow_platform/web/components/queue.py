"""Aba Fila da plataforma em Reflex (W-PILOTO-UX-1.2).

Paridade com ``views/queue.py`` — banner OVER_LIMIT, cabeçalhos por tipo com
contagem, cards clicáveis. Detecção (``detect_all_items``) e prompts
(``prompts/*``) intocados; esta camada só renderiza os dicts serializados em
``PlatformState.grouped_queue``.
"""

from __future__ import annotations

import reflex as rx

from tools.workflow_platform.web.components.detail import queue_detail_panel
from tools.workflow_platform.web.state import PlatformState


def _over_limit_banner() -> rx.Component:
    return rx.callout(
        "Fila com "
        + PlatformState.queue_items.length().to_string()
        + " itens (limite alvo: 20). Considere fechar itens antes de iniciar "
        "novos. No MVP, o proponente vai pausar criação automaticamente.",
        icon="triangle-alert",
        color_scheme="orange",
        size="1",
        margin_bottom="8px",
    )


def _queue_card(item) -> rx.Component:
    return rx.box(
        rx.button(
            item.card_label,
            on_click=PlatformState.select_item(item.id),
            variant=rx.cond(PlatformState.selected_item_id == item.id, "solid", "surface"),
            width="100%",
            justify_content="start",
            white_space="normal",
            height="auto",
            padding_y="8px",
        ),
        rx.text(item.context, size="1", color_scheme="gray", margin_top="2px"),
        rx.text(item.action_label, size="1", margin_top="2px"),
        margin_bottom="10px",
        width="100%",
    )


def _queue_group(group) -> rx.Component:
    return rx.box(
        rx.heading(
            group.header,
            size="3",
            margin_top="12px",
            margin_bottom="6px",
        ),
        rx.foreach(group.cards, _queue_card),
        rx.divider(margin_y="8px"),
        width="100%",
    )


def queue_tab() -> rx.Component:
    return rx.box(
        rx.cond(PlatformState.is_over_limit, _over_limit_banner(), rx.fragment()),
        rx.cond(
            PlatformState.has_queue_items,
            rx.foreach(PlatformState.grouped_queue, _queue_group),
            rx.callout(
                "Sem itens na fila — nada esperando ação no momento.",
                icon="info",
                size="1",
            ),
        ),
        queue_detail_panel(),
        width="100%",
    )
