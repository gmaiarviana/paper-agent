# Estratégia de Snapshots

## Visão Geral

Snapshot é uma versão persistida do argumento quando ele atinge **maturidade**. Representa um ponto de cristalização do pensamento que permite ao usuário pausar a conversa sem perder progresso.

**Por que existe:**
- Argumento evolui durante conversa (claim muda, fundamentos são refinados)
- Nem toda evolução merece persistência (exploração inicial é volátil)
- Snapshot marca momento em que argumento está **estável o suficiente** para ser salvo
- Permite versionamento: V1 (vago) → V2 (refinado) → V3 (específico)

**Status atual:** SnapshotManager implementado mas **NÃO integrado** no fluxo conversacional. Integração planejada no Épico 15.

## Quando Criar Snapshot

### Critérios de Maturidade (via LLM)

Snapshot é criado quando argumento atende **todos** os critérios abaixo:

1. **Claim estável e específico**: Afirmação clara (>20 chars), não vaga
2. **Fundamentos sólidos**: Proposições com solidez > 0.6 (>= 2)
3. **Fundamentos frágeis**: Proposições com solidez < 0.4 (<= 2)
4. **Open_questions respondidas**: Lista vazia ou apenas questões secundárias (<= 1)
5. **Contradictions resolvidas**: Nenhuma contradição detectada
6. **Context completo**: Domínio, tecnologia, população definidos

**Confiança mínima:** Threshold de 0.8 (80%) para criar snapshot automaticamente.

**Exemplo de argumento maduro:**
```python
cognitive_model = {
    "claim": "Claude Code reduz tempo de sprint em 30% em equipes Python de 2-5 devs",
    "fundamentos": [
        {"proposicao_id": "prop_1", "solidez": 0.8},
        {"proposicao_id": "prop_2", "solidez": 0.7}
    ],
    "open_questions": [],
    "contradictions": [],
    "context": {
        "domain": "software development",
        "technology": "Python, Claude Code",
        "population": "teams of 2-5 developers"
    }
}
# → Snapshot V1 criado (maturidade detectada)
```

## Quando NÃO Criar Snapshot

### Casos que NÃO contribuem para maturidade

**1. Fugiu do assunto:**
```python
# Turno anterior: "LLMs aumentam produtividade"
# Turno atual: "Como funciona ChatGPT?"
# → Não cria snapshot (mudança de direção, não refinamento)
```

**2. Repetiu informação:**
```python
# Usuário: "LLMs aumentam produtividade"
# Sistema: "Entendi, LLMs aumentam produtividade"
# → Não cria snapshot (sem novo conteúdo)
```

**3. Apenas pergunta:**
```python
# Usuário: "O que é produtividade?"
# → Não cria snapshot (exploração, não afirmação)
```

**4. Claim muito vago:**
```python
cognitive_model = {
    "claim": "LLMs são úteis",  # < 20 chars, vago
    "fundamentos": []
}
# → Não cria snapshot (claim não específico)
```

**5. Muitas lacunas:**
```python
cognitive_model = {
    "claim": "LLMs aumentam produtividade",
    "fundamentos": [],
    "open_questions": [
        "Qual população?",
        "Qual métrica?",
        "Qual contexto?"
    ]
}
# → Não cria snapshot (muitas questões abertas)
```

## Integração com SnapshotManager

### Arquitetura Técnica

**Módulo:** `agents/persistence/snapshot_manager.py`

**Componentes:**

1. **MaturityAssessment (Pydantic):**
```python
class MaturityAssessment(BaseModel):
    is_mature: bool          # Argumento atingiu maturidade?
    confidence: float        # Confiança (0-1)
    justification: str        # Por que maduro/imaturo
    missing_elements: list[str]  # Elementos faltando (se imaturo)
```

2. **SnapshotManager:**
```python
manager = SnapshotManager()

# Avaliar maturidade via LLM
assessment = manager.assess_maturity(cognitive_model, claim_history)

# Criar snapshot se maduro (threshold 0.8)
snapshot_id = manager.create_snapshot_if_mature(
    idea_id, 
    cognitive_model,
    confidence_threshold=0.8
)
```

### MaturityAssessment via LLM

**Modelo:** Claude 3.5 Haiku (custo-benefício)

**Prompt:** `MATURITY_DETECTION_PROMPT`
- Recebe: `cognitive_model` serializado em JSON
- Opcional: `claim_history` (para detectar estabilidade)
- Retorna: `MaturityAssessment` (JSON estruturado)

**Fallback:** Se LLM falhar, usa heurística simplificada (`cognitive_model.is_mature()`) com confiança 0.6.

### Threshold de Confiança

**Padrão:** 0.8 (80%)

