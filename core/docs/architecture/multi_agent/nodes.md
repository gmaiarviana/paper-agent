# Componentes Detalhados - Nós do Grafo

## 1. Orchestrator Node

> **✅ Implementado (Épico 7+):** Orquestrador Socrático conversacional que facilita diálogo e faz transições fluidas entre agentes.

**Responsabilidade:** Manter diálogo fluido, detectar necessidades, fazer transições automáticas para agentes quando contexto suficiente, fazer curadoria das respostas.

**Implementação atual:**
- Usa prompt conversacional carregado de `config/agents/orchestrator.yaml`
- Analisa contexto e histórico da conversa
- Decide automaticamente quando chamar agentes (sem pedir confirmação)
- Faz curadoria das respostas dos agentes para apresentar tom unificado

**Detalhes completos:** Ver `../../orchestrator/conversational/README.md`

---

## 2. Structurer Node

**Responsabilidade:** Organizar ideias vagas em questões de pesquisa estruturadas e argumentos cristalizados.

**Implementação atual:**
- Usa prompt carregado de `config/agents/structurer.yaml`
- Estrutura observações em argumentos com claim, fundamentos e proposições
- Trabalha nos bastidores quando chamado pelo Orquestrador
- Retorna resultado que é curado pelo Orquestrador antes de apresentar ao usuário

**Detalhes completos:** Ver `../../patterns/refinement.md` e `../../../agents/overview.md`

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

**Detalhes completos:** Ver `../../../agents/methodologist.md` e `../../patterns/refinement.md`

---

## Referências

- **Estado completo:** [state.md](state.md)
- **Construção do grafo:** [graph.md](graph.md)
- **Fluxos de execução:** [flows.md](flows.md)
- **Prompts:** [prompts.md](prompts.md)

