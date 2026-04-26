"""Testes unitários para o grafo do Ensaio com Metodologista — E-PROTO-3.2."""

from unittest.mock import MagicMock, patch
from pathlib import Path


class TestEnsaioGraphMethodologist:
    def test_graph_has_methodologist_node(self):
        with patch("products.ensaio.app.graph.SqliteSaver"), \
             patch("sqlite3.connect"):
            from products.ensaio.app.graph import create_ensaio_graph
            graph = create_ensaio_graph(checkpointer=MagicMock())

        node_names = list(graph.get_graph().nodes.keys())
        assert "methodologist" in node_names

    def test_graph_has_structurer_node(self):
        with patch("products.ensaio.app.graph.SqliteSaver"), \
             patch("sqlite3.connect"):
            from products.ensaio.app.graph import create_ensaio_graph
            graph = create_ensaio_graph(checkpointer=MagicMock())

        node_names = list(graph.get_graph().nodes.keys())
        assert "structurer" in node_names

    def test_graph_has_orchestrator_node(self):
        with patch("products.ensaio.app.graph.SqliteSaver"), \
             patch("sqlite3.connect"):
            from products.ensaio.app.graph import create_ensaio_graph
            graph = create_ensaio_graph(checkpointer=MagicMock())

        node_names = list(graph.get_graph().nodes.keys())
        assert "orchestrator" in node_names

    def test_create_ensaio_graph_returns_compiled_graph(self):
        with patch("products.ensaio.app.graph.SqliteSaver"), \
             patch("sqlite3.connect"):
            from products.ensaio.app.graph import create_ensaio_graph
            graph = create_ensaio_graph(checkpointer=MagicMock())

        assert graph is not None
        assert hasattr(graph, "invoke")