**Lógica:**
- `is_mature=True` + `confidence >= 0.8` → Cria snapshot
- `is_mature=False` ou `confidence < 0.8` → Não cria snapshot

**Configurável:** `confidence_threshold` em `create_snapshot_if_mature()`.

## Integração com Fluxo

### Status Atual

**SnapshotManager implementado mas NÃO integrado** no fluxo conversacional.

**Onde deveria ser chamado:**
- Orquestrador após cada turno (avalia maturidade do `cognitive_model`)
- Antes de transição de agente (se argumento maduro, criar snapshot)

### Integração Planejada (Épico 15)

**Fluxo futuro:**
```python
# Orquestrador (após processar turno)
def orchestrator_node(state: MultiAgentState):
    # ... processa input ...
    
    # Avaliar maturidade e criar snapshot se necessário
    if state["cognitive_model"]:
        snapshot_id = create_snapshot_if_mature(
            idea_id=state["active_idea_id"],
            cognitive_model=state["cognitive_model"],
            claim_history=state.get("claim_history")
        )
        
        if snapshot_id:
            logger.info(f"Snapshot automático criado: {snapshot_id}")
    
    return state
```

**Frequência:** A cada turno de conversa (avaliação contínua).

## Versionamento

### Como V1, V2, V3 Funcionam

**Auto-incremento por idea_id:**
- Cada snapshot recebe `version` sequencial (1, 2, 3...)
- Versão é única por ideia (UNIQUE constraint: `idea_id, version`)
- Versão é gerada automaticamente pelo `DatabaseManager.create_argument()`

**Exemplo:**
```python
# Ideia: "LLMs aumentam produtividade"

# Turno 5: Argumento maduro → Snapshot V1
argument_id_1 = create_snapshot(idea_id, cognitive_model_v1)
# → version = 1

# Turno 10: Argumento refinado → Snapshot V2
argument_id_2 = create_snapshot(idea_id, cognitive_model_v2)
# → version = 2

# Turno 15: Argumento específico → Snapshot V3
argument_id_3 = create_snapshot(idea_id, cognitive_model_v3)
# → version = 3
```

**Evolução típica:**
- **V1:** Claim vago, poucos fundamentos, muitos com baixa solidez
- **V2:** Claim refinado, fundamentos sólidos (solidez > 0.6), poucos frágeis
- **V3:** Claim específico, fundamentos completos, solidez alta (> 0.8)

**Schema SQLite:**
```sql
CREATE TABLE arguments (
    id TEXT PRIMARY KEY,
    idea_id TEXT NOT NULL,
    version INTEGER NOT NULL,
    -- ... campos do cognitive_model ...
    UNIQUE (idea_id, version)  -- Garante versões únicas
);
```

## Trigger para Conceitos (Épico 13)

### Snapshot como Trigger de Detecção

**Épico 13.3:** Pipeline de Detecção de Conceitos

**Fluxo:**
1. Argumento amadurece → Snapshot criado
2. **Trigger:** Detecção de conceitos via LLM
3. LLM extrai conceitos-chave do snapshot
4. Sistema gera embeddings (sentence-transformers)
5. Salva em ChromaDB (vetores) + SQLite (metadata)
6. Cria relacionamento N:N (`idea_concepts`)

**Por que no snapshot:**
- Não executa a cada mensagem (apenas quando argumento cristaliza)
- Conceitos extraídos de argumento maduro são mais confiáveis
- Evita ruído de exploração inicial

**Exemplo:**
```python
# Snapshot V1 criado
snapshot_id = create_snapshot(idea_id, cognitive_model)

# Trigger: Detecção de conceitos
concepts = extract_concepts_from_snapshot(snapshot_id)
# → ["produtividade", "desenvolvimento", "IA"]

# Salvar conceitos
for concept in concepts:
    concept_id = save_concept(concept)  # ChromaDB + SQLite
    link_idea_concept(idea_id, concept_id)  # N:N
```

## Referências

- `agents/persistence/snapshot_manager.py` - Implementação técnica do SnapshotManager
- `docs/architecture/persistence_foundation.md` - Fundação de persistência (SQLite, schema)
- `core/docs/vision/cognitive_model/core.md` - Conceitos fundamentais do modelo cognitivo
- `core/docs/vision/cognitive_model/evolution.md` - Evolução do pensamento e snapshots
- `docs/architecture/argument_model.md` - Schema técnico de Argument
- `docs/architecture/idea_model.md` - Schema de Idea (possui Arguments)
- `core/docs/vision/epistemology.md` - Epistemologia do sistema (fundamentos com solidez)
- `ROADMAP.md` - Épico 13 (Conceitos), Épico 15 (Integração de snapshots)

