# Paper Agent - Constitution

Princípios não-negociáveis para trabalhar com este projeto.

---

## 1. PRINCÍPIOS DE TRABALHO

### Unidade de Entrega
- **Fluxo autônomo: milestone.** Um **milestone** agrupa épicos relacionados dentro de um estágio (POC, Protótipo, MVP). Um estágio pode ter 1 ou N milestones. Um milestone fecha quando todos os seus épicos caem na branch do milestone, validados pelos gates automáticos, e recebem aval humano.
- **Fluxo manual via Cursor: funcionalidade/épico.** O fluxo manual segue operando no grão de funcionalidade dentro de épico, como ferramenta complementar ao autônomo.
- Estágio, milestone, épico e funcionalidade são definidos no Glossário ao fim deste documento.

### Como Refinamos
- POC → Protótipo → MVP (incremental)
- Discussão > especulação antecipada
- Épicos percorrem até oito estados no ROADMAP: `🌱 Visão` → `🧭 Jornada alinhada` → `📐 Funcionalidades esboçadas` → `📋 Critérios definidos` → `🔍 Detalhes definidos` → `🏗️ Em andamento` → `🔀 Em revisão` → `✅ Implementado`. Modelo completo em `docs/process/refinement/planning_guidelines.md`.
- Toda sessão de refinamento opera com um **alvo definido** (o estado ao qual o épico deve chegar). O alvo pode ser declarado pelo usuário ao abrir a sessão ou inferido pelo refinador a partir da camada que ainda não está clara e confirmado antes do primeiro edit (não é gate de abertura). Uma vez definido, o refinador — Claude Web (estratégico) ou PM skill (tático, dentro da branch do milestone) — conduz as perguntas até atingir o alvo, sem parar em estados intermediários.
- Alvo `📋 Critérios definidos` basta para o fluxo manual.
- Alvo `🔍 Detalhes definidos` é pré-requisito do fluxo autônomo; guiado pelo checklist em `docs/process/refinement/autonomous_readiness.md`. Aplicado sob demanda, épico a épico — pelo Claude Web antes do milestone existir, ou pela PM skill dentro da branch do milestone quando o milestone é disparado com épicos ainda em `🌱` ou `📐`.
- Fechamento do épico (extração de conhecimento permanente + poda do ROADMAP) segue `docs/process/refinement/epic_completion.md` antes de marcar como `✅ Implementado`.
- Funcionalidades detalhadas aceleram implementação.

### Como Implementamos
- Refinamento estratégico (visão → milestones → épicos) via Claude Web → docs atualizadas → fluxo manual via Cursor (grão de funcionalidade) OU fluxo autônomo via Claude Code Web (grão de milestone)
- Milestone disparado por linguagem natural ("implementa a POC do Ensaio") entra em branch própria `milestone/<id-em-caixa-baixa>`; main só recebe milestone com aval humano
- TDD pragmático (lógica crítica sim, UI não)
- Validação incremental obrigatória
- Commits estratégicos (não obrigatórios)

**Tipos de sessão:**
- **Sessão de implementação** — autônoma; produz código e docs; encerra com PR criada pela RTE. Detalhes: `docs/process/autonomous/workflow.md`.
- **Sessão de refinamento** — colaborativa (operador + agente); produz atualizações de ROADMAP; encerra com rito de encerramento de sessão (`docs/process/refinement/planning_guidelines.md`).

### Fluxos Disponíveis
Dois modos coexistem; o dev escolhe por funcionalidade. Cada modo exige um estado mínimo do épico no ROADMAP:

