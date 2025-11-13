"""
Script de diagnóstico para debugar o super-grafo multi-agente.

Testa cada componente isoladamente e depois integrado.
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

print("=" * 80)
print("DIAGNÓSTICO DO SUPER-GRAFO MULTI-AGENTE")
print("=" * 80)

# Teste 1: Verificar variável de ambiente
print("\n1. Verificando ANTHROPIC_API_KEY...")
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")
if api_key:
    print(f"   ✅ API key encontrada (primeiros 10 chars: {api_key[:10]}...)")
else:
    print("   ❌ API key NÃO encontrada")
    sys.exit(1)

# Teste 2: Testar LLM diretamente
print("\n2. Testando LLM diretamente...")
try:
    from langchain_anthropic import ChatAnthropic
    from langchain_core.messages import HumanMessage
    from utils.config import get_anthropic_model

    llm = ChatAnthropic(model=get_anthropic_model(), temperature=0)
    response = llm.invoke([HumanMessage(content="Responda apenas: OK")])
    print(f"   ✅ LLM funcionando: {response.content}")
except Exception as e:
    print(f"   ❌ Erro ao testar LLM: {e}")
    sys.exit(1)

# Teste 3: Testar orchestrator_node isolado
print("\n3. Testando orchestrator_node isolado...")
try:
    from agents.orchestrator.state import create_initial_multi_agent_state
    from agents.orchestrator.nodes import orchestrator_node

    state = create_initial_multi_agent_state("Teste simples")
    result = orchestrator_node(state)
    print(f"   ✅ Orchestrator funcionando: classificação = {result['orchestrator_classification']}")
except Exception as e:
    print(f"   ❌ Erro no orchestrator: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Teste 4: Testar structurer_node isolado
print("\n4. Testando structurer_node isolado...")
try:
    from agents.structurer.nodes import structurer_node

    state = create_initial_multi_agent_state("Observei algo interessante")
    result = structurer_node(state)
    print(f"   ✅ Structurer funcionando: questão gerada")
except Exception as e:
    print(f"   ❌ Erro no structurer: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Teste 5: Testar criação do super-grafo
print("\n5. Testando criação do super-grafo...")
try:
    from agents.multi_agent_graph import create_multi_agent_graph

    graph = create_multi_agent_graph()
    print(f"   ✅ Super-grafo criado com sucesso")
except Exception as e:
    print(f"   ❌ Erro ao criar super-grafo: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Teste 6: Testar execução do super-grafo (CRÍTICO)
print("\n6. Testando execução do super-grafo...")
try:
    from agents.multi_agent_graph import create_multi_agent_graph, create_initial_multi_agent_state

    graph = create_multi_agent_graph()
    state = create_initial_multi_agent_state("Teste de execução")

    print("   Executando invoke()...")
    result = graph.invoke(
        state,
        config={"configurable": {"thread_id": "debug-test"}}
    )

    print(f"   ✅ Super-grafo executado com sucesso!")
    print(f"   Classificação: {result.get('orchestrator_classification')}")
    print(f"   Estágio final: {result.get('current_stage')}")

except Exception as e:
    print(f"   ❌ Erro ao executar super-grafo: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 80)
print("✅ TODOS OS TESTES DE DIAGNÓSTICO PASSARAM!")
print("=" * 80)
