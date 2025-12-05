"""
Testes unitários para o agente Orquestrador.

Cobre:
- orchestrator_node: Nó conversacional (exploração, sugestão, clarificação)
- route_from_orchestrator: Router baseado em next_step e agent_suggestion
- _build_context: Construção de contexto com histórico
- MultiAgentState: Estado compartilhado
- cognitive_model: Validação e fallback do modelo cognitivo (Épico 9.1)

Estes testes usam MOCKS para a API da Anthropic (rápidos, sem custo).
"""

import pytest
from unittest.mock import Mock, patch
from langchain_core.messages import AIMessage, HumanMessage

from agents.orchestrator.state import MultiAgentState, create_initial_multi_agent_state
from agents.orchestrator.nodes import (
    orchestrator_node,
    _build_context,
    _validate_cognitive_model,
    _create_fallback_cognitive_model
)
from agents.orchestrator.router import route_from_orchestrator


# =============================================================================
# TESTES DO NÓ ORCHESTRATOR_NODE
# =============================================================================

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
        mock_response.usage_metadata = {"input_tokens": 100, "output_tokens": 50}

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
        mock_response.usage_metadata = {"input_tokens": 100, "output_tokens": 50}

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
        mock_response.usage_metadata = {"input_tokens": 100, "output_tokens": 50}

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
        mock_response.usage_metadata = {"input_tokens": 80, "output_tokens": 40}

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
        mock_response.usage_metadata = {"input_tokens": 50, "output_tokens": 10}

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
        mock_response.usage_metadata = {"input_tokens": 50, "output_tokens": 20}

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
        mock_response.usage_metadata = {"input_tokens": 200, "output_tokens": 80}

        with patch('agents.orchestrator.nodes.ChatAnthropic') as mock_llm_class:
            mock_llm = Mock()
            mock_llm.invoke.return_value = mock_response
            mock_llm_class.return_value = mock_llm

            result = orchestrator_node(state)

        assert result['next_step'] == "suggest_agent"
        assert result['agent_suggestion']['agent'] == "structurer"
        assert "PICO/SPIDER" in result['agent_suggestion']['justification']


# =============================================================================
# TESTES DO ROUTER
# =============================================================================

class TestRouteFromOrchestrator:
    """Testes para route_from_orchestrator - decisão de próximo nó."""

    def test_explore_routes_to_user(self):
        """next_step = explore → retorna para usuário."""
        state = create_initial_multi_agent_state(user_input="Teste", session_id="test")
        state['next_step'] = "explore"
        state['agent_suggestion'] = None

        assert route_from_orchestrator(state) == "user"

    def test_clarify_routes_to_user(self):
        """next_step = clarify → retorna para usuário."""
        state = create_initial_multi_agent_state(user_input="Teste", session_id="test")
        state['next_step'] = "clarify"
        state['agent_suggestion'] = None

        assert route_from_orchestrator(state) == "user"

    def test_suggest_structurer_routes_to_structurer(self):
        """Agente sugerido = structurer → roteia para structurer."""
        state = create_initial_multi_agent_state(user_input="Teste", session_id="test")
        state["next_step"] = "suggest_agent"
        state["agent_suggestion"] = {
            "agent": "structurer",
            "justification": "Observação não estruturada"
        }

        assert route_from_orchestrator(state) == "structurer"

    def test_suggest_methodologist_routes_to_methodologist(self):
        """Agente sugerido = methodologist → roteia para methodologist."""
        state = create_initial_multi_agent_state(user_input="Teste", session_id="test")
        state["next_step"] = "suggest_agent"
        state["agent_suggestion"] = {
            "agent": "methodologist",
            "justification": "Hipótese pronta para validação"
        }

        assert route_from_orchestrator(state) == "methodologist"

    def test_invalid_agent_routes_to_user(self):
        """Agente inválido → fallback para user."""
        state = create_initial_multi_agent_state(user_input="Teste", session_id="test")
        state['next_step'] = "suggest_agent"
        state['agent_suggestion'] = {
            "agent": "invalid_agent",
            "justification": "Teste"
        }

        assert route_from_orchestrator(state) == "user"

    def test_missing_suggestion_routes_to_user(self):
        """next_step=suggest_agent mas suggestion=None → fallback para user."""
        state = create_initial_multi_agent_state(user_input="Teste", session_id="test")
        state['next_step'] = "suggest_agent"
        state['agent_suggestion'] = None

        assert route_from_orchestrator(state) == "user"

    def test_none_next_step_raises_error(self):
        """next_step = None → lança ValueError."""
        state = create_initial_multi_agent_state(user_input="Teste", session_id="test")
        state["next_step"] = None

        with pytest.raises(ValueError, match="next_step do Orquestrador está None"):
            route_from_orchestrator(state)

    def test_invalid_next_step_raises_error(self):
        """next_step inválido → lança ValueError."""
        state = create_initial_multi_agent_state(user_input="Teste", session_id="test")
        state["next_step"] = "invalid_value"

        with pytest.raises(ValueError, match="next_step inválido"):
            route_from_orchestrator(state)


