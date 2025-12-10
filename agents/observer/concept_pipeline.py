"""
Pipeline de Detecção e Persistência de Conceitos.

Este módulo implementa a "cola" entre extração de conceitos (LLM)
e persistência no catálogo (ChromaDB + SQLite).

Fluxo:
1. extract_concepts() retorna List[str] de conceitos
2. persist_concepts() processa cada conceito:
   - Gera embedding
   - Salva no catálogo (com deduplicação automática)
   - Opcionalmente linka a uma Idea

"""

import logging
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

from .embeddings import generate_embedding
from .catalog import (
    ConceptCatalog,
    get_concept_catalog,
    SIMILARITY_THRESHOLD_SAME
)

logger = logging.getLogger(__name__)

@dataclass
class ConceptPersistResult:
    """Resultado da persistência de um conceito."""

    concept_id: str
    label: str
    is_new: bool
    similarity: Optional[float] = None  # Se não é novo, qual foi a similaridade
    merged_with: Optional[str] = None   # Se não é novo, com qual conceito foi merged

    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário."""
        return {
            "concept_id": self.concept_id,
            "label": self.label,
            "is_new": self.is_new,
            "similarity": self.similarity,
            "merged_with": self.merged_with
        }

def persist_concepts(
    concepts: List[str],
    idea_id: Optional[str] = None,
    catalog: Optional[ConceptCatalog] = None
) -> List[ConceptPersistResult]:
    """
    Persiste conceitos extraídos no catálogo.

    Para cada conceito:
    1. Gera embedding via sentence-transformers
    2. Chama catalog.save_concept() (deduplicação automática)
    3. Se idea_id fornecido, cria link N:N

    Args:
        concepts: Lista de conceitos extraídos (strings).
        idea_id: ID da Idea para criar link N:N (opcional).
        catalog: Instância do catálogo (usa singleton se não fornecido).

    Returns:
        Lista de ConceptPersistResult com info de cada conceito.

    Example:
        >>> results = persist_concepts(
        ...     concepts=["cooperação", "produtividade"],
        ...     idea_id="idea-123"
        ... )
        >>> for r in results:
        ...     print(f"{r.label}: {'novo' if r.is_new else 'existente'}")
        cooperação: novo
        produtividade: existente
    """
    if not concepts:
        logger.debug("Nenhum conceito para persistir")
        return []

    if catalog is None:
        catalog = get_concept_catalog()

    results = []

    for concept_label in concepts:
        result = _persist_single_concept(
            concept_label=concept_label,
            idea_id=idea_id,
            catalog=catalog
        )
        results.append(result)

    # Log resumo
    new_count = sum(1 for r in results if r.is_new)
    merged_count = len(results) - new_count

    logger.info(
        f"Conceitos persistidos: {len(results)} total "
        f"({new_count} novos, {merged_count} merged)"
    )

    return results

def _persist_single_concept(
    concept_label: str,
    idea_id: Optional[str],
    catalog: ConceptCatalog
) -> ConceptPersistResult:
    """
    Persiste um único conceito no catálogo.

    Args:
        concept_label: Label do conceito.
        idea_id: ID da Idea para link (opcional).
        catalog: Instância do catálogo.

    Returns:
        ConceptPersistResult com informações da persistência.
    """
    # 1. Verificar se conceito similar já existe
    similar = catalog.find_similar_concepts(
        query=concept_label,
        top_k=1,
        threshold=SIMILARITY_THRESHOLD_SAME
    )

    is_new = len(similar) == 0
    similarity = similar[0].similarity if similar else None
    merged_with = similar[0].concept.label if similar else None

    # 2. Gerar embedding
    embedding = generate_embedding(concept_label)

    # 3. Salvar no catálogo (save_concept já faz deduplicação)
    concept_id = catalog.save_concept(
        label=concept_label,
        essence=None,  # Pode ser extraído pelo LLM no futuro
        embedding=embedding
    )

    # 4. Linkar à Idea (se fornecido)
    if idea_id:
        catalog.link_idea_concept(idea_id, concept_id)
        logger.debug(f"Conceito '{concept_label}' linkado à idea {idea_id}")

    # Log individual
    if is_new:
        logger.debug(f"Novo conceito criado: '{concept_label}' (id={concept_id})")
    else:
        logger.debug(
            f"Conceito '{concept_label}' merged com '{merged_with}' "
            f"(similaridade={similarity:.2f})"
        )

    return ConceptPersistResult(
        concept_id=concept_id,
        label=concept_label,
        is_new=is_new,
        similarity=similarity,
        merged_with=merged_with
    )

def persist_concepts_batch(
    concepts: List[str],
    idea_id: Optional[str] = None,
    catalog: Optional[ConceptCatalog] = None
) -> Dict[str, Any]:
    """
    Versão batch que retorna resumo agregado.

    Útil para integração com process_turn() onde queremos
    apenas o resumo, não detalhes de cada conceito.

    Args:
        concepts: Lista de conceitos.
        idea_id: ID da Idea (opcional).
        catalog: Instância do catálogo (opcional).

    Returns:
        Dict com:
        - concept_ids: Lista de IDs persistidos
        - new_count: Quantidade de conceitos novos
        - merged_count: Quantidade de conceitos merged
        - details: Lista de ConceptPersistResult (para debug)

    Example:
        >>> result = persist_concepts_batch(["cooperação", "produtividade"])
        >>> print(result["new_count"])
        1
    """
    results = persist_concepts(
        concepts=concepts,
        idea_id=idea_id,
        catalog=catalog
    )

    new_count = sum(1 for r in results if r.is_new)

    return {
        "concept_ids": [r.concept_id for r in results],
        "new_count": new_count,
        "merged_count": len(results) - new_count,
        "total": len(results),
        "details": [r.to_dict() for r in results]
    }
