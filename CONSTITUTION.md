# Paper Agent - Constitution

Princípios não-negociáveis para trabalhar com este projeto.

---

## 1. PRINCÍPIOS DE TRABALHO

### Como Refinamos
- POC → Protótipo → MVP (incremental)
- Discussão > especulação antecipada
- Épicos refinados apenas quando prioritários
- Funcionalidades detalhadas aceleram implementação

### Como Implementamos
- Claude web refina → Cursor atualiza docs → Claude Code implementa
- TDD pragmático (lógica crítica sim, UI não)
- Validação incremental obrigatória
- Commits estratégicos (não obrigatórios)

### Fluxos Disponíveis
Dois modos coexistem; o dev escolhe por funcionalidade:

- **Manual (Cursor):** dev acompanha cada checkpoint. Indicado para épicos novos, decisões arquiteturais ou trade-offs em aberto. Fluxo descrito nas seções 2-7 deste documento.
- **Autônomo (Claude Code Web):** dev dispara pela manhã e valida à noite; skills automáticas (Planning → Dev → QA → TL → PO → Validation) atuam como gates no lugar das aprovações explícitas. Indicado para funcionalidades já refinadas e claras. Detalhes em `docs/process/autonomous/` e template em `AUTONOMOUS_DISPATCH.md` (raiz).

Princípios, responsabilidades e anti-padrões deste documento valem para os dois modos.

---

## 2. RESPONSABILIDADES

### Claude Web (Consultor Estratégico)
**Papel:** Refinar épicos, discutir comportamentos, gerar prompts.

**Deve:**
- ✅ Ler contexto completo (4 arquivos da raiz)
- ✅ Consultar docs adicionais via mapa (pull sob demanda)
- ✅ Perguntar clarificações necessárias
- ✅ Oferecer opções + recomendação (balizada por vision.md + guidelines)
- ✅ Gerar múltiplos prompts (1 por arquivo a atualizar)
- ✅ Manter padrões existentes nos prompts

**Não deve:**
- ❌ Atualizar documentações diretamente
- ❌ Implementar código
- ❌ Assumir preferências sem base em vision/guidelines

### Cursor (Atualizador de Documentações)
**Papel:** Aplicar prompts gerados pelo Claude web nas documentações.

**Deve:**
- ✅ Seguir prompts com liberdade de pensamento (ganhar tokens)
- ✅ Manter formatação markdown existente
- ✅ Preservar padrões de escrita
- ✅ Não criar arquivos extras sem permissão

**Não deve:**
- ❌ Alterar estrutura sem instruções explícitas
- ❌ Criar documentação extra (README, resumos, etc)

### Claude Code (Implementador)
**Papel:** Implementar código baseado em documentações atualizadas.

**Deve:**
- ✅ Seguir docs/process/implementation/ (guidelines)
- ✅ Seguir `docs/testing/strategy.md` para pirâmide de testes, markers (`integration`, `slow`) e política de uso da API real
- ✅ Ler ROADMAP.md + specs técnicas
- ✅ TDD onde aplicável
- ✅ Validar incrementalmente
- ✅ Atualizar docs se mudou estrutura

**Não deve:**
- ❌ Refinar épicos
- ❌ Tomar decisões arquiteturais sem base

---

## 3. PROCESSO DE REFINAMENTO

### Input Esperado (você fornece)
- Comportamento desejado OU problema existente
- Contexto: épico novo, ajuste, discussão

### Claude Web Deve:

**1. Análise Contextual**
- Consultar `products/<produto>/docs/vision.md` (expectativas do produto em refinamento)
- Consultar ROADMAP.md do produto + `core/ROADMAP.md` (épicos anteriores, padrões)
- Consultar `docs/process/refinement/planning_guidelines.md` (processo)
- Consultar docs técnicas via `docs/CONTEXT_INDEX.md` (se necessário)
- Identificar onde comportamento está documentado (OU pedir pra ver)

**2. Clarificação**
- Fazer perguntas específicas
- Validar entendimento
- Apontar trade-offs técnicos

**3. Recomendação**
- Oferecer opções (A, B, C)
- Recomendar baseado em vision.md + guidelines
- Justificar recomendação

**4. Gerar Prompts**
- Múltiplos prompts (1 por arquivo)
- Ordem de execução clara
- Instruções enxutas (Cursor pensa também)
- Manter padrões existentes

**5. Validação**
- Confirmar que prompts fazem sentido
- Verificar se nada foi esquecido

### Output Esperado (Claude web gera)
PROMPT 1: ROADMAP.md
[instruções enxutas pro Cursor]
PROMPT 2: core/docs/architecture/agents/orchestrator/conversational/README.md
[instruções enxutas pro Cursor]
PROMPT 3: ARCHITECTURE.md
[instruções enxutas pro Cursor]

---

## 4. O QUE PROPOR (Guidelines de Recomendação)

