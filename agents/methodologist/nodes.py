"""
Nós do grafo do agente Metodologista.

Este módulo implementa os nós do Metodologista:

GRAFO INTERNO (MethodologistState - Épico 2):
- analyze: Avalia a hipótese e decide se precisa de clarificações
- ask_clarification: Solicita informações adicionais ao usuário
- decide: Toma a decisão final (aprovar/rejeitar)

MODO COLABORATIVO (MultiAgentState - Épico 4):
- decide_collaborative: Decisão com 3 status (approved/needs_refinement/rejected)

Versão: 3.0 (Épico 6, Funcionalidade 6.1 - Config externa)
Data: 13/11/2025
"""

import logging
import json
from typing import Optional
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import RunnableConfig
from langchain_anthropic import ChatAnthropic

from .state import MethodologistState
from .tools import ask_user
from utils.json_parser import extract_json_from_llm_response
from utils.prompts import METHODOLOGIST_DECIDE_PROMPT_V2
from utils.config import get_anthropic_model, invoke_with_retry
from agents.memory.config_loader import get_agent_prompt, get_agent_model, ConfigLoadError
from agents.memory.execution_tracker import register_execution
from agents.orchestrator.state import MethodologistOutputModel

logger = logging.getLogger(__name__)


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
    llm = ChatAnthropic(model=get_anthropic_model(), temperature=0)
    messages = [HumanMessage(content=analysis_prompt)]
    response = invoke_with_retry(llm=llm, messages=messages, agent_name="methodologist-analyze")

    logger.info(f"Resposta do LLM: {response.content}")

    # Parse da resposta usando função robusta
    try:
        analysis = extract_json_from_llm_response(response.content)
        needs_clarification = not analysis.get("has_sufficient_info", False)
        logger.debug(f"JSON parseado com sucesso: {analysis}")
    except json.JSONDecodeError as e:
        logger.warning(f"Falha ao parsear JSON da resposta do LLM: {e}. Assumindo que precisa de clarificação.")
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
    llm = ChatAnthropic(model=get_anthropic_model(), temperature=0)
    response = invoke_with_retry(
        llm=llm,
        messages=[HumanMessage(content=question_prompt)],
        agent_name="methodologist-ask_clarification",
    )
    question = response.content.strip()

    logger.info(f"Pergunta formulada: {question}")

    # Chamar ask_user para obter resposta
    # ask_user é um StructuredTool, então usamos .invoke() com dict de args
    answer = ask_user.invoke({"question": question})

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
    llm = ChatAnthropic(model=get_anthropic_model(), temperature=0)
    response = invoke_with_retry(
        llm=llm,
        messages=[HumanMessage(content=decision_prompt)],
        agent_name="methodologist-decide",
    )

    logger.info(f"Resposta do LLM: {response.content}")

    # Parse da decisão usando função robusta
    try:
        decision_data = extract_json_from_llm_response(response.content)
        status = decision_data.get("decision", "rejected")
        justification = decision_data.get("justification", "Decisão não especificada.")
        logger.debug(f"JSON parseado com sucesso: {decision_data}")

        # Validar status
        if status not in ["approved", "rejected"]:
            logger.warning(f"Status inválido '{status}'. Usando 'rejected' como padrão.")
            status = "rejected"

    except json.JSONDecodeError as e:
        logger.error(f"Falha ao parsear JSON da decisão: {e}. Rejeitando por segurança.")
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


# ==============================================================================
# MODO COLABORATIVO (Épico 4) - Nós para MultiAgentState
# ==============================================================================

