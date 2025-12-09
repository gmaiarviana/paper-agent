"""
Modelos Pydantic para entidades do domínio.

Este módulo contém schemas validados para as entidades principais do sistema:
- CognitiveModel: Modelo cognitivo em memória durante conversa
- Proposicao: Unidade base de conhecimento (substitui premise/assumption)
- Argument: Entidade persistida de argumento
- Idea: Entidade persistida de ideia
- Clarification: Modelos para consultas inteligentes do Observer

Épico 11: Modelagem Cognitiva
Épico 11.1: Schema Unificado (Camada Modelo)
Épico 14: Observer - Consultas Inteligentes
Data: 2025-12-09
"""

from .cognitive_model import CognitiveModel, Contradiction, SolidGround
from .proposition import Proposicao, ProposicaoRef
from .clarification import (
    ClarificationNeed,
    ClarificationContext,
    ClarificationTimingDecision,
    ClarificationResponse,
    ClarificationUpdates,
    QuestionSuggestion,
)

__all__ = [
    "CognitiveModel",
    "Contradiction",
    "SolidGround",
    "Proposicao",
    "ProposicaoRef",
    # Épico 14: Clarification
    "ClarificationNeed",
    "ClarificationContext",
    "ClarificationTimingDecision",
    "ClarificationResponse",
    "ClarificationUpdates",
    "QuestionSuggestion",
]
