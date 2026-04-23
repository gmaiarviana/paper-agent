"""Botão "Gerar artigo" / "Regenerar" do Ensaio (E-POC-1.5, 3.3, 3.4).

Primeira aplicação do padrão declarado em
``core/docs/agents/writer/design.md``: o produto invoca o nó do Writer
diretamente como função Python, fora do grafo conversacional.
"""

from __future__ import annotations

import logging

import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage

from core.agents.writer.nodes import writer_node

logger = logging.getLogger(__name__)


def render_generate_button(product_context: str) -> None:
    """Renderiza o botão de geração e, quando clicado, invoca o Writer.

    Disponível desde o primeiro load (E-POC-3.3: geração prematura permitida).
    Muda o label para "Regenerar" quando já existe artigo em sessão (3.4).
    """
    has_article = bool(st.session_state.get("current_article"))
    label = "🔁 Regenerar" if has_article else "✍️ Gerar artigo"

    generating = st.session_state.get("generating", False)
    clicked = st.button(
        label,
        type="primary",
        use_container_width=True,
        disabled=generating,
        key="ensaio_generate_article_btn",
    )

    if generating:
        st.info("✍️ Writer redigindo o artigo...")

    if clicked and not generating:
        st.session_state.generating = True
        st.rerun()

    if generating and not clicked:
        _run_writer(product_context)
        st.session_state.generating = False
        st.rerun()


def _run_writer(product_context: str) -> None:
    messages = _messages_for_writer()
    focal_argument = st.session_state.get("focal_argument")
    previous_article = st.session_state.get("current_article")

    try:
        result = writer_node(
            {
                "messages": messages,
                "focal_argument": focal_argument,
                "previous_article": previous_article,
                "product_context": product_context,
            }
        )
        article = result.get("article", "").strip()
        if not article:
            st.warning(
                "Writer retornou vazio. Tente enviar mais contexto no chat antes "
                "de regerar."
            )
            return
        st.session_state.current_article = article
        logger.info("Writer gerou artigo de %d chars", len(article))
    except Exception as exc:  # pragma: no cover - depende de API externa
        logger.error("Erro ao invocar Writer: %s", exc, exc_info=True)
        st.error(f"❌ Erro ao gerar artigo: {exc}")


def _messages_for_writer() -> list:
    """Monta o histórico em formato LangChain para o Writer.

    Prefere o histórico já em formato LangChain acumulado pelo ``chat_input``;
    em último caso, converte ``st.session_state.messages`` (dicts usados pelo
    componente de histórico) em ``HumanMessage``/``AIMessage``.
    """
    history = st.session_state.get("langchain_history")
    if history:
        return list(history)

    converted = []
    for msg in st.session_state.get("messages", []):
        role = msg.get("role")
        content = msg.get("content", "")
        if not content:
            continue
        if role == "user":
            converted.append(HumanMessage(content=content))
        elif role == "assistant":
            converted.append(AIMessage(content=content))
    return converted
