# ROADMAP - Paper Agent

> **📖 Status Atual:** Para entender o estado atual do sistema (épicos concluídos, funcionalidades implementadas), consulte [README.md](README.md) e [ARCHITECTURE.md](ARCHITECTURE.md).

> **📖 Melhorias Técnicas:** Para funcionalidades planejadas não vinculadas a épicos, consulte [docs/backlog.md](docs/backlog.md).

> **📖 Visão de Produto:** Para entender tipos de artigo, fluxos adaptativos e jornada do usuário, consulte `docs/vision/vision.md`.

---

## 📋 Status dos Épicos

### ✅ Concluídos
- Infraestrutura base completa
- **ÉPICO 1**: Convergência Orgânica
- **ÉPICO 2**: Sidebar
- **ÉPICO 3**: Bastidores
- **ÉPICO 4**: Contexto
- **ÉPICO 5**: UX Polish - Custos exibidos em reais (BRL) com formato brasileiro
- **ÉPICO 6**: Limpeza de Testes - Suite de testes limpa e focada com testes de integração reais
- **ÉPICO 7**: Validação de Maturidade do Sistema - Validação manual com 10 cenários críticos executados
- **ÉPICO 8**: Análise Assistida de Qualidade - Ferramentas para execução multi-turn, relatórios estruturados, sistema de observabilidade completo e migração da estrutura de testes (226 unit tests, 11 smoke tests, estrutura modular por categoria)
- **ÉPICO 9**: Integração Backend↔Frontend - Persistência silenciosa e feedback visual de progresso completos
- **ÉPICO 10**: Observador - Mente Analítica (POC) - ChromaDB + SQLite para catálogo de conceitos, pipeline de persistência, busca semântica e 22 testes unitários
- **ÉPICO 11**: Alinhamento de Ontologia - Migração completa de premises/assumptions para Proposições unificadas com solidez. Sistema usa `proposicoes` em todas as camadas (modelo, orquestrador, observador, interface). Schema SQLite atualizado, testes migrados, documentação alinhada.
- **ÉPICO 12**: Observer - Integração Básica (MVP) - Observer integrado ao fluxo multi-agente via callback assíncrono. Processa turnos em background após Orchestrator, publica eventos cognitive_model_updated, e exibe atividade na Timeline. Orquestrador acessa cognitive_model via prompt context. 28 testes passando.

### 🟡 Épicos Em Andamento

### ⏳ Épicos Planejados

> **Nota:** Épicos foram renumerados. O antigo "ÉPICO 6: Qualidade de Testes" foi dividido em 3 épicos refinados (6, 7, 8). Épicos antigos 7-11 foram renumerados para 9-13.

#### Planejados (não refinados)
- **ÉPICO 13**: Observer - Consultas Inteligentes (não refinado)
- **ÉPICO 14**: Observer - Detecção de Mudanças (não refinado)
- **ÉPICO 15**: Observer - Painel Dedicado (não refinado)
- **ÉPICO 16**: Catálogo de Conceitos - Interface Web (não refinado)
- **ÉPICO 17**: Pesquisador (não refinado)
- **ÉPICO 18**: Escritor (não refinado)


**Regra**: Claude Code só trabalha em funcionalidades de épicos refinados.

> Para fluxo completo de planejamento, consulte `planning_guidelines.md`.

---

## ✅ ÉPICO 8: Análise Assistida de Qualidade

Ferramentas para execução multi-turn, relatórios estruturados, sistema de observabilidade completo e migração da estrutura de testes. Implementado: Multi-Turn Executor (8.1), Debug Mode (8.2), logging estruturado (JSONL), debug reports, session replay e reorganização completa dos testes em estrutura modular (unit/smoke/behavior/e2e). Resultado: 226 unit tests e 11 smoke tests passando, 0 falhas.

---

## ✅ ÉPICO 10: Observador - Mente Analítica (POC)

