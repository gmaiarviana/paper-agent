"""
Script de validação manual dos nós do grafo do Metodologista.

Este script permite testar manualmente os 3 nós implementados:
- analyze: Avalia hipótese e decide se precisa de clarificações
- ask_clarification: Solicita informação ao usuário
- decide: Toma decisão final sobre a hipótese

IMPORTANTE: Este script faz chamadas REAIS à API da Anthropic.
Certifique-se de ter configurado ANTHROPIC_API_KEY no arquivo .env

Uso:
    python scripts/validate_graph_nodes.py
"""

import sys
import logging
from pathlib import Path
from dotenv import load_dotenv

# Adicionar diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.methodologist import create_initial_state
from agents.methodologist.nodes import (
    analyze,
    ask_clarification,
    decide
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


def test_analyze_node():
    """Testa o nó analyze com hipóteses diferentes."""
    print_separator("TESTE 1: NÓ ANALYZE")

    # Teste 1a: Hipótese vaga (deve precisar de clarificação)
    print("Teste 1a: Hipótese vaga")
    state = create_initial_state("Café aumenta produtividade")
    result = analyze(state)

    print(f"✓ Hipótese: {state['hypothesis']}")
    print(f"✓ Needs clarification: {result['needs_clarification']}")
    print(f"✓ Mensagens adicionadas: {len(result['messages'])}")

    print_separator()

    # Teste 1b: Hipótese bem especificada (não deve precisar de clarificação)
    print("Teste 1b: Hipótese bem especificada")
    state = create_initial_state(
        "O consumo de 200mg de cafeína melhora o tempo de reação em tarefas de atenção "
        "sustentada (teste PVT) em 10% ± 5%, medido 30-60 minutos após ingestão, "
        "em adultos de 18-40 anos sem tolerância à cafeína."
    )
    result = analyze(state)

    print(f"✓ Hipótese: {state['hypothesis'][:80]}...")
    print(f"✓ Needs clarification: {result['needs_clarification']}")
    print(f"✓ Mensagens adicionadas: {len(result['messages'])}")


def test_ask_clarification_node():
    """Testa o nó ask_clarification (modo simulado)."""
    print_separator("TESTE 2: NÓ ASK_CLARIFICATION (SIMULADO)")

    print("NOTA: Este teste usa mock para ask_user, pois não podemos")
    print("fazer input interativo em script de validação.\n")

    from unittest.mock import patch

    state = create_initial_state("Café aumenta produtividade")

    # Simular resposta do usuário
    with patch('agents.methodologist.nodes.ask_user', return_value="Adultos de 18-40 anos sem histórico de doenças cardiovasculares"):
        result = ask_clarification(state)

    print(f"✓ Hipótese: {state['hypothesis']}")
    print(f"✓ Iterações antes: {state['iterations']}")
    print(f"✓ Iterações depois: {result['iterations']}")
    print(f"✓ Clarificações registradas: {len(result['clarifications'])}")

    if result['clarifications']:
        print("\nClarificações:")
        for question, answer in result['clarifications'].items():
            print(f"  - P: {question}")
            print(f"    R: {answer}")


def test_decide_node():
    """Testa o nó decide com hipóteses diferentes."""
    print_separator("TESTE 3: NÓ DECIDE")

    # Teste 3a: Hipótese boa
    print("Teste 3a: Hipótese bem formulada (deve aprovar)")
    state = create_initial_state(
        "O consumo de 200mg de cafeína melhora o tempo de reação em tarefas de atenção "
        "sustentada (teste PVT) em 10% ± 5%, medido 30-60 minutos após ingestão, "
        "em adultos de 18-40 anos sem tolerância à cafeína."
    )
    result = decide(state)

    print(f"✓ Hipótese: {state['hypothesis'][:80]}...")
    print(f"✓ Status: {result['status']}")
    print(f"✓ Justificativa: {result['justification'][:200]}...")

    print_separator()

    # Teste 3b: Hipótese ruim
    print("Teste 3b: Hipótese mal formulada (deve rejeitar)")
    state = create_initial_state("Café faz bem para o cérebro")
    result = decide(state)

    print(f"✓ Hipótese: {state['hypothesis']}")
    print(f"✓ Status: {result['status']}")
    print(f"✓ Justificativa: {result['justification'][:200]}...")

    print_separator()

    # Teste 3c: Hipótese com clarificações
    print("Teste 3c: Hipótese vaga mas com clarificações (pode aprovar)")
    state = create_initial_state("Café aumenta produtividade")
    state['clarifications'] = {
        "Qual é a população-alvo?": "Adultos de 18-40 anos",
        "Quais métricas serão usadas?": "Tempo de reação no teste PVT",
        "Qual a dose de cafeína?": "200mg"
    }
    result = decide(state)

    print(f"✓ Hipótese: {state['hypothesis']}")
    print(f"✓ Clarificações fornecidas: {len(state['clarifications'])}")
    print(f"✓ Status: {result['status']}")
    print(f"✓ Justificativa: {result['justification'][:200]}...")


def test_max_iterations_limit():
    """Testa que ask_clarification respeita o limite de iterações."""
    print_separator("TESTE 4: LIMITE DE ITERAÇÕES")

    state = create_initial_state("Café aumenta produtividade", max_iterations=3)
    state['iterations'] = 3  # Já atingiu o limite

    from unittest.mock import patch
    with patch('agents.methodologist.nodes.ask_user') as mock_ask:
        result = ask_clarification(state)

    print(f"✓ Max iterations: {state['max_iterations']}")
    print(f"✓ Current iterations: {state['iterations']}")
    print(f"✓ ask_user foi chamado? {mock_ask.called}")
    print(f"✓ Mensagem retornada: {result['messages'][0].content}")


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
    print("  VALIDAÇÃO MANUAL DOS NÓS DO GRAFO - METODOLOGISTA")
    print("="*80)
    print("\nEste script valida os 3 nós implementados na funcionalidade 2.4:")
    print("  1. analyze - Avalia hipótese e decide se precisa de clarificações")
    print("  2. ask_clarification - Solicita informação ao usuário")
    print("  3. decide - Toma decisão final sobre a hipótese")
    print("\n⚠️  IMPORTANTE: Este script faz chamadas REAIS à API da Anthropic")
    print("   e irá consumir tokens. Custo estimado: ~$0.01-0.02\n")

    input("Pressione ENTER para continuar ou Ctrl+C para cancelar...")

    try:
        # Executar testes
        test_analyze_node()
        test_ask_clarification_node()
        test_decide_node()
        test_max_iterations_limit()

        # Resumo final
        print_separator("VALIDAÇÃO CONCLUÍDA")
        print("✅ Todos os testes de validação manual foram executados com sucesso!")
        print("\nPróximos passos:")
        print("  1. Execute os testes unitários: pytest tests/unit/test_graph_nodes.py -v")
        print("  2. Revise os logs para verificar o comportamento dos nós")
        print("  3. Prossiga para a funcionalidade 2.5 (Construção do Grafo)")

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
