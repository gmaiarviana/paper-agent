"""
Testes unitários para DatabaseManager e operações CRUD.

Cobre:
- DatabaseManager: Inicialização, singleton, delegação
- IdeasCRUD: create, get, update, list
- ArgumentsCRUD: create, get, versionamento
- Schema: Validação de estrutura do banco

Estes testes usam SQLite em memória (sem persistência real).
Seguem a estratégia: unit tests rápidos, sem dependências externas.

Versão: 1.0
Data: 2025-12-XX
"""

import pytest
import sqlite3
import tempfile
from pathlib import Path
from uuid import uuid4

from agents.database.manager import DatabaseManager, get_database_manager
from agents.database.ideas_crud import IdeasCRUD
from agents.database.arguments_crud import ArgumentsCRUD
from agents.models.cognitive_model import CognitiveModel
from agents.models.proposition import Proposicao


# =============================================================================
# FIXTURES
# =============================================================================

@pytest.fixture
def temp_db():
    """Cria banco SQLite temporário em memória para testes."""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row  # Permite acesso por nome de coluna
    yield conn
    conn.close()


@pytest.fixture
def initialized_db(temp_db):
    """Banco inicializado com schema completo."""
    from agents.database.schema import SCHEMA_SQL
    temp_db.executescript(SCHEMA_SQL)
    return temp_db


@pytest.fixture
def ideas_crud(initialized_db):
    """IdeasCRUD com banco inicializado."""
    return IdeasCRUD(initialized_db)


@pytest.fixture
def arguments_crud(initialized_db):
    """ArgumentsCRUD com banco inicializado."""
    return ArgumentsCRUD(initialized_db)


@pytest.fixture
def sample_cognitive_model():
    """CognitiveModel de exemplo para testes."""
    return CognitiveModel(
        claim="LLMs aumentam produtividade em desenvolvimento",
        proposicoes=[
            Proposicao(texto="Desenvolvimento com IA é mais rápido", solidez=0.8),
            Proposicao(texto="Código gerado precisa revisão", solidez=0.7),
            Proposicao(texto="Desenvolvedores usam ferramentas corretamente", solidez=0.5),
        ],
        open_questions=["Qual o impacto na qualidade?"],
        contradictions=[],
        solid_grounds=[],
        context={"domain": "software", "technology": "LLMs"}
    )


# =============================================================================
# TESTES: IDEASCRUD
# =============================================================================

class TestIdeasCRUD:
    """Testes para operações CRUD de Ideas."""

    def test_create_idea_basic(self, ideas_crud):
        """Testa criação básica de ideia."""
        idea_id = ideas_crud.create_idea(
            title="Drones em obras",
            status="exploring"
        )

        assert idea_id is not None
        assert isinstance(idea_id, str)
        assert len(idea_id) == 36  # UUID length

        # Verificar que foi inserida
        idea = ideas_crud.get_idea(idea_id)
        assert idea is not None
        assert idea["title"] == "Drones em obras"
        assert idea["status"] == "exploring"
        assert idea["current_argument_id"] is None

    def test_create_idea_with_custom_id(self, ideas_crud):
        """Testa criação com ID customizado."""
        custom_id = str(uuid4())
        idea_id = ideas_crud.create_idea(
            title="Teste",
            idea_id=custom_id
        )

        assert idea_id == custom_id
        assert ideas_crud.get_idea(custom_id) is not None

    def test_create_idea_with_thread_id(self, ideas_crud):
        """Testa criação com thread_id (preservação de histórico)."""
        idea_id = ideas_crud.create_idea(
            title="Teste",
            thread_id="langgraph-thread-123"
        )

        idea = ideas_crud.get_idea(idea_id)
        assert idea["thread_id"] == "langgraph-thread-123"

    def test_create_idea_invalid_status(self, ideas_crud):
        """Testa que status inválido lança ValueError."""
        with pytest.raises(ValueError, match="Status inválido"):
            ideas_crud.create_idea(
                title="Teste",
                status="invalid_status"
            )

    def test_get_idea_not_found(self, ideas_crud):
        """Testa get_idea retorna None para ID inexistente."""
        result = ideas_crud.get_idea("non-existent-id")
        assert result is None

    def test_update_idea_status(self, ideas_crud):
        """Testa atualização de status."""
        idea_id = ideas_crud.create_idea(title="Teste", status="exploring")
        
        ideas_crud.update_idea_status(idea_id, "structured")
        
        idea = ideas_crud.get_idea(idea_id)
        assert idea["status"] == "structured"

    def test_update_idea_status_invalid(self, ideas_crud):
        """Testa que status inválido na atualização lança erro."""
        idea_id = ideas_crud.create_idea(title="Teste")
        
        with pytest.raises(ValueError, match="Status inválido"):
            ideas_crud.update_idea_status(idea_id, "invalid")

    def test_update_idea_current_argument(self, ideas_crud, initialized_db):
        """Testa atualização de argumento focal."""
        # Criar ideia e argumento
        idea_id = ideas_crud.create_idea(title="Teste")
        arg_id = str(uuid4())
        
        # Simular argumento (para poder criar FK)
        initialized_db.execute(
            "INSERT INTO arguments (id, idea_id, claim, version) VALUES (?, ?, ?, ?)",
            (arg_id, idea_id, "Claim teste", 1)
        )
        initialized_db.commit()
        
        ideas_crud.update_idea_current_argument(idea_id, arg_id)
        
        idea = ideas_crud.get_idea(idea_id)
        assert idea["current_argument_id"] == arg_id

    def test_list_ideas_empty(self, ideas_crud):
        """Testa list_ideas retorna vazio quando não há ideias."""
        ideas = ideas_crud.list_ideas()
        assert ideas == []

    def test_list_ideas_with_status_filter(self, ideas_crud):
        """Testa list_ideas com filtro de status."""
        idea1 = ideas_crud.create_idea(title="Exploring", status="exploring")
        idea2 = ideas_crud.create_idea(title="Structured", status="structured")
        idea3 = ideas_crud.create_idea(title="Validated", status="validated")

        exploring = ideas_crud.list_ideas(status="exploring")
        assert len(exploring) == 1
        assert exploring[0]["id"] == idea1

        structured = ideas_crud.list_ideas(status="structured")
        assert len(structured) == 1
        assert structured[0]["id"] == idea2

    def test_list_ideas_ordering(self, ideas_crud, initialized_db):
        """Testa que list_ideas ordena por updated_at DESC."""
        idea1 = ideas_crud.create_idea(title="First")
        idea2 = ideas_crud.create_idea(title="Second")
        idea3 = ideas_crud.create_idea(title="Third")

        all_ideas = ideas_crud.list_ideas()
        assert len(all_ideas) == 3
        
        # Verificar que todas as ideias estão presentes
        titles = [idea["title"] for idea in all_ideas]
        assert "First" in titles
        assert "Second" in titles
        assert "Third" in titles
        
        # Verificar que está ordenado (mais recente primeiro)
        # SQLite pode ter timestamps muito próximos, então verificamos que pelo menos está ordenado
        updated_dates = [idea["updated_at"] for idea in all_ideas]
        assert updated_dates == sorted(updated_dates, reverse=True)


