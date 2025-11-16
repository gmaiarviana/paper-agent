# Modelo Tópico ↔ Argumento Focal

## Visão Geral

O sistema Paper Agent trabalha com duas entidades fundamentais que representam diferentes dimensões do pensamento científico:

- **Tópico**: Consolidação do pensamento (conceitual)
  - Representa "sobre o que estou pensando" de forma estável
  - Exemplo: "Drones em obras"
  - Persiste como snapshot consolidado de uma linha de investigação

- **Argumento Focal**: Evolução dentro da conversa (temporal)
  - Representa "o que estou dizendo agora" em um momento específico
  - Exemplo: "IA ajuda" → "Regulamentação impede" → "Custo-benefício viável"
  - Evolui dinamicamente durante a conversa
  - Um tópico pode ter múltiplos argumentos ao longo do tempo

## Diferença Conceitual

### Tópico: "Sobre o que estou pensando"

O **Tópico** é uma entidade conceitual que consolida uma linha de investigação científica. Ele representa o domínio de conhecimento sobre o qual o pesquisador está trabalhando, independentemente de como o argumento evolui dentro da conversa.

**Características:**
- Estável e persistente
- Identificado por título e tipo de artigo
- Pode ter múltiplos argumentos ao longo do tempo
- Serve como contêiner de contexto para agentes

**Exemplo:**
```
Tópico: "Drones em levantamento de obra"
- Tipo: "empirical"
- Estágio: "hypothesis"
- Criado em: 2025-01-15
```

### Argumento Focal: "O que estou dizendo agora"

O **Argumento Focal** (representado pelo campo `focal_argument` no `MultiAgentState`) é uma entidade temporal que captura o entendimento atual do sistema sobre o que o usuário quer fazer **neste momento específico** da conversa.

**Características:**
- Evolui dinamicamente a cada turno
- Extraído/atualizado pelo Orquestrador
- Pode mudar radicalmente durante a conversa
- Representa a direção atual do pensamento

**Estrutura:**
```python
focal_argument: {
    "intent": "test_hypothesis" | "review_literature" | "build_theory" | "explore" | "unclear",
    "subject": str,          # Tópico principal
    "population": str,       # População-alvo (ou "not specified")
    "metrics": str,          # Métricas mencionadas (ou "not specified")
    "article_type": str      # Tipo inferido: "empirical" | "review" | "theoretical" | etc.
}
```

**Exemplo de evolução:**
```
Turno 1: "IA ajuda levantamento"
  → focal_argument: { intent: "explore", subject: "IA in construction", ... }

Turno 2: "Regulamentação impede"
  → focal_argument: { intent: "explore", subject: "Regulation barriers", ... }

Turno 3: "Custo-benefício viável"
  → focal_argument: { intent: "test_hypothesis", subject: "Cost-benefit analysis", ... }
```

**Observação:** Todos esses argumentos podem pertencer ao mesmo **Tópico** ("Drones em obras"), mas representam diferentes direções de pensamento ao longo do tempo.

## Relação Entre Entidades

### Modelo de Relacionamento

**Opção escolhida:** Tópico e Argumento Focal (CognitiveModel) são entidades relacionadas (1:N)

- Um **Tópico** pode ter múltiplos **Argumentos Focais** ao longo do tempo
- Cada **Argumento Focal** pertence a um único **Tópico**
- O **Tópico** é um snapshot/consolidação de um argumento maduro
- O **Argumento Focal** atual vive em memória durante a conversa

### Casos de Uso de Busca

O usuário pode buscar conversas de diferentes formas:

1. **Busca temporal (thread_id)**
   - Recupera conversa específica pelo identificador do LangGraph
   - Restaura estado completo incluindo `focal_argument` do checkpoint

2. **Busca conceitual (título, stage)**
   - Lista tópicos por título ou estágio de maturidade
   - Permite navegar entre diferentes linhas de investigação

3. **Retomar tópico com novo argumento**
   - Usuário retoma um tópico existente
   - Sistema cria novo argumento focal (nova versão)
   - Histórico de argumentos anteriores preservado

