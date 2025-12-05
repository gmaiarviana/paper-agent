"""
Calculo de metricas do Observador.

Este modulo contem funcoes para calcular metricas de qualidade
do argumento em construcao:
- Solidez: quao bem fundamentado esta o argumento
- Completude: quanto do argumento esta desenvolvido

Versao: 1.0 (Epico 10.2)
Data: 05/12/2025
"""

import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


def calculate_solidez(
    claim: str,
    fundamentos: List[str],
    assumptions: List[str],
    contradictions: List[Dict[str, Any]],
    solid_grounds: Optional[List[Dict[str, Any]]] = None
) -> float:
    """
    Calcula solidez do argumento (0-1).

    Solidez mede quao bem fundamentado esta o argumento.
    Baseado em:
    - Especificidade do claim (+)
    - Quantidade de fundamentos (+)
    - Quantidade de assumptions (-)
    - Presenca de contradicoes (--)
    - Evidencias bibliograficas (bonus)

    Args:
        claim: Afirmacao central do argumento.
        fundamentos: Lista de argumentos de suporte.
        assumptions: Lista de suposicoes nao verificadas.
        contradictions: Lista de contradicoes detectadas.
        solid_grounds: Lista de evidencias (opcional).

    Returns:
        float: Solidez entre 0.0 e 1.0.

    Example:
        >>> solidez = calculate_solidez(
        ...     claim="LLMs aumentam produtividade em 30%",
        ...     fundamentos=["Equipes usam LLMs", "Tempo e mensuravel"],
        ...     assumptions=["Qualidade nao e afetada"],
        ...     contradictions=[]
        ... )
        >>> print(f"Solidez: {solidez:.0%}")
        Solidez: 65%
    """
    score = 0.0

    # 1. Claim definido: base 20%
    if claim:
        score += 0.20

        # Bonus para claim especifico (> 50 chars)
        if len(claim) > 50:
            score += 0.05

    # 2. Fundamentos: cada um adiciona ate 15% (max 45%)
    fundamentos_score = min(0.45, len(fundamentos) * 0.15)
    score += fundamentos_score

    # 3. Assumptions: cada uma subtrai 5% (max -20%)
    assumptions_penalty = min(0.20, len(assumptions) * 0.05)
    score -= assumptions_penalty

    # 4. Contradicoes: cada uma subtrai 10% (max -30%)
    contradictions_penalty = min(0.30, len(contradictions) * 0.10)
    score -= contradictions_penalty

    # 5. Bonus: evidencias bibliograficas (se existirem)
    if solid_grounds:
        evidence_bonus = min(0.15, len(solid_grounds) * 0.05)
        score += evidence_bonus

    # Garantir range 0-1
    solidez = max(0.0, min(1.0, score))

    logger.debug(
        f"Solidez calculada: {solidez:.2f} "
        f"(claim={bool(claim)}, fundamentos={len(fundamentos)}, "
        f"assumptions={len(assumptions)}, contradictions={len(contradictions)})"
    )

    return solidez


def calculate_completude(
    claims: List[str],
    fundamentos: List[str],
    open_questions: List[str],
    context: Optional[Dict[str, Any]] = None
) -> float:
    """
    Calcula completude do argumento (0-1).

    Completude mede quanto do argumento esta desenvolvido.
    Baseado em:
    - Presenca de claims (+)
    - Presenca de fundamentos (+)
    - Quantidade de open questions (-)
    - Contexto definido (+)

    Args:
        claims: Lista de claims extraidos.
        fundamentos: Lista de fundamentos.
        open_questions: Lista de questoes abertas.
        context: Contexto do argumento (opcional).

    Returns:
        float: Completude entre 0.0 e 1.0.

    Example:
        >>> completude = calculate_completude(
        ...     claims=["LLMs aumentam produtividade"],
        ...     fundamentos=["Equipes usam LLMs"],
        ...     open_questions=["Como medir?", "Qual baseline?"]
        ... )
        >>> print(f"Completude: {completude:.0%}")
        Completude: 40%
    """
    score = 0.0

    # 1. Claims definidos: ate 25%
    if claims:
        claims_score = min(0.25, len(claims) * 0.10)
        score += claims_score

    # 2. Fundamentos: ate 35%
    if fundamentos:
        fundamentos_score = min(0.35, len(fundamentos) * 0.12)
        score += fundamentos_score

    # 3. Open questions: subtraem da completude (max -30%)
    if open_questions:
        questions_penalty = min(0.30, len(open_questions) * 0.10)
        score -= questions_penalty

    # 4. Contexto definido: bonus ate 20%
    if context:
        # Cada campo do contexto adiciona pontos
        context_fields = ['domain', 'population', 'technology', 'metrics', 'article_type']
        defined_fields = sum(1 for f in context_fields if context.get(f))
        context_bonus = min(0.20, defined_fields * 0.04)
        score += context_bonus

    # Base minima se tiver pelo menos claim
    if claims and score < 0.10:
        score = 0.10

    # Garantir range 0-1
    completude = max(0.0, min(1.0, score))

    logger.debug(
        f"Completude calculada: {completude:.2f} "
        f"(claims={len(claims)}, fundamentos={len(fundamentos)}, "
        f"open_questions={len(open_questions)})"
    )

    return completude


