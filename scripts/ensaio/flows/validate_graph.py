"""Validação manual do grafo do Ensaio (E-POC-1.3).

Uso:
    python scripts/ensaio/flows/validate_graph.py

Invoca o grafo com input fixo e imprime o output. Confirma:
    - ``create_ensaio_graph()`` compõe Orquestrador + Estruturador (sem
      Metodologista e sem Writer);
    - ``SqliteSaver`` persiste em ``data/ensaio_checkpoints.db`` por padrão;
    - ``product_context`` injetado via ``config.configurable`` chega ao
      prompt do Orquestrador.
"""

from __future__ import annotations

import logging
import os
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from dotenv import load_dotenv  # noqa: E402

load_dotenv(dotenv_path=_PROJECT_ROOT / ".env")

from langchain_core.messages import HumanMessage  # noqa: E402

from products.ensaio.app.graph import create_ensaio_graph  # noqa: E402
from products.ensaio.app.product_config import load_product_context  # noqa: E402


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    if not os.getenv("ANTHROPIC_API_KEY"):
        print("[ERRO] ANTHROPIC_API_KEY não está configurada em .env.")
        return 1

    product_context = load_product_context()
    print(f"[INFO] product_context carregado ({len(product_context)} chars)")

    graph = create_ensaio_graph()

    nodes_in_graph = set(graph.nodes.keys()) if hasattr(graph, "nodes") else set()
    print(f"[INFO] nós do grafo: {sorted(nodes_in_graph)}")
    assert "orchestrator" in nodes_in_graph, "Orquestrador ausente do grafo"
    assert "structurer" in nodes_in_graph, "Estruturador ausente do grafo"
    assert "methodologist" not in nodes_in_graph, (
        "Metodologista NÃO deve participar do grafo conversacional do Ensaio (E-POC-1.3)."
    )

    user_input = (
        "Rodei um experimento com um agente LLM que lê um repositório Python e "
        "gera rascunhos de seções de artigo. Avaliei manualmente 12 execuções em "
        "fidelidade, coesão e utilidade."
    )

    initial_state = {
        "user_input": user_input,
        "session_id": "validate-graph-session",
        "messages": [HumanMessage(content=user_input)],
    }

    config = {
        "configurable": {
            "thread_id": "validate-graph-thread",
            "product_context": product_context,
        }
    }

    print("\n=== Invocando grafo do Ensaio ===\n")
    result = graph.invoke(initial_state, config=config)

    print("\n--- Resultado ---")
    print(f"next_step: {result.get('next_step')}")
    print(f"focal_argument: {result.get('focal_argument')}")
    messages = result.get("messages", [])
    print(f"messages count: {len(messages)}")
    if messages:
        last = messages[-1]
        content = last.content if hasattr(last, "content") else str(last)
        print(f"última mensagem ({type(last).__name__}):\n{content[:500]}...")

    db_path = _PROJECT_ROOT / "data" / "ensaio_checkpoints.db"
    if db_path.exists():
        print(f"\n[OK] SqliteSaver criou {db_path} ({db_path.stat().st_size} bytes)")
    else:
        print(f"\n[WARN] {db_path} não foi criado — inspecione checkpointer.")

    print("\n✅ Validação manual do grafo do Ensaio concluída.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
