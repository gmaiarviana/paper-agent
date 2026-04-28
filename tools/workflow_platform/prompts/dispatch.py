"""Construção de prompts de dispatch para milestone.

Coerente com ``docs/process/autonomous/dispatch.md`` — o dispatch opera
sempre sobre milestone inteiro em linguagem natural ("implementa o <ID>").
Quando algum épico está em estado pré-execução pré-`🔍`, o prompt cita
explicitamente quais a PM skill refinará. Quando há épico em execução
ou concluído (🏗️/🔀/✅), o prompt é bloqueado.
"""

from dataclasses import dataclass, field

from tools.workflow_platform.models import Epic, EpicState


PRE_REFINEMENT_STATES: set[EpicState] = {
    EpicState.VISION,
    EpicState.ALIGNED,
    EpicState.SKETCHED,
    EpicState.CRITERIA,
}

EXECUTION_STATES: set[EpicState] = {
    EpicState.IN_PROGRESS,
    EpicState.IN_REVIEW,
    EpicState.DONE,
}


@dataclass
class DispatchPromptResult:
    prompt_text: str | None = None
    warnings: list[str] = field(default_factory=list)
    blocked: bool = False


def build_dispatch_prompt(
    epic: Epic,
    all_epics_in_milestone: list[Epic],
) -> DispatchPromptResult:
    """Monta prompt de dispatch para o milestone-pai do épico.

    - Se ``epic.milestone_id`` é ``None``: bloqueia, sem prompt.
    - Se algum épico do milestone está em 🏗️/🔀/✅: bloqueia, sem prompt.
    - Se algum está em 🌱/🧭/📐/📋: prompt + nota "PM skill refinará".
    - Caso contrário: prompt simples ``"implementa o <MILESTONE_ID>"``.
    """
    if epic.milestone_id is None:
        return DispatchPromptResult(
            prompt_text=None,
            warnings=["épico sem milestone declarado — não pode ser despachado"],
            blocked=True,
        )

    milestone_id = epic.milestone_id
    others = [e for e in all_epics_in_milestone if e.id != epic.id] + [epic]
    # Garante que o próprio épico entra na avaliação dos estados do milestone.
    seen: set[str] = set()
    deduped: list[Epic] = []
    for e in others:
        if e.id in seen:
            continue
        seen.add(e.id)
        deduped.append(e)

    in_execution = [e for e in deduped if e.state in EXECUTION_STATES]
    if in_execution:
        states_seen = sorted({e.state.value for e in in_execution})
        ids_seen = sorted({e.id for e in in_execution})
        return DispatchPromptResult(
            prompt_text=None,
            warnings=[
                f"milestone em execução/concluído — dispatch não recomendado "
                f"(épicos {', '.join(ids_seen)} em {' / '.join(states_seen)})"
            ],
            blocked=True,
        )

    pre_refinement = sorted(
        (e for e in deduped if e.state in PRE_REFINEMENT_STATES),
        key=lambda e: e.id,
    )

    lines = [f"implementa o {milestone_id}"]
    warnings: list[str] = []

    if pre_refinement:
        ids = [e.id for e in pre_refinement]
        lines.append("")
        lines.append("Nota: PM skill refinará os épicos abaixo (→ 🔍) antes da EM rodar:")
        for epic_id in ids:
            lines.append(f"- {epic_id}")
        warnings.append(
            "milestone tem épicos em estado pré-🔍: " + ", ".join(ids)
        )

    return DispatchPromptResult(
        prompt_text="\n".join(lines),
        warnings=warnings,
        blocked=False,
    )
