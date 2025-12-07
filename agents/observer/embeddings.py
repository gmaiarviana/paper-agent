"""
Geracao de embeddings semanticos para o Observador.

Este modulo encapsula a geracao de embeddings via sentence-transformers
para busca semantica de conceitos.

Modelo: all-MiniLM-L6-v2
- Dimensoes: 384
- Tamanho: ~80MB
- Performance: ~50ms por texto
- Gratuito e local (nao requer API)

Versao: 1.0 (Epico 10.3)
Data: 07/12/2025
"""

import logging
from typing import List, Optional
from functools import lru_cache

logger = logging.getLogger(__name__)

# Modelo recomendado para embeddings semanticos
DEFAULT_MODEL = "all-MiniLM-L6-v2"

# Cache para o modelo (carrega apenas uma vez)
_embedding_model = None


def _get_model():
    """
    Retorna instancia do modelo de embeddings (singleton).

    Carrega o modelo apenas uma vez e reutiliza nas chamadas subsequentes.
    """
    global _embedding_model

    if _embedding_model is None:
        from sentence_transformers import SentenceTransformer

        logger.info(f"Carregando modelo de embeddings: {DEFAULT_MODEL}")
        _embedding_model = SentenceTransformer(DEFAULT_MODEL)
        logger.info(f"Modelo carregado: {DEFAULT_MODEL} (384 dimensoes)")

    return _embedding_model


def generate_embedding(text: str) -> List[float]:
    """
    Gera embedding semantico para um texto.

    Args:
        text: Texto para gerar embedding (ex: "cooperacao", "LLMs").

    Returns:
        Lista de floats representando o vetor semantico (384 dimensoes).

    Example:
        >>> embedding = generate_embedding("cooperacao")
        >>> print(len(embedding))
        384
        >>> print(type(embedding[0]))
        <class 'float'>
    """
    model = _get_model()

    # Gerar embedding
    embedding = model.encode(text)

    # Converter para lista de floats (compativel com ChromaDB)
    return embedding.tolist()


def generate_embeddings_batch(texts: List[str]) -> List[List[float]]:
    """
    Gera embeddings para multiplos textos em lote.

    Mais eficiente que chamar generate_embedding() para cada texto.

    Args:
        texts: Lista de textos para gerar embeddings.

    Returns:
        Lista de embeddings (cada um com 384 dimensoes).

    Example:
        >>> embeddings = generate_embeddings_batch(["cooperacao", "colaboracao"])
        >>> print(len(embeddings))
        2
        >>> print(len(embeddings[0]))
        384
    """
    if not texts:
        return []

    model = _get_model()

    # Gerar embeddings em lote
    embeddings = model.encode(texts)

    # Converter para lista de listas
    return [emb.tolist() for emb in embeddings]


def calculate_similarity(embedding1: List[float], embedding2: List[float]) -> float:
    """
    Calcula similaridade cosseno entre dois embeddings.

    Args:
        embedding1: Primeiro vetor (384 dims).
        embedding2: Segundo vetor (384 dims).

    Returns:
        Similaridade cosseno (0.0 a 1.0).

    Example:
        >>> emb1 = generate_embedding("cooperacao")
        >>> emb2 = generate_embedding("colaboracao")
        >>> similarity = calculate_similarity(emb1, emb2)
        >>> print(f"Similaridade: {similarity:.2f}")
        Similaridade: 0.87
    """
    import numpy as np

    # Converter para numpy arrays
    vec1 = np.array(embedding1)
    vec2 = np.array(embedding2)

    # Calcular similaridade cosseno
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    similarity = dot_product / (norm1 * norm2)

    return float(similarity)


def get_embedding_dimensions() -> int:
    """
    Retorna numero de dimensoes do modelo de embeddings.

    Returns:
        Numero de dimensoes (384 para all-MiniLM-L6-v2).
    """
    return 384


def get_model_name() -> str:
    """
    Retorna nome do modelo de embeddings em uso.

    Returns:
        Nome do modelo.
    """
    return DEFAULT_MODEL
