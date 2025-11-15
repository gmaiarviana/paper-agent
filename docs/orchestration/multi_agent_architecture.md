# Multi-Agent Architecture - Épico 3

## 🎯 Fonte Única da Verdade

**Este documento é a fonte única da verdade para:**
- ✅ **Fluxo de agentes:** Todos os fluxos de execução do sistema multi-agente
- ✅ **MultiAgentState:** Schema completo com todos os campos e estruturas
- ✅ **Construção do super-grafo:** Especificação completa da arquitetura LangGraph

**Outros documentos devem referenciar este arquivo:**
- `ARCHITECTURE.md`: Resumo + referência para este documento
- `docs/agents/overview.md`: Referência para fluxo e estado
- `docs/orchestration/refinement_loop.md`: Referência para schema completo

## Visão Geral

Este documento detalha a **implementação técnica** do sistema multi-agente. Para visão arquitetural geral, consulte `ARCHITECTURE.md`.

**Foco deste documento:**
- Estrutura do MultiAgentState (campos, tipos, uso)
- Implementação dos nós (código, decisões técnicas)
- Routers e lógica de fluxo
- Integração entre agentes
- Prompts e configuração

**Arquitetura de super-grafo LangGraph** com múltiplos agentes especializados coordenados por Orquestrador.

**Status atual:** Sistema em transição de fluxo determinístico para conversacional adaptativo (Épico 7).

---

## Transição Arquitetural (Épico 7)

### Sistema Atual (Épicos 3-4)
- Orquestrador **classifica** maturidade (vague/semi_formed/complete)
- **Roteia automaticamente** para agente apropriado
- Loop de refinamento **automático** (até limite fixo)
- Fluxo **determinístico**: Entrada → Classificação → Roteamento → Processamento

### Sistema Futuro (Épico 7 em desenvolvimento)
- Orquestrador **conversa** com usuário
- **Oferece opções** em vez de rotear automaticamente
- Refinamento **sob demanda** (usuário decide)
- Fluxo **adaptativo**: Conversa → Negocia → Usuário decide → Executa

### Impacto na Implementação
**O que manter:**
- ✅ MultiAgentState (estrutura boa)
- ✅ Nós especializados (Estruturador, Metodologista funcionam)
- ✅ Versionamento de hipóteses (V1 → V2 → V3)
- ✅ Feedback estruturado do Metodologista

**O que evoluir:**
- 🔄 `orchestrator_node`: De classificador para facilitador
- 🔄 Routers: De automático para negociado
- 🔄 `route_after_methodologist`: De automático para oferece opções
- ✅ Refinamento sob demanda: usuário controla quando refinar (sem limite fixo)

**Especificação detalhada:** `docs/orchestration/conversational_orchestrator.md`

---

## Componentes

### 1. Super-Grafo Multi-Agente
┌─────────────────────────────────────────────────┐
│         Multi-Agent Super-Grafo                 │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌──────────────┐       ┌─────────────┐       │
│  │ Orchestrator │──────▶│ Structurer  │       │
│  │   (nó LLM)   │       │ (nó simples)│       │
│  └──────┬───────┘       └──────┬──────┘       │
│         │                      │               │
│         │         ┌────────────▼──────────┐    │
│         └────────▶│   Methodologist       │    │
│                   │   (grafo existente)   │    │
│                   └───────────────────────┘    │
│                                                 │
│  State: Híbrido (compartilhado + específico)   │
└─────────────────────────────────────────────────┘

---

## State Management

### MultiAgentState - Schema Completo

**Fonte única da verdade:** Este é o schema completo e autoritativo do `MultiAgentState`. Todos os outros documentos devem referenciar este schema.

