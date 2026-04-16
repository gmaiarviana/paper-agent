# Índice Temático de Contexto

> **Objetivo:** Mapear código → documentação e organizar contexto por temas (não sequencialmente)

---

## 🟢 CONTEXTO OBRIGATÓRIO (Sempre Enviar)

### Contexto Padronizado (Ver REFINEMENT_STARTER.md)
- `CONSTITUTION.md` - Princípios, responsabilidades, processo
- `ARCHITECTURE.md` - Decisões técnicas consolidadas  
- `core/ROADMAP.md` - Épicos e melhorias do core
- `products/<produto>/ROADMAP.md` - Épicos do produto específico (Revelar, Ensaio, etc.)

**Total obrigatório:** 4 arquivos (~1.200 linhas, ~5.000 tokens)

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
- `core/docs/architecture/agents/multi_agent/` - **FONTE ÚNICA DA VERDADE** para fluxo e estado
- `core/docs/architecture/agents/orchestrator/conversational/` - Orquestrador conversacional
- `core/docs/architecture/agents/orchestrator/socratic.md` - Orquestrador socrático
- `core/docs/architecture/patterns/refinement.md` - Loop de refinamento

**Solicitar quando:**
- Discutir fluxo de agentes
- Modificar comportamento do Orquestrador
- Entender MultiAgentState
- Implementar novo agente

---

### TEMA: Agentes Específicos

**Código:**
- `core/agents/methodologist/` - Metodologista (graph, nodes, router, state, tools, wrapper)
- `core/agents/structurer/nodes.py` - Estruturador
- `core/agents/models/cognitive_model.py` - Modelos Pydantic (CognitiveModel, Contradiction, SolidGround)

**Documentação:**
- `core/docs/agents/overview.md` - Visão geral de todos os agentes
- `core/docs/agents/methodologist.md` - Especificação do Metodologista
- `core/docs/agents/methodologist_knowledge.md` - Conhecimento do Metodologista
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
- `core/docs/architecture/vision/super_system.md` - Super-sistema

**Solicitar quando:**
- Modificar modelos de dados
- Entender ontologia do sistema
- Implementar persistência
- Discutir stack técnico

---

### TEMA: Interface Web

**Código:**
- `products/revelar/app/chat.py` - Interface principal
- `products/revelar/app/dashboard.py` - Dashboard de debug
- `products/revelar/app/components/` - Componentes (chat_input, chat_history, backstage, sidebar/, etc)
  - `sidebar/` - Sidebar modular (navigation, conversations, ideas)
- `products/revelar/app/pages/` - Páginas dedicadas (pensamentos, ideia_detalhes)

**Documentação:**
- `products/revelar/docs/interface/` - Especificação completa da interface web (overview.md, components.md, flows.md)
  - Seção 3.6: Painel Progress (Checklist) - documenta `progress_tracker.py`
- `products/revelar/docs/interface/navigation_philosophy.md` - Filosofia de navegação (3 espaços)

**Solicitar quando:**
- Implementar features de interface
- Modificar UX/UI
- Entender fluxo de navegação

**Gaps identificados:**
- ⚠️ `products/revelar/app/components/session_helpers.py` - **GAP REAL**: Não encontrei menção específica na documentação

---

### TEMA: CLI e Automação

**Codigo:**
- `core/tools/cli/chat.py` - CLI conversacional

**Documentação:**
- `docs/core/tools/cli.md` - CLI básico
- `docs/core/tools/conversational_cli.md` - CLI conversacional

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
- `ARCHITECTURE.md` - Menciona sistema de configuração (seção "Configuração Externa de Agentes")

**Solicitar quando:**
- Modificar configuração de agentes
- Entender sistema de memória
- Debugging de tokens/custos

**Gaps identificados:**
- ⚠️ Sistema de memória - **GAP REAL**: Mencionado em `ARCHITECTURE.md` (seção "Registro de Memória e Metadados") mas **sem doc técnica detalhada** dos componentes (`memory_manager.py`, `execution_tracker.py`, `config_loader.py`, `config_validator.py`)

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
- `tests/unit/` - Testes unitários organizados por categoria (226 testes)
  - `agents/` - Lógica de agentes (orchestrator, structurer, methodologist) - **Nota:** Ainda na raiz, será migrado para `tests/core/unit/agents/`
  - `models/` - Estruturas de dados (cognitive_model)
  - `memory/` - Sistema de memória (config_loader, execution_tracker, memory_manager)
  - `utils/` - Utilitários (cost_tracker, event_bus, json_extraction, currency) - **Nota:** Ainda na raiz, será migrado para `tests/core/unit/utils/`
  - `database/` - Database operations (database_manager)
- `tests/integration/` - Testes de integração (19 testes)
  - `smoke/` - Validação rápida (3 testes, ~$0.01)
  - `behavior/` - Comportamentos específicos (15 testes, ~$0.02-0.03)
  - `e2e/` - Cenários completos multi-turn (1 teste, ~$0.05)
- `scripts/testing/` - Ferramentas de teste (Épico 8)
  - `execute_scenario.py`, `debug_scenario.py`, `replay_session.py`
- `scripts/health_checks/` - Health checks de setup
- `scripts/debug/` - Ferramentas de debug

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

### TEMA: Produtos

**Documentação:**
- `products/produtor-cientifico/docs/vision.md` - Produtor Científico (produto atual)
- `products/prisma-verbal/docs/vision.md` - Fichamento (produto futuro)

**Solicitar quando:**
- Refinar funcionalidades específicas de produto
- Entender diferenças entre produtos

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
1. ⚠️ `products/revelar/app/components/session_helpers.py` - **GAP CONFIRMADO**: Helpers de sessão. Não encontrei menção específica na documentação.

### Menores (Utils e Infraestrutura)
2. ⚠️ `core/utils/config.py` - **GAP CONFIRMADO**: Circuit breaker da API Anthropic. Não encontrado na documentação.
3. ⚠️ `core/utils/json_parser.py` - **GAP CONFIRMADO**: Parser de JSON de respostas LLM. Não encontrado na documentação.
4. ⚠️ `core/agents/memory/` - **GAP CONFIRMADO**: Sistema de memória completo (`memory_manager.py`, `execution_tracker.py`, `config_loader.py`, `config_validator.py`). Mencionado em `ARCHITECTURE.md` mas sem doc técnica detalhada.
5. ⚠️ `scripts/flows/` - **GAP CONFIRMADO**: Scripts de validação manual. Listados em `testing/inventory.md` mas sem doc de propósito/uso.
6. ⚠️ `scripts/health_checks/` - **GAP CONFIRMADO**: Health checks do sistema. Não encontrado na documentação.

### ✅ NÃO SÃO GAPS (Documentados)
- ✅ `core/agents/structurer/` - Documentado em `refinement_loop.md`
- ✅ `core/agents/models/cognitive_model.py` - Documentado em `core/docs/vision/cognitive_model/` e `argument_model.md`
- ✅ `core/agents/persistence/snapshot_manager.py` - Documentado em `snapshot_strategy.md`
- ✅ `core/agents/checklist/progress_tracker.py` - Documentado em `web/components.md` (seção 3.6)
- ✅ `products/revelar/app/pages/` - Documentado em `web/components.md` e `navigation_philosophy.md`
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

**Versão:** 1.0  
**Data:** 2025-01-XX  
**Para:** Organização temática de contexto e identificação de gaps

