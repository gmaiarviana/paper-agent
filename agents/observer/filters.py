"""
Filtros de regras de negocio para o Observer.

Este modulo implementa a arquitetura de duas camadas:
- Camada 1: Observer (analise contextual via LLM)
- Camada 2: Filtros (regras de negocio deterministicas)

Filosofia:
- Observer DETECTA (qualitativo, contextual, LLM)
- Filtros MODULAM (quantitativo, deterministico, codigo)
- Orquestrador DECIDE (baseado em ambos)

A separacao permite:
- Manter analise rica e contextual do Observer
- Adicionar previsibilidade onde necessario
- Testar ambas as camadas independentemente
- Evoluir regras sem mudar prompts do LLM

Epico 13.6: Arquitetura de Duas Camadas
Data: 2025-12-10
"""

import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


class FilterType(Enum):
    """Tipos de filtros aplicados."""
    COLD_START = "cold_start_exemption"
    HIGH_CLARITY = "high_clarity_exemption"
    VARIATION_ONLY = "variation_exemption"
    COOLDOWN = "cooldown_exemption"
    NONE = "no_filter_applied"


@dataclass
class FilterResult:
    """Resultado da aplicacao de filtros."""
    needs_checkpoint: bool
    filter_applied: FilterType
    original_needs_checkpoint: bool
    reason: str
    observer_analysis: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionario."""
        return {
            "needs_checkpoint": self.needs_checkpoint,
            "filter_applied": self.filter_applied.value,
            "original_needs_checkpoint": self.original_needs_checkpoint,
            "reason": self.reason,
            "was_filtered": self.needs_checkpoint != self.original_needs_checkpoint
        }


# =============================================================================
# CONFIGURACAO DE FILTROS
# =============================================================================

# Turno minimo para permitir checkpoint (cold start)
MIN_TURN_FOR_CHECKPOINT = 2

# Score minimo de clareza para isentar de checkpoint
MIN_CLARITY_SCORE_FOR_EXEMPTION = 4

# Turnos minimos entre checkpoints (cooldown)
MIN_TURNS_BETWEEN_CHECKPOINTS = 3


# =============================================================================
# FUNCAO PRINCIPAL
# =============================================================================

def apply_business_rules(
    observer_result: Dict[str, Any],
    turn_number: int,
    turns_since_last_checkpoint: int = 999,
    conversation_context: Optional[Dict[str, Any]] = None
) -> FilterResult:
    """
    Aplica regras de negocio sobre analise contextual do Observer.

    Esta funcao implementa a segunda camada da arquitetura:
    - Observer ja analisou (camada 1)
    - Filtros modulam a decisao (camada 2)

    Regras aplicadas (em ordem de prioridade):
    1. Cold start: turno 1 nunca e checkpoint
    2. Alta clareza: clarity_score >= 4 nao e checkpoint
    3. Variacao simples: classification="variation" nao e checkpoint
    4. Cooldown: respeitar intervalo minimo entre checkpoints

    Args:
        observer_result: Resultado da analise do Observer contendo:
            - needs_checkpoint: bool
            - clarity_score: int (1-5)
            - clarity_level: str
            - classification: str (variation/real_change)
        turn_number: Numero do turno atual (1-indexed).
        turns_since_last_checkpoint: Turnos desde ultimo checkpoint.
        conversation_context: Contexto adicional (opcional).

    Returns:
        FilterResult: Resultado com decisao final e metadados.

    Example:
        >>> observer = {"needs_checkpoint": True, "clarity_score": 2}
        >>> result = apply_business_rules(observer, turn_number=1)
        >>> print(result.needs_checkpoint)
        False  # Cold start exemption
        >>> print(result.filter_applied)
        FilterType.COLD_START
    """
    original_needs_checkpoint = observer_result.get("needs_checkpoint", False)

    # Se Observer nao pediu checkpoint, nao precisa filtrar
    if not original_needs_checkpoint:
        return FilterResult(
            needs_checkpoint=False,
            filter_applied=FilterType.NONE,
            original_needs_checkpoint=False,
            reason="Observer nao solicitou checkpoint",
            observer_analysis=observer_result
        )

    # Regra 1: Cold start (turno 1 ou 2) - nunca checkpoint
    if turn_number < MIN_TURN_FOR_CHECKPOINT:
        logger.info(
            f"Filtro COLD_START aplicado: turno {turn_number} < {MIN_TURN_FOR_CHECKPOINT}"
        )
        return FilterResult(
            needs_checkpoint=False,
            filter_applied=FilterType.COLD_START,
            original_needs_checkpoint=True,
            reason=f"Turno {turn_number} esta em cold start (< {MIN_TURN_FOR_CHECKPOINT})",
            observer_analysis=observer_result
        )

    # Regra 2: Alta clareza - nao interromper
    clarity_score = observer_result.get("clarity_score", 0)
    if clarity_score >= MIN_CLARITY_SCORE_FOR_EXEMPTION:
        logger.info(
            f"Filtro HIGH_CLARITY aplicado: score {clarity_score} >= {MIN_CLARITY_SCORE_FOR_EXEMPTION}"
        )
        return FilterResult(
            needs_checkpoint=False,
            filter_applied=FilterType.HIGH_CLARITY,
            original_needs_checkpoint=True,
            reason=f"Clareza alta (score {clarity_score} >= {MIN_CLARITY_SCORE_FOR_EXEMPTION})",
            observer_analysis=observer_result
        )

    # Regra 3: Variacao simples - nao interromper
    classification = observer_result.get("classification", "")
    if classification == "variation":
        logger.info("Filtro VARIATION_ONLY aplicado: classificacao e 'variation'")
        return FilterResult(
            needs_checkpoint=False,
            filter_applied=FilterType.VARIATION_ONLY,
            original_needs_checkpoint=True,
            reason="Detectada variacao simples, nao mudanca real",
            observer_analysis=observer_result
        )

    # Regra 4: Cooldown entre checkpoints
    if turns_since_last_checkpoint < MIN_TURNS_BETWEEN_CHECKPOINTS:
        logger.info(
            f"Filtro COOLDOWN aplicado: {turns_since_last_checkpoint} turnos "
            f"< {MIN_TURNS_BETWEEN_CHECKPOINTS} minimo"
        )
        return FilterResult(
            needs_checkpoint=False,
            filter_applied=FilterType.COOLDOWN,
            original_needs_checkpoint=True,
            reason=f"Cooldown ativo ({turns_since_last_checkpoint} < {MIN_TURNS_BETWEEN_CHECKPOINTS} turnos)",
            observer_analysis=observer_result
        )

    # Nenhum filtro aplicado - manter decisao do Observer
    logger.info("Nenhum filtro aplicado - mantendo decisao do Observer")
    return FilterResult(
        needs_checkpoint=True,
        filter_applied=FilterType.NONE,
        original_needs_checkpoint=True,
        reason="Checkpoint necessario conforme analise do Observer",
        observer_analysis=observer_result
    )


def should_checkpoint(
    clarity_evaluation: Optional[Dict[str, Any]],
    variation_analysis: Optional[Dict[str, Any]],
    turn_number: int,
    turns_since_last_checkpoint: int = 999
) -> FilterResult:
    """
    Funcao de conveniencia que combina clarity e variation em uma decisao.

    Esta funcao e o ponto de entrada principal para o Orquestrador.
    Ela combina as analises de clareza e variacao do Observer e aplica
    os filtros de negocio para produzir uma decisao final.

    Args:
        clarity_evaluation: Resultado de evaluate_conversation_clarity().
        variation_analysis: Resultado de detect_variation().
        turn_number: Numero do turno atual.
        turns_since_last_checkpoint: Turnos desde ultimo checkpoint.

    Returns:
        FilterResult: Decisao final com metadados.

    Example:
        >>> clarity = {"needs_checkpoint": True, "clarity_score": 2}
        >>> variation = {"classification": "variation"}
        >>> result = should_checkpoint(clarity, variation, turn_number=3)
        >>> print(result.needs_checkpoint)
        False  # variation_exemption applied
    """
    # Combinar resultados do Observer
    combined = {}

    if clarity_evaluation:
        combined["needs_checkpoint"] = clarity_evaluation.get("needs_checkpoint", False)
        combined["clarity_score"] = clarity_evaluation.get("clarity_score", 3)
        combined["clarity_level"] = clarity_evaluation.get("clarity_level", "nebulosa")

    if variation_analysis:
        combined["classification"] = variation_analysis.get("classification", "")
        # Se variacao detectou mudanca real, pode precisar checkpoint
        if variation_analysis.get("classification") == "real_change":
            combined["needs_checkpoint"] = True

    # Aplicar filtros
    return apply_business_rules(
        observer_result=combined,
        turn_number=turn_number,
        turns_since_last_checkpoint=turns_since_last_checkpoint
    )


# =============================================================================
# FUNCOES DE CONFIGURACAO
# =============================================================================

def get_filter_config() -> Dict[str, Any]:
    """Retorna configuracao atual dos filtros."""
    return {
        "min_turn_for_checkpoint": MIN_TURN_FOR_CHECKPOINT,
        "min_clarity_score_for_exemption": MIN_CLARITY_SCORE_FOR_EXEMPTION,
        "min_turns_between_checkpoints": MIN_TURNS_BETWEEN_CHECKPOINTS
    }


def update_filter_config(
    min_turn: Optional[int] = None,
    min_clarity: Optional[int] = None,
    min_cooldown: Optional[int] = None
) -> Dict[str, Any]:
    """
    Atualiza configuracao dos filtros em runtime.

    Util para testes ou ajustes dinamicos.

    Args:
        min_turn: Novo valor para MIN_TURN_FOR_CHECKPOINT.
        min_clarity: Novo valor para MIN_CLARITY_SCORE_FOR_EXEMPTION.
        min_cooldown: Novo valor para MIN_TURNS_BETWEEN_CHECKPOINTS.

    Returns:
        Dict com configuracao atualizada.
    """
    global MIN_TURN_FOR_CHECKPOINT, MIN_CLARITY_SCORE_FOR_EXEMPTION, MIN_TURNS_BETWEEN_CHECKPOINTS

    if min_turn is not None:
        MIN_TURN_FOR_CHECKPOINT = min_turn
    if min_clarity is not None:
        MIN_CLARITY_SCORE_FOR_EXEMPTION = min_clarity
    if min_cooldown is not None:
        MIN_TURNS_BETWEEN_CHECKPOINTS = min_cooldown

    return get_filter_config()