- **Manual (Cursor):** estado mínimo `📋 Critérios definidos`. Dev acompanha cada checkpoint. Indicado para épicos novos, decisões arquiteturais ou trade-offs ainda em aberto durante a implementação. Fluxo descrito nas seções 2-7 deste documento.
- **Autônomo (Claude Code Web):** estado mínimo `🔍 Detalhes definidos` (checklist de `autonomous_readiness.md` aplicado). Dev dispara pela manhã e valida à noite; skills automáticas (Scrum Master → Dev → QA → TL → PO → RTE) atuam como gates no lugar das aprovações explícitas. Indicado para funcionalidades com detalhes de execução fechados. Detalhes em `docs/process/autonomous/` e template em `docs/process/autonomous/dispatch.md`.

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
**Papel:** Implementar código baseado em documentações atualizadas e — no fluxo autônomo, dentro da branch do milestone — refinar épicos ainda pendentes via PM skill.

**Deve:**
- ✅ Seguir docs/process/implementation/ (guidelines)
- ✅ Seguir `docs/testing/strategy.md` para pirâmide de testes, markers (`integration`, `slow`) e política de uso da API real
- ✅ Ler ROADMAP.md + specs técnicas
- ✅ TDD onde aplicável
- ✅ Validar incrementalmente
- ✅ Atualizar docs se mudou estrutura
- ✅ No fluxo autônomo, refinar épicos de um milestone que ainda estão em `🌱` ou `📐` **dentro da branch do milestone**, via PM skill, antes de entrar em implementação — nunca em main

**Não deve:**
- ❌ Refinar visão ou quebrar visão em milestones (trabalho estratégico, feito via Claude Web antes de existir milestone)
- ❌ Mergear em main sem aval humano explícito sobre o milestone
- ❌ Tomar decisões arquiteturais sem base

**Princípio de refinamento na reforma:**
- Refinamento **estratégico** (visão → milestones, visão → épicos em `🌱`/`📐`) segue sendo feito via Claude Web, antes de qualquer milestone existir.
- Refinamento **tático** (épico em `🌱` ou `📐` → `🔍 Detalhes definidos`) acontece dentro da branch do milestone, via PM skill, como parte do fluxo autônomo.
- `main` só recebe milestone que passou por todos os gates automáticos e recebeu aval humano explícito.

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

**4. Gerar Prompts** (quando a entrada é para fluxo manual via Cursor)
- Múltiplos prompts (1 por arquivo)
- Ordem de execução clara
- Instruções enxutas (Cursor pensa também)
- Manter padrões existentes

**5. Validação**
- Confirmar que prompts ou plano de milestones fazem sentido
- Verificar se nada foi esquecido

### Output Esperado

O formato do output depende do alvo da sessão de refinamento. Os dois formatos abaixo são complementares — sessões estratégicas produzem o primeiro, sessões de preparação para o fluxo manual produzem o segundo.

**Formato A — Sessão estratégica (visão → milestones / épicos em `🌱` / `📐`)**

Lista de milestones e/ou épicos proposta para o ROADMAP do produto, com o id no formato `<ESTAGIO>-<PRODUTO>` e o agrupamento de épicos por milestone. Nenhum prompt para Cursor — a materialização no ROADMAP é parte do fluxo de desenvolvimento a jusante.

**Formato B — Sessão de preparação para fluxo manual via Cursor (alvo `📋 Critérios definidos` ou `🔍 Detalhes definidos` de épicos já existentes)**

Um prompt por arquivo a atualizar, para o Cursor executar:

```
PROMPT 1: ROADMAP.md
[instruções enxutas pro Cursor]
PROMPT 2: core/docs/agents/orchestrator/conversational/README.md
[instruções enxutas pro Cursor]
PROMPT 3: docs/ARCHITECTURE.md
[instruções enxutas pro Cursor]
```

> No fluxo autônomo, refinamento tático (épico em `🌱`/`📐` → `🔍`) não passa por Claude Web nem por Cursor — acontece dentro da branch do milestone, via PM skill, como parte da mesma sessão de dispatch.

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
├── skills/                          # Skills do modo autônomo (Scrum Master/QA/TL/PO/RTE) — processo de dev, NÃO runtime do produto
│   ├── README.md                    # Índice + como o Claude Web carrega cada skill
│   ├── scrum-master/                # Gate 1 — quebra funcionalidade em tasks
│   ├── qa/                          # Gate 3 — valida testes, sintaxe, imports
│   ├── tl/                          # Gate 4 — valida arquitetura e padrões
│   ├── po/                          # Gate 5 — valida critérios de aceite
│   └── rte/                         # Gate 6 — prepara branch + comandos p/ dev
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

