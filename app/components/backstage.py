"""
Componentes do Painel Direito: Contexto + Bastidores (Épico 3 + 4).

Responsável por:
- Seção "💡 Contexto" (Épico 4): ideia ativa, status, custo acumulado
- Seção "📊 Bastidores" (Épico 3): reasoning dos agentes, histórico
- Card de pensamento: emoji + nome + reasoning resumido (~280 chars) + link "Ver completo"
- Estado vazio: 🤖 + "Aguardando..." centralizado
- Modal de raciocínio completo (JSON estruturado)
- Modal de detalhes da conversa (custos, métricas)

Estrutura:
┌──────────────────────┐
│ 💡 Contexto [▼]      │  ← Expander (expandido por padrão)
│ └─ Ideia ativa       │
│ └─ Custo acumulado   │
├──────────────────────┤
│ 📊 Bastidores [▶]    │  ← Expander (colapsado por padrão)
│ └─ Reasoning         │
│ └─ Histórico         │
└──────────────────────┘

Versão: 4.1
Data: 04/12/2025
Status: Épico 3 + 4 implementados
"""

import streamlit as st
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from utils.event_bus import get_event_bus
from utils.currency import format_currency, format_currency_precise
from agents.database.manager import get_database_manager

logger = logging.getLogger(__name__)

# Mapeamento de nomes de agentes para emojis
AGENT_EMOJIS = {
    "orchestrator": "🎯",
    "structurer": "📝",
    "methodologist": "🔬"
}


def render_right_panel(session_id: str) -> None:
    """
    Renderiza painel direito completo: Contexto + Bastidores (Épico 4.1).

    Args:
        session_id: ID da sessão ativa

    Estrutura:
        1. Seção "💡 Contexto" (expandida por padrão)
           - Ideia ativa (título, status, metadados)
           - Custo acumulado
        2. Seção "📊 Bastidores" (colapsada por padrão)
           - Reasoning dos agentes, histórico
    """
    # Seção 1: Contexto (acima)
    render_context_section(session_id)

    # Seção 2: Bastidores (abaixo)
    render_backstage(session_id)


def render_context_section(session_id: str) -> None:
    """
    Renderiza seção "💡 Contexto" colapsável (Épico 4.1 + 4.3).

    Args:
        session_id: ID da sessão ativa

    Comportamento:
        - Expander "💡 Contexto" clicável para expandir/colapsar
        - Expandido por padrão
        - Contém: ideia ativa (título, status, metadados)
        - Contém: custo acumulado da conversa (4.3)
    """
    with st.expander("💡 Contexto", expanded=True):
        _render_idea_status(session_id)
        _render_accumulated_cost(session_id)


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
            _render_agent_timeline(session_id)


def _get_session_accumulated_cost(session_id: str) -> Dict[str, Any]:
    """
    Calcula custo e tokens acumulados da sessão (Épico 4.3).

    Args:
        session_id: ID da sessão ativa

    Returns:
        dict: {"cost": float, "tokens": int, "num_events": int}
    """
    try:
        bus = get_event_bus()
        events = bus.get_session_events(session_id)

        # Filtrar eventos "agent_completed"
        completed_events = [e for e in events if e.get("event_type") == "agent_completed"]

        if not completed_events:
            return {"cost": 0.0, "tokens": 0, "num_events": 0}

        # Somar custos e tokens
        total_cost = sum(e.get("cost", 0.0) for e in completed_events)
        total_tokens = sum(e.get("tokens_total", 0) for e in completed_events)

        return {
            "cost": total_cost,
            "tokens": total_tokens,
            "num_events": len(completed_events)
        }

    except Exception as e:
        logger.error(f"Erro ao calcular custo acumulado: {e}", exc_info=True)
        return {"cost": 0.0, "tokens": 0, "num_events": 0}


