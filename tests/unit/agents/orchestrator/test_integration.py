"""
Testes de integração para funcionalidades avançadas do Orquestrador.

Cobre:
- Integração com active_idea_id do config
- Criação automática de snapshots
- Tratamento de falhas silenciosas

IMPORTANTE:
- orchestrator_node() agora chama _consult_observer() que faz chamadas LLM
- Testes DEVEM mockar _consult_observer para evitar dependência de API key
- Sem mock, fallback retorna needs_checkpoint=True, mudando next_step para "clarify"
"""

import pytest
from unittest.mock import Mock, patch
from core.agents.orchestrator.state import create_initial_multi_agent_state
from core.agents.orchestrator.nodes import orchestrator_node

# Fixture para mock padrão do Observer
# Retorna resultado neutro que não interfere no fluxo normal do teste
MOCK_OBSERVER_RESULT = {
    "clarity_evaluation": None,
    "variation_analysis": None,
    "needs_checkpoint": False,
    "checkpoint_reason": None
}

@pytest.fixture(autouse=True)
def mock_consult_observer():
    """Mock automático de _consult_observer para todos os testes deste módulo.

    orchestrator_node() agora consulta o Observer para análise
    de clareza e variação. Sem mock, testes falham no CI (sem API key).
    """
    with patch('agents.orchestrator.nodes._consult_observer') as mock:
        mock.return_value = MOCK_OBSERVER_RESULT
        yield mock

