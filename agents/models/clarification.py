"""
Schema Pydantic para Clarification (Esclarecimento).

Este modulo define modelos para o sistema de consultas inteligentes do Observer.
Quando o Observer detecta confusao ou tensoes, ele identifica pontos que precisam
esclarecimento e sugere como o Orquestrador pode formular perguntas naturais.

Filosofia:
- Observer identifica O QUE precisa esclarecimento
- Orquestrador formula perguntas NATURAIS (nao roboticas)
- Tom de parceiro pensante, nao fiscalizador
- Perguntas ajudam a AVANCAR, nao apenas apontam problemas

Epico 14: Observer - Consultas Inteligentes
Data: 2025-12-09
"""

from typing import Optional, List, Literal
from uuid import uuid4
from pydantic import BaseModel, Field, ConfigDict


class ClarificationContext(BaseModel):
    """
    Contexto relevante para uma necessidade de esclarecimento.

    Agrupa as proposicoes, contradicoes e questoes abertas
    relacionadas ao ponto que precisa esclarecimento.

    Attributes:
        proposicoes: IDs ou textos das proposicoes envolvidas
        contradictions: Descricoes das contradicoes relacionadas
        open_questions: Questoes abertas relevantes
        claim_excerpt: Trecho do claim afetado
    """

    proposicoes: List[str] = Field(
        default_factory=list,
        description="Textos das proposicoes envolvidas no esclarecimento"
    )

    contradictions: List[str] = Field(
        default_factory=list,
        description="Descricoes das contradicoes relacionadas"
    )

    open_questions: List[str] = Field(
        default_factory=list,
        description="Questoes abertas relevantes ao esclarecimento"
    )

    claim_excerpt: Optional[str] = Field(
        default=None,
        description="Trecho do claim afetado pelo esclarecimento"
    )

    model_config = ConfigDict(extra="forbid")


class ClarificationNeed(BaseModel):
    """
    Necessidade de esclarecimento identificada pelo Observer.

    Quando o Observer detecta confusao, tensoes ou gaps, ele cria
    uma ClarificationNeed descrevendo o que precisa ser esclarecido
    e sugerindo como abordar.

    Attributes:
        id: UUID unico da necessidade
        needs_clarification: Se realmente precisa esclarecimento
        clarification_type: Tipo de esclarecimento necessario
        description: Descricao textual do que precisa ser esclarecido
        relevant_context: Contexto relacionado (proposicoes, contradicoes, etc)
        suggested_approach: Sugestao de como perguntar
        priority: Prioridade do esclarecimento
        turn_detected: Turno em que foi detectado

    Clarification Types:
        - contradiction: Tensao entre proposicoes
        - gap: Informacao faltante para o claim
        - confusion: Confusao geral detectada
        - direction_change: Mudanca de direcao nao confirmada

    Example:
        >>> need = ClarificationNeed(
        ...     needs_clarification=True,
        ...     clarification_type="contradiction",
        ...     description="Usuario disse que LLMs aumentam produtividade "
        ...                 "mas tambem que aumentam bugs",
        ...     suggested_approach="Explorar se os contextos sao diferentes",
        ...     priority="high"
        ... )
    """

    id: str = Field(
        default_factory=lambda: str(uuid4()),
        description="UUID unico da necessidade de esclarecimento"
    )

    needs_clarification: bool = Field(
        default=True,
        description="Se realmente precisa esclarecimento (pode ser False se gap e menor)"
    )

    clarification_type: Literal["contradiction", "gap", "confusion", "direction_change"] = Field(
        ...,
        description="Tipo de esclarecimento necessario"
    )

    description: str = Field(
        ...,
        description="Descricao textual do que precisa ser esclarecido",
        min_length=1
    )

    relevant_context: ClarificationContext = Field(
        default_factory=ClarificationContext,
        description="Contexto relevante (proposicoes, contradicoes, etc)"
    )

    suggested_approach: Optional[str] = Field(
        default=None,
        description="Sugestao de como abordar o esclarecimento (None se nao precisa)"
    )

    priority: Literal["high", "medium", "low"] = Field(
        default="medium",
        description="Prioridade do esclarecimento"
    )

    turn_detected: int = Field(
        default=0,
        description="Turno em que a necessidade foi detectada",
        ge=0
    )

    turns_persisted: int = Field(
        default=0,
        description="Numero de turnos que essa necessidade persiste",
        ge=0
    )

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "id": "clar-550e8400-e29b-41d4-a716-446655440000",
                "needs_clarification": True,
                "clarification_type": "contradiction",
                "description": "Usuario disse que LLMs aumentam produtividade mas tambem que aumentam bugs",
                "relevant_context": {
                    "proposicoes": [
                        "LLMs aumentam produtividade em 30%",
                        "LLMs aumentam quantidade de bugs"
                    ],
                    "contradictions": ["Aumento de produtividade vs aumento de bugs"],
                    "open_questions": [],
                    "claim_excerpt": "LLMs impactam desenvolvimento"
                },
                "suggested_approach": "Explorar se os contextos sao diferentes (tipo de tarefa, experiencia do dev)",
                "priority": "high",
                "turn_detected": 3,
                "turns_persisted": 2
            }
        }
    )

    def to_dict(self) -> dict:
        """Serializa para dict."""
        return self.model_dump()

    @classmethod
    def from_dict(cls, data: dict) -> "ClarificationNeed":
        """Cria instancia a partir de dict."""
        return cls(**data)


