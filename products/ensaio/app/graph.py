"""
Grafo conversacional do Ensaio (E-POC-1.3).

Compõe o grafo próprio do Ensaio a partir dos nós do core, em postura
"ativo-leve":

- Orquestrador (core/agents/orchestrator): facilitador conversacional.
- Estruturador (core/agents/structurer): organiza o claim focal.
- Writer fica FORA do grafo - é invocado diretamente pelo app quando o
  usuário clica em "Gerar artigo".
- Metodologista NÃO entra no grafo nesta POC.

Decisão arquitetural (super-sistema):
O produto compõe seu próprio grafo a partir dos nós do core. O core
expõe nós isolados e roteadores reutilizáveis, sem conhecer o produto
consumidor.
"""

from __future__ import annotations

import logging
import sqlite3
from pathlib import Path
from typing import Literal, Optional, Union

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, StateGraph

from core.agents.orchestrator.nodes import orchestrator_node
from core.agents.orchestrator.router import route_from_orchestrator
from core.agents.orchestrator.state import MultiAgentState
from core.agents.structurer.nodes import structurer_node

logger = logging.getLogger(__name__)


def _ensaio_route_from_orchestrator(
    state: MultiAgentState,
) -> Union[Literal["structurer", "end"], str]:
    """
    Router do Ensaio: reutiliza a lógica do core e mapeia destinos não suportados para END.

    O Ensaio só tem orchestrator + structurer no grafo. Quando o Orquestrador sugerir
    agentes não presentes (methodologist/researcher/writer), o Ensaio trata como
    "conversar mais com o usuário" (END). Writer é invocado fora do grafo.
    """
    next_destination = route_from_orchestrator(state)
    if next_destination == "structurer":
        return "structurer"
    if next_destination == "user":
        return "end"
    # methodologist/researcher/writer ou qualquer outro: Ensaio não suporta no grafo.
    logger.info(
        "Ensaio graph: destino '%s' do core mapeado para 'end' (fora do escopo da POC).",
        next_destination,
    )
    return "end"


def _get_ensaio_checkpoint_db() -> Path:
    """Retorna o caminho absoluto do SQLite de checkpoints do Ensaio."""
    # products/ensaio/app/graph.py -> project root = parent.parent.parent.parent
    project_root = Path(__file__).resolve().parent.parent.parent.parent
    db_path = project_root / "data" / "ensaio_checkpoints.db"
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return db_path


_checkpointer_singleton: Optional[SqliteSaver] = None


def _get_checkpointer() -> SqliteSaver:
    """Retorna um SqliteSaver próprio para o Ensaio (singleton)."""
    global _checkpointer_singleton
    if _checkpointer_singleton is None:
        db_path = _get_ensaio_checkpoint_db()
        conn = sqlite3.connect(str(db_path), check_same_thread=False)
        _checkpointer_singleton = SqliteSaver(conn)
        logger.info("Ensaio: SqliteSaver criado em %s", db_path)
    return _checkpointer_singleton


def create_ensaio_graph():
    """
    Cria e compila o grafo conversacional do Ensaio.

    Estrutura:
        START → orchestrator
        orchestrator → [router] → structurer | END
        structurer → orchestrator  (para curadoria do resultado)

    Observações:
    - Writer NÃO entra no grafo (invocado diretamente pelo app).
    - Metodologista NÃO entra nesta POC.
    - Checkpoints em data/ensaio_checkpoints.db (descartáveis por design).

    Returns:
        CompiledGraph do LangGraph, pronto para `graph.invoke(state, config=...)`.
    """
    logger.info("Ensaio: criando grafo conversacional (orchestrator + structurer)...")

    graph = StateGraph(MultiAgentState)

    graph.add_node("orchestrator", orchestrator_node)
    graph.add_node("structurer", structurer_node)

    graph.set_entry_point("orchestrator")

    graph.add_conditional_edges(
        "orchestrator",
        _ensaio_route_from_orchestrator,
        {
            "structurer": "structurer",
            "end": END,
        },
    )

    # Após o Estruturador, voltamos ao Orquestrador para curadoria do resultado.
    graph.add_edge("structurer", "orchestrator")

    compiled = graph.compile(checkpointer=_get_checkpointer())
    logger.info("Ensaio: grafo compilado.")
    return compiled


__all__ = ["create_ensaio_graph"]
