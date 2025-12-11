# Memory Agent (Memória de Longo Prazo)

## Visão Geral

O **Memory Agent** é responsável por armazenar e recuperar memória de longo prazo do sistema. Inspirado na memória humana, organiza informações em **camadas temporais** com degradação natural: informação recente é mais acessível, informação antiga requer mais esforço para acessar.

## Status

⚠️ **CONCEITUAL - NÃO IMPLEMENTADO**

Este documento descreve a visão futura do Memory Agent. Atualmente, o sistema mantém histórico completo em memória ativa do Orquestrador/Observador.

## Filosofia

### Inspiração: Memória Humana

Assim como humanos:
- Lembram facilmente do que aconteceu ontem
- Precisam de esforço para lembrar do mês passado
- Podem esquecer detalhes, mas lembrar da essência
- Consolidam memórias importantes, descartam trivialidades

### Problema que Resolve

**Sem Memory Agent:**
Conversa com 50 turnos:
├─ Orquestrador processa 10k tokens de histórico a cada turno
├─ Custo: ~$0.15 por turno
├─ Latência: ~2s de processamento
└─ Escalabilidade: quebra em conversas longas (100+ turnos)

**Com Memory Agent:**
Conversa com 50 turnos:
├─ Orquestrador processa apenas CognitiveModel (~500 tokens)
├─ Memory consultado apenas quando necessário (5-10% dos turnos)
├─ Custo: ~$0.03 por turno (economia de 80%)
├─ Latência: ~500ms (busca em camada superficial)
└─ Escalabilidade: suporta conversas infinitas

## Arquitetura

### Três Camadas de Memória
┌─────────────────────────────────────────────────┐
│           CAMADA SUPERFICIAL (Recente)          │
│  ┌──────────────────────────────────────────┐   │
│  │  Resumos Condensados                     │   │
│  │  - key_phrases: ["LLMs", "produtividade"]│   │
│  │  - context_summary: "..."                │   │
│  │  - concepts: [conceito_ids]              │   │
│  │  - turn_range: 40-50                     │   │
│  │  - accessibility: RÁPIDA (~100-300ms)    │   │
│  └──────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
↓
┌─────────────────────────────────────────────────┐
│      CAMADA INTERMEDIÁRIA (Evolução)            │
│  ┌──────────────────────────────────────────┐   │
│  │  Snapshots de CognitiveModel             │   │
│  │  - claim: "..."                          │   │
│  │  - proposicoes: [...]                    │   │
│  │  - solidez: 0.65                         │   │
│  │  - turn: 25                              │   │
│  │  - accessibility: MODERADA (~300ms-1s)   │   │
│  └──────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
↓
┌─────────────────────────────────────────────────┐
│         CAMADA PROFUNDA (Literal)               │
│  ┌──────────────────────────────────────────┐   │
│  │  Mensagens Literais Brutas               │   │
│  │  - user_message: "..."                   │   │
│  │  - assistant_message: "..."              │   │
│  │  - turn: 5                               │   │
│  │  - timestamp: ISO-8601                   │   │
│  │  - accessibility: LENTA (~1-5s)          │   │
│  │  - pode estar COMPACTADA (>30 dias)      │   │
│  └──────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘

### Degradação Temporal
```python
def calcular_accessibility(dias_desde_turno: int) -> float:
    """
    Retorna score de acessibilidade (1.0 = instantâneo, 0.1 = muito lento)
    """
    if dias_desde_turno <= 7:
        return 1.0  # Última semana: fresco
    elif dias_desde_turno <= 30:
        return 0.7  # Último mês: acessível
    elif dias_desde_turno <= 365:
        return 0.4  # Último ano: requer esforço
    else:
        return 0.1  # Mais de 1 ano: arquivado, muito lento
```

## Responsabilidades

### 1. Armazenamento em Camadas

**Quando um turno ocorre:**

Mensagem literal → armazenada em Camada Profunda
Observador processa → gera resumo condensado → Camada Superficial
CognitiveModel muda significativamente → snapshot → Camada Intermediária


**Exemplo:**
```python
# Turno 15: Usuário define baseline
memory.store_literal(
    turn=15,
    user_msg="Baseline é 45min sem ferramenta",
    assistant_msg="Entendi. Então a métrica será tempo economizado vs 45min"
)

memory.store_summary(
    turn_range=(15, 15),
    summary="Baseline definido: 45min sem ferramenta",
    key_phrases=["baseline", "45min", "sem ferramenta"],
    concepts=["métrica", "baseline"]
)

# CognitiveModel mudou: baseline era undefined, agora é 45min
memory.store_snapshot(
    turn=15,
    cognitive_model={
        "claim": "LLMs aumentam produtividade",
        "baseline": "45min",
        "metrica": "tempo economizado",
        "solidez": 0.65
    }
)
```

