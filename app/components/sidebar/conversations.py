"""
Módulo de conversas do sidebar (Épico 14.1).

Responsável por:
- Listar conversas recentes
- Criar nova conversa
- Alternar entre conversas
- Renderizar lista de conversas

Versão: 1.0
Data: 19/11/2025
Status: Épico 14.1 - Navegação em Três Espaços
"""

import streamlit as st
from typing import List, Dict, Any
import logging

from app.components.session_helpers import get_current_session_id
from app.components.conversation_helpers import (
    restore_conversation_context,
    list_recent_conversations,
    get_relative_timestamp
)

logger = logging.getLogger(__name__)


def create_new_conversation() -> None:
    """
    Cria nova conversa e define como ativa (Épico 14.1).

    Comportamento:
        - Gera novo thread_id (LangGraph)
        - Limpa histórico de mensagens
        - Define como conversa ativa
        - Força re-render da interface

    Nota:
        Não cria registro em data.db (diferente de _create_new_idea).
        Conversa só existe no SqliteSaver (checkpoints.db).
        Ideia será cristalizada depois pelo sistema durante conversa.
    """
    try:
        # Gerar novo thread_id para LangGraph
        new_session_id = get_current_session_id()

        # Definir como ativa
        st.session_state.active_session_id = new_session_id

        # Limpar histórico
        if "messages" in st.session_state:
            st.session_state.messages = []

        # Limpar ideia ativa (nova conversa não está vinculada a ideia ainda)
        if "active_idea_id" in st.session_state:
            del st.session_state.active_idea_id

        logger.info(f"Nova conversa criada: thread_id={new_session_id}")
        st.success(f"✅ Nova conversa iniciada!")
        st.rerun()

    except Exception as e:
        logger.error(f"Erro ao criar nova conversa: {e}", exc_info=True)
        st.error(f"❌ Erro ao criar nova conversa: {e}")


def switch_conversation(thread_id: str) -> None:
    """
    Alterna para outra conversa (Épico 14.1 + 14.5).

    Args:
        thread_id: ID da conversa a carregar

    Comportamento:
        - Restaura histórico de mensagens do SqliteSaver (Épico 14.5)
        - Define thread_id como ativo
        - Força re-render da interface

    Nota:
        Usa restore_conversation_context() do Épico 14.5 para garantir
        que histórico de mensagens é restaurado corretamente.
    """
    try:
        logger.info(f"Alternando para conversa: {thread_id}")

        # Restaurar contexto completo (Épico 14.5)
        success = restore_conversation_context(thread_id)

        if not success:
            # Fallback: se restauração falhar, pelo menos limpar estado
            logger.warning(f"Falha ao restaurar contexto de {thread_id}. Limpando mensagens.")
            st.session_state.active_session_id = thread_id
            st.session_state.messages = []

        st.success(f"✅ Conversa restaurada!")
        st.rerun()

    except Exception as e:
        logger.error(f"Erro ao alternar conversa: {e}", exc_info=True)
        st.error(f"❌ Erro ao alternar conversa: {e}")


def render_conversation_list(conversations: List[Dict[str, Any]]) -> None:
    """
    Renderiza lista de conversas recentes na sidebar (Épico 14.1).

    Args:
        conversations: Lista de conversas do SqliteSaver

    Layout:
        Título da conversa  (ativa)
        5min atrás

        Título da conversa
        2h atrás

        ...

    Comportamento:
        - Conversa ativa marcada visualmente (bold, background)
        - Formato: "Título da conversa · Timestamp relativo"
        - Clique em conversa alterna via restore_conversation_context()
    """
    active_session_id = st.session_state.get("active_session_id")

    for conv in conversations:
        thread_id = conv["thread_id"]
        title = conv["title"]
        last_updated = conv["last_updated"]
        is_active = (thread_id == active_session_id)

        # Timestamp relativo
        relative_time = get_relative_timestamp(last_updated)

        # Botão para selecionar conversa
        button_label = f"{title}"
        button_help = f"Última atualização: {relative_time}"

        # Destacar ativa
        button_type = "primary" if is_active else "secondary"

        if st.button(
            button_label,
            key=f"conv_{thread_id}",
            use_container_width=True,
            disabled=is_active,  # Desabilitar se já está ativa
            type=button_type,
            help=button_help
        ):
            switch_conversation(thread_id)

        # Mostrar timestamp relativo abaixo do botão
        if not is_active:
            st.caption(f"  {relative_time}")

