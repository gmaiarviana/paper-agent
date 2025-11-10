"""
Agente Metodologista: Avalia rigor científico de hipóteses e constatações.

Este módulo implementa o agente Metodologista usando LangGraph,
responsável por validar hipóteses do ponto de vista metodológico.

Versão: 1.2
Data: 10/11/2025
Status: Funcionalidade 2.4 - Nós do Grafo implementados
"""

import logging
import json
from typing import TypedDict, Annotated, Literal
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_anthropic import ChatAnthropic

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
        max_iterations=max_iterations,
        justification="",
        needs_clarification=False
    )


# ==============================================================================
# GRAPH NODES
# ==============================================================================

def analyze(state: MethodologistState) -> dict:
    """
    Nó que avalia a hipótese usando LLM e decide se precisa de clarificações.

    Este nó é o primeiro passo do raciocínio do agente. Ele:
    1. Analisa a hipótese fornecida
    2. Considera clarificações já coletadas (se houver)
    3. Decide se há informação suficiente para deliberar ou se precisa de mais contexto
    4. Atualiza o histórico de mensagens com a análise do LLM

    Args:
        state (MethodologistState): Estado atual do grafo.

    Returns:
        dict: Dicionário com updates incrementais do estado:
            - messages: Nova mensagem do LLM adicionada
            - needs_clarification: True se precisa de mais informações, False caso contrário

    Example:
        >>> state = create_initial_state("Café aumenta produtividade")
        >>> updates = analyze(state)
        >>> updates['needs_clarification']
        True  # Provavelmente precisa de mais detalhes
    """
    logger.info("=== NÓ ANALYZE: Iniciando análise da hipótese ===")
    logger.info(f"Hipótese: {state['hypothesis']}")
    logger.info(f"Iterações: {state['iterations']}/{state['max_iterations']}")
    logger.info(f"Clarificações coletadas: {len(state['clarifications'])}")

    # Construir contexto com clarificações já obtidas
    clarifications_context = ""
    if state['clarifications']:
        clarifications_context = "\n\nClarificações obtidas:\n"
        for question, answer in state['clarifications'].items():
            clarifications_context += f"- Pergunta: {question}\n  Resposta: {answer}\n"

    # Criar prompt para análise
    analysis_prompt = f"""Você é um Metodologista científico especializado em avaliar rigor de hipóteses.

HIPÓTESE A AVALIAR:
{state['hypothesis']}
{clarifications_context}

TAREFA:
Analise se você tem informação SUFICIENTE para decidir se esta hipótese atende critérios de rigor científico (testabilidade, falseabilidade, especificidade).

RESPONDA EM JSON:
{{
    "has_sufficient_info": true/false,
    "reasoning": "breve explicação do que você observa",
    "missing_info": "o que está faltando (se has_sufficient_info for false)"
}}

Se faltam detalhes ESSENCIAIS (população, variáveis, métricas, condições), marque has_sufficient_info como false.
Se a hipótese é claramente boa ou ruim com o contexto atual, marque true."""

    # Chamar LLM
    llm = ChatAnthropic(model="claude-3-5-haiku-20241022", temperature=0)
    messages = [HumanMessage(content=analysis_prompt)]
    response = llm.invoke(messages)

    logger.info(f"Resposta do LLM: {response.content}")

    # Parse da resposta
    try:
        analysis = json.loads(response.content)
        needs_clarification = not analysis.get("has_sufficient_info", False)
    except json.JSONDecodeError:
        logger.warning("Falha ao parsear JSON da resposta do LLM. Assumindo que precisa de clarificação.")
        needs_clarification = True

    logger.info(f"Decisão: needs_clarification = {needs_clarification}")
    logger.info("=== NÓ ANALYZE: Finalizado ===\n")

    return {
        "messages": [response],
        "needs_clarification": needs_clarification
    }


