"""
Unit tests for CostTracker utility.

Tests cost calculation logic without making actual API calls.
"""

import pytest
from utils.cost_tracker import CostTracker

class TestCostTracker:
    """Test suite for CostTracker class."""

    def test_calculate_cost_haiku(self):
        """Test cost calculation for Haiku model."""
        model = "claude-3-5-haiku-20241022"
        input_tokens = 18
        output_tokens = 25

        result = CostTracker.calculate_cost(model, input_tokens, output_tokens)

        # Expected costs based on Haiku pricing
        # Input: (18 / 1M) * $0.80 = $0.0000144
        # Output: (25 / 1M) * $4.00 = $0.0001
        # Total: $0.0001144
        assert result["input_cost"] == pytest.approx(0.0000144, rel=1e-6)
        assert result["output_cost"] == pytest.approx(0.0001, rel=1e-6)
        assert result["total_cost"] == pytest.approx(0.0001144, rel=1e-6)

    def test_calculate_cost_opus(self):
        """Test cost calculation for Opus model."""
        model = "claude-3-opus-20240229"
        input_tokens = 500
        output_tokens = 1000

        result = CostTracker.calculate_cost(model, input_tokens, output_tokens)

        # Expected costs based on Opus pricing
        # Input: (500 / 1M) * $15.00 = $0.0075
        # Output: (1000 / 1M) * $75.00 = $0.075
        # Total: $0.0825
        assert result["input_cost"] == pytest.approx(0.0075, rel=1e-6)
        assert result["output_cost"] == pytest.approx(0.075, rel=1e-6)
        assert result["total_cost"] == pytest.approx(0.0825, rel=1e-6)

    def test_calculate_cost_zero_tokens(self):
        """Test cost calculation with zero tokens."""
        model = "claude-3-5-haiku-20241022"
        input_tokens = 0
        output_tokens = 0

        result = CostTracker.calculate_cost(model, input_tokens, output_tokens)

        assert result["input_cost"] == 0.0
        assert result["output_cost"] == 0.0
        assert result["total_cost"] == 0.0

    def test_calculate_cost_invalid_model(self):
        """Test that invalid model raises ValueError."""
        with pytest.raises(ValueError, match="Model .* not supported"):
            CostTracker.calculate_cost("invalid-model", 100, 100)

    def test_format_cost(self):
        """Test cost formatting."""
        assert CostTracker.format_cost(0.0001144) == "$0.00011440"
        assert CostTracker.format_cost(0.00000001) == "$0.00000001"
        assert CostTracker.format_cost(1.23456789) == "$1.23456789"
        assert CostTracker.format_cost(0) == "$0.00000000"

    def test_get_model_info_haiku(self):
        """Test getting model pricing info for Haiku."""
        model = "claude-3-5-haiku-20241022"
        info = CostTracker.get_model_info(model)

        assert info["input"] == 0.80
        assert info["output"] == 4.00

    def test_get_model_info_invalid(self):
        """Test that getting info for invalid model raises ValueError."""
        with pytest.raises(ValueError, match="Model .* not supported"):
            CostTracker.get_model_info("invalid-model")

    def test_cost_structure(self):
        """Test that result has expected structure."""
        model = "claude-3-5-haiku-20241022"
        result = CostTracker.calculate_cost(model, 100, 100)

        # Verify all expected keys are present
        assert "input_cost" in result
        assert "output_cost" in result
        assert "total_cost" in result

        # Verify all values are floats
        assert isinstance(result["input_cost"], float)
        assert isinstance(result["output_cost"], float)
        assert isinstance(result["total_cost"], float)

    def test_large_token_counts(self):
        """Test cost calculation with large token counts (1M tokens)."""
        model = "claude-3-5-haiku-20241022"
        input_tokens = 1_000_000
        output_tokens = 1_000_000

        result = CostTracker.calculate_cost(model, input_tokens, output_tokens)

        # 1M input tokens * $0.80 = $0.80
        # 1M output tokens * $4.00 = $4.00
        # Total: $4.80
        assert result["input_cost"] == pytest.approx(0.80, rel=1e-6)
        assert result["output_cost"] == pytest.approx(4.00, rel=1e-6)
        assert result["total_cost"] == pytest.approx(4.80, rel=1e-6)
