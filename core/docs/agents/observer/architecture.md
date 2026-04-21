# Arquitetura Técnica do Observador

**Status:** Implementado (Épico 10.1, 10.2) | Pendente (10.3-10.6)
**Versão:** 2.0
**Data:** 05/12/2025

## Visão Geral

Documentação técnica da arquitetura do Observador - Mente Analítica. Detalha implementação, integração com grafo, e estratégias de paralelismo.

---

## Estrutura de Diretórios

> **Nota de Implementação:** O CRUD de conceitos está implementado em `core/agents/observer/catalog.py` (classe `ConceptCatalog`), não em um arquivo separado `concepts_crud.py`.

```
paper-agent/
├── agents/
│   ├── observer/                   # NOVO - Agente Observador
│   │   ├── __init__.py
│   │   ├── api.py                  # ObservadorAPI (interface de consulta)
│   │   ├── nodes.py                # Nós do grafo (process_turn)
│   │   ├── state.py                # ObserverState (TypedDict)
│   │   ├── extractors.py           # Extratores (claims, concepts, contradictions)
│   │   ├── metrics.py              # Cálculo de solidez e completude
│   │   └── prompts.py              # Prompts de extração
│   │
│   ├── orchestrator/               # Orquestrador (facilitador)
│   │   ├── nodes.py                # ATUALIZADO - consulta Observador
│   │   └── ...
│   │
│   └── ...
│
├── data/
│   ├── chroma/                     # NOVO - ChromaDB persistente
│   │   └── concepts/               # Collection de conceitos
│   │
│   └── database.db                 # SQLite (já existe)
│
├── database/
│   ├── schema.py                   # ATUALIZADO - adiciona tabelas concepts
│   └── ...
│
└── utils/
    ├── cognitive_model.py          # ATUALIZADO - estado completo
    └── embeddings.py               # NOVO - sentence-transformers
```

---

## Componentes Principais

### 1. ObservadorAPI (Interface de Consulta)

**Arquivo:** `agents/observer/api.py`

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class ObserverInsight:
    """Insight contextual do Observador."""
    insight: str            # Observação principal
    suggestion: str         # Sugestão de ação (opcional)
    confidence: float       # 0-1
    evidence: dict          # Dados do CognitiveModel que sustentam

class ObservadorAPI:
    """
    Interface de consulta não-determinística.
    
    Orquestrador consulta quando incerto, Observador responde
    com insights (não comandos).
    """
    
    def __init__(self, cognitive_model: CognitiveModel):
        self.cognitive_model = cognitive_model
    
    def what_do_you_see(
        self, 
        context: str, 
        question: str
    ) -> ObserverInsight:
        """
        Responde consulta contextual do Orquestrador.
        
        Args:
            context: Contexto da consulta (ex: "mudança de direção")
            question: Pergunta específica (ex: "conceitos ainda relevantes?")
            
        Returns:
            ObserverInsight com insight, sugestão, confiança, evidências
            
        Exemplos:
            context="Usuário mudou de LLMs para bugs"
            question="Conceitos anteriores ainda relevantes?"
            
            → {
                insight: "Parcial - LLMs ainda central, bugs é novo foco",
                suggestion: "Pode conectar: bugs como métrica de produtividade",
                confidence: 0.8,
                evidence: {concepts: ["LLMs", "bugs"], claims: [...]}
            }
        """
        # Usa LLM para analisar CognitiveModel e responder
        pass
    
    def get_current_state(self) -> dict:
        """
        Retorna estado atual completo do CognitiveModel.
        
        Usado quando Orquestrador precisa de visão geral,
        não apenas insight específico.
        """
        return self.cognitive_model.to_dict()
    
    def has_contradiction(self) -> bool:
        """Check rápido: há contradições detectadas?"""
        return len(self.cognitive_model.contradictions) > 0
    
    def get_solidez(self) -> float:
        """Check rápido: solidez geral atual."""
        return self.cognitive_model.solidez_geral
    
    def get_completude(self) -> float:
        """Check rápido: completude atual."""
        return self.cognitive_model.completude
```

---

### 2. ObserverState (Estado do Observador)

**Arquivo:** `agents/observer/state.py`

```python
from typing import TypedDict, Annotated
from langchain_core.messages import add_messages, BaseMessage

