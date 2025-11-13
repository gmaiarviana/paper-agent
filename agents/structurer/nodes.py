"""
Nós do grafo do agente Estruturador.

Este módulo implementa o nó principal do Estruturador:
- structurer_node: Organiza ideias vagas em questões de pesquisa estruturadas (Épico 3)
- Suporta refinamento baseado em feedback do Metodologista (Épico 4)

Versão: 3.0 (Épico 6, Funcionalidade 6.1 - Config externa)
Data: 13/11/2025
"""

import logging
import json
from langchain_core.messages import HumanMessage, AIMessage
from langchain_anthropic import ChatAnthropic

from agents.orchestrator.state import MultiAgentState
from utils.json_parser import extract_json_from_llm_response
from utils.prompts import STRUCTURER_REFINEMENT_PROMPT_V1
from utils.config import get_anthropic_model
from agents.memory.config_loader import get_agent_prompt, get_agent_model, ConfigLoadError

logger = logging.getLogger(__name__)


def structurer_node(state: MultiAgentState) -> dict:
    """
    Nó que organiza ideias vagas em questões de pesquisa estruturadas.

    Este nó opera em dois modos:

    1. ESTRUTURAÇÃO INICIAL (Épico 3):
       - Recebe observação vaga do usuário
       - Gera questão de pesquisa estruturada (V1)

    2. REFINAMENTO (Épico 4):
       - Recebe feedback do Metodologista (needs_refinement)
       - Gera versão refinada endereçando gaps específicos (V2, V3)

    IMPORTANTE: Este nó é COLABORATIVO:
    - NÃO rejeita ideias
    - NÃO valida rigor científico (isso é responsabilidade do Metodologista)
    - Apenas organiza e estrutura o pensamento do usuário

    Args:
        state (MultiAgentState): Estado atual do sistema multi-agente.

    Returns:
        dict: Dicionário com updates incrementais do estado:
            - structurer_output: Dict com elementos extraídos
            - refinement_iteration: Incrementado se modo refinamento
            - current_stage: "validating" (próximo: Metodologista)
            - messages: Mensagem do LLM adicionada ao histórico

    Example:
        >>> # Modo estruturação inicial
        >>> state = create_initial_multi_agent_state("Método X é rápido")
        >>> result = structurer_node(state)
        >>> result['structurer_output']['structured_question']
        'Como método X impacta velocidade?'

        >>> # Modo refinamento
        >>> state['methodologist_output'] = {
        ...     "status": "needs_refinement",
        ...     "improvements": [{"aspect": "população", ...}]
        ... }
        >>> result = structurer_node(state)
        >>> result['refinement_iteration']
        1
    """
    # Carregar prompt e modelo do YAML (Épico 6, Funcionalidade 6.1)
    try:
        system_prompt = get_agent_prompt("structurer")
        model_name = get_agent_model("structurer")
        logger.info("✅ Configurações carregadas do YAML: config/agents/structurer.yaml")
    except ConfigLoadError as e:
        logger.warning(f"⚠️ Falha ao carregar config do structurer: {e}")
        logger.warning("⚠️ Usando prompt e modelo padrão (fallback)")
        # Fallback: prompt hard-coded do YAML como referência
        system_prompt = """Você é um Estruturador que organiza ideias em questões de pesquisa estruturadas.

CONTEXTO:
Você pode operar em dois modos:
1. ESTRUTURAÇÃO INICIAL: Recebe ideia vaga e gera questão V1
2. REFINAMENTO: Recebe feedback do Metodologista e gera versão refinada (V2/V3)

IMPORTANTE: Você é COLABORATIVO, não rejeita ideias, apenas estrutura o pensamento do usuário."""
        model_name = "claude-3-5-haiku-20241022"

    # Passar config para funções auxiliares
    config = {"system_prompt": system_prompt, "model_name": model_name}

    # Detectar modo: estruturação inicial ou refinamento
    methodologist_feedback = state.get('methodologist_output')
    is_refinement_mode = (
        methodologist_feedback is not None and
        methodologist_feedback.get('status') == 'needs_refinement'
    )

    current_iteration = state.get('refinement_iteration', 0)

    if is_refinement_mode:
        logger.info(f"=== NÓ STRUCTURER: Modo REFINAMENTO (Iteração {current_iteration + 1}) ===")
        logger.info(f"Gaps a endereçar: {len(methodologist_feedback['improvements'])}")
        return _refine_question(state, methodologist_feedback, config)
    else:
        logger.info("=== NÓ STRUCTURER: Modo ESTRUTURAÇÃO INICIAL ===")
        logger.info(f"Input do usuário: {state['user_input']}")
        return _structure_initial_question(state, config)


