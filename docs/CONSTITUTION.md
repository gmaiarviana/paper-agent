# Paper Agent - Constitution

Princípios não-negociáveis para trabalhar com este projeto.

---

## 1. PRINCÍPIOS DE TRABALHO

### Como Refinamos
- POC → Protótipo → MVP (incremental)
- Discussão > especulação antecipada
- Épicos percorrem até seis estados no ROADMAP: `🌱 Visão` → `📐 Funcionalidades esboçadas` → `📋 Critérios definidos` → `🔍 Detalhes definidos` → `🏗️ Em andamento` → `✅ Implementado`. Modelo completo em `docs/process/refinement/planning_guidelines.md`.
- Toda sessão de refinamento começa com um **alvo declarado** (o estado ao qual o épico deve chegar). O Claude Web conduz as perguntas até atingir o alvo, sem parar em estados intermediários.
- Alvo `📋 Critérios definidos` basta para o fluxo manual via Cursor.
- Alvo `🔍 Detalhes definidos` é pré-requisito do fluxo autônomo; guiado pelo checklist em `docs/process/refinement/autonomous_readiness.md`. Aplicado sob demanda para o épico específico que vai ser disparado.
- Fechamento do épico (extração de conhecimento permanente + poda do ROADMAP) segue `docs/process/refinement/epic_completion.md` antes de marcar como `✅ Implementado`.
- Funcionalidades detalhadas aceleram implementação.

### Como Implementamos
- Claude web refina → Cursor atualiza docs → Claude Code implementa
- TDD pragmático (lógica crítica sim, UI não)
- Validação incremental obrigatória
- Commits estratégicos (não obrigatórios)

### Fluxos Disponíveis
Dois modos coexistem; o dev escolhe por funcionalidade. Cada modo exige um estado mínimo do épico no ROADMAP:

- **Manual (Cursor):** estado mínimo `📋 Critérios definidos`. Dev acompanha cada checkpoint. Indicado para épicos novos, decisões arquiteturais ou trade-offs ainda em aberto durante a implementação. Fluxo descrito nas seções 2-7 deste documento.
- **Autônomo (Claude Code Web):** estado mínimo `🔍 Detalhes definidos` (checklist de `autonomous_readiness.md` aplicado). Dev dispara pela manhã e valida à noite; skills automáticas (Planning → Dev → QA → TL → PO → Validation) atuam como gates no lugar das aprovações explícitas. Indicado para funcionalidades com detalhes de execução fechados. Detalhes em `docs/process/autonomous/` e template em `docs/process/autonomous/dispatch.md`.

Épicos em `🌱 Visão` ou `📐 Funcionalidades esboçadas` passam por sessão de refinamento com alvo `📋` ou `🔍` antes de qualquer fluxo de execução.

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
- ❌ Refinar épicos (refinamento em qualquer alvo — `📋 Critérios definidos` ou `🔍 Detalhes definidos` — é manual, via Claude Web)
- ❌ Tomar decisões arquiteturais sem base

---

## 3. PROCESSO DE REFINAMENTO

### Input Esperado (você fornece)
- Comportamento desejado OU problema existente
- Contexto: épico novo, ajuste, discussão

### Claude Web Deve:

**1. Análise Contextual**
- Consultar `products/<produto>/docs/vision.md` (expectativas do produto em refinamento)
- Consultar ROADMAP.md do produto + `docs/ROADMAP.md` (épicos anteriores, padrões)
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
PROMPT 2: core/docs/agents/orchestrator/conversational/README.md
[instruções enxutas pro Cursor]
PROMPT 3: docs/ARCHITECTURE.md
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

Mapa único vive em `docs/CONTEXT_INDEX.md` (já no pack inicial):

- **Por tema** → seções `## TEMA: ...` com "Solicitar quando..." em cada uma.
- **Resumo rápido** → tabela `🎯 MAPA RÁPIDO DE DECISÃO` no fim do arquivo.

Ao refinar: identifique o tema relevante no CONTEXT_INDEX e peça os paths listados ali. Para os arquivos-alvo de prompts (onde escrever), ver também ROADMAP do produto + `docs/ARCHITECTURE.md`.

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

**Ver `docs/process/refinement/starter.md` para lista autoritativa.**

Resumo: 4 arquivos genéricos + 2 específicos do produto = 6 arquivos total.

**Como enviar:** Conforme produto que está refinando, arraste os 6 arquivos listados no starter.