Observador implementado com ChromaDB + SQLite para catálogo de conceitos. Inclui pipeline de persistência com deduplicação automática (threshold 0.80), busca semântica via embeddings (all-MiniLM-L6-v2), e 22 testes unitários. Preparado para Agentic RAG (Epic 12) com parâmetros opcionais em `process_turn()`.

**Consulte:** `docs/agents/observer.md` - Documentação completa do Observador

---

## ✅ ÉPICO 11: Alinhamento de Ontologia

Migração completa de premises/assumptions (strings separadas) para Proposições unificadas com solidez. Sistema usa `proposicoes` em todas as camadas: modelo (Proposicao Pydantic), orquestrador (validação e fallbacks), observador (extração e mesclagem), interface (renderização com indicadores de solidez). Schema SQLite atualizado, testes migrados (377 testes Proposicao, 330 testes CognitiveModel), documentação técnica alinhada.

**Consulte:**
- `docs/architecture/ontology.md` - Nova ontologia (Proposição)
- `docs/vision/epistemology.md` - Base filosófica
- `docs/vision/cognitive_model/core.md` - Evolução de solidez

---

## ÉPICO 12: Observer - Integração Básica (MVP)

**Objetivo:** Integrar Observer ao grafo principal. CognitiveModel disponível no estado para uso pelo orquestrador. Timeline mostra ações do Observer.

**Status:** ✅ Refinado (pronto para implementação)

**Dependências:**
- Épicos 10-11

> **Decisão Técnica:** Após spikes de validação (2025-12-08), confirmado que LangGraph não suporta paralelismo nativo via `add_edge(START, [list])`. Implementação usará callback assíncrono. Claude demonstrou uso natural do CognitiveModel via prompt (80% score), validando que tool explícita não é necessária no MVP.

**Consulte:**
- `docs/epics/epic-12-observer-integration.md` - **Especificação técnica completa**
- `docs/agents/observer.md` - Comunicação Observador ↔ Orquestrador
- `docs/architecture/observer_architecture.md` - Integração com grafo

### Funcionalidades:

#### 12.1 Callback Assíncrono Observer

- **Descrição:** Observer roda automaticamente após cada turno do Orquestrador em background thread
- **Critérios de Aceite:**
  - Observer dispara após `orchestrator_node` completar
  - Execução em thread daemon (não bloqueia shutdown)
  - Latência do usuário não aumenta (Observer <3s em background)
  - CognitiveModel atualizado no `state["cognitive_model"]`
  - Evento `cognitive_model_updated` publicado no EventBus
  - Erros não quebram fluxo principal (try/except completo)

#### 12.2 CognitiveModel no Estado e Prompt do Orquestrador

- **Descrição:** Orquestrador acessa cognitive_model via prompt e usa naturalmente
- **Critérios de Aceite:**
  - Campo `cognitive_model` existe em `MultiAgentState` (já existe)
  - Prompt do Orquestrador inclui seção "COGNITIVE MODEL DISPONÍVEL" quando disponível
  - Formato inclui: afirmação, fundamentos (com solidez), conceitos, contradições, questões abertas, métricas
  - Claude menciona cognitive_model no reasoning (validado por spike - 80% score)
  - Limites de conteúdo (5 fundamentos, 3 contradições, 5 questões) para não sobrecarregar prompt

#### 12.3 Timeline Visual

- **Descrição:** Timeline mostra quando Observer processou turno
- **Critérios de Aceite:**
  - Eventos `cognitive_model_updated` aparecem na timeline
  - Formato: "👁️ Turno X processado" com métricas (conceitos, solidez)
  - Integrado com timeline existente (não quebra UX)
  - Mostra últimos 3-5 eventos do Observer
  - Opcional: Seção colapsável separada "👁️ Observador"

#### 12.4 Testes de Integração

- **Descrição:** Validação completa da integração
- **Critérios de Aceite:**
  - Testes unitários: callback disparado, state atualizado, eventos publicados
  - Testes de integração: cenários multi-turn com Observer ativo
  - Validação: Observer não interfere no fluxo principal
  - Validação: cognitive_model disponível no próximo turno do Orquestrador
  - Script de validação: `scripts/validate_observer_integration.py`

