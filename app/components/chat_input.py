"""
Componente de input de chat para interface web conversacional (Épico 9.1 + 9.2).

Responsável por:
- Renderizar campo de texto para mensagens do usuário
- Invocar LangGraph quando usuário envia mensagem
- Atualizar histórico de conversa
- Exibir métricas inline (tokens, custo, tempo)

Versão: 3.0
Data: 16/11/2025
Status: Protótipo completo (localStorage - Épico 9.9)
"""

import streamlit as st
import logging
from datetime import datetime
from typing import Optional

# Imports do backend
from agents.multi_agent_graph import create_multi_agent_graph
from agents.orchestrator.state import create_initial_multi_agent_state
from utils.event_bus import get_event_bus

# Import localStorage (Épico 9.9 - Protótipo)
from app.components.storage import (
    save_session_messages,
    save_session_metadata,
    add_session_to_list
)

logger = logging.getLogger(__name__)


def render_chat_input(session_id: str) -> None:
    """
    Renderiza input de chat e processa mensagens do usuário.

    Args:
        session_id: ID da sessão ativa

    Comportamento POC (9.1 + 9.2):
        - Campo de texto para mensagem
        - Botão "Enviar" para submeter
        - Spinner durante processamento
        - Invoca LangGraph com session_id
        - Atualiza st.session_state.messages com resultado

    Integração:
        - LangGraph: Processa input e retorna resposta do orquestrador
        - EventBus: Eventos são publicados automaticamente pelo grafo
        - Métricas: Tokens, custo e tempo extraídos dos eventos
    """
    # Usar st.form para melhor UX (permite Enter para enviar)
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_area(
            "Digite sua mensagem:",
            key="chat_input",
            placeholder="Me conte sobre sua ideia ou observação...",
            height=100,
            label_visibility="collapsed"
        )

        col1, col2 = st.columns([1, 5])
        with col1:
            send_button = st.form_submit_button("Enviar", type="primary", use_container_width=True)

    # Processar mensagem quando botão clicado
    if send_button and user_input.strip():
        _process_user_message(user_input.strip(), session_id)


def _process_user_message(user_input: str, session_id: str) -> None:
    """
    Processa mensagem do usuário invocando LangGraph.

    Args:
        user_input: Mensagem do usuário
        session_id: ID da sessão ativa

    Fluxo:
        1. Adiciona mensagem do usuário ao histórico
        2. Invoca LangGraph (mostra spinner)
        3. Extrai resposta do orquestrador
        4. Busca métricas consolidadas do EventBus
        5. Adiciona resposta do sistema ao histórico
        6. Re-renderiza interface
    """
    # Inicializar histórico se necessário
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Adicionar mensagem do usuário (sem métricas ainda)
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "tokens": None,
        "cost": None,
        "duration": None,
        "timestamp": datetime.now().isoformat()
    })

    # Invocar LangGraph com spinner
    with st.spinner("🤖 Sistema está pensando..."):
        try:
            result = _invoke_langgraph(user_input, session_id)

            # Extrair resposta do orquestrador
            # A mensagem está em messages[-1].content (último AIMessage)
            messages = result.get("messages", [])
            if messages and len(messages) > 0:
                # Pegar última mensagem (AIMessage do orquestrador)
                last_message = messages[-1]
                assistant_message = last_message.content if hasattr(last_message, 'content') else str(last_message)
            else:
                # Fallback se não houver mensagens
                logger.warning(f"Nenhuma mensagem encontrada no resultado. Usando fallback.")
                assistant_message = "Sistema processou mas não retornou mensagem. Verifique os logs."

            # Debug logging
            logger.info(f"Mensagem extraída do orquestrador: {assistant_message[:100]}...")

            # Buscar métricas consolidadas do EventBus
            metrics = _get_latest_metrics(session_id)

            # Adicionar resposta do sistema ao histórico
            st.session_state.messages.append({
                "role": "assistant",
                "content": assistant_message,
                "tokens": metrics.get("tokens"),
                "cost": metrics.get("cost"),
                "duration": metrics.get("duration"),
                "timestamp": datetime.now().isoformat()
            })

            logger.info(f"Mensagem processada com sucesso (sessão: {session_id[:8]}...)")

            # Salvar no localStorage (Épico 9.9 - Protótipo)
            _save_to_localstorage(session_id, user_input)

        except Exception as e:
            logger.error(f"Erro ao processar mensagem: {e}", exc_info=True)
            st.error(f"❌ Erro ao processar mensagem: {e}")
            # Remover mensagem do usuário se houve erro
            st.session_state.messages.pop()
            return

    # Re-renderizar interface (force update)
    st.rerun()