# =============================================================================
# TESTES DO ESTADO
# =============================================================================

class TestMultiAgentState:
    """Testes para MultiAgentState e create_initial_multi_agent_state."""

    def test_initial_state_has_required_fields(self):
        """Estado inicial possui todos os campos obrigatórios."""
        state = create_initial_multi_agent_state(
            user_input="Teste de input",
            session_id="test-session-1",
        )

        # Campos compartilhados
        assert state['user_input'] == "Teste de input"
        assert state['session_id'] == "test-session-1"
        assert state['conversation_history'] == ["Usuário: Teste de input"]
        assert state['current_stage'] == "classifying"
        assert state['hypothesis_versions'] == []

        # Campos específicos (devem começar None)
        assert state['orchestrator_analysis'] is None
        assert state['next_step'] is None
        assert state['agent_suggestion'] is None
        assert state['focal_argument'] is None
        assert state['reflection_prompt'] is None
        assert state['stage_suggestion'] is None
        assert state['structurer_output'] is None
        assert state['methodologist_output'] is None

        # Mensagens (1 HumanMessage inicial)
        assert len(state['messages']) == 1
        assert isinstance(state['messages'][0], HumanMessage)
        assert state['messages'][0].content == "Teste de input"

    def test_state_is_mutable(self):
        """Campos do estado podem ser atualizados."""
        state = create_initial_multi_agent_state(user_input="Teste", session_id="test")

        state['next_step'] = "explore"
        state['current_stage'] = "structuring"

        assert state['next_step'] == "explore"
        assert state['current_stage'] == "structuring"


# =============================================================================
# TESTES DO BUILD_CONTEXT
# =============================================================================

