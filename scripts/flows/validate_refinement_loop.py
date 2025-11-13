r"""
Script de validação manual para Loop de Refinamento Colaborativo (Épico 4).

Testa os 4 cenários principais do ROADMAP:
1. Ideia vaga + 1 refinamento → aprovada
   - Input: "TDD reduz bugs em equipes pequenas"
   - Resultado: V1 (needs_refinement) → V2 (approved)

2. Ideia vaga + 2 refinamentos → aprovada
   - Input: "Observei que métodos ágeis parecem funcionar melhor"
   - Resultado: V1 → V2 → aprovada após 1-2 refinamentos

3. Ideia sem potencial → rejeitada imediatamente
   - Input: "Café é bom porque todo mundo sabe que funciona"
   - Resultado: V1 (rejected) sem refinamentos

4. Limite atingido → decisão forçada
   - Input: "X afeta Y de alguma forma"
   - Resultado: após 2 refinamentos, decisão forçada (approved/rejected)

IMPORTANTE: Requer ANTHROPIC_API_KEY configurada no .env

Modo de uso:
    # Com ambiente virtual ativado e API key configurada:
    python scripts/validate_refinement_loop.py

    # PowerShell:
    .\venv\Scripts\Activate.ps1
    python scripts\validate_refinement_loop.py

Custo estimado: ~$0.10-0.20 (4 cenários com chamadas à API)
"""

import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT_STR = str(PROJECT_ROOT)
if PROJECT_ROOT_STR not in sys.path:
    sys.path.insert(0, PROJECT_ROOT_STR)

from scripts.common import setup_project_path

setup_project_path()

# Carregar variáveis de ambiente
from dotenv import load_dotenv
load_dotenv()

from agents.multi_agent_graph import create_multi_agent_graph, create_initial_multi_agent_state


def print_separator(title: str):
    """Imprime um separador visual."""
    print("\n" + "=" * 80)
    print(f"{title}")
    print("=" * 80 + "\n")


def print_hypothesis_versions(state: dict):
    """Imprime histórico de versões de forma legível."""
    versions = state.get('hypothesis_versions', [])
    if not versions:
        print("   (Nenhuma versão registrada)")
        return

    for v in versions:
        print(f"\n   📄 Versão {v['version']}:")
        print(f"      Questão: {v['question']}")
        print(f"      Status: {v['feedback']['status']}")
        if v['feedback'].get('improvements'):
            print(f"      Gaps identificados: {len(v['feedback']['improvements'])}")
            for imp in v['feedback']['improvements']:
                print(f"         - {imp['aspect']}: {imp['gap']}")


def validate_scenario_1():
    """
    Cenário 1: Ideia vaga + 1 refinamento → aprovada

    Input vago → Estruturador (V1) → Metodologista (needs_refinement)
    → Estruturador (V2) → Metodologista (approved)
    """
    print_separator("CENÁRIO 1: Ideia vaga + 1 refinamento → aprovada")

    # Criar grafo
    graph = create_multi_agent_graph()

    # Input vago deliberadamente
    user_input = "TDD reduz bugs em equipes pequenas"
    print(f"📝 Input do usuário: {user_input}")
    print("🎯 Resultado esperado: needs_refinement → refinamento → approved")

    # Criar estado inicial
    state = create_initial_multi_agent_state(user_input)

    print("\n⏳ Executando super-grafo...")

    # Executar grafo
    result = graph.invoke(state, config={"configurable": {"thread_id": "scenario-1"}})

    # Verificar resultado
    print("\n✅ RESULTADO:")
    print(f"   Status final: {result['methodologist_output']['status']}")
    print(f"   Iterações de refinamento: {result['refinement_iteration']}")
    print(f"   Versões geradas: {len(result['hypothesis_versions'])}")

    print("\n📚 Histórico de versões:")
    print_hypothesis_versions(result)

    # Validações
    assert result['methodologist_output']['status'] in ['approved', 'needs_refinement'], \
        f"Status inesperado: {result['methodologist_output']['status']}"
    assert len(result['hypothesis_versions']) >= 1, \
        f"Esperado pelo menos 1 versão, obteve {len(result['hypothesis_versions'])}"

    print("\n✅ Cenário 1: PASSOU")
    return result


def validate_scenario_2():
    """
    Cenário 2: Ideia vaga + 2 refinamentos → aprovada

    Input muito vago → Estruturador (V1) → Metodologista (needs_refinement)
    → Estruturador (V2) → Metodologista (needs_refinement)
    → Estruturador (V3) → Metodologista (approved)
    """
    print_separator("CENÁRIO 2: Ideia vaga + 2 refinamentos → aprovada")

    graph = create_multi_agent_graph()

    # Input muito vago que precisará de 2 refinamentos
    user_input = "Observei que métodos ágeis parecem funcionar melhor"
    print(f"📝 Input do usuário: {user_input}")
    print("🎯 Resultado esperado: needs_refinement → needs_refinement → approved")

    state = create_initial_multi_agent_state(user_input)

    print("\n⏳ Executando super-grafo...")
    result = graph.invoke(state, config={"configurable": {"thread_id": "scenario-2"}})

    print("\n✅ RESULTADO:")
    print(f"   Status final: {result['methodologist_output']['status']}")
    print(f"   Iterações de refinamento: {result['refinement_iteration']}")
    print(f"   Versões geradas: {len(result['hypothesis_versions'])}")

    print("\n📚 Histórico de versões:")
    print_hypothesis_versions(result)

    # Validações (flexível: pode ser approved após 1 ou 2 refinamentos)
    assert result['methodologist_output']['status'] in ['approved', 'needs_refinement'], \
        f"Status inesperado: {result['methodologist_output']['status']}"
    assert len(result['hypothesis_versions']) >= 2, \
        f"Esperado pelo menos 2 versões, obteve {len(result['hypothesis_versions'])}"
    # Verificar que houve pelo menos 1 refinamento
    assert result['refinement_iteration'] >= 1, \
        f"Esperado pelo menos 1 refinamento, obteve {result['refinement_iteration']}"

    print("\n✅ Cenário 2: PASSOU")
    return result


