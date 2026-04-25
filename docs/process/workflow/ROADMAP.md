# ROADMAP — Workflow de Desenvolvimento

Milestones e épicos do processo de desenvolvimento do paper-agent.

> Visão completa em [vision.md](vision.md).

## 🧭 Estados dos Épicos

Cada épico percorre até sete estados. Os mesmos estados aplicam-se ao campo "Status" do milestone. Detalhes em [docs/process/refinement/planning_guidelines.md](../refinement/planning_guidelines.md).

- **`🌱 Visão`** — apenas objetivo definido. Aguarda refinamento.
- **`🧭 Jornada alinhada`** — objetivo refinado + rationale (o que é / o que não é) + glossário ancorado + acoplamentos sinalizados; jornada alvo e escopo declinados (para milestone). Funcionalidades ainda não esboçadas. Aguarda refinamento.
- **`📐 Funcionalidades esboçadas`** — funcionalidades listadas sem critérios de aceite. Aguarda refinamento.
- **`📋 Critérios definidos`** — critérios de aceite definidos. Pronto para fluxo manual via Cursor.
- **`🔍 Detalhes definidos`** — checklist em [autonomous_readiness.md](../refinement/autonomous_readiness.md) aplicado. Pronto para fluxo autônomo via Claude Code Web.
- **`🏗️ Em andamento`** — implementação em curso, até o ciclo de fechamento.
- **`✅ Implementado`** — ciclo de fechamento executado (ver [epic_completion.md](../refinement/epic_completion.md)).

> **Retroatividade:** épicos concluídos antes da introdução do modelo de estados permanecem em formato simplificado (título ✅ + 1-2 linhas de resumo) e não são reclassificados retroativamente. O modelo aplica-se a épicos em andamento e futuros.

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
  e dívidas declaradas em W-POC-3) vive na fase Protótipo, distribuída
  entre `PROTO-WORKFLOW-DOC` (W-PROTO-1..4 — saneamento documental) e
  `PROTO-WORKFLOW-ENCERRAMENTO` (W-PROTO-5..7 — refinamento do ciclo
  de encerramento). O antigo `docs/process/refactor-backlog.md` foi
  migrado para este ROADMAP e removido.

### PROTO-WORKFLOW-ENCERRAMENTO

- **Objetivo:** refinamento do ciclo de encerramento autônomo —
  validação async via PR, extração como passo do implementador, faxina
  mecânica via GitHub Action pós-merge. Primeira unidade coerente da
  fase Protótipo do Workflow.
- **Estágio:** Protótipo
- **Épicos agrupados:** W-PROTO-5, W-PROTO-6, W-PROTO-7
- **Dependências de core:** nenhuma
- **Branch associada:** `milestone/proto-workflow-encerramento`
- **Status dos épicos:** W-PROTO-5 🏗️ Em andamento, W-PROTO-6 🏗️ Em
  andamento, W-PROTO-7 🏗️ Em andamento.
- **Nota:** unidade lógica descoberta durante refinamento
  (2026-04-24) — os três épicos dividem o rito de `epic_completion.md`
  e foram refinados em conjunto na branch
  `claude/continue-workflow-implementation-5PKVa`. Ordem sugerida de
  implementação: W-PROTO-5 → W-PROTO-7 → W-PROTO-6.

### PROTO-WORKFLOW-DOC

- **Objetivo:** saneamento documental residual da reforma de milestone
  — reescrever arquivos de `docs/process/autonomous/` e
  `docs/process/refinement/` para o modelo de milestone, migrar
  template de `delivery-report.md`, fechar cross-references e limpar
  ponteiros quebrados. Segunda unidade coerente da fase Protótipo do
  Workflow, independente de `PROTO-WORKFLOW-ENCERRAMENTO`.
- **Estágio:** Protótipo
- **Épicos agrupados:** W-PROTO-1, W-PROTO-2, W-PROTO-3, W-PROTO-4
- **Dependências de core:** nenhuma
- **Branch associada:** `milestone/proto-workflow-doc`
- **Status dos épicos:** W-PROTO-1 🌱 Visão, W-PROTO-2 🌱 Visão,
  W-PROTO-3 🌱 Visão, W-PROTO-4 🌱 Visão.
- **Nota:** pendente de refinamento tático (não bloqueia
  `PROTO-WORKFLOW-ENCERRAMENTO`).

### MVP-WORKFLOW

