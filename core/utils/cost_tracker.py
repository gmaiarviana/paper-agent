"""
Cost tracking utility for Anthropic API usage.

Calculates costs based on token usage and model pricing.
Pricing information: https://www.anthropic.com/pricing
"""

import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class CostTracker:
    """
    Tracks and calculates costs for Anthropic API calls.

    Supports multiple Claude models with their respective pricing tiers.
    """

    # Pricing in USD per 1M tokens.
    # Ver https://www.anthropic.com/pricing — confirmar antes de reportar custo em produção.
    PRICING = {
        # Claude 3 family
        "claude-3-5-haiku-20241022": {"input": 0.80, "output": 4.00},
        "claude-3-haiku-20240307": {"input": 0.25, "output": 1.25},
        "claude-3-5-sonnet-20240620": {"input": 3.00, "output": 15.00},
        "claude-3-5-sonnet-20241022": {"input": 3.00, "output": 15.00},
        "claude-3-opus-20240229": {"input": 15.00, "output": 75.00},
        # Claude 4 family — validar valores em https://www.anthropic.com/pricing
        "claude-haiku-4-5-20251001": {"input": 1.00, "output": 5.00},
        "claude-sonnet-4-0": {"input": 3.00, "output": 15.00},
        "claude-sonnet-4-5": {"input": 3.00, "output": 15.00},
        "claude-sonnet-4-6": {"input": 3.00, "output": 15.00},
        "claude-opus-4-6": {"input": 15.00, "output": 75.00},
        "claude-opus-4-7": {"input": 15.00, "output": 75.00},
    }

    # Aliases ou nomes alternativos que mapeiam para o mesmo tier de preço.
    # Evita ValueError quando o provider aceita um formato curto do modelo.
    _ALIASES = {
        "claude-sonnet-4": "claude-sonnet-4-0",
        "claude-haiku-4": "claude-haiku-4-5-20251001",
    }

    @classmethod
    def _resolve_pricing(cls, model: str) -> Optional[Dict[str, float]]:
        if model in cls.PRICING:
            return cls.PRICING[model]
        alias_target = cls._ALIASES.get(model)
        if alias_target and alias_target in cls.PRICING:
            return cls.PRICING[alias_target]
        # Match por prefixo: heurística para variantes versionadas (ex.: "-20250601")
        # que não foram catalogadas explicitamente mas pertencem a uma família conhecida.
        for known, pricing in cls.PRICING.items():
            base = known.rsplit("-", 1)[0]
            if base and model.startswith(base):
                return pricing
        return None

    @classmethod
    def calculate_cost(
        cls,
        model: str,
        input_tokens: int,
        output_tokens: int,
    ) -> Dict[str, float]:
        """
        Calculate cost for an API call.

        Quando ``model`` não está mapeado em ``PRICING`` (nem por alias, nem por
        prefixo), retorna custo zero e loga um warning — o custo é métrica
        secundária e não deve derrubar o fluxo do chat.

        Args:
            model: Model identifier (e.g., "claude-3-5-haiku-20241022")
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens

        Returns:
            Dictionary with cost breakdown::

                {
                    "input_cost": float,
                    "output_cost": float,
                    "total_cost": float,
                }
        """
        pricing = cls._resolve_pricing(model)

        if pricing is None:
            logger.warning(
                "Modelo '%s' não mapeado em CostTracker.PRICING — custo reportado "
                "como $0. Adicione o pricing em core/utils/cost_tracker.py para "
                "obter valores reais.",
                model,
            )
            return {"input_cost": 0.0, "output_cost": 0.0, "total_cost": 0.0}

        input_cost = (input_tokens / 1_000_000) * pricing["input"]
        output_cost = (output_tokens / 1_000_000) * pricing["output"]
        total_cost = input_cost + output_cost

        return {
            "input_cost": input_cost,
            "output_cost": output_cost,
            "total_cost": total_cost,
        }

    @classmethod
    def format_cost(cls, cost: float) -> str:
        """Format cost for display (e.g., ``$0.00012345``)."""
        return f"${cost:.8f}"

    @classmethod
    def get_model_info(cls, model: str) -> Dict[str, float]:
        """Retorna pricing por 1M tokens.

        Quando o modelo não está mapeado, devolve um dicionário com zeros em
        vez de levantar ``ValueError``. Verifique o log para adicionar o
        pricing correto.
        """
        pricing = cls._resolve_pricing(model)
        if pricing is None:
            logger.warning(
                "Modelo '%s' não mapeado em CostTracker.PRICING — retornando zeros.",
                model,
            )
            return {"input": 0.0, "output": 0.0}
        return pricing
