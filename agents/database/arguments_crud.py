"""
CRUD operations para entidade Arguments.

Este módulo implementa operações de Create, Read para Arguments:
- create_argument: Criar novo argumento versionado
- get_argument: Buscar argumento por ID
- get_arguments_by_idea: Buscar todos os argumentos de uma ideia
- get_latest_argument_version: Buscar versão mais recente

Épico 11.2: Setup de Persistência e Schema SQLite
Data: 2025-11-17
Refatoração: Divisão de manager.py em CRUD separados
"""

import sqlite3
import json
import logging
from typing import Optional, List, Dict, Any
from uuid import uuid4

from agents.models.cognitive_model import CognitiveModel

logger = logging.getLogger(__name__)


class ArgumentsCRUD:
    """
    CRUD operations para entidade Arguments.
    
    Esta classe encapsula todas as operações de banco relacionadas a Arguments.
    Recebe conexão SQLite como dependência (não gerencia conexão).
    """

    def __init__(self, conn: sqlite3.Connection):
        """
        Inicializa ArgumentsCRUD com conexão SQLite.
        
        Args:
            conn: Conexão SQLite ativa (row_factory já configurado)
        """
        self.conn = conn

    def create_argument(
        self,
        idea_id: str,
        cognitive_model: CognitiveModel,
        argument_id: Optional[str] = None,
        version: Optional[int] = None
    ) -> str:
        """
        Cria um novo argumento versionado para uma ideia.

        Auto-incrementa version se não especificada: busca MAX(version) + 1 para idea_id.

        Args:
            idea_id: UUID da ideia proprietária
            cognitive_model: CognitiveModel Pydantic com argumento completo
            argument_id: UUID customizado (opcional)
            version: Versão customizada (opcional). Se None, auto-incrementa.

        Returns:
            str: UUID do argumento criado

        Example:
            >>> crud = ArgumentsCRUD(conn)
            >>> model = CognitiveModel(claim="LLMs aumentam produtividade", ...)
            >>> arg_id = crud.create_argument(idea_id, model)  # version=1 (auto)
            >>> arg_id_v2 = crud.create_argument(idea_id, model_v2)  # version=2 (auto)
        """
        if argument_id is None:
            argument_id = str(uuid4())

        # Auto-incrementar version se não especificada
        if version is None:
            version = self._get_next_argument_version(idea_id)

        # Serializar campos JSON do CognitiveModel
        query = """
        INSERT INTO arguments (
            id, idea_id, claim, premises, assumptions,
            open_questions, contradictions, solid_grounds, context, version
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        params = (
            argument_id,
            idea_id,
            cognitive_model.claim,
            json.dumps(cognitive_model.premises),
            json.dumps(cognitive_model.assumptions),
            json.dumps(cognitive_model.open_questions),
            json.dumps([c.model_dump() for c in cognitive_model.contradictions]),
            json.dumps([s.model_dump() for s in cognitive_model.solid_grounds]),
            json.dumps(cognitive_model.context),
            version
        )

        try:
            self.conn.execute(query, params)
            self.conn.commit()
            logger.info(f"Argumento criado: {argument_id} (idea={idea_id}, version={version})")
            return argument_id

        except sqlite3.Error as e:
            logger.error(f"Erro ao criar argumento: {e}")
            self.conn.rollback()
            raise

    def get_argument(self, argument_id: str) -> Optional[Dict[str, Any]]:
        """
        Busca um argumento por ID.

        Args:
            argument_id: UUID do argumento

        Returns:
            Dict com campos do argumento (JSON deserializado) ou None

        Example:
            >>> arg = crud.get_argument(argument_id)
            >>> if arg:
            ...     print(arg["claim"])
            ...     print(arg["premises"])  # Lista deserializada
        """
        query = """
        SELECT id, idea_id, claim, premises, assumptions, open_questions,
               contradictions, solid_grounds, context, version, created_at, updated_at
        FROM arguments
        WHERE id = ?
        """

        cursor = self.conn.execute(query, (argument_id,))
        row = cursor.fetchone()

        if row:
            return self._deserialize_argument(dict(row))
        return None

    def get_arguments_by_idea(
        self,
        idea_id: str,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Busca todos os argumentos de uma ideia (histórico de versões).

        Args:
            idea_id: UUID da ideia
            limit: Máximo de resultados (opcional)

        Returns:
            List[Dict]: Argumentos ordenados por version DESC (V3, V2, V1...)

        Example:
            >>> args = crud.get_arguments_by_idea(idea_id)
            >>> for arg in args:
            ...     print(f"V{arg['version']}: {arg['claim']}")
        """
        if limit:
            query = """
            SELECT id, idea_id, claim, premises, assumptions, open_questions,
                   contradictions, solid_grounds, context, version, created_at, updated_at
            FROM arguments
            WHERE idea_id = ?
            ORDER BY version DESC
            LIMIT ?
            """
            params = (idea_id, limit)
        else:
            query = """
            SELECT id, idea_id, claim, premises, assumptions, open_questions,
                   contradictions, solid_grounds, context, version, created_at, updated_at
            FROM arguments
            WHERE idea_id = ?
            ORDER BY version DESC
            """
            params = (idea_id,)

        cursor = self.conn.execute(query, params)
        rows = cursor.fetchall()

        return [self._deserialize_argument(dict(row)) for row in rows]

    def get_latest_argument_version(self, idea_id: str) -> Optional[Dict[str, Any]]:
        """
        Busca a versão mais recente do argumento de uma ideia.

        Args:
            idea_id: UUID da ideia

        Returns:
            Dict com argumento mais recente ou None se ideia não tem argumentos

        Example:
            >>> latest = crud.get_latest_argument_version(idea_id)
            >>> if latest:
            ...     print(f"Versão atual: V{latest['version']}")
        """
        args = self.get_arguments_by_idea(idea_id, limit=1)
        return args[0] if args else None

    # =========================================================================
    # HELPERS INTERNOS
    # =========================================================================

    def _get_next_argument_version(self, idea_id: str) -> int:
        """
        Obtém próxima versão de argumento para uma ideia (MAX + 1).

        Args:
            idea_id: UUID da ideia

        Returns:
            int: Próxima versão (1 se primeira, 2 se já existe V1, etc)
        """
        query = "SELECT MAX(version) as max_version FROM arguments WHERE idea_id = ?"
        cursor = self.conn.execute(query, (idea_id,))
        row = cursor.fetchone()

        max_version = row["max_version"]
        return 1 if max_version is None else max_version + 1

    def _deserialize_argument(self, row: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deserializa campos JSON de um argumento.

        Args:
            row: Dict com dados brutos do banco (JSON como strings)

        Returns:
            Dict com JSON deserializado (listas e dicts Python)
        """
        return {
            "id": row["id"],
            "idea_id": row["idea_id"],
            "claim": row["claim"],
            "premises": json.loads(row["premises"]),
            "assumptions": json.loads(row["assumptions"]),
            "open_questions": json.loads(row["open_questions"]),
            "contradictions": json.loads(row["contradictions"]),
            "solid_grounds": json.loads(row["solid_grounds"]),
            "context": json.loads(row["context"]),
            "version": row["version"],
            "created_at": row["created_at"],
            "updated_at": row["updated_at"]
        }