class ObserverState(TypedDict):
    """
    Estado do agente Observador.
    
    Mantém informações de processamento de turno,
    não confundir com CognitiveModel (que é o output).
    """
    messages: Annotated[list[BaseMessage], add_messages]
    user_input: str                     # Input atual sendo processado
    conversation_history: list[dict]    # Histórico completo
    
    # Output do processamento
    extracted_claims: list[str]
    extracted_concepts: list[str]
    extracted_contradictions: list[dict]
    extracted_open_questions: list[str]
    
    # Métricas calculadas
    solidez_calculated: float
    completude_calculated: float
```

---

### 3. Nós do Grafo

**Arquivo:** `agents/observer/nodes.py`

```python
from langchain_anthropic import ChatAnthropic
from core.agents.observer.state import ObserverState
from core.agents.observer.extractors import (
    extract_claims,
    extract_concepts,
    detect_contradictions
)
from core.agents.observer.metrics import (
    calculate_solidez,
    calculate_completude
)

# LLM eficiente para extração
llm = ChatAnthropic(
    model="claude-3-5-haiku-20241022",
    temperature=0
)

def process_turn(state: ObserverState) -> dict:
    """
    Nó principal: processa turno completo.
    
    Pipeline:
    1. Extrai claims via LLM
    2. Extrai conceitos via LLM
    3. Detecta contradições
    4. Identifica open_questions
    5. Calcula métricas (solidez, completude)
    6. Atualiza CognitiveModel
    7. Salva conceitos no catálogo
    8. Publica eventos
    
    Returns:
        Estado atualizado + flags de novidades
    """
    
    user_input = state["user_input"]
    history = state["conversation_history"]
    
    # 1. Extração via LLM
    claims = extract_claims(llm, user_input, history)
    concepts = extract_concepts(llm, user_input)
    contradictions = detect_contradictions(llm, claims)
    open_questions = identify_gaps(llm, claims, history)
    
    # 2. Métricas
    solidez = calculate_solidez(fundamentos=[])  # TODO: extrair fundamentos
    completude = calculate_completude(open_questions)
    
    # 3. Salvar conceitos no catálogo
    for concept_label in concepts:
        save_to_catalog(concept_label)  # ChromaDB + SQLite
    
    # 4. Atualizar CognitiveModel (global)
    cognitive_model.update({
        "claims": claims,
        "conceitos": concepts,
        "contradictions": contradictions,
        "open_questions": open_questions,
        "solidez_geral": solidez,
        "completude": completude
    })
    
    # 5. Publicar eventos
    event_bus.publish(ConceptsDetectedEvent(concepts))
    event_bus.publish(CognitiveModelUpdatedEvent(cognitive_model))
    
    # 6. Retornar estado atualizado
    return {
        "extracted_claims": claims,
        "extracted_concepts": concepts,
        "extracted_contradictions": contradictions,
        "extracted_open_questions": open_questions,
        "solidez_calculated": solidez,
        "completude_calculated": completude,
        # Flags para timeline (mostrar quando relevante)
        "has_new_concepts": len(concepts) > 0,
        "has_new_contradictions": len(contradictions) > 0,
        "solidez_changed_significantly": abs(solidez - cognitive_model.solidez_geral) > 0.15
    }
```

---

### 4. Extratores (LLM)

**Arquivo:** `agents/observer/extractors.py`

```python
from langchain_anthropic import ChatAnthropic
from core.agents.observer.prompts import (
    EXTRACT_CLAIMS_PROMPT,
    EXTRACT_CONCEPTS_PROMPT,
    DETECT_CONTRADICTIONS_PROMPT
)

def extract_claims(llm: ChatAnthropic, user_input: str, history: list) -> list[str]:
    """
    Extrai claims (proposições centrais) do turno atual.
    
    Prompt instrui LLM a identificar afirmações centrais que o usuário está fazendo.
    """
    prompt = EXTRACT_CLAIMS_PROMPT.format(
        user_input=user_input,
        history=history
    )
    
    response = llm.invoke(prompt)
    claims = parse_list(response.content)
    
    return claims

def extract_concepts(llm: ChatAnthropic, user_input: str) -> list[str]:
    """
    Extrai conceitos-chave (essências semânticas) do turno atual.
    
    Conceitos são abstrações reutilizáveis, não específicas desta conversa.
    Ex: "LLMs", "produtividade", "desenvolvimento ágil"
    """
    prompt = EXTRACT_CONCEPTS_PROMPT.format(user_input=user_input)
    
    response = llm.invoke(prompt)
    concepts = parse_list(response.content)
    
    return concepts

