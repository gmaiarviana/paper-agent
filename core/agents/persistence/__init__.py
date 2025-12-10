"""
Módulo de persistência e gerenciamento de snapshots.

Este módulo contém helpers para:
- Detecção de maturidade de argumentos via LLM
- Criação automática de snapshots (argumentos versionados)
- Integração entre MultiAgentState e DatabaseManager

Épico 11.5: Indicadores de Maturidade

"""

from .snapshot_manager import (
    SnapshotManager,
    MaturityAssessment,
    detect_argument_maturity,
    create_snapshot_if_mature
)

__all__ = [
    "SnapshotManager",
    "MaturityAssessment",
    "detect_argument_maturity",
    "create_snapshot_if_mature",
]
