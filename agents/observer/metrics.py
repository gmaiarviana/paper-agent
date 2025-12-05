"""
Cálculo de métricas do Observador.

Este módulo implementa funções para calcular solidez e completude
do argumento baseado no estado do CognitiveModel.

As métricas são usadas pelo Observador para avaliar a evolução
do raciocínio e informar o Orquestrador sobre o estado atual.

Épico 10.1: Mitose do Orquestrador
Data: 05/12/2025
"""

import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


def calculate_solidez(cognitive_data: Dict[str, Any]) -> float:
    """
    Calcula solidez do argumento (0-1).

    Solidez mede a força/fundação do argumento baseado em:
    - Especificidade do claim (0-20%)
    - Força dos fundamentos/premissas (0-25%)
    - Fraqueza das suposições não verificadas (0-20%)
    - Questões respondidas (0-20%)
    - Ausência de contradições (0-15%)
    - Presença de evidências bibliográficas (0-10% bonus)

    Total máximo: 110%, normalizado para 100% (1.0).

    Args:
        cognitive_data: Dict com campos do CognitiveModel.
            Campos esperados: claim, premises, assumptions,
            open_questions, contradictions, solid_grounds.

    Returns:
        float: Solidez normalizada (0-1).

    Example:
        >>> data = {
        ...     "claim": "LLMs aumentam produtividade em 30%",
        ...     "premises": ["Equipes usam LLMs", "Tempo é mensurável"],
        ...     "assumptions": [],
        ...     "open_questions": [],
        ...     "contradictions": [],
        ...     "solid_grounds": []
        ... }
        >>> solidez = calculate_solidez(data)
        >>> print(f"Solidez: {solidez:.2f}")
        Solidez: 0.80
    """
    score = 0.0

    # Extrai campos com fallback
    claim = cognitive_data.get("claim", "")
    premises = cognitive_data.get("premises", [])
    assumptions = cognitive_data.get("assumptions", [])
    open_questions = cognitive_data.get("open_questions", [])
    contradictions = cognitive_data.get("contradictions", [])
    solid_grounds = cognitive_data.get("solid_grounds", [])

    # 1. Especificidade do claim (0-20)
    claim_len = len(claim) if isinstance(claim, str) else 0
    if claim_len > 50:
        score += 20
    elif claim_len > 20:
        score += 10 + min(10, (claim_len - 20) / 3)
    elif claim_len > 0:
        score += 5

    # 2. Força dos fundamentos (0-25)
    premises_count = len(premises) if isinstance(premises, list) else 0
    if premises_count >= 3:
        score += 25
    elif premises_count == 2:
        score += 20
    elif premises_count == 1:
        score += 10

    # 3. Fraqueza das suposições (0-20) - menos é melhor
    assumptions_count = len(assumptions) if isinstance(assumptions, list) else 0
    if assumptions_count == 0:
        score += 20
    elif assumptions_count == 1:
        score += 15
    elif assumptions_count == 2:
        score += 10
    elif assumptions_count <= 5:
        score += max(0, 10 - assumptions_count)

    # 4. Questões respondidas (0-20) - menos é melhor
    questions_count = len(open_questions) if isinstance(open_questions, list) else 0
    if questions_count == 0:
        score += 20
    elif questions_count == 1:
        score += 10
    elif questions_count == 2:
        score += 5

    # 5. Contradições resolvidas (0-15)
    contradictions_count = len(contradictions) if isinstance(contradictions, list) else 0
    if contradictions_count == 0:
        score += 15
    elif contradictions_count == 1:
        score += 5

    # 6. Evidências presentes (0-10 bonus)
    solid_count = len(solid_grounds) if isinstance(solid_grounds, list) else 0
    if solid_count > 0:
        score += min(10, solid_count * 3)

    # Normaliza para 0-1
    normalized = min(1.0, score / 100.0)

    logger.debug(
        f"Solidez calculada: {normalized:.2f} "
        f"(claim={claim_len}chars, premises={premises_count}, "
        f"assumptions={assumptions_count}, questions={questions_count}, "
        f"contradictions={contradictions_count}, evidence={solid_count})"
    )

    return normalized


