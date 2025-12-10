"""
Script de validação manual para Estruturador com Refinamento (Épico 4, Checkpoint 3).

Valida que o Estruturador consegue:
1. Estruturar ideia inicial (V1)
2. Receber feedback do Metodologista e refinar (V2)
3. Incrementar refinement_iteration corretamente

Modo de uso:
    python scripts/validate_structurer_refinement.py
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT_STR = str(PROJECT_ROOT)
if PROJECT_ROOT_STR not in sys.path:
    sys.path.insert(0, PROJECT_ROOT_STR)

from scripts.common import setup_project_path

setup_project_path()

from core.agents.orchestrator.state import create_initial_multi_agent_state
from core.agents.structurer.nodes import structurer_node

def validate_structurer_refinement():
    """Valida a implementação do refinamento no Estruturador."""
    print("=" * 70)
    print("VALIDAÇÃO DO ESTRUTURADOR COM REFINAMENTO (Épico 4 - Checkpoint 3)")
    print("=" * 70)

    # =========================================================================
    # TESTE 1: Estruturação inicial (V1)
    # =========================================================================
    print("\n" + "=" * 70)
    print("TESTE 1: Estruturação inicial (V1)")
    print("=" * 70)

    state1 = create_initial_multi_agent_state(
        user_input="Método incremental é mais rápido"
    )

    print(f"\n📝 Input do usuário: {state1['user_input']}")
    print(f"🔢 Iteração inicial: {state1['refinement_iteration']}")
    print(f"📊 Feedback do Metodologista: None (primeira vez)")

    print("\n⏳ Executando structurer_node (modo estruturação)...")
    result1 = structurer_node(state1)

    print("\n✅ RESULTADO:")
    print(f"   Questão V1: {result1['structurer_output']['structured_question']}")
    print(f"   Contexto: {result1['structurer_output']['elements']['context']}")
    print(f"   Próximo estágio: {result1['current_stage']}")

    assert 'structured_question' in result1['structurer_output'], \
        "❌ ERRO: structured_question não encontrada no output"
    assert result1['current_stage'] == 'validating', \
        f"❌ ERRO: current_stage deveria ser 'validating', mas é '{result1['current_stage']}'"

    print("\n✅ Teste 1 passou: Estruturação inicial funciona corretamente")

    # =========================================================================
    # TESTE 2: Refinamento (V2) após feedback do Metodologista
    # =========================================================================
    print("\n" + "=" * 70)
    print("TESTE 2: Refinamento (V2) com feedback do Metodologista")
    print("=" * 70)

    # Simular estado após Metodologista retornar needs_refinement
    state2 = create_initial_multi_agent_state(
        user_input="Método incremental é mais rápido"
    )

    # Aplicar resultado do Estruturador V1
    state2['structurer_output'] = result1['structurer_output']

    # Simular feedback do Metodologista (needs_refinement)
    state2['methodologist_output'] = {
        "status": "needs_refinement",
        "justification": "Ideia central clara, mas falta operacionalização",
        "improvements": [
            {
                "aspect": "população",
                "gap": "Não especificada",
                "suggestion": "Definir população-alvo (ex: equipes de 2-5 devs)"
            },
            {
                "aspect": "métricas",
                "gap": "Velocidade vaga",
                "suggestion": "Operacionalizar (ex: tempo de entrega em dias)"
            }
        ]
    }

    # Simular hypothesis_versions (V1 registrada pelo Metodologista)
    state2['hypothesis_versions'] = [{
        "version": 1,
        "question": result1['structurer_output']['structured_question'],
        "feedback": state2['methodologist_output']
    }]

    print(f"\n📝 Questão V1 (anterior): {state2['hypothesis_versions'][0]['question']}")
    print(f"📊 Feedback do Metodologista:")
    print(f"   Status: {state2['methodologist_output']['status']}")
    print(f"   Gaps identificados: {len(state2['methodologist_output']['improvements'])}")
    for imp in state2['methodologist_output']['improvements']:
        print(f"      - {imp['aspect']}: {imp['gap']}")

    print("\n⏳ Executando structurer_node (modo refinamento)...")
    result2 = structurer_node(state2)

    print("\n✅ RESULTADO:")
    print(f"   Questão V2 (refinada): {result2['structurer_output']['structured_question']}")
    print(f"   Gaps endereçados: {result2['structurer_output'].get('addressed_gaps', [])}")
    print(f"   Iteração: {state2.get('refinement_iteration', 0)} → {result2['refinement_iteration']}")
    print(f"   Próximo estágio: {result2['current_stage']}")

    assert 'structured_question' in result2['structurer_output'], \
        "❌ ERRO: structured_question não encontrada no output refinado"
    assert result2['refinement_iteration'] == 1, \
        f"❌ ERRO: refinement_iteration deveria ser 1, mas é {result2['refinement_iteration']}"
    assert result2['current_stage'] == 'validating', \
        f"❌ ERRO: current_stage deveria ser 'validating', mas é '{result2['current_stage']}'"
    assert 'addressed_gaps' in result2['structurer_output'], \
        "❌ ERRO: addressed_gaps não encontrado no output refinado"

    # Verificar que questão mudou
    v1_question = state2['hypothesis_versions'][0]['question']
    v2_question = result2['structurer_output']['structured_question']
    assert v1_question != v2_question, \
        "❌ ERRO: Questão V2 deveria ser diferente de V1"

    print("\n✅ Teste 2 passou: Refinamento funciona corretamente")

    # =========================================================================
    # RESUMO FINAL
    # =========================================================================
    print("\n" + "=" * 70)
    print("RESUMO DA VALIDAÇÃO")
    print("=" * 70)
    print("✅ Teste 1: Estruturação inicial (V1) - PASSOU")
    print("✅ Teste 2: Refinamento com feedback (V2) - PASSOU")
    print("\n" + "=" * 70)
    print("TODOS OS TESTES PASSARAM! ✅")
    print("=" * 70)
    print("\n📋 Checkpoint 3 (Estruturador com Refinamento) está funcionando!")
    print("🔄 Próximo: Checkpoint 4 (Router + Loop no super-grafo)")

if __name__ == "__main__":
    try:
        validate_structurer_refinement()
    except AssertionError as e:
        print(f"\n❌ ERRO: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERRO INESPERADO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
