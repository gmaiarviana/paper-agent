"""
Rastreamento de progresso e checklist adaptativo.

Este módulo detecta status de progresso baseado no modelo cognitivo,
adaptando checklist conforme tipo de artigo (empírico, revisão, teórico).

Épico 11.6: Checklist de Progresso (Backend)
Data: 2025-11-17
"""

import logging
from typing import List, Literal, Optional, Dict, Any
from pydantic import BaseModel, Field

from agents.models.cognitive_model import CognitiveModel

logger = logging.getLogger(__name__)


# Tipos de status de item do checklist
ChecklistStatus = Literal["pending", "in_progress", "completed"]


class ChecklistItem(BaseModel):
    """
    Item individual do checklist de progresso.

    Campos:
    - id: Identificador único do item (ex: "scope", "population", "metrics")
    - label: Label legível (ex: "Escopo definido", "População identificada")
    - status: Status atual ("pending" | "in_progress" | "completed")
    - description: Descrição do que o item verifica (opcional)
    """

    id: str = Field(..., description="Identificador único do item")
    label: str = Field(..., description="Label legível para exibição")
    status: ChecklistStatus = Field(default="pending", description="Status atual do item")
    description: Optional[str] = Field(
        default=None,
        description="Descrição do que o item verifica"
    )


# =========================================================================
# DEFINIÇÃO DE CHECKLISTS POR TIPO DE ARTIGO
# =========================================================================

# Checklist para artigo empírico/experimental
CHECKLIST_EMPIRICAL = [
    ChecklistItem(
        id="scope",
        label="Escopo definido",
        description="Claim específico e delimitado"
    ),
    ChecklistItem(
        id="population",
        label="População identificada",
        description="População-alvo clara (quem será estudado)"
    ),
    ChecklistItem(
        id="metrics",
        label="Métricas definidas",
        description="Como medir resultados (métricas operacionais)"
    ),
    ChecklistItem(
        id="methodology",
        label="Metodologia estruturada",
        description="Desenho experimental ou quasi-experimental"
    ),
    ChecklistItem(
        id="baseline",
        label="Baseline definido",
        description="Ponto de comparação claro"
    ),
]

# Checklist para revisão de literatura
CHECKLIST_REVIEW = [
    ChecklistItem(
        id="research_question",
        label="Questão de pesquisa (PICO/SPIDER)",
        description="Questão estruturada para revisão"
    ),
    ChecklistItem(
        id="search_strategy",
        label="Estratégia de busca",
        description="Bases de dados e termos de busca definidos"
    ),
    ChecklistItem(
        id="inclusion_criteria",
        label="Critérios de inclusão/exclusão",
        description="Como filtrar estudos relevantes"
    ),
    ChecklistItem(
        id="synthesis",
        label="Síntese de evidências",
        description="Como sintetizar achados (narrativa, meta-análise, etc)"
    ),
    ChecklistItem(
        id="gaps",
        label="Lacunas identificadas",
        description="O que falta na literatura"
    ),
]

# Checklist para artigo teórico/conceitual
CHECKLIST_THEORETICAL = [
    ChecklistItem(
        id="problem",
        label="Problema conceitual",
        description="Problema ou gap teórico identificado"
    ),
    ChecklistItem(
        id="framework",
        label="Framework proposto",
        description="Modelo ou framework teórico estruturado"
    ),
    ChecklistItem(
        id="logical_consistency",
        label="Consistência lógica",
        description="Argumentação coerente e sem contradições"
    ),
    ChecklistItem(
        id="contributions",
        label="Contribuições claras",
        description="Como framework avança conhecimento existente"
    ),
    ChecklistItem(
        id="implications",
        label="Implicações discutidas",
        description="Implicações teóricas e práticas explícitas"
    ),
]

