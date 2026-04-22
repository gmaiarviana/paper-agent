"""
Unit test do writer_node (C-ENSAIO-2.1).

Escopo mínimo declarado no ROADMAP: "validar que writer_node retorna dict com
chave article quando invocado com input mínimo (mock do LLM)".
"""

from __future__ import annotations

from unittest.mock import patch

from langchain_core.messages import AIMessage, HumanMessage

from core.agents.writer.nodes import writer_node


class _FakeLLM:
    """Stub mínimo que devolve sempre o mesmo artigo markdown."""

    def __init__(self, response_text: str = "# Artigo\n\nConteúdo gerado pelo mock."):
        self._response_text = response_text
        self.calls = []

    def invoke(self, messages):
        self.calls.append(messages)
        return AIMessage(content=self._response_text)


def _patch_llm(monkey_response: str = "# Artigo\n\nConteúdo gerado pelo mock.") -> _FakeLLM:
    fake = _FakeLLM(monkey_response)
    patcher = patch(
        "core.agents.writer.nodes.create_anthropic_client",
        return_value=fake,
    )
    patcher.start()
    return fake, patcher


def test_writer_node_returns_article_on_minimal_input():
    """writer_node com input mínimo retorna dict contendo a chave article."""
    fake, patcher = _patch_llm()
    try:
        state = {
            "messages": [HumanMessage(content="Observei que método X reduz tempo.")],
            "focal_argument": None,
            "previous_article": None,
            "product_context": None,
        }
        result = writer_node(state)
    finally:
        patcher.stop()

    assert isinstance(result, dict)
    assert "article" in result
    assert isinstance(result["article"], str)
    assert result["article"].startswith("#")
    assert len(fake.calls) == 1


def test_writer_node_refinement_mode_includes_previous_article_in_prompt():
    """Quando previous_article é passado, o prompt contém o artigo anterior."""
    fake, patcher = _patch_llm("# Artigo Refinado\n\nVersão 2.")
    try:
        state = {
            "messages": [
                HumanMessage(content="Observei X."),
                AIMessage(content="Organizei sua ideia."),
                HumanMessage(content="Deixa mais conciso."),
            ],
            "focal_argument": {"intent": "test_hypothesis", "subject": "X"},
            "previous_article": "# Artigo V1\n\nTexto original.",
            "product_context": "Pesquisador transformando experimento em artigo IMRaD.",
        }
        result = writer_node(state)
    finally:
        patcher.stop()

    assert result["article"].startswith("# Artigo Refinado")
    # Conferir que o prompt enviado ao LLM contém o artigo anterior e o contexto do produto.
    prompt_content = fake.calls[0][0].content
    assert "ARTIGO ANTERIOR" in prompt_content
    assert "Texto original" in prompt_content
    assert "CONTEXTO DO PRODUTO" in prompt_content
    assert "pesquisador transformando" in prompt_content.lower()


def test_writer_node_rejects_non_dict_state():
    """Entrada não-dict levanta TypeError (contrato explícito)."""
    import pytest

    with pytest.raises(TypeError):
        writer_node("not a dict")  # type: ignore[arg-type]
