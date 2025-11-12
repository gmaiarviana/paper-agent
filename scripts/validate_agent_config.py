#!/usr/bin/env python3
"""
Script de validação manual para configurações de agentes (Épico 6).

Valida que arquivos YAML de configuração foram implementados corretamente:
- Estrutura de diretórios
- Arquivos YAML existentes
- Schema válido
- Config loader funcionando
- MemoryManager funcionando

Versão: 1.0
Data: 12/11/2025
"""

import sys
from pathlib import Path

# Adicionar o diretório raiz ao PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from agents.memory.config_loader import (
    load_agent_config,
    load_all_agent_configs,
    list_available_agents,
    get_agent_prompt,
    get_agent_context_limits,
    get_agent_model,
    ConfigLoadError
)
from agents.memory.config_validator import (
    validate_agent_config_schema,
    ConfigValidationError,
    get_schema_documentation
)
from agents.memory.memory_manager import MemoryManager


def validate_directory_structure():
    """Valida que estrutura de diretórios foi criada corretamente."""
    print("=" * 70)
    print("VALIDAÇÃO DA ESTRUTURA DE DIRETÓRIOS")
    print("=" * 70)

    config_dir = project_root / "config" / "agents"
    memory_dir = project_root / "agents" / "memory"

    print("\n1. Verificando diretório config/agents/...")
    assert config_dir.exists(), f"Diretório não encontrado: {config_dir}"
    assert config_dir.is_dir(), f"Não é um diretório: {config_dir}"
    print("   ✅ config/agents/ existe")

    print("\n2. Verificando diretório agents/memory/...")
    assert memory_dir.exists(), f"Diretório não encontrado: {memory_dir}"
    assert memory_dir.is_dir(), f"Não é um diretório: {memory_dir}"
    print("   ✅ agents/memory/ existe")


def validate_yaml_files():
    """Valida que arquivos YAML foram criados para cada agente."""
    print("\n" + "=" * 70)
    print("VALIDAÇÃO DOS ARQUIVOS YAML")
    print("=" * 70)

    config_dir = project_root / "config" / "agents"
    expected_agents = ["orchestrator", "structurer", "methodologist"]

    for agent_name in expected_agents:
        yaml_file = config_dir / f"{agent_name}.yaml"

        print(f"\n{len(expected_agents) - expected_agents.index(agent_name)}. Verificando {agent_name}.yaml...")
        assert yaml_file.exists(), f"Arquivo não encontrado: {yaml_file}"
        print(f"   ✅ {agent_name}.yaml existe")

        # Verificar tamanho mínimo (não vazio)
        file_size = yaml_file.stat().st_size
        assert file_size > 100, f"Arquivo muito pequeno (possivelmente vazio): {file_size} bytes"
        print(f"   ✅ Tamanho do arquivo: {file_size} bytes")


def validate_config_loader():
    """Valida que config_loader está funcionando corretamente."""
    print("\n" + "=" * 70)
    print("VALIDAÇÃO DO CONFIG LOADER")
    print("=" * 70)

    print("\n1. Testando list_available_agents()...")
    agents = list_available_agents()
    assert len(agents) >= 3, f"Esperado pelo menos 3 agentes, encontrado: {len(agents)}"
    assert "orchestrator" in agents
    assert "structurer" in agents
    assert "methodologist" in agents
    print(f"   ✅ {len(agents)} agentes encontrados: {', '.join(agents)}")

    print("\n2. Testando load_agent_config() para cada agente...")
    for agent_name in ["orchestrator", "structurer", "methodologist"]:
        config = load_agent_config(agent_name)
        assert config is not None
        assert "prompt" in config
        assert "tags" in config
        assert "context_limits" in config
        assert "model" in config
        assert "metadata" in config
        print(f"   ✅ {agent_name}: configuração carregada com sucesso")

    print("\n3. Testando load_all_agent_configs()...")
    all_configs = load_all_agent_configs()
    assert len(all_configs) >= 3
    print(f"   ✅ Todas as configurações carregadas: {len(all_configs)} agentes")

    print("\n4. Testando funções auxiliares...")

    # get_agent_prompt
    prompt = get_agent_prompt("orchestrator")
    assert isinstance(prompt, str)
    assert len(prompt) > 0
    print("   ✅ get_agent_prompt() funciona")

    # get_agent_context_limits
    limits = get_agent_context_limits("structurer")
    assert "max_input_tokens" in limits
    assert "max_output_tokens" in limits
    assert "max_total_tokens" in limits
    print("   ✅ get_agent_context_limits() funciona")

    # get_agent_model
    model = get_agent_model("methodologist")
    assert isinstance(model, str)
    assert "claude" in model.lower()
    print("   ✅ get_agent_model() funciona")


def validate_schema_validator():
    """Valida que validador de schema está funcionando."""
    print("\n" + "=" * 70)
    print("VALIDAÇÃO DO SCHEMA VALIDATOR")
    print("=" * 70)

    print("\n1. Testando validação de configurações existentes...")
    all_configs = load_all_agent_configs()

    for agent_name, config in all_configs.items():
        validate_agent_config_schema(config, agent_name)
        print(f"   ✅ {agent_name}: schema válido")

    print("\n2. Testando validação de configuração inválida...")
    try:
        invalid_config = {"prompt": "teste"}  # Faltando campos obrigatórios
        validate_agent_config_schema(invalid_config, "test")
        assert False, "Deveria ter falhado na validação"
    except ConfigValidationError:
        print("   ✅ Detecta configurações inválidas corretamente")

    print("\n3. Testando documentação do schema...")
    doc = get_schema_documentation()
    assert len(doc) > 0
    assert "Schema de Configuração" in doc
    print("   ✅ Documentação do schema disponível")


