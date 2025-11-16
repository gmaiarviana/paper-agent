"""
Componente sidebar para gerenciamento de sessões (Épico 9.10-9.11 MVP).

Responsável por:
- Listar sessões recentes (últimas 10)
- Destacar sessão ativa
- Botão "+ Nova conversa"
- Alternar entre sessões
- Integração com SqliteSaver (persistência em banco)

Versão: 2.0
Data: 16/11/2025
Status: MVP completo (SqliteSaver integrado)
"""

import streamlit as st
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

from app.components.session_helpers import (
    list_sessions,
    get_current_session_id,
    session_exists
)

logger = logging.getLogger(__name__)


def render_sidebar() -> str:
    """
    Renderiza sidebar com lista de sessões (MVP completo - Épico 9.10-9.11).

    Returns:
        str: ID da sessão ativa selecionada

    Comportamento MVP:
        - Lista de sessões do SqliteSaver (backend)
        - Últimas 10 sessões ordenadas por data
        - Botão "+ Nova conversa"
        - Sessão ativa destacada
        - Alternância entre sessões preserva histórico completo (do banco)
    """
    with st.sidebar:
        st.title("📂 Sessões")

        # Botão para nova conversa
        if st.button("➕ Nova conversa", use_container_width=True, type="primary"):
            _create_new_session()

        st.markdown("---")

        # Buscar sessões do banco
        sessions = _get_recent_sessions(limit=10)

        if sessions and len(sessions) > 0:
            # Renderizar lista de sessões
            _render_session_list(sessions)
        else:
            # Nenhuma sessão no banco ainda
            st.caption("Nenhuma sessão encontrada.")
            st.caption("Clique em '➕ Nova conversa' para começar!")

    # Retornar sessão ativa
    return _get_active_session_id()


def _get_active_session_id() -> str:
    """
    Retorna ID da sessão ativa (MVP - Épico 9.10-9.11).

    Returns:
        str: ID da sessão ativa (formato: session-YYYYMMDD-HHMMSS-{millis})

    Comportamento:
        - Se já existe sessão ativa em st.session_state, retorna
        - Senão, gera nova sessão com get_current_session_id()
    """
    if "active_session_id" not in st.session_state:
        # Gerar novo ID de sessão (formato legível com timestamp)
        st.session_state.active_session_id = get_current_session_id()
        logger.debug(f"Nova sessão ativa criada: {st.session_state.active_session_id}")

    return st.session_state.active_session_id


def _create_new_session() -> None:
    """
    Cria nova sessão e define como ativa (MVP completo).

    Comportamento:
        - Gera novo ID com timestamp
        - Limpa histórico de mensagens
        - Define como sessão ativa
        - SqliteSaver criará checkpoint automaticamente na próxima interação
    """
    # Gerar novo ID
    new_session_id = get_current_session_id()

    # Definir como ativa
    st.session_state.active_session_id = new_session_id

    # Limpar histórico
    if "messages" in st.session_state:
        st.session_state.messages = []

    logger.info(f"Nova conversa criada: {new_session_id}")
    st.success(f"✅ Nova conversa criada")
    st.rerun()


def _get_recent_sessions(limit: int = 10) -> List[Dict[str, Any]]:
    """
    Busca sessões recentes do SqliteSaver (MVP completo - Épico 9.10-9.11).

    Args:
        limit: Número máximo de sessões a retornar

    Returns:
        Lista de sessões ordenadas por data (mais recente primeiro)
        [
            {
                "thread_id": str,
                "title": str,
                "last_activity": str (ISO)
            }
        ]
    """
    try:
        sessions = list_sessions(limit=limit)
        logger.debug(f"Sessões carregadas do banco: {len(sessions)}")
        return sessions
    except Exception as e:
        logger.error(f"Erro ao carregar sessões: {e}", exc_info=True)
        return []


def _load_session(session_id: str) -> None:
    """
    Carrega sessão específica como ativa (MVP completo - Épico 9.10-9.11).

    Args:
        session_id: ID da sessão a carregar (thread_id do SqliteSaver)

    Comportamento:
        - Define session_id como ativa
        - Limpa histórico de mensagens atual
        - SqliteSaver carregará checkpoint automaticamente na próxima renderização
        - Força re-render da interface
    """
    # Definir como ativa
    st.session_state.active_session_id = session_id

    # Limpar histórico (será recarregado do SqliteSaver)
    if "messages" in st.session_state:
        st.session_state.messages = []

    logger.info(f"Sessão carregada: {session_id}")
    st.rerun()


def _render_session_list(sessions: List[Dict[str, Any]]) -> None:
    """
    Renderiza lista de sessões na sidebar (MVP completo - Épico 9.10-9.11).

    Args:
        sessions: Lista de sessões do SqliteSaver

    Layout:
        🟢 Título da conversa
        ⚪ Título da conversa
        ...

    Comportamento:
        - Sessão ativa marcada com 🟢
        - Outras sessões com ⚪
        - Clique em sessão carrega via _load_session()
    """
    active_session_id = _get_active_session_id()

    st.caption("**Sessões recentes:**")

    for session in sessions:
        thread_id = session["thread_id"]
        title = session["title"]
        is_active = (thread_id == active_session_id)

        # Ícone baseado em sessão ativa
        icon = "🟢" if is_active else "⚪"

        # Botão para selecionar sessão
        button_label = f"{icon} {title}"

        # Usar container para cada sessão
        if st.button(
            button_label,
            key=f"session_{thread_id}",
            use_container_width=True,
            disabled=is_active  # Desabilitar se já está ativa
        ):
            _load_session(thread_id)
