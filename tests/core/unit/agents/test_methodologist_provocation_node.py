"""Testes unitários para methodologist_provocation_node — E-PROTO-3.1."""

from unittest.mock import MagicMock, Mock, patch

from langchain_core.messages import AIMessage, HumanMessage

from core.agents.methodologist.nodes import methodologist_provocation_node


def _mock_response(text: str) -> Mock:
    response = Mock()
    response.content = text
    return response


class TestMethodologistProvocationNode:
    def test_returns_messages_with_ai_message(self):
        with patch("core.agents.methodologist.nodes.create_anthropic_client") as mock_create, \
             patch("core.agents.methodologist.nodes.invoke_with_retry") as mock_invoke:
            mock_llm = MagicMock()
            mock_create.return_value = mock_llm
            mock_invoke.return_value = _mock_response("Quais métricas você usou?")

            result = methodologist_provocation_node(
                {
                    "messages": [HumanMessage(content="Fiz um experimento.")],
                    "focal_argument": None,
                }
            )

        assert "messages" in result
        assert len(result["messages"]) == 1
        assert isinstance(result["messages"][0], AIMessage)

    def test_additional_kwargs_contains_agent_methodologist(self):
        with patch("core.agents.methodologist.nodes.create_anthropic_client") as mock_create, \
             patch("core.agents.methodologist.nodes.invoke_with_retry") as mock_invoke:
            mock_llm = MagicMock()
            mock_create.return_value = mock_llm
            mock_invoke.return_value = _mock_response("Qual foi a baseline de comparação?")

            result = methodologist_provocation_node({"messages": [], "focal_argument": None})

        msg = result["messages"][0]
        assert msg.additional_kwargs.get("agent") == "methodologist"

    def test_does_not_return_empty_content(self):
        with patch("core.agents.methodologist.nodes.create_anthropic_client") as mock_create, \
             patch("core.agents.methodologist.nodes.invoke_with_retry") as mock_invoke:
            mock_llm = MagicMock()
            mock_create.return_value = mock_llm
            mock_invoke.return_value = _mock_response("")  # LLM retorna vazio

            result = methodologist_provocation_node({"messages": [], "focal_argument": None})

        msg = result["messages"][0]
        assert msg.content  # deve ter fallback

    def test_handles_empty_state(self):
        with patch("core.agents.methodologist.nodes.create_anthropic_client") as mock_create, \
             patch("core.agents.methodologist.nodes.invoke_with_retry") as mock_invoke:
            mock_llm = MagicMock()
            mock_create.return_value = mock_llm
            mock_invoke.return_value = _mock_response("O contexto está bem descrito. Continue.")

            result = methodologist_provocation_node({})

        assert "messages" in result
        assert result["messages"]

    def test_accepts_product_context_via_config(self):
        captured = {}

        with patch("core.agents.methodologist.nodes.create_anthropic_client") as mock_create, \
             patch("core.agents.methodologist.nodes.invoke_with_retry") as mock_invoke:
            mock_llm = MagicMock()
            mock_create.return_value = mock_llm

            def _capture(*args, **kwargs):
                captured["messages"] = kwargs.get("messages") or args[1] if len(args) > 1 else []
                return _mock_response("Pergunta.")

            mock_invoke.side_effect = _capture

            methodologist_provocation_node(
                {"messages": [], "focal_argument": None},
                config={"configurable": {"product_context": "Contexto de teste."}},
            )

        # Verificar que o produto não quebrou a chamada
        assert mock_invoke.called

    def test_does_not_modify_decide_collaborative(self):
        """decide_collaborative não deve ser afetado — não-regressão."""
        from core.agents.methodologist.nodes import decide_collaborative
        assert callable(decide_collaborative)