class TestBuildContext:
    """Testes para _build_context - construção de contexto para LLM."""

    def test_with_initial_input_only(self):
        """Contexto com apenas input inicial."""
        state = create_initial_multi_agent_state(
            user_input="Observei que LLMs aumentam produtividade",
            session_id="session-123"
        )

        context = _build_context(state)

        assert "INPUT INICIAL DO USUÁRIO:" in context
        assert "Observei que LLMs aumentam produtividade" in context
        assert "HISTÓRICO DA CONVERSA:" in context

    def test_with_conversation_history(self):
        """Contexto com histórico de conversa."""
        state = create_initial_multi_agent_state(
            user_input="Observei que LLMs aumentam produtividade",
            session_id="session-123"
        )
        state['messages'] = [
            HumanMessage(content="Quero validar essa observação"),
            AIMessage(content="Vou organizar sua ideia em uma questão de pesquisa."),
            HumanMessage(content="Perfeito, obrigado")
        ]

        context = _build_context(state)

        assert "[Usuário]: Quero validar essa observação" in context
        assert "[Assistente]: Vou organizar sua ideia em uma questão de pesquisa." in context
        assert "[Usuário]: Perfeito, obrigado" in context

    def test_preserves_chronological_order(self):
        """Contexto preserva ordem cronológica."""
        state = create_initial_multi_agent_state(user_input="Input", session_id="test")
        state['messages'] = [
            HumanMessage(content="Mensagem 1"),
            AIMessage(content="Resposta 1"),
            HumanMessage(content="Mensagem 2"),
            AIMessage(content="Resposta 2")
        ]

        context = _build_context(state)
        lines = context.split("\n")

        msg1_idx = next(i for i, line in enumerate(lines) if "Mensagem 1" in line)
        resp1_idx = next(i for i, line in enumerate(lines) if "Resposta 1" in line)
        msg2_idx = next(i for i, line in enumerate(lines) if "Mensagem 2" in line)
        resp2_idx = next(i for i, line in enumerate(lines) if "Resposta 2" in line)

        assert msg1_idx < resp1_idx < msg2_idx < resp2_idx

    def test_empty_messages_omits_history_section(self):
        """Lista vazia de mensagens omite seção de histórico."""
        state = create_initial_multi_agent_state(user_input="Input", session_id="test")
        state['messages'] = []

        context = _build_context(state)

        assert "INPUT INICIAL DO USUÁRIO:" in context
        assert "HISTÓRICO DA CONVERSA:" not in context

    def test_format_is_llm_friendly(self):
        """Formato é adequado para LLM (estrutura clara)."""
        state = create_initial_multi_agent_state(user_input="Observei X", session_id="test")
        state['messages'] = [
            AIMessage(content="Pergunta"),
            HumanMessage(content="Resposta")
        ]

        context = _build_context(state)

        assert context.startswith("INPUT INICIAL DO USUÁRIO:")
        assert "[Usuário]:" in context
        assert "[Assistente]:" in context

    def test_preserves_direction_change_context(self):
        """Contexto preserva mudanças de direção para detecção pelo LLM."""
        state = create_initial_multi_agent_state(
            user_input="Quero estudar impacto de LLMs em produtividade",
            session_id="test"
        )
        state['messages'] = [
            AIMessage(content="Vamos explorar produtividade então"),
            HumanMessage(content="Na verdade, quero focar em qualidade de código")
        ]

        context = _build_context(state)

        assert "produtividade" in context
        assert "qualidade de código" in context


# =============================================================================
# TESTES DO COGNITIVE_MODEL (Épico 9.1)
# =============================================================================

class TestCognitiveModelValidation:
    """Testes para validação e fallback do cognitive_model."""

    def test_fallback_when_none(self):
        """Fallback quando cognitive_model é None."""
        state = create_initial_multi_agent_state(
            user_input="LLMs aumentam produtividade",
            session_id="test"
        )

        result = _validate_cognitive_model(None, state)

        assert result["claim"] == "LLMs aumentam produtividade"
        assert result["premises"] == []
        assert result["assumptions"] == []
        assert "O que você quer explorar" in result["open_questions"][0]
        assert result["contradictions"] == []
        assert result["solid_grounds"] == []
        assert result["context"] == {}

    def test_valid_cognitive_model_passes(self):
        """cognitive_model válido é retornado corretamente."""
        state = create_initial_multi_agent_state(user_input="Teste", session_id="test")

        valid_cm = {
            "claim": "Claude Code aumenta produtividade",
            "premises": ["Equipes Python existem"],
            "assumptions": ["Produtividade é mensurável"],
            "open_questions": ["Qual é o baseline?"],
            "contradictions": [],
            "solid_grounds": [],
            "context": {"domain": "software development"}
        }

        result = _validate_cognitive_model(valid_cm, state)

        assert result["claim"] == "Claude Code aumenta produtividade"
        assert result["premises"] == ["Equipes Python existem"]
        assert result["assumptions"] == ["Produtividade é mensurável"]
        assert result["open_questions"] == ["Qual é o baseline?"]
        assert result["context"]["domain"] == "software development"

    def test_filters_low_confidence_contradictions(self):
        """Contradictions com confiança < 0.80 são filtradas."""
        state = create_initial_multi_agent_state(user_input="Teste", session_id="test")

        cm_with_contradictions = {
            "claim": "Teste",
            "premises": [],
            "assumptions": [],
            "open_questions": [],
            "contradictions": [
                {"description": "Baixa confiança", "confidence": 0.5},  # Filtrada
                {"description": "Alta confiança", "confidence": 0.85}  # Mantida
            ],
            "solid_grounds": [],
            "context": {}
        }

        result = _validate_cognitive_model(cm_with_contradictions, state)

        assert len(result["contradictions"]) == 1
        assert result["contradictions"][0]["description"] == "Alta confiança"

    def test_empty_claim_is_valid(self):
        """claim vazio é válido (início da conversa)."""
        state = create_initial_multi_agent_state(user_input="Teste", session_id="test")

        cm_empty_claim = {
            "claim": "",
            "premises": [],
            "assumptions": [],
            "open_questions": [],
            "contradictions": [],
            "solid_grounds": [],
            "context": {}
        }

        result = _validate_cognitive_model(cm_empty_claim, state)

        assert result["claim"] == ""

    def test_context_with_null_fields_is_valid(self):
        """context com campos null é válido (não-determinístico)."""
        state = create_initial_multi_agent_state(user_input="Teste", session_id="test")

        cm_with_nulls = {
            "claim": "Teste",
            "premises": [],
            "assumptions": [],
            "open_questions": [],
            "contradictions": [],
            "solid_grounds": [],
            "context": {
                "domain": None,
                "technology": "LLMs",
                "population": None,
                "metrics": None,
                "article_type": None
            }
        }

        result = _validate_cognitive_model(cm_with_nulls, state)

        assert result["context"]["domain"] is None
        assert result["context"]["technology"] == "LLMs"
        assert result["context"]["article_type"] is None


