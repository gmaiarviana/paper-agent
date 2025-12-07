"""
Testes unitarios para Observador POC (Epico 10.6).

Valida o Observador de forma isolada, sem chamadas LLM reais.
Usa mocks para extratores e vetores fixos para busca semantica.

Versao: 1.0
Data: 07/12/2025
"""

import pytest
import tempfile
import shutil
import sqlite3
from pathlib import Path
from unittest.mock import patch, MagicMock

from agents.observer import (
    ConceptCatalog,
    Concept,
    SimilarConcept,
    persist_concepts,
    persist_concepts_batch,
    ConceptPersistResult,
    generate_embedding,
    calculate_similarity,
    SIMILARITY_THRESHOLD_SAME,
    SIMILARITY_THRESHOLD_AUTO
)


class TestConceptCatalog:
    """Testes para ConceptCatalog (ChromaDB + SQLite)."""

    @pytest.fixture
    def temp_dir(self):
        """Cria diretorio temporario para testes."""
        temp_path = Path(tempfile.mkdtemp())
        yield temp_path
        # Cleanup
        if temp_path.exists():
            shutil.rmtree(temp_path, ignore_errors=True)

    @pytest.fixture
    def catalog(self, temp_dir):
        """Cria ConceptCatalog com diretorio temporario."""
        return ConceptCatalog(
            chroma_path=str(temp_dir / "chroma"),
            sqlite_path=str(temp_dir / "concepts.db")
        )

    def test_init_creates_directories(self, temp_dir):
        """Testa que __init__ cria diretorios necessarios."""
        chroma_path = temp_dir / "chroma"
        sqlite_path = temp_dir / "concepts.db"

        catalog = ConceptCatalog(
            chroma_path=str(chroma_path),
            sqlite_path=str(sqlite_path)
        )

        assert chroma_path.exists()
        assert sqlite_path.exists()

    def test_sqlite_schema_created(self, catalog, temp_dir):
        """Valida que schema SQLite foi criado corretamente."""
        conn = sqlite3.connect(str(temp_dir / "concepts.db"))
        cursor = conn.cursor()

        # Verificar tabelas
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )
        tables = [row[0] for row in cursor.fetchall()]

        assert "concepts" in tables
        assert "concept_variations" in tables
        assert "idea_concepts" in tables

        # Verificar indices
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='index' ORDER BY name"
        )
        indexes = [row[0] for row in cursor.fetchall()]

        assert "idx_concepts_label" in indexes
        assert "idx_concept_variations_concept" in indexes
        assert "idx_idea_concepts_idea" in indexes
        assert "idx_idea_concepts_concept" in indexes

        conn.close()

    def test_save_concept_creates_new(self, catalog):
        """Testa que save_concept cria novo conceito."""
        embedding = [0.1] * 384  # Vetor fixo

        concept_id = catalog.save_concept(
            label="cooperacao",
            essence="trabalho conjunto",
            embedding=embedding
        )

        assert concept_id is not None
        assert len(concept_id) == 36  # UUID format

        # Verificar no SQLite
        concept = catalog.get_concept_by_id(concept_id)
        assert concept is not None
        assert concept.label == "cooperacao"
        assert concept.essence == "trabalho conjunto"

    def test_save_concept_deduplicates(self, catalog):
        """Testa que conceitos similares sao deduplicados."""
        # Criar primeiro conceito (sem fornecer embedding - usa real)
        id1 = catalog.save_concept("cooperacao", "trabalho conjunto")

        # Tentar criar conceito identico (mesmo label)
        id2 = catalog.save_concept("cooperacao", "acao conjunta")

        # Deve retornar mesmo ID (deduplicado por similaridade alta)
        assert id1 == id2

    def test_find_similar_concepts_returns_ordered(self, catalog):
        """Testa que find_similar_concepts retorna ordenado por similaridade."""
        # Criar conceitos com embeddings distintos
        catalog.save_concept("A", "conceito A", [1.0] + [0.0] * 383)
        catalog.save_concept("B", "conceito B", [0.9] + [0.1] * 383)
        catalog.save_concept("C", "conceito C", [0.5] + [0.5] * 383)

        # Buscar similar a A
        with patch('agents.observer.catalog.generate_embedding') as mock_embed:
            mock_embed.return_value = [1.0] + [0.0] * 383
            results = catalog.find_similar_concepts("A", top_k=3, threshold=0.0)

        # Deve estar ordenado por similaridade (desc)
        assert len(results) >= 1
        if len(results) > 1:
            assert results[0].similarity >= results[1].similarity

    def test_add_variation(self, catalog):
        """Testa adicao de variacao a conceito existente."""
        embedding = [0.1] * 384
        concept_id = catalog.save_concept("cooperacao", "trabalho conjunto", embedding)

        # Adicionar variacao
        result = catalog.add_variation(concept_id, "colaboracao")
        assert result is True

        # Verificar que variacao foi adicionada
        concept = catalog.get_concept_by_id(concept_id)
        assert "colaboracao" in concept.variations

    def test_link_idea_concept(self, catalog):
        """Testa criacao de link N:N entre Idea e Concept."""
        embedding = [0.1] * 384
        concept_id = catalog.save_concept("cooperacao", "trabalho conjunto", embedding)

        # Criar link
        result = catalog.link_idea_concept("idea-123", concept_id)
        assert result is True

        # Verificar link
        concepts = catalog.get_concepts_for_idea("idea-123")
        assert len(concepts) == 1
        assert concepts[0].id == concept_id

    def test_get_stats(self, catalog):
        """Testa get_stats retorna estatisticas corretas."""
        # Criar dados de teste
        embedding = [0.1] * 384
        c1 = catalog.save_concept("A", "conceito A", embedding)
        c2 = catalog.save_concept("B", "conceito B", [0.2] * 384)

        catalog.add_variation(c1, "variacao1")
        catalog.add_variation(c1, "variacao2")
        catalog.link_idea_concept("idea-1", c1)
        catalog.link_idea_concept("idea-2", c2)

        stats = catalog.get_stats()

        assert stats["concepts"] == 2
        assert stats["variations"] == 2
        assert stats["idea_links"] == 2
        assert stats["chroma_vectors"] == 2

    def test_delete_concept(self, catalog):
        """Testa remocao de conceito."""
        embedding = [0.1] * 384
        concept_id = catalog.save_concept("temp", "temporario", embedding)

        # Deletar
        result = catalog.delete_concept(concept_id)
        assert result is True

        # Verificar que foi removido
        concept = catalog.get_concept_by_id(concept_id)
        assert concept is None