def ask_clarification(state: MethodologistState) -> dict:
    """
    Nó que solicita clarificação ao usuário e registra a resposta.

    Este nó é executado quando o agente precisa de mais informações para avaliar
    a hipótese. Ele:
    1. Verifica se ainda não atingiu o limite de iterações
    2. Usa LLM para formular uma pergunta específica
    3. Chama a tool ask_user para obter resposta do usuário
    4. Registra a pergunta/resposta em clarifications
    5. Incrementa o contador de iterações

    Args:
        state (MethodologistState): Estado atual do grafo.

    Returns:
        dict: Dicionário com updates incrementais do estado:
            - clarifications: Pergunta e resposta adicionadas
            - iterations: Contador incrementado
            - messages: Mensagem do LLM adicionada

    Example:
        >>> state = create_initial_state("Café aumenta produtividade")
        >>> state['iterations'] = 1
        >>> updates = ask_clarification(state)
        >>> updates['iterations']
        2
    """
    logger.info("=== NÓ ASK_CLARIFICATION: Solicitando clarificação ===")
    logger.info(f"Iterações: {state['iterations']}/{state['max_iterations']}")

    # Verificar se já atingiu o limite
    if state['iterations'] >= state['max_iterations']:
        logger.warning(f"Limite de iterações atingido ({state['max_iterations']}). Pulando clarificação.")
        return {"messages": [AIMessage(content="Limite de perguntas atingido. Prosseguindo para decisão.")]}

    # Construir contexto
    clarifications_context = ""
    if state['clarifications']:
        clarifications_context = "\n\nPerguntas já feitas:\n"
        for question, answer in state['clarifications'].items():
            clarifications_context += f"- {question}\n"

    # Criar prompt para formular pergunta
    question_prompt = f"""Você é um Metodologista científico. Você está avaliando esta hipótese:

HIPÓTESE:
{state['hypothesis']}
{clarifications_context}

TAREFA:
Formule UMA pergunta específica para obter informação essencial que falta para avaliar o rigor científico desta hipótese.

Foque em aspectos metodológicos críticos:
- População/amostra
- Variáveis (dependente, independente)
- Métricas e instrumentos de medição
- Condições experimentais
- Critérios de testabilidade

RESPONDA APENAS COM A PERGUNTA (sem preâmbulo ou explicação)."""

    # Chamar LLM para gerar pergunta
    llm = ChatAnthropic(model="claude-3-5-haiku-20241022", temperature=0)
    response = llm.invoke([HumanMessage(content=question_prompt)])
    question = response.content.strip()

    logger.info(f"Pergunta formulada: {question}")

    # Chamar ask_user para obter resposta
    answer = ask_user(question)

    logger.info(f"Resposta do usuário: {answer}")

    # Atualizar clarifications
    new_clarifications = state['clarifications'].copy()
    new_clarifications[question] = answer

    # Incrementar iterations
    new_iterations = state['iterations'] + 1

    logger.info(f"Clarificação registrada. Total de iterações: {new_iterations}")
    logger.info("=== NÓ ASK_CLARIFICATION: Finalizado ===\n")

    return {
        "clarifications": new_clarifications,
        "iterations": new_iterations,
        "messages": [response, HumanMessage(content=answer)]
    }


def decide(state: MethodologistState) -> dict:
    """
    Nó que toma a decisão final sobre a hipótese.

    Este é o nó final do raciocínio do agente. Ele:
    1. Analisa toda a informação coletada (hipótese + clarificações)
    2. Decide se a hipótese deve ser aprovada ou rejeitada
    3. Gera uma justificativa detalhada da decisão
    4. Atualiza o status final

    Args:
        state (MethodologistState): Estado atual do grafo.

    Returns:
        dict: Dicionário com updates finais do estado:
            - status: "approved" ou "rejected"
            - justification: Explicação detalhada da decisão
            - messages: Mensagem do LLM com a deliberação

    Example:
        >>> state = create_initial_state("Café aumenta produtividade")
        >>> state['clarifications'] = {"População?": "Adultos 18-40 anos"}
        >>> updates = decide(state)
        >>> updates['status'] in ['approved', 'rejected']
        True
    """
    logger.info("=== NÓ DECIDE: Tomando decisão final ===")
    logger.info(f"Hipótese: {state['hypothesis']}")
    logger.info(f"Total de clarificações: {len(state['clarifications'])}")

    # Construir contexto completo
    clarifications_context = ""
    if state['clarifications']:
        clarifications_context = "\n\nClarificações obtidas:\n"
        for question, answer in state['clarifications'].items():
            clarifications_context += f"- Pergunta: {question}\n  Resposta: {answer}\n"

    # Criar prompt para decisão final
    decision_prompt = f"""Você é um Metodologista científico. Avalie esta hipótese segundo critérios de rigor científico.

HIPÓTESE:
{state['hypothesis']}
{clarifications_context}

CRITÉRIOS DE AVALIAÇÃO:
1. **Testabilidade**: A hipótese pode ser testada empiricamente?
2. **Falseabilidade**: É possível conceber um resultado que a refutaria?
3. **Especificidade**: Define claramente população, variáveis, métricas e condições?
4. **Operacionalização**: As variáveis são mensuráveis e bem definidas?

DECISÃO:
- **APROVAR** se a hipótese atende os critérios acima (mesmo que precise de pequenos ajustes)
- **REJEITAR** se há falhas graves que comprometem o rigor científico

RESPONDA EM JSON:
{{
    "decision": "approved" ou "rejected",
    "justification": "explicação detalhada da decisão, citando critérios específicos e evidências da hipótese"
}}"""

    # Chamar LLM para decisão
    llm = ChatAnthropic(model="claude-3-5-haiku-20241022", temperature=0)
    response = llm.invoke([HumanMessage(content=decision_prompt)])

    logger.info(f"Resposta do LLM: {response.content}")

    # Parse da decisão
    try:
        decision_data = json.loads(response.content)
        status = decision_data.get("decision", "rejected")
        justification = decision_data.get("justification", "Decisão não especificada.")

        # Validar status
        if status not in ["approved", "rejected"]:
            logger.warning(f"Status inválido '{status}'. Usando 'rejected' como padrão.")
            status = "rejected"

    except json.JSONDecodeError:
        logger.error("Falha ao parsear JSON da decisão. Rejeitando por segurança.")
        status = "rejected"
        justification = "Erro ao processar decisão do LLM."

    logger.info(f"Decisão final: {status}")
    logger.info(f"Justificativa: {justification}")
    logger.info("=== NÓ DECIDE: Finalizado ===\n")

    return {
        "status": status,
        "justification": justification,
        "messages": [response]
    }
