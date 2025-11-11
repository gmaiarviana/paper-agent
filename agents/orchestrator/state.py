"""
Definição do estado compartilhado do sistema multi-agente.

Este módulo define o schema do estado que é compartilhado entre todos os agentes
do sistema (Orquestrador, Estruturador, Metodologista).

O estado é híbrido: possui campos compartilhados (todos os agentes leem/escrevem)
e campos específicos por agente (apenas o agente responsável escreve).

Versão: 1.0 (Épico 3, Funcionalidade 3.1)
Data: 11/11/2025
"""

from typing import TypedDict, Optional, Annotated, Literal
from langgraph.graph.message import add_messages


class MultiAgentState(TypedDict):
    """
    Estado compartilhado entre todos os agentes do sistema multi-agente.

    Este estado é organizado em 3 seções principais:
    1. COMPARTILHADO: Campos que todos os agentes leem e escrevem
    2. ESPECÍFICO POR AGENTE: Campos que apenas um agente específico escreve
    3. MENSAGENS (LangGraph): Histórico de mensagens do LLM

    === SEÇÃO 1: CAMPOS COMPARTILHADOS ===

    user_input (str):
        Input original do usuário. Pode ser uma ideia vaga ou hipótese completa.
        Todos os agentes leem este campo como entrada inicial.

    conversation_history (list):
        Histórico legível da conversa em formato humano.
        Usado para rastreabilidade e debugging.
        Exemplo: ["Usuário: Observei X", "Orquestrador: Detectei ideia vaga"]

    current_stage (str):
        Estágio atual do processamento no sistema.
        Valores possíveis:
        - "classifying": Orquestrador está classificando input
        - "structuring": Estruturador está organizando ideia vaga
        - "validating": Metodologista está validando hipótese
        - "done": Processamento concluído

    === SEÇÃO 2: CAMPOS ESPECÍFICOS POR AGENTE ===

    orchestrator_classification (Optional[str]):
        Classificação feita pelo Orquestrador sobre a maturidade do input.
        Valores possíveis:
        - "vague": Ideia não estruturada → encaminha para Estruturador
        - "semi_formed": Hipótese parcial → encaminha para Metodologista
        - "complete": Hipótese completa → encaminha para Metodologista

    orchestrator_reasoning (Optional[str]):
        Justificativa do Orquestrador sobre por que escolheu aquela classificação.
        Usado para transparência e debugging.

    structurer_output (Optional[dict]):
        Output do Estruturador após processar ideia vaga.
        Estrutura:
        {
            "structured_question": str,  # Questão de pesquisa estruturada
            "elements": {
                "context": str,          # Contexto da observação
                "problem": str,          # Problema identificado
                "contribution": str      # Possível contribuição acadêmica
            }
        }

    methodologist_output (Optional[dict]):
        Output do Metodologista após validar hipótese.
        Estrutura:
        {
            "status": "approved" | "rejected",
            "justification": str,           # Justificativa detalhada
            "suggestions": List[str]        # Melhorias sugeridas (se aplicável)
        }

    === SEÇÃO 3: MENSAGENS (LangGraph) ===

    messages (Annotated[list, add_messages]):
        Histórico de mensagens LLM gerenciado pelo LangGraph.
        O decorator `add_messages` garante que novas mensagens sejam
        adicionadas incrementalmente (não substituídas).

    Observações:
        - Campos Optional começam como None
        - Cada agente atualiza apenas seus campos específicos
        - Orquestrador não conhece detalhes de outros agentes
        - Estado persiste entre nós via checkpointer do LangGraph
    """

    # === COMPARTILHADO ===
    user_input: str
    conversation_history: list
    current_stage: Literal["classifying", "structuring", "validating", "done"]

    # === ESPECÍFICO: ORQUESTRADOR ===
    orchestrator_classification: Optional[str]
    orchestrator_reasoning: Optional[str]

    # === ESPECÍFICO: ESTRUTURADOR ===
    structurer_output: Optional[dict]

    # === ESPECÍFICO: METODOLOGISTA ===
    methodologist_output: Optional[dict]

    # === MENSAGENS (LangGraph) ===
    messages: Annotated[list, add_messages]


def create_initial_multi_agent_state(user_input: str) -> MultiAgentState:
    """
    Cria o estado inicial do sistema multi-agente com valores padrão.

    Args:
        user_input (str): Input do usuário (ideia, observação ou hipótese).

    Returns:
        MultiAgentState: Estado inicial pronto para ser usado pelo super-grafo.

    Example:
        >>> state = create_initial_multi_agent_state(
        ...     user_input="Observei que desenvolver com Claude Code é mais rápido"
        ... )
        >>> state['current_stage']
        'classifying'
        >>> state['orchestrator_classification']
        None
        >>> state['user_input']
        'Observei que desenvolver com Claude Code é mais rápido'
    """
    return MultiAgentState(
        # Compartilhado
        user_input=user_input,
        conversation_history=[f"Usuário: {user_input}"],
        current_stage="classifying",

        # Específico: Orquestrador
        orchestrator_classification=None,
        orchestrator_reasoning=None,

        # Específico: Estruturador
        structurer_output=None,

        # Específico: Metodologista
        methodologist_output=None,

        # Mensagens LangGraph
        messages=[]
    )
