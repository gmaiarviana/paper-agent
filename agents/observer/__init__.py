"""
Agente Observador - Mente Analítica.

Este módulo implementa o Observador, agente especializado em monitorar
e catalogar a evolução do raciocínio durante conversas.

O Observador trabalha silenciosamente em paralelo ao Orquestrador:
- Atualiza CognitiveModel a cada turno
- Extrai conceitos para biblioteca global
- Calcula métricas (solidez, completude)
- Responde consultas do Orquestrador

Épico 10: Observador - Mente Analítica (POC)
Funcionalidade 10.1: Mitose do Orquestrador

Data: 05/12/2025
"""

from .api import ObservadorAPI, ObserverInsight
from .state import ObserverState
from .nodes import process_turn
from .metrics import calculate_solidez, calculate_completude

__all__ = [
    "ObservadorAPI",
    "ObserverInsight",
    "ObserverState",
    "process_turn",
    "calculate_solidez",
    "calculate_completude",
]
