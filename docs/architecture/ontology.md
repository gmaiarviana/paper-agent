# Ontologia do Sistema

## Visão Geral

Este documento é o **Single Source of Truth (SSoT)** que define a ontologia do super-sistema. Ele estabelece o que são Conceito, Ideia, Argumento, Proposição e Evidência do ponto de vista filosófico, e como essas entidades se relacionam entre si.

A ontologia reflete uma filosofia epistemológica onde não existe distinção binária entre "fato" e "suposição", mas sim proposições com diferentes graus de solidez baseados em evidências. Para entender a base filosófica completa, consulte `core/docs/vision/epistemology.md`.

Outros documentos de arquitetura referenciam este documento como base para entender as entidades fundamentais do sistema.

---

## Observador e CognitiveModel

### Responsável pela Atualização

O **Observador (Mente Analítica)** é o agente responsável por monitorar conversa e atualizar o `CognitiveModel` a cada turno.

**Processo:**
1. Usuário envia mensagem
2. Orquestrador processa (decide next_step)
3. **Observador processa em paralelo** (silencioso):
   - Extrai claims emergentes
   - Identifica fundamentos
   - Detecta contradições
   - Cataloga conceitos (ChromaDB + SQLite)
   - Identifica open_questions
   - Atualiza context (domínio, população, tecnologia)
   - Calcula métricas (solidez, completude)
4. CognitiveModel atualizado

**Timing:** Todo turno, sempre (não apenas snapshots).

**Características:**
- ✅ Silencioso (não interfere no fluxo)
- ✅ Automático (não precisa ser chamado)
- ✅ Completo (processa todos os turnos)
- ✅ Consultável (Orquestrador pode pedir insights)

**Memória e Degradação:**
- CognitiveModel atual = mantido em memória ativa (Observador)
- CognitiveModel histórico = armazenado em MemoryLayer.intermediária como snapshots
- CognitiveModel recente é rapidamente acessível, antigo requer consulta a Memory

### Estrutura do CognitiveModel

```python
CognitiveModel:
  # Proposições centrais
  claims: list[str]
  
  # Argumentos de suporte
  fundamentos: list[str]
  
  # Inconsistências detectadas
  contradictions: list[dict]
  
  # Conceitos semânticos (biblioteca global)
  conceitos: list[UUID]  # Referências a Concept
  
  # Lacunas a investigar
  open_questions: list[str]
  
  # Contexto evolutivo
  context: dict  # {domain, population, technology}
  
  # Métricas calculadas
  solidez_geral: float  # 0-1
  completude: float     # 0-1
```

---

## Entidades Fundamentais

### Conceito (Abstrato, Reutilizável, Atemporal)

**O que é:** Núcleo semântico abstrato que pode assumir diferentes formas linguísticas.

**Natureza:** Entidade **GLOBAL** (biblioteca única, não pertence a uma ideia específica).

**Filosofia:**
- Conceitos são **essências compartilhadas** entre múltiplas ideias
- Uma ideia **referencia** conceitos, não os **possui**
- Biblioteca cresce continuamente (conceitos de todas as conversas)
- Deduplicação automática (threshold 0.80) garante catálogo limpo

**Características:**
- Transcende palavras específicas
- Reutilizável entre diferentes ideias
- Tem variações linguísticas (produtividade, eficiência, performance = mesma essência)
- **Atemporal**: Conceitos existem independentemente de tempo, contexto ou usuário
- **Não possui solidez**: Conceitos são rótulos semânticos, não afirmações sobre o mundo
- **Origem flexível**: Podem vir de usuário, literatura, múltiplos usuários ou emergir do sistema

#### Biblioteca Global de Conceitos

**Natureza independente:**
- Conceitos existem independentemente de ideias
- Sistema mantém vocabulário compartilhado (dicionário universal)
- Múltiplas ideias referenciam o mesmo conceito da biblioteca global
- Conceito existe uma vez na biblioteca, usado por N ideias
- **Conceitos são atemporais**: Existem independente de quem os usa ou quando foram criados
- **Conceitos não têm "solidez"**: São rótulos semânticos, não afirmações que podem ser verdadeiras ou falsas

