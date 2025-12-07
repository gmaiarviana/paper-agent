"""
Catalogo de Conceitos do Observador.

Este modulo implementa a persistencia de conceitos usando:
- ChromaDB: Vetores semanticos para busca por similaridade
- SQLite: Metadados estruturados (label, essence, variations)

Arquitetura hibrida permite busca semantica rapida (ChromaDB)
com metadados ricos e relacionamentos (SQLite).

Versao: 1.0 (Epico 10.3)
Data: 07/12/2025
"""

import logging
import sqlite3
import json
import uuid
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

import chromadb
from chromadb.config import Settings

from .embeddings import generate_embedding, calculate_similarity

logger = logging.getLogger(__name__)

# Paths padrao para persistencia
DEFAULT_CHROMA_PATH = "./data/chroma"
DEFAULT_SQLITE_PATH = "./data/concepts.db"

# Thresholds de similaridade
SIMILARITY_THRESHOLD_SAME = 0.80  # >= 0.80: mesmo conceito
SIMILARITY_THRESHOLD_AUTO = 0.90  # >= 0.90: adiciona variation automaticamente


@dataclass
class Concept:
    """Representa um conceito no catalogo."""

    id: str
    label: str
    essence: Optional[str] = None
    variations: Optional[List[str]] = None
    chroma_id: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionario."""
        return {
            "id": self.id,
            "label": self.label,
            "essence": self.essence,
            "variations": self.variations or [],
            "chroma_id": self.chroma_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


@dataclass
class SimilarConcept:
    """Resultado de busca de conceito similar."""

    concept: Concept
    similarity: float

    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionario."""
        return {
            "concept": self.concept.to_dict(),
            "similarity": self.similarity
        }


