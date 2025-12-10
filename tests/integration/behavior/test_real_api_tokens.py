"""
Teste para verificar formato real da resposta da API Anthropic.

Este script chama a API real e inspeciona os metadados de tokens.

"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from utils.token_extractor import extract_tokens_and_cost
import json

def test_real_api_response():
    """Testa formato real da resposta da API Anthropic."""
    print("=" * 70)
    print("TESTE: INSPEÇÃO DE RESPOSTA REAL DA API ANTHROPIC")
    print("=" * 70)
    print()

    # Chamar API real com mensagem simples
    print("1. Chamando API Anthropic com mensagem simples...")
    llm = ChatAnthropic(model="claude-3-5-haiku-20241022", temperature=0)
    response = llm.invoke([HumanMessage(content="Hello, respond with 'Hi' only")])
    print(f"   ✅ API chamada com sucesso")
    print(f"   Resposta: {response.content[:50]}...")
    print()

    # Inspecionar atributos da resposta
    print("2. Inspecionando atributos da resposta...")
    print(f"   Tipo: {type(response)}")
    print(f"   Atributos disponíveis: {dir(response)}")
    print()

    # Verificar usage_metadata
    print("3. Verificando usage_metadata...")
    if hasattr(response, 'usage_metadata'):
        print(f"   ✅ usage_metadata existe")
        print(f"   Tipo: {type(response.usage_metadata)}")
        print(f"   Conteúdo: {response.usage_metadata}")
    else:
        print(f"   ❌ usage_metadata NÃO existe")
    print()

    # Verificar response_metadata
    print("4. Verificando response_metadata...")
    if hasattr(response, 'response_metadata'):
        print(f"   ✅ response_metadata existe")
        print(f"   Tipo: {type(response.response_metadata)}")
        print(f"   Conteúdo: {json.dumps(response.response_metadata, indent=2, default=str)}")
    else:
        print(f"   ❌ response_metadata NÃO existe")
    print()

    # Tentar extrair tokens
    print("5. Tentando extrair tokens com token_extractor...")
    try:
        metrics = extract_tokens_and_cost(response, "claude-3-5-haiku-20241022")
        print(f"   ✅ Extração bem-sucedida!")
        print(f"   Tokens input: {metrics['tokens_input']}")
        print(f"   Tokens output: {metrics['tokens_output']}")
        print(f"   Tokens total: {metrics['tokens_total']}")
        print(f"   Custo: ${metrics['cost']:.6f}")
    except Exception as e:
        print(f"   ❌ Erro na extração: {e}")
        import traceback
        traceback.print_exc()
    print()

    # Verificar todos os atributos que contêm 'usage' ou 'token'
    print("6. Buscando atributos relacionados a tokens/usage...")
    for attr in dir(response):
        if 'usage' in attr.lower() or 'token' in attr.lower():
            try:
                value = getattr(response, attr)
                print(f"   - {attr}: {value}")
            except:
                pass
    print()

    print("=" * 70)
    print("FIM DA INSPEÇÃO")
    print("=" * 70)

if __name__ == "__main__":
    try:
        test_real_api_response()
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
