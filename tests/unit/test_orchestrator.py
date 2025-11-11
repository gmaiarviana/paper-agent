"""
Testes unitários para o agente Orquestrador.

Testa os componentes do Épico 3, Funcionalidade 3.1:
- orchestrator_node: Nó que classifica maturidade do input
- route_from_orchestrator: Router que decide próximo agente

Estes testes usam MOCKS para a API da Anthropic (rápidos, sem custo).

Versão: 1.0
Data: 11/11/2025
"""

import pytest
from unittest.mock import Mock, patch
from langchain_core.messages import AIMessage

from agents.orchestrator.state import MultiAgentState, create_initial_multi_agent_state
from agents.orchestrator.nodes import orchestrator_node
from agents.orchestrator.router import route_from_orchestrator


class TestOrchestratorNode:
    """Testes para o nó orchestrator_node."""

    def test_classifies_vague_input(self):
        """Testa classificação de input vago (ideia não estruturada)."""
        # Arrange
        state = create_initial_multi_agent_state(
            user_input="Observei que desenvolver com Claude Code é mais rápido"
        )

        # Mock da resposta do LLM
        mock_response = Mock()
        mock_response.content = '{"classification": "vague", "reasoning": "Falta estruturação da ideia"}'

        # Act
        with patch('agents.orchestrator.nodes.ChatAnthropic') as mock_llm_class:
            mock_llm = Mock()
            mock_llm.invoke.return_value = mock_response
            mock_llm_class.return_value = mock_llm

            result = orchestrator_node(state)

        # Assert
        assert result['orchestrator_classification'] == "vague"
        assert result['orchestrator_reasoning'] == "Falta estruturação da ideia"
        assert result['current_stage'] == "structuring"
        assert len(result['messages']) == 1
        assert isinstance(result['messages'][0], AIMessage)

    def test_classifies_semi_formed_input(self):
        """Testa classificação de hipótese parcial (semi_formed)."""
        # Arrange
        state = create_initial_multi_agent_state(
            user_input="Método incremental melhora desenvolvimento multi-agente"
        )

        # Mock da resposta do LLM
        mock_response = Mock()
        mock_response.content = '{"classification": "semi_formed", "reasoning": "Tem ideia central mas falta especificidade"}'

        # Act
        with patch('agents.orchestrator.nodes.ChatAnthropic') as mock_llm_class:
            mock_llm = Mock()
            mock_llm.invoke.return_value = mock_response
            mock_llm_class.return_value = mock_llm

            result = orchestrator_node(state)

        # Assert
        assert result['orchestrator_classification'] == "semi_formed"
        assert result['orchestrator_reasoning'] == "Tem ideia central mas falta especificidade"
        assert result['current_stage'] == "validating"

    def test_classifies_complete_hypothesis(self):
        """Testa classificação de hipótese completa."""
        # Arrange
        state = create_initial_multi_agent_state(
            user_input=(
                "Método incremental reduz tempo de implementação de sistemas "
                "multi-agente em 30%, medido por sprints, em equipes de 2-5 devs"
            )
        )

        # Mock da resposta do LLM
        mock_response = Mock()
        mock_response.content = '{"classification": "complete", "reasoning": "Hipótese bem especificada com métricas"}'

        # Act
        with patch('agents.orchestrator.nodes.ChatAnthropic') as mock_llm_class:
            mock_llm = Mock()
            mock_llm.invoke.return_value = mock_response
            mock_llm_class.return_value = mock_llm

            result = orchestrator_node(state)

        # Assert
        assert result['orchestrator_classification'] == "complete"
        assert result['current_stage'] == "validating"

    def test_handles_malformed_json_gracefully(self):
        """Testa que nó lida graciosamente com JSON malformado do LLM."""
        # Arrange
        state = create_initial_multi_agent_state(user_input="Teste")

        # Mock com JSON inválido
        mock_response = Mock()
        mock_response.content = "Resposta sem JSON válido"

        # Act
        with patch('agents.orchestrator.nodes.ChatAnthropic') as mock_llm_class:
            mock_llm = Mock()
            mock_llm.invoke.return_value = mock_response
            mock_llm_class.return_value = mock_llm

            result = orchestrator_node(state)

        # Assert - Deve ter valor padrão em caso de erro
        assert result['orchestrator_classification'] in ["vague", "semi_formed", "complete"]
        assert result['orchestrator_reasoning'] is not None

    def test_adds_message_to_state(self):
        """Testa que o nó adiciona mensagem ao histórico."""
        # Arrange
        state = create_initial_multi_agent_state(user_input="Teste")

        # Mock
        mock_response = Mock()
        mock_response.content = '{"classification": "vague", "reasoning": "Teste"}'

        # Act
        with patch('agents.orchestrator.nodes.ChatAnthropic') as mock_llm_class:
            mock_llm = Mock()
            mock_llm.invoke.return_value = mock_response
            mock_llm_class.return_value = mock_llm

            result = orchestrator_node(state)

        # Assert
        assert 'messages' in result
        assert len(result['messages']) == 1
        assert isinstance(result['messages'][0], AIMessage)