class ClarificationTimingDecision(BaseModel):
    """
    Decisao de timing para fazer pergunta de esclarecimento.

    O Observer sugere quando perguntar, e o Orquestrador decide.
    Esta classe encapsula a recomendacao do Observer.

    Attributes:
        should_ask: Se deve fazer a pergunta agora
        reason: Razao da decisao
        delay_turns: Quantos turnos esperar (0 = agora)
        urgency: Nivel de urgencia

    Timing Rules:
        - NAO pergunta apos cada input
        - Pergunta quando confusao se acumula
        - Pergunta quando contradicao persiste 2+ turns
        - NAO pergunta quando usuario esta fluindo bem

    Example:
        >>> decision = ClarificationTimingDecision(
        ...     should_ask=True,
        ...     reason="Contradicao persiste ha 3 turnos",
        ...     delay_turns=0,
        ...     urgency="medium"
        ... )
    """

    should_ask: bool = Field(
        ...,
        description="Se deve fazer a pergunta agora"
    )

    reason: str = Field(
        ...,
        description="Razao da decisao (por que perguntar ou nao)",
        min_length=1
    )

    delay_turns: int = Field(
        default=0,
        description="Quantos turnos esperar antes de perguntar (0 = agora)",
        ge=0
    )

    urgency: Literal["high", "medium", "low"] = Field(
        default="medium",
        description="Nivel de urgencia da pergunta"
    )

    model_config = ConfigDict(extra="forbid")


class ClarificationUpdates(BaseModel):
    """
    Atualizacoes a fazer no CognitiveModel apos esclarecimento.

    Define quais proposicoes atualizar, contradicoes resolver,
    e questoes abertas fechar.

    Attributes:
        proposicoes_to_add: Novas proposicoes a adicionar
        proposicoes_to_update: Proposicoes existentes a atualizar (id -> novo texto/solidez)
        contradictions_to_resolve: Indices de contradicoes resolvidas
        open_questions_to_close: Indices de questoes abertas respondidas
        context_to_add: Contexto adicional a incluir
    """

    proposicoes_to_add: List[str] = Field(
        default_factory=list,
        description="Textos de novas proposicoes a adicionar"
    )

    proposicoes_to_update: dict = Field(
        default_factory=dict,
        description="Proposicoes a atualizar (id -> {texto, solidez})"
    )

    contradictions_to_resolve: List[int] = Field(
        default_factory=list,
        description="Indices das contradicoes resolvidas"
    )

    open_questions_to_close: List[int] = Field(
        default_factory=list,
        description="Indices das questoes abertas respondidas"
    )

    context_to_add: dict = Field(
        default_factory=dict,
        description="Contexto adicional a incluir no CognitiveModel"
    )

    model_config = ConfigDict(extra="forbid")


