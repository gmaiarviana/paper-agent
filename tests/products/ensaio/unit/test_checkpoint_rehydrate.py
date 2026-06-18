"""Testes do recovery de delta perdido na reconexão de websocket.

Cobre o comportamento de ``EnsaioState._sync_with_checkpoint_if_completed``:
quando o backend terminou um turno mas o delta ``messages`` /
``processing_agent=""`` não chegou ao cliente (típico de socket que cai
durante turno > limiar de ping), a UI deve rehidratar dos dados do
checkpoint do LangGraph ao re-disparar ``initialize``.
"""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from langchain_core.messages import AIMessage, HumanMessage

from products.ensaio.app.state import EnsaioState


def _make_state() -> SimpleNamespace:
    """Instância simulada de ``EnsaioState`` com atributos relevantes."""
    obj = SimpleNamespace(
        messages=[],
        langchain_history=[],
        focal_argument={},
        current_article=[],
        processing_agent="",
        thread_id="t-1",
        product_context="Ensaio test",
        pending_structure_proposal={},
        editing_proposal=False,
        proposal_draft=[],
        proposal_rationale_draft="",
        proposal_edit_error="",
    )
    # Métodos privados (que começam com `_`) não são wrapped por
    # Reflex em EventHandler — vivem como função simples.
    attr = getattr(EnsaioState, "_sync_with_checkpoint_if_completed")
    fn = getattr(attr, "fn", attr)
    obj._sync_with_checkpoint_if_completed = fn.__get__(obj, type(obj))
    return obj


def _snapshot(messages: list, focal_argument: dict | None = None):
    """Mock de ``graph.get_state(config)``."""
    return SimpleNamespace(
        values={
            "messages": messages,
            "focal_argument": focal_argument or {},
        }
    )


def test_rehydrate_when_backend_has_more_ai_messages_than_ui():
    """Backend terminou turno mas UI não recebeu delta → rehidrata."""
    state = _make_state()
    state.processing_agent = "orchestrator"  # spinner preso
    state.messages = [
        {"role": "user", "agent": "user", "content": "ola",
         "content_html": "", "timestamp": "", "change_summary": ""},
    ]

    graph_messages = [
        HumanMessage(content="ola"),
        AIMessage(
            content="resposta do orquestrador",
            additional_kwargs={"agent": "orchestrator",
                               "change_summary": "🎯 Foco atualizado"},
        ),
    ]
    fake_graph = MagicMock()
    fake_graph.get_state.return_value = _snapshot(
        graph_messages, focal_argument={"intent": "explore"}
    )

    with patch(
        "products.ensaio.app.graph.create_ensaio_graph",
        return_value=fake_graph,
    ):
        state._sync_with_checkpoint_if_completed()

    assert state.processing_agent == ""  # spinner some
    assert len(state.messages) == 2
    assert state.messages[1]["role"] == "assistant"
    assert state.messages[1]["agent"] == "orchestrator"
    assert "resposta" in state.messages[1]["content"]
    assert state.messages[1]["change_summary"] == "🎯 Foco atualizado"
    assert state.focal_argument == {"intent": "explore"}
    assert len(state.langchain_history) == 2


def test_no_op_when_backend_synced_with_ui():
    """Backend e UI têm a mesma contagem de AI msgs → não rehidrata."""
    state = _make_state()
    state.processing_agent = "orchestrator"
    state.messages = [
        {"role": "user", "agent": "user", "content": "ola",
         "content_html": "", "timestamp": "", "change_summary": ""},
        {"role": "assistant", "agent": "orchestrator", "content": "resp",
         "content_html": "", "timestamp": "", "change_summary": ""},
    ]
    original_messages = list(state.messages)

    graph_messages = [
        HumanMessage(content="ola"),
        AIMessage(content="resp", additional_kwargs={"agent": "orchestrator"}),
    ]
    fake_graph = MagicMock()
    fake_graph.get_state.return_value = _snapshot(graph_messages)

    with patch(
        "products.ensaio.app.graph.create_ensaio_graph",
        return_value=fake_graph,
    ):
        state._sync_with_checkpoint_if_completed()

    assert state.processing_agent == "orchestrator"  # mantém spinner
    assert state.messages == original_messages


def test_no_op_when_thread_id_missing():
    """Sem thread_id (sessão nunca processou turno), nada a rehidratar."""
    state = _make_state()
    state.thread_id = ""
    state.processing_agent = "orchestrator"

    fake_graph = MagicMock()
    with patch(
        "products.ensaio.app.graph.create_ensaio_graph",
        return_value=fake_graph,
    ):
        state._sync_with_checkpoint_if_completed()

    fake_graph.get_state.assert_not_called()


def test_rehydrate_propagates_pending_structure_proposal():
    """Se o turno cujo delta se perdeu trouxe proposta de estrutura,
    o ``pending_structure_proposal`` é reconstruído ao rehidratar."""
    state = _make_state()
    state.processing_agent = "orchestrator"
    state.messages = [
        {"role": "user", "agent": "user", "content": "experimento",
         "content_html": "", "timestamp": "", "change_summary": ""},
    ]

    graph_messages = [
        HumanMessage(content="experimento"),
        AIMessage(
            content="estrutura sugerida",
            additional_kwargs={
                "agent": "structurer",
                "article_sections": ["Intro", "Métodos", "Resultados"],
                "rationale": "Ordem padrão.",
                "change_summary": "📐 Estrutura proposta",
            },
        ),
    ]
    fake_graph = MagicMock()
    fake_graph.get_state.return_value = _snapshot(graph_messages)

    with patch(
        "products.ensaio.app.graph.create_ensaio_graph",
        return_value=fake_graph,
    ):
        state._sync_with_checkpoint_if_completed()

    assert state.processing_agent == ""
    assert state.pending_structure_proposal == {
        "sections": ["Intro", "Métodos", "Resultados"],
        "rationale": "Ordem padrão.",
    }


def test_no_op_when_snapshot_empty():
    """Checkpoint vazio → função não toca o state."""
    state = _make_state()
    state.processing_agent = "orchestrator"

    fake_graph = MagicMock()
    fake_graph.get_state.return_value = SimpleNamespace(values={})

    with patch(
        "products.ensaio.app.graph.create_ensaio_graph",
        return_value=fake_graph,
    ):
        state._sync_with_checkpoint_if_completed()

    assert state.processing_agent == "orchestrator"
    assert state.messages == []
