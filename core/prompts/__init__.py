"""
Módulo de prompts dos agentes do Paper Agent.

Este módulo re-exporta todos os prompts dos agentes para manter compatibilidade
com imports existentes que usam `from core.prompts import ...`.

Estrutura modular:
- core/prompts/methodologist.py - Prompts do Metodologista
- core/prompts/orchestrator.py - Prompts do Orquestrador
- core/prompts/structurer.py - Prompts do Estruturador
"""

# Re-exportar prompts do Metodologista
from core.prompts.methodologist import (
    METHODOLOGIST_AGENT_SYSTEM_PROMPT_V1,
    METHODOLOGIST_DECIDE_PROMPT_V2,
)

# Re-exportar prompts do Orquestrador
from core.prompts.orchestrator import (
    ORCHESTRATOR_SOCRATIC_PROMPT_V1,
)

# Re-exportar prompts do Estruturador
from core.prompts.structurer import (
    STRUCTURER_REFINEMENT_PROMPT_V1,
)

__all__ = [
    # Metodologista
    "METHODOLOGIST_AGENT_SYSTEM_PROMPT_V1",
    "METHODOLOGIST_DECIDE_PROMPT_V2",
    # Orquestrador
    "ORCHESTRATOR_SOCRATIC_PROMPT_V1",
    # Estruturador
    "STRUCTURER_REFINEMENT_PROMPT_V1",
]