def detect_contradictions(
    llm: ChatAnthropic, 
    claims: list[str]
) -> list[dict]:
    """
    Detecta contradições lógicas entre claims.
    
    Returns:
        [
            {
                "claim_a": "X é mais rápido",
                "claim_b": "Velocidade não importa",
                "explanation": "Contradição direta sobre importância de velocidade"
            }
        ]
    """
    if len(claims) < 2:
        return []
    
    prompt = DETECT_CONTRADICTIONS_PROMPT.format(claims=claims)
    
    response = llm.invoke(prompt)
    contradictions = parse_contradictions(response.content)
    
    return contradictions

def identify_gaps(
    llm: ChatAnthropic,
    claims: list[str],
    history: list
) -> list[str]:
    """
    Identifica open_questions (lacunas a investigar).
    
    Ex: "Como medir produtividade?", "Qual população-alvo?"
    """
    # TODO: Implementar
    pass
```

---

### 5. Catálogo de Conceitos

#### ChromaDB (Vetores)

**Setup:** `core/agents/observer/catalog.py`

```python
import chromadb
from sentence_transformers import SentenceTransformer

# Cliente persistente
chroma_client = chromadb.PersistentClient(path="./data/chroma")

# Collection de conceitos
concepts_collection = chroma_client.get_or_create_collection(
    name="concepts",
    metadata={"description": "Biblioteca global de conceitos"}
)

# Modelo de embedding
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

def save_to_catalog(concept_label: str) -> str:
    """
    Salva conceito no catálogo (ChromaDB + SQLite).
    
    Pipeline:
    1. Gera embedding
    2. Busca similares (threshold 0.80)
    3. Se similar existe: adiciona variation
    4. Se não existe: cria novo
    5. Salva metadata no SQLite
    
    Returns:
        concept_id (UUID)
    """
    # 1. Gera embedding
    embedding = embedding_model.encode(concept_label)
    
    # 2. Busca similares
    results = concepts_collection.query(
        query_embeddings=[embedding.tolist()],
        n_results=3
    )
    
    # 3. Deduplicação (threshold 0.80)
    if results['distances'][0] and results['distances'][0][0] < 0.20:  # distância < 0.20 = similaridade > 0.80
        # Conceito já existe, adiciona variation
        existing_id = results['ids'][0][0]
        add_variation(existing_id, concept_label)
        return existing_id
    else:
        # Conceito novo
        concept_id = str(uuid.uuid4())
        
        # Salva no ChromaDB
        concepts_collection.add(
            ids=[concept_id],
            embeddings=[embedding.tolist()],
            metadatas=[{"label": concept_label}]
        )
        
        # Salva no SQLite
        db.execute(
            "INSERT INTO concepts (id, label, chroma_id) VALUES (?, ?, ?)",
            (concept_id, concept_label, concept_id)
        )
        
        return concept_id

def find_similar_concepts(query: str, top_k: int = 5) -> list[dict]:
    """
    Busca conceitos similares via embeddings.
    
    Returns:
        [
            {
                "id": UUID,
                "label": str,
                "similarity": float,
                "variations": list[str]
            }
        ]
    """
    # Gera embedding da query
    query_embedding = embedding_model.encode(query)
    
    # Busca no ChromaDB
    results = concepts_collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k
    )
    
    # Formata resultados
    concepts = []
    for i, concept_id in enumerate(results['ids'][0]):
        metadata = db.execute(
            "SELECT label, variations FROM concepts WHERE id = ?",
            (concept_id,)
        ).fetchone()
        
        concepts.append({
            "id": concept_id,
            "label": metadata['label'],
            "similarity": 1 - results['distances'][0][i],  # distância → similaridade
            "variations": json.loads(metadata['variations'] or '[]')
        })
    
    return concepts
```

#### SQLite (Metadados)

**Migrations:** `database/migrations/010_add_concepts.sql`

```sql
-- Tabela principal de conceitos
CREATE TABLE IF NOT EXISTS concepts (
    id TEXT PRIMARY KEY,
    label TEXT NOT NULL,
    essence TEXT,  -- Definição curta (opcional)
    variations TEXT,  -- JSON array de variations
    chroma_id TEXT NOT NULL,  -- Referência ao ChromaDB
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices
CREATE INDEX idx_concepts_label ON concepts(label);
CREATE INDEX idx_concepts_chroma_id ON concepts(chroma_id);

-- Tabela de variations (normalizada)
CREATE TABLE IF NOT EXISTS concept_variations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    concept_id TEXT NOT NULL,
    variation TEXT NOT NULL,
    FOREIGN KEY (concept_id) REFERENCES concepts(id) ON DELETE CASCADE
);