class TestCognitiveModelFallback:
    """Testes para _create_fallback_cognitive_model."""

    def test_fallback_uses_user_input(self):
        """Fallback usa user_input como claim."""
        state = create_initial_multi_agent_state(
            user_input="Minha observação sobre LLMs",
            session_id="test"
        )

        result = _create_fallback_cognitive_model(state)

        assert result["claim"] == "Minha observação sobre LLMs"
        assert len(result["open_questions"]) == 1

    def test_fallback_truncates_long_input(self):
        """Fallback trunca user_input longo para 200 chars."""
        long_input = "A" * 300
        state = create_initial_multi_agent_state(user_input=long_input, session_id="test")

        result = _create_fallback_cognitive_model(state)

        assert len(result["claim"]) == 200

    def test_fallback_handles_empty_input(self):
        """Fallback lida com user_input vazio."""
        state = create_initial_multi_agent_state(user_input="", session_id="test")

        result = _create_fallback_cognitive_model(state)

        assert result["claim"] == ""


class TestOrchestratorReturnsCognitiveModel:
    """Testes para verificar que orchestrator_node retorna cognitive_model."""

    def test_returns_cognitive_model_from_llm(self):
        """orchestrator_node retorna cognitive_model do LLM."""
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
    "premises": [],
    "assumptions": ["Produtividade é mensurável"],
    "open_questions": ["Qual métrica?"],
    "contradictions": [],
    "solid_grounds": [],
    "context": {"domain": null, "technology": "LLMs"}
  },
  "agent_suggestion": null,
  "reflection_prompt": null
}
"""
        mock_response.usage_metadata = {"input_tokens": 100, "output_tokens": 50}

        with patch('agents.orchestrator.nodes.ChatAnthropic') as mock_llm_class:
            mock_llm = Mock()
            mock_llm.invoke.return_value = mock_response
            mock_llm_class.return_value = mock_llm

            result = orchestrator_node(state)

        assert "cognitive_model" in result
        assert result["cognitive_model"]["claim"] == "LLMs aumentam produtividade"
        assert result["cognitive_model"]["assumptions"] == ["Produtividade é mensurável"]
        assert result["cognitive_model"]["open_questions"] == ["Qual métrica?"]

    def test_returns_fallback_when_llm_omits_cognitive_model(self):
        """orchestrator_node retorna fallback quando LLM não inclui cognitive_model."""
        state = create_initial_multi_agent_state(
            user_input="Minha observação",
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
    "subject": "test",
    "population": "not specified",
    "metrics": "not specified",
    "article_type": "unclear"
  },
  "agent_suggestion": null
}
"""
        mock_response.usage_metadata = {"input_tokens": 100, "output_tokens": 50}

        with patch('agents.orchestrator.nodes.ChatAnthropic') as mock_llm_class:
            mock_llm = Mock()
            mock_llm.invoke.return_value = mock_response
            mock_llm_class.return_value = mock_llm

            result = orchestrator_node(state)

        assert "cognitive_model" in result
        assert result["cognitive_model"]["claim"] == "Minha observação"
        assert len(result["cognitive_model"]["open_questions"]) >= 1
