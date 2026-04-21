# Índice Temático de Contexto

> **Objetivo:** Mapear código → documentação e organizar contexto por temas (não sequencialmente)

---

## 🟢 CONTEXTO OBRIGATÓRIO (Sempre Enviar)

### Contexto Padronizado (Ver docs/process/refinement/starter.md)

**Genéricos (4):**
- `docs/CONSTITUTION.md` - Princípios, responsabilidades, processo
- `docs/ARCHITECTURE.md` - Decisões técnicas consolidadas
- `docs/ROADMAP.md` - Épicos e melhorias do core
- `docs/CONTEXT_INDEX.md` - **Este arquivo** (mapa temático código↔doc)

**Específicos do produto em refinamento (2):**
- `products/<produto>/ROADMAP.md` - Épicos do produto (Revelar, Ensaio, Prisma Verbal, ...)
- `products/<produto>/docs/vision.md` - Visão do produto (o "por quê" e escopo POC/Protótipo/MVP)

**Total obrigatório:** 6 arquivos.

---

## 📚 TEMAS INDEPENDENTES (Solicitar Conforme Necessidade)

Cada tema pode ser solicitado independentemente, sem ordem fixa.

---

### TEMA: Orquestração e Fluxo

**Código:**
- `core/agents/multi_agent_graph.py` - Super-grafo principal
- `core/agents/orchestrator/` - Orquestrador (nodes, router, state)
- `core/agents/orchestrator/state.py` - MultiAgentState (schema completo)

**Documentação:**
- `core/docs/architecture/multi_agent/` - **FONTE ÚNICA DA VERDADE** para fluxo e estado (state.md, graph.md, nodes.md, flows.md, config.md, prompts.md, evolution.md)
- `core/docs/agents/orchestrator/conversational/` - Orquestrador conversacional
- `core/docs/agents/orchestrator/socratic.md` - Orquestrador socrático
- `core/docs/architecture/patterns/refinement.md` - Loop de refinamento

**Solicitar quando:**
- Discutir fluxo de agentes
- Modificar comportamento do Orquestrador
- Entender MultiAgentState
- Implementar novo agente

---

### TEMA: Agentes Específicos

> **Organização:** Cada agente tem uma pasta própria em `core/docs/agents/<nome>/` contendo:
> - `responsibilities.md` — **quem faz o quê**, PODE/NÃO PODE, input/output (leitura primária ao discutir comportamento).
> - `architecture.md` ou `design.md` — **como** o agente se encaixa no grafo, estado, prompts, fluxos (leitura para implementação).
>
> O super-grafo (orquestração de todos os agentes) vive em `core/docs/architecture/multi_agent/`.

**Código:**
- `core/agents/methodologist/` - Metodologista (graph, nodes, router, state, tools, wrapper)
- `core/agents/structurer/nodes.py` - Estruturador
- `core/agents/observer/` - Observador
- `core/agents/models/cognitive_model.py` - Modelos Pydantic (CognitiveModel, Contradiction, SolidGround)

**Documentação — por agente (`core/docs/agents/<nome>/`):**
- `core/docs/agents/overview.md` - Visão geral de todos os agentes (responsabilidades, PODE/NÃO PODE, dimensões)
- `core/docs/agents/methodologist/responsibilities.md`, `knowledge.md` - Metodologista
- `core/docs/agents/orchestrator/responsibilities.md`, `socratic.md`, `conversational/` - Orquestrador
- `core/docs/agents/observer/responsibilities.md`, `architecture.md` - Observador
- `core/docs/agents/writer/design.md` - Writer (motivado pelo Ensaio, compartilhado com Produtor Científico)
- `core/docs/agents/researcher/responsibilities.md` - Pesquisador (futuro)
- `core/docs/agents/memory_agent/responsibilities.md`, `communicator/responsibilities.md` - Demais agentes planejados

**Documentação — super-grafo e padrões transversais:**
- `core/docs/architecture/multi_agent/` - Super-grafo, estado, nós, fluxos
- `core/docs/architecture/patterns/refinement.md` - **Estruturador documentado aqui** (processamento de feedback, lógica de refinamento)

**Solicitar quando:**
- Refinar comportamento de agente específico
- Implementar novo agente
- Entender responsabilidades de um agente

---

### TEMA: Dados e Persistência

