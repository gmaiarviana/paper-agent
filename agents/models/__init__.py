"""
Modelos Pydantic para entidades do domínio.

Este módulo contém schemas validados para as entidades principais do sistema:
- CognitiveModel: Modelo cognitivo em memória durante conversa
- Argument: Entidade persistida de argumento
- Idea: Entidade persistida de ideia

Épico 11: Modelagem Cognitiva
Data: 2025-11-17
"""

from .cognitive_model import CognitiveModel, Contradiction, SolidGround

__all__ = [
    "CognitiveModel",
    "Contradiction",
    "SolidGround",
]
