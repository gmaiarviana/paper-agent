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
from langchain_core.messages import AIMessage, HumanMessage

from agents.orchestrator.state import MultiAgentState, create_initial_multi_agent_state
from agents.orchestrator.nodes import orchestrator_node, _build_context
from agents.orchestrator.router import route_from_orchestrator


class TestOrchestratorNode:
    """Testes para o nó orchestrator_node (versão conversacional MVP)."""

    def test_classifies_vague_input(self):
        """Testa que input vago leva a next_step = explore com análise preenchida."""
        # Arrange
        state = create_initial_multi_agent_state(
            user_input="Observei que desenvolver com Claude Code é mais rápido",
            session_id="test-session-1",
        )

        # Mock da resposta do LLM (next_step = "explore")
        mock_response = Mock()
        mock_response.content = """
{
  "reasoning": "Falta estruturação da ideia",
  "next_step": "explore",
  "message": "Interessante observação! Me conta um pouco mais sobre o contexto.",
  "agent_suggestion": null
}
"""

        # Act
        with patch('agents.orchestrator.nodes.ChatAnthropic') as mock_llm_class:
            mock_llm = Mock()
            mock_llm.invoke.return_value = mock_response
            mock_llm_class.return_value = mock_llm

            result = orchestrator_node(state)

        # Assert
        assert result["next_step"] == "explore"
        assert result["orchestrator_analysis"].startswith("Falta estruturação da ideia")
        assert len(result['messages']) == 1
        assert isinstance(result['messages'][0], AIMessage)

    def test_classifies_semi_formed_input(self):
        """Testa que hipótese semi-formada leva a sugestão de agente structurer."""
        # Arrange
        state = create_initial_multi_agent_state(
            user_input="Método incremental melhora desenvolvimento multi-agente",
            session_id="test-session-1",
        )

        # Mock da resposta do LLM (next_step = "suggest_agent" → structurer)
        mock_response = Mock()
        mock_response.content = """
{
  "reasoning": "Tem ideia central mas falta especificidade",
  "next_step": "suggest_agent",
  "message": "Posso chamar o Estruturador para transformar sua observação em questão de pesquisa?",
  "agent_suggestion": {
    "agent": "structurer",
    "justification": "Ideia concreta porém não estruturada como questão"
  }
}
"""

        # Act
        with patch('agents.orchestrator.nodes.ChatAnthropic') as mock_llm_class:
            mock_llm = Mock()
            mock_llm.invoke.return_value = mock_response
            mock_llm_class.return_value = mock_llm

            result = orchestrator_node(state)

        # Assert
        assert result["next_step"] == "suggest_agent"
        assert result["agent_suggestion"] is not None
        assert result["agent_suggestion"]["agent"] == "structurer"
        assert result["orchestrator_analysis"].startswith("Tem ideia central")

    def test_classifies_complete_hypothesis(self):
        """Testa que hipótese completa leva a sugestão de agente methodologist."""
        # Arrange
        state = create_initial_multi_agent_state(
            user_input=(
                "Método incremental reduz tempo de implementação de sistemas "
                "multi-agente em 30%, medido por sprints, em equipes de 2-5 devs"
            ),
            session_id="test-session-1",
        )

        # Mock da resposta do LLM (next_step = "suggest_agent" → methodologist)
        mock_response = Mock()
        mock_response.content = """
{
  "reasoning": "Hipótese bem especificada com métricas",
  "next_step": "suggest_agent",
  "message": "Sua hipótese já está bem formada. Posso chamar o Metodologista para validar?",
  "agent_suggestion": {
    "agent": "methodologist",
    "justification": "Hipótese completa, pronta para validação metodológica"
  }
}
"""

        # Act
        with patch('agents.orchestrator.nodes.ChatAnthropic') as mock_llm_class:
            mock_llm = Mock()
            mock_llm.invoke.return_value = mock_response
            mock_llm_class.return_value = mock_llm

            result = orchestrator_node(state)

        # Assert
        assert result["next_step"] == "suggest_agent"
        assert result["agent_suggestion"] is not None
        assert result["agent_suggestion"]["agent"] == "methodologist"
        assert result["orchestrator_analysis"].startswith("Hipótese bem especificada")

    def test_handles_malformed_json_gracefully(self):
        """Testa que nó lida graciosamente com JSON malformado do LLM (fallback)."""
        # Arrange
        state = create_initial_multi_agent_state(
            user_input="Teste",
            session_id="test-session-1",
        )

        # Mock com JSON inválido
        mock_response = Mock()
        mock_response.content = "Resposta sem JSON válido"

        # Act
        with patch('agents.orchestrator.nodes.ChatAnthropic') as mock_llm_class:
            mock_llm = Mock()
            mock_llm.invoke.return_value = mock_response
            mock_llm_class.return_value = mock_llm

            result = orchestrator_node(state)

        # Assert - Deve fazer fallback seguro em caso de erro
        assert result["next_step"] == "explore"
        assert result["orchestrator_analysis"] is not None
        assert "Erro ao processar resposta do orquestrador" in result["orchestrator_analysis"]

    def test_adds_message_to_state(self):
        """Testa que o nó adiciona mensagem ao histórico."""
        # Arrange
        state = create_initial_multi_agent_state(
            user_input="Teste",
            session_id="test-session-1",
        )

        # Mock (formato mínimo aceitável)
        mock_response = Mock()
        mock_response.content = """
{
  "reasoning": "Teste",
  "next_step": "explore",
  "message": "Mensagem de teste para o usuário",
  "agent_suggestion": null
}
"""

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
        """Testa roteamento quando agente sugerido é structurer."""
        # Arrange
        state = create_initial_multi_agent_state(
            user_input="Teste",
            session_id="test-session-1",
        )
        state["next_step"] = "suggest_agent"
        state["agent_suggestion"] = {
            "agent": "structurer",
            "justification": "Observação não estruturada"
        }

        # Act
        next_node = route_from_orchestrator(state)

        # Assert
        assert next_node == "structurer"

    def test_routes_semi_formed_to_methodologist(self):
        """Testa roteamento quando agente sugerido é methodologist (semi_formed)."""
        # Arrange
        state = create_initial_multi_agent_state(
            user_input="Teste",
            session_id="test-session-1",
        )
        state["next_step"] = "suggest_agent"
        state["agent_suggestion"] = {
            "agent": "methodologist",
            "justification": "Hipótese semi-formada pronta para validação"
        }

        # Act
        next_node = route_from_orchestrator(state)

        # Assert
        assert next_node == "methodologist"

    def test_routes_complete_to_methodologist(self):
        """Testa roteamento quando agente sugerido é methodologist (hipótese completa)."""
        # Arrange
        state = create_initial_multi_agent_state(
            user_input="Teste",
            session_id="test-session-1",
        )
        state["next_step"] = "suggest_agent"
        state["agent_suggestion"] = {
            "agent": "methodologist",
            "justification": "Hipótese completa pronta para validação"
        }

        # Act
        next_node = route_from_orchestrator(state)

        # Assert
        assert next_node == "methodologist"

    def test_handles_none_next_step(self):
        """Testa que router lida com next_step None (erro no orchestrator)."""
        # Arrange
        state = create_initial_multi_agent_state(
            user_input="Teste",
            session_id="test-session-1",
        )
        state["next_step"] = None

        # Act & Assert - Deve lançar exceção clara
        with pytest.raises(ValueError):
            route_from_orchestrator(state)

    def test_handles_invalid_next_step(self):
        """Testa que router lida com next_step inválido."""
        # Arrange
        state = create_initial_multi_agent_state(
            user_input="Teste",
            session_id="test-session-1",
        )
        state["next_step"] = "invalid_value"

        # Act & Assert - Deve lançar exceção clara
        with pytest.raises(ValueError):
            route_from_orchestrator(state)