def _structure_initial_question(state: MultiAgentState, config: dict) -> dict:
    """
    Modo estruturação inicial: primeira vez, gera questão V1.

    Args:
        state (MultiAgentState): Estado do sistema.
        config (dict): Configuração com system_prompt e model_name.

    Returns:
        dict: Updates do estado com questão estruturada V1.
    """

    # Extrair config
    system_prompt = config["system_prompt"]
    model_name = config["model_name"]

    # Criar prompt de estruturação usando config do YAML
    structuring_prompt = f"""{system_prompt}

OBSERVAÇÃO DO USUÁRIO:
{state['user_input']}

TAREFA:
Extraia e estruture os seguintes elementos da observação acima:

1. **Contexto**: De onde vem essa observação? Qual é o domínio ou área de aplicação?
2. **Problema**: Qual problema, gap ou fenômeno está sendo observado?
3. **Contribuição potencial**: Como essa observação pode contribuir para academia ou prática?
4. **Questão de pesquisa estruturada**: Transforme a observação em uma questão de pesquisa clara

RESPONDA EM JSON:
{{
    "context": "descrição do contexto da observação",
    "problem": "descrição do problema ou gap identificado",
    "contribution": "possível contribuição acadêmica ou prática",
    "structured_question": "questão de pesquisa estruturada baseada na observação"
}}

IMPORTANTE: Retorne APENAS o JSON, sem texto adicional."""

    # Chamar LLM para estruturação usando modelo do config
    llm = ChatAnthropic(model=model_name, temperature=0)
    messages = [HumanMessage(content=structuring_prompt)]
    response = llm.invoke(messages)

    logger.info(f"Resposta do LLM: {response.content}")

    # Parse da resposta
    try:
        structured_data = extract_json_from_llm_response(response.content)

        context = structured_data.get("context", "Contexto não identificado")
        problem = structured_data.get("problem", "Problema não identificado")
        contribution = structured_data.get("contribution", "Contribuição potencial não identificada")
        structured_question = structured_data.get("structured_question", state['user_input'])

        logger.debug(f"Contexto: {context}")
        logger.debug(f"Problema: {problem}")
        logger.debug(f"Contribuição: {contribution}")
        logger.debug(f"Questão estruturada: {structured_question}")

        # Validar que pelo menos a questão foi gerada
        if not structured_question or structured_question == state['user_input']:
            logger.warning("LLM não gerou questão estruturada diferente do input original. Usando padrão.")
            structured_question = f"Como {state['user_input'].lower().strip('.')} pode ser investigado cientificamente?"

    except json.JSONDecodeError as e:
        logger.error(f"Falha ao parsear JSON da estruturação: {e}. Usando valores padrão.")
        context = "Contexto não identificado devido a erro de parsing"
        problem = "Problema não identificado devido a erro de parsing"
        contribution = "Contribuição não identificada devido a erro de parsing"
        structured_question = f"Como investigar: {state['user_input']}?"

    # Montar output estruturado
    structurer_output = {
        "structured_question": structured_question,
        "elements": {
            "context": context,
            "problem": problem,
            "contribution": contribution
        }
    }

    logger.info(f"Questão estruturada: {structured_question}")
    logger.info(f"Próximo estágio: validating (vai para Metodologista)")
    logger.info("=== NÓ STRUCTURER: Finalizado ===\n")

    # Criar AIMessage com o conteúdo da estruturação para histórico
    ai_message = AIMessage(
        content=f"Questão estruturada: {structured_question}\n\n"
                f"Contexto: {context}\n"
                f"Problema: {problem}\n"
                f"Contribuição potencial: {contribution}"
    )

    return {
        "structurer_output": structurer_output,
        "current_stage": "validating",  # Próximo: Metodologista
        "messages": [ai_message]
    }


