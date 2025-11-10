"""
Definição do estado do agente Metodologista.

Este módulo define o schema do estado gerenciado pelo LangGraph,
incluindo todos os campos necessários para rastrear a análise de hipóteses.

Versão: 1.3
Data: 10/11/2025
"""

from typing import TypedDict, Annotated, Literal
from langgraph.graph.message import add_messages


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

        justification (str): Justificativa detalhada da decisão final.
            Preenchida pelo nó `decide` ao aprovar ou rejeitar a hipótese.

        needs_clarification (bool): Indica se o agente precisa de mais informações.
            Definido pelo nó `analyze` para controlar o fluxo do grafo.
    """
    hypothesis: str
    messages: Annotated[list, add_messages]
    clarifications: dict[str, str]
    status: Literal["pending", "approved", "rejected"]
    iterations: int
    max_iterations: int
    justification: str
    needs_clarification: bool


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
        max_iterations=max_iterations,
        justification="",
        needs_clarification=False
    )