**Estimativas:**
- LOC: ~600 linhas
- Tempo: 2h
- Risco: Baixo

---

## ÉPICO 13: Observer - Consultas Inteligentes

**Objetivo:** Orquestrador pode fazer perguntas pontuais ao Observador para decisões contextuais.

**Status:** ⏳ Planejado (não refinado)

**Dependências:**
- Épico 12

**Entregas:**
- API `what_do_you_see()` melhorada (LLM-based)
- Consultas otimizadas (`has_contradiction()`, `get_maturity()`, `get_dominant_concept()`)
- Orquestrador usa API em momentos estratégicos

**Estimativa:** ~400 linhas, 1.5h
**Risco:** Baixo

---

## ÉPICO 14: Observer - Detecção de Mudanças

**Objetivo:** Sistema detecta quando usuário mudou de ideia significativamente.

**Status:** ⏳ Planejado (não refinado)

**Dependências:**
- Épico 12

**Entregas:**
- Algoritmo de detecção de variations
- Threshold configurável (>0.90)
- Orquestrador reage a variations
- Timeline marca variations visualmente

**Estimativa:** ~500 linhas, 2h
**Risco:** Médio

---

## ÉPICO 15: Observer - Painel Dedicado

**Objetivo:** Interface visual completa para explorar cognitive_model.

**Status:** ⏳ Planejado (não refinado)

**Dependências:**
- Épico 12

**Entregas:**
- Painel colapsável "👁️ Observador"
- Seções: Afirmação, Fundamentos, Conceitos, Contradições, Lacunas
- Métricas visuais (barras de progresso)
- Reasoning colapsável (debug)

**Estimativa:** ~400 linhas, 1.5h
**Risco:** Baixo

---

## ÉPICO 16: Catálogo de Conceitos - Interface Web

**Objetivo:** Usuário explora biblioteca de conceitos via web. Transparência sobre o que sistema aprendeu.

**Status:** ⏳ Planejado (não refinado)

**Dependências:**
- Épico 15

**Consulte:**
- `docs/products/paper_agent.md` - Interface web conversacional
- `docs/interface/web/components.md` - Componentes Streamlit

### Funcionalidades Planejadas:

#### 16.1 Página Catálogo (`/catalogo`)

- Lista todos conceitos da biblioteca
- Busca por nome (fuzzy search)
- Filtros: por ideia, por frequência, por data
- Visualização: cards com conceito + variations + ideias relacionadas

#### 16.2 Preview na Página da Ideia

- Mostra discretamente: "Usa 3 conceitos: [X] [Y] [Z]"
- Tags clicáveis → redireciona para catálogo
- Não polui interface

#### 16.3 Analytics de Conceitos

- Conceitos mais mencionados (gráfico)
- Conceitos por ideia/artigo
- Evolução temporal
- Export em JSON
- Sistema detecta padrões: "5+ usuários adicionaram conceito X" → atualiza biblioteca base

#### 16.4 Testes E2E

- Fluxo completo: conversa → conceitos → catálogo
- Validar UX (não quebra experiência)
- Performance (biblioteca com 100+ conceitos)

---

## ÉPICO 17: Pesquisador

**Objetivo:** Agente para busca e síntese de literatura científica. Introduz Evidência como entidade prática.

**Status:** ⏳ Planejado (não refinado)

**Dependências:**
- Épico 16

**Adição:** Pesquisador pode usar catálogo de conceitos para buscar papers relacionados.

---

## ÉPICO 18: Escritor

**Objetivo:** Agente para compilação de seções do artigo científico.

**Status:** ⏳ Planejado (não refinado)

**Dependências:**
- Épico 17

---

## 📝 Observações

- Cada épico pode ser desenvolvido **isoladamente**
- Entrega **valor incremental**
- Pode ser **testado** antes do próximo
- Épicos não refinados requerem discussão antes da implementação
