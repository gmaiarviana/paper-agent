"""
Testes unitarios para eventos do Observer (Epico 13.5).

Valida publicacao, serializacao e desserializacao dos eventos de deteccao
de mudancas do Observer.

Versao: 1.0
Data: 10/12/2025
"""

import pytest
import tempfile
import shutil
from pathlib import Path

from core.utils.event_bus import EventBus
from core.utils.event_models import (
    VariationDetectedEvent,
    DirectionChangeConfirmedEvent,
    ClarityCheckpointEvent,
)


class TestVariationDetectedEvent:
    """Testes para VariationDetectedEvent."""

    @pytest.fixture
    def temp_dir(self):
        """Cria diretorio temporario para testes."""
        temp_path = Path(tempfile.mkdtemp())
        yield temp_path
        if temp_path.exists():
            shutil.rmtree(temp_path)

    @pytest.fixture
    def event_bus(self, temp_dir):
        """Cria EventBus com diretorio temporario."""
        return EventBus(events_dir=temp_dir)

    def test_create_variation_detected_event(self):
        """Testa criacao de VariationDetectedEvent."""
        event = VariationDetectedEvent(
            session_id="test-session",
            turn_number=3,
            essence_previous="LLMs aumentam produtividade",
            essence_new="IA generativa melhora eficiencia",
            shared_concepts=["produtividade", "IA"],
            new_concepts=["eficiencia"],
            analysis="Variacao do mesmo conceito"
        )

        assert event.event_type == "variation_detected"
        assert event.classification == "variation"
        assert event.turn_number == 3
        assert event.essence_previous == "LLMs aumentam produtividade"
        assert event.essence_new == "IA generativa melhora eficiencia"
        assert len(event.shared_concepts) == 2
        assert len(event.new_concepts) == 1

    def test_publish_variation_detected(self, event_bus):
        """Testa publicacao de evento de variacao detectada."""
        event_bus.publish_variation_detected(
            session_id="test-session",
            turn_number=3,
            essence_previous="LLMs aumentam produtividade",
            essence_new="IA generativa melhora eficiencia",
            shared_concepts=["produtividade", "IA"],
            new_concepts=["eficiencia"],
            analysis="Variacao do mesmo conceito"
        )

        events = event_bus.get_session_events("test-session")
        assert len(events) == 1
        assert events[0]["event_type"] == "variation_detected"
        assert events[0]["classification"] == "variation"
        assert events[0]["turn_number"] == 3
        assert events[0]["essence_previous"] == "LLMs aumentam produtividade"
        assert events[0]["essence_new"] == "IA generativa melhora eficiencia"
        assert events[0]["shared_concepts"] == ["produtividade", "IA"]
        assert events[0]["new_concepts"] == ["eficiencia"]

    def test_variation_detected_defaults(self, event_bus):
        """Testa valores default do evento de variacao."""
        event_bus.publish_variation_detected(
            session_id="test-session",
            turn_number=1,
            essence_previous="anterior",
            essence_new="novo"
        )

        events = event_bus.get_session_events("test-session")
        assert events[0]["shared_concepts"] == []
        assert events[0]["new_concepts"] == []
        assert events[0]["analysis"] == ""


