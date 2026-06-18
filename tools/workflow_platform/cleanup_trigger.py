"""Resolve o milestone a limpar para uma PR mergeada, lendo o estado do ROADMAP.

Trigger da Action de cleanup (W-PROTO-17): em vez de depender do nome da branch
da PR (que no harness do Claude Code Web nunca casa com ``milestone/*``), casa os
épicos em ``🔀 Em revisão`` cujo ``PR #N`` é igual ao número da PR mergeada e
devolve o ``milestone_id`` único desses épicos. É o mesmo join por ``pr_number``
que a fila reativa usa em ``queue/detect.py::detect_review_items``.

Uso como CLI (invocado pela Action):

    python -m tools.workflow_platform.cleanup_trigger <pr_number>

Imprime o ``milestone_id`` resolvido em stdout (string vazia se a PR não é de
milestone) e sai 0; inconsistência no ROADMAP → stderr + exit 1.
"""

from __future__ import annotations

import sys

from .config_loader import load_config
from .models import EpicState
from .parser import parse_roadmap


def resolve_milestone_for_merged_pr(
    pr_number: int, roadmap_paths: list[str]
) -> str | None:
    """Milestone a limpar para a PR mergeada, ou ``None`` se não é PR de milestone.

    Parseia cada ROADMAP em ``roadmap_paths`` (``parser.parse_roadmap``, que tolera
    arquivo ausente), coleta os épicos em ``EpicState.IN_REVIEW`` com
    ``epic.pr_number == pr_number`` e devolve o ``milestone_id`` único desses
    épicos. Devolve ``None`` quando nenhum épico casa o número.

    Épicos já em ``✅`` com o mesmo ``PR #N`` **não** casam (só ``IN_REVIEW``):
    isso garante idempotência — um re-trigger sobre um milestone já fechado não
    o re-limpa.

    Raises:
        ValueError: se os épicos casados divergem no ``milestone_id`` (>1 valor
            distinto) ou têm ``milestone_id`` ausente — ROADMAP inconsistente,
            não silenciar.
    """
    matched_milestones: set[str | None] = set()
    found = False
    for path in roadmap_paths:
        parsed = parse_roadmap(path)
        for epic in parsed.epics:
            if epic.state == EpicState.IN_REVIEW and epic.pr_number == pr_number:
                found = True
                matched_milestones.add(epic.milestone_id)

    if not found:
        return None

    if None in matched_milestones or len(matched_milestones) != 1:
        raise ValueError(
            f"PR #{pr_number}: épicos em 🔀 com milestone_id inconsistente: "
            f"{sorted(str(m) for m in matched_milestones)}"
        )

    return next(iter(matched_milestones))


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if len(argv) != 1:
        print(
            "uso: python -m tools.workflow_platform.cleanup_trigger <pr_number>",
            file=sys.stderr,
        )
        return 2
    try:
        pr_number = int(argv[0])
    except ValueError:
        print(f"pr_number inválido: {argv[0]!r}", file=sys.stderr)
        return 2

    config = load_config()
    try:
        milestone_id = resolve_milestone_for_merged_pr(pr_number, config.roadmaps)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(milestone_id or "")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
