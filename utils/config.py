"""
Configurações centralizadas do sistema e helpers de integração com Anthropic.
"""

import os
import time
import json
import logging
from typing import Optional, Sequence, TypeVar, Callable, Dict, Any
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import BaseMessage

# Carregar variáveis de ambiente
load_dotenv()

logger = logging.getLogger(__name__)

T = TypeVar("T")


class CircuitBreakerOpenError(RuntimeError):
    """Erro lançado quando o circuit breaker da API Anthropic está aberto."""


class _AnthropicCircuitBreaker:
    """
    Circuit breaker simples para chamadas à API Anthropic.

    Estratégia:
    - Incrementa contador em cada falha
    - Reseta contador em sucesso
    - Após 5 falhas consecutivas, entra em estado "aberto"
    - Enquanto aberto, todas as chamadas falham imediatamente com CircuitBreakerOpenError
    """

    def __init__(self, failure_threshold: int = 5) -> None:
        self.failure_threshold = failure_threshold
        self._consecutive_failures = 0
        self._is_open = False

    @property
    def is_open(self) -> bool:
        return self._is_open

    def register_success(self) -> None:
        self._consecutive_failures = 0
        if self._is_open:
            logger.info("✅ Circuit breaker Anthropic fechado após sucesso.")
        self._is_open = False

    def register_failure(self, error: Exception) -> None:
        self._consecutive_failures += 1
        logger.warning(
            "⚠️ Falha em chamada Anthropic (consecutivas=%s, limite=%s, erro=%s)",
            self._consecutive_failures,
            self.failure_threshold,
            error.__class__.__name__,
        )
        if self._consecutive_failures >= self.failure_threshold and not self._is_open:
            self._is_open = True
            logger.error(
                "🚨 Circuit breaker Anthropic aberto após %s falhas consecutivas.",
                self._consecutive_failures,
            )


_anthropic_circuit_breaker = _AnthropicCircuitBreaker()


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


def create_anthropic_client(model: Optional[str] = None, temperature: float = 0) -> ChatAnthropic:
    """
    Cria instância de ChatAnthropic usando configuração centralizada.

    Args:
        model: Nome do modelo. Se None, usa get_anthropic_model().
        temperature: Temperatura a ser usada nas chamadas.

    Returns:
        ChatAnthropic configurado.
    """
    model_name = model or get_anthropic_model()
    return ChatAnthropic(model=model_name, temperature=temperature)


def invoke_with_retry(
    llm: ChatAnthropic,
    messages: Sequence[BaseMessage],
    agent_name: str,
    max_attempts: int = 3,
    base_backoff_seconds: float = 2.0,
    sleep_fn: Callable[[float], None] = time.sleep,
) -> BaseMessage:
    """
    Invoca LLM Anthropic com retry exponencial e circuit breaker.

    Estratégia de retry:
    - Até 3 tentativas
    - Backoff exponencial: 2s, 4s, 8s (base_backoff_seconds * 2**(attempt-1))
    - Registra logs estruturados de erro e retry

    Circuit breaker:
    - Se _anthropic_circuit_breaker.is_open, lança CircuitBreakerOpenError imediatamente
    - Em cada falha, incrementa contador; em sucesso, reseta.
    """
    if _anthropic_circuit_breaker.is_open:
        log_payload: Dict[str, Any] = {
            "event": "anthropic_circuit_breaker_open",
            "agent": agent_name,
        }
        logger.error(json.dumps(log_payload, ensure_ascii=False))
        raise CircuitBreakerOpenError(
            "Circuit breaker da API Anthropic está aberto após falhas consecutivas."
        )

    attempt = 0
    last_error: Optional[Exception] = None

    while attempt < max_attempts:
        attempt += 1
        try:
            logger.debug(
                json.dumps(
                    {
                        "event": "anthropic_call_start",
                        "agent": agent_name,
                        "attempt": attempt,
                        "max_attempts": max_attempts,
                    },
                    ensure_ascii=False,
                )
            )
            response = llm.invoke(list(messages))
            _anthropic_circuit_breaker.register_success()
            logger.debug(
                json.dumps(
                    {
                        "event": "anthropic_call_success",
                        "agent": agent_name,
                        "attempt": attempt,
                    },
                    ensure_ascii=False,
                )
            )
            return response
        except Exception as e:  # noqa: BLE001 - queremos capturar qualquer erro de API
            last_error = e
            _anthropic_circuit_breaker.register_failure(e)

            if attempt >= max_attempts:
                logger.error(
                    json.dumps(
                        {
                            "event": "anthropic_call_failed_permanently",
                            "agent": agent_name,
                            "attempts": attempt,
                            "error_type": e.__class__.__name__,
                            "error_message": str(e),
                        },
                        ensure_ascii=False,
                    )
                )
                break

            backoff = base_backoff_seconds * (2 ** (attempt - 1))
            logger.warning(
                json.dumps(
                    {
                        "event": "anthropic_retry_scheduled",
                        "agent": agent_name,
                        "attempt": attempt,
                        "max_attempts": max_attempts,
                        "backoff_seconds": round(backoff, 1),
                        "error_type": e.__class__.__name__,
                        "error_message": str(e),
                    },
                    ensure_ascii=False,
                )
            )
            sleep_fn(backoff)

    # Se chegou aqui, todas as tentativas falharam
    assert last_error is not None
    raise last_error
