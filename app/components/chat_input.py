"""
Componente de input de chat para interface web conversacional (Épico 9.1 + 9.2 + 14.4).

Responsável por:
- Renderizar campo de texto para mensagens do usuário
- Invocar LangGraph quando usuário envia mensagem
- Atualizar histórico de conversa
- Exibir métricas inline (tokens, custo, tempo)
- Feedback visual forte durante processamento (Épico 14.4):
  - Input desabilitado com opacidade 50%
  - Barra inline "Sistema pensando..." com texto dinâmico
  - Texto muda conforme agente ativo

Status: Épico 14.4 - Feedback Visual Forte
"""

import streamlit as st
import logging
from datetime import datetime
from typing import Optional

# Imports do backend
from core.agents.multi_agent_graph import create_multi_agent_graph
from core.agents.orchestrator.state import create_initial_multi_agent_state
from core.utils.event_bus import get_event_bus

logger = logging.getLogger(__name__)

def render_chat_input(session_id: str) -> None:
    """
    Renderiza input de chat e processa mensagens do usuário.

    Args:
        session_id: ID da sessão ativa

    Comportamento (Épico 9.1 + 9.2 + 14.4):
        - Campo de texto para mensagem
        - Botão "Enviar" para submeter
        - Input desabilitado durante processamento (Épico 14.4)
        - Barra inline com texto dinâmico (Épico 14.4)
        - Invoca LangGraph com session_id
        - Atualiza st.session_state.messages com resultado

    Integração:
        - LangGraph: Processa input e retorna resposta do orquestrador
        - EventBus: Eventos são publicados automaticamente pelo grafo
        - Métricas: Tokens, custo e tempo extraídos dos eventos
    """
    # Inicializar estado de processamento
    if "processing" not in st.session_state:
        st.session_state.processing = False
    if "pending_message" not in st.session_state:
        st.session_state.pending_message = None
    if "pending_session_id" not in st.session_state:
        st.session_state.pending_session_id = None

    # Estado de processamento
    processing = st.session_state.processing

    # Se há mensagem pendente e estamos processando, processar agora
    if processing and st.session_state.pending_message:
        _process_user_message(
            st.session_state.pending_message,
            st.session_state.pending_session_id
        )
        return

    # CSS customizado para opacidade do input desabilitado (Épico 14.4)
    _apply_processing_styles()

    # Barra de feedback visual (Épico 14.4)
    if processing:
        _render_processing_feedback(session_id)

    # Usar st.form para melhor UX (permite Enter para enviar)
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_area(
            "Digite sua mensagem:",
            key="chat_input",
            placeholder="Me conte sobre sua ideia ou observação..." if not processing else "Aguarde o processamento...",
            height=100,
            label_visibility="collapsed",
            disabled=processing  # Desabilitar durante processamento (Épico 14.4)
        )

        col1, col2 = st.columns([1, 5])
        with col1:
            send_button = st.form_submit_button(
                "Enviar",
                type="primary",
                use_container_width=True,
                disabled=processing  # Desabilitar durante processamento (Épico 14.4)
            )

    # Processar mensagem quando botão clicado
    if send_button and user_input.strip() and not processing:
        # Primeiro rerun: mostrar feedback de processamento
        st.session_state.processing = True
        st.session_state.pending_message = user_input.strip()
        st.session_state.pending_session_id = session_id
        st.rerun()

def _apply_processing_styles() -> None:
    """
    Aplica CSS customizado para feedback visual durante processamento (Épico 14.4).

    Comportamento:
        - Opacidade 50% em inputs desabilitados
        - Cursor not-allowed
        - Animação suave para barra de processamento
    """
    st.markdown("""
        <style>
        /* Input desabilitado com opacidade 50% (Épico 14.4) */
        .stTextArea textarea:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }

        /* Botão desabilitado */
        .stButton button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }

        /* Barra de processamento com animação suave */
        .processing-bar {
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid #4CAF50;
            animation: pulse 2s ease-in-out infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        </style>
    """, unsafe_allow_html=True)

