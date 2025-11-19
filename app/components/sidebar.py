"""
Componente sidebar para navegação de conversas (Épico 14.1).

Responsável por:
- Listar conversas recentes (últimas 5 - reduzido de 10)
- Destacar conversa ativa
- Botão "+ Nova Conversa"
- Alternar entre conversas (restaura contexto completo - Épico 14.5)
- Botões de navegação para páginas dedicadas:
  - [📖 Meus Pensamentos] → /pensamentos
  - [🏷️ Catálogo] → /catalogo (desabilitado até Épico 13)

Versão: 4.0
Data: 19/11/2025
Status: Épico 14.1 - Navegação em Três Espaços
"""

import streamlit as st
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

from app.components.session_helpers import (
    get_current_session_id
)
from app.components.conversation_helpers import (
    restore_conversation_context,
    list_recent_conversations,
    get_relative_timestamp
)
from agents.database.manager import get_database_manager

logger = logging.getLogger(__name__)


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
            _create_new_conversation()

        st.markdown("---")

        # Buscar conversas recentes do SqliteSaver (14.1)
        conversations = list_recent_conversations(limit=5)

        if conversations and len(conversations) > 0:
            st.caption("**Conversas recentes:**")
            _render_conversation_list(conversations)
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
    return _get_active_session_id()


def _get_active_session_id() -> str:
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


def _create_new_conversation() -> None:
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


def _create_new_idea() -> None:
    """
    Cria nova ideia e define como ativa (Épico 12.4 + melhorias).

    NOTA: Esta função mantida para compatibilidade com sistema anterior.
    A partir do Épico 14, conversas são criadas primeiro (_create_new_conversation),
    e ideias são cristaliz adas pelo sistema durante conversa.

    Comportamento:
        - Gera título com timestamp
        - Gera novo thread_id (LangGraph)
        - Cria registro no database (status="exploring", thread_id persistido)
        - Limpa histórico de mensagens
        - Define como ideia ativa
    """
    try:
        # Gerar título com timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        title = f"Nova Ideia {timestamp}"

        # Gerar novo thread_id para LangGraph
        new_session_id = get_current_session_id()

        # Criar registro no database COM thread_id
        db = get_database_manager()
        idea_id = db.create_idea(title=title, status="exploring", thread_id=new_session_id)

        # Definir como ativa
        st.session_state.active_idea_id = idea_id
        st.session_state.active_session_id = new_session_id

        # Limpar histórico
        if "messages" in st.session_state:
            st.session_state.messages = []

        logger.info(f"Nova ideia criada: {idea_id} - '{title}' - thread_id: {new_session_id}")
        st.success(f"✅ Nova ideia criada: {title}")
        st.rerun()

    except Exception as e:
        logger.error(f"Erro ao criar nova ideia: {e}", exc_info=True)
        st.error(f"❌ Erro ao criar nova ideia: {e}")


def _get_recent_ideas(
    search_query: str = "",
    status_filter: str = "Todas",
    limit: int = 10
) -> List[Dict[str, Any]]:
    """
    Busca ideias recentes do DatabaseManager com filtros (Épico 12.2 + 12.6).

    Args:
        search_query: Termo de busca no título (LIKE query)
        status_filter: Filtro por status ("Todas" | "Explorando" | "Estruturada" | "Validada")
        limit: Número máximo de ideias a retornar

    Returns:
        Lista de ideias ordenadas por updated_at DESC
        [
            {
                "id": str (UUID),
                "title": str,
                "status": str,
                "current_argument_id": str (UUID ou None),
                "created_at": str (ISO),
                "updated_at": str (ISO)
            }
        ]
    """
    try:
        db = get_database_manager()

        # Mapear filtro de status para valor do banco
        status_map = {
            "Explorando": "exploring",
            "Estruturada": "structured",
            "Validada": "validated"
        }
        status = status_map.get(status_filter)  # None se "Todas"

        # Buscar ideias do banco
        ideas = db.list_ideas(status=status, limit=limit)

        # Filtrar por título (busca case-insensitive)
        if search_query:
            search_lower = search_query.lower()
            ideas = [
                idea for idea in ideas
                if search_lower in idea["title"].lower()
            ]

        logger.debug(f"Ideias carregadas do banco: {len(ideas)}")
        return ideas

    except Exception as e:
        logger.error(f"Erro ao carregar ideias: {e}", exc_info=True)
        return []


