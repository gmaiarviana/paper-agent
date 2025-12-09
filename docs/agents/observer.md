# Observador - Mente Analítica

**Status:** ✅ Implementado (Épico 10 + 11.4 Completos)
**Versão:** 2.3
**Data:** 08/12/2025

## Resumo

Agente especializado em observar e catalogar a evolução do raciocínio durante conversas. Trabalha **silenciosamente em paralelo** ao Orquestrador, atualizando o CognitiveModel e extraindo conceitos automaticamente.

**Analogia:**
```
Orquestrador = Ator principal (fala, age, decide)
Observador = Testemunha silenciosa (vê tudo, cataloga, não interfere)
```

---

## Mitose do Orquestrador

### Por Que Separar?

**Antes (Orquestrador monolítico):**
- Facilitava conversa E observava raciocínio
- Duas responsabilidades conflitantes
- Complexidade crescente

**Depois (Separação clara):**
```
┌──────────────────────────────┐  ┌──────────────────────────────┐
│   ORQUESTRADOR               │  │   OBSERVADOR                 │
│   (Facilitador)              │  │   (Mente Analítica)          │
├──────────────────────────────┤  ├──────────────────────────────┤
│ • Facilita conversa          │  │ • Monitora TODA conversa     │
│ • Negocia caminhos           │  │ • Atualiza CognitiveModel    │
│ • Apresenta opções           │  │ • Extrai conceitos           │
│ • Provoca reflexão           │  │ • Avalia evolução            │
│ • Consulta Observador ──────────▶ • Detecta lacunas            │
│ • Decide next_step           │  │ • Responde consultas ◀───────│
└──────────────────────────────┘  └──────────────────────────────┘
```

---

## Responsabilidades

### O que FAZ

- ✅ **Monitorar TODA conversa** (todo turno, não apenas snapshots)
- ✅ **Atualizar CognitiveModel completo:**
  - Claims emergentes (proposições centrais)
  - Fundamentos (argumentos de suporte)
  - Contradições (inconsistências detectadas)
  - Conceitos (essências semânticas - ChromaDB + SQLite)
  - Open questions (lacunas a investigar)
  - Context (domínio, população, tecnologia)
- ✅ **Avaliar evolução** de ideias e argumentos
- ✅ **Detectar lacunas** e inconsistências
- ✅ **Calcular métricas** (solidez, completude)
- ✅ **Responder consultas** do Orquestrador (insights, não comandos)
- ✅ **Publicar eventos** para Dashboard (silencioso)

### O que NÃO FAZ

- ❌ Decidir next_step (quem decide: Orquestrador)
- ❌ Falar com usuário (quem fala: Orquestrador)
- ❌ Negociar caminhos (quem negocia: Orquestrador)
- ❌ Interromper fluxo conversacional

---

## Timing: Todo Turno (Sempre)

**Decisão:** Observador processa **TODOS os turnos**, não apenas snapshots.

**Por quê?**
- Garante que nada é perdido
- CognitiveModel sempre atualizado
- Conceitos detectados continuamente
- Não depende de eventos externos (snapshots)

**Custo vs Completude:**
- ✅ Completude máxima (nunca perde conceito)
- ⚠️ Custo constante (LLM em todo turno)
- ⚠️ Mas: Observador usa modelo eficiente (Haiku) e processamento é rápido

---

## CognitiveModel Completo

### Estrutura Atualizada pelo Observador

> **Épico 11.4:** Estrutura migrada de `premises`/`assumptions` para `proposicoes` unificadas.

```python
CognitiveModel:
  # Claim (afirmação central)
  claim: str

  # Proposições (fundamentos com solidez variável)
  # Substitui distinção binária premise/assumption
  proposicoes: list[Proposicao]  # {texto, solidez, evidencias}

  # Contradições (inconsistências)
  contradictions: list[Contradiction]  # {description, confidence, suggested_resolution}

  # Conceitos (essências semânticas)
  concepts_detected: list[str]  # Labels detectados (ChromaDB)

  # Open questions (lacunas)
  open_questions: list[str]

  # Context (contexto evolutivo)
  context: dict  # {domain, population, technology}

  # Solid grounds (evidências bibliográficas - futuro)
  solid_grounds: list[SolidGround]  # {claim, evidence, source}
```

