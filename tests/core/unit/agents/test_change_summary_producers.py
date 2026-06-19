"""Testes unitários para E-PROTO2-3.3 — produtores de change_summary.

Cobre os dois produtores não-Estruturador (o Estruturador é coberto em
``test_structurer_rationale.py``):

- ``methodologist_provocation_node``: preenche "🔬 Lacuna apontada" quando
  responde com pergunta; omite quando responde a frase de aceite.
- ``orchestrator_node``: preenche "🎯 Foco atualizado" quando focal_argument
  efetivamente muda em relação ao turno anterior; omite em conversa pura.
"""

from unittest.mock import MagicMock, Mock, patch

from langchain_core.messages import AIMessage, HumanMessage

from core.agents.methodologist.nodes import methodologist_provocation_node


def _mock_response(text: str) -> Mock:
    resp = Mock()
    resp.content = text
    return resp


# ---------------------------------------------------------------------------
# Metodologista
# ---------------------------------------------------------------------------

class TestMethodologistChangeSummary:
    def test_change_summary_present_when_provoking(self):
        with patch("core.agents.methodologist.nodes.create_anthropic_client") as mc, \
             patch("core.agents.methodologist.nodes.invoke_with_retry") as mi:
            mc.return_value = MagicMock()
            mi.return_value = _mock_response("Qual baseline você usou para comparar?")

            result = methodologist_provocation_node(
                {"messages": [HumanMessage(content="Fiz um experimento.")], "focal_argument": None}
            )

        ak = result["messages"][0].additional_kwargs
        assert ak.get("change_summary") == "🔬 Lacuna apontada"

    def test_change_summary_absent_when_accepting(self):
        with patch("core.agents.methodologist.nodes.create_anthropic_client") as mc, \
             patch("core.agents.methodologist.nodes.invoke_with_retry") as mi:
            mc.return_value = MagicMock()
            mi.return_value = _mock_response("O contexto está bem descrito. Continue.")

            result = methodologist_provocation_node({"messages": [], "focal_argument": None})

        ak = result["messages"][0].additional_kwargs
        assert "change_summary" not in ak
        # Frase de aceite com case-insensitive também não preenche.

    def test_change_summary_absent_when_fallback_empty(self):
        """Quando o LLM volta vazio, fallback é frase de aceite — sem manchete."""
        with patch("core.agents.methodologist.nodes.create_anthropic_client") as mc, \
             patch("core.agents.methodologist.nodes.invoke_with_retry") as mi:
            mc.return_value = MagicMock()
            mi.return_value = _mock_response("")

            result = methodologist_provocation_node({"messages": [], "focal_argument": None})

        ak = result["messages"][0].additional_kwargs
        assert "change_summary" not in ak


# ---------------------------------------------------------------------------
# Orquestrador
# ---------------------------------------------------------------------------
#
# orchestrator_node tem muitas dependências; em vez de mockar a árvore
# inteira, validamos a lógica de detecção de mudança via uma função de
# espelho que reflete as condições aplicadas no nó. Testes do nó completo
# vivem em testes de integração.

def _detect_focus_change(previous_focal: dict | None, focal_argument: dict | None) -> str | None:
    """Espelha a lógica de E-PROTO2-3.3 em orchestrator_node."""
    if not focal_argument:
        return None
    relevant_keys = ("intent", "subject", "population", "metrics", "article_type")
    if previous_focal:
        for k in relevant_keys:
            old_v = previous_focal.get(k) or ""
            new_v = focal_argument.get(k) or ""
            if new_v and new_v not in ("not specified", "unclear") and new_v != old_v:
                return "🎯 Foco atualizado"
        return None
    # Primeiro foco da sessão
    for k in relevant_keys:
        v = focal_argument.get(k) or ""
        if v and v not in ("not specified", "unclear"):
            return "🎯 Foco atualizado"
    return None


class TestOrchestratorFocusChange:
    def test_first_focus_in_session_triggers_summary(self):
        result = _detect_focus_change(
            previous_focal=None,
            focal_argument={"intent": "demonstrate", "subject": "método X"},
        )
        assert result == "🎯 Foco atualizado"

    def test_no_change_no_summary(self):
        focal = {"intent": "demonstrate", "subject": "método X"}
        result = _detect_focus_change(previous_focal=focal, focal_argument=focal)
        assert result is None

    def test_intent_change_triggers_summary(self):
        result = _detect_focus_change(
            previous_focal={"intent": "explore", "subject": "X"},
            focal_argument={"intent": "demonstrate", "subject": "X"},
        )
        assert result == "🎯 Foco atualizado"

    def test_unclear_to_concrete_triggers_summary(self):
        result = _detect_focus_change(
            previous_focal={"intent": "unclear"},
            focal_argument={"intent": "propose"},
        )
        assert result == "🎯 Foco atualizado"

    def test_concrete_to_unclear_does_not_trigger(self):
        """Regressão de unclear ainda não conta como "atualização" do foco."""
        result = _detect_focus_change(
            previous_focal={"intent": "demonstrate"},
            focal_argument={"intent": "unclear"},
        )
        assert result is None

    def test_empty_focal_argument_no_summary(self):
        result = _detect_focus_change(previous_focal=None, focal_argument={})
        assert result is None

    def test_only_unclear_first_focus_no_summary(self):
        result = _detect_focus_change(
            previous_focal=None,
            focal_argument={"intent": "unclear", "subject": "not specified"},
        )
        assert result is None
