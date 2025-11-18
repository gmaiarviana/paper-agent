"""
Script para debugar resposta do LLM na detecção de maturidade.
"""
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.config import create_anthropic_client, get_anthropic_api_key
from langchain_core.messages import HumanMessage

def test_llm_connection():
    """Testa conexão com LLM e resposta."""
    print("=" * 70)
    print(" DEBUG: Testando conexão com LLM")
    print("=" * 70)

    # Verificar API key
    api_key = get_anthropic_api_key()
    if not api_key:
        print("❌ API key não configurada (ANTHROPIC_API_KEY não encontrada no .env)")
        return False

    print(f"✅ API key configurada: {api_key[:10]}...{api_key[-4:]}")

    # Criar cliente LLM
    try:
        llm = create_anthropic_client("claude-3-5-haiku-20241022")
        print("✅ Cliente LLM criado com sucesso")
    except Exception as e:
        print(f"❌ Erro ao criar cliente LLM: {e}")
        return False

    # Testar chamada simples
    try:
        print("\n📞 Testando chamada simples ao LLM...")
        message = HumanMessage(content="Responda apenas: OK")
        response = llm.invoke([message])
        print(f"✅ Resposta recebida: {response.content}")
    except Exception as e:
        print(f"❌ Erro ao chamar LLM: {e}")
        return False

    # Testar chamada com JSON
    try:
        print("\n📞 Testando chamada com resposta JSON...")
        message = HumanMessage(content='Retorne exatamente este JSON: {"status": "ok", "value": 42}')
        response = llm.invoke([message])
        print(f"✅ Resposta JSON: {response.content}")

        # Tentar parsear
        import json
        response_text = response.content.strip()

        # Remover markdown se presente
        if response_text.startswith("```"):
            lines = response_text.split("\n")
            response_text = "\n".join(lines[1:-1])

        parsed = json.loads(response_text)
        print(f"✅ JSON parseado com sucesso: {parsed}")
    except json.JSONDecodeError as e:
        print(f"❌ Erro ao parsear JSON: {e}")
        print(f"   Resposta raw: {response.content}")
        return False
    except Exception as e:
        print(f"❌ Erro ao chamar LLM: {e}")
        return False

    print("\n" + "=" * 70)
    print("✅ TODOS OS TESTES PASSARAM!")
    print("=" * 70)
    return True

if __name__ == "__main__":
    success = test_llm_connection()
    sys.exit(0 if success else 1)
