"""
Testes unitários para função de extração de JSON de respostas do LLM.

Valida que a função extract_json_from_llm_response consegue parsear
JSON em diversos formatos retornados pelo LLM.
"""

import pytest
import json
from utils.json_parser import extract_json_from_llm_response

class TestExtractJsonFromLLMResponse:
    """Testes da função extract_json_from_llm_response."""

    def test_extract_pure_json(self):
        """Testa extração de JSON puro sem formatação adicional."""
        content = '{"status": "approved", "reason": "válido"}'
        result = extract_json_from_llm_response(content)

        assert result == {"status": "approved", "reason": "válido"}

    def test_extract_json_with_line_breaks(self):
        """Testa extração de JSON com line breaks dentro de strings."""
        content = '''{
    "decision": "approved",
    "justification": "A hipótese atende aos critérios:

    1. Testabilidade: POSITIVA
    2. Falseabilidade: POSITIVA"
}'''
        result = extract_json_from_llm_response(content)

        assert result["decision"] == "approved"
        assert "Testabilidade: POSITIVA" in result["justification"]

    def test_extract_json_from_markdown_code_block(self):
        """Testa extração de JSON dentro de markdown code block."""
        content = '''Aqui está a resposta:

```json
{
    "status": "rejected",
    "reason": "falta especificidade"
}
```

Espero que ajude!'''
        result = extract_json_from_llm_response(content)

        assert result == {"status": "rejected", "reason": "falta especificidade"}

    def test_extract_json_from_code_block_without_language(self):
        """Testa extração de JSON de code block sem especificar linguagem."""
        content = '''```
{
    "has_sufficient_info": false,
    "missing_info": "população não especificada"
}
```'''
        result = extract_json_from_llm_response(content)

        assert result["has_sufficient_info"] is False
        assert "população" in result["missing_info"]

    def test_extract_json_with_text_before_and_after(self):
        """Testa extração de JSON com texto adicional antes e depois."""
        content = '''Com base na análise, aqui está minha decisão:

{
    "decision": "approved",
    "justification": "Hipótese bem formulada"
}

Isso conclui a avaliação.'''
        result = extract_json_from_llm_response(content)

        assert result["decision"] == "approved"

    def test_extract_nested_json(self):
        """Testa extração de JSON com objetos aninhados."""
        content = '''{
    "status": "approved",
    "details": {
        "score": 9,
        "criteria": ["testabilidade", "falseabilidade"]
    }
}'''
        result = extract_json_from_llm_response(content)

        assert result["status"] == "approved"
        assert result["details"]["score"] == 9
        assert len(result["details"]["criteria"]) == 2

    def test_extract_json_with_unicode(self):
        """Testa extração de JSON com caracteres Unicode."""
        content = '{"mensagem": "Hipótese científica válida ✓", "ação": "aprovar"}'
        result = extract_json_from_llm_response(content)

        assert "válida" in result["mensagem"]
        assert result["ação"] == "aprovar"

    def test_fails_on_invalid_json(self):
        """Testa que a função lança erro quando não encontra JSON válido."""
        content = "Isto é apenas texto sem JSON algum"

        with pytest.raises(json.JSONDecodeError):
            extract_json_from_llm_response(content)

    def test_fails_on_incomplete_json(self):
        """Testa que a função lança erro com JSON incompleto."""
        content = '{"status": "approved", "reason": '

        with pytest.raises(json.JSONDecodeError):
            extract_json_from_llm_response(content)

    def test_extract_first_valid_json_when_multiple_present(self):
        """Testa que extrai o primeiro JSON válido quando há múltiplos."""
        content = '''Primeiro JSON inválido: { broken

Agora o JSON correto:
{
    "status": "approved",
    "reason": "válido"
}

E outro JSON depois:
{"outro": "valor"}'''
        result = extract_json_from_llm_response(content)

        # Deve extrair o primeiro JSON válido
        assert result["status"] == "approved"
        assert result["reason"] == "válido"

    def test_extract_json_with_escaped_quotes(self):
        """Testa extração de JSON com aspas escapadas."""
        content = r'{"message": "O autor disse: \"A hipótese é válida\""}'
        result = extract_json_from_llm_response(content)

        assert 'A hipótese é válida' in result["message"]

    def test_extract_json_with_arrays(self):
        """Testa extração de JSON com arrays."""
        content = '''{
    "criteria": ["testabilidade", "falseabilidade", "especificidade"],
    "scores": [8, 9, 7]
}'''
        result = extract_json_from_llm_response(content)

        assert len(result["criteria"]) == 3
        assert result["scores"][1] == 9