```python
from typing import TypedDict, Optional, Annotated, Literal
from langgraph.graph.message import add_messages

class MultiAgentState(TypedDict):
    """
    Estado compartilhado entre todos os agentes do sistema multi-agente.
    
    Organizado em 3 seções principais:
    1. COMPARTILHADO: Campos que todos os agentes leem e escrevem
    2. ESPECÍFICO POR AGENTE: Campos que apenas um agente específico escreve
    3. MENSAGENS (LangGraph): Histórico de mensagens do LLM
    """
    
    # === SEÇÃO 1: CAMPOS COMPARTILHADOS ===
    user_input: str  # Input original do usuário
    session_id: str  # ID único da sessão (para EventBus)
    conversation_history: list  # Histórico legível da conversa
    current_stage: Literal["classifying", "structuring", "validating", "done"]  # Estágio atual
    
    # === VERSIONAMENTO (Épico 4) ===
    hypothesis_versions: list  # Histórico de versões da hipótese (V1, V2, V3...)
    
    # === SEÇÃO 2: ESPECÍFICO POR AGENTE ===
    
    # Orquestrador (Épico 7 - Conversacional MVP)
    orchestrator_analysis: Optional[str]  # Análise do contexto conversacional
    next_step: Optional[Literal["explore", "suggest_agent", "clarify"]]  # Próximo passo
    agent_suggestion: Optional[dict]  # Sugestão de agente com justificativa
    focal_argument: Optional[dict]  # Argumento focal explícito (intent, subject, population, metrics, article_type)
    reflection_prompt: Optional[str]  # Provocação de reflexão sobre lacunas
    stage_suggestion: Optional[dict]  # Sugestão emergente de mudança de estágio
    
    # Estruturador
    structurer_output: Optional[dict]  # Output do Estruturador
    
    # Metodologista
    methodologist_output: Optional[dict]  # Output do Metodologista
    
    # === SEÇÃO 3: MENSAGENS (LangGraph) ===
    messages: Annotated[list, add_messages]  # Histórico de mensagens LLM
```

**Estrutura de `hypothesis_versions`:**
```python
hypothesis_versions: [
    {
        "version": 1,
        "question": "Como X impacta Y?",
        "feedback": {
            "status": "needs_refinement",
            "improvements": [
                {
                    "aspect": "população",
                    "gap": "Não especificada",
                    "suggestion": "Definir: adultos 18-40 anos"
                }
            ]
        }
    },
    {
        "version": 2,
        "question": "Como X impacta Y em adultos 18-40 anos?",
        "feedback": {
            "status": "approved",
            "improvements": []
        }
    }
]
```

**Estrutura de `structurer_output`:**
```python
structurer_output: {
    "structured_question": str,  # Questão de pesquisa estruturada/refinada
    "elements": {
        "context": str,  # Contexto da observação
        "problem": str,  # Problema identificado
        "contribution": str  # Possível contribuição acadêmica
    },
    "version": int,  # V1, V2 ou V3
    "addressed_gaps": list  # Gaps endereçados (apenas refinamento)
}
```

**Estrutura de `methodologist_output` (Épico 4 - Modo Colaborativo):**
```python
methodologist_output: {
    "status": "approved" | "needs_refinement" | "rejected",
    "justification": str,  # Justificativa detalhada
    "improvements": [  # Apenas se needs_refinement
        {
            "aspect": "população" | "métricas" | "variáveis" | "testabilidade",
            "gap": str,  # O que está faltando
            "suggestion": str  # Como preencher
        }
    ],
    "clarifications": dict  # Mantido do Épico 2
}
```

**Estrutura de `focal_argument` (Épico 7.8):**
```python
focal_argument: {
    "intent": str,  # "test_hypothesis", "review_literature", "build_theory"
    "subject": str,  # Tópico principal
    "population": str,  # População-alvo
    "metrics": str,  # Métricas mencionadas
    "article_type": str  # "empirical", "review", "theoretical", etc.
}
```

**Estrutura de `stage_suggestion` (Épico 7.10):**
```python
stage_suggestion: {
    "from_stage": str,  # Estágio atual inferido (ex: "exploration")
    "to_stage": str,  # Estágio sugerido (ex: "hypothesis")
    "justification": str  # Por que sistema acha que evoluiu
}
```

**Observações:**
- Campos `Optional` começam como `None`
- Cada agente atualiza apenas seus campos específicos
- Orquestrador não conhece detalhes de outros agentes
- Estado persiste entre nós via checkpointer do LangGraph

---

## Configuração de Agentes (Épico 6)

### Arquivos `config/agents/<papel>.yaml`
- Um arquivo por agente, carregado no boot.
- Campos obrigatórios:
  - `name` (str): rótulo exibido na interface.
  - `role` (str): identificador interno (`methodologist`, `structurer`, ...).
  - `model` (str): id do modelo LLM.
  - `prompt` (str): prompt base (texto multilinha).
  - `tags` (list[str]): etiquetas para filtros/telemetria.
  - `context_limit` (int): tokens máximos permitidos por chamada.
  - `memory_window` (int): quantidade de eventos recentes preservados (`>=1`).
  - `tools` (list[str]): nomes das ferramentas habilitadas (pode ser vazio).
