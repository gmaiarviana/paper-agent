"""
Nós do grafo do agente Orquestrador.

Este módulo implementa o nó principal do Orquestrador:
- orchestrator_node: Facilitador conversacional MVP com argumento focal explícito
- _build_context: Constrói contexto incluindo outputs de agentes para curadoria

Versão: 5.1 (Épico 9.2 - active_idea_id via config)
Data: 05/12/2025
"""

import logging
import json
from typing import Optional, Dict, Any
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import RunnableConfig
from langchain_anthropic import ChatAnthropic
from pydantic import ValidationError

from .state import MultiAgentState
from utils.json_parser import extract_json_from_llm_response
from utils.config import get_anthropic_model, invoke_with_retry
from agents.memory.config_loader import get_agent_prompt, get_agent_model, ConfigLoadError
from agents.memory.execution_tracker import register_execution
from utils.token_extractor import extract_tokens_and_cost
from agents.models.cognitive_model import CognitiveModel

logger = logging.getLogger(__name__)


def _create_fallback_cognitive_model(state: MultiAgentState) -> Dict[str, Any]:
    """
    Cria cognitive_model de fallback quando LLM não retorna ou retorna inválido.

    Usa o user_input para criar um modelo mínimo.

    Args:
        state: Estado atual do sistema

    Returns:
        Dict com cognitive_model mínimo válido
    """
    user_input = state.get("user_input", "")

    return {
        "claim": user_input[:200] if user_input else "",
        "premises": [],
        "assumptions": [],
        "open_questions": ["O que você quer explorar sobre isso?"],
        "contradictions": [],
        "solid_grounds": [],
        "context": {}
    }


def _validate_cognitive_model(
    cognitive_model_raw: Optional[Dict[str, Any]],
    state: MultiAgentState
) -> Dict[str, Any]:
    """
    Valida cognitive_model usando schema Pydantic e retorna dict válido.

    Esta função:
    1. Se cognitive_model_raw for None, cria fallback
    2. Valida contra schema CognitiveModel (Pydantic)
    3. Se validação falhar, loga erro e cria fallback
    4. Retorna dict (não instância Pydantic) para compatibilidade com state

    Args:
        cognitive_model_raw: Dict extraído do JSON do LLM (pode ser None)
        state: Estado atual do sistema (para criar fallback)

    Returns:
        Dict[str, Any]: cognitive_model validado como dict

    Example:
        >>> raw = {"claim": "LLMs aumentam produtividade", "premises": [], ...}
        >>> validated = _validate_cognitive_model(raw, state)
        >>> validated["claim"]
        'LLMs aumentam produtividade'
    """
    # Se não veio cognitive_model, cria fallback
    if not cognitive_model_raw:
        logger.warning("cognitive_model não fornecido pelo LLM. Usando fallback.")
        return _create_fallback_cognitive_model(state)

    # Tentar validar com Pydantic
    try:
        # Garantir que contradictions tenha estrutura correta
        # LLM pode retornar contradictions vazio como [] ou com items sem confidence
        contradictions = cognitive_model_raw.get("contradictions", [])
        validated_contradictions = []
        for c in contradictions:
            if isinstance(c, dict):
                # Garantir confidence >= 0.80 (regra do schema)
                confidence = c.get("confidence", 0.85)
                if confidence >= 0.80:
                    validated_contradictions.append({
                        "description": c.get("description", ""),
                        "confidence": confidence,
                        "suggested_resolution": c.get("suggested_resolution")
                    })

        # Construir dict para validação
        model_dict = {
            "claim": cognitive_model_raw.get("claim", ""),
            "premises": cognitive_model_raw.get("premises", []),
            "assumptions": cognitive_model_raw.get("assumptions", []),
            "open_questions": cognitive_model_raw.get("open_questions", []),
            "contradictions": validated_contradictions,
            "solid_grounds": cognitive_model_raw.get("solid_grounds", []),
            "context": cognitive_model_raw.get("context", {})
        }

        # Validar com Pydantic
        validated_model = CognitiveModel.model_validate(model_dict)
        logger.info(f"✅ cognitive_model validado: claim={validated_model.claim[:50]}...")

        # Retornar como dict para compatibilidade com TypedDict state
        return validated_model.model_dump()

    except ValidationError as e:
        logger.error(f"❌ Falha na validação do cognitive_model: {e}")
        logger.warning("Usando cognitive_model fallback.")
        return _create_fallback_cognitive_model(state)
    except Exception as e:
        logger.error(f"❌ Erro inesperado ao validar cognitive_model: {e}")
        return _create_fallback_cognitive_model(state)


