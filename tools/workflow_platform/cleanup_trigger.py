"""Detecção determinística das faxinas pendentes, lendo o estado do ROADMAP.

Resolve o milestone a limpar casando os épicos em ``🔀 Em revisão`` cujo ``PR #N``
é igual ao número de uma PR mergeada (W-PROTO-17), e devolve o ``milestone_id``
único desses épicos. É o mesmo join por ``pr_number`` que a fila reativa usa em
``queue/detect.py::detect_review_items``.

Originalmente o trigger da GitHub Action de cleanup; a Action foi aposentada e a
faxina migrou para o **fold-in do dispatch** (``docs/process/autonomous/dispatch.md``
§4.5). Este módulo sobreviveu como a detecção reusada por esse fluxo.

Uso como CLI:

    python -m tools.workflow_platform.cleanup_trigger <pr_number>   # resolve 1 PR
    python -m tools.workflow_platform.cleanup_trigger --list        # lista todas

``<pr_number>`` imprime o ``milestone_id`` resolvido (vazio se a PR não é de
milestone). ``--list`` imprime uma linha ``<MILESTONE_ID>\\t<PR>\\t<URL>`` por
faxina pendente — consumido pela regra de fold-in ao iniciar um milestone novo.
Inconsistência no ROADMAP → stderr + exit 1.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass

from .config_loader import load_config
from .models import EpicState
from .parser import parse_roadmap


@dataclass(frozen=True)
class PendingCleanup:
    """Uma faxina pendente: um milestone mergeado cujo enxugamento ainda não rodou.

    ``pr_url`` pode vir vazio se o épico em 🔀 não declarou a URL (só o número).
    """

    milestone_id: str
    pr_number: int
    pr_url: str


def list_pending_cleanups(roadmap_paths: list[str]) -> list[PendingCleanup]:
    """Lista **todas** as faxinas pendentes lendo o estado dos ROADMAPs.

    Usada no fold-in: ao iniciar um milestone novo (branch recém-criada de uma
    ``main`` atualizada), o implementador chama esta função para descobrir quais
    milestones anteriores ainda precisam de faxina e roda ``skills/cleanup/skill.md``
    para cada um **nesta branch**, entrando na PR revisada.

    Invariante load-bearing: um épico em ``🔀 Em revisão`` presente em ``main``
    implica que a PR dele **já foi mergeada**. A RTE seta ``🔀`` dentro da branch
    do milestone (no commit do ``current_validation.md``, antes do push), então o
    ``🔀`` só aparece em ``main`` depois que aquela PR mergeia. Logo varrer ``🔀``
    em ``main`` enumera exatamente as faxinas pendentes — e nunca o milestone
    atual, cujos épicos estão em ``🔍``/pré-``📋`` no início do dispatch (o parser
    de dispatch aborta se algum está ``🏗️``/``✅``).

    Idempotência: épico já enxuto está em ``✅`` (não ``🔀``), então não reaparece
    aqui. Reusa ``resolve_milestone_for_merged_pr`` por ``pr_number`` distinto —
    não reimplementa o parsing nem a convenção "1 PR = 1 milestone".

    Limitação conhecida: dispatch concorrente de dois milestones em paralelo veria
    a mesma faxina pendente nas duas branches → dupla transição / conflito de
    merge. O time despacha em série; registrado como limitação, não tratado aqui.

    Raises:
        ValueError: propaga de ``resolve_milestone_for_merged_pr`` se algum
            ``pr_number`` casar épicos com ``milestone_id`` inconsistente.
    """
    pr_urls: dict[int, str] = {}
    for path in roadmap_paths:
        parsed = parse_roadmap(path)
        for epic in parsed.epics:
            if epic.state == EpicState.IN_REVIEW and epic.pr_number is not None:
                # Primeiro pr_url não-vazio vence; mantém entrada mesmo se vazio.
                if epic.pr_number not in pr_urls or (
                    not pr_urls[epic.pr_number] and epic.pr_url
                ):
                    pr_urls[epic.pr_number] = epic.pr_url or ""

    pending: list[PendingCleanup] = []
    for pr_number in sorted(pr_urls):
        milestone_id = resolve_milestone_for_merged_pr(pr_number, roadmap_paths)
        if milestone_id is None:
            continue
        pending.append(
            PendingCleanup(
                milestone_id=milestone_id,
                pr_number=pr_number,
                pr_url=pr_urls[pr_number],
            )
        )
    return pending


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

    Convenção load-bearing: **1 PR = 1 milestone**. Se uma PR fechar épicos de
    milestones distintos (ou um épico casado não declarar ``**Milestone:**``),
    a função levanta ``ValueError`` **por design**, em vez de adivinhar qual
    milestone limpar. Falha visível é preferível a limpar um ROADMAP
    inconsistente do jeito errado; o implementador investiga o ROADMAP antes de
    rodar a faxina no fold-in (ver ``docs/process/autonomous/dispatch.md`` §4.5).

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


_USAGE = (
    "uso: python -m tools.workflow_platform.cleanup_trigger <pr_number>\n"
    "     python -m tools.workflow_platform.cleanup_trigger --list"
)


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if len(argv) != 1:
        print(_USAGE, file=sys.stderr)
        return 2

    config = load_config()

    # Modo fold-in: lista todas as faxinas pendentes (uma linha por milestone),
    # consumido pela regra de dispatch ao iniciar um milestone novo.
    if argv[0] == "--list":
        try:
            pending = list_pending_cleanups(config.roadmaps)
        except ValueError as exc:
            print(str(exc), file=sys.stderr)
            return 1
        for item in pending:
            print(f"{item.milestone_id}\t{item.pr_number}\t{item.pr_url}")
        return 0

    try:
        pr_number = int(argv[0])
    except ValueError:
        print(f"pr_number inválido: {argv[0]!r}", file=sys.stderr)
        return 2

    try:
        milestone_id = resolve_milestone_for_merged_pr(pr_number, config.roadmaps)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(milestone_id or "")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
