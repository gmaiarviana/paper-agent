"""
Modelos de eventos para comunicação entre CLI/Graph e Dashboard (Épico 5.1).

Este módulo define os schemas dos eventos emitidos pelo sistema durante
execução de agentes e sessões. Os eventos são usados pelo Dashboard Streamlit
para exibir timeline em tempo real.

Versão: 1.0
Data: 13/11/2025
"""

from typing import Literal, Optional, Any, Dict
from datetime import datetime, timezone
from pydantic import BaseModel, Field, ConfigDict


class BaseEvent(BaseModel):
    """
    Evento base com campos comuns a todos os eventos.

    Attributes:
        session_id (str): ID único da sessão
        timestamp (str): Timestamp ISO 8601 UTC do evento
        event_type (str): Tipo do evento (agent_started, agent_completed, etc)
    """
    session_id: str = Field(..., description="ID único da sessão")
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
        description="Timestamp ISO 8601 UTC"
    )
    event_type: str = Field(..., description="Tipo do evento")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "session_id": "cli-session-abc123",
                "timestamp": "2025-11-13T14:30:00Z",
                "event_type": "agent_started"
            }
        }
    )


class AgentStartedEvent(BaseEvent):
    """
    Evento emitido quando um agente inicia execução.

    Attributes:
        agent_name (str): Nome do agente (orchestrator, structurer, methodologist)
        metadata (dict): Metadados adicionais opcionais
    """
    event_type: Literal["agent_started"] = "agent_started"
    agent_name: str = Field(..., description="Nome do agente")
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Metadados adicionais opcionais"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "session_id": "cli-session-abc123",
                "timestamp": "2025-11-13T14:30:00Z",
                "event_type": "agent_started",
                "agent_name": "orchestrator",
                "metadata": {"input": "Observei que LLMs aumentam produtividade"}
            }
        }
    )


class AgentCompletedEvent(BaseEvent):
    """
    Evento emitido quando um agente finaliza execução com sucesso.

    Attributes:
        agent_name (str): Nome do agente
        summary (str): Resumo curto da ação/decisão do agente (até 280 chars)
        tokens_input (int): Tokens de entrada consumidos
        tokens_output (int): Tokens de saída gerados
        tokens_total (int): Total de tokens
        cost (float): Custo da execução em USD
        duration (float): Duração da execução em segundos
        metadata (dict): Metadados adicionais opcionais
    """
    event_type: Literal["agent_completed"] = "agent_completed"
    agent_name: str = Field(..., description="Nome do agente")
    summary: str = Field(..., description="Resumo curto da ação (até 280 chars)")
    tokens_input: int = Field(0, ge=0, description="Tokens de entrada")
    tokens_output: int = Field(0, ge=0, description="Tokens de saída")
    tokens_total: int = Field(0, ge=0, description="Total de tokens")
    cost: float = Field(0.0, ge=0.0, description="Custo da execução em USD")
    duration: float = Field(0.0, ge=0.0, description="Duração da execução em segundos")
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Metadados adicionais opcionais"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "session_id": "cli-session-abc123",
                "timestamp": "2025-11-13T14:30:05Z",
                "event_type": "agent_completed",
                "agent_name": "orchestrator",
                "summary": "Classificou input como 'vague'",
                "tokens_input": 100,
                "tokens_output": 50,
                "tokens_total": 150,
                "cost": 0.0012,
                "duration": 1.2,
                "metadata": {"classification": "vague"}
            }
        }
    )


class AgentErrorEvent(BaseEvent):
    """
    Evento emitido quando um agente falha durante execução.

    Attributes:
        agent_name (str): Nome do agente
        error_message (str): Mensagem de erro
        error_type (str): Tipo do erro (opcional)
        metadata (dict): Metadados adicionais opcionais
    """
    event_type: Literal["agent_error"] = "agent_error"
    agent_name: str = Field(..., description="Nome do agente")
    error_message: str = Field(..., description="Mensagem de erro")
    error_type: Optional[str] = Field(None, description="Tipo do erro")
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Metadados adicionais opcionais"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "session_id": "cli-session-abc123",
                "timestamp": "2025-11-13T14:30:10Z",
                "event_type": "agent_error",
                "agent_name": "methodologist",
                "error_message": "API rate limit exceeded",
                "error_type": "RateLimitError",
                "metadata": {}
            }
        }
    )


