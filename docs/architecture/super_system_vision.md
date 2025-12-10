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
│  │  (Conceito, Ideia, Argumento,             │  │
│  │   MemoryLayer, BackstageContext)          │  │
│  └──────────────────────────────────────────┘  │
│                                                  │
│  ┌──────────────────────────────────────────┐  │
│  │  Modelo Cognitivo                         │  │
│  │  (claim, fundamentos, ...)                │  │
│  └──────────────────────────────────────────┘  │
│                                                  │
│  ┌──────────────────────────────────────────┐  │
│  │  Agentes                                  │  │
│  │  (Orquestrador, Observador,               │  │
│  │   Memory Agent, Estruturador, ...)        │  │
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

✅ **Ontologia:** Conceito, Ideia, Argumento, MemoryLayer, BackstageContext  
✅ **Modelo Cognitivo:** claim → fundamentos (com solidez variável)  
✅ **Agentes:** Orquestrador, Observador, Estruturador, Metodologista, Memory Agent, Comunicador (futuro)  
✅ **Infraestrutura:** LangGraph (state), ChromaDB (vetores), SQLite (metadados)  
✅ **Conversação:** Diálogo socrático, provocação, refinamento  

### O Que NÃO é Core

Tudo que é **específico de produto**:

❌ `Article` (paper-agent)  
❌ `Book` (fichamento)  
❌ `Profile` (rede social)  
❌ Interfaces específicas (dashboard, feed)  

## Agentes do Core

### Orquestrador (Coordenação Lógica)
Responsável por coordenar o fluxo de trabalho entre agentes, decidindo qual agente deve ser acionado em cada etapa do processo. Gerencia o estado global da execução e garante que as transições entre agentes ocorram de forma coerente.

**Visão futura:** Orquestrador evolui para gerenciar múltiplos produtos simultaneamente, roteando requisições de diferentes serviços para os agentes apropriados do core.

### Observador (Processamento Interno)
Processa e analisa o conteúdo gerado pelos outros agentes, extraindo conceitos, identificando padrões e mantendo a consistência ontológica. Trabalha de forma transparente, sem interação direta com o usuário.

**Visão futura:** Observador se torna o "olho" do core, monitorando qualidade, consistência e evolução do conhecimento em todos os produtos.

### Memory Agent (Memória de Longo Prazo)
Gerencia as camadas de memória (superficial, intermediária, profunda) do sistema. Responsável por armazenar, recuperar e compactar memórias de longo prazo, garantindo escalabilidade temporal e degradação controlada.

**Responsabilidades:**
- Gerenciar snapshots de estado
- Compactação periódica de memórias antigas
- Busca otimizada por camada (recente = rápido, antigo = lento)
- Configuração de memória por produto

### Comunicador (Interface Linguística - Futuro)
Agente responsável por traduzir entre a linguagem natural do usuário e as operações do core. Abstrai a complexidade dos agentes internos, oferecendo uma interface conversacional unificada para todos os produtos.

**Status:** Planejado para futuro, permitirá que produtos diferentes compartilhem a mesma capacidade de diálogo socrático e refinamento.

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

### Configuração de Memory por Produto

Cada produto configura as camadas de memória de acordo com suas necessidades específicas:

#### Paper-Agent: Memory de Sessão
- **Superficial (10 turnos):** Últimas interações da conversa atual, acesso instantâneo
- **Intermediária (snapshots):** Estados importantes da sessão, pontos de decisão, ideias geradas
- **Profunda (50 turnos):** Histórico completo da sessão, contexto de longo prazo para continuidade

**Uso:** Manter contexto conversacional, permitir retomada de sessões, rastrear evolução de ideias.

#### Fichamento: Memory de Documento
- **Superficial (capítulos):** Estrutura do documento, navegação rápida entre seções
- **Intermediária (conceitos):** Conceitos extraídos, relações entre ideias do documento
- **Profunda (citações):** Citações completas, contexto original, referências cruzadas

**Uso:** Catálogo de livros, busca por conceitos, análise comparativa entre documentos.

#### Rede Social: Memory de Perfil
- **Superficial (semana):** Atividades recentes, interações atuais, feed dinâmico
- **Intermediária (evolução):** Mudanças de cosmovisão ao longo do tempo, conexões estabelecidas
- **Profunda (anos arquivados):** Histórico completo de perfil, arquivo de longa duração, análise de tendências

**Uso:** Conexão por cosmovisões, evolução de pensamento, matching baseado em histórico.

### Vantagens do Desacoplamento

✅ **Independência:** Produtos evoluem sem quebrar outros  
✅ **Reuso:** Core evolui, todos produtos se beneficiam  
✅ **Escalabilidade:** Novos produtos consomem core existente  
✅ **Manutenção:** Bugs no core fixados uma vez, todos produtos se beneficiam  
✅ **Escalabilidade da Memory configurável por produto:** Cada produto define suas próprias camadas de memória (superficial, intermediária, profunda) de acordo com suas necessidades específicas  
✅ **Bastidores transparentes como diferencial:** O BackstageContext permite que produtos exponham (ou ocultem) o processo interno de geração de conhecimento, oferecendo transparência como feature

## Escalabilidade da Memory

A arquitetura de memória em camadas permite escalabilidade temporal através de degradação controlada e compactação periódica.

### Degradação Temporal

Memórias mais recentes são acessadas mais rapidamente, enquanto memórias antigas podem ter latência maior:

```python
# Exemplo de tempos de busca por camada
def search_memory(query: str, product: str) -> dict:
    """
    Busca em memória com degradação temporal.
    Retorna resultados ordenados por relevância e velocidade de acesso.
    """
    results = {
        "superficial": {
            "data": search_superficial(query, product),
            "latency_ms": 10,  # Acesso instantâneo
            "scope": "últimos 10 turnos/capítulos/semana"
        },
        "intermediaria": {
            "data": search_intermediaria(query, product),
            "latency_ms": 50,  # Acesso rápido
            "scope": "snapshots/conceitos/evolução"
        },
        "profunda": {
            "data": search_profunda(query, product),
            "latency_ms": 200,  # Acesso mais lento
            "scope": "50 turnos/citações/anos arquivados"
        }
    }
    return results
```

**Estratégia:** Busca começa pela camada superficial e expande para camadas mais profundas apenas quando necessário, otimizando performance.

### Compactação Periódica

Memórias antigas são compactadas para reduzir custo de armazenamento e manter performance:

- **Compactação mensal:** Memórias intermediárias de mais de 30 dias são comprimidas
- **Compactação anual:** Memórias profundas de mais de 1 ano são arquivadas em formato otimizado
- **Recuperação sob demanda:** Memórias compactadas podem ser restauradas quando necessário, com latência maior

**Benefício:** Sistema mantém performance constante mesmo com crescimento exponencial de dados históricos.

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

**Memória:**
```
GET    /memory/search      # Buscar em memória (com degradação temporal)
GET    /memory/layers      # Obter configuração de camadas por produto
POST   /memory/compact     # Compactar memórias antigas (admin)
```

## Referências

- `docs/architecture/ontology.md` - Ontologia base (Core)
- `docs/products/paper_agent.md` - Produto específico
- `docs/products/fichamento.md` - Produto específico
- `docs/vision/epistemology.md` - Epistemologia do sistema (fundamentos com solidez)
- `ROADMAP.md` - Épicos 11+ (migração)

