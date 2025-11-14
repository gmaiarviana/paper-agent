"""
Utilitário para extrair e parsear JSON de respostas de LLMs.

Este módulo fornece parsing robusto de JSON que lida com:
- JSON puro
- JSON dentro de markdown code blocks
- JSON com texto adicional
- JSON com formatação e line breaks

Versão: 1.1
Data: 14/11/2025
"""

import json
import re
import logging
from typing import TypedDict, Optional, Literal

logger = logging.getLogger(__name__)


# ============================================================================
# TIPOS PARA ORQUESTRADOR CONVERSACIONAL (Épico 7 POC)
# ============================================================================

class AgentSuggestion(TypedDict):
    """Sugestão de agente retornada pelo Orquestrador."""
    agent: str
    justification: str


class OrchestratorResponse(TypedDict):
    """
    Resposta estruturada do Orquestrador Conversacional.

    Formato esperado pelo Épico 7 POC.
    """
    reasoning: str
    next_step: Literal["explore", "suggest_agent", "clarify"]
    message: str
    agent_suggestion: Optional[AgentSuggestion]


class OrchestratorValidationError(ValueError):
    """Erro de validação de resposta do Orquestrador."""
    pass


def extract_json_from_llm_response(content: str) -> dict:
    """
    Extrai e parseia JSON de resposta do LLM de forma robusta.

    Trata os seguintes casos:
    1. JSON puro
    2. JSON dentro de markdown code blocks (```json ... ```)
    3. JSON com texto adicional antes/depois
    4. JSON com formatação e line breaks (inclusive dentro de strings)

    Args:
        content: Conteúdo da resposta do LLM

    Returns:
        dict: Objeto JSON parseado

    Raises:
        json.JSONDecodeError: Se não conseguir extrair JSON válido

    Example:
        >>> response = '```json\\n{"status": "approved"}\\n```'
        >>> extract_json_from_llm_response(response)
        {'status': 'approved'}
    """
    def try_parse_json(json_str: str) -> dict:
        """Tenta parsear JSON, aplicando correções se necessário."""
        # Tentativa 1: parsing direto
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            pass

        # Tentativa 2: escapar line breaks dentro de strings
        # Regex para encontrar strings JSON e escapar line breaks dentro delas
        try:
            # Remove line breaks dentro de valores de string JSON
            # Procura por padrões como "chave": "valor\ncom quebra"
            fixed = re.sub(
                r':\s*"([^"]*?)"',
                lambda m: ': "' + m.group(1).replace('\n', '\\n') + '"',
                json_str,
                flags=re.DOTALL
            )
            return json.loads(fixed)
        except json.JSONDecodeError:
            pass

        raise json.JSONDecodeError("Não foi possível parsear", json_str, 0)

    # Estratégia 1: Tentar parsing direto do conteúdo completo
    try:
        return try_parse_json(content)
    except json.JSONDecodeError:
        pass

    # Estratégia 2: Extrair JSON de markdown code block
    markdown_pattern = r'```(?:json)?\s*(\{.*?\})\s*```'
    match = re.search(markdown_pattern, content, re.DOTALL)
    if match:
        try:
            return try_parse_json(match.group(1))
        except json.JSONDecodeError:
            pass

    # Estratégia 3: Encontrar primeiro objeto JSON válido no texto
    # Procura por múltiplos { e tenta parsear cada um
    start_idx = 0
    while True:
        start_idx = content.find('{', start_idx)
        if start_idx == -1:
            break

        # Tenta encontrar o JSON completo balanceando chaves
        brace_count = 0
        for i in range(start_idx, len(content)):
            if content[i] == '{':
                brace_count += 1
            elif content[i] == '}':
                brace_count -= 1
                if brace_count == 0:
                    # Encontrou o fim do objeto JSON
                    json_str = content[start_idx:i+1]
                    try:
                        return try_parse_json(json_str)
                    except json.JSONDecodeError:
                        # Tenta o próximo {
                        start_idx += 1
                        break
        else:
            # Não encontrou }, tenta próximo {
            start_idx += 1

    # Se nenhuma estratégia funcionou, lança erro
    raise json.JSONDecodeError(
        f"Não foi possível extrair JSON válido da resposta: {content[:100]}...",
        content,
        0
    )


# ============================================================================
# VALIDAÇÃO ESPECÍFICA DO ORQUESTRADOR
# ============================================================================

