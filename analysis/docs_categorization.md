# Categorização Completa de Documentação

**Data:** 2025-01-27  
**Objetivo:** Categorizar todos os diretórios em `docs/` como **core** (genérico) ou **revelar** (específico do produto Revelar)  
**Uso:** Referência para Fase 10 da migração (reorganização de documentação)

---

## Critérios de Categorização

### Core (genérico)
- Documentação de arquitetura genérica
- Design de agentes (independente do produto)
- Processos de desenvolvimento
- Visão de produto genérica
- Análises técnicas e estratégias

### Revelar (específico do produto)
- Documentação específica da interface web (Streamlit)
- Features específicas do produto Revelar
- Fluxos e componentes da interface

---

## Categorização por Diretório

### ✅ Core

#### `docs/architecture/` → `docs/core/architecture/`
**Categoria:** Core  
**Justificativa:** Documentação genérica de arquitetura, modelos, ontologia, tech stack. Não específico do produto Revelar.

**Conteúdo:**
- `argument_model.md` - Modelo genérico de argumentos
- `concept_model.md` - Modelo genérico de conceitos
- `idea_model.md` - Modelo genérico de ideias
- `observer_architecture.md` - Arquitetura do agente Observer
- `ontology.md` - Ontologia base
- `persistence_foundation.md` - Fundação de persistência
- `snapshot_strategy.md` - Estratégia de snapshots
- `super_system_vision.md` - Visão do super-sistema
- `tech_stack.md` - Stack tecnológico

---

#### `docs/agents/` → `docs/core/agents/`
**Categoria:** Core  
**Justificativa:** Documentação dos agentes (orchestrator, methodologist, observer, etc.) é genérica e compartilhável entre produtos.

**Conteúdo:**
- `communicator.md` - Agente Communicator
- `memory_agent.md` - Agente de Memória
- `methodologist_knowledge.md` - Conhecimento do Methodologist
- `methodologist.md` - Agente Methodologist
- `observer.md` - Agente Observer
- `orchestrator.md` - Agente Orchestrator
- `overview.md` - Visão geral dos agentes

---

#### `docs/testing/` → `docs/core/testing/`
**Categoria:** Core  
**Justificativa:** Estratégias, estrutura e processos de teste são genéricos. Resultados de épicos específicos podem ser mantidos como histórico, mas a metodologia é core.

**Conteúdo:**
- `README.md` - Índice e guidelines de teste
- `strategy.md` - Estratégia de testes (pirâmide)
- `structure.md` - Estrutura de testes
- `commands.md` - Comandos pytest
- `inventory.md` - Inventário de testes
- `migration/` - Histórico de migração de testes
- `epics/epic6/`, `epic7/`, `epic8/` - Histórico de épicos de teste
- `epic7_results/` - Resultados históricos (manter como referência)

---

#### `docs/orchestration/` → `docs/core/orchestration/`
**Categoria:** Core  
**Justificativa:** Documentação sobre orquestração de agentes é genérica e aplicável a qualquer produto que use o sistema multi-agente.

**Conteúdo:**
- `orchestrator.md` - Visão geral do orchestrator
- `refinement_loop.md` - Loop de refinamento
- `socratic_orchestrator.md` - Orchestrator socrático
- `conversational_orchestrator/` - Orchestrator conversacional (genérico)
- `multi_agent_architecture/` - Arquitetura multi-agente (genérico)

---

#### `docs/process/` → `docs/core/process/`
**Categoria:** Core  
**Justificativa:** Processos de desenvolvimento, workflows, guidelines são genéricos e compartilháveis.

**Conteúdo:**
- `current_implementation.md` - Estado atual da implementação
- `development/overview.md` - Visão geral de desenvolvimento
- `development/blockers.md` - Blockers técnicos
- `development/delivery.md` - Processo de entrega
- `development/implementation.md` - Processo de implementação
- `development/language_guidelines.md` - Guidelines de linguagem
- `development/quality_rules.md` - Regras de qualidade
- `development/workflow.md` - Workflow de desenvolvimento

---

#### `docs/vision/` → `docs/core/vision/`
**Categoria:** Core  
**Justificativa:** Visão de produto, epistemologia, modelos cognitivos são genéricos e formam a base filosófica do sistema, não específicos do Revelar.

