#!/usr/bin/env python3
"""
Script de validação simples para integração de configs YAML (Épico 6, Funcionalidade 6.1).

Valida carregamento de configs sem executar o grafo completo.

Versão: 1.0
Data: 13/11/2025
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT_STR = str(PROJECT_ROOT)
if PROJECT_ROOT_STR not in sys.path:
    sys.path.insert(0, PROJECT_ROOT_STR)

from scripts.common import setup_project_path

setup_project_path()

from agents.memory.config_loader import (
    load_all_agent_configs,
    get_agent_prompt,
    get_agent_model,
    get_agent_context_limits,
    list_available_agents,
    ConfigLoadError
)


def print_header(title: str):
    """Imprime cabeçalho formatado."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def print_section(title: str):
    """Imprime seção formatada."""
    print("\n" + "-" * 80)
    print(f"  {title}")
    print("-" * 80)


def validate_config_loading():
    """Valida que todas as configs podem ser carregadas."""
    print_section("1. CARREGAMENTO DE TODAS AS CONFIGURAÇÕES")

    try:
        configs = load_all_agent_configs()
        print(f"✅ {len(configs)} configurações carregadas com sucesso")

        for agent_name, config in configs.items():
            print(f"\n  Agente: {agent_name}")
            print(f"    - Modelo: {config['model']}")
            print(f"    - Prompt length: {len(config['prompt'])} caracteres")
            print(f"    - Max tokens: {config['context_limits']['max_total_tokens']}")
            print(f"    - Tags: {', '.join(config['tags'])}")
            print(f"    - Versão: {config['metadata']['version']}")
            print(f"    - Épico: {config['metadata']['epic']}")

        return True

    except ConfigLoadError as e:
        print(f"❌ FALHA ao carregar configs: {e}")
        return False


def validate_individual_loaders():
    """Valida funções individuais de carregamento."""
    print_section("2. FUNÇÕES INDIVIDUAIS DE CARREGAMENTO")

    agents = ["orchestrator", "structurer", "methodologist"]
    all_ok = True

    for agent_name in agents:
        try:
            prompt = get_agent_prompt(agent_name)
            model = get_agent_model(agent_name)
            limits = get_agent_context_limits(agent_name)

            print(f"\n  {agent_name}:")
            print(f"    ✅ Prompt carregado ({len(prompt)} caracteres)")
            print(f"    ✅ Modelo: {model}")
            print(f"    ✅ Limites: input={limits['max_input_tokens']}, output={limits['max_output_tokens']}")

        except ConfigLoadError as e:
            print(f"\n  {agent_name}:")
            print(f"    ❌ FALHA: {e}")
            all_ok = False

    return all_ok


def validate_list_agents():
    """Valida listagem de agentes disponíveis."""
    print_section("3. LISTAGEM DE AGENTES DISPONÍVEIS")

    try:
        agents = list_available_agents()
        print(f"✅ {len(agents)} agentes disponíveis:")

        for agent_name in agents:
            print(f"  - {agent_name}")

        required_agents = ["orchestrator", "structurer", "methodologist"]
        missing = [a for a in required_agents if a not in agents]

        if missing:
            print(f"\n❌ Agentes obrigatórios faltando: {', '.join(missing)}")
            return False

        print("\n✅ Todos os agentes obrigatórios estão presentes")
        return True

    except Exception as e:
        print(f"❌ FALHA ao listar agentes: {e}")
        return False


def validate_fallback_behavior():
    """Valida comportamento de fallback quando YAML não existe."""
    print_section("4. VALIDAÇÃO DE FALLBACK")

    print("\nTestando fallback para agente inexistente...")
    try:
        prompt = get_agent_prompt("nonexistent_agent")
        print(f"❌ Deveria ter falhado, mas retornou prompt")
        return False

    except ConfigLoadError as e:
        print(f"✅ ConfigLoadError levantado corretamente")
        error_msg = str(e)
        print(f"   Mensagem: {error_msg[:120]}...")

        # Verificar se mensagem está em PT-BR
        if "não encontrado" in error_msg.lower():
            print("✅ Mensagem de erro em PT-BR")
            return True
        else:
            print("⚠️ Mensagem de erro não está completamente em PT-BR")
            return True  # Não é crítico


def validate_yaml_structure():
    """Valida estrutura dos YAMLs."""
    print_section("5. VALIDAÇÃO DE ESTRUTURA DOS YAMLs")

    try:
        configs = load_all_agent_configs()
        all_ok = True

        required_fields = ["prompt", "tags", "context_limits", "model", "metadata"]
        context_fields = ["max_input_tokens", "max_output_tokens", "max_total_tokens"]
        metadata_fields = ["version", "epic", "created_at", "description"]

        for agent_name, config in configs.items():
            print(f"\n  Validando {agent_name}:")

            # Campos de nível superior
            missing = [f for f in required_fields if f not in config]
            if missing:
                print(f"    ❌ Campos faltando: {', '.join(missing)}")
                all_ok = False
            else:
                print(f"    ✅ Todos os campos obrigatórios presentes")

            # Campos de context_limits
            if "context_limits" in config:
                missing_context = [f for f in context_fields if f not in config["context_limits"]]
                if missing_context:
                    print(f"    ❌ Campos faltando em context_limits: {', '.join(missing_context)}")
                    all_ok = False
                else:
                    print(f"    ✅ context_limits completo")

            # Campos de metadata
            if "metadata" in config:
                missing_meta = [f for f in metadata_fields if f not in config["metadata"]]
                if missing_meta:
                    print(f"    ❌ Campos faltando em metadata: {', '.join(missing_meta)}")
                    all_ok = False
                else:
                    print(f"    ✅ metadata completo")

        return all_ok

    except ConfigLoadError as e:
        print(f"❌ FALHA na validação: {e}")
        return False


def main():
    """Executa todas as validações."""
    print_header("VALIDAÇÃO DE CONFIGURAÇÕES YAML - ÉPICO 6, FUNCIONALIDADE 6.1")

    print("\nEste script valida que os arquivos YAML em config/agents/ estão corretos")
    print("e que o config_loader funciona adequadamente.")

    results = []

    # Teste 1: Carregamento de configs
    results.append(("Carregamento de configs", validate_config_loading()))

    # Teste 2: Funções individuais
    results.append(("Funções individuais", validate_individual_loaders()))

    # Teste 3: Listagem de agentes
    results.append(("Listagem de agentes", validate_list_agents()))

    # Teste 4: Fallback
    results.append(("Fallback", validate_fallback_behavior()))

    # Teste 5: Estrutura YAML
    results.append(("Estrutura YAML", validate_yaml_structure()))

    # Sumário
    print_header("SUMÁRIO DA VALIDAÇÃO")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    print(f"\nResultados: {passed}/{total} testes passaram\n")

    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"  {status}: {test_name}")

    print("\n" + "=" * 80)

    if passed == total:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("✅ Config loader implementado corretamente")
        print("✅ Próximo passo: Validar integração runtime nos nós (requer ambiente virtual)")
        print("=" * 80)
        return 0
    else:
        print(f"⚠️  {total - passed} TESTE(S) FALHARAM")
        print("❌ Verifique os erros acima e corrija antes de continuar")
        print("=" * 80)
        return 1


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️ Validação interrompida pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ ERRO INESPERADO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
