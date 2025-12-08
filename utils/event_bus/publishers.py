"""
Métodos de publicação de eventos do EventBus.

Este módulo contém todos os métodos publish_* que publicam eventos
no barramento de eventos.
"""

import logging
from typing import Optional, Dict, Any

from utils.event_models import (
    EventType,
    AgentStartedEvent,
    AgentCompletedEvent,
    AgentErrorEvent,
    SessionStartedEvent,
    SessionCompletedEvent,
    CognitiveModelUpdatedEvent
)

logger = logging.getLogger(__name__)


class EventBusPublishers:
    """
    Mixin com métodos de publicação de eventos.

    Adiciona métodos publish_* à classe EventBus.
    """

    def publish_event(self, event: EventType) -> None:
        """
        Publica um evento genérico.

        Args:
            event (EventType): Evento Pydantic a ser publicado

        Example:
            >>> bus = EventBus()
            >>> event = AgentStartedEvent(
            ...     session_id="session-1",
            ...     agent_name="orchestrator"
            ... )
            >>> bus.publish_event(event)
        """
        session_id = event.session_id
        data = self._load_events(session_id)
        data["events"].append(event.model_dump())
        self._save_events(session_id, data)
        logger.debug(f"Evento publicado: {event.event_type} para {session_id}")

    def publish_agent_started(
        self,
        session_id: str,
        agent_name: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Publica evento de início de agente.

        Args:
            session_id (str): ID da sessão
            agent_name (str): Nome do agente (orchestrator, structurer, methodologist)
            metadata (dict, optional): Metadados adicionais

        Example:
            >>> bus = EventBus()
            >>> bus.publish_agent_started("session-1", "orchestrator")
        """
        event = AgentStartedEvent(
            session_id=session_id,
            agent_name=agent_name,
            metadata=metadata or {}
        )
        self.publish_event(event)

    def publish_agent_completed(
        self,
        session_id: str,
        agent_name: str,
        summary: str,
        tokens_input: int = 0,
        tokens_output: int = 0,
        tokens_total: int = 0,
        cost: float = 0.0,
        duration: float = 0.0,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Publica evento de conclusão de agente.

        Args:
            session_id (str): ID da sessão
            agent_name (str): Nome do agente
            summary (str): Resumo da ação (até 280 chars)
            tokens_input (int): Tokens de entrada
            tokens_output (int): Tokens de saída
            tokens_total (int): Total de tokens
            cost (float): Custo da execução em USD
            duration (float): Duração da execução em segundos
            metadata (dict, optional): Metadados adicionais

        Example:
            >>> bus = EventBus()
            >>> bus.publish_agent_completed(
            ...     "session-1", "orchestrator",
            ...     summary="Classificou como vague",
            ...     tokens_input=100, tokens_output=50, tokens_total=150,
            ...     cost=0.0012, duration=1.2
            ... )
        """
        event = AgentCompletedEvent(
            session_id=session_id,
            agent_name=agent_name,
            summary=summary,
            tokens_input=tokens_input,
            tokens_output=tokens_output,
            tokens_total=tokens_total,
            cost=cost,
            duration=duration,
            metadata=metadata or {}
        )
        self.publish_event(event)

    def publish_agent_error(
        self,
        session_id: str,
        agent_name: str,
        error_message: str,
        error_type: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Publica evento de erro em agente.

        Args:
            session_id (str): ID da sessão
            agent_name (str): Nome do agente
            error_message (str): Mensagem de erro
            error_type (str, optional): Tipo do erro
            metadata (dict, optional): Metadados adicionais

        Example:
            >>> bus = EventBus()
            >>> bus.publish_agent_error(
            ...     "session-1", "methodologist",
            ...     error_message="API timeout",
            ...     error_type="TimeoutError"
            ... )
        """
        event = AgentErrorEvent(
            session_id=session_id,
            agent_name=agent_name,
            error_message=error_message,
            error_type=error_type,
            metadata=metadata or {}
        )
        self.publish_event(event)

    def publish_session_started(
        self,
        session_id: str,
        user_input: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Publica evento de início de sessão.

        Args:
            session_id (str): ID da sessão
            user_input (str): Input inicial do usuário
            metadata (dict, optional): Metadados adicionais

        Example:
            >>> bus = EventBus()
            >>> bus.publish_session_started(
            ...     "session-1",
            ...     "Observei que LLMs aumentam produtividade"
            ... )
        """
        event = SessionStartedEvent(
            session_id=session_id,
            user_input=user_input,
            metadata=metadata or {}
        )
        self.publish_event(event)

    def publish_session_completed(
        self,
        session_id: str,
        final_status: str,
        tokens_total: int = 0,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Publica evento de conclusão de sessão.

        Args:
            session_id (str): ID da sessão
            final_status (str): Status final (approved, rejected, etc)
            tokens_total (int): Total de tokens consumidos
            metadata (dict, optional): Metadados adicionais

        Example:
            >>> bus = EventBus()
            >>> bus.publish_session_completed(
            ...     "session-1", "approved",
            ...     tokens_total=850
            ... )
        """
        event = SessionCompletedEvent(
            session_id=session_id,
            final_status=final_status,
            tokens_total=tokens_total,
            metadata=metadata or {}
        )
        self.publish_event(event)

    def publish_cognitive_model_updated(
        self,
        session_id: str,
        turn_number: int,
        solidez: float,
        completude: float,
        claims_count: int = 0,
        proposicoes_count: int = 0,
        concepts_count: int = 0,
        open_questions_count: int = 0,
        contradictions_count: int = 0,
        is_mature: bool = False,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Publica evento de atualizacao do CognitiveModel (Epico 10.2).

        Este evento e publicado pelo Observador a cada turno processado.
        Permite ao Dashboard exibir a evolucao do argumento em tempo real.

        Args:
            session_id (str): ID da sessao
            turn_number (int): Numero do turno processado
            solidez (float): Solidez do argumento (0-1)
            completude (float): Completude do argumento (0-1)
            claims_count (int): Numero de claims
            proposicoes_count (int): Numero de proposicoes
            concepts_count (int): Numero de conceitos
            open_questions_count (int): Numero de questoes abertas
            contradictions_count (int): Numero de contradicoes
            is_mature (bool): Se argumento esta maduro
            metadata (dict, optional): Metadados adicionais

        Example:
            >>> bus = EventBus()
            >>> bus.publish_cognitive_model_updated(
            ...     "session-1",
            ...     turn_number=3,
            ...     solidez=0.65,
            ...     completude=0.50,
            ...     claims_count=1,
            ...     proposicoes_count=2,
            ...     concepts_count=3
            ... )
        """
        event = CognitiveModelUpdatedEvent(
            session_id=session_id,
            turn_number=turn_number,
            solidez=solidez,
            completude=completude,
            claims_count=claims_count,
            proposicoes_count=proposicoes_count,
            concepts_count=concepts_count,
            open_questions_count=open_questions_count,
            contradictions_count=contradictions_count,
            is_mature=is_mature,
            metadata=metadata or {}
        )
        self.publish_event(event)