- Campos opcionais:
  - `temperature` (float) e `top_p` (float) com defaults globais.
  - `summary_template` (str) para personalizar resumo apresentado na interface.
- Validação ocorre na inicialização:
  - Mensagens de erro em PT-BR com caminho do arquivo e campo inválido.
  - Falha aborta a execução antes de instanciar o grafo.

Exemplo:

```yaml
name: Metodologista
role: methodologist
model: gpt-4o-mini
prompt: |
  Você é o agente metodologista responsável por avaliar hipóteses...
tags:
  - core
  - validation
context_limit: 4096
memory_window: 5
tools:
  - ask_user
temperature: 0.2
```

### Histórico em Memória
- `MultiAgentState` passa a expor `agent_memory: dict[str, deque]`.
- Cada item mantém `event_id`, `timestamp`, `summary`, `tokens_input`, `tokens_output`, `tokens_total`.
- Tamanho do buffer por agente controlado por `memory_window` (default 5).
- Após cada evento, CLI persiste snapshot em `runtime/snapshots/<session_id>.json`:
  ```json
  {
    "session_id": "cli-session-123",
    "updated_at": "2025-11-12T10:35:30.000Z",
    "agents": {
      "methodologist": [
        {"event_id": "evt-0003", "summary": "...", "tokens_total": 728}
      ]
    }
  }
  ```
- Streamlit consome snapshots para métricas agregadas sem reprocessar todo o JSONL.

### Reset Global de Sessão
- CLI ganhará flag `--reset-session <session_id>` (ou menu interativo) que limpa `agent_memory`, snapshots e stream associado.
- Reset mantém o histórico já emitido na interface; apenas o estado ativo é limpo.
- Reset individual por agente fica registrado no backlog.

### Identificadores
- `session_id`: reaproveita o `thread_id` (`cli-session-<uuid>`).
- `event_id`: contador incremental por sessão (`evt-0001`, `evt-0002`...), gerenciado pelo orquestrador.
- Abordagem evita colisões e funciona com execuções concorrentes sem configuração extra.

---

## Componentes Detalhados

### 1. Orchestrator Node

> **⚠️ EM TRANSIÇÃO (Épico 7):** Este nó evoluirá de classificador para facilitador conversacional. Implementação atual é POC que será expandida.

**Responsabilidade atual:** Analisar input do usuário, classificar maturidade da ideia, rotear para agente apropriado.

**Responsabilidade futura:** Manter diálogo fluido, detectar necessidades, oferecer opções, negociar caminho com usuário.

**Implementação:**
```python
def orchestrator_node(state: MultiAgentState) -> dict:
    """
    Classifica input e decide próximo agente.
    
    Classificação:
    - "vague": Ideia não estruturada → Chama Estruturador
    - "semi_formed": Hipótese parcial → Chama Metodologista
    - "complete": Hipótese completa → Chama Metodologista
    """
    user_input = state['user_input']
    
    # LLM classifica maturidade
    classification = llm.invoke(ORCHESTRATOR_CLASSIFICATION_PROMPT.format(
        user_input=user_input
    ))
    
    # Atualiza state com decisão
    return {
        "current_stage": classification,
        "messages": [AIMessage(content=f"Detectei: {classification}")]
    }
```

**Router:**
```python
def route_from_orchestrator(state: MultiAgentState) -> str:
    """Roteia baseado na classificação."""
    stage = state['current_stage']
    
    if stage == "vague":
        return "structurer"
    elif stage in ["semi_formed", "complete"]:
        return "methodologist"
```

---

### 2. Structurer Node (POC)

**Responsabilidade:** Organizar ideias vagas em questões de pesquisa estruturadas.

**Implementação (versão simples - POC):**
```python
def structurer_node(state: MultiAgentState) -> dict:
    """
    Transforma observação vaga em questão estruturada.
    
    Processo:
    1. Analisa input do usuário
    2. Identifica: contexto, problema, possível contribuição
    3. Estrutura questão de pesquisa
    """
    user_input = state['user_input']
    
    # LLM estrutura a ideia
    result = llm.invoke(STRUCTURER_PROMPT.format(
        observation=user_input
    ))
    
    # Parse do resultado
    structured_output = parse_structurer_output(result)
    
    return {
        "structurer_output": structured_output,
        "current_stage": "validating",  # Próximo: validar com Metodologista
        "messages": [AIMessage(content=result)]
    }
```

