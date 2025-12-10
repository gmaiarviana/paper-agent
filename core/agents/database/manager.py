"""
DatabaseManager para persistência de Ideas e Arguments.

Este módulo atua como orquestrador que delega operações CRUD para módulos especializados:
- IdeasCRUD: Operações de Ideas (agents/database/ideas_crud.py)
- ArgumentsCRUD: Operações de Arguments (agents/database/arguments_crud.py)

Responsabilidades:
- Gerenciar conexão SQLite (data/data.db)
- Inicializar schema automaticamente
- Delegar operações CRUD para módulos especializados
- Manter interface compatível com código existente

Épico 11.2: Setup de Persistência e Schema SQLite

Refatoração: Divisão em CRUD separados (ideas_crud.py, arguments_crud.py)
"""

import sqlite3
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any

from .schema import SCHEMA_SQL, DATABASE_VERSION, CREATE_METADATA_TABLE
from .ideas_crud import IdeasCRUD
from .arguments_crud import ArgumentsCRUD
from core.agents.models.cognitive_model import CognitiveModel

logger = logging.getLogger(__name__)


def _get_default_db_path() -> str:
    """
    Retorna o caminho padrão do banco de dados, suportando ambas as estruturas.

    Detecta automaticamente se está em core/agents/database/ ou agents/database/
    e ajusta o caminho para data/data.db na raiz do projeto.
    """
    current_file = Path(__file__).resolve()
    # Subir até encontrar a raiz do projeto (onde data/ deve estar)
    # De core/agents/database/ → subir 4 níveis → raiz
    # De agents/database/ → subir 3 níveis → raiz

    # Verificar se estamos em core/agents/database/
    if current_file.parent.parent.parent.name == "core":
        project_root = current_file.parent.parent.parent.parent
    else:
        # Estamos em agents/database/
        project_root = current_file.parent.parent.parent

    return str(project_root / "data" / "data.db")

class DatabaseManager:
    """
    Gerenciador de banco de dados SQLite para Ideas e Arguments.

    Atua como orquestrador que delega operações CRUD para módulos especializados.
    Mantém interface compatível com código existente.

    Singleton pattern: Use get_database_manager() ao invés de instanciar diretamente.

    Example:
        >>> db = get_database_manager()
        >>> idea_id = db.create_idea("Drones em obras", "exploring")
        >>> arg_id = db.create_argument(idea_id, cognitive_model)
        >>> db.update_idea_current_argument(idea_id, arg_id)
        >>> idea = db.get_idea(idea_id)
    """

    def __init__(self, db_path: Optional[str] = None):
        """
        Inicializa DatabaseManager com conexão SQLite.

        Args:
            db_path: Caminho para arquivo SQLite (padrão: data/data.db na raiz do projeto)

        Notes:
            - Cria diretório data/ se não existir
            - Inicializa schema automaticamente
            - Habilita foreign keys (SQLite default é desabilitado)
            - Cria instâncias de CRUDs especializados
        """
        if db_path is None:
            db_path = _get_default_db_path()
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        self.conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # Retorna dicts ao invés de tuples

        # Habilitar foreign keys (SQLite default é desabilitado)
        self.conn.execute("PRAGMA foreign_keys = ON")

        # Inicializar schema
        self._initialize_schema()

        # Criar instâncias de CRUDs especializados
        self.ideas = IdeasCRUD(self.conn)
        self.arguments = ArgumentsCRUD(self.conn)

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
    # OPERAÇÕES CRUD - IDEAS (Delegadas para IdeasCRUD)
    # =========================================================================

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
            >>> db = get_database_manager()
            >>> idea_id = db.create_idea("LLMs e produtividade", "exploring", thread_id="session-123")
        """
        return self.ideas.create_idea(title, status, idea_id, thread_id)

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
            ...     print(idea["thread_id"])  # Thread ID do LangGraph
        """
        return self.ideas.get_idea(idea_id)

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
        return self.ideas.update_idea_status(idea_id, status)

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
        return self.ideas.update_idea_current_argument(idea_id, argument_id)

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
            >>> db.update_idea(idea_id, title="Novo título")
            >>> db.update_idea(idea_id, thread_id="session-456")
        """
        return self.ideas.update_idea(idea_id, title, status, thread_id, current_argument_id)

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
            ...     print(idea["thread_id"])  # Thread ID do LangGraph
        """
        return self.ideas.list_ideas(status, limit)

    # =========================================================================
    # OPERAÇÕES CRUD - ARGUMENTS (Delegadas para ArgumentsCRUD)
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
        return self.arguments.create_argument(idea_id, cognitive_model, argument_id, version)

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
            ...     print(arg["proposicoes"])  # Lista deserializada com solidez
        """
        return self.arguments.get_argument(argument_id)

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
        return self.arguments.get_arguments_by_idea(idea_id, limit)

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
        return self.arguments.get_latest_argument_version(idea_id)

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
