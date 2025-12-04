"""
Componentes Streamlit para Interface Web Conversacional (Épico 4 + 9 + 14).

Este pacote contém componentes modulares para a interface de chat:
- chat_input: Input de mensagens do usuário
- chat_history: Histórico de conversação
- backstage: Painel direito (Contexto + Bastidores)
- sidebar: Lista de sessões (SqliteSaver - MVP)
- session_helpers: Helpers para gerenciar sessões do banco
- conversation_helpers: Helpers para restauração de contexto (Épico 14.5)

Versão: 4.0
Data: 04/12/2025
Épicos: 4 (Contexto) + 9 (POC → MVP) + 14 (Navegação em Três Espaços)
"""

from app.components.chat_input import render_chat_input
from app.components.chat_history import render_chat_history
from app.components.backstage import (
    render_right_panel,
    render_context_section,
    render_backstage,
)
from app.components.sidebar import render_sidebar
from app.components.conversation_helpers import (
    restore_conversation_context,
    list_recent_conversations,
    get_relative_timestamp
)

__all__ = [
    "render_chat_input",
    "render_chat_history",
    "render_right_panel",
    "render_context_section",
    "render_backstage",
    "render_sidebar",
    "restore_conversation_context",
    "list_recent_conversations",
    "get_relative_timestamp",
]
