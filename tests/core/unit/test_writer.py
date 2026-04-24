"""Unit tests for the Writer node (C-ENSAIO-2)."""

from unittest.mock import MagicMock, Mock, patch

from langchain_core.messages import AIMessage, HumanMessage

from core.agents.writer.nodes import writer_node


def _mock_response(text: str) -> Mock:
    response = Mock()
    response.content = text
    return response


class TestWriterNode:
    """Contract tests for writer_node — C-ENSAIO-2.1 / 2.4."""

    def test_returns_dict_with_article_key_on_minimal_input(self):
        with patch("core.agents.writer.nodes.create_anthropic_client") as mock_create:
            mock_llm = MagicMock()
            mock_llm.invoke.return_value = _mock_response("# Artigo\n\nConteúdo.")
            mock_create.return_value = mock_llm

            result = writer_node(
                {
                    "messages": [HumanMessage(content="Experimento X deu resultado Y")],
                    "focal_argument": None,
                    "previous_article": None,
                    "product_context": None,
                }
            )

        assert isinstance(result, dict)
        assert "article" in result
        assert isinstance(result["article"], str)
        assert result["article"].startswith("# Artigo")

    def test_handles_completely_empty_state(self):
        with patch("core.agents.writer.nodes.create_anthropic_client") as mock_create:
            mock_llm = MagicMock()
            mock_llm.invoke.return_value = _mock_response("# Rascunho\n\n_em construção_")
            mock_create.return_value = mock_llm

            result = writer_node({})

        assert "article" in result
        assert result["article"].startswith("# Rascunho")

    def test_previous_article_triggers_refinement_prompt(self):
        captured = {}

        def _capture(messages):
            captured["prompt"] = messages[0].content
            return _mock_response("# Versão Refinada\n\nMais conciso.")

        with patch("core.agents.writer.nodes.create_anthropic_client") as mock_create:
            mock_llm = MagicMock()
            mock_llm.invoke.side_effect = _capture
            mock_create.return_value = mock_llm

            result = writer_node(
                {
                    "messages": [
                        HumanMessage(content="Experimento X"),
                        AIMessage(content="# Versão 1\n\nOriginal extenso."),
                        HumanMessage(content="deixa mais conciso"),
                    ],
                    "previous_article": "# Versão 1\n\nOriginal extenso.",
                }
            )

        assert "ARTIGO ANTERIOR" in captured["prompt"]
        assert "Versão 1" in captured["prompt"]
        assert "deixa mais conciso" in captured["prompt"]
        assert result["article"].startswith("# Versão Refinada")

    def test_product_context_is_injected_when_provided(self):
        captured = {}

        def _capture(messages):
            captured["prompt"] = messages[0].content
            return _mock_response("# Artigo\n\nOK.")

        with patch("core.agents.writer.nodes.create_anthropic_client") as mock_create:
            mock_llm = MagicMock()
            mock_llm.invoke.side_effect = _capture
            mock_create.return_value = mock_llm

            writer_node(
                {
                    "messages": [HumanMessage(content="hola")],
                    "product_context": "Laboratório de escrita para pesquisadores em IA agêntica.",
                }
            )

        assert "## CONTEXTO DO PRODUTO" in captured["prompt"]
        assert "IA agêntica" in captured["prompt"]

    def test_product_context_absent_does_not_leak_section(self):
        captured = {}

        def _capture(messages):
            captured["prompt"] = messages[0].content
            return _mock_response("# Artigo\n\nOK.")

        with patch("core.agents.writer.nodes.create_anthropic_client") as mock_create:
            mock_llm = MagicMock()
            mock_llm.invoke.side_effect = _capture
            mock_create.return_value = mock_llm

            writer_node({"messages": [HumanMessage(content="hola")]})

        assert "## CONTEXTO DO PRODUTO" not in captured["prompt"]
        # Placeholders devem ter sido substituídos (vazios, mas substituídos):
        assert "{product_context_section}" not in captured["prompt"]
        assert "{focal_argument_section}" not in captured["prompt"]
        assert "{previous_article_section}" not in captured["prompt"]
        assert "{conversation_section}" not in captured["prompt"]