def _refine_question(state: MultiAgentState, methodologist_feedback: dict, config: dict) -> dict:
    """
    Modo refinamento: gera versão refinada endereçando gaps do Metodologista (Épico 4).

    Args:
        state (MultiAgentState): Estado do sistema.
        methodologist_feedback (dict): Output do Metodologista com improvements.
        config (dict): Configuração com system_prompt e model_name.

    Returns:
        dict: Updates do estado com questão refinada (V2/V3) e iteration incrementada.
    """
    # Extrair config
    model_name = config["model_name"]
    # Obter questão anterior (da última versão)
    if state.get('hypothesis_versions'):
        last_version = state['hypothesis_versions'][-1]
        previous_question = last_version['question']
        current_version = last_version['version'] + 1
    else:
        # Fallback: usar structurer_output anterior
        previous_question = state['structurer_output']['structured_question']
        current_version = 2  # V1 foi inicial, agora V2

    logger.info(f"Questão anterior (V{current_version - 1}): {previous_question}")

    # Extrair gaps do feedback
    improvements = methodologist_feedback['improvements']
    logger.info(f"Refinando para V{current_version}...")

    # Construir prompt de refinamento
    improvements_str = json.dumps(improvements, ensure_ascii=False, indent=2)

    refinement_prompt = f"""{STRUCTURER_REFINEMENT_PROMPT_V1}

**Input original do usuário:**
{state['user_input']}

**Questão V{current_version - 1} (anterior):**
{previous_question}

**Feedback do Metodologista:**
{{
  "improvements": {improvements_str}
}}

Gere uma versão REFINADA (V{current_version}) que endereça TODOS os gaps listados.
Retorne APENAS JSON com: context, problem, contribution, structured_question, addressed_gaps."""

    # Chamar LLM usando modelo do config
    llm = ChatAnthropic(model=model_name, temperature=0)
    response = llm.invoke([HumanMessage(content=refinement_prompt)])

    logger.info(f"Resposta do LLM: {response.content[:200]}...")

    # Parse da resposta
    try:
        refined_data = extract_json_from_llm_response(response.content)

        context = refined_data.get("context", "Contexto refinado não identificado")
        problem = refined_data.get("problem", "Problema refinado não identificado")
        contribution = refined_data.get("contribution", "Contribuição refinada não identificada")
        structured_question = refined_data.get("structured_question", previous_question)
        addressed_gaps = refined_data.get("addressed_gaps", [])

        logger.debug(f"Questão refinada (V{current_version}): {structured_question}")
        logger.debug(f"Gaps endereçados: {addressed_gaps}")

        # Validar que questão foi refinada
        if structured_question == previous_question:
            logger.warning("LLM retornou mesma questão. Forçando diferenciação.")
            # Adicionar indicação de versão
            structured_question = f"{previous_question} [V{current_version} refinada]"

    except json.JSONDecodeError as e:
        logger.error(f"Falha ao parsear JSON do refinamento: {e}. Usando questão anterior.")
        context = state['structurer_output']['elements']['context']
        problem = state['structurer_output']['elements']['problem']
        contribution = state['structurer_output']['elements']['contribution']
        structured_question = f"{previous_question} [tentativa de refinamento V{current_version}]"
        addressed_gaps = []

    # Montar output refinado
    structurer_output = {
        "structured_question": structured_question,
        "elements": {
            "context": context,
            "problem": problem,
            "contribution": contribution
        },
        "version": current_version,
        "addressed_gaps": addressed_gaps
    }

    # Incrementar refinement_iteration
    new_iteration = state.get('refinement_iteration', 0) + 1

    logger.info(f"Questão refinada V{current_version}: {structured_question}")
    logger.info(f"Iteração de refinamento: {state.get('refinement_iteration', 0)} → {new_iteration}")
    logger.info(f"Gaps endereçados: {addressed_gaps}")
    logger.info("=== NÓ STRUCTURER (Refinamento): Finalizado ===\n")

    # Criar AIMessage
    ai_message = AIMessage(
        content=f"Questão refinada V{current_version}: {structured_question}\n\n"
                f"Gaps endereçados: {', '.join(addressed_gaps)}\n"
                f"Contexto: {context}\n"
                f"Problema: {problem}\n"
                f"Contribuição potencial: {contribution}"
    )

    return {
        "structurer_output": structurer_output,
        "refinement_iteration": new_iteration,
        "current_stage": "validating",  # Volta para Metodologista
        "messages": [ai_message]
    }
