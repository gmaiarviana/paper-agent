"""
Helpers para gerenciamento de conversas e restauração de contexto (Épico 14.5).

Responsável por:
- Restaurar histórico de mensagens do SqliteSaver
- Converter mensagens do formato LangGraph para formato Streamlit
- Listar conversas recentes do SqliteSaver
- Alternar entre conversas preservando contexto

Status: Épico 14.5 - Bugfix Crítico
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage

from agents.multi_agent_graph import create_multi_agent_graph

logger = logging.getLogger(__name__)

def restore_conversation_context(thread_id: str) -> bool:
    """
    Restaura contexto completo de uma conversa do SqliteSaver.

    Este é o bugfix crítico do Épico 14.5. Anteriormente, alternar entre
    conversas limpava o histórico mas não restaurava do SqliteSaver,
    resultando em chat branco.

    Args:
        thread_id: ID da conversa a restaurar (formato: session-YYYYMMDD-HHMMSS-{millis})

    Returns:
        bool: True se restauração foi bem-sucedida, False caso contrário

    Comportamento:
        1. Carrega estado do LangGraph via graph.get_state(config)
        2. Extrai mensagens do estado (formato LangChain)
        3. Converte para formato Streamlit (role, content, tokens, cost, duration)
        4. Atualiza st.session_state.messages
        5. Atualiza st.session_state.active_session_id
        6. Registra logs DEBUG para troubleshooting

    Side Effects:
        - Modifica st.session_state.messages
        - Modifica st.session_state.active_session_id
        - Registra logs (INFO e DEBUG)

    Example:
        >>> success = restore_conversation_context("session-20251119-143056-123")
        >>> if success:
        >>>     st.rerun()
    """
    try:
        logger.info(f"Iniciando restauração de conversa: {thread_id}")

        # 1. Criar grafo (singleton em produção via cache)
        graph = create_multi_agent_graph()

        # 2. Carregar estado do SqliteSaver
        config = {"configurable": {"thread_id": thread_id}}
        restored_state = graph.get_state(config)

        if not restored_state:
            logger.warning(f"Estado não encontrado para thread_id: {thread_id}")
            return False

        # 3. Extrair mensagens do estado
        messages = restored_state.values.get("messages", [])
        logger.debug(f"Mensagens encontradas no SqliteSaver: {len(messages)}")

        # 4. Converter mensagens para formato Streamlit
        streamlit_messages = _convert_messages_to_streamlit_format(messages)

        # 5. Atualizar session_state
        st.session_state.messages = streamlit_messages
        st.session_state.active_session_id = thread_id

        logger.info(
            f"Conversa restaurada com sucesso: {thread_id} "
            f"({len(streamlit_messages)} mensagens)"
        )

        # Debug logging (apenas primeiros caracteres)
        if streamlit_messages:
            first_msg_preview = streamlit_messages[0]["content"][:50]
            logger.debug(f"Primeira mensagem: {first_msg_preview}...")

        return True

    except Exception as e:
        logger.error(
            f"Erro ao restaurar conversa {thread_id}: {e}",
            exc_info=True
        )
        return False

def _convert_messages_to_streamlit_format(
    messages: List[Any]
) -> List[Dict[str, Any]]:
    """
    Converte mensagens do formato LangGraph para formato Streamlit.

    Args:
        messages: Lista de mensagens do LangGraph
            [HumanMessage(...), AIMessage(...), ...]

    Returns:
        Lista de mensagens no formato Streamlit:
            [
                {
                    "role": "user" | "assistant",
                    "content": str,
                    "tokens": None,  # Pode ser preenchido do EventBus
                    "cost": None,
                    "duration": None,
                    "timestamp": str (ISO format)
                }
            ]

    Comportamento:
        - HumanMessage → role="user"
        - AIMessage → role="assistant"
        - Outros tipos de mensagem são ignorados (SystemMessage, etc)
        - Métricas (tokens, cost, duration) são None (podem ser buscadas do EventBus)
    """
    streamlit_messages = []

    for msg in messages:
        # Determinar role baseado no tipo
        if isinstance(msg, HumanMessage):
            role = "user"
        elif isinstance(msg, AIMessage):
            role = "assistant"
        else:
            # Ignorar outros tipos (SystemMessage, ToolMessage, etc)
            logger.debug(f"Ignorando mensagem de tipo: {type(msg).__name__}")
            continue

        # Extrair conteúdo
        content = msg.content if hasattr(msg, 'content') else str(msg)

        # Timestamp: tentar extrair dos metadados, senão usar None
        timestamp = None
        if hasattr(msg, 'additional_kwargs'):
            timestamp = msg.additional_kwargs.get('timestamp')

        streamlit_messages.append({
            "role": role,
            "content": content,
            "tokens": None,  # TODO: buscar do EventBus se disponível
            "cost": None,
            "duration": None,
            "timestamp": timestamp
        })

    logger.debug(f"Convertidas {len(streamlit_messages)} mensagens para formato Streamlit")
    return streamlit_messages

def list_recent_conversations(limit: int = 10) -> List[Dict[str, Any]]:
    """
    Lista conversas recentes do SqliteSaver (últimas N conversas).

    Args:
        limit: Número máximo de conversas a retornar (padrão: 10)

    Returns:
        Lista de conversas ordenadas por timestamp DESC:
            [
                {
                    "thread_id": str,
                    "title": str (inferido da primeira mensagem),
                    "last_updated": str (timestamp ISO),
                    "message_count": int,
                    "preview": str (primeiros 50 chars da última mensagem)
                }
            ]

    Comportamento:
        - Query direto no SQLite do SqliteSaver (checkpoints.db)
        - Agrupa por thread_id, ordena por checkpoint_ns DESC
        - Título inferido da primeira mensagem do usuário
        - Fallback: "Conversa de DD/MM HH:MM"

    Nota:
        SqliteSaver armazena checkpoints em tabela `checkpoints`
        com colunas: thread_id, checkpoint_ns, channel_values (blob)
    """
    try:
        import sqlite3
        from pathlib import Path

        # Caminho do banco SqliteSaver (mesmo usado no LangGraph)
        db_path = Path(__file__).parent.parent.parent / "data" / "checkpoints.db"

        if not db_path.exists():
            logger.warning(f"Banco checkpoints.db não encontrado em {db_path}")
            return []

        # Conectar ao banco (usar context manager para garantir fechamento)
        with sqlite3.connect(str(db_path)) as conn:
            cursor = conn.cursor()

            # Query para listar thread_ids com último checkpoint
            # Nota: checkpoint_ns é um número (nanoseconds), maior = mais recente
            query = """
            SELECT
                thread_id,
                MAX(checkpoint_ns) as last_checkpoint_ns
            FROM checkpoints
            GROUP BY thread_id
            ORDER BY last_checkpoint_ns DESC
            LIMIT ?
            """

            cursor.execute(query, (limit,))
            rows = cursor.fetchall()

            conversations = []
            for row in rows:
                thread_id = row[0]
                last_checkpoint_ns = row[1]

                # Inferir título e preview da conversa
                # (requer carregar estado completo - pode ser custoso)
                # Por enquanto, usar fallback simples
                title = _infer_conversation_title(thread_id)
                last_updated = _checkpoint_ns_to_iso(last_checkpoint_ns)

                conversations.append({
                    "thread_id": thread_id,
                    "title": title,
                    "last_updated": last_updated,
                    "message_count": None,  # Requer carregar estado completo
                    "preview": None  # Requer carregar estado completo
                })

        logger.debug(f"Encontradas {len(conversations)} conversas recentes")
        return conversations

    except Exception as e:
        logger.error(f"Erro ao listar conversas recentes: {e}", exc_info=True)
        return []

def _infer_conversation_title(thread_id: str) -> str:
    """
    Infere título da conversa a partir da primeira mensagem do usuário.

    Args:
        thread_id: ID da conversa

    Returns:
        str: Título inferido ou fallback "Conversa de DD/MM HH:MM"

    Comportamento:
        - Carrega estado do SqliteSaver
        - Busca primeira HumanMessage
        - Retorna primeiros 50 caracteres como título
        - Fallback: gera título baseado no timestamp do thread_id
    """
    try:
        graph = create_multi_agent_graph()
        config = {"configurable": {"thread_id": thread_id}}
        state = graph.get_state(config)

        if not state:
            return _fallback_title_from_thread_id(thread_id)

        messages = state.values.get("messages", [])

        # Buscar primeira mensagem do usuário
        for msg in messages:
            if isinstance(msg, HumanMessage):
                content = msg.content[:50]
                # Remover quebras de linha
                content = content.replace("\n", " ").strip()
                return content if content else _fallback_title_from_thread_id(thread_id)

        return _fallback_title_from_thread_id(thread_id)

    except Exception as e:
        logger.warning(f"Erro ao inferir título de {thread_id}: {e}")
        return _fallback_title_from_thread_id(thread_id)

def _fallback_title_from_thread_id(thread_id: str) -> str:
    """
    Gera título fallback a partir do thread_id.

    Args:
        thread_id: ID da conversa (formato: session-YYYYMMDD-HHMMSS-{millis})

    Returns:
        str: "Conversa de DD/MM HH:MM" ou "Conversa (ID curto)"
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

            return f"Conversa de {day}/{month} {hour}:{minute}"

    except Exception as e:
        logger.debug(f"Não foi possível extrair timestamp de {thread_id}: {e}")

    # Fallback final: ID curto
    return f"Conversa ({thread_id[:8]}...)"

