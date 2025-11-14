"""
Testes unitários para o Orquestrador Conversacional (Épico 7 POC).

Testa os componentes do Épico 7, Task 7.1:
- orchestrator_node: Nó conversacional que explora, analisa e sugere
- route_from_orchestrator: Router baseado em next_step e agent_suggestion
- _build_context: Construção de contexto com histórico completo

Estes testes usam MOCKS para a API da Anthropic (rápidos, sem custo).

Versão: 1.0 (Épico 7 POC)
Data: 14/11/2025
"""

import pytest
from unittest.mock import Mock, patch
from langchain_core.messages import AIMessage, HumanMessage

from agents.orchestrator.state import MultiAgentState, create_initial_multi_agent_state
from agents.orchestrator.nodes import orchestrator_node, _build_context
from agents.orchestrator.router import route_from_orchestrator


class TestBuildContext:
    """Testes para a função _build_context (Task 7.1.3)."""

    def test_build_context_with_empty_history(self):
        """Testa construção de contexto com histórico vazio."""
        # Arrange
        state = create_initial_multi_agent_state(
            user_input="Observei que LLMs aumentam produtividade",
            session_id="test-session-1"
        )

        # Act
        context = _build_context(state)

        # Assert
        assert "INPUT INICIAL DO USUÁRIO:" in context
        assert "Observei que LLMs aumentam produtividade" in context
        assert "HISTÓRICO DA CONVERSA:" not in context  # Sem histórico

    def test_build_context_with_conversation_history(self):
        """Testa construção de contexto com histórico de mensagens."""
        # Arrange
        state = create_initial_multi_agent_state(
            user_input="Observei que LLMs aumentam produtividade",
            session_id="test-session-1"
        )
        # Adicionar mensagens ao histórico
        state["messages"] = [
            HumanMessage(content="Quero validar essa observação"),
            AIMessage(content="Entendi. Posso chamar o Estruturador?"),
            HumanMessage(content="Sim, pode chamar")
        ]

        # Act
        context = _build_context(state)

        # Assert
        assert "INPUT INICIAL DO USUÁRIO:" in context
        assert "Observei que LLMs aumentam produtividade" in context
        assert "HISTÓRICO DA CONVERSA:" in context
        assert "[Usuário]: Quero validar essa observação" in context
        assert "[Assistente]: Entendi. Posso chamar o Estruturador?" in context
        assert "[Usuário]: Sim, pode chamar" in context


class TestOrchestratorNodeConversational:
    """Testes para o nó orchestrator_node conversacional (Épico 7 POC)."""

    def test_exploration_initial_vague_input(self):
        """Testa exploração inicial com input vago (perguntas abertas)."""
        # Arrange
        state = create_initial_multi_agent_state(
            user_input="Observei que LLMs aumentam produtividade",
            session_id="test-session-1"
        )

        # Mock da resposta do LLM (next_step = "explore")
        mock_response = Mock()
        mock_response.content = '''
{
  "reasoning": "Usuário tem observação mas não especificou contexto, métricas ou população. Preciso explorar intenção.",
  "next_step": "explore",
  "message": "Interessante observação! Onde você observou isso? Como você mediu produtividade?",
  "agent_suggestion": null
}
'''
        mock_response.usage_metadata = {"input_tokens": 100, "output_tokens": 50}

        # Act
        with patch('agents.orchestrator.nodes.ChatAnthropic') as mock_llm_class:
            mock_llm = Mock()
            mock_llm.invoke.return_value = mock_response
            mock_llm_class.return_value = mock_llm

            result = orchestrator_node(state)

        # Assert
        assert result['next_step'] == "explore"
        assert result['orchestrator_analysis'].startswith("Usuário tem observação")
        assert result['agent_suggestion'] is None
        assert len(result['messages']) == 1
        assert isinstance(result['messages'][0], AIMessage)
        assert "Interessante observação" in result['messages'][0].content

    def test_suggestion_with_context(self):
        """Testa sugestão de agente quando contexto está claro."""
        # Arrange
        state = create_initial_multi_agent_state(
            user_input="Observei que LLMs aumentam produtividade",
            session_id="test-session-1"
        )
        state["messages"] = [
            HumanMessage(content="Na minha equipe, usando Claude Code, tarefas de 2h agora levam 30min"),
            AIMessage(content="Você quer validar ou entender literatura?"),
            HumanMessage(content="Quero validar como hipótese")
        ]

        # Mock da resposta do LLM (next_step = "suggest_agent")
        mock_response = Mock()
        mock_response.content = '''
{
  "reasoning": "Usuário escolheu validar. Tem observação concreta mas não estruturada como questão. Estruturador é ideal.",
  "next_step": "suggest_agent",
  "message": "Posso chamar o Estruturador para transformar sua observação em questão de pesquisa estruturada?",
  "agent_suggestion": {
    "agent": "structurer",
    "justification": "Observação concreta existe mas não está estruturada como questão PICO/SPIDER"
  }
}
'''
        mock_response.usage_metadata = {"input_tokens": 200, "output_tokens": 80}

        # Act
        with patch('agents.orchestrator.nodes.ChatAnthropic') as mock_llm_class:
            mock_llm = Mock()
            mock_llm.invoke.return_value = mock_response
            mock_llm_class.return_value = mock_llm

            result = orchestrator_node(state)

        # Assert
        assert result['next_step'] == "suggest_agent"
        assert result['agent_suggestion'] is not None
        assert result['agent_suggestion']['agent'] == "structurer"
        assert "PICO/SPIDER" in result['agent_suggestion']['justification']
        assert "Estruturador" in result['messages'][0].content

    def test_clarification_on_ambiguity(self):
        """Testa clarificação quando input é ambíguo."""
        # Arrange
        state = create_initial_multi_agent_state(
            user_input="Quero estudar LLMs",
            session_id="test-session-1"
        )

        # Mock da resposta do LLM (next_step = "clarify")
        mock_response = Mock()
        mock_response.content = '''
{
  "reasoning": "Input muito vago. Pode significar revisar literatura, testar hipótese ou desenvolver método. Preciso clarificar intenção.",
  "next_step": "clarify",
  "message": "Entender o que já existe (literatura)? Testar uma observação? Ou desenvolver algo novo?",
  "agent_suggestion": null
}
'''
        mock_response.usage_metadata = {"input_tokens": 80, "output_tokens": 40}

        # Act
        with patch('agents.orchestrator.nodes.ChatAnthropic') as mock_llm_class:
            mock_llm = Mock()
            mock_llm.invoke.return_value = mock_response
            mock_llm_class.return_value = mock_llm

            result = orchestrator_node(state)

        # Assert
        assert result['next_step'] == "clarify"
        assert result['agent_suggestion'] is None
        assert "Entender o que já existe" in result['messages'][0].content

    def test_fallback_on_invalid_json(self):
        """Testa fallback quando LLM retorna JSON inválido."""
        # Arrange
        state = create_initial_multi_agent_state(
            user_input="Teste",
            session_id="test-session-1"
        )

        # Mock da resposta do LLM (JSON inválido)
        mock_response = Mock()
        mock_response.content = "Resposta sem JSON válido"
        mock_response.usage_metadata = {"input_tokens": 50, "output_tokens": 10}

        # Act
        with patch('agents.orchestrator.nodes.ChatAnthropic') as mock_llm_class:
            mock_llm = Mock()
            mock_llm.invoke.return_value = mock_response
            mock_llm_class.return_value = mock_llm

            result = orchestrator_node(state)

        # Assert - deve fazer fallback seguro
        assert result['next_step'] == "explore"
        assert "dificuldade em processar" in result['messages'][0].content
        assert result['agent_suggestion'] is None


