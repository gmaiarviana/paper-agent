"""Grafo LangGraph do produto Ensaio (PROTO-ENSAIO).

Compõe um grafo conversacional próprio a partir dos nós do core:
Orquestrador → Estruturador | Metodologista → END.

O Writer é invocado diretamente pelo estado Reflex (``state.py``) — não
entra no grafo conversacional (ver ``core/docs/agents/writer/design.md``).

Princípio do super-sistema (ver ``core/docs/vision/super_system.md``): o
produto compõe seu próprio grafo; o core expõe nós individuais.

Roteamento:
    - ``route_from_orchestrator`` retorna "structurer", "methodologist" ou "user".
    - "structurer" → Estruturador → END
    - "methodologist" → Metodologista (provocação) → END  (E-PROTO-3.2)
    - "user" → END (Orquestrador responde diretamente)
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, StateGraph

from core.agents.methodologist.nodes import methodologist_provocation_node
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
    return route_from_orchestrator(state)


def create_ensaio_graph(
    checkpointer: Any | None = None,
    db_path: Path | None = None,
):
    """Compila o grafo conversacional do Ensaio (PROTO-ENSAIO).

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
    graph.add_node("methodologist", methodologist_provocation_node)

    graph.set_entry_point("orchestrator")

    graph.add_conditional_edges(
        "orchestrator",
        _route,
        {
            "structurer": "structurer",
            "methodologist": "methodologist",
            "user": END,
        },
    )

    graph.add_edge("structurer", END)
    graph.add_edge("methodologist", END)

    if checkpointer is None:
        path = db_path or _default_db_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(path), check_same_thread=False)
        checkpointer = SqliteSaver(conn)

    return graph.compile(checkpointer=checkpointer)
