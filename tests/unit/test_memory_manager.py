"""
Testes unitários para MemoryManager (Épico 6).

Valida gerenciamento de histórico e metadados por agente.

Versão: 1.0
Data: 12/11/2025
"""

import pytest
from agents.memory.memory_manager import MemoryManager, AgentExecution


class TestMemoryManagerBasics:
    """Testes básicos de adição de execuções (lógica de negócio)."""

    def test_tokens_total_calculation(self):
        """Deve calcular tokens_total corretamente (lógica de negócio)."""
        manager = MemoryManager()

        execution = manager.add_execution(
            session_id="test-session",
            agent_name="orchestrator",
            tokens_input=100,
            tokens_output=50,
            summary="Teste"
        )

        assert execution.tokens_total == 150  # Valida cálculo real




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
