# Construção do Super-Grafo

**Fonte única da verdade:** Esta é a especificação completa da construção do super-grafo. Implementação em `agents/multi_agent_graph.py`.

## Estrutura do Grafo

```
START
  ↓
orchestrator (entry point)
  ↓ [router 1: route_from_orchestrator]
  ├─→ structurer → methodologist → orchestrator (router 2)
  ├─→ methodologist → orchestrator (router 2)
  └─→ END (retorna para usuário - Épico 7)
```

## Implementação

```python
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from core.agents.orchestrator.state import MultiAgentState
from core.agents.orchestrator.nodes import orchestrator_node
from core.agents.orchestrator.router import route_from_orchestrator
from core.agents.structurer.nodes import structurer_node
from core.agents.methodologist.nodes import decide_collaborative

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

## Routers

### Router 1: `route_from_orchestrator`

Decide destino baseado em `next_step` do Orquestrador.

**Valores possíveis:**
- `"structurer"`: Roteia para Estruturador
- `"methodologist"`: Roteia para Metodologista
- `"user"` (END): Retorna para usuário (Épico 7)

**Implementação:**
```python
def route_from_orchestrator(state: MultiAgentState) -> str:
    """Roteia baseado na decisão do Orquestrador."""
    next_step = state.get('next_step')
    
    if next_step == "suggest_agent":
        agent = state.get('agent_suggestion', {}).get('agent')
        if agent == "structurer":
            return "structurer"
        elif agent == "methodologist":
            return "methodologist"
    
    # Se não há sugestão ou usuário escolheu não seguir, retorna para usuário
    return "user"
```

### Router 2: `route_after_methodologist`

Sempre retorna para o Orquestrador após o Metodologista processar. O Orquestrador apresenta feedback e opções ao usuário, que decide o próximo passo (refinar, pesquisar, ou mudar direção).

**Comportamento atual:** Sempre retorna para o Orquestrador após o Metodologista processar. O Orquestrador apresenta feedback e opções ao usuário, que decide o próximo passo (refinar, pesquisar, ou mudar direção).

**Implementação:**
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

## Fluxo de Dados

1. **Orquestrador** recebe input do usuário
2. **Router 1** decide próximo agente (ou retorna para usuário)
3. **Estruturador** (se necessário) estrutura ideia vaga
4. **Metodologista** valida rigor científico
5. **Router 2** sempre retorna para Orquestrador
6. **Orquestrador** apresenta feedback e opções ao usuário
7. Usuário decide próximo passo (refinar, pesquisar, mudar direção)

## Referências

- **Estado completo:** [state.md](state.md)
- **Implementação dos nós:** [nodes.md](nodes.md)
- **Fluxos de execução:** [flows.md](flows.md)

