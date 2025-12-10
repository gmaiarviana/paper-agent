"""
Testes unitarios para Clarification (Epico 14).

Valida modelos Pydantic e funcoes de clarification de forma isolada,
sem chamadas LLM reais. Usa mocks para extratores.

"""

import pytest
from unittest.mock import patch, MagicMock

from agents.models.clarification import (
    ClarificationNeed,
    ClarificationContext,
    ClarificationTimingDecision,
    ClarificationResponse,
    ClarificationUpdates,
    QuestionSuggestion,
)

class TestClarificationModels:
    """Testes para modelos Pydantic de clarification."""

    def test_clarification_need_creation(self):
        """Testa criacao de ClarificationNeed."""
        need = ClarificationNeed(
            needs_clarification=True,
            clarification_type="contradiction",
            description="Usuario disse X e Y que parecem contraditorios",
            suggested_approach="Explorar contextos diferentes",
            priority="high"
        )

        assert need.needs_clarification is True
        assert need.clarification_type == "contradiction"
        assert need.priority == "high"
        assert need.turns_persisted == 0
        assert need.id is not None  # UUID gerado automaticamente

    def test_clarification_need_no_clarification(self):
        """Testa ClarificationNeed quando nao precisa esclarecimento."""
        need = ClarificationNeed(
            needs_clarification=False,
            clarification_type="confusion",
            description="Conversa fluindo bem"
            # suggested_approach omitido (default=None)
        )

        assert need.needs_clarification is False
        assert need.priority == "medium"  # Default
        assert need.suggested_approach is None

    def test_clarification_context_creation(self):
        """Testa criacao de ClarificationContext."""
        context = ClarificationContext(
            proposicoes=["LLMs aumentam produtividade", "LLMs aumentam bugs"],
            contradictions=["Produtividade vs bugs"],
            open_questions=["Em que contexto?"],
            claim_excerpt="LLMs impactam desenvolvimento"
        )

        assert len(context.proposicoes) == 2
        assert len(context.contradictions) == 1
        assert context.claim_excerpt == "LLMs impactam desenvolvimento"

    def test_clarification_context_empty(self):
        """Testa ClarificationContext vazio."""
        context = ClarificationContext()

        assert context.proposicoes == []
        assert context.contradictions == []
        assert context.open_questions == []
        assert context.claim_excerpt is None

    def test_timing_decision_should_ask(self):
        """Testa ClarificationTimingDecision quando deve perguntar."""
        decision = ClarificationTimingDecision(
            should_ask=True,
            reason="Contradicao persiste ha 3 turnos",
            delay_turns=0,
            urgency="high"
        )

        assert decision.should_ask is True
        assert decision.delay_turns == 0
        assert decision.urgency == "high"

    def test_timing_decision_should_wait(self):
        """Testa ClarificationTimingDecision quando deve esperar."""
        decision = ClarificationTimingDecision(
            should_ask=False,
            reason="Usuario fluindo bem",
            delay_turns=2,
            urgency="low"
        )

        assert decision.should_ask is False
        assert decision.delay_turns == 2

    def test_clarification_response_resolved(self):
        """Testa ClarificationResponse quando esclarecimento resolvido."""
        response = ClarificationResponse(
            resolution_status="resolved",
            summary="Usuario esclareceu que X e Y se aplicam em contextos diferentes",
            needs_followup=False
        )

        assert response.resolution_status == "resolved"
        assert response.needs_followup is False
        assert response.followup_suggestion is None

    def test_clarification_response_with_updates(self):
        """Testa ClarificationResponse com atualizacoes."""
        updates = ClarificationUpdates(
            proposicoes_to_add=["Nova proposicao esclarecida"],
            contradictions_to_resolve=[0],
            open_questions_to_close=[1, 2]
        )

        response = ClarificationResponse(
            resolution_status="resolved",
            summary="Esclarecimento completo",
            updates=updates,
            needs_followup=False
        )

        assert len(response.updates.proposicoes_to_add) == 1
        assert response.updates.contradictions_to_resolve == [0]
        assert response.updates.open_questions_to_close == [1, 2]

    def test_clarification_response_needs_followup(self):
        """Testa ClarificationResponse quando precisa acompanhamento."""
        response = ClarificationResponse(
            resolution_status="partially_resolved",
            summary="Algumas duvidas permanecem",
            needs_followup=True,
            followup_suggestion="Perguntar sobre contexto especifico"
        )

        assert response.resolution_status == "partially_resolved"
        assert response.needs_followup is True
        assert response.followup_suggestion is not None

    def test_question_suggestion_contradiction(self):
        """Testa QuestionSuggestion para contradicao."""
        suggestion = QuestionSuggestion(
            question_text="Voce mencionou X e Y. Eles se aplicam em situacoes diferentes?",
            target_type="contradiction",
            related_proposicoes=["X", "Y"],
            expected_outcome="Esclarecimento do contexto",
            tone_guidance="Curiosidade genuina"
        )

        assert suggestion.target_type == "contradiction"
        assert len(suggestion.related_proposicoes) == 2
        assert "Curiosidade" in suggestion.tone_guidance

    def test_question_suggestion_gap(self):
        """Testa QuestionSuggestion para gap."""
        suggestion = QuestionSuggestion(
            question_text="O que te levou a essa conclusao?",
            target_type="gap",
            expected_outcome="Evidencia empirica"
        )

        assert suggestion.target_type == "gap"
        assert suggestion.related_proposicoes == []  # Default

    def test_clarification_need_to_dict(self):
        """Testa serializacao de ClarificationNeed."""
        need = ClarificationNeed(
            needs_clarification=True,
            clarification_type="gap",
            description="Falta evidencia",
            suggested_approach="Perguntar sobre experiencia"
        )

        data = need.to_dict()

        assert data["needs_clarification"] is True
        assert data["clarification_type"] == "gap"
        assert "id" in data

    def test_clarification_need_from_dict(self):
        """Testa desserializacao de ClarificationNeed."""
        data = {
            "id": "test-id-123",
            "needs_clarification": True,
            "clarification_type": "contradiction",
            "description": "Teste",
            "suggested_approach": "Perguntar",
            "priority": "high",
            "turn_detected": 5,
            "turns_persisted": 2
        }

        need = ClarificationNeed.from_dict(data)

        assert need.id == "test-id-123"
        assert need.turn_detected == 5
        assert need.turns_persisted == 2