**Código:**
- `core/agents/database/` - DatabaseManager (orquestrador), IdeasCRUD, ArgumentsCRUD, schema SQLite
  - `manager.py` - DatabaseManager singleton (orquestrador)
  - `ideas_crud.py` - CRUD operations para Ideas
  - `arguments_crud.py` - CRUD operations para Arguments
  - `schema.py` - Schema SQL (tabelas, índices, triggers, views)
- `core/agents/persistence/snapshot_manager.py` - Snapshots e detecção de maturidade
- `core/agents/checklist/progress_tracker.py` - Rastreamento de progresso
- `core/agents/models/cognitive_model.py` - Modelos de domínio

**Documentação:**
- `core/docs/architecture/data-models/ontology.md` - O que é Conceito, Ideia, Argumento
- `core/docs/architecture/data-models/idea_model.md` - Schema técnico de Ideia
- `core/docs/architecture/data-models/concept_model.md` - Schema técnico de Conceito
- `core/docs/architecture/data-models/argument_model.md` - Schema técnico de Argumento
- `core/docs/architecture/data-models/persistence.md` - Estratégia de persistência
- `core/docs/architecture/patterns/snapshots.md` - Estratégia de snapshots
- `core/docs/architecture/infrastructure/tech_stack.md` - Stack técnico (SQLite, ChromaDB)
- `core/docs/vision/super_system.md` - Super-sistema

**Solicitar quando:**
- Modificar modelos de dados
- Entender ontologia do sistema
- Implementar persistência
- Discutir stack técnico

---

### TEMA: Interface Web (por produto)

Cada produto tem seu próprio app. O padrão é: `products/<produto>/app/` para código Streamlit e `products/<produto>/docs/interface/` (ou equivalente) para a spec.

**Revelar (app atual):**
- Código: `products/revelar/app/chat.py`, `products/revelar/app/dashboard.py`, `products/revelar/app/components/` (chat_input, chat_history, backstage, sidebar/, ...), `products/revelar/app/pages/` (pensamentos, ideia_detalhes)
- Docs: `products/revelar/docs/interface/` (overview.md, components.md, flows.md — seção 3.6 documenta `progress_tracker.py`), `products/revelar/docs/interface/navigation_philosophy.md`, `products/revelar/docs/ux/conversation_patterns.md`

**Ensaio (próximo app):**
- Código: `products/ensaio/app/` (a ser criado no E-POC-1 — chat.py, components/, graph.py, product_config.py)
- Docs: `products/ensaio/docs/vision.md` (visão do produto, POC/Protótipo/MVP), `products/ensaio/ROADMAP.md` (épicos E-POC-1..3)

**Solicitar quando:**
- Implementar features de interface
- Modificar UX/UI
- Entender fluxo de navegação

**Gaps identificados:**
- ⚠️ `products/revelar/app/components/session_helpers.py` - **GAP REAL**: Não encontrei menção específica na documentação

---

### TEMA: CLI e Automação

**Código:**
- `core/tools/cli/chat.py` - CLI conversacional

**Documentação:**
- `core/docs/tools/cli.md` - CLI básico
- `core/docs/tools/conversational_cli.md` - CLI conversacional

**Solicitar quando:**
- Entender CLI
- Modificar automação

---

### TEMA: Infraestrutura e Utils

**Código:**
- `core/utils/event_bus/` - EventBus modularizado (comunicação CLI ↔ Dashboard)
  - `core.py` - Classe base com persistência
  - `publishers.py` - Métodos publish_*
  - `readers.py` - Métodos get_* e list_*
  - `singleton.py` - Classe EventBus completa e get_event_bus()
- `core/utils/event_models.py` - Modelos Pydantic de eventos
- `core/utils/cost_tracker.py` - Cálculo de custos
- `core/utils/token_extractor.py` - Extração de tokens
- `core/utils/json_parser.py` - Parser de JSON de LLM
- `core/prompts/` - Prompts dos agentes (modularizado por agente: methodologist.py, orchestrator.py, structurer.py)
- `core/utils/config.py` - Configurações e circuit breaker

**Documentação:**
- `core/docs/architecture/infrastructure/tech_stack.md` - Menciona EventBus

**Solicitar quando:**
- Entender infraestrutura de eventos
- Modificar métricas/custos
- Debugging de comunicação

