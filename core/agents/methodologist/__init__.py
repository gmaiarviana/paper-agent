"""
Agente Metodologista: Avalia rigor científico de hipóteses e constatações.

Este pacote implementa o agente Metodologista usando LangGraph,
responsável por validar hipóteses do ponto de vista metodológico.

Status: Módulo reorganizado e modularizado

API Pública:
    - create_methodologist_graph: Função para criar o grafo compilado
    - MethodologistState: Schema do estado do agente
    - create_initial_state: Função para criar estado inicial
    - checkpointer: MemorySaver para persistência

Exemplo de uso:
    >>> from core.agents.methodologist import create_methodologist_graph, create_initial_state
    >>>
    >>> graph = create_methodologist_graph()
    >>> state = create_initial_state("Café aumenta produtividade")
    >>>
    >>> result = graph.invoke(
    ...     state,
    ...     config={"configurable": {"thread_id": "session-123"}}
    ... )
    >>> print(result['status'])
    'approved'
"""

from .graph import create_methodologist_graph, checkpointer
from .state import MethodologistState, create_initial_state

__all__ = [
    "create_methodologist_graph",
    "MethodologistState",
    "create_initial_state",
    "checkpointer",
]

__version__ = "1.3"
