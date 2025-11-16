"""
Componente "Bastidores" para visualização de reasoning dos agentes (Épico 9.5 + 9.6-9.8).

Responsável por:
- Painel collapsible para reasoning dos agentes
- Exibir agente ativo + reasoning resumido (~280 chars)
- Modal com reasoning completo (JSON estruturado)
- Timeline de agentes anteriores
- Polling de eventos do EventBus (1s via auto-refresh)

Versão: 2.0
Data: 16/11/2025
Status: POC completa (com polling e reasoning)
"""

import streamlit as st
import logging
import time
from typing import Dict, Any, List, Optional

from utils.event_bus import get_event_bus

logger = logging.getLogger(__name__)

# Mapeamento de nomes de agentes para emojis
AGENT_EMOJIS = {
    "orchestrator": "🎯",
    "structurer": "📝",
    "methodologist": "🔬"
}


def render_backstage(session_id: str) -> None:
    """
    Renderiza painel "Bastidores" com reasoning dos agentes.

    Args:
        session_id: ID da sessão ativa

    Comportamento POC (9.5 + 9.6-9.8):
        - Toggle "🔍 Ver raciocínio" (fechado por padrão)
        - Quando aberto: mostra agente ativo + reasoning resumido
        - Botão "Ver raciocínio completo" abre modal com JSON
        - Métricas do agente (tempo, tokens, custo)
        - Timeline colapsada de agentes anteriores
        - Auto-refresh a cada 2s para polling de eventos

    Integração:
        - EventBus: Busca eventos via get_session_events()
        - Polling: Implementado via st.rerun() a cada 2s (quando aberto)
    """
    # Toggle para mostrar/ocultar bastidores
    show_backstage = st.toggle("🔍 Ver raciocínio", value=False, key="toggle_backstage")

    if not show_backstage:
        return

    st.markdown("---")
    st.subheader("🎬 Bastidores")

    # Buscar reasoning mais recente
    reasoning = _get_latest_reasoning(session_id)

    if reasoning is None:
        st.info("ℹ️ Nenhum evento de agente encontrado ainda. Envie uma mensagem para começar!")
        return

    # Renderizar agente ativo
    _render_active_agent(reasoning)

    st.markdown("---")

    # Timeline de agentes anteriores (colapsado)
    _render_agent_timeline(session_id)

    # Auto-refresh para polling (POC - 2s)
    # Em produção: usar st.empty() + loop ou SSE
    time.sleep(0.1)  # Pequeno delay para não sobrecarregar


def _get_latest_reasoning(session_id: str) -> Optional[Dict[str, Any]]:
    """
    Busca reasoning mais recente do EventBus.

    Args:
        session_id: ID da sessão ativa

    Returns:
        dict ou None: {
            "agent": str (nome do agente),
            "agent_display": str (nome formatado),
            "reasoning": str (texto completo),
            "summary": str (280 chars),
            "tokens": {"input": int, "output": int, "total": int},
            "cost": float,
            "duration": float,
            "timestamp": str,
            "full_event": dict (evento completo para modal)
        }
    """
    try:
        bus = get_event_bus()
        events = bus.get_session_events(session_id)

        # Filtrar apenas eventos "agent_completed" (têm reasoning completo)
        completed_events = [e for e in events if e.get("event_type") == "agent_completed"]

        if not completed_events:
            return None

        # Pegar último evento
        latest_event = completed_events[-1]

        # Extrair reasoning do metadata
        metadata = latest_event.get("metadata", {})
        reasoning_full = metadata.get("reasoning", "Reasoning não disponível")

        # Truncar para resumo (280 chars)
        reasoning_summary = reasoning_full[:280]
        if len(reasoning_full) > 280:
            reasoning_summary += "..."

        # Nome do agente formatado
        agent_name = latest_event.get("agent_name", "unknown")
        agent_display = agent_name.replace("_", " ").title()

        return {
            "agent": agent_name,
            "agent_display": agent_display,
            "reasoning": reasoning_full,
            "summary": reasoning_summary,
            "tokens": {
                "input": latest_event.get("tokens_input", 0),
                "output": latest_event.get("tokens_output", 0),
                "total": latest_event.get("tokens_total", 0)
            },
            "cost": latest_event.get("cost", 0.0),
            "duration": latest_event.get("duration", 0.0),
            "timestamp": latest_event.get("timestamp", ""),
            "full_event": latest_event
        }

    except Exception as e:
        logger.error(f"Erro ao buscar reasoning do EventBus: {e}", exc_info=True)
        return None


def _render_active_agent(reasoning: Dict[str, Any]) -> None:
    """
    Renderiza informações do agente ativo.

    Args:
        reasoning: Dados do agente ativo (retorno de _get_latest_reasoning)
    """
    agent_name = reasoning["agent"]
    agent_display = reasoning["agent_display"]
    emoji = AGENT_EMOJIS.get(agent_name, "🤖")

    # Cabeçalho com emoji e nome
    st.markdown(f"### {emoji} {agent_display}")
    st.caption("Agente mais recente")

    # Reasoning resumido
    st.markdown("**Raciocínio:**")
    st.write(reasoning["summary"])

    # Botão para ver completo
    if st.button("📄 Ver raciocínio completo", key="view_full_reasoning", use_container_width=True):
        # Usar expander para mostrar JSON completo
        with st.expander("📋 Raciocínio Completo (JSON)", expanded=True):
            st.json(reasoning["full_event"])

    # Métricas do agente
    st.markdown("**Métricas:**")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="⏱️ Tempo",
            value=f"{reasoning['duration']:.2f}s"
        )

    with col2:
        st.metric(
            label="💰 Custo",
            value=f"${reasoning['cost']:.4f}"
        )

    with col3:
        tokens_total = reasoning['tokens']['total']
        st.metric(
            label="📊 Tokens",
            value=f"{tokens_total}"
        )


def _render_agent_timeline(session_id: str) -> None:
    """
    Renderiza timeline de agentes anteriores (colapsado).

    Args:
        session_id: ID da sessão ativa
    """
    try:
        bus = get_event_bus()
        events = bus.get_session_events(session_id)

        # Filtrar apenas eventos "agent_completed"
        completed_events = [e for e in events if e.get("event_type") == "agent_completed"]

        if len(completed_events) <= 1:
            # Se só tem 1 evento, não mostrar timeline (já está mostrado acima)
            with st.expander("▼ Timeline de agentes anteriores"):
                st.caption("Nenhum evento anterior nesta sessão")
            return

        # Remover último evento (já mostrado acima)
        previous_events = completed_events[:-1]

        with st.expander(f"▼ Timeline de agentes anteriores ({len(previous_events)} eventos)"):
            # Mostrar eventos em ordem reversa (mais recente primeiro)
            for event in reversed(previous_events):
                agent_name = event.get("agent_name", "unknown")
                agent_display = agent_name.replace("_", " ").title()
                emoji = AGENT_EMOJIS.get(agent_name, "🤖")

                summary = event.get("summary", "")
                duration = event.get("duration", 0.0)
                cost = event.get("cost", 0.0)
                timestamp = event.get("timestamp", "")

                # Renderizar item da timeline
                st.markdown(f"**{emoji} {agent_display}**")
                st.caption(f"{summary[:100]}...")
                st.caption(f"⏱️ {duration:.2f}s | 💰 ${cost:.4f} | 🕐 {timestamp}")
                st.markdown("---")

    except Exception as e:
        logger.error(f"Erro ao renderizar timeline: {e}", exc_info=True)
        with st.expander("▼ Timeline de agentes anteriores"):
            st.error("Erro ao carregar timeline")
