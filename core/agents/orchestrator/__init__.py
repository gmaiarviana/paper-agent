"""
Módulo do agente Orquestrador.

Este módulo contém o agente responsável por:
- Classificar maturidade de inputs do usuário
- Rotear para agentes especializados (Estruturador ou Metodologista)
- Coordenar fluxo do super-grafo multi-agente

Componentes:
    - state: MultiAgentState (TypedDict) compartilhado entre agentes
    - nodes: orchestrator_node (nó de classificação)
    - router: route_from_orchestrator (lógica de roteamento)
    - graph: (Épico 3.3 - construção do super-grafo)

"""

from .state import MultiAgentState, create_initial_multi_agent_state
from .nodes import orchestrator_node
from .router import route_from_orchestrator

__all__ = [
    "MultiAgentState",
    "create_initial_multi_agent_state",
    "orchestrator_node",
    "route_from_orchestrator",
]
