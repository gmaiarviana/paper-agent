"""
Testes unitarios para avaliacao de clareza da conversa (Epico 13.2).

Valida a funcao evaluate_conversation_clarity() que avalia se a conversa
esta fluindo bem ou precisa de checkpoint para esclarecimentos.

Escala de clareza: cristalina -> clara -> nebulosa -> confusa

Usa mocks para LLM - nao faz chamadas reais.

"""

import pytest
from unittest.mock import patch, MagicMock
import sys

# Mock chromadb antes de importar modulos que dependem dele
sys.modules['chromadb'] = MagicMock()
sys.modules['chromadb.config'] = MagicMock()

# Import direto do modulo (evita __init__.py com dependencias pesadas)
from agents.observer.extractors import evaluate_conversation_clarity
from agents.observer.prompts import CLARITY_EVALUATION_PROMPT

class TestEvaluateClarityBasic:
    """Testes basicos para evaluate_conversation_clarity."""

    def test_function_exists(self):
        """Valida que funcao existe e e importavel."""
        from agents.observer.extractors import evaluate_conversation_clarity
        assert callable(evaluate_conversation_clarity)

    def test_function_signature(self):
        """Valida assinatura da funcao."""
        import inspect
        sig = inspect.signature(evaluate_conversation_clarity)
        params = list(sig.parameters.keys())

        assert "cognitive_model" in params
        assert "conversation_history" in params
        assert "llm" in params

    def test_returns_dict_with_required_fields(self):
        """Valida que retorno contem campos obrigatorios."""
        mock_response = MagicMock()
        mock_response.content = '''{
            "clarity_level": "clara",
            "clarity_score": 4,
            "description": "Conversa fluindo bem",
            "needs_checkpoint": false,
            "factors": {
                "claim_definition": "bem definido",
                "coherence": "alta",
                "direction_stability": "estavel"
            },
            "suggestion": null
        }'''

        with patch('agents.observer.extractors.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response

            result = evaluate_conversation_clarity(
                cognitive_model={"claim": "Teste"}
            )

        # Campos obrigatorios
        assert "clarity_level" in result
        assert "clarity_score" in result
        assert "description" in result
        assert "needs_checkpoint" in result
        assert "factors" in result
        assert "suggestion" in result

class TestClarityLevels:
    """Testes para os niveis de clareza."""

    def test_clarity_cristalina(self):
        """Testa nivel cristalina (melhor)."""
        mock_response = MagicMock()
        mock_response.content = '''{
            "clarity_level": "cristalina",
            "clarity_score": 5,
            "description": "Conversa excepcional, claim claro e coerente",
            "needs_checkpoint": false,
            "factors": {
                "claim_definition": "bem definido",
                "coherence": "alta",
                "direction_stability": "estavel"
            },
            "suggestion": null
        }'''

        with patch('agents.observer.extractors.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response

            result = evaluate_conversation_clarity({"claim": "Teste"})

        assert result["clarity_level"] == "cristalina"
        assert result["clarity_score"] == 5
        assert result["needs_checkpoint"] is False

    def test_clarity_clara(self):
        """Testa nivel clara (bom)."""
        mock_response = MagicMock()
        mock_response.content = '''{
            "clarity_level": "clara",
            "clarity_score": 4,
            "description": "Conversa boa, flui bem",
            "needs_checkpoint": false,
            "factors": {
                "claim_definition": "bem definido",
                "coherence": "alta",
                "direction_stability": "estavel"
            },
            "suggestion": null
        }'''

        with patch('agents.observer.extractors.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response

            result = evaluate_conversation_clarity({"claim": "Teste"})

        assert result["clarity_level"] == "clara"
        assert result["clarity_score"] == 4
        assert result["needs_checkpoint"] is False

    def test_clarity_nebulosa(self):
        """Testa nivel nebulosa (precisa atencao)."""
        mock_response = MagicMock()
        mock_response.content = '''{
            "clarity_level": "nebulosa",
            "clarity_score": 3,
            "description": "Ha pontos que merecem esclarecimento",
            "needs_checkpoint": true,
            "factors": {
                "claim_definition": "parcial",
                "coherence": "media",
                "direction_stability": "algumas mudancas"
            },
            "suggestion": "Esclarecer as metricas"
        }'''

        with patch('agents.observer.extractors.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response

            result = evaluate_conversation_clarity({"claim": "Teste"})

        assert result["clarity_level"] == "nebulosa"
        assert result["clarity_score"] == 3
        assert result["needs_checkpoint"] is True
        assert result["suggestion"] is not None

    def test_clarity_confusa(self):
        """Testa nivel confusa (pior)."""
        mock_response = MagicMock()
        mock_response.content = '''{
            "clarity_level": "confusa",
            "clarity_score": 1,
            "description": "Conversa dificil, precisa parar e clarificar",
            "needs_checkpoint": true,
            "factors": {
                "claim_definition": "vago",
                "coherence": "baixa",
                "direction_stability": "instavel"
            },
            "suggestion": "Pausar e perguntar qual o foco principal"
        }'''

        with patch('agents.observer.extractors.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response

            result = evaluate_conversation_clarity({"claim": ""})

        assert result["clarity_level"] == "confusa"
        assert result["clarity_score"] == 1
        assert result["needs_checkpoint"] is True

class TestClarityScore:
    """Testes para o score numerico."""

    def test_score_range_valid(self):
        """Testa que score esta no range 1-5."""
        mock_response = MagicMock()
        mock_response.content = '''{
            "clarity_level": "clara",
            "clarity_score": 4,
            "description": "Teste",
            "needs_checkpoint": false,
            "factors": {"claim_definition": "bem definido", "coherence": "alta", "direction_stability": "estavel"},
            "suggestion": null
        }'''

        with patch('agents.observer.extractors.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response

            result = evaluate_conversation_clarity({"claim": "Teste"})

        assert 1 <= result["clarity_score"] <= 5

    def test_invalid_score_infers_from_level(self):
        """Testa que score invalido e inferido do level."""
        mock_response = MagicMock()
        mock_response.content = '''{
            "clarity_level": "cristalina",
            "clarity_score": 99,
            "description": "Teste",
            "needs_checkpoint": false,
            "factors": {"claim_definition": "bem definido", "coherence": "alta", "direction_stability": "estavel"},
            "suggestion": null
        }'''

        with patch('agents.observer.extractors.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response

            result = evaluate_conversation_clarity({"claim": "Teste"})

        # Score invalido (99) deve ser corrigido para 5 (cristalina)
        assert result["clarity_score"] == 5

class TestNeedsCheckpoint:
    """Testes para o campo needs_checkpoint."""

    def test_checkpoint_false_for_cristalina(self):
        """Cristalina nao precisa de checkpoint."""
        mock_response = MagicMock()
        mock_response.content = '''{
            "clarity_level": "cristalina",
            "clarity_score": 5,
            "description": "Excelente",
            "needs_checkpoint": false,
            "factors": {"claim_definition": "bem definido", "coherence": "alta", "direction_stability": "estavel"},
            "suggestion": null
        }'''

        with patch('agents.observer.extractors.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response

            result = evaluate_conversation_clarity({"claim": "Teste"})

        assert result["needs_checkpoint"] is False

    def test_checkpoint_false_for_clara(self):
        """Clara nao precisa de checkpoint."""
        mock_response = MagicMock()
        mock_response.content = '''{
            "clarity_level": "clara",
            "clarity_score": 4,
            "description": "Boa",
            "needs_checkpoint": false,
            "factors": {"claim_definition": "bem definido", "coherence": "alta", "direction_stability": "estavel"},
            "suggestion": null
        }'''

        with patch('agents.observer.extractors.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response

            result = evaluate_conversation_clarity({"claim": "Teste"})

        assert result["needs_checkpoint"] is False

    def test_checkpoint_true_for_nebulosa(self):
        """Nebulosa precisa de checkpoint."""
        mock_response = MagicMock()
        mock_response.content = '''{
            "clarity_level": "nebulosa",
            "clarity_score": 3,
            "description": "Ambigua",
            "needs_checkpoint": true,
            "factors": {"claim_definition": "parcial", "coherence": "media", "direction_stability": "algumas mudancas"},
            "suggestion": "Esclarecer"
        }'''

        with patch('agents.observer.extractors.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response

            result = evaluate_conversation_clarity({"claim": "Teste"})

        assert result["needs_checkpoint"] is True

    def test_checkpoint_true_for_confusa(self):
        """Confusa precisa de checkpoint."""
        mock_response = MagicMock()
        mock_response.content = '''{
            "clarity_level": "confusa",
            "clarity_score": 1,
            "description": "Dificil",
            "needs_checkpoint": true,
            "factors": {"claim_definition": "vago", "coherence": "baixa", "direction_stability": "instavel"},
            "suggestion": "Pausar"
        }'''

        with patch('agents.observer.extractors.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response

            result = evaluate_conversation_clarity({"claim": ""})

        assert result["needs_checkpoint"] is True

class TestFactors:
    """Testes para os fatores de clareza."""

    def test_factors_has_required_keys(self):
        """Testa que factors tem as chaves obrigatorias."""
        mock_response = MagicMock()
        mock_response.content = '''{
            "clarity_level": "clara",
            "clarity_score": 4,
            "description": "Teste",
            "needs_checkpoint": false,
            "factors": {
                "claim_definition": "bem definido",
                "coherence": "alta",
                "direction_stability": "estavel"
            },
            "suggestion": null
        }'''

        with patch('agents.observer.extractors.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response

            result = evaluate_conversation_clarity({"claim": "Teste"})

        assert "claim_definition" in result["factors"]
        assert "coherence" in result["factors"]
        assert "direction_stability" in result["factors"]

    def test_invalid_factor_values_get_defaults(self):
        """Testa que valores invalidos recebem defaults."""
        mock_response = MagicMock()
        mock_response.content = '''{
            "clarity_level": "clara",
            "clarity_score": 4,
            "description": "Teste",
            "needs_checkpoint": false,
            "factors": {
                "claim_definition": "valor_invalido",
                "coherence": "outro_invalido",
                "direction_stability": "mais_invalido"
            },
            "suggestion": null
        }'''

        with patch('agents.observer.extractors.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response

            result = evaluate_conversation_clarity({"claim": "Teste"})

        # Valores invalidos devem virar defaults
        assert result["factors"]["claim_definition"] == "parcial"
        assert result["factors"]["coherence"] == "media"
        assert result["factors"]["direction_stability"] == "algumas mudancas"

    def test_missing_factors_get_defaults(self):
        """Testa que factors ausentes recebem defaults."""
        mock_response = MagicMock()
        mock_response.content = '''{
            "clarity_level": "clara",
            "clarity_score": 4,
            "description": "Teste",
            "needs_checkpoint": false,
            "factors": {},
            "suggestion": null
        }'''

        with patch('agents.observer.extractors.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response

            result = evaluate_conversation_clarity({"claim": "Teste"})

        # Factors ausentes devem ter defaults
        assert result["factors"]["claim_definition"] == "parcial"
        assert result["factors"]["coherence"] == "media"
        assert result["factors"]["direction_stability"] == "algumas mudancas"

class TestErrorHandling:
    """Testes para tratamento de erros."""

    def test_handles_llm_error_gracefully(self):
        """Testa que erro no LLM retorna fallback nebulosa."""
        with patch('agents.observer.extractors.invoke_with_retry') as mock_invoke:
            mock_invoke.side_effect = Exception("LLM timeout")

            result = evaluate_conversation_clarity({"claim": "Teste"})

        # Fallback: nebulosa com checkpoint=True
        assert result["clarity_level"] == "nebulosa"
        assert result["clarity_score"] == 3
        assert result["needs_checkpoint"] is True
        assert "Erro" in result["description"]

    def test_handles_invalid_json_response(self):
        """Testa que JSON invalido retorna fallback."""
        mock_response = MagicMock()
        mock_response.content = "Resposta invalida sem JSON"

        with patch('agents.observer.extractors.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response
            with patch('agents.observer.extractors.extract_json_from_llm_response') as mock_json:
                mock_json.side_effect = Exception("JSON parse error")

                result = evaluate_conversation_clarity({"claim": "Teste"})

        # Fallback
        assert result["clarity_level"] == "nebulosa"
        assert result["needs_checkpoint"] is True

    def test_handles_empty_cognitive_model(self):
        """Testa que modelo vazio nao causa erro."""
        mock_response = MagicMock()
        mock_response.content = '''{
            "clarity_level": "confusa",
            "clarity_score": 1,
            "description": "Modelo vazio",
            "needs_checkpoint": true,
            "factors": {"claim_definition": "vago", "coherence": "baixa", "direction_stability": "instavel"},
            "suggestion": "Definir um claim"
        }'''

        with patch('agents.observer.extractors.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response

            result = evaluate_conversation_clarity({})

        assert "clarity_level" in result

    def test_invalid_clarity_level_defaults_to_nebulosa(self):
        """Testa que level invalido vira nebulosa."""
        mock_response = MagicMock()
        mock_response.content = '''{
            "clarity_level": "valor_invalido",
            "clarity_score": 3,
            "description": "Teste",
            "needs_checkpoint": true,
            "factors": {},
            "suggestion": null
        }'''

        with patch('agents.observer.extractors.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response

            result = evaluate_conversation_clarity({"claim": "Teste"})

        assert result["clarity_level"] == "nebulosa"

class TestPrompt:
    """Testes para o prompt de avaliacao de clareza."""

    def test_prompt_exists(self):
        """Valida que prompt existe."""
        assert CLARITY_EVALUATION_PROMPT is not None
        assert len(CLARITY_EVALUATION_PROMPT) > 100

    def test_prompt_has_placeholders(self):
        """Valida que prompt tem placeholders necessarios."""
        assert "{claim}" in CLARITY_EVALUATION_PROMPT
        assert "{proposicoes}" in CLARITY_EVALUATION_PROMPT
        assert "{contradictions}" in CLARITY_EVALUATION_PROMPT
        assert "{open_questions}" in CLARITY_EVALUATION_PROMPT
        assert "{concepts}" in CLARITY_EVALUATION_PROMPT
        assert "{recent_history}" in CLARITY_EVALUATION_PROMPT

    def test_prompt_has_clarity_scale(self):
        """Valida que prompt define escala de clareza."""
        assert "cristalina" in CLARITY_EVALUATION_PROMPT
        assert "clara" in CLARITY_EVALUATION_PROMPT
        assert "nebulosa" in CLARITY_EVALUATION_PROMPT
        assert "confusa" in CLARITY_EVALUATION_PROMPT

    def test_prompt_mentions_checkpoint(self):
        """Valida que prompt menciona checkpoint."""
        assert "checkpoint" in CLARITY_EVALUATION_PROMPT.lower()

class TestScenarios:
    """Testes de cenarios reais de uso."""

    def test_scenario_well_defined_claim(self):
        """Cenario: Claim bem definido = clareza alta."""
        mock_response = MagicMock()
        mock_response.content = '''{
            "clarity_level": "cristalina",
            "clarity_score": 5,
            "description": "Claim claro e bem fundamentado",
            "needs_checkpoint": false,
            "factors": {
                "claim_definition": "bem definido",
                "coherence": "alta",
                "direction_stability": "estavel"
            },
            "suggestion": null
        }'''

        cognitive_model = {
            "claim": "LLMs aumentam produtividade de desenvolvedores em 30%",
            "proposicoes": [
                {"texto": "Estudos mostram ganho de produtividade", "solidez": 0.85},
                {"texto": "Medicoes feitas em empresas de tecnologia", "solidez": 0.8}
            ],
            "contradictions": [],
            "open_questions": []
        }

        with patch('agents.observer.extractors.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response

            result = evaluate_conversation_clarity(cognitive_model)

        assert result["clarity_level"] == "cristalina"
        assert result["needs_checkpoint"] is False

    def test_scenario_vague_claim(self):
        """Cenario: Claim vago = clareza baixa."""
        mock_response = MagicMock()
        mock_response.content = '''{
            "clarity_level": "confusa",
            "clarity_score": 1,
            "description": "Claim muito vago, dificil entender o foco",
            "needs_checkpoint": true,
            "factors": {
                "claim_definition": "vago",
                "coherence": "baixa",
                "direction_stability": "instavel"
            },
            "suggestion": "Perguntar: o que especificamente voce quer investigar?"
        }'''

        cognitive_model = {
            "claim": "IA e importante",
            "proposicoes": [],
            "contradictions": [],
            "open_questions": ["O que significa importante?", "Qual aspecto de IA?"]
        }

        with patch('agents.observer.extractors.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response

            result = evaluate_conversation_clarity(cognitive_model)

        assert result["clarity_level"] == "confusa"
        assert result["needs_checkpoint"] is True
        assert result["factors"]["claim_definition"] == "vago"

    def test_scenario_direction_changes(self):
        """Cenario: Mudancas de direcao = clareza nebulosa."""
        mock_response = MagicMock()
        mock_response.content = '''{
            "clarity_level": "nebulosa",
            "clarity_score": 2,
            "description": "Conversa mudou de direcao algumas vezes",
            "needs_checkpoint": true,
            "factors": {
                "claim_definition": "parcial",
                "coherence": "media",
                "direction_stability": "instavel"
            },
            "suggestion": "Esclarecer qual dos topicos e o foco principal"
        }'''

        cognitive_model = {
            "claim": "Produtividade em software",
            "proposicoes": [
                {"texto": "LLMs ajudam", "solidez": 0.5},
                {"texto": "Testes sao importantes", "solidez": 0.6}
            ],
            "contradictions": [],
            "open_questions": ["Estamos falando de LLMs ou de testes?"]
        }

        with patch('agents.observer.extractors.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response

            result = evaluate_conversation_clarity(cognitive_model)

        assert result["clarity_level"] == "nebulosa"
        assert result["factors"]["direction_stability"] == "instavel"
        assert result["needs_checkpoint"] is True