def _build_context(state: MultiAgentState) -> str:
    """
    Constrói contexto completo para o Orquestrador, incluindo outputs de agentes.

    Esta função helper constrói o contexto que será enviado ao LLM, incluindo:
    - Input inicial do usuário
    - Histórico de mensagens da conversa
    - Outputs de agentes (para curadoria - Épico 1.1)

    Quando structurer_output ou methodologist_output existem no state,
    o Orquestrador está em MODO CURADORIA e deve apresentar o resultado
    ao usuário de forma coesa.

    Args:
        state (MultiAgentState): Estado atual do sistema multi-agente.

    Returns:
        str: Contexto formatado para análise pelo LLM.
            Formato:
            ```
            INPUT INICIAL DO USUÁRIO:
            {user_input}

            HISTÓRICO DA CONVERSA:
            [Usuário]: {mensagem 1}
            [Assistente]: {resposta 1}
            ...

            RESULTADO DO ESTRUTURADOR (você deve fazer curadoria):
            {structurer_output em JSON}

            RESULTADO DO METODOLOGISTA (você deve fazer curadoria):
            {methodologist_output em JSON}
            ```

    Example:
        >>> state = create_initial_multi_agent_state("Observei X", "session-123")
        >>> context = _build_context(state)
        >>> "INPUT INICIAL DO USUÁRIO" in context
        True

        >>> # Com output de agente (modo curadoria)
        >>> state['structurer_output'] = {"research_question": "Como X impacta Y?"}
        >>> context = _build_context(state)
        >>> "RESULTADO DO ESTRUTURADOR" in context
        True

    Notes:
        - Se não houver mensagens, retorna apenas o input inicial
        - Se houver outputs de agentes, Orquestrador deve fazer curadoria
        - Formato é otimizado para análise contextual pelo LLM
    """
    # Input inicial do usuário
    context_parts = [
        "INPUT INICIAL DO USUÁRIO:",
        state["user_input"],
        ""  # linha em branco
    ]

    # Histórico de mensagens (se houver)
    messages = state.get("messages", [])
    if messages:
        context_parts.append("HISTÓRICO DA CONVERSA:")

        for msg in messages:
            # Identificar tipo de mensagem
            if hasattr(msg, '__class__'):
                msg_type = msg.__class__.__name__
            else:
                msg_type = "Unknown"

            # Formatar conforme tipo
            if msg_type == "HumanMessage":
                context_parts.append(f"[Usuário]: {msg.content}")
            elif msg_type == "AIMessage":
                context_parts.append(f"[Assistente]: {msg.content}")
            else:
                # Fallback para outros tipos de mensagem
                context_parts.append(f"[{msg_type}]: {msg.content}")

        context_parts.append("")  # linha em branco final

    # Output do Estruturador (se existir - Épico 1.1 Curadoria)
    structurer_output = state.get("structurer_output")
    if structurer_output:
        context_parts.append("RESULTADO DO ESTRUTURADOR (você deve fazer curadoria):")
        context_parts.append(json.dumps(structurer_output, indent=2, ensure_ascii=False))
        context_parts.append("")

    # Output do Metodologista (se existir - Épico 1.1 Curadoria)
    methodologist_output = state.get("methodologist_output")
    if methodologist_output:
        context_parts.append("RESULTADO DO METODOLOGISTA (você deve fazer curadoria):")
        context_parts.append(json.dumps(methodologist_output, indent=2, ensure_ascii=False))
        context_parts.append("")

    return "\n".join(context_parts)


