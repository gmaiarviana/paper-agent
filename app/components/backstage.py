"""
Componente "Bastidores" para visualização de reasoning dos agentes.

Responsável por:
- Seção colapsável "📊 Bastidores" (header clicável, sem toggle separado)
- Exibir agente ativo + reasoning resumido (~280 chars)
- Modal com reasoning completo (JSON estruturado)
- Timeline de agentes anteriores

Versão: 3.1
Data: 04/12/2025
Status: Épico 3.1 - Remover toggle "Ver raciocínio"
"""

import streamlit as st
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from utils.event_bus import get_event_bus
from agents.database.manager import get_database_manager

logger = logging.getLogger(__name__)

# Mapeamento de nomes de agentes para emojis
AGENT_EMOJIS = {
    "orchestrator": "🎯",
    "structurer": "📝",
    "methodologist": "🔬"
}


def render_backstage(session_id: str) -> None:
    """
    Renderiza painel "Bastidores" com reasoning dos agentes e status da ideia.

    Args:
        session_id: ID da sessão ativa

    Comportamento (Épico 3.1 + Épico 12.1):
        - Mostra status da ideia ativa (título, badge, metadados) - fora do expander
        - Seção colapsável "📊 Bastidores" (header clicável, colapsado por padrão)
        - Quando expandido: mostra agente ativo + reasoning resumido
        - Botão "Ver raciocínio completo" abre modal com JSON
        - Métricas do agente (tempo, tokens, custo)
        - Timeline colapsada de agentes anteriores

    Integração:
        - EventBus: Busca eventos via get_session_events()
        - Database: Busca ideia ativa via get_database_manager()
    """
    st.markdown("---")

    # 12.1: Mostrar status da ideia ativa (fora do expander - futuro: seção Contexto)
    _render_idea_status(session_id)

    st.markdown("---")

    # Seção colapsável "Bastidores" (Épico 3.1 - sem toggle separado)
    with st.expander("📊 Bastidores", expanded=False):
        # Buscar reasoning mais recente
        reasoning = _get_latest_reasoning(session_id)

        if reasoning is None:
            st.info("ℹ️ Nenhum evento de agente encontrado ainda. Envie uma mensagem para começar!")
        else:
            # Renderizar agente ativo
            _render_active_agent(reasoning)

            st.markdown("---")

            # Timeline de agentes anteriores (colapsado)
            _render_agent_timeline(session_id)


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

    if not active_idea_id:
        st.info("ℹ️ Nenhuma ideia ativa. Crie ou selecione uma ideia na sidebar.")
        return

    try:
        db = get_database_manager()
        idea = db.get_idea(active_idea_id)

        if not idea:
            st.warning("⚠️ Ideia ativa não encontrada no banco de dados.")
            return

        # Exibir título e status
        st.markdown("### 💡 Ideia Atual")

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
                value=f"${reasoning['cost']:.6f}"
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
                    value=f"${cost_per_1k:.4f}"
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

    # Cabeçalho com emoji e nome
    st.markdown(f"### {emoji} {agent_display}")
    st.caption("Agente mais recente")

    # Reasoning resumido
    st.markdown("**Raciocínio:**")
    st.write(reasoning["summary"])

    # Botão para ver completo (abre modal)
    if st.button("📄 Ver raciocínio completo", key="view_full_reasoning", use_container_width=True):
        _show_reasoning_modal(reasoning)

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
