"""Grafo LangGraph do produto Ensaio (E-POC-1.3).

Compõe um grafo conversacional próprio a partir dos nós do core
(``orchestrator_node`` e ``structurer_node``) — sem Metodologista e sem
Writer. O Writer é invocado diretamente pelo app quando o pesquisador clica
em "Gerar artigo" (ver ``generate_button.py``).

Princípio do super-sistema (ver ``core/docs/vision/super_system.md``): o
produto compõe seu próprio grafo; o core expõe nós individuais. O Ensaio
não reusa ``create_multi_agent_graph`` do core — reusa apenas os nós.

Comportamento do roteamento:
    - ``route_from_orchestrator`` retorna "structurer", "methodologist",
      "user" ou algo inválido.
    - Neste grafo, "methodologist" é mapeado para END (Ensaio não tem
      Metodologista na POC — ver E-POC-3, critério "Não deve invocar o
      Metodologista neste épico"). Quando o Orquestrador sugerir
      Metodologista, a sugestão é absorvida silenciosamente e o controle
      retorna ao usuário.
    - "structurer" → vai para o Estruturador e dali direto para END (sem
      Metodologista encadeado no fluxo do Ensaio).
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, StateGraph

from core.agents.orchestrator.nodes import orchestrator_node
from core.agents.orchestrator.router import route_from_orchestrator
from core.agents.orchestrator.state import MultiAgentState
from core.agents.structurer.nodes import structurer_node


def _project_root() -> Path:
    # products/ensaio/app/graph.py → subir 3 níveis → raiz do projeto
    return Path(__file__).resolve().parent.parent.parent.parent


def _default_db_path() -> Path:
    return _project_root() / "data" / "ensaio_checkpoints.db"


def _route(state: MultiAgentState) -> str:
    destination = route_from_orchestrator(state)
    # Ensaio POC não invoca Metodologista — absorver sugestão e voltar ao usuário.
    if destination == "methodologist":
        return "user"
    return destination


def create_ensaio_graph(
    checkpointer: Any | None = None,
    db_path: Path | None = None,
):
    """Compila o grafo conversacional do Ensaio.

    Args:
        checkpointer: checkpointer customizado (útil em testes e no script
            de validação). Quando ``None``, cria um ``SqliteSaver`` em
            ``data/ensaio_checkpoints.db``.
        db_path: caminho alternativo para o SqliteSaver (ignorado quando
            ``checkpointer`` é passado).

    Returns:
        ``CompiledStateGraph`` pronto para ``invoke()``.
    """
    graph = StateGraph(MultiAgentState)
    graph.add_node("orchestrator", orchestrator_node)
    graph.add_node("structurer", structurer_node)

    graph.set_entry_point("orchestrator")

    graph.add_conditional_edges(
        "orchestrator",
        _route,
        {
            "structurer": "structurer",
            "user": END,
        },
    )

    # Sem Metodologista: o Estruturador encerra o turno e volta ao usuário.
    graph.add_edge("structurer", END)

    if checkpointer is None:
        path = db_path or _default_db_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(path), check_same_thread=False)
        checkpointer = SqliteSaver(conn)

    return graph.compile(checkpointer=checkpointer)