## 9. GLOSSÁRIO

Cinco termos fixam a hierarquia de entrega usada pelo projeto. Refinamento, planejamento e dispatch se referem a eles com esse significado exato.

**Estágio**
Fase do produto no eixo "quem usa": POC (prova que a ideia faz sentido), Protótipo (o próprio dev usa de verdade), MVP (outros usam sem o dev do lado). Definições completas e implicações em `docs/process/refinement/planning_guidelines.md`. Um produto atravessa os estágios em ordem; não é uma caixa de tempo. **Estágio** é o agregador do ROADMAP (seção "Fase <estágio>"), não é dispatcheável — milestones que o compõem é que são.

**Milestone**
Unidade de entrega do **fluxo autônomo** = uma sessão de trabalho coerente. Agrupa épicos relacionados dentro de um mesmo estágio. Um estágio pode ter 1 ou N milestones; o agrupamento é output do **refinamento estratégico** (Claude Web, fora da branch), antes do dispatch. Um milestone é disparado por linguagem natural ("implementa a POC do Ensaio"), executado numa branch `milestone/<id-em-caixa-baixa>`, e só chega em main depois do aval humano explícito.

- **Id do milestone:** `<ESTAGIO>-<PRODUTO>` em caixa alta, com hífen. Ex.: `POC-ENSAIO`, `PROTO-REVELAR`, `MVP-ENSAIO`.
- **Sufixo** quando um estágio tem mais de um milestone: `POC-ENSAIO-ALPHA`, `POC-ENSAIO-BETA`, `PROTO-WORKFLOW-ENCERRAMENTO`.
- **Branch:** id em caixa baixa com `milestone/` na frente. Ex.: `milestone/poc-ensaio`.

**Épico**
Agrupamento coeso de funcionalidades que entrega valor incremental. Unidade do ROADMAP. Percorre até oito estados (`🌱 Visão` → `🧭 Jornada alinhada` → `📐 Funcionalidades esboçadas` → `📋 Critérios definidos` → `🔍 Detalhes definidos` → `🏗️ Em andamento` → `🔀 Em revisão` → `✅ Implementado`). Um épico pode pertencer a um milestone (quando for ser executado via fluxo autônomo) ou ser implementado isoladamente no fluxo manual via Cursor. **Os mesmos estados aplicam-se ao campo "Status" do milestone** — milestone em `🧭 Jornada alinhada` significa objetivo, jornada e escopo declinados, glossário ancorado e mapeamento de feedback do estágio anterior consolidados, com lista de épicos definida (mesmo que individualmente em estados anteriores). `🔀 Em revisão` não se aplica ao milestone como um todo — aplica-se a épicos individualmente quando a RTE abre a PR do milestone.

**Funcionalidade**
Unidade mínima do ROADMAP, dentro de um épico. Tem critérios de aceite próprios e, em estado `🔍`, detalhes de execução fechados (arquivos-alvo, contratos, acoplamentos, escopo de teste). É a unidade do **fluxo manual** via Cursor; no fluxo autônomo é a unidade sobre a qual cada gate (QA/TL/PO) decide APROVA/REJEITA.

**Tarefa**
Unidade mínima de **execução** dentro de uma funcionalidade. Criada pela Scrum Master skill em `docs/process/current_implementation.md` no início da sessão autônoma; consumida pelo Dev na ordem declarada. Tarefas não existem no ROADMAP — vivem só no artefato de sessão; somem quando o milestone fecha.

---

**Versão:** 1.1
**Data:** 22/04/2026
**Para:** Claude Web (consultor estratégico de refinamento) e Claude Code Web (executor autônomo)

