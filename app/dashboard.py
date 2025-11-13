"""
Dashboard Streamlit para visualização de sessões e eventos em tempo real (Épico 5.1).

Este módulo implementa interface web que exibe:
- Lista de sessões ativas
- Timeline de eventos por sessão
- Status visual dos agentes (executando, concluído, erro)
- Auto-refresh automático

Versão: 1.0
Data: 13/11/2025
"""

import sys
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# Adicionar o diretório raiz ao PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import streamlit as st
from utils.event_bus import get_event_bus


# === CONFIGURAÇÃO ===

# Intervalo de auto-refresh em segundos (default: 2s)
AUTO_REFRESH_INTERVAL = 2


# === CONFIGURAÇÃO DO STREAMLIT ===

st.set_page_config(
    page_title="Paper Agent Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# === UTILITÁRIOS ===

def format_timestamp(timestamp_str: str) -> str:
    """
    Formata timestamp ISO para exibição legível.

    Args:
        timestamp_str (str): Timestamp ISO 8601

    Returns:
        str: Timestamp formatado (HH:MM:SS)
    """
    try:
        dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        return dt.strftime("%H:%M:%S")
    except (ValueError, AttributeError):
        return timestamp_str


def get_status_icon(event_type: str) -> str:
    """
    Retorna ícone para tipo de evento.

    Args:
        event_type (str): Tipo do evento

    Returns:
        str: Ícone emoji
    """
    icons = {
        "session_started": "🚀",
        "agent_started": "▶️",
        "agent_completed": "✅",
        "agent_error": "❌",
        "session_completed": "🏁"
    }
    return icons.get(event_type, "📍")


def get_agent_color(agent_name: str) -> str:
    """
    Retorna cor para cada agente.

    Args:
        agent_name (str): Nome do agente

    Returns:
        str: Nome da cor CSS
    """
    colors = {
        "orchestrator": "#4A90E2",  # Azul
        "structurer": "#7ED321",    # Verde
        "methodologist": "#F5A623",  # Laranja
        "force_decision": "#D0021B"  # Vermelho
    }
    return colors.get(agent_name, "#9B9B9B")


# === COMPONENTES DA UI ===

def render_header():
    """Renderiza cabeçalho do dashboard."""
    st.title("📊 Paper Agent Dashboard")
    st.markdown("**Visualização em tempo real de sessões e eventos**")
    st.divider()


def render_session_selector(sessions: List[str]) -> Optional[str]:
    """
    Renderiza seletor de sessões na sidebar.

    Args:
        sessions (List[str]): Lista de session IDs

    Returns:
        Optional[str]: Session ID selecionada ou None
    """
    st.sidebar.header("📋 Sessões Ativas")

    if not sessions:
        st.sidebar.info("Nenhuma sessão ativa encontrada.")
        st.sidebar.markdown("""
        **💡 Como iniciar uma sessão:**
        1. Execute o CLI: `python cli/chat.py`
        2. Digite uma hipótese para análise
        3. A sessão aparecerá aqui automaticamente
        """)
        return None

    # Mostrar contagem
    st.sidebar.metric("Total de sessões", len(sessions))

    # Seletor de sessão
    selected_session = st.sidebar.selectbox(
        "Selecione uma sessão:",
        sessions,
        format_func=lambda s: f"Session: {s[:20]}..." if len(s) > 20 else s
    )

    return selected_session


def render_session_summary(summary: Dict[str, Any]):
    """
    Renderiza resumo da sessão selecionada.

    Args:
        summary (Dict): Resumo da sessão do EventBus
    """
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        status_emoji = "🟢" if summary["status"] == "active" else "🔵"
        st.metric("Status", f"{status_emoji} {summary['status'].upper()}")

    with col2:
        st.metric("Total de Eventos", summary["total_events"])

    with col3:
        st.metric("Início", format_timestamp(summary["started_at"]))

    with col4:
        if summary["final_status"]:
            final_icon = "✅" if summary["final_status"] == "approved" else "❌"
            st.metric("Resultado", f"{final_icon} {summary['final_status']}")
        else:
            st.metric("Resultado", "Em andamento...")

    # User input
    if summary["user_input"]:
        st.info(f"**Input:** {summary['user_input']}")


def render_timeline(events: List[Dict[str, Any]]):
    """
    Renderiza timeline de eventos.

    Args:
        events (List[Dict]): Lista de eventos da sessão
    """
    st.subheader("🕒 Timeline de Eventos")

    if not events:
        st.warning("Nenhum evento registrado ainda.")
        return

    # Renderizar cada evento
    for idx, event in enumerate(events):
        event_type = event.get("event_type", "unknown")
        timestamp = event.get("timestamp", "")
        icon = get_status_icon(event_type)

        # Container para o evento
        with st.container():
            col1, col2 = st.columns([1, 5])

            with col1:
                st.markdown(f"### {icon}")
                st.caption(format_timestamp(timestamp))

            with col2:
                # Renderizar baseado no tipo
                if event_type == "session_started":
                    st.markdown(f"**🚀 Sessão iniciada**")
                    st.caption(f"Input: {event.get('user_input', 'N/A')}")

                elif event_type == "agent_started":
                    agent_name = event.get("agent_name", "unknown")
                    color = get_agent_color(agent_name)
                    st.markdown(f"**▶️ Agente iniciado:** `{agent_name}`")
                    st.markdown(f"<div style='height:4px; background-color:{color}; border-radius:2px;'></div>", unsafe_allow_html=True)

                elif event_type == "agent_completed":
                    agent_name = event.get("agent_name", "unknown")
                    summary_text = event.get("summary", "Concluído")
                    tokens = event.get("tokens_total", 0)
                    color = get_agent_color(agent_name)

                    st.markdown(f"**✅ Agente concluído:** `{agent_name}`")
                    st.caption(f"📝 {summary_text}")
                    if tokens > 0:
                        st.caption(f"🔢 Tokens: {tokens}")
                    st.markdown(f"<div style='height:4px; background-color:{color}; border-radius:2px;'></div>", unsafe_allow_html=True)

                elif event_type == "agent_error":
                    agent_name = event.get("agent_name", "unknown")
                    error_msg = event.get("error_message", "Erro desconhecido")
                    error_type = event.get("error_type", "")

                    st.markdown(f"**❌ Erro no agente:** `{agent_name}`")
                    st.error(f"{error_type}: {error_msg}")

                elif event_type == "session_completed":
                    final_status = event.get("final_status", "unknown")
                    tokens = event.get("tokens_total", 0)
                    status_icon = "✅" if final_status == "approved" else "❌"

                    st.markdown(f"**🏁 Sessão finalizada**")
                    st.success(f"{status_icon} Status final: **{final_status}**")
                    if tokens > 0:
                        st.caption(f"🔢 Total de tokens: {tokens}")

            st.divider()


def render_event_stats(events: List[Dict[str, Any]]):
    """
    Renderiza estatísticas dos eventos.

    Args:
        events (List[Dict]): Lista de eventos
    """
    st.subheader("📈 Estatísticas")

    # Contar eventos por tipo
    event_counts = {}
    agent_counts = {}
    total_tokens = 0

    for event in events:
        event_type = event.get("event_type")
        event_counts[event_type] = event_counts.get(event_type, 0) + 1

        if event_type in ["agent_started", "agent_completed", "agent_error"]:
            agent_name = event.get("agent_name")
            agent_counts[agent_name] = agent_counts.get(agent_name, 0) + 1

        if event_type in ["agent_completed", "session_completed"]:
            total_tokens += event.get("tokens_total", 0)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Eventos por tipo:**")
        for event_type, count in event_counts.items():
            icon = get_status_icon(event_type)
            st.text(f"{icon} {event_type}: {count}")

    with col2:
        st.markdown("**Agentes executados:**")
        for agent_name, count in agent_counts.items():
            color = get_agent_color(agent_name)
            st.markdown(f"<span style='color:{color}'>●</span> {agent_name}: {count}", unsafe_allow_html=True)

    if total_tokens > 0:
        st.metric("🔢 Total de tokens", total_tokens)


# === MAIN ===

def main():
    """Função principal do dashboard."""
    # Renderizar cabeçalho
    render_header()

    # === AUTO-REFRESH CONTROL ===
    # Inicializar estado de auto-refresh
    if "auto_refresh_enabled" not in st.session_state:
        st.session_state.auto_refresh_enabled = True
    if "last_refresh_time" not in st.session_state:
        st.session_state.last_refresh_time = time.time()

    # Controles de auto-refresh na sidebar
    st.sidebar.divider()
    st.sidebar.subheader("🔄 Auto-Refresh")

    auto_refresh = st.sidebar.checkbox(
        "Ativar atualização automática",
        value=st.session_state.auto_refresh_enabled,
        help=f"Atualiza a cada {AUTO_REFRESH_INTERVAL} segundos"
    )
    st.session_state.auto_refresh_enabled = auto_refresh

    if auto_refresh:
        refresh_interval = st.sidebar.slider(
            "Intervalo (segundos)",
            min_value=1,
            max_value=10,
            value=AUTO_REFRESH_INTERVAL,
            help="Intervalo de atualização em segundos"
        )
        st.sidebar.caption(f"⏱️ Próxima atualização em {refresh_interval}s")
    else:
        refresh_interval = AUTO_REFRESH_INTERVAL

    # Obter EventBus
    event_bus = get_event_bus()

    # Listar sessões ativas
    sessions = event_bus.list_active_sessions()

    # Renderizar seletor de sessões
    selected_session = render_session_selector(sessions)

    if selected_session:
        # Obter dados da sessão
        summary = event_bus.get_session_summary(selected_session)
        events = event_bus.get_session_events(selected_session)

        # Layout principal
        col1, col2 = st.columns([2, 1])

        with col1:
            # Resumo da sessão
            render_session_summary(summary)

            # Timeline
            st.divider()
            render_timeline(events)

        with col2:
            # Estatísticas
            render_event_stats(events)

            # Botões de ação
            st.divider()
            st.subheader("⚙️ Ações")

            if st.button("🔄 Atualizar manualmente", use_container_width=True):
                st.rerun()

            if st.button("🗑️ Limpar sessão", use_container_width=True, type="secondary"):
                event_bus.clear_session(selected_session)
                st.success("Sessão limpa com sucesso!")
                st.rerun()
    else:
        # Mensagem quando não há sessões
        st.info("👈 Selecione uma sessão na barra lateral para visualizar eventos.")

    # === AUTO-REFRESH MECHANISM ===
    # Trigger auto-refresh se habilitado
    if auto_refresh:
        current_time = time.time()
        elapsed = current_time - st.session_state.last_refresh_time

        if elapsed >= refresh_interval:
            st.session_state.last_refresh_time = current_time
            time.sleep(0.1)  # Small delay para evitar CPU usage alto
            st.rerun()


if __name__ == "__main__":
    main()