class TestDirectionChangeConfirmedEvent:
    """Testes para DirectionChangeConfirmedEvent."""

    @pytest.fixture
    def temp_dir(self):
        """Cria diretorio temporario para testes."""
        temp_path = Path(tempfile.mkdtemp())
        yield temp_path
        if temp_path.exists():
            shutil.rmtree(temp_path)

    @pytest.fixture
    def event_bus(self, temp_dir):
        """Cria EventBus com diretorio temporario."""
        return EventBus(events_dir=temp_dir)

    def test_create_direction_change_event(self):
        """Testa criacao de DirectionChangeConfirmedEvent."""
        event = DirectionChangeConfirmedEvent(
            session_id="test-session",
            turn_number=5,
            previous_claim="LLMs aumentam produtividade",
            new_claim="Blockchain revoluciona financas",
            user_confirmed=True,
            reasoning="Topicos completamente distintos"
        )

        assert event.event_type == "direction_change_confirmed"
        assert event.classification == "real_change"
        assert event.turn_number == 5
        assert event.previous_claim == "LLMs aumentam produtividade"
        assert event.new_claim == "Blockchain revoluciona financas"
        assert event.user_confirmed is True

    def test_publish_direction_change_confirmed(self, event_bus):
        """Testa publicacao de evento de mudanca de direcao."""
        event_bus.publish_direction_change_confirmed(
            session_id="test-session",
            turn_number=5,
            previous_claim="LLMs aumentam produtividade",
            new_claim="Blockchain revoluciona financas",
            user_confirmed=True,
            reasoning="Topicos completamente distintos"
        )

        events = event_bus.get_session_events("test-session")
        assert len(events) == 1
        assert events[0]["event_type"] == "direction_change_confirmed"
        assert events[0]["classification"] == "real_change"
        assert events[0]["turn_number"] == 5
        assert events[0]["previous_claim"] == "LLMs aumentam produtividade"
        assert events[0]["new_claim"] == "Blockchain revoluciona financas"
        assert events[0]["user_confirmed"] is True
        assert events[0]["reasoning"] == "Topicos completamente distintos"

    def test_direction_change_defaults(self, event_bus):
        """Testa valores default do evento de mudanca."""
        event_bus.publish_direction_change_confirmed(
            session_id="test-session",
            turn_number=1,
            previous_claim="claim anterior",
            new_claim="novo claim"
        )

        events = event_bus.get_session_events("test-session")
        assert events[0]["user_confirmed"] is False
        assert events[0]["reasoning"] == ""


class TestClarityCheckpointEvent:
    """Testes para ClarityCheckpointEvent."""

    @pytest.fixture
    def temp_dir(self):
        """Cria diretorio temporario para testes."""
        temp_path = Path(tempfile.mkdtemp())
        yield temp_path
        if temp_path.exists():
            shutil.rmtree(temp_path)

    @pytest.fixture
    def event_bus(self, temp_dir):
        """Cria EventBus com diretorio temporario."""
        return EventBus(events_dir=temp_dir)

    def test_create_clarity_checkpoint_event(self):
        """Testa criacao de ClarityCheckpointEvent."""
        event = ClarityCheckpointEvent(
            session_id="test-session",
            turn_number=4,
            clarity_level="nebulosa",
            clarity_score=2,
            checkpoint_reason="Multiplos topicos sem conexao",
            factors={"coherence": "baixa", "claim_definition": "vago"},
            suggestion="Qual topico explorar primeiro?"
        )

        assert event.event_type == "clarity_checkpoint"
        assert event.turn_number == 4
        assert event.clarity_level == "nebulosa"
        assert event.clarity_score == 2
        assert event.checkpoint_reason == "Multiplos topicos sem conexao"
        assert event.factors["coherence"] == "baixa"
        assert event.suggestion == "Qual topico explorar primeiro?"

    def test_publish_clarity_checkpoint(self, event_bus):
        """Testa publicacao de evento de checkpoint de clareza."""
        event_bus.publish_clarity_checkpoint(
            session_id="test-session",
            turn_number=4,
            clarity_level="nebulosa",
            clarity_score=2,
            checkpoint_reason="Multiplos topicos sem conexao",
            factors={"coherence": "baixa", "claim_definition": "vago"},
            suggestion="Qual topico explorar primeiro?"
        )

        events = event_bus.get_session_events("test-session")
        assert len(events) == 1
        assert events[0]["event_type"] == "clarity_checkpoint"
        assert events[0]["turn_number"] == 4
        assert events[0]["clarity_level"] == "nebulosa"
        assert events[0]["clarity_score"] == 2
        assert events[0]["checkpoint_reason"] == "Multiplos topicos sem conexao"
        assert events[0]["factors"]["coherence"] == "baixa"
        assert events[0]["suggestion"] == "Qual topico explorar primeiro?"

    def test_clarity_checkpoint_defaults(self, event_bus):
        """Testa valores default do evento de checkpoint."""
        event_bus.publish_clarity_checkpoint(
            session_id="test-session",
            turn_number=1,
            clarity_level="confusa",
            clarity_score=1,
            checkpoint_reason="Razao"
        )

        events = event_bus.get_session_events("test-session")
        assert events[0]["factors"] == {}
        assert events[0]["suggestion"] == ""

    def test_clarity_score_boundaries(self):
        """Testa limites do clarity_score (1-5)."""
        # Score minimo valido
        event_min = ClarityCheckpointEvent(
            session_id="test",
            turn_number=1,
            clarity_level="confusa",
            clarity_score=1,
            checkpoint_reason="Razao"
        )
        assert event_min.clarity_score == 1

        # Score maximo valido
        event_max = ClarityCheckpointEvent(
            session_id="test",
            turn_number=1,
            clarity_level="cristalina",
            clarity_score=5,
            checkpoint_reason="Razao"
        )
        assert event_max.clarity_score == 5


