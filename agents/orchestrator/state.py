"""
Definição do estado compartilhado do sistema multi-agente.

Este módulo define o schema do estado que é compartilhado entre todos os agentes
do sistema (Orquestrador, Estruturador, Metodologista).

O estado é híbrido: possui campos compartilhados (todos os agentes leem/escrevem)
e campos específicos por agente (apenas o agente responsável escreve).

Versão: 2.1 (Épico 7, Task 7.1.5 - Orquestrador Conversacional POC)
Data: 14/11/2025
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


    hypothesis_versions (list):
        Histórico de versões da hipótese/questão de pesquisa (Épico 4).
        Cada versão contém: version (int), question (str), feedback (dict)
        Usado para rastreabilidade e transparência do processo de refinamento.
        Estrutura:
        [
            {
                "version": 1,
                "question": "Como X impacta Y?",
                "feedback": {
                    "status": "needs_refinement",
                    "improvements": [...]
                }
            }
        ]

    === SEÇÃO 2: CAMPOS ESPECÍFICOS POR AGENTE ===

    orchestrator_analysis (Optional[str]):
        Análise do Orquestrador sobre o contexto e histórico conversacional (Épico 7).
        Contém o raciocínio do Orquestrador sobre o que está claro e o que falta.
        Usado para transparência e debugging.
        Exemplo: "Usuário mencionou produtividade mas não especificou métricas..."

    next_step (Optional[Literal["explore", "suggest_agent", "clarify"]]):
        Próximo passo definido pelo Orquestrador (Épico 7).
        Valores possíveis:
        - "explore": Fazer perguntas abertas para entender melhor o contexto
        - "suggest_agent": Sugerir chamada de agente especializado
        - "clarify": Esclarecer algum aspecto específico do input

    agent_suggestion (Optional[dict]):
        Sugestão de agente com justificativa (Épico 7).
        Apenas preenchido quando next_step = "suggest_agent".
        Estrutura:
        {
            "agent": str,            # Nome do agente (ex: "methodologist", "structurer")
            "justification": str     # Por que faz sentido chamar este agente
        }
        Exemplo: {"agent": "methodologist", "justification": "Usuário definiu população e métricas"}

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
        Estrutura (Épico 4 - Modo Colaborativo):
        {
            "status": "approved" | "needs_refinement" | "rejected",
            "justification": str,           # Justificativa detalhada
            "improvements": List[dict]      # Gaps e sugestões (se needs_refinement)
        }

        Status:
        - "approved": Hipótese testável, aprovada
        - "needs_refinement": Tem potencial mas faltam elementos (volta para Estruturador)
        - "rejected": Sem potencial científico (finaliza)

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
    session_id: str  # ID único da sessão (Épico 5.1 - para EventBus)
    conversation_history: list
    current_stage: Literal["classifying", "structuring", "validating", "done"]

    # === VERSIONAMENTO (Épico 4) ===
    hypothesis_versions: list

    # === ESPECÍFICO: ORQUESTRADOR (Épico 7 - Conversacional) ===
    orchestrator_analysis: Optional[str]
    next_step: Optional[Literal["explore", "suggest_agent", "clarify"]]
    agent_suggestion: Optional[dict]

    # === ESPECÍFICO: ESTRUTURADOR ===
    structurer_output: Optional[dict]

    # === ESPECÍFICO: METODOLOGISTA ===
    methodologist_output: Optional[dict]

    # === MENSAGENS (LangGraph) ===
    messages: Annotated[list, add_messages]


def create_initial_multi_agent_state(user_input: str, session_id: str) -> MultiAgentState:
    """
    Cria o estado inicial do sistema multi-agente com valores padrão.

    Args:
        user_input (str): Input do usuário (ideia, observação ou hipótese).
        session_id (str): ID único da sessão (para EventBus - Épico 5.1).

    Returns:
        MultiAgentState: Estado inicial pronto para ser usado pelo super-grafo.

    Example:
        >>> state = create_initial_multi_agent_state(
        ...     user_input="Observei que desenvolver com Claude Code é mais rápido",
        ...     session_id="cli-session-abc123"
        ... )
        >>> state['current_stage']
        'classifying'
        >>> state['session_id']
        'cli-session-abc123'
        >>> state['hypothesis_versions']
        []
    """
    return MultiAgentState(
        # Compartilhado
        user_input=user_input,
        session_id=session_id,
        conversation_history=[f"Usuário: {user_input}"],
        current_stage="classifying",

        # Versionamento (Épico 4)
        hypothesis_versions=[],

        # Específico: Orquestrador (Épico 7 - Conversacional)
        orchestrator_analysis=None,
        next_step=None,
        agent_suggestion=None,

        # Específico: Estruturador
        structurer_output=None,

        # Específico: Metodologista
        methodologist_output=None,

        # Mensagens LangGraph
        messages=[]
    )