**Proposicao:**
```python
class Proposicao:
    texto: str          # Enunciado da proposição
    solidez: float|None # 0-1 (None = não avaliada)
    evidencias: list    # IDs de evidências (futuro)
```

### Atualização a Cada Turno

```python
def process_turn(user_input: str, conversation_history: list):
    """Observador processa cada turno (Épico 11.4)."""

    # 1. Extração semântica via LLM
    extracted = extract_all(user_input, conversation_history)
    # extracted = {
    #     "claims": [...],
    #     "concepts": [...],
    #     "proposicoes": [Proposicao(texto=..., solidez=None), ...],
    #     "contradictions": [...],
    #     "open_questions": [...]
    # }

    # 2. Mescla com CognitiveModel anterior
    cognitive_model = merge_cognitive_model(previous, extracted)
    # proposicoes acumulam por similaridade de texto

    # 3. Calcula métricas (via LLM)
    metrics = calculate_metrics(
        claim=cognitive_model["claim"],
        proposicoes=cognitive_model["proposicoes"],  # Lista unificada
        open_questions=cognitive_model["open_questions"],
        contradictions=cognitive_model["contradictions"]
    )

    # 4. Persiste conceitos no catálogo
    persist_concepts_batch(extracted["concepts"], idea_id)

    # 5. Publica eventos (silencioso)
    event_bus.publish(CognitiveModelUpdatedEvent(cognitive_model, metrics))
```

---

## Interface de Consulta (Não-Determinística)

### Filosofia

**NÃO é command & control:**
```python
# ❌ ERRADO: Observador dá ordens
solidez = observador.get_solidez()
if solidez < 0.7:
    next_step = "explore"  # Orquestrador perde autonomia
```

**É diálogo contextual:**
```python
# ✅ CERTO: Observador dá insights
insight = observador.what_do_you_see(
    context="Usuário mudou de direção",
    question="Conceitos anteriores ainda relevantes?"
)
# Retorna: {
#   "relevance": "Parcial - LLMs ainda central, mas bugs é novo foco",
#   "suggestion": "Pode conectar: bugs como métrica de produtividade",
#   "confidence": 0.8
# }

# Orquestrador decide autonomamente baseado em insight
decision = decide_with_insight(my_analysis, insight)
```

### Quando Orquestrador Consulta?

**Gatilhos naturais** (não regras fixas):

1. **Mudança de direção detectada:**
   ```
   Usuário (turno 1): "LLMs aumentam produtividade"
   Usuário (turno 5): "Na verdade, quero focar em bugs"
   
   Orquestrador: "Hmm, percebi mudança. Deixa eu verificar contexto..."
   → Consulta: "O que mudou? Conceitos anteriores ainda relevantes?"
   ```

2. **Contradição aparente:**
   ```
   Usuário (turno 3): "Claude Code é mais rápido"
   Usuário (turno 8): "Mas velocidade não importa tanto"
   
   Orquestrador: "Você mencionou velocidade antes de forma diferente..."
   → Consulta: "Há contradição? Claim evoluiu ou há inconsistência?"
   ```

3. **Incerteza sobre profundidade:**
   ```
   Usuário: "Produtividade depende de muitos fatores"
   
   Orquestrador: "Quantos fundamentos já temos? Vale aprofundar mais?"
   → Consulta: "Fundamentos atuais cobrem o claim?"
   ```

4. **Checagem de completude:**
   ```
   Orquestrador: "Acho que temos claim + fundamentos sólidos..."
   → Consulta: "Solidez suficiente? Há gaps críticos?"
   ```

### API de Consulta