class SessionStartedEvent(BaseEvent):
    """
    Evento emitido quando uma sessão inicia.

    Attributes:
        user_input (str): Input inicial do usuário
        metadata (dict): Metadados adicionais opcionais
    """
    event_type: Literal["session_started"] = "session_started"
    user_input: str = Field(..., description="Input inicial do usuário")
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Metadados adicionais opcionais"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "session_id": "cli-session-abc123",
                "timestamp": "2025-11-13T14:30:00Z",
                "event_type": "session_started",
                "user_input": "Observei que LLMs aumentam produtividade",
                "metadata": {}
            }
        }
    )


class SessionCompletedEvent(BaseEvent):
    """
    Evento emitido quando uma sessão finaliza.

    Attributes:
        final_status (str): Status final (approved, rejected, needs_refinement)
        tokens_total (int): Total de tokens consumidos na sessão
        metadata (dict): Metadados adicionais opcionais
    """
    event_type: Literal["session_completed"] = "session_completed"
    final_status: str = Field(..., description="Status final da sessão")
    tokens_total: int = Field(0, ge=0, description="Total de tokens da sessão")
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Metadados adicionais opcionais"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "session_id": "cli-session-abc123",
                "timestamp": "2025-11-13T14:32:00Z",
                "event_type": "session_completed",
                "final_status": "approved",
                "tokens_total": 850,
                "metadata": {"duration_seconds": 120}
            }
        }
    )


class CognitiveModelUpdatedEvent(BaseEvent):
    """
    Evento emitido quando o Observador atualiza o CognitiveModel (Epico 10.2).

    Este evento e publicado silenciosamente a cada turno processado
    pelo Observador. Permite ao Dashboard exibir evolucao do argumento.

    Attributes:
        turn_number (int): Numero do turno processado
        solidez (float): Solidez atual do argumento (0-1)
        completude (float): Completude atual do argumento (0-1)
        claims_count (int): Numero de claims no modelo
        proposicoes_count (int): Numero de proposicoes/fundamentos
        concepts_count (int): Numero de conceitos detectados
        open_questions_count (int): Numero de questoes abertas
        contradictions_count (int): Numero de contradicoes detectadas
        is_mature (bool): Se argumento atingiu maturidade
        metadata (dict): Metadados adicionais opcionais
    """
    event_type: Literal["cognitive_model_updated"] = "cognitive_model_updated"
    turn_number: int = Field(..., ge=1, description="Numero do turno processado")
    solidez: float = Field(..., ge=0.0, le=1.0, description="Solidez do argumento")
    completude: float = Field(..., ge=0.0, le=1.0, description="Completude do argumento")
    claims_count: int = Field(0, ge=0, description="Numero de claims")
    proposicoes_count: int = Field(0, ge=0, description="Numero de proposicoes")
    concepts_count: int = Field(0, ge=0, description="Numero de conceitos")
    open_questions_count: int = Field(0, ge=0, description="Numero de questoes abertas")
    contradictions_count: int = Field(0, ge=0, description="Numero de contradicoes")
    is_mature: bool = Field(False, description="Se argumento esta maduro")
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Metadados adicionais opcionais"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "session_id": "cli-session-abc123",
                "timestamp": "2025-12-05T18:30:00Z",
                "event_type": "cognitive_model_updated",
                "turn_number": 3,
                "solidez": 0.65,
                "completude": 0.50,
                "claims_count": 1,
                "proposicoes_count": 2,
                "concepts_count": 3,
                "open_questions_count": 1,
                "contradictions_count": 0,
                "is_mature": False,
                "metadata": {"claim": "LLMs aumentam produtividade"}
            }
        }
    )


