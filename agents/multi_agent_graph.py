"""
Super-grafo multi-agente que integra Orquestrador, Estruturador e Metodologista.

Este módulo implementa o grafo principal do sistema Paper Agent, conectando
múltiplos agentes especializados em uma arquitetura de super-grafo.

Fluxo do sistema (Épico 4 - Loop de Refinamento):
1. Orquestrador: Classifica maturidade do input (vague/semi_formed/complete)
2. Router 1: Decide próximo agente baseado na classificação
   - "vague" → Estruturador → Metodologista
   - "semi_formed" ou "complete" → Metodologista direto
3. Estruturador (se necessário): Organiza ideia vaga em questão estruturada (V1)
4. Metodologista: Valida rigor científico (3 status: approved, needs_refinement, rejected)
5. Router 2: Decide se continua loop ou finaliza
   - "approved" → END
   - "rejected" → END
   - "needs_refinement" + iteration < max → Estruturador (refina para V2/V3)
   - "needs_refinement" + iteration >= max → force_decision → END

Versão: 2.0 (Épico 4 - Loop de Refinamento Colaborativo)
Data: 12/11/2025
"""

import logging
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from agents.orchestrator.state import MultiAgentState, create_initial_multi_agent_state
from agents.orchestrator.nodes import orchestrator_node
from agents.orchestrator.router import route_from_orchestrator
from agents.structurer.nodes import structurer_node
from agents.methodologist.nodes import decide_collaborative, force_decision_collaborative

logger = logging.getLogger(__name__)

# MemorySaver: Checkpointer padrão do LangGraph para persistência de sessão em memória.
# Permite que o estado do grafo seja salvo e recuperado durante a execução,
# essencial para rastreabilidade e continuação entre chamadas.
checkpointer = MemorySaver()


def route_after_methodologist(state: MultiAgentState) -> str:
    """
    Router que decide o fluxo após o Metodologista processar a hipótese (Épico 4).

    Lógica de decisão:
    1. Se status = "approved" → END (finaliza)
    2. Se status = "rejected" → END (finaliza)
    3. Se status = "needs_refinement":
       a. Se iteration < max_refinements → "structurer" (refina)
       b. Se iteration >= max_refinements → "force_decision" (força decisão final)

    Args:
        state (MultiAgentState): Estado do sistema multi-agente.

    Returns:
        str: Nome do próximo nó ("structurer", "force_decision" ou END)

    Example:
        >>> state = {...}
        >>> state['methodologist_output'] = {"status": "needs_refinement", ...}
        >>> state['refinement_iteration'] = 1
        >>> state['max_refinements'] = 2
        >>> route_after_methodologist(state)
        'structurer'  # Ainda pode refinar

        >>> state['refinement_iteration'] = 2
        >>> route_after_methodologist(state)
        'force_decision'  # Limite atingido
    """
    methodologist_output = state.get('methodologist_output')

    if not methodologist_output:
        logger.warning("methodologist_output não encontrado. Finalizando.")
        return END

    status = methodologist_output.get('status')
    iteration = state.get('refinement_iteration', 0)
    max_iter = state.get('max_refinements', 2)

    logger.info(f"=== ROUTER APÓS METODOLOGISTA ===")
    logger.info(f"Status: {status}")
    logger.info(f"Iteração: {iteration}/{max_iter}")

    # Decisão final (approved ou rejected)
    if status in ["approved", "rejected"]:
        logger.info(f"Decisão final: {status}. Finalizando.")
        return END

    # Precisa de refinamento
    if status == "needs_refinement":
        if iteration < max_iter:
            logger.info(f"Precisa refinamento. Voltando para Estruturador (V{iteration + 2}).")
            return "structurer"
        else:
            logger.info(f"Limite de refinamentos atingido ({max_iter}). Forçando decisão final.")
            return "force_decision"

    # Fallback: status desconhecido
    logger.warning(f"Status desconhecido '{status}'. Finalizando por segurança.")
    return END


