"""
Testes unitarios para deteccao de variacao (Epico 13.1).

Valida a funcao detect_variation() que analisa se mudancas
entre textos sao variacoes (mesma essencia) ou mudancas reais
(essencia diferente).

Usa mocks para LLM - nao faz chamadas reais.

Versao: 1.0
Data: 09/12/2025
"""

import pytest
from unittest.mock import patch, MagicMock
import sys

# Mock chromadb antes de importar modulos que dependem dele
sys.modules['chromadb'] = MagicMock()
sys.modules['chromadb.config'] = MagicMock()

# Import direto do modulo (evita __init__.py com dependencias pesadas)
from agents.observer.extractors import detect_variation
from agents.observer.prompts import VARIATION_DETECTION_PROMPT


class TestDetectVariationBasic:
    """Testes basicos para detect_variation."""

    def test_function_exists(self):
        """Valida que funcao existe e e importavel."""
        from agents.observer.extractors import detect_variation
        assert callable(detect_variation)

    def test_function_signature(self):
        """Valida assinatura da funcao."""
        import inspect
        sig = inspect.signature(detect_variation)
        params = list(sig.parameters.keys())

        assert "previous_text" in params
        assert "new_text" in params
        assert "cognitive_model" in params
        assert "llm" in params

    def test_returns_dict_with_required_fields(self):
        """Valida que retorno contem campos obrigatorios."""
        mock_response = MagicMock()
        mock_response.content = '''{
            "analysis": "Teste de analise",
            "classification": "variation",
            "essence_previous": "essencia anterior",
            "essence_new": "essencia nova",
            "shared_concepts": ["conceito1"],
            "new_concepts": [],
            "reasoning": "justificativa"
        }'''

        with patch('agents.observer.extractors.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response

            result = detect_variation(
                previous_text="texto anterior",
                new_text="texto novo"
            )

        # Campos obrigatorios
        assert "analysis" in result
        assert "classification" in result
        assert "essence_previous" in result
        assert "essence_new" in result
        assert "shared_concepts" in result
        assert "new_concepts" in result
        assert "reasoning" in result


class TestDetectVariationClassification:
    """Testes para classificacao de variacao vs mudanca real."""

    def test_classifies_variation_correctly(self):
        """Testa que variacao e classificada corretamente."""
        mock_response = MagicMock()
        mock_response.content = '''{
            "analysis": "Ambos textos focam em LLMs e produtividade",
            "classification": "variation",
            "essence_previous": "LLMs melhoram produtividade",
            "essence_new": "LLMs melhoram produtividade (quantificado)",
            "shared_concepts": ["LLMs", "produtividade"],
            "new_concepts": [],
            "reasoning": "Mesma essencia, apenas mais especifico"
        }'''

        with patch('agents.observer.extractors.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response

            result = detect_variation(
                previous_text="LLMs aumentam produtividade",
                new_text="LLMs aumentam produtividade em 30%"
            )

        assert result["classification"] == "variation"
        assert "LLMs" in result["shared_concepts"]
        assert len(result["new_concepts"]) == 0

    def test_classifies_real_change_correctly(self):
        """Testa que mudanca real e classificada corretamente."""
        mock_response = MagicMock()
        mock_response.content = '''{
            "analysis": "Textos tratam de assuntos completamente diferentes",
            "classification": "real_change",
            "essence_previous": "Impacto de LLMs em produtividade",
            "essence_new": "Causa de bugs em software",
            "shared_concepts": [],
            "new_concepts": ["bugs", "testes"],
            "reasoning": "Mudanca de foco de LLMs para qualidade de software"
        }'''

        with patch('agents.observer.extractors.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response

            result = detect_variation(
                previous_text="LLMs aumentam produtividade",
                new_text="Bugs sao causados por falta de testes"
            )

        assert result["classification"] == "real_change"
        assert len(result["shared_concepts"]) == 0
        assert len(result["new_concepts"]) > 0

    def test_invalid_classification_defaults_to_variation(self):
        """Testa que classificacao invalida vira 'variation'."""
        mock_response = MagicMock()
        mock_response.content = '''{
            "analysis": "Analise",
            "classification": "invalid_value",
            "essence_previous": "a",
            "essence_new": "b",
            "shared_concepts": [],
            "new_concepts": [],
            "reasoning": ""
        }'''

        with patch('agents.observer.extractors.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response

            result = detect_variation(
                previous_text="texto",
                new_text="outro texto"
            )

        # Deve fazer fallback para variation (conservador)
        assert result["classification"] == "variation"


class TestDetectVariationWithCognitiveModel:
    """Testes com CognitiveModel fornecido."""

    def test_uses_cognitive_model_context(self):
        """Testa que cognitive_model e usado como contexto."""
        mock_response = MagicMock()
        mock_response.content = '''{
            "analysis": "Analise contextual",
            "classification": "variation",
            "essence_previous": "a",
            "essence_new": "b",
            "shared_concepts": ["LLMs"],
            "new_concepts": [],
            "reasoning": "Contexto do modelo cognitivo"
        }'''

        cognitive_model = {
            "claim": "LLMs aumentam produtividade",
            "proposicoes": [
                {"texto": "Equipes usam LLMs", "solidez": 0.7}
            ],
            "concepts_detected": ["LLMs", "produtividade", "equipes"]
        }

        with patch('agents.observer.extractors.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response

            result = detect_variation(
                previous_text="LLMs ajudam equipes",
                new_text="LLMs melhoram produtividade de equipes",
                cognitive_model=cognitive_model
            )

        # Verifica que chamou LLM (contexto foi passado)
        assert mock_invoke.called
        assert result["classification"] == "variation"

    def test_handles_empty_cognitive_model(self):
        """Testa que cognitive_model vazio nao causa erro."""
        mock_response = MagicMock()
        mock_response.content = '''{
            "analysis": "Analise sem contexto",
            "classification": "variation",
            "essence_previous": "a",
            "essence_new": "b",
            "shared_concepts": [],
            "new_concepts": [],
            "reasoning": ""
        }'''

        with patch('agents.observer.extractors.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response

            result = detect_variation(
                previous_text="texto",
                new_text="outro texto",
                cognitive_model={}
            )

        assert "analysis" in result


class TestDetectVariationErrorHandling:
    """Testes para tratamento de erros."""

    def test_handles_llm_error_gracefully(self):
        """Testa que erro no LLM retorna fallback."""
        with patch('agents.observer.extractors.invoke_with_retry') as mock_invoke:
            mock_invoke.side_effect = Exception("LLM timeout")

            result = detect_variation(
                previous_text="texto",
                new_text="outro texto"
            )

        # Deve retornar fallback (variation - conservador)
        assert result["classification"] == "variation"
        assert "Erro" in result["analysis"] or "erro" in result["analysis"].lower()
        assert "Fallback" in result["reasoning"]

    def test_handles_invalid_json_response(self):
        """Testa que JSON invalido retorna fallback."""
        mock_response = MagicMock()
        mock_response.content = "Resposta invalida sem JSON"

        with patch('agents.observer.extractors.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response
            with patch('agents.observer.extractors.extract_json_from_llm_response') as mock_json:
                mock_json.side_effect = Exception("JSON parse error")

                result = detect_variation(
                    previous_text="texto",
                    new_text="outro texto"
                )

        # Deve retornar fallback
        assert result["classification"] == "variation"

    def test_handles_empty_texts(self):
        """Testa que textos vazios sao tratados."""
        mock_response = MagicMock()
        mock_response.content = '''{
            "analysis": "Textos vazios",
            "classification": "variation",
            "essence_previous": "",
            "essence_new": "",
            "shared_concepts": [],
            "new_concepts": [],
            "reasoning": "Sem conteudo para analisar"
        }'''

        with patch('agents.observer.extractors.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response

            result = detect_variation(
                previous_text="",
                new_text=""
            )

        assert "analysis" in result


class TestDetectVariationPrompt:
    """Testes para o prompt de deteccao."""

    def test_prompt_exists(self):
        """Valida que prompt existe."""
        assert VARIATION_DETECTION_PROMPT is not None
        assert len(VARIATION_DETECTION_PROMPT) > 100

    def test_prompt_has_placeholders(self):
        """Valida que prompt tem placeholders necessarios."""
        assert "{previous_text}" in VARIATION_DETECTION_PROMPT
        assert "{new_text}" in VARIATION_DETECTION_PROMPT
        assert "{cognitive_model}" in VARIATION_DETECTION_PROMPT

    def test_prompt_mentions_no_thresholds(self):
        """Valida que prompt enfatiza nao usar thresholds."""
        prompt_lower = VARIATION_DETECTION_PROMPT.lower()
        assert "threshold" in prompt_lower or "NAO use thresholds" in VARIATION_DETECTION_PROMPT

    def test_prompt_is_descriptive_not_prescriptive(self):
        """Valida que prompt e descritivo."""
        assert "DESCRITIVA" in VARIATION_DETECTION_PROMPT or "descritiva" in VARIATION_DETECTION_PROMPT


class TestDetectVariationScenarios:
    """Testes de cenarios reais de uso."""

    def test_scenario_refinement_is_variation(self):
        """Cenario: Refinamento de claim e variacao."""
        mock_response = MagicMock()
        mock_response.content = '''{
            "analysis": "Usuario esta refinando o claim original com mais detalhes",
            "classification": "variation",
            "essence_previous": "IA ajuda desenvolvimento",
            "essence_new": "IA ajuda desenvolvimento (com metricas)",
            "shared_concepts": ["IA", "desenvolvimento"],
            "new_concepts": ["metricas"],
            "reasoning": "Refinamento do mesmo argumento central"
        }'''

        with patch('agents.observer.extractors.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response

            result = detect_variation(
                previous_text="IA ajuda no desenvolvimento de software",
                new_text="IA melhora produtividade de desenvolvedores em 40%"
            )

        assert result["classification"] == "variation"

    def test_scenario_topic_change_is_real_change(self):
        """Cenario: Mudanca de topico e mudanca real."""
        mock_response = MagicMock()
        mock_response.content = '''{
            "analysis": "Usuario mudou completamente o foco da discussao",
            "classification": "real_change",
            "essence_previous": "IA e produtividade",
            "essence_new": "Custos de cloud computing",
            "shared_concepts": [],
            "new_concepts": ["cloud", "custos", "infraestrutura"],
            "reasoning": "Transicao para topico nao relacionado"
        }'''

        with patch('agents.observer.extractors.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response

            result = detect_variation(
                previous_text="IA ajuda no desenvolvimento",
                new_text="Custos de cloud computing sao muito altos"
            )

        assert result["classification"] == "real_change"

    def test_scenario_example_addition_is_variation(self):
        """Cenario: Adicao de exemplo e variacao."""
        mock_response = MagicMock()
        mock_response.content = '''{
            "analysis": "Usuario forneceu exemplo concreto do claim anterior",
            "classification": "variation",
            "essence_previous": "Testes automatizados reduzem bugs",
            "essence_new": "Testes automatizados reduzem bugs (com exemplo)",
            "shared_concepts": ["testes", "bugs", "automacao"],
            "new_concepts": ["CI/CD"],
            "reasoning": "Exemplo suporta o mesmo argumento"
        }'''

        with patch('agents.observer.extractors.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response

            result = detect_variation(
                previous_text="Testes automatizados reduzem bugs",
                new_text="Por exemplo, nosso CI/CD pegou 50 bugs antes do deploy"
            )

        assert result["classification"] == "variation"


class TestDetectVariationEdgeCases:
    """Testes de casos extremos."""

    def test_very_long_texts(self):
        """Testa com textos muito longos."""
        mock_response = MagicMock()
        mock_response.content = '''{
            "analysis": "Textos longos analisados",
            "classification": "variation",
            "essence_previous": "tema longo",
            "essence_new": "tema longo expandido",
            "shared_concepts": ["tema"],
            "new_concepts": [],
            "reasoning": ""
        }'''

        long_text = "Texto muito longo " * 500

        with patch('agents.observer.extractors.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response

            result = detect_variation(
                previous_text=long_text,
                new_text=long_text + " com adicao"
            )

        assert "analysis" in result

    def test_special_characters_in_text(self):
        """Testa com caracteres especiais."""
        mock_response = MagicMock()
        mock_response.content = '''{
            "analysis": "Textos com caracteres especiais",
            "classification": "variation",
            "essence_previous": "formula",
            "essence_new": "formula modificada",
            "shared_concepts": ["matematica"],
            "new_concepts": [],
            "reasoning": ""
        }'''

        with patch('agents.observer.extractors.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response

            result = detect_variation(
                previous_text="E = mc^2 e a formula da energia",
                new_text="E = mc^2 mostra equivalencia massa-energia"
            )

        assert "analysis" in result

    def test_portuguese_text_with_accents(self):
        """Testa com texto em portugues com acentos."""
        mock_response = MagicMock()
        mock_response.content = '''{
            "analysis": "Textos em portugues analisados",
            "classification": "variation",
            "essence_previous": "producao cientifica",
            "essence_new": "producao cientifica brasileira",
            "shared_concepts": ["ciencia", "producao"],
            "new_concepts": ["Brasil"],
            "reasoning": ""
        }'''

        with patch('agents.observer.extractors.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response

            result = detect_variation(
                previous_text="A producao cientifica e importante",
                new_text="A producao cientifica brasileira cresceu muito"
            )

        assert "analysis" in result
