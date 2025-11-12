"""
Testes unitários para MemoryManager (Épico 6).

Valida gerenciamento de histórico e metadados por agente.

Versão: 1.0
Data: 12/11/2025
"""

import pytest
from agents.memory.memory_manager import MemoryManager, AgentExecution


class TestMemoryManagerBasics:
    """Testes básicos de inicialização e adição de execuções."""

    def test_initialization(self):
        """MemoryManager deve inicializar com memória vazia."""
        manager = MemoryManager()

        assert manager is not None
        assert len(manager._memory) == 0

    def test_add_single_execution(self):
        """Deve adicionar execução única com sucesso."""
        manager = MemoryManager()

        execution = manager.add_execution(
            session_id="test-session",
            agent_name="orchestrator",
            tokens_input=100,
            tokens_output=50,
            summary="Classificou input como 'vague'"
        )

        assert execution is not None
        assert execution.agent_name == "orchestrator"
        assert execution.tokens_input == 100
        assert execution.tokens_output == 50
        assert execution.tokens_total == 150
        assert execution.summary == "Classificou input como 'vague'"
        assert execution.timestamp is not None

    def test_add_multiple_executions_same_agent(self):
        """Deve adicionar múltiplas execuções do mesmo agente."""
        manager = MemoryManager()

        manager.add_execution("s1", "orchestrator", 100, 50, "Ação 1")
        manager.add_execution("s1", "orchestrator", 200, 100, "Ação 2")

        history = manager.get_agent_history("s1", "orchestrator")
        assert len(history) == 2
        assert history[0].summary == "Ação 1"
        assert history[1].summary == "Ação 2"

    def test_add_executions_different_agents(self):
        """Deve adicionar execuções de diferentes agentes."""
        manager = MemoryManager()

        manager.add_execution("s1", "orchestrator", 100, 50, "Orquestrou")
        manager.add_execution("s1", "structurer", 200, 100, "Estruturou")
        manager.add_execution("s1", "methodologist", 300, 150, "Avaliou")

        orch_history = manager.get_agent_history("s1", "orchestrator")
        struct_history = manager.get_agent_history("s1", "structurer")
        meth_history = manager.get_agent_history("s1", "methodologist")

        assert len(orch_history) == 1
        assert len(struct_history) == 1
        assert len(meth_history) == 1


class TestGetHistory:
    """Testes para recuperação de histórico."""

    def test_get_agent_history_empty(self):
        """Deve retornar lista vazia para agente sem histórico."""
        manager = MemoryManager()

        history = manager.get_agent_history("nonexistent-session", "orchestrator")
        assert history == []

    def test_get_agent_history_wrong_agent(self):
        """Deve retornar lista vazia para agente que não executou."""
        manager = MemoryManager()
        manager.add_execution("s1", "orchestrator", 100, 50, "Ação")

        history = manager.get_agent_history("s1", "nonexistent-agent")
        assert history == []

    def test_get_session_history(self):
        """Deve retornar histórico completo da sessão."""
        manager = MemoryManager()

        manager.add_execution("s1", "orchestrator", 100, 50, "Orquestrou")
        manager.add_execution("s1", "methodologist", 200, 100, "Avaliou")

        session_history = manager.get_session_history("s1")

        assert len(session_history) == 2
        assert "orchestrator" in session_history
        assert "methodologist" in session_history
        assert len(session_history["orchestrator"]) == 1
        assert len(session_history["methodologist"]) == 1

    def test_get_session_history_empty(self):
        """Deve retornar dicionário vazio para sessão inexistente."""
        manager = MemoryManager()

        history = manager.get_session_history("nonexistent-session")
        assert history == {}


class TestTokenTotals:
    """Testes para cálculo de totais de tokens."""

    def test_get_session_totals_single_agent(self):
        """Deve calcular totais para agente único."""
        manager = MemoryManager()

        manager.add_execution("s1", "orchestrator", 100, 50, "A1")
        manager.add_execution("s1", "orchestrator", 200, 100, "A2")

        totals = manager.get_session_totals("s1")

        assert totals["orchestrator"] == 450  # (100+50) + (200+100)
        assert totals["total"] == 450

    def test_get_session_totals_multiple_agents(self):
        """Deve calcular totais para múltiplos agentes."""
        manager = MemoryManager()

        manager.add_execution("s1", "orchestrator", 100, 50, "A1")
        manager.add_execution("s1", "structurer", 200, 100, "A2")
        manager.add_execution("s1", "methodologist", 300, 150, "A3")

        totals = manager.get_session_totals("s1")

        assert totals["orchestrator"] == 150
        assert totals["structurer"] == 300
        assert totals["methodologist"] == 450
        assert totals["total"] == 900

    def test_get_session_totals_empty(self):
        """Deve retornar zero para sessão inexistente."""
        manager = MemoryManager()

        totals = manager.get_session_totals("nonexistent-session")

        assert totals["total"] == 0


