# Super-Sistema: Core Universal → Múltiplos Produtos

## Visão Geral

O sistema não é apenas "paper-agent". É um **super-sistema** com core universal que serve múltiplos produtos desacoplados via APIs.

**Produtos atuais/futuros:**
- **Paper-agent:** Auxílio em produção científica (atual)
- **Fichamento:** Catálogo de livros/textos (futuro próximo)
- **Rede Social:** Conexão por cosmovisões (futuro distante)

## Arquitetura: Core → Products

```
┌─────────────────────────────────────────────────┐
│              CORE UNIVERSAL                      │
│                                                  │
│  ┌──────────────────────────────────────────┐  │
│  │  Ontologia Base                           │  │
│  │  (Conceito, Ideia, Argumento)             │  │
│  └──────────────────────────────────────────┘  │
│                                                  │
│  ┌──────────────────────────────────────────┐  │
│  │  Modelo Cognitivo                         │  │
│  │  (claim, fundamentos, ...)                │  │
│  └──────────────────────────────────────────┘  │
│                                                  │
│  ┌──────────────────────────────────────────┐  │
│  │  Agentes                                  │  │
│  │  (Orquestrador, Estruturador, ...)        │  │
│  └──────────────────────────────────────────┘  │
│                                                  │
│  ┌──────────────────────────────────────────┐  │
│  │  Infraestrutura                           │  │
│  │  (LangGraph, ChromaDB, SQLite)            │  │
│  └──────────────────────────────────────────┘  │
│                                                  │
│  ┌──────────────────────────────────────────┐  │
│  │  APIs                                     │  │
│  │  (REST/GraphQL para produtos externos)    │  │
│  └──────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
                      ↓
        ┌─────────────┴─────────────┬──────────────┐
        ↓                           ↓              ↓
┌──────────────────┐    ┌──────────────────┐   ┌─────────────┐
│  PAPER-AGENT     │    │  FICHAMENTO      │   │ REDE SOCIAL │
│  (Serviço)       │    │  (Serviço)       │   │ (Futuro)    │
│                  │    │                  │   │             │
│  Entidades:      │    │  Entidades:      │   │ Entidades:  │
│  - Article       │    │  - Book          │   │ - Profile   │
│  - Section       │    │  - Chapter       │   │ - Connection│
│                  │    │                  │   │             │
│  Interface:      │    │  Interface:      │   │ Interface:  │
│  - Web Chat      │    │  - Upload PDF    │   │ - Feed      │
│  - Dashboard     │    │  - Review        │   │ - Match     │
└──────────────────┘    └──────────────────┘   └─────────────┘
```

## Core Universal (Compartilhado)

### O Que é Core

Tudo que é **independente de produto específico**:

✅ **Ontologia:** Conceito, Ideia, Argumento  
✅ **Modelo Cognitivo:** claim → fundamentos (com solidez variável)  
✅ **Agentes:** Orquestrador, Estruturador, Metodologista, Pesquisador  
✅ **Infraestrutura:** LangGraph (state), ChromaDB (vetores), SQLite (metadados)  
✅ **Conversação:** Diálogo socrático, provocação, refinamento  

### O Que NÃO é Core

Tudo que é **específico de produto**:

❌ `Article` (paper-agent)  
❌ `Book` (fichamento)  
❌ `Profile` (rede social)  
❌ Interfaces específicas (dashboard, feed)  

## Produtos como Serviços Desacoplados

### Produtos Consomem Core via API

**Exemplo: Paper-Agent**
```python
# Paper-agent chama core via API
response = core_api.create_idea(
    title="LLMs aumentam produtividade",
    context={"source_type": "conversation"}
)

idea_id = response.idea_id

# Paper-agent agrega ideias em Article
article = Article(
    title="Impacto de LLMs",
    ideas=[idea_id]
)
```

**Exemplo: Fichamento**
```python
# Fichamento processa livro via core
response = core_api.process_text(
    text=pdf_content,
    context={"source_type": "book", "source": "Sapiens"}
)

# Core retorna ideias extraídas
ideas = response.ideas
```

### Vantagens do Desacoplamento

✅ **Independência:** Produtos evoluem sem quebrar outros  
✅ **Reuso:** Core evolui, todos produtos se beneficiam  
✅ **Escalabilidade:** Novos produtos consomem core existente  
✅ **Manutenção:** Bugs no core fixados uma vez, todos produtos se beneficiam  

## Migração: Sistema Atual → Super-Sistema

Sistema migrou de entidade `Topic` para ontologia completa (`Idea`, `Concept`, `Argument`). Fundação técnica já implementada (Idea e Argument como entidades separadas). Próximos passos: Concept (Épico 13) e produtos futuros (Fichamento, Grafo de Conhecimento).

## APIs do Core (Futuro)

### Endpoints Planejados

**Ideias:**
```
POST   /ideas              # Criar nova ideia
GET    /ideas/:id          # Obter ideia
PATCH  /ideas/:id          # Atualizar ideia
GET    /ideas/search       # Buscar ideias por conceito/título
```

**Conceitos:**
```
POST   /concepts           # Criar conceito
GET    /concepts/:id       # Obter conceito
GET    /concepts/similar   # Buscar conceitos similares
```

**Argumentos:**
```
POST   /arguments          # Criar argumento
GET    /arguments/:id      # Obter argumento
PATCH  /arguments/:id      # Atualizar (refinar)
```

**Conversação:**
```
POST   /conversations      # Iniciar conversa
POST   /conversations/:id/messages  # Enviar mensagem
GET    /conversations/:id/ideas     # Ideias geradas na conversa
```

## Referências

- `docs/architecture/ontology.md` - Ontologia base (Core)
- `docs/products/paper_agent.md` - Produto específico
- `docs/products/fichamento.md` - Produto específico
- `docs/vision/epistemology.md` - Epistemologia do sistema (fundamentos com solidez)
- `ROADMAP.md` - Épicos 11+ (migração)

