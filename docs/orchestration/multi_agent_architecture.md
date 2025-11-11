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

### 3. Methodologist Integration

**Responsabilidade:** Validar rigor científico da hipótese (estruturada ou não).

**Input:**
- Se veio do Estruturador: usa `structurer_output`
- Se veio direto: usa `user_input`

**Implementação:**
```python
def methodologist_node(state: MultiAgentState) -> dict:
    """
    Valida rigor científico.
    
    Input prioritário:
    1. structurer_output (se disponível)
    2. user_input (caso contrário)
    """
    # Preparar input para o Metodologista
    if state.get('structurer_output'):
        hypothesis = state['structurer_output']['structured_question']
    else:
        hypothesis = state['user_input']
    
    # Chamar grafo existente do Metodologista
    methodologist_state = create_initial_state(hypothesis)
    result = methodologist_graph.invoke(
        methodologist_state,
        config={"configurable": {"thread_id": state.get('thread_id')}}
    )
    
    return {
        "methodologist_output": {
            "status": result['status'],
            "justification": result['justification']
        },
        "current_stage": "done",
        "messages": [AIMessage(content=result['justification'])]
    }
```

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

### Próximos Passos (Épico 4 - Loop Colaborativo)

- Metodologista em modo colaborativo (não rejeita, sugere melhorias)
- Loop Estruturador ↔ Metodologista (até 2 iterações)
- Memória de versões da hipótese

### Backlog "PRÓXIMOS"

- Estruturador vira grafo próprio
- Adicionar Pesquisador
- Adicionar Escritor

### Backlog "FUTURO DISTANTE"

- RAG para knowledge base
- Vector DB para memória de longo prazo

---

**Versão:** 1.0
**Data:** 10/11/2025
**Status:** Proposta técnica para implementação do Épico 3

