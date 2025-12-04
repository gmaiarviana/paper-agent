"""
Módulo de navegação do sidebar (Épico 2.1).

Responsável por:
- Renderizar sidebar minimalista com links de navegação
- Botão de nova conversa
- Links para páginas dedicadas

Versão: 2.0
Data: 04/12/2025
Status: Épico 2.1 - Sidebar com Links de Navegação
"""

import streamlit as st
import logging

from app.components.session_helpers import get_current_session_id

logger = logging.getLogger(__name__)


def get_active_session_id() -> str:
    """
    Retorna ID da sessão ativa.

    Returns:
        str: ID da sessão ativa (formato: session-YYYYMMDD-HHMMSS-{millis})

    Comportamento:
        - Se já existe sessão ativa em st.session_state, retorna
        - Senão, gera nova sessão com get_current_session_id()
    """
    if "active_session_id" not in st.session_state:
        st.session_state.active_session_id = get_current_session_id()
        logger.debug(f"Nova sessão ativa criada: {st.session_state.active_session_id}")

    return st.session_state.active_session_id


def create_new_conversation() -> None:
    """
    Cria nova conversa e define como ativa.

    Comportamento:
        - Gera novo thread_id (LangGraph)
        - Limpa histórico de mensagens
        - Define como conversa ativa
        - Força re-render da interface
    """
    try:
        new_session_id = get_current_session_id()
        st.session_state.active_session_id = new_session_id

        if "messages" in st.session_state:
            st.session_state.messages = []

        if "active_idea_id" in st.session_state:
            del st.session_state.active_idea_id

        logger.info(f"Nova conversa criada: thread_id={new_session_id}")
        st.rerun()

    except Exception as e:
        logger.error(f"Erro ao criar nova conversa: {e}", exc_info=True)
        st.error(f"❌ Erro ao criar nova conversa: {e}")


def render_sidebar() -> str:
    """
    Renderiza sidebar minimalista com links de navegação (Épico 2.1).

    Returns:
        str: ID da sessão ativa (thread_id do LangGraph)

    Layout:
        ┌─────────────────────────┐
        │ [+ Nova conversa]       │
        │                         │
        │ 📖 Pensamentos          │
        │ 🏷️ Catálogo            │
        │ 💬 Conversas            │
        └─────────────────────────┘

    Critérios de Aceite (2.1):
        - Link "📖 Pensamentos" → /pensamentos
        - Link "🏷️ Catálogo" → /catalogo (desabilitado)
        - Link "💬 Conversas" → /historico
        - Botão "+ Nova conversa" → inicia chat novo
        - Links com ícones, sem header/logo
    """
    with st.sidebar:
        # Botão para nova conversa (destaque primário)
        if st.button("➕ Nova conversa", use_container_width=True, type="primary"):
            create_new_conversation()

        st.markdown("---")

        # Links de navegação
        if st.button("📖 Pensamentos", use_container_width=True):
            st.switch_page("pages/1_pensamentos.py")

        st.button(
            "🏷️ Catálogo",
            use_container_width=True,
            disabled=True,
            help="Disponível em breve"
        )

        if st.button("💬 Conversas", use_container_width=True):
            st.switch_page("pages/3_historico.py")

    return get_active_session_id()