def validate_memory_manager():
    """Valida que MemoryManager está funcionando."""
    print("\n" + "=" * 70)
    print("VALIDAÇÃO DO MEMORY MANAGER")
    print("=" * 70)

    print("\n1. Testando inicialização...")
    manager = MemoryManager()
    assert manager is not None
    print("   ✅ MemoryManager inicializado")

    print("\n2. Testando adição de execuções...")
    execution1 = manager.add_execution(
        session_id="test-session",
        agent_name="orchestrator",
        tokens_input=100,
        tokens_output=50,
        summary="Classificou input como 'vague'"
    )
    assert execution1.tokens_total == 150
    print("   ✅ add_execution() funciona")

    print("\n3. Testando recuperação de histórico...")
    history = manager.get_agent_history("test-session", "orchestrator")
    assert len(history) == 1
    assert history[0].summary == "Classificou input como 'vague'"
    print("   ✅ get_agent_history() funciona")

    print("\n4. Testando múltiplos agentes...")
    manager.add_execution("test-session", "structurer", 200, 100, "Estruturou")
    manager.add_execution("test-session", "methodologist", 300, 150, "Avaliou")

    session_history = manager.get_session_history("test-session")
    assert len(session_history) == 3
    print("   ✅ Múltiplos agentes funcionando")

    print("\n5. Testando cálculo de totais...")
    totals = manager.get_session_totals("test-session")
    assert totals["orchestrator"] == 150
    assert totals["structurer"] == 300
    assert totals["methodologist"] == 450
    assert totals["total"] == 900
    print(f"   ✅ Totais corretos: {totals['total']} tokens")

    print("\n6. Testando reset de sessão...")
    result = manager.reset_session("test-session")
    assert result is True
    assert manager.get_session_history("test-session") == {}
    print("   ✅ reset_session() funciona")

    print("\n7. Testando reset global...")
    manager.add_execution("s1", "orchestrator", 100, 50, "A1")
    manager.add_execution("s2", "orchestrator", 200, 100, "A2")
    count = manager.reset_all()
    assert count == 2
    assert len(manager.list_sessions()) == 0
    print("   ✅ reset_all() funciona")

    print("\n8. Testando exportação...")
    manager.add_execution("export-test", "orchestrator", 100, 50, "Teste")
    export = manager.export_session_as_dict("export-test")
    assert export["session_id"] == "export-test"
    assert "agents" in export
    assert "totals" in export
    print("   ✅ export_session_as_dict() funciona")


def validate_integration():
    """Valida integração entre componentes."""
    print("\n" + "=" * 70)
    print("VALIDAÇÃO DE INTEGRAÇÃO")
    print("=" * 70)

    print("\n1. Testando integração Config Loader + Memory Manager...")

    # Carregar config de um agente
    config = load_agent_config("orchestrator")
    limits = config["context_limits"]

    # Criar execução com metadados da config
    manager = MemoryManager()
    manager.add_execution(
        session_id="integration-test",
        agent_name="orchestrator",
        tokens_input=limits["max_input_tokens"] // 2,
        tokens_output=limits["max_output_tokens"] // 2,
        summary="Teste de integração",
        metadata={
            "model": config["model"],
            "max_tokens": limits["max_total_tokens"]
        }
    )

    execution = manager.get_latest_execution("integration-test", "orchestrator")
    assert execution.metadata["model"] == config["model"]
    print("   ✅ Integração funcionando corretamente")


def main():
    """Executa todas as validações."""
    print("\n")
    print("█" * 70)
    print("█" + " " * 68 + "█")
    print("█" + "  VALIDAÇÃO COMPLETA - ÉPICO 6: MEMÓRIA E CONTEXTO POR AGENTE  ".center(68) + "█")
    print("█" + " " * 68 + "█")
    print("█" * 70)

    try:
        validate_directory_structure()
        validate_yaml_files()
        validate_config_loader()
        validate_schema_validator()
        validate_memory_manager()
        validate_integration()

        print("\n" + "=" * 70)
        print("RESUMO FINAL")
        print("=" * 70)
        print("\n✅ Estrutura de diretórios: OK")
        print("✅ Arquivos YAML: OK (3 agentes)")
        print("✅ Config Loader: OK")
        print("✅ Schema Validator: OK")
        print("✅ Memory Manager: OK")
        print("✅ Integração: OK")

        print("\n" + "█" * 70)
        print("█" + " " * 68 + "█")
        print("█" + "  🎉 TODAS AS VALIDAÇÕES PASSARAM! ÉPICO 6 IMPLEMENTADO! 🎉  ".center(68) + "█")
        print("█" + " " * 68 + "█")
        print("█" * 70)
        print()

    except AssertionError as e:
        print(f"\n❌ ERRO: {e}")
        print("\nValidação falhou. Verifique a implementação.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERRO INESPERADO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