def _get_session_events_details(session_id: str) -> List[Dict[str, Any]]:
    """
    Busca detalhes de todos os eventos da sessão para o modal (Épico 4.4).

    Args:
        session_id: ID da sessão ativa

    Returns:
        list: Lista de eventos com detalhes (agente, custo, tokens, timestamp)
    """
    try:
        bus = get_event_bus()
        events = bus.get_session_events(session_id)

        # Filtrar eventos "agent_completed"
        completed_events = [e for e in events if e.get("event_type") == "agent_completed"]

        details = []
        for event in completed_events:
            agent_name = event.get("agent_name", "unknown")
            details.append({
                "agent": agent_name,
                "agent_display": agent_name.replace("_", " ").title(),
                "emoji": AGENT_EMOJIS.get(agent_name, "🤖"),
                "cost": event.get("cost", 0.0),
                "tokens_input": event.get("tokens_input", 0),
                "tokens_output": event.get("tokens_output", 0),
                "tokens_total": event.get("tokens_total", 0),
                "duration": event.get("duration", 0.0),
                "timestamp": event.get("timestamp", ""),
                "model": event.get("model", "claude-3-5-sonnet")
            })

        return details

    except Exception as e:
        logger.error(f"Erro ao buscar detalhes de eventos: {e}", exc_info=True)
        return []


@st.dialog("📊 Detalhes da Conversa", width="large")
def _show_context_details_modal(session_id: str, accumulated: Dict[str, Any]) -> None:
    """
    Modal com detalhes expandidos do contexto (Épico 4.4).

    Args:
        session_id: ID da sessão ativa
        accumulated: Dict com custo/tokens acumulados

    Conteúdo:
        - Aba 1: Custos por agente
        - Aba 2: Métricas detalhadas
    """
    # Buscar detalhes dos eventos
    events_details = _get_session_events_details(session_id)

    # Abas
    tab1, tab2 = st.tabs(["💰 Custos", "📊 Métricas"])

    with tab1:
        st.markdown("### Custo por Chamada")

        if not events_details:
            st.info("Nenhuma chamada registrada ainda.")
        else:
            for i, event in enumerate(events_details, 1):
                with st.container():
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col1:
                        st.markdown(f"**{event['emoji']} {event['agent_display']}**")
                        st.caption(f"🕐 {event['timestamp']}")
                    with col2:
                        st.metric("Custo", format_currency(event['cost']))
                    with col3:
                        st.metric("Tokens", f"{event['tokens_total']:,}")
                    st.markdown("---")

            # Total
            st.markdown("### Total")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("💰 Custo Total", format_currency(accumulated['cost']))
            with col2:
                st.metric("📊 Tokens Totais", f"{accumulated['tokens']:,}")

    with tab2:
        st.markdown("### Métricas da Conversa")

        # Resumo geral
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Chamadas", accumulated['num_events'])
        with col2:
            avg_cost = accumulated['cost'] / max(accumulated['num_events'], 1)
            st.metric("Custo Médio", format_currency(avg_cost))
        with col3:
            avg_tokens = accumulated['tokens'] // max(accumulated['num_events'], 1)
            st.metric("Tokens Médio", f"{avg_tokens:,}")

        # Detalhes por agente
        if events_details:
            st.markdown("### Por Agente")

            # Agrupar por agente
            agent_stats = {}
            for event in events_details:
                agent = event['agent_display']
                if agent not in agent_stats:
                    agent_stats[agent] = {
                        "emoji": event['emoji'],
                        "calls": 0,
                        "cost": 0.0,
                        "tokens": 0,
                        "duration": 0.0
                    }
                agent_stats[agent]["calls"] += 1
                agent_stats[agent]["cost"] += event['cost']
                agent_stats[agent]["tokens"] += event['tokens_total']
                agent_stats[agent]["duration"] += event['duration']

            for agent, stats in agent_stats.items():
                st.markdown(f"**{stats['emoji']} {agent}**")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.caption(f"Chamadas: {stats['calls']}")
                with col2:
                    st.caption(f"Custo: {format_currency(stats['cost'])}")
                with col3:
                    st.caption(f"Tokens: {stats['tokens']:,}")
                with col4:
                    st.caption(f"Tempo: {stats['duration']:.1f}s")

            # Modelo usado
            if events_details:
                model = events_details[0].get("model", "desconhecido")
                st.markdown("---")
                st.caption(f"🤖 Modelo: {model}")


