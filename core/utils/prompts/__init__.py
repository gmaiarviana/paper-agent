"""
Módulo de prompts dos agentes do Paper Agent.

Este módulo re-exporta todos os prompts dos agentes para manter compatibilidade
com imports existentes que usam `from utils.prompts import ...`.

Estrutura modular:
- utils/prompts/methodologist.py - Prompts do Metodologista
- utils/prompts/orchestrator.py - Prompts do Orquestrador
- utils/prompts/structurer.py - Prompts do Estruturador
"""

# Re-exportar prompts do Metodologista
from core.utils.prompts.methodologist import (
    METHODOLOGIST_AGENT_SYSTEM_PROMPT_V1,
    METHODOLOGIST_DECIDE_PROMPT_V2,
)

# Re-exportar prompts do Orquestrador
from core.utils.prompts.orchestrator import (
    ORCHESTRATOR_SOCRATIC_PROMPT_V1,
)

# Re-exportar prompts do Estruturador
from core.utils.prompts.structurer import (
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