def _render_conversation_list(conversations: List[Dict[str, Any]]) -> None:
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
            _switch_conversation(thread_id)

        # Mostrar timestamp relativo abaixo do botão
        if not is_active:
            st.caption(f"  {relative_time}")


def _switch_conversation(thread_id: str) -> None:
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


def _switch_idea(idea_id: str) -> None:
    """
    Alterna para outra ideia (Épico 12.3 + melhorias).

    Args:
        idea_id: UUID da ideia a carregar

    Comportamento:
        - Define idea_id como ativa
        - Carrega thread_id persistido (restaura histórico de conversas!)
        - Restaura argumento focal (current_argument_id)
        - Limpa histórico de mensagens do session_state (será recarregado do SqliteSaver)
        - Força re-render da interface
    """
    try:
        db = get_database_manager()
        idea = db.get_idea(idea_id)

        if not idea:
            st.error(f"❌ Ideia {idea_id} não encontrada")
            return

        # Definir como ativa
        st.session_state.active_idea_id = idea_id

        # Carregar thread_id persistido
        loaded_thread_id = idea.get("thread_id")
        if not loaded_thread_id:
            # Fallback: gerar novo se ideia antiga não tem thread_id
            new_session_id = get_current_session_id()
            st.session_state.active_session_id = new_session_id
            st.session_state.messages = []
            logger.warning(f"Ideia sem thread_id. Gerando novo: {new_session_id}")
        else:
            # BUGFIX Épico 14.5: Restaurar histórico de mensagens do SqliteSaver
            logger.info(f"Restaurando contexto da conversa: {loaded_thread_id}")
            success = restore_conversation_context(loaded_thread_id)

            if not success:
                # Fallback: se restauração falhar, limpar mensagens
                logger.warning(f"Falha ao restaurar contexto de {loaded_thread_id}. Limpando mensagens.")
                st.session_state.active_session_id = loaded_thread_id
                st.session_state.messages = []

        # Restaurar argumento focal
        if idea.get("current_argument_id"):
            current_arg = db.get_argument(idea["current_argument_id"])
            st.session_state.current_argument = current_arg
        else:
            st.session_state.current_argument = None

        logger.info(f"Ideia alternada: {idea_id} - '{idea['title']}' - thread_id: {loaded_thread_id}")
        st.rerun()

    except Exception as e:
        logger.error(f"Erro ao alternar ideia: {e}", exc_info=True)
        st.error(f"❌ Erro ao alternar ideia: {e}")


def _render_idea_list(ideas: List[Dict[str, Any]]) -> None:
    """
    Renderiza lista de ideias na sidebar (Épico 12.2 + 12.5).

    Args:
        ideas: Lista de ideias do DatabaseManager

    Layout:
        🔍 Título da ideia • 3 argumentos
        📝 Título da ideia (ativa) • 2 argumentos
          ▼ Argumentos:
            • V2 [focal]: Claim...
            • V1: Claim...
        ...

    Comportamento:
        - Ideia ativa marcada visualmente (bold, background)
        - Badge de status (🔍 | 📝 | ✅)
        - # argumentos exibido
        - Expansível para mostrar argumentos versionados (12.5)
        - Clique em ideia alterna via _switch_idea()
    """
    active_idea_id = st.session_state.get("active_idea_id")

    st.caption("**Ideias recentes:**")

    db = get_database_manager()

    for idea in ideas:
        idea_id = idea["id"]
        title = idea["title"]
        status = idea["status"]
        is_active = (idea_id == active_idea_id)

        # Badge de status
        status_badges = {
            "exploring": "🔍",
            "structured": "📝",
            "validated": "✅"
        }
        status_icon = status_badges.get(status, "❓")

        # Contar argumentos
        arguments = db.get_arguments_by_idea(idea_id)
        num_args = len(arguments)

        # Botão para selecionar ideia
        button_label = f"{status_icon} {title} • {num_args} arg(s)"

        # Destacar ativa
        button_type = "primary" if is_active else "secondary"

        if st.button(
            button_label,
            key=f"idea_{idea_id}",
            use_container_width=True,
            disabled=is_active,  # Desabilitar se já está ativa
            type=button_type
        ):
            _switch_idea(idea_id)

        # Explorador de argumentos (12.5 - expansível)
        if num_args > 0:
            with st.expander(f"📂 Ver {num_args} argumento(s)", expanded=False):
                _render_argument_list(idea, arguments)


