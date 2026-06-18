"""Painel de chat do Ensaio em Reflex (E-PROTO-1.2, 1.3, 1.4, PROTO-ENSAIO-2).

Renderiza o histórico de mensagens com label de agente em cada bubble,
indicador de processamento inline, manchete "o que mudou" (E-PROTO2-3.2),
bubble especial de proposta de estrutura (E-PROTO2-1.2) e campo de entrada.

Mitigação de React Hooks violation com ``rx.markdown`` em ``rx.foreach``:
o ``react-markdown`` interno usa ``useContext``; montado pela primeira vez
dentro de uma lista, a ordem de hooks varia entre renders e o React aborta
com "change in order of Hooks". Estratégia: (1) ``component_map`` em escopo
de módulo, passado por referência estável a todas as chamadas; (2) instância
invisível pré-montada de ``rx.markdown`` antes do foreach, garantindo que
o provider do contexto exista desde o primeiro render.
"""

from __future__ import annotations

import reflex as rx

from products.ensaio.app.components.proposal_bubble import proposal_bubble
from products.ensaio.app.state import EnsaioState

# Referência estável compartilhada por todas as chamadas de rx.markdown no
# chat. Evita o React rebobinar o useContext entre renders do foreach.
_STABLE_MARKDOWN_COMPONENT_MAP: dict = {}


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

    # E-PROTO2-3.2: manchete "o que mudou" acima do label de agente. Sempre
    # renderiza um Box; visibilidade controlada por `display` para manter
    # contagem de hooks estável (evita React Hooks violation no Reflex).
    change_summary = msg["change_summary"]
    show_headline = (~is_user) & (change_summary != "")

    return rx.box(
        rx.box(
            rx.text(
                change_summary,
                size="1",
                weight="medium",
                color_scheme="blue",
            ),
            display=rx.cond(show_headline, "block", "none"),
            margin_bottom="2px",
        ),
        rx.text(
            label,
            size="1",
            color_scheme="gray",
            weight="bold",
            margin_bottom="2px",
        ),
        rx.box(
            rx.markdown(
                msg["content"],
                component_map=_STABLE_MARKDOWN_COMPONENT_MAP,
            ),
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
    """Indicador de processamento — sempre montado, visibilidade via display."""
    return rx.box(
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
        display=rx.cond(EnsaioState.processing_agent != "", "block", "none"),
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
        # Histórico de mensagens. O rx.markdown pré-montado invisível abaixo
        # garante que o provider de contexto do react-markdown exista desde
        # o primeiro render — sem ele, a primeira mensagem que entra no
        # foreach dispara React Hooks order violation ("useContext").
        rx.box(
            rx.markdown(
                "",
                component_map=_STABLE_MARKDOWN_COMPONENT_MAP,
                display="none",
            ),
            rx.foreach(EnsaioState.messages, _message_bubble),
            _processing_indicator(),
            overflow_y="auto",
            flex="1",
            padding="8px 0",
        ),
        # Bubble especial de proposta de estrutura (E-PROTO2-1.2). Persiste
        # acima do input enquanto pendente; some no aceite/recusa. Input do
        # chat continua habilitado durante a proposta — não bloqueia conversa.
        proposal_bubble(),
        # Área de erro — sempre montada, visibilidade via display.
        rx.box(
            rx.callout(
                EnsaioState.error_message,
                icon="triangle_alert",
                color_scheme="red",
                size="1",
                margin="8px 16px",
            ),
            display=rx.cond(EnsaioState.error_message != "", "block", "none"),
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