class ClarificationResponse(BaseModel):
    """
    Analise da resposta do usuario a uma pergunta de esclarecimento.

    Apos o usuario responder uma pergunta de esclarecimento, o Observer
    analisa se a confusao foi resolvida e que atualizacoes fazer.

    Attributes:
        resolution_status: Estado da resolucao
        summary: Resumo do que foi esclarecido
        updates: Atualizacoes a fazer no CognitiveModel
        needs_followup: Se precisa pergunta de acompanhamento
        followup_suggestion: Sugestao de pergunta de acompanhamento

    Resolution Status:
        - resolved: Esclarecimento completo
        - partially_resolved: Algumas duvidas permanecem
        - unresolved: Resposta nao esclareceu

    Example:
        >>> response = ClarificationResponse(
        ...     resolution_status="resolved",
        ...     summary="Usuario esclareceu que produtividade aumenta em tarefas simples, "
        ...             "bugs aumentam em tarefas complexas",
        ...     needs_followup=False
        ... )
    """

    resolution_status: Literal["resolved", "partially_resolved", "unresolved"] = Field(
        ...,
        description="Estado da resolucao do esclarecimento"
    )

    summary: str = Field(
        ...,
        description="Resumo do que foi esclarecido",
        min_length=1
    )

    updates: ClarificationUpdates = Field(
        default_factory=ClarificationUpdates,
        description="Atualizacoes a fazer no CognitiveModel"
    )

    needs_followup: bool = Field(
        default=False,
        description="Se precisa pergunta de acompanhamento"
    )

    followup_suggestion: Optional[str] = Field(
        default=None,
        description="Sugestao de pergunta de acompanhamento (se needs_followup=True)"
    )

    model_config = ConfigDict(extra="forbid")


class QuestionSuggestion(BaseModel):
    """
    Sugestao de pergunta para gap ou contradicao.

    O Observer sugere perguntas para preencher gaps ou explorar
    tensoes. O Orquestrador usa como base para formular pergunta natural.

    Attributes:
        question_text: Texto sugerido da pergunta
        target_type: O que a pergunta visa esclarecer
        related_proposicoes: Proposicoes relacionadas
        expected_outcome: O que se espera esclarecer com a resposta
        tone_guidance: Orientacao sobre tom da pergunta

    Example:
        >>> suggestion = QuestionSuggestion(
        ...     question_text="Voce tem algum dado ou experiencia que mostre esse aumento?",
        ...     target_type="gap",
        ...     expected_outcome="Evidencia empirica para a afirmacao",
        ...     tone_guidance="Curiosidade genuina, nao cobranca"
        ... )
    """

    question_text: str = Field(
        ...,
        description="Texto sugerido da pergunta",
        min_length=1
    )

    target_type: Literal["contradiction", "gap", "confusion"] = Field(
        ...,
        description="O que a pergunta visa esclarecer"
    )

    related_proposicoes: List[str] = Field(
        default_factory=list,
        description="Textos das proposicoes relacionadas"
    )

    expected_outcome: str = Field(
        ...,
        description="O que se espera esclarecer com a resposta",
        min_length=1
    )

    tone_guidance: str = Field(
        default="Curiosidade genuina e parceria intelectual",
        description="Orientacao sobre tom da pergunta"
    )

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "question_text": "Voce tem algum dado ou experiencia que mostre esse aumento de produtividade?",
                "target_type": "gap",
                "related_proposicoes": ["LLMs aumentam produtividade em 30%"],
                "expected_outcome": "Evidencia empirica ou experiencia pessoal para sustentar a afirmacao",
                "tone_guidance": "Curiosidade genuina, nao cobranca"
            }
        }
    )
