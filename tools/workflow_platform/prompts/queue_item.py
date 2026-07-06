"""Builders de prompt clipboard-ready por tipo de QueueItem (W-PROTO-FILA-2.2).

Despacha por ``item.type``:
    - DISPATCH    reusa ``build_dispatch_prompt`` (PLAT-3.1)
    - REFINE      reusa ``build_refinement_prompt`` (PLAT-4.2)
    - REVIEW      texto fixo parametrizado por PRPointer
    - CLEANUP     texto fixo parametrizado por CleanupPointer
    - STALE_BRANCH texto fixo parametrizado por BranchPointer

Sem placeholders pendentes na saída — item válido sempre tem prompt.
"""

from __future__ import annotations

from tools.workflow_platform.models import Epic
from tools.workflow_platform.prompts.dispatch import build_dispatch_prompt
from tools.workflow_platform.prompts.refinement import build_refinement_prompt
from tools.workflow_platform.job_queue.models import (
    BranchPointer,
    CleanupPointer,
    EpicPointer,
    ItemType,
    PRPointer,
    QueueItem,
    RefinePointer,
)


def _build_dispatch(
    pointer: EpicPointer,
    all_epics_by_milestone: dict[str, list[Epic]] | None,
) -> str:
    if not all_epics_by_milestone:
        return f"implementa o {pointer.milestone_id}"
    epics_in_ms = all_epics_by_milestone.get(pointer.milestone_id, [])
    if not epics_in_ms:
        return f"implementa o {pointer.milestone_id}"
    # build_dispatch_prompt precisa de um "épico anchor" — pegamos o primeiro
    anchor = epics_in_ms[0]
    result = build_dispatch_prompt(anchor, epics_in_ms)
    if result.prompt_text is None:
        # bloqueado — devolver mínimo informativo (item já existia, então
        # estado não deveria ser bloqueante; defensivo)
        return f"implementa o {pointer.milestone_id}"
    return result.prompt_text


def _build_refine(pointer: RefinePointer, epic_lookup: dict[str, Epic] | None) -> str:
    if not epic_lookup or pointer.epic_id not in epic_lookup:
        return (
            f"Refinar o épico {pointer.epic_id} até {pointer.target_state.value}.\n"
            f"ROADMAP: {pointer.roadmap_path}"
        )
    epic = epic_lookup[pointer.epic_id]
    prompt = build_refinement_prompt(epic)
    if prompt is None:
        return (
            f"Refinar o épico {pointer.epic_id} até {pointer.target_state.value}.\n"
            f"ROADMAP: {pointer.roadmap_path}"
        )
    return prompt


def _build_review_prompt(p: PRPointer) -> str:
    pr_url = p.pr_url or "(sem URL — verifique o ROADMAP)"
    return (
        f"Revisar PR #{p.pr_number}: {pr_url}\n"
        "\n"
        "Abra a PR, copie a Seção 🎯 Validação do body, cole no GitHub Copilot, "
        "e decida merge."
    )


def _build_cleanup_prompt(p: CleanupPointer) -> str:
    return (
        f"Rodar Cleanup skill manualmente para o épico {p.epic_id} "
        f"('{p.title}') em {p.roadmap_path}.\n"
        "\n"
        "Carregue skills/cleanup/skill.md e siga o protocolo. Cleanup move "
        "conteúdo histórico do épico pra fora do ROADMAP; coluna ✅ do kanban "
        "volta a ficar vazia."
    )


def _build_stale_branch_prompt(p: BranchPointer) -> str:
    return (
        f"Branch {p.branch_name} parada há {p.days_stale} dias sem PR aberta.\n"
        "\n"
        "Decida:\n"
        "(a) trabalho concluído sem PR — abrir PR via interface do GitHub\n"
        f"(b) abandonado — `git push origin --delete {p.branch_name}`\n"
        "(c) bloqueado — resgatar contexto e seguir"
    )


def build_prompt_for_item(
    item: QueueItem,
    all_epics_by_milestone: dict[str, list[Epic]] | None = None,
    epic_lookup: dict[str, Epic] | None = None,
) -> str:
    """Despacha por ``item.type`` e devolve prompt clipboard-ready.

    DISPATCH precisa de ``all_epics_by_milestone`` para reusar
    ``build_dispatch_prompt`` (assina pelo épico-âncora). REFINE precisa
    de ``epic_lookup`` para reusar ``build_refinement_prompt``.
    REVIEW/CLEANUP/STALE_BRANCH constroem do próprio pointer.
    """
    pointer = item.source_pointer
    if item.type == ItemType.DISPATCH:
        assert isinstance(pointer, EpicPointer)
        return _build_dispatch(pointer, all_epics_by_milestone)
    if item.type == ItemType.REVIEW:
        assert isinstance(pointer, PRPointer)
        return _build_review_prompt(pointer)
    if item.type == ItemType.REFINE:
        assert isinstance(pointer, RefinePointer)
        return _build_refine(pointer, epic_lookup)
    if item.type == ItemType.CLEANUP:
        assert isinstance(pointer, CleanupPointer)
        return _build_cleanup_prompt(pointer)
    if item.type == ItemType.STALE_BRANCH:
        assert isinstance(pointer, BranchPointer)
        return _build_stale_branch_prompt(pointer)
    raise ValueError(f"tipo de item desconhecido: {item.type}")
