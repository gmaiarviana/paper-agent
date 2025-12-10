"""
Componentes relacionados à timeline de agentes.

Responsável por:
- Histórico de agentes que trabalharam na sessão
- Modal com histórico completo
- Formatação de timestamps
- Seção do Observador com métricas cognitivas (Épico 12.3)
- Seção de Esclarecimentos com perguntas e respostas (Épico 14)
"""

import streamlit as st
import logging
from typing import Dict, Any, List
from datetime import datetime

from utils.event_bus import get_event_bus
from utils.currency import format_currency
from .constants import AGENT_EMOJIS

logger = logging.getLogger(__name__)

# Emojis especiais (não estão em AGENT_EMOJIS)
OBSERVER_EMOJI = "👁️"
CLARIFICATION_EMOJI = "❓"

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

        # Seção de Esclarecimentos (Épico 14)
        # Mostra perguntas de esclarecimento e suas respostas
        clarification_events = [
            e for e in events
            if e.get("event_type") in ("clarification_requested", "clarification_resolved")
        ]
        if clarification_events:
            render_clarification_section(clarification_events)

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

def render_clarification_section(clarification_events: List[Dict[str, Any]]) -> None:
    """
    Renderiza seção de esclarecimentos na timeline (Épico 14).

    Mostra perguntas de esclarecimento feitas e suas resoluções em seção colapsável:
    - Perguntas feitas (clarification_requested)
    - Status de resolução (clarification_resolved)
    - Resumo do que foi esclarecido

    Args:
        clarification_events: Lista de eventos 'clarification_requested' e 'clarification_resolved'

    Example:
        >>> events = [{"event_type": "clarification_requested", "turn_number": 5, ...}]
        >>> render_clarification_section(events)
        # Renderiza: ❓ Esclarecimentos (seção colapsável)
    """
    if not clarification_events:
        return

    st.markdown("---")

    # Contar perguntas e resoluções
    requested = [e for e in clarification_events if e.get("event_type") == "clarification_requested"]
    resolved = [e for e in clarification_events if e.get("event_type") == "clarification_resolved"]

    # Calcular estatísticas
    total_requested = len(requested)
    total_resolved = len([r for r in resolved if r.get("resolution_status") == "resolved"])
    total_partial = len([r for r in resolved if r.get("resolution_status") == "partially_resolved"])

    # Seção colapsável
    with st.expander(f"{CLARIFICATION_EMOJI} **Esclarecimentos** ({total_resolved}/{total_requested})", expanded=False):
        # Mostrar últimos 3 eventos (mais recentes primeiro)
        recent_events = list(reversed(clarification_events))[:5]

        for event in recent_events:
            event_type = event.get("event_type", "")
            turn_number = event.get("turn_number", 0)
            timestamp = event.get("timestamp", "")
            time_str = format_time(timestamp)
            clarification_type = event.get("clarification_type", "")

            # Mapear tipo para label amigável
            type_labels = {
                "contradiction": "Tensão",
                "gap": "Lacuna",
                "confusion": "Confusão",
                "direction_change": "Mudança de direção"
            }
            type_label = type_labels.get(clarification_type, clarification_type.title())

            if event_type == "clarification_requested":
                priority = event.get("priority", "medium")
                question = event.get("question", "")[:100]
                priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(priority, "")

                st.markdown(f"**{CLARIFICATION_EMOJI} Turno {turn_number}** - {type_label} {priority_emoji}")
                st.caption(f"📝 \"{question}...\"" if len(question) == 100 else f"📝 \"{question}\"")
                st.caption(f"{time_str}")

            elif event_type == "clarification_resolved":
                resolution_status = event.get("resolution_status", "")
                summary = event.get("summary", "")[:80]

                status_emoji = {
                    "resolved": "✅",
                    "partially_resolved": "🔶",
                    "unresolved": "❓"
                }.get(resolution_status, "")

                status_label = {
                    "resolved": "Esclarecido",
                    "partially_resolved": "Parcial",
                    "unresolved": "Pendente"
                }.get(resolution_status, resolution_status)

                st.markdown(f"**{status_emoji} Turno {turn_number}** - {type_label} {status_label}")
                if summary:
                    st.caption(f"📋 {summary}")
                st.caption(f"{time_str}")

        # Estatísticas gerais
        st.caption(f"📊 {total_requested} perguntas · {total_resolved} resolvidas · {total_partial} parciais")

        # Botão para ver detalhes completos
        if len(clarification_events) > 5:
            if st.button("Ver todos esclarecimentos", key="view_clarification_details", type="secondary"):
                _show_clarification_modal(clarification_events)