**Exemplo:**
```
Ideia 1: "LLMs aumentam produtividade"
  → referencia: [Concept: "LLMs", Concept: "Produtividade"]

Ideia 2: "Produtividade depende de métricas claras"
  → referencia: [Concept: "Produtividade", Concept: "Métricas"]

Biblioteca global:
  • LLMs (usado por: Ideia 1)
  • Produtividade (usado por: Ideia 1, Ideia 2)
  • Métricas (usado por: Ideia 2)
```

**Atualizado por:** Observador (a cada turno)

**Schema:**
```python
Concept:
  id: UUID
  label: str                    # "LLMs", "Produtividade"
  essence: str                  # Definição curta (opcional)
  variations: list[str]         # ["Language Models", "Large Language Models"]
  embedding: vector[384]        # ChromaDB (sentence-transformers)
  
  # Metadados
  created_at: datetime
  usage_count: int              # Quantas ideias usam este conceito
```

**Relacionamento N:N:**
```sql
idea_concepts:
  idea_id: UUID → ideas(id)
  concept_id: UUID → concepts(id)
```

**Deduplicação:**
- Similaridade > 0.80: variation do conceito existente
- Similaridade < 0.80: conceito novo

**Exemplos de globalidade:**

Conceito "Cooperação" (global, único na biblioteca):
- Essência: Ação coordenada de múltiplos agentes
- Variações linguísticas: cooperação, colaboração, teamwork, coopération (francês)
- Referenciado por Ideia 1: "Cooperação via mitos" (Sapiens)
- Referenciado por Ideia 2: "Cooperação tribal" (Clastres)
- Referenciado por Ideia 3: "Cooperação cívica" (Putnam)

### Ideia (Território, Contextual)

**O que é:** Pensamento articulado que reúne conceitos e argumentos em contexto específico.

**Características:**
- Usa múltiplos conceitos
- Pode ter múltiplos argumentos (diferentes lentes)
- Evolui ao longo de conversa
- Contextual (não necessariamente universal)

**Exemplos:**
- Ideia: "Cooperação humana via mitos compartilhados"
  - Conceitos usados: [Cooperação, Ficção, Linguagem]
  - Argumentos: [Religião permite cooperação, Nacionalismo permite cooperação]

### Proposição (Unidade Base de Conhecimento)

**O que é:** Afirmação sobre o mundo que pode ser sustentada ou refutada por evidências. É a unidade base de conhecimento no sistema.

**Estrutura:**
```python
Proposição:
  id: UUID
  texto: str                        # "Qualidade de código é mensurável"
  solidez: Optional[float]          # 0-1, DERIVADO (não definido manualmente)
                                    # None = proposição ainda não avaliada pelo sistema
  evidencias: list[Evidência]       # Lista de evidências (inicialmente vazia)
  usos: [ArgumentoRef]              # Onde é usada como fundamento
```

**Solidez inicial:**
- Proposições nascem com `solidez: None` (não avaliada)
- Observador ou Orquestrador avaliam via LLM e atualizam para valor numérico (0-1)
- Pesquisador (futuro) adiciona evidências que recalculam solidez
- Cálculos de maturidade ignoram proposições com `solidez=None`

**Características fundamentais:**
- **Não existe "fato" vs "suposição"**: Todas são proposições com diferentes graus de solidez
- **Solidez é calculada**: Derivada automaticamente das evidências (quantidade, qualidade, fonte)
- **Reutilizável**: Uma proposição pode ser usada como fundamento em múltiplos argumentos
- **Evolutiva**: Solidez muda conforme novas evidências são adicionadas

**Exemplos:**
- Proposição: "Linguagem permite transmitir ficções"
  - Solidez: 0.85 (múltiplas evidências de estudos linguísticos)
  - Usada em: Argumento sobre cooperação via mitos
  
- Proposição: "Qualidade de código é mensurável"
  - Solidez: 0.60 (algumas evidências, mas debate metodológico)
  - Usada em: Argumento sobre métricas de produtividade

**Importante:** "Premissa" agora é um **PAPEL**, não um tipo. Premissa = proposição sendo usada como fundamento de um argumento específico. Não há mais distinção entre premise/assumption - apenas proposições com solidez diferente.

### Evidência (Sustentação de Proposições)

**O que é:** Informação que apoia ou refuta uma proposição.

