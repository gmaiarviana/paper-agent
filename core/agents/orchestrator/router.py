"""
Lógica de roteamento do agente Orquestrador.

Este módulo define funções de roteamento que decidem qual agente
executar em seguida com base na análise conversacional do Orquestrador.

"""

import logging
from typing import Literal, Union

from .state import MultiAgentState

logger = logging.getLogger(__name__)

def route_from_orchestrator(state: MultiAgentState) -> Union[Literal["structurer", "methodologist", "user"], str]:
    """
    Router que decide o próximo passo após o Orquestrador Conversacional.

    MUDANÇA ARQUITETURAL (Épico 7):
    - ANTES: Baseado em classificação (vague/semi_formed/complete)
    - DEPOIS: Baseado em next_step e agent_suggestion do orquestrador conversacional

    Lógica de decisão:
    - next_step = "explore" → Retorna para usuário (mais perguntas necessárias)
    - next_step = "clarify" → Retorna para usuário (esclarecer ambiguidade)
    - next_step = "suggest_agent" + agent_suggestion:
      - "structurer" → Estruturador
      - "methodologist" → Metodologista
      - "researcher" → Pesquisador (futuro)
      - "writer" → Escritor (futuro)

    Args:
        state (MultiAgentState): Estado atual do sistema multi-agente.

    Returns:
        str: Nome do próximo agente ("structurer", "methodologist", "user", etc)

    Raises:
        ValueError: Se next_step for None ou agent_suggestion inválida

    Example (POC - Épico 7):
        >>> state = create_initial_multi_agent_state("Observei X", "session-1")
        >>> state['next_step'] = "explore"
        >>> route_from_orchestrator(state)
        'user'

        >>> state['next_step'] = "suggest_agent"
        >>> state['agent_suggestion'] = {"agent": "structurer", "justification": "..."}
        >>> route_from_orchestrator(state)
        'structurer'
    """
    logger.info("=== ROUTER CONVERSACIONAL: Decidindo próximo passo após Orquestrador ===")

    next_step = state.get('next_step')
    agent_suggestion = state.get('agent_suggestion')

    logger.info(f"Next step detectado: {next_step}")
    logger.info(f"Agent suggestion: {agent_suggestion}")

    # Validar que next_step existe
    if next_step is None:
        error_msg = (
            "next_step do Orquestrador está None. "
            "O nó orchestrator_node conversacional deve ser executado antes do router."
        )
        logger.error(error_msg)
        raise ValueError(error_msg)

    # Validar que next_step é válido
    valid_next_steps = ["explore", "suggest_agent", "clarify"]
    if next_step not in valid_next_steps:
        error_msg = (
            f"next_step inválido: '{next_step}'. "
            f"Valores válidos: {valid_next_steps}"
        )
        logger.error(error_msg)
        raise ValueError(error_msg)

    # Decisão de roteamento
    if next_step in ["explore", "clarify"]:
        # Orquestrador quer mais conversa com usuário
        next_destination = "user"
        logger.info("Orquestrador precisa de mais contexto. Retornando para usuário.")

    elif next_step == "suggest_agent":
        # Orquestrador sugere agente específico
        if not agent_suggestion or not isinstance(agent_suggestion, dict):
            logger.warning(
                "next_step='suggest_agent' mas agent_suggestion inválida. "
                "Retornando para usuário por segurança."
            )
            next_destination = "user"
        else:
            suggested_agent = agent_suggestion.get("agent")
            justification = agent_suggestion.get("justification", "N/A")

            # Validar agente sugerido
            valid_agents = ["structurer", "methodologist", "researcher", "writer"]
            if suggested_agent not in valid_agents:
                logger.warning(
                    f"Agente sugerido '{suggested_agent}' não reconhecido. "
                    f"Valores válidos: {valid_agents}. Retornando para usuário."
                )
                next_destination = "user"
            else:
                next_destination = suggested_agent
                logger.info(f"Agente sugerido: {suggested_agent}")
                logger.info(f"Justificativa: {justification}")

    logger.info(f"Decisão do router: {next_destination}")
    logger.info("=== ROUTER CONVERSACIONAL: Finalizado ===\n")

    return next_destination
