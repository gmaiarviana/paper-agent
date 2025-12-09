"""
Testes unitarios para avaliacao de confusao (Epico 13.2).

Valida a funcao calculate_confusion_level() que avalia qualitativamente
o nivel de confusao/tensao no raciocinio atual da conversa.

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
from agents.observer.extractors import calculate_confusion_level
from agents.observer.prompts import CONFUSION_EVALUATION_PROMPT


class TestCalculateConfusionLevelBasic:
    """Testes basicos para calculate_confusion_level."""

    def test_function_exists(self):
        """Valida que funcao existe e e importavel."""
        from agents.observer.extractors import calculate_confusion_level
        assert callable(calculate_confusion_level)

    def test_function_signature(self):
        """Valida assinatura da funcao."""
        import inspect
        sig = inspect.signature(calculate_confusion_level)
        params = list(sig.parameters.keys())

        assert "cognitive_model" in params
        assert "conversation_history" in params
        assert "llm" in params

    def test_returns_dict_with_required_fields(self):
        """Valida que retorno contem campos obrigatorios."""
        mock_response = MagicMock()
        mock_response.content = '''{
            "confusion_detected": true,
            "description": "Tensao detectada",
            "affected_areas": ["area1"],
            "sources": ["fonte1"],
            "recommendation": "Esclarecer",
            "intervention_suggestion": "Perguntar sobre contexto",
            "severity_qualitative": "moderada"
        }'''

        with patch('agents.observer.extractors.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response

            result = calculate_confusion_level(
                cognitive_model={"claim": "Teste"}
            )

        # Campos obrigatorios
        assert "confusion_detected" in result
        assert "description" in result
        assert "affected_areas" in result
        assert "sources" in result
        assert "recommendation" in result
        assert "intervention_suggestion" in result
        assert "severity_qualitative" in result


class TestConfusionDetection:
    """Testes para deteccao de confusao."""

    def test_detects_confusion_with_contradictions(self):
        """Testa que contradicoes geram confusao."""
        mock_response = MagicMock()
        mock_response.content = '''{
            "confusion_detected": true,
            "description": "Ha contradicoes nao resolvidas entre claims",
            "affected_areas": ["claim principal", "fundamentos"],
            "sources": ["contradicao entre proposicoes"],
            "recommendation": "Esclarecer qual posicao prevalece",
            "intervention_suggestion": "Perguntar: voce quis dizer X ou Y?",
            "severity_qualitative": "moderada"
        }'''

        cognitive_model = {
            "claim": "LLMs aumentam produtividade",
            "contradictions": [
                {"description": "Claim 1 diz que aumenta, Claim 2 diz que diminui"}
            ],
            "proposicoes": [],
            "open_questions": []
        }

        with patch('agents.observer.extractors.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response

            result = calculate_confusion_level(cognitive_model)

        assert result["confusion_detected"] is True
        assert len(result["affected_areas"]) > 0
        assert result["severity_qualitative"] in ("moderada", "significativa")

    def test_no_confusion_with_clear_model(self):
        """Testa que modelo claro nao gera confusao."""
        mock_response = MagicMock()
        mock_response.content = '''{
            "confusion_detected": false,
            "description": "Raciocinio esta fluindo bem",
            "affected_areas": [],
            "sources": [],
            "recommendation": null,
            "intervention_suggestion": null,
            "severity_qualitative": "leve"
        }'''

        cognitive_model = {
            "claim": "LLMs aumentam produtividade",
            "proposicoes": [
                {"texto": "Estudos mostram ganho de 30%", "solidez": 0.8}
            ],
            "contradictions": [],
            "open_questions": []
        }

        with patch('agents.observer.extractors.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response

            result = calculate_confusion_level(cognitive_model)

        assert result["confusion_detected"] is False
        assert result["affected_areas"] == []
        assert result["recommendation"] is None

    def test_confusion_clears_fields_when_false(self):
        """Testa que campos sao limpos quando nao ha confusao."""
        mock_response = MagicMock()
        # LLM retorna confusao como false mas com campos preenchidos
        mock_response.content = '''{
            "confusion_detected": false,
            "description": "Tudo ok",
            "affected_areas": ["area fantasma"],
            "sources": ["fonte fantasma"],
            "recommendation": "Recomendacao indevida",
            "intervention_suggestion": "Sugestao indevida",
            "severity_qualitative": "moderada"
        }'''

        with patch('agents.observer.extractors.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response

            result = calculate_confusion_level({"claim": "Teste"})

        # Deve limpar campos quando confusion_detected=false
        assert result["confusion_detected"] is False
        assert result["affected_areas"] == []
        assert result["sources"] == []
        assert result["recommendation"] is None
        assert result["intervention_suggestion"] is None
        assert result["severity_qualitative"] == "leve"


class TestSeverityQualitative:
    """Testes para severidade qualitativa."""

    def test_severity_leve(self):
        """Testa severidade leve."""
        mock_response = MagicMock()
        mock_response.content = '''{
            "confusion_detected": true,
            "description": "Pequena tensao",
            "affected_areas": ["area menor"],
            "sources": ["questao aberta"],
            "recommendation": "Pode ser esclarecido opcionalmente",
            "intervention_suggestion": null,
            "severity_qualitative": "leve"
        }'''

        with patch('agents.observer.extractors.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response

            result = calculate_confusion_level({"claim": "Teste"})

        assert result["severity_qualitative"] == "leve"

    def test_severity_moderada(self):
        """Testa severidade moderada."""
        mock_response = MagicMock()
        mock_response.content = '''{
            "confusion_detected": true,
            "description": "Tensao que merece atencao",
            "affected_areas": ["claim", "fundamentos"],
            "sources": ["contradicao parcial"],
            "recommendation": "Esclarecer antes de prosseguir",
            "intervention_suggestion": "Perguntar sobre o contexto",
            "severity_qualitative": "moderada"
        }'''

        with patch('agents.observer.extractors.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response

            result = calculate_confusion_level({"claim": "Teste"})

        assert result["severity_qualitative"] == "moderada"

    def test_severity_significativa(self):
        """Testa severidade significativa."""
        mock_response = MagicMock()
        mock_response.content = '''{
            "confusion_detected": true,
            "description": "Confusao importante que bloqueia progresso",
            "affected_areas": ["argumento central", "metodologia"],
            "sources": ["contradicoes multiplas", "questoes criticas"],
            "recommendation": "Necessario resolver antes de continuar",
            "intervention_suggestion": "Pausar e esclarecer pontos fundamentais",
            "severity_qualitative": "significativa"
        }'''

        with patch('agents.observer.extractors.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response

            result = calculate_confusion_level({"claim": "Teste"})

        assert result["severity_qualitative"] == "significativa"

    def test_invalid_severity_defaults_to_leve(self):
        """Testa que severidade invalida vira 'leve'."""
        mock_response = MagicMock()
        mock_response.content = '''{
            "confusion_detected": true,
            "description": "Tensao",
            "affected_areas": ["area"],
            "sources": ["fonte"],
            "recommendation": "Algo",
            "intervention_suggestion": null,
            "severity_qualitative": "invalido"
        }'''

        with patch('agents.observer.extractors.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response

            result = calculate_confusion_level({"claim": "Teste"})

        assert result["severity_qualitative"] == "leve"


class TestCognitiveModelFormatting:
    """Testes para formatacao do CognitiveModel."""

    def test_handles_empty_cognitive_model(self):
        """Testa que modelo vazio nao causa erro."""
        mock_response = MagicMock()
        mock_response.content = '''{
            "confusion_detected": false,
            "description": "Modelo vazio",
            "affected_areas": [],
            "sources": [],
            "recommendation": null,
            "intervention_suggestion": null,
            "severity_qualitative": "leve"
        }'''

        with patch('agents.observer.extractors.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response

            result = calculate_confusion_level({})

        assert "description" in result

    def test_handles_proposicoes_with_solidez(self):
        """Testa formatacao de proposicoes com solidez."""
        mock_response = MagicMock()
        mock_response.content = '''{
            "confusion_detected": false,
            "description": "Proposicoes analisadas",
            "affected_areas": [],
            "sources": [],
            "recommendation": null,
            "intervention_suggestion": null,
            "severity_qualitative": "leve"
        }'''

        cognitive_model = {
            "claim": "Teste",
            "proposicoes": [
                {"texto": "Prop solida", "solidez": 0.8},
                {"texto": "Prop fragil", "solidez": 0.3},
                {"texto": "Prop sem avaliacao", "solidez": None}
            ]
        }

        with patch('agents.observer.extractors.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response

            result = calculate_confusion_level(cognitive_model)

        # Nao deve lancar erro
        assert "description" in result

    def test_handles_conversation_history(self):
        """Testa que historico e passado ao LLM."""
        mock_response = MagicMock()
        mock_response.content = '''{
            "confusion_detected": false,
            "description": "Historico considerado",
            "affected_areas": [],
            "sources": [],
            "recommendation": null,
            "intervention_suggestion": null,
            "severity_qualitative": "leve"
        }'''

        history = [
            {"role": "user", "content": "Mensagem 1"},
            {"role": "assistant", "content": "Resposta 1"},
            {"role": "user", "content": "Mensagem 2"}
        ]

        with patch('agents.observer.extractors.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response

            result = calculate_confusion_level(
                cognitive_model={"claim": "Teste"},
                conversation_history=history
            )

        # Verifica que LLM foi chamado
        assert mock_invoke.called
        assert "description" in result


class TestErrorHandling:
    """Testes para tratamento de erros."""

    def test_handles_llm_error_gracefully(self):
        """Testa que erro no LLM retorna fallback sem confusao."""
        with patch('agents.observer.extractors.invoke_with_retry') as mock_invoke:
            mock_invoke.side_effect = Exception("LLM timeout")

            result = calculate_confusion_level({"claim": "Teste"})

        # Fallback conservador: assume que NAO ha confusao
        assert result["confusion_detected"] is False
        assert "Erro" in result["description"] or "erro" in result["description"].lower()
        assert result["severity_qualitative"] == "leve"

    def test_handles_invalid_json_response(self):
        """Testa que JSON invalido retorna fallback."""
        mock_response = MagicMock()
        mock_response.content = "Resposta invalida sem JSON"

        with patch('agents.observer.extractors.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response
            with patch('agents.observer.extractors.extract_json_from_llm_response') as mock_json:
                mock_json.side_effect = Exception("JSON parse error")

                result = calculate_confusion_level({"claim": "Teste"})

        # Fallback: sem confusao
        assert result["confusion_detected"] is False


class TestPrompt:
    """Testes para o prompt de avaliacao de confusao."""

    def test_prompt_exists(self):
        """Valida que prompt existe."""
        assert CONFUSION_EVALUATION_PROMPT is not None
        assert len(CONFUSION_EVALUATION_PROMPT) > 100

    def test_prompt_has_placeholders(self):
        """Valida que prompt tem placeholders necessarios."""
        assert "{claim}" in CONFUSION_EVALUATION_PROMPT
        assert "{proposicoes}" in CONFUSION_EVALUATION_PROMPT
        assert "{contradictions}" in CONFUSION_EVALUATION_PROMPT
        assert "{open_questions}" in CONFUSION_EVALUATION_PROMPT
        assert "{concepts}" in CONFUSION_EVALUATION_PROMPT
        assert "{recent_history}" in CONFUSION_EVALUATION_PROMPT

    def test_prompt_emphasizes_qualitative(self):
        """Valida que prompt enfatiza analise qualitativa."""
        prompt_lower = CONFUSION_EVALUATION_PROMPT.lower()
        assert "qualitativ" in prompt_lower
        assert "porcentag" in prompt_lower or "scores" in prompt_lower or "numerica" in prompt_lower

    def test_prompt_is_descriptive(self):
        """Valida que prompt e descritivo."""
        assert "DESCRITIVA" in CONFUSION_EVALUATION_PROMPT or "descritiva" in CONFUSION_EVALUATION_PROMPT


class TestScenarios:
    """Testes de cenarios reais de uso."""

    def test_scenario_multiple_open_questions(self):
        """Cenario: Muitas questoes abertas geram confusao."""
        mock_response = MagicMock()
        mock_response.content = '''{
            "confusion_detected": true,
            "description": "Varias questoes fundamentais permanecem sem resposta",
            "affected_areas": ["definicao de metricas", "escopo do estudo"],
            "sources": ["questoes abertas criticas"],
            "recommendation": "Abordar questoes antes de prosseguir",
            "intervention_suggestion": "Vamos esclarecer alguns pontos antes de continuar?",
            "severity_qualitative": "moderada"
        }'''

        cognitive_model = {
            "claim": "LLMs aumentam produtividade",
            "open_questions": [
                "Como medir produtividade?",
                "Qual o baseline de comparacao?",
                "Quais LLMs foram testados?",
                "Em que contexto (empresa, projeto)?"
            ],
            "contradictions": [],
            "proposicoes": []
        }

        with patch('agents.observer.extractors.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response

            result = calculate_confusion_level(cognitive_model)

        assert result["confusion_detected"] is True
        assert result["recommendation"] is not None

    def test_scenario_fragile_propositions(self):
        """Cenario: Proposicoes frageis indicam confusao."""
        mock_response = MagicMock()
        mock_response.content = '''{
            "confusion_detected": true,
            "description": "Fundamentos do argumento estao frageis",
            "affected_areas": ["base argumentativa"],
            "sources": ["proposicoes com solidez baixa"],
            "recommendation": "Fortalecer fundamentos antes de prosseguir",
            "intervention_suggestion": "Podemos explorar mais esses pontos?",
            "severity_qualitative": "leve"
        }'''

        cognitive_model = {
            "claim": "IA substituira programadores",
            "proposicoes": [
                {"texto": "IA ja escreve codigo", "solidez": 0.3},
                {"texto": "Programadores serao desnecessarios", "solidez": 0.2}
            ],
            "contradictions": [],
            "open_questions": []
        }

        with patch('agents.observer.extractors.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response

            result = calculate_confusion_level(cognitive_model)

        assert result["confusion_detected"] is True
        assert "frageis" in result["description"].lower() or "fundamentos" in result["description"].lower()

    def test_scenario_clear_well_structured_argument(self):
        """Cenario: Argumento bem estruturado sem confusao."""
        mock_response = MagicMock()
        mock_response.content = '''{
            "confusion_detected": false,
            "description": "Argumento esta bem estruturado e coerente",
            "affected_areas": [],
            "sources": [],
            "recommendation": null,
            "intervention_suggestion": null,
            "severity_qualitative": "leve"
        }'''

        cognitive_model = {
            "claim": "Testes automatizados reduzem bugs em producao",
            "proposicoes": [
                {"texto": "Testes detectam bugs antes do deploy", "solidez": 0.9},
                {"texto": "CI/CD executa testes automaticamente", "solidez": 0.85},
                {"texto": "Estudos mostram reducao de 40%", "solidez": 0.8}
            ],
            "contradictions": [],
            "open_questions": [],
            "concepts_detected": ["testes", "CI/CD", "bugs", "producao"]
        }

        with patch('agents.observer.extractors.invoke_with_retry') as mock_invoke:
            mock_invoke.return_value = mock_response

            result = calculate_confusion_level(cognitive_model)

        assert result["confusion_detected"] is False
        assert result["severity_qualitative"] == "leve"
