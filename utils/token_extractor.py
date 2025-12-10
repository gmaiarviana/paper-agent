"""
Helper para extração de tokens e cálculo de custo de respostas LLM.

Este módulo fornece função reutilizável para extrair métricas de uso de tokens
de respostas AIMessage do LangChain e calcular custos via CostTracker.

Épico 8.3: Métricas consolidadas (tokens, custo, tempo)

"""

from typing import Dict, Any
from utils.cost_tracker import CostTracker
import logging

logger = logging.getLogger(__name__)

def extract_tokens_and_cost(response: Any, model_name: str) -> Dict[str, Any]:
    """
    Extrai tokens e calcula custo de resposta LLM (AIMessage).

    Esta função tenta extrair tokens de múltiplos formatos de resposta:
    1. response.usage_metadata (LangChain 0.3+)
    2. response.response_metadata['usage'] (LangChain 0.2)

    Após extrair tokens, calcula custo usando CostTracker.

    Args:
        response: AIMessage do LangChain com metadados de uso
        model_name: Nome do modelo LLM usado (ex: "claude-3-5-haiku-20241022")

    Returns:
        Dict com estrutura:
        {
            "tokens_input": int,      # Tokens de entrada
            "tokens_output": int,     # Tokens de saída
            "tokens_total": int,      # Total de tokens
            "cost": float             # Custo em USD
        }

    Example:
        >>> from langchain_anthropic import ChatAnthropic
        >>> from langchain_core.messages import HumanMessage
        >>> llm = ChatAnthropic(model="claude-3-5-haiku-20241022")
        >>> response = llm.invoke([HumanMessage(content="Hello")])
        >>> metrics = extract_tokens_and_cost(response, "claude-3-5-haiku-20241022")
        >>> metrics['tokens_total'] > 0
        True
        >>> metrics['cost'] > 0
        True

    Notes:
        - Se tokens não puderem ser extraídos, retorna zeros (não falha)
        - Suporta múltiplos formatos de resposta do LangChain
        - Custo é calculado via CostTracker baseado no modelo
    """
    input_tokens = 0
    output_tokens = 0

    # Tentar extrair de usage_metadata (LangChain 0.3+)
    try:
        if hasattr(response, 'usage_metadata'):
            usage = response.usage_metadata
            if isinstance(usage, dict):
                input_tokens = usage.get('input_tokens', 0)
                output_tokens = usage.get('output_tokens', 0)
                logger.debug(f"Tokens extraídos de usage_metadata: input={input_tokens}, output={output_tokens}")
    except (AttributeError, TypeError) as e:
        logger.debug(f"Não foi possível extrair de usage_metadata: {e}")

    # Fallback: tentar response_metadata['usage'] (LangChain 0.2)
    if input_tokens == 0 and output_tokens == 0:
        try:
            if hasattr(response, 'response_metadata') and isinstance(response.response_metadata, dict):
                usage = response.response_metadata.get('usage', {})
                if isinstance(usage, dict):
                    input_tokens = usage.get('input_tokens', 0)
                    output_tokens = usage.get('output_tokens', 0)
                    logger.debug(f"Tokens extraídos de response_metadata: input={input_tokens}, output={output_tokens}")
        except (AttributeError, TypeError) as e:
            logger.debug(f"Não foi possível extrair de response_metadata: {e}")

    # Calcular total
    total_tokens = input_tokens + output_tokens

    # Calcular custo via CostTracker
    costs = CostTracker.calculate_cost(
        model=model_name,
        input_tokens=input_tokens,
        output_tokens=output_tokens
    )

    # Retornar métricas consolidadas
    return {
        "tokens_input": input_tokens,
        "tokens_output": output_tokens,
        "tokens_total": total_tokens,
        "cost": costs["total_cost"]
    }
