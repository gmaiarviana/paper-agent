"""
Validador de schema para arquivos de configuração de agentes (Épico 6).

Este módulo valida que arquivos YAML de configuração de agentes
seguem o schema esperado com todos os campos obrigatórios.

Versão: 1.0
Data: 12/11/2025
"""

from typing import Dict, Any, List, Optional


# Schema esperado para configurações de agentes
AGENT_CONFIG_SCHEMA = {
    "required_fields": [
        "prompt",           # System prompt do agente
        "tags",             # Lista de tags para categorização
        "context_limits",   # Limites de tokens
        "model",            # Modelo LLM a ser usado
        "metadata"          # Metadados do agente
    ],
    "context_limits_fields": [
        "max_input_tokens",
        "max_output_tokens",
        "max_total_tokens"
    ],
    "metadata_fields": [
        "version",
        "epic",
        "created_at",
        "description"
    ]
}


class ConfigValidationError(Exception):
    """Exceção levantada quando configuração de agente é inválida."""
    pass


def validate_agent_config_schema(config: Dict[str, Any], agent_name: str) -> None:
    """
    Valida que configuração de agente segue o schema esperado.

    Args:
        config (Dict[str, Any]): Configuração carregada do YAML
        agent_name (str): Nome do agente (para mensagens de erro)

    Raises:
        ConfigValidationError: Se configuração for inválida

    Example:
        >>> config = {
        ...     "prompt": "System prompt...",
        ...     "tags": ["orchestrator"],
        ...     "context_limits": {
        ...         "max_input_tokens": 4000,
        ...         "max_output_tokens": 1000,
        ...         "max_total_tokens": 5000
        ...     },
        ...     "model": "claude-3-5-haiku-20241022",
        ...     "metadata": {
        ...         "version": "1.0",
        ...         "epic": "6",
        ...         "created_at": "2025-11-12",
        ...         "description": "Descrição"
        ...     }
        ... }
        >>> validate_agent_config_schema(config, "orchestrator")  # OK
    """
    # Validar campos obrigatórios de nível superior
    missing_fields = []
    for field in AGENT_CONFIG_SCHEMA["required_fields"]:
        if field not in config:
            missing_fields.append(field)

    if missing_fields:
        raise ConfigValidationError(
            f"Configuração do agente '{agent_name}' inválida: "
            f"campos obrigatórios faltando: {', '.join(missing_fields)}"
        )

    # Validar campo 'prompt'
    if not isinstance(config["prompt"], str) or not config["prompt"].strip():
        raise ConfigValidationError(
            f"Configuração do agente '{agent_name}' inválida: "
            f"campo 'prompt' deve ser uma string não-vazia"
        )

    # Validar campo 'tags'
    if not isinstance(config["tags"], list) or len(config["tags"]) == 0:
        raise ConfigValidationError(
            f"Configuração do agente '{agent_name}' inválida: "
            f"campo 'tags' deve ser uma lista não-vazia"
        )

    # Validar campo 'model'
    if not isinstance(config["model"], str) or not config["model"].strip():
        raise ConfigValidationError(
            f"Configuração do agente '{agent_name}' inválida: "
            f"campo 'model' deve ser uma string não-vazia"
        )

    # Validar estrutura de 'context_limits'
    if not isinstance(config["context_limits"], dict):
        raise ConfigValidationError(
            f"Configuração do agente '{agent_name}' inválida: "
            f"campo 'context_limits' deve ser um dicionário"
        )

    missing_context_fields = []
    for field in AGENT_CONFIG_SCHEMA["context_limits_fields"]:
        if field not in config["context_limits"]:
            missing_context_fields.append(field)

    if missing_context_fields:
        raise ConfigValidationError(
            f"Configuração do agente '{agent_name}' inválida: "
            f"campos obrigatórios faltando em 'context_limits': {', '.join(missing_context_fields)}"
        )

    # Validar que valores de context_limits são inteiros positivos
    for field in AGENT_CONFIG_SCHEMA["context_limits_fields"]:
        value = config["context_limits"][field]
        if not isinstance(value, int) or value <= 0:
            raise ConfigValidationError(
                f"Configuração do agente '{agent_name}' inválida: "
                f"campo 'context_limits.{field}' deve ser um inteiro positivo (valor: {value})"
            )

    # Validar estrutura de 'metadata'
    if not isinstance(config["metadata"], dict):
        raise ConfigValidationError(
            f"Configuração do agente '{agent_name}' inválida: "
            f"campo 'metadata' deve ser um dicionário"
        )

    missing_metadata_fields = []
    for field in AGENT_CONFIG_SCHEMA["metadata_fields"]:
        if field not in config["metadata"]:
            missing_metadata_fields.append(field)

    if missing_metadata_fields:
        raise ConfigValidationError(
            f"Configuração do agente '{agent_name}' inválida: "
            f"campos obrigatórios faltando em 'metadata': {', '.join(missing_metadata_fields)}"
        )

    # Validar que campos de metadata são strings não-vazias
    for field in AGENT_CONFIG_SCHEMA["metadata_fields"]:
        value = config["metadata"][field]
        if not isinstance(value, str) or not value.strip():
            raise ConfigValidationError(
                f"Configuração do agente '{agent_name}' inválida: "
                f"campo 'metadata.{field}' deve ser uma string não-vazia"
            )


def get_schema_documentation() -> str:
    """
    Retorna documentação do schema esperado para configurações de agentes.

    Returns:
        str: Documentação formatada do schema

    Example:
        >>> print(get_schema_documentation())
        Schema de Configuração de Agentes
        ...
    """
    doc = """
Schema de Configuração de Agentes (Épico 6)
============================================

Campos obrigatórios de nível superior:
--------------------------------------
- prompt (string): System prompt do agente
- tags (list): Lista de tags para categorização
- context_limits (dict): Limites de tokens
- model (string): Modelo LLM a ser usado
- metadata (dict): Metadados do agente

Estrutura de 'context_limits':
------------------------------
- max_input_tokens (int): Máximo de tokens de entrada
- max_output_tokens (int): Máximo de tokens de saída
- max_total_tokens (int): Máximo total por chamada

Estrutura de 'metadata':
-----------------------
- version (string): Versão da configuração
- epic (string): Épico que criou/modificou
- created_at (string): Data de criação (YYYY-MM-DD)
- description (string): Descrição do agente

Exemplo de arquivo YAML válido:
-------------------------------
prompt: |
  Você é um agente...

tags:
  - orchestrator
  - router

context_limits:
  max_input_tokens: 4000
  max_output_tokens: 1000
  max_total_tokens: 5000

model: claude-3-5-haiku-20241022

metadata:
  version: "1.0"
  epic: "6"
  created_at: "2025-11-12"
  description: "Descrição do agente"
"""
    return doc.strip()
