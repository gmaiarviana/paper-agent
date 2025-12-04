# Índice Temático de Contexto

> **Objetivo:** Mapear código → documentação e organizar contexto por temas (não sequencialmente)

---

## 🟢 CONTEXTO OBRIGATÓRIO (Sempre Enviar)

### Raiz (Definido no CONSTITUTION.md)
- `CONSTITUTION.md` - Princípios, responsabilidades, processo
- `ROADMAP.md` - Épicos, funcionalidades, status
- `ARCHITECTURE.md` - Decisões técnicas consolidadas
- `planning_guidelines.md` - Processo de refinamento
- `README.md` - Setup básico e interfaces

### Visão (Crítico - Onde Queremos Chegar)
- `docs/vision/vision.md` - Visão de produto, jornada do usuário, tipos de artigo
- `docs/vision/cognitive_model.md` - Como pensamento evolui (claim → fundamentos)
- `docs/vision/conversation_patterns.md` - Padrões de conversação esperados

**Total obrigatório:** ~2.000 linhas (~8.000 tokens)

---

## 📚 TEMAS INDEPENDENTES (Solicitar Conforme Necessidade)

Cada tema pode ser solicitado independentemente, sem ordem fixa.

---

### TEMA: Orquestração e Fluxo

**Código:**
- `agents/multi_agent_graph.py` - Super-grafo principal
- `agents/orchestrator/` - Orquestrador (nodes, router, state)
- `agents/orchestrator/state.py` - MultiAgentState (schema completo)

**Documentação:**
- `docs/orchestration/multi_agent_architecture.md` - **FONTE ÚNICA DA VERDADE** para fluxo e estado
- `docs/orchestration/conversational_orchestrator/` - Orquestrador conversacional
- `docs/orchestration/socratic_orchestrator.md` - Orquestrador socrático
- `docs/orchestration/refinement_loop.md` - Loop de refinamento
- `docs/orchestration/orchestrator.md` - Orquestrador (especificação adicional)

**Solicitar quando:**
- Discutir fluxo de agentes
- Modificar comportamento do Orquestrador
- Entender MultiAgentState
- Implementar novo agente

---

### TEMA: Agentes Específicos

**Código:**
- `agents/methodologist/` - Metodologista (graph, nodes, router, state, tools, wrapper)
- `agents/structurer/nodes.py` - Estruturador
- `agents/models/cognitive_model.py` - Modelos Pydantic (CognitiveModel, Contradiction, SolidGround)

**Documentação:**
- `docs/agents/overview.md` - Visão geral de todos os agentes
- `docs/agents/methodologist.md` - Especificação do Metodologista
- `docs/agents/methodologist_knowledge.md` - Conhecimento do Metodologista
- `docs/orchestration/refinement_loop.md` - **Estruturador documentado aqui** (processamento de feedback, lógica de refinamento)

**Solicitar quando:**
- Refinar comportamento de agente específico
- Implementar novo agente
- Entender responsabilidades de um agente

---

### TEMA: Dados e Persistência

**Código:**
- `agents/database/` - DatabaseManager, schema SQLite
- `agents/persistence/snapshot_manager.py` - Snapshots e detecção de maturidade
- `agents/checklist/progress_tracker.py` - Rastreamento de progresso
- `agents/models/cognitive_model.py` - Modelos de domínio

**Documentação:**
- `docs/architecture/ontology.md` - O que é Conceito, Ideia, Argumento
- `docs/architecture/idea_model.md` - Schema técnico de Ideia
- `docs/architecture/concept_model.md` - Schema técnico de Conceito
- `docs/architecture/argument_model.md` - Schema técnico de Argumento
- `docs/architecture/persistence_foundation.md` - Estratégia de persistência
- `docs/architecture/snapshot_strategy.md` - Estratégia de snapshots
- `docs/architecture/tech_stack.md` - Stack técnico (SQLite, ChromaDB)
- `docs/architecture/super_system_vision.md` - Super-sistema

**Solicitar quando:**
- Modificar modelos de dados
- Entender ontologia do sistema
- Implementar persistência
- Discutir stack técnico

---

### TEMA: Interface Web

**Código:**
- `app/chat.py` - Interface principal
- `app/dashboard.py` - Dashboard de debug
- `app/components/` - Componentes (chat_input, chat_history, backstage, sidebar, etc)
- `app/pages/` - Páginas dedicadas (pensamentos, ideia_detalhes)

**Documentação:**
- `docs/interface/web/` - Especificação completa da interface web (overview.md, components.md, flows.md)
  - Seção 3.4: Painel Progress (Checklist) - documenta `progress_tracker.py`
- `docs/interface/navigation_philosophy.md` - Filosofia de navegação (3 espaços)

**Solicitar quando:**
- Implementar features de interface
- Modificar UX/UI
- Entender fluxo de navegação

**Gaps identificados:**
- ⚠️ `app/components/session_helpers.py` - **GAP REAL**: Não encontrei menção específica na documentação

---

### TEMA: CLI e Automação

**Código:**
- `cli/chat.py` - CLI conversacional

**Documentação:**
- `docs/interface/cli.md` - CLI básico
- `docs/interface/conversational_cli.md` - CLI conversacional

**Solicitar quando:**
- Entender CLI
- Modificar automação

---

### TEMA: Infraestrutura e Utils

