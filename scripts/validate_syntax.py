#!/usr/bin/env python3
"""
Script para validar sintaxe dos módulos modificados.

Testa que todos os módulos podem ser importados sem erros.
"""

import sys
from pathlib import Path

# Adicionar o diretório raiz ao PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_import(module_path: str, description: str):
    """Tenta importar um módulo e reporta resultado."""
    try:
        __import__(module_path)
        print(f"✅ {description}: OK")
        return True
    except Exception as e:
        print(f"❌ {description}: FALHOU")
        print(f"   Erro: {e}")
        return False


def main():
    """Valida imports dos módulos modificados."""
    print("=" * 80)
    print("  VALIDAÇÃO DE SINTAXE - Módulos Modificados (Épico 6.1)")
    print("=" * 80)
    print()

    results = []

    # Módulos modificados
    results.append(test_import(
        "agents.orchestrator.nodes",
        "agents/orchestrator/nodes.py (Orquestrador)"
    ))

    results.append(test_import(
        "agents.structurer.nodes",
        "agents/structurer/nodes.py (Estruturador)"
    ))

    results.append(test_import(
        "agents.methodologist.nodes",
        "agents/methodologist/nodes.py (Metodologista)"
    ))

    results.append(test_import(
        "agents.multi_agent_graph",
        "agents/multi_agent_graph.py (Super-grafo)"
    ))

    results.append(test_import(
        "agents.memory.config_loader",
        "agents/memory/config_loader.py (Config Loader)"
    ))

    results.append(test_import(
        "agents.memory.config_validator",
        "agents/memory/config_validator.py (Config Validator)"
    ))

    print()
    print("=" * 80)

    passed = sum(results)
    total = len(results)

    if passed == total:
        print(f"✅ TODOS OS {total} MÓDULOS VALIDADOS COM SUCESSO!")
        print("✅ Nenhum erro de sintaxe ou import encontrado")
        return 0
    else:
        print(f"❌ {total - passed} de {total} módulos falharam")
        print("⚠️ Corrija os erros acima antes de continuar")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
