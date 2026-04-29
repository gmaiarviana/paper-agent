# Paper Agent - Constitution

Princípios não-negociáveis para trabalhar com este projeto.

---

## 1. PRINCÍPIOS DE TRABALHO

### Unidade de Entrega
- **Milestone.** Um **milestone** agrupa épicos relacionados dentro de um estágio (POC, Protótipo, MVP). Um estágio pode ter 1 ou N milestones. Um milestone fecha quando todos os seus épicos caem na branch do milestone, validados pelos gates automáticos, e recebem aval humano. É a unidade do fluxo único de execução (Claude Code Web autônomo).
- Estágio, milestone, épico e funcionalidade são definidos no Glossário ao fim deste documento.

### Como Refinamos
- POC → Protótipo → MVP (incremental)
- Discussão > especulação antecipada
- Épicos percorrem até oito estados no ROADMAP: `🌱 Visão` → `🧭 Jornada alinhada` → `📐 Funcionalidades esboçadas` → `📋 Critérios definidos` → `🔍 Detalhes definidos` → `🏗️ Em andamento` → `🔀 Em revisão` → `✅ Implementado`. Modelo completo em `docs/process/refinement/planning_guidelines.md`.
- Toda sessão de refinamento opera com um **alvo definido** (o estado ao qual o épico deve chegar). O alvo pode ser declarado pelo usuário ao abrir a sessão ou inferido pelo refinador a partir da camada que ainda não está clara e confirmado antes do primeiro edit (não é gate de abertura). Uma vez definido, o refinador — sessão estratégica (caminho principal: Claude Code Web direto no repo; secundário: Claude Web em sessão externa) ou PM skill (tático, dentro da branch do milestone) — conduz as perguntas até atingir o alvo, sem parar em estados intermediários.
- Alvo `🔍 Detalhes definidos` é pré-requisito do fluxo único de execução; guiado pelo checklist em `docs/process/refinement/autonomous_readiness.md`. Aplicado sob demanda, épico a épico — pela sessão estratégica antes do milestone existir, ou pela PM skill dentro da branch do milestone quando o milestone é disparado com épicos ainda em `🌱`/`📐`/`📋`.
- `📋 Critérios definidos` é **passo intermediário** até `🔍`; não habilita execução por si só.
- Fechamento do épico (extração de conhecimento permanente + poda do ROADMAP) segue `docs/process/refinement/epic_completion.md` antes de marcar como `✅ Implementado`.
- Funcionalidades detalhadas aceleram implementação.

### Como Implementamos
- Refinamento estratégico (visão → milestones → épicos) — caminho principal via Claude Code Web direto no repo; caminho secundário via Claude Web em sessão externa quando há decisão de alto nível que exige alinhamento humano com contexto fora do repo
- Implementação via fluxo único: Claude Code Web autônomo (grão de milestone) com gates Scrum Master/Dev/QA/TL/PO/RTE
- Milestone disparado por linguagem natural ("implementa a POC do Ensaio") entra em branch própria `milestone/<id-em-caixa-baixa>`; main só recebe milestone com aval humano
- TDD pragmático (lógica crítica sim, UI não)
- Validação incremental obrigatória
- Commits estratégicos (não obrigatórios)
- **Sem gambiarra para postergar limpeza.** Nada está em produção; débito técnico se paga agora, não depois. Workaround para evitar atualizar consumidor (camada de compatibilidade gratuita, condicional permanente, código morto "por garantia", `TODO` sem dono) é débito e não entra. Padrão estabelecido do projeto não é gambiarra — o critério é "isto é workaround ou é o padrão do projeto?". Aplicação a breaking changes core ↔ produtos em `core/docs/vision/super_system.md` (seção "Política de Breaking Changes em Código Compartilhado").

**Tipos de sessão:**
- **Sessão de implementação** — autônoma; produz código e docs; encerra com PR criada pela RTE. Detalhes: `docs/process/autonomous/workflow.md`.
- **Sessão de refinamento** — colaborativa (operador + agente); produz atualizações de ROADMAP; encerra com rito de encerramento de sessão (`docs/process/refinement/planning_guidelines.md`).