**Evolução futura (backlog "PRÓXIMOS"):**
- Estruturador vira grafo próprio com nós separados
- Adiciona tool `ask_user` para clarificações
- Loop interno de refinamento

---

### 3. Methodologist - Modo Colaborativo (Épico 4)

**Responsabilidade:** Validar rigor científico E ajudar a construir hipóteses.

**Modos de operação:**
1. **approved**: Hipótese testável e pronta
2. **needs_refinement**: Tem potencial, falta especificidade (NOVO)
3. **rejected**: Sem base científica

**Output:**
```python
{
    "status": "approved" | "needs_refinement" | "rejected",
    "justification": str,
    "improvements": [  # NOVO - apenas se needs_refinement
        {
            "aspect": "população" | "métricas" | "variáveis",
            "gap": str,
            "suggestion": str
        }
    ],
    "clarifications": dict
}
```

**Integração no loop:**
- Se needs_refinement AND iteration < max → volta pro Estruturador
- Se needs_refinement AND iteration >= max → força decisão
- Se approved/rejected → END

---

## Construção do Super-Grafo

**Fonte única da verdade:** Esta é a especificação completa da construção do super-grafo. Implementação em `agents/multi_agent_graph.py`.

### Estrutura do Grafo

```
START
  ↓
orchestrator (entry point)
  ↓ [router 1: route_from_orchestrator]
  ├─→ structurer → methodologist → orchestrator (router 2)
  ├─→ methodologist → orchestrator (router 2)
  └─→ END (retorna para usuário - Épico 7)
```

### Implementação

```python
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from agents.orchestrator.state import MultiAgentState
from agents.orchestrator.nodes import orchestrator_node
from agents.orchestrator.router import route_from_orchestrator
from agents.structurer.nodes import structurer_node
from agents.methodologist.nodes import decide_collaborative

def create_multi_agent_graph():
    """Cria super-grafo com múltiplos agentes."""
    
    # Criar grafo
    graph = StateGraph(MultiAgentState)
    
    # Adicionar nós (instrumentados com EventBus - Épico 5.1)
    graph.add_node("orchestrator", instrument_node(orchestrator_node, "orchestrator"))
    graph.add_node("structurer", instrument_node(structurer_node, "structurer"))
    graph.add_node("methodologist", instrument_node(decide_collaborative, "methodologist"))
    
    # Entry point
    graph.set_entry_point("orchestrator")
    
    # ROUTER 1: Orquestrador → Estruturador | Metodologista | User (END)
    graph.add_conditional_edges(
        "orchestrator",
        route_from_orchestrator,
        {
            "structurer": "structurer",
            "methodologist": "methodologist",
            "user": END  # Épico 7: Retornar para usuário
        }
    )
    
    # Estruturador → Metodologista (sempre)
    graph.add_edge("structurer", "methodologist")
    
    # ROUTER 2: Metodologista → Orquestrador (sempre - para negociação com usuário)
    graph.add_conditional_edges(
        "methodologist",
        route_after_methodologist,
        {
            "orchestrator": "orchestrator"  # Sempre retorna para Orquestrador
        }
    )
    
    # Compilar com checkpointer
    return graph.compile(checkpointer=MemorySaver())
```

### Routers

**Router 1: `route_from_orchestrator`**
- Decide destino baseado em `next_step` do Orquestrador
- Valores possíveis: `"structurer"`, `"methodologist"`, `"user"` (END)

**Router 2: `route_after_methodologist`**
- Sempre retorna `"orchestrator"` após Metodologista processar
- Orquestrador apresenta feedback e opções ao usuário
- Usuário decide próximo passo (refinar, pesquisar, ou mudar direção)

---

## Router após Metodologista (Épico 4 - Refinamento Sob Demanda)

**Comportamento atual:** Sempre retorna para o Orquestrador após o Metodologista processar. O Orquestrador apresenta feedback e opções ao usuário, que decide o próximo passo (refinar, pesquisar, ou mudar direção).

```python
def route_after_methodologist(state: MultiAgentState) -> str:
    """
    Router que sempre retorna para Orquestrador após Metodologista.
    Orquestrador negocia com usuário sobre próximo passo.
    """
    methodologist_output = state.get('methodologist_output')
    
    if not methodologist_output:
        return "orchestrator"
    
    # Sempre retorna para Orquestrador (que negocia com usuário)
    return "orchestrator"


# Adicionar ao grafo:
graph.add_conditional_edges(
    "methodologist",
    route_after_methodologist,
    {
        "orchestrator": "orchestrator"  # Sempre retorna para Orquestrador
    }
)
```

