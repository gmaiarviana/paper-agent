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


# ============================================================================
# Eventos do Epico 13.5 - Timeline Visual de Mudancas
# ============================================================================


class VariationDetectedEvent(BaseEvent):
    """
    Evento emitido quando Observer detecta variacao (nao mudanca real) (Epico 13.5).

    Este evento e publicado discretamente quando o Observer identifica que
    o input do usuario e uma variacao do conceito anterior (mesma essencia),
    nao uma mudanca real de direcao. Nao interrompe o fluxo da conversa.

    Attributes:
        turn_number (int): Numero do turno atual
        classification (str): Sempre "variation" para este evento
        essence_previous (str): Essencia semantica do texto anterior
        essence_new (str): Essencia semantica do novo texto
        shared_concepts (list): Conceitos mantidos entre os textos
        new_concepts (list): Novos conceitos introduzidos
        analysis (str): Analise textual do LLM
        metadata (dict): Metadados adicionais opcionais
    """
    event_type: Literal["variation_detected"] = "variation_detected"
    turn_number: int = Field(..., ge=1, description="Numero do turno atual")
    classification: Literal["variation"] = Field(
        "variation",
        description="Classificacao da deteccao (sempre 'variation')"
    )
    essence_previous: str = Field(..., description="Essencia semantica do texto anterior")
    essence_new: str = Field(..., description="Essencia semantica do novo texto")
    shared_concepts: list = Field(
        default_factory=list,
        description="Conceitos mantidos entre os textos"
    )
    new_concepts: list = Field(
        default_factory=list,
        description="Novos conceitos introduzidos"
    )
    analysis: str = Field("", description="Analise textual do LLM")
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Metadados adicionais opcionais"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "session_id": "cli-session-abc123",
                "timestamp": "2025-12-10T10:30:00Z",
                "event_type": "variation_detected",
                "turn_number": 3,
                "classification": "variation",
                "essence_previous": "LLMs aumentam produtividade de desenvolvedores",
                "essence_new": "IA generativa melhora eficiencia no desenvolvimento",
                "shared_concepts": ["produtividade", "desenvolvimento", "IA"],
                "new_concepts": ["eficiencia"],
                "analysis": "Ambos textos tratam do impacto positivo de IA/LLMs na produtividade",
                "metadata": {}
            }
        }
    )


class DirectionChangeConfirmedEvent(BaseEvent):
    """
    Evento emitido quando mudanca real de direcao e detectada/confirmada (Epico 13.5).

    Este evento e publicado quando o Observer detecta que o usuario mudou
    de foco para um topico fundamentalmente diferente. Pode incluir
    confirmacao do usuario se o Orchestrator solicitou checkpoint.

    Attributes:
        turn_number (int): Numero do turno atual
        classification (str): Sempre "real_change" para este evento
        previous_claim (str): Claim/foco anterior da conversa
        new_claim (str): Novo claim/foco identificado
        user_confirmed (bool): Se usuario confirmou a mudanca (via checkpoint)
        reasoning (str): Justificativa para classificacao como mudanca real
        metadata (dict): Metadados adicionais opcionais
    """
    event_type: Literal["direction_change_confirmed"] = "direction_change_confirmed"
    turn_number: int = Field(..., ge=1, description="Numero do turno atual")
    classification: Literal["real_change"] = Field(
        "real_change",
        description="Classificacao da deteccao (sempre 'real_change')"
    )
    previous_claim: str = Field(..., description="Claim/foco anterior da conversa")
    new_claim: str = Field(..., description="Novo claim/foco identificado")
    user_confirmed: bool = Field(
        False,
        description="Se usuario confirmou a mudanca (via checkpoint)"
    )
    reasoning: str = Field("", description="Justificativa para classificacao")
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Metadados adicionais opcionais"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "session_id": "cli-session-abc123",
                "timestamp": "2025-12-10T10:35:00Z",
                "event_type": "direction_change_confirmed",
                "turn_number": 5,
                "classification": "real_change",
                "previous_claim": "LLMs aumentam produtividade de desenvolvedores",
                "new_claim": "Blockchain revoluciona transacoes financeiras",
                "user_confirmed": True,
                "reasoning": "Topicos completamente distintos sem conexao semantica",
                "metadata": {}
            }
        }
    )


class ClarityCheckpointEvent(BaseEvent):
    """
    Evento emitido quando checkpoint de clareza e solicitado (Epico 13.5).

    Este evento e publicado quando o Observer detecta que a conversa
    esta nebulosa ou confusa e o Orchestrator decide solicitar
    esclarecimento ao usuario.

    Attributes:
        turn_number (int): Numero do turno atual
        clarity_level (str): Nivel de clareza detectado (nebulosa, confusa)
        clarity_score (int): Score numerico de clareza (1-5)
        checkpoint_reason (str): Razao para solicitar checkpoint
        factors (dict): Fatores que contribuiram para avaliacao
        suggestion (str): Sugestao de como esclarecer
        metadata (dict): Metadados adicionais opcionais
    """
    event_type: Literal["clarity_checkpoint"] = "clarity_checkpoint"
    turn_number: int = Field(..., ge=1, description="Numero do turno atual")
    clarity_level: str = Field(
        ...,
        description="Nivel de clareza (cristalina, clara, nebulosa, confusa)"
    )
    clarity_score: int = Field(
        ...,
        ge=1,
        le=5,
        description="Score numerico de clareza (1=confusa, 5=cristalina)"
    )
    checkpoint_reason: str = Field(..., description="Razao para solicitar checkpoint")
    factors: Dict[str, str] = Field(
        default_factory=dict,
        description="Fatores da avaliacao (claim_definition, coherence, direction_stability)"
    )
    suggestion: str = Field("", description="Sugestao de como esclarecer")
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Metadados adicionais opcionais"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "session_id": "cli-session-abc123",
                "timestamp": "2025-12-10T10:40:00Z",
                "event_type": "clarity_checkpoint",
                "turn_number": 4,
                "clarity_level": "nebulosa",
                "clarity_score": 2,
                "checkpoint_reason": "Multiplos topicos mencionados sem conexao clara",
                "factors": {
                    "claim_definition": "vago",
                    "coherence": "baixa",
                    "direction_stability": "instavel"
                },
                "suggestion": "Qual desses topicos voce gostaria de explorar primeiro?",
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
    ClarificationResolvedEvent |
    # Epico 13.5 - Timeline Visual de Mudancas
    VariationDetectedEvent |
    DirectionChangeConfirmedEvent |
    ClarityCheckpointEvent
)
