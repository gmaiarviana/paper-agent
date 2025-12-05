"""
Testes unitários para o agente Observador.

Testa:
- ObservadorAPI (interface de consulta)
- ObserverState (estado do processamento)
- Métricas (solidez, completude)
- Nós de processamento (heurísticas POC)

Épico 10.1: Mitose do Orquestrador
Data: 05/12/2025
"""

import pytest
from agents.observer.api import ObservadorAPI, ObserverInsight
from agents.observer.state import ObserverState, create_initial_observer_state
from agents.observer.metrics import (
    calculate_solidez,
    calculate_completude,
    calculate_delta_solidez,
    get_solidez_indicator,
    get_completude_indicator,
    format_metrics_summary,
)
from agents.observer.nodes import (
    process_turn,
    update_cognitive_model_from_observation,
    _extract_concepts_heuristic,
    _extract_claims_heuristic,
)


# =============================================================================
# TESTES DE ObservadorAPI
# =============================================================================

class TestObservadorAPI:
    """Testes para a interface de consulta do Observador."""

    def test_create_empty_api(self):
        """API pode ser criada sem cognitive_model."""
        api = ObservadorAPI()
        assert api.get_solidez() == 0.0
        assert api.get_completude() == 0.0
        assert api.get_concepts() == []
        assert api.has_contradiction() is False

    def test_create_api_with_model(self):
        """API pode ser criada com cognitive_model."""
        model = {
            "claim": "LLMs aumentam produtividade",
            "premises": ["Premissa 1"],
            "assumptions": [],
            "open_questions": [],
            "contradictions": [],
            "solid_grounds": [],
            "context": {},
            "conceitos": ["LLMs", "Produtividade"],
            "solidez_geral": 0.65,
            "completude": 0.70,
        }
        api = ObservadorAPI(model)
        assert api.get_solidez() == 0.65
        assert api.get_completude() == 0.70
        assert api.get_concepts() == ["LLMs", "Produtividade"]

    def test_what_do_you_see_returns_insight(self):
        """what_do_you_see retorna ObserverInsight."""
        api = ObservadorAPI()
        insight = api.what_do_you_see(
            context="Teste",
            question="O que você vê?"
        )
        assert isinstance(insight, ObserverInsight)
        assert insight.insight is not None
        assert 0 <= insight.confidence <= 1
        assert isinstance(insight.evidence, dict)

    def test_what_do_you_see_direction_change(self):
        """what_do_you_see responde sobre mudança de direção."""
        model = {
            "claim": "LLMs",
            "premises": [],
            "assumptions": [],
            "open_questions": [],
            "contradictions": [],
            "solid_grounds": [],
            "context": {},
            "conceitos": ["LLMs", "Bugs"],
            "solidez_geral": 0.5,
            "completude": 0.5,
        }
        api = ObservadorAPI(model)
        insight = api.what_do_you_see(
            context="Usuário mudou de LLMs para bugs",
            question="Conceitos ainda relevantes?"
        )
        # Deve mencionar os conceitos
        assert "LLMs" in insight.insight or "conceitos" in insight.insight.lower()

    def test_what_do_you_see_contradiction(self):
        """what_do_you_see responde sobre contradições."""
        model = {
            "claim": "X",
            "premises": [],
            "assumptions": [],
            "open_questions": [],
            "contradictions": [{"description": "Tensão", "confidence": 0.85}],
            "solid_grounds": [],
            "context": {},
            "conceitos": [],
            "solidez_geral": 0.5,
            "completude": 0.5,
        }
        api = ObservadorAPI(model)
        insight = api.what_do_you_see(
            context="Detectei contradição",
            question="Há inconsistências?"
        )
        assert "contradição" in insight.insight.lower() or "1" in insight.insight

    def test_what_do_you_see_completude(self):
        """what_do_you_see responde sobre completude."""
        model = {
            "claim": "Claim específico com mais de 50 caracteres para teste",
            "premises": ["P1", "P2"],
            "assumptions": [],
            "open_questions": [],
            "contradictions": [],
            "solid_grounds": [],
            "context": {},
            "conceitos": [],
            "solidez_geral": 0.8,
            "completude": 0.85,
        }
        api = ObservadorAPI(model)
        insight = api.what_do_you_see(
            context="Checando profundidade",
            question="Argumento está completo?"
        )
        # Deve mencionar alta completude
        assert "85%" in insight.insight or "completo" in insight.insight.lower()

    def test_has_contradiction_true(self):
        """has_contradiction retorna True quando há contradições."""
        model = {
            "claim": "",
            "premises": [],
            "assumptions": [],
            "open_questions": [],
            "contradictions": [{"description": "Tensão", "confidence": 0.85}],
            "solid_grounds": [],
            "context": {},
            "conceitos": [],
            "solidez_geral": 0.0,
            "completude": 0.0,
        }
        api = ObservadorAPI(model)
        assert api.has_contradiction() is True

    def test_get_current_state(self):
        """get_current_state retorna cópia do modelo."""
        model = {"claim": "X", "conceitos": ["A"]}
        api = ObservadorAPI(model)
        state = api.get_current_state()
        # Deve ser cópia, não referência
        state["claim"] = "Y"
        assert api.get_current_state()["claim"] == "X"

    def test_update_cognitive_model(self):
        """update_cognitive_model atualiza estado interno."""
        api = ObservadorAPI()
        assert api.get_solidez() == 0.0

        new_model = {
            "claim": "Novo claim",
            "premises": [],
            "assumptions": [],
            "open_questions": [],
            "contradictions": [],
            "solid_grounds": [],
            "context": {},
            "conceitos": ["Novo"],
            "solidez_geral": 0.75,
            "completude": 0.80,
        }
        api.update_cognitive_model(new_model)

        assert api.get_solidez() == 0.75
        assert api.get_completude() == 0.80
        assert "Novo" in api.get_concepts()


