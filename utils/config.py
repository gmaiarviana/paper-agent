"""
Configurações centralizadas do sistema e helpers de integração com LLM providers.

Suporta múltiplos providers:
- Anthropic (Claude)
- Maritaca AI (Sabiazinho, Sabiá, etc.)
"""

import os
import logging
from typing import Optional, Sequence, TypeVar, Callable, Any, Union
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import BaseMessage

from .providers.anthropic import AnthropicProvider, CircuitBreakerOpenError
from .providers.maritaca import MaritacaProvider

# Carregar variáveis de ambiente
load_dotenv()

logger = logging.getLogger(__name__)

T = TypeVar("T")

# Modelo padrão do sistema (Haiku para economia)
DEFAULT_MODEL = "claude-3-5-haiku-20241022"


# Re-exportar CircuitBreakerOpenError para compatibilidade
# (agora vem de providers.anthropic)


def get_default_model(override: Optional[str] = None) -> str:
    """
    Retorna o modelo padrão a ser usado.

    Args:
        override: Modelo específico para sobrescrever a configuração do .env

    Returns:
        Nome do modelo (ex: "claude-3-5-haiku-20241022")

    Ordem de precedência:
    1. Parâmetro override (se fornecido)
    2. Variável de ambiente LLM_MODEL (genérico) ou ANTHROPIC_MODEL (legado)
    3. Fallback: DEFAULT_MODEL
    """
    if override:
        return override

    # Tentar ler do .env (suporta ambos LLM_MODEL e ANTHROPIC_MODEL para compatibilidade)
    env_model = os.getenv("LLM_MODEL") or os.getenv("ANTHROPIC_MODEL")
    if env_model:
        return env_model

    # Fallback padrão
    return DEFAULT_MODEL


def get_anthropic_model(override: Optional[str] = None) -> str:
    """
    Retorna o modelo Anthropic a ser usado (função legada).

    Mantida para compatibilidade. Use get_default_model() para novos códigos.
    """
    return get_default_model(override)


def get_anthropic_api_key() -> Optional[str]:
    """
    Retorna a API key da Anthropic do .env.

    Returns:
        API key ou None se não configurada
    """
    return os.getenv("ANTHROPIC_API_KEY")


def _detect_provider(model: str):
    """
    Detecta qual provider usar baseado no nome do modelo.

    Args:
        model: Nome do modelo

    Returns:
        Provider apropriado (AnthropicProvider ou MaritacaProvider)
    """
    if AnthropicProvider.supports_model(model):
        return AnthropicProvider
    elif MaritacaProvider.supports_model(model):
        return MaritacaProvider
    else:
        # Fallback para Anthropic se não conseguir detectar
        logger.warning(
            f"Não foi possível detectar provider para modelo '{model}'. "
            f"Usando Anthropic como fallback."
        )
        return AnthropicProvider


def create_llm_client(
    model: Optional[str] = None,
    temperature: float = 0,
    max_tokens: Optional[int] = None
) -> Any:
    """
    Cria instância de cliente LLM usando provider apropriado.

    Detecta automaticamente o provider baseado no nome do modelo:
    - Modelos "claude-*" -> Anthropic
    - Modelos "sabia*" ou "sabiazinho*" -> Maritaca AI

    Args:
        model: Nome do modelo. Se None, usa get_default_model().
        temperature: Temperatura a ser usada nas chamadas.
        max_tokens: Número máximo de tokens na resposta.

    Returns:
        Cliente LLM configurado (ChatAnthropic ou cliente Maritaca)

    Example:
        >>> llm = create_llm_client("claude-3-5-haiku-20241022")
        >>> llm = create_llm_client("sabiazinho-3")  # Quando implementado
    """
    model_name = model or get_default_model()
    provider = _detect_provider(model_name)
    return provider.create_client(model_name, temperature, max_tokens)


def create_anthropic_client(
    model: Optional[str] = None,
    temperature: float = 0,
    max_tokens: Optional[int] = None
) -> ChatAnthropic:
    """
    Cria instância de ChatAnthropic (função legada para compatibilidade).

    Mantida para compatibilidade. Use create_llm_client() para novos códigos.
    """
    model_name = model or get_default_model()
    return AnthropicProvider.create_client(model_name, temperature, max_tokens)


def invoke_with_retry(
    llm: Any,
    messages: Sequence[BaseMessage],
    agent_name: str,
    max_attempts: int = 3,
    base_backoff_seconds: float = 2.0,
    sleep_fn: Optional[Callable[[float], None]] = None,
) -> BaseMessage:
    """
    Invoca LLM com retry exponencial usando provider apropriado.

    Detecta automaticamente o provider baseado no tipo do cliente LLM.
    Suporta Anthropic (com circuit breaker) e outros providers.

    Args:
        llm: Cliente LLM (ChatAnthropic ou outro)
        messages: Mensagens para enviar ao LLM
        agent_name: Nome do agente (para logging)
        max_attempts: Número máximo de tentativas
        base_backoff_seconds: Tempo base de backoff
        sleep_fn: Função de sleep (para testes)

    Returns:
        Resposta do LLM

    Raises:
        CircuitBreakerOpenError: Se circuit breaker Anthropic estiver aberto
    """
    import time as time_module

    if sleep_fn is None:
        sleep_fn = time_module.sleep

    # Detectar provider baseado no tipo do cliente
    # Por enquanto, apenas Anthropic está totalmente implementado
    if isinstance(llm, ChatAnthropic):
        return AnthropicProvider.invoke_with_retry(
            llm, messages, agent_name, max_attempts, base_backoff_seconds, sleep_fn
        )
    else:
        # Para outros providers, usar implementação genérica simples
        # (Maritaca terá sua própria implementação quando pronto)
        attempt = 0
        last_error: Optional[Exception] = None

        while attempt < max_attempts:
            attempt += 1
            try:
                logger.debug(
                    f"Chamada LLM iniciada (provider genérico, attempt={attempt}/{max_attempts})"
                )
                response = llm.invoke(list(messages))
                logger.debug(f"Chamada LLM bem-sucedida (attempt={attempt})")
                return response
            except Exception as e:  # noqa: BLE001
                last_error = e
                if attempt >= max_attempts:
                    logger.error(
                        f"Chamada LLM falhou permanentemente após {attempt} tentativas: {e}"
                    )
                    break

                backoff = base_backoff_seconds * (2 ** (attempt - 1))
                logger.warning(
                    f"Retry agendado em {backoff}s (attempt={attempt}/{max_attempts})"
                )
                sleep_fn(backoff)

        assert last_error is not None
        raise last_error
