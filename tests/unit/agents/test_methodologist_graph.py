"""
Script de validação manual para a Funcionalidade 2.5: Construção do Grafo.

Valida que o grafo do Metodologista foi construído corretamente com:
- StateGraph instanciado com MethodologistState
- Nós registrados (analyze, ask_clarification, decide)
- Edges condicionais configurados
- Router funcionando corretamente
- Grafo compilado com MemorySaver checkpointer
- Grafo invocável e executável
"""

import logging
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT_STR = str(PROJECT_ROOT)
if PROJECT_ROOT_STR not in sys.path:
    sys.path.insert(0, PROJECT_ROOT_STR)

from scripts.common import setup_project_path

setup_project_path()
from agents.methodologist import (
    create_methodologist_graph,
    create_initial_state,
    MethodologistState
)

# Configurar logging para ver as decisões do router
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def validate_graph_creation():
    """Valida a criação e estrutura do grafo."""
    print("=" * 70)
    print("VALIDAÇÃO DA FUNCIONALIDADE 2.5: CONSTRUÇÃO DO GRAFO")
    print("=" * 70)

    # Teste 1: Criar o grafo
    print("\n1. Testando criação do grafo...")
    try:
        graph = create_methodologist_graph()
        print("   ✅ Grafo criado com sucesso")
    except Exception as e:
        print(f"   ❌ ERRO ao criar grafo: {e}")
        raise

    # Teste 2: Verificar que o grafo é compilado
    print("\n2. Verificando que o grafo foi compilado...")
    assert graph is not None, "Grafo não foi compilado"
    assert hasattr(graph, 'invoke'), "Grafo não possui método invoke"
    print("   ✅ Grafo foi compilado e é invocável")

    # Teste 3: Verificar estrutura do grafo
    print("\n3. Verificando estrutura do grafo...")
    # O grafo compilado possui um atributo 'nodes' com os nós registrados
    assert hasattr(graph, 'nodes'), "Grafo não possui atributo 'nodes'"
    nodes = graph.nodes
    assert 'analyze' in nodes, "Nó 'analyze' não foi registrado"
    assert 'ask_clarification' in nodes, "Nó 'ask_clarification' não foi registrado"
    assert 'decide' in nodes, "Nó 'decide' não foi registrado"
    print("   ✅ Todos os nós estão registrados: analyze, ask_clarification, decide")

    # Teste 4: Verificar que o grafo possui checkpointer
    print("\n4. Verificando checkpointer...")
    assert graph.checkpointer is not None, "Grafo não possui checkpointer"
    print(f"   ✅ Checkpointer configurado: {type(graph.checkpointer).__name__}")

    print("\n" + "=" * 70)
    print("VALIDAÇÃO ESTRUTURAL CONCLUÍDA COM SUCESSO! ✅")
    print("=" * 70)

def validate_graph_execution_simulation():
    """
    Simula a execução do grafo sem fazer chamadas à API.
    Valida apenas a lógica de roteamento.
    """
    print("\n" + "=" * 70)
    print("SIMULAÇÃO DE EXECUÇÃO (SEM API)")
    print("=" * 70)

    from agents.methodologist.router import route_after_analyze

    # Teste 5: Router - cenário 1 (precisa de clarificação, iterations < max)
    print("\n5. Testando router: needs_clarification=True, iterations=0/3...")
    state1 = create_initial_state("Test hypothesis", max_iterations=3)
    state1['needs_clarification'] = True
    state1['iterations'] = 0
    next_node = route_after_analyze(state1)
    assert next_node == "ask_clarification", f"Router deveria retornar 'ask_clarification', mas retornou '{next_node}'"
    print(f"   ✅ Router decidiu corretamente: {next_node}")

    # Teste 6: Router - cenário 2 (não precisa de clarificação)
    print("\n6. Testando router: needs_clarification=False, iterations=1/3...")
    state2 = create_initial_state("Test hypothesis", max_iterations=3)
    state2['needs_clarification'] = False
    state2['iterations'] = 1
    next_node = route_after_analyze(state2)
    assert next_node == "decide", f"Router deveria retornar 'decide', mas retornou '{next_node}'"
    print(f"   ✅ Router decidiu corretamente: {next_node}")

    # Teste 7: Router - cenário 3 (iterations >= max_iterations)
    print("\n7. Testando router: needs_clarification=True, iterations=3/3 (limite atingido)...")
    state3 = create_initial_state("Test hypothesis", max_iterations=3)
    state3['needs_clarification'] = True
    state3['iterations'] = 3
    next_node = route_after_analyze(state3)
    assert next_node == "decide", f"Router deveria retornar 'decide' (limite atingido), mas retornou '{next_node}'"
    print(f"   ✅ Router decidiu corretamente: {next_node} (forçou decisão após limite)")

    print("\n" + "=" * 70)
    print("SIMULAÇÃO DE ROTEAMENTO CONCLUÍDA COM SUCESSO! ✅")
    print("=" * 70)

def show_next_steps():
    """Mostra próximos passos para teste completo com API."""
    print("\n" + "=" * 70)
    print("PRÓXIMOS PASSOS")
    print("=" * 70)
    print("""
Este script validou a estrutura e lógica de roteamento do grafo.

Para testar a execução completa com chamadas à API real:
1. Garanta que ANTHROPIC_API_KEY está configurada no .env
2. Execute o teste de integração (Funcionalidade 2.8):

   python -m pytest tests/integration/test_methodologist_smoke.py -v

3. Ou teste manualmente via CLI (Funcionalidade 2.7):

   python cli/chat.py

Observações:
- O grafo foi construído com modelo: claude-3-5-haiku-20241022
- Checkpointer: MemorySaver (persistência em memória)
- Limite padrão: 3 iterações (perguntas ao usuário)
- Router implementa lógica condicional: analyze → ask_clarification | decide
""")

if __name__ == "__main__":
    try:
        validate_graph_creation()
        validate_graph_execution_simulation()
        show_next_steps()

        print("\n" + "=" * 70)
        print("✅ TODOS OS TESTES DE VALIDAÇÃO PASSARAM!")
        print("=" * 70)

    except AssertionError as e:
        print(f"\n❌ ERRO DE VALIDAÇÃO: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERRO INESPERADO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
