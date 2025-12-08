"""
Componentes relacionados à timeline de agentes.

Responsável por:
- Histórico de agentes que trabalharam na sessão
- Modal com histórico completo
- Formatação de timestamps
- Seção do Observador com métricas cognitivas (Épico 12.3)
"""

import streamlit as st
import logging
from typing import Dict, Any, List
from datetime import datetime

from utils.event_bus import get_event_bus
from utils.currency import format_currency
from .constants import AGENT_EMOJIS

logger = logging.getLogger(__name__)

# Emoji do Observer (não está em AGENT_EMOJIS por ser agente especial)
OBSERVER_EMOJI = "👁️"


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

        # Seção do Observer (Épico 12.3)
        # Mostra atividade do Observer em seção separada
        observer_events = [e for e in events if e.get("event_type") == "cognitive_model_updated"]
        if observer_events:
            render_observer_section(observer_events)

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


def render_observer_section(observer_events: List[Dict[str, Any]]) -> None:
    """
    Renderiza seção do Observer na timeline (Épico 12.3).

    Mostra atividade do Observer em seção colapsável com:
    - Últimos turnos processados
    - Métricas: conceitos detectados, solidez
    - Link para modal com detalhes completos

    Args:
        observer_events: Lista de eventos 'cognitive_model_updated'

    Example:
        >>> events = [{"event_type": "cognitive_model_updated", "turn_number": 1, ...}]
        >>> render_observer_section(events)
        # Renderiza: 👁️ Observador (seção colapsável)
    """
    if not observer_events:
        return

    st.markdown("---")

    # Seção colapsável do Observer
    with st.expander(f"{OBSERVER_EMOJI} **Observador**", expanded=False):
        # Mostrar últimos 3 eventos do Observer (mais recentes primeiro)
        recent_events = list(reversed(observer_events))[:3]

        for event in recent_events:
            turn_number = event.get("turn_number", 0)
            timestamp = event.get("timestamp", "")
            time_str = format_time(timestamp)

            # Extrair métricas do evento
            solidez = event.get("solidez", 0.0)
            concepts_count = event.get("concepts_count", 0)
            proposicoes_count = event.get("proposicoes_count", 0)
            is_mature = event.get("is_mature", False)

            # Indicador de maturidade
            maturity_indicator = "✅" if is_mature else ""

            st.markdown(f"**{OBSERVER_EMOJI} Turno {turn_number}** {maturity_indicator}")
            st.caption(
                f"🧠 {concepts_count} conceitos · "
                f"📊 {proposicoes_count} proposições · "
                f"Solidez: {solidez:.0%} · "
                f"{time_str}"
            )

        # Mostrar total de turnos processados
        st.caption(f"📈 {len(observer_events)} turnos analisados")

        # Botão para ver detalhes completos
        if len(observer_events) > 3:
            if st.button("Ver análise completa", key="view_observer_details", type="secondary"):
                _show_observer_modal(observer_events)


@st.dialog("👁️ Análise do Observador", width="large")
def _show_observer_modal(events: List[Dict[str, Any]]) -> None:
    """
    Modal para exibir histórico completo do Observer (Épico 12.3).

    Mostra todos os turnos processados com métricas detalhadas:
    - Solidez e completude
    - Conceitos detectados
    - Contradições encontradas
    - Questões abertas

    Args:
        events: Lista de eventos 'cognitive_model_updated'
    """
    st.markdown("### Evolução do Argumento")
    st.caption(f"O Observer analisou {len(events)} turnos nesta sessão")

    # Mostrar eventos em ordem cronológica reversa (mais recente primeiro)
    for event in reversed(events):
        turn_number = event.get("turn_number", 0)
        timestamp = event.get("timestamp", "")
        time_str = format_time(timestamp)

        # Métricas principais
        solidez = event.get("solidez", 0.0)
        completude = event.get("completude", 0.0)
        is_mature = event.get("is_mature", False)

        # Contadores
        concepts_count = event.get("concepts_count", 0)
        proposicoes_count = event.get("proposicoes_count", 0)
        open_questions_count = event.get("open_questions_count", 0)
        contradictions_count = event.get("contradictions_count", 0)

        # Metadata extra
        metadata = event.get("metadata", {})
        processing_time = metadata.get("processing_time_ms", 0)
        claim_preview = metadata.get("claim", "")[:100]

        # Status de maturidade
        status_emoji = "✅ Maduro" if is_mature else "🔄 Em desenvolvimento"

        st.markdown(f"**{OBSERVER_EMOJI} Turno {turn_number}** - {time_str}")

        # Afirmação central (se disponível)
        if claim_preview:
            st.caption(f"📝 \"{claim_preview}...\"")

        # Métricas em colunas
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Solidez", f"{solidez:.0%}")
            st.caption(f"🧠 {concepts_count} conceitos")
            st.caption(f"📊 {proposicoes_count} proposições")
        with col2:
            st.metric("Completude", f"{completude:.0%}")
            st.caption(f"❓ {open_questions_count} questões abertas")
            st.caption(f"⚠️ {contradictions_count} contradições")

        # Status e tempo de processamento
        st.caption(f"{status_emoji} · Processado em {processing_time:.0f}ms")
        st.markdown("---")

