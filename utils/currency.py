"""
Currency formatting utility for cost display (Epic 5.1).

Supports USD and BRL (Brazilian Real) formatting.
Reads configuration from environment variables.

Environment Variables:
    CURRENCY: Currency to display ("USD" or "BRL"). Default: "USD"
    USD_TO_BRL_RATE: Exchange rate for USD to BRL conversion. Default: 5.5

Usage:
    from utils.currency import format_currency

    cost_usd = 0.0012
    formatted = format_currency(cost_usd)  # Returns "$0.0012" or "R$ 0,01"
"""

import os
from typing import Optional


def get_currency_config() -> tuple[str, float]:
    """
    Get currency configuration from environment variables.

    Returns:
        tuple: (currency_code, exchange_rate)
            - currency_code: "USD" or "BRL"
            - exchange_rate: USD to BRL rate (only used if currency is BRL)
    """
    currency = os.getenv("CURRENCY", "USD").upper()
    rate_str = os.getenv("USD_TO_BRL_RATE", "5.5")

    try:
        rate = float(rate_str)
    except ValueError:
        rate = 5.5

    return currency, rate


def format_currency(
    cost_usd: float,
    decimals: int = 4,
    currency: Optional[str] = None,
    rate: Optional[float] = None
) -> str:
    """
    Format cost for display in configured currency.

    Args:
        cost_usd: Cost in USD
        decimals: Number of decimal places (default: 4)
        currency: Override currency (for testing). If None, reads from env.
        rate: Override exchange rate (for testing). If None, reads from env.

    Returns:
        Formatted string:
            - USD: "$0.0012" (dot as decimal separator)
            - BRL: "R$ 0,0066" (comma as decimal separator)

    Examples:
        >>> format_currency(0.0012)  # With CURRENCY=USD
        '$0.0012'
        >>> format_currency(0.0012)  # With CURRENCY=BRL, USD_TO_BRL_RATE=5.5
        'R$ 0,0066'
    """
    if currency is None or rate is None:
        env_currency, env_rate = get_currency_config()
        currency = currency or env_currency
        rate = rate if rate is not None else env_rate

    if currency == "BRL":
        # Convert USD to BRL
        cost_brl = cost_usd * rate
        # Format with Brazilian notation (comma as decimal separator)
        # Use f-string to get the number, then replace dot with comma
        formatted_number = f"{cost_brl:.{decimals}f}".replace(".", ",")
        return f"R$ {formatted_number}"
    else:
        # Default: USD format
        return f"${cost_usd:.{decimals}f}"


def format_currency_short(cost_usd: float) -> str:
    """
    Format cost for compact display (2 decimal places).

    Args:
        cost_usd: Cost in USD

    Returns:
        Formatted string with 2 decimal places

    Examples:
        >>> format_currency_short(0.02)  # With CURRENCY=BRL
        'R$ 0,11'
    """
    return format_currency(cost_usd, decimals=2)


def format_currency_precise(cost_usd: float) -> str:
    """
    Format cost for detailed display (6 decimal places).

    Args:
        cost_usd: Cost in USD

    Returns:
        Formatted string with 6 decimal places

    Examples:
        >>> format_currency_precise(0.000891)  # With CURRENCY=BRL
        'R$ 0,004901'
    """
    return format_currency(cost_usd, decimals=6)
