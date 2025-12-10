"""
Tools do agente Metodologista.

Este módulo define as ferramentas (tools) que o agente pode usar
para interagir com o usuário durante a análise de hipóteses.

"""

import logging
from langchain_core.tools import tool
from langgraph.types import interrupt

logger = logging.getLogger(__name__)

@tool
def ask_user(question: str) -> str:
    """
    Faz uma pergunta ao usuário para obter clarificações sobre a hipótese.

    Esta tool permite que o agente Metodologista interrompa a execução do grafo
    e solicite informações adicionais ao usuário quando o contexto fornecido
    não é suficiente para avaliar adequadamente a hipótese.

    A execução é pausada usando `interrupt()` do LangGraph, que suspende o grafo
    até que o usuário forneça uma resposta. Quando o grafo é retomado com a resposta,
    esta tool retorna o valor fornecido.

    Args:
        question (str): Pergunta específica a ser feita ao usuário.
            Deve ser clara, objetiva e focada em obter informação necessária
            para avaliação metodológica da hipótese.

    Returns:
        str: Resposta fornecida pelo usuário.

    Example:
        >>> # Durante execução do grafo, o LLM decide chamar esta tool:
        >>> response = ask_user("Qual é a população-alvo do estudo?")
        >>> # Grafo pausa, usuário responde, grafo retoma com a resposta
        >>> print(response)
        'Adultos de 18-65 anos sem histórico de doenças cardiovasculares'

    Observações:
        - Esta tool deve ser usada com moderação (limite definido em max_iterations).
        - O controle de iterações é gerenciado pelo nó que processa a execução da tool.
        - Perguntas devem ser sobre aspectos metodológicos essenciais (população,
          variáveis, métricas, desenho experimental, etc.).
    """
    logger.info(f"Pergunta enviada ao usuário: {question}")

    # Interrompe a execução do grafo e solicita input do usuário
    user_response = interrupt(question)

    logger.info(f"Resposta recebida do usuário: {user_response}")

    return user_response
