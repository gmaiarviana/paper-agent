"""
Configurações centralizadas do sistema.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()


def get_anthropic_model(override: Optional[str] = None) -> str:
    """
    Retorna o modelo Anthropic a ser usado.

    Args:
        override: Modelo específico para sobrescrever a configuração do .env

    Returns:
        Nome do modelo (ex: "claude-3-5-haiku-20241022")

    Ordem de precedência:
    1. Parâmetro override (se fornecido)
    2. Variável de ambiente ANTHROPIC_MODEL
    3. Fallback: claude-3-5-haiku-20241022 (custo-benefício)
    """
    if override:
        return override

    # Tentar ler do .env
    env_model = os.getenv("ANTHROPIC_MODEL")
    if env_model:
        return env_model

    # Fallback padrão
    return "claude-3-5-haiku-20241022"


def get_anthropic_api_key() -> Optional[str]:
    """
    Retorna a API key da Anthropic do .env.

    Returns:
        API key ou None se não configurada
    """
    return os.getenv("ANTHROPIC_API_KEY")
