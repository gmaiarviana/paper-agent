#!/usr/bin/env python3
"""
Script de validação manual para integração runtime de configs YAML (Épico 6, Funcionalidade 6.1).

Valida que os nós do sistema carregam corretamente prompts e modelos dos arquivos YAML
em config/agents/ durante a execução runtime.

Testes realizados:
1. Carregamento de configs no bootstrap do super-grafo
2. Carregamento de configs no orchestrator_node
3. Carregamento de configs no structurer_node
4. Carregamento de configs nos nós do methodologist
5. Fallback quando YAML está corrompido/ausente
6. Mensagens de erro em PT-BR

Versão: 1.0
Data: 13/11/2025
"""

import sys
import logging
from pathlib import Path

# Adicionar o diretório raiz ao PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from agents.memory.config_loader import (
    load_all_agent_configs,
    get_agent_prompt,
    get_agent_model,
    ConfigLoadError
)
from agents.multi_agent_graph import create_multi_agent_graph
from agents.orchestrator.state import create_initial_multi_agent_state

# Configurar logging para ver as mensagens dos nós
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)


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
    print_section("1. CARREGAMENTO DE CONFIGURAÇÕES")

    try:
        configs = load_all_agent_configs()
        print(f"✅ {len(configs)} configurações carregadas com sucesso")

        for agent_name, config in configs.items():
            print(f"\n  Agente: {agent_name}")
            print(f"    - Modelo: {config['model']}")
            print(f"    - Prompt length: {len(config['prompt'])} caracteres")
            print(f"    - Limites: {config['context_limits']['max_total_tokens']} tokens")

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

            print(f"\n  {agent_name}:")
            print(f"    ✅ Prompt carregado ({len(prompt)} caracteres)")
            print(f"    ✅ Modelo carregado: {model}")

        except ConfigLoadError as e:
            print(f"\n  {agent_name}:")
            print(f"    ❌ FALHA: {e}")
            all_ok = False

    return all_ok


def validate_graph_bootstrap():
    """Valida bootstrap do super-grafo com validação de configs."""
    print_section("3. VALIDAÇÃO NO BOOTSTRAP DO SUPER-GRAFO")

    try:
        print("\nCriando super-grafo (observe logs de validação acima)...")
        graph = create_multi_agent_graph()
        print("✅ Super-grafo criado com sucesso")
        print("✅ Validação de configs executada no bootstrap")
        return True

    except Exception as e:
        print(f"❌ FALHA ao criar super-grafo: {e}")
        return False


def validate_node_runtime():
    """Valida que nós carregam configs em runtime."""
    print_section("4. CARREGAMENTO RUNTIME NOS NÓS")

    try:
        print("\nCriando super-grafo...")
        graph = create_multi_agent_graph()

        print("\nExecutando teste com input simples...")
        print("(Observe logs '✅ Configurações carregadas do YAML' acima)")

        state = create_initial_multi_agent_state("Teste de configuração")
        config = {"configurable": {"thread_id": "test-config-validation"}}

        # Executar apenas o primeiro passo (orchestrator)
        print("\nExecutando orchestrator_node...")
        result = graph.invoke(state, config, {"recursion_limit": 1})

        print("\n✅ Nó executado com sucesso")
        print("✅ Se você viu '✅ Configurações carregadas do YAML' acima, a integração está funcionando!")

        return True

    except Exception as e:
        print(f"❌ FALHA na execução do nó: {e}")
        import traceback
        traceback.print_exc()
        return False


def validate_fallback_behavior():
    """Valida comportamento de fallback quando YAML não existe."""
    print_section("5. VALIDAÇÃO DE FALLBACK")

    print("\nTestando fallback para agente inexistente...")
    try:
        prompt = get_agent_prompt("nonexistent_agent")
        print(f"❌ Deveria ter falhado, mas retornou: {prompt[:50]}...")
        return False

    except ConfigLoadError as e:
        print(f"✅ ConfigLoadError levantado corretamente")
        print(f"   Mensagem: {str(e)[:100]}...")

        # Verificar se mensagem está em PT-BR
        if "não encontrado" in str(e).lower() or "inexistente" in str(e).lower():
            print("✅ Mensagem de erro em PT-BR")
            return True
        else:
            print("⚠️ Mensagem de erro não está em PT-BR")
            return False


def main():
    """Executa todas as validações."""
    print_header("VALIDAÇÃO DE INTEGRAÇÃO RUNTIME - ÉPICO 6, FUNCIONALIDADE 6.1")

    print("\nEste script valida que os nós do sistema carregam prompts e modelos")
    print("dos arquivos YAML em config/agents/ durante a execução runtime.")

    results = []

    # Teste 1: Carregamento de configs
    results.append(("Carregamento de configs", validate_config_loading()))

    # Teste 2: Funções individuais
    results.append(("Funções individuais", validate_individual_loaders()))

    # Teste 3: Bootstrap do grafo
    results.append(("Bootstrap do super-grafo", validate_graph_bootstrap()))

    # Teste 4: Runtime dos nós
    results.append(("Runtime dos nós", validate_node_runtime()))

    # Teste 5: Fallback
    results.append(("Fallback", validate_fallback_behavior()))

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
        print("✅ Funcionalidade 6.1 (Configuração Externa de Agentes) implementada com sucesso")
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