def extract_orchestrator_response(content: str) -> OrchestratorResponse:
    """
    Extrai e valida resposta do Orquestrador Conversacional.

    Usa extract_json_from_llm_response internamente para robustez,
    depois valida estrutura e campos específicos do Orquestrador.

    Args:
        content: Conteúdo da resposta do LLM

    Returns:
        OrchestratorResponse: Resposta validada e tipada

    Raises:
        OrchestratorValidationError: Se validação falhar
        json.JSONDecodeError: Se não conseguir extrair JSON válido

    Example:
        >>> response = '''{"reasoning": "...", "next_step": "explore",
        ...               "message": "...", "agent_suggestion": null}'''
        >>> extract_orchestrator_response(response)
        {'reasoning': '...', 'next_step': 'explore', ...}
    """
    # Passo 1: Extrair JSON usando função robusta existente
    try:
        data = extract_json_from_llm_response(content)
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(
            f"Não foi possível extrair JSON da resposta do Orquestrador: {str(e)}",
            content,
            0
        )

    # Passo 2: Validar campos obrigatórios
    required_fields = ["reasoning", "next_step", "message", "agent_suggestion"]
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        raise OrchestratorValidationError(
            f"Campos obrigatórios faltando na resposta do Orquestrador: {', '.join(missing_fields)}"
        )

    # Passo 3: Validar tipos e valores dos campos

    # 3.1: reasoning deve ser string não-vazia
    if not isinstance(data["reasoning"], str):
        raise OrchestratorValidationError(
            f"Campo 'reasoning' deve ser string, recebido: {type(data['reasoning']).__name__}"
        )
    if not data["reasoning"].strip():
        raise OrchestratorValidationError(
            "Campo 'reasoning' não pode ser vazio"
        )

    # 3.2: next_step deve ser um dos valores válidos
    valid_next_steps = ["explore", "suggest_agent", "clarify"]
    if data["next_step"] not in valid_next_steps:
        raise OrchestratorValidationError(
            f"Campo 'next_step' inválido: '{data['next_step']}'. "
            f"Valores válidos: {', '.join(valid_next_steps)}"
        )

    # 3.3: message deve ser string não-vazia
    if not isinstance(data["message"], str):
        raise OrchestratorValidationError(
            f"Campo 'message' deve ser string, recebido: {type(data['message']).__name__}"
        )
    if not data["message"].strip():
        raise OrchestratorValidationError(
            "Campo 'message' não pode ser vazio"
        )

    # 3.4: agent_suggestion deve ser None ou dict com campos específicos
    agent_suggestion = data["agent_suggestion"]

    if agent_suggestion is not None:
        if not isinstance(agent_suggestion, dict):
            raise OrchestratorValidationError(
                f"Campo 'agent_suggestion' deve ser dict ou null, recebido: {type(agent_suggestion).__name__}"
            )

        # Validar campos de agent_suggestion
        if "agent" not in agent_suggestion:
            raise OrchestratorValidationError(
                "Campo 'agent' obrigatório em 'agent_suggestion'"
            )
        if "justification" not in agent_suggestion:
            raise OrchestratorValidationError(
                "Campo 'justification' obrigatório em 'agent_suggestion'"
            )

        # Validar tipos
        if not isinstance(agent_suggestion["agent"], str):
            raise OrchestratorValidationError(
                f"Campo 'agent_suggestion.agent' deve ser string, recebido: {type(agent_suggestion['agent']).__name__}"
            )
        if not isinstance(agent_suggestion["justification"], str):
            raise OrchestratorValidationError(
                f"Campo 'agent_suggestion.justification' deve ser string, recebido: {type(agent_suggestion['justification']).__name__}"
            )

        # Validar não-vazios
        if not agent_suggestion["agent"].strip():
            raise OrchestratorValidationError(
                "Campo 'agent_suggestion.agent' não pode ser vazio"
            )
        if not agent_suggestion["justification"].strip():
            raise OrchestratorValidationError(
                "Campo 'agent_suggestion.justification' não pode ser vazio"
            )

    # Passo 4: Retornar resposta validada (TypedDict)
    return OrchestratorResponse(
        reasoning=data["reasoning"],
        next_step=data["next_step"],
        message=data["message"],
        agent_suggestion=agent_suggestion
    )
