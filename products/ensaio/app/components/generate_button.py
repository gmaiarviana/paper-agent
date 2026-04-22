"""
Botão de geração do artigo (E-POC-1.5 + E-POC-3.3 + E-POC-3.4).

Invoca o Writer (C-ENSAIO-2) DIRETAMENTE (fora do grafo):
- Primeira geração: `previous_article=None`
- Regeneração: passa `current_article` como `previous_article` e confia que o
  feedback mais recente do usuário já está em `st.session_state.messages`.
"""

from __future__ import annotations

import logging
from typing import Optional

import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage

from core.agents.writer import writer_node

logger = logging.getLogger(__name__)


def _invoke_writer(product_context: Optional[str]) -> None:
    """Invoca writer_node com o estado atual da sessão e atualiza current_article."""
    messages = [
        m for m in st.session_state.messages if isinstance(m, (HumanMessage, AIMessage))
    ]
    writer_state = {
        "messages": messages,
        "focal_argument": st.session_state.focal_argument,
        "previous_article": st.session_state.current_article,
        "product_context": product_context,
    }

    try:
        result = writer_node(writer_state)
    except Exception as exc:  # noqa: BLE001
        logger.exception("Ensaio: erro ao invocar Writer: %s", exc)
        st.error(f"Erro ao gerar artigo: {exc}")
        return

    article = result.get("article")
    if not article:
        st.warning("Writer retornou resposta vazia; tente novamente.")
        return

    st.session_state.current_article = article


def render_generate_button(product_context: Optional[str]) -> None:
    """
    Renderiza o botão "Gerar artigo" / "Regenerar" no topo da coluna direita.

    Args:
        product_context: string de foco do produto, passada ao Writer.
    """
    has_article = bool(st.session_state.get("current_article"))
    label = "Regenerar artigo" if has_article else "Gerar artigo"

    generating = st.session_state.get("generating", False)

    clicked = st.button(
        label,
        type="primary",
        disabled=generating,
        use_container_width=True,
        key="ensaio_generate_button",
    )

    if clicked and not generating:
        st.session_state.generating = True
        with st.spinner("Gerando artigo..."):
            _invoke_writer(product_context)
        st.session_state.generating = False
        st.rerun()