# =============================================================================
# TESTES: ARGUMENTSCRUD
# =============================================================================

class TestArgumentsCRUD:
    """Testes para operações CRUD de Arguments."""

    def test_create_argument_basic(self, arguments_crud, ideas_crud, sample_cognitive_model):
        """Testa criação básica de argumento."""
        idea_id = ideas_crud.create_idea(title="Teste")
        
        arg_id = arguments_crud.create_argument(
            idea_id=idea_id,
            cognitive_model=sample_cognitive_model
        )

        assert arg_id is not None
        assert isinstance(arg_id, str)

        # Verificar que foi inserido
        arg = arguments_crud.get_argument(arg_id)
        assert arg is not None
        assert arg["idea_id"] == idea_id
        assert arg["claim"] == sample_cognitive_model.claim
        assert arg["version"] == 1  # Primeira versão

    def test_create_argument_auto_versioning(self, arguments_crud, ideas_crud, sample_cognitive_model):
        """Testa que versionamento é auto-incrementado."""
        idea_id = ideas_crud.create_idea(title="Teste")
        
        arg1_id = arguments_crud.create_argument(idea_id, sample_cognitive_model)
        arg2_id = arguments_crud.create_argument(idea_id, sample_cognitive_model)
        arg3_id = arguments_crud.create_argument(idea_id, sample_cognitive_model)

        arg1 = arguments_crud.get_argument(arg1_id)
        arg2 = arguments_crud.get_argument(arg2_id)
        arg3 = arguments_crud.get_argument(arg3_id)

        assert arg1["version"] == 1
        assert arg2["version"] == 2
        assert arg3["version"] == 3

    def test_create_argument_custom_version(self, arguments_crud, ideas_crud, sample_cognitive_model):
        """Testa criação com versão customizada."""
        idea_id = ideas_crud.create_idea(title="Teste")
        
        arg_id = arguments_crud.create_argument(
            idea_id=idea_id,
            cognitive_model=sample_cognitive_model,
            version=5
        )

        arg = arguments_crud.get_argument(arg_id)
        assert arg["version"] == 5

    def test_get_arguments_by_idea(self, arguments_crud, ideas_crud, sample_cognitive_model):
        """Testa busca de argumentos por ideia."""
        idea1_id = ideas_crud.create_idea(title="Idea 1")
        idea2_id = ideas_crud.create_idea(title="Idea 2")
        
        # Criar 2 argumentos para idea1, 1 para idea2
        arg1_1 = arguments_crud.create_argument(idea1_id, sample_cognitive_model)
        arg1_2 = arguments_crud.create_argument(idea1_id, sample_cognitive_model)
        arg2_1 = arguments_crud.create_argument(idea2_id, sample_cognitive_model)

        args_idea1 = arguments_crud.get_arguments_by_idea(idea1_id)
        args_idea2 = arguments_crud.get_arguments_by_idea(idea2_id)

        assert len(args_idea1) == 2
        assert {arg["id"] for arg in args_idea1} == {arg1_1, arg1_2}
        
        assert len(args_idea2) == 1
        assert args_idea2[0]["id"] == arg2_1

    def test_get_latest_argument_version(self, arguments_crud, ideas_crud, sample_cognitive_model):
        """Testa busca da versão mais recente."""
        idea_id = ideas_crud.create_idea(title="Teste")
        
        arg1_id = arguments_crud.create_argument(idea_id, sample_cognitive_model)
        arg2_id = arguments_crud.create_argument(idea_id, sample_cognitive_model)
        arg3_id = arguments_crud.create_argument(idea_id, sample_cognitive_model)

        latest = arguments_crud.get_latest_argument_version(idea_id)
        assert latest is not None
        assert latest["id"] == arg3_id
        assert latest["version"] == 3

    def test_get_latest_argument_version_empty(self, arguments_crud, ideas_crud):
        """Testa que get_latest retorna None quando não há argumentos."""
        idea_id = ideas_crud.create_idea(title="Teste")
        
        latest = arguments_crud.get_latest_argument_version(idea_id)
        assert latest is None