class TestObserverEventsIntegration:
    """Testes de integracao para eventos do Observer."""

    @pytest.fixture
    def temp_dir(self):
        """Cria diretorio temporario para testes."""
        temp_path = Path(tempfile.mkdtemp())
        yield temp_path
        if temp_path.exists():
            shutil.rmtree(temp_path)

    @pytest.fixture
    def event_bus(self, temp_dir):
        """Cria EventBus com diretorio temporario."""
        return EventBus(events_dir=temp_dir)

    def test_multiple_detection_events_same_session(self, event_bus):
        """Testa multiplos eventos de deteccao na mesma sessao."""
        # Turno 1: variacao
        event_bus.publish_variation_detected(
            session_id="session-1",
            turn_number=1,
            essence_previous="A",
            essence_new="A'"
        )

        # Turno 2: mudanca de direcao
        event_bus.publish_direction_change_confirmed(
            session_id="session-1",
            turn_number=2,
            previous_claim="A",
            new_claim="B"
        )

        # Turno 3: checkpoint de clareza
        event_bus.publish_clarity_checkpoint(
            session_id="session-1",
            turn_number=3,
            clarity_level="nebulosa",
            clarity_score=2,
            checkpoint_reason="Razao"
        )

        events = event_bus.get_session_events("session-1")
        assert len(events) == 3

        # Verificar ordem cronologica
        assert events[0]["event_type"] == "variation_detected"
        assert events[1]["event_type"] == "direction_change_confirmed"
        assert events[2]["event_type"] == "clarity_checkpoint"

    def test_filter_observer_detection_events(self, event_bus):
        """Testa filtragem de eventos de deteccao do Observer."""
        # Publicar diferentes tipos de eventos
        event_bus.publish_agent_started("session-1", "orchestrator")
        event_bus.publish_variation_detected(
            session_id="session-1",
            turn_number=1,
            essence_previous="A",
            essence_new="A'"
        )
        event_bus.publish_agent_completed(
            "session-1", "orchestrator", summary="Done"
        )
        event_bus.publish_direction_change_confirmed(
            session_id="session-1",
            turn_number=2,
            previous_claim="A",
            new_claim="B"
        )

        events = event_bus.get_session_events("session-1")

        # Filtrar apenas eventos de deteccao
        detection_events = [
            e for e in events
            if e["event_type"] in [
                "variation_detected",
                "direction_change_confirmed",
                "clarity_checkpoint"
            ]
        ]

        assert len(detection_events) == 2
        assert detection_events[0]["event_type"] == "variation_detected"
        assert detection_events[1]["event_type"] == "direction_change_confirmed"

    def test_events_have_timestamp(self, event_bus):
        """Testa que todos eventos tem timestamp."""
        event_bus.publish_variation_detected(
            session_id="test",
            turn_number=1,
            essence_previous="A",
            essence_new="B"
        )

        events = event_bus.get_session_events("test")
        assert "timestamp" in events[0]
        assert events[0]["timestamp"] is not None
        # Formato ISO 8601
        assert "T" in events[0]["timestamp"]

    def test_events_with_metadata(self, event_bus):
        """Testa que eventos suportam metadata adicional."""
        event_bus.publish_variation_detected(
            session_id="test",
            turn_number=1,
            essence_previous="A",
            essence_new="B",
            metadata={"source": "test", "debug": True}
        )

        events = event_bus.get_session_events("test")
        assert events[0]["metadata"]["source"] == "test"
        assert events[0]["metadata"]["debug"] is True