class TestRouteFromOrchestrator:
    """Testes para a função de roteamento route_from_orchestrator."""

    def test_routes_vague_to_structurer(self):
        """Testa roteamento de input vago para Estruturador."""
        # Arrange
        state = create_initial_multi_agent_state(user_input="Teste")
        state['orchestrator_classification'] = "vague"

        # Act
        next_node = route_from_orchestrator(state)

        # Assert
        assert next_node == "structurer"

    def test_routes_semi_formed_to_methodologist(self):
        """Testa roteamento de hipótese semi_formed para Metodologista."""
        # Arrange
        state = create_initial_multi_agent_state(user_input="Teste")
        state['orchestrator_classification'] = "semi_formed"

        # Act
        next_node = route_from_orchestrator(state)

        # Assert
        assert next_node == "methodologist"

    def test_routes_complete_to_methodologist(self):
        """Testa roteamento de hipótese complete para Metodologista."""
        # Arrange
        state = create_initial_multi_agent_state(user_input="Teste")
        state['orchestrator_classification'] = "complete"

        # Act
        next_node = route_from_orchestrator(state)

        # Assert
        assert next_node == "methodologist"

    def test_handles_none_classification(self):
        """Testa que router lida com classificação None (erro no orchestrator)."""
        # Arrange
        state = create_initial_multi_agent_state(user_input="Teste")
        state['orchestrator_classification'] = None

        # Act & Assert - Deve ter valor padrão ou lançar exceção clara
        with pytest.raises(ValueError):
            route_from_orchestrator(state)

    def test_handles_invalid_classification(self):
        """Testa que router lida com classificação inválida."""
        # Arrange
        state = create_initial_multi_agent_state(user_input="Teste")
        state['orchestrator_classification'] = "invalid_value"

        # Act & Assert - Deve lançar exceção clara
        with pytest.raises(ValueError):
            route_from_orchestrator(state)


class TestMultiAgentState:
    """Testes para o estado MultiAgentState e função de criação."""

    def test_create_initial_state_has_required_fields(self):
        """Testa que estado inicial possui todos os campos obrigatórios."""
        # Arrange & Act
        state = create_initial_multi_agent_state(user_input="Teste de input")

        # Assert - Campos compartilhados
        assert state['user_input'] == "Teste de input"
        assert state['conversation_history'] == ["Usuário: Teste de input"]
        assert state['current_stage'] == "classifying"

        # Assert - Campos específicos (devem começar None)
        assert state['orchestrator_classification'] is None
        assert state['orchestrator_reasoning'] is None
        assert state['structurer_output'] is None
        assert state['methodologist_output'] is None

        # Assert - Mensagens
        assert state['messages'] == []

    def test_state_is_mutable(self):
        """Testa que campos do estado podem ser atualizados."""
        # Arrange
        state = create_initial_multi_agent_state(user_input="Teste")

        # Act
        state['orchestrator_classification'] = "vague"
        state['current_stage'] = "structuring"

        # Assert
        assert state['orchestrator_classification'] == "vague"
        assert state['current_stage'] == "structuring"
