"""
Componentes relacionados à timeline de agentes.

Responsável por:
- Histórico de agentes que trabalharam na sessão
- Modal com histórico completo
- Formatação de timestamps
- Seção do Observador com métricas cognitivas (Épico 12.3)
- Eventos de detecção de mudanças do Observer (Épico 13.5)
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

        # Seção de Detecção de Mudanças (Épico 13.5)
        # Mostra eventos de variação, mudança de direção e checkpoints de clareza
        detection_events = [
            e for e in events
            if e.get("event_type") in [
                "variation_detected",
                "direction_change_confirmed",
                "clarity_checkpoint"
            ]
        ]
        if detection_events:
            render_observer_detection_events(detection_events)

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


# ============================================================================
# Épico 13.5 - Timeline Visual de Mudanças
# ============================================================================


def render_observer_detection_events(detection_events: List[Dict[str, Any]]) -> None:
    """
    Renderiza eventos de detecção de mudanças do Observer (Épico 13.5).

    Mostra eventos de forma discreta e colapsada:
    - Variações detectadas (não interrompem fluxo)
    - Mudanças de direção confirmadas
    - Checkpoints de clareza solicitados

    Args:
        detection_events: Lista de eventos de detecção
            (variation_detected, direction_change_confirmed, clarity_checkpoint)

    Example:
        >>> events = [{"event_type": "variation_detected", "turn_number": 3, ...}]
        >>> render_observer_detection_events(events)
        # Renderiza: 🔍 Detecções (seção colapsável)
    """
    if not detection_events:
        return

    st.markdown("---")

    # Seção colapsável de detecções (discreta por padrão)
    with st.expander("🔍 **Detecções do Observer**", expanded=False):
        # Mostrar últimos 5 eventos de detecção (mais recentes primeiro)
        recent_events = list(reversed(detection_events))[:5]

        for event in recent_events:
            event_type = event.get("event_type", "")
            turn_number = event.get("turn_number", 0)
            timestamp = event.get("timestamp", "")
            time_str = format_time(timestamp)

            if event_type == "variation_detected":
                # ↪️ Variação identificada (não interrompeu fluxo)
                shared = len(event.get("shared_concepts", []))
                new = len(event.get("new_concepts", []))
                st.markdown(f"↪️ **Turno {turn_number}** - Variação identificada")
                st.caption(
                    f"Conceitos mantidos: {shared} · "
                    f"Novos: {new} · "
                    f"{time_str}"
                )

            elif event_type == "direction_change_confirmed":
                # 🔄 Mudança de foco confirmada
                user_confirmed = event.get("user_confirmed", False)
                status = "✅ confirmada" if user_confirmed else "⏳ pendente"
                previous = event.get("previous_claim", "")[:50]
                new_claim = event.get("new_claim", "")[:50]
                st.markdown(f"🔄 **Turno {turn_number}** - Mudança de foco ({status})")
                st.caption(
                    f"De: \"{previous}...\" → Para: \"{new_claim}...\" · "
                    f"{time_str}"
                )

            elif event_type == "clarity_checkpoint":
                # ⚠️ Checkpoint de clareza solicitado
                clarity_level = event.get("clarity_level", "nebulosa")
                clarity_score = event.get("clarity_score", 2)
                suggestion = event.get("suggestion", "")[:80]
                st.markdown(f"⚠️ **Turno {turn_number}** - Checkpoint de clareza")
                st.caption(
                    f"Clareza: {clarity_level} (score {clarity_score}/5) · "
                    f"{time_str}"
                )
                if suggestion:
                    st.caption(f"💡 {suggestion}...")

        # Resumo de detecções
        variation_count = len([e for e in detection_events if e.get("event_type") == "variation_detected"])
        change_count = len([e for e in detection_events if e.get("event_type") == "direction_change_confirmed"])
        checkpoint_count = len([e for e in detection_events if e.get("event_type") == "clarity_checkpoint"])

        st.caption(
            f"📊 {variation_count} variações · "
            f"{change_count} mudanças · "
            f"{checkpoint_count} checkpoints"
        )

        # Botão para ver detalhes completos (se muitos eventos)
        if len(detection_events) > 5:
            if st.button("Ver todas detecções", key="view_detection_details", type="secondary"):
                _show_detection_modal(detection_events)


@st.dialog("🔍 Detecções do Observer", width="large")
def _show_detection_modal(events: List[Dict[str, Any]]) -> None:
    """
    Modal para exibir histórico completo de detecções (Épico 13.5).

    Mostra todos os eventos de detecção com detalhes completos:
    - Variações detectadas
    - Mudanças de direção
    - Checkpoints de clareza

    Args:
        events: Lista de eventos de detecção
    """
    st.markdown("### Histórico de Detecções")
    st.caption(f"O Observer registrou {len(events)} detecções nesta sessão")

    # Contadores por tipo
    variation_count = len([e for e in events if e.get("event_type") == "variation_detected"])
    change_count = len([e for e in events if e.get("event_type") == "direction_change_confirmed"])
    checkpoint_count = len([e for e in events if e.get("event_type") == "clarity_checkpoint"])

    # Resumo em colunas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("↪️ Variações", variation_count)
    with col2:
        st.metric("🔄 Mudanças", change_count)
    with col3:
        st.metric("⚠️ Checkpoints", checkpoint_count)

    st.markdown("---")

    # Mostrar eventos em ordem cronológica reversa
    for event in reversed(events):
        event_type = event.get("event_type", "")
        turn_number = event.get("turn_number", 0)
        timestamp = event.get("timestamp", "")
        time_str = format_time(timestamp)

        if event_type == "variation_detected":
            st.markdown(f"**↪️ Turno {turn_number}** - Variação detectada - {time_str}")
            essence_prev = event.get("essence_previous", "")[:100]
            essence_new = event.get("essence_new", "")[:100]
            analysis = event.get("analysis", "")
            shared = event.get("shared_concepts", [])
            new = event.get("new_concepts", [])

            st.caption(f"📝 Essência anterior: \"{essence_prev}...\"")
            st.caption(f"📝 Nova essência: \"{essence_new}...\"")
            if shared:
                st.caption(f"🔗 Conceitos mantidos: {', '.join(shared[:5])}")
            if new:
                st.caption(f"✨ Novos conceitos: {', '.join(new[:5])}")
            if analysis:
                st.caption(f"💬 {analysis[:150]}...")

        elif event_type == "direction_change_confirmed":
            user_confirmed = event.get("user_confirmed", False)
            status = "✅ Confirmada pelo usuário" if user_confirmed else "⏳ Aguardando confirmação"
            st.markdown(f"**🔄 Turno {turn_number}** - Mudança de direção - {time_str}")
            st.caption(f"Status: {status}")
            st.caption(f"📝 Claim anterior: \"{event.get('previous_claim', '')[:100]}...\"")
            st.caption(f"📝 Novo claim: \"{event.get('new_claim', '')[:100]}...\"")
            reasoning = event.get("reasoning", "")
            if reasoning:
                st.caption(f"💬 Razão: {reasoning[:150]}...")

        elif event_type == "clarity_checkpoint":
            st.markdown(f"**⚠️ Turno {turn_number}** - Checkpoint de clareza - {time_str}")
            clarity_level = event.get("clarity_level", "nebulosa")
            clarity_score = event.get("clarity_score", 2)
            checkpoint_reason = event.get("checkpoint_reason", "")
            factors = event.get("factors", {})
            suggestion = event.get("suggestion", "")

            st.caption(f"📊 Clareza: {clarity_level} (score {clarity_score}/5)")
            if checkpoint_reason:
                st.caption(f"📝 Razão: {checkpoint_reason[:150]}...")
            if factors:
                factors_str = ", ".join([f"{k}: {v}" for k, v in factors.items()])
                st.caption(f"🔍 Fatores: {factors_str}")
            if suggestion:
                st.caption(f"💡 Sugestão: {suggestion}")

        st.markdown("---")