def _render_accumulated_cost(session_id: str) -> None:
    """
    Renderiza custo acumulado da conversa (Épico 4.3 + 4.4).

    Args:
        session_id: ID da sessão ativa

    Comportamento:
        - Exibe custo acumulado: "💰 $0.0045 total"
        - Exibe tokens totais abaixo
        - Só exibe se houver eventos (custo > 0)
        - Botão para abrir modal de detalhes (4.4)

    Critérios de Aceite (4.3 + 4.4):
        - ✅ Mostrar custo acumulado
        - ✅ Atualiza a cada mensagem
        - ✅ Clicável para ver detalhes
    """
    accumulated = _get_session_accumulated_cost(session_id)

    # Só exibe se houver custo
    if accumulated["cost"] <= 0 and accumulated["tokens"] <= 0:
        return

    st.markdown("---")

    # Layout: custo + botão de detalhes
    col1, col2 = st.columns([3, 1])
    with col1:
        st.caption(f"💰 {format_currency(accumulated['cost'])} total")
        st.caption(f"📊 {accumulated['tokens']:,} tokens")
    with col2:
        if st.button("📊", key="btn_details", help="Ver detalhes"):
            _show_context_details_modal(session_id, accumulated)


def _infer_status_from_argument(argument: Dict[str, Any]) -> str:
    """
    Infere status da ideia baseado no argumento focal (Épico 12.1 - melhorias).

    Args:
        argument: Dict do argumento (claim, premises, assumptions, open_questions, etc.)

    Returns:
        str: Status inferido ("exploring" | "structured" | "validated")

    Lógica de inferência:
        - Explorando: claim vago (<30 chars), premises vazias, open_questions > 3
        - Estruturada: claim específico, premises preenchidas, open_questions < 3
        - Validada: contradictions vazias, assumptions baixas, solid_grounds presente
    """
    claim = argument.get("claim", "")
    premises = argument.get("premises", [])
    assumptions = argument.get("assumptions", [])
    open_questions = argument.get("open_questions", [])
    contradictions = argument.get("contradictions", [])
    solid_grounds = argument.get("solid_grounds", [])

    # Critérios de validação (mais rigoroso)
    if (len(contradictions) == 0 and
        len(assumptions) <= 2 and
        len(solid_grounds) > 0):
        return "validated"

    # Critérios de estruturação (intermediário)
    if (len(claim) >= 30 and
        len(premises) >= 2 and
        len(open_questions) <= 2):
        return "structured"

    # Padrão: explorando (inicial)
    return "exploring"


