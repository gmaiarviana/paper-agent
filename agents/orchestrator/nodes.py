"""
Nós do grafo do agente Orquestrador.

Este módulo implementa o nó principal do Orquestrador:
- orchestrator_node: Classifica maturidade do input e decide roteamento

Versão: 1.0 (Épico 3, Funcionalidade 3.1)
Data: 11/11/2025
"""

import logging
import json
from langchain_core.messages import HumanMessage, AIMessage
from langchain_anthropic import ChatAnthropic

from .state import MultiAgentState
from utils.json_parser import extract_json_from_llm_response

logger = logging.getLogger(__name__)


def orchestrator_node(state: MultiAgentState) -> dict:
    """
    Nó que classifica a maturidade do input do usuário e decide roteamento.

    Este nó é o ponto de entrada do sistema multi-agente. Ele:
    1. Analisa o input do usuário
    2. Classifica a maturidade da ideia/hipótese
    3. Define o próximo estágio de processamento
    4. Registra reasoning para transparência

    Classificação de Maturidade:
    - "vague": Ideia não estruturada, observação sem contexto claro
              → Próximo: Estruturador
              → Exemplo: "Observei que X é mais rápido"

    - "semi_formed": Hipótese parcial, tem ideia central mas falta especificidade
                     → Próximo: Metodologista
                     → Exemplo: "Método Y melhora desenvolvimento"

    - "complete": Hipótese completa com população, variáveis e métricas
                  → Próximo: Metodologista
                  → Exemplo: "Método Y reduz tempo em 30% em equipes de 2-5 devs"

    Args:
        state (MultiAgentState): Estado atual do sistema multi-agente.

    Returns:
        dict: Dicionário com updates incrementais do estado:
            - orchestrator_classification: Classificação da maturidade
            - orchestrator_reasoning: Justificativa da decisão
            - current_stage: Próximo estágio ("structuring" ou "validating")
            - messages: Mensagem do LLM adicionada ao histórico

    Example:
        >>> state = create_initial_multi_agent_state("Observei que X é rápido")
        >>> result = orchestrator_node(state)
        >>> result['orchestrator_classification']
        'vague'
        >>> result['current_stage']
        'structuring'
    """
    logger.info("=== NÓ ORCHESTRATOR: Iniciando classificação de maturidade ===")
    logger.info(f"Input do usuário: {state['user_input']}")

    # Criar prompt de classificação
    classification_prompt = f"""Você é um Orquestrador que classifica inputs de usuários em sistemas de pesquisa científica.

INPUT DO USUÁRIO:
{state['user_input']}

TAREFA:
Classifique a maturidade deste input segundo os critérios abaixo.

CRITÉRIOS DE CLASSIFICAÇÃO:

1. **"vague"** - Ideia não estruturada:
   - Observação empírica sem contexto claro
   - Falta estruturação em forma de questão de pesquisa
   - Não menciona população, variáveis ou métricas
   - Exemplo: "Observei que desenvolver com IA é mais rápido"

2. **"semi_formed"** - Hipótese parcial:
   - Tem ideia central ou afirmação causal
   - Falta especificidade em população, variáveis ou métricas
   - É uma afirmação, mas não totalmente operacionalizada
   - Exemplo: "Método incremental melhora desenvolvimento de sistemas multi-agente"

3. **"complete"** - Hipótese completa:
   - População/amostra claramente definida
   - Variáveis (dependente/independente) especificadas
   - Métricas e condições mencionadas
   - Testável e falseável
   - Exemplo: "Método incremental reduz tempo em 30% em equipes de 2-5 devs"

RESPONDA EM JSON:
{{
    "classification": "vague" | "semi_formed" | "complete",
    "reasoning": "breve justificativa (1-2 frases) de por que você escolheu essa classificação"
}}

IMPORTANTE: Retorne APENAS o JSON, sem texto adicional."""

    # Chamar LLM para classificação
    llm = ChatAnthropic(model="claude-3-5-haiku-20241022", temperature=0)
    messages = [HumanMessage(content=classification_prompt)]
    response = llm.invoke(messages)

    logger.info(f"Resposta do LLM: {response.content}")

    # Parse da resposta
    try:
        classification_data = extract_json_from_llm_response(response.content)
        classification = classification_data.get("classification", "vague")
        reasoning = classification_data.get("reasoning", "Classificação padrão por falha no parsing")

        # Validar classificação
        valid_classifications = ["vague", "semi_formed", "complete"]
        if classification not in valid_classifications:
            logger.warning(f"Classificação inválida '{classification}'. Usando 'vague' como padrão.")
            classification = "vague"
            reasoning = f"Classificação inválida detectada. Assumindo input vago por segurança."

        logger.debug(f"Classificação parseada: {classification}")
        logger.debug(f"Reasoning: {reasoning}")

    except json.JSONDecodeError as e:
        logger.error(f"Falha ao parsear JSON da classificação: {e}. Usando 'vague' como padrão.")
        classification = "vague"
        reasoning = "Erro ao processar classificação do LLM. Assumindo input vago por segurança."

    # Determinar próximo estágio baseado na classificação
    if classification == "vague":
        next_stage = "structuring"  # Vai para Estruturador
    else:  # semi_formed ou complete
        next_stage = "validating"  # Vai para Metodologista

    logger.info(f"Classificação: {classification}")
    logger.info(f"Próximo estágio: {next_stage}")
    logger.info(f"Reasoning: {reasoning}")
    logger.info("=== NÓ ORCHESTRATOR: Finalizado ===\n")

    # Criar AIMessage com o conteúdo da classificação para histórico
    ai_message = AIMessage(
        content=f"Classificação: {classification}\nReasoning: {reasoning}"
    )

    return {
        "orchestrator_classification": classification,
        "orchestrator_reasoning": reasoning,
        "current_stage": next_stage,
        "messages": [ai_message]
    }
