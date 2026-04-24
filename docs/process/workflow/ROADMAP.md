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
  real de um milestone de produto como prova. Absorve o núcleo da reforma
  de milestone (M4 do plano original) via W-POC-1/2/3 e prova o fluxo via
  W-POC-4.
- **Estágio:** POC
- **Épicos agrupados:** W-POC-1, W-POC-2, W-POC-3, W-POC-4
- **Dependências de core:** nenhuma
- **Branch associada:** `milestone/poc-workflow`
- **Status dos épicos:** W-POC-1 ✅, W-POC-2 ✅, W-POC-3 ✅,
  W-POC-4 ✅.
- **Nota:** dívida residual da reforma de milestone (M4-restante, M5, M6
  e dívidas declaradas em W-POC-3) vive no PROTO-WORKFLOW como épicos
  W-PROTO-1..4. O antigo `docs/process/refactor-backlog.md` foi
  migrado para este ROADMAP e removido.

### PROTO-WORKFLOW

- **Objetivo:** fluxo de implementação estabilizado com uso real
  semanal + refinamento do ciclo de encerramento (validação async,
  extração no momento da implementação, faxina automática via Action)
  + segundo fluxo do workflow aparecendo (a definir no refinamento).
  Candidato forte para segundo fluxo: observação de arquitetura
  (detectar crescimento desordenado, atividade de baixo custo
  recorrente). Primeira safra de épicos absorve a dívida residual
  da reforma de milestone que não coube no POC; segunda safra ataca
  o atrito observado em W-POC-4 no rito de encerramento.
- **Estágio:** Protótipo
- **Épicos agrupados:** W-PROTO-1, W-PROTO-2, W-PROTO-3, W-PROTO-4
  (saneamento residual da reforma); W-PROTO-5, W-PROTO-6, W-PROTO-7
  (refinamento do ciclo de encerramento); + épicos do segundo fluxo
  a definir em refinamento estratégico.
- **Dependências de core:** nenhuma
- **Branch associada:** `milestone/proto-workflow`
- **Status dos épicos:** W-PROTO-1 🌱 Visão, W-PROTO-2 🌱 Visão,
  W-PROTO-3 🌱 Visão, W-PROTO-4 🌱 Visão, W-PROTO-5 🌱 Visão,
  W-PROTO-6 🌱 Visão, W-PROTO-7 🌱 Visão.

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

**Status:** ✅ Implementado

**Dependências:** nenhuma (primeiro do POC-WORKFLOW)

**Migra de:** reforma de milestone (branch `refactor/fluxo-milestone`,
2026-04)

**Entregue em:** commit `7ec1a4d` — reescrita completa de
`docs/process/autonomous/dispatch.md`. Substitui template de placeholder
por dispatch em linguagem natural ("implementa a POC do Ensaio") e
documenta parser informal de 5 passos (extrair id `<ESTAGIO>-<PRODUTO>`,
localizar no ROADMAP, identificar estado inicial do fluxo com base em
épicos `🌱/📐/📋/🔍`, preparar branch `milestone/<id>`, carregar skills
em sequência). 4 exemplos de dispatch cobrindo milestone com tudo em
`🔍`, milestone com épicos pré-`🔍` (PM skill roda), milestone com
sufixo e entrada ambígua.

#### ÉPICO W-POC-2: Template aninhado de current_implementation.md

**Objetivo:** migrar o template de `current_implementation.md` do shape
atual (linear por funcionalidade) para shape aninhado (milestone → épicos
→ funcionalidades → gates). Template é gerado pelo Scrum Master no início
de cada milestone.

**Status:** ✅ Implementado

**Dependências:** W-POC-1 (dispatch identifica o milestone que alimenta
o template)

**Migra de:** reforma de milestone (branch `refactor/fluxo-milestone`,
2026-04)

**Entregue em:** bloco markdown dentro de `skills/scrum-master/skill.md`,
seção "TEMPLATE DE `current_implementation.md`". Gates QA/TL/PO
representados por tabela por épico (linhas = funcionalidades, colunas =
Dev/QA/TL/PO, status por emoji ⏳/✅/❌/➖). Evidências de carregamento
separadas em dois blocos: únicas por milestone (PM/EM/Scrum Master/RTE,
1 linha cada) e repetidas por funcionalidade (QA/TL/PO, 1 linha cada
gate × funcionalidade, com contexto `épico <ID> | funcionalidade <N.M>`).
Histórico de reprovações carrega o mesmo contexto para a regra de
escalação (3 consecutivas no mesmo gate do mesmo épico → aborta
milestone) operar.