# =============================================================================
# TESTES DE ObserverState
# =============================================================================

class TestObserverState:
    """Testes para o estado do Observador."""

    def test_create_initial_state(self):
        """Estado inicial é criado corretamente."""
        state = create_initial_observer_state(
            user_input="LLMs aumentam produtividade"
        )
        assert state["user_input"] == "LLMs aumentam produtividade"
        assert state["conversation_history"] == []
        assert state["previous_cognitive_model"] is None
        assert state["extracted_claims"] == []
        assert state["extracted_concepts"] == []
        assert state["solidez_calculated"] == 0.0
        assert state["has_new_concepts"] is False

    def test_create_state_with_history(self):
        """Estado pode ser criado com histórico."""
        history = [{"role": "user", "content": "Olá"}]
        state = create_initial_observer_state(
            user_input="LLMs aumentam produtividade",
            conversation_history=history
        )
        assert len(state["conversation_history"]) == 1

    def test_create_state_with_previous_model(self):
        """Estado pode ser criado com modelo anterior."""
        previous = {"claim": "Claim anterior", "solidez_geral": 0.5}
        state = create_initial_observer_state(
            user_input="Novo input",
            previous_cognitive_model=previous
        )
        assert state["previous_cognitive_model"]["claim"] == "Claim anterior"


# =============================================================================
# TESTES DE MÉTRICAS
# =============================================================================

