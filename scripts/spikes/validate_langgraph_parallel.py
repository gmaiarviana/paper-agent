"""
Spike: Valida se LangGraph suporta execução paralela de nós
Objetivo: Testar se graph.add_edge(START, ["node_a", "node_b"]) funciona
"""
from langgraph.graph import StateGraph, START, END
from typing import TypedDict
import time

class TestState(TypedDict):
    input: str
    a_result: str
    b_result: str
    a_timestamp: float
    b_timestamp: float

def node_a(state: TestState) -> dict:
    """Simula processamento do Orquestrador (3s)"""
    print("🔵 Node A (Orchestrator) iniciou...")
    time.sleep(3)
    timestamp = time.time()
    print(f"🔵 Node A completou em {timestamp}")
    return {"a_result": "orchestrator_done", "a_timestamp": timestamp}

def node_b(state: TestState) -> dict:
    """Simula processamento do Observador (2s)"""
    print("👁️ Node B (Observer) iniciou...")
    time.sleep(2)
    timestamp = time.time()
    print(f"👁️ Node B completou em {timestamp}")
    return {"b_result": "observer_done", "b_timestamp": timestamp}

def test_parallel_execution():
    """Testa execução paralela"""
    print("\n" + "="*60)
    print("TESTE: Execução Paralela de Nós")
    print("="*60 + "\n")
    
    # Setup graph
    graph = StateGraph(TestState)
    graph.add_node("orchestrator", node_a)
    graph.add_node("observer", node_b)
    
    # ⚠️ CRÍTICO: Testar se lista funciona
    try:
        graph.add_edge(START, ["orchestrator", "observer"])
        print("✅ add_edge(START, [list]) aceito pela API\n")
    except Exception as e:
        print(f"❌ FALHOU: add_edge(START, [list]) não suportado")
        print(f"   Erro: {e}\n")
        return False
    
    graph.add_edge("orchestrator", END)
    graph.add_edge("observer", END)
    
    # Compile and execute
    compiled = graph.compile()
    
    start_time = time.time()
    print(f"⏱️ Início: {start_time}\n")
    
    result = compiled.invoke({
        "input": "test_parallel",
        "a_result": "",
        "b_result": "",
        "a_timestamp": 0.0,
        "b_timestamp": 0.0
    })
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"\n⏱️ Fim: {end_time}")
    print(f"⏱️ Tempo total: {total_time:.2f}s\n")
    
    # Análise
    print("="*60)
    print("ANÁLISE")
    print("="*60 + "\n")
    
    time_diff = abs(result["a_timestamp"] - result["b_timestamp"])
    
    print(f"Resultados:")
    print(f"  - Orchestrator: {result['a_result']}")
    print(f"  - Observer: {result['b_result']}")
    print(f"  - Diferença temporal: {time_diff:.2f}s\n")
    
    if total_time < 4:  # Se < 4s, rodou em paralelo
        print("✅ PARALELO: Nós executaram simultaneamente")
        print(f"   (Esperado: ~3s, Obtido: {total_time:.2f}s)")
        return True
    else:
        print("❌ SEQUENCIAL: Nós executaram em série")
        print(f"   (Esperado: ~5s, Obtido: {total_time:.2f}s)")
        return False

if __name__ == "__main__":
    success = test_parallel_execution()
    
    print("\n" + "="*60)
    if success:
        print("CONCLUSÃO: ✅ Paralelismo SUPORTADO")
        print("Recomendação: Usar add_edge(START, [list])")
    else:
        print("CONCLUSÃO: ❌ Paralelismo NÃO suportado")
        print("Recomendação: Usar callback assíncrono")
    print("="*60 + "\n")

