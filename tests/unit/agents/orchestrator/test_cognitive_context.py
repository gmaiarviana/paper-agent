"""
Testes unitários para _build_cognitive_model_context() do Orquestrador.

Épico 12.2: Valida formatação do cognitive_model para inclusão no prompt.
"""

import pytest
from agents.orchestrator.nodes import _build_cognitive_model_context

class TestBuildCognitiveModelContext:
    """Testes para _build_cognitive_model_context()"""

    def test_empty_cognitive_model_returns_minimal_context(self):
        """Cognitive model vazio retorna contexto mínimo."""
        cm = {}
        result = _build_cognitive_model_context(cm)

        assert "COGNITIVE MODEL DISPONÍVEL" in result
        assert "O Observador analisou" in result

    def test_claim_is_included(self):
        """Afirmação central (claim) é incluída no contexto."""
        cm = {"claim": "LLMs aumentam produtividade"}
        result = _build_cognitive_model_context(cm)

        assert "LLMs aumentam produtividade" in result
        assert "Afirmação central" in result

    def test_proposicoes_are_included_with_solidez(self):
        """Proposições são incluídas com solidez."""
        cm = {
            "proposicoes": [
                {"texto": "Estudos mostram ganho de 30%", "solidez": 0.8},
                {"texto": "Contexto é ambiente corporativo", "solidez": 0.6}
            ]
        }
        result = _build_cognitive_model_context(cm)

        assert "Estudos mostram ganho de 30%" in result
        assert "solidez: 0.80" in result
        assert "Fundamentos" in result

    def test_proposicoes_sorted_by_solidez(self):
        """Proposições são ordenadas por solidez (maior primeiro)."""
        cm = {
            "proposicoes": [
                {"texto": "Prop baixa", "solidez": 0.3},
                {"texto": "Prop alta", "solidez": 0.9},
                {"texto": "Prop media", "solidez": 0.5}
            ]
        }
        result = _build_cognitive_model_context(cm)

        # Verificar que a proposição com maior solidez aparece primeiro
        pos_alta = result.find("Prop alta")
        pos_media = result.find("Prop media")
        pos_baixa = result.find("Prop baixa")

        assert pos_alta < pos_media < pos_baixa

    def test_proposicoes_limited_to_five(self):
        """No máximo 5 proposições são mostradas."""
        cm = {
            "proposicoes": [
                {"texto": f"Proposição {i}", "solidez": 0.5}
                for i in range(10)
            ]
        }
        result = _build_cognitive_model_context(cm)

        assert "... e mais 5 fundamentos" in result

    def test_proposicoes_with_none_solidez(self):
        """Proposições sem solidez mostram 'pendente'."""
        cm = {
            "proposicoes": [
                {"texto": "Proposição sem avaliação", "solidez": None}
            ]
        }
        result = _build_cognitive_model_context(cm)

        assert "solidez: pendente" in result

    def test_concepts_are_included(self):
        """Conceitos detectados são incluídos."""
        cm = {
            "concepts_detected": ["LLM", "produtividade", "automação"]
        }
        result = _build_cognitive_model_context(cm)

        assert "LLM" in result
        assert "produtividade" in result
        assert "Conceitos detectados" in result

    def test_concepts_limited_to_ten(self):
        """No máximo 10 conceitos são mostrados."""
        cm = {
            "concepts_detected": [f"conceito_{i}" for i in range(15)]
        }
        result = _build_cognitive_model_context(cm)

        assert "+5 mais" in result

    def test_contradictions_are_included(self):
        """Contradições detectadas são incluídas."""
        cm = {
            "contradictions": [
                {"description": "Afirma A e não-A", "confidence": 0.85}
            ]
        }
        result = _build_cognitive_model_context(cm)

        assert "Afirma A e não-A" in result
        assert "Contradições detectadas" in result
        assert "85%" in result

    def test_contradictions_limited_to_three(self):
        """No máximo 3 contradições são mostradas."""
        cm = {
            "contradictions": [
                {"description": f"Contradição {i}", "confidence": 0.9}
                for i in range(5)
            ]
        }
        result = _build_cognitive_model_context(cm)

        assert "... e mais 2 contradições" in result

    def test_open_questions_are_included(self):
        """Questões em aberto são incluídas."""
        cm = {
            "open_questions": [
                "Qual a metodologia?",
                "Qual o contexto?"
            ]
        }
        result = _build_cognitive_model_context(cm)

        assert "Qual a metodologia?" in result
        assert "Questões em aberto" in result

    def test_open_questions_limited_to_five(self):
        """No máximo 5 questões são mostradas."""
        cm = {
            "open_questions": [f"Questão {i}?" for i in range(8)]
        }
        result = _build_cognitive_model_context(cm)

        assert "... e mais 3 questões" in result

    def test_metrics_are_included(self):
        """Métricas solidez e completude são incluídas."""
        cm = {
            "overall_solidez": 0.65,
            "overall_completude": 0.40
        }
        result = _build_cognitive_model_context(cm)

        assert "65%" in result
        assert "40%" in result
        assert "Métricas" in result

    def test_solidez_calculated_from_proposicoes_when_missing(self):
        """Solidez é calculada da média das proposições quando não fornecida."""
        cm = {
            "proposicoes": [
                {"texto": "Prop 1", "solidez": 0.8},
                {"texto": "Prop 2", "solidez": 0.6}
            ]
        }
        result = _build_cognitive_model_context(cm)

        # Média de 0.8 e 0.6 = 0.7 = 70%
        assert "70%" in result

    def test_usage_instructions_are_included(self):
        """Instruções de uso do cognitive model são incluídas."""
        cm = {"claim": "Teste"}
        result = _build_cognitive_model_context(cm)

        assert "Use este modelo cognitivo para:" in result
        assert "Identificar lacunas" in result

    def test_complete_cognitive_model(self):
        """Cognitive model completo é formatado corretamente."""
        cm = {
            "claim": "LLMs aumentam produtividade em 30%",
            "proposicoes": [
                {"texto": "Estudo X demonstrou ganho", "solidez": 0.75}
            ],
            "concepts_detected": ["LLM", "produtividade"],
            "contradictions": [
                {"description": "Conflito entre estudos", "confidence": 0.80}
            ],
            "open_questions": ["Qual o contexto?"],
            "overall_solidez": 0.65,
            "overall_completude": 0.50
        }
        result = _build_cognitive_model_context(cm)

        # Verificar todas as seções
        assert "COGNITIVE MODEL DISPONÍVEL" in result
        assert "LLMs aumentam produtividade" in result
        assert "Estudo X demonstrou ganho" in result
        assert "LLM, produtividade" in result
        assert "Conflito entre estudos" in result
        assert "Qual o contexto?" in result
        assert "65%" in result

class TestBuildCognitiveModelContextEdgeCases:
    """Testes de casos extremos."""

    def test_proposicao_as_pydantic_object(self):
        """Funciona com proposições como objetos Pydantic."""
        # Simular objeto Pydantic com atributos
        class FakeProposicao:
            texto = "Proposição objeto"
            solidez = 0.7

        cm = {"proposicoes": [FakeProposicao()]}
        result = _build_cognitive_model_context(cm)

        assert "Proposição objeto" in result

    def test_contradiction_as_string(self):
        """Funciona com contradições como strings simples."""
        cm = {
            "contradictions": [
                "Contradição simples"  # String ao invés de dict
            ]
        }
        result = _build_cognitive_model_context(cm)

        assert "Contradição simples" in result

    def test_very_long_claim_is_included(self):
        """Claims longos são incluídos integralmente."""
        long_claim = "A" * 500
        cm = {"claim": long_claim}
        result = _build_cognitive_model_context(cm)

        assert long_claim in result