---

## Fluxo de Execução

### Cenário 1: Ideia vaga + refinamento (Implementado - Épicos 3-4)
```
Usuário: "Método incremental é mais rápido"
↓
Orquestrador: classifica "vague"
↓
Estruturador V1: "Como método incremental impacta velocidade?"
↓
Metodologista: "needs_refinement" (falta população, métricas)
  hypothesis_versions: [] → [V1] → [V1, V2]
↓
Orquestrador: apresenta feedback e opções ao usuário → usuário decide refinar
↓
Estruturador V2: "Método incremental reduz tempo em 30%, medido por sprints, em equipes 2-5 devs"
↓
Metodologista: "approved"
↓
END
```

**Resultado:** Usuário recebe V2 aprovada com histórico V1 → V2

### Cenário 2: Hipótese → Metodologista direto (Implementado - Épico 3)
```
Usuário: "Método X reduz tempo em 30% em equipes de 2-5 devs"
↓
Orquestrador: classifica "semi_formed" ou "complete"
↓
Metodologista: valida rigor científico
↓
Status: "approved" ou "rejected"
↓
END
```

### Cenário 3: Conversação adaptativa (Futuro - Épico 7 POC)
```
Usuário: "Quero entender impacto de LLMs em produtividade"
↓
Orquestrador: "Interessante! Você quer VER o que já existe ou TESTAR uma hipótese?"
↓
Usuário: "Testar"
↓
Orquestrador: "Legal! Me conta: o que é 'produtividade' pra você?"
↓ [conversa continua]
Usuário: "Velocidade de desenvolvimento"
↓
Orquestrador: "Entendi. Posso chamar o Metodologista pra validar se isso é testável?"
↓
Usuário: "Sim"
↓
[Chama Metodologista] → Feedback: "Falta população e métricas"
↓
Orquestrador: "Ele sugeriu especificar:
               1. Quem você quer estudar?
               2. Como medir velocidade?
               Quer refinar agora ou pesquisar literatura primeiro?"
↓
Usuário: "Refinar"
↓
[Chama Estruturador] → V2 refinada
↓
[Loop continua conforme usuário decide]
```

---

## Prompts do Sistema

### Orchestrator Classification Prompt
```python
ORCHESTRATOR_CLASSIFICATION_PROMPT = """Você é um Orquestrador que classifica inputs de usuários.

INPUT DO USUÁRIO:
{user_input}

CLASSIFIQUE como:
- "vague": Observação ou ideia não estruturada (falta contexto, problema claro)
- "semi_formed": Hipótese parcial (tem ideia central, mas falta especificidade)
- "complete": Hipótese completa (população, variáveis, métricas definidas)

Retorne APENAS a classificação (uma palavra).
"""
```

### Structurer Prompt (POC)
```python
STRUCTURER_PROMPT = """Você é um Estruturador que organiza ideias vagas.

OBSERVAÇÃO DO USUÁRIO:
{observation}

TAREFA:
Extraia e estruture:
1. Contexto: De onde vem essa observação?
2. Problema: Qual problema ou gap está sendo observado?
3. Contribuição potencial: Como isso pode contribuir para academia/prática?
4. Questão de pesquisa: Transforme em questão estruturada

RETORNE JSON:
{
  "context": "...",
  "problem": "...",
  "contribution": "...",
  "structured_question": "..."
}
"""
```

---

## Evolução Futura

### Próximo Passo Imediato (Épico 7 POC)

**Orquestrador Conversacional:**
- Implementar diálogo fluido antes de chamar agentes
- Sistema oferece opções em vez de rotear automaticamente
- Usuário escolhe próximo passo (refinar, pesquisar, mudar direção)
- Routers viram "ofertas de opções"

**Código a criar:**
- Novo prompt conversacional do Orquestrador
- Lógica de detecção de necessidades
- Sistema de oferta de opções
- Handling de mudança de direção

### Próximos Épicos

**Épico 8:** Entidade Tópico + Persistência (pausar/retomar)
**Épico 9:** Finalizar Interface + Telemetria completa

### Backlog de Longo Prazo

- Pesquisador (busca bibliográfica)
- Escritor (compilar artigo)
- Crítico (revisão final)
- RAG para knowledge base
- Vector DB para memória de longo prazo

---

**Versão:** 1.1 (Épico 4 - Loop de Refinamento)
**Data:** 11/11/2025
**Status:** Atualizado com refinamento colaborativo

