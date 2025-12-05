"""
Definição do estado do agente Observador.

Este módulo define o schema do estado que o Observador usa durante
o processamento de um turno de conversa.

Diferente do MultiAgentState (compartilhado entre agentes),
o ObserverState é específico para o processamento interno do Observador.

Épico 10.1: Mitose do Orquestrador
Data: 05/12/2025
"""

from typing import TypedDict, Optional, List, Dict, Any
from uuid import UUID


class ObserverState(TypedDict):
    """
    Estado interno do agente Observador.

    Este estado mantém informações do processamento de turno,
    não confundir com CognitiveModel (que é o output global).

    === CAMPOS DE ENTRADA ===

    user_input (str):
        Input atual do usuário sendo processado.
        Usado para extração de claims e conceitos.

    conversation_history (list[dict]):
        Histórico completo da conversa em formato estruturado.
        Cada item contém: {"role": "user"|"assistant", "content": str}

    previous_cognitive_model (dict | None):
        CognitiveModel do turno anterior (se existir).
        Usado para detectar evolução e calcular deltas.

    === CAMPOS DE SAÍDA (Extração) ===

    extracted_claims (list[str]):
        Claims (proposições centrais) extraídas do turno atual.
        Exemplo: ["LLMs aumentam produtividade"]

    extracted_concepts (list[str]):
        Conceitos semânticos extraídos do turno atual.
        Exemplo: ["LLMs", "produtividade"]

    extracted_fundamentos (list[str]):
        Fundamentos (argumentos de suporte) identificados.
        Exemplo: ["Equipes reportam 30% menos tempo"]

    extracted_contradictions (list[dict]):
        Contradições detectadas entre claims/fundamentos.
        Estrutura: {"claim_a": str, "claim_b": str, "explanation": str}

    extracted_open_questions (list[str]):
        Lacunas/questões abertas identificadas.
        Exemplo: ["Como medir produtividade?"]

    === CAMPOS DE SAÍDA (Métricas) ===

    solidez_calculated (float):
        Solidez geral calculada (0-1).
        Mede a força da argumentação atual.

    completude_calculated (float):
        Completude calculada (0-1).
        Mede quanto do argumento está desenvolvido.

    === FLAGS DE NOVIDADES ===

    has_new_concepts (bool):
        True se conceitos novos foram detectados neste turno.
        Usado para filtrar eventos na timeline.

    has_new_contradictions (bool):
        True se novas contradições foram detectadas.
        Usado para alertar o Orquestrador.

    solidez_changed_significantly (bool):
        True se solidez mudou > 15% em relação ao turno anterior.
        Usado para mostrar evolução na timeline.
    """

    # === ENTRADA ===
    user_input: str
    conversation_history: List[Dict[str, Any]]
    previous_cognitive_model: Optional[Dict[str, Any]]

    # === SAÍDA: EXTRAÇÃO ===
    extracted_claims: List[str]
    extracted_concepts: List[str]
    extracted_fundamentos: List[str]
    extracted_contradictions: List[Dict[str, Any]]
    extracted_open_questions: List[str]

    # === SAÍDA: MÉTRICAS ===
    solidez_calculated: float
    completude_calculated: float

    # === FLAGS ===
    has_new_concepts: bool
    has_new_contradictions: bool
    solidez_changed_significantly: bool


def create_initial_observer_state(
    user_input: str,
    conversation_history: Optional[List[Dict[str, Any]]] = None,
    previous_cognitive_model: Optional[Dict[str, Any]] = None,
) -> ObserverState:
    """
    Cria estado inicial do Observador para processar um turno.

    Args:
        user_input: Input atual do usuário.
        conversation_history: Histórico da conversa (opcional).
        previous_cognitive_model: CognitiveModel do turno anterior (opcional).

    Returns:
        ObserverState: Estado inicial pronto para processamento.

    Example:
        >>> state = create_initial_observer_state(
        ...     user_input="LLMs aumentam produtividade",
        ...     conversation_history=[{"role": "user", "content": "Olá"}]
        ... )
        >>> state['user_input']
        'LLMs aumentam produtividade'
        >>> state['extracted_claims']
        []
    """
    return ObserverState(
        # Entrada
        user_input=user_input,
        conversation_history=conversation_history or [],
        previous_cognitive_model=previous_cognitive_model,

        # Saída: Extração (vazios inicialmente)
        extracted_claims=[],
        extracted_concepts=[],
        extracted_fundamentos=[],
        extracted_contradictions=[],
        extracted_open_questions=[],

        # Saída: Métricas (zeros inicialmente)
        solidez_calculated=0.0,
        completude_calculated=0.0,

        # Flags (falsos inicialmente)
        has_new_concepts=False,
        has_new_contradictions=False,
        solidez_changed_significantly=False,
    )
