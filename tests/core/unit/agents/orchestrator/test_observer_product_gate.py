"""Gate do Observer por product_context — PROTO-ENSAIO-2.

Quando o Orquestrador roda para um produto (product_context presente em
``config.configurable``), a consulta ao Observer (`_consult_observer`) é
pulada — produtos que não consomem ``clarity_evaluation``/``variation_analysis``
(caso do Ensaio) não devem arcar com ~2 chamadas LLM extras por turno.

Para Revelar (sem product_context), o Observer continua sendo consultado.
"""

from unittest.mock import Mock, patch

from core.agents.orchestrator.nodes import orchestrator_node
from core.agents.orchestrator.state import create_initial_multi_agent_state

_VALID_ORCH_JSON = """
{
  "reasoning": "Teste do gate.",
  "next_step": "explore",
  "message": "Me conta mais.",
  "agent_suggestion": null,
  "focal_argument": {
    "intent": "explore",
    "subject": "teste",
    "population": "not specified",
    "metrics": "not specified",
    "article_type": "unclear"
  },
  "cognitive_model": {
    "claim": "teste",
    "proposicoes": [],
    "open_questions": [],
    "contradictions": [],
    "solid_grounds": [],
    "context": {}
  }
}
"""


def _mock_llm_response() -> Mock:
    resp = Mock()
    resp.content = _VALID_ORCH_JSON
    resp.response_metadata = {
        "usage_metadata": {"input_tokens": 100, "output_tokens": 50}
    }
    return resp


def test_observer_skipped_when_product_context_present():
    """Ensaio (product_context setado) não dispara _consult_observer."""
    state = create_initial_multi_agent_state(
        user_input="Quero estruturar um artigo sobre meu experimento.",
        session_id="ensaio-1",
    )

    with patch(
        "core.agents.orchestrator.nodes.invoke_with_retry",
        return_value=_mock_llm_response(),
    ), patch(
        "core.agents.orchestrator.nodes._consult_observer"
    ) as mock_observer:
        result = orchestrator_node(
            state,
            config={
                "configurable": {
                    "thread_id": "ensaio-1",
                    "product_context": "Laboratório de escrita do Ensaio.",
                }
            },
        )

    mock_observer.assert_not_called()
    assert result["clarity_evaluation"] is None
    assert result["variation_analysis"] is None


def test_observer_invoked_when_no_product_context():
    """Revelar (sem product_context) continua consultando o Observer."""
    state = create_initial_multi_agent_state(
        user_input="Observei que LLMs ajudam na produtividade.",
        session_id="revelar-1",
    )

    with patch(
        "core.agents.orchestrator.nodes.invoke_with_retry",
        return_value=_mock_llm_response(),
    ), patch(
        "core.agents.orchestrator.nodes._consult_observer",
        return_value={
            "clarity_evaluation": {"clarity_level": "clara"},
            "variation_analysis": None,
            "needs_checkpoint": False,
            "checkpoint_reason": None,
        },
    ) as mock_observer:
        result = orchestrator_node(
            state,
            config={"configurable": {"thread_id": "revelar-1"}},
        )

    mock_observer.assert_called_once()
    assert result["clarity_evaluation"] == {"clarity_level": "clara"}
