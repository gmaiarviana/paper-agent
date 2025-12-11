# Idea Model - Estrutura de Dados

> **Nota:** Para entender o que é Ideia filosoficamente, consulte `ontology.md`.
> 
> **⚠️ Migração:** Este documento substitui o antigo `topic_argument_model.md` (obsoleto). A migração de "Topic" para "Idea" está planejada no Épico 11.

## Visão Geral

Ideia é a entidade central do sistema. Representa pensamento articulado que pode evoluir ao longo de conversa ou ser extraído de conteúdo estático (livros).

## Schema de Dados

```python
Idea:
    id: UUID
    title: str                    # "Cooperação via mitos compartilhados"
    concepts: list[UUID]          # referencia Concepts
    arguments: list[UUID]         # possui múltiplos Arguments
    
    # Hierarquia (opcional)
    parent_id: UUID | None        # se é sub-ideia
    children: list[UUID]          # sub-ideias
    
    # Metadados contextuais
    context: dict                 # source_type, source, author, etc
    created_at: datetime
    updated_at: datetime
    
    # Estado (para conversas dinâmicas)
    status: str                   # "exploring" | "structured" | "validated"
```

### Campos Detalhados

**concepts:**
Lista de IDs de conceitos que a ideia referencia (da biblioteca global):

```python
concepts: [
    concept_id_cooperacao,
    concept_id_ficcao,
    concept_id_linguagem
]
```

**arguments:**
Lista de argumentos que defendem/exploram a ideia:

```python
arguments: [
    argument_id_1,  # "Religião permite cooperação"
    argument_id_2   # "Nacionalismo permite cooperação"
]
```

**context:**
Metadados sobre origem/contexto:

```python
context: {
    "source_type": "book" | "conversation" | "article",
    "source": "Sapiens, Capítulo 2",
    "author": "Yuval Noah Harari",
    "language": "pt-BR"
}
```

## Hierarquia de Ideias

### Ideia Macro → Sub-ideias

Livros/textos complexos têm estrutura hierárquica:

```python
# Exemplo: Sapiens
# Ideia macro:
id: idea-001
title: "Revoluções que transformaram Sapiens"
parent_id: None
children: [idea-002, idea-003]

# Sub-ideia 1:
id: idea-002
title: "Revolução Cognitiva"
parent_id: idea-001
children: [idea-004]

# Ideia específica:
id: idea-004
title: "Cooperação via mitos"
parent_id: idea-002
children: []
```

### Quem Define Hierarquia?

**Sistema identifica automaticamente:**
- Processa livro/texto
- Detecta estrutura (capítulos, seções)
- Agrupa ideias relacionadas

**Usuário pode ajustar:**
- Sistema sugere: "Essas 3 ideias parecem relacionadas, quer agrupar?"
- Usuário valida/ajusta hierarquia

## Relacionamentos

### Idea ↔ Concept (N:N)

**Relacionamento é referência, não posse:**
- Ideia referencia múltiplos conceitos da biblioteca global
- Conceitos são globais (biblioteca única)
- Relacionamento N:N via tabela `idea_concepts`

```python
# Biblioteca global de conceitos
concept_cooperacao = {
    "id": "concept-001",
    "label": "Cooperação",
    "variations": ["colaboração", "teamwork"]
}

# Múltiplas ideias referenciam mesmo conceito
idea_1.concepts = ["concept-001"]  # Sapiens
idea_2.concepts = ["concept-001"]  # Clastres
idea_3.concepts = ["concept-001"]  # Putnam

# Ideia referencia múltiplos conceitos
idea.concepts = [concept_id_1, concept_id_2]

# Conceito usado em múltiplas ideias (via referências)
concept.used_in_ideas = [idea_id_1, idea_id_2]
```

### Idea ↔ Argument (1:N)

```python
# Ideia possui múltiplos argumentos
idea.arguments = [arg_id_1, arg_id_2]

# Argumento pertence a uma ideia
argument.idea_id = idea_id
```

### Idea ↔ Idea (Hierarquia)

```python
# Ideia macro
parent.children = [child_id_1, child_id_2]

# Sub-ideia
child.parent_id = parent_id
```

### Idea ↔ Idea (Relações Semânticas)

```python
# Ideias podem se relacionar semanticamente
idea_1 --[supports]--> idea_2
idea_3 --[contradicts]--> idea_4
idea_5 --[is_example_of]--> idea_6
```

> **Nota:** Grafo de relações é feature futura planejada.

## Evolução de Ideia (Conversas Dinâmicas)

Em conversas (paper-agent), ideia evolui:

```python
# Turno 1
idea.status = "exploring"
idea.title = "LLMs aumentam produtividade"  # vago

# Turno 5
idea.status = "structured"
idea.title = "Claude Code reduz tempo de sprint em 30%"  # específico

# Turno 10
idea.status = "validated"
# Metodologista validou, pronta para artigo
```

## Múltiplas Ideias em Uma Conversa

Sistema pode rastrear múltiplas ideias na mesma conversa:

```python
MultiAgentState:
    active_idea_id: UUID        # ideia atual sendo discutida
    ideas: list[UUID]           # todas as ideias da conversa
```

**Fluxo:**
1. Conversa começa → cria idea-001
2. Usuário muda de foco → sistema detecta
3. Sistema oferece: "Criar nova ideia ou continuar?"
4. Usuário decide → sistema cria idea-002 ou continua idea-001

> **Nota:** Detecção de mudança de foco via focal_argument (ver `docs/orchestration/conversational_orchestrator/reasoning.md`).

## Storage

**SQLite (metadados estruturados):**

```sql
CREATE TABLE ideas (
    id TEXT PRIMARY KEY,
    title TEXT,
    parent_id TEXT,
    context JSON,
    status TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE idea_concepts (
    idea_id TEXT,
    concept_id TEXT,  -- FK para tabela concepts (biblioteca global)
    PRIMARY KEY (idea_id, concept_id),
    FOREIGN KEY (concept_id) REFERENCES concepts(id)
);

CREATE TABLE idea_arguments (
    idea_id TEXT,
    argument_id TEXT,
    PRIMARY KEY (idea_id, argument_id)
);
```

## Referências

- `ontology.md` - Definição de Ideia
- `concept_model.md` - Conceitos que Ideia usa
- `argument_model.md` - Argumentos que Ideia possui
- `products/produtor-cientifico/docs/vision.md` - Como Produtor Científico usa Ideias
- `products/prisma-verbal/docs/vision.md` - Como fichamento extrai Ideias