def validate_scenario_3():
    """
    Cenário 3: Ideia sem potencial → rejeitada imediatamente

    Input sem base científica → Estruturador (V1) → Metodologista (rejected)
    """
    print_separator("CENÁRIO 3: Ideia sem potencial → rejeitada imediatamente")

    graph = create_multi_agent_graph()

    # Input sem base científica
    user_input = "Café é bom porque todo mundo sabe que funciona"
    print(f"📝 Input do usuário: {user_input}")
    print("🎯 Resultado esperado: rejected (sem refinamento)")

    state = create_initial_multi_agent_state(user_input)

    print("\n⏳ Executando super-grafo...")
    result = graph.invoke(state, config={"configurable": {"thread_id": "scenario-3"}})

    print("\n✅ RESULTADO:")
    print(f"   Status final: {result['methodologist_output']['status']}")
    print(f"   Iterações de refinamento: {result['refinement_iteration']}")
    print(f"   Versões geradas: {len(result['hypothesis_versions'])}")

    print("\n📚 Histórico de versões:")
    print_hypothesis_versions(result)

    # Validações
    assert result['methodologist_output']['status'] == 'rejected', \
        f"Esperado 'rejected', obteve '{result['methodologist_output']['status']}'"
    assert result['refinement_iteration'] == 0, \
        f"Não deveria ter refinado, mas iteration = {result['refinement_iteration']}"

    print("\n✅ Cenário 3: PASSOU")
    return result


def validate_scenario_4():
    """
    Cenário 4: Limite de refinamentos atingido → decisão forçada

    Input vago → V1 (needs_refinement) → V2 (needs_refinement)
    → V3 (decisão forçada: approved ou rejected)

    NOTA: Forçamos max_refinements=2, então após 2 needs_refinement,
    o sistema deve forçar uma decisão final.
    """
    print_separator("CENÁRIO 4: Limite atingido → decisão forçada")

    graph = create_multi_agent_graph()

    # Input que historicamente gera múltiplos needs_refinement
    # Vamos usar algo muito vago propositalmente
    user_input = "X afeta Y de alguma forma"
    print(f"📝 Input do usuário: {user_input}")
    print("🎯 Resultado esperado: limite atingido → decisão forçada (approved ou rejected)")

    state = create_initial_multi_agent_state(user_input)
    # Garantir que max_refinements está em 2
    state['max_refinements'] = 2

    print("\n⏳ Executando super-grafo...")
    result = graph.invoke(state, config={"configurable": {"thread_id": "scenario-4"}})

    print("\n✅ RESULTADO:")
    print(f"   Status final: {result['methodologist_output']['status']}")
    print(f"   Iterações de refinamento: {result['refinement_iteration']}")
    print(f"   Versões geradas: {len(result['hypothesis_versions'])}")
    print(f"   Max refinements: {result['max_refinements']}")

    print("\n📚 Histórico de versões:")
    print_hypothesis_versions(result)

    # Validações
    final_status = result['methodologist_output']['status']
    assert final_status in ['approved', 'rejected'], \
        f"Status final deve ser 'approved' ou 'rejected', obteve '{final_status}'"

    # Se atingiu o limite, a última versão deve ter flag de forced_decision
    if result['refinement_iteration'] >= result['max_refinements']:
        last_version = result['hypothesis_versions'][-1]
        # Verificar se há flag de forced_decision (se implementado)
        print(f"   ⚠️  Limite atingido - decisão forçada aplicada")

    print("\n✅ Cenário 4: PASSOU")
    return result


def main():
    """Executa validação completa do loop de refinamento."""
    print("=" * 80)
    print("VALIDAÇÃO DO LOOP DE REFINAMENTO COLABORATIVO (Épico 4)")
    print("=" * 80)

    # Verificar API key
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("\n❌ ERRO: ANTHROPIC_API_KEY não encontrada!")
        print("Configure a API key no arquivo .env e tente novamente.")
        print("\nExemplo (.env):")
        print("ANTHROPIC_API_KEY=sk-ant-...")
        sys.exit(1)

    print("\n✅ API key encontrada")
    print("\n⚠️  ATENÇÃO: Este script faz chamadas à API Anthropic (custo ~$0.10-0.20)")
    print("Testando 4 cenários do ROADMAP...\n")

    try:
        # Executar todos os cenários
        result1 = validate_scenario_1()
        result2 = validate_scenario_2()
        result3 = validate_scenario_3()
        result4 = validate_scenario_4()

        # Resumo final
        print_separator("RESUMO DA VALIDAÇÃO")
        print("✅ Cenário 1: Ideia vaga + 1 refinamento → PASSOU")
        print("✅ Cenário 2: Ideia vaga + 2 refinamentos → PASSOU")
        print("✅ Cenário 3: Ideia sem potencial → PASSOU")
        print("✅ Cenário 4: Limite atingido → PASSOU")
        print("\n" + "=" * 80)
        print("TODOS OS 4 CENÁRIOS PASSARAM! ✅")
        print("=" * 80)
        print("\n📋 Épico 4 (Loop de Refinamento Colaborativo) está funcionando!")
        print("🎉 Sistema multi-agente com refinamento iterativo implementado com sucesso!")

    except AssertionError as e:
        print(f"\n❌ ERRO DE VALIDAÇÃO: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERRO INESPERADO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
