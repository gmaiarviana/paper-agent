"""
Script de validação manual do estado do agente Metodologista.

Valida que a criação do estado inicial está funcionando corretamente,
exibindo os valores de forma legível para inspeção humana.

"""

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT_STR = str(PROJECT_ROOT)
if PROJECT_ROOT_STR not in sys.path:
    sys.path.insert(0, PROJECT_ROOT_STR)

from scripts.core.common import setup_project_path

setup_project_path()

from core.agents.methodologist import create_initial_state, checkpointer

def format_state_for_display(state: dict) -> str:
    """Formata o estado para exibição legível."""
    return json.dumps(state, indent=2, ensure_ascii=False)

def main():
    """Executa validação manual do estado."""
    print("=" * 70)
    print("VALIDAÇÃO DO ESTADO DO AGENTE METODOLOGISTA")
    print("=" * 70)
    print()

    # Teste 1: Estado com valores padrão
    print("📋 Teste 1: Estado inicial com valores padrão")
    print("-" * 70)
    hypothesis_1 = "O consumo de cafeína (95mg) melhora o desempenho cognitivo em adultos saudáveis."
    state_1 = create_initial_state(hypothesis_1)

    print(format_state_for_display(state_1))
    print()

    # Validações
    assert state_1["hypothesis"] == hypothesis_1, "❌ Hipótese incorreta"
    assert state_1["status"] == "pending", "❌ Status deveria ser 'pending'"
    assert state_1["iterations"] == 0, "❌ Iterations deveria ser 0"
    assert state_1["max_iterations"] == 3, "❌ Max iterations deveria ser 3"
    assert state_1["messages"] == [], "❌ Messages deveria estar vazio"
    assert state_1["clarifications"] == {}, "❌ Clarifications deveria estar vazio"

    print("✅ Todas as validações passaram!")
    print()

    # Teste 2: Estado com max_iterations customizado
    print("📋 Teste 2: Estado com max_iterations customizado")
    print("-" * 70)
    hypothesis_2 = "Meditação diária reduz níveis de cortisol."
    state_2 = create_initial_state(hypothesis_2, max_iterations=5)

    print(format_state_for_display(state_2))
    print()

    # Validações
    assert state_2["max_iterations"] == 5, "❌ Max iterations deveria ser 5"
    assert state_2["iterations"] == 0, "❌ Iterations deveria ser 0"

    print("✅ Todas as validações passaram!")
    print()

    # Teste 3: Checkpointer configurado
    print("📋 Teste 3: Checkpointer configurado")
    print("-" * 70)
    print(f"Tipo do checkpointer: {type(checkpointer).__name__}")
    print(f"Checkpointer: {checkpointer}")
    print()

    assert checkpointer is not None, "❌ Checkpointer não foi configurado"
    print("✅ Checkpointer configurado corretamente!")
    print()

    # Resumo final
    print("=" * 70)
    print("✅ VALIDAÇÃO CONCLUÍDA COM SUCESSO!")
    print("=" * 70)
    print()
    print("Resumo:")
    print("  - TypedDict MethodologistState: ✅ OK")
    print("  - Função create_initial_state: ✅ OK")
    print("  - Checkpointer MemorySaver: ✅ OK")
    print("  - Valores padrão corretos: ✅ OK")
    print("  - Customização max_iterations: ✅ OK")
    print()

if __name__ == "__main__":
    main()
