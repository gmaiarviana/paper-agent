"""
Script de validação manual do agente Orquestrador.

Este script permite testar manualmente o Orquestrador implementado no Épico 3.1:
- orchestrator_node: Classifica maturidade de inputs do usuário
- route_from_orchestrator: Roteia para agente apropriado

IMPORTANTE: Este script faz chamadas REAIS à API da Anthropic.
Certifique-se de ter configurado ANTHROPIC_API_KEY no arquivo .env

Uso:
    python scripts/validate_orchestrator.py
"""

import os
import sys
import logging
from dotenv import load_dotenv

# Adicionar diretório raiz ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.orchestrator import (
    create_initial_multi_agent_state,
    orchestrator_node,
    route_from_orchestrator
)

# Configurar logging para ver os detalhes
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def print_separator(title=""):
    """Imprime separador visual."""
    if title:
        print(f"\n{'='*80}")
        print(f"  {title}")
        print(f"{'='*80}\n")
    else:
        print(f"\n{'-'*80}\n")


def test_classification_vague():
    """Testa classificação de input vago."""
    print_separator("TESTE 1: CLASSIFICAÇÃO DE INPUT VAGO")

    # Input vago: observação sem estruturação
    user_input = "Observei que desenvolver com Claude Code é mais rápido que métodos tradicionais"

    print(f"Input do usuário: {user_input}\n")

    # Criar estado inicial
    state = create_initial_multi_agent_state(user_input)

    # Executar nó do orquestrador
    result = orchestrator_node(state)

    # Exibir resultados
    print("Resultados:")
    print(f"  Classificação: {result['orchestrator_classification']}")
    print(f"  Reasoning: {result['orchestrator_reasoning']}")
    print(f"  Próximo estágio: {result['current_stage']}")
    print(f"  Mensagens adicionadas: {len(result['messages'])}")

    # Testar router
    state['orchestrator_classification'] = result['orchestrator_classification']
    next_agent = route_from_orchestrator(state)

    print(f"\nDecisão do router: {next_agent}")

    # Validações
    assert result['orchestrator_classification'] in ['vague', 'semi_formed', 'complete'], \
        f"❌ Classificação inválida: {result['orchestrator_classification']}"
    assert result['current_stage'] in ['structuring', 'validating'], \
        f"❌ Estágio inválido: {result['current_stage']}"
    assert next_agent in ['structurer', 'methodologist'], \
        f"❌ Próximo agente inválido: {next_agent}"

    print("\n✅ Teste 1 passou!")


def test_classification_semi_formed():
    """Testa classificação de hipótese semi-formada."""
    print_separator("TESTE 2: CLASSIFICAÇÃO DE HIPÓTESE SEMI-FORMADA")

    # Hipótese parcial: tem ideia central mas falta especificidade
    user_input = "Método incremental melhora o desenvolvimento de sistemas multi-agente"

    print(f"Input do usuário: {user_input}\n")

    # Criar estado inicial
    state = create_initial_multi_agent_state(user_input)

    # Executar nó do orquestrador
    result = orchestrator_node(state)

    # Exibir resultados
    print("Resultados:")
    print(f"  Classificação: {result['orchestrator_classification']}")
    print(f"  Reasoning: {result['orchestrator_reasoning']}")
    print(f"  Próximo estágio: {result['current_stage']}")

    # Testar router
    state['orchestrator_classification'] = result['orchestrator_classification']
    next_agent = route_from_orchestrator(state)

    print(f"\nDecisão do router: {next_agent}")

    # Validações
    assert result['orchestrator_classification'] in ['vague', 'semi_formed', 'complete'], \
        f"❌ Classificação inválida: {result['orchestrator_classification']}"
    assert next_agent in ['structurer', 'methodologist'], \
        f"❌ Próximo agente inválido: {next_agent}"

    print("\n✅ Teste 2 passou!")