def _checkpoint_ns_to_iso(checkpoint_ns) -> str:
    """
    Converte checkpoint_ns (nanoseconds) para timestamp ISO.

    Args:
        checkpoint_ns: Checkpoint em nanoseconds (int ou str)

    Returns:
        str: Timestamp ISO (YYYY-MM-DDTHH:MM:SSZ)
    """
    try:
        # Validar e converter para int
        if checkpoint_ns is None:
            return datetime.now().isoformat()
        
        # Se for string, verificar se não está vazia
        if isinstance(checkpoint_ns, str):
            checkpoint_ns = checkpoint_ns.strip()
            if not checkpoint_ns:
                return datetime.now().isoformat()
            checkpoint_ns = int(checkpoint_ns)
        
        # Verificar se é um número válido
        if not isinstance(checkpoint_ns, (int, float)) or checkpoint_ns <= 0:
            return datetime.now().isoformat()
        
        # Converter nanoseconds para seconds
        timestamp_sec = checkpoint_ns / 1_000_000_000
        dt = datetime.fromtimestamp(timestamp_sec)
        return dt.isoformat()
    except (ValueError, TypeError) as e:
        logger.debug(f"Erro ao converter checkpoint_ns {checkpoint_ns}: {e}")
        return datetime.now().isoformat()
    except Exception as e:
        logger.warning(f"Erro inesperado ao converter checkpoint_ns {checkpoint_ns}: {e}")
        return datetime.now().isoformat()

