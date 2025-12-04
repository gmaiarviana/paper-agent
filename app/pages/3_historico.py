"""
Página: Histórico de Conversas (Épico 2.1).

Mostra lista de conversas passadas com preview:
- Título da conversa
- Timestamp relativo
- Clique para retomar conversa

URL: /historico
Layout: Lista simples

Versão: 1.0
Data: 04/12/2025
Status: Épico 2.1 - Sidebar com Links de Navegação
"""

import sys
from pathlib import Path

# Adicionar o diretório raiz ao PYTHONPATH
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import streamlit as st
from typing import List, Dict, Any

from app.components.conversation_helpers import (
    list_recent_conversations,
    get_relative_timestamp,
    restore_conversation_context
)
from app.components.sidebar import render_sidebar


# === CONFIGURAÇÃO ===

st.set_page_config(
    page_title="Conversas - Paper Agent",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)


# === FUNÇÕES AUXILIARES ===

def switch_to_conversation(thread_id: str) -> None:
    """
    Alterna para uma conversa e redireciona para o chat.

    Args:
        thread_id: ID da conversa a carregar
    """
    success = restore_conversation_context(thread_id)
    if success:
        st.switch_page("chat.py")
    else:
        st.error("❌ Erro ao carregar conversa")


def render_conversation_card(conv: Dict[str, Any]) -> None:
    """
    Renderiza um card de conversa.

    Args:
        conv: Dict com dados da conversa
    """
    thread_id = conv["thread_id"]
    title = conv["title"]
    last_updated = conv["last_updated"]

    # Timestamp relativo
    relative_time = get_relative_timestamp(last_updated)

    # Renderizar card
    with st.container():
        col_content, col_action = st.columns([4, 1])

        with col_content:
            st.markdown(f"### 💬 {title}")
            st.caption(f"📅 {relative_time}")

        with col_action:
            if st.button("Retomar →", key=f"conv_{thread_id}", use_container_width=True):
                switch_to_conversation(thread_id)

        st.markdown("---")


# === APLICAÇÃO PRINCIPAL ===

def main():
    """Função principal da página Histórico de Conversas."""

    # Sidebar com navegação
    render_sidebar()

    # Título
    st.title("💬 Conversas")
    st.caption("Histórico de conversas passadas")

    # Buscar conversas recentes
    try:
        # Buscar mais conversas para o histórico completo
        conversations = list_recent_conversations(limit=20)

        # Exibir contagem
        st.caption(f"**{len(conversations)} conversa(s) encontrada(s)**")

        if not conversations:
            st.info("ℹ️ Nenhuma conversa encontrada. Inicie uma nova conversa!")

            if st.button("➕ Nova Conversa", type="primary"):
                st.switch_page("chat.py")
            return

        # Lista de cards
        for conv in conversations:
            render_conversation_card(conv)

    except Exception as e:
        st.error(f"❌ Erro ao carregar conversas: {e}")
        import traceback
        st.code(traceback.format_exc())


if __name__ == "__main__":
    main()
