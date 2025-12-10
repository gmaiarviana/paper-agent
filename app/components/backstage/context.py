"""
Componentes da seção "💡 Contexto" do painel direito.

Responsável por:
- Ideia ativa (título, status, metadados)
- Indicador de solidez
- Custo acumulado da conversa
- Modal de detalhes da conversa
"""

import streamlit as st
import logging
from typing import Dict, Any, List
from datetime import datetime

from utils.event_bus import get_event_bus
from utils.currency import format_currency, format_currency_precise
from agents.database.manager import get_database_manager
from .constants import AGENT_EMOJIS

logger = logging.getLogger(__name__)


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
        - Contém: indicador de solidez (Épico 9.4)
    """
    with st.expander("💡 Contexto", expanded=True):
        _render_idea_status(session_id)
        _render_session_solidez(session_id)  # Épico 9.4: solidez da sessão atual
        _render_accumulated_cost(session_id)


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
                "model": event.get("model", "claude-3-5-haiku-20241022")
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
        argument: Dict do argumento (claim, proposicoes, open_questions, etc.)

    Returns:
        str: Status inferido ("exploring" | "structured" | "validated")

    Lógica de inferência (usando proposições):
        - Explorando: claim vago (<30 chars), proposições insuficientes, open_questions > 3
        - Estruturada: claim específico, proposições sólidas preenchidas, open_questions < 3
        - Validada: contradictions vazias, proposições frágeis baixas, solid_grounds presente
    """
    claim = argument.get("claim", "")
    proposicoes = argument.get("proposicoes", [])
    open_questions = argument.get("open_questions", [])
    contradictions = argument.get("contradictions", [])
    solid_grounds = argument.get("solid_grounds", [])

    # Calcular proposições sólidas e frágeis
    solid_props = [p for p in proposicoes if isinstance(p, dict) and p.get("solidez") is not None and p.get("solidez", 0) >= 0.6]
    fragile_props = [p for p in proposicoes if isinstance(p, dict) and p.get("solidez") is not None and p.get("solidez", 0) < 0.6]

    # Critérios de validação (mais rigoroso)
    if (len(contradictions) == 0 and
        len(fragile_props) <= 2 and
        len(solid_grounds) > 0):
        return "validated"

    # Critérios de estruturação (intermediário)
    if (len(claim) >= 30 and
        len(solid_props) >= 2 and
        len(open_questions) <= 2):
        return "structured"

    # Padrão: explorando (inicial)
    return "exploring"


def _render_session_solidez(session_id: str) -> None:
    """
    Renderiza indicador de solidez da sessão atual (Épico 9.4).

    Mostra a solidez do cognitive_model da última resposta do orchestrator,
    mesmo quando não há ideia persistida. Isso permite feedback visual
    durante toda a conversa.

    Args:
        session_id: ID da sessão ativa

    Comportamento:
        - Se há active_idea_id com focal_arg: solidez já é mostrada em _render_idea_status
        - Se não há: mostra solidez do cognitive_model da sessão (st.session_state)
        - Barra de progresso 0-100%
    """
    # Se já tem ideia ativa com argumento, a solidez é mostrada em _render_idea_status
    active_idea_id = st.session_state.get("active_idea_id")
    if active_idea_id:
        try:
            db = get_database_manager()
            idea = db.get_idea(active_idea_id)
            if idea and idea.get("current_argument_id"):
                # Já tem argumento focal - solidez mostrada em _render_idea_status
                return
        except Exception:
            pass

    # Buscar cognitive_model da sessão atual
    cognitive_model_dict = st.session_state.get("cognitive_model")

    if not cognitive_model_dict:
        # Sem cognitive_model ainda - nada a mostrar
        return

    try:
        from agents.models.cognitive_model import CognitiveModel
        from agents.models.proposition import Proposicao

        # Reconstruir proposições da sessão
        proposicoes_raw = cognitive_model_dict.get("proposicoes", [])
        proposicoes = []
        for p in proposicoes_raw:
            if isinstance(p, dict):
                proposicoes.append(Proposicao(**p))
            elif isinstance(p, str):
                proposicoes.append(Proposicao.from_text(p))

        # Reconstruir modelo cognitivo da sessão
        cognitive_model = CognitiveModel(
            claim=cognitive_model_dict.get("claim", ""),
            proposicoes=proposicoes,
            open_questions=cognitive_model_dict.get("open_questions", []),
            contradictions=[],  # Não persistido
            solid_grounds=[],   # Não persistido
            context=cognitive_model_dict.get("context", {})
        )

        solidez = cognitive_model.calculate_solidez()

        # Renderizar barra de progresso
        st.progress(
            value=solidez / 100.0,
            text=f"🎯 Solidez: {solidez:.0f}%"
        )
    except Exception as e:
        logger.debug(f"Não foi possível calcular solidez da sessão: {e}")


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
            from agents.models.proposition import Proposicao

            # Reconstruir modelo cognitivo do argumento persistido
            try:
                # Reconstruir proposições
                proposicoes_raw = focal_arg.get("proposicoes", [])
                proposicoes = []
                for p in proposicoes_raw:
                    if isinstance(p, dict):
                        proposicoes.append(Proposicao(**p))
                    elif isinstance(p, str):
                        proposicoes.append(Proposicao.from_text(p))

                cognitive_model = CognitiveModel(
                    claim=focal_arg.get("claim", ""),
                    proposicoes=proposicoes,
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

