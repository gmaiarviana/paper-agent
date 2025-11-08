"""
Agente Metodologista: Avalia rigor científico de hipóteses e constatações.

Este módulo implementa o agente Metodologista usando LangGraph,
responsável por validar hipóteses do ponto de vista metodológico.

Versão: 1.1
Data: 08/11/2025
Status: Funcionalidade 2.3 - Tool ask_user implementada
"""

import logging
from typing import TypedDict, Annotated, Literal
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt
from langchain_core.tools import tool

# Configurar logging
logger = logging.getLogger(__name__)


# ==============================================================================
# STATE DEFINITION
# ==============================================================================

class MethodologistState(TypedDict):
    """
    Estado do agente Metodologista gerenciado pelo LangGraph.

    Este estado mantém o contexto completo de uma análise de hipótese,
    incluindo o histórico de mensagens, clarificações e status da avaliação.

    Campos:
        hypothesis (str): A hipótese ou constatação a ser avaliada.

        messages (Annotated[list, add_messages]): Histórico de mensagens da conversa
            entre o agente e o LLM. O `add_messages` garante que novas mensagens
            sejam adicionadas à lista de forma incremental.

        clarifications (dict[str, str]): Dicionário de perguntas e respostas
            coletadas durante a análise. Chave = pergunta, Valor = resposta.

        status (Literal["pending", "approved", "rejected"]): Status atual da análise:
            - "pending": Análise em andamento, aguardando mais informações
            - "approved": Hipótese aprovada com rigor científico adequado
            - "rejected": Hipótese rejeitada por falhas metodológicas

        iterations (int): Contador de iterações realizadas (perguntas feitas).
            Incrementado a cada chamada da tool `ask_user`.

        max_iterations (int): Limite máximo de perguntas que o agente pode fazer
            ao usuário. Após atingir este limite, o agente deve decidir baseado
            no contexto disponível.
    """
    hypothesis: str
    messages: Annotated[list, add_messages]
    clarifications: dict[str, str]
    status: Literal["pending", "approved", "rejected"]
    iterations: int
    max_iterations: int


# ==============================================================================
# CHECKPOINTER CONFIGURATION
# ==============================================================================

# MemorySaver: Checkpointer padrão do LangGraph para persistência de sessão em memória.
# Permite que o estado do grafo seja salvo e recuperado durante a execução,
# essencial para handling de interrupções (interrupt) e continuação da conversa.
checkpointer = MemorySaver()


# ==============================================================================
# TOOLS
# ==============================================================================

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


# ==============================================================================
# STATE INITIALIZATION
# ==============================================================================

def create_initial_state(hypothesis: str, max_iterations: int = 3) -> MethodologistState:
    """
    Cria o estado inicial do agente Metodologista com valores padrão.

    Args:
        hypothesis (str): A hipótese ou constatação a ser avaliada.
        max_iterations (int): Limite de perguntas que o agente pode fazer.
            Padrão: 3 iterações.

    Returns:
        MethodologistState: Estado inicial pronto para ser usado pelo grafo.

    Example:
        >>> state = create_initial_state(
        ...     hypothesis="Café aumenta produtividade",
        ...     max_iterations=3
        ... )
        >>> state['status']
        'pending'
        >>> state['iterations']
        0
    """
    return MethodologistState(
        hypothesis=hypothesis,
        messages=[],
        clarifications={},
        status="pending",
        iterations=0,
        max_iterations=max_iterations
    )
