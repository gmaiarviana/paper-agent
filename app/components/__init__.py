"""
Componentes Streamlit para Interface Web Conversacional (Épico 9 + 14).

Este pacote contém componentes modulares para a interface de chat:
- chat_input: Input de mensagens do usuário
- chat_history: Histórico de conversação
- backstage: Painel de reasoning dos agentes
- sidebar: Lista de sessões (SqliteSaver - MVP)
- session_helpers: Helpers para gerenciar sessões do banco
- conversation_helpers: Helpers para restauração de contexto (Épico 14.5)

Versão: 3.0
Data: 19/11/2025
Épicos: 9 (POC → Protótipo → MVP completo) + 14 (Navegação em Três Espaços)
"""

from app.components.chat_input import render_chat_input
from app.components.chat_history import render_chat_history
from app.components.backstage import render_backstage
from app.components.sidebar import render_sidebar
from app.components.conversation_helpers import (
    restore_conversation_context,
    list_recent_conversations,
    get_relative_timestamp
)

__all__ = [
    "render_chat_input",
    "render_chat_history",
    "render_backstage",
    "render_sidebar",
    "restore_conversation_context",
    "list_recent_conversations",
    "get_relative_timestamp",
]
