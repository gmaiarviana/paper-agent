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

Status: Épico 14.3 - Navegação em Três Espaços
"""

import sys
from pathlib import Path

# Adicionar o diretório raiz ao PYTHONPATH
# Caminho: products/revelar/app/pages/*.py -> parent.parent.parent.parent.parent = project root
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

import streamlit as st
import logging
from datetime import datetime

from core.agents.database.manager import get_database_manager
from products.revelar.app.components.session_helpers import get_current_session_id
from products.revelar.app.components.conversation_helpers import get_relative_timestamp
from products.revelar.app.components.sidebar import render_sidebar

logger = logging.getLogger(__name__)

# === CONFIGURAÇÃO ===

st.set_page_config(
    page_title="Detalhes da Ideia - Paper Agent",
    page_icon="💡",
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
        proposicoes = arg.get("proposicoes", [])
        is_focal = (arg_id == focal_arg_id)

        # Badge focal
        focal_badge = " [FOCAL]" if is_focal else ""

        # Preview do claim
        claim_preview = claim[:100] + "..." if len(claim) > 100 else claim

        # Renderizar argumento
        with st.expander(f"**V{version}{focal_badge}**: {claim_preview}", expanded=is_focal):
            st.markdown("**Claim (Afirmação Central):**")
            st.write(claim)

            st.markdown("**Proposições:**")
            if proposicoes:
                # Separar por solidez
                solid = [p for p in proposicoes if isinstance(p, dict) and p.get("solidez") is not None and p.get("solidez", 0) >= 0.6]
                fragile = [p for p in proposicoes if isinstance(p, dict) and p.get("solidez") is not None and p.get("solidez", 0) < 0.6]
                not_evaluated = [p for p in proposicoes if isinstance(p, dict) and p.get("solidez") is None]

                if solid:
                    st.markdown("**🟢 Sólidas (solidez ≥ 0.6):**")
                    for p in solid:
                        texto = p.get("texto", str(p))
                        solidez_val = p.get("solidez", 0)
                        st.write(f"• [{solidez_val:.2f}] {texto}")

                if fragile:
                    st.markdown("**🟡 Frágeis (solidez < 0.6):**")
                    for p in fragile:
                        texto = p.get("texto", str(p))
                        solidez_val = p.get("solidez", 0)
                        st.write(f"• [{solidez_val:.2f}] {texto}")

                if not_evaluated:
                    st.markdown("**⚪ Não avaliadas:**")
                    for p in not_evaluated:
                        texto = p.get("texto", str(p))
                        st.write(f"• {texto}")
            else:
                st.caption("_Nenhuma proposição definida_")

def render_concepts_section():
    """
    Renderiza seção de conceitos (texto simples até Épico 13).
    """
    st.subheader("🏷️ Conceitos")
    st.caption("_Funcionalidade de conceitos disponível no Épico 13_")
    st.info("ℹ️ A busca semântica de conceitos será implementada no próximo épico.")

def format_thread_timestamp(thread_id: str) -> str:
    """
    Formata timestamp do thread_id para formato legível ("18/11, 14:56").
    
    Args:
        thread_id: ID da conversa (formato: session-YYYYMMDD-HHMMSS-{millis})
    
    Returns:
        str: Timestamp formatado ("DD/MM, HH:MM") ou fallback
    """
    try:
        # Extrair timestamp do thread_id (formato: session-YYYYMMDD-HHMMSS-...)
        parts = thread_id.split("-")
        if len(parts) >= 3:
            date_part = parts[1]  # YYYYMMDD
            time_part = parts[2]  # HHMMSS
            
            day = date_part[6:8]
            month = date_part[4:6]
            hour = time_part[0:2]
            minute = time_part[2:4]
            
            return f"{day}/{month}, {hour}:{minute}"
    except Exception as e:
        logger.warning(f"Erro ao formatar timestamp de {thread_id}: {e}")
    
    return "data desconhecida"

def get_thread_timestamp_from_checkpoint(thread_id: str) -> str:
    """
    Busca timestamp do último checkpoint da conversa no SqliteSaver.
    
    Args:
        thread_id: ID da conversa
    
    Returns:
        str: Timestamp ISO ou None se não encontrado
    """
    try:
        import sqlite3
        from pathlib import Path
        
        # Caminho do banco SqliteSaver (mesmo usado no LangGraph)
        # Caminho: products/revelar/app/pages/ -> parent.parent.parent.parent.parent = project root
        project_root = Path(__file__).parent.parent.parent.parent.parent
        db_path = project_root / "data" / "checkpoints.db"
        
        if not db_path.exists():
            return None
        
        # Conectar ao banco (usar context manager para garantir fechamento)
        with sqlite3.connect(str(db_path)) as conn:
            cursor = conn.cursor()
            
            # Buscar último checkpoint desta conversa
            query = """
            SELECT MAX(checkpoint_ns) as last_checkpoint_ns
            FROM checkpoints
            WHERE thread_id = ?
            """
            
            cursor.execute(query, (thread_id,))
            row = cursor.fetchone()
        
        if row and row[0]:
            # Converter checkpoint_ns (nanoseconds) para datetime
            checkpoint_ns = row[0]
            try:
                # Converter para int se necessário (SQLite pode retornar como string)
                if isinstance(checkpoint_ns, str):
                    checkpoint_ns = checkpoint_ns.strip()
                    if not checkpoint_ns:
                        return None
                    checkpoint_ns = int(checkpoint_ns)
                
                # Verificar se é um número válido
                if not isinstance(checkpoint_ns, (int, float)) or checkpoint_ns <= 0:
                    return None
                
                timestamp_sec = checkpoint_ns / 1_000_000_000
                dt = datetime.fromtimestamp(timestamp_sec)
                return dt.isoformat()
            except (ValueError, TypeError):
                logger.debug(f"Erro ao converter checkpoint_ns {checkpoint_ns}")
                return None
        
        return None
    except Exception as e:
        logger.warning(f"Erro ao buscar timestamp do checkpoint: {e}")
        return None

def render_conversations_section(idea: dict):
    """
    Renderiza seção de conversas relacionadas (Épico 14.3).
    
    Args:
        idea: Dict com dados da ideia
    
    Comportamento:
        - Lista threads relacionados à ideia com timestamp formatado ("18/11, 14:56")
        - Por enquanto, mostra apenas o thread_id atual (arquitetura atual não suporta múltiplos threads por ideia)
        - Formato: "Thread ID · 18/11, 14:56"
    """
    st.subheader("💬 Conversas relacionadas")
    
    thread_id = idea.get("thread_id")
    
    if thread_id:
        # Buscar timestamp do checkpoint (mais preciso)
        checkpoint_timestamp = get_thread_timestamp_from_checkpoint(thread_id)
        
        if checkpoint_timestamp:
            # Converter ISO para formato "DD/MM, HH:MM"
            try:
                dt = datetime.fromisoformat(checkpoint_timestamp.replace("Z", "+00:00"))
                formatted_timestamp = dt.strftime("%d/%m, %H:%M")
            except:
                # Fallback: extrair do thread_id
                formatted_timestamp = format_thread_timestamp(thread_id)
        else:
            # Fallback: extrair do thread_id
            formatted_timestamp = format_thread_timestamp(thread_id)
        
        # Mostrar lista de conversas (por enquanto apenas uma)
        st.markdown(f"**Conversa:** `{thread_id[:20]}...`")
        st.caption(f"📅 {formatted_timestamp}")
        st.caption("_Esta ideia foi cristalizada durante a conversa acima_")
    else:
        st.caption("_Nenhuma conversa vinculada_")

# === APLICAÇÃO PRINCIPAL ===

def main():
    """Função principal da página de detalhes."""

    # Sidebar com navegação
    render_sidebar()

    # Obter idea_id da query string
    idea_id = st.query_params.get("id")

    if not idea_id:
        st.error("❌ ID da ideia não fornecido.")
        st.info("Use o sidebar para navegar para 'Pensamentos'.")
        return

    # Carregar ideia do banco
    try:
        db = get_database_manager()
        idea = db.get_idea(idea_id)

        if not idea:
            st.error(f"❌ Ideia '{idea_id}' não encontrada.")
            st.info("Use o sidebar para navegar para 'Pensamentos'.")
            return

        # === HEADER ===

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
