"""
Script de validação manual para o fluxo completo multi-agente.

Valida que o super-grafo multi-agente foi implementado corretamente com:
- Integração entre Orquestrador, Estruturador e Metodologista
- Fluxo completo: ideia vaga → estruturação → validação
- Fluxo direto: hipótese → validação
- Preservação de contexto entre agentes via MultiAgentState
- Logs de decisões e transições

Versão: 1.0 (Épico 3, Funcionalidade 3.3)
Data: 11/11/2025
"""

import sys
import os
from pathlib import Path
import logging

# Adicionar o diretório raiz ao PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Carregar variáveis de ambiente do .env
from dotenv import load_dotenv
load_dotenv()

# Configurar logging para ver decisões e transições
logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - %(levelname)s - %(message)s'
)

# Importar módulos necessários
from agents.multi_agent_graph import create_multi_agent_graph, create_initial_multi_agent_state


def print_separator(title: str):
    """Imprime separador visual."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def print_result(result: dict):
    """Imprime resultado de forma estruturada."""
    print(f"\n{'─' * 80}")
    print("RESULTADO FINAL:")
    print(f"{'─' * 80}")

    print(f"\n📊 Estágio: {result['current_stage']}")

    if result.get('orchestrator_classification'):
        print(f"\n🎯 ORQUESTRADOR:")
        print(f"   Classificação: {result['orchestrator_classification']}")
        print(f"   Reasoning: {result['orchestrator_reasoning']}")

    if result.get('structurer_output'):
        print(f"\n🏗️  ESTRUTURADOR:")
        structurer = result['structurer_output']
        print(f"   Questão estruturada: {structurer['structured_question']}")
        print(f"   Contexto: {structurer['elements']['context']}")
        print(f"   Problema: {structurer['elements']['problem']}")
        print(f"   Contribuição: {structurer['elements']['contribution']}")

    if result.get('methodologist_output'):
        print(f"\n🔬 METODOLOGISTA:")
        methodologist = result['methodologist_output']
        print(f"   Status: {methodologist['status'].upper()}")
        print(f"   Justificativa: {methodologist['justification']}")
        if methodologist.get('clarifications'):
            print(f"   Clarificações coletadas: {len(methodologist['clarifications'])}")
            for q, a in methodologist['clarifications'].items():
                print(f"     - P: {q}")
                print(f"       R: {a}")

    print(f"\n{'─' * 80}\n")


def validate_scenario_1_vague_idea():
    """
    Cenário 1: Ideia vaga → Estruturador → Metodologista

    Input: Observação empírica sem estruturação
    Esperado:
    - Orquestrador classifica como "vague"
    - Estruturador organiza em questão de pesquisa
    - Metodologista valida (provavelmente rejeita por falta de especificidade)
    - Contexto preservado entre agentes
    """
    print_separator("CENÁRIO 1: Ideia Vaga → Estruturador → Metodologista")

    user_input = "Observei que desenvolver com Claude Code é muito mais rápido do que sem IA"
    print(f"📝 Input do usuário: {user_input}\n")

    # Criar estado inicial
    state = create_initial_multi_agent_state(user_input)

    # Criar e executar super-grafo
    graph = create_multi_agent_graph()
    result = graph.invoke(
        state,
        config={"configurable": {"thread_id": "validation-scenario-1"}}
    )

    # Validar resultado
    print_result(result)

    # Asserções
    assert result['orchestrator_classification'] == 'vague', \
        f"❌ Orquestrador deveria classificar como 'vague', mas classificou como '{result['orchestrator_classification']}'"
    print("   ✅ Orquestrador classificou corretamente como 'vague'")

    assert result['structurer_output'] is not None, \
        "❌ Estruturador deveria ter gerado output"
    print("   ✅ Estruturador gerou questão estruturada")

    assert result['methodologist_output'] is not None, \
        "❌ Metodologista deveria ter gerado output"
    print("   ✅ Metodologista avaliou a questão estruturada")

    assert result['current_stage'] == 'done', \
        f"❌ Estágio final deveria ser 'done', mas é '{result['current_stage']}'"
    print("   ✅ Fluxo completo executado (stage = 'done')")

    print("\n✅ CENÁRIO 1 VALIDADO COM SUCESSO!\n")
    return result


def validate_scenario_2_semi_formed():
    """
    Cenário 2: Hipótese semi-formada → Metodologista direto

    Input: Hipótese com ideia central mas falta especificidade
    Esperado:
    - Orquestrador classifica como "semi_formed"
    - Metodologista recebe direto (sem Estruturador)
    - Metodologista valida (provavelmente rejeita por falta de operacionalização)
    """
    print_separator("CENÁRIO 2: Hipótese Semi-Formada → Metodologista Direto")

    user_input = "Método incremental melhora o desenvolvimento de sistemas multi-agente"
    print(f"📝 Input do usuário: {user_input}\n")

    # Criar estado inicial
    state = create_initial_multi_agent_state(user_input)

    # Criar e executar super-grafo
    graph = create_multi_agent_graph()
    result = graph.invoke(
        state,
        config={"configurable": {"thread_id": "validation-scenario-2"}}
    )

    # Validar resultado
    print_result(result)

    # Asserções
    assert result['orchestrator_classification'] == 'semi_formed', \
        f"❌ Orquestrador deveria classificar como 'semi_formed', mas classificou como '{result['orchestrator_classification']}'"
    print("   ✅ Orquestrador classificou corretamente como 'semi_formed'")

    assert result['structurer_output'] is None, \
        "❌ Estruturador NÃO deveria ter sido executado (fluxo direto)"
    print("   ✅ Estruturador não foi executado (fluxo direto)")

    assert result['methodologist_output'] is not None, \
        "❌ Metodologista deveria ter gerado output"
    print("   ✅ Metodologista avaliou a hipótese diretamente")

    assert result['current_stage'] == 'done', \
        f"❌ Estágio final deveria ser 'done', mas é '{result['current_stage']}'"
    print("   ✅ Fluxo direto executado (stage = 'done')")

    print("\n✅ CENÁRIO 2 VALIDADO COM SUCESSO!\n")
    return result


def validate_scenario_3_complete():
    """
    Cenário 3: Hipótese completa → Metodologista direto

    Input: Hipótese com população, variáveis e métricas bem definidas
    Esperado:
    - Orquestrador classifica como "complete"
    - Metodologista recebe direto (sem Estruturador)
    - Metodologista aprova (ou rejeita com justificativa clara)
    """
    print_separator("CENÁRIO 3: Hipótese Completa → Metodologista Direto")

    user_input = (
        "Método incremental reduz tempo de implementação de sistemas multi-agente "
        "em 30%, medido em sprints de 2 semanas, em equipes de 2-5 desenvolvedores, "
        "comparado com método waterfall tradicional"
    )
    print(f"📝 Input do usuário: {user_input}\n")

    # Criar estado inicial
    state = create_initial_multi_agent_state(user_input)

    # Criar e executar super-grafo
    graph = create_multi_agent_graph()
    result = graph.invoke(
        state,
        config={"configurable": {"thread_id": "validation-scenario-3"}}
    )

    # Validar resultado
    print_result(result)

    # Asserções
    assert result['orchestrator_classification'] == 'complete', \
        f"❌ Orquestrador deveria classificar como 'complete', mas classificou como '{result['orchestrator_classification']}'"
    print("   ✅ Orquestrador classificou corretamente como 'complete'")

    assert result['structurer_output'] is None, \
        "❌ Estruturador NÃO deveria ter sido executado (fluxo direto)"
    print("   ✅ Estruturador não foi executado (fluxo direto)")

    assert result['methodologist_output'] is not None, \
        "❌ Metodologista deveria ter gerado output"
    print("   ✅ Metodologista avaliou a hipótese diretamente")

    assert result['current_stage'] == 'done', \
        f"❌ Estágio final deveria ser 'done', mas é '{result['current_stage']}'"
    print("   ✅ Fluxo direto executado (stage = 'done')")

    # Esta hipótese tem boa chance de ser aprovada
    if result['methodologist_output']['status'] == 'approved':
        print("   ✅ Metodologista aprovou a hipótese completa!")
    else:
        print(f"   ℹ️  Metodologista rejeitou (justificativa: {result['methodologist_output']['justification']})")

    print("\n✅ CENÁRIO 3 VALIDADO COM SUCESSO!\n")
    return result


def main():
    """Executa todos os cenários de validação."""
    print("\n" + "=" * 80)
    print("  VALIDAÇÃO DO SUPER-GRAFO MULTI-AGENTE")
    print("  Épico 3 - Funcionalidade 3.3: Integração Multi-Agente")
    print("=" * 80)

    try:
        # Validar cenário 1: Ideia vaga
        result1 = validate_scenario_1_vague_idea()

        # Validar cenário 2: Hipótese semi-formada
        result2 = validate_scenario_2_semi_formed()

        # Validar cenário 3: Hipótese completa
        result3 = validate_scenario_3_complete()

        # Resumo final
        print_separator("RESUMO FINAL")
        print("✅ Cenário 1: Ideia vaga → Estruturador → Metodologista")
        print("✅ Cenário 2: Hipótese semi-formada → Metodologista direto")
        print("✅ Cenário 3: Hipótese completa → Metodologista direto")
        print("\n" + "=" * 80)
        print("  TODOS OS CENÁRIOS VALIDADOS COM SUCESSO! ✅")
        print("=" * 80 + "\n")

        return 0

    except AssertionError as e:
        print(f"\n❌ ERRO DE VALIDAÇÃO: {e}\n")
        return 1
    except Exception as e:
        print(f"\n❌ ERRO INESPERADO: {e}\n")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
