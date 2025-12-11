# Concept Model - Estrutura de Dados

> **Nota:** Para entender o que é Conceito filosoficamente, consulte `ontology.md`.

## Visão Geral

Conceito é entidade de primeira classe com vetor semântico para busca por similaridade.

## Conceitos como Biblioteca Global

**Decisão do Épico 13:** Conceitos existem como biblioteca única e compartilhada, independentemente de ideias.

### Princípios Fundamentais

1. **Independência de Ideias**
   - Conceitos não pertencem a ideias específicas
   - Sistema mantém biblioteca global única de conceitos
   - Conceitos são reutilizáveis entre múltiplas ideias

2. **Modelo de Referência (N:N)**
   - Ideias referenciam conceitos (não possuem)
   - Um conceito pode aparecer em múltiplas ideias
   - Uma ideia pode usar múltiplos conceitos

3. **Deduplicação Automática**
   - Sistema evita criar conceitos duplicados
   - Busca por similaridade semântica antes de criar novo conceito
   - Threshold de similaridade determina ação (criar novo vs. adicionar variação)

**Exemplo:**
```python
# Biblioteca global de conceitos
concepts_library = {
    "cooperacao": Concept(
        id="uuid-1",
        label="Cooperação",
        variations=["colaboração", "trabalho em conjunto"]
    )
}

# Ideias referenciam conceitos
idea_1.concepts = ["uuid-1"]  # usa "Cooperação"
idea_2.concepts = ["uuid-1"]  # também usa "Cooperação"
# Mesmo conceito, ideias diferentes
```

## Schema de Dados

```python
Concept:
    id: UUID
    label: str                    # "Cooperação"
    semantic_vector: list[float]  # embedding (384 dimensões)
    variations: list[str]         # variações linguísticas
    essence: str                  # descrição da essência
    contexts: list[dict]          # contextos de uso com nuances
```

### Campos Detalhados

**semantic_vector:**
- Embedding gerado via sentence-transformers (all-MiniLM-L6-v2)
- 384 dimensões (modelo local, gratuito)
- Representa essência semântica do conceito

**variations:**
Lista de formas linguísticas que expressam mesma essência:

```python
variations: [
    "cooperação",
    "colaboração",
    "trabalho em conjunto",
    "coordination" (inglês),
    "coopération" (francês)
]
```

**contexts:**
Nuances do conceito em diferentes contextos:

```python
contexts: [
    {context: "biologia", nuance: "altruísmo evolutivo"},
    {context: "economia", nuance: "teoria dos jogos"},
    {context: "sociologia", nuance: "ação coletiva"}
]
```

## Detecção de Similaridade

### Como Sistema Identifica Conceitos Similares

**Processo:**
1. Usuário menciona "trabalho em conjunto"
2. Sistema gera embedding do input
3. Calcula similaridade cosseno com conceitos existentes
4. Se similaridade > 0.80 → mesmo conceito

**Exemplo:**

```python
# Input
input_text = "trabalho em conjunto"
input_vector = encoder.encode(input_text)

# Comparação
concept_cooperacao.semantic_vector = [0.23, 0.87, ...]
similarity = cosine_similarity(input_vector, concept_cooperacao.vector)
# similarity = 0.94 → reconhece como "Cooperação"
```

## Criação de Conceitos

**Abordagem Híbrida (Épico 13):** Sistema combina detecção automática com validação do usuário, com evolução planejada para extração de múltiplas fontes.

### Fase Atual (POC/MVP)

**Fluxo:**
1. Usuário menciona conceito na conversa (ex: "cooperação")
2. Sistema detecta via LLM (extração de conceitos-chave)
3. Sistema gera embedding do conceito detectado
4. Sistema busca conceitos similares na biblioteca global
5. Com base no threshold de similaridade:
   - **> 0.90**: Adiciona automaticamente como variação
   - **0.80-0.90**: Pergunta ao usuário se é o mesmo conceito
   - **< 0.80**: Cria novo conceito na biblioteca

**Exemplo:**
```python
# Usuário menciona: "trabalho colaborativo"
detected_concept = "trabalho colaborativo"
embedding = encoder.encode(detected_concept)

# Busca similar
similar_concepts = find_similar_concepts(detected_concept, top_k=1)
similarity = similar_concepts[0].similarity  # 0.87

if similarity > 0.90:
    # Automático: adiciona como variação
    concept.add_variation("trabalho colaborativo")
elif similarity >= 0.80:
    # Pergunta ao usuário
    user_response = ask_user("É o mesmo que 'Cooperação'?")
    if user_response:
        concept.add_variation("trabalho colaborativo")
    else:
        create_new_concept("trabalho colaborativo")
else:
    # Cria novo conceito
    create_new_concept("trabalho colaborativo")
```

