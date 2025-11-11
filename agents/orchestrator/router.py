"""
Lógica de roteamento do agente Orquestrador.

Este módulo define funções de roteamento que decidem qual agente
executar em seguida com base na classificação do Orquestrador.

Versão: 1.0 (Épico 3, Funcionalidade 3.1)
Data: 11/11/2025
"""

import logging
from typing import Literal

from .state import MultiAgentState

logger = logging.getLogger(__name__)


def route_from_orchestrator(state: MultiAgentState) -> Literal["structurer", "methodologist"]:
    """
    Router que decide o próximo agente após o Orquestrador.

    Lógica de decisão baseada na classificação de maturidade:
    - "vague" → Estruturador (precisa organizar ideia)
    - "semi_formed" → Metodologista (validar hipótese parcial)
    - "complete" → Metodologista (validar hipótese completa)

    Args:
        state (MultiAgentState): Estado atual do sistema multi-agente.

    Returns:
        str: Nome do próximo agente ("structurer" ou "methodologist")

    Raises:
        ValueError: Se classification for None ou inválida

    Example:
        >>> state = create_initial_multi_agent_state("Teste")
        >>> state['orchestrator_classification'] = "vague"
        >>> route_from_orchestrator(state)
        'structurer'

        >>> state['orchestrator_classification'] = "semi_formed"
        >>> route_from_orchestrator(state)
        'methodologist'
    """
    logger.info("=== ROUTER: Decidindo próximo agente após Orquestrador ===")

    classification = state.get('orchestrator_classification')

    logger.info(f"Classificação detectada: {classification}")

    # Validar que classificação existe
    if classification is None:
        error_msg = (
            "Classificação do Orquestrador está None. "
            "O nó orchestrator_node deve ser executado antes do router."
        )
        logger.error(error_msg)
        raise ValueError(error_msg)

    # Validar que classificação é válida
    valid_classifications = ["vague", "semi_formed", "complete"]
    if classification not in valid_classifications:
        error_msg = (
            f"Classificação inválida: '{classification}'. "
            f"Valores válidos: {valid_classifications}"
        )
        logger.error(error_msg)
        raise ValueError(error_msg)

    # Rotear baseado na classificação
    if classification == "vague":
        next_agent = "structurer"
    elif classification in ["semi_formed", "complete"]:
        next_agent = "methodologist"

    logger.info(f"Decisão do router: {next_agent}")
    logger.info("=== ROUTER: Finalizado ===\n")

    return next_agent
