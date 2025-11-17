"""
DatabaseManager para persistência de Ideas e Arguments.

Este módulo implementa operações CRUD para as entidades do domínio:
- Ideas: Criar, buscar, atualizar status e argumento focal
- Arguments: Criar com versionamento automático, buscar por idea

Responsabilidades:
- Gerenciar conexão SQLite (data/data.db)
- Inicializar schema automaticamente
- Auto-incrementar versões de argumentos por idea
- Serializar/deserializar JSON fields (premises, assumptions, etc)

Épico 11.2: Setup de Persistência e Schema SQLite
Data: 2025-11-17
"""

import sqlite3
import json
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any
from uuid import uuid4
from datetime import datetime

from .schema import SCHEMA_SQL, DATABASE_VERSION, CREATE_METADATA_TABLE
from agents.models.cognitive_model import CognitiveModel

logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    Gerenciador de banco de dados SQLite para Ideas e Arguments.

    Singleton pattern: Use get_database_manager() ao invés de instanciar diretamente.

    Example:
        >>> db = get_database_manager()
        >>> idea_id = db.create_idea("Drones em obras", "exploring")
        >>> arg_id = db.create_argument(idea_id, cognitive_model)
        >>> db.update_idea_current_argument(idea_id, arg_id)
        >>> idea = db.get_idea(idea_id)
    """

    def __init__(self, db_path: str = "data/data.db"):
        """
        Inicializa DatabaseManager com conexão SQLite.

        Args:
            db_path: Caminho para arquivo SQLite (padrão: data/data.db)

        Notes:
            - Cria diretório data/ se não existir
            - Inicializa schema automaticamente
            - Habilita foreign keys (SQLite default é desabilitado)
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        self.conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # Retorna dicts ao invés de tuples

        # Habilitar foreign keys (SQLite default é desabilitado)
        self.conn.execute("PRAGMA foreign_keys = ON")

        # Inicializar schema
        self._initialize_schema()

        logger.info(f"DatabaseManager inicializado: {self.db_path}")

    def _initialize_schema(self):
        """
        Inicializa schema do banco de dados.

        Executa SCHEMA_SQL para criar tabelas, índices, triggers e views.
        Também cria tabela de metadata para tracking de versão.

        Notes:
            - Idempotente: CREATE TABLE IF NOT EXISTS
            - Triggers são recriados se já existirem
        """
        logger.info("Inicializando schema do banco de dados...")

        try:
            # Executar schema principal (tabelas, índices, triggers, views)
            self.conn.executescript(SCHEMA_SQL)

            # Criar tabela de metadata e registrar versão
            # Usar executescript pois CREATE_METADATA_TABLE tem múltiplas instruções
            self.conn.executescript(CREATE_METADATA_TABLE.replace("?", f"'{DATABASE_VERSION}'"))

            self.conn.commit()
            logger.info(f"Schema inicializado com sucesso (versão {DATABASE_VERSION})")

        except sqlite3.Error as e:
            logger.error(f"Erro ao inicializar schema: {e}")
            self.conn.rollback()
            raise

    # =========================================================================
    # OPERAÇÕES CRUD - IDEAS
    # =========================================================================

    def create_idea(
        self,
        title: str,
        status: str = "exploring",
        idea_id: Optional[str] = None
    ) -> str:
        """
        Cria uma nova ideia no banco de dados.

        Args:
            title: Título da ideia (ex: "Drones em obras")
            status: Status inicial (padrão: "exploring")
                Valores válidos: "exploring" | "structured" | "validated"
            idea_id: UUID customizado (opcional). Se None, gera automaticamente.

        Returns:
            str: UUID da ideia criada

        Raises:
            ValueError: Se status inválido
            sqlite3.Error: Erro ao inserir no banco

        Example:
            >>> db = get_database_manager()
            >>> idea_id = db.create_idea("LLMs e produtividade", "exploring")
        """
        if status not in ("exploring", "structured", "validated"):
            raise ValueError(f"Status inválido: {status}. Use: exploring, structured, validated")

        if idea_id is None:
            idea_id = str(uuid4())

        query = """
        INSERT INTO ideas (id, title, status, current_argument_id)
        VALUES (?, ?, ?, NULL)
        """

        try:
            self.conn.execute(query, (idea_id, title, status))
            self.conn.commit()
            logger.info(f"Idea criada: {idea_id} - '{title}' ({status})")
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
            >>> idea = db.get_idea(idea_id)
            >>> if idea:
            ...     print(idea["title"])
        """
        query = """
        SELECT id, title, status, current_argument_id, created_at, updated_at
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
            >>> db.update_idea_status(idea_id, "structured")
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
            >>> db.update_idea_current_argument(idea_id, argument_id)
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
            >>> ideas = db.list_ideas(status="exploring", limit=5)
            >>> for idea in ideas:
            ...     print(idea["title"])
        """
        if status:
            query = """
            SELECT id, title, status, current_argument_id, created_at, updated_at
            FROM ideas
            WHERE status = ?
            ORDER BY updated_at DESC
            LIMIT ?
            """
            params = (status, limit)
        else:
            query = """
            SELECT id, title, status, current_argument_id, created_at, updated_at
            FROM ideas
            ORDER BY updated_at DESC
            LIMIT ?
            """
            params = (limit,)

        cursor = self.conn.execute(query, params)
        rows = cursor.fetchall()

        return [dict(row) for row in rows]

    # =========================================================================
    # OPERAÇÕES CRUD - ARGUMENTS
    # =========================================================================

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
            >>> model = CognitiveModel(claim="LLMs aumentam produtividade", ...)
            >>> arg_id = db.create_argument(idea_id, model)  # version=1 (auto)
            >>> arg_id_v2 = db.create_argument(idea_id, model_v2)  # version=2 (auto)
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
            >>> arg = db.get_argument(argument_id)
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
            >>> args = db.get_arguments_by_idea(idea_id)
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
            >>> latest = db.get_latest_argument_version(idea_id)
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

    def close(self):
        """Fecha conexão com banco de dados."""
        self.conn.close()
        logger.info("Conexão com banco de dados fechada")


# =========================================================================
# SINGLETON GLOBAL
# =========================================================================

_db_instance: Optional[DatabaseManager] = None


def get_database_manager(db_path: str = "data/data.db") -> DatabaseManager:
    """
    Obtém instância singleton de DatabaseManager.

    Garante que apenas uma conexão SQLite existe durante execução.

    Args:
        db_path: Caminho para banco de dados (padrão: data/data.db)

    Returns:
        DatabaseManager: Instância singleton

    Example:
        >>> db = get_database_manager()
        >>> idea_id = db.create_idea("Minha ideia")
    """
    global _db_instance

    if _db_instance is None:
        _db_instance = DatabaseManager(db_path)

    return _db_instance
