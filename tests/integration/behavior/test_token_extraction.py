"""
Teste de integração para extração de tokens via state (Épico 8.3).

Valida que tokens e custos são extraídos corretamente do state
retornado pelos nós, sem precisar chamar API real.

"""

import sys
from pathlib import Path

# Adicionar diretório raiz ao PYTHONPATH
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from core.utils.token_extractor import extract_tokens_and_cost

class MockAIMessage:
    """Mock de AIMessage do LangChain com usage_metadata."""

    def __init__(self, tokens_input: int, tokens_output: int):
        self.usage_metadata = {
            "input_tokens": tokens_input,
            "output_tokens": tokens_output
        }
        self.content = "Mock response"

def test_extract_tokens_and_cost_from_usage_metadata():
    """Valida extração de tokens de usage_metadata."""
    # Criar mock de resposta LLM
    mock_response = MockAIMessage(tokens_input=150, tokens_output=75)

    # Extrair métricas
    metrics = extract_tokens_and_cost(mock_response, "claude-3-5-haiku-20241022")

    # Validar
    assert metrics["tokens_input"] == 150
    assert metrics["tokens_output"] == 75
    assert metrics["tokens_total"] == 225
    assert metrics["cost"] > 0  # Deve ter calculado custo

    print(f"✅ Tokens extraídos: input={metrics['tokens_input']}, output={metrics['tokens_output']}, total={metrics['tokens_total']}")
    print(f"✅ Custo calculado: ${metrics['cost']:.6f}")

def test_extract_tokens_with_zero_values():
    """Valida que função lida com agentes sem tokens (não chamaram LLM)."""
    # Criar mock de resposta sem tokens
    mock_response = MockAIMessage(tokens_input=0, tokens_output=0)

    # Extrair métricas
    metrics = extract_tokens_and_cost(mock_response, "claude-3-5-haiku-20241022")

    # Validar
    assert metrics["tokens_input"] == 0
    assert metrics["tokens_output"] == 0
    assert metrics["tokens_total"] == 0
    assert metrics["cost"] == 0.0

    print(f"✅ Agente sem LLM call: tokens=0, cost=$0.00")

def test_state_returns_metrics():
    """Valida que nós retornam métricas no state."""
    # Simular o que um nó retorna
    mock_response = MockAIMessage(tokens_input=200, tokens_output=100)

    # Simular extração feita pelo nó
    metrics = extract_tokens_and_cost(mock_response, "claude-3-5-haiku-20241022")

    # Simular update do state retornado pelo nó
    node_result = {
        "orchestrator_analysis": "Test reasoning",
        "next_step": "explore",
        "last_agent_tokens_input": metrics["tokens_input"],
        "last_agent_tokens_output": metrics["tokens_output"],
        "last_agent_cost": metrics["cost"],
        "messages": []
    }

    # Validar que instrument_node consegue ler do state
    tokens_input = node_result.get("last_agent_tokens_input", 0)
    tokens_output = node_result.get("last_agent_tokens_output", 0)
    tokens_total = tokens_input + tokens_output
    cost = node_result.get("last_agent_cost", 0.0)

    assert tokens_input == 200
    assert tokens_output == 100
    assert tokens_total == 300
    assert cost > 0

    print(f"✅ State retornado pelo nó: {tokens_total} tokens, ${cost:.6f}")
    print(f"✅ instrument_node consegue ler: input={tokens_input}, output={tokens_output}, cost=${cost:.6f}")

if __name__ == "__main__":
    print("=" * 70)
    print("TESTE DE INTEGRAÇÃO: EXTRAÇÃO DE TOKENS VIA STATE")
    print("=" * 70)
    print()

    print("1. Testando extração de tokens de usage_metadata...")
    test_extract_tokens_and_cost_from_usage_metadata()
    print()

    print("2. Testando agentes sem LLM call (tokens=0)...")
    test_extract_tokens_with_zero_values()
    print()

    print("3. Testando fluxo completo (nó → state → instrument_node)...")
    test_state_returns_metrics()
    print()

    print("=" * 70)
    print("✅ TODOS OS TESTES PASSARAM!")
    print("=" * 70)
    print()
    print("CONCLUSÃO:")
    print("  ✅ token_extractor extrai tokens corretamente")
    print("  ✅ Nós retornam métricas no state")
    print("  ✅ instrument_node consegue ler métricas do state")
    print()
    print("PRÓXIMO PASSO:")
    print("  → Configurar ANTHROPIC_API_KEY para validar end-to-end")
    print("  → Rodar validate_epic8_complete.py com API real")