class TestMetrics:
    """Testes para cálculo de métricas."""

    def test_calculate_solidez_empty(self):
        """Dados vazios têm solidez baixa (mas não zero)."""
        data = {
            "claim": "",
            "premises": [],
            "assumptions": [],
            "open_questions": [],
            "contradictions": [],
            "solid_grounds": [],
        }
        solidez = calculate_solidez(data)
        # 0 claim + 0 premises + 20 assumptions + 20 questions + 15 contradictions
        assert solidez == 0.55

    def test_calculate_solidez_full(self):
        """Dados completos têm solidez alta."""
        data = {
            "claim": "Claim com mais de cinquenta caracteres para teste unitário completo",
            "premises": ["P1", "P2", "P3"],
            "assumptions": [],
            "open_questions": [],
            "contradictions": [],
            "solid_grounds": [],
        }
        solidez = calculate_solidez(data)
        # 20 + 25 + 20 + 20 + 15 = 100
        assert solidez == 1.0

    def test_calculate_completude_empty(self):
        """Dados vazios têm completude baixa."""
        data = {
            "claim": "",
            "premises": [],
            "assumptions": [],
            "open_questions": [],
        }
        completude = calculate_completude(data)
        # 0 claim + 0 premises + 25 questions + 20 assumptions
        assert completude == 0.45

    def test_calculate_completude_full(self):
        """Dados completos têm completude alta."""
        data = {
            "claim": "Claim com mais de cinquenta caracteres para teste unitário completo",
            "premises": ["P1", "P2", "P3"],
            "assumptions": [],
            "open_questions": [],
        }
        completude = calculate_completude(data)
        # 30 + 25 + 25 + 20 = 100
        assert completude == 1.0

    def test_calculate_delta_solidez_significant(self):
        """Delta significativo é detectado."""
        delta = calculate_delta_solidez(0.50, 0.70)
        assert delta["is_significant"] is True
        assert delta["direction"] == "up"
        assert abs(delta["delta"] - 0.20) < 0.001  # Float comparison

    def test_calculate_delta_solidez_not_significant(self):
        """Delta pequeno não é significativo."""
        delta = calculate_delta_solidez(0.50, 0.55)
        assert delta["is_significant"] is False
        assert delta["direction"] == "stable"

    def test_calculate_delta_solidez_down(self):
        """Queda de solidez é detectada."""
        delta = calculate_delta_solidez(0.70, 0.40)
        assert delta["is_significant"] is True
        assert delta["direction"] == "down"

    def test_get_solidez_indicator(self):
        """Indicadores visuais de solidez."""
        assert get_solidez_indicator(0.85) == "🟢"
        assert get_solidez_indicator(0.50) == "🟡"
        assert get_solidez_indicator(0.20) == "🔴"

    def test_get_completude_indicator(self):
        """Indicadores visuais de completude."""
        assert get_completude_indicator(0.90) == "✅"
        assert get_completude_indicator(0.60) == "🔄"
        assert get_completude_indicator(0.30) == "📝"

    def test_format_metrics_summary(self):
        """Formatação de resumo de métricas."""
        summary = format_metrics_summary(0.65, 0.70, 5, 2)
        assert "65%" in summary
        assert "70%" in summary
        assert "5" in summary
        assert "2" in summary


# =============================================================================
# TESTES DE NÓS DE PROCESSAMENTO
# =============================================================================