def decide_collaborative(state: dict, config: Optional[RunnableConfig] = None) -> dict:
    """
    Nó de decisão colaborativa do Metodologista (Épico 4).

    Opera no contexto do super-grafo (MultiAgentState).
    Retorna 3 status possíveis: approved, needs_refinement, rejected.

    Este nó:
    1. Avalia a questão de pesquisa estruturada
    2. Decide com base em critérios de rigor científico
    3. Retorna improvements específicos se needs_refinement
    4. Registra decisão no hypothesis_versions
    5. Registra execução no MemoryManager (se configurado - Épico 6.2)

    Args:
        state (MultiAgentState): Estado do sistema multi-agente.
        config (RunnableConfig, optional): Configuração do LangGraph (contém memory_manager)

    Returns:
        dict: Updates do estado:
            - methodologist_output: {status, justification, improvements}
            - hypothesis_versions: Versão adicionada com feedback
            - messages: Mensagem do LLM

    Example:
        >>> state = {...}
        >>> state['structurer_output'] = {
        ...     "structured_question": "Como X impacta Y?"
        ... }
        >>> result = decide_collaborative(state)
        >>> result['methodologist_output']['status']
        'needs_refinement'  # ou 'approved' ou 'rejected'
    """
    logger.info("=== NÓ DECIDE_COLLABORATIVE: Decisão colaborativa (Épico 4) ===")

    # Carregar prompt e modelo do YAML (Épico 6, Funcionalidade 6.1)
    try:
        system_prompt = get_agent_prompt("methodologist")
        model_name = get_agent_model("methodologist")
        logger.info("✅ Configurações carregadas do YAML: config/agents/methodologist.yaml")
    except ConfigLoadError as e:
        logger.warning(f"⚠️ Falha ao carregar config do methodologist: {e}")
        logger.warning("⚠️ Usando prompt e modelo padrão (fallback)")
        # Fallback: usar prompt da utils.prompts
        system_prompt = METHODOLOGIST_DECIDE_PROMPT_V2
        model_name = "claude-sonnet-4-20250514"

    # Obter questão estruturada e input original
    original_input = state.get('user_input', '')
    if state.get('structurer_output'):
        question = state['structurer_output']['structured_question']
        logger.info(f"Avaliando questão estruturada: {question}")
    else:
        # Usar input direto se não passou pelo Estruturador
        question = state['user_input']
        logger.info(f"Avaliando input direto: {question}")

    iteration = state.get('refinement_iteration', 0)
    logger.info(f"Iteração de refinamento: {iteration}")

    # Construir prompt com questão E input original (para detectar falta de base científica)
    # Na primeira iteração, incluir contexto do input original para detectar crenças populares
    if iteration == 0 and state.get('structurer_output'):
        # Primeira avaliação após estruturação: incluir input original
        full_prompt = f"""{system_prompt}

INPUT ORIGINAL DO USUÁRIO:
"{original_input}"

QUESTÃO DE PESQUISA ESTRUTURADA:
{question}

ATENÇÃO: Verifique se o INPUT ORIGINAL demonstra crença popular, apelo ao senso comum ou falta de base científica.
Se o input original mostra falta de fundamento científico (ex: "todo mundo sabe", "é óbvio"), use status "rejected" mesmo que a questão estruturada pareça boa.

Avalie considerando TANTO o input original QUANTO a questão estruturada, e retorne APENAS o JSON com status, justification e improvements."""
    else:
        # Refinamento ou input direto: avaliar apenas a questão
        full_prompt = f"""{system_prompt}

QUESTÃO DE PESQUISA A AVALIAR:
{question}

Avalie esta questão e retorne APENAS o JSON com status, justification e improvements."""

    # Chamar LLM usando modelo do config
    llm = ChatAnthropic(model=model_name, temperature=0)
    response = invoke_with_retry(
        llm=llm,
        messages=[HumanMessage(content=full_prompt)],
        agent_name="methodologist-decide_collaborative",
    )

    logger.info(f"Resposta do LLM: {response.content[:200]}...")

    # Registrar execução no MemoryManager (Épico 6.2)
    if config:
        memory_manager = config.get("configurable", {}).get("memory_manager")
        if memory_manager:
            # Extrair status antes de registrar
            try:
                temp_data = extract_json_from_llm_response(response.content)
                temp_status = temp_data.get("status", "unknown")
            except:
                temp_status = "unknown"

            register_execution(
                memory_manager=memory_manager,
                config=config,
                agent_name="methodologist",
                response=response,
                summary=f"Decisão: {temp_status}",
                model_name=model_name,
                extra_metadata={
                    "mode": "collaborative",
                    "iteration": iteration,
                    "status": temp_status
                }
            )

    # Parse da decisão
    try:
        decision_data = extract_json_from_llm_response(response.content)
        status = decision_data.get("status", "rejected")
        justification = decision_data.get("justification", "Decisão não especificada.")
        improvements = decision_data.get("improvements", [])

        logger.debug(f"JSON parseado: status={status}, improvements={len(improvements)} gaps")

        # Validar status
        if status not in ["approved", "needs_refinement", "rejected"]:
            logger.warning(f"Status inválido '{status}'. Usando 'rejected' como padrão.")
            status = "rejected"
            improvements = []

    except json.JSONDecodeError as e:
        logger.error(f"Falha ao parsear JSON da decisão: {e}. Rejeitando por segurança.")
        status = "rejected"
        justification = "Erro ao processar decisão do LLM."
        improvements = []

    # Montar output do Metodologista com validação Pydantic
    try:
        output_model = MethodologistOutputModel(
            status=status,
            justification=justification,
            improvements=improvements,
        )
        methodologist_output = output_model.model_dump()
    except Exception as e:
        logger.error(f"Falha ao validar output do Metodologista via Pydantic: {e}")
        methodologist_output = {
            "status": status,
            "justification": justification,
            "improvements": improvements,
        }

    # Calcular versão (V1, V2, V3)
    current_version = len(state.get('hypothesis_versions', [])) + 1

    # Registrar versão no histórico
    version_entry = {
        "version": current_version,
        "question": question,
        "feedback": {
            "status": status,
            "justification": justification,
            "improvements": improvements
        }
    }

    # Atualizar hypothesis_versions
    new_versions = state.get('hypothesis_versions', []).copy() if state.get('hypothesis_versions') else []
    new_versions.append(version_entry)

    logger.info(f"Decisão: {status}")
    logger.info(f"Versão registrada: V{current_version}")
    if status == "needs_refinement":
        logger.info(f"Gaps identificados: {len(improvements)}")
        for imp in improvements:
            logger.info(f"  - {imp['aspect']}: {imp['gap']}")
    logger.info("=== NÓ DECIDE_COLLABORATIVE: Finalizado ===\n")

    return {
        "methodologist_output": methodologist_output,
        "hypothesis_versions": new_versions,
        "messages": [response]
    }
