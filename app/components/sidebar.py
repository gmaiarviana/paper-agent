"""
Componente sidebar para gerenciamento de ideias (Épico 12).

Responsável por:
- Listar ideias recentes (últimas 10)
- Destacar ideia ativa
- Botão "+ Nova Ideia"
- Alternar entre ideias
- Busca de ideias por título e status
- Explorador de argumentos versionados
- Integração com DatabaseManager (persistência em data.db)

Versão: 3.0
Data: 18/11/2025
Status: Épico 12 - Gestão de Ideias
"""

import streamlit as st
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

from app.components.session_helpers import (
    get_current_session_id
)
from agents.database.manager import get_database_manager

logger = logging.getLogger(__name__)


def render_sidebar() -> str:
    """
    Renderiza sidebar com lista de ideias (Épico 12).

    Returns:
        str: ID da sessão ativa (thread_id do LangGraph)

    Comportamento (Épico 12):
        - Lista de ideias do DatabaseManager (data.db)
        - Últimas 10 ideias ordenadas por updated_at DESC
        - Botão "+ Nova Ideia"
        - Ideia ativa destacada
        - Busca por título e filtro por status
        - Explorador de argumentos versionados (expansível)
        - Alternância entre ideias restaura contexto completo
    """
    with st.sidebar:
        st.title("📂 Ideias")

        # Botão para nova ideia (12.4)
        if st.button("➕ Nova Ideia", use_container_width=True, type="primary"):
            _create_new_idea()

        st.markdown("---")

        # Busca e filtros (12.6)
        search_query = st.text_input("🔍 Buscar ideias...", key="search_ideas")
        status_filter = st.selectbox(
            "Filtrar por status",
            ["Todas", "Explorando", "Estruturada", "Validada"],
            key="filter_status"
        )

        st.markdown("---")

        # Buscar ideias do banco (12.2)
        ideas = _get_recent_ideas(search_query=search_query, status_filter=status_filter, limit=10)

        if ideas and len(ideas) > 0:
            # Renderizar lista de ideias (12.2)
            _render_idea_list(ideas)
        else:
            # Nenhuma ideia no banco ainda
            st.caption("Nenhuma ideia encontrada.")
            st.caption("Clique em '➕ Nova Ideia' para começar!")

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


def _create_new_idea() -> None:
    """
    Cria nova ideia e define como ativa (Épico 12.4 + melhorias).

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

        # Carregar thread_id persistido (RESTAURA HISTÓRICO!)
        loaded_thread_id = idea.get("thread_id")
        if loaded_thread_id:
            st.session_state.active_session_id = loaded_thread_id
            logger.info(f"Thread ID restaurado: {loaded_thread_id}")
        else:
            # Fallback: gerar novo se ideia antiga não tem thread_id
            new_session_id = get_current_session_id()
            st.session_state.active_session_id = new_session_id
            logger.warning(f"Ideia sem thread_id. Gerando novo: {new_session_id}")

        # Restaurar argumento focal
        if idea.get("current_argument_id"):
            current_arg = db.get_argument(idea["current_argument_id"])
            st.session_state.current_argument = current_arg
        else:
            st.session_state.current_argument = None

        # Limpar histórico (será recarregado do SqliteSaver automaticamente)
        if "messages" in st.session_state:
            st.session_state.messages = []

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