**Estrutura:**
```python
Evidência:
  id: UUID
  descricao: str                    # "Estudo de Smith et al. (2023)"
  fonte: str                        # DOI, URL, referência
  forca: str                        # "forte", "moderada", "fraca"
  tipo: str                         # "estudo", "exemplo", "autoridade", "experiência"
  contexto: str                     # Em que contexto essa evidência se aplica
```

**Características:**
- **Pode apoiar ou refutar**: Uma evidência pode fortalecer ou enfraquecer uma proposição
- **Força variável**: Evidências têm diferentes graus de força (forte, moderada, fraca)
- **Tipos diversos**: Estudos empíricos, exemplos, autoridade, experiência pessoal
- **Contexto importa**: Evidências são válidas em contextos específicos

**Exemplos:**
- Evidência (apoia): "Estudo de Smith et al. (2023) com 1000 desenvolvedores mostra correlação entre TDD e redução de bugs"
  - Tipo: estudo
  - Força: forte
  - Fonte: DOI: 10.1234/example

- Evidência (refuta): "Experiência pessoal: TDD aumentou tempo de desenvolvimento em 30%"
  - Tipo: experiência
  - Força: fraca
  - Contexto: equipe pequena, projeto específico

### Argumento (Lente, Estrutura Lógica)

**O que é:** Uma forma de ver/defender uma ideia através de estrutura lógica (claim + fundamentos).

**Características:**
- Estrutura: claim → fundamentos (proposições) → evidências
- Múltiplos argumentos podem defender mesma ideia (diferentes ângulos)
- Argumento = mapa, Ideia = território
- **Fundamentos são proposições**: Não há mais distinção entre premises/assumptions

**Estrutura:**
```python
Argumento:
  id: UUID
  idea_id: UUID
  claim: str                        # Afirmação principal (campo separado, não é proposição)
  fundamentos: [ProposicaoRef]      # Proposições que sustentam o argumento
  evidencias: [EvidenciaRef]        # Evidências diretas do argumento
```

**Exemplos:**
- Ideia: "Semana de 4 dias"
  - Argumento 1 (lente produtividade): 
    - Claim: "Aumenta produtividade via descanso"
    - Fundamentos: [Proposição: "Descanso aumenta foco", Proposição: "Foco aumenta produtividade"]
  - Argumento 2 (lente retenção):
    - Claim: "Reduz turnover em 20%"
    - Fundamentos: [Proposição: "Satisfação aumenta retenção"]

### MemoryLayer (Camada de Memória)

**O que é:** Representação temporal da memória de longo prazo. Inspirado na memória humana, onde informação recente é mais acessível que informação antiga.

**Características:**
- 3 tipos de camadas com diferentes características de acesso
- Degradação temporal natural: informação mais antiga fica menos acessível
- Permite busca eficiente priorizando recência sem perder histórico

**Estrutura:**
```python
MemoryLayer:
  id: UUID
  layer_type: str                   # "superficial" | "intermediária" | "profunda"
  turn_range: tuple[int, int]       # Intervalo de turnos cobertos (start, end)
  timestamp: datetime               # Quando foi criada
  accessibility: str                # Velocidade de busca: "rápida" | "moderada" | "lenta"
  degradation_score: float          # Quão "fresca" está (1.0 = ontem, 0.1 = ano passado)
  
  # Conteúdo específico por tipo
  content: dict                     # Varia conforme layer_type:
                                    # - superficial: {key_phrases, concepts, context_summary}
                                    # - intermediária: {cognitive_model_snapshot}
                                    # - profunda: {messages: [{role, content, timestamp}]}
```

**Tipos de Camada:**

**1. Superficial (recente):**
- Resumos condensados (key_phrases, concepts, context_summary)
- Busca rápida, últimos dias/semanas
- Acesso imediato para contexto conversacional atual
- Exemplo: "Resumo: usuário explorando produtividade com LLMs, conceitos chave: [LLMs, Produtividade, Métricas]"

**2. Intermediária:**
- Snapshots de CognitiveModel (evolução ao longo do tempo)
- Acesso moderado, útil para revisar progresso
- Captura estado do CognitiveModel em marcos importantes
- Exemplo: Snapshot do turno 50 mostrando CognitiveModel com claims consolidados e solidez calculada