#### ÉPICO W-POC-3: Reescrita operacional das skills por milestone

**Objetivo:** reescrever conteúdo operacional de Scrum Master, QA, TL, PO
e RTE para operar dentro do loop por épico de um milestone, em vez do
modelo atual per-funcionalidade. Pré-checagens de cada skill consomem o
shape aninhado definido em W-POC-2.

**Status:** ✅ Implementado

**Dependências:** W-POC-2 (template aninhado precisa existir para skills
poderem consumi-lo)

**Migra de:** reforma de milestone (branch `refactor/fluxo-milestone`,
2026-04)

**Entregue em:** reescrita de 5 skill.md —
`skills/scrum-master/skill.md` (PAPEL + REGRAS + Passos 1-8 reescritos
para planejar o milestone inteiro: N épicos quebrados em tasks numa
única passada, preenchimento das seções "Épicos" e "Esclarecimentos" do
template aninhado já criado por PM/EM; template em si intocado);
`skills/qa/skill.md`, `skills/tl/skill.md`, `skills/po/skill.md` (Passo
1 identifica épico+funcionalidade via ponteiro na tabela de gates —
primeira linha com Dev ✅ e gate corrente ⏳; Passo 2/diff compara
contra último sha validado na branch `milestone/<id>`, não contra
`main`; Passo 7/8 grava status na célula correta da tabela aninhada,
evidência com contexto `| épico <ID> | funcionalidade <N.M>`);
`skills/rte/skill.md` (Passo 1 exige todas as células Dev/QA/TL/PO ✅
em todas as tabelas; Passo 2 faz push único de `milestone/<id>`; Passo
3 coleta dados de `main...HEAD` sobre o milestone todo; Passo 5/7
consolida N épicos em relatório único e mensagem única; dívida do
template `delivery-report.md` declarada inline para migração posterior).

#### ÉPICO W-POC-4: Execução real da POC-ENSAIO no fluxo novo

**Objetivo:** primeira prova real do fluxo autônomo por milestone via
execução end-to-end da POC-ENSAIO.

**Status:** ✅ Implementado

**Entregue em:** PR #77 (merge `c423238`, 2026-04-24) — POC-ENSAIO
mergeada em main. Rito de fechamento (extração + enxugamento + transição)
executado manualmente no commit `9831d50`. Atrito observado durante o rito
alimenta W-PROTO-5/6/7 (refinamento do ciclo de encerramento).

### Épicos do PROTO-WORKFLOW

#### ÉPICO W-PROTO-1: Reescrita por milestone dos arquivos operacionais de `docs/process/autonomous/`

