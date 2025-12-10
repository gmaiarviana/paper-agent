"""
Helper para registro de execuções de agentes com captura de tokens.

Este módulo fornece funções para extrair metadados de tokens de respostas
LLM (LangChain AIMessage), calcular custos e registrar no MemoryManager.

Épico 6.2: Registro de Memória com Metadados

"""

from typing import Optional, Dict, Any
from agents.memory.memory_manager import MemoryManager, AgentExecution
from utils.cost_tracker import CostTracker

def register_execution(
    memory_manager: Optional[MemoryManager],
    config: Dict[str, Any],
    agent_name: str,
    response: Any,  # LangChain AIMessage
    summary: str,
    model_name: str,
    extra_metadata: Optional[Dict[str, Any]] = None
) -> Optional[AgentExecution]:
    """
    Extrai tokens de AIMessage, calcula custos e registra execução.

    Args:
        memory_manager: Instância do MemoryManager (None = não registra)
        config: Config do LangGraph contendo thread_id
        agent_name: Nome do agente executando
        response: AIMessage do LangChain com metadados de tokens
        summary: Resumo da ação executada (até 280 chars recomendado)
        model_name: Nome do modelo LLM usado
        extra_metadata: Metadados adicionais personalizados (opcional)

    Returns:
        AgentExecution registrada ou None se memory_manager não fornecido

    Example:
        >>> memory_manager = MemoryManager()
        >>> config = {"configurable": {"thread_id": "session-123"}}
        >>> response = llm.invoke(messages)  # AIMessage
        >>>
        >>> execution = register_execution(
        ...     memory_manager=memory_manager,
        ...     config=config,
        ...     agent_name="orchestrator",
        ...     response=response,
        ...     summary="Classificação: vague",
        ...     model_name="claude-3-5-haiku-20241022"
        ... )
    """
    # Retornar None se memory_manager não fornecido
    if memory_manager is None:
        return None

    # Extrair session_id do config
    session_id = config.get("configurable", {}).get("thread_id", "default")

    # Extrair tokens da resposta (suporta múltiplos formatos)
    input_tokens = 0
    output_tokens = 0

    # Tentar response_metadata['usage'] (LangChain 0.2)
    try:
        if hasattr(response, 'response_metadata') and isinstance(response.response_metadata, dict):
            usage = response.response_metadata.get('usage', {})
            if isinstance(usage, dict):
                input_tokens = usage.get('input_tokens', 0)
                output_tokens = usage.get('output_tokens', 0)
    except (AttributeError, TypeError):
        pass

    # Fallback: tentar usage_metadata como atributo (LangChain 0.3+)
    if input_tokens == 0 and output_tokens == 0:
        try:
            if hasattr(response, 'usage_metadata'):
                usage = response.usage_metadata
                if isinstance(usage, dict):
                    input_tokens = usage.get('input_tokens', 0)
                    output_tokens = usage.get('output_tokens', 0)
        except (AttributeError, TypeError):
            pass

    # Calcular custos
    costs = CostTracker.calculate_cost(
        model=model_name,
        input_tokens=input_tokens,
        output_tokens=output_tokens
    )

    # Montar metadados
    metadata = {
        "model": model_name,
        "cost_usd": costs["total_cost"],
        "cost_input_usd": costs["input_cost"],
        "cost_output_usd": costs["output_cost"]
    }

    # Adicionar metadados extras se fornecidos
    if extra_metadata:
        metadata.update(extra_metadata)

    # Registrar no MemoryManager
    execution = memory_manager.add_execution(
        session_id=session_id,
        agent_name=agent_name,
        tokens_input=input_tokens,
        tokens_output=output_tokens,
        summary=summary,
        metadata=metadata
    )

    return execution
