"""
Métodos de publicação de eventos do EventBus.

Este módulo contém todos os métodos publish_* que publicam eventos
no barramento de eventos.
"""

import logging
from typing import Optional, Dict, Any

from core.utils.event_models import (
    EventType,
    AgentStartedEvent,
    AgentCompletedEvent,
    AgentErrorEvent,
    SessionStartedEvent,
    SessionCompletedEvent,
    CognitiveModelUpdatedEvent,
    ClarificationRequestedEvent,
    ClarificationResolvedEvent,
    # Epico 13.5 - Timeline Visual de Mudancas
    VariationDetectedEvent,
    DirectionChangeConfirmedEvent,
    ClarityCheckpointEvent,
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
        Publica evento de atualizacao do CognitiveModel.

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

    def publish_clarification_requested(
        self,
        session_id: str,
        turn_number: int,
        clarification_type: str,
        question: str,
        priority: str = "medium",
        related_context: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Publica evento de pergunta de esclarecimento.

        Este evento e publicado quando o Orquestrador faz uma pergunta
        de esclarecimento ao usuario baseado em analise do Observer.

        Args:
            session_id (str): ID da sessao
            turn_number (int): Numero do turno atual
            clarification_type (str): Tipo (contradiction, gap, confusion)
            question (str): Pergunta feita ao usuario
            priority (str): Prioridade (high, medium, low)
            related_context (dict): Contexto relacionado
            metadata (dict): Metadados adicionais

        Example:
            >>> bus = EventBus()
            >>> bus.publish_clarification_requested(
            ...     "session-1",
            ...     turn_number=5,
            ...     clarification_type="contradiction",
            ...     question="Voce mencionou X e Y. Se aplicam em contextos diferentes?"
            ... )
        """
        event = ClarificationRequestedEvent(
            session_id=session_id,
            turn_number=turn_number,
            clarification_type=clarification_type,
            question=question,
            priority=priority,
            related_context=related_context or {},
            metadata=metadata or {}
        )
        self.publish_event(event)

    def publish_clarification_resolved(
        self,
        session_id: str,
        turn_number: int,
        clarification_type: str,
        resolution_status: str,
        summary: str,
        updates_made: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Publica evento de esclarecimento obtido.

        Este evento e publicado apos usuario responder pergunta de esclarecimento
        e Observer analisar a resposta.

        Args:
            session_id (str): ID da sessao
            turn_number (int): Numero do turno atual
            clarification_type (str): Tipo de esclarecimento original
            resolution_status (str): Status (resolved, partially_resolved, unresolved)
            summary (str): Resumo do que foi esclarecido
            updates_made (dict): Atualizacoes feitas no CognitiveModel
            metadata (dict): Metadados adicionais

        Example:
            >>> bus = EventBus()
            >>> bus.publish_clarification_resolved(
            ...     "session-1",
            ...     turn_number=6,
            ...     clarification_type="contradiction",
            ...     resolution_status="resolved",
            ...     summary="Usuario esclareceu que X e Y se aplicam em contextos diferentes"
            ... )
        """
        event = ClarificationResolvedEvent(
            session_id=session_id,
            turn_number=turn_number,
            clarification_type=clarification_type,
            resolution_status=resolution_status,
            summary=summary,
            updates_made=updates_made or {},
            metadata=metadata or {}
        )
        self.publish_event(event)

    # ========================================================================
    # Epico 13.5 - Timeline Visual de Mudancas
    # ========================================================================

    def publish_variation_detected(
        self,
        session_id: str,
        turn_number: int,
        essence_previous: str,
        essence_new: str,
        shared_concepts: Optional[list] = None,
        new_concepts: Optional[list] = None,
        analysis: str = "",
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Publica evento de variacao detectada (Epico 13.5).

        Este evento e publicado discretamente quando o Observer identifica
        que o input do usuario e uma variacao do conceito anterior (mesma
        essencia), nao uma mudanca real de direcao. Nao interrompe o fluxo.

        Args:
            session_id (str): ID da sessao
            turn_number (int): Numero do turno atual
            essence_previous (str): Essencia semantica do texto anterior
            essence_new (str): Essencia semantica do novo texto
            shared_concepts (list): Conceitos mantidos entre os textos
            new_concepts (list): Novos conceitos introduzidos
            analysis (str): Analise textual do LLM
            metadata (dict): Metadados adicionais

        Example:
            >>> bus = EventBus()
            >>> bus.publish_variation_detected(
            ...     "session-1",
            ...     turn_number=3,
            ...     essence_previous="LLMs aumentam produtividade",
            ...     essence_new="IA generativa melhora eficiencia",
            ...     shared_concepts=["produtividade", "IA"],
            ...     analysis="Variacao do mesmo conceito"
            ... )
        """
        event = VariationDetectedEvent(
            session_id=session_id,
            turn_number=turn_number,
            essence_previous=essence_previous,
            essence_new=essence_new,
            shared_concepts=shared_concepts or [],
            new_concepts=new_concepts or [],
            analysis=analysis,
            metadata=metadata or {}
        )
        self.publish_event(event)

    def publish_direction_change_confirmed(
        self,
        session_id: str,
        turn_number: int,
        previous_claim: str,
        new_claim: str,
        user_confirmed: bool = False,
        reasoning: str = "",
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Publica evento de mudanca real de direcao (Epico 13.5).

        Este evento e publicado quando o Observer detecta que o usuario
        mudou de foco para um topico fundamentalmente diferente.

        Args:
            session_id (str): ID da sessao
            turn_number (int): Numero do turno atual
            previous_claim (str): Claim/foco anterior da conversa
            new_claim (str): Novo claim/foco identificado
            user_confirmed (bool): Se usuario confirmou a mudanca
            reasoning (str): Justificativa para classificacao
            metadata (dict): Metadados adicionais

        Example:
            >>> bus = EventBus()
            >>> bus.publish_direction_change_confirmed(
            ...     "session-1",
            ...     turn_number=5,
            ...     previous_claim="LLMs aumentam produtividade",
            ...     new_claim="Blockchain revoluciona financas",
            ...     user_confirmed=True,
            ...     reasoning="Topicos completamente distintos"
            ... )
        """
        event = DirectionChangeConfirmedEvent(
            session_id=session_id,
            turn_number=turn_number,
            previous_claim=previous_claim,
            new_claim=new_claim,
            user_confirmed=user_confirmed,
            reasoning=reasoning,
            metadata=metadata or {}
        )
        self.publish_event(event)

    def publish_clarity_checkpoint(
        self,
        session_id: str,
        turn_number: int,
        clarity_level: str,
        clarity_score: int,
        checkpoint_reason: str,
        factors: Optional[Dict[str, str]] = None,
        suggestion: str = "",
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Publica evento de checkpoint de clareza (Epico 13.5).

        Este evento e publicado quando o Observer detecta que a conversa
        esta nebulosa ou confusa e o Orchestrator solicita esclarecimento.

        Args:
            session_id (str): ID da sessao
            turn_number (int): Numero do turno atual
            clarity_level (str): Nivel de clareza (cristalina, clara, nebulosa, confusa)
            clarity_score (int): Score numerico de clareza (1-5)
            checkpoint_reason (str): Razao para solicitar checkpoint
            factors (dict): Fatores da avaliacao
            suggestion (str): Sugestao de como esclarecer
            metadata (dict): Metadados adicionais

        Example:
            >>> bus = EventBus()
            >>> bus.publish_clarity_checkpoint(
            ...     "session-1",
            ...     turn_number=4,
            ...     clarity_level="nebulosa",
            ...     clarity_score=2,
            ...     checkpoint_reason="Multiplos topicos sem conexao",
            ...     factors={"coherence": "baixa"},
            ...     suggestion="Qual topico explorar primeiro?"
            ... )
        """
        event = ClarityCheckpointEvent(
            session_id=session_id,
            turn_number=turn_number,
            clarity_level=clarity_level,
            clarity_score=clarity_score,
            checkpoint_reason=checkpoint_reason,
            factors=factors or {},
            suggestion=suggestion,
            metadata=metadata or {}
        )
        self.publish_event(event)

