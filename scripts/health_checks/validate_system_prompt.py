"""
Script de validação manual para System Prompt do Metodologista (Funcionalidade 2.6).

Valida que METHODOLOGIST_AGENT_SYSTEM_PROMPT_V1 foi implementado corretamente:
- Constante definida em utils/prompts/methodologist.py
- Menciona tool ask_user explicitamente
- Define output JSON com campos corretos
- Linguagem direta, <= 500 palavras
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT_STR = str(PROJECT_ROOT)
if PROJECT_ROOT_STR not in sys.path:
    sys.path.insert(0, PROJECT_ROOT_STR)

from scripts.common import setup_project_path

setup_project_path()

from utils.prompts import METHODOLOGIST_AGENT_SYSTEM_PROMPT_V1


def validate_system_prompt():
    """Valida a implementação do system prompt."""
    print("=" * 70)
    print("VALIDAÇÃO DO SYSTEM PROMPT DO METODOLOGISTA (Funcionalidade 2.6)")
    print("=" * 70)

    # Teste 1: Prompt existe e não está vazio
    print("\n1. Verificando se o prompt existe e não está vazio...")
    assert METHODOLOGIST_AGENT_SYSTEM_PROMPT_V1, "Erro: Prompt está vazio"
    assert isinstance(METHODOLOGIST_AGENT_SYSTEM_PROMPT_V1, str), "Erro: Prompt não é string"
    print(f"   ✅ Prompt definido (tipo: {type(METHODOLOGIST_AGENT_SYSTEM_PROMPT_V1).__name__})")

    # Teste 2: Contagem de palavras (<= 500)
    print("\n2. Verificando limite de palavras (deve ser <= 500)...")
    word_count = len(METHODOLOGIST_AGENT_SYSTEM_PROMPT_V1.split())
    print(f"   Total de palavras: {word_count}")
    assert word_count <= 500, f"Erro: Prompt tem {word_count} palavras (limite: 500)"
    print(f"   ✅ Dentro do limite ({word_count}/500 palavras)")

    # Teste 3: Menciona tool ask_user
    print("\n3. Verificando se menciona tool 'ask_user'...")
    assert "ask_user" in METHODOLOGIST_AGENT_SYSTEM_PROMPT_V1, "Erro: Não menciona 'ask_user'"
    print("   ✅ Menciona tool 'ask_user'")

    # Teste 4: Define output JSON correto
    print("\n4. Verificando se define output JSON correto...")
    assert '"status"' in METHODOLOGIST_AGENT_SYSTEM_PROMPT_V1, "Erro: Não menciona campo 'status'"
    assert '"justification"' in METHODOLOGIST_AGENT_SYSTEM_PROMPT_V1, "Erro: Não menciona campo 'justification'"
    assert "approved" in METHODOLOGIST_AGENT_SYSTEM_PROMPT_V1, "Erro: Não menciona status 'approved'"
    assert "rejected" in METHODOLOGIST_AGENT_SYSTEM_PROMPT_V1, "Erro: Não menciona status 'rejected'"
    print("   ✅ Define output JSON com campos corretos")

    # Teste 5: Menciona critérios científicos
    print("\n5. Verificando se menciona critérios científicos...")
    criterios = ["testabilidade", "falseabilidade", "especificidade", "operacionalização"]
    for criterio in criterios:
        assert criterio.lower() in METHODOLOGIST_AGENT_SYSTEM_PROMPT_V1.lower(), \
            f"Erro: Não menciona critério '{criterio}'"
    print(f"   ✅ Menciona todos os 4 critérios: {', '.join(criterios)}")

    # Teste 6: Preview do prompt
    print("\n6. Preview do prompt (primeiras 500 caracteres):")
    print("-" * 70)
    print(METHODOLOGIST_AGENT_SYSTEM_PROMPT_V1[:500] + "...")
    print("-" * 70)

    # Teste 7: Informações estatísticas
    print("\n7. Estatísticas do prompt:")
    print(f"   - Caracteres: {len(METHODOLOGIST_AGENT_SYSTEM_PROMPT_V1)}")
    print(f"   - Palavras: {word_count}")
    print(f"   - Linhas: {len(METHODOLOGIST_AGENT_SYSTEM_PROMPT_V1.splitlines())}")

    print("\n" + "=" * 70)
    print("TODOS OS TESTES PASSARAM! ✅")
    print("=" * 70)
    print("\nCritérios de aceite atendidos:")
    print("  ✅ Constante METHODOLOGIST_AGENT_SYSTEM_PROMPT_V1 em utils/prompts/methodologist.py")
    print("  ✅ Tool calling explícito (instrui LLM a usar ask_user)")
    print("  ✅ Define output JSON: {\"status\": \"approved|rejected\", \"justification\": \"...\"}")
    print(f"  ✅ Linguagem direta, <= 500 palavras ({word_count}/500)")
    print("\n🎉 Funcionalidade 2.6 implementada com sucesso!")


if __name__ == "__main__":
    try:
        validate_system_prompt()
    except AssertionError as e:
        print(f"\n❌ ERRO: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERRO INESPERADO: {e}")
        sys.exit(1)
