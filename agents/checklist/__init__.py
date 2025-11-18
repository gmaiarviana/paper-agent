"""
Módulo de checklist de progresso.

Este módulo contém backend de checklist que detecta status de progresso
baseado no modelo cognitivo, adaptando checklist conforme tipo de artigo.

Épico 11.6: Checklist de Progresso (Backend)
Data: 2025-11-17
"""

from .progress_tracker import (
    ChecklistItem,
    ChecklistStatus,
    ProgressTracker,
    get_checklist_for_article_type,
    evaluate_progress
)

__all__ = [
    "ChecklistItem",
    "ChecklistStatus",
    "ProgressTracker",
    "get_checklist_for_article_type",
    "evaluate_progress",
]
