"""
Testes para orchestrator_node - classificação e análise de input.

Cobre comportamento do nó principal do Orquestrador:
- Classificação de inputs (vago, semi-formado, completo)
- Sugestões de agentes
- Fallbacks e tratamento de erros
- Integração com histórico de conversa

IMPORTANTE:
- orchestrator_node() agora chama _consult_observer() que faz chamadas LLM
- Testes DEVEM mockar _consult_observer para evitar dependência de API key
- Sem mock, fallback retorna needs_checkpoint=True, mudando next_step para "clarify"
"""

import pytest
from unittest.mock import Mock, patch
from langchain_core.messages import AIMessage, HumanMessage

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
    """Mock automático de _consult_observer para todos os testes desta classe.

    orchestrator_node() agora consulta o Observer para análise
    de clareza e variação. Sem mock, testes falham no CI (sem API key).
    """
    with patch('core.agents.orchestrator.nodes._consult_observer') as mock:
        mock.return_value = MOCK_OBSERVER_RESULT
        yield mock

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

        with patch('core.agents.orchestrator.nodes.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response

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

        with patch('core.agents.orchestrator.nodes.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response

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

        with patch('core.agents.orchestrator.nodes.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response

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

        with patch('core.agents.orchestrator.nodes.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response

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

        with patch('core.agents.orchestrator.nodes.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response

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

        with patch('core.agents.orchestrator.nodes.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response

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

        with patch('core.agents.orchestrator.nodes.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response

            result = orchestrator_node(state)

        assert result['next_step'] == "suggest_agent"
        assert result['agent_suggestion']['agent'] == "structurer"
        assert "PICO/SPIDER" in result['agent_suggestion']['justification']


# ============================================================================
# Testes de regressão — Observer consultivo + invariante de schema
# ============================================================================
#
# Antes do fix em `nodes.py`, o checkpoint de clareza do Observer rebaixava
# next_step="suggest_agent" → "clarify" mesmo quando o Orquestrador tinha
# decidido convocar um agente — descartando a `agent_suggestion` na
# prática (o Estruturador nunca era chamado no Ensaio). Os dois testes
# abaixo travam: (1) o Observer é consultivo e não sobrepõe decisão de
# agente do Orquestrador; (2) o schema do output mantém o invariante
# `next_step != "suggest_agent" → agent_suggestion is None`.


class TestObserverConsultativeRegression:
    """Cobre o fix Observer consultivo + invariante de schema."""

    _STRUCTURER_SUGGESTION_JSON = """
{
  "reasoning": "Tem observação concreta, vou sugerir Estruturador.",
  "next_step": "suggest_agent",
  "message": "Vou organizar sua observação em uma questão estruturada.",
  "agent_suggestion": {
    "agent": "structurer",
    "justification": "Observação concreta existe mas não está estruturada"
  }
}
"""

    @pytest.fixture
    def llm_response_suggesting_structurer(self):
        resp = Mock()
        resp.content = self._STRUCTURER_SUGGESTION_JSON
        resp.response_metadata = {
            "usage_metadata": {"input_tokens": 200, "output_tokens": 80}
        }
        return resp

    def test_observer_does_not_override_suggest_agent_decision(
        self, mock_consult_observer, llm_response_suggesting_structurer
    ):
        """Quando o Orquestrador escolhe `suggest_agent` com agent_suggestion
        válido, o Observer pedindo checkpoint de clareza **não** rebaixa
        para `clarify` — sua decisão é consultiva. O agent_suggestion é
        preservado para que o agente sugerido (ex.: Estruturador) seja
        de fato convocado downstream."""
        # Observer sugere clarify mas Orquestrador decidiu suggest_agent
        mock_consult_observer.return_value = {
            "clarity_evaluation": {
                "clarity_level": "nebulosa",
                "needs_checkpoint": True,
                "suggestion": "Pedir esclarecimento antes de avançar",
            },
            "variation_analysis": None,
            "needs_checkpoint": True,
            "checkpoint_reason": "Clareza baixa pelo Observer",
        }

        state = create_initial_multi_agent_state(
            user_input="Observei que método X reduz tempo de revisão em 30%",
            session_id="test-observer-consultive",
        )

        with patch('core.agents.orchestrator.nodes.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = llm_response_suggesting_structurer
            result = orchestrator_node(state)

        # Decisão do Orquestrador preservada.
        assert result["next_step"] == "suggest_agent", (
            "Observer não deve rebaixar 'suggest_agent' para 'clarify' — é consultivo"
        )
        # agent_suggestion intacta para chegar ao downstream.
        assert result["agent_suggestion"] is not None
        assert result["agent_suggestion"]["agent"] == "structurer"

    def test_schema_invariant_clears_agent_suggestion_when_next_step_changes(
        self, mock_consult_observer
    ):
        """Quando o LLM devolve agent_suggestion preenchido mas next_step
        diferente de "suggest_agent" (ex.: explore), o invariante de
        schema zera agent_suggestion para impedir inconsistência
        downstream. Cobre também o cenário em que validações internas do
        nó mudam next_step (ex.: rebaixar via Observer)."""
        # Postura socrática: input vago → Observer rebaixa para "clarify",
        # e o invariante garante agent_suggestion=None.
        mock_consult_observer.return_value = {
            "clarity_evaluation": {
                "clarity_level": "nebulosa",
                "needs_checkpoint": True,
                "suggestion": "Pedir esclarecimento",
            },
            "variation_analysis": None,
            "needs_checkpoint": True,
            "checkpoint_reason": "Clareza baixa",
        }

        # Input vago: LLM volta explore mas com agent_suggestion preenchido
        # (cenário sintético de inconsistência do prompt).
        mock_response = Mock()
        mock_response.content = """
{
  "reasoning": "Input vago, mas vou exemplificar uma sugestão pendurada.",
  "next_step": "explore",
  "message": "Me conta mais sobre o experimento.",
  "agent_suggestion": {
    "agent": "structurer",
    "justification": "Pendurada — não deveria estar aqui"
  }
}
"""
        mock_response.response_metadata = {
            "usage_metadata": {"input_tokens": 100, "output_tokens": 50}
        }

        state = create_initial_multi_agent_state(
            user_input="acho que LLMs ajudam",
            session_id="test-schema-invariant",
        )

        with patch('core.agents.orchestrator.nodes.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response
            result = orchestrator_node(state)

        # Observer rebaixa para "clarify" (input vago, Orquestrador NÃO
        # tinha decidido suggest_agent definitivo do ponto de vista do
        # invariante — explore não é suggest_agent).
        assert result["next_step"] == "clarify"
        # Invariante: agent_suggestion zerada porque next_step !=
        # "suggest_agent". Postura socrática (input vago → clarify SEM
        # sugestão) preservada para Revelar e qualquer consumidor.
        assert result["agent_suggestion"] is None, (
            "Invariante de schema: next_step != 'suggest_agent' deve zerar "
            "agent_suggestion (postura socrática: clarify sem sugestão)"
        )
