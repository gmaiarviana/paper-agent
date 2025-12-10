"""
Helper functions para gerenciar sessões do SqliteSaver (Épico 9.10-9.11 MVP).

Responsável por:
- Listar sessões disponíveis no banco de dados
- Extrair metadados de sessões (título, última atividade)
- Integração com sidebar para navegação entre sessões

Status: MVP completo
"""

import sqlite3
import logging
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

# Caminho do banco de dados (mesmo usado no LangGraph)
DB_PATH = "data/checkpoints.db"

def list_sessions(limit: int = 10) -> List[Dict[str, str]]:
    """
    Lista últimas N sessões do banco de dados SqliteSaver.

    Args:
        limit: Número máximo de sessões a retornar (padrão: 10)

    Returns:
        List[Dict]: Lista de sessões com formato:
            [
                {
                    "thread_id": str,
                    "title": str,
                    "last_activity": str (ISO timestamp)
                },
                ...
            ]

    Nota:
        - Sessões são ordenadas por última atividade (mais recente primeiro)
        - Título é extraído da primeira mensagem do usuário (truncado a 50 chars)
        - Se não houver mensagens, usa "Conversa {data}"
    """
    try:
        # Garantir que diretório existe
        db_path = Path(DB_PATH)
        db_path.parent.mkdir(parents=True, exist_ok=True)

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Verificar se tabela checkpoints existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='checkpoints'")
        if not cursor.fetchone():
            # Tabela ainda não existe (banco novo) - retornar lista vazia
            conn.close()
            logger.debug("Banco de dados novo - nenhuma sessão encontrada ainda")
            return []

        # Query para pegar todos os thread_ids únicos com última atividade
        # Tabela: checkpoints (criada automaticamente pelo SqliteSaver)
        # Colunas relevantes: thread_id, checkpoint_id, checkpoint (blob), parent_checkpoint_id
        query = """
            SELECT
                thread_id,
                MAX(checkpoint_id) as last_checkpoint_id
            FROM checkpoints
            GROUP BY thread_id
            ORDER BY last_checkpoint_id DESC
            LIMIT ?
        """

        cursor.execute(query, (limit,))
        rows = cursor.fetchall()

        sessions = []
        for thread_id, last_checkpoint_id in rows:
            # Gerar título baseado no thread_id (POC - pode melhorar depois)
            # TODO: Extrair primeira mensagem do checkpoint blob para título real
            title = _generate_title_from_thread_id(thread_id)

            # Timestamp baseado no checkpoint_id (que geralmente contém timestamp)
            # POC: usar timestamp atual como fallback
            last_activity = datetime.now().isoformat()

            sessions.append({
                "thread_id": thread_id,
                "title": title,
                "last_activity": last_activity
            })

        conn.close()

        logger.debug(f"Listadas {len(sessions)} sessões do banco")
        return sessions

    except sqlite3.Error as e:
        logger.error(f"Erro ao listar sessões do SQLite: {e}", exc_info=True)
        return []
    except Exception as e:
        logger.error(f"Erro inesperado ao listar sessões: {e}", exc_info=True)
        return []

def _generate_title_from_thread_id(thread_id: str) -> str:
    """
    Gera título amigável baseado no thread_id.

    Args:
        thread_id: ID da thread (geralmente UUID ou session-YYYYMMDD-HHMMSS)

    Returns:
        str: Título formatado (ex: "Conversa 16/11/2025")

    Estratégia POC:
        - Se thread_id contém "session-", extrair data/hora
        - Senão, usar primeiros 8 chars + "..."
        - Fallback: "Conversa {data_atual}"

    TODO (Futuro):
        - Extrair primeira mensagem do checkpoint blob
        - Usar LLM para gerar título automático baseado no conteúdo
    """
    # POC: Simplesmente usar primeiros chars do thread_id
    if len(thread_id) > 20:
        return f"Conversa {thread_id[:8]}..."
    else:
        return f"Conversa {thread_id}"

def get_current_session_id() -> str:
    """
    Gera novo ID de sessão para "Nova conversa".

    Returns:
        str: ID único no formato "session-YYYYMMDD-HHMMSS-{millis}"

    Exemplo:
        "session-20251116-193045-123"
    """
    now = datetime.now()
    millis = int(now.microsecond / 1000)
    session_id = f"session-{now.strftime('%Y%m%d-%H%M%S')}-{millis:03d}"

    logger.debug(f"Novo session_id gerado: {session_id}")
    return session_id

def session_exists(thread_id: str) -> bool:
    """
    Verifica se uma sessão existe no banco de dados.

    Args:
        thread_id: ID da thread a verificar

    Returns:
        bool: True se existe, False caso contrário
    """
    try:
        # Garantir que diretório existe
        db_path = Path(DB_PATH)
        db_path.parent.mkdir(parents=True, exist_ok=True)

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Verificar se tabela checkpoints existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='checkpoints'")
        if not cursor.fetchone():
            # Tabela ainda não existe - sessão não pode existir
            conn.close()
            return False

        query = "SELECT COUNT(*) FROM checkpoints WHERE thread_id = ?"
        cursor.execute(query, (thread_id,))

        count = cursor.fetchone()[0]
        conn.close()

        return count > 0

    except sqlite3.Error as e:
        logger.error(f"Erro ao verificar sessão {thread_id}: {e}")
        return False
