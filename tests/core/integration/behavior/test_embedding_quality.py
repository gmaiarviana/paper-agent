"""
Testes de qualidade do modelo de embeddings (sentence-transformers).

Estes testes nao validam codigo proprio - validam que o modelo escolhido
('all-MiniLM-L6-v2') se comporta como esperado para o uso do Observer:
- Retorna vetores com as dimensoes que o ChromaDB espera (384)
- E deterministico (mesmo input -> mesmo output)
- Produz similaridades semanticas coerentes em portugues

Sao marcados como integration porque:
- Dependem de download do modelo via HuggingFace Hub na primeira execucao
- Validam comportamento de uma biblioteca externa (sentence-transformers)
- Sao uteis como smoke test ao trocar o modelo de embeddings
"""

import pytest
import tempfile
import shutil
from pathlib import Path

pytest.importorskip("chromadb", reason="chromadb nao instalado")
pytest.importorskip("sentence_transformers", reason="sentence-transformers nao instalado")

from core.agents.observer import (
    ConceptCatalog,
    generate_embedding,
    calculate_similarity,
)

pytestmark = pytest.mark.integration


def _embedding_model_available() -> bool:
    """Tenta carregar o modelo local de embeddings. Retorna False se offline/sem cache.

    Captura apenas OSError (inclui LocalEntryNotFoundError do HuggingFace quando
    o modelo nao esta cacheado e nao ha internet) e ImportError. Bugs reais
    (TypeError, AttributeError, ValueError) propagam para nao mascarar falhas.
    """
    try:
        generate_embedding("probe")
        return True
    except (OSError, ImportError):
        return False


# Skip de modulo se o modelo nao estiver disponivel (offline, sem cache).
if not _embedding_model_available():
    pytest.skip(
        "modelo 'all-MiniLM-L6-v2' indisponivel (offline ou sem cache). "
        "Rode com internet uma vez para cachear localmente.",
        allow_module_level=True,
    )


class TestEmbeddings:
    """Sanity checks do modelo de embeddings."""

    def test_generate_embedding_returns_correct_dimensions(self):
        """Valida premissa de 384 dims assumida pelo schema ChromaDB."""
        embedding = generate_embedding("teste")
        assert len(embedding) == 384

    def test_generate_embedding_deterministic(self):
        """Mesmo texto deve produzir mesmo embedding (necessario para deduplicacao)."""
        emb1 = generate_embedding("cooperacao")
        emb2 = generate_embedding("cooperacao")
        assert emb1 == emb2

    def test_calculate_similarity_identical(self):
        """Vetores identicos tem similaridade 1.0."""
        emb = generate_embedding("teste")
        similarity = calculate_similarity(emb, emb)
        assert similarity == pytest.approx(1.0, abs=0.01)

    def test_calculate_similarity_different(self):
        """Conceitos de dominios diferentes devem ter similaridade baixa."""
        emb1 = generate_embedding("cooperacao")
        emb2 = generate_embedding("matematica")
        similarity = calculate_similarity(emb1, emb2)
        assert similarity < 0.5

    def test_calculate_similarity_similar(self):
        """Sinonimos em portugues devem ter similaridade alta (> 0.5)."""
        emb1 = generate_embedding("cooperacao")
        emb2 = generate_embedding("colaboracao")
        similarity = calculate_similarity(emb1, emb2)
        assert similarity > 0.5


class TestDeduplicationWithRealEmbeddings:
    """Valida que a deduplicacao do ConceptCatalog funciona com embeddings reais."""

    @pytest.fixture
    def temp_dir(self):
        temp_path = Path(tempfile.mkdtemp())
        yield temp_path
        if temp_path.exists():
            shutil.rmtree(temp_path, ignore_errors=True)

    @pytest.fixture
    def catalog(self, temp_dir):
        return ConceptCatalog(
            chroma_path=str(temp_dir / "chroma"),
            sqlite_path=str(temp_dir / "concepts.db"),
        )

    def test_deduplication_with_real_embeddings(self, catalog):
        """Labels identicos devem resolver para o mesmo concept_id via similaridade."""
        id1 = catalog.save_concept("cooperacao", "trabalho conjunto")
        id2 = catalog.save_concept("cooperacao", "outra descricao")

        assert id1 == id2

        concept = catalog.get_concept_by_id(id1)
        assert concept.label == "cooperacao"