- **Objetivo:** priorização autônoma rodando, materializada como POC
  mínimo da plataforma de workflow (ver
  [Forma da Plataforma](vision.md#forma-da-plataforma)). POC alimenta
  uma fila a partir do encerramento de implementação (W-PROTO-5: PR
  aberta = item) — com tipos de itens convivendo (decisão, escalação,
  PR pra revisar, proposta, relatório "trabalhamos isso hoje"). Kanban,
  chat focado, Proponente (1×/dia) e refinador autônomo (contínuo)
  entram em incrementos seguintes. Operador valida via fila, sem SLA.
- **Estágio:** MVP
- **Épicos agrupados:** a definir em refinamento estratégico
- **Dependências de core:** nenhuma
- **Branch associada:** `milestone/mvp-workflow`
- **Status dos épicos:** milestone em declaração — épicos serão
  definidos em refinamento estratégico via Claude Web após ambos os
  milestones da fase Protótipo fecharem.
- **Tensões pra refinamento estratégico** (discussão de 2026-04-25 ao
  mergear `vision.md` e `platform-vision.md`):
  - **(a) Quem cria itens "PR pra revisar"?** Inclinação: RTE no mesmo
    passo em que abre PR (W-PROTO-5 estendido). Alternativa: observador
    da plataforma observa a PR aberta e publica item.
  - **(b) Auto-regulação por capacidade (~20 itens).** Gatilho duro
    (autônomo trava de criar) ou soft (só prioriza)? Limite por tipo de
    item ou agregado?
  - **(c) Proponente no POC mínimo da plataforma?** Inclinação: fora —
    entra em incremento posterior pra manter POC realmente mínimo.
  - **(d) Reconstrução da fila se plataforma cair.** Validar na
    implementação que varrer markdown + estado de PRs reconstrói a fila
    deterministicamente — teste prático do princípio "markdown é fonte
    da verdade".
- **Fora do MVP (longo prazo):** outros fluxos do workflow
  (observar/auditar/reorganizar) e workflow como produto desacoplado
  multi-repo vivem no [Horizonte de vision.md](vision.md#horizonte) e
  não estruturam decisões deste milestone.

## 📋 Épicos Planejados

### ⏳ Fase POC

Único milestone: `POC-WORKFLOW`.

#### ÉPICO W-POC-1: Dispatch em linguagem natural

**Milestone:** `POC-WORKFLOW`

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

**Milestone:** `POC-WORKFLOW`

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

**Milestone:** `POC-WORKFLOW`

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

**Milestone:** `POC-WORKFLOW`

**Objetivo:** primeira prova real do fluxo autônomo por milestone via
execução end-to-end da POC-ENSAIO.

**Status:** ✅ Implementado

**Entregue em:** PR #77 (merge `c423238`, 2026-04-24) — POC-ENSAIO
mergeada em main. Rito de fechamento (extração + enxugamento + transição)
executado manualmente no commit `9831d50`. Atrito observado durante o rito
alimenta W-PROTO-5/6/7 (refinamento do ciclo de encerramento).

### ⏳ Fase Protótipo

> **Milestones:** `PROTO-WORKFLOW-ENCERRAMENTO` (W-PROTO-5, 6, 7) · `PROTO-WORKFLOW-DOC` (W-PROTO-1, 2, 3, 4).

#### ÉPICO W-PROTO-1: Reescrita por milestone dos arquivos operacionais de `docs/process/autonomous/`

**Milestone:** `PROTO-WORKFLOW-DOC`

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

**Milestone:** `PROTO-WORKFLOW-DOC`

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

**Milestone:** `PROTO-WORKFLOW-DOC`

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

**Milestone:** `PROTO-WORKFLOW-DOC`

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

**Milestone:** `PROTO-WORKFLOW-ENCERRAMENTO`

**Objetivo:** mover a validação do dev pra depois da abertura da PR.
Hoje a sessão autônoma (= "fase de implementação") só encerra quando o
dev valida localmente; passa a encerrar quando a RTE abre a PR (novo
estado terminal: "PR aberta, pending review"). Dev valida a PR com
auxílio do GitHub Copilot colando uma seção padronizada do body da PR
como prompt. Aprovação = merge.

**Status:** 🏗️ Em andamento

**Dependências:** nenhuma (refinamento operacional do ciclo de
encerramento; não bloqueia nem é bloqueado por W-PROTO-1/2/3/4; é
pré-requisito em conteúdo — não em código — de W-PROTO-7 e W-PROTO-6,
mas os três podem ser refinados/implementados em sequência curta).

**Motivação:** atrito observado em W-POC-4 — sessão do agente ficava
bloqueada aguardando validação manual antes de abrir PR, acoplando
conclusão da sessão ao timing do dev.

##### a) Termos e conceitos

- **Fase de implementação** = sessão autônoma inteira (Scrum Master →
  Dev → QA → TL → PO → RTE). Estado terminal pós-W-PROTO-5: **PR
  aberta**.
- **Fase de revisão humana** = Dev valida a PR com Copilot. Estado
  terminal: **merge**.
- **Seção 🎯 Validação** = bloco markdown padronizado no body da PR,
  copy-paste pronto pro Copilot processar sem contexto adicional. O
  "signo" que W-PROTO-5 introduz.
- **`validation-<milestone>.md`** = nome canônico do artefato que
  substitui `poc_validation.md` (hoje em `products/ensaio/docs/`).
  Vive em `products/<produto>/docs/validation-<milestone-id>.md` ou
  `docs/process/workflow/validation-<milestone-id>.md` conforme o
  milestone seja de produto ou de core/workflow. Gerado pela RTE no
  mesmo commit em que a PR é aberta; fica versionado junto com a
  entrega. Referência: estrutura atual de
  `products/ensaio/docs/poc_validation.md` serve como template de
  estilo.

##### b) Dados e contratos

**Shape da Seção 🎯 Validação no body da PR** (template fixo;
placeholders entre `<...>`):

```markdown
## 🎯 Validação (copie tudo abaixo e envie ao Copilot)

Você é revisor técnico desta PR. Valide o diff (`main...HEAD`) contra os
critérios abaixo. Para cada critério: ✅ (atende), ⚠️ (atende com
ressalva — justifique), ❌ (não atende — aponte arquivo/linha).
Reporte em markdown.

### Contexto
- Milestone: <ID> — <nome>
- Épicos entregues: <lista com IDs>
- Arquivo detalhado de validação: `<caminho>/validation-<id>.md`

### Critérios de aceite (consolidados do ROADMAP)

**Épico <ID-1>:**
1. <critério>
2. <critério>

**Épico <ID-2>:**
1. <critério>

### Comportamentos "não deve"
- <item>

### Formato de retorno esperado
- Tabela `Critério | Status | Observação`
- Seção "Riscos adicionais" (opcional)
```

**Shape de `validation-<milestone>.md`** (permanente; espelha
`poc_validation.md` atual):

- Cabeçalho com público (dev revisor), quando usar, estrutura.
- Seção "Preparação do ambiente" (checkout da branch, venv, deps).
- Seção "Testes unitários" (comandos determinísticos).
- Um bloco por épico do milestone, com sub-seção por funcionalidade
  (`N.M — <nome>`), contendo "O que rodar" (comandos) + "O que
  observar" (comportamento esperado).
- Seção final "Critérios de aprovação" com checklist agregado.

Campos obrigatórios no body da PR (além da Seção 🎯):
- Título: `<tipo>(<escopo>): <resumo do milestone> (<ID-MILESTONE>)`.
- Branch de origem: `milestone/<id-em-caixa-baixa>`; destino: `main`.
- Checklist de gates (cópia da tabela final consolidada de
  `current_implementation.md`).

##### c) Código-alvo e integração

**Arquivos a criar (como parte do fluxo, não deste épico):**
- `validation-<milestone-id>.md` gerado pela RTE a cada milestone.
  **Não** existe template fixo no repositório — o formato é
  descrito em `skills/rte/skill.md` e exemplificado pelo
  `poc_validation.md` atual.

**Arquivos a modificar (deste épico):**
- `docs/process/refinement/epic_completion.md` — remover referência a
  "dev valida localmente antes de abrir PR"; manter que PR aberta pela
  RTE é o artefato de entrada na revisão humana. A seção "Enxugamento"
  e "Transição de estado" continuam (elas movem com W-PROTO-6, não
  aqui).
- `skills/rte/skill.md` — **três mudanças cirúrgicas:**
  1. REGRAS NÃO-NEGOCIÁVEIS §5 `Sem PR automático` → `Abre PR com body
     padronizado`. §7 mantém restrição de não mergear.
  2. Novo Passo 6.5 (entre Passo 6 "Comandos de validação" e Passo 7
     "Notificar dev"): **"Gerar `validation-<milestone>.md` e abrir
     PR"**. Inclui geração do arquivo versionado (mesmo commit) e
     invocação de `mcp__github__create_pull_request` (ou `gh pr
     create` se fallback CLI); body preenchido com o template da
     Seção 🎯 (critérios agregados a partir das células PO ✅ da
     tabela de gates por funcionalidade).
  3. Passo 7 (mensagem final ao dev) — trocar "Próximo passo: você
     valida localmente, cria PR pela interface do GitHub e mergeia"
     por "Próximo passo: revisar PR #<N> (link), copiar seção 🎯
     Validação, enviar ao Copilot, aprovar e mergear via GitHub".
  4. CRITÉRIOS DE FALHA — remover "Tentou criar PR ou mergear
     automaticamente" e desmembrar: "Tentou mergear automaticamente"
     permanece como falha; "Abriu PR sem seção 🎯 completa" entra
     como nova falha.
- `skills/rte/templates/delivery-report.md` — acomodar a Seção 🎯
  Validação como bloco do template. Essa mudança sobrepõe parcialmente
  com W-PROTO-3 (reescrita completa do template para shape de
  milestone); declarar em comentário inline que W-PROTO-3 pode
  consolidar mais tarde.
- `docs/process/autonomous/workflow.md` — **edição cirúrgica** (ver
  seção d sobre overlap com W-PROTO-1):
  1. Diagrama do FLUXO GERAL: seta final de `RTE Skill → Dev valida`
     vira `RTE Skill → PR aberta → Dev revisa`.
  2. Seção "6. RTE SKILL" → "Não deve: Criar PR automaticamente"
     vira "Deve: Criar PR com body padronizado e seção 🎯
     Validação".
  3. Seção "TRANSIÇÃO DE ESTADO DO ÉPICO" — nota de que o estado
     terminal da fase de implementação é "PR aberta", não "Dev
     validou".
- `docs/process/autonomous/delivery.md` — **edição cirúrgica:**
  1. Seção 2 "AO RECEBER NOTIFICAÇÃO" — troca "rodar comandos de
     validação local + decidir" por "abrir PR, copiar seção 🎯 e
     enviar ao Copilot; rodar comandos localmente é opcional".
  2. Seção 5 "CRIAÇÃO DO PR" — inverte: RTE cria PR; dev revisa e
     mergeia (ou devolve com feedback no próprio PR).
- `.github/PULL_REQUEST_TEMPLATE.md` — **não tocar.** O template atual
  é genérico e a seção 🎯 é preenchida pela RTE sobrescrevendo o
  body. (Se no futuro W-PROTO-1/3 revisar o PR template, pode
  absorver.)

**Mecanismo de integração:**
- RTE usa a ferramenta `mcp__github__create_pull_request` (ou
  `gh pr create` como fallback) após push bem-sucedido da branch
  `milestone/<id>`. Autenticação já disponível no runner do Claude
  Code Web.
- Body da PR é construído programaticamente a partir dos critérios
  PO ✅ consolidados — a RTE varre `current_implementation.md`,
  extrai os critérios de aceite do ROADMAP (já linkados em
  `## Épicos`), e preenche o template.

**Template de estilo/estrutura:**
- Skill reescrita: **a própria `skills/rte/skill.md`** (hoje). Adicionar
  passos mantendo o padrão de "Checks duros / Checks soft / ação".
- Seção 🎯 Validação no body: **`products/ensaio/docs/poc_validation.md`
  atual** como referência de profundidade e formato por
  funcionalidade.

##### d) Acoplamentos

- **RTE hoje (skills/rte/skill.md:19-30 e 147-199) proíbe criar PR.**
  Essa regra inverte — exige reescrita cuidadosa das Regras
  Não-Negociáveis e dos Critérios de Falha para não deixar instrução
  conflitante.
- **Overlap com W-PROTO-1:** W-PROTO-5 faz **edição cirúrgica** em
  `workflow.md`, `delivery.md`, `session_conventions.md`. W-PROTO-1
  depois reescreve esses três por motivo diferente (linguagem
  per-funcionalidade → per-milestone). Cirúrgico evita doc
  inconsistente no ar e não gera retrabalho significativo (W-PROTO-1
  precisa reescrever seções inteiras de qualquer jeito).
- **Overlap com W-PROTO-3:** `templates/delivery-report.md` ganha
  Seção 🎯 aqui; W-PROTO-3 absorve depois no shape de milestone.
  Declarado inline.
- **Dependência transitiva:** MCP server GitHub (`mcp__github__...`)
  precisa estar disponível no runner do Claude Code Web. Já está,
  conforme uso neste refinamento.
- **Permissão de criar PR:** o token usado pelo Claude Code Web
  precisa ter escopo `pull_request: write` no repo. Confirmado pelo
  histórico — o dev hoje cria PR manualmente pela interface, mas o
  MCP server já está configurado no repo (conforme lista de tools
  `mcp__github__create_pull_request` disponível).

##### e) Sequência e testes

**Dependências entre funcionalidades do épico:**
Não há sub-funcionalidades — o épico é uma mudança processual coesa.
Ordem sugerida de implementação interna:
1. Editar `skills/rte/skill.md` (regras, Passo 6.5, Passo 7, falhas).
2. Editar `skills/rte/templates/delivery-report.md` (Seção 🎯).
3. Editar `docs/process/refinement/epic_completion.md`.
4. Edições cirúrgicas em `workflow.md` e `delivery.md`.

**Escopo de teste:**
- **Unit/integration:** N/A (épico 100% documental + processual; sem
  código executável novo).
- **Validação manual:** próximo milestone autônomo executado (candidato
  natural: W-PROTO-3, cirúrgico e pequeno, primeira prova do fluxo
  novo). Critério observável: a sessão termina com PR aberta contendo
  Seção 🎯 completa (sem placeholders), a cópia da seção no Copilot
  retorna tabela de critérios preenchida, dev mergeia sem rodar
  comandos locais.

**Critérios de aceite observáveis:**
- [ ] `skills/rte/skill.md` deixa explícito que RTE cria PR; Passo 6.5
  existe e descreve o template da Seção 🎯; CRITÉRIOS DE FALHA não
  contêm mais "tentou criar PR".
- [ ] `docs/process/refinement/epic_completion.md` não exige mais
  "validação local antes de PR"; referência à PR aberta como entrada
  da revisão humana.
- [ ] `docs/process/autonomous/workflow.md` diagrama termina em "PR
  aberta"; seção RTE declara criação de PR.
- [ ] `docs/process/autonomous/delivery.md` descreve revisão via PR +
  Copilot, não validação local pré-PR.

**Simplificações (estágio Protótipo):** nenhuma — épico é documental,
todos os critérios são textualmente verificáveis.

**Migra de:** refinamento iniciado em 2026-04-24 na branch
`claude/continue-workflow-implementation-5PKVa`.

#### ÉPICO W-PROTO-6: Skill de faxina + GitHub Action pós-merge

**Milestone:** `PROTO-WORKFLOW-ENCERRAMENTO`

**Objetivo:** automatizar enxugamento do ROADMAP e transição de estado
(🏗️→✅) via GitHub Action disparada no merge da PR de milestone.
Cria `skills/cleanup/skill.md` com as regras determinísticas (reduzir
épico a título + 1-2 linhas + PR; virar status na tabela do milestone);
`.github/workflows/milestone-cleanup.yml` roda Claude Code via Action
oficial da Anthropic no runner, carrega a skill, e grava o resultado
na main (direto ou via PR secundária, conforme branch protection).
Primeira skill do projeto executada via GitHub Action em vez de via
Claude Code Web — estabelece o padrão para automações futuras.

**Status:** 🏗️ Em andamento

**Dependências:**
- **W-PROTO-7** — bloqueante. Extração precisa sair do rito de
  fechamento antes de a faxina ser automatizada. A skill cleanup
  cobre **só** enxugamento + transição (determinísticos).
- **W-PROTO-5** — conteúdo. O trigger da Action é o merge da PR
  aberta pela RTE via W-PROTO-5.

**Motivação:** atrito observado em W-POC-4 — rito de fechamento manual
consome ~300 linhas de edição em ROADMAPs após merge, tarefa repetitiva
e mecânica que não exige julgamento do dev nem do implementador.

##### a) Termos e conceitos

- **Fase de higiene** = tudo que roda depois do merge da PR de
  milestone. Escopo: enxugamento do épico no ROADMAP + transição
  🏗️→✅. Definição introduzida em W-PROTO-5; consolidada aqui.
- **Skill executada em Action** = primeira skill do paper-agent que
  não é carregada pelo Claude Code Web mas por um workflow do
  GitHub Actions invocando Claude Code via Action oficial da
  Anthropic (ex.: `anthropics/claude-code-action` — nome exato a
  confirmar na implementação). Serve de template para automações
  futuras (candidatas na fase Protótipo e além).
- **ID de milestone na branch** = `milestone/<id-em-caixa-baixa>`.
  Padrão já estabelecido em W-POC-3; é o único identificador que a
  Action precisa para localizar o milestone no ROADMAP relevante.

##### b) Dados e contratos

**Shape do trigger (`.github/workflows/milestone-cleanup.yml`):**

```yaml
on:
  pull_request:
    types: [closed]
    branches: [main]
```

Action roda **somente** quando:
1. `github.event.pull_request.merged == true` (ignora PR fechada sem
   merge).
2. `startsWith(github.event.pull_request.head.ref, 'milestone/')`
   (ignora PRs que não são de milestone).

**Shape do input da skill cleanup** (passado como variáveis de ambiente
ou argumento do prompt inicial):
- `MILESTONE_ID` — extraído do `head.ref` via regex
  `milestone/(.+)` → upper-case (ex.:
  `milestone/proto-workflow-encerramento` →
  `PROTO-WORKFLOW-ENCERRAMENTO`).
- `MERGED_PR_URL` — `github.event.pull_request.html_url`, pra linkar
  no enxugamento.
- `MERGE_SHA` — `github.event.pull_request.merge_commit_sha`, pra
  compor link de commit no enxugamento se aplicável.

**Shape do output da skill cleanup:**
- Edições em 1 ou mais ROADMAPs (`docs/process/workflow/ROADMAP.md`,
  `docs/ROADMAP.md`, `products/<produto>/ROADMAP.md`) — conforme
  onde o milestone está declarado.
- Commit único: `chore(cleanup): faxina pós-merge <MILESTONE_ID>` +
  body com lista de épicos transitados e link do PR mergeado.

**Estratégia de escrita** (depende de acoplamento d):
- **Modo A — commit direto em main** (preferido se branch protection
  permitir): Action faz `git commit` + `git push origin main` no
  próprio runner.
- **Modo B — PR secundária** (fallback se main tem proteção): Action
  cria branch `cleanup/<milestone-id>-<timestamp>`, commita ali, abre
  PR auto-merge habilitado via `peter-evans/create-pull-request` ou
  equivalente. A skill `cleanup` não precisa saber qual modo —
  workflow resolve.

##### c) Código-alvo e integração

**Arquivos a criar:**
- `skills/cleanup/skill.md` — spec executável determinística. Sem
  julgamento arquitetural: só aplica regras. Estrutura (seguindo
  padrão de outras skills):
  - PAPEL: "aplicar enxugamento e transição de estado aos épicos do
    milestone mergeado".
  - REGRAS NÃO-NEGOCIÁVEIS: nunca tocar extração; nunca alterar
    ARCHITECTURE/core-docs; nunca criar código; aborta se
    current_implementation.md reporta épico não-✅ nas tabelas de
    gates; escreve só em arquivos com sufixo `ROADMAP.md`.
  - SEQUÊNCIA OBRIGATÓRIA:
    1. Localizar milestone no ROADMAP (grep por `MILESTONE_ID`).
    2. Validar gates: todos os épicos do milestone têm tabelas
       Dev/QA/TL/PO ✅ em `current_implementation.md` (arquivo já
       mergeado em main).
    3. Para cada épico do milestone: aplicar enxugamento conforme
       `docs/process/refinement/epic_completion.md` (reduzir a
       título + 1-2 linhas + link PR + link docs permanentes).
    4. Virar status do épico para `✅ Implementado`.
    5. Virar status do milestone conforme regra do ROADMAP do
       produto/core (se aplicável).
    6. Commitar via git (modo A ou B conforme ambiente).
  - CRITÉRIOS DE SUCESSO / FALHA.
- `skills/cleanup/README.md` — visão geral humana (mesmo padrão de
  `skills/rte/README.md`, `skills/em/README.md`, etc.).
- `.github/workflows/milestone-cleanup.yml` — workflow do GitHub
  Actions. Estrutura:
  - `runs-on: ubuntu-latest`.
  - Checkout `main` com `fetch-depth: 0`.
  - Setup da Action oficial Claude Code (`anthropics/claude-code-action`
    ou equivalente; nome exato e versão a confirmar; ver "Acoplamentos").
  - Passa como prompt inicial: "carregue `skills/cleanup/skill.md`
    e execute com MILESTONE_ID=<valor>, MERGED_PR_URL=<valor>,
    MERGE_SHA=<valor>".
  - Commit+push (modo A) ou create-pull-request (modo B), decidido
    por variável de ambiente/config do workflow.
  - Secrets requeridos: `ANTHROPIC_API_KEY` (tem que ser adicionado
    ao repo antes do primeiro run; declarar no épico como setup
    operacional).

**Arquivos a modificar:**
- `docs/process/refinement/epic_completion.md` — **mudanças:**
  1. Já terá sido alterado por W-PROTO-7 (remoção da extração). Aqui
     declarar explicitamente que "Enxugamento" e "Transição" são
     executadas por `skills/cleanup/skill.md` via
     `.github/workflows/milestone-cleanup.yml`; manual como fallback
     se Action falhar.
  2. Nova seção curta "Fallback manual" com os comandos que o dev
     roda se a Action não disparar/falhar.
- `docs/ARCHITECTURE.md` — seção "Estrutura do Projeto" (verificar se
  existe; grep mostra referência em `ROADMAP.md` linha 254): adicionar
  `.github/workflows/` + `skills/cleanup/` à listagem.
- `docs/process/workflow/vision.md` — nota curta sobre padrão "skill
  em Action" emergindo (candidata a virar padrão reutilizável).

**Mecanismo de integração:**
- Workflow GitHub Actions escuta `pull_request.closed` na branch
  `main`, filtra por branch de origem começando com `milestone/`.
- Quando dispara: runner faz checkout, invoca Claude Code via Action
  oficial, passando o `skill.md` como prompt de entrada + variáveis
  extraídas do evento.
- Claude Code carrega a skill, executa os passos, edita arquivos
  conforme regras.
- Workflow faz commit/push (modo A) ou cria PR secundária (modo B)
  conforme configuração.

**Template de estilo/estrutura:**
- Skill nova: **`skills/em/skill.md` como template** (EM é pequena,
  determinística, só escreve em arquivos específicos — perfil similar
  ao que cleanup precisa). Usar o mesmo shape de PAPEL / REGRAS /
  SEQUÊNCIA / CRITÉRIOS.
- Workflow: **`.github/workflows/test-unit.yml` como template mínimo**
  para forma de arquivo e `runs-on`. A seção da Action Claude Code é
  adicional.

##### d) Acoplamentos

- **Branch protection em main:** **a verificar durante implementação.**
  Se main tem proteção "require pull request reviews", modo A (commit
  direto) falha; modo B (PR secundária) é obrigatório. Recomendação:
  implementar modo B por padrão (conservador); dev humano auto-mergeia
  a PR de cleanup se quiser, ou habilita auto-merge da Action. Workflow
  deve tentar A; se falhar com erro de policy, cair para B na mesma
  execução.
- **Action oficial Claude Code:** **a verificar durante implementação.**
  Nome e versão exatos dependem do que a Anthropic publicou (candidatos:
  `anthropics/claude-code-action@v1`, `anthropics/claude-code-base-action`).
  Declarar o nome exato no `.yml` na implementação; o épico estabelece
  que a integração existe.
- **Secret `ANTHROPIC_API_KEY`:** precisa ser adicionado ao repo
  (Settings → Secrets → Actions) antes do primeiro run. Passo manual,
  fora do commit de W-PROTO-6. Declarado como "pré-requisito
  operacional" no README da skill cleanup.
- **Custo por execução:** Action roda 1× por merge de milestone. Custo
  de Claude Code por run: baixo (edição mecânica em ROADMAP de ~300
  linhas; cabe em uma Sonnet run < $0.50). Sem throttling necessário
  na POC.
- **Dependência transitiva do W-PROTO-7:** `current_implementation.md`
  mergeado em main precisa ter bloco "Extração pendente" com todos
  os itens `[x]` — a skill cleanup **valida** isso no início (read-only,
  não tenta extrair). Se achar item `[ ]`, aborta com erro no log da
  Action (dev investiga manualmente).
- **Ordem de merge não é um problema:** cleanup é idempotente — roda
  de novo se dev rodar manualmente depois de um run falho; a primeira
  execução é a que marca ✅, próximas são no-op.
- **Overlap com W-PROTO-5:** depende só do conteúdo do W-PROTO-5 (PR
  que é mergeada) — a Action já está genérica pra qualquer PR de
  milestone. Sem overlap de código.

##### e) Sequência e testes

**Dependências entre funcionalidades do épico:**
Sub-funcionalidades internas, implementadas em ordem:
1. **Cria `skills/cleanup/skill.md` + `skills/cleanup/README.md`**
   (skill funciona mesmo sem a Action — dev pode chamar manualmente
   via Claude Code Web como fallback).
2. **Edita `docs/process/refinement/epic_completion.md`** para
   declarar automação + fallback manual.
3. **Cria `.github/workflows/milestone-cleanup.yml`** (infra em
   cima da skill já funcional).
4. **Atualiza `docs/ARCHITECTURE.md`** + nota em
   `docs/process/workflow/vision.md`.
5. **Passo manual (fora do commit):** dev adiciona secret
   `ANTHROPIC_API_KEY` ao repo; teste da Action roda em merge real
   ou em merge simulado via `workflow_dispatch`.

**Escopo de teste (Protótipo — rigor formal exigido):**
- **Validação manual do skill.md:** carregar a skill em uma sessão
  Claude Code Web contra uma branch de teste (pode ser a própria
  branch deste épico antes do merge); aplicar enxugamento em um
  milestone fictício ou no próprio W-PROTO-5/6/7 se já fechados;
  verificar que o output respeita as regras (só mexe em ROADMAP,
  aborta se gates pendentes).
- **Dry-run da Action:** habilitar `workflow_dispatch` temporariamente
  no workflow + invocar via UI do GitHub Actions passando parâmetros
  manuais. Observar que o Claude Code Action executa, a skill corre,
  o commit é gerado (modo A ou B).
- **Teste real:** o próprio merge da PR do milestone
  `PROTO-WORKFLOW-ENCERRAMENTO` **não** dispara a Action
  retroativamente (GitHub lê o workflow YAML da branch base =
  `main` no momento do evento; o YAML só chega em `main` **depois**
  do merge). O primeiro teste real é no próximo milestone fechado
  após W-PROTO-6 estar em `main`.
- **Critério de aceite:** próximo milestone fechado após W-PROTO-6
  tem o ROADMAP atualizado automaticamente; dev confirma via diff
  da Action no histórico do GitHub.

**Critérios de aceite observáveis:**
- [ ] `skills/cleanup/skill.md` existe e segue padrão de outras
  skills (PAPEL / REGRAS / SEQUÊNCIA / CRITÉRIOS DE SUCESSO-FALHA).
- [ ] `skills/cleanup/README.md` existe.
- [ ] `.github/workflows/milestone-cleanup.yml` existe e declara
  trigger `pull_request.closed` + filtro `merged == true` + filtro
  `branch startsWith milestone/`.
- [ ] `docs/process/refinement/epic_completion.md` declara
  automação + nota de fallback manual.
- [ ] Secret `ANTHROPIC_API_KEY` configurado no repo (verificado
  pelo dev, não commitável).
- [ ] Dry-run via `workflow_dispatch` completa sem erro em um
  milestone de teste.

**Simplificações (estágio Protótipo — nenhuma quebra formal, mas
estas são verificações adiadas deliberadamente):**
- Nome/versão exata da Action Claude Code da Anthropic: declarada
  aqui como "investigar na implementação" porque a API de Actions da
  Anthropic está em movimento. O épico trata isso como Acoplamento a
  verificar, não como Simplificação de POC.
- Modo A vs B de commit: a implementação escolhe conforme o que
  funciona no repo. Não é Simplificação — é decisão a materializar
  na implementação com base no teste de branch protection.

**Migra de:** refinamento iniciado em 2026-04-24 na branch
`claude/continue-workflow-implementation-5PKVa`.

#### ÉPICO W-PROTO-7: Extração pra ARCHITECTURE.md como passo do implementador

**Milestone:** `PROTO-WORKFLOW-ENCERRAMENTO`

**Objetivo:** mover extração de conhecimento permanente (padrões novos
em `docs/ARCHITECTURE.md` ou `core/docs/architecture/`, notas em
`.claudecode.md`, comportamento em `core/docs/agents/<agente>/`) do
rito de fechamento (`epic_completion.md`) pra dentro da fase de
implementação. Responsabilidade distribuída: **TL identifica** o que
merece virar padrão permanente; **Dev executa** as edições no próximo
commit; **RTE confirma** que não há extração pendente antes do push +
abertura de PR. `epic_completion.md` passa a cobrir só enxugamento +
transição (partes determinísticas que a Action de W-PROTO-6 consegue
executar).

**Status:** 🏗️ Em andamento

**Dependências:** nenhuma própria. É pré-requisito de conteúdo (não
de código) para W-PROTO-6 — a Action de cleanup só pode assumir
"extração feita" depois que este épico definir ONDE ela é feita.

**Motivação:** extração exige julgamento ("isso é padrão reusável?
merece entrada em ARCHITECTURE.md?") e não pode ser automatizada.
Separar dos passos mecânicos (enxugamento + transição) libera esses
últimos pra automação em W-PROTO-6.

##### a) Termos e conceitos

- **Extração** = ato de identificar conhecimento permanente gerado por
  um épico e gravar em docs/ARCHITECTURE.md, core/docs/architecture/,
  core/docs/agents/<agente>/ ou .claudecode.md. Definição já existe em
  `docs/process/refinement/epic_completion.md` seções a/b/c — este
  épico move o **ato**, não redefine o conceito.
- **Conhecimento permanente** = padrão arquitetural novo, decisão
  técnica reutilizável por outros épicos, comportamento de agente
  que o código sozinho não expressa. Lista não-exaustiva no próprio
  `epic_completion.md` (mantida).
- **Extração pendente** = novo bloco em `current_implementation.md`
  onde TL registra itens a extrair; Dev marca como feito conforme
  executa.

##### b) Dados e contratos

**Shape do bloco "Extração pendente" em `current_implementation.md`**
(adicionado ao template gerado pela Scrum Master Skill):

```markdown
## Extração pendente

Itens identificados pelo TL durante os gates como conhecimento
permanente a gravar em docs estruturais. Dev executa antes da próxima
funcionalidade/épico. RTE aborta se houver `- [ ]` pendente.

### Épico <ID-EPICO-1>
- [ ] `docs/ARCHITECTURE.md` §<seção>: <o que gravar em 1 linha>
- [x] `core/docs/agents/<agente>/<arquivo>.md`: <o que gravar>
- [ ] `.claudecode.md`: <o que gravar>

### Épico <ID-EPICO-2>
- (vazio — TL não identificou conhecimento permanente neste épico)
```

**Contrato TL → current_implementation.md:**
- TL, no Passo de aprovação de cada funcionalidade, adiciona item a
  "Extração pendente" quando julgar aplicável. Item deve citar
  arquivo-alvo + descrição curta. Item vazio = TL avaliou e nada a
  extrair (registrar explicitamente `(vazio — TL não identificou
  conhecimento permanente neste épico)` no bloco do épico ao fechar
  a última funcionalidade).

**Contrato Dev → current_implementation.md:**
- Dev, antes de iniciar a próxima funcionalidade OU no último commit
  do épico, executa os itens pendentes e marca `[x]`. Edições ficam
  no mesmo commit que já faria do épico (Dev decide a granularidade
  de commit, conforme decisão de W-PROTO-5 sobre "commits a critério
  do agente").

**Contrato RTE → gate de entrada:**
- Novo check duro no Passo 1 da RTE: "Todos os itens de 'Extração
  pendente' estão `[x]`". Se houver `[ ]`, **aborta** com mensagem
  dizendo quais itens faltam e devolve ao Dev.

##### c) Código-alvo e integração

**Arquivos a modificar (deste épico):**
- `docs/process/refinement/epic_completion.md` — **mudanças:**
  1. Seção "Três Tipos de Conteúdo e Seus Destinos" mantida (serve
     de guia pro TL julgar).
  2. Checklist "Extração" (linhas 31-36 atuais) removida do rito
     pós-merge. Substituída por nota curta dizendo que extração é
     responsabilidade da fase de implementação (link para `skills/tl/
     skill.md` e `skills/rte/skill.md`).
  3. Checklist "Enxugamento" e "Transição de estado" mantidos; em
     W-PROTO-6 passam a ser automatizados.
- `skills/tl/skill.md` — **mudanças:**
  1. Passo 3 "Verificações arquiteturais" ganha sub-seção nova **3.5
     Identificação de conhecimento permanente** descrevendo quando
     um item merece extração (usar os tipos b/c de
     `epic_completion.md` como guia).
  2. Passo 7 (ou o passo que grava decisão final; checar skill.md)
     inclui registro em `current_implementation.md` → "Extração
     pendente" quando TL aprovar a funcionalidade. Item sempre
     declarado, mesmo quando vazio (marcador explícito no fechamento
     do épico).
- `skills/rte/skill.md` — **uma mudança cirúrgica no Passo 1:**
  novo bullet nos "Checks duros": "Bloco 'Extração pendente' em
  `current_implementation.md` não tem item `- [ ]` (todos `[x]` ou
  declarações explícitas de vazio por épico)". Se falhar, a mensagem
  de aborto lista os itens pendentes agrupados por épico.
- `skills/scrum-master/skill.md` — **uma mudança cirúrgica na seção
  "TEMPLATE DE `current_implementation.md`"** (linhas 141-260
  atuais): adicionar o bloco `## Extração pendente` (shape acima)
  entre "Esclarecimentos" e "Status dos Gates (nível milestone)".
  Template renderizado pelo Scrum Master Passo 5 passa a incluir o
  bloco automaticamente; começa vazio (TL preenche).
- `docs/process/autonomous/workflow.md` — **edição cirúrgica** na
  seção "4. TL SKILL": item novo em "Deve verificar" citando
  "identificar conhecimento permanente e registrar em 'Extração
  pendente' de `current_implementation.md`". Mesma lógica
  cirúrgica-antes-de-W-PROTO-1 do W-PROTO-5.

**Mecanismo de integração:**
- Já existente: TL grava decisões em `current_implementation.md`
  (skill.md:52-55); extração é novo campo gravado no mesmo
  mecanismo.
- Já existente: RTE lê `current_implementation.md` no Passo 1
  (skill.md:37-55); novo check é um bullet adicional no Passo 1.
- Já existente: Scrum Master escreve template inicial
  (skill.md:141-260); "Extração pendente" é nova seção estática no
  template.

**Template de estilo/estrutura:**
- Para o bloco em `current_implementation.md`: o próprio bloco
  "Gates por funcionalidade" (tabela markdown simples) serve como
  referência de granularidade e estilo.
- Para a sub-seção 3.5 em `skills/tl/skill.md`: as sub-seções
  existentes 3.1-3.4 (Estrutura, Contratos, Aderência, Qualidade)
  servem como template de tom e granularidade.

##### d) Acoplamentos

- **TL hoje roda por funcionalidade** (skills/tl/skill.md:12) —
  identificação de extração por funcionalidade é natural; a
  consolidação por épico acontece no momento em que TL aprova a
  última funcionalidade do épico (fecha o bloco do épico com
  `(vazio — ...)` se nada foi identificado).
- **Dev não tem skill.md própria.** A obrigação de executar itens
  pendentes é gravada em `docs/process/autonomous/workflow.md`
  seção "2. DEV (Implementação)" como novo item em "Deve" +
  mencionada em `skills/tl/skill.md` (TL devolve ao Dev se Dev
  passou pra próxima funcionalidade com item `[ ]` aberto do
  mesmo épico). Ficará mais robusto quando W-PROTO-1 reescrever
  workflow.md — aqui fica cirúrgico.
- **Overlap com W-PROTO-6:** este épico define que "fase de
  higiene" (W-PROTO-6) assume extração = ✅. A skill `cleanup` em
  W-PROTO-6 não toca ARCHITECTURE/core-docs/.claudecode — só
  ROADMAP. Sem overlap de código.
- **Retroatividade:** épicos já em `🏗️` no momento de implementação
  deste ficam sem bloco "Extração pendente" (template já foi
  gerado). Não há como aplicar retroativamente; dev segue com rito
  antigo pra esses. Declarar na "Retroatividade" do
  `epic_completion.md`.

##### e) Sequência e testes

**Dependências entre funcionalidades do épico:**
Não há sub-funcionalidades. Ordem sugerida de implementação interna:
1. Editar `docs/process/refinement/epic_completion.md` (remover
   extração do pós-merge, linkar skills).
2. Editar `skills/scrum-master/skill.md` (novo bloco no template).
3. Editar `skills/tl/skill.md` (sub-seção 3.5 + registro).
4. Editar `skills/rte/skill.md` (novo check duro Passo 1).
5. Edição cirúrgica em `docs/process/autonomous/workflow.md`.

**Escopo de teste:**
- **Unit/integration:** N/A (épico 100% documental + processual).
- **Validação manual:** próximo milestone autônomo executado após
  W-PROTO-5 (candidato: mesmo W-PROTO-3 usado para validar
  W-PROTO-5, já que esses três épicos formam unidade). Critérios
  observáveis:
  - Template gerado pelo Scrum Master contém bloco "Extração
    pendente".
  - TL grava ao menos uma linha por épico (pode ser declaração de
    vazio).
  - RTE aborta em dry-run quando ação simular item pendente.
  - `epic_completion.md` revisado no PR não contém mais checklist
    de extração.

**Critérios de aceite observáveis:**
- [ ] `docs/process/refinement/epic_completion.md` remove checklist
  de extração; mantém enxugamento + transição; nota aponta para as
  skills.
- [ ] `skills/scrum-master/skill.md` seção "TEMPLATE DE
  `current_implementation.md`" contém bloco "Extração pendente"
  com shape descrito acima.
- [ ] `skills/tl/skill.md` tem sub-seção 3.5 e grava registro em
  "Extração pendente" (citação literal no passo de aprovação).
- [ ] `skills/rte/skill.md` Passo 1 "Checks duros" inclui novo
  bullet sobre Extração pendente = 0 itens `[ ]`.
- [ ] `docs/process/autonomous/workflow.md` seção TL lista extração
  em "Deve verificar".

**Simplificações (estágio Protótipo):** nenhuma — épico é
documental, todos os critérios são textualmente verificáveis.

**Migra de:** refinamento iniciado em 2026-04-24 na branch
`claude/continue-workflow-implementation-5PKVa`.

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
encerramento) e foram agrupados no milestone
`PROTO-WORKFLOW-ENCERRAMENTO`. Ordem sugerida de execução: W-PROTO-5
(processual, baixo custo) → W-PROTO-7 (separa extração da faxina) →
W-PROTO-6 (infra de automação). Os três foram refinados em conjunto
em 2026-04-24 na branch `claude/continue-workflow-implementation-5PKVa`
e estão em `🔍 Detalhes definidos` — prontos para dispatch autônomo
via Claude Code Web (a gatilhar pelo operador). W-PROTO-1/2/3/4
(dívida documental da reforma de milestone) vivem em
`PROTO-WORKFLOW-DOC` e permanecem em `🌱 Visão` pendentes de
refinamento tático; os dois milestones da fase Protótipo são
independentes e podem ser executados em qualquer ordem.

A quebra da fase Protótipo do Workflow em dois milestones
(`PROTO-WORKFLOW-ENCERRAMENTO` e `PROTO-WORKFLOW-DOC`) foi aplicada
em 2026-04-24 como bootstrap manual da convenção "sessão = milestone
coerente" — similar ao bootstrap de W-POC-1/2. Para evitar que o
erro do milestone-balaio se repita, foi introduzido um checklist de
coerência no refinamento estratégico em
`docs/process/refinement/planning_guidelines.md` (seção "Checklist
de coerência para declarar um milestone").

**Observação sobre evolução da EM skill.** A EM skill hoje decide
sobre tamanho (FIT/TIGHT/OVERFLOW) com base em LOC e risco, rodando
**depois** da PM skill no fluxo autônomo. Isso significa que, se o
checklist estratégico falhar e um milestone-balaio chegar ao dispatch,
o refinamento tático (PM) já foi executado antes da EM detectar o
problema — desperdiçando trabalho. Caminhos considerados e ainda não
formalizados em épico: (a) EM ganha preflight de coerência antes da
PM (detecção via métrica de acoplamento entre épicos, devolve antes
de PM rodar); (b) manter ordem atual e aceitar que EM emite warning
tardio com custo de PM já pago; (c) nova skill "Coherence" entre
Dispatch e PM, especializada em verificar coerência do agrupamento.
Decisão adiada — vira épico na fase Protótipo ou MVP quando houver
sinal real de necessidade (erro recorrente que o checklist estratégico
não pegou). Primeiro instrumento de detecção é o próprio checklist
estratégico introduzido nesta reforma.

Épicos MVP ainda não foram desenhados — ficam a definir em refinamento
estratégico após ambos os milestones da fase Protótipo fecharem, com
aprendizado real no bolso.