def get_relative_timestamp(iso_timestamp: str) -> str:
    """
    Converte timestamp ISO para formato relativo ("5min atrás", "2h atrás").

    Args:
        iso_timestamp: Timestamp em formato ISO (YYYY-MM-DDTHH:MM:SSZ)

    Returns:
        str: Timestamp relativo legível

    Examples:
        >>> get_relative_timestamp("2025-11-19T14:25:00Z")
        "5min atrás"
        >>> get_relative_timestamp("2025-11-19T12:00:00Z")
        "2h atrás"
    """
    try:
        dt = datetime.fromisoformat(iso_timestamp.replace("Z", "+00:00"))
        now = datetime.now(dt.tzinfo)
        delta = now - dt

        # Menos de 1 minuto
        if delta.total_seconds() < 60:
            return "agora"

        # Menos de 1 hora
        if delta.total_seconds() < 3600:
            minutes = int(delta.total_seconds() / 60)
            return f"{minutes}min atrás"

        # Menos de 24 horas
        if delta.total_seconds() < 86400:
            hours = int(delta.total_seconds() / 3600)
            return f"{hours}h atrás"

        # Menos de 7 dias
        if delta.days < 7:
            if delta.days == 1:
                return "ontem"
            return f"{delta.days} dias atrás"

        # Mais de 7 dias
        weeks = delta.days // 7
        if weeks == 1:
            return "1 semana atrás"
        return f"{weeks} semanas atrás"

    except Exception as e:
        logger.warning(f"Erro ao converter timestamp {iso_timestamp}: {e}")
        return "data desconhecida"