### Requisitos de Refinamento

O fluxo único de execução (Claude Code Web autônomo) exige **estado mínimo `🔍 Detalhes definidos`** no épico — checklist de `docs/process/refinement/autonomous_readiness.md` aplicado. Dev dispara pela manhã e valida à noite; skills automáticas (Scrum Master → Dev → QA → TL → PO → RTE) atuam como gates no lugar das aprovações explícitas. Detalhes em `docs/process/autonomous/` e template em `docs/process/autonomous/dispatch.md`.

`📋 Critérios definidos` é **passo intermediário** — não habilita execução por si só. Épicos em `🌱`, `📐` ou `📋` passam por sessão de refinamento com alvo `🔍` antes de qualquer dispatch (caminho principal: Claude Code Web na branch do repo; caminho secundário: Claude Web em sessão externa para decisões estruturais).

---

## 2. RESPONSABILIDADES

### Sessão Estratégica (Refinamento de Alto Nível)
**Papel:** Refinar épicos, discutir comportamentos, materializar decisões no ROADMAP. Caminho principal: Claude Code Web direto na branch do repo. Caminho secundário: Claude Web em sessão externa, quando a decisão exige contexto humano fora do repo (operador conduzindo via chat web).

**Deve:**
- ✅ Ler contexto completo (4 arquivos da raiz)
- ✅ Consultar docs adicionais via mapa (pull sob demanda)
- ✅ Perguntar clarificações necessárias
- ✅ Oferecer opções + recomendação (balizada por vision.md + guidelines)
- ✅ Materializar decisões no ROADMAP / specs ao final da sessão (no caminho principal, edição direta; no caminho secundário, output legível para o operador aplicar)

**Não deve:**
- ❌ Implementar código (refinamento ≠ execução)
- ❌ Assumir preferências sem base em vision/guidelines

### Claude Code (Implementador)
**Papel:** Implementar código baseado em documentações atualizadas e — no fluxo único de execução, dentro da branch do milestone — refinar épicos ainda pendentes via PM skill.

**Deve:**
- ✅ Seguir docs/process/implementation/ (guidelines)
- ✅ Seguir `docs/testing/strategy.md` para pirâmide de testes, markers (`integration`, `slow`) e política de uso da API real
- ✅ Ler ROADMAP.md + specs técnicas
- ✅ TDD onde aplicável
- ✅ Validar incrementalmente
- ✅ Atualizar docs se mudou estrutura
- ✅ No fluxo único de execução, refinar épicos de um milestone que ainda estão em `🌱`/`📐`/`📋` **dentro da branch do milestone**, via PM skill, antes de entrar em implementação — nunca em main

**Não deve:**
- ❌ Refinar visão ou quebrar visão em milestones (trabalho estratégico, feito em sessão dedicada antes de existir milestone)
- ❌ Mergear em main sem aval humano explícito sobre o milestone
- ❌ Tomar decisões arquiteturais sem base

**Princípio de refinamento:**
- Refinamento **estratégico** (visão → milestones, visão → épicos em `🌱`/`📐`) é feito em sessão dedicada antes de qualquer milestone existir — caminho principal via Claude Code Web direto no repo; caminho secundário via Claude Web em sessão externa.
- Refinamento **tático** (épico em `🌱`/`📐`/`📋` → `🔍 Detalhes definidos`) acontece dentro da branch do milestone, via PM skill, como parte do fluxo único de execução.
- `main` só recebe milestone que passou por todos os gates automáticos e recebeu aval humano explícito.

---

## 3. PROCESSO DE REFINAMENTO

### Input Esperado (você fornece)
- Comportamento desejado OU problema existente
- Contexto: épico novo, ajuste, discussão

### Sessão Estratégica Deve:

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

**4. Materialização no ROADMAP**
- Registrar decisões diretamente no ROADMAP do produto, ARCHITECTURE.md e specs técnicas relevantes
- Manter padrões existentes; commits incrementais