CREATE INDEX idx_variations_concept_id ON concept_variations(concept_id);

-- Tabela N:N entre ideas e concepts
CREATE TABLE IF NOT EXISTS idea_concepts (
    idea_id TEXT NOT NULL,
    concept_id TEXT NOT NULL,
    PRIMARY KEY (idea_id, concept_id),
    FOREIGN KEY (idea_id) REFERENCES ideas(id) ON DELETE CASCADE,
    FOREIGN KEY (concept_id) REFERENCES concepts(id) ON DELETE CASCADE
);

CREATE INDEX idx_idea_concepts_idea_id ON idea_concepts(idea_id);
CREATE INDEX idx_idea_concepts_concept_id ON idea_concepts(concept_id);
```

**CRUD:** `core/agents/observer/catalog.py`

```python
class ConceptCatalog:
    """CRUD operations para Concepts."""
    
    def create(self, concept: Concept) -> str:
        """Cria novo conceito."""
        pass
    
    def get_by_id(self, concept_id: str) -> Concept:
        """Busca conceito por ID."""
        pass
    
    def add_variation(self, concept_id: str, variation: str):
        """Adiciona variation a conceito existente."""
        pass
    
    def link_to_idea(self, idea_id: str, concept_ids: list[str]):
        """Cria links N:N entre idea e concepts."""
        pass
    
    def get_by_idea(self, idea_id: str) -> list[Concept]:
        """Retorna todos conceitos de uma idea."""
        pass
    
    def get_ideas_by_concept(self, concept_id: str) -> list[str]:
        """Retorna todas ideas que usam este conceito."""
        pass
```

---

## Integração com Grafo Multi-Agente

### Estratégia de Paralelismo

**Desafio:** Observador deve processar cada turno SEM bloquear fluxo principal.

#### Opção A: Paralelo (LangGraph Native)

```python
from langgraph.graph import StateGraph

# Grafo principal
graph = StateGraph(MultiAgentState)

# Nós principais
graph.add_node("orchestrator", orchestrator_node)
graph.add_node("structurer", structurer_node)
# ...

# Nó paralelo: Observador
graph.add_node("observer", observer_node)

# Edges paralelos
graph.add_edge(START, ["orchestrator", "observer"])  # Ambos recebem input
graph.add_edge("orchestrator", "router")
graph.add_edge("observer", END)  # Observador não bloqueia

graph.compile()
```

**Pros:**
- Verdadeiramente paralelo
- Observador não adiciona latência

**Contras:**
- Precisa validar se LangGraph suporta isso (investigar no Épico 12)

---

#### Opção B: Callback Assíncrono

```python
import asyncio

def orchestrator_node(state: MultiAgentState) -> dict:
    """Orquestrador chama Observador assincronamente."""
    
    # 1. Análise principal
    analysis = analyze_conversation(state)
    
    # 2. Dispara Observador (não aguarda)
    asyncio.create_task(observer_node(state))
    
    # 3. Continua sem esperar
    return {
        "next_step": analysis.next_step,
        "orchestrator_analysis": analysis.reasoning
    }

async def observer_node(state: MultiAgentState):
    """Processa turno em background."""
    observer_state = create_observer_state(state)
    result = process_turn(observer_state)
    # Publica eventos, atualiza CognitiveModel
```

**Pros:**
- Simples de implementar
- Funciona com LangGraph atual

**Contras:**
- Tecnicamente não é paralelo (é assíncrono)
- Orquestrador fica responsável por chamar

---

### Comunicação Observador → Orquestrador

**Como Orquestrador consulta:**

```python
def orchestrator_node(state: MultiAgentState) -> dict:
    """Orquestrador consulta Observador quando incerto."""
    
    # Análise própria
    my_analysis = analyze_conversation(state)
    
    # Gatilho natural: mudança de direção detectada
    if my_analysis.direction_changed:
        insight = observador_api.what_do_you_see(
            context="Usuário mudou de LLMs para bugs",
            question="Conceitos anteriores ainda relevantes?"
        )
        
        # Usa insight para enriquecer decisão
        decision = decide_with_insight(my_analysis, insight)
    else:
        decision = decide_autonomously(my_analysis)
    
    return {
        "next_step": decision.next_step,
        "orchestrator_analysis": decision.reasoning,
        "observer_insight": insight if insight else None
    }
