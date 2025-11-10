"""
Construção e configuração do grafo LangGraph do agente Metodologista.

Este módulo cria o StateGraph completo, conectando todos os nós
e configurando o fluxo de execução com checkpointer para persistência.

Versão: 1.3
Data: 10/11/2025
"""

import logging
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from .state import MethodologistState
from .nodes import analyze, ask_clarification, decide
from .router import route_after_analyze

logger = logging.getLogger(__name__)

# MemorySaver: Checkpointer padrão do LangGraph para persistência de sessão em memória.
# Permite que o estado do grafo seja salvo e recuperado durante a execução,
# essencial para handling de interrupções (interrupt) e continuação da conversa.
checkpointer = MemorySaver()


def create_methodologist_graph():
    """
    Cria e compila o grafo do agente Metodologista.

    Este grafo implementa o fluxo completo de análise de hipóteses:
    1. START → analyze: Avalia a hipótese e decide se precisa de mais informações
    2. analyze → router → ask_clarification ou decide
    3. ask_clarification → analyze (loop até max_iterations)
    4. decide → END: Decisão final

    Returns:
        CompiledGraph: Grafo compilado pronto para execução via invoke()

    Example:
        >>> graph = create_methodologist_graph()
        >>> result = graph.invoke(
        ...     {"hypothesis": "Café aumenta produtividade"},
        ...     config={"configurable": {"thread_id": "test-1"}}
        ... )
        >>> result['status'] in ['approved', 'rejected']
        True
    """
    logger.info("=== CRIANDO GRAFO DO METODOLOGISTA ===")

    # Criar o StateGraph
    graph = StateGraph(MethodologistState)

    # Adicionar nós
    graph.add_node("analyze", analyze)
    graph.add_node("ask_clarification", ask_clarification)
    graph.add_node("decide", decide)

    logger.info("Nós adicionados: analyze, ask_clarification, decide")

    # Definir entrada do grafo
    graph.set_entry_point("analyze")

    # Adicionar edges condicionais
    graph.add_conditional_edges(
        "analyze",
        route_after_analyze,
        {
            "ask_clarification": "ask_clarification",
            "decide": "decide"
        }
    )

    # Edge de ask_clarification volta para analyze (loop)
    graph.add_edge("ask_clarification", "analyze")

    # Edge de decide para END (finaliza o grafo)
    graph.add_edge("decide", END)

    logger.info("Edges configurados:")
    logger.info("  - START → analyze")
    logger.info("  - analyze → [router] → ask_clarification | decide")
    logger.info("  - ask_clarification → analyze")
    logger.info("  - decide → END")

    # Compilar o grafo com checkpointer
    compiled_graph = graph.compile(checkpointer=checkpointer)

    logger.info("Grafo compilado com MemorySaver checkpointer")
    logger.info("=== GRAFO CRIADO COM SUCESSO ===\n")

    return compiled_graph