class TestShouldAskClarification:
    """Testes para funcao should_ask_clarification."""

    def test_no_clarification_needed(self):
        """Testa quando nao precisa esclarecimento."""
        from agents.observer.clarification import should_ask_clarification

        need = ClarificationNeed(
            needs_clarification=False,
            clarification_type="confusion",
            description="Sem necessidade"
            # suggested_approach omitido (default=None)
        )

        decision = should_ask_clarification(
            clarification_need=need,
            turn_history=[],
            current_turn=5
        )

        assert decision.should_ask is False
        assert "nao ha necessidade" in decision.reason.lower()

    def test_high_priority_always_asks(self):
        """Testa que prioridade alta sempre pergunta."""
        from agents.observer.clarification import should_ask_clarification

        need = ClarificationNeed(
            needs_clarification=True,
            clarification_type="contradiction",
            description="Contradicao critica",
            suggested_approach="Perguntar",
            priority="high"
        )

        decision = should_ask_clarification(
            clarification_need=need,
            turn_history=[],
            current_turn=5,
            turns_since_last_question=3
        )

        assert decision.should_ask is True
        assert decision.urgency == "high"

    def test_contradiction_persists_should_ask(self):
        """Testa que contradicao persistente deve perguntar."""
        from agents.observer.clarification import should_ask_clarification

        need = ClarificationNeed(
            needs_clarification=True,
            clarification_type="contradiction",
            description="Contradicao entre X e Y",
            suggested_approach="Explorar contextos",
            priority="medium",
            turns_persisted=3  # Persiste ha 3 turnos
        )

        decision = should_ask_clarification(
            clarification_need=need,
            turn_history=[],
            current_turn=5,
            turns_since_last_question=5
        )

        assert decision.should_ask is True
        assert "persiste" in decision.reason.lower()

    def test_user_flowing_should_not_interrupt(self):
        """Testa que usuario fluindo bem nao deve ser interrompido."""
        from agents.observer.clarification import should_ask_clarification

        need = ClarificationNeed(
            needs_clarification=True,
            clarification_type="gap",
            description="Gap menor",
            suggested_approach="Perguntar eventualmente",
            priority="low",
            turns_persisted=1
        )

        decision = should_ask_clarification(
            clarification_need=need,
            turn_history=[],
            current_turn=5,
            turns_since_last_question=5,
            is_user_flowing=True
        )

        assert decision.should_ask is False
        assert "fluindo" in decision.reason.lower()

    def test_recent_question_should_wait(self):
        """Testa que deve esperar apos pergunta recente."""
        from agents.observer.clarification import should_ask_clarification

        need = ClarificationNeed(
            needs_clarification=True,
            clarification_type="contradiction",
            description="Contradicao",
            suggested_approach="Perguntar",
            priority="medium"
        )

        decision = should_ask_clarification(
            clarification_need=need,
            turn_history=[],
            current_turn=5,
            turns_since_last_question=1  # Perguntou ha 1 turno
        )

        assert decision.should_ask is False
        assert decision.delay_turns > 0