**5. Validação**
- Confirmar que as edições refletem o alinhamento
- Verificar se nada foi esquecido

### Output Esperado

Lista de milestones e/ou épicos materializada diretamente no ROADMAP do produto, com o id no formato `<ESTAGIO>-<PRODUTO>` e o agrupamento de épicos por milestone. A materialização é a entrega da sessão estratégica — não há um passo intermediário de "gerar prompts para outra ferramenta executar".

> No fluxo único de execução, refinamento tático (épico em `🌱`/`📐`/`📋` → `🔍`) acontece dentro da branch do milestone, via PM skill, como parte da mesma sessão de dispatch.

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

### ❌ Confundir Refinamento com Execução
- Sessão estratégica refina e materializa decisões no ROADMAP / specs (não implementa código)
- Claude Code (na branch do milestone) implementa código + atualiza docs estruturais quando muda

### ❌ Assumir sem Base
- Sempre consultar `products/<produto>/docs/vision.md` + guidelines
- Perguntar se incerto
- Não inventar padrões

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
Unidade de entrega do **fluxo único de execução** = uma sessão de trabalho coerente. Agrupa épicos relacionados dentro de um mesmo estágio. Um estágio pode ter 1 ou N milestones; o agrupamento é output do **refinamento estratégico** (sessão dedicada antes do dispatch — caminho principal via Claude Code Web direto no repo; secundário via Claude Web em sessão externa). Um milestone é disparado por linguagem natural ("implementa a POC do Ensaio"), executado numa branch `milestone/<id-em-caixa-baixa>`, e só chega em main depois do aval humano explícito.

- **Id do milestone:** `<ESTAGIO>-<PRODUTO>` em caixa alta, com hífen. Ex.: `POC-ENSAIO`, `PROTO-REVELAR`, `MVP-ENSAIO`.
- **Sufixo** quando um estágio tem mais de um milestone: `POC-ENSAIO-ALPHA`, `POC-ENSAIO-BETA`, `PROTO-WORKFLOW-ENCERRAMENTO`.
- **Branch:** id em caixa baixa com `milestone/` na frente. Ex.: `milestone/poc-ensaio`.

**Épico**
Agrupamento coeso de funcionalidades que entrega valor incremental. Unidade do ROADMAP. Percorre até oito estados (`🌱 Visão` → `🧭 Jornada alinhada` → `📐 Funcionalidades esboçadas` → `📋 Critérios definidos` → `🔍 Detalhes definidos` → `🏗️ Em andamento` → `🔀 Em revisão` → `✅ Implementado`). Um épico só é executável quando pertence a um milestone disparado pelo fluxo único de execução. **Os mesmos estados aplicam-se ao campo "Status" do milestone** — milestone em `🧭 Jornada alinhada` significa objetivo, jornada e escopo declinados, glossário ancorado e mapeamento de feedback do estágio anterior consolidados, com lista de épicos definida (mesmo que individualmente em estados anteriores). `🔀 Em revisão` não se aplica ao milestone como um todo — aplica-se a épicos individualmente quando a RTE abre a PR do milestone.

**Funcionalidade**
Unidade mínima do ROADMAP, dentro de um épico. Tem critérios de aceite próprios e, em estado `🔍`, detalhes de execução fechados (arquivos-alvo, contratos, acoplamentos, escopo de teste). É a unidade sobre a qual cada gate do fluxo único (QA/TL/PO) decide APROVA/REJEITA.

**Tarefa**
Unidade mínima de **execução** dentro de uma funcionalidade. Criada pela Scrum Master skill em `docs/process/current_implementation.md` no início da sessão de implementação; consumida pelo Dev na ordem declarada. Tarefas não existem no ROADMAP — vivem só no artefato de sessão; somem quando o milestone fecha.

---

**Versão:** 1.1
**Data:** 22/04/2026
**Para:** Claude Code Web (refinamento estratégico no repo + executor autônomo) e Claude Web (refinamento estratégico em sessão externa, caminho secundário)