### Ao Refinar Épico Novo
- ✅ Consultar `products/<produto>/docs/vision.md` (visão, tipos de saída, jornada do usuário)
- ✅ Consultar ROADMAP.md do produto (épicos anteriores - manter padrão)
- ✅ Propor funcionalidades detalhadas (critérios de aceite claros)
- ✅ Perguntar sobre trade-offs técnicos (performance vs simplicidade)
- ✅ Sugerir divisão POC → Protótipo → MVP

### Ao Discutir Comportamento Existente
- ✅ Identificar onde está documentado (via mapa)
- ✅ Analisar impacto da mudança (quais docs precisam atualizar)
- ✅ Propor mudança arquitetural OU ajuste de spec (dependendo do impacto)
- ✅ Gerar prompts pra todos os arquivos afetados

### Ao Propor Melhorias
- ✅ Ser proativo quando guidelines são claros
- ✅ Ser reativo (oferecer opções) quando trade-offs existem
- ✅ Sempre justificar com base em vision.md ou guidelines

---

## 5. MAPA DE DECISÃO

| Se você quer... | Claude web consulta... | Gera prompts para... |
|----------------|----------------------|---------------------|
| **Refinar épico novo** | `products/<produto>/docs/vision.md` + core/ROADMAP.md + products/<produto>/ROADMAP.md + ARCHITECTURE.md | core/ROADMAP.md ou products/<produto>/ROADMAP.md + docs da spec técnica nova (ver `docs/CONTEXT_INDEX.md`) |
| **Discutir comportamento do orquestrador** | `core/docs/architecture/agents/orchestrator/conversational/` + `products/<produto>/docs/ux/conversation_patterns.md` (quando existir) | `conversational/README.md` + ROADMAP.md + ARCHITECTURE.md |
| **Discutir comportamento de agente** | `core/docs/agents/<agente>.md` (responsabilidades) + `core/docs/architecture/agents/multi_agent/` (design técnico) | `core/docs/agents/<agente>.md` + ROADMAP.md + ARCHITECTURE.md |
| **Ajustar fluxo de dados** | `core/docs/architecture/agents/multi_agent/` + ARCHITECTURE.md | `multi_agent/` + ARCHITECTURE.md |
| **Mudar interface** | `products/<produto>/docs/interface/` OU `core/docs/tools/cli.md` + ARCHITECTURE.md | `products/<produto>/docs/interface/` (overview.md, components.md, flows.md) ou `core/docs/tools/cli.md` + ROADMAP.md + ARCHITECTURE.md |
| **Revisar processo de refinamento** | `docs/process/refinement/planning_guidelines.md` (já tem no contexto) | `docs/process/refinement/planning_guidelines.md` + CONSTITUTION.md (se princípios mudarem) |
| **Revisar processo de implementação** | `docs/process/implementation/*.md` | `docs/process/implementation/*.md` (não é seu escopo principal) |

---

## 6. ANTI-PADRÕES (O QUE NÃO FAZER)

### ❌ Duplicar Informação
- Cada info vive em 1 lugar só
- Outros fazem referência ("Ver detalhes em...")
- Não copiar specs entre docs

### ❌ Atualizar Diretamente
- Claude web NÃO atualiza docs (gera prompts)
- Cursor atualiza docs (executa prompts)
- Claude Code atualiza código (+ docs estruturais se mudar)

### ❌ Assumir sem Base
- Sempre consultar `products/<produto>/docs/vision.md` + guidelines
- Perguntar se incerto
- Não inventar padrões

### ❌ Prompts Verbosos
- Enxuto > detalhado (Cursor pensa também)
- Instruções claras suficiente
- Evitar micro-gerenciamento

---

## 7. DOCUMENTOS ESSENCIAIS

### Contexto Inicial Padronizado

**Ver REFINEMENT_STARTER.md (raiz) para lista autoritativa.**

Resumo: 4 arquivos genéricos + 2 específicos do produto = 6 arquivos total.

**Como enviar:** Conforme produto que está refinando, arraste os 6 arquivos listados no REFINEMENT_STARTER.md.

### Processo de Refinamento

- **Processo completo:** `docs/process/refinement/planning_guidelines.md` (movido da raiz)
- **Visão geral:** `docs/process/refinement/overview.md`
- **Starter pack:** `REFINEMENT_STARTER.md` (raiz)

### Consultados Via Mapa (`docs/CONTEXT_INDEX.md` - sob demanda)

**Produto (estratégia):**
- `products/<produto>/docs/vision.md` - Visão, jornada do usuário, expectativas
- `products/<produto>/docs/ux/conversation_patterns.md` - Padrões esperados de interação (quando existir)

