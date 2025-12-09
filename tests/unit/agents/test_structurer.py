"""
Testes unitários para o agente Estruturador.

Testa os componentes do Épico 3, Funcionalidade 3.2:
- structurer_node: Nó que organiza ideias vagas em questões estruturadas

Estes testes usam MOCKS para a API da Anthropic (rápidos, sem custo).

Versão: 1.1
Data: 09/12/2025
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from langchain_core.messages import AIMessage

from agents.orchestrator.state import MultiAgentState, create_initial_multi_agent_state
from agents.structurer.nodes import structurer_node


def create_mock_llm_response(content):
    """Helper para criar mock response do LLM."""
    mock_response = Mock()
    mock_response.content = content
    return mock_response


class TestStructurerNode:
    """Testes para o nó structurer_node."""

    def test_structures_vague_observation(self):
        """Testa estruturação de observação vaga básica."""
        # Arrange
        state = create_initial_multi_agent_state(
            user_input="Observei que desenvolver com Claude Code é mais rápido",
            session_id="test-session-1",
        )

        mock_response = create_mock_llm_response('''{
            "context": "Desenvolvimento de software com IA",
            "problem": "Falta de métodos para medir produtividade com ferramentas de IA",
            "contribution": "Método para avaliar eficácia de ferramentas de IA no desenvolvimento",
            "structured_question": "Como ferramentas de IA como Claude Code impactam a produtividade no desenvolvimento de software?"
        }''')

        # Act - Mock do create_anthropic_client
        with patch('agents.structurer.nodes.create_anthropic_client') as mock_create_client:
            mock_llm_instance = MagicMock()
            mock_llm_instance.invoke.return_value = mock_response
            mock_create_client.return_value = mock_llm_instance

            result = structurer_node(state)

        # Assert
        assert 'structurer_output' in result
        output = result['structurer_output']

        # Verificar estrutura do output
        assert 'structured_question' in output
        assert 'elements' in output
        assert 'context' in output['elements']
        assert 'problem' in output['elements']
        assert 'contribution' in output['elements']

        # Verificar conteúdo
        assert output['elements']['context'] == "Desenvolvimento de software com IA"
        assert "produtividade" in output['elements']['problem'].lower()
        assert "Claude Code" in output['structured_question']

        # Verificar transição de estado
        assert result['current_stage'] == "validating"
        assert len(result['messages']) == 1
        assert isinstance(result['messages'][0], AIMessage)

    def test_extracts_all_elements(self):
        """Testa que todos os elementos são extraídos corretamente."""
        # Arrange
        state = create_initial_multi_agent_state(
            user_input="Notei que alunos se engajam mais em aulas interativas",
            session_id="test-session-1",
        )

        mock_response = create_mock_llm_response('''{
            "context": "Educação online",
            "problem": "Baixo engajamento em aulas tradicionais",
            "contribution": "Framework de design instrucional para aulas interativas",
            "structured_question": "Qual o impacto de elementos interativos no engajamento de alunos em educação online?"
        }''')

        # Act
        with patch('agents.structurer.nodes.create_anthropic_client') as mock_create_client:
            mock_llm_instance = MagicMock()
            mock_llm_instance.invoke.return_value = mock_response
            mock_create_client.return_value = mock_llm_instance

            result = structurer_node(state)

        # Assert
        output = result['structurer_output']
        assert output['elements']['context'] == "Educação online"
        assert output['elements']['problem'] == "Baixo engajamento em aulas tradicionais"
        assert output['elements']['contribution'] == "Framework de design instrucional para aulas interativas"
        assert "interativos" in output['structured_question'].lower()

    def test_handles_malformed_json(self):
        """Testa que nó lida graciosamente com JSON malformado."""
        # Arrange
        state = create_initial_multi_agent_state(
            user_input="Teste de observação",
            session_id="test-session-1",
        )

        mock_response = create_mock_llm_response("Resposta sem JSON válido")

        # Act
        with patch('agents.structurer.nodes.create_anthropic_client') as mock_create_client:
            mock_llm_instance = MagicMock()
            mock_llm_instance.invoke.return_value = mock_response
            mock_create_client.return_value = mock_llm_instance

            result = structurer_node(state)

        # Assert - Deve ter valores padrão em caso de erro
        assert 'structurer_output' in result
        output = result['structurer_output']

        # Deve ter estrutura mínima mesmo com erro
        assert 'structured_question' in output
        assert 'elements' in output
        assert output['elements']['context'] is not None
        assert output['elements']['problem'] is not None
        assert output['elements']['contribution'] is not None

    def test_handles_partial_json(self):
        """Testa que nó lida com JSON parcial (alguns campos faltando)."""
        # Arrange
        state = create_initial_multi_agent_state(
            user_input="Observação parcial",
            session_id="test-session-1",
        )

        mock_response = create_mock_llm_response('''{
            "context": "Contexto identificado",
            "structured_question": "Questão estruturada?"
        }''')

        # Act
        with patch('agents.structurer.nodes.create_anthropic_client') as mock_create_client:
            mock_llm_instance = MagicMock()
            mock_llm_instance.invoke.return_value = mock_response
            mock_create_client.return_value = mock_llm_instance

            result = structurer_node(state)

        # Assert - Deve preencher campos faltantes com valores padrão
        output = result['structurer_output']
        assert output['elements']['context'] == "Contexto identificado"
        assert output['structured_question'] == "Questão estruturada?"

        # Campos faltantes devem ter valores padrão
        assert output['elements']['problem'] is not None
        assert output['elements']['contribution'] is not None

    def test_updates_state_correctly(self):
        """Testa que nó atualiza o estado corretamente."""
        # Arrange
        state = create_initial_multi_agent_state(
            user_input="Teste",
            session_id="test-session-1",
        )

        mock_response = create_mock_llm_response('''{
            "context": "Teste contexto",
            "problem": "Teste problema",
            "contribution": "Teste contribuição",
            "structured_question": "Teste questão?"
        }''')

        # Act
        with patch('agents.structurer.nodes.create_anthropic_client') as mock_create_client:
            mock_llm_instance = MagicMock()
            mock_llm_instance.invoke.return_value = mock_response
            mock_create_client.return_value = mock_llm_instance

            result = structurer_node(state)

        # Assert
        assert result['current_stage'] == "validating"
        assert 'structurer_output' in result
        assert 'messages' in result
        assert len(result['messages']) == 1

    def test_adds_message_to_state(self):
        """Testa que o nó adiciona mensagem ao histórico."""
        # Arrange
        state = create_initial_multi_agent_state(
            user_input="Teste",
            session_id="test-session-1",
        )

        mock_response = create_mock_llm_response('''{
            "context": "Ctx",
            "problem": "Prb",
            "contribution": "Cnt",
            "structured_question": "Questão?"
        }''')

        # Act
        with patch('agents.structurer.nodes.create_anthropic_client') as mock_create_client:
            mock_llm_instance = MagicMock()
            mock_llm_instance.invoke.return_value = mock_response
            mock_create_client.return_value = mock_llm_instance

            result = structurer_node(state)

        # Assert
        assert 'messages' in result
        assert len(result['messages']) == 1
        assert isinstance(result['messages'][0], AIMessage)

        # Mensagem deve conter informações estruturadas
        message_content = result['messages'][0].content
        assert "Questão estruturada:" in message_content
        assert "Contexto:" in message_content
        assert "Problema:" in message_content
        assert "Contribuição potencial:" in message_content

    def test_is_collaborative_not_rejecting(self):
        """Testa que o nó é colaborativo e não rejeita ideias."""
        # Arrange - Input muito vago
        state = create_initial_multi_agent_state(
            user_input="Coisas são interessantes",
            session_id="test-session-1",
        )

        # Mock - LLM deve tentar estruturar mesmo input vago
        mock_response = create_mock_llm_response('''{
            "context": "Observação geral",
            "problem": "Falta especificidade na observação",
            "contribution": "Exploração de padrões interessantes",
            "structured_question": "Quais aspectos das 'coisas' são considerados interessantes e por quê?"
        }''')

        # Act
        with patch('agents.structurer.nodes.create_anthropic_client') as mock_create_client:
            mock_llm_instance = MagicMock()
            mock_llm_instance.invoke.return_value = mock_response
            mock_create_client.return_value = mock_llm_instance

            result = structurer_node(state)

        # Assert - Deve ter estruturado, não rejeitado
        output = result['structurer_output']
        assert output['structured_question'] is not None
        assert len(output['structured_question']) > 0

        # Não deve ter palavras como "rejeitado", "inválido", etc.
        message_content = result['messages'][0].content.lower()
        assert "rejeita" not in message_content
        assert "inválid" not in message_content
        assert "não é possível" not in message_content

    def test_structured_question_format(self):
        """Testa que a questão estruturada tem formato apropriado."""
        # Arrange
        state = create_initial_multi_agent_state(
            user_input="Método X funciona melhor",
            session_id="test-session-1",
        )

        mock_response = create_mock_llm_response('''{
            "context": "Metodologias de trabalho",
            "problem": "Comparação de eficácia entre métodos",
            "contribution": "Critérios para seleção de métodos",
            "structured_question": "Em que contextos o Método X demonstra maior eficácia comparado a alternativas?"
        }''')

        # Act
        with patch('agents.structurer.nodes.create_anthropic_client') as mock_create_client:
            mock_llm_instance = MagicMock()
            mock_llm_instance.invoke.return_value = mock_response
            mock_create_client.return_value = mock_llm_instance

            result = structurer_node(state)

        # Assert
        question = result['structurer_output']['structured_question']

        # Questão deve ser não-vazia e ter comprimento razoável
        assert len(question) > 10

        # Questão deve ser diferente do input original
        assert question != state['user_input']

        # Deve parecer uma questão (termina com ?)
        assert "?" in question or question.endswith("?")
