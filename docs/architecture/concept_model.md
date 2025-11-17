# Concept Model - Estrutura de Dados

> **Nota:** Para entender o que é Conceito filosoficamente, consulte `docs/architecture/ontology.md`.

## Visão Geral

Conceito é entidade de primeira classe com vetor semântico para busca por similaridade.

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

### Automática (Sistema)
Durante conversas ou fichamento, sistema detecta conceitos mencionados e cria automaticamente.

### Validada por Usuário
Sistema sugere: "Você mencionou 'ganho de tempo'. Isso é o mesmo que 'produtividade'?"
Usuário confirma → sistema registra variação.

### Híbrido
Sistema sugere via embedding + usuário valida/ajusta.

## Relacionamentos

### Concept ↔ Idea (N:N)

```python
# Uma ideia usa múltiplos conceitos
idea.concepts = [concept_id_1, concept_id_2, ...]

# Um conceito aparece em múltiplas ideias
concept.used_in_ideas = [idea_id_1, idea_id_2, ...]
```

## Implementação Técnica

> **Nota:** Para detalhes de stack técnico (ChromaDB, embeddings), consulte `docs/architecture/tech_stack.md`.

**Storage:**
- Metadados estruturados: SQLite
- Vetores semânticos: ChromaDB

**Busca:**

```python
def find_similar_concepts(query_text, top_k=5):
    query_vector = encoder.encode(query_text)
    results = chroma_collection.query(
        query_embeddings=[query_vector],
        n_results=top_k
    )
    return results
```

## Referências

- `docs/architecture/ontology.md` - Definição filosófica de Conceito
- `docs/architecture/idea_model.md` - Como Ideias referenciam Conceitos
- `docs/architecture/tech_stack.md` - ChromaDB e sentence-transformers