class TestUpdateClarificationPersistence:
    """Testes para funcao update_clarification_persistence."""

    def test_increment_persistence(self):
        """Testa incremento de turnos persistidos."""
        from agents.observer.clarification import update_clarification_persistence

        need = ClarificationNeed(
            needs_clarification=True,
            clarification_type="contradiction",
            description="Contradicao",
            suggested_approach="Perguntar",
            turns_persisted=2
        )

        updated = update_clarification_persistence(need, still_relevant=True)

        assert updated.turns_persisted == 3
        assert updated.needs_clarification is True

    def test_reset_when_not_relevant(self):
        """Testa reset quando nao e mais relevante."""
        from agents.observer.clarification import update_clarification_persistence

        need = ClarificationNeed(
            needs_clarification=True,
            clarification_type="contradiction",
            description="Contradicao",
            suggested_approach="Perguntar",
            turns_persisted=5
        )

        updated = update_clarification_persistence(need, still_relevant=False)

        assert updated.turns_persisted == 0
        assert updated.needs_clarification is False

class TestClarificationSummaryForTimeline:
    """Testes para funcao get_clarification_summary_for_timeline."""

    def test_resolved_summary(self):
        """Testa resumo para esclarecimento resolvido."""
        from agents.observer.clarification import get_clarification_summary_for_timeline

        response = ClarificationResponse(
            resolution_status="resolved",
            summary="Usuario explicou os contextos diferentes"
        )

        summary = get_clarification_summary_for_timeline(response, "contradiction")

        assert "Tensao esclarecida" in summary
        assert "Usuario explicou" in summary

    def test_partially_resolved_summary(self):
        """Testa resumo para esclarecimento parcial."""
        from agents.observer.clarification import get_clarification_summary_for_timeline

        response = ClarificationResponse(
            resolution_status="partially_resolved",
            summary="Algumas duvidas permanecem"
        )

        summary = get_clarification_summary_for_timeline(response, "gap")

        assert "parcialmente" in summary.lower()

    def test_unresolved_summary(self):
        """Testa resumo para esclarecimento nao resolvido."""
        from agents.observer.clarification import get_clarification_summary_for_timeline

        response = ClarificationResponse(
            resolution_status="unresolved",
            summary="Resposta tangencial"
        )

        summary = get_clarification_summary_for_timeline(response, "confusion")

        assert "pendente" in summary.lower()