# Checklist genérico (quando tipo não especificado)
CHECKLIST_GENERIC = [
    ChecklistItem(
        id="claim",
        label="Afirmação clara",
        description="Claim específico e não vago"
    ),
    ChecklistItem(
        id="context",
        label="Contexto definido",
        description="Domínio e tecnologia identificados"
    ),
    ChecklistItem(
        id="foundations",
        label="Fundamentos sólidos",
        description="Premises claras (>= 2)"
    ),
    ChecklistItem(
        id="assumptions_low",
        label="Suposições baixas",
        description="Poucas hipóteses não verificadas (<= 2)"
    ),
    ChecklistItem(
        id="questions_answered",
        label="Lacunas respondidas",
        description="Open_questions vazias ou poucas (<= 1)"
    ),
]


# =========================================================================
# LÓGICA DE DETECÇÃO DE STATUS
# =========================================================================

class ProgressTracker:
    """
    Rastreador de progresso baseado em modelo cognitivo.

    Detecta status de cada item do checklist analisando campos do CognitiveModel.

    Example:
        >>> tracker = ProgressTracker(article_type="empirical")
        >>> checklist = tracker.evaluate(cognitive_model)
        >>> for item in checklist:
        ...     print(f"{item.label}: {item.status}")
    """

    def __init__(self, article_type: str = "generic"):
        """
        Inicializa ProgressTracker.

        Args:
            article_type: Tipo de artigo ("empirical", "review", "theoretical", "generic")
        """
        self.article_type = article_type
        self.checklist_template = get_checklist_for_article_type(article_type)

    def evaluate(self, cognitive_model: CognitiveModel) -> List[ChecklistItem]:
        """
        Avalia progresso baseado no modelo cognitivo.

        Args:
            cognitive_model: CognitiveModel a avaliar

        Returns:
            List[ChecklistItem]: Checklist com status atualizado

        Example:
            >>> checklist = tracker.evaluate(cognitive_model)
            >>> completed = [item for item in checklist if item.status == "completed"]
            >>> print(f"{len(completed)}/{len(checklist)} itens completos")
        """
        # Copiar template para não modificar original
        checklist = [item.model_copy() for item in self.checklist_template]

        # Avaliar cada item baseado no tipo de artigo
        if self.article_type == "empirical":
            self._evaluate_empirical(checklist, cognitive_model)
        elif self.article_type == "review":
            self._evaluate_review(checklist, cognitive_model)
        elif self.article_type == "theoretical":
            self._evaluate_theoretical(checklist, cognitive_model)
        else:
            self._evaluate_generic(checklist, cognitive_model)

        return checklist

    def _evaluate_empirical(
        self,
        checklist: List[ChecklistItem],
        model: CognitiveModel
    ):
        """Avalia checklist empírico baseado em modelo cognitivo."""
        context = model.context

        for item in checklist:
            if item.id == "scope":
                # Escopo: claim não vazio e específico (>20 chars)
                item.status = "completed" if len(model.claim) > 20 else "pending"

            elif item.id == "population":
                # População: context.population definido e não "not specified"
                population = context.get("population", "")
                if population and population != "not specified":
                    item.status = "completed"
                elif len(model.premises) > 0:  # Mencionado em premises
                    item.status = "in_progress"
                else:
                    item.status = "pending"

            elif item.id == "metrics":
                # Métricas: context.metrics definido
                metrics = context.get("metrics", "")
                if metrics and metrics != "not specified":
                    item.status = "completed"
                else:
                    item.status = "pending"

            elif item.id == "methodology":
                # Metodologia: premises >= 2 (fundamentos claros)
                item.status = "completed" if len(model.premises) >= 2 else "pending"

            elif item.id == "baseline":
                # Baseline: assumptions <= 2 (poucas suposições não verificadas)
                item.status = "completed" if len(model.assumptions) <= 2 else "in_progress"

    def _evaluate_review(
        self,
        checklist: List[ChecklistItem],
        model: CognitiveModel
    ):
        """Avalia checklist de revisão baseado em modelo cognitivo."""
        for item in checklist:
            if item.id == "research_question":
                # Questão estruturada: claim específico
                item.status = "completed" if len(model.claim) > 20 else "pending"

            elif item.id == "search_strategy":
                # Estratégia de busca: mencionado em premises ou context
                if any("search" in p.lower() or "base" in p.lower() for p in model.premises):
                    item.status = "completed"
                else:
                    item.status = "pending"

            elif item.id == "inclusion_criteria":
                # Critérios: mencionado em assumptions ou premises
                if len(model.premises) >= 1:
                    item.status = "in_progress"
                else:
                    item.status = "pending"

            elif item.id == "synthesis":
                # Síntese: solid_grounds preenchido (evidências encontradas)
                item.status = "completed" if len(model.solid_grounds) > 0 else "pending"

            elif item.id == "gaps":
                # Lacunas: open_questions preenchido
                item.status = "completed" if len(model.open_questions) > 0 else "pending"

    def _evaluate_theoretical(
        self,
        checklist: List[ChecklistItem],
        model: CognitiveModel
    ):
        """Avalia checklist teórico baseado em modelo cognitivo."""
        for item in checklist:
            if item.id == "problem":
                # Problema conceitual: claim específico
                item.status = "completed" if len(model.claim) > 20 else "pending"

            elif item.id == "framework":
                # Framework: premises estruturadas
                item.status = "completed" if len(model.premises) >= 2 else "in_progress"

            elif item.id == "logical_consistency":
                # Consistência lógica: sem contradições
                item.status = "completed" if len(model.contradictions) == 0 else "in_progress"

            elif item.id == "contributions":
                # Contribuições: context completo
                context = model.context
                if context.get("domain") and context.get("technology"):
                    item.status = "completed"
                else:
                    item.status = "pending"

            elif item.id == "implications":
                # Implicações: assumptions baixas (explorou bem)
                item.status = "completed" if len(model.assumptions) <= 2 else "in_progress"

    def _evaluate_generic(
        self,
        checklist: List[ChecklistItem],
        model: CognitiveModel
    ):
        """Avalia checklist genérico baseado em modelo cognitivo."""
        for item in checklist:
            if item.id == "claim":
                item.status = "completed" if len(model.claim) > 20 else "pending"

            elif item.id == "context":
                context = model.context
                if context.get("domain") or context.get("technology"):
                    item.status = "completed"
                else:
                    item.status = "pending"

            elif item.id == "foundations":
                item.status = "completed" if len(model.premises) >= 2 else "in_progress"

            elif item.id == "assumptions_low":
                item.status = "completed" if len(model.assumptions) <= 2 else "in_progress"

            elif item.id == "questions_answered":
                item.status = "completed" if len(model.open_questions) <= 1 else "in_progress"


