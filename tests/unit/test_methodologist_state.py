"""
Testes unitários para o estado do agente Metodologista.

Valida a criação e inicialização correta do MethodologistState.
"""

import pytest
from agents.methodologist import MethodologistState, create_initial_state


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

    def test_initial_state_has_correct_types(self):
        """Deve criar estado com tipos corretos."""
        state = create_initial_state("Hipótese teste")

        # Validar tipos
        assert isinstance(state["hypothesis"], str)
        assert isinstance(state["messages"], list)
        assert isinstance(state["clarifications"], dict)
        assert isinstance(state["status"], str)
        assert isinstance(state["iterations"], int)
        assert isinstance(state["max_iterations"], int)

    def test_initial_state_status_is_pending(self):
        """Deve sempre iniciar com status 'pending'."""
        state = create_initial_state("Qualquer hipótese")

        assert state["status"] == "pending"

    def test_initial_state_iterations_is_zero(self):
        """Deve sempre iniciar com iterations = 0."""
        state = create_initial_state("Qualquer hipótese")

        assert state["iterations"] == 0

    def test_state_structure_matches_typeddict(self):
        """Deve criar estado com todos os campos do TypedDict."""
        state = create_initial_state("Teste")

        # Validar que todos os campos obrigatórios estão presentes
        required_fields = {
            "hypothesis",
            "messages",
            "clarifications",
            "status",
            "iterations",
            "max_iterations"
        }

        assert set(state.keys()) == required_fields
