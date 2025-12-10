"""
Componentes da seção "📊 Bastidores" relacionados a reasoning dos agentes.

Responsável por:
- Exibição do reasoning do agente ativo
- Modal com raciocínio completo
- Card de pensamento com resumo
"""

import streamlit as st
import logging
from typing import Dict, Any, Optional

from utils.event_bus import get_event_bus
from utils.currency import format_currency, format_currency_precise
from .constants import AGENT_EMOJIS

logger = logging.getLogger(__name__)

def render_backstage(session_id: str) -> None:
    """
    Renderiza seção "📊 Bastidores" colapsável com reasoning dos agentes (Épico 3).

    Args:
        session_id: ID da sessão ativa

    Comportamento:
        - Expander "📊 Bastidores" clicável (colapsado por padrão)
        - Card de pensamento: emoji + nome + reasoning (~280 chars) + link "Ver completo"
        - Estado vazio: 🤖 + "Aguardando..." centralizado
        - Histórico de agentes anteriores

    Integração:
        - EventBus: Busca eventos via get_session_events()
    """
    with st.expander("📊 Bastidores", expanded=False):
        # Buscar reasoning mais recente
        reasoning = _get_latest_reasoning(session_id)

        if reasoning is None:
            # Estado vazio: 🤖 + "Aguardando..." centralizado (Épico 3.2)
            st.markdown(
                """
                <div style='text-align: center; padding: 2rem; color: #666;'>
                    <div style='font-size: 2rem;'>🤖</div>
                    <div>Aguardando...</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            # Renderizar agente ativo
            _render_active_agent(reasoning)

            st.markdown("---")

            # Histórico de agentes anteriores
            from .timeline import render_agent_timeline
            render_agent_timeline(session_id)

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

@st.dialog("🧠 Raciocínio Completo do Agente", width="large")
def _show_reasoning_modal(reasoning: Dict[str, Any]) -> None:
    """
    Modal para exibir raciocínio completo do agente com abas.

    Args:
        reasoning: Dados do agente (retorno de _get_latest_reasoning)

    Layout:
        - Aba 1: Reasoning formatado (markdown)
        - Aba 2: Métricas detalhadas
        - Aba 3: JSON completo (evento completo)
    """
    agent_name = reasoning["agent"]
    agent_display = reasoning["agent_display"]
    emoji = AGENT_EMOJIS.get(agent_name, "🤖")

    # Cabeçalho do modal
    st.markdown(f"### {emoji} {agent_display}")
    st.caption(f"Timestamp: {reasoning['timestamp']}")

    # Abas
    tab1, tab2, tab3 = st.tabs(["📝 Raciocínio", "📊 Métricas", "🔍 JSON Completo"])

    with tab1:
        st.markdown("### Raciocínio Detalhado")

        # Reasoning em markdown (texto formatado)
        reasoning_text = reasoning["reasoning"]
        st.markdown(reasoning_text)

        # Botão para copiar
        if st.button("📋 Copiar raciocínio", key="copy_reasoning"):
            st.code(reasoning_text, language=None)
            st.success("✅ Texto exibido acima. Copie manualmente.")

    with tab2:
        st.markdown("### Métricas Detalhadas")

        # Métricas em grid
        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                label="⏱️ Tempo de Execução",
                value=f"{reasoning['duration']:.2f}s"
            )
            st.metric(
                label="📥 Tokens de Entrada",
                value=f"{reasoning['tokens']['input']:,}"
            )
            st.metric(
                label="📤 Tokens de Saída",
                value=f"{reasoning['tokens']['output']:,}"
            )

        with col2:
            st.metric(
                label="💰 Custo Total",
                value=format_currency_precise(reasoning['cost'])
            )
            st.metric(
                label="📊 Tokens Totais",
                value=f"{reasoning['tokens']['total']:,}"
            )

            # Custo por 1K tokens (se houver tokens)
            if reasoning['tokens']['total'] > 0:
                cost_per_1k = (reasoning['cost'] / reasoning['tokens']['total']) * 1000
                st.metric(
                    label="💵 Custo/1K tokens",
                    value=format_currency(cost_per_1k)
                )

    with tab3:
        st.markdown("### Evento Completo (JSON)")
        st.caption("Estrutura interna do evento publicado no EventBus")

        # JSON completo com syntax highlighting
        st.json(reasoning["full_event"])

        # Botão para copiar JSON
        if st.button("📋 Copiar JSON", key="copy_json"):
            import json
            json_str = json.dumps(reasoning["full_event"], indent=2, ensure_ascii=False)
            st.code(json_str, language="json")
            st.success("✅ JSON exibido acima. Copie manualmente.")

def _render_active_agent(reasoning: Dict[str, Any]) -> None:
    """
    Renderiza informações do agente ativo.

    Args:
        reasoning: Dados do agente ativo (retorno de _get_latest_reasoning)
    """
    agent_name = reasoning["agent"]
    agent_display = reasoning["agent_display"]
    emoji = AGENT_EMOJIS.get(agent_name, "🤖")

    # Cabeçalho com emoji e nome (Épico 3.2)
    st.markdown(f"**{emoji} {agent_display}**")

    # Reasoning resumido (~280 chars)
    st.write(reasoning["summary"])

    # Link discreto para ver completo (abre modal)
    if st.button("Ver completo", key="view_full_reasoning", type="secondary"):
        _show_reasoning_modal(reasoning)