### Fase Futura (Roadmap)

**Extração de Múltiplas Fontes:**
- Extrair conceitos de livros (fichamento)
- Extrair conceitos de papers acadêmicos
- Extrair conceitos de conteúdo da internet
- Processamento em lote de documentos

**Deduplicação Avançada:**
- Threshold > 0.90: fusão automática (sem perguntar)
- Threshold 0.80-0.90: validação do usuário
- Threshold < 0.80: conceito novo

**Exemplo Futuro:**
```python
# Processar livro completo
book_concepts = extract_concepts_from_book("Sapiens.pdf")

for concept_text in book_concepts:
    embedding = encoder.encode(concept_text)
    similar = find_similar_concepts(concept_text)
    
    if similar.similarity > 0.90:
        # Automático: adiciona variação
        existing_concept.add_variation(concept_text)
    elif similar.similarity >= 0.80:
        # Batch: adiciona à fila de validação
        validation_queue.append((concept_text, similar))
    else:
        # Novo conceito
        create_new_concept(concept_text)
```

## Pipeline de Detecção (Épico 13)

**Decisão do Épico 13:** Pipeline de detecção de conceitos é acionado quando um snapshot de Idea é criado, não a cada mensagem do usuário.

### Quando Disparar

**Trigger:** Criação de snapshot de Idea
- Sistema cria snapshot quando Idea atinge maturidade suficiente
- Pipeline roda automaticamente após snapshot ser persistido
- Evita processamento excessivo (não roda a cada mensagem)

**Fluxo Completo:**

```python
# 1. Snapshot de Idea é criado
idea_snapshot = create_idea_snapshot(idea_id)

# 2. Pipeline de detecção é acionado
def detect_concepts_pipeline(idea_snapshot):
    # 2.1. LLM extrai conceitos-chave
    concepts_text = llm_extract_concepts(idea_snapshot.content)
    # Exemplo: ["cooperação", "produtividade", "eficiência"]
    
    # 2.2. Para cada conceito detectado
    for concept_text in concepts_text:
        # 2.3. Gera embedding
        embedding = encoder.encode(concept_text)
        
        # 2.4. Busca similares na biblioteca global
        similar = find_similar_concepts(concept_text, top_k=1)
        
        # 2.5. Decide ação baseado em threshold
        if similar and similar.similarity > 0.90:
            # Adiciona variação ao conceito existente
            existing_concept = get_concept(similar.id)
            existing_concept.add_variation(concept_text)
            concept_id = existing_concept.id
        elif similar and similar.similarity >= 0.80:
            # Pergunta ao usuário (ou adiciona à fila)
            concept_id = handle_user_validation(concept_text, similar)
        else:
            # Cria novo conceito
            new_concept = create_concept(
                label=concept_text,
                embedding=embedding
            )
            concept_id = new_concept.id
        
        # 2.6. Salva no ChromaDB (vetor)
        chroma_id = save_to_chromadb(concept_id, embedding)
        
        # 2.7. Salva no SQLite (metadados)
        save_to_sqlite(concept_id, chroma_id, concept_text)
        
        # 2.8. Cria link Idea ↔ Concept
        link_idea_concept(idea_snapshot.idea_id, concept_id)
```

### Componentes do Pipeline

1. **Extração via LLM**
   - Prompt: "Extrair conceitos-chave desta ideia"
   - Retorna lista de strings (nomes de conceitos)

2. **Geração de Embeddings**
   - Modelo: `all-MiniLM-L6-v2` (sentence-transformers)
   - Dimensões: 384
   - Performance: ~50ms por conceito

3. **Busca Semântica**
   - ChromaDB query com top_k=1
   - Similaridade cosseno
   - Threshold: 0.80 (mesmo conceito), 0.90 (automático)

4. **Persistência Dupla**
   - ChromaDB: vetor semântico
   - SQLite: metadados (label, essence, variations, chroma_id)

5. **Linking**
   - Tabela `idea_concepts`: relacionamento N:N
   - Vincula Idea ao Concept detectado

## Relacionamentos

### Concept ↔ Idea (N:N)

```python
# Uma ideia usa múltiplos conceitos
idea.concepts = [concept_id_1, concept_id_2, ...]

# Um conceito aparece em múltiplas ideias
concept.used_in_ideas = [idea_id_1, idea_id_2, ...]
```

## Implementação Técnica

> **Nota:** Para detalhes de stack técnico (ChromaDB, embeddings), consulte `../infrastructure/tech_stack.md`.

## Storage

**Arquitetura Híbrida (Épico 13):** Sistema usa ChromaDB para vetores semânticos e SQLite para metadados estruturados, com referência cruzada via `chroma_id`.

### ChromaDB (Vetores Semânticos)

**Collection:** `concepts`

