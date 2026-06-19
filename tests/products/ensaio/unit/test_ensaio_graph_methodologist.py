"""Testes unitários para o grafo do Ensaio com Metodologista — E-PROTO-3.2."""

from unittest.mock import patch


def _make_graph():
    """Cria o grafo do Ensaio com checkpointer in-memory para teste.

    Patches ``SqliteSaver`` e ``sqlite3.connect`` para evitar criar arquivo
    em disco; usa ``InMemorySaver`` (um ``BaseCheckpointSaver`` real, exigido
    por langgraph >= 0.2 — substitui ``MagicMock`` que era rejeitado).

    ``InMemorySaver`` é importado lazy aqui (não no topo do arquivo) porque
    ``tests/core/unit/agents/test_methodologist_*.py`` envenenam
    ``sys.modules['langgraph.checkpoint.memory']`` durante a fase de
    coleção do pytest. O import lazy resolve só na chamada de
    ``_make_graph()``, depois do teardown das fixtures autouse desses
    arquivos restaurarem ``sys.modules`` via ``importlib.import_module``.
    """
    from langgraph.checkpoint.memory import InMemorySaver

    with patch("products.ensaio.app.graph.SqliteSaver"), patch("sqlite3.connect"):
        from products.ensaio.app.graph import create_ensaio_graph
        return create_ensaio_graph(checkpointer=InMemorySaver())


class TestEnsaioGraphMethodologist:
    def test_graph_has_methodologist_node(self):
        graph = _make_graph()
        node_names = list(graph.get_graph().nodes.keys())
        assert "methodologist" in node_names

    def test_graph_has_structurer_node(self):
        graph = _make_graph()
        node_names = list(graph.get_graph().nodes.keys())
        assert "structurer" in node_names

    def test_graph_has_orchestrator_node(self):
        graph = _make_graph()
        node_names = list(graph.get_graph().nodes.keys())
        assert "orchestrator" in node_names

    def test_create_ensaio_graph_returns_compiled_graph(self):
        graph = _make_graph()
        assert graph is not None
        assert hasattr(graph, "invoke")