**Gaps identificados:**
- ⚠️ `core/utils/config.py` - **GAP REAL**: Circuit breaker não encontrado na documentação
- ⚠️ `core/utils/json_parser.py` - **GAP REAL**: Parser JSON não encontrado na documentação

---

### TEMA: Configuração e Memória

**Código:**
- `core/agents/memory/config_loader.py` - Carregamento de configs YAML
- `core/agents/memory/config_validator.py` - Validação de schema YAML
- `core/agents/memory/memory_manager.py` - Gestão de memória por agente
- `core/agents/memory/execution_tracker.py` - Helper para captura de tokens
- `core/config/agents/*.yaml` - Configs externas por agente

**Documentação:**
- `core/docs/architecture/infrastructure/config_system.md` - **Sistema de configuração e memória** (YAML, loader, validator, memory_manager, execution_tracker)
- `docs/ARCHITECTURE.md` - Menciona sistema de configuração (seção "Configuração Externa de Agentes")

**Solicitar quando:**
- Modificar configuração de agentes
- Entender sistema de memória
- Debugging de tokens/custos
- Implementar parametrização de contexto de produto (Ensaio E-POC-2 / core C-ENSAIO-1)

---

### TEMA: Desenvolvimento e Processo

**Documentação:**
- `docs/process/refinement/` - Processo de refinement com Claude Web
- `docs/process/implementation/` - Processo de implementação (era development/)
- `docs/process/autonomous/` - Fluxo autônomo via Claude Code Web

**Solicitar quando:**
- Refinar épico (Claude Web) → `refinement/`
- Implementar código manualmente via Cursor → `implementation/`
- Disparar fluxo autônomo (Claude Code Web) → `autonomous/`
- Validar qualidade → `implementation/quality_rules.md`

---

### TEMA: Testes e Qualidade

**Código:**
- `tests/core/unit/` - Testes unitários do core (agents/, models/, memory/, utils/, database/)
- `tests/core/integration/` - Testes de integração do core
  - `smoke/` - Validação rápida
  - `behavior/` - Comportamentos específicos
  - `e2e/` - Cenários completos multi-turn
- `tests/products/<produto>/` - Testes específicos por produto (ex.: `tests/products/revelar/integration/`)
- `scripts/core/testing/` - Ferramentas de teste (execute_scenario.py, debug_scenario.py, replay_session.py)
- `scripts/core/health_checks/` - Health checks de setup
- `scripts/core/debug/` - Ferramentas de debug
- `scripts/core/spikes/`, `scripts/core/state_introspection/` - Exploração e inspeção
- `scripts/<produto>/flows/` - Scripts de validação manual por produto (ex.: `scripts/revelar/flows/`)

> **Nota:** Comandos em `docs/testing/commands.md` e `.github/workflows/` podem ainda referenciar `tests/unit/` e `tests/integration/` (migração para `tests/core/...` em andamento). Ao escrever testes novos, usar o layout `tests/core/...` e `tests/products/<produto>/...`.

**Documentação:**
- `docs/testing/README.md` - Índice e quick start
- `docs/testing/strategy.md` - Estratégia de testes (pirâmide, quando usar)
- `docs/testing/structure.md` - Estrutura de pastas detalhada
- `docs/testing/commands.md` - Comandos pytest
- `docs/testing/inventory.md` - Inventário de testes
- `docs/testing/migration/` - Histórico de reestruturação (Épico 8)
- `docs/testing/epics/` - Histórico de épicos de testes

**Solicitar quando:**
- Escrever novos testes
- Entender estrutura de testes
- Escolher entre unit/smoke/behavior/e2e
- Usar ferramentas de debug do Épico 8
- Troubleshooting de testes

**Observações:**
- Sistema reestruturado no Épico 8 (Dezembro 2025)
- 237 testes, 0 falhas
- Unit tests ($0) rodam em CI sempre
- Integration tests ($$) rodam manual ou CI seletivo
- Ferramentas de debug: replay, structured logging, debug reports

---

### TEMA: Produtos (Super-Sistema)

**Visão do super-sistema:**
- `core/docs/vision/super_system.md` - Como core e produtos se relacionam (desacoplamento, injeção de contexto de produto)

**Produto atual:**
- `products/revelar/README.md`, `ROADMAP.md`, `docs/vision.md`, `docs/interface/`, `docs/ux/`, `docs/use_cases.md`

