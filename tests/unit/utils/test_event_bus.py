"""
Testes unitários para EventBus (Épico 5.1).

Valida publicação, consumo e gerenciamento de eventos via arquivos JSON.

Versão: 1.0
Data: 13/11/2025
"""

import pytest
import tempfile
import shutil
from pathlib import Path

from utils.event_bus import EventBus, get_event_bus
from utils.event_models import AgentStartedEvent


class TestEventBus:
    """Testes para EventBus."""

    @pytest.fixture
    def temp_dir(self):
        """Cria diretório temporário para testes."""
        temp_path = Path(tempfile.mkdtemp())
        yield temp_path
        # Cleanup
        if temp_path.exists():
            shutil.rmtree(temp_path)

    @pytest.fixture
    def event_bus(self, temp_dir):
        """Cria EventBus com diretório temporário."""
        return EventBus(events_dir=temp_dir)

    def test_init_creates_directory(self, temp_dir):
        """Testa que __init__ cria diretório de eventos."""
        events_dir = temp_dir / "custom_events"
        assert not events_dir.exists()

        bus = EventBus(events_dir=events_dir)
        assert events_dir.exists()

    def test_publish_agent_started(self, event_bus):
        """Testa publicação de evento de início de agente."""
        event_bus.publish_agent_started("test-session", "orchestrator")

        events = event_bus.get_session_events("test-session")
        assert len(events) == 1
        assert events[0]["event_type"] == "agent_started"
        assert events[0]["agent_name"] == "orchestrator"
        assert events[0]["session_id"] == "test-session"

    def test_publish_agent_completed(self, event_bus):
        """Testa publicação de evento de conclusão de agente."""
        event_bus.publish_agent_completed(
            "test-session",
            "methodologist",
            summary="Aprovou hipótese",
            tokens_input=100,
            tokens_output=50,
            tokens_total=150
        )

        events = event_bus.get_session_events("test-session")
        assert len(events) == 1
        assert events[0]["event_type"] == "agent_completed"
        assert events[0]["agent_name"] == "methodologist"
        assert events[0]["summary"] == "Aprovou hipótese"
        assert events[0]["tokens_total"] == 150

    def test_publish_agent_error(self, event_bus):
        """Testa publicação de evento de erro."""
        event_bus.publish_agent_error(
            "test-session",
            "structurer",
            error_message="Validation failed",
            error_type="ValidationError"
        )

        events = event_bus.get_session_events("test-session")
        assert len(events) == 1
        assert events[0]["event_type"] == "agent_error"
        assert events[0]["error_message"] == "Validation failed"
        assert events[0]["error_type"] == "ValidationError"

    def test_publish_session_started(self, event_bus):
        """Testa publicação de evento de início de sessão."""
        event_bus.publish_session_started(
            "test-session",
            "Observei que LLMs aumentam produtividade"
        )

        events = event_bus.get_session_events("test-session")
        assert len(events) == 1
        assert events[0]["event_type"] == "session_started"
        assert events[0]["user_input"] == "Observei que LLMs aumentam produtividade"

    def test_publish_session_completed(self, event_bus):
        """Testa publicação de evento de conclusão de sessão."""
        event_bus.publish_session_completed(
            "test-session",
            "approved",
            tokens_total=850
        )

        events = event_bus.get_session_events("test-session")
        assert len(events) == 1
        assert events[0]["event_type"] == "session_completed"
        assert events[0]["final_status"] == "approved"
        assert events[0]["tokens_total"] == 850

    def test_multiple_events_same_session(self, event_bus):
        """Testa múltiplos eventos na mesma sessão."""
        event_bus.publish_session_started("session-1", "Test input")
        event_bus.publish_agent_started("session-1", "orchestrator")
        event_bus.publish_agent_completed(
            "session-1", "orchestrator",
            summary="Classificou", tokens_total=100
        )

        events = event_bus.get_session_events("session-1")
        assert len(events) == 3
        assert events[0]["event_type"] == "session_started"
        assert events[1]["event_type"] == "agent_started"
        assert events[2]["event_type"] == "agent_completed"

    def test_multiple_sessions_isolated(self, event_bus):
        """Testa que sessões diferentes são isoladas."""
        event_bus.publish_agent_started("session-1", "orchestrator")
        event_bus.publish_agent_started("session-2", "methodologist")

        events_1 = event_bus.get_session_events("session-1")
        events_2 = event_bus.get_session_events("session-2")

        assert len(events_1) == 1
        assert len(events_2) == 1
        assert events_1[0]["agent_name"] == "orchestrator"
        assert events_2[0]["agent_name"] == "methodologist"

    def test_get_session_events_empty(self, event_bus):
        """Testa obtenção de eventos de sessão inexistente."""
        events = event_bus.get_session_events("nonexistent-session")
        assert events == []

    def test_list_active_sessions(self, event_bus):
        """Testa listagem de sessões ativas."""
        event_bus.publish_session_started("session-1", "Test 1")
        event_bus.publish_session_started("session-2", "Test 2")
        event_bus.publish_session_started("session-3", "Test 3")

        sessions = event_bus.list_active_sessions()
        assert len(sessions) == 3
        assert "session-1" in sessions
        assert "session-2" in sessions
        assert "session-3" in sessions

    def test_list_active_sessions_empty(self, event_bus):
        """Testa listagem quando não há sessões."""
        sessions = event_bus.list_active_sessions()
        assert sessions == []

    def test_clear_session(self, event_bus):
        """Testa remoção de sessão."""
        event_bus.publish_session_started("session-1", "Test")
        event_bus.publish_agent_started("session-1", "orchestrator")

        # Verificar que sessão existe
        assert len(event_bus.get_session_events("session-1")) == 2

        # Remover sessão
        result = event_bus.clear_session("session-1")
        assert result is True

        # Verificar que sessão foi removida
        assert event_bus.get_session_events("session-1") == []

    def test_clear_session_nonexistent(self, event_bus):
        """Testa remoção de sessão inexistente."""
        result = event_bus.clear_session("nonexistent")
        assert result is False

    def test_get_session_summary_active(self, event_bus):
        """Testa resumo de sessão ativa."""
        event_bus.publish_session_started("session-1", "Test input")
        event_bus.publish_agent_started("session-1", "orchestrator")
        event_bus.publish_agent_completed(
            "session-1", "orchestrator",
            summary="Done", tokens_total=100
        )

        summary = event_bus.get_session_summary("session-1")
        assert summary is not None
        assert summary["session_id"] == "session-1"
        assert summary["total_events"] == 3
        assert summary["status"] == "active"
        assert summary["final_status"] is None
        assert summary["user_input"] == "Test input"

    def test_get_session_summary_completed(self, event_bus):
        """Testa resumo de sessão completa."""
        event_bus.publish_session_started("session-1", "Test input")
        event_bus.publish_agent_started("session-1", "orchestrator")
        event_bus.publish_session_completed("session-1", "approved", 500)

        summary = event_bus.get_session_summary("session-1")
        assert summary is not None
        assert summary["status"] == "completed"
        assert summary["final_status"] == "approved"
        assert summary["total_events"] == 3

    def test_get_session_summary_nonexistent(self, event_bus):
        """Testa resumo de sessão inexistente."""
        summary = event_bus.get_session_summary("nonexistent")
        assert summary is None

    def test_publish_event_generic(self, event_bus):
        """Testa publicação de evento genérico via Pydantic model."""
        event = AgentStartedEvent(
            session_id="test-session",
            agent_name="orchestrator",
            metadata={"key": "value"}
        )

        event_bus.publish_event(event)

        events = event_bus.get_session_events("test-session")
        assert len(events) == 1
        assert events[0]["metadata"]["key"] == "value"

    def test_persistence_across_instances(self, temp_dir):
        """Testa que eventos persistem entre instâncias do EventBus."""
        bus1 = EventBus(events_dir=temp_dir)
        bus1.publish_agent_started("session-1", "orchestrator")

        # Criar nova instância apontando para mesmo diretório
        bus2 = EventBus(events_dir=temp_dir)
        events = bus2.get_session_events("session-1")

        assert len(events) == 1
        assert events[0]["agent_name"] == "orchestrator"


class TestEventBusSingleton:
    """Testes para função get_event_bus (singleton)."""

    def test_get_event_bus_singleton(self):
        """Testa que get_event_bus retorna sempre a mesma instância."""
        bus1 = get_event_bus()
        bus2 = get_event_bus()

        assert bus1 is bus2

    def test_get_event_bus_shared_state(self):
        """Testa que instâncias singleton compartilham estado."""
        bus1 = get_event_bus()
        bus1.publish_agent_started("test-session", "orchestrator")

        bus2 = get_event_bus()
        events = bus2.get_session_events("test-session")

        assert len(events) >= 1  # Pode ter eventos de outros testes
