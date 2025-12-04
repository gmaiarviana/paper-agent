"""
Interface Web Conversacional - Paper Agent (Épico 9 - POC Completa).

Interface principal do sistema:
- Chat conversacional com histórico
- Bastidores com reasoning dos agentes (seção colapsável)
- Sidebar com lista de sessões
- Backend compartilhado com CLI (LangGraph + EventBus)

Layout (Desktop):
┌─────────────────────────────────────────────────────────────┐
│  [Sidebar - 20%]    [Chat - 50%]      [Bastidores - 30%]   │
│                                                             │
│  📂 Sessões          💬 Chat           📊 Bastidores        │
│  • Nova conversa     Histórico         [Colapsável]        │
│                      Input                                  │
└─────────────────────────────────────────────────────────────┘

Progressão:
- ✅ POC (9.1-9.5): Chat básico + polling + métricas + backend integrado
- ✅ Protótipo (9.6-9.9): localStorage (removido no MVP)
- ✅ MVP (9.10-9.11): Sidebar + SqliteSaver + persistência em banco
- ✅ Épico 3: Bastidores reorganizados (seção colapsável, cards, histórico)

Versão: 3.1
Data: 04/12/2025
Status: MVP + Épico 3 (Bastidores)
"""

import sys
from pathlib import Path

# Adicionar o diretório raiz ao PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import streamlit as st
from app.components import (
    render_chat_input,
    render_chat_history,
    render_backstage,
    render_sidebar,
)


# === CONFIGURAÇÃO ===

st.set_page_config(
    page_title="Paper Agent - Chat",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)


# === ESTILOS CUSTOMIZADOS ===

def apply_custom_styles():
    """
    Aplica CSS customizado para melhorar layout e UX.

    Ajustes:
    - Reduzir padding/margin padrão do Streamlit
    - Estilizar métricas inline
    - Ajustar cores e bordas
    """
    st.markdown("""
        <style>
        /* Reduzir padding do container principal */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 0rem;
        }

        /* Estilizar métricas inline discretas */
        .stCaption {
            font-size: 0.8rem;
            color: #666;
        }

        /* Destacar mensagem do usuário */
        div[data-testid="stChatMessage"][data-role="user"] {
            background-color: #f0f2f6;
        }

        /* Botões mais compactos */
        .stButton button {
            padding: 0.4rem 1rem;
        }
        </style>
    """, unsafe_allow_html=True)


# === APLICAÇÃO PRINCIPAL ===

def main():
    """
    Função principal da interface web conversacional.

    Fluxo:
    1. Renderizar sidebar (retorna session_id ativo)
    2. Layout de 2 colunas: Chat (60%) + Bastidores (40%)
    3. Chat: histórico + input
    4. Bastidores: reasoning collapsible

    TODO (após Épico 8.2/8.3):
        - Integrar com LangGraph para processamento
        - Consumir eventos do EventBus via polling (1s)
        - Exibir métricas reais (tokens, custo, tempo)
    """
    apply_custom_styles()

    # Título
    st.title("💬 Paper Agent - Chat Conversacional")
    st.caption("Interface web para desenvolvimento de artigos científicos com IA")

    # Sidebar (retorna sessão ativa)
    session_id = render_sidebar()

    # Layout principal: Chat + Bastidores
    # POC: 2 colunas (chat + bastidores)
    # Ajustar proporções conforme necessário
    col_chat, col_backstage = st.columns([0.6, 0.4])

    with col_chat:
        st.markdown("### 💬 Conversa")
        render_chat_history(session_id)
        render_chat_input(session_id)

    with col_backstage:
        render_backstage(session_id)

    # Footer
    st.markdown("---")
    st.caption(
        "✅ **MVP COMPLETO (Épico 9.1-9.11)** | "
        f"Sessão: `{session_id[:20]}...` | "
        "Chat + SqliteSaver + Sidebar integrados"
    )


if __name__ == "__main__":
    main()
