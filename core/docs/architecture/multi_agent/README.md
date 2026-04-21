# Multi-Agent Architecture - Épico 3

## 🎯 Fonte Única da Verdade

**Este documento é a fonte única da verdade para:**
- ✅ **Fluxo de agentes:** Todos os fluxos de execução do sistema multi-agente
- ✅ **MultiAgentState:** Schema completo com todos os campos e estruturas
- ✅ **Construção do super-grafo:** Especificação completa da arquitetura LangGraph

**Outros documentos devem referenciar este diretório:**
- `docs/ARCHITECTURE.md`: Resumo + referência para este diretório
- `core/docs/agents/overview.md`: Referência para fluxo e estado
- `../patterns/refinement.md`: Referência para schema completo

## Visão Geral

Este documento detalha a **implementação técnica** do sistema multi-agente. Para visão arquitetural geral, consulte `docs/ARCHITECTURE.md`.

**Foco deste diretório:**
- Estrutura do MultiAgentState (campos, tipos, uso)
- Implementação dos nós (código, decisões técnicas)
- Routers e lógica de fluxo
- Integração entre agentes
- Prompts e configuração

**Arquitetura de super-grafo LangGraph** com múltiplos agentes especializados coordenados por Orquestrador.

**Status atual:** Sistema em transição de fluxo determinístico para conversacional adaptativo (Épico 7).

---

## Estrutura da Documentação

Este diretório está organizado em módulos temáticos:

1. **[README.md](README.md)** (este arquivo) - Visão geral e índice
2. **[state.md](state.md)** - MultiAgentState completo (schema, campos, estruturas)
3. **[graph.md](graph.md)** - Construção do super-grafo e routers
4. **[nodes.md](nodes.md)** - Componentes detalhados (Orchestrator, Structurer, Methodologist)
5. **[flows.md](flows.md)** - Fluxos de execução (cenários completos)
6. **[config.md](config.md)** - Configuração de agentes (YAML, memória, identificadores)
7. **[prompts.md](prompts.md)** - Prompts do sistema
8. **[evolution.md](evolution.md)** - Evolução futura e backlog

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

**Especificação detalhada:** `../../orchestrator/conversational/`

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

**Detalhes:** Ver [graph.md](graph.md) para construção completa e [nodes.md](nodes.md) para implementação dos nós.

---

## Referências Rápidas

- **Estado completo:** [state.md](state.md)
- **Construção do grafo:** [graph.md](graph.md)
- **Implementação dos nós:** [nodes.md](nodes.md)
- **Fluxos de execução:** [flows.md](flows.md)
- **Configuração:** [config.md](config.md)
- **Prompts:** [prompts.md](prompts.md)
- **Evolução futura:** [evolution.md](evolution.md)

---

**Versão:** 1.1 (Épico 4 - Loop de Refinamento)  
**Data:** 11/11/2025  
**Status:** Atualizado com refinamento colaborativo