**Estrutura:**
- **ids**: UUID do conceito (mesmo ID do SQLite)
- **embeddings**: Vetor semântico (384 dimensões)
- **metadatas**: Label, essence, variations (JSON)

**Exemplo de Código:**
```python
import chromadb

# Cliente persistente
client = chromadb.PersistentClient(path="./data/chroma")
collection = client.get_or_create_collection("concepts")

# Adicionar conceito
collection.add(
    ids=["concept-uuid-123"],
    embeddings=[[0.23, 0.87, 0.45, ...]],  # 384 dims
    metadatas=[{
        "label": "Cooperação",
        "essence": "Ação coordenada entre agentes",
        "variations": '["colaboração", "trabalho em conjunto"]'
    }]
)

# Buscar similar
results = collection.query(
    query_embeddings=[query_vector],
    n_results=5,
    include=["metadatas", "distances"]
)
```

**Storage:**
- Local: `./data/chroma/` (arquivo único)
- Tamanho: ~10MB para 500 conceitos
- Backup: copiar diretório completo

### SQLite (Metadados Estruturados)

**Tabela:** `concepts`

**Schema:**
```sql
CREATE TABLE concepts (
    id TEXT PRIMARY KEY,           -- UUID do conceito
    label TEXT NOT NULL,           -- "Cooperação"
    essence TEXT,                  -- Descrição da essência
    variations JSON,               -- ["colaboração", "trabalho em conjunto"]
    chroma_id TEXT,                -- Referência ao registro no ChromaDB
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE idea_concepts (
    idea_id TEXT NOT NULL,
    concept_id TEXT NOT NULL,
    PRIMARY KEY (idea_id, concept_id),
    FOREIGN KEY (concept_id) REFERENCES concepts(id)
);

CREATE INDEX idx_concepts_label ON concepts(label);
CREATE INDEX idx_idea_concepts_idea ON idea_concepts(idea_id);
CREATE INDEX idx_idea_concepts_concept ON idea_concepts(concept_id);
```

**Campo `chroma_id`:**
- Referencia o registro correspondente no ChromaDB
- Permite sincronização entre SQLite e ChromaDB
- Usado para atualizar/remover vetores quando metadados mudam

**Exemplo de Código:**
```python
# Salvar conceito (dupla persistência)
def save_concept(concept):
    # 1. Salvar no ChromaDB (vetor)
    chroma_id = collection.add(
        ids=[concept.id],
        embeddings=[concept.embedding],
        metadatas=[{
            "label": concept.label,
            "essence": concept.essence,
            "variations": json.dumps(concept.variations)
        }]
    )
    
    # 2. Salvar no SQLite (metadados)
    db.execute("""
        INSERT INTO concepts (id, label, essence, variations, chroma_id)
        VALUES (?, ?, ?, ?, ?)
    """, (concept.id, concept.label, concept.essence, 
          json.dumps(concept.variations), chroma_id))
```

**Storage:**
- Local: `./data/data.db` (mesmo arquivo das ideias)
- Tamanho: ~5MB para 500 conceitos
- Backup: copiar arquivo SQLite

### Busca Semântica

**Função Principal:**
```python
from sentence_transformers import SentenceTransformer
import chromadb

encoder = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.PersistentClient(path="./data/chroma")
collection = client.get_collection("concepts")

def find_similar_concepts(query_text, top_k=5, threshold=0.80):
    """
    Busca conceitos similares na biblioteca global.
    
    Args:
        query_text: Texto do conceito a buscar
        top_k: Número de resultados
        threshold: Similaridade mínima (0.80 = mesmo conceito)
    
    Returns:
        Lista de conceitos similares com similarity score
    """
    # Gerar embedding da query
    query_vector = encoder.encode(query_text).tolist()
    
    # Buscar no ChromaDB
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=top_k,
        include=["metadatas", "distances"]
    )
    
    # Converter distância para similaridade
    similar_concepts = []
    for i, concept_id in enumerate(results['ids'][0]):
        distance = results['distances'][0][i]
        similarity = 1 - distance  # ChromaDB retorna distância, converter para similaridade
        
        if similarity >= threshold:
            # Buscar metadados completos no SQLite
            concept_metadata = db.get_concept_by_id(concept_id)
            similar_concepts.append({
                "id": concept_id,
                "similarity": similarity,
                "label": concept_metadata["label"],
                "essence": concept_metadata["essence"]
            })
    
    return similar_concepts
```

**Performance:**
- Geração de embedding: ~50ms
- Busca no ChromaDB: ~100-500ms (500 conceitos)
- Total: <1s (aceitável para UX)

## Referências

- `ontology.md` - Definição filosófica de Conceito
- `idea_model.md` - Como Ideias referenciam Conceitos
- `../infrastructure/tech_stack.md` - ChromaDB e sentence-transformers

