"""
CRUD operations para entidade Ideas.

Este módulo implementa operações de Create, Read, Update para Ideas:
- create_idea: Criar nova ideia
- get_idea: Buscar ideia por ID
- update_idea_status: Atualizar status
- update_idea_current_argument: Atualizar argumento focal
- update_idea: Atualizar campos genéricos (title, thread_id, etc)
- list_ideas: Listar ideias com filtros

Épico 11.2: Setup de Persistência e Schema SQLite
Data: 2025-11-17
Refatoração: Divisão de manager.py em CRUD separados
"""

import sqlite3
import logging
from typing import Optional, List, Dict, Any
from uuid import uuid4

logger = logging.getLogger(__name__)


class IdeasCRUD:
    """
    CRUD operations para entidade Ideas.
    
    Esta classe encapsula todas as operações de banco relacionadas a Ideas.
    Recebe conexão SQLite como dependência (não gerencia conexão).
    """

    def __init__(self, conn: sqlite3.Connection):
        """
        Inicializa IdeasCRUD com conexão SQLite.
        
        Args:
            conn: Conexão SQLite ativa (row_factory já configurado)
        """
        self.conn = conn

    def create_idea(
        self,
        title: str,
        status: str = "exploring",
        idea_id: Optional[str] = None,
        thread_id: Optional[str] = None
    ) -> str:
        """
        Cria uma nova ideia no banco de dados.

        Args:
            title: Título da ideia (ex: "Drones em obras")
            status: Status inicial (padrão: "exploring")
                Valores válidos: "exploring" | "structured" | "validated"
            idea_id: UUID customizado (opcional). Se None, gera automaticamente.
            thread_id: Thread ID do LangGraph (opcional). Para preservar histórico de conversas.

        Returns:
            str: UUID da ideia criada

        Raises:
            ValueError: Se status inválido
            sqlite3.Error: Erro ao inserir no banco

        Example:
            >>> crud = IdeasCRUD(conn)
            >>> idea_id = crud.create_idea("LLMs e produtividade", "exploring", thread_id="session-123")
        """
        if status not in ("exploring", "structured", "validated"):
            raise ValueError(f"Status inválido: {status}. Use: exploring, structured, validated")

        if idea_id is None:
            idea_id = str(uuid4())

        query = """
        INSERT INTO ideas (id, title, status, current_argument_id, thread_id)
        VALUES (?, ?, ?, NULL, ?)
        """

        try:
            self.conn.execute(query, (idea_id, title, status, thread_id))
            self.conn.commit()
            logger.info(f"Idea criada: {idea_id} - '{title}' ({status}) - thread_id: {thread_id}")
            return idea_id

        except sqlite3.Error as e:
            logger.error(f"Erro ao criar idea: {e}")
            self.conn.rollback()
            raise

    def get_idea(self, idea_id: str) -> Optional[Dict[str, Any]]:
        """
        Busca uma ideia por ID.

        Args:
            idea_id: UUID da ideia

        Returns:
            Dict com campos da ideia ou None se não encontrada

        Example:
            >>> idea = crud.get_idea(idea_id)
            >>> if idea:
            ...     print(idea["title"])
            ...     print(idea["thread_id"])  # Thread ID do LangGraph
        """
        query = """
        SELECT id, title, status, current_argument_id, thread_id, created_at, updated_at
        FROM ideas
        WHERE id = ?
        """

        cursor = self.conn.execute(query, (idea_id,))
        row = cursor.fetchone()

        if row:
            return dict(row)
        return None

    def update_idea_status(self, idea_id: str, status: str) -> bool:
        """
        Atualiza status de uma ideia.

        Args:
            idea_id: UUID da ideia
            status: Novo status ("exploring" | "structured" | "validated")

        Returns:
            bool: True se atualizado com sucesso, False se ideia não encontrada

        Raises:
            ValueError: Se status inválido

        Example:
            >>> crud.update_idea_status(idea_id, "structured")
        """
        if status not in ("exploring", "structured", "validated"):
            raise ValueError(f"Status inválido: {status}")

        query = "UPDATE ideas SET status = ? WHERE id = ?"

        try:
            cursor = self.conn.execute(query, (status, idea_id))
            self.conn.commit()

            if cursor.rowcount > 0:
                logger.info(f"Status da idea {idea_id} atualizado para: {status}")
                return True
            else:
                logger.warning(f"Idea {idea_id} não encontrada para atualizar status")
                return False

        except sqlite3.Error as e:
            logger.error(f"Erro ao atualizar status: {e}")
            self.conn.rollback()
            raise

    def update_idea_current_argument(
        self,
        idea_id: str,
        argument_id: Optional[str]
    ) -> bool:
        """
        Atualiza argumento focal de uma ideia (FK current_argument_id).

        Args:
            idea_id: UUID da ideia
            argument_id: UUID do argumento focal (ou None para remover)

        Returns:
            bool: True se atualizado, False se ideia não encontrada

        Example:
            >>> crud.update_idea_current_argument(idea_id, argument_id)
        """
        query = "UPDATE ideas SET current_argument_id = ? WHERE id = ?"

        try:
            cursor = self.conn.execute(query, (argument_id, idea_id))
            self.conn.commit()

            if cursor.rowcount > 0:
                logger.info(f"Argumento focal da idea {idea_id} atualizado: {argument_id}")
                return True
            else:
                logger.warning(f"Idea {idea_id} não encontrada para atualizar argumento")
                return False

        except sqlite3.Error as e:
            logger.error(f"Erro ao atualizar argumento focal: {e}")
            self.conn.rollback()
            raise

    def update_idea(
        self,
        idea_id: str,
        title: Optional[str] = None,
        status: Optional[str] = None,
        thread_id: Optional[str] = None,
        current_argument_id: Optional[str] = None
    ) -> bool:
        """
        Atualiza campos genéricos de uma ideia.

        Args:
            idea_id: UUID da ideia
            title: Novo título (opcional)
            status: Novo status (opcional)
            thread_id: Novo thread_id (opcional)
            current_argument_id: Novo argumento focal (opcional)

        Returns:
            bool: True se atualizado, False se ideia não encontrada

        Raises:
            ValueError: Se status inválido

        Example:
            >>> crud.update_idea(idea_id, title="Novo título")
            >>> crud.update_idea(idea_id, thread_id="session-456")
        """
        # Validar status se fornecido
        if status is not None and status not in ("exploring", "structured", "validated"):
            raise ValueError(f"Status inválido: {status}")

        # Construir query dinamicamente baseado nos campos fornecidos
        updates = []
        params = []

        if title is not None:
            updates.append("title = ?")
            params.append(title)

        if status is not None:
            updates.append("status = ?")
            params.append(status)

        if thread_id is not None:
            updates.append("thread_id = ?")
            params.append(thread_id)

        if current_argument_id is not None:
            updates.append("current_argument_id = ?")
            params.append(current_argument_id)

        if not updates:
            logger.warning(f"Nenhum campo fornecido para atualizar idea {idea_id}")
            return False

        query = f"UPDATE ideas SET {', '.join(updates)} WHERE id = ?"
        params.append(idea_id)

        try:
            cursor = self.conn.execute(query, params)
            self.conn.commit()

            if cursor.rowcount > 0:
                logger.info(f"Idea {idea_id} atualizada: {', '.join(updates)}")
                return True
            else:
                logger.warning(f"Idea {idea_id} não encontrada para atualizar")
                return False

        except sqlite3.Error as e:
            logger.error(f"Erro ao atualizar idea: {e}")
            self.conn.rollback()
            raise

    def list_ideas(
        self,
        status: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Lista ideias com filtros opcionais.

        Args:
            status: Filtrar por status (opcional)
            limit: Máximo de resultados (padrão: 10)

        Returns:
            List[Dict]: Lista de ideias ordenadas por updated_at DESC

        Example:
            >>> ideas = crud.list_ideas(status="exploring", limit=5)
            >>> for idea in ideas:
            ...     print(idea["title"])
            ...     print(idea["thread_id"])  # Thread ID do LangGraph
        """
        if status:
            query = """
            SELECT id, title, status, current_argument_id, thread_id, created_at, updated_at
            FROM ideas
            WHERE status = ?
            ORDER BY updated_at DESC
            LIMIT ?
            """
            params = (status, limit)
        else:
            query = """
            SELECT id, title, status, current_argument_id, thread_id, created_at, updated_at
            FROM ideas
            ORDER BY updated_at DESC
            LIMIT ?
            """
            params = (limit,)

        cursor = self.conn.execute(query, params)
        rows = cursor.fetchall()

        return [dict(row) for row in rows]

