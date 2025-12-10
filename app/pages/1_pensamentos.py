"""
Página: Meus Pensamentos - Grid de Ideias Cristalizadas (Épico 14.2).

Mostra grid de cards com ideias cristalizadas durante conversas:
- Preview: título, status, # argumentos, # conceitos
- Busca por título
- Filtros por status
- Cards clicáveis → redireciona para /pensamentos/{idea_id}

URL: /pensamentos
Layout: Grid 2 colunas (responsivo)

Status: Épico 14.2 - Navegação em Três Espaços
"""

import sys
from pathlib import Path

# Adicionar o diretório raiz ao PYTHONPATH
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import streamlit as st
from datetime import datetime

from agents.database.manager import get_database_manager
from app.components.conversation_helpers import get_relative_timestamp
from app.components.sidebar import render_sidebar

# === CONFIGURAÇÃO ===

st.set_page_config(
    page_title="Meus Pensamentos - Paper Agent",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# === FUNÇÕES AUXILIARES ===

def get_status_badge(status: str) -> str:
    """Retorna badge visual para status da ideia."""
    badges = {
        "exploring": "🔍 Explorando",
        "structured": "📝 Estruturada",
        "validated": "✅ Validada"
    }
    return badges.get(status, "❓ Desconhecido")

def render_idea_card(idea: dict, db):
    """
    Renderiza um card de ideia.

    Args:
        idea: Dict com dados da ideia
        db: DatabaseManager para buscar argumentos
    """
    title = idea["title"]
    status = idea["status"]
    idea_id = idea["id"]
    updated_at = idea.get("updated_at", "")

    # Badge de status
    status_badge = get_status_badge(status)

    # Contar argumentos
    arguments = db.get_arguments_by_idea(idea_id)
    num_arguments = len(arguments)

    # Conceitos (fixo 0 até Épico 13)
    num_concepts = 0

    # Timestamp relativo
    if updated_at:
        try:
            relative_time = get_relative_timestamp(updated_at)
        except:
            relative_time = "data desconhecida"
    else:
        relative_time = "data desconhecida"

    # Renderizar card
    with st.container():
        st.markdown(
            f"""
            <div style="
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 1.5rem;
                margin-bottom: 1rem;
                background-color: #fafafa;
                cursor: pointer;
                transition: box-shadow 0.2s;
            "
            onmouseover="this.style.boxShadow='0 4px 8px rgba(0,0,0,0.1)'"
            onmouseout="this.style.boxShadow='none'">
                <h3 style="margin: 0 0 0.5rem 0;">💡 {title}</h3>
                <p style="margin: 0.25rem 0; color: #666;">
                    {status_badge} · {num_arguments} argumento(s) · {num_concepts} conceito(s)
                </p>
                <p style="margin: 0.5rem 0 0 0; font-size: 0.85rem; color: #999;">
                    📅 {relative_time}
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Botão para ver detalhes (redireciona para página dedicada)
        if st.button(f"Ver detalhes →", key=f"btn_{idea_id}", use_container_width=True):
            # Passar idea_id via query params ANTES do switch_page
            st.query_params["id"] = idea_id
            # Redirecionar para página de detalhes
            st.switch_page("pages/_ideia_detalhes.py")

# === APLICAÇÃO PRINCIPAL ===

def main():
    """Função principal da página Meus Pensamentos."""

    # Sidebar com navegação
    render_sidebar()

    # Título
    st.title("📖 Meus Pensamentos")
    st.caption("Ideias cristalizadas durante suas conversas")

    # Busca e filtros (Épico 14.2)
    col_search, col_filter = st.columns([3, 1])

    with col_search:
        search_query = st.text_input(
            "🔍 Buscar ideias...",
            key="search_ideas",
            placeholder="Digite palavras-chave..."
        )

    with col_filter:
        status_filter = st.selectbox(
            "Filtrar por status",
            ["Todas", "Explorando", "Estruturada", "Validada"],
            key="filter_status"
        )

    st.markdown("---")

    # Buscar ideias do banco
    try:
        db = get_database_manager()

        # Mapear filtro de status
        status_map = {
            "Explorando": "exploring",
            "Estruturada": "structured",
            "Validada": "validated"
        }
        status = status_map.get(status_filter)  # None se "Todas"

        # Buscar ideias
        ideas = db.list_ideas(status=status, limit=50)

        # Filtrar por busca (case-insensitive)
        if search_query:
            search_lower = search_query.lower()
            ideas = [
                idea for idea in ideas
                if search_lower in idea["title"].lower()
            ]

        # Exibir contagem
        st.caption(f"**{len(ideas)} ideia(s) encontrada(s)**")

        if not ideas:
            st.info("ℹ️ Nenhuma ideia encontrada. Continue conversando para cristalizar ideias!")
            return

        # Grid de cards (2 colunas)
        col1, col2 = st.columns(2)

        for idx, idea in enumerate(ideas):
            with col1 if idx % 2 == 0 else col2:
                render_idea_card(idea, db)

    except Exception as e:
        st.error(f"❌ Erro ao carregar ideias: {e}")
        import traceback
        st.code(traceback.format_exc())

if __name__ == "__main__":
    main()
