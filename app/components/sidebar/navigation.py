"""
Módulo de navegação do sidebar (Épico 14.1).

Responsável por:
- Renderizar sidebar completo
- Botões de navegação para páginas dedicadas
- Coordenar renderização de conversas e ideias

Versão: 1.0
Data: 19/11/2025
Status: Épico 14.1 - Navegação em Três Espaços
"""

import streamlit as st
from typing import List, Dict, Any
import logging

from app.components.session_helpers import get_current_session_id
from app.components.conversation_helpers import list_recent_conversations
from app.components.sidebar.conversations import (
    create_new_conversation,
    render_conversation_list
)
from app.components.sidebar.ideas import (
    get_recent_ideas,
    render_idea_list
)

logger = logging.getLogger(__name__)


def get_active_session_id() -> str:
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


def render_sidebar() -> str:
    """
    Renderiza sidebar com lista de conversas recentes (Épico 14.1).

    Returns:
        str: ID da sessão ativa (thread_id do LangGraph)

    Comportamento (Épico 14.1):
        - Lista de conversas do SqliteSaver (checkpoints.db)
        - Últimas 5 conversas ordenadas por timestamp DESC
        - Botão "+ Nova Conversa"
        - Conversa ativa destacada (bold, background diferente)
        - Formato: "Título da conversa · Timestamp relativo" ("5min atrás", "2h atrás")
        - Botão [📖 Meus Pensamentos] → redireciona para /pensamentos
        - Botão [🏷️ Catálogo] → desabilitado até Épico 13
        - Alternância entre conversas restaura contexto completo (Épico 14.5)
    """
    with st.sidebar:
        st.title("💬 Conversas")

        # Botão para nova conversa (14.1)
        if st.button("➕ Nova Conversa", use_container_width=True, type="primary"):
            create_new_conversation()

        st.markdown("---")

        # Buscar conversas recentes do SqliteSaver (14.1)
        conversations = list_recent_conversations(limit=5)

        if conversations and len(conversations) > 0:
            st.caption("**Conversas recentes:**")
            render_conversation_list(conversations)
        else:
            # Nenhuma conversa no banco ainda
            st.caption("Nenhuma conversa encontrada.")
            st.caption("Clique em '➕ Nova Conversa' para começar!")

        st.markdown("---")

        # Botões de navegação para páginas dedicadas (14.1)
        st.subheader("📖 Navegação")

        # Botão: Meus Pensamentos
        if st.button("📖 Meus Pensamentos", use_container_width=True):
            # Redirecionar para página /pensamentos
            # Nota: Streamlit não tem redirect nativo; usar query_params ou link
            st.switch_page("pages/1_pensamentos.py")

        # Botão: Catálogo (desabilitado até Épico 13)
        st.button(
            "🏷️ Catálogo",
            use_container_width=True,
            disabled=True,
            help="Disponível no Épico 13"
        )

    # Retornar sessão ativa (thread_id para compatibilidade)
    return get_active_session_id()