```

**Gatilhos para consulta:**

1. Mudança de direção: `if focal_argument != previous_focal_argument`
2. Contradição aparente: `if claims_seem_inconsistent()`
3. Incerteza sobre completude: `if uncertain_about_depth()`
4. Check final: `if about_to_suggest_methodologist()`

---

## Visualização nos Bastidores

### EventBus (Publicação)

**Eventos publicados pelo Observador:**

```python
@dataclass
class ConceptsDetectedEvent(Event):
    """Conceitos novos detectados."""
    concepts: list[str]
    turn: int
    
@dataclass
class CognitiveModelUpdatedEvent(Event):
    """CognitiveModel foi atualizado."""
    solidez: float
    completude: float
    has_contradictions: bool
    
@dataclass
class ContradictionDetectedEvent(Event):
    """Contradição detectada."""
    claim_a: str
    claim_b: str
    explanation: str
```

### Dashboard (Consumo)

**Timeline Principal (Esquerda):**

```python
# Apenas quando relevante
if event.type == "ConceptsDetectedEvent" and len(event.concepts) > 0:
    add_to_timeline(
        f"👁️ Observador detectou {len(event.concepts)} conceitos: {', '.join(event.concepts[:3])}"
    )

if event.type == "ContradictionDetectedEvent":
    add_to_timeline(
        f"👁️ Observador detectou contradição entre '{event.claim_a}' e '{event.claim_b}'"
    )
```

**Painel Observador (Direita):**

```python
# Sempre atualizado (colapsável)
with st.expander("👁️ Observador - Mente Analítica", expanded=False):
    # Estado atual
    st.write("📋 Estado do raciocínio:")
    
    st.write(f"**Conceitos:** {', '.join(cognitive_model.conceitos[:5])}")
    st.write(f"**Claims:** {cognitive_model.claims[0] if cognitive_model.claims else 'Nenhum'}")
    
    # Métricas visuais
    solidez_color = "🟢" if cognitive_model.solidez_geral > 0.7 else "🟡" if > 0.5 else "🔴"
    st.write(f"**Solidez:** {solidez_color} {cognitive_model.solidez_geral:.2f}")
    
    if cognitive_model.open_questions:
        st.write("**Open questions:**")
        for q in cognitive_model.open_questions:
            st.write(f"• {q}")
    
    # Modo debug (colapsável dentro)
    with st.expander("🔍 Ver reasoning completo"):
        st.code(observer_last_prompt, language="text")
        st.code(observer_last_response, language="text")
```

---

## Performance e Custos

### Estimativas

**Por turno:**
- Extração de claims: ~200 tokens (input + output)
- Extração de conceitos: ~150 tokens
- Detecção de contradições: ~100 tokens (se > 2 claims)
- **Total:** ~450 tokens/turno

**Custos (Haiku):**
- Input: $0.25/1M tokens = $0.0001125 por turno
- Output: $1.25/1M tokens = $0.0005625 por turno
- **Total:** ~$0.000675 por turno (~R$ 0.0034)

**Conversa típica (20 turnos):**
- Tokens: ~9,000
- Custo: ~$0.0135 (~R$ 0.068)

**Comparado ao sistema total:**
- Orquestrador + agentes: ~$0.10 por conversa
- Observador: +$0.01 por conversa (+10%)
- **Aceitável** dado valor agregado

### Otimizações Futuras

1. **Cache de conceitos:** Não reprocessar conceitos idênticos
2. **Batch processing:** Acumular 3-5 turnos antes de processar (trade-off: latência vs custo)
3. **Modelo menor:** Avaliar modelos locais para extração (e.g., Llama 3.2 1B)

---

## Testes

### Testes Unitários (Épico 10)

- Mock do LLM (não chamadas reais)
- Vetores fixos (não embeddings reais)
- Schema SQLite validado
- Deduplicação testada (threshold 0.80)

### Testes de Integração (Épico 12)

- Cenários multi-turn com Observador ativo
- Validar que não interfere no fluxo
- LLM-as-Judge para qualidade de insights

### Testes E2E (Épico 13)

- Fluxo completo: conversa → conceitos → catálogo
- Performance com 100+ conceitos
- UX não quebra

---

## Referências

- `core/docs/agents/observer.md` - Documentação completa do Observador
- `../../data-models/ontology.md` - CognitiveModel e Conceitos
- `../../data-models/concept_model.md` - Schema de Concept
- `ROADMAP.md` - Épicos 10, 12, 13

---

**Versão:** 2.0
**Data:** 05/12/2025
**Status:** Implementado (Épico 10.1, 10.2) | Pendente (10.3-10.6)

