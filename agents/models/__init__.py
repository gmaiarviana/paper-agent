"""
Modelos Pydantic para entidades do domínio.

Este módulo contém schemas validados para as entidades principais do sistema:
- CognitiveModel: Modelo cognitivo em memória durante conversa
- Proposicao: Unidade base de conhecimento (substitui premise/assumption)
- Argument: Entidade persistida de argumento
- Idea: Entidade persistida de ideia

Épico 11: Modelagem Cognitiva
Épico 11.1: Schema Unificado (Camada Modelo)
Data: 2025-12-08
"""

from .cognitive_model import CognitiveModel, Contradiction, SolidGround
from .proposicao import Proposicao, ProposicaoRef

__all__ = [
    "CognitiveModel",
    "Contradiction",
    "SolidGround",
    "Proposicao",
    "ProposicaoRef",
]
