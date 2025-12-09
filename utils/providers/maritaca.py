"""
Provider Maritaca AI (Sabiazinho, Sabiá, etc.).

Implementação do provider Maritaca AI.
Preparado para uso futuro quando a chave de API for configurada.

Documentação: https://docs.maritaca.ai
"""

import os
import logging
from typing import Optional, Sequence, Callable, Dict, Any
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage

load_dotenv()

logger = logging.getLogger(__name__)


class MaritacaProvider:
    """Provider para modelos Maritaca AI (Sabiazinho, Sabiá, etc.)."""

    @staticmethod
    def get_api_key() -> Optional[str]:
        """Retorna a API key da Maritaca AI do .env."""
        return os.getenv("MARITACA_API_KEY")

    @staticmethod
    def create_client(
        model: str,
        temperature: float = 0,
        max_tokens: Optional[int] = None
    ):
        """
        Cria instância do cliente Maritaca AI.

        Args:
            model: Nome do modelo (ex: "sabiazinho-3", "sabia-3")
            temperature: Temperatura a ser usada nas chamadas
            max_tokens: Número máximo de tokens na resposta

        Returns:
            Cliente LLM configurado

        Raises:
            NotImplementedError: Se a chave de API não estiver configurada
        """
        api_key = MaritacaProvider.get_api_key()
        if not api_key:
            raise NotImplementedError(
                "Maritaca AI não está configurado. "
                "Configure MARITACA_API_KEY no .env para usar modelos Maritaca."
            )

        # TODO: Implementar quando SDK estiver disponível ou usar HTTP client
        # Por enquanto, retorna erro informativo
        raise NotImplementedError(
            f"Provider Maritaca AI ainda não implementado. "
            f"Modelo solicitado: {model}. "
            f"Verifique a documentação em https://docs.maritaca.ai para integração."
        )

    @staticmethod
    def invoke_with_retry(
        llm,
        messages: Sequence[BaseMessage],
        agent_name: str,
        max_attempts: int = 3,
        base_backoff_seconds: float = 2.0,
        sleep_fn: Callable[[float], None] = None,
    ) -> BaseMessage:
        """
        Invoca LLM Maritaca AI com retry exponencial.

        Raises:
            NotImplementedError: Se ainda não implementado
        """
        raise NotImplementedError("Maritaca AI ainda não implementado.")

    @staticmethod
    def supports_model(model: str) -> bool:
        """Verifica se o provider suporta o modelo especificado."""
        return model.startswith("sabia") or model.startswith("sabiazinho")

