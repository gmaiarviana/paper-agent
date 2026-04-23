"""Input de chat do Ensaio — versão própria (E-POC-1.4, 3.1, 3.2).

Não importa EventBus nem métricas inline (POC não usa). Invoca o grafo do
Ensaio passando o ``product_context`` no config.
"""

from __future__ import annotations

import logging
from datetime import datetime

import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage

from products.ensaio.app.graph import create_ensaio_graph

logger = logging.getLogger(__name__)


def render_chat_input(session_id: str, product_context: str) -> None:
    """Renderiza o input de chat e processa mensagens do pesquisador.

    Args:
        session_id: id da sessão / thread_id do checkpointer.
        product_context: foco do produto carregado do YAML (injetado no grafo).
    """
    if "processing" not in st.session_state:
        st.session_state.processing = False
    if "pending_message" not in st.session_state:
        st.session_state.pending_message = None

    processing = st.session_state.processing

    if processing and st.session_state.pending_message:
        _process_user_message(
            st.session_state.pending_message,
            session_id,
            product_context,
        )
        return

    if processing:
        st.info("🤖 Sistema pensando...")

    with st.form(key="ensaio_chat_form", clear_on_submit=True):
        user_input = st.text_area(
            "Digite sua mensagem:",
            key="ensaio_chat_input",
            placeholder=(
                "Conte sobre seu experimento — cole trechos de código, tabelas "
                "ou logs livremente..."
            ),
            height=140,
            label_visibility="collapsed",
            disabled=processing,
        )

        send_button = st.form_submit_button(
            "Enviar",
            type="primary",
            disabled=processing,
        )

    if send_button and user_input.strip() and not processing:
        st.session_state.processing = True
        st.session_state.pending_message = user_input.strip()
        st.rerun()


def _process_user_message(
    user_input: str,
    session_id: str,
    product_context: str,
) -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Preservar formatação original do usuário (E-POC-3.1): sem parsing especial.
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input,
            "tokens": None,
            "cost": None,
            "duration": None,
            "timestamp": datetime.now().isoformat(),
        }
    )

    try:
        result = _invoke_ensaio_graph(user_input, session_id, product_context)

        messages = result.get("messages", [])
        assistant_message = ""
        if messages:
            last = messages[-1]
            assistant_message = (
                last.content if hasattr(last, "content") else str(last)
            )

        if not assistant_message:
            assistant_message = (
                "Entendi. Pode me contar mais sobre o experimento para eu ajudar?"
            )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": assistant_message,
                "tokens": None,
                "cost": None,
                "duration": None,
                "timestamp": datetime.now().isoformat(),
            }
        )

        focal = result.get("focal_argument")
        if focal:
            st.session_state.focal_argument = focal

        # Acumular mensagens em forma LangChain para o Writer consumir depois (3.3).
        langchain_history = st.session_state.get("langchain_history", [])
        langchain_history.append(HumanMessage(content=user_input))
        langchain_history.append(AIMessage(content=assistant_message))
        st.session_state.langchain_history = langchain_history

    except Exception as exc:  # pragma: no cover - depende de API externa
        logger.error("Erro ao processar mensagem do Ensaio: %s", exc, exc_info=True)
        st.error(f"❌ Erro ao processar mensagem: {exc}")
        # Remover mensagem do usuário para permitir nova tentativa
        if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
            st.session_state.messages.pop()
    finally:
        st.session_state.processing = False
        st.session_state.pending_message = None

    st.rerun()


def _invoke_ensaio_graph(
    user_input: str,
    session_id: str,
    product_context: str,
) -> dict:
    graph = create_ensaio_graph()

    state: dict = {
        "user_input": user_input,
        "session_id": session_id,
        "messages": [HumanMessage(content=user_input)],
    }

    config = {
        "configurable": {
            "thread_id": st.session_state.get("thread_id", session_id),
            "product_context": product_context,
        }
    }

    return graph.invoke(state, config=config)
