"""Construção de prompts de dispatch **por épico** (W-PILOTO-DISP-1).

Coerente com ``docs/process/autonomous/dispatch.md`` — o dispatch opera sobre o
épico-alvo em linguagem natural (``"implementa o épico <ID>"``). A única coisa
que bloqueia o prompt é um **predecessor bloqueante** declarado ainda não `✅`
(regra compartilhada em ``models.blocking_predecessors_of``). Um irmão do
milestone em 🏗️/🔀/✅ **não** bloqueia mais — entrega faseada é first-class.
"""

from dataclasses import dataclass, field

from tools.workflow_platform.models import Epic, blocking_predecessors_of


@dataclass
class DispatchPromptResult:
    prompt_text: str | None = None
    warnings: list[str] = field(default_factory=list)
    blocked: bool = False


def build_dispatch_prompt(
    epic: Epic,
    epics_by_id: dict[str, Epic],
    epics_by_milestone: dict[str, list[Epic]] | None = None,
) -> DispatchPromptResult:
    """Monta prompt de dispatch para ``epic``.

    - ``epic.milestone_id`` é ``None`` → bloqueia, sem prompt.
    - Predecessor bloqueante não-`✅` → bloqueia, sem prompt, com o motivo.
    - Caso contrário → prompt ``"implementa o épico <ID>"``.

    Não bloqueia mais só porque um irmão do milestone está em 🏗️/🔀/✅.
    """
    epics_by_milestone = epics_by_milestone or {}

    if epic.milestone_id is None:
        return DispatchPromptResult(
            prompt_text=None,
            warnings=["épico sem milestone declarado — não pode ser despachado"],
            blocked=True,
        )

    blocking = blocking_predecessors_of(epic, epics_by_id, epics_by_milestone)
    if blocking:
        return DispatchPromptResult(
            prompt_text=None,
            warnings=[f"bloqueado por {', '.join(blocking)} — precisa estar ✅"],
            blocked=True,
        )

    return DispatchPromptResult(
        prompt_text=f"implementa o épico {epic.id}",
        warnings=[],
        blocked=False,
    )