def _render_idea_status(session_id: str) -> None:
    """
    Renderiza status da ideia ativa no painel Bastidores (Épico 12.1 + melhorias).

    Args:
        session_id: ID da sessão ativa

    Comportamento:
        - Exibe título da ideia ativa
        - Badge de status INFERIDO do modelo cognitivo (🔍 Explorando | 📝 Estruturada | ✅ Validada)
        - Metadados: # argumentos, argumento focal, última atualização
        - Se nenhuma ideia ativa, exibe mensagem informativa

    Integração:
        - Busca ideia ativa de st.session_state["active_idea_id"]
        - Consulta database via get_database_manager()
        - Infere status do argumento focal
    """
    # Buscar ideia ativa do session_state
    active_idea_id = st.session_state.get("active_idea_id")

    # 4.2: Estado vazio = seção em branco (não mostrar mensagem)
    if not active_idea_id:
        return

    try:
        db = get_database_manager()
        idea = db.get_idea(active_idea_id)

        if not idea:
            st.warning("⚠️ Ideia ativa não encontrada no banco de dados.")
            return

        # Exibir título da ideia (sem header, pois já está no expander)

        # Buscar argumento focal
        focal_arg_id = idea.get("current_argument_id")
        focal_arg = None
        if focal_arg_id:
            focal_arg = db.get_argument(focal_arg_id)

        # Inferir status do argumento focal (ao invés de ler estático do banco)
        if focal_arg:
            inferred_status = _infer_status_from_argument(focal_arg)
        else:
            inferred_status = "exploring"  # Sem argumento = explorando

        # Badge de status INFERIDO
        status_badges = {
            "exploring": "🔍 Explorando",
            "structured": "📝 Estruturada",
            "validated": "✅ Validada"
        }
        status_badge = status_badges.get(inferred_status, "❓ Desconhecido")

        # Título com badge
        st.markdown(f"**{idea['title']}**")
        st.caption(status_badge)

        # Indicador de Solidez (Épico 9.4)
        if focal_arg:
            from agents.models.cognitive_model import CognitiveModel

            # Reconstruir modelo cognitivo do argumento persistido
            try:
                cognitive_model = CognitiveModel(
                    claim=focal_arg.get("claim", ""),
                    premises=focal_arg.get("premises", []),
                    assumptions=focal_arg.get("assumptions", []),
                    open_questions=focal_arg.get("open_questions", []),
                    contradictions=[],  # Contradictions não persistidas diretamente
                    solid_grounds=[],   # Solid grounds não persistidos diretamente
                    context=focal_arg.get("context", {})
                )

                solidez = cognitive_model.calculate_solidez()

                # Renderizar barra de progresso
                st.progress(
                    value=solidez / 100.0,
                    text=f"🎯 Solidez: {solidez:.0f}%"
                )
            except Exception as e:
                logger.debug(f"Não foi possível calcular solidez: {e}")

        # Metadados
        arguments = db.get_arguments_by_idea(active_idea_id)
        num_arguments = len(arguments)

        # Argumento focal versão
        if focal_arg:
            focal_version = f"V{focal_arg['version']}"
        else:
            focal_version = "Nenhum"

        # Última atualização
        updated_at = idea.get("updated_at", "")
        if updated_at:
            # Converter para formato mais legível (se possível)
            try:
                dt = datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
                updated_str = dt.strftime("%d/%m/%Y %H:%M")
            except:
                updated_str = updated_at
        else:
            updated_str = "Desconhecida"

        # Exibir metadados
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Argumentos", value=num_arguments)
        with col2:
            st.metric(label="Argumento Focal", value=focal_version)

        st.caption(f"📅 Última atualização: {updated_str}")

    except Exception as e:
        logger.error(f"Erro ao renderizar status da ideia: {e}", exc_info=True)
        st.error(f"❌ Erro ao carregar status da ideia: {e}")


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
        time_str = _format_time(timestamp)

        st.markdown(f"**{emoji} {agent_display}** - {time_str}")
        st.caption(f"{summary[:150]}..." if len(summary) > 150 else summary)
        st.caption(f"⏱️ {duration:.2f}s | 💰 {format_currency(cost)}")
        st.markdown("---")


def _format_time(timestamp: str) -> str:
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


def _render_agent_timeline(session_id: str) -> None:
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
                time_str = _format_time(timestamp)

                st.markdown(f"● {emoji} {agent_short} - {time_str}")

        # Link "Ver histórico" (só mostra se há eventos)
        if completed_events:
            if st.button("Ver histórico", key="view_timeline_history", type="secondary"):
                _show_timeline_modal(completed_events)

    except Exception as e:
        logger.error(f"Erro ao renderizar timeline: {e}", exc_info=True)
        st.error("Erro ao carregar timeline")