class TestClarificationEventsModels:
    """Testes para modelos de eventos de clarification."""

    def test_clarification_requested_event(self):
        """Testa ClarificationRequestedEvent."""
        from utils.event_models import ClarificationRequestedEvent

        event = ClarificationRequestedEvent(
            session_id="session-123",
            turn_number=5,
            clarification_type="contradiction",
            question="Voce mencionou X e Y. Eles se aplicam em contextos diferentes?",
            priority="medium",
            related_context={"proposicoes": ["X", "Y"]}
        )

        assert event.event_type == "clarification_requested"
        assert event.turn_number == 5
        assert event.clarification_type == "contradiction"
        assert "X e Y" in event.question

    def test_clarification_resolved_event(self):
        """Testa ClarificationResolvedEvent."""
        from utils.event_models import ClarificationResolvedEvent

        event = ClarificationResolvedEvent(
            session_id="session-123",
            turn_number=6,
            clarification_type="contradiction",
            resolution_status="resolved",
            summary="Usuario esclareceu os contextos",
            updates_made={"contradictions_resolved": 1}
        )

        assert event.event_type == "clarification_resolved"
        assert event.resolution_status == "resolved"
        assert event.updates_made["contradictions_resolved"] == 1

class TestIdentifyClarificationNeedsWithMock:
    """Testes para identify_clarification_needs com mock do LLM."""

    @patch('agents.observer.clarification.invoke_with_retry')
    @patch('agents.observer.clarification._get_llm')
    def test_identifies_contradiction(self, mock_get_llm, mock_invoke):
        """Testa identificacao de contradicao com mock."""
        from agents.observer.clarification import identify_clarification_needs

        # Mock da resposta do LLM
        mock_response = MagicMock()
        mock_response.content = '''```json
        {
            "needs_clarification": true,
            "clarification_type": "contradiction",
            "description": "Usuario disse X e Y que parecem contraditorios",
            "relevant_context": {
                "proposicoes": ["X", "Y"],
                "contradictions": ["X vs Y"]
            },
            "suggested_approach": "Explorar contextos diferentes",
            "priority": "high",
            "reasoning": "Contradicao clara detectada"
        }
        ```'''
        mock_invoke.return_value = mock_response

        cognitive_model = {
            "claim": "LLMs impactam desenvolvimento",
            "proposicoes": [
                {"texto": "LLMs aumentam produtividade", "solidez": 0.7},
                {"texto": "LLMs aumentam bugs", "solidez": 0.6}
            ],
            "contradictions": [{"description": "Produtividade vs bugs"}],
            "open_questions": []
        }

        need = identify_clarification_needs(cognitive_model, turn_number=5)

        assert need.needs_clarification is True
        assert need.clarification_type == "contradiction"
        assert need.priority == "high"
        assert need.turn_detected == 5

    @patch('agents.observer.clarification.invoke_with_retry')
    @patch('agents.observer.clarification._get_llm')
    def test_no_clarification_when_flowing(self, mock_get_llm, mock_invoke):
        """Testa que nao identifica necessidade quando conversa flui bem."""
        from agents.observer.clarification import identify_clarification_needs

        mock_response = MagicMock()
        mock_response.content = '''```json
        {
            "needs_clarification": false,
            "clarification_type": null,
            "description": "Conversa fluindo bem, sem necessidade de esclarecimento",
            "relevant_context": {},
            "suggested_approach": null,
            "priority": null,
            "reasoning": "Usuario adicionando proposicoes consistentes"
        }
        ```'''
        mock_invoke.return_value = mock_response

        cognitive_model = {
            "claim": "LLMs aumentam produtividade",
            "proposicoes": [
                {"texto": "Equipes usam LLMs", "solidez": 0.8}
            ],
            "contradictions": [],
            "open_questions": []
        }

        need = identify_clarification_needs(cognitive_model, turn_number=3)

        assert need.needs_clarification is False