**Código:**
- `utils/event_bus.py` - EventBus (comunicação CLI ↔ Dashboard)
- `utils/event_models.py` - Modelos Pydantic de eventos
- `utils/cost_tracker.py` - Cálculo de custos
- `utils/token_extractor.py` - Extração de tokens
- `utils/json_parser.py` - Parser de JSON de LLM
- `utils/prompts/` - Prompts dos agentes (modularizado por agente: methodologist.py, orchestrator.py, structurer.py)
- `utils/config.py` - Configurações e circuit breaker

**Documentação:**
- `docs/architecture/tech_stack.md` - Menciona EventBus

**Solicitar quando:**
- Entender infraestrutura de eventos
- Modificar métricas/custos
- Debugging de comunicação

**Gaps identificados:**
- ⚠️ `utils/config.py` - **GAP REAL**: Circuit breaker não encontrado na documentação
- ⚠️ `utils/json_parser.py` - **GAP REAL**: Parser JSON não encontrado na documentação

---

### TEMA: Configuração e Memória

**Código:**
- `agents/memory/config_loader.py` - Carregamento de configs YAML
- `agents/memory/config_validator.py` - Validação de schema YAML
- `agents/memory/memory_manager.py` - Gestão de memória por agente
- `agents/memory/execution_tracker.py` - Helper para captura de tokens
- `config/agents/*.yaml` - Configs externas por agente

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
- `docs/process/development/overview.md` - Visão geral
- `docs/process/development/workflow.md` - Workflow
- `docs/process/development/quality_rules.md` - Regras de qualidade
- `docs/process/development/language_guidelines.md` - Guidelines de linguagem
- `docs/process/development/implementation.md` - Processo de implementação
- `docs/process/development/delivery.md` - Processo de entrega
- `docs/process/development/blockers.md` - Bloqueadores

**Solicitar quando:**
- Implementar código (Claude Code)
- Entender processo de desenvolvimento
- Validar qualidade

---

### TEMA: Testes

**Código:**
- `tests/unit/` - Testes unitários
- `tests/integration/` - Testes de integração
- `scripts/flows/` - Scripts de validação manual
- `scripts/health_checks/` - Health checks

**Documentação:**
- `docs/testing/README.md` - Visão geral
- `docs/testing/strategy.md` - Estratégia de testes
- `docs/testing/structure.md` - Estrutura de testes
- `docs/testing/inventory.md` - Inventário de testes
- `docs/testing/commands.md` - Comandos de teste

**Solicitar quando:**
- Escrever testes
- Entender estratégia de testes
- Validar cobertura

**Gaps identificados:**
- ⚠️ `scripts/flows/` - Scripts de validação (não encontrei doc)
- ⚠️ `scripts/health_checks/` - Health checks (não encontrei doc)

---

### TEMA: Produtos

**Documentação:**
- `docs/products/paper_agent.md` - Paper-agent (produto atual)
- `docs/products/fichamento.md` - Fichamento (produto futuro)

**Solicitar quando:**
- Refinar funcionalidades específicas de produto
- Entender diferenças entre produtos

---

### TEMA: Exemplos

**Documentação:**
- `docs/examples/sapiens_processing.md` - Exemplo de processamento

**Solicitar quando:**
- Entender casos de uso práticos
- Ver exemplos de interação

---

## 🔍 RESUMO DE GAPS (Código Sem Documentação Técnica Detalhada)

### Críticos (Funcionalidades Importantes)
1. ⚠️ `app/components/session_helpers.py` - **GAP CONFIRMADO**: Helpers de sessão. Não encontrei menção específica na documentação.

### Menores (Utils e Infraestrutura)
2. ⚠️ `utils/config.py` - **GAP CONFIRMADO**: Circuit breaker da API Anthropic. Não encontrado na documentação.
3. ⚠️ `utils/json_parser.py` - **GAP CONFIRMADO**: Parser de JSON de respostas LLM. Não encontrado na documentação.
4. ⚠️ `agents/memory/` - **GAP CONFIRMADO**: Sistema de memória completo (`memory_manager.py`, `execution_tracker.py`, `config_loader.py`, `config_validator.py`). Mencionado em `ARCHITECTURE.md` mas sem doc técnica detalhada.
5. ⚠️ `scripts/flows/` - **GAP CONFIRMADO**: Scripts de validação manual. Listados em `testing/inventory.md` mas sem doc de propósito/uso.
6. ⚠️ `scripts/health_checks/` - **GAP CONFIRMADO**: Health checks do sistema. Não encontrado na documentação.

### ✅ NÃO SÃO GAPS (Documentados)
- ✅ `agents/structurer/` - Documentado em `refinement_loop.md`
- ✅ `agents/models/cognitive_model.py` - Documentado em `cognitive_model.md` e `argument_model.md`
- ✅ `agents/persistence/snapshot_manager.py` - Documentado em `snapshot_strategy.md`
- ✅ `agents/checklist/progress_tracker.py` - Documentado em `web/components.md` (seção 3.6)
- ✅ `app/pages/` - Documentado em `web/components.md` e `navigation_philosophy.md`
- ✅ `app/components/conversation_helpers.py` - Docstrings detalhadas no código
- ✅ `utils/event_bus.py` - Docstrings detalhadas no código

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
| **Escrever testes** | Testes |
| **Entender infraestrutura** | Infraestrutura e Utils |

---

**Versão:** 1.0  
**Data:** 2025-01-XX  
**Para:** Organização temática de contexto e identificação de gaps

