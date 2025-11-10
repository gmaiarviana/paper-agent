"""
Utilitário para extrair e parsear JSON de respostas de LLMs.

Este módulo fornece parsing robusto de JSON que lida com:
- JSON puro
- JSON dentro de markdown code blocks
- JSON com texto adicional
- JSON com formatação e line breaks

Versão: 1.0
Data: 10/11/2025
"""

import json
import re
import logging

logger = logging.getLogger(__name__)


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
