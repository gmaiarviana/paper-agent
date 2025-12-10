"""
Wrapper/adapter para integrar o Metodologista no super-grafo multi-agente.

Este módulo cria uma camada de integração entre o MultiAgentState (usado pelo
super-grafo) e o MethodologistState (usado pelo grafo interno do Metodologista).

O wrapper é responsável por:
1. Extrair o input correto do MultiAgentState (structurer_output ou user_input)
2. Converter para MethodologistState
3. Executar o grafo do Metodologista
4. Converter o resultado de volta para MultiAgentState

"""

import logging
from langchain_core.messages import AIMessage

from core.agents.orchestrator.state import MultiAgentState
from core.agents.methodologist.state import create_initial_state
from core.agents.methodologist.graph import create_methodologist_graph

logger = logging.getLogger(__name__)

def methodologist_wrapper_node(state: MultiAgentState) -> dict:
    """
    Nó wrapper que integra o Metodologista no super-grafo multi-agente.

    Este nó é responsável por:
    1. Determinar o input correto para o Metodologista:
       - Se structurer_output existe → usa structured_question
       - Senão → usa user_input direto
    2. Criar MethodologistState com o input correto
    3. Executar o grafo do Metodologista
    4. Extrair resultado e converter para formato MultiAgentState

    Args:
        state (MultiAgentState): Estado atual do super-grafo multi-agente.

    Returns:
        dict: Dicionário com updates incrementais do MultiAgentState:
            - methodologist_output: Resultado da análise do Metodologista
                {
                    "status": "approved" | "rejected",
                    "justification": str,
                    "clarifications": dict  # Perguntas/respostas coletadas
                }
            - current_stage: "done" (processamento concluído)
            - messages: Mensagens do LLM adicionadas ao histórico

    Example:
        >>> # Cenário 1: Após Estruturador
        >>> state = {
        ...     "user_input": "Observei que X é rápido",
        ...     "structurer_output": {
        ...         "structured_question": "Em que condições X é mais rápido?",
        ...         "elements": {...}
        ...     }
        ... }
        >>> result = methodologist_wrapper_node(state)
        >>> result['methodologist_output']['status'] in ['approved', 'rejected']
        True

        >>> # Cenário 2: Direto do Orquestrador
        >>> state = {
        ...     "user_input": "Método Y reduz tempo em 30%",
        ...     "structurer_output": None
        ... }
        >>> result = methodologist_wrapper_node(state)
        >>> result['methodologist_output']['status'] in ['approved', 'rejected']
        True
    """
    logger.info("=== WRAPPER METHODOLOGIST: Iniciando integração ===")

    # 1. Determinar input correto
    if state.get('structurer_output'):
        # Caso 1: Veio do Estruturador, usar questão estruturada
        hypothesis_input = state['structurer_output']['structured_question']
        logger.info(f"Input via Estruturador: {hypothesis_input}")
        logger.info(f"Elementos estruturados: {state['structurer_output']['elements']}")
    else:
        # Caso 2: Veio direto do Orquestrador, usar input do usuário
        hypothesis_input = state['user_input']
        logger.info(f"Input direto do usuário: {hypothesis_input}")

    # 2. Criar MethodologistState inicial
    logger.info("Criando MethodologistState para execução do grafo...")
    methodologist_state = create_initial_state(
        hypothesis=hypothesis_input,
        max_iterations=3  # Limite padrão de perguntas
    )

    # 3. Executar grafo do Metodologista
    logger.info("Executando grafo do Metodologista...")
    methodologist_graph = create_methodologist_graph()

    # Criar thread_id único baseado no user_input (para persistência de sessão)
    thread_id = f"multi_agent_{hash(state['user_input'])}"

    try:
        result = methodologist_graph.invoke(
            methodologist_state,
            config={"configurable": {"thread_id": thread_id}}
        )
        logger.info(f"Grafo do Metodologista executado com sucesso")
        logger.debug(f"Resultado completo: {result}")
    except Exception as e:
        logger.error(f"Erro ao executar grafo do Metodologista: {e}")
        # Em caso de erro, retornar resultado de rejeição por segurança
        result = {
            "status": "rejected",
            "justification": f"Erro ao processar hipótese: {str(e)}",
            "clarifications": {}
        }

    # 4. Extrair resultado do Metodologista
    methodologist_status = result.get('status', 'rejected')
    methodologist_justification = result.get('justification', 'Sem justificativa fornecida.')
    methodologist_clarifications = result.get('clarifications', {})

    logger.info(f"Status do Metodologista: {methodologist_status}")
    logger.info(f"Justificativa: {methodologist_justification}")
    logger.info(f"Clarificações coletadas: {len(methodologist_clarifications)}")

    # 5. Montar output estruturado para MultiAgentState
    methodologist_output = {
        "status": methodologist_status,
        "justification": methodologist_justification,
        "clarifications": methodologist_clarifications
    }

    # 6. Criar mensagem para histórico
    ai_message = AIMessage(
        content=f"Análise do Metodologista:\n"
                f"Status: {methodologist_status}\n"
                f"Justificativa: {methodologist_justification}"
    )

    logger.info("=== WRAPPER METHODOLOGIST: Finalizado ===\n")

    return {
        "methodologist_output": methodologist_output,
        "current_stage": "done",  # Processamento concluído
        "messages": [ai_message]
    }