```python
class ObservadorAPI:
    def what_do_you_see(self, context: str, question: str) -> dict:
        """
        Responde consulta contextual do Orquestrador.
        
        Args:
            context: Contexto da consulta (ex: "mudança de direção")
            question: Pergunta específica (ex: "conceitos ainda relevantes?")
            
        Returns:
            {
                "insight": str,         # Observação principal
                "suggestion": str,      # Sugestão de ação (opcional)
                "confidence": float,    # 0-1
                "evidence": dict        # Dados do CognitiveModel que sustentam
            }
        """
        pass
    
    def get_current_state(self) -> dict:
        """
        Retorna estado atual completo do CognitiveModel.
        
        Usado quando Orquestrador precisa de visão geral,
        não apenas insight específico.
        """
        return cognitive_model.to_dict()
    
    def has_contradiction(self) -> bool:
        """Check rápido: há contradições detectadas?"""
        return len(cognitive_model.contradictions) > 0
    
    def get_solidez(self) -> float:
        """Check rápido: solidez geral atual."""
        return cognitive_model.solidez_geral
```

---

## Visualização nos Bastidores

### Layout (Ambos Colapsáveis)

```
┌─────────────────────────────────────────────────────────────────┐
│                     📊 BASTIDORES                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [▶ Timeline] (colapsado)      │  [▶ Observador] (colapsado)   │
│                                │                                │
└─────────────────────────────────────────────────────────────────┘
```

**Estado padrão:** Ambos colapsados (interface limpa)

### Timeline (Esquerda - Colapsável)

**Quando expandido:**
```
[▼ Timeline]
12:34:01 🎯 Orquestrador analisa input
12:34:02 🎯 Orquestrador consulta Observador
12:34:03 👁️ Observador atualizou modelo (2 conceitos novos)
12:34:04 🎯 Orquestrador decide: explore
12:34:05 📐 Estruturador estrutura questão
```

**Quando mostrar Observador na timeline?**

Apenas quando **relevante:**
- ✅ Conceito novo detectado: "👁️ Observador detectou 2 conceitos: LLMs, Produtividade"
- ✅ Contradição detectada: "👁️ Observador detectou contradição entre X e Y"
- ✅ Solidez mudou significativamente: "👁️ Solidez aumentou: 0.65 → 0.80"
- ❌ Atualização rotineira sem novidades

### Painel Observador (Direita - Colapsável)

**Quando expandido:**
```
[▼ Observador - Mente Analítica]

📋 Estado atual do raciocínio:

Conceitos detectados:
• LLMs (agora)
• Produtividade (2 turnos atrás)
• Claude Code (agora) 🆕

Claims atuais:
• "LLMs aumentam produtividade"

Solidez geral: 0.65 ⚠️

Open questions:
• Como medir produtividade?
• Qual população-alvo?

[▼ Ver reasoning completo]
  (expande para mostrar prompt usado, análise LLM)
```

**Informações visíveis:**
- Conceitos detectados (com timing)
- Claims atuais
- Solidez geral (visual: 🟢 alta, 🟡 média, 🔴 baixa)
- Open questions pendentes
- Contradições (se houver)

**Modo debug (colapsável dentro do painel):**
- Prompt completo enviado ao LLM
- Resposta bruta do LLM
- Reasoning detalhado
- Embeddings gerados (ChromaDB)

---

## Extração de Conceitos

### Pipeline

