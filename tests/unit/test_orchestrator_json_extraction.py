"""
Testes unitários para extração e validação de JSON do Orquestrador Conversacional.

Valida que extract_orchestrator_response consegue parsear e validar
respostas do Orquestrador no formato esperado pelo Épico 7 POC.

Versão: 1.0
Data: 14/11/2025
"""

import pytest
import json
from utils.json_parser import extract_orchestrator_response, OrchestratorValidationError


class TestExtractOrchestratorResponse:
    """Testes da função extract_orchestrator_response."""

    def test_extract_valid_explore_response(self):
        """Testa extração de resposta válida com next_step='explore'."""
        content = '''{
    "reasoning": "Usuário tem observação mas não especificou contexto",
    "next_step": "explore",
    "message": "Interessante! Me conta mais: onde você observou isso?",
    "agent_suggestion": null
}'''
        result = extract_orchestrator_response(content)

        assert result["reasoning"] == "Usuário tem observação mas não especificou contexto"
        assert result["next_step"] == "explore"
        assert result["message"] == "Interessante! Me conta mais: onde você observou isso?"
        assert result["agent_suggestion"] is None

    def test_extract_valid_suggest_agent_response(self):
        """Testa extração de resposta válida com agent_suggestion."""
        content = '''{
    "reasoning": "Hipótese estruturada com população e métricas definidas",
    "next_step": "suggest_agent",
    "message": "Posso chamar o Metodologista para validar?",
    "agent_suggestion": {
        "agent": "methodologist",
        "justification": "Hipótese pronta para validação metodológica"
    }
}'''
        result = extract_orchestrator_response(content)

        assert result["next_step"] == "suggest_agent"
        assert result["agent_suggestion"] is not None
        assert result["agent_suggestion"]["agent"] == "methodologist"
        assert result["agent_suggestion"]["justification"] == "Hipótese pronta para validação metodológica"

    def test_extract_valid_clarify_response(self):
        """Testa extração de resposta válida com next_step='clarify'."""
        content = '''{
    "reasoning": "Informação ambígua, preciso clarificar antes de sugerir direção",
    "next_step": "clarify",
    "message": "Você quer dizer produtividade em termos de tempo ou qualidade?",
    "agent_suggestion": null
}'''
        result = extract_orchestrator_response(content)

        assert result["next_step"] == "clarify"
        assert result["agent_suggestion"] is None

    def test_extract_from_markdown_code_block(self):
        """Testa extração de JSON dentro de markdown code block."""
        content = '''Aqui está minha análise:

```json
{
    "reasoning": "Análise do contexto",
    "next_step": "explore",
    "message": "Conte mais sobre isso",
    "agent_suggestion": null
}
```

Espero que ajude!'''
        result = extract_orchestrator_response(content)

        assert result["next_step"] == "explore"
        assert result["message"] == "Conte mais sobre isso"

    def test_extract_with_text_before_and_after(self):
        """Testa extração de JSON com texto adicional antes e depois."""
        content = '''Baseado na conversa, aqui está minha decisão:

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
        result = extract_orchestrator_response(content)

        assert result["next_step"] == "suggest_agent"
        assert result["agent_suggestion"]["agent"] == "structurer"

    def test_fails_on_missing_reasoning(self):
        """Testa que falha quando campo 'reasoning' está faltando."""
        content = '''{
    "next_step": "explore",
    "message": "Conte mais",
    "agent_suggestion": null
}'''
        with pytest.raises(OrchestratorValidationError) as exc_info:
            extract_orchestrator_response(content)

        assert "reasoning" in str(exc_info.value).lower()

    def test_fails_on_missing_next_step(self):
        """Testa que falha quando campo 'next_step' está faltando."""
        content = '''{
    "reasoning": "Análise",
    "message": "Conte mais",
    "agent_suggestion": null
}'''
        with pytest.raises(OrchestratorValidationError) as exc_info:
            extract_orchestrator_response(content)

        assert "next_step" in str(exc_info.value).lower()

    def test_fails_on_missing_message(self):
        """Testa que falha quando campo 'message' está faltando."""
        content = '''{
    "reasoning": "Análise",
    "next_step": "explore",
    "agent_suggestion": null
}'''
        with pytest.raises(OrchestratorValidationError) as exc_info:
            extract_orchestrator_response(content)

        assert "message" in str(exc_info.value).lower()

    def test_fails_on_missing_agent_suggestion(self):
        """Testa que falha quando campo 'agent_suggestion' está faltando."""
        content = '''{
    "reasoning": "Análise",
    "next_step": "explore",
    "message": "Conte mais"
}'''
        with pytest.raises(OrchestratorValidationError) as exc_info:
            extract_orchestrator_response(content)

        assert "agent_suggestion" in str(exc_info.value).lower()

    def test_fails_on_invalid_next_step(self):
        """Testa que falha quando next_step tem valor inválido."""
        content = '''{
    "reasoning": "Análise",
    "next_step": "invalid_step",
    "message": "Conte mais",
    "agent_suggestion": null
}'''
        with pytest.raises(OrchestratorValidationError) as exc_info:
            extract_orchestrator_response(content)

        assert "next_step" in str(exc_info.value).lower()
        assert "explore" in str(exc_info.value).lower() or "suggest_agent" in str(exc_info.value).lower()

    def test_fails_on_malformed_agent_suggestion_missing_agent(self):
        """Testa que falha quando agent_suggestion está sem campo 'agent'."""
        content = '''{
    "reasoning": "Análise",
    "next_step": "suggest_agent",
    "message": "Posso chamar?",
    "agent_suggestion": {
        "justification": "Faz sentido"
    }
}'''
        with pytest.raises(OrchestratorValidationError) as exc_info:
            extract_orchestrator_response(content)

        assert "agent" in str(exc_info.value).lower()

    def test_fails_on_malformed_agent_suggestion_missing_justification(self):
        """Testa que falha quando agent_suggestion está sem campo 'justification'."""
        content = '''{
    "reasoning": "Análise",
    "next_step": "suggest_agent",
    "message": "Posso chamar?",
    "agent_suggestion": {
        "agent": "methodologist"
    }
}'''
        with pytest.raises(OrchestratorValidationError) as exc_info:
            extract_orchestrator_response(content)

        assert "justification" in str(exc_info.value).lower()

    def test_fails_on_agent_suggestion_wrong_type(self):
        """Testa que falha quando agent_suggestion não é dict nem null."""
        content = '''{
    "reasoning": "Análise",
    "next_step": "explore",
    "message": "Conte mais",
    "agent_suggestion": "invalid_string"
}'''
        with pytest.raises(OrchestratorValidationError) as exc_info:
            extract_orchestrator_response(content)

        assert "agent_suggestion" in str(exc_info.value).lower()

    def test_extract_with_multiline_message(self):
        """Testa extração de JSON com mensagem multilinhas."""
        content = '''{
    "reasoning": "Análise detalhada",
    "next_step": "explore",
    "message": "Vejo duas direções possíveis:\\n\\nA) Validar como hipótese\\nB) Entender literatura\\n\\nQual faz sentido?",
    "agent_suggestion": null
}'''
        result = extract_orchestrator_response(content)

        assert result["next_step"] == "explore"
        assert "A) Validar" in result["message"]
        assert "B) Entender" in result["message"]

    def test_extract_with_unicode_characters(self):
        """Testa extração de JSON com caracteres Unicode."""
        content = '''{
    "reasoning": "Usuário mencionou métricas de qualidade",
    "next_step": "explore",
    "message": "Interessante! 🤔 Você quer focar em métricas quantitativas?",
    "agent_suggestion": null
}'''
        result = extract_orchestrator_response(content)

        assert "métricas" in result["reasoning"]
        assert "🤔" in result["message"]

    def test_extract_with_nested_quotes(self):
        """Testa extração de JSON com aspas aninhadas."""
        content = r'''{
    "reasoning": "O usuário disse: \"quero testar hipótese\"",
    "next_step": "suggest_agent",
    "message": "Entendi que você quer testar a hipótese!",
    "agent_suggestion": {
        "agent": "methodologist",
        "justification": "Validação de \"rigor científico\" necessária"
    }
}'''
        result = extract_orchestrator_response(content)

        assert "quero testar hipótese" in result["reasoning"]
        assert "rigor científico" in result["agent_suggestion"]["justification"]

    def test_fails_on_invalid_json(self):
        """Testa que falha quando não consegue encontrar JSON válido."""
        content = "Isto é apenas texto sem JSON algum"

        with pytest.raises((json.JSONDecodeError, OrchestratorValidationError)):
            extract_orchestrator_response(content)

    def test_fails_on_incomplete_json(self):
        """Testa que falha com JSON incompleto."""
        content = '{"reasoning": "Análise", "next_step": '

        with pytest.raises((json.JSONDecodeError, OrchestratorValidationError)):
            extract_orchestrator_response(content)

    def test_extract_all_valid_next_steps(self):
        """Testa que todos os valores válidos de next_step são aceitos."""
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

    def test_empty_strings_are_invalid(self):
        """Testa que strings vazias em campos obrigatórios são inválidas."""
        content = '''{
    "reasoning": "",
    "next_step": "explore",
    "message": "Conte mais",
    "agent_suggestion": null
}'''
        with pytest.raises(OrchestratorValidationError) as exc_info:
            extract_orchestrator_response(content)

        assert "reasoning" in str(exc_info.value).lower() or "vazio" in str(exc_info.value).lower()
