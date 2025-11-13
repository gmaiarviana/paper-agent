"""
Nós do grafo do agente Orquestrador.

Este módulo implementa o nó principal do Orquestrador:
- orchestrator_node: Classifica maturidade do input e decide roteamento

Versão: 2.0 (Épico 6, Funcionalidade 6.1 - Config externa)
Data: 13/11/2025
"""

import logging
import json
from langchain_core.messages import HumanMessage, AIMessage
from langchain_anthropic import ChatAnthropic

from .state import MultiAgentState
from utils.json_parser import extract_json_from_llm_response
from utils.config import get_anthropic_model
from agents.memory.config_loader import get_agent_prompt, get_agent_model, ConfigLoadError

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

    # Carregar prompt e modelo do YAML (Épico 6, Funcionalidade 6.1)
    try:
        system_prompt = get_agent_prompt("orchestrator")
        model_name = get_agent_model("orchestrator")
        logger.info("✅ Configurações carregadas do YAML: config/agents/orchestrator.yaml")
    except ConfigLoadError as e:
        logger.warning(f"⚠️ Falha ao carregar config do orchestrator: {e}")
        logger.warning("⚠️ Usando prompt e modelo padrão (fallback)")
        # Fallback: prompt hard-coded
        system_prompt = """Você é o Orquestrador do sistema multi-agente Paper Agent.

SEU PAPEL:
Classificar a maturidade do input do usuário e rotear para o agente apropriado.

CLASSIFICAÇÕES POSSÍVEIS:
1. "vague": Ideia não estruturada, observação casual → encaminhar para Estruturador
2. "semi_formed": Hipótese parcial com alguma estrutura → encaminhar para Metodologista
3. "complete": Hipótese bem formulada e testável → encaminhar para Metodologista

CRITÉRIOS DE CLASSIFICAÇÃO:
- "vague": Apenas observação, sem questão clara, termos vagos
- "semi_formed": Questão de pesquisa presente mas falta especificidade (população, métricas)
- "complete": Questão clara, população definida, métricas especificadas, testável

OUTPUT OBRIGATÓRIO (SEMPRE JSON):
{
  "classification": "vague" | "semi_formed" | "complete",
  "reasoning": "Justificativa específica da classificação"
}

INSTRUÇÕES:
- Analise apenas MATURIDADE do input, não rigor científico
- Seja objetivo: classifique baseado em estrutura presente
- Não faça análise científica profunda (isso é do Metodologista)
- SEMPRE retorne JSON válido"""
        model_name = "claude-3-5-haiku-20241022"

    # Construir prompt completo com input do usuário
    classification_prompt = f"""{system_prompt}

INPUT DO USUÁRIO:
{state['user_input']}

Avalie este input e retorne APENAS JSON com classification e reasoning."""

    # Chamar LLM para classificação
    llm = ChatAnthropic(model=model_name, temperature=0)
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