def create_multi_agent_graph():
    """
    Cria e compila o super-grafo multi-agente do sistema Paper Agent.

    Este grafo implementa o fluxo completo com loop de refinamento colaborativo (Épico 4):

    Fluxo 1 - Ideia vaga + refinamento:
        START → Orquestrador (classifica: "vague")
              → Estruturador (gera V1)
              → Metodologista (valida: "needs_refinement")
              → Estruturador (gera V2 refinada)
              → Metodologista (valida: "approved")
              → END

    Fluxo 2 - Hipótese → Metodologista direto:
        START → Orquestrador (classifica: "semi_formed" ou "complete")
              → Metodologista (valida: "approved" ou "rejected")
              → END

    Fluxo 3 - Limite de refinamentos atingido:
        ...  → Metodologista (valida: "needs_refinement", iteration=2)
             → force_decision (decide "approved" ou "rejected")
             → END

    Estrutura do grafo (Épico 4):
        - Nós:
            * orchestrator: Classifica maturidade do input
            * structurer: Organiza/refina questões (V1, V2, V3)
            * methodologist: Valida rigor (modo colaborativo)
            * force_decision: Decisão forçada após limite

        - Edges:
            * START → orchestrator
            * orchestrator → [router 1] → structurer | methodologist
            * structurer → methodologist
            * methodologist → [router 2] → structurer | force_decision | END
            * force_decision → END

        - Loop: methodologist → structurer (até max_refinements=2)

        - State: MultiAgentState com refinement_iteration, hypothesis_versions

    Returns:
        CompiledGraph: Super-grafo compilado pronto para execução via invoke()

    Example:
        >>> graph = create_multi_agent_graph()
        >>> state = create_initial_multi_agent_state("Método X é rápido")
        >>> result = graph.invoke(state, config={"configurable": {"thread_id": "1"}})
        >>> result['methodologist_output']['status']
        'approved'  # Após 1-2 refinamentos
        >>> len(result['hypothesis_versions'])
        2  # V1 + V2
    """
    logger.info("=== CRIANDO SUPER-GRAFO MULTI-AGENTE COM LOOP DE REFINAMENTO ===")

    # Criar o StateGraph com MultiAgentState
    graph = StateGraph(MultiAgentState)
    logger.info("StateGraph criado com MultiAgentState")

    # Adicionar nós do sistema (Épico 4)
    graph.add_node("orchestrator", orchestrator_node)
    graph.add_node("structurer", structurer_node)
    graph.add_node("methodologist", decide_collaborative)  # Modo colaborativo
    graph.add_node("force_decision", force_decision_collaborative)  # Decisão forçada
    logger.info("Nós adicionados: orchestrator, structurer, methodologist (colaborativo), force_decision")

    # Definir entry point
    graph.set_entry_point("orchestrator")
    logger.info("Entry point: orchestrator")

    # ROUTER 1: Orquestrador → Estruturador | Metodologista
    graph.add_conditional_edges(
        "orchestrator",
        route_from_orchestrator,
        {
            "structurer": "structurer",
            "methodologist": "methodologist"
        }
    )
    logger.info("Edge condicional: orchestrator → [router1] → structurer | methodologist")

    # Estruturador → Metodologista (sempre)
    graph.add_edge("structurer", "methodologist")
    logger.info("Edge fixo: structurer → methodologist")

    # ROUTER 2: Metodologista → Estruturador | force_decision | END (loop de refinamento)
    graph.add_conditional_edges(
        "methodologist",
        route_after_methodologist,
        {
            "structurer": "structurer",  # Loop: refina V2, V3
            "force_decision": "force_decision",  # Limite atingido
            END: END  # approved ou rejected
        }
    )
    logger.info("Edge condicional: methodologist → [router2] → structurer | force_decision | END")

    # force_decision → END (finaliza)
    graph.add_edge("force_decision", END)
    logger.info("Edge fixo: force_decision → END")

    # Compilar o grafo com checkpointer
    compiled_graph = graph.compile(checkpointer=checkpointer)
    logger.info("Super-grafo compilado com MemorySaver checkpointer")

    logger.info("=== SUPER-GRAFO COM LOOP DE REFINAMENTO CRIADO COM SUCESSO ===")
    logger.info("")
    logger.info("Fluxos disponíveis (Épico 4):")
    logger.info("  1. Ideia vaga → Orquestrador → Estruturador (V1) → Metodologista")
    logger.info("     → [se needs_refinement] → Estruturador (V2) → Metodologista → END")
    logger.info("  2. Hipótese → Orquestrador → Metodologista → END")
    logger.info("  3. Loop: até 2 refinamentos (V1 → V2 → V3)")
    logger.info("  4. Limite: force_decision após 2 refinamentos")
    logger.info("")

    return compiled_graph


# Exportar função helper para criar estado inicial
__all__ = ['create_multi_agent_graph', 'create_initial_multi_agent_state']
