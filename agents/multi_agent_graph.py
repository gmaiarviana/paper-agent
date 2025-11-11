"""
Super-grafo multi-agente que integra Orquestrador, Estruturador e Metodologista.

Este módulo implementa o grafo principal do sistema Paper Agent, conectando
múltiplos agentes especializados em uma arquitetura de super-grafo.

Fluxo do sistema:
1. Orquestrador: Classifica maturidade do input (vague/semi_formed/complete)
2. Router: Decide próximo agente baseado na classificação
   - "vague" → Estruturador → Metodologista
   - "semi_formed" ou "complete" → Metodologista direto
3. Estruturador (se necessário): Organiza ideia vaga em questão estruturada
4. Metodologista: Valida rigor científico e retorna decisão final

Versão: 1.0 (Épico 3, Funcionalidade 3.3)
Data: 11/11/2025
"""

import logging
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from agents.orchestrator.state import MultiAgentState, create_initial_multi_agent_state
from agents.orchestrator.nodes import orchestrator_node
from agents.orchestrator.router import route_from_orchestrator
from agents.structurer.nodes import structurer_node
from agents.methodologist.wrapper import methodologist_wrapper_node

logger = logging.getLogger(__name__)

# MemorySaver: Checkpointer padrão do LangGraph para persistência de sessão em memória.
# Permite que o estado do grafo seja salvo e recuperado durante a execução,
# essencial para rastreabilidade e continuação entre chamadas.
checkpointer = MemorySaver()


def create_multi_agent_graph():
    """
    Cria e compila o super-grafo multi-agente do sistema Paper Agent.

    Este grafo implementa o fluxo completo de processamento de ideias/hipóteses:

    Fluxo 1 - Ideia vaga:
        START → Orquestrador (classifica: "vague")
              → Estruturador (organiza em questão)
              → Metodologista (valida rigor)
              → END

    Fluxo 2 - Hipótese semi-formada ou completa:
        START → Orquestrador (classifica: "semi_formed" ou "complete")
              → Metodologista (valida rigor)
              → END

    Estrutura do grafo:
        - Nós:
            * orchestrator: Classifica maturidade do input
            * structurer: Organiza ideias vagas (nó simples)
            * methodologist: Valida rigor científico (wrapper para grafo interno)

        - Edges:
            * START → orchestrator (entry point)
            * orchestrator → [conditional router] → structurer OU methodologist
            * structurer → methodologist (edge fixo)
            * methodologist → END (finaliza processamento)

        - State: MultiAgentState (híbrido: compartilhado + específico por agente)

        - Checkpointer: MemorySaver (persistência em memória)

    Returns:
        CompiledGraph: Super-grafo compilado pronto para execução via invoke()

    Example:
        >>> # Criar grafo
        >>> graph = create_multi_agent_graph()
        >>>
        >>> # Executar com ideia vaga
        >>> state = create_initial_multi_agent_state(
        ...     "Observei que desenvolver com Claude Code é mais rápido"
        ... )
        >>> result = graph.invoke(
        ...     state,
        ...     config={"configurable": {"thread_id": "session-1"}}
        ... )
        >>>
        >>> # Verificar resultado
        >>> result['orchestrator_classification']
        'vague'
        >>> result['structurer_output']['structured_question']
        'Em que condições o desenvolvimento com Claude Code demonstra maior velocidade?'
        >>> result['methodologist_output']['status']
        'rejected'  # Provavelmente falta especificidade
        >>> result['current_stage']
        'done'
    """
    logger.info("=== CRIANDO SUPER-GRAFO MULTI-AGENTE ===")

    # Criar o StateGraph com MultiAgentState
    graph = StateGraph(MultiAgentState)
    logger.info("StateGraph criado com MultiAgentState")

    # Adicionar nós do sistema
    graph.add_node("orchestrator", orchestrator_node)
    graph.add_node("structurer", structurer_node)
    graph.add_node("methodologist", methodologist_wrapper_node)
    logger.info("Nós adicionados: orchestrator, structurer, methodologist")

    # Definir entry point (ponto de entrada do grafo)
    graph.set_entry_point("orchestrator")
    logger.info("Entry point definido: orchestrator")

    # Adicionar edges condicionais do Orquestrador
    # O router decide se vai para Estruturador ou Metodologista
    graph.add_conditional_edges(
        "orchestrator",
        route_from_orchestrator,
        {
            "structurer": "structurer",
            "methodologist": "methodologist"
        }
    )
    logger.info("Edge condicional: orchestrator → [router] → structurer | methodologist")

    # Estruturador sempre vai para Metodologista após processar
    graph.add_edge("structurer", "methodologist")
    logger.info("Edge fixo: structurer → methodologist")

    # Metodologista finaliza o fluxo
    graph.add_edge("methodologist", END)
    logger.info("Edge fixo: methodologist → END")

    # Compilar o grafo com checkpointer
    compiled_graph = graph.compile(checkpointer=checkpointer)
    logger.info("Super-grafo compilado com MemorySaver checkpointer")

    logger.info("=== SUPER-GRAFO CRIADO COM SUCESSO ===")
    logger.info("")
    logger.info("Fluxos disponíveis:")
    logger.info("  1. Ideia vaga → Orquestrador → Estruturador → Metodologista → END")
    logger.info("  2. Hipótese → Orquestrador → Metodologista → END")
    logger.info("")

    return compiled_graph


# Exportar função helper para criar estado inicial
__all__ = ['create_multi_agent_graph', 'create_initial_multi_agent_state']
