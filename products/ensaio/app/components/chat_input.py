"""
Componente chat_input do Ensaio (E-POC-1.4 + E-POC-3.1).

Simplificação POC em relação ao chat_input do Revelar:
- Sem EventBus / métricas inline (fora do escopo da POC).
- Invoca o grafo do Ensaio (orchestrator + structurer) com `product_context`
  injetado no config.configurable (E-POC-2.4).
- Texto do usuário vai cru para o grafo; blocos markdown (code fences, tabelas)
  são preservados no histórico (E-POC-3.1).
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Optional

import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage

from core.agents.orchestrator.state import create_initial_multi_agent_state
from products.ensaio.app.graph import create_ensaio_graph

logger = logging.getLogger(__name__)


def _get_graph():
    """Cria (ou recupera do cache) o grafo do Ensaio."""
    if "ensaio_graph" not in st.session_state:
        st.session_state.ensaio_graph = create_ensaio_graph()
    return st.session_state.ensaio_graph


def _invoke_graph(user_input: str, product_context: Optional[str]) -> dict:
    """Invoca o grafo do Ensaio com product_context e histórico atual de mensagens."""
    graph = _get_graph()
    session_id = st.session_state.session_id
    thread_id = st.session_state.thread_id

    state = create_initial_multi_agent_state(user_input=user_input, session_id=session_id)

    # Anexa o histórico já acumulado na sessão (assim o grafo vê a conversa completa).
    existing_messages = [
        m for m in st.session_state.messages if isinstance(m, (HumanMessage, AIMessage))
    ]
    # O create_initial_multi_agent_state já inclui a nova HumanMessage no state,
    # então prepend existing_messages apenas uma vez.
    state["messages"] = existing_messages + state["messages"]
    if st.session_state.focal_argument is not None:
        state["focal_argument"] = st.session_state.focal_argument

    config = {
        "configurable": {
            "thread_id": thread_id,
            "session_id": session_id,
            "product_context": product_context,
        }
    }

    return graph.invoke(state, config=config)


def render_chat_input(product_context: Optional[str]) -> None:
    """
    Renderiza o form de input e processa a mensagem do usuário.

    Args:
        product_context: String do foco do produto (E-POC-2) a ser injetada no config
            do grafo. Pode ser None se o YAML não estiver disponível (fallback).
    """
    if "processing" not in st.session_state:
        st.session_state.processing = False
    if "pending_message" not in st.session_state:
        st.session_state.pending_message = None

    processing = st.session_state.processing

    # Se há mensagem pendente do rerun anterior, processa agora.
    if processing and st.session_state.pending_message:
        _process_message(st.session_state.pending_message, product_context)
        return

    with st.form(key="ensaio_chat_form", clear_on_submit=True):
        user_input = st.text_area(
            "Mensagem",
            key="ensaio_chat_input",
            placeholder=(
                "Descreva o experimento, cole código, tabelas, observações... "
                "a conversa é livre."
                if not processing
                else "Aguarde o processamento..."
            ),
            height=140,
            label_visibility="collapsed",
            disabled=processing,
        )

        send = st.form_submit_button(
            "Enviar",
            type="primary",
            disabled=processing,
        )

    if send and user_input.strip() and not processing:
        st.session_state.processing = True
        st.session_state.pending_message = user_input.strip()
        st.rerun()


def _process_message(user_input: str, product_context: Optional[str]) -> None:
    """Adiciona a mensagem do usuário, invoca o grafo e grava a resposta."""
    # Adiciona a HumanMessage no histórico da UI.
    st.session_state.messages.append(HumanMessage(content=user_input))

    try:
        result = _invoke_graph(user_input, product_context)

        # Extrai nova AIMessage produzida pelo grafo (última mensagem do result).
        result_messages = result.get("messages", [])
        assistant_message = None
        for msg in reversed(result_messages):
            if isinstance(msg, AIMessage):
                assistant_message = msg
                break

        if assistant_message is None:
            logger.warning("Ensaio: grafo não retornou AIMessage; usando fallback.")
            assistant_message = AIMessage(
                content="Processado, mas não consegui gerar uma resposta conversacional."
            )

        st.session_state.messages.append(assistant_message)
        st.session_state.focal_argument = result.get("focal_argument")

        # Meta para debug (timestamp da última resposta).
        st.session_state.last_turn_at = datetime.now().isoformat()

    except Exception as exc:  # noqa: BLE001
        logger.exception("Ensaio: erro ao processar mensagem: %s", exc)
        st.error(f"Erro ao processar mensagem: {exc}")
        # Remove a HumanMessage adicionada para manter consistência visual.
        if st.session_state.messages and isinstance(
            st.session_state.messages[-1], HumanMessage
        ):
            st.session_state.messages.pop()
    finally:
        st.session_state.processing = False
        st.session_state.pending_message = None

    st.rerun()