class ConceptCatalog:
    """
    Catalogo de conceitos com persistencia hibrida ChromaDB + SQLite.

    ChromaDB armazena vetores semanticos para busca por similaridade.
    SQLite armazena metadados estruturados e relacionamentos.

    Attributes:
        chroma_path: Caminho para persistencia do ChromaDB.
        sqlite_path: Caminho para banco SQLite.

    Example:
        >>> catalog = ConceptCatalog()
        >>> concept_id = catalog.save_concept(
        ...     label="Cooperacao",
        ...     essence="Acao coordenada entre agentes"
        ... )
        >>> similar = catalog.find_similar_concepts("colaboracao")
        >>> print(similar[0].similarity)
        0.87
    """

    def __init__(
        self,
        chroma_path: str = DEFAULT_CHROMA_PATH,
        sqlite_path: str = DEFAULT_SQLITE_PATH
    ):
        """
        Inicializa o catalogo de conceitos.

        Args:
            chroma_path: Caminho para persistencia do ChromaDB.
            sqlite_path: Caminho para banco SQLite.
        """
        self.chroma_path = chroma_path
        self.sqlite_path = sqlite_path

        # Garantir que diretorios existam
        os.makedirs(os.path.dirname(chroma_path) or ".", exist_ok=True)
        os.makedirs(os.path.dirname(sqlite_path) or ".", exist_ok=True)

        # Inicializar ChromaDB
        self._init_chromadb()

        # Inicializar SQLite
        self._init_sqlite()

        logger.info(
            f"ConceptCatalog inicializado "
            f"(chroma={chroma_path}, sqlite={sqlite_path})"
        )

    def _init_chromadb(self) -> None:
        """Inicializa cliente e collection do ChromaDB."""
        self._chroma_client = chromadb.PersistentClient(
            path=self.chroma_path,
            settings=Settings(anonymized_telemetry=False)
        )

        self._collection = self._chroma_client.get_or_create_collection(
            name="concepts",
            metadata={"description": "Biblioteca global de conceitos"}
        )

        logger.debug(f"ChromaDB collection 'concepts' inicializada")

    def _init_sqlite(self) -> None:
        """Inicializa banco SQLite com schema."""
        self._conn = sqlite3.connect(self.sqlite_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row

        # Criar tabelas
        self._conn.executescript("""
            -- Tabela principal de conceitos
            CREATE TABLE IF NOT EXISTS concepts (
                id TEXT PRIMARY KEY,
                label TEXT NOT NULL,
                essence TEXT,
                variations TEXT,  -- JSON array
                chroma_id TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            );

            -- Tabela de variacoes (normalizacao)
            CREATE TABLE IF NOT EXISTS concept_variations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                concept_id TEXT NOT NULL,
                variation TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (concept_id) REFERENCES concepts(id),
                UNIQUE(concept_id, variation)
            );

            -- Tabela de relacionamento Idea <-> Concept (N:N)
            CREATE TABLE IF NOT EXISTS idea_concepts (
                idea_id TEXT NOT NULL,
                concept_id TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (idea_id, concept_id),
                FOREIGN KEY (concept_id) REFERENCES concepts(id)
            );

            -- Indices para performance
            CREATE INDEX IF NOT EXISTS idx_concepts_label ON concepts(label);
            CREATE INDEX IF NOT EXISTS idx_concept_variations_concept
                ON concept_variations(concept_id);
            CREATE INDEX IF NOT EXISTS idx_idea_concepts_idea
                ON idea_concepts(idea_id);
            CREATE INDEX IF NOT EXISTS idx_idea_concepts_concept
                ON idea_concepts(concept_id);
        """)

        self._conn.commit()
        logger.debug("SQLite schema inicializado")

    def save_concept(
        self,
        label: str,
        essence: Optional[str] = None,
        embedding: Optional[List[float]] = None
    ) -> str:
        """
        Salva um conceito no catalogo (ChromaDB + SQLite).

        Se o conceito ja existir (similaridade >= 0.80), adiciona como variation.

        Args:
            label: Label do conceito (ex: "Cooperacao").
            essence: Descricao da essencia (opcional).
            embedding: Vetor semantico (gera automaticamente se nao fornecido).

        Returns:
            ID do conceito (novo ou existente).

        Example:
            >>> concept_id = catalog.save_concept(
            ...     label="Cooperacao",
            ...     essence="Acao coordenada entre agentes"
            ... )
            >>> print(concept_id)
            'a1b2c3d4-...'
        """
        # Gerar embedding se nao fornecido
        if embedding is None:
            embedding = generate_embedding(label)

        # Buscar conceitos similares
        similar = self.find_similar_concepts(label, top_k=1, threshold=SIMILARITY_THRESHOLD_SAME)

        if similar and similar[0].similarity >= SIMILARITY_THRESHOLD_SAME:
            # Conceito ja existe, adicionar variation
            existing_id = similar[0].concept.id

            if similar[0].similarity >= SIMILARITY_THRESHOLD_AUTO:
                # Automatico: adiciona variation sem perguntar
                self.add_variation(existing_id, label)
                logger.info(f"Variation '{label}' adicionada ao conceito {existing_id}")
            else:
                # Threshold 0.80-0.90: poderia perguntar ao usuario
                # Por enquanto, adiciona automaticamente
                self.add_variation(existing_id, label)
                logger.info(
                    f"Variation '{label}' adicionada ao conceito {existing_id} "
                    f"(similaridade {similar[0].similarity:.2f})"
                )

            return existing_id

        # Conceito novo
        concept_id = str(uuid.uuid4())

        # Salvar no ChromaDB
        self._collection.add(
            ids=[concept_id],
            embeddings=[embedding],
            metadatas=[{
                "label": label,
                "essence": essence or ""
            }]
        )

        # Salvar no SQLite
        cursor = self._conn.execute(
            """
            INSERT INTO concepts (id, label, essence, variations, chroma_id)
            VALUES (?, ?, ?, ?, ?)
            """,
            (concept_id, label, essence, json.dumps([]), concept_id)
        )
        self._conn.commit()

        logger.info(f"Novo conceito criado: '{label}' (id={concept_id})")

        return concept_id

    def find_similar_concepts(
        self,
        query: str,
        top_k: int = 5,
        threshold: float = 0.0
    ) -> List[SimilarConcept]:
        """
        Busca conceitos similares por similaridade semantica.

        Args:
            query: Texto para buscar (ex: "colaboracao").
            top_k: Numero maximo de resultados.
            threshold: Similaridade minima (0.0 a 1.0).

        Returns:
            Lista de SimilarConcept ordenada por similaridade (descendente).

        Example:
            >>> similar = catalog.find_similar_concepts("colaboracao", top_k=3)
            >>> for s in similar:
            ...     print(f"{s.concept.label}: {s.similarity:.2f}")
            Cooperacao: 0.87
        """
        # Gerar embedding da query
        query_embedding = generate_embedding(query)

        # Buscar no ChromaDB
        results = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=min(top_k, self._collection.count() or 1),
            include=["metadatas", "distances"]
        )

        similar_concepts = []

        if results["ids"] and results["ids"][0]:
            for i, concept_id in enumerate(results["ids"][0]):
                # ChromaDB retorna distancia L2, converter para similaridade
                # Distancia L2 para similaridade cosseno aproximada:
                # similarity = 1 - (distance^2 / 2)
                distance = results["distances"][0][i]
                similarity = 1 - (distance ** 2 / 2)
                similarity = max(0.0, min(1.0, similarity))

                if similarity >= threshold:
                    # Buscar metadados completos no SQLite
                    concept = self.get_concept_by_id(concept_id)
                    if concept:
                        similar_concepts.append(
                            SimilarConcept(concept=concept, similarity=similarity)
                        )

        # Ordenar por similaridade (descendente)
        similar_concepts.sort(key=lambda x: x.similarity, reverse=True)

        return similar_concepts

    def add_variation(self, concept_id: str, variation: str) -> bool:
        """
        Adiciona uma variacao linguistica a um conceito existente.

        Args:
            concept_id: ID do conceito.
            variation: Nova variacao (ex: "colaboracao").

        Returns:
            True se adicionou, False se ja existia.

        Example:
            >>> catalog.add_variation("uuid-123", "trabalho em conjunto")
            True
        """
        try:
            # Adicionar na tabela de variacoes
            self._conn.execute(
                """
                INSERT OR IGNORE INTO concept_variations (concept_id, variation)
                VALUES (?, ?)
                """,
                (concept_id, variation)
            )

            # Atualizar JSON de variacoes no conceito
            concept = self.get_concept_by_id(concept_id)
            if concept:
                variations = concept.variations or []
                if variation not in variations:
                    variations.append(variation)

                    self._conn.execute(
                        """
                        UPDATE concepts
                        SET variations = ?, updated_at = ?
                        WHERE id = ?
                        """,
                        (json.dumps(variations), datetime.utcnow().isoformat(), concept_id)
                    )

            self._conn.commit()

            logger.debug(f"Variation '{variation}' adicionada ao conceito {concept_id}")
            return True

        except sqlite3.IntegrityError:
            logger.debug(f"Variation '{variation}' ja existe no conceito {concept_id}")
            return False

    def link_idea_concept(self, idea_id: str, concept_id: str) -> bool:
        """
        Cria link N:N entre Idea e Concept.

        Args:
            idea_id: ID da Idea.
            concept_id: ID do Concept.

        Returns:
            True se criou link, False se ja existia.

        Example:
            >>> catalog.link_idea_concept("idea-123", "concept-456")
            True
        """
        try:
            self._conn.execute(
                """
                INSERT OR IGNORE INTO idea_concepts (idea_id, concept_id)
                VALUES (?, ?)
                """,
                (idea_id, concept_id)
            )
            self._conn.commit()

            logger.debug(f"Link criado: idea={idea_id} <-> concept={concept_id}")
            return True

        except sqlite3.IntegrityError:
            logger.debug(f"Link ja existe: idea={idea_id} <-> concept={concept_id}")
            return False

    def get_concept_by_id(self, concept_id: str) -> Optional[Concept]:
        """
        Busca conceito por ID.

        Args:
            concept_id: ID do conceito.

        Returns:
            Concept ou None se nao encontrado.
        """
        cursor = self._conn.execute(
            """
            SELECT id, label, essence, variations, chroma_id, created_at, updated_at
            FROM concepts
            WHERE id = ?
            """,
            (concept_id,)
        )

        row = cursor.fetchone()
        if row:
            return Concept(
                id=row["id"],
                label=row["label"],
                essence=row["essence"],
                variations=json.loads(row["variations"]) if row["variations"] else [],
                chroma_id=row["chroma_id"],
                created_at=row["created_at"],
                updated_at=row["updated_at"]
            )

        return None

    def get_concept_by_label(self, label: str) -> Optional[Concept]:
        """
        Busca conceito por label exato.

        Args:
            label: Label do conceito.

        Returns:
            Concept ou None se nao encontrado.
        """
        cursor = self._conn.execute(
            """
            SELECT id, label, essence, variations, chroma_id, created_at, updated_at
            FROM concepts
            WHERE label = ?
            """,
            (label,)
        )

        row = cursor.fetchone()
        if row:
            return Concept(
                id=row["id"],
                label=row["label"],
                essence=row["essence"],
                variations=json.loads(row["variations"]) if row["variations"] else [],
                chroma_id=row["chroma_id"],
                created_at=row["created_at"],
                updated_at=row["updated_at"]
            )

        return None

    def get_concepts_for_idea(self, idea_id: str) -> List[Concept]:
        """
        Retorna todos os conceitos vinculados a uma Idea.

        Args:
            idea_id: ID da Idea.

        Returns:
            Lista de Concepts.
        """
        cursor = self._conn.execute(
            """
            SELECT c.id, c.label, c.essence, c.variations, c.chroma_id,
                   c.created_at, c.updated_at
            FROM concepts c
            INNER JOIN idea_concepts ic ON c.id = ic.concept_id
            WHERE ic.idea_id = ?
            """,
            (idea_id,)
        )

        concepts = []
        for row in cursor.fetchall():
            concepts.append(Concept(
                id=row["id"],
                label=row["label"],
                essence=row["essence"],
                variations=json.loads(row["variations"]) if row["variations"] else [],
                chroma_id=row["chroma_id"],
                created_at=row["created_at"],
                updated_at=row["updated_at"]
            ))

        return concepts

    def get_all_concepts(self, limit: int = 100) -> List[Concept]:
        """
        Retorna todos os conceitos do catalogo.

        Args:
            limit: Numero maximo de conceitos.

        Returns:
            Lista de Concepts.
        """
        cursor = self._conn.execute(
            """
            SELECT id, label, essence, variations, chroma_id, created_at, updated_at
            FROM concepts
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (limit,)
        )

        concepts = []
        for row in cursor.fetchall():
            concepts.append(Concept(
                id=row["id"],
                label=row["label"],
                essence=row["essence"],
                variations=json.loads(row["variations"]) if row["variations"] else [],
                chroma_id=row["chroma_id"],
                created_at=row["created_at"],
                updated_at=row["updated_at"]
            ))

        return concepts

    def count_concepts(self) -> int:
        """Retorna numero total de conceitos no catalogo."""
        cursor = self._conn.execute("SELECT COUNT(*) FROM concepts")
        return cursor.fetchone()[0]

    def delete_concept(self, concept_id: str) -> bool:
        """
        Remove um conceito do catalogo.

        Args:
            concept_id: ID do conceito.

        Returns:
            True se removeu, False se nao existia.
        """
        # Remover do ChromaDB
        try:
            self._collection.delete(ids=[concept_id])
        except Exception as e:
            logger.warning(f"Erro ao remover do ChromaDB: {e}")

        # Remover variacoes
        self._conn.execute(
            "DELETE FROM concept_variations WHERE concept_id = ?",
            (concept_id,)
        )

        # Remover links com ideas
        self._conn.execute(
            "DELETE FROM idea_concepts WHERE concept_id = ?",
            (concept_id,)
        )

        # Remover conceito
        cursor = self._conn.execute(
            "DELETE FROM concepts WHERE id = ?",
            (concept_id,)
        )
        self._conn.commit()

        deleted = cursor.rowcount > 0
        if deleted:
            logger.info(f"Conceito removido: {concept_id}")

        return deleted

    def close(self) -> None:
        """Fecha conexoes."""
        if hasattr(self, "_conn"):
            self._conn.close()
            logger.debug("SQLite connection fechada")


# Singleton global para acesso facil
_catalog_instance: Optional[ConceptCatalog] = None


def get_concept_catalog(
    chroma_path: str = DEFAULT_CHROMA_PATH,
    sqlite_path: str = DEFAULT_SQLITE_PATH
) -> ConceptCatalog:
    """
    Retorna instancia singleton do ConceptCatalog.

    Args:
        chroma_path: Caminho para ChromaDB.
        sqlite_path: Caminho para SQLite.

    Returns:
        Instancia do ConceptCatalog.

    Example:
        >>> catalog = get_concept_catalog()
        >>> catalog.save_concept("LLMs", "Large Language Models")
    """
    global _catalog_instance

    if _catalog_instance is None:
        _catalog_instance = ConceptCatalog(
            chroma_path=chroma_path,
            sqlite_path=sqlite_path
        )

    return _catalog_instance