**Objetivo:** alinhar `workflow.md` (corpo abaixo do diagrama),
`overview.md`, `delivery.md` e `session_conventions.md` ao modelo de
milestone. Hoje esses arquivos ainda descrevem decisão/entrega
per-funcionalidade (`feature/X.Y-nome`, "dispara pela manhã / valida à
noite" por funcionalidade, um commit por funcionalidade). A reescrita
passa a descrever loop por épico dentro do milestone, gates QA/TL/PO
per-funcionalidade operando dentro do loop, RTE fechando o milestone
com notificação única, e `session_conventions.md` §2 explicitando que
um milestone tem N commits (padrão: um por épico) na branch
`milestone/<id-em-caixa-baixa>`. Política de 3 reprovações consecutivas
no mesmo gate do mesmo épico (já fixada em `dispatch.md` via W-POC-1)
ganha descrição detalhada em `workflow.md`.

**Status:** 🌱 Visão

**Dependências:** W-POC-3 (semântica operacional já está nos skill.md;
os arquivos de `docs/process/autonomous/` são a descrição humana desse
mesmo modelo)

**Migra de:** reforma de milestone (branch `refactor/fluxo-milestone`,
2026-04)

#### ÉPICO W-PROTO-2: Distinção estratégico × tático em `docs/process/refinement/`

**Objetivo:** promover a distinção refinamento estratégico (Claude
Web, fora da branch, antes do dispatch) × refinamento tático (PM
skill, dentro da branch do milestone) de callout isolado para conteúdo
de primeira classe ao longo de `docs/process/refinement/`. Tocar:
`planning_guidelines.md` (callout vira seção própria + sub-seção
"Processo de Refinamento Autônomo (PM Skill)" irmã de "Processo de
Refinamento com Claude Web"; revisar exemplos para cobrir os dois
caminhos); `starter.md` (explicitar que o pack cobre apenas o
estratégico; nova seção "Contexto consumido pela PM skill"); `overview.md`
(ajustar "Quando usar"); `autonomous_readiness.md` (deixar claro que o
checklist é consumido pela PM skill como programa executável);
`epic_completion.md` (ajuste pontual: ciclo pode ser acionado pela RTE
em bulk para todos os épicos do milestone).

**Status:** 🌱 Visão

**Dependências:** W-POC-3 (PM skill estável operacionalmente); idealmente
após W-PROTO-1 para manter coerência entre `autonomous/` e
`refinement/`, mas não bloqueante.

**Migra de:** reforma de milestone (branch `refactor/fluxo-milestone`,
2026-04)

#### ÉPICO W-PROTO-3: Migração do template `skills/rte/templates/delivery-report.md` para shape de milestone

**Objetivo:** reescrever o template de relatório de entrega para
acomodar N épicos em sub-seções, em vez do formato atual (uma
funcionalidade isolada). A skill RTE (`skills/rte/skill.md` Passo 5,
reescrita em W-POC-3) já opera sobre milestone inteiro e consolida N
épicos na mensagem final, mas preenche um template ainda no shape
antigo. Dívida declarada inline no próprio `skill.md` durante W-POC-3.

**Status:** 🌱 Visão

**Dependências:** W-POC-3 (RTE já opera por milestone; o template é o
último ponto do fluxo ainda não-migrado)

**Migra de:** dívida declarada em commit `7cde7d9` (W-POC-3)

#### ÉPICO W-PROTO-4: Cross-references e saneamento documental pós-reforma

**Objetivo:** fechar pontas periféricas para que o grep do repositório
fique coerente e a reforma de milestone não deixe ponteiros quebrados.
Tocar: `docs/CONTEXT_INDEX.md` (tema "Desenvolvimento e Processo" lista
as 7 skills — PM, EM, Scrum Master, Dev, QA, TL, PO, RTE — e referencia
`docs/process/sizing/`; linha nova no MAPA RÁPIDO DE DECISÃO para
"Implementar milestone de produto"); `docs/ARCHITECTURE.md` (seção
"Estrutura do Projeto": `skills/` passa de 5 para 7 entradas +
`docs/process/sizing/`); `.github/copilot-instructions.md` (Modo A
referencia shape novo de `current_implementation.md`; exemplo
`C-ENSAIO-2` vira `POC-ENSAIO` ou similar); `README.md` (linha ~195
menciona `sizing/` se oportuno); `docs/process/implementation/overview.md`
(nota curta declarando que fluxo manual opera em funcionalidade/épico e
é complementar ao autônomo que opera em milestone). Micro-dívidas:
typo `IImplementado` pós-M1; inconsistência "5 arquivos essenciais"
(`planning_guidelines.md` linha 32) vs pack de 6 em `starter.md`. Fechar
com varredura `grep -rn` por "Planning Skill", "Validation Skill",
"planning/skill.md", "validation/skill.md", "feature/X.Y-" e corrigir
o que sobrou.

**Status:** 🌱 Visão

**Dependências:** W-PROTO-1 e W-PROTO-2 (varredura final faz sentido
depois que os arquivos operacionais e de refinamento foram migrados)

**Migra de:** reforma de milestone (branch `refactor/fluxo-milestone`,
2026-04)

#### ÉPICO W-PROTO-5: Validação async — PR antes da aprovação, Copilot como validador local

**Objetivo:** mover a validação do implementador pra depois da abertura
da PR. Hoje o agente implementador só encerra quando o dev valida;
passa a encerrar quando abre a PR (novo estado terminal: "PR aberta,
pending review"). Dev valida localmente com GitHub Copilot usando os
critérios inline no body da PR (ou referenciados via `poc_validation.md`
equivalente gerado no mesmo commit da implementação). Aprovação = merge.

**Status:** 🌱 Visão

**Dependências:** nenhuma (refinamento operacional do ciclo de
encerramento; não bloqueia nem é bloqueado por W-PROTO-1/2/3/4)

**Motivação:** atrito observado em W-POC-4 — sessão do agente ficava
bloqueada aguardando validação manual antes de abrir PR, acoplando
conclusão da sessão ao timing do dev. Tocar: `epic_completion.md`
(reordenar os passos; PR passa a ser artefato aberto pelo implementador
com critérios de validação embutidos, não último passo do rito);
documentação de estado terminal da sessão do agente em
`docs/process/autonomous/` (sessão pode encerrar com PR aberta).

#### ÉPICO W-PROTO-6: Skill de faxina + GitHub Action pós-merge

**Objetivo:** automatizar enxugamento do ROADMAP e transição de estado
(🏗️→✅) via GitHub Action disparada no merge da PR do épico. Cria
`skills/cleanup/skill.md` com as regras determinísticas (reduzir épico
a título + 1-2 linhas + PR; virar status na tabela do milestone);
`.github/workflows/epic-cleanup.yml` roda Claude Code CLI no runner,
carrega a skill, commita o resultado direto na main (mudança só em
docs, baixo risco). Secret `ANTHROPIC_API_KEY` configurado no repo.
Primeira skill do projeto executada via Action em vez de via fluxo
local — experimento com Claude Code CLI.

**Status:** 🌱 Visão

**Dependências:** W-PROTO-7 (extração precisa sair do rito de
fechamento antes da faxina ser automatizada — skill de cleanup cobre
só enxugamento + transição, que são determinísticos).

**Motivação:** atrito observado em W-POC-4 — rito de fechamento manual
consome ~300 linhas de edição em ROADMAPs após merge, tarefa repetitiva
e mecânica que não exige julgamento do dev nem do implementador.

#### ÉPICO W-PROTO-7: Extração pra ARCHITECTURE.md como passo do implementador

**Objetivo:** mover extração de conhecimento permanente (padrões novos
em `docs/ARCHITECTURE.md` ou `core/docs/architecture/`, notas em
`.claudecode.md`, comportamento em `core/docs/agents/<agente>/`) do
rito de fechamento (`epic_completion.md`) pro momento da implementação.
Implementador escreve no mesmo commit da entrega, enquanto o contexto
do que foi construído está fresco; `epic_completion.md` passa a cobrir
só enxugamento + transição (partes determinísticas que a Action de
W-PROTO-6 consegue executar).

**Status:** 🌱 Visão

**Dependências:** nenhuma (é pré-requisito técnico de W-PROTO-6, não
tem dependências próprias).

**Motivação:** extração exige julgamento ("isso é padrão reusável?
merece entrada em ARCHITECTURE.md?") e não pode ser automatizada.
Separar dos passos mecânicos (enxugamento + transição) libera esses
últimos pra automação. Tocar: `epic_completion.md` (remover seção
"Extração" do rito pós-merge; nova referência de que extração é
responsabilidade do implementador); skills do implementador ou
convenção de commit que sinalize a obrigatoriedade da extração antes
de abrir PR.

---

## 📚 Observações

**Regra:** fluxo manual via Cursor exige épico em `📋 Critérios definidos`;
fluxo autônomo via Claude Code Web exige `🔍 Detalhes definidos`.

W-POC-1 e W-POC-2 foram executados manualmente via Claude Code (fora do
fluxo autônomo) na branch `claude/create-workflow-docs-6CR73` porque o
próprio fluxo autônomo é o que está sendo reescrito. W-POC-3 segue o
mesmo caminho. W-POC-4 foi executado em 2026-04-24 via PR #77 (POC-ENSAIO),
confirmando o fluxo novo end-to-end; atrito observado no rito de
encerramento alimentou o desenho de W-PROTO-5/6/7.

W-PROTO-5/6/7 formam uma unidade lógica (refinamento do ciclo de
encerramento) e podem ser executados em sequência: W-PROTO-5 (processual,
baixo custo) → W-PROTO-7 (separa extração da faxina) → W-PROTO-6 (infra
de automação). W-PROTO-1/2/3/4 (dívida documental da reforma de
milestone) podem rodar em paralelo quando houver capacidade.

Épicos MVP ainda não foram desenhados — ficam a definir em refinamento
estratégico após PROTO-WORKFLOW fechar, com aprendizado real no bolso.