**Próximo produto:**
- `products/ensaio/README.md`, `ROADMAP.md`, `docs/vision.md` - Transformar experimentos de código em artigos técnico-científicos (POC conversacional + Writer)

**Produtos planejados:**
- `products/prisma-verbal/` - Extração de conceitos de textos (fichamento)
- `products/camadas-da-linguagem/` - Ideia → Mensagem
- `products/expressao/` - Mensagem → Conteúdo (forma)
- `products/produtor-cientifico/` - Especialização acadêmica de Expressão (compartilha Writer com Ensaio)

**Solicitar quando:**
- Refinar funcionalidades específicas de produto
- Entender diferenças entre produtos
- Discutir o que é do core vs. o que é do produto

---

### TEMA: Exemplos

**Documentação:**
- `core/docs/examples/text_processing.md` - Exemplo de processamento (produto Fichamento)

**Solicitar quando:**
- Entender casos de uso práticos
- Ver exemplos de interação

---

## 🔍 RESUMO DE GAPS (Código Sem Documentação Técnica Detalhada)

### Críticos (Funcionalidades Importantes)
1. ⚠️ `products/revelar/app/components/session_helpers.py` - **GAP**: Helpers de sessão sem menção específica na documentação.

### Menores (Utils e Infraestrutura)
2. ⚠️ `core/utils/config.py` - **GAP**: Circuit breaker da API Anthropic não documentado.
3. ⚠️ `core/utils/json_parser.py` - **GAP**: Parser de JSON de respostas LLM não documentado.
4. ⚠️ `scripts/<produto>/flows/` - **GAP**: Scripts de validação manual (ex.: `scripts/revelar/flows/`) sem doc de propósito/uso.
5. ⚠️ `scripts/core/health_checks/` - **GAP**: Health checks do sistema sem documentação.

### ✅ NÃO SÃO GAPS (Documentados)
- ✅ `core/agents/structurer/` - Documentado em `core/docs/architecture/patterns/refinement.md`
- ✅ `core/agents/models/cognitive_model.py` - Documentado em `core/docs/vision/cognitive_model/` e `core/docs/architecture/data-models/argument_model.md`
- ✅ `core/agents/persistence/snapshot_manager.py` - Documentado em `core/docs/architecture/patterns/snapshots.md`
- ✅ `core/agents/memory/` - Documentado em `core/docs/architecture/infrastructure/config_system.md` (sistema YAML + memória + execution tracker)
- ✅ `core/agents/checklist/progress_tracker.py` - Documentado em `products/revelar/docs/interface/components.md` (seção 3.6)
- ✅ `products/revelar/app/pages/` - Documentado em `products/revelar/docs/interface/components.md` e `navigation_philosophy.md`
- ✅ `products/revelar/app/components/conversation_helpers.py` - Docstrings detalhadas no código
- ✅ `core/utils/event_bus/` - Docstrings detalhadas no código (estrutura modular)

---

## 📝 COMO USAR ESTE ÍNDICE

### Para Claude Web (Refinamento)
1. Sempre enviar **Contexto Obrigatório** (raiz + visão)
2. Solicitar temas específicos conforme necessidade
3. Exemplo: "Preciso do tema Orquestração" ou "Preciso entender Dados e Persistência"

### Para Claude Code (Implementação)
1. Contexto Obrigatório + tema relevante
2. Exemplo: Implementar feature de interface → Tema Interface Web
3. Exemplo: Modificar agente → Tema Agentes Específicos
4. Exemplo: Escrever testes → Tema Testes e Qualidade

### Formato de Solicitação
```
"Preciso do tema [NOME_DO_TEMA] para [MOTIVO]"
```

---

## 🎯 MAPA RÁPIDO DE DECISÃO

| Se você quer... | Solicite tema... |
|----------------|------------------|
| **Refinar épico novo** | Obrigatório (raiz + visão) |
| **Discutir comportamento do orquestrador** | Orquestração e Fluxo |
| **Implementar novo agente** | Agentes Específicos + Orquestração |
| **Modificar modelo de dados** | Dados e Persistência |
| **Implementar feature de interface** | Interface Web |
| **Escrever código** | Desenvolvimento e Processo |
| **Escrever testes** | Testes e Qualidade |
| **Entender infraestrutura** | Infraestrutura e Utils |

---

**Versão:** 2.0
**Para:** Organização temática de contexto e identificação de gaps. Promovido ao pack inicial de refinamento.