# =========================================================================
# FUNÇÕES HELPERS GLOBAIS
# =========================================================================

def get_checklist_for_article_type(article_type: str) -> List[ChecklistItem]:
    """
    Retorna checklist template para tipo de artigo.

    Args:
        article_type: Tipo de artigo ("empirical", "review", "theoretical", "generic")

    Returns:
        List[ChecklistItem]: Template de checklist (status pendente)

    Example:
        >>> checklist = get_checklist_for_article_type("empirical")
        >>> for item in checklist:
        ...     print(f"- {item.label}")
    """
    checklists = {
        "empirical": CHECKLIST_EMPIRICAL,
        "review": CHECKLIST_REVIEW,
        "theoretical": CHECKLIST_THEORETICAL,
        "generic": CHECKLIST_GENERIC,
    }

    return checklists.get(article_type, CHECKLIST_GENERIC)


def evaluate_progress(
    cognitive_model: CognitiveModel,
    article_type: Optional[str] = None
) -> List[ChecklistItem]:
    """
    Helper global para avaliar progresso de argumento.

    Args:
        cognitive_model: CognitiveModel a avaliar
        article_type: Tipo de artigo (opcional). Se None, infere de context.article_type

    Returns:
        List[ChecklistItem]: Checklist com status atualizado

    Example:
        >>> from agents.checklist import evaluate_progress
        >>> checklist = evaluate_progress(cognitive_model)
        >>> completed_count = sum(1 for item in checklist if item.status == "completed")
        >>> print(f"Progresso: {completed_count}/{len(checklist)}")
    """
    # Inferir article_type se não especificado
    if article_type is None:
        article_type = cognitive_model.context.get("article_type", "generic")

    tracker = ProgressTracker(article_type)
    return tracker.evaluate(cognitive_model)
