"""
Definição do estado compartilhado do sistema multi-agente.

Este módulo define o schema do estado que é compartilhado entre todos os agentes
do sistema (Orquestrador, Estruturador, Metodologista).

O estado é híbrido: possui campos compartilhados (todos os agentes leem/escrevem)
e campos específicos por agente (apenas o agente responsável escreve).

Versão: 4.0 (Épico 11 - Modelagem Cognitiva)
Data: 17/11/2025
"""

from typing import TypedDict, Optional, Annotated, Literal, List
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage
from pydantic import BaseModel, Field, ConfigDict


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

    focal_argument (Optional[dict]):
        Argumento focal explícito extraído/atualizado pelo Orquestrador (Épico 7.8).
        Representa o entendimento atual do sistema sobre o que o usuário quer fazer.
        Atualizado a cada turno de conversa pelo Orquestrador.
        Usado para:
        - Detecção eficiente de mudança de direção (compara focal atual vs novo)
        - Contexto preservado entre turnos
        - Fundação para persistência (Épico 10)
        Estrutura:
        {
            "intent": str,           # "test_hypothesis", "review_literature", "build_theory"
            "subject": str,          # Tópico principal (ex: "LLMs impact on productivity")
            "population": str,       # População-alvo (ex: "teams of 2-5 developers")
            "metrics": str,          # Métricas mencionadas (ex: "time per sprint")
            "article_type": str      # Tipo inferido: "empirical", "review", "theoretical", etc.
        }
        Exemplo: {
            "intent": "test_hypothesis",
            "subject": "LLMs impact on developer productivity",
            "population": "teams of 2-5 developers",
            "metrics": "time per sprint",
            "article_type": "empirical"
        }

    cognitive_model (Optional[dict]):
        Modelo cognitivo explícito que representa evolução do argumento (Épico 11.1).
        Estrutura lógica completa do argumento em construção durante conversa.
        Volátil (em memória) - atualizado pelo Orquestrador a cada turno.
        Ao ser persistido, vira entidade Argument no banco de dados.
        Estrutura:
        {
            "claim": str,                      # Afirmação central
            "proposicoes": list[dict],         # Fundamentos com solidez gradual (0-1)
            "open_questions": list[str],       # Lacunas identificadas
            "contradictions": list[dict],      # Tensões internas (confiança > 80%)
            "solid_grounds": list[dict],       # Evidências bibliográficas
            "context": dict                    # Metadados (domínio, tecnologia, etc)
        }
        Proposições substituem premises/assumptions (Épico 11):
        - proposicoes com solidez >= 0.6: fundamentos sólidos (antes: premises)
        - proposicoes com solidez < 0.6: hipóteses a validar (antes: assumptions)
        Responsabilidades:
        - Orquestrador: claim, proposicoes, open_questions, context
        - Metodologista: contradictions
        - Pesquisador (futuro): solid_grounds
        Ver agents/models/cognitive_model.py para schema Pydantic completo.

    reflection_prompt (Optional[str]):
        Provocação de reflexão gerada pelo Orquestrador (Épico 7.9).
        Pergunta que ajuda usuário a pensar sobre aspectos não explorados.
        Apenas preenchida quando Orquestrador identifica lacuna na conversa.
        Exemplo: "Você mencionou produtividade, mas e QUALIDADE do código? Isso importa para sua pesquisa?"

    stage_suggestion (Optional[dict]):
        Sugestão emergente de mudança de estágio (Épico 7.10).
        Orquestrador detecta quando conversa evoluiu naturalmente.
        Apenas preenchida quando sistema infere mudança de estágio.
        Estrutura:
        {
            "from_stage": str,       # Estágio atual inferido (ex: "exploration")
            "to_stage": str,         # Estágio sugerido (ex: "hypothesis")
            "justification": str     # Por que sistema acha que evoluiu
        }
        Exemplo: {
            "from_stage": "exploration",
            "to_stage": "hypothesis",
            "justification": "Usuário definiu população, métricas e contexto. Parece que temos hipótese formada."
        }

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

    === SEÇÃO 2.5: MÉTRICAS DO ÚLTIMO AGENTE (Épico 8.3) ===

    last_agent_tokens_input (Optional[int]):
        Tokens de entrada consumidos pelo último agente que executou.
        Usado por instrument_node para publicar métricas no EventBus.
        Extraído de response.usage_metadata pelo próprio agente.

    last_agent_tokens_output (Optional[int]):
        Tokens de saída gerados pelo último agente que executou.
        Usado por instrument_node para publicar métricas no EventBus.
        Extraído de response.usage_metadata pelo próprio agente.

    last_agent_cost (Optional[float]):
        Custo em USD da execução do último agente.
        Calculado via CostTracker baseado nos tokens.
        Usado por instrument_node para publicar métricas no EventBus.

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

    # === ESPECÍFICO: ORQUESTRADOR (Épico 7 - Conversacional MVP) ===
    orchestrator_analysis: Optional[str]
    next_step: Optional[Literal["explore", "suggest_agent", "clarify"]]
    agent_suggestion: Optional[dict]
    focal_argument: Optional[dict]  # Épico 7.8: Argumento focal explícito
    cognitive_model: Optional[dict]  # Épico 11.1: Modelo cognitivo explícito
    reflection_prompt: Optional[str]  # Épico 7.9: Provocação de reflexão
    stage_suggestion: Optional[dict]  # Épico 7.10: Detecção emergente de estágio

    # === ESPECÍFICO: ESTRUTURADOR ===
    structurer_output: Optional[dict]

    # === ESPECÍFICO: METODOLOGISTA ===
    methodologist_output: Optional[dict]

    # === MÉTRICAS DO ÚLTIMO AGENTE (Épico 8.3) ===
    last_agent_tokens_input: Optional[int]
    last_agent_tokens_output: Optional[int]
    last_agent_cost: Optional[float]

    # === MENSAGENS (LangGraph) ===
    messages: Annotated[list, add_messages]