**3. Profunda (antiga):**
- Mensagens literais brutas (user/assistant messages)
- Acesso mais lento, pode ser compactada periodicamente
- Arquivo histórico completo preservado

**Relações:**
- MemoryLayer.superficial → contém resumo de múltiplos turnos
- MemoryLayer.intermediária → contém snapshot de CognitiveModel
- MemoryLayer.profunda → contém mensagens literais originais

**Degradação temporal:**
- Informação de ontem (degradation_score: 1.0) está mais acessível que de mês passado (0.5) ou ano passado (0.1)
- Sistema prioriza recência sem perder rastreabilidade completa
- Futuro: compactação/arquivamento periódico (ex: anual) para manter performance

### BackstageContext (Contexto dos Bastidores)

**O que é:** Rastreamento de decisões e processamento interno do sistema. Captura transparência sobre como decisões foram tomadas, alimentando a feature "Bastidores Transparentes".

**Características:**
- Registra ações e raciocínio de todos os agentes
- Permite ao usuário entender origem de informações e decisões
- Funcionalidade opt-in (não distrai por padrão, mas disponível para transparência)

**Estrutura:**
```python
BackstageContext:
  id: UUID
  turn_id: UUID                     # Turno relacionado
  agent: str                        # Qual agente executou: "Observador" | "Orquestrador" | "Memory"
  action: str                       # O que foi feito:
                                    # - "detectou_incongruencia"
                                    # - "consultou_memory"
                                    # - "decidiu_next_step"
                                    # - "identificou_conceito"
                                    # - "atualizou_cognitive_model"
  input: dict                       # Contexto que levou à ação
  output: dict                      # Resultado da ação
  reasoning: str                    # Explicação em linguagem natural (legível para usuário)
  timestamp: datetime               # Quando ocorreu
```

**Exemplos de ações:**

**Observador:**
```python
BackstageContext(
  agent: "Observador",
  action: "detectou_incongruencia",
  input: {
    "turn_id": "abc123",
    "claim_atual": "LLMs aumentam produtividade",
    "claim_anterior": "Automação reduz qualidade"
  },
  output: {
    "incongruencia": "Afirmação atual contradiz claim anterior sobre qualidade"
  },
  reasoning: "Sistema detectou possível contradição: usuário afirmou que automação reduz qualidade, mas agora sugere que LLMs (tipo de automação) aumentam produtividade. Isso pode indicar necessidade de clarificação sobre o contexto específico."
)
```

**Memory:**
```python
BackstageContext(
  agent: "Memory",
  action: "consultou_memory",
  input: {
    "query": "produtividade com LLMs",
    "turn_id": "xyz789"
  },
  output: {
    "results": [
      {"layer": "superficial", "matches": 3, "relevance": 0.85},
      {"layer": "intermediária", "matches": 1, "relevance": 0.72}
    ]
  },
  reasoning: "Buscou informações sobre produtividade com LLMs. Encontrou 3 resumos recentes (últimas 2 semanas) e 1 snapshot de CognitiveModel de conversa anterior que abordou tema similar."
)
```

**Orquestrador:**
```python
BackstageContext(
  agent: "Orquestrador",
  action: "decidiu_next_step",
  input: {
    "cognitive_model": {"solidez": 0.45, "open_questions": 2},
    "user_intent": "quero entender métricas"
  },
  output: {
    "decision": "chamar_metodologista",
    "justification": "Baixa solidez e questão sobre métricas sugere necessidade de validação metodológica"
  },
  reasoning: "Decisão: acionar Metodologista para validar rigor científico. O CognitiveModel mostra solidez baixa (0.45) e usuário está questionando métricas, indicando necessidade de fortalecimento metodológico antes de prosseguir."
)
```

**Relações:**
- BackstageContext → rastreia decisões de Observador
- BackstageContext → rastreia consultas a Memory
- BackstageContext → rastreia decisões de Orquestrador

**Uso:**
- Alimenta feature "Bastidores Transparentes" (opt-in para usuário)
- Permite transparência sobre origem de informações e raciocínio do sistema
- Formato legível (não JSON/técnico por padrão) para melhor UX

---

## Fluxo de Detecção de Conceitos

### Pipeline (Observador)