class TestConceptPipeline:
    """Testes para pipeline de persistencia de conceitos."""

    @pytest.fixture
    def temp_dir(self):
        """Cria diretorio temporario para testes."""
        temp_path = Path(tempfile.mkdtemp())
        yield temp_path
        if temp_path.exists():
            shutil.rmtree(temp_path, ignore_errors=True)

    @pytest.fixture
    def catalog(self, temp_dir):
        """Cria ConceptCatalog com diretorio temporario."""
        return ConceptCatalog(
            chroma_path=str(temp_dir / "chroma"),
            sqlite_path=str(temp_dir / "concepts.db")
        )

    def test_persist_concepts_empty_list(self, catalog):
        """Testa que lista vazia retorna lista vazia."""
        results = persist_concepts([], catalog=catalog)
        assert results == []

    def test_persist_concepts_creates_new(self, catalog):
        """Testa que conceitos novos sao criados."""
        with patch('agents.observer.concept_pipeline.generate_embedding') as mock_embed:
            mock_embed.return_value = [0.1] * 384

            results = persist_concepts(
                ["conceito1", "conceito2"],
                catalog=catalog
            )

        assert len(results) == 2
        assert all(r.is_new for r in results)

    def test_persist_concepts_with_idea_id(self, catalog):
        """Testa que conceitos sao linkados a idea quando fornecido."""
        with patch('agents.observer.concept_pipeline.generate_embedding') as mock_embed:
            mock_embed.return_value = [0.1] * 384

            results = persist_concepts(
                ["conceito1"],
                idea_id="idea-test",
                catalog=catalog
            )

        # Verificar link foi criado
        concepts = catalog.get_concepts_for_idea("idea-test")
        assert len(concepts) == 1

    def test_persist_concepts_batch_returns_summary(self, catalog):
        """Testa que persist_concepts_batch retorna resumo correto."""
        with patch('agents.observer.concept_pipeline.generate_embedding') as mock_embed:
            mock_embed.return_value = [0.1] * 384

            result = persist_concepts_batch(
                ["A", "B", "C"],
                catalog=catalog
            )

        assert "concept_ids" in result
        assert "new_count" in result
        assert "merged_count" in result
        assert "total" in result
        assert result["total"] == 3