class ClarificationRequestedEvent(BaseEvent):
    """
    Evento emitido quando Orquestrador faz pergunta de esclarecimento (Epico 14).

    Este evento e publicado quando o sistema detecta necessidade de
    esclarecimento e faz uma pergunta ao usuario.

    Attributes:
        turn_number (int): Numero do turno atual
        clarification_type (str): Tipo de esclarecimento (contradiction, gap, confusion)
        question (str): Pergunta feita ao usuario
        priority (str): Prioridade do esclarecimento (high, medium, low)
        related_context (dict): Contexto relacionado (proposicoes, contradicoes, etc)
        metadata (dict): Metadados adicionais opcionais
    """
    event_type: Literal["clarification_requested"] = "clarification_requested"
    turn_number: int = Field(..., ge=1, description="Numero do turno atual")
    clarification_type: str = Field(..., description="Tipo de esclarecimento")
    question: str = Field(..., description="Pergunta feita ao usuario")
    priority: str = Field("medium", description="Prioridade do esclarecimento")
    related_context: Dict[str, Any] = Field(
        default_factory=dict,
        description="Contexto relacionado (proposicoes, contradicoes, etc)"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Metadados adicionais opcionais"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "session_id": "cli-session-abc123",
                "timestamp": "2025-12-09T18:30:00Z",
                "event_type": "clarification_requested",
                "turn_number": 5,
                "clarification_type": "contradiction",
                "question": "Voce mencionou X e Y. Eles se aplicam em situacoes diferentes?",
                "priority": "medium",
                "related_context": {
                    "proposicoes": ["LLMs aumentam produtividade", "LLMs aumentam bugs"],
                    "contradiction_description": "Aumento de produtividade vs aumento de bugs"
                },
                "metadata": {}
            }
        }
    )


class ClarificationResolvedEvent(BaseEvent):
    """
    Evento emitido quando esclarecimento e obtido (Epico 14).

    Este evento e publicado apos usuario responder pergunta de esclarecimento
    e Observer analisar a resposta.

    Attributes:
        turn_number (int): Numero do turno atual
        clarification_type (str): Tipo de esclarecimento original
        resolution_status (str): Status da resolucao (resolved, partially_resolved, unresolved)
        summary (str): Resumo do que foi esclarecido
        updates_made (dict): Atualizacoes feitas no CognitiveModel
        metadata (dict): Metadados adicionais opcionais
    """
    event_type: Literal["clarification_resolved"] = "clarification_resolved"
    turn_number: int = Field(..., ge=1, description="Numero do turno atual")
    clarification_type: str = Field(..., description="Tipo de esclarecimento original")
    resolution_status: str = Field(..., description="Status da resolucao")
    summary: str = Field(..., description="Resumo do que foi esclarecido")
    updates_made: Dict[str, Any] = Field(
        default_factory=dict,
        description="Atualizacoes feitas no CognitiveModel"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Metadados adicionais opcionais"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "session_id": "cli-session-abc123",
                "timestamp": "2025-12-09T18:32:00Z",
                "event_type": "clarification_resolved",
                "turn_number": 6,
                "clarification_type": "contradiction",
                "resolution_status": "resolved",
                "summary": "Usuario esclareceu que produtividade aumenta em tarefas simples, bugs aumentam em tarefas complexas",
                "updates_made": {
                    "contradictions_resolved": 1,
                    "proposicoes_added": 2
                },
                "metadata": {}
            }
        }
    )


# Union type para deserializacao automatica
EventType = (
    AgentStartedEvent |
    AgentCompletedEvent |
    AgentErrorEvent |
    SessionStartedEvent |
    SessionCompletedEvent |
    CognitiveModelUpdatedEvent |
    ClarificationRequestedEvent |
    ClarificationResolvedEvent
)