class TestGenerateContradictionQuestion:
    """Testes para generate_contradiction_question com mock do LLM."""

    @patch('agents.observer.clarification.invoke_with_retry')
    @patch('agents.observer.clarification._get_llm')
    def test_generates_contextual_question(self, mock_get_llm, mock_invoke):
        """Testa que gera pergunta contextual sobre contradicao."""
        from agents.observer.clarification import generate_contradiction_question

        mock_response = MagicMock()
        mock_response.content = '''```json
        {
            "question": "Voce mencionou que LLMs aumentam produtividade e tambem aumentam bugs. Esses efeitos acontecem em contextos diferentes?",
            "expected_outcomes": [
                "Esclarecimento sobre contextos especificos",
                "Diferenciacao de cenarios"
            ],
            "tone_check": "Curiosidade genuina, sem julgamento"
        }
        ```'''
        mock_invoke.return_value = mock_response

        contradiction = {
            "description": "LLMs aumentam produtividade vs LLMs aumentam bugs",
            "confidence": 0.85
        }
        propositions = [
            {"texto": "LLMs aumentam produtividade em 30%", "solidez": 0.7},
            {"texto": "LLMs aumentam quantidade de bugs", "solidez": 0.6}
        ]

        suggestion = generate_contradiction_question(
            contradiction, propositions, "Usuario discutindo impacto de LLMs"
        )

        assert suggestion.question_text is not None
        assert len(suggestion.question_text) > 0
        assert suggestion.target_type == "contradiction"
        assert "Curiosidade" in suggestion.tone_guidance

    @patch('agents.observer.clarification.invoke_with_retry')
    @patch('agents.observer.clarification._get_llm')
    def test_fallback_on_error(self, mock_get_llm, mock_invoke):
        """Testa fallback quando LLM falha."""
        from agents.observer.clarification import generate_contradiction_question

        mock_invoke.side_effect = Exception("LLM error")

        contradiction = {"description": "Teste"}
        propositions = []

        suggestion = generate_contradiction_question(
            contradiction, propositions, "contexto"
        )

        # Deve retornar fallback generico
        assert suggestion.question_text is not None
        assert suggestion.target_type == "contradiction"

class TestSuggestQuestionForGap:
    """Testes para suggest_question_for_gap com mock do LLM."""

    @patch('agents.observer.clarification.invoke_with_retry')
    @patch('agents.observer.clarification._get_llm')
    def test_suggests_question_for_gap(self, mock_get_llm, mock_invoke):
        """Testa sugestao de pergunta para gap."""
        from agents.observer.clarification import suggest_question_for_gap

        mock_response = MagicMock()
        mock_response.content = '''```json
        {
            "question": "Voce tem algum dado ou experiencia que demonstre esse aumento de produtividade?",
            "connection_to_claim": "Evidencia empirica fortaleceria o argumento central"
        }
        ```'''
        mock_invoke.return_value = mock_response

        cognitive_model = {
            "claim": "LLMs aumentam produtividade em 30%",
            "proposicoes": [{"texto": "Equipes de tech usam LLMs", "solidez": 0.6}],
            "open_questions": [
                "Qual baseline de comparacao?",
                "Qual a metodologia de medicao?"
            ],
            "contradictions": []
        }

        suggestion = suggest_question_for_gap(
            cognitive_model, gap_index=0, conversation_context="Discussao sobre impacto"
        )

        assert suggestion is not None
        assert suggestion.question_text is not None
        assert suggestion.target_type == "gap"

    def test_returns_none_when_no_gaps(self):
        """Testa que retorna None quando nao ha gaps."""
        from agents.observer.clarification import suggest_question_for_gap

        cognitive_model = {
            "claim": "LLMs aumentam produtividade",
            "proposicoes": [],
            "open_questions": [],  # Sem gaps
            "contradictions": []
        }

        suggestion = suggest_question_for_gap(cognitive_model)

        assert suggestion is None

