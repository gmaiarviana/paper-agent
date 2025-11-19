"""
Página: Detalhes da Ideia (Épico 14.3).

Mostra detalhes completos de uma ideia:
- Título editável
- Badge de status
- Seção Argumentos (versionados, com argumento focal destacado)
- Seção Conceitos (texto simples até Épico 13)
- Seção Conversas relacionadas
- Botões: [🔄 Continuar explorando] [📝 Editar título]

URL: /pensamentos?id={idea_id}
Layout: Página única com seções

Versão: 1.0
Data: 19/11/2025
Status: Épico 14.3 - Navegação em Três Espaços
"""

import sys
from pathlib import Path

# Adicionar o diretório raiz ao PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import streamlit as st
from datetime import datetime

from agents.database.manager import get_database_manager
from app.components.session_helpers import get_current_session_id
from app.components.conversation_helpers import get_relative_timestamp


# === CONFIGURAÇÃO ===

st.set_page_config(
    page_title="Detalhes da Ideia - Paper Agent",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="collapsed"
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


def render_arguments_section(idea: dict, arguments: list, db):
    """
    Renderiza seção de argumentos versionados.

    Args:
        idea: Dict com dados da ideia
        arguments: Lista de argumentos ordenados por versão DESC
        db: DatabaseManager
    """
    st.subheader("📊 Argumentos")

    if not arguments:
        st.caption("_Nenhum argumento definido ainda_")
        return

    focal_arg_id = idea.get("current_argument_id")

    for arg in arguments:
        arg_id = arg["id"]
        version = arg["version"]
        claim = arg["claim"]
        premises = arg["premises"]
        assumptions = arg["assumptions"]
        is_focal = (arg_id == focal_arg_id)

        # Badge focal
        focal_badge = " [FOCAL]" if is_focal else ""

        # Preview do claim
        claim_preview = claim[:100] + "..." if len(claim) > 100 else claim

        # Renderizar argumento
        with st.expander(f"**V{version}{focal_badge}**: {claim_preview}", expanded=is_focal):
            st.markdown("**Claim (Afirmação Central):**")
            st.write(claim)

            st.markdown("**Premises (Premissas):**")
            if premises:
                for i, premise in enumerate(premises, 1):
                    st.write(f"{i}. {premise}")
            else:
                st.caption("_Nenhuma premissa definida_")

            st.markdown("**Assumptions (Suposições):**")
            if assumptions:
                for i, assumption in enumerate(assumptions, 1):
                    st.write(f"⚠️ {i}. {assumption}")
            else:
                st.caption("_Nenhuma suposição identificada_")


def render_concepts_section():
    """
    Renderiza seção de conceitos (texto simples até Épico 13).
    """
    st.subheader("🏷️ Conceitos")
    st.caption("_Funcionalidade de conceitos disponível no Épico 13_")
    st.info("ℹ️ A busca semântica de conceitos será implementada no próximo épico.")


def render_conversations_section(idea: dict):
    """
    Renderiza seção de conversas relacionadas.

    Args:
        idea: Dict com dados da ideia
    """
    st.subheader("💬 Conversas relacionadas")

    thread_id = idea.get("thread_id")

    if thread_id:
        st.caption(f"Thread ID: `{thread_id}`")
        st.caption("_Esta ideia foi cristalizada durante a conversa acima_")
    else:
        st.caption("_Nenhuma conversa vinculada_")


# === APLICAÇÃO PRINCIPAL ===

def main():
    """Função principal da página de detalhes."""

    # Obter idea_id da query string
    idea_id = st.query_params.get("id")

    if not idea_id:
        st.error("❌ ID da ideia não fornecido. Volte para 'Meus Pensamentos'.")
        if st.button("← Voltar para Meus Pensamentos"):
            st.switch_page("pages/1_pensamentos.py")
        return

    # Carregar ideia do banco
    try:
        db = get_database_manager()
        idea = db.get_idea(idea_id)

        if not idea:
            st.error(f"❌ Ideia '{idea_id}' não encontrada.")
            if st.button("← Voltar para Meus Pensamentos"):
                st.switch_page("pages/1_pensamentos.py")
            return

        # === HEADER ===

        # Botão voltar
        if st.button("← Voltar para Meus Pensamentos", key="back_button"):
            st.switch_page("pages/1_pensamentos.py")

        st.markdown("---")

        # Título e status
        title = idea["title"]
        status = idea["status"]
        updated_at = idea.get("updated_at", "")

        # Badge de status
        status_badge = get_status_badge(status)

        # Timestamp relativo
        if updated_at:
            try:
                relative_time = get_relative_timestamp(updated_at)
            except:
                relative_time = "data desconhecida"
        else:
            relative_time = "data desconhecida"

        st.title(f"💡 {title}")
        st.caption(f"{status_badge} · Atualizado: {relative_time}")

        st.markdown("---")

        # === BOTÕES DE AÇÃO ===

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔄 Continuar explorando", key="continue_button", use_container_width=True, type="primary"):
                # Criar novo thread_id e redirecionar para chat
                new_thread_id = get_current_session_id()

                # Atualizar thread_id da ideia
                db.update_idea(idea_id, thread_id=new_thread_id)

                # Definir como ativa e redirecionar
                st.session_state.active_idea_id = idea_id
                st.session_state.active_session_id = new_thread_id
                st.session_state.messages = []

                st.success(f"✅ Nova conversa iniciada! Redirecionando...")
                st.switch_page("chat.py")

        with col2:
            # Editar título (inline)
            with st.form(key="edit_title_form"):
                new_title = st.text_input(
                    "📝 Editar título:",
                    value=title,
                    key="new_title_input"
                )
                submit = st.form_submit_button("Salvar título")

                if submit and new_title.strip() and new_title.strip() != title:
                    db.update_idea(idea_id, title=new_title.strip())
                    st.success(f"✅ Título atualizado!")
                    st.rerun()

        st.markdown("---")

        # === SEÇÕES ===

        # Argumentos
        arguments = db.get_arguments_by_idea(idea_id)
        render_arguments_section(idea, arguments, db)

        st.markdown("---")

        # Conceitos (texto simples até Épico 13)
        render_concepts_section()

        st.markdown("---")

        # Conversas relacionadas
        render_conversations_section(idea)

    except Exception as e:
        st.error(f"❌ Erro ao carregar detalhes da ideia: {e}")
        import traceback
        st.code(traceback.format_exc())


if __name__ == "__main__":
    main()
