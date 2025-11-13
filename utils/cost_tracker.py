"""
Cost tracking utility for Anthropic API usage.

Calculates costs based on token usage and model pricing.
Pricing information: https://www.anthropic.com/pricing
"""

from typing import Dict, Tuple


class CostTracker:
    """
    Tracks and calculates costs for Anthropic API calls.

    Supports multiple Claude models with their respective pricing tiers.
    """

    # Pricing in USD per 1M tokens (as of January 2025)
    PRICING = {
        "claude-3-5-haiku-20241022": {
            "input": 0.80,   # $0.80 per 1M input tokens
            "output": 4.00,  # $4.00 per 1M output tokens
        },
        "claude-3-5-sonnet-20241022": {
            "input": 3.00,   # $3.00 per 1M input tokens
            "output": 15.00, # $15.00 per 1M output tokens
        },
        "claude-sonnet-4-20250514": {
            "input": 3.00,   # $3.00 per 1M input tokens (same as 3.5 Sonnet)
            "output": 15.00, # $15.00 per 1M output tokens (same as 3.5 Sonnet)
        },
        "claude-3-opus-20240229": {
            "input": 15.00,  # $15.00 per 1M input tokens
            "output": 75.00, # $75.00 per 1M output tokens
        },
    }

    @classmethod
    def calculate_cost(
        cls,
        model: str,
        input_tokens: int,
        output_tokens: int
    ) -> Dict[str, float]:
        """
        Calculate cost for an API call.

        Args:
            model: Model identifier (e.g., "claude-3-5-haiku-20241022")
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens

        Returns:
            Dictionary with cost breakdown:
            {
                "input_cost": float,
                "output_cost": float,
                "total_cost": float
            }

        Raises:
            ValueError: If model is not supported
        """
        if model not in cls.PRICING:
            raise ValueError(
                f"Model '{model}' not supported. "
                f"Supported models: {list(cls.PRICING.keys())}"
            )

        pricing = cls.PRICING[model]

        # Calculate costs (price per 1M tokens)
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
        """
        Format cost for display.

        Args:
            cost: Cost in USD

        Returns:
            Formatted string (e.g., "$0.00012345")
        """
        return f"${cost:.8f}"

    @classmethod
    def get_model_info(cls, model: str) -> Dict[str, float]:
        """
        Get pricing information for a model.

        Args:
            model: Model identifier

        Returns:
            Dictionary with pricing per 1M tokens

        Raises:
            ValueError: If model is not supported
        """
        if model not in cls.PRICING:
            raise ValueError(
                f"Model '{model}' not supported. "
                f"Supported models: {list(cls.PRICING.keys())}"
            )

        return cls.PRICING[model]