class TestResetFunctionality:
    """Testes para funcionalidade de reset."""

    def test_reset_session(self):
        """Deve limpar histórico de sessão específica."""
        manager = MemoryManager()

        manager.add_execution("s1", "orchestrator", 100, 50, "Ação")
        manager.add_execution("s2", "methodologist", 200, 100, "Ação")

        # Resetar sessão s1
        result = manager.reset_session("s1")

        assert result is True
        assert manager.get_session_history("s1") == {}
        assert len(manager.get_session_history("s2")) > 0  # s2 preservada

    def test_reset_nonexistent_session(self):
        """Deve retornar False ao resetar sessão inexistente."""
        manager = MemoryManager()

        result = manager.reset_session("nonexistent-session")
        assert result is False

    def test_reset_all(self):
        """Deve limpar todas as sessões."""
        manager = MemoryManager()

        manager.add_execution("s1", "orchestrator", 100, 50, "A1")
        manager.add_execution("s2", "methodologist", 200, 100, "A2")
        manager.add_execution("s3", "structurer", 300, 150, "A3")

        count = manager.reset_all()

        assert count == 3
        assert len(manager._memory) == 0


class TestLatestExecution:
    """Testes para obter última execução."""

    def test_get_latest_execution(self):
        """Deve retornar execução mais recente de agente."""
        manager = MemoryManager()

        manager.add_execution("s1", "orchestrator", 100, 50, "Primeira")
        manager.add_execution("s1", "orchestrator", 200, 100, "Segunda")
        manager.add_execution("s1", "orchestrator", 300, 150, "Terceira")

        latest = manager.get_latest_execution("s1", "orchestrator")

        assert latest is not None
        assert latest.summary == "Terceira"
        assert latest.tokens_total == 450

    def test_get_latest_execution_empty(self):
        """Deve retornar None se não há execuções."""
        manager = MemoryManager()

        latest = manager.get_latest_execution("s1", "orchestrator")
        assert latest is None


class TestSessionManagement:
    """Testes para gerenciamento de sessões."""

    def test_list_sessions(self):
        """Deve listar todas as sessões ativas."""
        manager = MemoryManager()

        manager.add_execution("s1", "orchestrator", 100, 50, "A1")
        manager.add_execution("s2", "methodologist", 200, 100, "A2")
        manager.add_execution("s3", "structurer", 300, 150, "A3")

        sessions = manager.list_sessions()

        assert len(sessions) == 3
        assert "s1" in sessions
        assert "s2" in sessions
        assert "s3" in sessions

    def test_list_sessions_empty(self):
        """Deve retornar lista vazia se não há sessões."""
        manager = MemoryManager()

        sessions = manager.list_sessions()
        assert sessions == []


class TestExport:
    """Testes para exportação de histórico."""

    def test_export_session_as_dict(self):
        """Deve exportar sessão como dicionário."""
        manager = MemoryManager()

        manager.add_execution("s1", "orchestrator", 100, 50, "Orquestrou")
        manager.add_execution("s1", "methodologist", 200, 100, "Avaliou")

        export = manager.export_session_as_dict("s1")

        assert export["session_id"] == "s1"
        assert "agents" in export
        assert "totals" in export
        assert "orchestrator" in export["agents"]
        assert "methodologist" in export["agents"]
        assert export["totals"]["total"] == 450

    def test_export_empty_session(self):
        """Deve exportar sessão vazia."""
        manager = MemoryManager()

        export = manager.export_session_as_dict("nonexistent-session")

        assert export["session_id"] == "nonexistent-session"
        assert export["agents"] == {}
        assert export["totals"]["total"] == 0


class TestMetadata:
    """Testes para metadados de execuções."""

    def test_add_execution_with_metadata(self):
        """Deve adicionar execução com metadados customizados."""
        manager = MemoryManager()

        execution = manager.add_execution(
            session_id="s1",
            agent_name="orchestrator",
            tokens_input=100,
            tokens_output=50,
            summary="Classificou",
            metadata={"classification": "vague", "reasoning": "Falta estrutura"}
        )

        assert execution.metadata["classification"] == "vague"
        assert execution.metadata["reasoning"] == "Falta estrutura"

    def test_execution_to_dict(self):
        """Deve converter execução para dicionário."""
        execution = AgentExecution(
            agent_name="orchestrator",
            tokens_input=100,
            tokens_output=50,
            tokens_total=150,
            summary="Teste",
            timestamp="2025-11-12T10:00:00Z",
            metadata={"key": "value"}
        )

        result = execution.to_dict()

        assert result["agent_name"] == "orchestrator"
        assert result["tokens_total"] == 150
        assert result["metadata"]["key"] == "value"


class TestMultipleSessions:
    """Testes para isolamento entre sessões."""

    def test_sessions_are_isolated(self):
        """Sessões devem ser isoladas umas das outras."""
        manager = MemoryManager()

        manager.add_execution("s1", "orchestrator", 100, 50, "S1-A1")
        manager.add_execution("s2", "orchestrator", 200, 100, "S2-A1")

        s1_history = manager.get_agent_history("s1", "orchestrator")
        s2_history = manager.get_agent_history("s2", "orchestrator")

        assert len(s1_history) == 1
        assert len(s2_history) == 1
        assert s1_history[0].summary == "S1-A1"
        assert s2_history[0].summary == "S2-A1"

    def test_reset_one_session_preserves_others(self):
        """Resetar uma sessão não deve afetar outras."""
        manager = MemoryManager()

        manager.add_execution("s1", "orchestrator", 100, 50, "A1")
        manager.add_execution("s2", "orchestrator", 200, 100, "A2")
        manager.add_execution("s3", "orchestrator", 300, 150, "A3")

        manager.reset_session("s2")

        assert len(manager.get_session_history("s1")) > 0
        assert len(manager.get_session_history("s2")) == 0
        assert len(manager.get_session_history("s3")) > 0
