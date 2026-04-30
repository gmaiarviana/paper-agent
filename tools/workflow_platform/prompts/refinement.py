"""Próximo passo de refinamento por estado pré-execução + builder do prompt.

Mapa fixo de transições baseado em
``docs/process/refinement/planning_guidelines.md``. Mudanças nos estados
ali declarados exigem atualização aqui.

Paths para ``planning_guidelines.md``, ``autonomous_readiness.md`` e
``starter.md`` são constantes — se mudarem, os prompts copiados pelo
operador apontam para arquivos errados.
"""

from dataclasses import dataclass

from tools.workflow_platform.models import Epic, EpicState


PLANNING_GUIDELINES_PATH = "docs/process/refinement/planning_guidelines.md"
AUTONOMOUS_READINESS_PATH = "docs/process/refinement/autonomous_readiness.md"
STARTER_PATH = "docs/process/refinement/starter.md"


@dataclass
class NextStepInfo:
    target_states: list[EpicState]
    guidance_text: str
    readiness_checklist: bool = False


_STATE_NAMES: dict[EpicState, str] = {
    EpicState.VISION: "🌱 Visão",
    EpicState.ALIGNED: "🧭 Jornada alinhada",
    EpicState.SKETCHED: "📐 Funcionalidades esboçadas",
    EpicState.CRITERIA: "📋 Critérios definidos",
    EpicState.DETAILED: "🔍 Detalhes definidos",
    EpicState.IN_PROGRESS: "🏗️ Em andamento",
    EpicState.IN_REVIEW: "🔀 Em revisão",
    EpicState.DONE: "✅ Implementado",
}


NEXT_STEP_MAP: dict[EpicState, NextStepInfo] = {
    EpicState.VISION: NextStepInfo(
        target_states=[EpicState.ALIGNED, EpicState.SKETCHED],
        guidance_text=(
            "Próximo alvo: `🧭 Jornada alinhada` ou `📐 Funcionalidades esboçadas`. "
            "Refinamento via PM skill (no fluxo autônomo) ou sessão estratégica."
        ),
    ),
    EpicState.ALIGNED: NextStepInfo(
        target_states=[EpicState.SKETCHED, EpicState.CRITERIA],
        guidance_text=(
            "Próximo alvo: `📐 Funcionalidades esboçadas` ou `📋 Critérios definidos`. "
            "Refinamento via PM skill ou sessão estratégica."
        ),
    ),
    EpicState.SKETCHED: NextStepInfo(
        target_states=[EpicState.CRITERIA],
        guidance_text=(
            "Próximo alvo: `📋 Critérios definidos`. "
            "Refinamento via PM skill ou sessão estratégica."
        ),
    ),
    EpicState.CRITERIA: NextStepInfo(
        target_states=[EpicState.DETAILED],
        guidance_text=(
            "Próximo alvo: `🔍 Detalhes definidos` (apto ao fluxo autônomo). "
            f"Checklist do alvo: `{AUTONOMOUS_READINESS_PATH}`."
        ),
        readiness_checklist=True,
    ),
}


def get_next_step(epic: Epic) -> NextStepInfo | None:
    """Retorna NextStepInfo para estados pré-execução; None caso contrário."""
    return NEXT_STEP_MAP.get(epic.state)


def build_refinement_prompt(epic: Epic) -> str | None:
    """Monta prompt de refinamento clipboard-ready.

    Para épicos em estados de execução (🔍/🏗️/🔀/✅), devolve None.
    Para estados pré-execução, devolve texto fixo apontando os documentos
    canônicos do refinamento.
    """
    info = get_next_step(epic)
    if info is None:
        return None

    target_text = " ou ".join(_STATE_NAMES[s] for s in info.target_states)
    primary_target = _STATE_NAMES[info.target_states[0]]

    lines = [
        f'Refinar o épico {epic.id} ("{epic.title}") até {primary_target}.',
        "",
        f"Estado atual: {_STATE_NAMES[epic.state]}",
        f"Alvo: {target_text}",
        f"ROADMAP de origem: {epic.roadmap_path}",
        "",
    ]

    if info.readiness_checklist:
        lines.append(f"Aplicar checklist em {AUTONOMOUS_READINESS_PATH}.")

    lines.append(f"Convenções da sessão em {PLANNING_GUIDELINES_PATH}.")
    lines.append(f"Pack inicial de contexto em {STARTER_PATH}.")

    return "\n".join(lines)