def create_initial_multi_agent_state(user_input: str, session_id: Optional[str] = None) -> MultiAgentState:
    """
    Cria o estado inicial do sistema multi-agente com valores padrão.

    Args:
        user_input (str): Input do usuário (ideia, observação ou hipótese).
        session_id (str | None): ID único da sessão (para EventBus - Épico 5.1).
            Se None, será usado um ID padrão genérico (apenas para testes).

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
    if session_id is None:
        # ID genérico usado em contextos de teste ou quando o chamador não precisa
        # de integração com EventBus/Dashboard.
        session_id = "test-session-default"

    return MultiAgentState(
        # Compartilhado
        user_input=user_input,
        session_id=session_id,
        conversation_history=[f"Usuário: {user_input}"],
        current_stage="classifying",

        # Versionamento (Épico 4)
        hypothesis_versions=[],

        # Específico: Orquestrador (Épico 7 - Conversacional MVP)
        orchestrator_analysis=None,
        next_step=None,
        agent_suggestion=None,
        focal_argument=None,  # Épico 7.8
        cognitive_model=None,  # Épico 11.1
        reflection_prompt=None,  # Épico 7.9
        stage_suggestion=None,  # Épico 7.10

        # Específico: Estruturador
        structurer_output=None,

        # Específico: Metodologista
        methodologist_output=None,

        # Métricas do último agente (Épico 8.3)
        last_agent_tokens_input=None,
        last_agent_tokens_output=None,
        last_agent_cost=None,

        # Mensagens LangGraph (BUGFIX: adicionar HumanMessage para persistência)
        messages=[HumanMessage(content=user_input)]
    )


# ============================================================================
# MODELOS Pydantic PARA OUTPUTS DOS AGENTES
# ============================================================================


class StructurerElementsModel(BaseModel):
    """Elementos estruturados retornados pelo Estruturador."""

    context: str = Field(..., description="Contexto da observação")
    problem: str = Field(..., description="Problema ou gap identificado")
    contribution: str = Field(..., description="Possível contribuição acadêmica ou prática")


class StructurerOutputModel(BaseModel):
    """
    Output estruturado do agente Estruturador.

    Este modelo reflete a estrutura esperada em MultiAgentState.structurer_output.
    """

    structured_question: str = Field(..., description="Questão de pesquisa estruturada")
    elements: StructurerElementsModel

    model_config = ConfigDict(extra="ignore")


class MethodologistImprovementModel(BaseModel):
    """Gap identificado pelo Metodologista em modo colaborativo."""

    aspect: str = Field(..., description="Aspecto a ser melhorado (ex: população, métricas)")
    gap: str = Field(..., description="Descrição do gap identificado")


class MethodologistOutputModel(BaseModel):
    """
    Output estruturado do Metodologista em MultiAgentState.methodologist_output.
    """

    status: Literal["approved", "needs_refinement", "rejected"] = Field(
        ...,
        description="Status final da avaliação",
    )
    justification: str = Field(
        ...,
        description="Justificativa detalhada da decisão",
    )
    improvements: List[MethodologistImprovementModel] = Field(
        default_factory=list,
        description="Lista de gaps e sugestões quando status=needs_refinement",
    )

    model_config = ConfigDict(extra="ignore")