class TestMultiAgentState:
    """Testes para o estado MultiAgentState e função de criação."""

    def test_create_initial_state_has_required_fields(self):
        """Testa que estado inicial possui todos os campos obrigatórios."""
        # Arrange & Act
        state = create_initial_multi_agent_state(
            user_input="Teste de input",
            session_id="test-session-1",
        )

        # Assert - Campos compartilhados
        assert state['user_input'] == "Teste de input"
        assert state['session_id'] == "test-session-1"
        assert state['conversation_history'] == ["Usuário: Teste de input"]
        assert state['current_stage'] == "classifying"
        assert state['hypothesis_versions'] == []

        # Assert - Campos específicos (devem começar None)
        assert state['orchestrator_analysis'] is None
        assert state['next_step'] is None
        assert state['agent_suggestion'] is None
        assert state['focal_argument'] is None
        assert state['reflection_prompt'] is None
        assert state['stage_suggestion'] is None
        assert state['structurer_output'] is None
        assert state['methodologist_output'] is None

        # Assert - Mensagens (fix Épico 14.5: deve ter 1 HumanMessage inicial)
        assert len(state['messages']) == 1
        from langchain_core.messages import HumanMessage
        assert isinstance(state['messages'][0], HumanMessage)
        assert state['messages'][0].content == "Teste de input"

    def test_state_is_mutable(self):
        """Testa que campos do estado podem ser atualizados."""
        # Arrange
        state = create_initial_multi_agent_state(
            user_input="Teste",
            session_id="test-session-1",
        )

        # Act
        state['next_step'] = "explore"
        state['current_stage'] = "structuring"

        # Assert
        assert state['next_step'] == "explore"
        assert state['current_stage'] == "structuring"


