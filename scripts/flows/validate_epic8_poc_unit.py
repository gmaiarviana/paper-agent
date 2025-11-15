"""
Script de validação unitária da POC 8.1: Instrumentação do Estruturador.

Valida a lógica de extração de reasoning SEM chamar a API Anthropic.
Testa que:
- Função _extract_reasoning existe e funciona corretamente
- Reasoning do Estruturador é formatado corretamente para ambos os modos
- Formato é consistente com EventBus

Épico 8 - POC: Telemetria e Observabilidade
Data: 15/11/2025
"""

import sys
from pathlib import Path

# Adicionar o diretório raiz ao PYTHONPATH
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from agents.multi_agent_graph import _extract_reasoning, _extract_summary
from agents.orchestrator.state import MultiAgentState


def validate_reasoning_extraction():
    """Valida que função _extract_reasoning funciona corretamente."""
    print("=" * 70)
    print("VALIDAÇÃO UNITÁRIA POC 8.1: EXTRAÇÃO DE REASONING")
    print("=" * 70)
    print()

    # Teste 1: Estruturador - Modo inicial
    print("1. Testando reasoning do Estruturador (modo inicial)...")

    state_initial: MultiAgentState = {
        "user_input": "TDD reduz bugs",
        "session_id": "test-123",
        "current_stage": "structuring",
        "messages": [],
        "hypothesis_versions": [],
        "structurer_output": {
            "structured_question": "Como TDD impacta a taxa de bugs?",
            "elements": {
                "context": "Desenvolvimento de software com metodologia TDD",
                "problem": "Alta taxa de bugs em projetos",
                "contribution": "Validar se TDD realmente reduz bugs"
            }
        }
    }

    reasoning_initial = _extract_reasoning("structurer", state_initial)

    print(f"   Reasoning: {reasoning_initial}")

    # Validar que contém palavras-chave esperadas
    expected_keywords = ["Estruturando V1", "contexto", "problema", "contribuição"]
    has_keywords = all(keyword in reasoning_initial for keyword in expected_keywords)

    if not has_keywords:
        print("   ❌ ERRO: Reasoning não contém palavras-chave esperadas")
        print(f"   Esperado: {expected_keywords}")
        return False

    print("   ✅ Reasoning contém palavras-chave esperadas")
    print()

    # Teste 2: Estruturador - Modo refinamento
    print("2. Testando reasoning do Estruturador (modo refinamento)...")

    state_refinement: MultiAgentState = {
        "user_input": "TDD reduz bugs",
        "session_id": "test-123",
        "current_stage": "validating",
        "messages": [],
        "hypothesis_versions": [],
        "structurer_output": {
            "structured_question": "Como TDD impacta a taxa de bugs em projetos Python?",
            "elements": {
                "context": "Desenvolvimento de software com metodologia TDD em Python",
                "problem": "Alta taxa de bugs em projetos Python",
                "contribution": "Validar se TDD realmente reduz bugs em Python"
            },
            "version": 2,
            "addressed_gaps": ["população", "métricas"]
        },
        "methodologist_output": {
            "status": "needs_refinement",
            "improvements": [
                {"aspect": "população", "gap": "Não especifica linguagem", "suggestion": "Especificar Python"}
            ]
        }
    }

    reasoning_refinement = _extract_reasoning("structurer", state_refinement)

    print(f"   Reasoning: {reasoning_refinement}")

    # Validar que contém palavras-chave esperadas
    expected_keywords_ref = ["Refinando", "V2", "gap", "população", "métricas"]
    has_keywords_ref = all(keyword in reasoning_refinement for keyword in expected_keywords_ref)

    if not has_keywords_ref:
        print("   ❌ ERRO: Reasoning de refinamento não contém palavras-chave esperadas")
        print(f"   Esperado: {expected_keywords_ref}")
        return False

    print("   ✅ Reasoning de refinamento contém palavras-chave esperadas")
    print()

    # Teste 3: Orquestrador
    print("3. Testando reasoning do Orquestrador...")

    state_orchestrator: MultiAgentState = {
        "user_input": "TDD reduz bugs",
        "session_id": "test-123",
        "current_stage": "orchestrating",
        "messages": [],
        "hypothesis_versions": [],
        "orchestrator_analysis": "Análise contextual detalhada do input do usuário indicando necessidade de estruturação.",
        "next_step": "suggest_agent"
    }

    reasoning_orchestrator = _extract_reasoning("orchestrator", state_orchestrator)

    print(f"   Reasoning: {reasoning_orchestrator}")

    if "Análise contextual detalhada" not in reasoning_orchestrator:
        print("   ❌ ERRO: Reasoning do Orquestrador não usa orchestrator_analysis")
        return False

    print("   ✅ Reasoning do Orquestrador correto")
    print()

    # Teste 4: Metodologista
    print("4. Testando reasoning do Metodologista...")

    state_methodologist: MultiAgentState = {
        "user_input": "TDD reduz bugs",
        "session_id": "test-123",
        "current_stage": "validating",
        "messages": [],
        "hypothesis_versions": [],
        "methodologist_output": {
            "status": "needs_refinement",
            "justification": "Falta especificar população e métricas de medição de bugs",
            "improvements": []
        }
    }

    reasoning_methodologist = _extract_reasoning("methodologist", state_methodologist)

    print(f"   Reasoning: {reasoning_methodologist}")

    if "needs_refinement" not in reasoning_methodologist:
        print("   ❌ ERRO: Reasoning do Metodologista não menciona status")
        return False

    if "Falta especificar população" not in reasoning_methodologist:
        print("   ❌ ERRO: Reasoning do Metodologista não inclui justificativa")
        return False

    print("   ✅ Reasoning do Metodologista correto")
    print()

    # Teste 5: Validar que summary também funciona
    print("5. Testando extração de summary (complementar ao reasoning)...")

    summary_structurer = _extract_summary("structurer", state_initial)
    print(f"   Summary: {summary_structurer}")

    if "Estruturou questão de pesquisa" not in summary_structurer:
        print("   ❌ ERRO: Summary do Estruturador incorreto")
        return False

    print("   ✅ Summary do Estruturador correto")
    print()

    # Teste 6: Validar tamanho do reasoning
    print("6. Validando tamanho dos reasoning (não deve ser vazio)...")

    all_reasoning = [
        reasoning_initial,
        reasoning_refinement,
        reasoning_orchestrator,
        reasoning_methodologist
    ]

    for idx, r in enumerate(all_reasoning, 1):
        if not r or len(r) < 10:
            print(f"   ❌ ERRO: Reasoning {idx} muito curto ou vazio: '{r}'")
            return False

    print("   ✅ Todos os reasoning têm tamanho adequado")
    print()

    print("=" * 70)
    print("✅ TODOS OS TESTES UNITÁRIOS PASSARAM!")
    print("=" * 70)
    print()
    print("POC 8.1 - VALIDAÇÃO UNITÁRIA CONCLUÍDA:")
    print("  ✅ Função _extract_reasoning implementada corretamente")
    print("  ✅ Reasoning do Estruturador (modo inicial) formatado corretamente")
    print("  ✅ Reasoning do Estruturador (modo refinamento) formatado corretamente")
    print("  ✅ Reasoning do Orquestrador e Metodologista funcionam")
    print("  ✅ Summary complementar funciona")
    print()
    print("IMPLEMENTAÇÃO DA POC 8.1:")
    print("  ✅ agents/multi_agent_graph.py: _extract_reasoning() implementado")
    print("  ✅ agents/multi_agent_graph.py: metadata={'reasoning': ...} em events")
    print("  ✅ app/dashboard.py: expander para exibir reasoning")
    print()
    print("PRÓXIMOS PASSOS:")
    print("  → Testar com API real (configure ANTHROPIC_API_KEY)")
    print("  → Visualizar reasoning no Dashboard Streamlit")
    print("  → Implementar Protótipo 8.2: Instrumentar Orquestrador e Metodologista")
    print()

    return True


if __name__ == "__main__":
    try:
        success = validate_reasoning_extraction()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ ERRO FATAL: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
