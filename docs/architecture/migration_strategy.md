# Estratégia de Migração: Sistema Atual → Super-Sistema

## Visão Geral

Plano de migração incremental do paper-agent atual (entidade `Topic`) para super-sistema (entidades `Idea`, `Concept`, `Argument`).

**Objetivo:** Preparar fundação para múltiplos produtos sem quebrar paper-agent.

---

## Fase 1: Abstrair Fundação

**Objetivo:** Renomear `Topic` → `Idea` e generalizar campos, sem quebrar funcionalidade.

### Tarefas

**1.1 Renomear entidade**
```python
# Antes
class Topic(TypedDict):
    id: str
    title: str
    article_type: str  # específico de artigo
    stage: str         # específico de artigo

# Depois
class Idea(TypedDict):
    id: str
    title: str
    context: dict      # genérico (source_type, source, ...)
    status: str        # genérico (exploring, structured, validated)
```

**1.2 Migração de código**
- Find/replace estruturado: `Topic` → `Idea`
- Atualizar imports
- Manter backward compatibility (aliases temporários)

**1.3 Migração de dados**
```sql
-- Renomear tabela
ALTER TABLE topics RENAME TO ideas;

-- Migrar campos
ALTER TABLE ideas ADD COLUMN context JSON;
UPDATE ideas SET context = json_object(
    'source_type', 'conversation',
    'article_type', article_type
);
ALTER TABLE ideas DROP COLUMN article_type;
```

**1.4 Validação**
- Paper-agent continua funcionando normalmente
- Testes passando
- Nenhuma funcionalidade perdida

### Entrega

✅ Entidade central renomeada (`Idea`)  
✅ Campos generalizados  
✅ Paper-agent funcional  
✅ Fundação pronta para expandir  

---

## Fase 2: Criar Entidade `Concept`

**Objetivo:** Conceitos como entidade de primeira classe com vetores semânticos.

### Tarefas

**2.1 Setup ChromaDB**
```bash
pip install chromadb sentence-transformers
```

**2.2 Schema Concept**
```python
class Concept(TypedDict):
    id: str
    label: str
    semantic_vector: list[float]
    variations: list[str]
    essence: str
```

**2.3 Pipeline de detecção**
```python
def extract_concepts(text: str) -> list[Concept]:
    """Detecta conceitos mencionados em texto"""
    # LLM identifica conceitos-chave
    # Gera embeddings
    # Salva em ChromaDB + SQLite
```

**2.4 Linking Idea ↔ Concept**
```sql
CREATE TABLE idea_concepts (
    idea_id TEXT,
    concept_id TEXT,
    PRIMARY KEY (idea_id, concept_id)
);
```

**2.5 Busca semântica**
```python
def find_similar_concepts(query: str) -> list[Concept]:
    """Busca conceitos similares via embedding"""
    vector = encoder.encode(query)
    results = chroma_collection.query(vector)
    return results
```

### Entrega

✅ Conceitos detectados automaticamente  
✅ Busca semântica funciona  
✅ Ideias referenciam conceitos  
✅ "produtividade" encontra "eficiência"  

---

## Fase 3: Tornar `Argument` Explícito

**Objetivo:** Separar `Argument` de `Idea`, permitir múltiplos argumentos por ideia.

### Tarefas

**3.1 Schema Argument**
```python
class Argument(TypedDict):
    id: str
    idea_id: str  # pertence a qual ideia
    claim: str
    premises: list[str]
    assumptions: list[str]
    evidence: list[dict]
```

**3.2 Migrar cognitive_model**
```python
# Antes: cognitive_model é dict em MultiAgentState
state["cognitive_model"] = {
    "claim": "...",
    "premises": [...]
}

# Depois: argument é entidade persistida
argument = Argument(
    claim=state["cognitive_model"]["claim"],
    premises=state["cognitive_model"]["premises"]
)
db.save_argument(argument)
```

**3.3 Múltiplos argumentos**
```python
# Ideia pode ter múltiplos argumentos
idea.arguments = [arg_id_1, arg_id_2]

# Exemplo: "Semana 4 dias"
arg_1 = Argument(claim="Aumenta produtividade")
arg_2 = Argument(claim="Reduz turnover")
```

### Entrega

✅ Argument é entidade separada  
✅ Ideia pode ter múltiplos argumentos  
✅ Cognitive_model persiste como Argument  

---

## Fase 4: Fichamento Automático

**Objetivo:** Novo produto - processar livros/textos e extrair ideias.

### Tarefas

