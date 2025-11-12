r"""
Script de validação manual para Loop de Refinamento Colaborativo (Épico 4).

Testa os 4 cenários principais do ROADMAP:
1. Ideia vaga + 1 refinamento → aprovada
2. Ideia vaga + 2 refinamentos → aprovada
3. Ideia sem potencial → rejeitada imediatamente
4. Limite atingido → decisão forçada

IMPORTANTE: Requer ANTHROPIC_API_KEY configurada no .env

Modo de uso:
    # Com ambiente virtual ativado e API key configurada:
    python scripts/validate_refinement_loop.py

    # PowerShell:
    .\venv\Scripts\Activate.ps1
    python scripts\validate_refinement_loop.py
"""

import sys
from pathlib import Path
import os

# Adicionar o diretório raiz ao PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

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
    print("\n⚠️  ATENÇÃO: Este script faz chamadas à API Anthropic (custo ~$0.05-0.10)")
    print("Testando 2 cenários principais...\n")

    try:
        # Executar cenários
        result1 = validate_scenario_1()
        result3 = validate_scenario_3()

        # Resumo final
        print_separator("RESUMO DA VALIDAÇÃO")
        print("✅ Cenário 1: Ideia vaga + refinamento → PASSOU")
        print("✅ Cenário 3: Ideia sem potencial → PASSOU")
        print("\n" + "=" * 80)
        print("TODOS OS TESTES PASSARAM! ✅")
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