```
Usuário: "LLMs aumentam produtividade"
    ↓
Observador: Processa turno
    ↓
1. LLM extrai conceitos: ["LLMs", "Produtividade"]
    ↓
2. Para cada conceito:
    ↓
   Gera embedding (sentence-transformers)
    ↓
   Busca similares no catálogo (ChromaDB)
    ↓
   Similaridade > 0.80?
     ├─ SIM → Adiciona como variation
     └─ NÃO → Cria novo conceito
    ↓
   Salva metadados (SQLite)
    ↓
3. Atualiza CognitiveModel.conceitos
    ↓
4. Publica evento: ConceptsDetectedEvent
```

### Exemplo Completo

**Turno 1:**
```
Input: "LLMs aumentam produtividade"
Detecta: ["LLMs", "Produtividade"]
Salva ambos (conceitos novos)

Biblioteca:
• LLMs
• Produtividade
```

**Turno 3:**
```
Input: "Language models são eficientes"
Detecta: ["Language models", "Eficiência"]

"Language models" similar a "LLMs" (0.92)
→ Adiciona como variation de "LLMs"

"Eficiência" similar a "Produtividade" (0.85)
→ Adiciona como variation de "Produtividade"

Biblioteca:
• LLMs (variations: ["Language models"])
• Produtividade (variations: ["Eficiência"])
```

**Turno 5:**
```
Input: "Bugs afetam qualidade"
Detecta: ["Bugs", "Qualidade"]

Ambos novos (similaridade < 0.80)
→ Cria 2 novos conceitos

Biblioteca:
• LLMs (variations: ["Language models"])
• Produtividade (variations: ["Eficiência"])
• Bugs
• Qualidade
```

---

## Relações Entre Entidades

### Ideia ↔ Conceito (N:N)
- **Relacionamento é referência, não posse**: Ideia referencia múltiplos conceitos da biblioteca global
- Ideia não possui conceitos, apenas referencia entidades globais existentes
- Mesmo conceito da biblioteca aparece em múltiplas ideias (reutilização)
- Sistema detecta conceitos compartilhados via vetor semântico
- Conceito existe independentemente: mesmo que todas as ideias que o referenciam sejam removidas, o conceito permanece na biblioteca global

### Ideia ↔ Argumento (1:N)
- Ideia pode ter múltiplos argumentos (diferentes lentes)
- Argumento pertence a uma ideia

### Argumento ↔ Conceito (N:N)
- Argumento usa conceitos nos fundamentos (proposições contêm conceitos)

### Argumento ↔ Proposição (N:N)
- Argumento usa proposições como fundamentos
- Uma proposição pode ser usada em múltiplos argumentos

### Proposição ↔ Evidência (N:N)
- Proposição tem evidências que apoiam e evidências que refutam
- Evidência pode apoiar ou refutar múltiplas proposições

### CognitiveModel ↔ MemoryLayer (1:N)
- CognitiveModel atual = mantido em memória ativa (Observador)
- CognitiveModel histórico = armazenado em MemoryLayer.intermediária como snapshots
- Múltiplos snapshots de CognitiveModel podem existir ao longo do tempo

### MemoryLayer (Tipos de Relação)
- MemoryLayer.superficial → contém resumo de múltiplos turnos
- MemoryLayer.intermediária → contém snapshot de CognitiveModel
- MemoryLayer.profunda → contém mensagens literais originais
- Degradação temporal: superficial → intermediária → profunda

### BackstageContext (Rastreamento)
- BackstageContext → rastreia decisões de Observador
- BackstageContext → rastreia consultas a Memory
- BackstageContext → rastreia decisões de Orquestrador
- BackstageContext → vinculado a turn_id específico

## Exemplo Completo: Sapiens (Harari)

**Texto original:**
"Cooperação humana em massa depende de mitos compartilhados. Dois católicos que nunca se encontraram podem embarcar juntos numa cruzada porque ambos acreditam que Deus encarnou num corpo humano."

**Sistema cristaliza:**

