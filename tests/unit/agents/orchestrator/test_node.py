"""
Testes para orchestrator_node - classificação e análise de input.

Cobre comportamento do nó principal do Orquestrador:
- Classificação de inputs (vago, semi-formado, completo)
- Sugestões de agentes
- Fallbacks e tratamento de erros
- Integração com histórico de conversa
"""

import pytest
from unittest.mock import Mock, patch
from langchain_core.messages import AIMessage, HumanMessage

from agents.orchestrator.state import create_initial_multi_agent_state
from agents.orchestrator.nodes import orchestrator_node


class TestOrchestratorNode:
    """Testes para orchestrator_node - classificação e análise de input."""

    def test_vague_input_returns_explore(self):
        """Input vago → next_step = explore, sem sugestão de agente."""
        state = create_initial_multi_agent_state(
            user_input="Observei que desenvolver com Claude Code é mais rápido",
            session_id="test-session-1",
        )

        mock_response = Mock()
        mock_response.content = """
{
  "reasoning": "Falta estruturação da ideia",
  "next_step": "explore",
  "message": "Interessante observação! Me conta um pouco mais sobre o contexto.",
  "agent_suggestion": null
}
"""
        mock_response.response_metadata = {"usage_metadata": {"input_tokens": 100, "output_tokens": 50}}

        with patch('agents.orchestrator.nodes.ChatAnthropic') as mock_llm_class:
            mock_llm = Mock()
            mock_llm.invoke.return_value = mock_response
            mock_llm_class.return_value = mock_llm

            result = orchestrator_node(state)

        assert result["next_step"] == "explore"
        assert result["orchestrator_analysis"].startswith("Falta estruturação da ideia")
        assert result["agent_suggestion"] is None
        assert len(result['messages']) == 1
        assert isinstance(result['messages'][0], AIMessage)

    def test_semi_formed_input_suggests_structurer(self):
        """Hipótese semi-formada → sugere structurer."""
        state = create_initial_multi_agent_state(
            user_input="Método incremental melhora desenvolvimento multi-agente",
            session_id="test-session-1",
        )

        mock_response = Mock()
        mock_response.content = """
{
  "reasoning": "Tem ideia central mas falta especificidade",
  "next_step": "suggest_agent",
  "message": "Vou organizar sua observação em uma questão de pesquisa estruturada.",
  "agent_suggestion": {
    "agent": "structurer",
    "justification": "Ideia concreta porém não estruturada como questão"
  }
}
"""
        mock_response.response_metadata = {"usage_metadata": {"input_tokens": 100, "output_tokens": 50}}

        with patch('agents.orchestrator.nodes.ChatAnthropic') as mock_llm_class:
            mock_llm = Mock()
            mock_llm.invoke.return_value = mock_response
            mock_llm_class.return_value = mock_llm

            result = orchestrator_node(state)

        assert result["next_step"] == "suggest_agent"
        assert result["agent_suggestion"]["agent"] == "structurer"
        assert result["orchestrator_analysis"].startswith("Tem ideia central")

    def test_complete_hypothesis_suggests_methodologist(self):
        """Hipótese completa → sugere methodologist."""
        state = create_initial_multi_agent_state(
            user_input=(
                "Método incremental reduz tempo de implementação de sistemas "
                "multi-agente em 30%, medido por sprints, em equipes de 2-5 devs"
            ),
            session_id="test-session-1",
        )

        mock_response = Mock()
        mock_response.content = """
{
  "reasoning": "Hipótese bem especificada com métricas",
  "next_step": "suggest_agent",
  "message": "Sua hipótese está bem formada. Vou validar metodologicamente.",
  "agent_suggestion": {
    "agent": "methodologist",
    "justification": "Hipótese completa, pronta para validação metodológica"
  }
}
"""
        mock_response.response_metadata = {"usage_metadata": {"input_tokens": 100, "output_tokens": 50}}

        with patch('agents.orchestrator.nodes.ChatAnthropic') as mock_llm_class:
            mock_llm = Mock()
            mock_llm.invoke.return_value = mock_response
            mock_llm_class.return_value = mock_llm

            result = orchestrator_node(state)

        assert result["next_step"] == "suggest_agent"
        assert result["agent_suggestion"]["agent"] == "methodologist"
        assert result["orchestrator_analysis"].startswith("Hipótese bem especificada")

    def test_ambiguous_input_returns_clarify(self):
        """Input ambíguo → next_step = clarify."""
        state = create_initial_multi_agent_state(
            user_input="Quero estudar LLMs",
            session_id="test-session-1",
        )

        mock_response = Mock()
        mock_response.content = """
{
  "reasoning": "Input muito vago. Pode significar revisar literatura, testar hipótese ou desenvolver método.",
  "next_step": "clarify",
  "message": "Entender o que já existe (literatura)? Testar uma observação? Ou desenvolver algo novo?",
  "agent_suggestion": null
}
"""
        mock_response.response_metadata = {"usage_metadata": {"input_tokens": 80, "output_tokens": 40}}

        with patch('agents.orchestrator.nodes.ChatAnthropic') as mock_llm_class:
            mock_llm = Mock()
            mock_llm.invoke.return_value = mock_response
            mock_llm_class.return_value = mock_llm

            result = orchestrator_node(state)

        assert result["next_step"] == "clarify"
        assert result["agent_suggestion"] is None
        assert "Entender o que já existe" in result['messages'][0].content

    def test_malformed_json_returns_fallback(self):
        """JSON malformado → fallback seguro (explore)."""
        state = create_initial_multi_agent_state(
            user_input="Teste",
            session_id="test-session-1",
        )

        mock_response = Mock()
        mock_response.content = "Resposta sem JSON válido"
        mock_response.response_metadata = {"usage_metadata": {"input_tokens": 50, "output_tokens": 10}}

        with patch('agents.orchestrator.nodes.ChatAnthropic') as mock_llm_class:
            mock_llm = Mock()
            mock_llm.invoke.return_value = mock_response
            mock_llm_class.return_value = mock_llm

            result = orchestrator_node(state)

        assert result["next_step"] == "explore"
        assert "dificuldade em processar" in result['messages'][0].content

    def test_adds_ai_message_to_history(self):
        """Nó adiciona AIMessage ao histórico de mensagens."""
        state = create_initial_multi_agent_state(
            user_input="Teste",
            session_id="test-session-1",
        )

        mock_response = Mock()
        mock_response.content = """
{
  "reasoning": "Teste",
  "next_step": "explore",
  "message": "Mensagem de teste para o usuário",
  "agent_suggestion": null
}
"""
        mock_response.response_metadata = {"usage_metadata": {"input_tokens": 50, "output_tokens": 20}}

        with patch('agents.orchestrator.nodes.ChatAnthropic') as mock_llm_class:
            mock_llm = Mock()
            mock_llm.invoke.return_value = mock_response
            mock_llm_class.return_value = mock_llm

            result = orchestrator_node(state)

        assert len(result['messages']) == 1
        assert isinstance(result['messages'][0], AIMessage)

    def test_with_conversation_history(self):
        """Nó funciona com histórico de conversa existente."""
        state = create_initial_multi_agent_state(
            user_input="Observei que LLMs aumentam produtividade",
            session_id="test-session-1"
        )
        state["messages"] = [
            HumanMessage(content="Na minha equipe, usando Claude Code, tarefas de 2h agora levam 30min"),
            AIMessage(content="Você quer validar ou entender literatura?"),
            HumanMessage(content="Quero validar como hipótese")
        ]

        mock_response = Mock()
        mock_response.content = """
{
  "reasoning": "Usuário escolheu validar. Tem observação concreta mas não estruturada.",
  "next_step": "suggest_agent",
  "message": "Vou organizar sua observação em uma questão de pesquisa estruturada.",
  "agent_suggestion": {
    "agent": "structurer",
    "justification": "Observação concreta existe mas não está estruturada como questão PICO/SPIDER"
  }
}
"""
        mock_response.response_metadata = {"usage_metadata": {"input_tokens": 200, "output_tokens": 80}}

        with patch('agents.orchestrator.nodes.ChatAnthropic') as mock_llm_class:
            mock_llm = Mock()
            mock_llm.invoke.return_value = mock_response
            mock_llm_class.return_value = mock_llm

            result = orchestrator_node(state)

        assert result['next_step'] == "suggest_agent"
        assert result['agent_suggestion']['agent'] == "structurer"
        assert "PICO/SPIDER" in result['agent_suggestion']['justification']

