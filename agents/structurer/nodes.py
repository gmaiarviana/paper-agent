"""
Nós do grafo do agente Estruturador.

Este módulo implementa o nó principal do Estruturador:
- structurer_node: Organiza ideias vagas em questões de pesquisa estruturadas

Versão: 1.0 (Épico 3, Funcionalidade 3.2)
Data: 11/11/2025
"""

import logging
import json
from langchain_core.messages import HumanMessage, AIMessage
from langchain_anthropic import ChatAnthropic

from agents.orchestrator.state import MultiAgentState
from utils.json_parser import extract_json_from_llm_response

logger = logging.getLogger(__name__)


def structurer_node(state: MultiAgentState) -> dict:
    """
    Nó que organiza ideias vagas em questões de pesquisa estruturadas.

    Este nó recebe observações ou ideias não estruturadas e:
    1. Identifica o contexto da observação
    2. Extrai o problema ou gap observado
    3. Identifica possível contribuição acadêmica/prática
    4. Gera uma questão de pesquisa estruturada

    IMPORTANTE: Este nó é COLABORATIVO:
    - NÃO rejeita ideias
    - NÃO valida rigor científico (isso é responsabilidade do Metodologista)
    - Apenas organiza e estrutura o pensamento do usuário

    Args:
        state (MultiAgentState): Estado atual do sistema multi-agente.

    Returns:
        dict: Dicionário com updates incrementais do estado:
            - structurer_output: Dict com elementos extraídos
                {
                    "structured_question": str,
                    "elements": {
                        "context": str,
                        "problem": str,
                        "contribution": str
                    }
                }
            - current_stage: "validating" (próximo: Metodologista)
            - messages: Mensagem do LLM adicionada ao histórico

    Example:
        >>> state = create_initial_multi_agent_state("Observei que X é rápido")
        >>> result = structurer_node(state)
        >>> result['structurer_output']['structured_question']
        'Em que condições X demonstra maior velocidade?'
        >>> result['current_stage']
        'validating'
    """
    logger.info("=== NÓ STRUCTURER: Iniciando estruturação de ideia vaga ===")
    logger.info(f"Input do usuário: {state['user_input']}")

    # Criar prompt de estruturação
    structuring_prompt = f"""Você é um Estruturador que organiza ideias e observações vagas em questões de pesquisa estruturadas.

OBSERVAÇÃO DO USUÁRIO:
{state['user_input']}

TAREFA:
Extraia e estruture os seguintes elementos da observação acima:

1. **Contexto**: De onde vem essa observação? Qual é o domínio ou área de aplicação?
   - Exemplo: "Desenvolvimento de software com IA", "Educação online", "Gestão de projetos"

2. **Problema**: Qual problema, gap ou fenômeno está sendo observado?
   - Exemplo: "Falta de métodos para medir produtividade", "Dificuldade em engajamento"

3. **Contribuição potencial**: Como essa observação pode contribuir para academia ou prática?
   - Exemplo: "Método para avaliar eficácia de ferramentas IA", "Framework de engajamento"

4. **Questão de pesquisa estruturada**: Transforme a observação em uma questão de pesquisa clara
   - Deve ser uma pergunta bem formulada
   - Não precisa ter todas as variáveis operacionalizadas (isso virá depois)
   - Deve capturar a essência da observação

COMPORTAMENTO ESPERADO:
- Seja COLABORATIVO: ajude a estruturar, não critique
- NÃO valide rigor científico (o Metodologista fará isso depois)
- NÃO rejeite ou julgue a ideia
- Trabalhe com o que foi fornecido, mesmo se incompleto

RESPONDA EM JSON:
{{
    "context": "descrição do contexto da observação",
    "problem": "descrição do problema ou gap identificado",
    "contribution": "possível contribuição acadêmica ou prática",
    "structured_question": "questão de pesquisa estruturada baseada na observação"
}}

IMPORTANTE: Retorne APENAS o JSON, sem texto adicional."""

    # Chamar LLM para estruturação
    llm = ChatAnthropic(model="claude-3-5-haiku-20241022", temperature=0)
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