def _render_processing_feedback(session_id: str) -> None:
    """
    Renderiza barra inline com feedback visual durante processamento (Épico 14.4).

    Args:
        session_id: ID da sessão ativa

    Comportamento:
        - Barra inline: "🤖 Sistema pensando..."
        - Texto dinâmico muda conforme agente ativo:
          - "⚡ Analisando sua mensagem..."
          - "🎯 Orquestrador pensando..."
          - "📝 Estruturador organizando..."
          - "🔬 Metodologista validando..."
        - Animação suave (pulse)

    Integração:
        - Busca último evento do EventBus para determinar agente ativo
        - Fallback: "⚡ Analisando sua mensagem..." se nenhum agente detectado
    """
    # Buscar agente ativo do EventBus
    active_agent = _get_active_agent(session_id)

    # Mapear agente para mensagem
    agent_messages = {
        "orchestrator": "🎯 Orquestrador pensando...",
        "structurer": "📝 Estruturador organizando...",
        "methodologist": "🔬 Metodologista validando...",
        "default": "⚡ Analisando sua mensagem..."
    }

    message = agent_messages.get(active_agent, agent_messages["default"])

    # Renderizar barra com CSS customizado
    st.markdown(
        f"""
        <div class="processing-bar">
            🤖 <strong>Sistema pensando...</strong><br>
            <span style="font-size: 0.9rem; color: #666;">{message}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

def _get_active_agent(session_id: str) -> str:
    """
    Determina qual agente está ativo atualmente baseado no EventBus.

    Args:
        session_id: ID da sessão ativa

    Returns:
        str: Nome do agente ativo ("orchestrator", "structurer", "methodologist")
             ou "default" se nenhum evento encontrado
    """
    try:
        bus = get_event_bus()
        events = bus.get_session_events(session_id)

        # Buscar último evento "agent_started" (agente que começou mas não terminou)
        started_events = [e for e in events if e.get("event_type") == "agent_started"]

        if started_events:
            last_started = started_events[-1]
            return last_started.get("agent_name", "default")

        return "default"

    except Exception as e:
        logger.debug(f"Erro ao determinar agente ativo: {e}")
        return "default"

def _process_user_message(user_input: str, session_id: str) -> None:
    """
    Processa mensagem do usuário invocando LangGraph.

    Args:
        user_input: Mensagem do usuário
        session_id: ID da sessão ativa

    Fluxo (Bugfix Épico 14.4):
        1. Adiciona mensagem do usuário ao histórico
        2. Invoca LangGraph (processamento síncrono)
        3. Extrai resposta do orquestrador
        4. Busca métricas consolidadas do EventBus
        5. Adiciona resposta do sistema ao histórico
        6. Desmarca estado "processing" e limpa mensagem pendente
        7. Re-renderiza interface

    Nota: Esta função é chamada no segundo rerun, após o feedback visual
    já estar visível para o usuário.
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

    # Invocar LangGraph (sem spinner - usar feedback visual customizado)
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

        # Salvar cognitive_model na sessão para exibir solidez (Épico 9.4)
        cognitive_model = result.get("cognitive_model")
        if cognitive_model:
            st.session_state.cognitive_model = cognitive_model
            logger.debug(f"cognitive_model salvo na sessão: claim={cognitive_model.get('claim', '')[:50]}...")

    except Exception as e:
        logger.error(f"Erro ao processar mensagem: {e}", exc_info=True)
        st.error(f"❌ Erro ao processar mensagem: {e}")
        # Remover mensagem do usuário se houve erro
        st.session_state.messages.pop()
    finally:
        # Desmarcar processamento e limpar estado pendente (Épico 14.4)
        st.session_state.processing = False
        st.session_state.pending_message = None
        st.session_state.pending_session_id = None

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

    # Configuração com thread_id e active_idea_id (Épico 9.2)
    # thread_id: preserva histórico entre turnos (LangGraph)
    # active_idea_id: ideia ativa para persistência (Épico 9.3)
    config = {
        "configurable": {
            "thread_id": session_id,
            "active_idea_id": st.session_state.get("active_idea_id")  # Épico 9.2
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
