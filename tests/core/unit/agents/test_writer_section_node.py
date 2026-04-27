"""Testes unitários para writer_section_node — C-ENSAIO-3.2."""

from unittest.mock import MagicMock, Mock, patch

from langchain_core.messages import HumanMessage

from core.agents.writer.nodes import writer_node, writer_section_node


def _mock_response(text: str) -> Mock:
    response = Mock()
    response.content = text
    return response


class TestWriterSectionNode:
    def test_returns_section_content_key(self):
        with patch("core.agents.writer.nodes.create_anthropic_client") as mock_create:
            mock_llm = MagicMock()
            mock_llm.invoke.return_value = _mock_response("Corpo da seção em markdown.")
            mock_create.return_value = mock_llm

            result = writer_section_node(
                {
                    "messages": [HumanMessage(content="Experimento X")],
                    "focal_argument": None,
                    "section_title": "Metodologia",
                    "current_body": "",
                    "article_context": "",
                    "product_context": None,
                }
            )

        assert isinstance(result, dict)
        assert "section_content" in result
        assert isinstance(result["section_content"], str)
        assert result["section_content"] != ""

    def test_generation_mode_with_empty_current_body(self):
        captured = {}

        def _capture(messages):
            captured["prompt"] = messages[0].content
            return _mock_response("Conteúdo gerado.")

        with patch("core.agents.writer.nodes.create_anthropic_client") as mock_create:
            mock_llm = MagicMock()
            mock_llm.invoke.side_effect = _capture
            mock_create.return_value = mock_llm

            writer_section_node(
                {
                    "messages": [],
                    "focal_argument": None,
                    "section_title": "Resultados",
                    "current_body": "",
                    "article_context": "",
                    "product_context": None,
                }
            )

        assert "Resultados" in captured["prompt"]
        # Modo geração: sem instrução de refinamento
        assert "REGENERAÇÃO" not in captured["prompt"]

    def test_refinement_mode_with_existing_body(self):
        captured = {}

        def _capture(messages):
            captured["prompt"] = messages[0].content
            return _mock_response("Versão refinada.")

        with patch("core.agents.writer.nodes.create_anthropic_client") as mock_create:
            mock_llm = MagicMock()
            mock_llm.invoke.side_effect = _capture
            mock_create.return_value = mock_llm

            writer_section_node(
                {
                    "messages": [HumanMessage(content="Feedback do pesquisador")],
                    "focal_argument": None,
                    "section_title": "Discussão",
                    "current_body": "Rascunho anterior.",
                    "article_context": "",
                    "product_context": None,
                }
            )

        assert "REGENERAÇÃO" in captured["prompt"]

    def test_writer_node_non_regression(self):
        """writer_node existente não deve ser afetado (não-regressão C-ENSAIO-2)."""
        with patch("core.agents.writer.nodes.create_anthropic_client") as mock_create:
            mock_llm = MagicMock()
            mock_llm.invoke.return_value = _mock_response("# Artigo\n\nConteúdo.")
            mock_create.return_value = mock_llm

            result = writer_node(
                {
                    "messages": [HumanMessage(content="Experimento Y")],
                    "focal_argument": None,
                    "previous_article": None,
                    "product_context": None,
                }
            )

        assert "article" in result
        assert isinstance(result["article"], str)

    def test_handles_missing_optional_fields(self):
        with patch("core.agents.writer.nodes.create_anthropic_client") as mock_create:
            mock_llm = MagicMock()
            mock_llm.invoke.return_value = _mock_response("Conteúdo mínimo.")
            mock_create.return_value = mock_llm

            result = writer_section_node({})

        assert "section_content" in result
