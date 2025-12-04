# Componentes Detalhados - Nós do Grafo

## 1. Orchestrator Node

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

**Detalhes completos:** Ver `docs/orchestration/conversational_orchestrator/README.md`

---

## 2. Structurer Node (POC)

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

**Detalhes completos:** Ver `docs/orchestration/refinement_loop.md`

---

## 3. Methodologist - Modo Colaborativo (Épico 4)

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

**Detalhes completos:** Ver `docs/agents/methodologist.md` e `docs/orchestration/refinement_loop.md`

---

## Referências

- **Estado completo:** [state.md](state.md)
- **Construção do grafo:** [graph.md](graph.md)
- **Fluxos de execução:** [flows.md](flows.md)
- **Prompts:** [prompts.md](prompts.md)