def _render_argument_list(idea: Dict[str, Any], arguments: List[Dict[str, Any]]) -> None:
    """
    Renderiza lista de argumentos versionados (Épico 12.5).

    Args:
        idea: Dict da ideia (contém current_argument_id)
        arguments: Lista de argumentos ordenados por versão DESC

    Layout:
        • V3 [focal]: Claim curto...
          [Ver detalhes]
        • V2: Claim curto...
          [Ver detalhes]
        • V1: Claim curto...
          [Ver detalhes]

    Comportamento:
        - Badge [focal] destaca argumento focal
        - Claim truncado (~50 chars)
        - Botão "Ver detalhes" abre modal (12.5.4)
    """
    focal_arg_id = idea.get("current_argument_id")

    for arg in arguments:
        arg_id = arg["id"]
        version = arg["version"]
        claim = arg["claim"]
        is_focal = (arg_id == focal_arg_id)

        # Badge focal
        focal_badge = " [focal]" if is_focal else ""

        # Claim truncado
        claim_short = claim[:50] + "..." if len(claim) > 50 else claim

        # Exibir argumento
        st.caption(f"• **V{version}{focal_badge}**: {claim_short}")

        # Botão para ver detalhes (modal)
        if st.button(
            "🔍 Ver detalhes",
            key=f"arg_details_{arg_id}",
            use_container_width=True
        ):
            _show_argument_details(arg)


@st.dialog("🧠 Detalhes do Argumento", width="large")
def _show_argument_details(argument: Dict[str, Any]) -> None:
    """
    Modal com detalhes completos do argumento (Épico 12.5.4).

    Args:
        argument: Dict do argumento (com claim, premises, assumptions, etc)

    Layout (modal):
        Versão: V3
        ---
        Claim: [texto completo]
        Premises: [lista]
        Assumptions: [lista]
        Open Questions: [lista]
        Contradictions: [lista]
        Solid Grounds: [lista]
        Context: [JSON]
    """
    version = argument["version"]
    claim = argument["claim"]
    premises = argument["premises"]
    assumptions = argument["assumptions"]
    open_questions = argument["open_questions"]
    contradictions = argument["contradictions"]
    solid_grounds = argument["solid_grounds"]
    context = argument["context"]

    # Cabeçalho
    st.markdown(f"### Versão V{version}")
    st.caption(f"Criado em: {argument.get('created_at', 'Desconhecido')}")

    st.markdown("---")

    # Claim
    st.markdown("**Claim (Afirmação Central)**")
    st.write(claim)

    # Premises
    if premises:
        st.markdown("**Premises (Premissas)**")
        for i, premise in enumerate(premises, 1):
            st.write(f"{i}. {premise}")
    else:
        st.caption("_Nenhuma premissa definida_")

    st.markdown("---")

    # Assumptions
    if assumptions:
        st.markdown("**Assumptions (Suposições)**")
        for i, assumption in enumerate(assumptions, 1):
            st.write(f"⚠️ {i}. {assumption}")
    else:
        st.caption("_Nenhuma suposição identificada_")

    # Open Questions
    if open_questions:
        st.markdown("**Open Questions (Perguntas Abertas)**")
        for i, question in enumerate(open_questions, 1):
            st.write(f"❓ {i}. {question}")
    else:
        st.caption("_Nenhuma pergunta aberta_")

    st.markdown("---")

    # Contradictions
    if contradictions:
        st.markdown("**Contradictions (Contradições)**")
        for i, contradiction in enumerate(contradictions, 1):
            st.write(f"❌ {i}. {contradiction}")
    else:
        st.caption("_Nenhuma contradição detectada_")

    # Solid Grounds
    if solid_grounds:
        st.markdown("**Solid Grounds (Bases Sólidas)**")
        for i, ground in enumerate(solid_grounds, 1):
            st.write(f"✅ {i}. {ground}")
    else:
        st.caption("_Nenhuma base sólida identificada_")

    st.markdown("---")

    # Context (JSON)
    if context:
        with st.expander("🔍 Contexto (JSON)"):
            st.json(context)
