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

    def test_load_orchestrator_config(self):
        """Deve carregar configuração do orchestrator com sucesso."""
        config = load_agent_config("orchestrator")

        assert config is not None
        assert "prompt" in config
        assert "tags" in config
        assert "context_limits" in config
        assert "model" in config
        assert "metadata" in config

    def test_load_structurer_config(self):
        """Deve carregar configuração do structurer com sucesso."""
        config = load_agent_config("structurer")

        assert config is not None
        assert "prompt" in config
        assert isinstance(config["tags"], list)
        assert len(config["tags"]) > 0

    def test_load_methodologist_config(self):
        """Deve carregar configuração do methodologist com sucesso."""
        config = load_agent_config("methodologist")

        assert config is not None
        assert config["model"] == "claude-sonnet-4-20250514"
        assert config["metadata"]["version"] == "1.0"

    def test_load_nonexistent_agent(self):
        """Deve falhar ao carregar agente inexistente."""
        with pytest.raises(ConfigLoadError) as exc_info:
            load_agent_config("nonexistent_agent")

        assert "não encontrado" in str(exc_info.value)


class TestLoadAllAgentConfigs:
    """Testes para load_all_agent_configs()."""

    def test_load_all_configs(self):
        """Deve carregar todas as configurações disponíveis."""
        configs = load_all_agent_configs()

        assert isinstance(configs, dict)
        assert len(configs) >= 3  # orchestrator, structurer, methodologist

        # Verificar que agentes esperados estão presentes
        assert "orchestrator" in configs
        assert "structurer" in configs
        assert "methodologist" in configs

    def test_all_configs_valid(self):
        """Todas as configurações devem ter campos obrigatórios."""
        configs = load_all_agent_configs()

        for agent_name, config in configs.items():
            assert "prompt" in config, f"{agent_name} faltando 'prompt'"
            assert "tags" in config, f"{agent_name} faltando 'tags'"
            assert "context_limits" in config, f"{agent_name} faltando 'context_limits'"
            assert "model" in config, f"{agent_name} faltando 'model'"
            assert "metadata" in config, f"{agent_name} faltando 'metadata'"


class TestContextLimits:
    """Testes para validação de limites de contexto."""

    def test_orchestrator_context_limits(self):
        """Orchestrator deve ter limites de contexto válidos."""
        config = load_agent_config("orchestrator")
        limits = config["context_limits"]

        assert limits["max_input_tokens"] > 0
        assert limits["max_output_tokens"] > 0
        assert limits["max_total_tokens"] > 0
        assert limits["max_total_tokens"] >= limits["max_input_tokens"] + limits["max_output_tokens"]

    def test_methodologist_larger_limits(self):
        """Methodologist deve ter limites maiores que orchestrator."""
        orch_config = load_agent_config("orchestrator")
        meth_config = load_agent_config("methodologist")

        orch_max = orch_config["context_limits"]["max_total_tokens"]
        meth_max = meth_config["context_limits"]["max_total_tokens"]

        assert meth_max > orch_max


class TestHelperFunctions:
    """Testes para funções auxiliares."""

    def test_get_agent_prompt(self):
        """Deve obter prompt de agente."""
        prompt = get_agent_prompt("orchestrator")

        assert isinstance(prompt, str)
        assert len(prompt) > 0
        assert "Orquestrador" in prompt

    def test_get_agent_context_limits(self):
        """Deve obter limites de contexto."""
        limits = get_agent_context_limits("structurer")

        assert isinstance(limits, dict)
        assert "max_input_tokens" in limits
        assert "max_output_tokens" in limits
        assert "max_total_tokens" in limits

    def test_get_agent_model(self):
        """Deve obter modelo de agente."""
        model = get_agent_model("methodologist")

        assert isinstance(model, str)
        assert "claude" in model.lower()

    def test_list_available_agents(self):
        """Deve listar agentes disponíveis."""
        agents = list_available_agents()

        assert isinstance(agents, list)
        assert len(agents) >= 3
        assert "orchestrator" in agents
        assert "structurer" in agents
        assert "methodologist" in agents


class TestMetadata:
    """Testes para metadados de configurações."""

    def test_all_configs_have_metadata(self):
        """Todas as configurações devem ter metadados completos."""
        configs = load_all_agent_configs()

        for agent_name, config in configs.items():
            metadata = config["metadata"]

            assert "version" in metadata
            assert "epic" in metadata
            assert "created_at" in metadata
            assert "description" in metadata

            # Validar que são strings não-vazias
            assert isinstance(metadata["version"], str)
            assert len(metadata["version"]) > 0

    def test_epic_6_metadata(self):
        """Todos os agentes devem estar marcados como Épico 6."""
        configs = load_all_agent_configs()

        for agent_name, config in configs.items():
            assert config["metadata"]["epic"] == "6"


class TestModels:
    """Testes para configurações de modelos LLM."""

    def test_orchestrator_uses_haiku(self):
        """Orchestrator deve usar Haiku (custo-benefício)."""
        config = load_agent_config("orchestrator")
        assert "haiku" in config["model"].lower()

    def test_structurer_uses_haiku(self):
        """Structurer deve usar Haiku (custo-benefício)."""
        config = load_agent_config("structurer")
        assert "haiku" in config["model"].lower()

    def test_methodologist_uses_sonnet(self):
        """Methodologist deve usar Sonnet (maior confiabilidade)."""
        config = load_agent_config("methodologist")
        assert "sonnet" in config["model"].lower()


class TestTags:
    """Testes para tags de configurações."""

    def test_orchestrator_tags(self):
        """Orchestrator deve ter tags apropriadas."""
        config = load_agent_config("orchestrator")
        tags = config["tags"]

        assert "orchestrator" in tags
        assert "router" in tags or "classifier" in tags

    def test_structurer_tags(self):
        """Structurer deve ter tags apropriadas."""
        config = load_agent_config("structurer")
        tags = config["tags"]

        assert "structurer" in tags
        assert "refinement" in tags or "research-question" in tags

    def test_methodologist_tags(self):
        """Methodologist deve ter tags apropriadas."""
        config = load_agent_config("methodologist")
        tags = config["tags"]

        assert "methodologist" in tags
        assert "scientific-rigor" in tags or "collaborative" in tags