```python
Ideia: "Cooperação humana via mitos compartilhados"

Conceitos centrais:
- Ficção/Mito (vetor semântico)
- Cooperação (vetor semântico)
- Linguagem (vetor semântico)

Proposições:
- P1: "Linguagem permite transmitir ficções" (solidez: 0.85)
- P2: "Mitos compartilhados permitem cooperação em massa" (solidez: 0.75)

Evidências:
- E1: "Católicos cooperam via crença em Deus" (apoia P2, tipo: exemplo, força: moderada)
- E2: "Sérvios cooperam via crença em nação" (apoia P2, tipo: exemplo, força: moderada)
- E3: "Estudos linguísticos mostram capacidade de transmitir abstrações" (apoia P1, tipo: estudo, força: forte)

Argumento principal:
claim: "Cooperação em massa depende de mitos compartilhados"
fundamentos: [P1, P2]  # Proposições usadas como fundamentos
evidências: [E1, E2, E3]
```

## Hierarquia (Ideias dentro de Ideias)

Livros/textos complexos podem ter estrutura hierárquica:

```
Ideia macro: "Revoluções que transformaram Sapiens"
├─ Sub-ideia 1: "Revolução Cognitiva"
│   └─ Ideia específica: "Cooperação via mitos"
├─ Sub-ideia 2: "Revolução Agrícola"
│   └─ Ideia específica: "Agricultura como armadilha"
```

Sistema identifica hierarquia automaticamente processando conteúdo.

---

## Observador e Snapshots

### Complementaridade

**Observador:** Processa TODOS os turnos (monitoramento contínuo)
**Snapshots:** Marcos importantes quando argumento amadurece

**Fluxo:**
```
Turno 1-5: Observador cataloga conceitos continuamente
    ↓
Turno 5: Argumento amadurece → Snapshot criado
    ↓
Snapshot referencia conceitos catalogados pelo Observador
    ↓
Turno 6-10: Observador continua catalogando
    ↓
Turno 10: Novo snapshot → referencia conceitos novos
```

**Vantagem:**
- Snapshots não precisam reprocessar para detectar conceitos
- Conceitos já estão catalogados pelo Observador
- Snapshot apenas cria links (idea_concepts)

## Fluxo de Memória em Camadas

### Ciclo de Vida da Informação

**Fluxo temporal da informação entre camadas:**

```
┌─────────────────────────────────────────────────────────────┐
│ TURNO ATUAL                                                 │
│                                                             │
│ Usuário: "LLMs aumentam produtividade"                     │
│     ↓                                                       │
│ Observador processa (em paralelo, silencioso)              │
│     ↓                                                       │
│ Atualiza CognitiveModel (memória ativa)                    │
│     ↓                                                       │
│ Registra BackstageContext                                   │
└─────────────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────────────┐
│ CAMADA SUPERFICIAL (últimos dias/semanas)                  │
│                                                             │
│ • Resumos condensados (key_phrases, concepts)              │
│ • Busca rápida para contexto conversacional                │
│ • Degradação: 0.8-1.0 (informação fresca)                  │
│                                                             │
│ Exemplo:                                                    │
│ {                                                           │
│   "key_phrases": ["LLMs", "produtividade", "métricas"],    │
│   "concepts": [uuid1, uuid2],                              │
│   "context_summary": "Explorando impacto de LLMs..."       │
│ }                                                           │
└─────────────────────────────────────────────────────────────┘
                    ↓
              [Periódico, a cada N turnos ou marcos]
                    ↓
┌─────────────────────────────────────────────────────────────┐
│ CAMADA INTERMEDIÁRIA (semanas/meses)                       │
│                                                             │
│ • Snapshots de CognitiveModel                              │
│ • Evolução da ideia ao longo do tempo                      │
│ • Degradação: 0.3-0.7 (acesso moderado)                    │
│                                                             │
│ Exemplo:                                                    │
│ {                                                           │
│   "turn_id": 50,                                           │
│   "cognitive_model": {                                     │
│     "claims": ["LLMs aumentam produtividade em 30%"],     │
│     "solidez_geral": 0.65,                                 │
│     "conceitos": [uuid1, uuid2, uuid3]                     │
│   }                                                         │
│ }                                                           │
└─────────────────────────────────────────────────────────────┘
                    ↓
              [Após período estendido ou compactação]
                    ↓
┌─────────────────────────────────────────────────────────────┐
│ CAMADA PROFUNDA (meses/anos)                               │
│                                                             │
│ • Mensagens literais brutas                                │
│ • Arquivo histórico completo                               │
│ • Degradação: 0.1-0.3 (acesso lento)                       │
│                                                             │
│ Exemplo:                                                    │
│ {                                                           │
│   "messages": [                                            │
│     {"role": "user", "content": "LLMs aumentam...", ...}, │
│     {"role": "assistant", "content": "Interessante!...",...}│
│   ]                                                         │
│ }                                                           │
└─────────────────────────────────────────────────────────────┘
                    ↓
              [Compactação/Arquivamento Anual]
                    ↓
         [Informação preservada, acesso arquivado]
```

