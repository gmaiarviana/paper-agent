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
import time
from typing import Optional
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import RunnableConfig
from langchain_anthropic import ChatAnthropic

from agents.orchestrator.state import MultiAgentState, StructurerOutputModel
from core.utils.json_parser import extract_json_from_llm_response
from core.utils.prompts import STRUCTURER_REFINEMENT_PROMPT_V1
from agents.memory.config_loader import get_agent_prompt, get_agent_model, ConfigLoadError
from agents.memory.execution_tracker import register_execution
from core.utils.token_extractor import extract_tokens_and_cost
from core.utils.structured_logger import StructuredLogger
from core.utils.config import create_anthropic_client, get_anthropic_model

logger = logging.getLogger(__name__)


def structurer_node(state: MultiAgentState, config: Optional[RunnableConfig] = None) -> dict:
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
    - Registra execução no MemoryManager (se configurado - Épico 6.2)

    Args:
        state (MultiAgentState): Estado atual do sistema multi-agente.
        config (RunnableConfig, optional): Configuração do LangGraph (contém memory_manager)

    Returns:
        dict: Dicionário com updates incrementais do estado:
            - structurer_output: Dict com elementos extraídos
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
        model_name = get_anthropic_model()  # Fallback usa modelo centralizado

    # Extrair trace_id do config para logging estruturado
    trace_id = "unknown"
    if config:
        trace_id = config.get("configurable", {}).get("thread_id", "unknown")
    
    # Inicializar logger estruturado
    structured_logger = StructuredLogger()
    
    # Log de início
    start_time = time.time()
    
    # Detectar modo: estruturação inicial ou refinamento
    methodologist_feedback = state.get('methodologist_output')
    is_refinement_mode = (
        methodologist_feedback is not None and
        methodologist_feedback.get('status') == 'needs_refinement'
    )
    
    mode = "refinement" if is_refinement_mode else "initial"
    
    # Calcular versão antecipadamente para metadata
    if is_refinement_mode:
        # Em modo refinamento, calcular versão a partir do state
        if state.get('hypothesis_versions'):
            version = state['hypothesis_versions'][-1]['version'] + 1
        else:
            # Fallback: V1 foi inicial, agora V2
            version = 2
    else:
        # Modo inicial sempre gera V1
        version = 1
    
    structured_logger.log_agent_start(
        trace_id=trace_id,
        agent="structurer",
        node="structurer_node",
        metadata={
            "mode": mode,
            "version": version
        }
    )

    # Passar config para funções auxiliares
    node_config = {"system_prompt": system_prompt, "model_name": model_name, "langgraph_config": config, "trace_id": trace_id, "structured_logger": structured_logger, "start_time": start_time}

    try:
        if is_refinement_mode:
            logger.info("=== NÓ STRUCTURER: Modo REFINAMENTO ===")
            logger.info(f"Gaps a endereçar: {len(methodologist_feedback['improvements'])}")
            result = _refine_question(state, methodologist_feedback, node_config)
        else:
            logger.info("=== NÓ STRUCTURER: Modo ESTRUTURAÇÃO INICIAL ===")
            logger.info(f"Input do usuário: {state['user_input']}")
            result = _structure_initial_question(state, node_config)
        
        # Log de conclusão
        duration_ms = (time.time() - start_time) * 1000
        structurer_output = result.get("structurer_output", {})
        version = structurer_output.get("version", 1)
        
        structured_logger.log_agent_complete(
            trace_id=trace_id,
            agent="structurer",
            node="structurer_node",
            metadata={
                "duration_ms": duration_ms,
                "tokens_input": result.get("last_agent_tokens_input", 0),
                "tokens_output": result.get("last_agent_tokens_output", 0),
                "tokens_total": result.get("last_agent_tokens_input", 0) + result.get("last_agent_tokens_output", 0),
                "cost": result.get("last_agent_cost", 0.0),
                "version": version,
                "mode": mode
            }
        )
        
        return result
        
    except Exception as e:
        # Log de erro antes de raise
        structured_logger.log_error(
            trace_id=trace_id,
            agent="structurer",
            node="structurer_node",
            error=e,
            metadata={"mode": mode, "version": version}
        )
        raise


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
    llm = create_anthropic_client(model=model_name, temperature=0)
    messages = [HumanMessage(content=structuring_prompt)]
    response = llm.invoke(messages)

    logger.info(f"Resposta do LLM: {response.content}")

    # Registrar execução no MemoryManager (Épico 6.2)
    langgraph_config = config.get("langgraph_config")
    if langgraph_config:
        memory_manager = langgraph_config.get("configurable", {}).get("memory_manager")
        if memory_manager:
            register_execution(
                memory_manager=memory_manager,
                config=langgraph_config,
                agent_name="structurer",
                response=response,
                summary="Estruturação V1",
                model_name=model_name,
                extra_metadata={
                    "mode": "initial_structuring",
                    "version": 1
                }
            )

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

    # Montar output estruturado com validação Pydantic
    try:
        output_model = StructurerOutputModel(
            structured_question=structured_question,
            elements={
                "context": context,
                "problem": problem,
                "contribution": contribution,
            },
        )
        structurer_output = output_model.model_dump()
    except Exception as e:  # Falha de validação é improvável, mas fazemos fallback seguro
        logger.error(f"Falha ao validar output do Estruturador via Pydantic: {e}")
        structurer_output = {
            "structured_question": structured_question,
            "elements": {
                "context": context,
                "problem": problem,
                "contribution": contribution,
            },
        }

    # Extrair tokens e custo da resposta (Épico 8.3)
    try:
        logger.debug(f"[TOKEN EXTRACTION] Tentando extrair tokens de response (tipo: {type(response)})")
        metrics = extract_tokens_and_cost(response, model_name)
        logger.debug(f"[TOKEN EXTRACTION] ✅ Métricas extraídas: {metrics['tokens_total']} tokens, ${metrics['cost']:.6f}")
    except Exception as e:
        logger.error(f"[TOKEN EXTRACTION] ❌ Erro ao extrair tokens: {e}")
        import traceback
        traceback.print_exc()
        # Fallback: métricas zeradas
        metrics = {"tokens_input": 0, "tokens_output": 0, "tokens_total": 0, "cost": 0.0}

    # Log de decisão (estruturação inicial - V1 criada)
    structured_logger = config.get("structured_logger")
    trace_id = config.get("trace_id", "unknown")
    if structured_logger:
        structured_logger.log_decision(
            trace_id=trace_id,
            agent="structurer",
            node="structurer_node",
            decision={
                "version": 1,
                "structured_question": structured_question[:100],
                "elements_extracted": list(structurer_output.get("elements", {}).keys())
            },
            reasoning=f"Estruturou observação do usuário em questão V1. Contexto: {context[:50]}... Problema: {problem[:50]}...",
            metadata={
                "tokens_input": metrics.get("tokens_input", 0),
                "tokens_output": metrics.get("tokens_output", 0),
                "tokens_total": metrics.get("tokens_total", 0),
                "cost": metrics.get("cost", 0.0)
            }
        )

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
        "last_agent_tokens_input": metrics["tokens_input"],
        "last_agent_tokens_output": metrics["tokens_output"],
        "last_agent_cost": metrics["cost"],
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
    llm = create_anthropic_client(model=model_name, temperature=0)
    response = llm.invoke([HumanMessage(content=refinement_prompt)])

    logger.info(f"Resposta do LLM: {response.content[:200]}...")

    # Registrar execução no MemoryManager (Épico 6.2)
    langgraph_config = config.get("langgraph_config")
    if langgraph_config:
        memory_manager = langgraph_config.get("configurable", {}).get("memory_manager")
        if memory_manager:
            register_execution(
                memory_manager=memory_manager,
                config=langgraph_config,
                agent_name="structurer",
                response=response,
                summary=f"Refinamento V{current_version}",
                model_name=model_name,
                extra_metadata={
                    "mode": "refinement",
                    "version": current_version,
                    "gaps_count": len(improvements)
                }
            )

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

    # Extrair tokens e custo da resposta (Épico 8.3)
    try:
        logger.debug(f"[TOKEN EXTRACTION] Tentando extrair tokens de response (tipo: {type(response)})")
        metrics = extract_tokens_and_cost(response, model_name)
        logger.debug(f"[TOKEN EXTRACTION] ✅ Métricas extraídas: {metrics['tokens_total']} tokens, ${metrics['cost']:.6f}")
    except Exception as e:
        logger.error(f"[TOKEN EXTRACTION] ❌ Erro ao extrair tokens: {e}")
        import traceback
        traceback.print_exc()
        # Fallback: métricas zeradas
        metrics = {"tokens_input": 0, "tokens_output": 0, "tokens_total": 0, "cost": 0.0}

    # Log de decisão (refinamento - versão refinada criada)
    structured_logger = config.get("structured_logger")
    trace_id = config.get("trace_id", "unknown")
    if structured_logger:
        structured_logger.log_decision(
            trace_id=trace_id,
            agent="structurer",
            node="structurer_node",
            decision={
                "version": current_version,
                "structured_question": structured_question[:100],
                "addressed_gaps": addressed_gaps,
                "gaps_count": len(improvements)
            },
            reasoning=f"Refinou questão para V{current_version} endereçando {len(improvements)} gap(s) do Metodologista: {', '.join(addressed_gaps[:3]) if addressed_gaps else 'nenhum gap específico'}...",
            metadata={
                "tokens_input": metrics.get("tokens_input", 0),
                "tokens_output": metrics.get("tokens_output", 0),
                "tokens_total": metrics.get("tokens_total", 0),
                "cost": metrics.get("cost", 0.0)
            }
        )

    logger.info(f"Questão refinada V{current_version}: {structured_question}")
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
        "current_stage": "validating",  # Volta para Metodologista
        "last_agent_tokens_input": metrics["tokens_input"],
        "last_agent_tokens_output": metrics["tokens_output"],
        "last_agent_cost": metrics["cost"],
        "messages": [ai_message]
    }