### 2. Busca Estratificada (Query)

**Orquestrador consulta Memory:**
```python
# Busca por padrão: começa na camada superficial
resultado = memory.query(
    query="O que o usuário disse sobre baseline?",
    max_results=3,
    strategy="superficial_first"  # tenta superficial → intermediária → profunda
)
```

**Estratégias de busca:**

**A) Superficial First (padrão):**

Busca embedding em Camada Superficial
Se encontrar match (score > 0.8) → retorna
Se não, busca em Camada Intermediária
Se não, busca em Camada Profunda (último recurso)


**B) Deep Search (quando precisão literal é necessária):**

Busca diretamente em Camada Profunda
Retorna mensagens literais exatas
Mais lento, mas mais preciso


**C) Evolution Search (rastrear mudanças):**

Busca snapshots em Camada Intermediária
Retorna evolução temporal de CognitiveModel
Útil para: "quando definimos população?", "como claim mudou?"


### 3. Compactação Periódica

**Processo mensal (automatizado):**
```python
def compactar_mensal():
    """
    Turnos com >30 dias:
    1. Camada Profunda: comprimir mensagens literais (gzip)
    2. Camada Superficial: manter intacto (já é resumo)
    3. Camada Intermediária: manter snapshots críticos apenas
    """
    turnos_antigos = memory.get_turns_older_than(days=30)
    
    for turno in turnos_antigos:
        # Comprimir literal
        memory.compress_literal(turno, method="gzip")
        
        # Manter snapshot apenas se CognitiveModel mudou >20%
        if snapshot_is_critical(turno):
            memory.keep_snapshot(turno)
        else:
            memory.delete_snapshot(turno)
```

**Processo anual (automatizado):**
```python
def compactar_anual():
    """
    Turnos com >365 dias:
    1. Arquivar Camada Profunda (cold storage)
    2. Manter apenas Camada Superficial + snapshots críticos
    3. Acesso requer descompactação (~10s+)
    """
    turnos_muito_antigos = memory.get_turns_older_than(days=365)
    memory.archive_to_cold_storage(turnos_muito_antigos)
```

## Gatilhos de Consulta

Memory Agent é **reativo**, não proativo. Consultado apenas quando necessário:

### 1. Observador Detecta Incongruência
Observador: "Usuário disse 'bugs aumentaram', mas CognitiveModel diz 'bugs estáveis'"
↓
Observador sinaliza Orquestrador
↓
Orquestrador: "Deixa eu verificar contexto histórico..."
↓
Orquestrador consulta Memory: "Buscar menções a 'bugs' nos últimos 20 turnos"
↓
Memory retorna: "Turno 3: 'bugs estáveis há 6 meses'
Turno 15: 'bugs aumentaram 20% no último mês'"
↓
Orquestrador: "Não é contradição, são períodos diferentes"

### 2. Validação de Entendimento
Orquestrador: "Usuário mencionou 'baseline'. Ele já definiu isso?"
↓
Orquestrador consulta Memory: "Buscar definição de 'baseline'"
↓
Memory retorna: "Turno 8: 'Baseline é 45min sem ferramenta'"
↓
Orquestrador: "Sim, já definiu. Não preciso perguntar de novo."

### 3. Recall Explícito do Usuário
Usuário: "O que eu disse sobre população?"
↓
Orquestrador consulta Memory: "Buscar menções a 'população'"
↓
Memory retorna: "Turno 12: 'População são equipes Python de 2-5 devs'"
↓
Orquestrador responde: "Você definiu população como equipes Python de 2-5 devs"

### 4. Mudança de Foco (Retomar Ideia Anterior)
Usuário: "E aquela ideia de produtividade?"
↓
Observador: "Foco atual é 'bugs', usuário quer voltar para 'produtividade'"
↓
Observador sinaliza Orquestrador
↓
Orquestrador consulta Memory: "Buscar discussões sobre 'produtividade'"
↓
Memory retorna: "Turnos 1-12: Exploração de LLMs e produtividade,
Claim em construção: 'LLMs aumentam produtividade'"
↓
Orquestrador: "A gente estava explorando LLMs e produtividade. Quer retomar?"

