"""
Lógica de roteamento do grafo do agente Metodologista.

Este módulo define funções de roteamento que decidem qual nó
executar em seguida com base no estado atual do grafo.

Versão: 1.3
Data: 10/11/2025
"""

import logging
from typing import Literal

from .state import MethodologistState

logger = logging.getLogger(__name__)


def route_after_analyze(state: MethodologistState) -> Literal["ask_clarification", "decide"]:
    """
    Router que decide o próximo nó após o nó analyze.

    Lógica de decisão:
    - Se needs_clarification é True E iterations < max_iterations → ask_clarification
    - Caso contrário → decide (tempo de decidir com o contexto disponível)

    Args:
        state (MethodologistState): Estado atual do grafo.

    Returns:
        str: Nome do próximo nó ("ask_clarification" ou "decide")

    Example:
        >>> state = create_initial_state("Café aumenta produtividade")
        >>> state['needs_clarification'] = True
        >>> state['iterations'] = 1
        >>> state['max_iterations'] = 3
        >>> route_after_analyze(state)
        'ask_clarification'
    """
    logger.info("=== ROUTER: Decidindo próximo nó após analyze ===")
    logger.info(f"needs_clarification: {state['needs_clarification']}")
    logger.info(f"iterations: {state['iterations']}/{state['max_iterations']}")

    # Se precisa de clarificação E ainda não atingiu o limite
    if state['needs_clarification'] and state['iterations'] < state['max_iterations']:
        next_node = "ask_clarification"
    else:
        next_node = "decide"

    logger.info(f"Decisão do router: {next_node}")
    logger.info("=== ROUTER: Finalizado ===\n")

    return next_node
