"""
Testes de integração para o Observer no fluxo multi-agente.

Épico 12: Valida que o Observer é integrado corretamente ao grafo,
processando turnos em background e publicando eventos.
"""

import pytest
import time
from unittest.mock import MagicMock, patch
from langchain_core.messages import HumanMessage, AIMessage

class TestObserverIntegrationFlow:
    """Testes de integração do Observer no fluxo do sistema."""

    @pytest.fixture
    def mock_llm_response(self):
        """Resposta simulada do LLM para o orchestrator."""
        return {
            "reasoning": "Análise do input do usuário",
            "focal_argument": {
                "intent": "compare",
                "subject": "LLMs vs desenvolvedores",
                "population": "empresas de tecnologia",
                "metrics": "not specified",
                "article_type": "empirical"
            },
            "cognitive_model": {
                "claim": "LLMs aumentam produtividade de desenvolvedores",
                "proposicoes": [
                    {"texto": "Estudo X mostrou ganho de 30%", "solidez": 0.75}
                ],
                "open_questions": ["Qual o contexto específico?"],
                "contradictions": [],
                "solid_grounds": []
            },
            "next_step": "explore",
            "message": "Interessante! Me conta mais sobre o contexto."
        }

    def test_orchestrator_includes_cognitive_model_in_context(self):
        """Orquestrador inclui cognitive_model no contexto quando disponível."""
        from core.agents.orchestrator.nodes import _build_context, _build_cognitive_model_context
        from core.agents.orchestrator.state import create_initial_multi_agent_state

        # Criar estado com cognitive_model
        state = create_initial_multi_agent_state(
            user_input="LLMs aumentam produtividade",
            session_id="test-session"
        )
        state["cognitive_model"] = {
            "claim": "LLMs aumentam produtividade",
            "proposicoes": [
                {"texto": "Estudo demonstrou ganho", "solidez": 0.8}
            ],
            "concepts_detected": ["LLM", "produtividade"]
        }

        # Construir contexto
        context = _build_context(state)

        # Verificar que cognitive_model está no contexto
        assert "COGNITIVE MODEL DISPONÍVEL" in context
        assert "LLMs aumentam produtividade" in context
        assert "Estudo demonstrou ganho" in context

    def test_context_excludes_empty_cognitive_model(self):
        """Contexto não inclui seção de cognitive_model se vazio."""
        from core.agents.orchestrator.nodes import _build_context
        from core.agents.orchestrator.state import create_initial_multi_agent_state

        # Criar estado sem cognitive_model
        state = create_initial_multi_agent_state(
            user_input="LLMs aumentam produtividade",
            session_id="test-session"
        )
        state["cognitive_model"] = {}

        # Construir contexto
        context = _build_context(state)

        # Verificar que seção não está presente
        assert "COGNITIVE MODEL DISPONÍVEL" not in context

    def test_context_excludes_cognitive_model_without_claim(self):
        """Contexto não inclui seção se cognitive_model não tem claim."""
        from core.agents.orchestrator.nodes import _build_context
        from core.agents.orchestrator.state import create_initial_multi_agent_state

        # Criar estado com cognitive_model vazio (sem claim)
        state = create_initial_multi_agent_state(
            user_input="LLMs aumentam produtividade",
            session_id="test-session"
        )
        state["cognitive_model"] = {
            "claim": "",
            "proposicoes": []
        }

        # Construir contexto
        context = _build_context(state)

        # Verificar que seção não está presente
        assert "COGNITIVE MODEL DISPONÍVEL" not in context

class TestObserverEventPublishing:
    """Testes de publicação de eventos do Observer."""

    def test_cognitive_model_updated_event_structure(self):
        """Evento cognitive_model_updated tem estrutura correta."""
        from core.utils.event_bus import get_event_bus

        bus = get_event_bus()

        # Publicar evento
        bus.publish_cognitive_model_updated(
            session_id="test-session",
            turn_number=1,
            solidez=0.65,
            completude=0.40,
            claims_count=1,
            proposicoes_count=3,
            concepts_count=5,
            open_questions_count=2,
            contradictions_count=0,
            is_mature=False,
            metadata={
                "processing_time_ms": 1500,
                "observer_version": "12.1"
            }
        )

        # Recuperar eventos
        events = bus.get_session_events("test-session")
        cm_events = [e for e in events if e.get("event_type") == "cognitive_model_updated"]

        assert len(cm_events) >= 1
        event = cm_events[-1]

        # Verificar campos
        assert event["session_id"] == "test-session"
        assert event["turn_number"] == 1
        assert event["solidez"] == 0.65
        assert event["completude"] == 0.40
        assert event["is_mature"] == False

    def test_multiple_turn_events_accumulate(self):
        """Múltiplos turnos geram eventos acumulados."""
        from core.utils.event_bus import get_event_bus

        bus = get_event_bus()
        session_id = f"test-multi-turn-{time.time()}"

        # Simular 3 turnos
        for turn in range(1, 4):
            bus.publish_cognitive_model_updated(
                session_id=session_id,
                turn_number=turn,
                solidez=0.3 + (turn * 0.1),
                completude=0.2 + (turn * 0.1),
                claims_count=1,
                proposicoes_count=turn,
                concepts_count=turn * 2,
                open_questions_count=3 - turn,
                contradictions_count=0,
                is_mature=turn >= 3
            )

        # Recuperar eventos
        events = bus.get_session_events(session_id)
        cm_events = [e for e in events if e.get("event_type") == "cognitive_model_updated"]

        assert len(cm_events) == 3

        # Verificar evolução
        solidez_values = [e["solidez"] for e in cm_events]
        assert solidez_values == [0.4, 0.5, 0.6]  # 0.3+0.1, 0.3+0.2, 0.3+0.3