def _invoke_langgraph(user_input: str, session_id: str) -> dict:
    """
    Invoca LangGraph e retorna resultado.

    Args:
        user_input: Mensagem do usuário
        session_id: ID da sessão ativa

    Returns:
        dict: Estado final do grafo com:
            - orchestrator_output: {message, next_step, agent_suggestion, ...}
            - next_step: "explore", "clarify", "suggest_agent", etc
            - orchestrator_analysis: reasoning completo
            - ... (outros campos do MultiAgentState)

    Raises:
        Exception: Se houver erro na execução do grafo
    """
    logger.info(f"Invocando LangGraph para sessão {session_id[:8]}...")

    # Criar grafo (singleton - cache em produção)
    graph = create_multi_agent_graph()

    # Criar estado inicial
    state = create_initial_multi_agent_state(
        user_input=user_input,
        session_id=session_id
    )

    # Configuração com thread_id (preserva histórico entre turnos)
    config = {
        "configurable": {
            "thread_id": session_id
        }
    }

    # Invocar grafo
    result = graph.invoke(state, config=config)

    logger.debug(f"LangGraph executado. Next step: {result.get('next_step')}")

    return result


def _get_latest_metrics(session_id: str) -> dict:
    """
    Busca métricas consolidadas do último turno no EventBus.

    Args:
        session_id: ID da sessão ativa

    Returns:
        dict: {
            "tokens": {"input": int, "output": int, "total": int},
            "cost": float,
            "duration": float
        }

    Nota:
        Consolida métricas de todos os agentes executados no último turno.
        Se múltiplos agentes foram chamados (ex: orchestrator → structurer),
        soma tokens/custo e usa duração total.
    """
    try:
        bus = get_event_bus()
        events = bus.get_session_events(session_id)

        # Filtrar apenas eventos "agent_completed" do último turno
        # (assumir que último turno = eventos após último "agent_started" do orchestrator)
        completed_events = [e for e in events if e.get("event_type") == "agent_completed"]

        if not completed_events:
            logger.warning(f"Nenhum evento agent_completed encontrado para {session_id}")
            return {"tokens": None, "cost": None, "duration": None}

        # Consolidar métricas (soma tokens/custo, max duration)
        total_tokens_input = 0
        total_tokens_output = 0
        total_cost = 0.0
        max_duration = 0.0

        # Pegar apenas eventos do último turno (últimos N eventos - heurística: últimos 5)
        recent_events = completed_events[-5:]

        for event in recent_events:
            total_tokens_input += event.get("tokens_input", 0)
            total_tokens_output += event.get("tokens_output", 0)
            total_cost += event.get("cost", 0.0)
            max_duration = max(max_duration, event.get("duration", 0.0))

        total_tokens = total_tokens_input + total_tokens_output

        logger.debug(f"Métricas consolidadas: {total_tokens} tokens, ${total_cost:.4f}, {max_duration:.2f}s")

        return {
            "tokens": {
                "input": total_tokens_input,
                "output": total_tokens_output,
                "total": total_tokens
            },
            "cost": total_cost,
            "duration": max_duration
        }

    except Exception as e:
        logger.warning(f"Erro ao buscar métricas do EventBus: {e}")
        return {"tokens": None, "cost": None, "duration": None}


def _save_to_localstorage(session_id: str, user_input: str) -> None:
    """
    Salva histórico e metadados no localStorage (Épico 9.9 - Protótipo).

    Args:
        session_id: ID da sessão ativa
        user_input: Primeiro input do usuário (para gerar título)

    Comportamento:
        - Salva st.session_state.messages no localStorage
        - Atualiza metadados da sessão (título, última atividade)
        - Adiciona sessão à lista de sessões
    """
    try:
        # Salvar mensagens
        messages = st.session_state.get("messages", [])
        save_session_messages(session_id, messages)

        # Gerar/atualizar metadados
        message_count = len(messages)

        # Auto-gerar título baseado no primeiro input do usuário
        title = _generate_session_title(messages, user_input)

        metadata = {
            "title": title,
            "created_at": messages[0]["timestamp"] if messages else datetime.now().isoformat(),
            "last_activity": datetime.now().isoformat(),
            "message_count": message_count
        }

        save_session_metadata(session_id, metadata)

        # Adicionar à lista de sessões (evita duplicatas automaticamente)
        add_session_to_list(session_id)

        logger.debug(f"Sessão salva no localStorage: {session_id[:8]}... ({message_count} mensagens)")

    except Exception as e:
        logger.warning(f"Erro ao salvar no localStorage: {e}")
        # Não interromper fluxo se localStorage falhar


def _generate_session_title(messages: list, user_input: str) -> str:
    """
    Gera título automático para a sessão baseado no primeiro input.

    Args:
        messages: Lista de mensagens da sessão
        user_input: Input atual do usuário

    Returns:
        str: Título da sessão (max 50 chars)

    Estratégia:
        - Se é primeira mensagem: usar user_input truncado
        - Se já existe título nos metadados: manter
        - Fallback: "Conversa {data}"
    """
    # Se é primeira mensagem do usuário (índice 0 ou 1), usar como título
    user_messages = [m for m in messages if m.get("role") == "user"]

    if len(user_messages) <= 1 and user_input:
        # Primeira interação - usar input como título
        title = user_input[:50]
        if len(user_input) > 50:
            title += "..."
        return title
    elif user_messages:
        # Usar primeira mensagem como título (já salvo antes)
        first_user_msg = user_messages[0]["content"]
        title = first_user_msg[:50]
        if len(first_user_msg) > 50:
            title += "..."
        return title
    else:
        # Fallback
        return f"Conversa {datetime.now().strftime('%d/%m/%Y %H:%M')}"
