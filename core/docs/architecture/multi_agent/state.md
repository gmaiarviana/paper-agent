# MultiAgentState - Schema Completo

**Fonte única da verdade:** Este é o schema completo e autoritativo do `MultiAgentState`. Todos os outros documentos devem referenciar este schema.

## Schema Base

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

## Estruturas Detalhadas

### `hypothesis_versions`

Histórico de versões da hipótese com feedback do Metodologista:

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

### `structurer_output`

Output do Estruturador com questão estruturada:

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

### `methodologist_output` (Épico 4 - Modo Colaborativo)

Output do Metodologista com validação e feedback:

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

### `focal_argument` (Épico 7.8)

Argumento focal explícito extraído pelo Orquestrador:

```python
focal_argument: {
    "intent": str,  # "test_hypothesis", "review_literature", "build_theory"
    "subject": str,  # Tópico principal
    "population": str,  # População-alvo
    "metrics": str,  # Métricas mencionadas
    "article_type": str  # "empirical", "review", "theoretical", etc.
}
```

### `stage_suggestion` (Épico 7.10)

Sugestão emergente de mudança de estágio:

```python
stage_suggestion: {
    "from_stage": str,  # Estágio atual inferido (ex: "exploration")
    "to_stage": str,  # Estágio sugerido (ex: "hypothesis")
    "justification": str  # Por que sistema acha que evoluiu
}
```

## Observações Importantes

- Campos `Optional` começam como `None`
- Cada agente atualiza apenas seus campos específicos
- Orquestrador não conhece detalhes de outros agentes
- Estado persiste entre nós via checkpointer do LangGraph

## Referências

- **Construção do grafo:** [graph.md](graph.md)
- **Implementação dos nós:** [nodes.md](nodes.md)
- **Fluxos de execução:** [flows.md](flows.md)

