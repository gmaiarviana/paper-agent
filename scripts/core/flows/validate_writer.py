"""Validação manual do Writer (C-ENSAIO-2).

Uso:
    python scripts/core/flows/validate_writer.py
    python scripts/core/flows/validate_writer.py --refinement

Invoca ``writer_node`` isoladamente e imprime o markdown retornado. O modo
``--refinement`` chama o Writer duas vezes: primeira com ``previous_article=None``
e segunda com o artigo anterior + feedback "deixa mais conciso" no histórico.
"""

from __future__ import annotations

import argparse
import logging
import os
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from dotenv import load_dotenv  # noqa: E402

load_dotenv(dotenv_path=_PROJECT_ROOT / ".env")

from langchain_core.messages import AIMessage, HumanMessage  # noqa: E402

from core.agents.writer.nodes import writer_node  # noqa: E402


def _run_initial() -> str:
    print("\n=== PASSADA 1: Geração inicial (previous_article=None) ===\n")
    result = writer_node(
        {
            "messages": [
                HumanMessage(
                    content=(
                        "Rodei um experimento com um agente LLM que lê um repositório "
                        "Python e gera rascunhos de seções de artigo. O agente usa "
                        "claude-3-5-haiku-20241022, prompt único de ~800 tokens, e "
                        "consumiu em média 3200 tokens por geração em 12 execuções."
                    )
                ),
                AIMessage(
                    content=(
                        "Entendi. Você quer avaliar a viabilidade de gerar artigos a "
                        "partir de repositórios via LLM. Quais métricas usou pra "
                        "avaliar a qualidade do rascunho?"
                    )
                ),
                HumanMessage(
                    content=(
                        "Pontuei manualmente cada rascunho numa escala 1-5 em três "
                        "dimensões: fidelidade ao código, coesão textual e utilidade "
                        "como ponto de partida. Média 3.2, 3.8 e 4.1 respectivamente."
                    )
                ),
            ],
            "focal_argument": {
                "intent": "test_hypothesis",
                "subject": "LLM para gerar rascunhos de artigo a partir de repositórios",
                "population": "repositórios Python pequenos e médios",
                "metrics": "scores 1-5 em fidelidade, coesão e utilidade",
                "article_type": "empirical",
            },
            "previous_article": None,
            "product_context": (
                "Laboratório de escrita para pesquisadores de ICT que produzem "
                "experimentos em código e querem transformar o experimento em artigo "
                "técnico-científico no formato IMRaD."
            ),
        }
    )
    article = result.get("article", "")
    print(article)
    print("\n--- fim da passada 1 ---\n")
    _assert_imrad(article)
    return article


def _run_refinement(previous: str) -> None:
    print("\n=== PASSADA 2: Refinamento (previous_article preenchido) ===\n")
    result = writer_node(
        {
            "messages": [
                HumanMessage(content="O rascunho ficou bom, mas deixa mais conciso — "
                                      "corte pelo menos 30% do tamanho."),
            ],
            "focal_argument": None,
            "previous_article": previous,
            "product_context": None,
        }
    )
    refined = result.get("article", "")
    print(refined)
    print("\n--- fim da passada 2 ---\n")
    if len(refined) >= len(previous):
        print(
            f"[WARN] artigo refinado ({len(refined)} chars) não ficou menor que o "
            f"original ({len(previous)} chars). Inspecione manualmente."
        )
    else:
        print(
            f"[OK] artigo refinado ({len(refined)} chars) é menor que o original "
            f"({len(previous)} chars)."
        )


def _assert_imrad(article: str) -> None:
    lowered = article.lower()
    expected = ["introdu", "métod", "resultado", "discus", "conclus"]
    missing = [term for term in expected if term not in lowered]
    if missing:
        print(
            f"[WARN] artigo não contém marcadores IMRaD esperados: {missing}. "
            "Revise manualmente."
        )
    else:
        print("[OK] artigo contém marcadores IMRaD esperados.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--refinement",
        action="store_true",
        help="Depois da geração inicial, invocar novamente com previous_article.",
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    if not os.getenv("ANTHROPIC_API_KEY"):
        print("[ERRO] ANTHROPIC_API_KEY não está configurada em .env.")
        return 1

    previous = _run_initial()
    if args.refinement:
        _run_refinement(previous)

    print("\n✅ Validação manual do Writer concluída.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
