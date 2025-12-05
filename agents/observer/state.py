"""
Definicao do estado do agente Observador.

Este modulo define o schema do estado usado pelo Observador (Mente Analitica)
para processar turnos e atualizar o CognitiveModel.

O ObserverState e interno ao Observador e nao e compartilhado diretamente
com outros agentes. O output do Observador e comunicado via:
- CognitiveModel (atualizado em memoria)
- Eventos publicados no EventBus
- API de consulta (ObservadorAPI)

Versao: 1.0 (Epico 10.1 - Mitose do Orquestrador)
Data: 05/12/2025
"""

from typing import TypedDict, Optional, List, Dict, Any
from dataclasses import dataclass


class ObserverState(TypedDict):
    """
    Estado interno do agente Observador.

    Mantem informacoes de processamento de turno. Este estado e usado
    internamente pelo Observador e nao e exposto diretamente para outros agentes.

    O Observador processa TODOS os turnos da conversa e atualiza o CognitiveModel
    completo. Este estado captura o processo de extracao.

    === CAMPOS DE INPUT ===

    user_input (str):
        Mensagem atual do usuario sendo processada.
        Copiada do MultiAgentState a cada turno.

    conversation_history (list[dict]):
        Historico completo da conversa ate o turno atual.
        Formato: [{"role": "user"|"assistant", "content": str}, ...]

    previous_cognitive_model (Optional[dict]):
        Modelo cognitivo do turno anterior (se existir).
        Usado para calcular diferencas e evolucao.

    === CAMPOS DE EXTRACAO (OUTPUT DO PROCESSAMENTO) ===

    extracted_claims (list[str]):
        Claims (proposicoes centrais) extraidos do turno atual.
        Detectados via LLM com prompt especifico.

    extracted_concepts (list[str]):
        Conceitos-chave (essencias semanticas) extraidos.
        Serao salvos no catalogo (ChromaDB + SQLite) em 10.3+.

    extracted_fundamentos (list[str]):
        Fundamentos (argumentos de suporte) identificados.
        Usados para calcular solidez.

    extracted_contradictions (list[dict]):
        Contradicoes detectadas entre claims.
        Estrutura: {"claim_a": str, "claim_b": str, "explanation": str}

    extracted_open_questions (list[str]):
        Lacunas identificadas que precisam investigacao.
        Geradas quando LLM detecta gaps no raciocinio.

    === CAMPOS DE METRICAS ===

    solidez_calculated (float):
        Solidez geral calculada (0-1).
        Baseada em: fundamentos solidos / total de claims.

    completude_calculated (float):
        Completude calculada (0-1).
        Baseada em: (total - open_questions) / total.

    === CAMPOS DE CONTROLE ===

    turn_number (int):
        Numero do turno sendo processado.
        Usado para logging e rastreabilidade.

    processing_timestamp (Optional[str]):
        Timestamp ISO do processamento.
        Formato: "2025-12-05T18:30:00Z"

    Notes:
        - Este estado e interno ao Observador
        - Nao confundir com MultiAgentState (estado global do sistema)
        - CognitiveModel e o OUTPUT do processamento (nao faz parte deste state)
    """

    # === INPUT ===
    user_input: str
    conversation_history: List[Dict[str, Any]]
    previous_cognitive_model: Optional[Dict[str, Any]]

    # === EXTRACAO ===
    extracted_claims: List[str]
    extracted_concepts: List[str]
    extracted_fundamentos: List[str]
    extracted_contradictions: List[Dict[str, Any]]
    extracted_open_questions: List[str]

    # === METRICAS ===
    solidez_calculated: float
    completude_calculated: float

    # === CONTROLE ===
    turn_number: int
    processing_timestamp: Optional[str]


def create_initial_observer_state(
    user_input: str,
    conversation_history: List[Dict[str, Any]],
    previous_cognitive_model: Optional[Dict[str, Any]] = None,
    turn_number: int = 1
) -> ObserverState:
    """
    Cria estado inicial do Observador para processar um turno.

    Args:
        user_input: Mensagem atual do usuario.
        conversation_history: Historico completo da conversa.
        previous_cognitive_model: CognitiveModel do turno anterior (se existir).
        turn_number: Numero do turno atual.

    Returns:
        ObserverState: Estado inicial pronto para processamento.

    Example:
        >>> state = create_initial_observer_state(
        ...     user_input="LLMs aumentam produtividade",
        ...     conversation_history=[{"role": "user", "content": "LLMs aumentam produtividade"}],
        ...     turn_number=1
        ... )
        >>> state['user_input']
        'LLMs aumentam produtividade'
        >>> state['extracted_claims']
        []
    """
    from datetime import datetime, timezone

    return ObserverState(
        # Input
        user_input=user_input,
        conversation_history=conversation_history,
        previous_cognitive_model=previous_cognitive_model,

        # Extracao (vazio - sera preenchido pelo processamento)
        extracted_claims=[],
        extracted_concepts=[],
        extracted_fundamentos=[],
        extracted_contradictions=[],
        extracted_open_questions=[],

        # Metricas (zeradas - serao calculadas)
        solidez_calculated=0.0,
        completude_calculated=0.0,

        # Controle
        turn_number=turn_number,
        processing_timestamp=datetime.now(timezone.utc).isoformat()
    )


@dataclass
class ObserverInsight:
    """
    Insight contextual retornado pelo Observador em resposta a consulta.

    Quando o Orquestrador consulta o Observador via `what_do_you_see()`,
    esta estrutura encapsula a resposta.

    Attributes:
        insight: Observacao principal sobre o estado atual.
        suggestion: Sugestao de acao (opcional, nao e comando).
        confidence: Confianca na observacao (0-1).
        evidence: Dados do CognitiveModel que sustentam o insight.

    Example:
        >>> insight = ObserverInsight(
        ...     insight="Parcial - LLMs ainda central, bugs e novo foco",
        ...     suggestion="Pode conectar: bugs como metrica de produtividade",
        ...     confidence=0.8,
        ...     evidence={"concepts": ["LLMs", "bugs"], "claims": [...]}
        ... )
        >>> insight.confidence
        0.8
    """

    insight: str
    suggestion: Optional[str]
    confidence: float
    evidence: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        """Serializa para dict."""
        return {
            "insight": self.insight,
            "suggestion": self.suggestion,
            "confidence": self.confidence,
            "evidence": self.evidence
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ObserverInsight":
        """Cria instancia a partir de dict."""
        return cls(
            insight=data.get("insight", ""),
            suggestion=data.get("suggestion"),
            confidence=data.get("confidence", 0.5),
            evidence=data.get("evidence", {})
        )
