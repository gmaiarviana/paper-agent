"""
Script de validação para MultiAgentState (Épico 7, Task 7.1.5).

Valida que as mudanças na estrutura do estado foram implementadas corretamente:
- Novos campos adicionados: orchestrator_analysis, next_step, agent_suggestion
- Campos obsoletos removidos: orchestrator_classification, orchestrator_reasoning

"""

import sys
from pathlib import Path

# Adicionar o diretório raiz ao PYTHONPATH
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from agents.orchestrator.state import MultiAgentState, create_initial_multi_agent_state

def validate_multi_agent_state():
    """Valida a estrutura e tipos do MultiAgentState após mudanças do Épico 7."""
    print("=" * 70)
    print("VALIDAÇÃO DO MULTIAGENTSTATE (ÉPICO 7, TASK 7.1.5)")
    print("=" * 70)

    # Criar estado inicial
    print("\n1. Criando estado inicial...")
    state = create_initial_multi_agent_state(
        user_input="Observei que LLMs aumentam produtividade",
        session_id="validate-session-123"
    )
    print("   ✅ Estado criado com sucesso")

    # Validar campos compartilhados
    print("\n2. Validando campos compartilhados...")
    required_shared_fields = [
        "user_input",
        "session_id",
        "conversation_history",
        "current_stage",
        "hypothesis_versions"
    ]

    for field in required_shared_fields:
        assert field in state, f"Campo compartilhado '{field}' não encontrado"
        print(f"   ✅ Campo '{field}' presente")

    # Validar novos campos do Orquestrador (Épico 7)
    print("\n3. Validando NOVOS campos do Orquestrador (Épico 7)...")
    new_orchestrator_fields = [
        "orchestrator_analysis",
        "next_step",
        "agent_suggestion"
    ]

    for field in new_orchestrator_fields:
        assert field in state, f"Novo campo '{field}' não encontrado"
        assert state[field] is None, f"Campo '{field}' deveria começar como None"
        print(f"   ✅ Campo '{field}' presente e inicializado como None")

    # Validar remoção de campos obsoletos
    print("\n4. Validando REMOÇÃO de campos obsoletos...")
    obsolete_fields = [
        "orchestrator_classification",
        "orchestrator_reasoning"
    ]

    for field in obsolete_fields:
        assert field not in state, f"Campo obsoleto '{field}' ainda existe"
        print(f"   ✅ Campo obsoleto '{field}' foi removido corretamente")

    # Validar campos de outros agentes
    print("\n5. Validando campos de outros agentes...")
    other_agent_fields = {
        "structurer_output": None,
        "methodologist_output": None,
        "messages": []
    }

    for field, expected_value in other_agent_fields.items():
        assert field in state, f"Campo '{field}' não encontrado"
        if expected_value is None:
            assert state[field] is None, f"Campo '{field}' deveria ser None"
        elif expected_value == []:
            assert state[field] == [], f"Campo '{field}' deveria ser lista vazia"
        print(f"   ✅ Campo '{field}' presente e inicializado corretamente")

    # Validar valores iniciais
    print("\n6. Validando valores iniciais do estado...")
    assert state["user_input"] == "Observei que LLMs aumentam produtividade"
    assert state["session_id"] == "validate-session-123"
    assert state["current_stage"] == "classifying"
    assert len(state["conversation_history"]) == 1
    assert "Usuário:" in state["conversation_history"][0]
    assert state["hypothesis_versions"] == []
    print("   ✅ Valores iniciais corretos")

    # Testar atualização de novos campos
    print("\n7. Testando atualização dos novos campos...")

    # orchestrator_analysis
    state["orchestrator_analysis"] = "Usuário mencionou produtividade mas não especificou métricas"
    assert state["orchestrator_analysis"] == "Usuário mencionou produtividade mas não especificou métricas"
    print("   ✅ orchestrator_analysis pode ser atualizado")

    # next_step
    valid_next_steps = ["explore", "suggest_agent", "clarify"]
    for step in valid_next_steps:
        state["next_step"] = step
        assert state["next_step"] == step
    print(f"   ✅ next_step aceita valores válidos: {valid_next_steps}")

    # agent_suggestion
    suggestion = {
        "agent": "methodologist",
        "justification": "Usuário definiu população e métricas"
    }
    state["agent_suggestion"] = suggestion
    assert state["agent_suggestion"]["agent"] == "methodologist"
    assert state["agent_suggestion"]["justification"] == "Usuário definiu população e métricas"
    print("   ✅ agent_suggestion aceita estrutura correta")

    # Validar anotações de tipo
    print("\n8. Validando anotações de tipo...")
    annotations = MultiAgentState.__annotations__

    assert "orchestrator_analysis" in annotations
    assert "next_step" in annotations
    assert "agent_suggestion" in annotations
    assert "orchestrator_classification" not in annotations
    assert "orchestrator_reasoning" not in annotations

    print("   ✅ Anotações de tipo corretas")

    # Validar que campos compartilhados não foram afetados
    print("\n9. Validando que campos compartilhados permaneceram intactos...")
    assert state["user_input"] == "Observei que LLMs aumentam produtividade"
    assert state["session_id"] == "validate-session-123"
    assert state["current_stage"] == "classifying"
    print("   ✅ Campos compartilhados intactos")

    # Exibir estrutura final
    print("\n10. Estrutura final do estado:")
    print("\n    CAMPOS COMPARTILHADOS:")
    for field in required_shared_fields:
        print(f"      - {field}: {type(state[field]).__name__}")

    print("\n    CAMPOS DO ORQUESTRADOR (ÉPICO 7):")
    for field in new_orchestrator_fields:
        print(f"      - {field}: {type(state[field]).__name__ if state[field] else 'None'}")

    print("\n    CAMPOS DE OUTROS AGENTES:")
    for field in other_agent_fields.keys():
        print(f"      - {field}: {type(state[field]).__name__ if state[field] else 'None'}")

    print("\n" + "=" * 70)
    print("TODOS OS TESTES PASSARAM! ✅")
    print("=" * 70)
    print("\n📝 RESUMO DAS MUDANÇAS (TASK 7.1.5):")
    print("   ✅ Adicionados: orchestrator_analysis, next_step, agent_suggestion")
    print("   ✅ Removidos: orchestrator_classification, orchestrator_reasoning")
    print("   ✅ Estado pronto para Orquestrador Conversacional (Épico 7 POC)")
    print("=" * 70)

if __name__ == "__main__":
    try:
        validate_multi_agent_state()
    except AssertionError as e:
        print(f"\n❌ ERRO: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERRO INESPERADO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