class TestProcessingNodes:
    """Testes para os nós de processamento do Observador."""

    def test_extract_concepts_heuristic_siglas(self):
        """Extração de conceitos detecta siglas."""
        concepts = _extract_concepts_heuristic("LLMs são úteis para IA e ML")
        concepts_upper = [c.upper() for c in concepts]
        # Siglas devem ser detectadas (em qualquer capitalização)
        assert "LLMS" in concepts_upper or "LLM" in concepts_upper
        assert "IA" in concepts_upper
        assert "ML" in concepts_upper

    def test_extract_concepts_heuristic_known_terms(self):
        """Extração de conceitos detecta termos conhecidos."""
        concepts = _extract_concepts_heuristic("produtividade melhora com tdd")
        concepts_lower = [c.lower() for c in concepts]
        assert "produtividade" in concepts_lower or "Produtividade" in concepts

    def test_extract_concepts_heuristic_ignores_stopwords(self):
        """Extração de conceitos ignora stopwords."""
        concepts = _extract_concepts_heuristic("o que é isso para você")
        assert len(concepts) == 0 or all(c.lower() not in ["o", "que", "é", "isso", "para", "você"] for c in concepts)

    def test_extract_claims_heuristic_declarative(self):
        """Extração de claims detecta frases declarativas."""
        claims = _extract_claims_heuristic(
            "LLMs aumentam produtividade em 30%",
            []
        )
        assert len(claims) >= 1
        assert "LLMs" in claims[0] or "produtividade" in claims[0]

    def test_extract_claims_heuristic_ignores_questions(self):
        """Extração de claims ignora perguntas."""
        claims = _extract_claims_heuristic(
            "O que você acha?",
            []
        )
        # Perguntas não devem ser claims
        assert len(claims) == 0 or "?" not in claims[0]

    def test_process_turn_returns_state(self):
        """process_turn retorna estado atualizado."""
        state = create_initial_observer_state(
            user_input="LLMs aumentam produtividade em equipes de desenvolvimento"
        )
        result = process_turn(state)

        assert "extracted_claims" in result
        assert "extracted_concepts" in result
        assert "solidez_calculated" in result
        assert "completude_calculated" in result
        assert "has_new_concepts" in result

    def test_process_turn_extracts_concepts(self):
        """process_turn extrai conceitos do input."""
        state = create_initial_observer_state(
            user_input="LLMs como Claude e GPT aumentam produtividade"
        )
        result = process_turn(state)

        concepts = result["extracted_concepts"]
        assert len(concepts) > 0
        # Deve detectar pelo menos um dos termos conhecidos
        concepts_lower = [c.lower() for c in concepts]
        assert any(c in concepts_lower for c in ["llms", "claude", "gpt", "produtividade"])

    def test_update_cognitive_model_from_observation(self):
        """update_cognitive_model_from_observation atualiza modelo."""
        observation = {
            "extracted_claims": ["LLMs aumentam produtividade"],
            "extracted_concepts": ["LLMs", "Produtividade"],
            "extracted_fundamentos": [],
            "extracted_contradictions": [],
            "extracted_open_questions": ["Como medir?"],
            "solidez_calculated": 0.65,
            "completude_calculated": 0.70,
        }

        model = update_cognitive_model_from_observation(observation)

        assert model["claim"] == "LLMs aumentam produtividade"
        assert "LLMs" in model["conceitos"]
        assert "Produtividade" in model["conceitos"]
        assert "Como medir?" in model["open_questions"]
        assert model["solidez_geral"] == 0.65
        assert model["completude"] == 0.70

    def test_update_cognitive_model_merges_concepts(self):
        """update_cognitive_model_from_observation faz merge de conceitos."""
        existing = {
            "claim": "Claim anterior",
            "premises": [],
            "assumptions": [],
            "open_questions": [],
            "contradictions": [],
            "solid_grounds": [],
            "context": {},
            "conceitos": ["LLMs"],  # Já existe
            "solidez_geral": 0.5,
            "completude": 0.5,
        }

        observation = {
            "extracted_claims": ["Novo claim"],
            "extracted_concepts": ["LLMs", "Produtividade"],  # LLMs já existe
            "extracted_fundamentos": [],
            "extracted_contradictions": [],
            "extracted_open_questions": [],
            "solidez_calculated": 0.7,
            "completude_calculated": 0.8,
        }

        model = update_cognitive_model_from_observation(observation, existing)

        # Deve ter merge sem duplicar
        assert len([c for c in model["conceitos"] if c.lower() == "llms"]) == 1
        assert "Produtividade" in model["conceitos"]


# =============================================================================
# TESTES DE INTEGRAÇÃO API + NÓS
# =============================================================================

class TestObserverIntegration:
    """Testes de integração entre API e nós."""

    def test_full_observation_flow(self):
        """Fluxo completo: state → process_turn → update_model → API."""
        # 1. Criar estado inicial
        state = create_initial_observer_state(
            user_input="LLMs como Claude Code aumentam produtividade em equipes de desenvolvimento Python"
        )

        # 2. Processar turno
        result = process_turn(state)

        # 3. Atualizar modelo
        model = update_cognitive_model_from_observation(result)

        # 4. Criar API com modelo
        api = ObservadorAPI(model)

        # 5. Consultar API
        insight = api.what_do_you_see(
            context="Checando estado",
            question="O que foi catalogado?"
        )

        # Verificações
        assert api.get_concepts()  # Deve ter conceitos
        assert api.get_solidez() > 0  # Deve ter solidez calculada
        assert insight.insight  # Deve retornar insight