```python
def extract_concepts(user_input: str) -> list[Concept]:
    """
    Extrai conceitos-chave do turno atual.
    
    Pipeline:
    1. LLM extrai conceitos (prompt específico)
    2. Gera embeddings (sentence-transformers)
    3. Busca similares no catálogo (ChromaDB)
    4. Deduplica ou cria novo (threshold 0.80)
    5. Salva metadados (SQLite)
    """
    
    # 1. LLM extrai
    concepts_text = llm.invoke(EXTRACT_CONCEPTS_PROMPT.format(input=user_input))
    
    # 2. Para cada conceito
    for concept_label in concepts_text:
        # Gera embedding
        embedding = sentence_transformer.encode(concept_label)
        
        # Busca similares
        similar = chromadb.query(embedding, top_k=3)
        
        # Deduplica ou cria
        if similar and similar[0].similarity > 0.80:
            # Mesmo conceito, adiciona variation
            concept = similar[0]
            concept.variations.append(concept_label)
        else:
            # Conceito novo
            concept = Concept(
                label=concept_label,
                embedding=embedding
            )
            chromadb.save(concept)
            sqlite.save(concept)
    
    return concepts
```

### Deduplicação (Threshold)

- **> 0.80:** Mesmo conceito (adiciona como variation)
- **0.75-0.80:** Zona cinzenta (pergunta ao usuário no futuro)
- **< 0.75:** Conceito diferente (cria novo)

### Exemplo

```
Turno 1: "LLMs aumentam produtividade"
→ Detecta: ["LLMs", "Produtividade"]
→ Salva ambos no catálogo

Turno 3: "Language models são eficientes"
→ Detecta: ["Language models", "Eficiência"]
→ "Language models" similar a "LLMs" (0.92)
→ Adiciona "Language models" como variation de "LLMs"
→ "Eficiência" similar a "Produtividade" (0.85)
→ Adiciona "Eficiência" como variation de "Produtividade"

Catálogo final:
• LLMs (variations: ["Language models"])
• Produtividade (variations: ["Eficiência"])
```

---

## Integração com CognitiveModel

### Relação com Épico 9 (Snapshots)

**Épico 9:** Snapshots de Idea (quando argumento amadurece)
**Épico 10:** Observador processa TODOS os turnos

**Complementaridade:**
- Snapshots = marcos importantes (salva progresso)
- Observador = monitoramento contínuo (cataloga conceitos)

**Fluxo:**
```
Turno 1-5: Observador cataloga conceitos
Turno 5: Argumento amadurece → Snapshot criado
         → Snapshot referencia conceitos catalogados
Turno 6-10: Observador continua catalogando
Turno 10: Novo snapshot → referencia conceitos novos
```

### Atualização do Snapshot

```python
# Quando snapshot é criado
def create_snapshot(idea_id: UUID):
    # Pega conceitos detectados pelo Observador
    conceitos = cognitive_model.conceitos
    
    # Associa ao snapshot
    snapshot = Snapshot(
        idea_id=idea_id,
        concept_ids=conceitos,  # Referência N:N
        focal_argument=cognitive_model.claims[0],
        solidez=cognitive_model.solidez_geral
    )
    
    db.save(snapshot)
```

---

## Tecnologias

### LLM
- **Modelo:** claude-3-5-haiku-20241022
- **Justificativa:** Custo-efetivo, rápido, suficiente para extração
- **Temperature:** 0 (determinístico)

### ChromaDB
- **Tipo:** Local, persistente
- **Path:** `./data/chroma`
- **Collection:** `concepts`
- **Embedding:** sentence-transformers (all-MiniLM-L6-v2, 384 dim)

### SQLite
- **Tabelas:**
  - `concepts` (id, label, essence, variations JSON, chroma_id)
  - `concept_variations` (concept_id, variation)
  - `idea_concepts` (idea_id, concept_id)

---

## Evolução (Épicos)

### ✅ Épico 10: Observador - Mente Analítica (POC) - COMPLETO
- ✅ **10.1 Mitose do Orquestrador** - IMPLEMENTADO
  - Estrutura `agents/observer/` criada
  - ObservadorAPI com interface de consulta
  - Separação de responsabilidades documentada
- ✅ **10.2 Processamento via LLM** - IMPLEMENTADO
  - Extratores semânticos (claims, concepts, fundamentos, contradictions)
  - Métricas via LLM (solidez, completude)
  - `process_turn()` + `ObserverProcessor`
  - `CognitiveModelUpdatedEvent` no EventBus
