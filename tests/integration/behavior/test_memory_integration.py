"""
Script de validação end-to-end para integração de MemoryManager (Épico 6.2).

Valida que o sistema multi-agente completo registra execuções corretamente:
- Orquestrador classifica input
- Estruturador organiza questão
- Metodologista valida rigor
- Todos registram tokens e custos no MemoryManager

"""

import sys
from pathlib import Path

# Adicionar o diretório raiz ao PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from agents.multi_agent_graph import create_multi_agent_graph, create_initial_multi_agent_state
from agents.memory.memory_manager import MemoryManager
from core.utils.cost_tracker import CostTracker

def validate_memory_integration():
    """Valida integração completa do MemoryManager com o super-grafo."""
    print("=" * 70)
    print("VALIDAÇÃO END-TO-END: INTEGRAÇÃO DO MEMORYMANGER (Épico 6.2)")
    print("=" * 70)

    # 1. Criar MemoryManager e super-grafo
    print("\n1. Criando MemoryManager e super-grafo...")
    memory_manager = MemoryManager()
    graph = create_multi_agent_graph()
    print("   ✅ MemoryManager e super-grafo criados")

    # 2. Criar estado inicial com input vago (testa fluxo completo)
    print("\n2. Criando estado inicial com input vago...")
    session_id = "validation-session-001"
    input_text = "Observei que desenvolvedores que usam IA são mais produtivos"

    state = create_initial_multi_agent_state(input_text)
    print(f"   ✅ Estado inicial criado: \"{input_text}\"")

    # 3. Configurar com MemoryManager
    print("\n3. Configurando grafo com MemoryManager...")
    config = {
        "configurable": {
            "thread_id": session_id,
            "memory_manager": memory_manager  # Épico 6.2
        }
    }
    print("   ✅ Config criado com memory_manager")

    # 4. Executar super-grafo
    print("\n4. Executando super-grafo (fluxo completo)...")
    print("   Este fluxo deve passar por:")
    print("   - Orquestrador (classifica como 'vague')")
    print("   - Estruturador (organiza em questão V1)")
    print("   - Metodologista (valida rigor)\n")

    try:
        result = graph.invoke(state, config=config)
        print("   ✅ Super-grafo executado com sucesso")
    except Exception as e:
        print(f"   ❌ ERRO ao executar super-grafo: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # 5. Validar resultado da execução
    print("\n5. Validando resultado da execução...")

    orchestrator_classification = result.get('orchestrator_classification')
    structurer_output = result.get('structurer_output')
    methodologist_output = result.get('methodologist_output')

    assert orchestrator_classification is not None, "Orquestrador não classificou"
    assert structurer_output is not None, "Estruturador não processou"
    assert methodologist_output is not None, "Metodologista não decidiu"

    print(f"   ✅ Orquestrador: {orchestrator_classification}")
    print(f"   ✅ Estruturador: questão V{structurer_output.get('version', 1)} gerada")
    print(f"   ✅ Metodologista: status = {methodologist_output['status']}")

    # 6. Validar registros no MemoryManager
    print("\n6. Validando registros no MemoryManager...")

    # Verificar que todos os agentes registraram execuções
    orchestrator_history = memory_manager.get_agent_history(session_id, "orchestrator")
    structurer_history = memory_manager.get_agent_history(session_id, "structurer")
    methodologist_history = memory_manager.get_agent_history(session_id, "methodologist")

    assert len(orchestrator_history) > 0, "Orquestrador não registrou execução"
    assert len(structurer_history) > 0, "Estruturador não registrou execução"
    assert len(methodologist_history) > 0, "Metodologista não registrou execução"

    print(f"   ✅ Orquestrador: {len(orchestrator_history)} execução(ões)")
    print(f"   ✅ Estruturador: {len(structurer_history)} execução(ões)")
    print(f"   ✅ Metodologista: {len(methodologist_history)} execução(ões)")

    # 7. Validar dados das execuções
    print("\n7. Validando dados das execuções...")

    # Verificar orquestrador
    orch_exec = orchestrator_history[0]
    assert orch_exec.tokens_input > 0, "Orquestrador: tokens_input deve ser > 0"
    assert orch_exec.tokens_output > 0, "Orquestrador: tokens_output deve ser > 0"
    assert orch_exec.tokens_total == orch_exec.tokens_input + orch_exec.tokens_output
    assert "model" in orch_exec.metadata, "Orquestrador: metadata deve conter 'model'"
    assert "cost_usd" in orch_exec.metadata, "Orquestrador: metadata deve conter 'cost_usd'"
    print(f"   ✅ Orquestrador: {orch_exec.tokens_total} tokens, ${orch_exec.metadata['cost_usd']:.6f}")

    # Verificar estruturador
    struct_exec = structurer_history[0]
    assert struct_exec.tokens_input > 0, "Estruturador: tokens_input deve ser > 0"
    assert struct_exec.tokens_output > 0, "Estruturador: tokens_output deve ser > 0"
    assert "model" in struct_exec.metadata, "Estruturador: metadata deve conter 'model'"
    assert "cost_usd" in struct_exec.metadata, "Estruturador: metadata deve conter 'cost_usd'"
    print(f"   ✅ Estruturador: {struct_exec.tokens_total} tokens, ${struct_exec.metadata['cost_usd']:.6f}")

    # Verificar metodologista
    meth_exec = methodologist_history[0]
    assert meth_exec.tokens_input > 0, "Metodologista: tokens_input deve ser > 0"
    assert meth_exec.tokens_output > 0, "Metodologista: tokens_output deve ser > 0"
    assert "model" in meth_exec.metadata, "Metodologista: metadata deve conter 'model'"
    assert "cost_usd" in meth_exec.metadata, "Metodologista: metadata deve conter 'cost_usd'"
    print(f"   ✅ Metodologista: {meth_exec.tokens_total} tokens, ${meth_exec.metadata['cost_usd']:.6f}")

    # 8. Validar totais agregados
    print("\n8. Validando totais agregados...")

    totals = memory_manager.get_session_totals(session_id)

    assert "orchestrator" in totals, "Totais devem incluir orchestrator"
    assert "structurer" in totals, "Totais devem incluir structurer"
    assert "methodologist" in totals, "Totais devem incluir methodologist"
    assert "total" in totals, "Totais devem incluir total geral"

    expected_total = totals["orchestrator"] + totals["structurer"] + totals["methodologist"]
    assert totals["total"] == expected_total, f"Total inconsistente: {totals['total']} != {expected_total}"

    print(f"   ✅ Orquestrador total: {totals['orchestrator']} tokens")
    print(f"   ✅ Estruturador total: {totals['structurer']} tokens")
    print(f"   ✅ Metodologista total: {totals['methodologist']} tokens")
    print(f"   ✅ TOTAL GERAL: {totals['total']} tokens")

    # 9. Validar integração com CostTracker
    print("\n9. Validando integração com CostTracker...")

    total_cost = 0.0
    for agent_name in ["orchestrator", "structurer", "methodologist"]:
        agent_history = memory_manager.get_agent_history(session_id, agent_name)
        for execution in agent_history:
            if "cost_usd" in execution.metadata:
                total_cost += execution.metadata["cost_usd"]
                # Validar que o custo foi calculado corretamente
                expected_cost = CostTracker.calculate_cost(
                    model=execution.metadata["model"],
                    input_tokens=execution.tokens_input,
                    output_tokens=execution.tokens_output
                )
                assert abs(execution.metadata["cost_usd"] - expected_cost["total_cost"]) < 0.000001, \
                    f"Custo inconsistente para {agent_name}"

    print(f"   ✅ Custo total validado: ${total_cost:.6f}")
    print(f"   ✅ CostTracker integrado corretamente")

    # 10. Validar export da sessão
    print("\n10. Validando export da sessão...")

    export_data = memory_manager.export_session_as_dict(session_id)

    assert "session_id" in export_data, "Export deve conter session_id"
    assert "agents" in export_data, "Export deve conter agents"
    assert "orchestrator" in export_data["agents"], "Export deve conter orchestrator"
    assert "structurer" in export_data["agents"], "Export deve conter structurer"
    assert "methodologist" in export_data["agents"], "Export deve conter methodologist"

    # Validar que export é serializável em JSON
    import json
    try:
        json_str = json.dumps(export_data, indent=2)
        assert len(json_str) > 0, "Export JSON vazio"
        print(f"   ✅ Export JSON gerado: {len(json_str)} caracteres")
    except Exception as e:
        raise AssertionError(f"Export não é serializável: {e}")

    print(f"   ✅ Export validado com {len(export_data['agents'])} agentes")

    # Resumo final
    print("\n" + "=" * 70)
    print("TODOS OS TESTES PASSARAM! ✅")
    print("=" * 70)
    print("\n📊 Resumo da validação:")
    print(f"   - Super-grafo executado: orchestrator → structurer → methodologist")
    print(f"   - Execuções registradas: {len(orchestrator_history) + len(structurer_history) + len(methodologist_history)}")
    print(f"   - Tokens totais: {totals['total']}")
    print(f"   - Custo total: ${total_cost:.6f}")
    print(f"   - Export JSON: válido")
    print("\n🎉 Épico 6.2 implementado com sucesso!")
    print("   - Nós do LangGraph registram tokens reais")
    print("   - MemoryManager exposto via config do super-grafo")
    print("   - Integração com CostTracker validada")
    print("   - Métricas de tokens e custos disponíveis por agente")

if __name__ == "__main__":
    try:
        validate_memory_integration()
    except AssertionError as e:
        print(f"\n❌ ERRO DE VALIDAÇÃO: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERRO INESPERADO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