class TestObserverTimelineIntegration:
    """Testes de integração do Observer com Timeline."""

    def test_timeline_renders_observer_events(self):
        """Timeline renderiza eventos do Observer corretamente."""
        from app.components.backstage.timeline import render_observer_section

        observer_events = [
            {
                "event_type": "cognitive_model_updated",
                "turn_number": 1,
                "timestamp": "2025-12-08T10:30:00Z",
                "solidez": 0.45,
                "completude": 0.30,
                "concepts_count": 3,
                "proposicoes_count": 2,
                "is_mature": False,
                "metadata": {"processing_time_ms": 1200}
            },
            {
                "event_type": "cognitive_model_updated",
                "turn_number": 2,
                "timestamp": "2025-12-08T10:31:00Z",
                "solidez": 0.65,
                "completude": 0.50,
                "concepts_count": 5,
                "proposicoes_count": 4,
                "is_mature": False,
                "metadata": {"processing_time_ms": 1100}
            }
        ]

        # Função render_observer_section usa Streamlit
        # Testar que não lança exceção
        with patch("streamlit.markdown") as mock_md:
            with patch("streamlit.caption") as mock_cap:
                with patch("streamlit.expander") as mock_exp:
                    mock_exp.return_value.__enter__ = MagicMock()
                    mock_exp.return_value.__exit__ = MagicMock()

                    # Não deve lançar exceção
                    render_observer_section(observer_events)

class TestObserverCognitiveModelContext:
    """Testes de formatação do cognitive_model no contexto."""

    def test_proposicoes_are_sorted_by_solidez(self):
        """Proposições são ordenadas por solidez decrescente."""
        from core.agents.orchestrator.nodes import _build_cognitive_model_context

        cm = {
            "proposicoes": [
                {"texto": "Baixa", "solidez": 0.2},
                {"texto": "Alta", "solidez": 0.9},
                {"texto": "Media", "solidez": 0.5}
            ]
        }

        result = _build_cognitive_model_context(cm)

        # Alta deve aparecer antes de Media, que deve aparecer antes de Baixa
        pos_alta = result.find("Alta")
        pos_media = result.find("Media")
        pos_baixa = result.find("Baixa")

        assert pos_alta < pos_media < pos_baixa

    def test_metrics_fallback_calculation(self):
        """Solidez é calculada como fallback se não fornecida."""
        from core.agents.orchestrator.nodes import _build_cognitive_model_context

        cm = {
            "proposicoes": [
                {"texto": "P1", "solidez": 0.8},
                {"texto": "P2", "solidez": 0.6}
            ]
            # overall_solidez não fornecido
        }

        result = _build_cognitive_model_context(cm)

        # Média de 0.8 e 0.6 = 0.7 = 70%
        assert "70%" in result

    def test_all_sections_present_for_complete_model(self):
        """Todas as seções são incluídas para modelo completo."""
        from core.agents.orchestrator.nodes import _build_cognitive_model_context

        cm = {
            "claim": "Afirmação central",
            "proposicoes": [{"texto": "Fundamento", "solidez": 0.8}],
            "concepts_detected": ["conceito1", "conceito2"],
            "contradictions": [{"description": "Contradição", "confidence": 0.9}],
            "open_questions": ["Questão?"],
            "overall_solidez": 0.75,
            "overall_completude": 0.60
        }

        result = _build_cognitive_model_context(cm)

        assert "Afirmação central" in result
        assert "Fundamento" in result
        assert "conceito1" in result
        assert "Contradição" in result
        assert "Questão?" in result
        assert "75%" in result
        assert "60%" in result
