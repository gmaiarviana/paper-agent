"""
Testes unitários para os modelos de eventos (Épico 5.1).

Valida schemas Pydantic, serialização JSON e validação de campos.

Versão: 1.0
Data: 13/11/2025
"""

import pytest
from datetime import datetime, timezone
from utils.event_models import (
    AgentStartedEvent,
    AgentCompletedEvent,
    AgentErrorEvent,
    SessionStartedEvent,
    SessionCompletedEvent
)


class TestAgentStartedEvent:
    """Testes para AgentStartedEvent."""

    def test_create_valid_event(self):
        """Testa criação de evento válido."""
        event = AgentStartedEvent(
            session_id="test-session-123",
            agent_name="orchestrator"
        )

        assert event.session_id == "test-session-123"
        assert event.agent_name == "orchestrator"
        assert event.event_type == "agent_started"
        assert event.timestamp is not None

    def test_timestamp_auto_generated(self):
        """Testa que timestamp é gerado automaticamente."""
        event = AgentStartedEvent(
            session_id="test-session",
            agent_name="orchestrator"
        )

        # Timestamp deve estar no formato ISO 8601
        assert "T" in event.timestamp
        assert event.timestamp.endswith("Z")

    def test_metadata_optional(self):
        """Testa que metadata é opcional."""
        event = AgentStartedEvent(
            session_id="test-session",
            agent_name="orchestrator"
        )

        assert event.metadata == {}

        # Com metadata
        event_with_meta = AgentStartedEvent(
            session_id="test-session",
            agent_name="orchestrator",
            metadata={"key": "value"}
        )

        assert event_with_meta.metadata == {"key": "value"}

    def test_json_serialization(self):
        """Testa serialização para JSON."""
        event = AgentStartedEvent(
            session_id="test-session",
            agent_name="orchestrator",
            metadata={"input": "test"}
        )

        json_data = event.model_dump()

        assert json_data["session_id"] == "test-session"
        assert json_data["agent_name"] == "orchestrator"
        assert json_data["event_type"] == "agent_started"
        assert json_data["metadata"]["input"] == "test"


class TestAgentCompletedEvent:
    """Testes para AgentCompletedEvent."""

    def test_create_valid_event(self):
        """Testa criação de evento válido."""
        event = AgentCompletedEvent(
            session_id="test-session",
            agent_name="methodologist",
            summary="Aprovou hipótese",
            tokens_input=100,
            tokens_output=50,
            tokens_total=150
        )

        assert event.session_id == "test-session"
        assert event.agent_name == "methodologist"
        assert event.summary == "Aprovou hipótese"
        assert event.tokens_input == 100
        assert event.tokens_output == 50
        assert event.tokens_total == 150
        assert event.event_type == "agent_completed"

    def test_tokens_default_to_zero(self):
        """Testa que tokens defaultam para 0."""
        event = AgentCompletedEvent(
            session_id="test-session",
            agent_name="structurer",
            summary="Estruturou questão"
        )

        assert event.tokens_input == 0
        assert event.tokens_output == 0
        assert event.tokens_total == 0

    def test_tokens_non_negative(self):
        """Testa que tokens não podem ser negativos."""
        with pytest.raises(Exception):  # Pydantic ValidationError
            AgentCompletedEvent(
                session_id="test-session",
                agent_name="orchestrator",
                summary="Test",
                tokens_input=-10
            )

    def test_json_serialization_with_all_fields(self):
        """Testa serialização completa."""
        event = AgentCompletedEvent(
            session_id="test-session",
            agent_name="orchestrator",
            summary="Classificou como vague",
            tokens_input=200,
            tokens_output=100,
            tokens_total=300,
            metadata={"classification": "vague"}
        )

        json_data = event.model_dump()

        assert json_data["summary"] == "Classificou como vague"
        assert json_data["tokens_total"] == 300
        assert json_data["metadata"]["classification"] == "vague"


class TestAgentErrorEvent:
    """Testes para AgentErrorEvent."""

    def test_create_valid_event(self):
        """Testa criação de evento válido."""
        event = AgentErrorEvent(
            session_id="test-session",
            agent_name="methodologist",
            error_message="API timeout",
            error_type="TimeoutError"
        )

        assert event.session_id == "test-session"
        assert event.agent_name == "methodologist"
        assert event.error_message == "API timeout"
        assert event.error_type == "TimeoutError"
        assert event.event_type == "agent_error"

    def test_error_type_optional(self):
        """Testa que error_type é opcional."""
        event = AgentErrorEvent(
            session_id="test-session",
            agent_name="orchestrator",
            error_message="Unknown error"
        )

        assert event.error_type is None

    def test_json_serialization(self):
        """Testa serialização para JSON."""
        event = AgentErrorEvent(
            session_id="test-session",
            agent_name="structurer",
            error_message="Validation failed",
            error_type="ValidationError",
            metadata={"details": "Missing field"}
        )

        json_data = event.model_dump()

        assert json_data["error_message"] == "Validation failed"
        assert json_data["error_type"] == "ValidationError"
        assert json_data["metadata"]["details"] == "Missing field"


class TestSessionStartedEvent:
    """Testes para SessionStartedEvent."""

    def test_create_valid_event(self):
        """Testa criação de evento válido."""
        event = SessionStartedEvent(
            session_id="test-session",
            user_input="Observei que X impacta Y"
        )

        assert event.session_id == "test-session"
        assert event.user_input == "Observei que X impacta Y"
        assert event.event_type == "session_started"

    def test_json_serialization(self):
        """Testa serialização para JSON."""
        event = SessionStartedEvent(
            session_id="test-session",
            user_input="Test input",
            metadata={"source": "cli"}
        )

        json_data = event.model_dump()

        assert json_data["user_input"] == "Test input"
        assert json_data["metadata"]["source"] == "cli"


class TestSessionCompletedEvent:
    """Testes para SessionCompletedEvent."""

    def test_create_valid_event(self):
        """Testa criação de evento válido."""
        event = SessionCompletedEvent(
            session_id="test-session",
            final_status="approved",
            tokens_total=850
        )

        assert event.session_id == "test-session"
        assert event.final_status == "approved"
        assert event.tokens_total == 850
        assert event.event_type == "session_completed"

    def test_tokens_total_default_to_zero(self):
        """Testa que tokens_total defaulta para 0."""
        event = SessionCompletedEvent(
            session_id="test-session",
            final_status="rejected"
        )

        assert event.tokens_total == 0

    def test_tokens_total_non_negative(self):
        """Testa que tokens_total não pode ser negativo."""
        with pytest.raises(Exception):  # Pydantic ValidationError
            SessionCompletedEvent(
                session_id="test-session",
                final_status="approved",
                tokens_total=-100
            )

    def test_json_serialization(self):
        """Testa serialização para JSON."""
        event = SessionCompletedEvent(
            session_id="test-session",
            final_status="approved",
            tokens_total=1500,
            metadata={"duration_seconds": 180}
        )

        json_data = event.model_dump()

        assert json_data["final_status"] == "approved"
        assert json_data["tokens_total"] == 1500
        assert json_data["metadata"]["duration_seconds"] == 180