class TestBuildContext:
    """
    Testes para a função _build_context().

    Esta função helper reconstrói o "argumento focal" implícito da conversa
    analisando todo o histórico de mensagens (Épico 7, Tarefa 7.1.3).
    """

    def test_build_context_with_only_initial_input(self):
        """Testa construção de contexto com apenas input inicial.

        Após fix Épico 14.5, o estado inicial sempre tem 1 HumanMessage,
        então sempre haverá histórico (com a mensagem inicial).
        """
        # Arrange
        state = create_initial_multi_agent_state(
            user_input="Observei que LLMs aumentam produtividade",
            session_id="session-123"
        )

        # Act
        context = _build_context(state)

        # Assert
        assert "INPUT INICIAL DO USUÁRIO:" in context
        assert "Observei que LLMs aumentam produtividade" in context
        # Após fix Épico 14.5: histórico sempre existe (com mensagem inicial)
        assert "HISTÓRICO DA CONVERSA:" in context
        assert "[Usuário]: Observei que LLMs aumentam produtividade" in context

    def test_build_context_with_human_messages(self):
        """Testa construção de contexto com mensagens do usuário."""
        # Arrange
        state = create_initial_multi_agent_state(
            user_input="Observei que LLMs aumentam produtividade",
            session_id="session-123"
        )
        state['messages'] = [
            HumanMessage(content="Na minha equipe, usando Claude Code"),
            HumanMessage(content="Tarefas que levavam 2h agora levam 30min")
        ]

        # Act
        context = _build_context(state)

        # Assert
        assert "INPUT INICIAL DO USUÁRIO:" in context
        assert "Observei que LLMs aumentam produtividade" in context
        assert "HISTÓRICO DA CONVERSA:" in context
        assert "[Usuário]: Na minha equipe, usando Claude Code" in context
        assert "[Usuário]: Tarefas que levavam 2h agora levam 30min" in context

    def test_build_context_with_ai_messages(self):
        """Testa construção de contexto com mensagens do assistente."""
        # Arrange
        state = create_initial_multi_agent_state(
            user_input="Observei que LLMs aumentam produtividade",
            session_id="session-123"
        )
        state['messages'] = [
            AIMessage(content="Interessante! Me conta mais sobre isso."),
            AIMessage(content="Você mediu isso de alguma forma?")
        ]

        # Act
        context = _build_context(state)

        # Assert
        assert "HISTÓRICO DA CONVERSA:" in context
        assert "[Assistente]: Interessante! Me conta mais sobre isso." in context
        assert "[Assistente]: Você mediu isso de alguma forma?" in context

    def test_build_context_with_mixed_messages(self):
        """Testa construção de contexto com mix de mensagens (usuário + assistente)."""
        # Arrange
        state = create_initial_multi_agent_state(
            user_input="Observei que LLMs aumentam produtividade",
            session_id="session-123"
        )
        state['messages'] = [
            AIMessage(content="Interessante! Me conta mais."),
            HumanMessage(content="Vi na minha equipe, usando Claude Code"),
            AIMessage(content="Você mediu isso?"),
            HumanMessage(content="Tarefas que levavam 2h agora levam 30min")
        ]

        # Act
        context = _build_context(state)

        # Assert
        assert "INPUT INICIAL DO USUÁRIO:" in context
        assert "HISTÓRICO DA CONVERSA:" in context
        assert "[Assistente]: Interessante! Me conta mais." in context
        assert "[Usuário]: Vi na minha equipe, usando Claude Code" in context
        assert "[Assistente]: Você mediu isso?" in context
        assert "[Usuário]: Tarefas que levavam 2h agora levam 30min" in context

    def test_build_context_preserves_chronological_order(self):
        """Testa que contexto preserva ordem cronológica das mensagens."""
        # Arrange
        state = create_initial_multi_agent_state(
            user_input="Input inicial",
            session_id="session-123"
        )
        state['messages'] = [
            HumanMessage(content="Mensagem 1"),
            AIMessage(content="Resposta 1"),
            HumanMessage(content="Mensagem 2"),
            AIMessage(content="Resposta 2")
        ]

        # Act
        context = _build_context(state)
        lines = context.split("\n")

        # Assert - Ordem deve ser mantida
        msg1_idx = next(i for i, line in enumerate(lines) if "Mensagem 1" in line)
        resp1_idx = next(i for i, line in enumerate(lines) if "Resposta 1" in line)
        msg2_idx = next(i for i, line in enumerate(lines) if "Mensagem 2" in line)
        resp2_idx = next(i for i, line in enumerate(lines) if "Resposta 2" in line)

        assert msg1_idx < resp1_idx < msg2_idx < resp2_idx

    def test_build_context_format_is_llm_friendly(self):
        """Testa que formato do contexto é adequado para análise pelo LLM."""
        # Arrange
        state = create_initial_multi_agent_state(
            user_input="Observei X",
            session_id="session-123"
        )
        state['messages'] = [
            AIMessage(content="Pergunta aberta"),
            HumanMessage(content="Resposta do usuário")
        ]

        # Act
        context = _build_context(state)

        # Assert - Formato deve ter estrutura clara
        assert context.startswith("INPUT INICIAL DO USUÁRIO:")
        assert "\n\n" in context  # Linhas em branco para separação visual
        assert "[Usuário]:" in context  # Prefixos claros
        assert "[Assistente]:" in context

    def test_build_context_with_empty_messages_list(self):
        """Testa construção de contexto quando messages está vazio."""
        # Arrange
        state = create_initial_multi_agent_state(
            user_input="Input teste",
            session_id="session-123"
        )
        state['messages'] = []  # Lista vazia explícita

        # Act
        context = _build_context(state)

        # Assert
        assert "INPUT INICIAL DO USUÁRIO:" in context
        assert "Input teste" in context
        assert "HISTÓRICO DA CONVERSA:" not in context  # Não deve incluir seção vazia

    def test_build_context_detects_change_in_direction(self):
        """
        Testa que contexto construído permite detecção de mudança de direção.

        Este teste valida que o histórico completo é preservado,
        permitindo ao LLM detectar contradições ou mudanças de foco.
        """
        # Arrange
        state = create_initial_multi_agent_state(
            user_input="Quero estudar impacto de LLMs em produtividade",
            session_id="session-123"
        )
        state['messages'] = [
            AIMessage(content="Vamos explorar produtividade então"),
            HumanMessage(content="Na verdade, quero focar em qualidade de código")
        ]

        # Act
        context = _build_context(state)

        # Assert - Ambas direções devem estar presentes no contexto
        assert "produtividade" in context
        assert "qualidade de código" in context
        # LLM pode detectar mudança comparando "produtividade" vs "qualidade"
