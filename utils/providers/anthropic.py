"""
Provider Anthropic (Claude).

Implementação do provider Anthropic usando langchain-anthropic.
"""

import os
import time
import json
import logging
from typing import Optional, Sequence, Callable, Dict, Any
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import BaseMessage

load_dotenv()

logger = logging.getLogger(__name__)


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


_circuit_breaker = _AnthropicCircuitBreaker()


class AnthropicProvider:
    """Provider para modelos Anthropic (Claude)."""

    @staticmethod
    def get_api_key() -> Optional[str]:
        """Retorna a API key da Anthropic do .env."""
        return os.getenv("ANTHROPIC_API_KEY")

    @staticmethod
    def create_client(
        model: str,
        temperature: float = 0,
        max_tokens: Optional[int] = None
    ) -> ChatAnthropic:
        """
        Cria instância de ChatAnthropic.

        Args:
            model: Nome do modelo (ex: "claude-3-5-haiku-20241022")
            temperature: Temperatura a ser usada nas chamadas
            max_tokens: Número máximo de tokens na resposta

        Returns:
            ChatAnthropic configurado
        """
        kwargs = {"model": model, "temperature": temperature}
        if max_tokens is not None:
            kwargs["max_tokens"] = max_tokens
        return ChatAnthropic(**kwargs)

    @staticmethod
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
        - Backoff exponencial: 2s, 4s, 8s
        - Registra logs estruturados de erro e retry

        Circuit breaker:
        - Se circuit breaker está aberto, lança CircuitBreakerOpenError imediatamente
        - Em cada falha, incrementa contador; em sucesso, reseta.
        """
        if _circuit_breaker.is_open:
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
                _circuit_breaker.register_success()
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
            except Exception as e:  # noqa: BLE001
                last_error = e
                _circuit_breaker.register_failure(e)

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

    @staticmethod
    def supports_model(model: str) -> bool:
        """Verifica se o provider suporta o modelo especificado."""
        return model.startswith("claude-")

