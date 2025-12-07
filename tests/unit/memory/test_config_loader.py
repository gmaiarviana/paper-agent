"""
Testes unitários para config_loader (Épico 6).

Valida carregamento e validação de configurações YAML de agentes.

Versão: 1.0
Data: 12/11/2025
"""

import pytest
from pathlib import Path

from agents.memory.config_loader import (
    load_agent_config,
    load_all_agent_configs,
    get_agent_prompt,
    get_agent_context_limits,
    get_agent_model,
    list_available_agents,
    ConfigLoadError
)
from agents.memory.config_validator import ConfigValidationError


class TestLoadAgentConfig:
    """Testes para load_agent_config()."""

    def test_load_nonexistent_agent(self):
        """Deve falhar ao carregar agente inexistente (validação de erro real)."""
        with pytest.raises(ConfigLoadError) as exc_info:
            load_agent_config("nonexistent_agent")

        assert "não encontrado" in str(exc_info.value)


class TestContextLimits:
    """Testes para validação de limites de contexto (lógica de negócio)."""

    def test_context_limits_are_valid(self):
        """Limites de contexto devem ser válidos (max_total >= max_input + max_output)."""
        configs = load_all_agent_configs()

        for agent_name, config in configs.items():
            limits = config["context_limits"]
            assert limits["max_input_tokens"] > 0
            assert limits["max_output_tokens"] > 0
            assert limits["max_total_tokens"] > 0
            assert limits["max_total_tokens"] >= limits["max_input_tokens"] + limits["max_output_tokens"]
