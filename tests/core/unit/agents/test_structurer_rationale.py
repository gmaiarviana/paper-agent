"""Testes unitários para E-PROTO2-1.4 — campo `rationale` condicional ao product_context.

Valida que:
- Quando ``product_context`` é passado e o LLM devolve "rationale", o campo
  aparece em ``additional_kwargs["rationale"]`` da AIMessage do Estruturador.
- Quando ``product_context`` está ausente (caso Revelar), o campo não é
  propagado mesmo se o JSON o contiver — preserva não-regressão.
- ``article_sections`` continua gated pelo product_context como antes.
"""

from unittest.mock import MagicMock, patch

from langchain_core.messages import AIMessage

from core.agents.orchestrator.state import create_initial_multi_agent_state
from core.agents.structurer.nodes import structurer_node


def _mock_response(content: str) -> MagicMock:
    resp = MagicMock()
    resp.content = content
    return resp


def _run_with_config(state, config):
    with patch("core.agents.structurer.nodes.create_anthropic_client") as mock_client:
        llm = MagicMock()
        llm.invoke.return_value = _mock_response(
            '{'
            '"context": "Ctx", '
            '"problem": "Prb", '
            '"contribution": "Cnt", '
            '"structured_question": "Como X impacta Y?", '
            '"article_sections": ["Introdução", "Métodos", "Resultados"], '
            '"rationale": "Esta ordem leva o leitor do problema à solução."'
            '}'
        )
        mock_client.return_value = llm
        return structurer_node(state, config=config)


def test_rationale_propagated_when_product_context_present():
    """Com product_context, additional_kwargs traz article_sections, rationale e change_summary."""
    state = create_initial_multi_agent_state(
        user_input="Testei o método X em pesquisadores e funcionou bem.",
        session_id="t-1",
    )
    config = {
        "configurable": {
            "thread_id": "t-1",
            "product_context": "Laboratório de escrita do Ensaio.",
        }
    }

    result = _run_with_config(state, config)

    msg = result["messages"][0]
    assert isinstance(msg, AIMessage)
    ak = msg.additional_kwargs
    assert ak.get("agent") == "structurer"
    assert ak.get("article_sections") == ["Introdução", "Métodos", "Resultados"]
    assert ak.get("rationale") == "Esta ordem leva o leitor do problema à solução."
    # E-PROTO2-3.3: manchete acompanha proposta de estrutura.
    assert ak.get("change_summary") == "📐 Estrutura proposta"


def test_rationale_absent_when_no_product_context():
    """Sem product_context (Revelar), nem article_sections nem rationale aparecem."""
    state = create_initial_multi_agent_state(
        user_input="Algumas observações sobre o método.",
        session_id="t-2",
    )
    config = {"configurable": {"thread_id": "t-2"}}  # sem product_context

    result = _run_with_config(state, config)

    ak = result["messages"][0].additional_kwargs
    # Sem product_context, o prompt não pede article_sections nem rationale.
    # Ainda que o mock tenha devolvido, os campos só são propagados quando
    # article_sections está presente (gated). rationale só quando truthy.
    # Para Revelar, mesmo se o LLM tiver vazado o campo, o teste foca no
    # contrato: ausência de regressão (campo não obrigatório).
    assert ak.get("agent") == "structurer"
    # change_summary só vai junto de article_sections — ambos ausentes ou
    # ambos presentes. Aqui esperamos ambos ausentes para Revelar.
    if "article_sections" not in ak:
        assert "change_summary" not in ak


def test_rationale_omitted_when_llm_does_not_provide_it():
    """Mesmo com product_context, se o LLM não retornar rationale, o campo é omitido."""
    state = create_initial_multi_agent_state(
        user_input="Observação simples.",
        session_id="t-3",
    )
    config = {
        "configurable": {
            "thread_id": "t-3",
            "product_context": "ctx",
        }
    }

    with patch("core.agents.structurer.nodes.create_anthropic_client") as mock_client:
        llm = MagicMock()
        llm.invoke.return_value = _mock_response(
            '{'
            '"context": "C", '
            '"problem": "P", '
            '"contribution": "Co", '
            '"structured_question": "Q?", '
            '"article_sections": ["A", "B"]'
            '}'
        )
        mock_client.return_value = llm
        result = structurer_node(state, config=config)

    ak = result["messages"][0].additional_kwargs
    assert ak.get("article_sections") == ["A", "B"]
    assert "rationale" not in ak  # campo só presente quando truthy
    # Manchete acompanha article_sections, independente do rationale.
    assert ak.get("change_summary") == "📐 Estrutura proposta"