- ✅ **10.3 ChromaDB + SQLite setup** - IMPLEMENTADO
  - ChromaDB persistente com cosine distance (`data/chroma/`)
  - SQLite com tabelas: concepts, concept_variations, idea_concepts
  - Embedding model: all-MiniLM-L6-v2 (384 dim)
  - `ConceptCatalog` com deduplicação automática
- ✅ **10.4 Pipeline de conceitos** - IMPLEMENTADO
  - `persist_concepts()` e `persist_concepts_batch()`
  - Integração com `process_turn()` via `persist_concepts_flag`
  - Link N:N entre Idea e Concept via `idea_id`
  - Parâmetros opcionais para Agentic RAG (Epic 12)
- ✅ **10.5 Busca semântica** - IMPLEMENTADO
  - `find_similar_concepts()` com threshold configurável
  - Similaridade cosseno ordenada descendente
  - Thresholds: 0.80 (mesmo conceito), 0.90 (auto-variation)
- ✅ **10.6 Testes POC** - IMPLEMENTADO
  - 22 testes unitários em `tests/unit/test_observer.py`
  - Cobertura: ConceptCatalog, Pipeline, Embeddings, Deduplicação
  - Mocks para LLM, vetores fixos para busca semântica
### ✅ Épico 12: Observador Integrado ao Fluxo - COMPLETO

Observer integrado ao grafo multi-agente via callback assíncrono.

**Implementação:**
- ✅ **12.1 Callback Assíncrono** - IMPLEMENTADO
  - `_create_observer_callback()` em `agents/multi_agent_graph.py`
  - Thread daemon após `orchestrator_node` (não bloqueia shutdown)
  - Atualiza `state["cognitive_model"]` com análise semântica
  - Tempo de processamento: <3s em background
  - Publica `CognitiveModelUpdatedEvent` via EventBus

- ✅ **12.2 CognitiveModel no Prompt** - IMPLEMENTADO
  - `_build_cognitive_model_context()` em `agents/orchestrator/nodes.py`
  - Formata claim, proposições (top 5 por solidez), conceitos (max 10)
  - Inclui contradições (max 3), questões abertas (max 5), métricas
  - Orquestrador usa naturalmente via prompt context

- ✅ **12.3 Timeline Visual** - IMPLEMENTADO
  - `render_observer_section()` em `app/components/backstage/timeline.py`
  - Seção colapsável "👁️ Observador" com últimos turnos
  - Métricas: conceitos, proposições, solidez, maturidade
  - Modal "👁️ Análise do Observador" com histórico completo

- ✅ **12.4 Testes** - IMPLEMENTADO
  - 9 testes em `tests/unit/test_observer_callback.py`
  - 19 testes em `tests/unit/agents/orchestrator/test_cognitive_context.py`
  - Script `scripts/validate_observer_integration.py`

**Fluxo de integração:**
```
User Input → Orchestrator → Response
                  ↓
           [Background]
                  ↓
             Observer → cognitive_model
                  ↓
         EventBus → Timeline
```

**Detalhes:** Ver `docs/epics/epic-12-observer-integration.md`

### Épico 13: Catálogo de Conceitos (Interface)
- ✅ Página `/catalogo` (busca, filtros, analytics)
- ✅ Preview na página da ideia
- ✅ Navegação: conceito → ideias → detalhes
- ✅ Export/import de biblioteca

---

## Referências

- `docs/architecture/observer_architecture.md` - Arquitetura técnica
- `docs/architecture/ontology.md` - CognitiveModel e Conceitos
- `docs/architecture/concept_model.md` - Schema de Concept
- `docs/vision/cognitive_model/core.md` - Fundamentos epistemológicos
- `ROADMAP.md` - Épicos 10, 12, 13

---

**Versão:** 2.3
**Data:** 08/12/2025
**Status:** ✅ Épico 10 Completo (POC) | ✅ Épico 11.4 Completo (Migração Proposições) | Próximo: Épico 12