# =============================================================================
# TESTES: DATABASEMANAGER
# =============================================================================

@pytest.fixture
def temp_db_path():
    """Cria caminho temporário para banco de dados."""
    import tempfile
    import os
    fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    yield db_path
    # Limpar arquivo
    try:
        Path(db_path).unlink(missing_ok=True)
    except PermissionError:
        pass


@pytest.fixture(autouse=True)
def reset_db_singleton():
    """Reset singleton antes de cada teste em TestDatabaseManager."""
    import agents.database.manager as manager_module
    # Fechar conexão existente se houver
    if manager_module._db_instance is not None:
        try:
            manager_module._db_instance.conn.close()
        except Exception:
            pass
        manager_module._db_instance = None
    yield
    # Limpar após teste
    if manager_module._db_instance is not None:
        try:
            manager_module._db_instance.conn.close()
        except Exception:
            pass
        manager_module._db_instance = None


class TestDatabaseManager:
    """Testes para DatabaseManager (orquestrador)."""

    def test_initialization_creates_schema(self):
        """Testa que inicialização cria schema automaticamente."""
        import tempfile
        import os
        
        # Criar arquivo temporário com nome único
        fd, db_path = tempfile.mkstemp(suffix=".db")
        os.close(fd)  # Fechar file descriptor, mantendo o arquivo
        
        try:
            db = DatabaseManager(db_path=db_path)
            
            # Verificar que tabelas existem (usar conn, não _conn)
            conn = db.conn
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name IN ('ideas', 'arguments')"
            )
            tables = {row[0] for row in cursor.fetchall()}
            
            assert "ideas" in tables
            assert "arguments" in tables
            
            # Fechar conexão antes de deletar
            db.conn.close()
        finally:
            # Tentar deletar arquivo (pode falhar no Windows se ainda estiver aberto)
            try:
                Path(db_path).unlink(missing_ok=True)
            except PermissionError:
                # No Windows, pode estar travado. Tentar depois.
                pass

    def test_get_database_manager_singleton(self, temp_db_path):
        """Testa que get_database_manager retorna singleton."""
        db1 = get_database_manager(temp_db_path)
        db2 = get_database_manager(temp_db_path)

        # Mesma instância (singleton)
        assert db1 is db2

    def test_delegates_to_ideas_crud(self, temp_db_path):
        """Testa que DatabaseManager delega para IdeasCRUD."""
        db = get_database_manager(temp_db_path)

        idea_id = db.create_idea("Teste Delegation")
        idea = db.get_idea(idea_id)

        assert idea is not None
        assert idea["title"] == "Teste Delegation"

    def test_delegates_to_arguments_crud(self, temp_db_path, sample_cognitive_model):
        """Testa que DatabaseManager delega para ArgumentsCRUD."""
        db = get_database_manager(temp_db_path)

        idea_id = db.create_idea("Teste")
        arg_id = db.create_argument(idea_id, sample_cognitive_model)

        arg = db.get_argument(arg_id)
        assert arg is not None
        assert arg["claim"] == sample_cognitive_model.claim

    def test_update_idea_current_argument(self, temp_db_path, sample_cognitive_model):
        """Testa operação completa: criar ideia → argumento → atualizar."""
        db = get_database_manager(temp_db_path)

        idea_id = db.create_idea("Teste")
        arg_id = db.create_argument(idea_id, sample_cognitive_model)

        db.update_idea_current_argument(idea_id, arg_id)

        idea = db.get_idea(idea_id)
        assert idea["current_argument_id"] == arg_id

