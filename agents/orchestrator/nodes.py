"""
Nós do grafo do agente Orquestrador.

Este módulo implementa o nó principal do Orquestrador:
- orchestrator_node: Classifica maturidade do input e decide roteamento

Versão: 2.0 (Épico 6, Funcionalidade 6.1 - Config externa)
Data: 13/11/2025
"""

import logging
import json
from typing import Optional
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import RunnableConfig
from langchain_anthropic import ChatAnthropic

from .state import MultiAgentState
from utils.json_parser import extract_json_from_llm_response
from utils.config import get_anthropic_model
from agents.memory.config_loader import get_agent_prompt, get_agent_model, ConfigLoadError
from agents.memory.execution_tracker import register_execution

logger = logging.getLogger(__name__)


def _build_context(state: MultiAgentState) -> str:
    """
    Constrói contexto completo a partir do histórico de mensagens.

    Esta função helper reconstrói o "argumento focal" implícito da conversa
    analisando todo o histórico de mensagens (user_input + messages).

    O argumento focal é o entendimento atual do sistema sobre:
    - O que o usuário quer fazer (intenção)
    - Contexto compartilhado até agora
    - Direção da conversa

    No POC do Épico 7, o argumento focal é implícito (reconstruído via histórico).
    No Protótipo/MVP, será campo explícito no state.

    Args:
        state (MultiAgentState): Estado atual do sistema multi-agente.

    Returns:
        str: Histórico formatado para análise contextual pelo LLM.
            Formato:
            ```
            INPUT INICIAL DO USUÁRIO:
            {user_input}

            HISTÓRICO DA CONVERSA:
            [Usuário]: {mensagem 1}
            [Assistente]: {resposta 1}
            [Usuário]: {mensagem 2}
            ...
            ```

    Example:
        >>> state = create_initial_multi_agent_state(
        ...     "Observei que LLMs aumentam produtividade",
        ...     "session-123"
        ... )
        >>> context = _build_context(state)
        >>> "INPUT INICIAL DO USUÁRIO" in context
        True
        >>> "Observei que LLMs aumentam produtividade" in context
        True

    Notes:
        - Se não houver mensagens, retorna apenas o input inicial
        - Formato é otimizado para análise contextual pelo LLM
        - Usado pelo orchestrator_node conversacional (Épico 7)

    Technical Details:
        - Lê state['user_input'] como input inicial
        - Lê state['messages'] (gerenciado por LangGraph com add_messages)
        - HumanMessage → "[Usuário]"
        - AIMessage → "[Assistente]"
        - Mantém ordem cronológica (importante para detectar mudanças de direção)
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

    return "\n".join(context_parts)


def orchestrator_node(state: MultiAgentState, config: Optional[RunnableConfig] = None) -> dict:
    """
    Nó conversacional que facilita diálogo adaptativo com o usuário.

    Este nó é o facilitador inteligente do sistema multi-agente (Épico 7 POC). Ele:
    1. Analisa input + histórico completo da conversa
    2. Explora contexto através de perguntas abertas
    3. Sugere próximos passos com justificativas claras
    4. Negocia com o usuário antes de chamar agentes
    5. Detecta mudanças de direção e adapta sem questionar
    6. Registra execução no MemoryManager (se configurado - Épico 6.2)

    MUDANÇA ARQUITETURAL (Épico 7):
    - ANTES: Classificava input (vague/semi_formed/complete) e roteava automaticamente
    - DEPOIS: Conversa, analisa contexto, sugere opções, negocia com usuário

    Comportamento Conversacional:
    - "explore": Fazer perguntas abertas para entender contexto
    - "suggest_agent": Sugerir agente específico com justificativa
    - "clarify": Esclarecer ambiguidade ou contradição detectada

    Args:
        state (MultiAgentState): Estado atual do sistema multi-agente.
        config (RunnableConfig, optional): Configuração do LangGraph (contém memory_manager)

    Returns:
        dict: Dicionário com updates incrementais do estado:
            - orchestrator_analysis: Raciocínio detalhado sobre contexto e histórico
            - next_step: Próxima ação ("explore", "suggest_agent", "clarify")
            - agent_suggestion: Sugestão de agente com justificativa (se next_step="suggest_agent")
            - messages: Mensagem conversacional adicionada ao histórico

    Example:
        >>> state = create_initial_multi_agent_state("Observei que LLMs aumentam produtividade", "session-1")
        >>> result = orchestrator_node(state)
        >>> result['next_step']
        'explore'
        >>> result['orchestrator_analysis']
        'Usuário tem observação mas não especificou contexto...'
    """
    logger.info("=== NÓ ORCHESTRATOR CONVERSACIONAL: Iniciando análise contextual ===")
    logger.info(f"Input do usuário: {state['user_input']}")

    # Usar prompt conversacional do Épico 7
    from utils.prompts import ORCHESTRATOR_CONVERSATIONAL_PROMPT_V1

    # Construir contexto completo (histórico + input atual)
    full_context = _build_context(state)
    logger.info("Contexto construído com histórico completo")
    logger.debug(f"Contexto:\n{full_context}")

    # Construir prompt completo
    conversational_prompt = f"""{ORCHESTRATOR_CONVERSATIONAL_PROMPT_V1}

CONTEXTO DA CONVERSA:
{full_context}

Analise o contexto completo acima e responda APENAS com JSON estruturado conforme especificado."""

    # Chamar LLM para análise conversacional
    # Usar modelo mais potente para raciocínio complexo (Claude Sonnet)
    model_name = "claude-3-5-sonnet-20241022"
    llm = ChatAnthropic(model=model_name, temperature=0)
    messages = [HumanMessage(content=conversational_prompt)]
    response = llm.invoke(messages)

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

    # Parse da resposta JSON
    try:
        orchestrator_response = extract_json_from_llm_response(response.content)

        reasoning = orchestrator_response.get("reasoning", "Raciocínio não fornecido")
        next_step = orchestrator_response.get("next_step", "explore")
        message = orchestrator_response.get("message", "Entendi. Como posso ajudar?")
        agent_suggestion = orchestrator_response.get("agent_suggestion", None)

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

        logger.info(f"Raciocínio: {reasoning[:100]}...")
        logger.info(f"Próximo passo: {next_step}")
        logger.info(f"Mensagem ao usuário: {message[:100]}...")
        if agent_suggestion:
            logger.info(f"Sugestão de agente: {agent_suggestion.get('agent', 'N/A')}")

    except json.JSONDecodeError as e:
        logger.error(f"Falha ao parsear JSON do orquestrador: {e}")
        logger.error(f"Resposta recebida: {response.content[:300]}...")
        # Fallback seguro
        reasoning = "Erro ao processar resposta do orquestrador"
        next_step = "explore"
        message = "Desculpe, tive dificuldade em processar. Pode reformular sua ideia?"
        agent_suggestion = None

    logger.info("=== NÓ ORCHESTRATOR CONVERSACIONAL: Finalizado ===\n")

    # Criar AIMessage com a mensagem conversacional para histórico
    ai_message = AIMessage(content=message)

    return {
        "orchestrator_analysis": reasoning,
        "next_step": next_step,
        "agent_suggestion": agent_suggestion,
        "messages": [ai_message]
    }