def calculate_metrics(
    claim: str,
    claims: List[str],
    fundamentos: List[str],
    assumptions: List[str],
    open_questions: List[str],
    contradictions: List[Dict[str, Any]],
    context: Optional[Dict[str, Any]] = None,
    solid_grounds: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, float]:
    """
    Calcula todas as metricas do CognitiveModel.

    Funcao de conveniencia que calcula solidez e completude
    em uma unica chamada.

    Args:
        claim: Afirmacao central.
        claims: Lista de claims extraidos.
        fundamentos: Lista de fundamentos.
        assumptions: Lista de suposicoes.
        open_questions: Lista de questoes abertas.
        contradictions: Lista de contradicoes.
        context: Contexto do argumento.
        solid_grounds: Evidencias bibliograficas.

    Returns:
        Dict com 'solidez' e 'completude' (ambos 0-1).

    Example:
        >>> metrics = calculate_metrics(
        ...     claim="LLMs aumentam produtividade",
        ...     claims=["LLMs aumentam produtividade"],
        ...     fundamentos=["Equipes usam LLMs"],
        ...     assumptions=["Qualidade nao afetada"],
        ...     open_questions=["Como medir?"],
        ...     contradictions=[]
        ... )
        >>> print(metrics)
        {'solidez': 0.35, 'completude': 0.25}
    """
    solidez = calculate_solidez(
        claim=claim,
        fundamentos=fundamentos,
        assumptions=assumptions,
        contradictions=contradictions,
        solid_grounds=solid_grounds
    )

    completude = calculate_completude(
        claims=claims,
        fundamentos=fundamentos,
        open_questions=open_questions,
        context=context
    )

    return {
        "solidez": solidez,
        "completude": completude
    }


def evaluate_maturity(
    solidez: float,
    completude: float,
    open_questions: List[str],
    contradictions: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Avalia maturidade do argumento para potencial snapshot.

    Determina se o argumento esta maduro o suficiente para
    criar um snapshot (persisti-lo).

    Args:
        solidez: Solidez calculada (0-1).
        completude: Completude calculada (0-1).
        open_questions: Lista de questoes abertas.
        contradictions: Lista de contradicoes.

    Returns:
        Dict com:
        - is_mature: bool indicando se esta maduro
        - confidence: float indicando confianca (0-1)
        - reason: str explicando a avaliacao

    Example:
        >>> result = evaluate_maturity(
        ...     solidez=0.75,
        ...     completude=0.80,
        ...     open_questions=[],
        ...     contradictions=[]
        ... )
        >>> print(result)
        {'is_mature': True, 'confidence': 0.85, 'reason': 'Argumento bem fundamentado'}
    """
    # Criterios de maturidade
    has_high_solidez = solidez >= 0.60
    has_high_completude = completude >= 0.50
    has_few_questions = len(open_questions) <= 1
    has_no_contradictions = len(contradictions) == 0

    # Calcular confianca
    confidence = (solidez + completude) / 2

    # Avaliar maturidade
    if has_high_solidez and has_high_completude and has_few_questions and has_no_contradictions:
        return {
            "is_mature": True,
            "confidence": confidence,
            "reason": "Argumento bem fundamentado com poucas lacunas"
        }
    elif has_high_solidez and has_high_completude:
        return {
            "is_mature": True,
            "confidence": confidence * 0.9,
            "reason": "Argumento solido, mas com algumas questoes abertas"
        }
    elif solidez >= 0.40 and completude >= 0.40:
        return {
            "is_mature": False,
            "confidence": confidence,
            "reason": "Argumento em desenvolvimento, precisa mais fundamentos"
        }
    else:
        return {
            "is_mature": False,
            "confidence": confidence,
            "reason": "Argumento inicial, precisa ser mais desenvolvido"
        }