## Fluxo de Informação
┌──────────────────────────────────────────────────┐
│                    TURNO                          │
│  Usuário envia mensagem                           │
└────────────────┬──────────────────────────────────┘
↓
┌──────────────────────────────────────────────────┐
│                 OBSERVADOR                        │
│  1. Processa turno                                │
│  2. Detecta padrões/incongruências                │
│  3. Gera resumo condensado                        │
│  4. Atualiza CognitiveModel                       │
│  5. Sinaliza Orquestrador (se necessário)         │
└────────────────┬──────────────────────────────────┘
↓
┌──────────────────────────────────────────────────┐
│               ORQUESTRADOR                        │
│  1. Recebe sinal do Observador                    │
│  2. Decide se precisa consultar Memory            │
│  3. Se sim: formula query                         │
└────────────────┬──────────────────────────────────┘
↓ (apenas se necessário)
┌──────────────────────────────────────────────────┐
│               MEMORY AGENT                        │
│  1. Recebe query do Orquestrador                  │
│  2. Busca em camadas (superficial → profunda)     │
│  3. Retorna resultados                            │
└────────────────┬──────────────────────────────────┘
↓
┌──────────────────────────────────────────────────┐
│               ORQUESTRADOR                        │
│  1. Processa resultados de Memory                 │
│  2. Decide next_step                              │
│  3. Responde usuário (ou envia para Comunicador)  │
└──────────────────────────────────────────────────┘
↓
(fim do turno)
↓
┌──────────────────────────────────────────────────┐
│               MEMORY AGENT                        │
│  1. Armazena mensagem literal (Camada Profunda)   │
│  2. Armazena resumo (Camada Superficial)          │
│  3. Armazena snapshot se necessário (Intermediária)│
└──────────────────────────────────────────────────┘

## Integração com Bastidores Transparentes

Quando usuário ativa bastidores transparentes, Memory Agent registra:
```json
{
  "agent": "memory_agent",
  "action": "query",
  "input": {
    "query": "Buscar definição de baseline",
    "strategy": "superficial_first"
  },
  "output": {
    "layer": "superficial",
    "results": [
      {
        "turn_range": "8-8",
        "summary": "Baseline definido: 45min sem ferramenta",
        "score": 0.92
      }
    ],
    "latency_ms": 120
  },
  "reasoning": "Orquestrador consultou Memory porque usuário mencionou 'baseline' sem contexto"
}
```

Usuário vê:
🔍 [Bastidores]
├─ Orquestrador consultou Memory
├─ Busca: "definição de baseline"
├─ Encontrado em: Camada Superficial (Turno 8)
└─ Latência: 120ms

## Configuração por Produto

### Paper-Agent (Sessão)
```python
memory_config = {
    "scope": "session",
    "superficial": {
        "max_turns": 10,  # Últimos 10 turnos resumidos
        "retention_days": 7
    },
    "intermediaria": {
        "snapshot_on": "cognitive_model_change > 20%",
        "retention_days": 30
    },
    "profunda": {
        "max_turns": 50,  # Últimas 50 mensagens literais
        "compress_after_days": 30
    }
}
```

### Fichamento (Documento)
```python
memory_config = {
    "scope": "document",
    "superficial": {
        "group_by": "chapter",  # Resumo por capítulo
        "retention_days": 90
    },
    "intermediaria": {
        "snapshot_on": "new_concept_identified",
        "retention_days": 365
    },
    "profunda": {
        "store": "citations_only",  # Apenas citações literais
        "compress_after_days": 90
    }
}
```

### Rede Social (Perfil)
```python
memory_config = {
    "scope": "user_profile",
    "superficial": {
        "max_conversations": 10,  # Últimas 10 conversas resumidas
        "retention_days": 30
    },
    "intermediaria": {
        "snapshot_on": "interest_evolution",  # Mudanças de interesse
        "retention_years": 5
    },
    "profunda": {
        "archive_after_days": 365,
        "compress": True
    }
}
```

## Implementação Futura

### Tecnologias Candidatas

**Armazenamento:**
- ChromaDB: embeddings para busca semântica (Camada Superficial)
- SQLite: metadados estruturados (timestamps, turn_ids, scores)
- Redis: cache de queries recentes (hot memory)
- S3/Blob Storage: camada profunda compactada/arquivada

**Busca:**
- Sentence-Transformers: gerar embeddings de queries
- FAISS: busca vetorial rápida
- Full-text search: fallback para literais (PostgreSQL FTS ou Elasticsearch)

**Compactação:**
- gzip: compressão de mensagens literais
- Delta encoding: armazenar apenas mudanças em snapshots consecutivos

### Métricas de Sucesso

- **Taxa de hit em Camada Superficial**: >70% das queries resolvidas sem ir fundo
- **Latência média de query**: <500ms (P95)
- **Economia de custo**: >60% vs processar histórico completo
- **Precisão de recall**: >90% quando usuário pergunta sobre passado

## Referências

- `../architecture/data-models/ontology.md` - MemoryLayer na ontologia
- `../architecture/vision/super_system.md` - Configuração por produto
- `docs/agents/orchestrator.md` - Quem consulta Memory
- `docs/agents/observer.md` - Quem detecta necessidade de consulta
- `core/docs/features/transparent_backstage.md` - Rastreamento de consultas

---

**Status**: Conceitual, aguardando implementação
**Prioridade**: Alta (após Épico 13 - Conceitos)
**Complexidade**: Alta (novo agente, novo storage, nova lógica de busca)