### Processo de Refinamento

- **Processo completo:** `docs/process/refinement/planning_guidelines.md`
- **Visão geral:** `docs/process/refinement/overview.md`
- **Starter pack:** `docs/process/refinement/starter.md`
- **Checklist de entrada para `🔍 Detalhes definidos`:** `docs/process/refinement/autonomous_readiness.md`
- **Checklist de saída (fechamento do épico):** `docs/process/refinement/epic_completion.md`

### Consultados Sob Demanda

Tudo fora do pack inicial — specs técnicas, filosofia, interface, processo (inclusive `autonomous_readiness.md` quando um épico é preparado para o fluxo autônomo, e `epic_completion.md` no fechamento), testes — está mapeado em `docs/CONTEXT_INDEX.md` (já no pack inicial). Não duplicar a lista aqui.

---

## 8. ESTRUTURA DO PROJETO (Resumida)

> **Mapa detalhado código↔doc:** `docs/CONTEXT_INDEX.md` (no pack inicial)

```
paper-agent/
├── README.md                        # 🟢 USUÁRIOS - Setup básico
│
├── docs/                            # 🟢 PACK INICIAL do Claude Web (tudo o que se carrega antes)
│   ├── CONSTITUTION.md              # 🔴 ESSENCIAL - Princípios e processo (este arquivo)
│   ├── ARCHITECTURE.md              # 🔴 ESSENCIAL - Decisões técnicas consolidadas
│   ├── ROADMAP.md                   # 🔴 ESSENCIAL - Épicos do core
│   ├── CONTEXT_INDEX.md             # 🔴 ESSENCIAL - Mapa temático código↔doc
│   ├── backlog.md, maturity_checklist.md
│   ├── analysis/                    # Análises meta (débitos técnicos, otimização)
│   ├── process/
│   │   ├── refinement/              # Processo de refinement + starter.md
│   │   ├── implementation/          # Processo de implementação manual
│   │   └── autonomous/              # Fluxo autônomo + dispatch.md
│   └── testing/                     # Estratégia, estrutura, comandos de teste
│
├── core/                            # Sistema universal compartilhado (runtime do produto)
│   ├── README.md                    # Visão do core
│   ├── agents/                      # Código dos agentes (orchestrator, methodologist, observer, structurer, memory, database, persistence, checklist, models)
│   ├── prompts/                     # Prompts por agente
│   ├── config/agents/*.yaml         # Config externa por agente
│   ├── tools/cli/                   # CLI conversacional
│   ├── utils/                       # EventBus, cost_tracker, json_parser, config (circuit breaker)
│   └── docs/                        # 🟡 DETALHE SOB DEMANDA (carregado conforme tema)
│       ├── vision/                  # Filosofia + super_system (cognitive_model, epistemology, ...)
│       ├── agents/                  # Pasta por agente (responsibilities.md + design.md/architecture.md)
│       ├── architecture/
│       │   ├── multi_agent/         # Super-grafo (state, graph, nodes, flows, config, prompts, evolution)
│       │   ├── data-models/         # Ontologia, idea/concept/argument, persistence
│       │   ├── patterns/            # refinement.md, snapshots.md
│       │   └── infrastructure/      # tech_stack.md, config_system.md (memória/YAML)
│       ├── tools/                   # cli.md, conversational_cli.md
│       ├── features/                # transparent_backstage.md
│       └── examples/                # Exemplos práticos
│
├── skills/                          # Skills do modo autônomo (Planning/QA/TL/PO/Validation) — processo de dev, NÃO runtime do produto
│   ├── README.md                    # Índice + como o Claude Web carrega cada skill
│   ├── planning/                    # Gate 1 — quebra funcionalidade em tasks
│   ├── qa/                          # Gate 3 — valida testes, sintaxe, imports
│   ├── tl/                          # Gate 4 — valida arquitetura e padrões
│   ├── po/                          # Gate 5 — valida critérios de aceite
│   └── validation/                  # Gate 6 — prepara branch + comandos p/ dev
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
├── tests/                           # tests/core/{unit,integration} e tests/products/<produto>/
└── scripts/                         # scripts/core/{debug,health_checks,spikes,testing} e scripts/<produto>/
```

**Legenda:** 🔴 no pack inicial de contexto | 🟢 para humanos/setup.

---

**Versão:** 1.0  
**Data:** 15/11/2025  
**Para:** Claude Web (consultor estratégico de refinamento)

