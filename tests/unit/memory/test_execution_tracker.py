"""
Testes unitários para ExecutionTracker (Épico 6.2).

Valida captura de tokens de AIMessage e registro no MemoryManager.

"""

import pytest
from unittest.mock import Mock, patch
from agents.memory.execution_tracker import register_execution
from agents.memory.memory_manager import MemoryManager

class TestExecutionTracker:
    """Testes para a função register_execution."""

    def test_register_execution_with_valid_response(self):
        """Deve extrair tokens de AIMessage e registrar no MemoryManager."""
        # Arrange
        memory_manager = MemoryManager()
        session_id = "test-session"
        agent_name = "orchestrator"

        # Mock da AIMessage do LangChain com response_metadata
        mock_response = Mock()
        mock_response.response_metadata = {
            "usage": {
                "input_tokens": 150,
                "output_tokens": 75
            }
        }

        config = {
            "configurable": {
                "thread_id": session_id
            }
        }

        model_name = "claude-3-5-haiku-20241022"
        summary = "Classificação: vague"

        # Act
        with patch('agents.memory.execution_tracker.CostTracker.calculate_cost') as mock_cost:
            mock_cost.return_value = {
                "input_cost": 0.00012,
                "output_cost": 0.0003,
                "total_cost": 0.00042
            }

            execution = register_execution(
                memory_manager=memory_manager,
                config=config,
                agent_name=agent_name,
                response=mock_response,
                summary=summary,
                model_name=model_name
            )

        # Assert
        assert execution is not None
        assert execution.agent_name == agent_name
        assert execution.tokens_input == 150
        assert execution.tokens_output == 75
        assert execution.tokens_total == 225
        assert execution.summary == summary
        assert execution.metadata["model"] == model_name
        assert execution.metadata["cost_usd"] == 0.00042

        # Verificar que CostTracker foi chamado corretamente
        mock_cost.assert_called_once_with(
            model=model_name,
            input_tokens=150,
            output_tokens=75,
        )

        # Verificar que foi registrado no MemoryManager
        history = memory_manager.get_agent_history(session_id, agent_name)
        assert len(history) == 1
        assert history[0] == execution

    def test_register_execution_without_memory_manager(self):
        """Deve retornar None se memory_manager não for fornecido."""
        # Arrange
        mock_response = Mock()
        mock_response.response_metadata = {
            "usage": {
                "input_tokens": 100,
                "output_tokens": 50
            }
        }

        config = {"configurable": {"thread_id": "test"}}

        # Act
        execution = register_execution(
            memory_manager=None,
            config=config,
            agent_name="test_agent",
            response=mock_response,
            summary="Test",
            model_name="claude-3-5-haiku-20241022"
        )

        # Assert
        assert execution is None

    def test_register_execution_without_usage_metadata(self):
        """Deve usar zeros se response não tiver metadados de uso."""
        # Arrange
        memory_manager = MemoryManager()
        session_id = "test-session"

        # Mock de AIMessage sem usage metadata
        mock_response = Mock()
        mock_response.response_metadata = {}

        config = {"configurable": {"thread_id": session_id}}

        # Act
        with patch('agents.memory.execution_tracker.CostTracker.calculate_cost') as mock_cost:
            mock_cost.return_value = {
                "input_cost": 0.0,
                "output_cost": 0.0,
                "total_cost": 0.0
            }

            execution = register_execution(
                memory_manager=memory_manager,
                config=config,
                agent_name="test_agent",
                response=mock_response,
                summary="Test",
                model_name="claude-3-5-haiku-20241022"
            )

        # Assert
        assert execution is not None
        assert execution.tokens_input == 0
        assert execution.tokens_output == 0
        assert execution.tokens_total == 0

    def test_register_execution_with_usage_metadata_attribute(self):
        """Deve suportar usage_metadata como atributo (LangChain 0.3+)."""
        # Arrange
        memory_manager = MemoryManager()
        session_id = "test-session"

        # Mock com usage_metadata como atributo
        mock_response = Mock()
        mock_response.response_metadata = {}
        mock_response.usage_metadata = {
            "input_tokens": 200,
            "output_tokens": 100
        }

        config = {"configurable": {"thread_id": session_id}}

        # Act
        with patch('agents.memory.execution_tracker.CostTracker.calculate_cost') as mock_cost:
            mock_cost.return_value = {
                "input_cost": 0.00024,
                "output_cost": 0.0006,
                "total_cost": 0.00084
            }

            execution = register_execution(
                memory_manager=memory_manager,
                config=config,
                agent_name="test_agent",
                response=mock_response,
                summary="Test",
                model_name="claude-3-5-haiku-20241022"
            )

        # Assert
        assert execution is not None
        assert execution.tokens_input == 200
        assert execution.tokens_output == 100

    def test_register_execution_with_custom_metadata(self):
        """Deve permitir metadados adicionais personalizados."""
        # Arrange
        memory_manager = MemoryManager()
        session_id = "test-session"

        mock_response = Mock()
        mock_response.response_metadata = {
            "usage": {
                "input_tokens": 100,
                "output_tokens": 50
            }
        }

        config = {"configurable": {"thread_id": session_id}}

        custom_metadata = {
            "classification": "vague",
            "reasoning": "Input não possui estrutura clara"
        }

        # Act
        with patch('agents.memory.execution_tracker.CostTracker.calculate_cost') as mock_cost:
            mock_cost.return_value = {
                "input_cost": 0.0001,
                "output_cost": 0.0002,
                "total_cost": 0.0003
            }

            execution = register_execution(
                memory_manager=memory_manager,
                config=config,
                agent_name="orchestrator",
                response=mock_response,
                summary="Classificação: vague",
                model_name="claude-3-5-haiku-20241022",
                extra_metadata=custom_metadata
            )

        # Assert
        assert execution is not None
        assert execution.metadata["classification"] == "vague"
        assert execution.metadata["reasoning"] == "Input não possui estrutura clara"
        assert execution.metadata["model"] == "claude-3-5-haiku-20241022"
        assert execution.metadata["cost_usd"] == 0.0003