**Conteúdo:**
- `vision.md` - Visão de produto (genérica)
- `epistemology.md` - Epistemologia do sistema
- `agent_personas.md` - Personas dos agentes
- `cognitive_model/` - Modelo cognitivo genérico
- `conversation_mechanics.md` - Padrões de conversação

---

#### `docs/analysis/` → `docs/core/analysis/`
**Categoria:** Core  
**Justificativa:** Análises técnicas, estratégias de migração, estimativas são documentação técnica genérica do projeto.

**Conteúdo:**
- `automation_strategy.md` - Estratégia de automação
- `debitos_tecnicos.md` - Débitos técnicos
- `eventbus_visualization_analysis.md` - Análise do EventBus
- `memory_agent_problem_statement.md` - Problema do agente de memória
- `migration_order.md` - Ordem de migração
- `risk_assessment.md` - Avaliação de riscos
- `time_estimation.md` - Estimativa de tempo
- `token_cost_optimization.md` - Otimização de custos

---

#### `docs/epics/` → `docs/core/epics/`
**Categoria:** Core  
**Justificativa:** Épicos são históricos de desenvolvimento genéricos. Pode haver épicos específicos do Revelar no futuro, mas os atuais são core.

**Conteúdo:**
- `epic-12-observer-integration.md` - Integração do Observer (core)

---

#### `docs/products/` → `docs/products/revelar/`
**Categoria:** Revelar  
**Justificativa:** Documentação específica dos produtos. `paper_agent.md` descreve o produto que se tornou Revelar.

**Ações:**
- `paper_agent.md` → `docs/products/revelar/paper_agent.md` (ou renomear para `revelar.md`)
- `fichamento.md` → `products/prisma-verbal/docs/vision.md` (movido para prisma-verbal)
- `examples/sapiens_processing.md` → `core/docs/examples/text_processing.md`

---

### ✅ Revelar (específico do produto)

#### `docs/interface/` → `docs/products/revelar/interface/`
**Categoria:** Revelar  
**Justificativa:** Documentação específica das interfaces do produto Revelar (CLI e Web).

**Conteúdo:**
- `cli.md` - Interface CLI do Revelar
- `conversational_cli.md` - CLI conversacional do Revelar
- `navigation_philosophy.md` - Filosofia de navegação da interface
- `products/revelar/docs/interface/overview.md` - Visão geral da interface web
- `products/revelar/docs/interface/components.md` - Componentes Streamlit
- `products/revelar/docs/interface/flows.md` - Fluxos da interface web

---

#### `docs/features/` → `docs/products/revelar/features/`
**Categoria:** Revelar  
**Justificativa:** Features específicas do produto Revelar.

**Conteúdo:**
- `transparent_backstage.md` - Feature "Bastidores Transparentes" (específico do Revelar)

---

## Arquivos na Raiz de `docs/`

### Core
- `backlog.md` → `docs/core/backlog.md` (backlog genérico do projeto)
- `CONTEXT_INDEX.md` → `docs/core/CONTEXT_INDEX.md` (índice de contexto)
- `maturity_checklist.md` → `docs/core/maturity_checklist.md` (checklist de maturidade)

---

## Resumo

### Total de Diretórios Analisados: 9

**Core (7 diretórios):**
1. ✅ `docs/architecture/` → `docs/core/architecture/`
2. ✅ `docs/agents/` → `docs/core/agents/`
3. ✅ `docs/testing/` → `docs/core/testing/`
4. ✅ `docs/orchestration/` → `docs/core/orchestration/`
5. ✅ `docs/process/` → `docs/core/process/`
6. ✅ `docs/vision/` → `docs/core/vision/`
7. ✅ `docs/analysis/` → `docs/core/analysis/`

**Revelar (2 diretórios):**
1. ✅ `docs/interface/` → `docs/products/revelar/interface/`
2. ✅ `docs/features/` → `docs/products/revelar/features/`

**Outros (1 diretório):**
1. ✅ `docs/epics/` → `docs/core/epics/` (core)
2. ✅ `docs/products/` → `docs/products/revelar/` (revelar)

---

## Próximos Passos (Fase 10)

1. Criar estrutura de diretórios:
   ```
   docs/core/
   docs/products/revelar/
   ```

2. Mover diretórios conforme categorização acima

3. Atualizar referências em:
   - Outros arquivos `.md`
   - `CONTEXT_INDEX.md`
   - Links internos entre documentos

4. Validar que nenhum link interno foi quebrado

