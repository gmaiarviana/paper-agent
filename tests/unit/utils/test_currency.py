"""
Unit tests for currency formatting utility (Epic 5.1).

Tests currency conversion and formatting without external dependencies.
"""

import pytest
from core.utils.currency import (
    format_currency,
    format_currency_short,
    format_currency_precise,
    get_currency_config
)

class TestCurrencyFormatting:
    """Test suite for currency formatting functions."""

    def test_format_currency_usd_default(self):
        """Test default USD formatting with 4 decimal places."""
        # Force USD currency for test
        result = format_currency(0.0012, currency="USD")
        assert result == "$0.0012"

    def test_format_currency_usd_zero(self):
        """Test USD formatting with zero cost."""
        result = format_currency(0.0, currency="USD")
        assert result == "$0.0000"

    def test_format_currency_usd_large(self):
        """Test USD formatting with larger amounts."""
        result = format_currency(1.2345, currency="USD")
        assert result == "$1.2345"

    def test_format_currency_brl_basic(self):
        """Test BRL formatting with basic conversion."""
        # $0.01 * 5.5 = R$ 0,055 -> R$ 0,0550
        result = format_currency(0.01, currency="BRL", rate=5.5)
        assert result == "R$ 0,0550"

    def test_format_currency_brl_uses_comma(self):
        """Test that BRL uses comma as decimal separator."""
        result = format_currency(0.02, currency="BRL", rate=5.0)
        # $0.02 * 5.0 = R$ 0.10 -> "R$ 0,1000"
        assert "," in result
        assert "." not in result.replace("R$ ", "")

    def test_format_currency_brl_conversion(self):
        """Test accurate USD to BRL conversion."""
        # $0.10 * 5.5 = R$ 0.55
        result = format_currency(0.10, currency="BRL", rate=5.5)
        assert result == "R$ 0,5500"

    def test_format_currency_brl_small_amount(self):
        """Test BRL formatting with very small amount."""
        # $0.0012 * 5.5 = R$ 0.0066
        result = format_currency(0.0012, currency="BRL", rate=5.5)
        assert result == "R$ 0,0066"

    def test_format_currency_custom_decimals(self):
        """Test formatting with custom decimal places."""
        result = format_currency(0.123456, decimals=6, currency="USD")
        assert result == "$0.123456"

    def test_format_currency_two_decimals(self):
        """Test formatting with 2 decimal places."""
        result = format_currency(0.125, decimals=2, currency="USD")
        assert result == "$0.12"

    def test_format_currency_brl_custom_decimals(self):
        """Test BRL formatting with custom decimal places."""
        # $0.10 * 5.5 = R$ 0.55 with 2 decimals -> "R$ 0,55"
        result = format_currency(0.10, decimals=2, currency="BRL", rate=5.5)
        assert result == "R$ 0,55"

class TestCurrencyHelpers:
    """Test suite for currency helper functions."""

    def test_format_currency_short(self):
        """Test short format (2 decimals) for USD."""
        # Temporarily override env vars
        result = format_currency_short(0.125)
        # Result depends on env, but format should be consistent
        assert len(result.split(".")[-1]) <= 2 or "," in result

    def test_format_currency_precise(self):
        """Test precise format (6 decimals) for USD."""
        result = format_currency_precise(0.000891)
        # Result depends on env, but format should be consistent
        decimals_part = result.replace("R$ ", "").replace("$", "").replace(",", ".")
        assert len(decimals_part.split(".")[-1]) == 6

class TestCurrencyConfig:
    """Test suite for currency configuration."""

    def test_get_currency_config_returns_tuple(self):
        """Test that config returns a tuple of (currency, rate)."""
        currency, rate = get_currency_config()
        assert isinstance(currency, str)
        assert isinstance(rate, float)

    def test_currency_defaults_to_usd(self, monkeypatch):
        """Test that currency defaults to USD when not set."""
        monkeypatch.delenv("CURRENCY", raising=False)
        currency, _ = get_currency_config()
        assert currency == "USD"

    def test_rate_defaults_to_5_5(self, monkeypatch):
        """Test that rate defaults to 5.5 when not set."""
        monkeypatch.delenv("USD_TO_BRL_RATE", raising=False)
        _, rate = get_currency_config()
        assert rate == 5.5

    def test_config_reads_currency_env(self, monkeypatch):
        """Test that currency reads from CURRENCY env var."""
        monkeypatch.setenv("CURRENCY", "BRL")
        currency, _ = get_currency_config()
        assert currency == "BRL"

    def test_config_reads_rate_env(self, monkeypatch):
        """Test that rate reads from USD_TO_BRL_RATE env var."""
        monkeypatch.setenv("USD_TO_BRL_RATE", "6.0")
        _, rate = get_currency_config()
        assert rate == 6.0

    def test_currency_uppercase(self, monkeypatch):
        """Test that currency is converted to uppercase."""
        monkeypatch.setenv("CURRENCY", "brl")
        currency, _ = get_currency_config()
        assert currency == "BRL"

    def test_invalid_rate_fallback(self, monkeypatch):
        """Test that invalid rate falls back to 5.5."""
        monkeypatch.setenv("USD_TO_BRL_RATE", "invalid")
        _, rate = get_currency_config()
        assert rate == 5.5

class TestBRLIntegration:
    """Integration tests for BRL formatting with env vars."""

    def test_brl_end_to_end(self, monkeypatch):
        """Test complete BRL formatting flow."""
        monkeypatch.setenv("CURRENCY", "BRL")
        monkeypatch.setenv("USD_TO_BRL_RATE", "5.5")

        # $0.02 * 5.5 = R$ 0.11
        result = format_currency(0.02)
        assert result == "R$ 0,1100"

    def test_usd_end_to_end(self, monkeypatch):
        """Test complete USD formatting flow."""
        monkeypatch.setenv("CURRENCY", "USD")

        result = format_currency(0.02)
        assert result == "$0.0200"

    def test_fallback_when_currency_not_brl(self, monkeypatch):
        """Test that non-BRL currencies use USD format."""
        monkeypatch.setenv("CURRENCY", "EUR")

        result = format_currency(0.02)
        assert result == "$0.0200"  # Falls back to USD format