class TestRouterConversational:
    """Testes para o router conversacional (Task 7.1.6)."""

    def test_route_explore_returns_user(self):
        """Testa roteamento quando next_step = explore (retorna para usuário)."""
        # Arrange
        state = create_initial_multi_agent_state(
            user_input="Teste",
            session_id="test-session-1"
        )
        state['next_step'] = "explore"
        state['agent_suggestion'] = None

        # Act
        destination = route_from_orchestrator(state)

        # Assert
        assert destination == "user"

    def test_route_clarify_returns_user(self):
        """Testa roteamento quando next_step = clarify (retorna para usuário)."""
        # Arrange
        state = create_initial_multi_agent_state(
            user_input="Teste",
            session_id="test-session-1"
        )
        state['next_step'] = "clarify"
        state['agent_suggestion'] = None

        # Act
        destination = route_from_orchestrator(state)

        # Assert
        assert destination == "user"

    def test_route_suggest_agent_structurer(self):
        """Testa roteamento quando agente sugerido é structurer."""
        # Arrange
        state = create_initial_multi_agent_state(
            user_input="Teste",
            session_id="test-session-1"
        )
        state['next_step'] = "suggest_agent"
        state['agent_suggestion'] = {
            "agent": "structurer",
            "justification": "Observação não estruturada"
        }

        # Act
        destination = route_from_orchestrator(state)

        # Assert
        assert destination == "structurer"

    def test_route_suggest_agent_methodologist(self):
        """Testa roteamento quando agente sugerido é methodologist."""
        # Arrange
        state = create_initial_multi_agent_state(
            user_input="Teste",
            session_id="test-session-1"
        )
        state['next_step'] = "suggest_agent"
        state['agent_suggestion'] = {
            "agent": "methodologist",
            "justification": "Hipótese pronta para validação"
        }

        # Act
        destination = route_from_orchestrator(state)

        # Assert
        assert destination == "methodologist"

    def test_route_suggest_agent_invalid_returns_user(self):
        """Testa roteamento quando agente sugerido é inválido (fallback para user)."""
        # Arrange
        state = create_initial_multi_agent_state(
            user_input="Teste",
            session_id="test-session-1"
        )
        state['next_step'] = "suggest_agent"
        state['agent_suggestion'] = {
            "agent": "invalid_agent",
            "justification": "Teste"
        }

        # Act
        destination = route_from_orchestrator(state)

        # Assert
        assert destination == "user"  # Fallback seguro

    def test_route_suggest_agent_no_suggestion_returns_user(self):
        """Testa roteamento quando next_step=suggest_agent mas suggestion está vazia."""
        # Arrange
        state = create_initial_multi_agent_state(
            user_input="Teste",
            session_id="test-session-1"
        )
        state['next_step'] = "suggest_agent"
        state['agent_suggestion'] = None  # Inconsistência

        # Act
        destination = route_from_orchestrator(state)

        # Assert
        assert destination == "user"  # Fallback seguro

    def test_route_raises_error_on_none_next_step(self):
        """Testa que router lança erro se next_step for None."""
        # Arrange
        state = create_initial_multi_agent_state(
            user_input="Teste",
            session_id="test-session-1"
        )
        state['next_step'] = None  # Estado inválido

        # Act & Assert
        with pytest.raises(ValueError, match="next_step do Orquestrador está None"):
            route_from_orchestrator(state)

    def test_route_raises_error_on_invalid_next_step(self):
        """Testa que router lança erro se next_step for inválido."""
        # Arrange
        state = create_initial_multi_agent_state(
            user_input="Teste",
            session_id="test-session-1"
        )
        state['next_step'] = "invalid_step"  # Estado inválido

        # Act & Assert
        with pytest.raises(ValueError, match="next_step inválido"):
            route_from_orchestrator(state)
