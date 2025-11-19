# Stack Técnico

## Visão Geral

Stack híbrido para rodar **local** com migração suave para **cloud** (6 meses).

**Princípios:**
- ✅ Gratuito e local (prioritário)
- ✅ Simples de configurar
- ✅ Fácil de manter
- ✅ Migração cloud sem refatorar código

## Componentes

### ChromaDB (Vetores Semânticos)

**O que é:** Banco de dados vetorial local para embeddings e busca por similaridade.

**Por que ChromaDB:**
- Gratuito e open source
- Roda local (arquivo único)
- Setup zero: `pip install chromadb`
- API simples (10 linhas de código)
- Migração fácil para Qdrant Cloud depois

**Uso no sistema:**
- Armazena conceitos (vetores semânticos)
- Busca por similaridade (conceitos relacionados)
- Performance: <500ms para 500 conceitos

**Setup:**
```bash
pip install chromadb
```

**Código básico:**
```python
import chromadb

# Cliente persistente (salva em disco)
client = chromadb.PersistentClient(path="./data/chroma")
collection = client.get_or_create_collection("concepts")

# Adicionar conceito
collection.add(
    ids=["concept-cooperacao"],
    embeddings=[vector],  # list[float]
    metadatas=[{"label": "Cooperação", "essence": "..."}]
)

# Buscar similar
results = collection.query(
    query_embeddings=[query_vector],
    n_results=5
)
```

**Storage:**
- Local: `./data/chroma/` (arquivo único)
- Tamanho: ~10MB para 500 conceitos
- Backup: copiar diretório

---

### SQLite (Dados Estruturados)

**O que é:** Banco relacional local para metadados e relacionamentos.

**Por que SQLite:**
- Já usado pelo LangGraph (checkpointer)
- Gratuito, local, zero configuração
- SQL familiar
- Migração trivial para PostgreSQL

**Uso no sistema:**
- Metadados de Ideias, Argumentos
- Relacionamentos (Ideia ↔ Conceitos)
- Sessões LangGraph (checkpointer)

**Schema principal:**
```sql
CREATE TABLE ideas (
    id TEXT PRIMARY KEY,
    title TEXT,
    parent_id TEXT,
    context JSON,
    status TEXT,
    created_at TIMESTAMP
);

CREATE TABLE concepts (
    id TEXT PRIMARY KEY,
    label TEXT,
    essence TEXT,
    variations JSON,
    chroma_id TEXT  -- link para ChromaDB
);

CREATE TABLE idea_concepts (
    idea_id TEXT,
    concept_id TEXT,
    PRIMARY KEY (idea_id, concept_id)
);
```

**Storage:**
- Local: `./data/sqlite/paper_agent.db`
- Tamanho: ~5MB para 50 ideias
- Backup: copiar arquivo

---

### Sentence-Transformers (Embeddings Locais)

**O que é:** Biblioteca para gerar embeddings localmente (sem API).

**Por que sentence-transformers:**
- Gratuito (roda offline)
- Modelo pequeno: 80MB download
- Performance: <100ms por embedding
- Qualidade boa para similaridade semântica

**Modelo recomendado:**
```python
from sentence_transformers import SentenceTransformer

encoder = SentenceTransformer('all-MiniLM-L6-v2')
# Dimensões: 384
# Download: 80MB (uma vez)
```

**Uso no sistema:**
```python
# Gerar embedding de conceito
text = "Cooperação. Ação coordenada. colaboração, teamwork"
embedding = encoder.encode(text).tolist()

# Embedding vai para ChromaDB
collection.add(
    ids=["concept-cooperacao"],
    embeddings=[embedding]
)
```

**Performance:**
- Geração: ~50ms por conceito
- Busca (ChromaDB): ~100-500ms (500 conceitos)
- Total: <1s (aceitável)

---

### LangGraph (Orquestração)

**O que é:** Framework para sistemas multi-agente com state management.

**Uso no sistema:**
- Orquestração de agentes
- State management (MultiAgentState)
- Checkpointer (persistência de sessões via SQLite)

> **Nota:** Arquitetura multi-agente detalhada em `docs/orchestration/multi_agent_architecture.md`.

---

## Camada de Abstração (Facilita Migração)

**Princípio:** Isolar implementação técnica do código dos agentes.

```python
# Abstração
class ConceptStore:
    def add_concept(self, concept: Concept):
        """Adiciona conceito ao storage"""
        pass
    
    def find_similar(self, query: str, top_k: int) -> list[Concept]:
        """Busca conceitos similares"""
        pass

# Implementação atual (ChromaDB)
class ChromaConceptStore(ConceptStore):
    def __init__(self):
        self.client = chromadb.PersistentClient(...)
        self.encoder = SentenceTransformer(...)
    
    def add_concept(self, concept):
        embedding = self.encoder.encode(concept.text)
        self.client.add(...)

# Implementação futura (Qdrant Cloud)
class QdrantConceptStore(ConceptStore):
    def __init__(self):
        self.client = qdrant_client.QdrantClient(...)
    
    def add_concept(self, concept):
        # Mesmo método, implementação diferente
```

**Vantagem:** Trocar ChromaDB → Qdrant sem refatorar agentes.

---

## Migração Cloud (6 meses)

### Local → Cloud

**ChromaDB → Qdrant Cloud:**
```python
# Configuração muda, API similar
from qdrant_client import QdrantClient

client = QdrantClient(
    url="https://xyz.qdrant.cloud",
    api_key=os.getenv("QDRANT_API_KEY")
)

# Resto do código igual (graças à abstração)
```

**SQLite → PostgreSQL (Supabase):**
```python
# Migração automática via ferramentas
pgloader sqlite://./data/sqlite/paper_agent.db \
         postgresql://user:pass@supabase.com/db

# ORMs (SQLAlchemy) já suportam ambos
engine = create_engine("postgresql://...")
```

**Sentence-transformers → API (opcional):**
```python
# Se quiser usar embeddings via API
from anthropic import Anthropic

client = Anthropic()
embedding = client.embeddings.create(
    model="voyage-2",
    input="texto..."
)
```

### Custos Cloud (Estimados)

**6 meses (500 conceitos, 50 ideias, 100 sessões):**
```
Qdrant Cloud:
  - Free tier: até 1M vetores (suficiente)
  - Custo: $0/mês

PostgreSQL (Supabase):
  - Free tier: 500MB (suficiente)
  - Custo: $0/mês

Embeddings:
  - Continuar local: $0/mês
  - OU usar API: ~$1-5/mês (low volume)

Total: $0-5/mês
```

### Setup Migração (~2-3h)

1. Criar conta Qdrant Cloud (15min)
2. Criar projeto Supabase (15min)
3. Migrar dados (1h - scripts automatizados)
4. Testar (30-60min)

---

## Volumes Esperados (6 meses)
```
Ideias: ~50
Conceitos: ~500
Conversas: ~100
Argumentos: ~100

Storage total: ~15MB local
```

**ChromaDB aguenta milhões de vetores** - volume atual é pequeno.

---

## Setup Local (30 minutos)

### Passo 1: Instalar dependências
```bash
pip install chromadb sentence-transformers
```

### Passo 2: Estrutura de diretórios
```bash
mkdir -p data/chroma data/sqlite
```

### Passo 3: Código básico (já incluído acima)

### Passo 4: Testar
```bash
python scripts/test_stack.py
# Cria conceitos, testa busca, valida storage
```

---

## Referências

- `docs/architecture/concept_model.md` - Como conceitos usam ChromaDB
- ChromaDB docs: https://docs.trychroma.com
- Sentence-transformers: https://www.sbert.net