class TestAnalyzeClarificationResponse:
    """Testes para analyze_clarification_response com mock do LLM."""

    @patch('agents.observer.clarification.invoke_with_retry')
    @patch('agents.observer.clarification._get_llm')
    def test_analyzes_resolved_response(self, mock_get_llm, mock_invoke):
        """Testa analise de resposta que resolve esclarecimento."""
        from agents.observer.clarification import analyze_clarification_response

        mock_response = MagicMock()
        mock_response.content = '''```json
        {
            "resolution_status": "resolved",
            "summary": "Usuario esclareceu que produtividade aumenta em tarefas simples",
            "updates": {
                "proposicoes_to_add": ["Produtividade aumenta em tarefas simples"],
                "contradictions_to_resolve": [0]
            },
            "needs_followup": false
        }
        ```'''
        mock_invoke.return_value = mock_response

        original_need = ClarificationNeed(
            needs_clarification=True,
            clarification_type="contradiction",
            description="Produtividade vs bugs"
        )

        cognitive_model = {
            "claim": "LLMs impactam desenvolvimento",
            "proposicoes": [],
            "contradictions": [{"description": "Produtividade vs bugs"}],
            "open_questions": []
        }

        response = analyze_clarification_response(
            user_response="Produtividade aumenta em tarefas simples, bugs em tarefas complexas",
            question_asked="Esses efeitos acontecem em contextos diferentes?",
            original_need=original_need,
            cognitive_model=cognitive_model
        )

        assert response.resolution_status == "resolved"
        assert response.needs_followup is False
        assert len(response.updates.proposicoes_to_add) > 0

    @patch('agents.observer.clarification.invoke_with_retry')
    @patch('agents.observer.clarification._get_llm')
    def test_analyzes_partial_response(self, mock_get_llm, mock_invoke):
        """Testa analise de resposta parcialmente resolvida."""
        from agents.observer.clarification import analyze_clarification_response

        mock_response = MagicMock()
        mock_response.content = '''```json
        {
            "resolution_status": "partially_resolved",
            "summary": "Usuario deu alguma clareza mas duvidas permanecem",
            "updates": {},
            "needs_followup": true,
            "followup_suggestion": "Perguntar sobre contexto especifico de tarefas complexas"
        }
        ```'''
        mock_invoke.return_value = mock_response

        original_need = ClarificationNeed(
            needs_clarification=True,
            clarification_type="gap",
            description="Falta evidencia"
        )

        response = analyze_clarification_response(
            user_response="Acho que sim, mas nao tenho certeza",
            question_asked="Voce tem dados?",
            original_need=original_need,
            cognitive_model={"claim": "", "proposicoes": [], "contradictions": [], "open_questions": []}
        )

        assert response.resolution_status == "partially_resolved"
        assert response.needs_followup is True
        assert response.followup_suggestion is not None

class TestClarificationTypes:
    """Testes para diferentes tipos de clarification."""

    def test_all_clarification_types_valid(self):
        """Testa que todos os tipos de clarification sao validos."""
        valid_types = ["contradiction", "gap", "confusion", "direction_change"]

        for ctype in valid_types:
            need = ClarificationNeed(
                needs_clarification=True,
                clarification_type=ctype,
                description=f"Teste {ctype}"
            )
            assert need.clarification_type == ctype

    def test_all_priority_levels_valid(self):
        """Testa que todos os niveis de prioridade sao validos."""
        valid_priorities = ["high", "medium", "low"]

        for priority in valid_priorities:
            need = ClarificationNeed(
                needs_clarification=True,
                clarification_type="gap",
                description="Teste",
                priority=priority
            )
            assert need.priority == priority

    def test_all_resolution_statuses_valid(self):
        """Testa que todos os status de resolucao sao validos."""
        valid_statuses = ["resolved", "partially_resolved", "unresolved"]

        for status in valid_statuses:
            response = ClarificationResponse(
                resolution_status=status,
                summary="Teste"
            )
            assert response.resolution_status == status

class TestClarificationUpdates:
    """Testes para ClarificationUpdates."""

    def test_empty_updates(self):
        """Testa ClarificationUpdates vazio."""
        updates = ClarificationUpdates()

        assert updates.proposicoes_to_add == []
        assert updates.proposicoes_to_update == {}
        assert updates.contradictions_to_resolve == []
        assert updates.open_questions_to_close == []
        assert updates.context_to_add == {}

    def test_full_updates(self):
        """Testa ClarificationUpdates com todos os campos."""
        updates = ClarificationUpdates(
            proposicoes_to_add=["Nova proposicao 1", "Nova proposicao 2"],
            proposicoes_to_update={"id1": {"texto": "Atualizado", "solidez": 0.9}},
            contradictions_to_resolve=[0, 1],
            open_questions_to_close=[2],
            context_to_add={"domain": "tecnologia"}
        )

        assert len(updates.proposicoes_to_add) == 2
        assert "id1" in updates.proposicoes_to_update
        assert updates.contradictions_to_resolve == [0, 1]
        assert updates.open_questions_to_close == [2]
        assert updates.context_to_add["domain"] == "tecnologia"
