# ROADMAP — Workflow de Desenvolvimento

Milestones e épicos do processo de desenvolvimento do paper-agent.

> Visão completa em [vision.md](vision.md).

## 🧭 Estados dos Épicos

Cada épico percorre até seis estados. Detalhes em [docs/process/refinement/planning_guidelines.md](../refinement/planning_guidelines.md).

- **`🌱 Visão`** — apenas objetivo definido. Aguarda refinamento.
- **`📐 Funcionalidades esboçadas`** — funcionalidades listadas sem critérios de aceite. Aguarda refinamento.
- **`📋 Critérios definidos`** — critérios de aceite definidos. Pronto para fluxo manual via Cursor.
- **`🔍 Detalhes definidos`** — checklist em [autonomous_readiness.md](../refinement/autonomous_readiness.md) aplicado. Pronto para fluxo autônomo via Claude Code Web.
- **`🏗️ Em andamento`** — implementação em curso, até o ciclo de fechamento.
- **`✅ Implementado`** — ciclo de fechamento executado (ver [epic_completion.md](../refinement/epic_completion.md)).

> **Retroatividade:** épicos concluídos antes da introdução do modelo de 6 estados permanecem em formato simplificado (título ✅ + 1-2 linhas de resumo) e não são reclassificados retroativamente. O modelo aplica-se a épicos em andamento e futuros.

---

## 🎯 Milestones

### POC-WORKFLOW

- **Objetivo:** primeiro fluxo do workflow (implementação de código)
  funcionando ponta a ponta em escala de milestone, incluindo execução
  real de um milestone de produto como prova. Absorve a dívida da reforma
  de milestone atualmente em `docs/process/refactor-backlog.md`.
- **Estágio:** POC
- **Épicos agrupados:** W-POC-1, W-POC-2, W-POC-3, W-POC-4
- **Dependências de core:** nenhuma
- **Branch associada:** `milestone/poc-workflow`
- **Status dos épicos:** todos em 🌱 Visão no momento da criação deste
  ROADMAP (derivados de discussão prévia, aguardam refinamento formal).
- **Nota:** este milestone promove a dívida documentada em
  `docs/process/refactor-backlog.md` a épicos do workflow. Uma vez este
  ROADMAP em vigor, `refactor-backlog.md` pode referenciar W-POC-* e ser
  enxugado em sessão separada.

### PROTO-WORKFLOW

- **Objetivo:** fluxo de implementação estabilizado com uso real
  semanal + segundo fluxo do workflow aparecendo (a definir no
  refinamento). Candidato forte para segundo fluxo: observação de
  arquitetura (detectar crescimento desordenado, atividade de baixo
  custo recorrente).
- **Estágio:** Protótipo
- **Épicos agrupados:** a definir em refinamento estratégico
- **Dependências de core:** nenhuma
- **Branch associada:** `milestone/proto-workflow`
- **Status dos épicos:** milestone em declaração — épicos serão
  definidos em refinamento estratégico via Claude Web após POC-WORKFLOW
  fechar.

### MVP-WORKFLOW

- **Objetivo:** priorização autônoma rodando. Skill orquestradora
  escolhe tarefa do dia a partir de backlog curado; Claude Code Routine
  dispara execução uma vez por dia; operador recebe relatório executivo
  no formato "trabalhamos isso hoje, faz sentido? para validar faça XYZ".
- **Estágio:** MVP
- **Épicos agrupados:** a definir em refinamento estratégico
- **Dependências de core:** nenhuma
- **Branch associada:** `milestone/mvp-workflow`
- **Status dos épicos:** milestone em declaração — épicos serão
  definidos em refinamento estratégico via Claude Web após
  PROTO-WORKFLOW fechar.

## 📋 Épicos Planejados

### Épicos do POC-WORKFLOW

#### ÉPICO W-POC-1: Dispatch em linguagem natural

**Objetivo:** permitir que o dispatch autônomo seja invocado por linguagem
natural ("implementa a POC do Ensaio") em vez do template de placeholder
atual ("[Funcionalidade X.Y]"). Parser informal que Claude Code Web aplica
para identificar milestone alvo e estado inicial.

**Status:** 🌱 Visão

**Dependências:** nenhuma (primeiro do POC-WORKFLOW)

**Migra de:** `docs/process/refactor-backlog.md` → M4-restante (item
"docs/process/autonomous/dispatch.md")

#### ÉPICO W-POC-2: Template aninhado de current_implementation.md

**Objetivo:** migrar o template de `current_implementation.md` do shape
atual (linear por funcionalidade) para shape aninhado (milestone → épicos
→ funcionalidades → gates). Template é gerado pelo Scrum Master no início
de cada milestone.

**Status:** 🌱 Visão

**Dependências:** W-POC-1 (dispatch identifica o milestone que alimenta
o template)

**Migra de:** `docs/process/refactor-backlog.md` → M4-restante (item
"Template de current_implementation.md")

#### ÉPICO W-POC-3: Reescrita operacional das skills por milestone

**Objetivo:** reescrever conteúdo operacional de Scrum Master, QA, TL, PO
e RTE para operar dentro do loop por épico de um milestone, em vez do
modelo atual per-funcionalidade. Pré-checagens de cada skill consomem o
shape aninhado definido em W-POC-2.

**Status:** 🌱 Visão

**Dependências:** W-POC-2 (template aninhado precisa existir para skills
poderem consumi-lo)

**Migra de:** `docs/process/refactor-backlog.md` → M4-restante (item
"Conteúdo operacional dos skill.md")

#### ÉPICO W-POC-4: Execução real da POC-ENSAIO no fluxo novo

**Objetivo:** executar o milestone POC-ENSAIO de ponta a ponta usando o
fluxo reescrito (W-POC-1/2/3). Primeira prova real do fluxo autônomo por
milestone. Aprendizado desta execução informa refinamento de M5 e M6 da
reforma original (que entram no PROTO-WORKFLOW).

**Status:** 🌱 Visão

**Dependências:** W-POC-1, W-POC-2, W-POC-3 (fluxo precisa estar
operacional antes da execução real)

**Nota:** a POC-ENSAIO em si é milestone do produto Ensaio. W-POC-4 é o
épico do workflow que usa a POC-ENSAIO como teste do fluxo.

---

## 📚 Observações

**Regra:** fluxo manual via Cursor exige épico em `📋 Critérios definidos`;
fluxo autônomo via Claude Code Web exige `🔍 Detalhes definidos`.

Todos os épicos W-POC-* estão em `🌱 Visão` e precisam passar por
refinamento antes de qualquer fluxo de execução. Refinamento estratégico
(visão → critérios) via Claude Web; refinamento tático (critérios →
detalhes) via PM Skill dentro da branch do milestone.

Épicos PROTO e MVP ainda não foram desenhados — ficam a definir em
refinamento estratégico após POC-WORKFLOW fechar, com aprendizado real
no bolso.