**4.1 Pipeline de ingestão**
```python
def process_pdf(file_path: str) -> list[Idea]:
    """Extrai texto, chunka, processa com agentes"""
    text = extract_text_from_pdf(file_path)
    chunks = chunk_text(text)
    ideas = []
    for chunk in chunks:
        idea = agents.process_chunk(chunk)
        ideas.append(idea)
    return ideas
```

**4.2 Fichamento base (catálogo)**
```python
class BookFichamento:
    book_id: str
    title: str
    author: str
    ideas: list[str]  # idea_ids
    is_base: bool     # True = catálogo público
```

**4.3 Customização usuário**
```python
class UserFichamento:
    user_id: str
    book_id: str
    base_fichamento_id: str
    customizations: list[dict]  # adições/ajustes
```

**4.4 Sistema aprende**
```python
def learn_from_customizations():
    """Se múltiplos usuários adicionam mesmo aspecto,
       sistema atualiza fichamento base"""
    common_additions = aggregate_customizations()
    if common_additions.confidence > 0.8:
        update_base_fichamento(common_additions)
```

**4.5 Interface de revisão**
- Upload PDF
- Sistema extrai ideias
- Usuário revisa/ajusta
- Salva fichamento

### Entrega

✅ Usuário pode fichar livro (upload PDF)  
✅ Sistema extrai ideias automaticamente  
✅ Catálogo público de fichamentos  
✅ Usuário pode customizar  
✅ Sistema aprende com customizações  

---

## Fase 5: Grafo de Conhecimento

**Objetivo:** Ideias se conectam semanticamente, navegação por grafo.

### Tarefas

**5.1 Modelar relacionamentos**
```python
class IdeaRelation:
    from_idea_id: str
    to_idea_id: str
    relation_type: str  # "supports", "contradicts", "is_example_of"
    confidence: float
```

**5.2 Detecção automática**
```python
def detect_relations(ideas: list[Idea]) -> list[IdeaRelation]:
    """Sistema detecta ideias relacionadas via:
       - Conceitos compartilhados
       - Similaridade semântica
       - Análise LLM"""
    relations = []
    for idea_a in ideas:
        for idea_b in ideas:
            if shares_concepts(idea_a, idea_b):
                relation = analyze_relation(idea_a, idea_b)
                relations.append(relation)
    return relations
```

**5.3 Queries no grafo**
```python
# Quais ideias usam conceito X?
ideas = graph.find_ideas_with_concept("Cooperação")

# Ideias que contradizem ideia Y?
contradictions = graph.find_related(idea_y, "contradicts")

# Livros relacionados a ideia Z?
books = graph.find_books_with_similar_ideas(idea_z)
```

**5.4 Visualização**
- Grafo interativo (D3.js)
- Navegar por conexões
- Filtrar por tipo de relação

### Entrega

✅ Sistema conecta ideias automaticamente  
✅ Queries no grafo funcionam  
✅ Usuário navega por relações  
✅ Base para rede social (futuro)  

---

## Resumo das Fases

| Fase | Objetivo | Afeta Paper-Agent? |
|------|----------|-------------------|
| 1 | Abstrair fundação (Topic → Idea) | Não (transparente) |
| 2 | Criar Concept (vetores semânticos) | Não (nova feature) |
| 3 | Argument explícito (múltiplos por ideia) | Não (melhoria interna) |
| 4 | Fichamento (novo produto) | Não (produto separado) |
| 5 | Grafo de conhecimento | Sim (nova feature visível) |

---

## Validação Incremental

**Após cada fase:**
1. ✅ Testes automatizados passando
2. ✅ Paper-agent funcional
3. ✅ Nenhuma funcionalidade perdida
4. ✅ Novo comportamento validado manualmente
5. ✅ Documentação atualizada

**Rollback fácil:**
- Commits estratégicos por fase
- Branches separados
- Testes de regressão

---

## Priorização

**Fase 1-3: Base técnica** (sem impacto visual no paper-agent)  
**Fase 4: Novo produto** (fichamento)  
**Fase 5: Feature visível** (grafo)  

**Recomendação:** Executar Fases 1-3 sequencialmente antes de Fase 4.

---

## Referências

- `docs/architecture/ontology.md` - Ontologia alvo (Concept, Idea, Argument)
- `docs/architecture/idea_model.md` - Schema Idea
- `docs/architecture/concept_model.md` - Schema Concept
- `docs/architecture/argument_model.md` - Schema Argument
- `docs/architecture/tech_stack.md` - ChromaDB, embeddings

