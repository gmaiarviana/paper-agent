"""Bubble de proposta de estrutura do Estruturador (E-PROTO2-1.2, 1.3).

Renderiza ``EnsaioState.pending_structure_proposal`` como bubble especial
acima do input do chat, com ações Aceitar / Editar / Recusar. Em modo de
edição (E-PROTO2-1.3), permite renomear, reordenar, remover e adicionar
seções antes do aceite.

Componente puro de UI: lê estado e despacha event handlers definidos em
``products.ensaio.app.state``.
"""

from __future__ import annotations

import reflex as rx

from products.ensaio.app.state import EnsaioState


def _proposal_view() -> rx.Component:
    """Modo leitura: lista das seções, racional e três ações."""
    return rx.vstack(
        rx.hstack(
            rx.text("📐", size="3"),
            rx.text(
                "Proposta de estrutura",
                size="2",
                weight="bold",
                color_scheme="blue",
            ),
            spacing="2",
            align="center",
        ),
        rx.cond(
            EnsaioState.proposal_rationale != "",
            rx.text(
                EnsaioState.proposal_rationale,
                size="2",
                color_scheme="gray",
                style={"font_style": "italic"},
            ),
            rx.fragment(),
        ),
        rx.box(
            rx.foreach(
                EnsaioState.proposal_sections,
                lambda title, i: rx.text(
                    rx.text.span(f"{i + 1}. ", weight="bold"),
                    title,
                    size="2",
                    margin_y="2px",
                ),
            ),
            padding="8px 12px",
            background="var(--accent-1)",
            border_radius="6px",
            width="100%",
        ),
        rx.hstack(
            rx.button(
                "Aceitar",
                on_click=EnsaioState.accept_structure_proposal,
                color_scheme="green",
                size="2",
            ),
            rx.button(
                "Editar",
                on_click=EnsaioState.start_editing_proposal,
                color_scheme="blue",
                variant="soft",
                size="2",
            ),
            rx.button(
                "Recusar",
                on_click=EnsaioState.reject_structure_proposal,
                color_scheme="gray",
                variant="soft",
                size="2",
            ),
            spacing="2",
            justify="end",
            width="100%",
        ),
        spacing="2",
        width="100%",
    )


def _proposal_edit_row(title: str, index: int) -> rx.Component:
    return rx.hstack(
        rx.input(
            value=title,
            on_change=lambda v: EnsaioState.update_proposal_section(index, v),
            size="2",
            width="100%",
        ),
        rx.button(
            "↑",
            on_click=lambda: EnsaioState.move_proposal_section(index, -1),
            size="1",
            variant="soft",
        ),
        rx.button(
            "↓",
            on_click=lambda: EnsaioState.move_proposal_section(index, 1),
            size="1",
            variant="soft",
        ),
        rx.button(
            "🗑️",
            on_click=lambda: EnsaioState.remove_proposal_section(index),
            size="1",
            variant="soft",
            color_scheme="red",
        ),
        spacing="1",
        width="100%",
        align="center",
    )


def _proposal_edit() -> rx.Component:
    """Modo edição: renomear / mover / remover / adicionar antes do aceite."""
    return rx.vstack(
        rx.hstack(
            rx.text("📐", size="3"),
            rx.text(
                "Editando estrutura proposta",
                size="2",
                weight="bold",
                color_scheme="blue",
            ),
            spacing="2",
            align="center",
        ),
        rx.foreach(EnsaioState.proposal_draft, _proposal_edit_row),
        rx.button(
            "+ Adicionar seção",
            on_click=EnsaioState.add_proposal_section,
            size="1",
            variant="soft",
        ),
        rx.cond(
            EnsaioState.proposal_edit_error != "",
            rx.text(
                EnsaioState.proposal_edit_error,
                size="1",
                color_scheme="red",
            ),
            rx.fragment(),
        ),
        rx.hstack(
            rx.button(
                "Confirmar edição",
                on_click=EnsaioState.confirm_proposal_edit,
                color_scheme="green",
                size="2",
            ),
            rx.button(
                "Cancelar",
                on_click=EnsaioState.cancel_proposal_edit,
                color_scheme="gray",
                variant="soft",
                size="2",
            ),
            spacing="2",
            justify="end",
            width="100%",
        ),
        spacing="2",
        width="100%",
    )


def proposal_bubble() -> rx.Component:
    """Bubble especial renderizado quando há proposta de estrutura pendente."""
    return rx.cond(
        EnsaioState.has_pending_proposal,
        rx.box(
            rx.cond(
                EnsaioState.editing_proposal,
                _proposal_edit(),
                _proposal_view(),
            ),
            padding="14px 16px",
            margin="8px 16px",
            border="2px solid var(--accent-9)",
            border_radius="10px",
            background="var(--accent-2)",
            width="auto",
        ),
        rx.fragment(),
    )