def calculate_completude(cognitive_data: Dict[str, Any]) -> float:
    """
    Calcula completude do argumento (0-1).

    Completude mede quanto do argumento está desenvolvido baseado em:
    - Presença de claim (0-30%)
    - Presença de premissas (0-25%)
    - Poucas questões abertas (0-25%)
    - Poucas suposições não verificadas (0-20%)

    Total máximo: 100% (1.0).

    Args:
        cognitive_data: Dict com campos do CognitiveModel.
            Campos esperados: claim, premises, assumptions, open_questions.

    Returns:
        float: Completude normalizada (0-1).

    Example:
        >>> data = {
        ...     "claim": "LLMs aumentam produtividade em equipes de 2-5 devs",
        ...     "premises": ["Equipes usam LLMs", "Tempo é mensurável"],
        ...     "assumptions": [],
        ...     "open_questions": []
        ... }
        >>> completude = calculate_completude(data)
        >>> print(f"Completude: {completude:.2f}")
        Completude: 1.00
    """
    score = 0.0

    # Extrai campos com fallback
    claim = cognitive_data.get("claim", "")
    premises = cognitive_data.get("premises", [])
    assumptions = cognitive_data.get("assumptions", [])
    open_questions = cognitive_data.get("open_questions", [])

    # 1. Presença de claim (0-30)
    claim_len = len(claim) if isinstance(claim, str) else 0
    if claim_len > 50:
        score += 30
    elif claim_len > 20:
        score += 20
    elif claim_len > 0:
        score += 10

    # 2. Presença de premissas (0-25)
    premises_count = len(premises) if isinstance(premises, list) else 0
    if premises_count >= 3:
        score += 25
    elif premises_count == 2:
        score += 20
    elif premises_count == 1:
        score += 10

    # 3. Poucas questões abertas (0-25) - menos é melhor
    questions_count = len(open_questions) if isinstance(open_questions, list) else 0
    if questions_count == 0:
        score += 25
    elif questions_count == 1:
        score += 15
    elif questions_count == 2:
        score += 10
    elif questions_count <= 4:
        score += 5

    # 4. Poucas suposições (0-20) - menos é melhor
    assumptions_count = len(assumptions) if isinstance(assumptions, list) else 0
    if assumptions_count == 0:
        score += 20
    elif assumptions_count == 1:
        score += 15
    elif assumptions_count == 2:
        score += 10
    elif assumptions_count <= 4:
        score += 5

    # Normaliza para 0-1
    normalized = min(1.0, score / 100.0)

    logger.debug(
        f"Completude calculada: {normalized:.2f} "
        f"(claim={claim_len}chars, premises={premises_count}, "
        f"assumptions={assumptions_count}, questions={questions_count})"
    )

    return normalized


def calculate_delta_solidez(
    previous_solidez: float,
    current_solidez: float,
    threshold: float = 0.15
) -> Dict[str, Any]:
    """
    Calcula delta de solidez entre dois turnos.

    Útil para detectar mudanças significativas e informar na timeline.

    Args:
        previous_solidez: Solidez do turno anterior (0-1).
        current_solidez: Solidez do turno atual (0-1).
        threshold: Limite para considerar mudança significativa.

    Returns:
        Dict com:
            - delta: Diferença (pode ser negativa)
            - is_significant: True se |delta| > threshold
            - direction: "up", "down" ou "stable"
            - message: Mensagem descritiva

    Example:
        >>> delta = calculate_delta_solidez(0.50, 0.70)
        >>> delta['is_significant']
        True
        >>> delta['direction']
        'up'
    """
    delta = current_solidez - previous_solidez
    is_significant = abs(delta) > threshold

    if delta > threshold:
        direction = "up"
        message = f"Solidez aumentou: {previous_solidez:.0%} → {current_solidez:.0%}"
    elif delta < -threshold:
        direction = "down"
        message = f"Solidez diminuiu: {previous_solidez:.0%} → {current_solidez:.0%}"
    else:
        direction = "stable"
        message = f"Solidez estável: {current_solidez:.0%}"

    return {
        "delta": delta,
        "is_significant": is_significant,
        "direction": direction,
        "message": message,
        "previous": previous_solidez,
        "current": current_solidez,
    }


def get_solidez_indicator(solidez: float) -> str:
    """
    Retorna indicador visual de solidez.

    Args:
        solidez: Valor de solidez (0-1).

    Returns:
        str: Emoji indicador (verde, amarelo, vermelho).

    Example:
        >>> get_solidez_indicator(0.85)
        '🟢'
        >>> get_solidez_indicator(0.50)
        '🟡'
        >>> get_solidez_indicator(0.20)
        '🔴'
    """
    if solidez >= 0.7:
        return "🟢"  # Alta
    elif solidez >= 0.4:
        return "🟡"  # Média
    else:
        return "🔴"  # Baixa


def get_completude_indicator(completude: float) -> str:
    """
    Retorna indicador visual de completude.

    Args:
        completude: Valor de completude (0-1).

    Returns:
        str: Emoji indicador.

    Example:
        >>> get_completude_indicator(0.90)
        '✅'
        >>> get_completude_indicator(0.50)
        '🔄'
        >>> get_completude_indicator(0.20)
        '📝'
    """
    if completude >= 0.8:
        return "✅"  # Completo
    elif completude >= 0.5:
        return "🔄"  # Em progresso
    else:
        return "📝"  # Inicial


def format_metrics_summary(
    solidez: float,
    completude: float,
    concepts_count: int = 0,
    questions_count: int = 0
) -> str:
    """
    Formata resumo das métricas para exibição.

    Usado pelo painel Bastidores na interface web.

    Args:
        solidez: Solidez atual (0-1).
        completude: Completude atual (0-1).
        concepts_count: Número de conceitos catalogados.
        questions_count: Número de questões abertas.

    Returns:
        str: Resumo formatado em múltiplas linhas.

    Example:
        >>> summary = format_metrics_summary(0.65, 0.70, 5, 2)
        >>> print(summary)
        Solidez: 🟡 65%
        Completude: 🔄 70%
        Conceitos: 5
        Questões abertas: 2
    """
    solidez_indicator = get_solidez_indicator(solidez)
    completude_indicator = get_completude_indicator(completude)

    lines = [
        f"Solidez: {solidez_indicator} {solidez:.0%}",
        f"Completude: {completude_indicator} {completude:.0%}",
    ]

    if concepts_count > 0:
        lines.append(f"Conceitos: {concepts_count}")

    if questions_count > 0:
        lines.append(f"Questões abertas: {questions_count}")

    return "\n".join(lines)
