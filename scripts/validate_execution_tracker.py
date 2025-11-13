"""
Script de validação manual para ExecutionTracker.

Valida que o execution_tracker foi implementado corretamente com:
- Extração de tokens de AIMessage (response_metadata e usage_metadata)
- Cálculo de custos via CostTracker
- Registro no MemoryManager
- Suporte a metadados extras

Versão: 1.0
Data: 13/11/2025
"""

import sys
from pathlib import Path
from unittest.mock import Mock

# Adicionar o diretório raiz ao PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from agents.memory.execution_tracker import register_execution
from agents.memory.memory_manager import MemoryManager


def validate_execution_tracker():
    """Valida a implementação do ExecutionTracker."""
    print("=" * 70)
    print("VALIDAÇÃO DO EXECUTION TRACKER (Épico 6.2)")
    print("=" * 70)

    # Teste 1: Registro com response_metadata (LangChain 0.2)
    print("\n1. Testando extração de tokens de response_metadata...")
    memory_manager = MemoryManager()
    session_id = "test-session-1"

    mock_response = Mock()
    mock_response.response_metadata = {
        "usage": {
            "input_tokens": 150,
            "output_tokens": 75
        }
    }

    config = {"configurable": {"thread_id": session_id}}

    execution = register_execution(
        memory_manager=memory_manager,
        config=config,
        agent_name="orchestrator",
        response=mock_response,
        summary="Classificação: vague",
        model_name="claude-3-5-haiku-20241022"
    )

    assert execution is not None, "Execution não deve ser None"
    assert execution.agent_name == "orchestrator", "Agent name incorreto"
    assert execution.tokens_input == 150, f"Tokens input incorreto: {execution.tokens_input}"
    assert execution.tokens_output == 75, f"Tokens output incorreto: {execution.tokens_output}"
    assert execution.tokens_total == 225, f"Tokens total incorreto: {execution.tokens_total}"
    assert execution.summary == "Classificação: vague", "Summary incorreto"
    assert "model" in execution.metadata, "Metadata deve conter 'model'"
    assert "cost_usd" in execution.metadata, "Metadata deve conter 'cost_usd'"
    assert execution.metadata["model"] == "claude-3-5-haiku-20241022", "Model name incorreto"
    print(f"   ✅ Tokens extraídos: input={execution.tokens_input}, output={execution.tokens_output}")
    print(f"   ✅ Custo calculado: ${execution.metadata['cost_usd']:.6f}")

    # Verificar registro no MemoryManager
    history = memory_manager.get_agent_history(session_id, "orchestrator")
    assert len(history) == 1, f"História deve ter 1 execução, tem {len(history)}"
    print("   ✅ Registrado no MemoryManager")

    # Teste 2: Registro com usage_metadata (LangChain 0.3+)
    print("\n2. Testando extração de tokens de usage_metadata...")
    session_id_2 = "test-session-2"

    mock_response_2 = Mock()
    mock_response_2.response_metadata = {}
    mock_response_2.usage_metadata = {
        "input_tokens": 200,
        "output_tokens": 100
    }

    config_2 = {"configurable": {"thread_id": session_id_2}}

    execution_2 = register_execution(
        memory_manager=memory_manager,
        config=config_2,
        agent_name="structurer",
        response=mock_response_2,
        summary="Estruturação V1",
        model_name="claude-3-5-haiku-20241022"
    )

    assert execution_2 is not None, "Execution não deve ser None"
    assert execution_2.tokens_input == 200, f"Tokens input incorreto: {execution_2.tokens_input}"
    assert execution_2.tokens_output == 100, f"Tokens output incorreto: {execution_2.tokens_output}"
    print(f"   ✅ Tokens extraídos de usage_metadata: input={execution_2.tokens_input}, output={execution_2.tokens_output}")

    # Teste 3: Sem memory_manager (deve retornar None)
    print("\n3. Testando comportamento sem MemoryManager...")
    execution_3 = register_execution(
        memory_manager=None,
        config=config,
        agent_name="test",
        response=mock_response,
        summary="Test",
        model_name="claude-3-5-haiku-20241022"
    )

    assert execution_3 is None, "Execution deve ser None quando memory_manager é None"
    print("   ✅ Retorna None quando memory_manager não fornecido")

    # Teste 4: Sem metadados de tokens (deve usar zeros)
    print("\n4. Testando resposta sem metadados de tokens...")
    mock_response_empty = Mock()
    mock_response_empty.response_metadata = {}

    execution_4 = register_execution(
        memory_manager=memory_manager,
        config={"configurable": {"thread_id": "test-session-3"}},
        agent_name="test_agent",
        response=mock_response_empty,
        summary="Test",
        model_name="claude-3-5-haiku-20241022"
    )

    assert execution_4 is not None, "Execution não deve ser None"
    assert execution_4.tokens_input == 0, "Tokens input deve ser 0"
    assert execution_4.tokens_output == 0, "Tokens output deve ser 0"
    assert execution_4.tokens_total == 0, "Tokens total deve ser 0"
    print("   ✅ Usa zeros quando metadados não disponíveis")

    # Teste 5: Metadados extras personalizados
    print("\n5. Testando metadados extras personalizados...")
    custom_metadata = {
        "classification": "vague",
        "reasoning": "Input não possui estrutura clara"
    }

    execution_5 = register_execution(
        memory_manager=memory_manager,
        config={"configurable": {"thread_id": "test-session-4"}},
        agent_name="orchestrator",
        response=mock_response,
        summary="Classificação: vague",
        model_name="claude-3-5-haiku-20241022",
        extra_metadata=custom_metadata
    )

    assert execution_5 is not None, "Execution não deve ser None"
    assert "classification" in execution_5.metadata, "Metadata deve conter 'classification'"
    assert "reasoning" in execution_5.metadata, "Metadata deve conter 'reasoning'"
    assert execution_5.metadata["classification"] == "vague", "Classification incorreto"
    assert "model" in execution_5.metadata, "Metadata deve conter 'model' padrão"
    assert "cost_usd" in execution_5.metadata, "Metadata deve conter 'cost_usd' padrão"
    print(f"   ✅ Metadados extras adicionados: {list(custom_metadata.keys())}")
    print(f"   ✅ Metadados padrão preservados: model, cost_usd")

    # Teste 6: Verificar totais da sessão
    print("\n6. Testando agregação de totais por sessão...")
    totals = memory_manager.get_session_totals(session_id)

    assert "orchestrator" in totals, "Totais devem incluir orchestrator"
    assert totals["orchestrator"] == 225, f"Total incorreto: {totals['orchestrator']}"
    assert totals["total"] == 225, f"Total geral incorreto: {totals['total']}"
    print(f"   ✅ Totais calculados: {totals['total']} tokens")

    # Teste 7: Múltiplas execuções do mesmo agente
    print("\n7. Testando múltiplas execuções do mesmo agente...")
    execution_6 = register_execution(
        memory_manager=memory_manager,
        config=config,
        agent_name="orchestrator",
        response=mock_response,
        summary="Segunda execução",
        model_name="claude-3-5-haiku-20241022"
    )

    history = memory_manager.get_agent_history(session_id, "orchestrator")
    assert len(history) == 2, f"História deve ter 2 execuções, tem {len(history)}"
    print(f"   ✅ Múltiplas execuções registradas: {len(history)} execuções")

    # Teste 8: Verificar compatibilidade com CostTracker
    print("\n8. Testando cálculo de custos para diferentes modelos...")
    models_to_test = [
        "claude-3-5-haiku-20241022",
        "claude-3-5-sonnet-20241022",
        "claude-3-opus-20240229"
    ]

    for model in models_to_test:
        exec_test = register_execution(
            memory_manager=memory_manager,
            config={"configurable": {"thread_id": f"test-{model}"}},
            agent_name="test",
            response=mock_response,
            summary=f"Teste {model}",
            model_name=model
        )

        assert exec_test is not None, f"Execution não deve ser None para {model}"
        assert exec_test.metadata["cost_usd"] > 0, f"Custo deve ser > 0 para {model}"
        print(f"   ✅ {model}: ${exec_test.metadata['cost_usd']:.6f}")

    print("\n" + "=" * 70)
    print("TODOS OS TESTES PASSARAM! ✅")
    print("=" * 70)
    print("\n📊 Resumo:")
    print("   - Extração de tokens: response_metadata e usage_metadata ✅")
    print("   - Cálculo de custos via CostTracker ✅")
    print("   - Registro no MemoryManager ✅")
    print("   - Metadados extras personalizados ✅")
    print("   - Compatibilidade com múltiplos modelos ✅")
    print("   - Agregação de totais por sessão ✅")


if __name__ == "__main__":
    try:
        validate_execution_tracker()
    except AssertionError as e:
        print(f"\n❌ ERRO: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERRO INESPERADO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
