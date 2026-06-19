"""Painel de chat do Ensaio em Reflex (E-PROTO-1.2, 1.3, 1.4).

Renderiza o histórico de mensagens com label de agente em cada bubble,
indicador de processamento inline e campo de entrada.
"""

from __future__ import annotations

import reflex as rx

from products.ensaio.app.state import EnsaioState


def _message_bubble(msg: dict) -> rx.Component:
    is_user = msg["role"] == "user"
    label = rx.cond(
        is_user,
        "👤 Você",
        rx.match(
            msg["agent"],
            ("orchestrator", "🎯 Orquestrador"),
            ("structurer", "📐 Estruturador"),
            ("methodologist", "🔬 Metodologista"),
            ("writer", "✍️ Writer"),
            "🤖 Sistema",
        ),
    )

    return rx.box(
        rx.text(
            label,
            size="1",
            color_scheme="gray",
            weight="bold",
            margin_bottom="2px",
        ),
        rx.box(
            rx.text(msg["content"], white_space="pre-wrap"),
            background=rx.cond(is_user, "var(--accent-3)", "var(--gray-2)"),
            border_radius="8px",
            padding="12px 16px",
            max_width="90%",
        ),
        align_items=rx.cond(is_user, "flex-end", "flex-start"),
        display="flex",
        flex_direction="column",
        width="100%",
        padding_x="8px",
        padding_y="4px",
    )


def _processing_indicator() -> rx.Component:
    return rx.cond(
        EnsaioState.processing_agent != "",
        rx.box(
            rx.hstack(
                rx.spinner(size="1"),
                rx.match(
                    EnsaioState.processing_agent,
                    ("orchestrator", rx.text("🎯 Orquestrador processando...", size="2", color_scheme="gray")),
                    ("structurer", rx.text("📐 Estruturador processando...", size="2", color_scheme="gray")),
                    ("methodologist", rx.text("🔬 Metodologista processando...", size="2", color_scheme="gray")),
                    ("writer", rx.text("✍️ Writer redigindo...", size="2", color_scheme="gray")),
                    rx.text("🤖 Sistema processando...", size="2", color_scheme="gray"),
                ),
                spacing="2",
                align="center",
            ),
            padding="8px 16px",
        ),
        rx.fragment(),
    )


def chat_panel() -> rx.Component:
    return rx.flex(
        # Cabeçalho
        rx.box(
            rx.heading("💬 Conversa sobre o experimento", size="4"),
            rx.text(
                "Conte sobre seu experimento — cole trechos de código, "
                "tabelas ou logs livremente.",
                size="2",
                color_scheme="gray",
            ),
            padding="16px",
            border_bottom="1px solid var(--gray-4)",
        ),
        # Histórico de mensagens
        rx.box(
            rx.foreach(EnsaioState.messages, _message_bubble),
            _processing_indicator(),
            overflow_y="auto",
            flex="1",
            padding="8px 0",
        ),
        # Área de erro
        rx.cond(
            EnsaioState.error_message != "",
            rx.callout(
                EnsaioState.error_message,
                icon="triangle_alert",
                color_scheme="red",
                size="1",
                margin="8px 16px",
            ),
            rx.fragment(),
        ),
        # Campo de entrada
        rx.box(
            rx.vstack(
                rx.text_area(
                    placeholder=(
                        "Descreva seu experimento, cole código ou resultados..."
                    ),
                    value=EnsaioState.user_input_field,
                    on_change=EnsaioState.set_user_input_field,
                    disabled=EnsaioState.processing_agent != "",
                    rows="4",
                    width="100%",
                    resize="vertical",
                ),
                rx.button(
                    "Enviar",
                    on_click=EnsaioState.send_message,
                    disabled=EnsaioState.processing_agent != "",
                    color_scheme="blue",
                    width="100%",
                ),
                spacing="2",
                width="100%",
            ),
            padding="12px 16px",
            border_top="1px solid var(--gray-4)",
        ),
        direction="column",
        height="100vh",
        width="60%",
        border_right="1px solid var(--gray-4)",
        overflow="hidden",
    )