## Estrutura de Dados

### POC (em memória) - Épico 10

Estado atual do sistema: apenas `CognitiveModel` (argumento focal) em memória, sem persistência de tópicos.

```python
MultiAgentState:
  messages: []
  cognitive_model: CognitiveModel  # argumento focal atual
  # sem persistência ainda
```

**Características:**
- `focal_argument` extraído/atualizado pelo Orquestrador a cada turno
- Estado persiste apenas durante execução do grafo
- Checkpoint LangGraph salva estado completo (incluindo `focal_argument`)
- Sem entidade `Topic` ainda

### Protótipo (persistência básica) - Épico 11

Persistência do `CognitiveModel` (argumento focal) via checkpoint do LangGraph.

```python
# LangGraph checkpoint salva cognitive_model
# SqliteSaver já salva thread_id (já temos!)
# Pausar/retomar preserva modelo
```

**Características:**
- `focal_argument` serializado no checkpoint LangGraph
- `thread_id` já persistido via SqliteSaver (Épico 9)
- Pausar/retomar preserva argumento focal completo
- Ainda sem entidade `Topic` explícita

### MVP (múltiplos tópicos) - Épico 12

Entidade `Topic` explícita com gestão de múltiplos tópicos e histórico de argumentos.

```python
Topic:
  id: UUID
  title: "Drones em levantamento de obra"
  article_type: "empirical"  # inferido
  stage: "hypothesis"  # inferido
  created_at: timestamp
  updated_at: timestamp
  thread_id: str  # LangGraph
  
  # Relação 1:N com argumentos
  arguments: [
    {
      "version": 1,
      "claim": "IA ajuda levantamento",
      "focal_argument": {
        "intent": "explore",
        "subject": "IA in construction",
        "population": "not specified",
        "metrics": "not specified",
        "article_type": "unclear"
      },
      "created_at": timestamp
    },
    {
      "version": 2,
      "claim": "Regulamentação impede",
      "focal_argument": {
        "intent": "explore",
        "subject": "Regulation barriers",
        "population": "not specified",
        "metrics": "not specified",
        "article_type": "unclear"
      },
      "created_at": timestamp
    },
    {
      "version": 3,
      "claim": "Custo-benefício viável",
      "focal_argument": {
        "intent": "test_hypothesis",
        "subject": "Cost-benefit analysis of drones",
        "population": "construction companies",
        "metrics": "ROI, time savings",
        "article_type": "empirical"
      },
      "created_at": timestamp
    }
  ]

# CognitiveModel serializado no checkpoint LangGraph
# Argumento focal atual (última versão) também em memória
```

**Características:**
- Entidade `Topic` explícita com metadados (título, tipo, estágio)
- Histórico de argumentos versionado (V1, V2, V3...)
- Cada argumento preserva snapshot do `focal_argument` completo
- `thread_id` vincula tópico à sessão LangGraph
- Busca por tópico ou por thread_id

## Casos de Uso

### UC1: Usuário começa conversa → CognitiveModel em memória → claim evolui

**Fluxo:**
1. Usuário inicia conversa: "Observei que drones ajudam em obras"
2. Orquestrador extrai `focal_argument` inicial:
   ```python
   {
     "intent": "unclear",
     "subject": "drones in construction",
     "population": "not specified",
     "metrics": "not specified",
     "article_type": "unclear"
   }
   ```
3. Durante conversa, `focal_argument` evolui conforme usuário fornece mais contexto
4. Claim (subject) refinado: "drones in construction" → "drones for site surveying"

**Estado:** Apenas em memória (POC)

### UC2: Usuário pausa → Topic criado com snapshot do CognitiveModel

**Fluxo:**
1. Usuário pausa conversa após argumento focal estabilizar
2. Sistema cria entidade `Topic`:
   ```python
   Topic(
     id=uuid4(),
     title="Drones em levantamento de obra",  # inferido do subject
     article_type="empirical",  # inferido do focal_argument
     stage="hypothesis",  # inferido do estado da conversa
     thread_id="thread-123",
     arguments=[{
       "version": 1,
       "claim": "Drones ajudam levantamento",
       "focal_argument": {...}  # snapshot atual
     }]
   )
   ```
