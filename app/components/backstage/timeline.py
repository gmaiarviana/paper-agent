"""
Componentes relacionados à timeline de agentes.

Responsável por:
- Histórico de agentes que trabalharam na sessão
- Modal com histórico completo
- Formatação de timestamps
"""

import streamlit as st
import logging
from typing import Dict, Any, List
from datetime import datetime

from utils.event_bus import get_event_bus
from utils.currency import format_currency
from .constants import AGENT_EMOJIS

logger = logging.getLogger(__name__)


def render_agent_timeline(session_id: str) -> None:
    """
    Renderiza histórico com últimos 2 agentes anteriores (Épico 3.3).

    Args:
        session_id: ID da sessão ativa

    Comportamento:
        - Header "📜 Histórico"
        - Mostra últimos 2 eventos (atual já está no card de pensamento)
        - Formato: ● emoji + nome curto + horário
        - Link "Ver histórico" abre modal com lista completa
    """
    try:
        bus = get_event_bus()
        events = bus.get_session_events(session_id)

        # Filtrar apenas eventos "agent_completed"
        completed_events = [e for e in events if e.get("event_type") == "agent_completed"]

        # Remover último evento (já mostrado no card de pensamento)
        previous_events = completed_events[:-1] if len(completed_events) > 1 else []

        # Header do histórico
        st.markdown("**📜 Histórico**")

        if not previous_events:
            st.caption("Nenhum evento anterior")
        else:
            # Mostrar apenas últimos 2 eventos (formato simplificado)
            recent_events = list(reversed(previous_events))[:2]

            for event in recent_events:
                agent_name = event.get("agent_name", "unknown")
                # Nome curto: primeiras 3 letras + ponto
                agent_short = agent_name[:3].capitalize() + "."
                emoji = AGENT_EMOJIS.get(agent_name, "🤖")
                timestamp = event.get("timestamp", "")
                time_str = format_time(timestamp)

                st.markdown(f"● {emoji} {agent_short} - {time_str}")

        # Link "Ver histórico" (só mostra se há eventos)
        if completed_events:
            if st.button("Ver histórico", key="view_timeline_history", type="secondary"):
                _show_timeline_modal(completed_events)

    except Exception as e:
        logger.error(f"Erro ao renderizar timeline: {e}", exc_info=True)
        st.error("Erro ao carregar timeline")


@st.dialog("📜 Histórico Completo", width="large")
def _show_timeline_modal(events: List[Dict[str, Any]]) -> None:
    """
    Modal para exibir histórico completo de agentes (Épico 3.3).

    Args:
        events: Lista de eventos "agent_completed"
    """
    st.markdown("### Todos os agentes que trabalharam")
    st.caption(f"{len(events)} eventos nesta sessão")

    # Mostrar eventos em ordem reversa (mais recente primeiro)
    for event in reversed(events):
        agent_name = event.get("agent_name", "unknown")
        agent_display = agent_name.replace("_", " ").title()
        emoji = AGENT_EMOJIS.get(agent_name, "🤖")

        summary = event.get("summary", "")
        timestamp = event.get("timestamp", "")
        duration = event.get("duration", 0.0)
        cost = event.get("cost", 0.0)

        # Extrair horário do timestamp
        time_str = format_time(timestamp)

        st.markdown(f"**{emoji} {agent_display}** - {time_str}")
        st.caption(f"{summary[:150]}..." if len(summary) > 150 else summary)
        st.caption(f"⏱️ {duration:.2f}s | 💰 {format_currency(cost)}")
        st.markdown("---")


def format_time(timestamp: str) -> str:
    """
    Formata timestamp para exibição curta (HH:MM).

    Args:
        timestamp: String de timestamp ISO

    Returns:
        str: Horário formatado (ex: "10:32")
    """
    if not timestamp:
        return "—"
    try:
        dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        return dt.strftime("%H:%M")
    except Exception:
        return timestamp[:5] if len(timestamp) >= 5 else "—"