**Specs Técnicas (detalhes):**
- `core/docs/agents/` - Responsabilidades de cada agente (quem faz o quê)
- `core/docs/architecture/agents/` - Design técnico dos agentes (multi_agent, orchestrator, observer, writer)
- `core/docs/architecture/data-models/` - Ontologia e modelos de dados
- `core/docs/architecture/patterns/` - Padrões transversais (refinement, snapshots)
- `core/docs/architecture/infrastructure/` - Stack técnico e sistemas transversais
- `products/<produto>/docs/interface/` - Specs de interface do produto (quando existir)
- `core/docs/tools/` - CLI e ferramentas

**Processo (desenvolvimento):**
- `docs/process/implementation/` - Para Claude Code (implementação)
- `docs/process/autonomous/` - Para Claude Code Web (fluxo autônomo)
- `docs/testing/` - Estratégia de testes

**Outros:**
- `docs/backlog.md` - Ideias futuras (não essencial)

---

## 8. ESTRUTURA DO PROJETO (Resumida)

> **Mapa detalhado código↔doc:** `docs/CONTEXT_INDEX.md` (no pack inicial)

```
paper-agent/
├── CONSTITUTION.md                  # 🔴 ESSENCIAL - Princípios e processo (este arquivo)
├── ARCHITECTURE.md                  # 🔴 ESSENCIAL - Decisões técnicas consolidadas
├── REFINEMENT_STARTER.md            # 🔴 ESSENCIAL - Lista autoritativa do pack de contexto
├── AUTONOMOUS_DISPATCH.md           # Template de disparo autônomo (Claude Code Web)
├── README.md                        # 🟢 USUÁRIOS - Setup básico
│
├── core/                            # Sistema universal compartilhado
│   ├── README.md                    # Visão do core
│   ├── ROADMAP.md                   # 🔴 ESSENCIAL - Épicos do core
│   ├── agents/                      # Código dos agentes (orchestrator, methodologist, observer, structurer, memory, database, persistence, checklist, models)
│   ├── prompts/                     # Prompts por agente
│   ├── config/agents/*.yaml         # Config externa por agente
│   ├── skills/                      # Skills PO/QA/TL/Planning/Validation (modo autônomo)
│   ├── tools/cli/                   # CLI conversacional
│   ├── utils/                       # EventBus, cost_tracker, json_parser, config (circuit breaker)
│   └── docs/
│       ├── vision/                  # Filosofia (system_philosophy, epistemology, cognitive_model, ...)
│       ├── agents/                  # Responsabilidades dos agentes (overview, orchestrator, methodologist, observer, researcher, memory_agent, communicator)
│       ├── architecture/
│       │   ├── agents/              # Design técnico (multi_agent/, orchestrator/, observer/, writer.md)
│       │   ├── data-models/         # Ontologia, idea/concept/argument, persistence
│       │   ├── patterns/            # refinement.md, snapshots.md
│       │   ├── infrastructure/      # tech_stack.md, config_system.md (memória/YAML)
│       │   └── vision/              # super_system.md
│       ├── tools/                   # cli.md, conversational_cli.md
│       ├── features/                # transparent_backstage.md
│       └── examples/                # Exemplos práticos
│
├── products/                        # Aplicações específicas (app próprio por produto)
│   ├── revelar/                     # (atual) Chat para clareza de pensamento
│   │   ├── README.md, ROADMAP.md
│   │   ├── app/                     # Streamlit (chat.py, dashboard.py, components/, pages/)
│   │   └── docs/                    # vision.md, interface/, ux/, use_cases.md
│   ├── ensaio/                      # (próximo) Experimento → artigo técnico-científico
│   │   ├── README.md, ROADMAP.md
│   │   └── docs/vision.md
│   ├── prisma-verbal/               # (futuro) Extração de conceitos de textos
│   ├── camadas-da-linguagem/        # (futuro) Ideia → Mensagem
│   ├── expressao/                   # (futuro) Mensagem → Conteúdo
│   └── produtor-cientifico/         # (futuro) Artigo acadêmico (especialização)
│
├── docs/                            # Meta-docs do repo (transversais aos produtos)
│   ├── CONTEXT_INDEX.md             # 🔴 ESSENCIAL - Mapa temático código↔doc
│   ├── backlog.md                   # Melhorias técnicas não vinculadas a épicos
│   ├── maturity_checklist.md
│   ├── analysis/                    # débitos técnicos, otimização de custo
│   ├── process/
│   │   ├── refinement/              # Refinamento (planning_guidelines.md + overview.md)
│   │   ├── implementation/          # Implementação manual via Cursor
│   │   └── autonomous/              # Fluxo autônomo via Claude Code Web
│   └── testing/                     # Estratégia, estrutura, comandos, inventário
│
├── tests/                           # tests/core/{unit,integration} e tests/products/<produto>/
└── scripts/                         # scripts/core/{debug,health_checks,spikes,state_introspection,testing} e scripts/<produto>/
```

**Legenda:** 🔴 no pack inicial de contexto | 🟢 para humanos/setup.

---

**Versão:** 1.0  
**Data:** 15/11/2025  
**Para:** Claude Web (consultor estratégico de refinamento)