class TestEmbeddings:
    """Testes para funcoes de embedding."""

    def test_generate_embedding_returns_correct_dimensions(self):
        """Testa que embedding tem dimensoes corretas (384)."""
        embedding = generate_embedding("teste")
        assert len(embedding) == 384

    def test_generate_embedding_deterministic(self):
        """Testa que mesmo texto gera mesmo embedding."""
        emb1 = generate_embedding("cooperacao")
        emb2 = generate_embedding("cooperacao")

        # Deve ser identico
        assert emb1 == emb2

    def test_calculate_similarity_identical(self):
        """Testa que vetores identicos tem similaridade 1.0."""
        emb = generate_embedding("teste")
        similarity = calculate_similarity(emb, emb)

        assert similarity == pytest.approx(1.0, abs=0.01)

    def test_calculate_similarity_different(self):
        """Testa que conceitos diferentes tem similaridade menor."""
        emb1 = generate_embedding("cooperacao")
        emb2 = generate_embedding("matematica")

        similarity = calculate_similarity(emb1, emb2)

        assert similarity < 0.5  # Conceitos bem diferentes

    def test_calculate_similarity_similar(self):
        """Testa que conceitos similares tem similaridade alta."""
        emb1 = generate_embedding("cooperacao")
        emb2 = generate_embedding("colaboracao")

        similarity = calculate_similarity(emb1, emb2)

        assert similarity > 0.5  # Conceitos relacionados


class TestDeduplication:
    """Testes especificos para logica de deduplicacao."""

    @pytest.fixture
    def temp_dir(self):
        """Cria diretorio temporario para testes."""
        temp_path = Path(tempfile.mkdtemp())
        yield temp_path
        if temp_path.exists():
            shutil.rmtree(temp_path, ignore_errors=True)

    @pytest.fixture
    def catalog(self, temp_dir):
        """Cria ConceptCatalog com diretorio temporario."""
        return ConceptCatalog(
            chroma_path=str(temp_dir / "chroma"),
            sqlite_path=str(temp_dir / "concepts.db")
        )

    def test_threshold_same_is_080(self):
        """Valida que threshold para mesmo conceito e 0.80."""
        assert SIMILARITY_THRESHOLD_SAME == 0.80

    def test_threshold_auto_is_090(self):
        """Valida que threshold para auto-add variation e 0.90."""
        assert SIMILARITY_THRESHOLD_AUTO == 0.90

    def test_deduplication_with_real_embeddings(self, catalog):
        """Testa deduplicacao com embeddings reais (nao mocks)."""
        # Salvar "cooperacao"
        id1 = catalog.save_concept("cooperacao", "trabalho conjunto")

        # Tentar salvar "cooperacao" novamente (identico)
        id2 = catalog.save_concept("cooperacao", "outra descricao")

        # Deve ser o mesmo conceito
        assert id1 == id2

        # Verificar que variacao foi adicionada (se threshold alto)
        concept = catalog.get_concept_by_id(id1)
        # Label original deve ser mantido
        assert concept.label == "cooperacao"


class TestProcessTurnIntegration:
    """Testes de integracao leve para process_turn (com mocks de LLM)."""

    def test_process_turn_signature(self):
        """Testa que process_turn aceita novos parametros."""
        from agents.observer import process_turn
        import inspect

        sig = inspect.signature(process_turn)
        params = list(sig.parameters.keys())

        # Parametros do Epic 10.4
        assert "persist_concepts_flag" in params
        assert "idea_id" in params

        # Parametros do Epic 10.3 (Agentic RAG prep)
        assert "extract_claims" in params
        assert "extract_concepts" in params
        assert "extract_fundamentos" in params
        assert "detect_contradictions" in params
        assert "calculate_metrics_flag" in params
