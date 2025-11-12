# Multi-Agent Architecture - Épico 3

## Visão Geral

Arquitetura de super-grafo LangGraph com múltiplos agentes especializados coordenados por um Orquestrador inteligente.

**Decisões arquiteturais:**
- Orquestrador: Nó do grafo (não controller externo)
- Estruturador: Nó simples inicialmente (pode evoluir para grafo no futuro)
- Integração: Super-grafo (grafo de grafos)
- State: Híbrido (compartilhado + campos específicos por agente)

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

### MultiAgentState - Campos do Épico 4
```python
class MultiAgentState(TypedDict):
    # ... campos do Épico 3 ...
    
    # === ÉPICO 4: REFINEMENT LOOP ===
    refinement_iteration: int  # Contador de refinamentos (0, 1, 2)
    max_refinements: int       # Limite padrão: 2
    hypothesis_versions: list  # Histórico de evolução da hipótese
```

**Estrutura de hypothesis_versions:**
```python
[
    {
        "version": 1,
        "question": str,
        "feedback": {
            "status": str,
            "improvements": list
        }
    },
    # ...
]
```

### MultiAgentState (TypedDict)
```python
class MultiAgentState(TypedDict):
    """
    Estado compartilhado entre todos os agentes do sistema.
    
    Organizado em 3 seções:
    1. COMPARTILHADO: Todos os agentes leem/escrevem
    2. ESPECÍFICO: Cada agente tem seu espaço
    3. MENSAGENS: Histórico LangGraph
    """
    
    # === COMPARTILHADO ===
    user_input: str  # Input original do usuário
    conversation_history: list  # Histórico legível da conversa
    current_stage: str  # Estado atual: "structuring" | "validating" | "done"
    
    # === ESPECÍFICO POR AGENTE ===
    structurer_output: Optional[dict]  # Output do Estruturador
    methodologist_output: Optional[dict]  # Output do Metodologista
    
    # === MENSAGENS (LangGraph) ===
    messages: Annotated[list, add_messages]  # Mensagens LLM
```

**Estrutura dos outputs específicos:**
```python
# structurer_output
{
    "structured_question": str,  # Questão de pesquisa estruturada
    "elements": {
        "context": str,  # Contexto da observação
        "problem": str,  # Problema identificado
        "contribution": str  # Possível contribuição acadêmica
    }
}

# methodologist_output
{
    "status": "approved" | "rejected",
    "justification": str,
    "suggestions": List[str]  # Melhorias sugeridas
}
```

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

**Responsabilidade:** Analisar input do usuário, classificar maturidade da ideia, rotear para agente apropriado.

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
```python
from langgraph.graph import StateGraph, END

def create_multi_agent_graph():
    """Cria super-grafo com múltiplos agentes."""
    
    # Criar grafo
    graph = StateGraph(MultiAgentState)
    
    # Adicionar nós
    graph.add_node("orchestrator", orchestrator_node)
    graph.add_node("structurer", structurer_node)
    graph.add_node("methodologist", methodologist_node)
    
    # Entry point
    graph.set_entry_point("orchestrator")
    
    # Edges condicionais do Orchestrator
    graph.add_conditional_edges(
        "orchestrator",
        route_from_orchestrator,
        {
            "structurer": "structurer",
            "methodologist": "methodologist"
        }
    )
    
    # Structurer sempre vai para Methodologist
    graph.add_edge("structurer", "methodologist")
    
    # Methodologist finaliza
    graph.add_edge("methodologist", END)
    
    # Compilar
    return graph.compile(checkpointer=MemorySaver())
```

---

## Router após Metodologista (Épico 4)
```python
def route_after_methodologist(state: MultiAgentState) -> str:
    """
    Decide fluxo após Metodologista processar hipótese.
    
    Lógica:
    - approved → END
    - rejected → END
    - needs_refinement:
        - Se iteration < max → "structurer" (refinar)
        - Se iteration >= max → "methodologist_force_decision"
    """
    output = state['methodologist_output']
    status = output['status']
    iteration = state['refinement_iteration']
    max_iter = state['max_refinements']
    
    if status in ["approved", "rejected"]:
        return END
    
    if status == "needs_refinement":
        if iteration < max_iter:
            return "structurer"
        else:
            return "methodologist_force_decision"
    
    return END


# Adicionar ao grafo:
graph.add_conditional_edges(
    "methodologist",
    route_after_methodologist,
    {
        "structurer": "structurer",
        "methodologist_force_decision": "methodologist_force_decision",
        END: END
    }
)
```

---

## Fluxo de Execução

### Cenário 1: Ideia vaga
Usuário: "Observei que desenvolver com Claude Code é mais rápido"

Orchestrator classifica: "vague"
→ Structurer organiza:

Contexto: Desenvolvimento com IA
Problema: Falta método para medir produtividade
Questão estruturada: "Método incremental aumenta eficácia?"


→ Methodologist valida:

Status: rejected (falta métricas, população)
Sugestões: definir métricas, especificar população




### Cenário 2: Hipótese semi-pronta
Usuário: "Método incremental melhora desenvolvimento multi-agente"

Orchestrator classifica: "semi_formed"
→ Methodologist (direto):

Status: rejected (falta especificidade)
Sugestões: definir métricas, operacionalizar "melhora"




### Cenário 3: Hipótese completa
Usuário: "Método incremental reduz tempo de implementação de sistemas
multi-agente em 30%, medido por sprints, em equipes de 2-5 devs"

Orchestrator classifica: "complete"
→ Methodologist (direto):

Status: approved
Justificativa: Testável, falseável, específico


### Cenário 4: Loop de Refinamento (Épico 4)

**Input:** "Método X é mais rápido"

**Fluxo:**
Orquestrador: classifica "vague"
↓
Estruturador V1: "Como método X impacta velocidade?"
↓
Metodologista: "needs_refinement"

gaps: população, métricas
refinement_iteration: 0 → 1
↓
Router: volta pro Estruturador (iteration < max)
↓
Estruturador V2: "Método X reduz tempo em 30%, medido por sprints, em equipes de 2-5 devs"
↓
Metodologista: "approved"
↓
END

**Resultado:**
- Usuário recebe: V2 aprovada
- Histórico: V1 (needs_refinement) → V2 (approved)
- Total de iterações: 1 refinamento

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

### Próximos Passos (Épico 5+)

- **Épico 5**: Pesquisador (busca bibliográfica)
- **Épico 6**: Escritor (compilar artigo)
- **Épico 7**: Interface Conversacional
- **Épico 8**: Crítico (revisão final)

### Backlog "PRÓXIMOS"

- Estruturador vira grafo próprio (loop interno)
- RAG para knowledge base
- Vector DB para memória de longo prazo

---

**Versão:** 1.1 (Épico 4 - Loop de Refinamento)
**Data:** 11/11/2025
**Status:** Atualizado com refinamento colaborativo