def orchestrator_node(state: MultiAgentState, config: Optional[RunnableConfig] = None) -> dict:
    """
    Nó socrático que facilita diálogo provocativo com exposição de assumptions implícitas.

    Este nó é o facilitador inteligente do sistema multi-agente (Épico 7 MVP). Ele:
    1. Analisa input + histórico completo da conversa
    2. Extrai e atualiza ARGUMENTO FOCAL explícito a cada turno (7.8)
    3. Explora contexto através de perguntas abertas
    4. Provoca REFLEXÃO sobre lacunas quando relevante (7.9)
    5. Detecta EMERGÊNCIA de novo estágio naturalmente (7.10)
    6. Sugere próximos passos com justificativas claras
    7. Negocia com o usuário antes de chamar agentes
    8. Detecta mudanças de direção comparando focal_argument (7.8)
    9. Registra execução no MemoryManager (se configurado - Épico 6.2)

    NOVIDADES MVP (Épico 7.8-7.10):
    - focal_argument: Campo explícito extraído a cada turno (intent, subject, population, metrics, article_type)
    - reflection_prompt: Provocação de reflexão quando lacuna clara detectada
    - stage_suggestion: Sugestão emergente quando estágio evolui (exploration → hypothesis)

    Comportamento Conversacional:
    - "explore": Fazer perguntas abertas para entender contexto
    - "suggest_agent": Sugerir agente específico com justificativa
    - "clarify": Esclarecer ambiguidade ou contradição detectada

    Args:
        state (MultiAgentState): Estado atual do sistema multi-agente.
        config (RunnableConfig, optional): Configuração do LangGraph.
            Campos suportados em config["configurable"]:
            - memory_manager: MemoryManager para tracking de tokens (Épico 6.2)
            - active_idea_id: UUID da ideia ativa para persistência (Épico 9.2)

    Returns:
        dict: Dicionário com updates incrementais do estado:
            - orchestrator_analysis: Raciocínio detalhado sobre contexto e histórico
            - focal_argument: Argumento focal extraído/atualizado (OBRIGATÓRIO)
            - cognitive_model: Modelo cognitivo do argumento (Épico 9.1 - OBRIGATÓRIO)
            - next_step: Próxima ação ("explore", "suggest_agent", "clarify")
            - agent_suggestion: Sugestão de agente com justificativa (se next_step="suggest_agent")
            - reflection_prompt: Provocação de reflexão (se lacuna detectada)
            - stage_suggestion: Sugestão de mudança de estágio (se evolução detectada)
            - messages: Mensagem conversacional adicionada ao histórico

    Example:
        >>> state = create_initial_multi_agent_state("Observei que LLMs aumentam produtividade", "session-1")
        >>> result = orchestrator_node(state)
        >>> result['focal_argument']['intent']
        'unclear'
        >>> result['focal_argument']['subject']
        'LLMs impact on productivity'
        >>> result['next_step']
        'explore'
    """
    logger.info("=== NÓ ORCHESTRATOR SOCRÁTICO: Iniciando análise contextual (Épico 10) ===")
    logger.info(f"Input do usuário: {state['user_input']}")

    # Verificar se já existe argumento focal anterior (para detectar mudança de direção)
    previous_focal = state.get("focal_argument")
    if previous_focal:
        logger.info(f"Argumento focal anterior: intent={previous_focal.get('intent')}, subject={previous_focal.get('subject')}")

    # Usar prompt socrático do Épico 10
    from utils.prompts import ORCHESTRATOR_SOCRATIC_PROMPT_V1

    # Construir contexto completo (histórico + input atual)
    full_context = _build_context(state)
    logger.info("Contexto construído com histórico completo")
    logger.debug(f"Contexto:\n{full_context}")

    # Adicionar argumento focal anterior ao contexto (se existir)
    focal_context = ""
    if previous_focal:
        focal_context = f"""
ARGUMENTO FOCAL ANTERIOR:
{json.dumps(previous_focal, indent=2, ensure_ascii=False)}

(Compare com novo input para detectar mudança de direção)
"""

    # Construir prompt completo
    conversational_prompt = f"""{ORCHESTRATOR_SOCRATIC_PROMPT_V1}

CONTEXTO DA CONVERSA:
{full_context}
{focal_context}
Analise o contexto completo acima e responda APENAS com JSON estruturado conforme especificado."""

    # Chamar LLM para análise conversacional
    # DECISÃO: Tentar usar modelo mais potente para raciocínio complexo (Épico 7)
    # Fallback: Se não disponível, usa modelo do YAML (config/agents/orchestrator.yaml)
    # Razão: Análise contextual complexa requer raciocínio avançado
    #        (detecção de mudança de direção, reconstrução de argumento focal)
    try:
        # Tentar carregar modelo do YAML primeiro (mais flexível)
        model_name = get_agent_model("orchestrator")
        logger.info(f"Usando modelo do YAML: {model_name}")
    except ConfigLoadError:
        # Fallback: modelo padrão Haiku (mais econômico e sempre disponível)
        model_name = "claude-3-5-haiku-20241022"
        logger.warning(f"Config YAML não disponível. Usando fallback: {model_name}")

    llm = ChatAnthropic(model=model_name, temperature=0)
    messages = [HumanMessage(content=conversational_prompt)]
    response = invoke_with_retry(llm=llm, messages=messages, agent_name="orchestrator")

    logger.info(f"Resposta do LLM (primeiros 200 chars): {response.content[:200]}...")

    # Registrar execução no MemoryManager (Épico 6.2)
    if config:
        memory_manager = config.get("configurable", {}).get("memory_manager")
        if memory_manager:
            # Extrair next_step antes de registrar (será usada no summary)
            try:
                temp_data = extract_json_from_llm_response(response.content)
                temp_next_step = temp_data.get("next_step", "unknown")
            except:
                temp_next_step = "unknown"

            register_execution(
                memory_manager=memory_manager,
                config=config,
                agent_name="orchestrator",
                response=response,
                summary=f"Próximo passo: {temp_next_step}",
                model_name=model_name,
                extra_metadata={
                    "next_step": temp_next_step,
                    "context_length": len(full_context)
                }
            )

    # Extrair active_idea_id do config (Épico 9.2)
    # Usado pelo SnapshotManager para persistência (Épico 9.3)
    active_idea_id = None
    if config:
        active_idea_id = config.get("configurable", {}).get("active_idea_id")
        if active_idea_id:
            logger.info(f"📝 Processando ideia: {active_idea_id[:8]}...")
        else:
            logger.debug("active_idea_id não fornecido no config (opcional)")

    # Parse da resposta JSON
    try:
        orchestrator_response = extract_json_from_llm_response(response.content)

        reasoning = orchestrator_response.get("reasoning", "Raciocínio não fornecido")
        focal_argument = orchestrator_response.get("focal_argument")
        cognitive_model_raw = orchestrator_response.get("cognitive_model")
        next_step = orchestrator_response.get("next_step", "explore")
        message = orchestrator_response.get("message", "Entendi. Como posso ajudar?")
        agent_suggestion = orchestrator_response.get("agent_suggestion", None)
        reflection_prompt = orchestrator_response.get("reflection_prompt", None)
        stage_suggestion = orchestrator_response.get("stage_suggestion", None)

        # Validar e processar cognitive_model (Épico 9.1 - OBRIGATÓRIO)
        cognitive_model_dict = _validate_cognitive_model(cognitive_model_raw, state)

        # Validar focal_argument (OBRIGATÓRIO no MVP)
        if not focal_argument:
            logger.error("ERRO: focal_argument é obrigatório no MVP mas não foi fornecido pelo LLM!")
            # Fallback: criar focal_argument mínimo
            focal_argument = {
                "intent": "unclear",
                "subject": "not specified",
                "population": "not specified",
                "metrics": "not specified",
                "article_type": "unclear"
            }
            logger.warning(f"Usando focal_argument fallback: {focal_argument}")

        # Validar next_step
        valid_next_steps = ["explore", "suggest_agent", "clarify"]
        if next_step not in valid_next_steps:
            logger.warning(f"next_step inválido '{next_step}'. Usando 'explore' como padrão.")
            next_step = "explore"

        # Validar consistência: se next_step="suggest_agent", agent_suggestion deve existir
        if next_step == "suggest_agent" and not agent_suggestion:
            logger.warning("next_step='suggest_agent' mas agent_suggestion é None. Mudando para 'explore'.")
            next_step = "explore"
            message = "Preciso entender melhor o contexto. Me conta mais sobre sua ideia?"

        # Detectar mudança de direção (7.8)
        if previous_focal and focal_argument:
            prev_intent = previous_focal.get('intent')
            new_intent = focal_argument.get('intent')
            if prev_intent and new_intent and prev_intent != new_intent and prev_intent != 'unclear' and new_intent != 'unclear':
                logger.info(f"🔄 MUDANÇA DE DIREÇÃO DETECTADA: {prev_intent} → {new_intent}")

        # Logs MVP
        logger.info(f"Raciocínio: {reasoning[:100]}...")
        logger.info(f"Argumento focal: intent={focal_argument.get('intent')}, subject={focal_argument.get('subject', 'N/A')[:50]}")
        logger.info(f"🧠 Modelo cognitivo: claim={cognitive_model_dict.get('claim', 'N/A')[:50]}...")
        logger.info(f"Próximo passo: {next_step}")
        logger.info(f"Mensagem ao usuário: {message[:100]}...")
        if agent_suggestion:
            logger.info(f"Sugestão de agente: {agent_suggestion.get('agent', 'N/A')}")
        if reflection_prompt:
            logger.info(f"💭 Provocação de reflexão: {reflection_prompt[:80]}...")
        if stage_suggestion:
            logger.info(f"🎯 Sugestão de estágio: {stage_suggestion.get('from_stage')} → {stage_suggestion.get('to_stage')}")

    except json.JSONDecodeError as e:
        logger.error(f"Falha ao parsear JSON do orquestrador: {e}")
        logger.error(f"Resposta recebida: {response.content[:300]}...")
        # Fallback seguro
        reasoning = "Erro ao processar resposta do orquestrador"
        focal_argument = {
            "intent": "unclear",
            "subject": "not specified",
            "population": "not specified",
            "metrics": "not specified",
            "article_type": "unclear"
        }
        cognitive_model_dict = _create_fallback_cognitive_model(state)
        next_step = "explore"
        message = "Desculpe, tive dificuldade em processar. Pode reformular sua ideia?"
        agent_suggestion = None
        reflection_prompt = None
        stage_suggestion = None

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

    logger.info("=== NÓ ORCHESTRATOR SOCRÁTICO: Finalizado ===\n")

    # Criar AIMessage com a mensagem conversacional para histórico
    ai_message = AIMessage(content=message)

    return {
        "orchestrator_analysis": reasoning,
        "focal_argument": focal_argument,
        "cognitive_model": cognitive_model_dict,
        "next_step": next_step,
        "agent_suggestion": agent_suggestion,
        "reflection_prompt": reflection_prompt,
        "stage_suggestion": stage_suggestion,
        "last_agent_tokens_input": metrics["tokens_input"],
        "last_agent_tokens_output": metrics["tokens_output"],
        "last_agent_cost": metrics["cost"],
        "messages": [ai_message]
    }