def test_classification_complete():
    """Testa classificação de hipótese completa."""
    print_separator("TESTE 3: CLASSIFICAÇÃO DE HIPÓTESE COMPLETA")

    # Hipótese completa: população, variáveis, métricas definidas
    user_input = (
        "Método incremental reduz tempo de implementação de sistemas multi-agente "
        "em 30%, medido por sprints completos (2 semanas), em equipes de 2-5 "
        "desenvolvedores com experiência em LangGraph"
    )

    print(f"Input do usuário: {user_input}\n")

    # Criar estado inicial
    state = create_initial_multi_agent_state(user_input)

    # Executar nó do orquestrador
    result = orchestrator_node(state)

    # Exibir resultados
    print("Resultados:")
    print(f"  Classificação: {result['orchestrator_classification']}")
    print(f"  Reasoning: {result['orchestrator_reasoning']}")
    print(f"  Próximo estágio: {result['current_stage']}")

    # Testar router
    state['orchestrator_classification'] = result['orchestrator_classification']
    next_agent = route_from_orchestrator(state)

    print(f"\nDecisão do router: {next_agent}")

    # Validações
    assert result['orchestrator_classification'] in ['vague', 'semi_formed', 'complete'], \
        f"❌ Classificação inválida: {result['orchestrator_classification']}"
    assert next_agent in ['structurer', 'methodologist'], \
        f"❌ Próximo agente inválido: {next_agent}"

    print("\n✅ Teste 3 passou!")


def test_state_creation():
    """Testa criação do estado multi-agente."""
    print_separator("TESTE 4: CRIAÇÃO DO ESTADO MULTI-AGENTE")

    user_input = "Teste de estado"

    state = create_initial_multi_agent_state(user_input)

    print("Estado inicial criado:")
    print(f"  user_input: {state['user_input']}")
    print(f"  current_stage: {state['current_stage']}")
    print(f"  orchestrator_classification: {state['orchestrator_classification']}")
    print(f"  orchestrator_reasoning: {state['orchestrator_reasoning']}")
    print(f"  structurer_output: {state['structurer_output']}")
    print(f"  methodologist_output: {state['methodologist_output']}")
    print(f"  messages: {state['messages']}")

    # Validações
    assert state['user_input'] == user_input, "❌ user_input incorreto"
    assert state['current_stage'] == "classifying", "❌ current_stage deveria ser 'classifying'"
    assert state['orchestrator_classification'] is None, "❌ orchestrator_classification deveria ser None"
    assert state['orchestrator_reasoning'] is None, "❌ orchestrator_reasoning deveria ser None"
    assert state['structurer_output'] is None, "❌ structurer_output deveria ser None"
    assert state['methodologist_output'] is None, "❌ methodologist_output deveria ser None"
    assert state['messages'] == [], "❌ messages deveria estar vazio"

    print("\n✅ Teste 4 passou!")


def main():
    """Executa todos os testes de validação."""
    # Carregar variáveis de ambiente
    load_dotenv()

    # Verificar se API key está configurada
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("❌ ERRO: ANTHROPIC_API_KEY não está configurada no arquivo .env")
        print("   Configure a chave antes de executar este script.")
        sys.exit(1)

    print("\n" + "="*80)
    print("  VALIDAÇÃO MANUAL DO ORQUESTRADOR - ÉPICO 3.1")
    print("="*80)
    print("\nEste script valida os componentes implementados na funcionalidade 3.1:")
    print("  1. MultiAgentState - Estado compartilhado entre agentes")
    print("  2. orchestrator_node - Nó que classifica maturidade de inputs")
    print("  3. route_from_orchestrator - Router que decide próximo agente")
    print("\n⚠️  IMPORTANTE: Este script faz chamadas REAIS à API da Anthropic")
    print("   e irá consumir tokens. Custo estimado: ~$0.005-0.01\n")

    input("Pressione ENTER para continuar ou Ctrl+C para cancelar...")

    try:
        # Executar testes
        test_state_creation()
        test_classification_vague()
        test_classification_semi_formed()
        test_classification_complete()

        # Resumo final
        print_separator("VALIDAÇÃO CONCLUÍDA")
        print("✅ Todos os testes de validação manual foram executados com sucesso!")
        print("\nResumo dos componentes testados:")
        print("  ✅ MultiAgentState: Criação e estrutura de campos")
        print("  ✅ orchestrator_node: Classificação de 3 tipos de input")
        print("  ✅ route_from_orchestrator: Roteamento para agentes corretos")
        print("\nPróximos passos:")
        print("  1. Execute os testes unitários: pytest tests/unit/test_orchestrator.py -v")
        print("  2. Prossiga para a funcionalidade 3.2 (Estruturador)")
        print("  3. Depois implemente 3.3 (Super-grafo Multi-Agente)")

    except KeyboardInterrupt:
        print("\n\n⚠️  Validação cancelada pelo usuário.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ ERRO durante validação: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