class TestActiveIdeaIdFromConfig:
    """Testes para extração de active_idea_id do config."""

    def test_orchestrator_works_without_active_idea_id(self):
        """orchestrator_node funciona sem active_idea_id no config."""
        state = create_initial_multi_agent_state(
            user_input="LLMs aumentam produtividade",
            session_id="test-session"
        )

        mock_response = Mock()
        mock_response.content = """
{
  "reasoning": "Teste",
  "next_step": "explore",
  "message": "Interessante!",
  "focal_argument": {
    "intent": "unclear",
    "subject": "LLMs productivity",
    "population": "not specified",
    "metrics": "not specified",
    "article_type": "unclear"
  },
  "cognitive_model": {
    "claim": "LLMs aumentam produtividade",
    "proposicoes": [],
    "open_questions": [],
    "contradictions": [],
    "solid_grounds": [],
    "context": {}
  },
  "agent_suggestion": null
}
"""
        mock_response.response_metadata = {"usage_metadata": {"input_tokens": 100, "output_tokens": 50}}

        # Config SEM active_idea_id
        config = {"configurable": {"thread_id": "test-thread"}}

        with patch('agents.orchestrator.nodes.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response

            # Não deve lançar exceção
            result = orchestrator_node(state, config=config)

        assert result["next_step"] == "explore"

    def test_orchestrator_works_with_active_idea_id(self):
        """orchestrator_node funciona com active_idea_id no config."""
        state = create_initial_multi_agent_state(
            user_input="LLMs aumentam produtividade",
            session_id="test-session"
        )

        mock_response = Mock()
        mock_response.content = """
{
  "reasoning": "Teste",
  "next_step": "explore",
  "message": "Interessante!",
  "focal_argument": {
    "intent": "unclear",
    "subject": "LLMs productivity",
    "population": "not specified",
    "metrics": "not specified",
    "article_type": "unclear"
  },
  "cognitive_model": {
    "claim": "LLMs aumentam produtividade",
    "proposicoes": [],
    "open_questions": [],
    "contradictions": [],
    "solid_grounds": [],
    "context": {}
  },
  "agent_suggestion": null
}
"""
        mock_response.response_metadata = {"usage_metadata": {"input_tokens": 100, "output_tokens": 50}}

        # Config COM active_idea_id
        config = {
            "configurable": {
                "thread_id": "test-thread",
                "active_idea_id": "idea-uuid-12345678"
            }
        }

        with patch('agents.orchestrator.nodes.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response

            result = orchestrator_node(state, config=config)

        assert result["next_step"] == "explore"

    def test_orchestrator_works_with_none_active_idea_id(self):
        """orchestrator_node funciona com active_idea_id=None no config."""
        state = create_initial_multi_agent_state(
            user_input="LLMs aumentam produtividade",
            session_id="test-session"
        )

        mock_response = Mock()
        mock_response.content = """
{
  "reasoning": "Teste",
  "next_step": "explore",
  "message": "Interessante!",
  "focal_argument": {
    "intent": "unclear",
    "subject": "LLMs productivity",
    "population": "not specified",
    "metrics": "not specified",
    "article_type": "unclear"
  },
  "cognitive_model": {
    "claim": "LLMs aumentam produtividade",
    "proposicoes": [],
    "open_questions": [],
    "contradictions": [],
    "solid_grounds": [],
    "context": {}
  },
  "agent_suggestion": null
}
"""
        mock_response.response_metadata = {"usage_metadata": {"input_tokens": 100, "output_tokens": 50}}

        # Config COM active_idea_id=None (padrão CLI)
        config = {
            "configurable": {
                "thread_id": "test-thread",
                "active_idea_id": None
            }
        }

        with patch('agents.orchestrator.nodes.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response

            result = orchestrator_node(state, config=config)

        assert result["next_step"] == "explore"

class TestSnapshotCreation:
    """Testes para criação automática de snapshot quando argumento amadurece."""

    def test_snapshot_called_when_active_idea_and_cognitive_model(self):
        """create_snapshot_if_mature é chamado quando há active_idea_id e cognitive_model."""
        state = create_initial_multi_agent_state(
            user_input="LLMs aumentam produtividade",
            session_id="test-session"
        )

        mock_response = Mock()
        mock_response.content = """
{
  "reasoning": "Teste",
  "next_step": "explore",
  "message": "Interessante!",
  "focal_argument": {
    "intent": "unclear",
    "subject": "LLMs productivity",
    "population": "not specified",
    "metrics": "not specified",
    "article_type": "unclear"
  },
  "cognitive_model": {
    "claim": "LLMs aumentam produtividade",
    "proposicoes": [
      {"texto": "Premissa 1", "solidez": null},
      {"texto": "Premissa 2", "solidez": null}
    ],
    "open_questions": [],
    "contradictions": [],
    "solid_grounds": [],
    "context": {"domain": "software"}
  },
  "agent_suggestion": null
}
"""
        mock_response.response_metadata = {"usage_metadata": {"input_tokens": 100, "output_tokens": 50}}

        config = {
            "configurable": {
                "thread_id": "test-thread",
                "active_idea_id": "idea-uuid-12345678"
            }
        }

        with patch('agents.orchestrator.nodes.invoke_with_retry') as mock_invoke, \
             patch('agents.orchestrator.nodes.create_snapshot_if_mature') as mock_snapshot:
            mock_invoke.return_value = mock_response
            mock_snapshot.return_value = None  # Argumento não maduro

            result = orchestrator_node(state, config=config)

            # Verifica que create_snapshot_if_mature foi chamado
            mock_snapshot.assert_called_once()
            call_args = mock_snapshot.call_args
            assert call_args.kwargs["idea_id"] == "idea-uuid-12345678"
            assert call_args.kwargs["confidence_threshold"] == 0.8

        assert result["next_step"] == "explore"

    def test_snapshot_not_called_without_active_idea_id(self):
        """create_snapshot_if_mature NÃO é chamado sem active_idea_id."""
        state = create_initial_multi_agent_state(
            user_input="LLMs aumentam produtividade",
            session_id="test-session"
        )

        mock_response = Mock()
        mock_response.content = """
{
  "reasoning": "Teste",
  "next_step": "explore",
  "message": "Interessante!",
  "focal_argument": {
    "intent": "unclear",
    "subject": "LLMs",
    "population": "not specified",
    "metrics": "not specified",
    "article_type": "unclear"
  },
  "cognitive_model": {
    "claim": "LLMs aumentam produtividade",
    "proposicoes": [],
    "open_questions": [],
    "contradictions": [],
    "solid_grounds": [],
    "context": {}
  },
  "agent_suggestion": null
}
"""
        mock_response.response_metadata = {"usage_metadata": {"input_tokens": 100, "output_tokens": 50}}

        # Config SEM active_idea_id
        config = {"configurable": {"thread_id": "test-thread"}}

        with patch('agents.orchestrator.nodes.invoke_with_retry') as mock_invoke, \
             patch('agents.orchestrator.nodes.create_snapshot_if_mature') as mock_snapshot:
            mock_invoke.return_value = mock_response

            result = orchestrator_node(state, config=config)

            # create_snapshot_if_mature NÃO deve ser chamado
            mock_snapshot.assert_not_called()

        assert result["next_step"] == "explore"

    def test_snapshot_failure_does_not_break_orchestrator(self):
        """Falha no snapshot não interrompe o orchestrator (silencioso)."""
        state = create_initial_multi_agent_state(
            user_input="LLMs aumentam produtividade",
            session_id="test-session"
        )

        mock_response = Mock()
        mock_response.content = """
{
  "reasoning": "Teste",
  "next_step": "explore",
  "message": "Interessante!",
  "focal_argument": {
    "intent": "unclear",
    "subject": "LLMs",
    "population": "not specified",
    "metrics": "not specified",
    "article_type": "unclear"
  },
  "cognitive_model": {
    "claim": "LLMs aumentam produtividade",
    "proposicoes": [],
    "open_questions": [],
    "contradictions": [],
    "solid_grounds": [],
    "context": {}
  },
  "agent_suggestion": null
}
"""
        mock_response.response_metadata = {"usage_metadata": {"input_tokens": 100, "output_tokens": 50}}

        config = {
            "configurable": {
                "thread_id": "test-thread",
                "active_idea_id": "idea-uuid-12345678"
            }
        }

        with patch('agents.orchestrator.nodes.invoke_with_retry') as mock_invoke, \
             patch('agents.orchestrator.nodes.create_snapshot_if_mature') as mock_snapshot:
            mock_invoke.return_value = mock_response
            # Simula falha no snapshot
            mock_snapshot.side_effect = Exception("Database error")

            # Não deve lançar exceção - falha silenciosa
            result = orchestrator_node(state, config=config)

        # Orchestrator continua funcionando normalmente
        assert result["next_step"] == "explore"
        assert "cognitive_model" in result
