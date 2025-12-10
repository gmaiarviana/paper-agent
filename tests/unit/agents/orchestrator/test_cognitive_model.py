"""
Testes para validação e fallback do cognitive_model (Épico 9.1).

Cobre:
- Validação de cognitive_model retornado pelo LLM
- Fallback quando cognitive_model é None ou inválido
- Filtragem de contradictions com baixa confiança
- Retorno de cognitive_model pelo orchestrator_node
"""

from unittest.mock import Mock, patch
import json

from core.agents.orchestrator.state import create_initial_multi_agent_state
from core.agents.orchestrator.nodes import (
    orchestrator_node,
    _validate_cognitive_model,
    _create_fallback_cognitive_model
)

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
        assert result["proposicoes"] == []
        assert "O que você quer explorar" in result["open_questions"][0]
        assert result["contradictions"] == []
        assert result["solid_grounds"] == []
        assert result["context"] == {}

    def test_valid_cognitive_model_passes(self):
        """cognitive_model válido é retornado corretamente."""
        state = create_initial_multi_agent_state(user_input="Teste", session_id="test")

        valid_cm = {
            "claim": "Claude Code aumenta produtividade",
            "proposicoes": [
                {"texto": "Equipes Python existem", "solidez": None},
                {"texto": "Produtividade é mensurável", "solidez": None}
            ],
            "open_questions": ["Qual é o baseline?"],
            "contradictions": [],
            "solid_grounds": [],
            "context": {"domain": "software development"}
        }

        result = _validate_cognitive_model(valid_cm, state)

        assert result["claim"] == "Claude Code aumenta produtividade"
        assert len(result["proposicoes"]) == 2
        # proposicoes vem como lista de dicts (serializado do Pydantic)
        proposicoes_textos = [p["texto"] for p in result["proposicoes"]]
        assert "Equipes Python existem" in proposicoes_textos
        assert "Produtividade é mensurável" in proposicoes_textos
        assert result["open_questions"] == ["Qual é o baseline?"]
        assert result["context"]["domain"] == "software development"

    def test_filters_low_confidence_contradictions(self):
        """Contradictions com confiança < 0.80 são filtradas."""
        state = create_initial_multi_agent_state(user_input="Teste", session_id="test")

        cm_with_contradictions = {
            "claim": "Teste",
            "proposicoes": [],
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
            "proposicoes": [],
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
            "proposicoes": [],
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
        # Usar json.dumps para garantir formato válido, convertendo None para null
        mock_response.content = json.dumps({
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
                    {"texto": "Produtividade é mensurável", "solidez": None}
                ],
                "open_questions": ["Qual métrica?"],
                "contradictions": [],
                "solid_grounds": [],
                "context": {"domain": None, "technology": "LLMs"}
            },
            "agent_suggestion": None,
            "reflection_prompt": None
        })
        mock_response.response_metadata = {"usage_metadata": {"input_tokens": 100, "output_tokens": 50}}

        with patch('core.agents.orchestrator.nodes.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response

            result = orchestrator_node(state)

        assert "cognitive_model" in result
        assert result["cognitive_model"]["claim"] == "LLMs aumentam produtividade"
        assert len(result["cognitive_model"]["proposicoes"]) == 1
        assert result["cognitive_model"]["proposicoes"][0]["texto"] == "Produtividade é mensurável"
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
        mock_response.response_metadata = {"usage_metadata": {"input_tokens": 100, "output_tokens": 50}}

        with patch('core.agents.orchestrator.nodes.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response

            result = orchestrator_node(state)

        assert "cognitive_model" in result
        assert result["cognitive_model"]["claim"] == "Minha observação"
        assert len(result["cognitive_model"]["open_questions"]) >= 1
