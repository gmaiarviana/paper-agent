"""
Componentes Streamlit para Interface Web Conversacional (Épico 9).

Este pacote contém componentes modulares para a interface de chat:
- chat_input: Input de mensagens do usuário
- chat_history: Histórico de conversação
- backstage: Painel de reasoning dos agentes
- sidebar: Lista de sessões (SqliteSaver - MVP)
- session_helpers: Helpers para gerenciar sessões do banco

Versão: 2.0
Data: 16/11/2025
Épico: 9 (POC → Protótipo → MVP completo)
"""

from app.components.chat_input import render_chat_input
from app.components.chat_history import render_chat_history
from app.components.backstage import render_backstage
from app.components.sidebar import render_sidebar

__all__ = [
    "render_chat_input",
    "render_chat_history",
    "render_backstage",
    "render_sidebar",
]