@st.dialog("❓ Esclarecimentos", width="large")
def _show_clarification_modal(events: List[Dict[str, Any]]) -> None:
    """
    Modal para exibir histórico completo de esclarecimentos (Épico 14).

    Mostra todas as perguntas de esclarecimento feitas e suas resoluções:
    - Tipo de esclarecimento (contradição, gap, confusão)
    - Pergunta feita
    - Resposta e status de resolução
    - Atualizações feitas no CognitiveModel

    Args:
        events: Lista de eventos de clarification
    """
    st.markdown("### Histórico de Esclarecimentos")

    # Separar eventos por tipo
    requested = [e for e in events if e.get("event_type") == "clarification_requested"]
    resolved = [e for e in events if e.get("event_type") == "clarification_resolved"]

    st.caption(f"{len(requested)} perguntas feitas · {len(resolved)} respostas analisadas")

    # Mapear tipo para label amigável
    type_labels = {
        "contradiction": "Tensão entre proposições",
        "gap": "Lacuna no argumento",
        "confusion": "Confusão detectada",
        "direction_change": "Mudança de direção"
    }

    # Agrupar por turno para mostrar pergunta + resposta juntas
    events_by_turn = {}
    for event in events:
        turn = event.get("turn_number", 0)
        if turn not in events_by_turn:
            events_by_turn[turn] = []
        events_by_turn[turn].append(event)

    # Mostrar em ordem reversa (mais recente primeiro)
    for turn in sorted(events_by_turn.keys(), reverse=True):
        turn_events = events_by_turn[turn]

        st.markdown(f"#### Turno {turn}")

        for event in turn_events:
            event_type = event.get("event_type", "")
            timestamp = event.get("timestamp", "")
            time_str = format_time(timestamp)
            clarification_type = event.get("clarification_type", "")
            type_label = type_labels.get(clarification_type, clarification_type.title())

            if event_type == "clarification_requested":
                priority = event.get("priority", "medium")
                question = event.get("question", "")
                related_context = event.get("related_context", {})

                priority_emoji = {"high": "🔴 Alta", "medium": "🟡 Média", "low": "🟢 Baixa"}.get(priority, "")

                st.markdown(f"**{CLARIFICATION_EMOJI} Pergunta de Esclarecimento** - {time_str}")
                st.caption(f"Tipo: {type_label} · Prioridade: {priority_emoji}")
                st.info(f"📝 {question}")

                # Contexto relacionado (se disponível)
                if related_context:
                    proposicoes = related_context.get("proposicoes", [])
                    if proposicoes:
                        with st.expander("Proposições relacionadas", expanded=False):
                            for p in proposicoes[:3]:
                                st.caption(f"• {p}")

            elif event_type == "clarification_resolved":
                resolution_status = event.get("resolution_status", "")
                summary = event.get("summary", "")
                updates_made = event.get("updates_made", {})

                status_config = {
                    "resolved": ("✅", "success", "Esclarecido"),
                    "partially_resolved": ("🔶", "warning", "Parcialmente esclarecido"),
                    "unresolved": ("❓", "error", "Não esclarecido")
                }
                emoji, color, label = status_config.get(resolution_status, ("", "info", resolution_status))

                st.markdown(f"**{emoji} Resolução** - {time_str}")

                if color == "success":
                    st.success(f"{label}: {summary}")
                elif color == "warning":
                    st.warning(f"{label}: {summary}")
                elif color == "error":
                    st.error(f"{label}: {summary}")
                else:
                    st.info(f"{label}: {summary}")

                # Atualizações feitas (se disponível)
                if updates_made:
                    with st.expander("Atualizações no modelo", expanded=False):
                        if updates_made.get("contradictions_resolved"):
                            st.caption(f"• {updates_made['contradictions_resolved']} contradição(ões) resolvida(s)")
                        if updates_made.get("proposicoes_added"):
                            st.caption(f"• {updates_made['proposicoes_added']} proposição(ões) adicionada(s)")
                        if updates_made.get("questions_closed"):
                            st.caption(f"• {updates_made['questions_closed']} questão(ões) fechada(s)")

        st.markdown("---")

