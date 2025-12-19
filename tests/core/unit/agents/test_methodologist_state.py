"""
Testes unitários para o estado do agente Metodologista.

Valida a criação e inicialização correta do MethodologistState.
"""

import pytest
import sys
from unittest.mock import MagicMock

# Mock langgraph antes de importar módulos que dependem dele
# Criar estrutura completa de mocks para evitar problemas de __path__
_mock_langgraph = MagicMock()
_mock_checkpoint = MagicMock()
_mock_memory = MagicMock()
_mock_memory.MemorySaver = MagicMock()

sys.modules['langgraph'] = _mock_langgraph
sys.modules['langgraph.checkpoint'] = _mock_checkpoint
sys.modules['langgraph.checkpoint.memory'] = _mock_memory

# Configurar __path__ nos mocks para evitar AttributeError
_mock_langgraph.__path__ = []
_mock_checkpoint.__path__ = []
_mock_memory.__path__ = []

from core.agents.methodologist import MethodologistState, create_initial_state

class TestMethodologistState:
    """Testes para criação e validação do estado do Metodologista."""

    def test_create_initial_state_with_defaults(self):
        """Deve criar estado inicial com valores padrão corretos."""
        hypothesis = "Café aumenta produtividade"

        state = create_initial_state(hypothesis)

        # Validar todos os campos obrigatórios
        assert state["hypothesis"] == hypothesis
        assert state["messages"] == []
        assert state["clarifications"] == {}
        assert state["status"] == "pending"
        assert state["iterations"] == 0
        assert state["max_iterations"] == 3  # Valor padrão

    def test_create_initial_state_with_custom_max_iterations(self):
        """Deve respeitar max_iterations customizado."""
        hypothesis = "Teste"
        custom_max = 5

        state = create_initial_state(hypothesis, max_iterations=custom_max)

        assert state["max_iterations"] == custom_max
        assert state["iterations"] == 0

    def test_initial_state_status_is_pending(self):
        """Deve sempre iniciar com status 'pending'."""
        state = create_initial_state("Qualquer hipótese")

        assert state["status"] == "pending"

    def test_initial_state_iterations_is_zero(self):
        """Deve sempre iniciar com iterations = 0."""
        state = create_initial_state("Qualquer hipótese")

        assert state["iterations"] == 0
