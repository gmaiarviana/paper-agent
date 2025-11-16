"""
Componente sidebar para gerenciamento de sessões (Épico 9.10).

Responsável por:
- Listar sessões recentes (últimas 10)
- Destacar sessão ativa
- Botão "+ Nova conversa"
- Alternar entre sessões
- Integração com SqliteSaver (MVP) ou localStorage (Protótipo)

Versão: 1.0
Data: 16/11/2025
Status: Esqueleto (MVP - aguardando 9.1-9.9)
"""

import streamlit as st
from typing import List, Dict, Any, Optional
from datetime import datetime


def render_sidebar() -> str:
    """
    Renderiza sidebar com lista de sessões.

    Returns:
        str: ID da sessão ativa selecionada

    Comportamento POC (9.1-9.5):
        - Apenas sessão atual (sem lista)
        - st.session_state para gerenciar sessão ativa

    Comportamento Protótipo (9.9):
        - Lista de sessões do localStorage
        - Alternar entre sessões preserva histórico

    Comportamento MVP (9.10):
        - Lista de sessões do SqliteSaver (backend)
        - Últimas 10 sessões ordenadas por data
        - Botão "+ Nova conversa"
        - Sessão ativa destacada

    TODO (MVP - após 9.1-9.9):
        - Integrar com SqliteSaver
        - Carregar lista de sessões do banco
        - Implementar alternância entre sessões
    """
    with st.sidebar:
        st.title("📂 Sessões")

        # Botão para nova conversa
        if st.button("➕ Nova conversa", use_container_width=True, type="primary"):
            _create_new_session()

        st.markdown("---")

        # TODO: Implementar lista de sessões após 9.9/9.10
        # sessions = _get_recent_sessions(limit=10)

        # Placeholder para desenvolvimento
        st.info("🚧 Lista de sessões será implementada no MVP (9.10)")

        # Exemplo de estrutura (para referência futura)
        _render_sessions_placeholder()

    # Retornar sessão ativa
    return _get_active_session_id()


def _render_sessions_placeholder() -> None:
    """
    Placeholder visual para lista de sessões.
    Remove após implementação real (9.10).
    """
    st.caption("**Sessão atual:**")
    session_id = _get_active_session_id()
    st.write(f"🟢 Conversa atual")
    st.caption(f"ID: {session_id[:8]}...")
    st.caption(datetime.now().strftime("%d/%m/%Y %H:%M"))


def _get_active_session_id() -> str:
    """
    Retorna ID da sessão ativa.

    POC: Sessão única gerada automaticamente
    MVP: Sessão selecionada na sidebar ou nova

    Returns:
        str: ID da sessão ativa (UUID ou thread_id)
    """
    if "active_session_id" not in st.session_state:
        # Gerar novo ID de sessão
        import uuid
        st.session_state.active_session_id = str(uuid.uuid4())

    return st.session_state.active_session_id


def _create_new_session() -> None:
    """
    Cria nova sessão e define como ativa.

    Comportamento:
        - Gera novo UUID
        - Limpa histórico de mensagens
        - Define como sessão ativa
        - Limpa bastidores/timeline

    TODO (MVP - 9.10):
        - Criar registro no SqliteSaver
        - Adicionar à lista de sessões na sidebar
    """
    import uuid

    # Gerar novo ID
    new_session_id = str(uuid.uuid4())

    # Definir como ativa
    st.session_state.active_session_id = new_session_id

    # Limpar histórico
    if "messages" in st.session_state:
        st.session_state.messages = []

    st.success(f"✅ Nova conversa criada")
    st.rerun()


def _get_recent_sessions(limit: int = 10) -> List[Dict[str, Any]]:
    """
    Busca sessões recentes do storage (localStorage ou SqliteSaver).

    TODO: Implementar na fase MVP (9.10)

    Args:
        limit: Número máximo de sessões a retornar

    Returns:
        Lista de sessões ordenadas por data (mais recente primeiro)
        [
            {
                "session_id": str,
                "title": str,
                "created_at": str (ISO),
                "last_activity": str (ISO),
                "message_count": int
            }
        ]
    """
    raise NotImplementedError("Aguardando implementação MVP (9.10)")


def _load_session(session_id: str) -> None:
    """
    Carrega sessão específica como ativa.

    TODO: Implementar na fase MVP (9.10)

    Args:
        session_id: ID da sessão a carregar

    Comportamento:
        - Define session_id como ativa
        - Carrega histórico de mensagens do storage
        - Carrega timeline de agentes (se disponível)
        - Força re-render da interface
    """
    raise NotImplementedError("Aguardando implementação MVP (9.10)")


def _render_session_list(sessions: List[Dict[str, Any]]) -> None:
    """
    Renderiza lista de sessões na sidebar.

    TODO: Implementar na fase MVP (9.10)

    Args:
        sessions: Lista de sessões a exibir

    Layout esperado:
        🟢 Título da conversa · DD/MM/YYYY
        ⚪ Título da conversa · DD/MM/YYYY
        ...
    """
    raise NotImplementedError("Aguardando implementação MVP (9.10)")