3. Topic persistido em banco de dados

**Estado:** Protótipo ou MVP

### UC3: Usuário retoma → CognitiveModel restaurado do checkpoint

**Fluxo:**
1. Usuário seleciona tópico existente da lista
2. Sistema recupera `thread_id` do Topic
3. LangGraph restaura estado completo do checkpoint (incluindo `focal_argument`)
4. Conversa continua de onde parou

**Estado:** Protótipo ou MVP

### UC4: Usuário muda claim radicalmente → novo argumento no mesmo Topic (arguments v2)

**Fluxo:**
1. Usuário retoma tópico "Drones em obras"
2. Durante conversa, muda direção: "Na verdade, quero focar em regulamentação"
3. Orquestrador detecta mudança e atualiza `focal_argument`:
   ```python
   {
     "intent": "explore",
     "subject": "Regulation barriers for drones",  # mudou!
     ...
   }
   ```
4. Sistema cria novo argumento (V2) no mesmo Topic:
   ```python
   Topic.arguments.append({
     "version": 2,
     "claim": "Regulamentação impede uso",
     "focal_argument": {...}  # novo snapshot
   })
   ```
5. Histórico preservado: V1 (IA ajuda) e V2 (Regulamentação) coexistem

**Estado:** MVP

### UC5: Usuário busca tópicos → lista por título/stage

**Fluxo:**
1. Usuário acessa interface de busca
2. Sistema lista tópicos filtrados:
   - Por título: "Drones em obras", "LLMs e produtividade", ...
   - Por estágio: "hypothesis", "methodology", "writing", ...
3. Usuário seleciona tópico
4. Sistema exibe histórico de argumentos (V1, V2, V3...)
5. Usuário escolhe argumento para retomar ou criar novo

**Estado:** MVP

## Progressão POC → MVP

### POC: Apenas CognitiveModel em memória (Épico 10)

**Escopo:**
- `focal_argument` extraído/atualizado pelo Orquestrador
- Estado em memória durante execução
- Checkpoint LangGraph preserva estado entre turnos (já implementado)
- Sem entidade `Topic` explícita

**Limitações:**
- Não há busca conceitual (apenas por `thread_id`)
- Não há histórico de argumentos anteriores
- Não há consolidação de tópicos

### Protótipo: CognitiveModel persistido no checkpoint (Épico 11)

**Escopo:**
- `focal_argument` serializado no checkpoint LangGraph
- Pausar/retomar preserva argumento focal completo
- `thread_id` já persistido (SqliteSaver - Épico 9)
- Ainda sem entidade `Topic` explícita

**Melhorias:**
- Persistência completa do estado entre sessões
- Retomar conversa preserva contexto completo

**Limitações:**
- Busca apenas por `thread_id` (temporal)
- Não há busca conceitual por tópico
- Não há histórico de múltiplos argumentos

### MVP: Entidade Topic + gestão de múltiplos (Épico 12)

**Escopo:**
- Entidade `Topic` explícita com metadados
- Histórico versionado de argumentos (V1, V2, V3...)
- Busca conceitual (título, estágio) e temporal (`thread_id`)
- Relação 1:N entre Topic e Argumentos

**Funcionalidades:**
- Criar tópico a partir de argumento maduro
- Listar tópicos por título/estágio
- Retomar tópico com novo argumento
- Histórico completo de evolução do pensamento

**Benefícios:**
- Navegação conceitual (não apenas temporal)
- Preservação de múltiplas direções de investigação
- Rastreabilidade completa da evolução do pensamento

## Referências

- `docs/product/vision.md` - Visão de produto e modelo conceitual da entidade Tópico
- `ARCHITECTURE.md` - Visão arquitetural e entidade central Tópico/Ideia
- `docs/orchestration/multi_agent_architecture.md` - Schema completo do MultiAgentState e campo `focal_argument`
- `agents/orchestrator/state.py` - Definição do `focal_argument` no `MultiAgentState`