### Processo de Degradação

**Degradação temporal natural:**
1. **Turno atual → Superficial:** Informação imediatamente disponível, busca instantânea
2. **Superficial → Intermediária:** Após período (ex: 1-2 semanas), snapshot criado periodicamente
3. **Intermediária → Profunda:** Após período estendido (ex: 1-2 meses), mensagens literais arquivadas
4. **Profunda → Compactada:** Após período anual, pode ser compactada/arquivada

**Degradação não significa perda:**
- Informação nunca é perdida, apenas fica menos acessível
- Sistema prioriza recência (busca superficial primeiro)
- Consulta camadas mais profundas apenas quando necessário
- Rastreabilidade completa mantida

### Consulta a Memory

**Quando sistema consulta memória:**

```
Usuário pergunta sobre tópico abordado anteriormente
    ↓
Memory busca em camadas (ordem de prioridade):
    1. Superficial (rápida) → se encontrar relevante, retorna
    2. Intermediária (moderada) → se necessário, busca snapshots
    3. Profunda (lenta) → apenas se informação específica necessária
    ↓
Resultado agrega informações de múltiplas camadas
    ↓
BackstageContext registra consulta e resultados
```

**Eficiência:**
- 90% das consultas resolvidas na camada superficial (acesso rápido)
- 8% requerem camada intermediária (snapshots de CognitiveModel)
- 2% requerem camada profunda (mensagens literais específicas)

---

## Rastreabilidade

### Propagação de Solidez

Quando uma proposição é usada como fundamento em múltiplos argumentos, sua solidez afeta todos eles:

- **Fragilidade se propaga**: Se uma proposição base tem baixa solidez, todos os argumentos que dependem dela são afetados
- **Fortalecimento se propaga**: Fortalecer uma proposição fortalece todos os argumentos que dependem dela
- **Alertas automáticos**: Sistema pode alertar: "3 argumentos dependem de proposição com baixa solidez (0.35)"

**Exemplo:**
```
Proposição P: "Qualidade de código é mensurável" (solidez: 0.40)
  └─ Usada em Argumento A1: "Métricas de qualidade validam TDD"
  └─ Usada em Argumento A2: "Code review reduz bugs"
  └─ Usada em Argumento A3: "Refactoring melhora manutenibilidade"

Sistema alerta: "3 argumentos dependem de proposição com baixa solidez. 
Fortalecer P fortaleceria A1, A2 e A3."
```

### Dependências Explícitas

O sistema mantém rastreabilidade clara de:
- Quais argumentos dependem de cada proposição
- Quais proposições são fundamentais (usadas em muitos argumentos)
- Como fragilidades em proposições base afetam a solidez geral do conhecimento

### Estratégia de Fortalecimento

Quando uma proposição é identificada como frágil:
1. Sistema identifica todos os argumentos que dependem dela
2. Sugere buscar evidências para fortalecer a proposição
3. Mostra impacto: "Fortalecer esta proposição afetaria 5 argumentos"

## Referências

- `core/docs/vision/epistemology.md` - Fundamento filosófico da ontologia (proposições, solidez, evidências)
- `docs/architecture/concept_model.md` - Schema detalhado de Concept
- `docs/architecture/idea_model.md` - Estrutura de dados técnica de Ideia
- `docs/architecture/argument_model.md` - Estrutura de dados técnica de Argumento
- `core/docs/vision/cognitive_model/core.md` - Conceitos fundamentais (artefatos, solidez)
- `core/docs/vision/cognitive_model/evolution.md` - Como pensamento evolui e solidez é calculada
- `docs/agents/observer.md` - Documentação completa do Observador
- `ROADMAP.md` - Épicos 10, 12, 13 (Observador e Conceitos)

