"""
Script de validação manual para parsing de JSON do Orquestrador Conversacional.

Valida que extract_orchestrator_response foi implementado corretamente com:
- Parsing robusto de JSON em diferentes formatos
- Validação de campos obrigatórios
- Validação de tipos e valores
- Error handling apropriado

Versão: 1.0
Data: 14/11/2025
"""

import sys
from pathlib import Path

# Adicionar o diretório raiz ao PYTHONPATH
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from utils.json_parser import (
    extract_orchestrator_response,
    OrchestratorValidationError,
    OrchestratorResponse
)
import json


def validate_orchestrator_json_parsing():
    """Valida a implementação do parsing de JSON do Orquestrador."""
    print("=" * 70)
    print("VALIDAÇÃO DO PARSING DE JSON DO ORQUESTRADOR CONVERSACIONAL")
    print("=" * 70)

    # Teste 1: JSON válido básico com explore
    print("\n1. Testando JSON válido com next_step='explore'...")
    content_explore = '''{
    "reasoning": "Usuário tem observação mas não especificou contexto",
    "next_step": "explore",
    "message": "Interessante! Me conta mais: onde você observou isso?",
    "agent_suggestion": null
}'''
    result = extract_orchestrator_response(content_explore)
    assert result["reasoning"] == "Usuário tem observação mas não especificou contexto"
    assert result["next_step"] == "explore"
    assert result["message"] == "Interessante! Me conta mais: onde você observou isso?"
    assert result["agent_suggestion"] is None
    print("   ✅ JSON com next_step='explore' funciona corretamente")

    # Teste 2: JSON válido com agent_suggestion
    print("\n2. Testando JSON válido com agent_suggestion...")
    content_suggest = '''{
    "reasoning": "Hipótese estruturada com população e métricas definidas",
    "next_step": "suggest_agent",
    "message": "Posso chamar o Metodologista para validar?",
    "agent_suggestion": {
        "agent": "methodologist",
        "justification": "Hipótese pronta para validação metodológica"
    }
}'''
    result = extract_orchestrator_response(content_suggest)
    assert result["next_step"] == "suggest_agent"
    assert result["agent_suggestion"] is not None
    assert result["agent_suggestion"]["agent"] == "methodologist"
    assert result["agent_suggestion"]["justification"] == "Hipótese pronta para validação metodológica"
    print("   ✅ JSON com agent_suggestion funciona corretamente")

    # Teste 3: JSON válido com clarify
    print("\n3. Testando JSON válido com next_step='clarify'...")
    content_clarify = '''{
    "reasoning": "Informação ambígua",
    "next_step": "clarify",
    "message": "Você quer dizer produtividade em termos de tempo ou qualidade?",
    "agent_suggestion": null
}'''
    result = extract_orchestrator_response(content_clarify)
    assert result["next_step"] == "clarify"
    print("   ✅ JSON com next_step='clarify' funciona corretamente")

    # Teste 4: JSON dentro de markdown code block
    print("\n4. Testando JSON dentro de markdown code block...")
    content_markdown = '''Aqui está minha análise:

```json
{
    "reasoning": "Análise do contexto",
    "next_step": "explore",
    "message": "Conte mais sobre isso",
    "agent_suggestion": null
}
```

Espero que ajude!'''
    result = extract_orchestrator_response(content_markdown)
    assert result["next_step"] == "explore"
    print("   ✅ Extração de markdown code block funciona")

    # Teste 5: JSON com texto antes e depois
    print("\n5. Testando JSON com texto antes e depois...")
    content_text = '''Baseado na conversa, aqui está minha decisão:

{
    "reasoning": "Usuário definiu hipótese claramente",
    "next_step": "suggest_agent",
    "message": "Posso chamar o Estruturador?",
    "agent_suggestion": {
        "agent": "structurer",
        "justification": "Precisa estruturar questão de pesquisa"
    }
}

Isso conclui a análise.'''
    result = extract_orchestrator_response(content_text)
    assert result["agent_suggestion"]["agent"] == "structurer"
    print("   ✅ Extração com texto adicional funciona")

    # Teste 6: JSON com mensagem multilinhas
    print("\n6. Testando JSON com mensagem multilinhas...")
    content_multiline = '''{
    "reasoning": "Análise detalhada",
    "next_step": "explore",
    "message": "Vejo duas direções possíveis:\\n\\nA) Validar como hipótese\\nB) Entender literatura\\n\\nQual faz sentido?",
    "agent_suggestion": null
}'''
    result = extract_orchestrator_response(content_multiline)
    assert "A) Validar" in result["message"]
    assert "B) Entender" in result["message"]
    print("   ✅ JSON com mensagem multilinhas funciona")

    # Teste 7: JSON com caracteres Unicode
    print("\n7. Testando JSON com caracteres Unicode...")
    content_unicode = '''{
    "reasoning": "Usuário mencionou métricas de qualidade",
    "next_step": "explore",
    "message": "Interessante! 🤔 Você quer focar em métricas quantitativas?",
    "agent_suggestion": null
}'''
    result = extract_orchestrator_response(content_unicode)
    assert "métricas" in result["reasoning"]
    assert "🤔" in result["message"]
    print("   ✅ JSON com Unicode funciona")

    # Teste 8: Validação de campo faltando
    print("\n8. Testando validação de campos obrigatórios...")
    content_missing = '''{
    "next_step": "explore",
    "message": "Conte mais",
    "agent_suggestion": null
}'''
    try:
        extract_orchestrator_response(content_missing)
        assert False, "Deveria ter lançado OrchestratorValidationError"
    except OrchestratorValidationError as e:
        assert "reasoning" in str(e).lower()
        print("   ✅ Validação de campos faltando funciona")

    # Teste 9: Validação de next_step inválido
    print("\n9. Testando validação de next_step inválido...")
    content_invalid_step = '''{
    "reasoning": "Análise",
    "next_step": "invalid_step",
    "message": "Conte mais",
    "agent_suggestion": null
}'''
    try:
        extract_orchestrator_response(content_invalid_step)
        assert False, "Deveria ter lançado OrchestratorValidationError"
    except OrchestratorValidationError as e:
        assert "next_step" in str(e).lower()
        print("   ✅ Validação de next_step inválido funciona")

    # Teste 10: Validação de agent_suggestion malformado
    print("\n10. Testando validação de agent_suggestion malformado...")
    content_malformed_agent = '''{
    "reasoning": "Análise",
    "next_step": "suggest_agent",
    "message": "Posso chamar?",
    "agent_suggestion": {
        "justification": "Faz sentido"
    }
}'''
    try:
        extract_orchestrator_response(content_malformed_agent)
        assert False, "Deveria ter lançado OrchestratorValidationError"
    except OrchestratorValidationError as e:
        assert "agent" in str(e).lower()
        print("   ✅ Validação de agent_suggestion malformado funciona")

    # Teste 11: Validação de string vazia
    print("\n11. Testando validação de strings vazias...")
    content_empty = '''{
    "reasoning": "",
    "next_step": "explore",
    "message": "Conte mais",
    "agent_suggestion": null
}'''
    try:
        extract_orchestrator_response(content_empty)
        assert False, "Deveria ter lançado OrchestratorValidationError"
    except OrchestratorValidationError as e:
        assert "reasoning" in str(e).lower() or "vazio" in str(e).lower()
        print("   ✅ Validação de strings vazias funciona")

    # Teste 12: Todos os valores válidos de next_step
    print("\n12. Testando todos os valores válidos de next_step...")
    valid_next_steps = ["explore", "suggest_agent", "clarify"]
    for step in valid_next_steps:
        content = f'''{{
    "reasoning": "Teste",
    "next_step": "{step}",
    "message": "Mensagem de teste",
    "agent_suggestion": null
}}'''
        result = extract_orchestrator_response(content)
        assert result["next_step"] == step
    print(f"   ✅ Todos os next_step válidos funcionam: {', '.join(valid_next_steps)}")

    # Teste 13: Verificar tipo de retorno
    print("\n13. Testando tipo de retorno (OrchestratorResponse)...")
    content_type = '''{
    "reasoning": "Teste de tipo",
    "next_step": "explore",
    "message": "Mensagem teste",
    "agent_suggestion": null
}'''
    result = extract_orchestrator_response(content_type)
    # TypedDict é um dict em runtime, mas vamos verificar as chaves
    assert isinstance(result, dict)
    assert set(result.keys()) == {"reasoning", "next_step", "message", "agent_suggestion"}
    print("   ✅ Tipo de retorno está correto")

    print("\n" + "=" * 70)
    print("TODOS OS TESTES PASSARAM! ✅")
    print("=" * 70)
    print("\nResumo:")
    print("  ✅ Parsing robusto de JSON (puro, markdown, com texto)")
    print("  ✅ Validação de campos obrigatórios")
    print("  ✅ Validação de tipos e valores")
    print("  ✅ Validação de next_step (explore, suggest_agent, clarify)")
    print("  ✅ Validação de agent_suggestion (estrutura correta)")
    print("  ✅ Error handling apropriado")
    print("  ✅ Suporte a Unicode e mensagens multilinhas")
    print("\nFunção extract_orchestrator_response está pronta para uso! 🎉")
    print("=" * 70)


if __name__ == "__main__":
    try:
        validate_orchestrator_json_parsing()
    except AssertionError as e:
        print(f"\n❌ ERRO: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERRO INESPERADO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
