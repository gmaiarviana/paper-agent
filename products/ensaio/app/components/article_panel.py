"""Painel de artigo seccionado do Ensaio em Reflex (E-PROTO-1.2, 2.1, 2.2, 2.3, 2.4, PROTO-ENSAIO-2).

Renderiza as seções propostas pelo Estruturador como accordion (E-PROTO2-4):
cada seção colapsa/expande individualmente, todas iniciam colapsadas. Mantém
botões de geração por seção, badges de status e edição inline de markdown.
"""

from __future__ import annotations

import reflex as rx

from products.ensaio.app.state import EnsaioState


def _status_badge(status: str) -> rx.Component:
    return rx.match(
        status,
        ("empty", rx.badge("—", color_scheme="gray", size="1")),
        ("draft", rx.badge("Rascunho", color_scheme="orange", size="1")),
        ("edited", rx.badge("Editado", color_scheme="green", size="1")),
        rx.badge(status, size="1"),
    )


def _section_header(section: dict) -> rx.Component:
    """Header colapsável: título + badge de status."""
    return rx.hstack(
        rx.heading(section["title"], size="3"),
        _status_badge(section["status"]),
        justify="between",
        align="center",
        width="100%",
        padding_right="8px",
    )


def _section_body(section: dict) -> rx.Component:
    """Conteúdo expandido: corpo + botão Gerar/Regenerar."""
    return rx.box(
        rx.cond(
            section["body"] == "",
            rx.text(
                "Clique em Gerar para redigir esta seção.",
                color_scheme="gray",
                size="2",
                style={"font_style": "italic"},
                margin_y="8px",
            ),
            rx.box(
                rx.markdown(section["body"]),
                margin_y="8px",
            ),
        ),
        rx.button(
            rx.cond(section["body"] == "", "Gerar", "Regenerar"),
            on_click=EnsaioState.generate_section(section["index"]),
            disabled=EnsaioState.processing_agent != "",
            size="1",
            color_scheme="blue",
            variant="soft",
            margin_top="8px",
        ),
        padding="0 16px 16px 16px",
    )


def _section_item(section: dict) -> rx.Component:
    """Item individual do accordion: header colapsável + corpo."""
    return rx.accordion.item(
        header=_section_header(section),
        content=_section_body(section),
        value=section["index"].to_string(),
        margin_bottom="8px",
        border="1px solid var(--gray-4)",
        border_radius="8px",
        background="white",
        overflow="hidden",
    )


def article_panel() -> rx.Component:
    return rx.flex(
        # Cabeçalho
        rx.box(
            rx.heading("📄 Artigo em construção", size="4"),
            rx.text(
                "Seções propostas pelo Estruturador. "
                "Gere cada seção individualmente.",
                size="2",
                color_scheme="gray",
            ),
            padding="16px",
            border_bottom="1px solid var(--gray-4)",
        ),
        # Indicador de Writer em processamento
        rx.cond(
            EnsaioState.processing_agent == "writer",
            rx.box(
                rx.hstack(
                    rx.spinner(size="1"),
                    rx.text("✍️ Writer redigindo...", size="2", color_scheme="gray"),
                    spacing="2",
                    align="center",
                ),
                padding="8px 16px",
                border_bottom="1px solid var(--gray-4)",
            ),
            rx.fragment(),
        ),
        # Conteúdo do painel
        rx.box(
            rx.cond(
                EnsaioState.current_article.length() > 0,
                # E-PROTO2-4: accordion colapsado por padrão (default_value=[]),
                # múltiplas seções podem estar abertas simultaneamente.
                rx.box(
                    rx.accordion.root(
                        rx.foreach(EnsaioState.current_article, _section_item),
                        type="multiple",
                        collapsible=True,
                        default_value=[],
                        width="100%",
                        variant="ghost",
                    ),
                    padding="16px",
                ),
                # Estado vazio — aguardando proposta do Estruturador
                rx.center(
                    rx.vstack(
                        rx.icon("file_text", size=32, color="var(--gray-8)"),
                        rx.text(
                            "Aguardando proposta de estrutura...",
                            color_scheme="gray",
                            size="3",
                            text_align="center",
                        ),
                        rx.text(
                            "Continue conversando sobre seu experimento. "
                            "Quando o Estruturador tiver contexto suficiente, "
                            "ele proporá as seções do artigo.",
                            color_scheme="gray",
                            size="2",
                            text_align="center",
                            max_width="280px",
                        ),
                        align="center",
                        spacing="3",
                    ),
                    height="100%",
                    padding="40px",
                ),
            ),
            overflow_y="auto",
            flex="1",
        ),
        direction="column",
        height="100vh",
        width="40%",
        background="var(--gray-1)",
        overflow="hidden",
    )
