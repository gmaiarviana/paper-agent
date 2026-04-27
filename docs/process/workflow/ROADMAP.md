# ROADMAP — Workflow de Desenvolvimento

Milestones e épicos do processo de desenvolvimento do paper-agent.

> Visão completa em [vision.md](vision.md).

> **🧭 Estados dos épicos:** ver [planning_guidelines.md](../refinement/planning_guidelines.md) para definições completas.

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
- **Nota:** dívida residual da reforma de milestone (M4-restante, M5,
  M6 e dívidas do W-POC-3) foi absorvida pelos milestones
  `PROTO-WORKFLOW-ENCERRAMENTO` (W-PROTO-5..7) e `PROTO-WORKFLOW-DOC`
  (W-PROTO-DOC-1/2/3) — ambos já mergeados. O antigo
  `docs/process/refactor-backlog.md` foi migrado para este ROADMAP e
  removido.

### PROTO-WORKFLOW-ENCERRAMENTO

- **Objetivo:** refinamento do ciclo de encerramento autônomo —
  validação async via PR, extração como passo do implementador, faxina
  mecânica via GitHub Action pós-merge.
- **Estágio:** Protótipo
- **Épicos agrupados:** W-PROTO-5, W-PROTO-6, W-PROTO-7
- **Dependências de core:** nenhuma
- **Branch associada:** `milestone/proto-workflow-encerramento`
- **Status dos épicos:** W-PROTO-5 ✅, W-PROTO-6 ✅, W-PROTO-7 ✅.
- **Implementado em:** PR https://github.com/gmaiarviana/paper-agent/pull/83 (merge `94173a9`, 2026-04-25).

### PROTO-WORKFLOW-DOC

- **Objetivo:** consolidar a reforma de milestone na documentação do
  fluxo — absorver cirurgias do `PROTO-WORKFLOW-ENCERRAMENTO` em
  reescrita coerente per-milestone (`docs/process/autonomous/`),
  migrar `skills/rte/templates/delivery-report.md` pro shape de
  milestone, fechar ponteiros quebrados e vocabulário antigo em
  arquivos periféricos.
- **Estágio:** Protótipo
- **Épicos agrupados:** W-PROTO-DOC-1, W-PROTO-DOC-2, W-PROTO-DOC-3
- **Dependências de core:** nenhuma
- **Branch associada:** `milestone/proto-workflow-doc`
- **Status dos épicos:** W-PROTO-DOC-1 ✅, W-PROTO-DOC-2 ✅,
  W-PROTO-DOC-3 ✅.
- **Implementado em:** PR https://github.com/gmaiarviana/paper-agent/pull/90 (merge `dc00f67`, 2026-04-26).

### PROTO-WORKFLOW-AJUSTES

- **Objetivo:** consolidar dois ajustes de qualidade na fase Protótipo —
  corrigir a criação de PR pela RTE para ser autônoma e cobrir todos
  os commits do milestone; desacoplar as descrições dos estados de
  épico das ferramentas e nomear formalmente os dois tipos de sessão
  (implementação e refinamento).
- **Estágio:** Protótipo
- **Épicos agrupados:** W-PROTO-8, W-PROTO-9
- **Dependências de core:** nenhuma
- **Branch associada:** `milestone/proto-workflow-ajustes`
- **Status dos épicos:** W-PROTO-8 ✅, W-PROTO-9 ✅.
- **Implementado em:** PR https://github.com/gmaiarviana/paper-agent/pull/93 (merge `a687743`, 2026-04-27).

### PROTO-WORKFLOW-PLATAFORMA

- **Objetivo:** central de acompanhamento da plataforma de workflow —
  kanban com todos os estados de épicos de todos os ROADMAPs
  configurados, ações contextuais por estado (dispatch para 🔍,
  acompanhamento de 🏗️/🔀, direcionamento de refinamento para estados
  pré-execução). Operador visualiza o estado de todos os épicos e é
  direcionado para a próxima ação sem precisar ler o ROADMAP à mão.
- **Estágio:** Protótipo
- **Épicos agrupados:** W-PROTO-PLAT-1, W-PROTO-PLAT-2,
  W-PROTO-PLAT-3, W-PROTO-PLAT-4
- **Dependências de core:** nenhuma
- **Branch associada:** `milestone/proto-workflow-plataforma`
- **Status dos épicos:** W-PROTO-PLAT-1 📋, W-PROTO-PLAT-2 📋,
  W-PROTO-PLAT-3 📋, W-PROTO-PLAT-4 📋.
- **Nota:** milestone refinado em 2026-04-27 na branch
  `claude/refine-workflow-mvp-tu06p`. Épicos em `📋 Critérios
  definidos` — prontos para fluxo manual via Cursor. Refinamento
  tático (via PM skill ou Claude Web) leva a `🔍 Detalhes definidos`
  antes do dispatch autônomo.

### MVP-WORKFLOW-PLATAFORMA

- **Objetivo:** plataforma com fila de decisões populada
  automaticamente por eventos de estado do repo e das PRs, e chat
  focado por item com contexto pré-carregado. Operador chega e
  encontra a próxima decisão esperando, sem montar a fila
  manualmente.
- **Estágio:** MVP
- **Épicos agrupados:** W-MVP-PLAT-1, W-MVP-PLAT-2, W-MVP-PLAT-3
- **Dependências de core:** nenhuma; depende de
  PROTO-WORKFLOW-PLATAFORMA (scaffold e kanban como base)
- **Branch associada:** `milestone/mvp-workflow-plataforma`
- **Status dos épicos:** W-MVP-PLAT-1 📐, W-MVP-PLAT-2 📐,
  W-MVP-PLAT-3 📐.
- **Tensões para refinamento estratégico:**
  - **(a) Quem cria itens "PR pra revisar"?** Inclinação: RTE no
    mesmo passo em que abre PR (W-PROTO-5 estendido). Alternativa:
    observador da plataforma detecta PR aberta via GitHub API.
  - **(b) Auto-regulação por capacidade (~20 itens).** Gatilho duro
    (autônomo trava de criar) ou soft (só prioriza)? Limite por tipo
    de item ou agregado?
  - **(c) Reconstrução da fila se plataforma cair.** Varrer markdown
    + estado de PRs deve reconstruir a fila deterministicamente —
    teste prático do princípio "markdown é fonte da verdade".
- **Nota:** milestone declarado em 2026-04-27. Épicos em `📐
  Funcionalidades esboçadas` — aguardam refinamento estratégico antes
  do dispatch.

### MVP-WORKFLOW-REFINADOR

- **Objetivo:** refinador autônomo como processo de fundo — avança
  épicos de 🌱/📐 sem supervisão contínua, para limpo ao travar, e
  deposita resultado na fila da plataforma como item de decisão.
- **Estágio:** MVP
- **Épicos agrupados:** W-MVP-REF-1, W-MVP-REF-2
- **Dependências de core:** nenhuma; depende de
  MVP-WORKFLOW-PLATAFORMA (fila como destino dos itens produzidos)
- **Branch associada:** `milestone/mvp-workflow-refinador`
- **Status dos épicos:** W-MVP-REF-1 📐, W-MVP-REF-2 📐.
- **Fora do MVP (longo prazo):** Proponente (1×/dia), voice
  interface e workflow como produto desacoplado multi-repo vivem no
  [Horizonte de vision.md](vision.md#horizonte) e não estruturam
  decisões destes milestones.
- **Nota:** milestone declarado em 2026-04-27. Épicos em `📐
  Funcionalidades esboçadas` — aguardam refinamento estratégico antes
  do dispatch.

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

> **Milestones:** `PROTO-WORKFLOW-ENCERRAMENTO` (W-PROTO-5, 6, 7) · `PROTO-WORKFLOW-DOC` (W-PROTO-DOC-1, 2, 3) · `PROTO-WORKFLOW-AJUSTES` (W-PROTO-8, W-PROTO-9) · `PROTO-WORKFLOW-PLATAFORMA` (W-PROTO-PLAT-1..4).

#### ÉPICO W-PROTO-DOC-1: Reescrita per-milestone de `docs/process/autonomous/`

**Milestone:** `PROTO-WORKFLOW-DOC`

**Status:** ✅ Implementado

**Entregue em:** PR https://github.com/gmaiarviana/paper-agent/pull/90 (merge `dc00f67`, 2026-04-26) — `workflow.md`, `delivery.md`, `overview.md` e `session_conventions.md` reescritos no vocabulário per-milestone, absorvendo as cirurgias órfãs do W-PROTO-5/6/7 e fechando refs quebradas para `../development/`.

---

#### ÉPICO W-PROTO-DOC-2: Migração do template `skills/rte/templates/delivery-report.md` pro shape de milestone

**Milestone:** `PROTO-WORKFLOW-DOC`

**Status:** ✅ Implementado

**Entregue em:** PR https://github.com/gmaiarviana/paper-agent/pull/90 (merge `dc00f67`, 2026-04-26) — template de relatório de entrega reescrito para acomodar N épicos em sub-seções; Seção 🎯 Validação preservada; nota de dívida W-POC-3 removida da skill RTE.

---

#### ÉPICO W-PROTO-DOC-3: Saneamento residual em arquivos periféricos

**Milestone:** `PROTO-WORKFLOW-DOC`

**Status:** ✅ Implementado

**Entregue em:** PR https://github.com/gmaiarviana/paper-agent/pull/90 (merge `dc00f67`, 2026-04-26) — `planning_guidelines.md`, `implementation/overview.md` e `.github/copilot-instructions.md` atualizados para o vocabulário per-milestone; varredura de fechamento sem ocorrências de `feature/X.Y`.

---

#### ÉPICO W-PROTO-5: Validação async — PR antes da aprovação, Copilot como validador local

**Milestone:** `PROTO-WORKFLOW-ENCERRAMENTO`

**Status:** ✅ Implementado

**Entregue em:** PR https://github.com/gmaiarviana/paper-agent/pull/83 (merge `94173a9`, 2026-04-25) — RTE passa a abrir PR via `mcp__github__create_pull_request` com Seção 🎯 Validação copy-paste pronta para o Copilot; estado terminal da fase de implementação vira "PR aberta", com revisão humana movida para a própria PR.

---

#### ÉPICO W-PROTO-6: Skill de faxina + GitHub Action pós-merge

**Milestone:** `PROTO-WORKFLOW-ENCERRAMENTO`

**Status:** ✅ Implementado

**Entregue em:** PR https://github.com/gmaiarviana/paper-agent/pull/83 (merge `94173a9`, 2026-04-25) — `skills/cleanup/skill.md` + `.github/workflows/milestone-cleanup.yml` automatizam enxugamento e transição 🏗️→✅ no merge da PR de milestone; primeira skill do paper-agent executada via GitHub Action. Follow-up de log de tokens por run em commit `3aeab97`.

---

#### ÉPICO W-PROTO-7: Extração pra ARCHITECTURE.md como passo do implementador

**Milestone:** `PROTO-WORKFLOW-ENCERRAMENTO`

**Status:** ✅ Implementado

**Entregue em:** PR https://github.com/gmaiarviana/paper-agent/pull/83 (merge `94173a9`, 2026-04-25) — extração de conhecimento permanente sai do rito pós-merge e passa a ser registrada pelo TL em `current_implementation.md` (bloco "Extração pendente"), executada pelo Dev e checada pela RTE como gate de entrada.

---

#### ÉPICO W-PROTO-8: RTE cria PR com escopo completo e encerramento estruturado

**Milestone:** `PROTO-WORKFLOW-AJUSTES`

**Status:** ✅ Implementado

**Entregue em:** PR https://github.com/gmaiarviana/paper-agent/pull/93 (merge `a687743`, 2026-04-27) — Passo 6.5 da RTE corrigido para invocação autônoma com parâmetros explícitos; body da PR construído a partir do diff `main...HEAD` cobrindo todos os épicos; output estruturado pré-PR; rito de encerramento de sessão de refinamento formalizado em `planning_guidelines.md`.

---

#### ÉPICO W-PROTO-9: Desacoplar estados de épico das ferramentas + nomear tipos de sessão

**Milestone:** `PROTO-WORKFLOW-AJUSTES`

**Status:** ✅ Implementado

**Entregue em:** PR https://github.com/gmaiarviana/paper-agent/pull/93 (merge `a687743`, 2026-04-27) — descrições dos estados `📋` e `🔍` desancoradas de "via Cursor"/"via Claude Code Web"; bloco de estados consolidado em `planning_guidelines.md` (eliminando duplicação nos 6 ROADMAPs); dois tipos de sessão (implementação e refinamento) nomeados em `CONSTITUTION.md`.

---

#### ÉPICO W-PROTO-PLAT-1: Scaffold da plataforma

**Milestone:** `PROTO-WORKFLOW-PLATAFORMA`

**Objetivo:** estrutura Streamlit funcionando localmente, lendo ROADMAPs do repo e com navegação básica entre as views da plataforma.

**Status:** 📋 Critérios definidos

**Dependências:** nenhuma

### Funcionalidades:

#### 1.1: App Streamlit com configuração e navegação

- **Descrição:** App Streamlit estruturado com arquivo de configuração declarando quais ROADMAPs ler, leitura defensiva dos arquivos e navegação entre as views dos épicos seguintes.
- **Critérios de Aceite:**
  - Deve iniciar com `streamlit run` a partir do repo raiz sem erros
  - Deve ler ROADMAPs configurados sem travar se algum estiver ausente ou malformado
  - Deve ter estrutura de navegação entre as views dos épicos W-PROTO-PLAT-2, 3 e 4
  - Deve ter arquivo de configuração declarando quais ROADMAPs ler e qual repo GitHub usar
  - Deve funcionar em modo local sem dependência de serviço externo além de acesso de leitura ao GitHub

---

#### ÉPICO W-PROTO-PLAT-2: Kanban completo

**Milestone:** `PROTO-WORKFLOW-PLATAFORMA`

**Objetivo:** view com todos os épicos de todos os ROADMAPs configurados organizados por estado e milestone, numa única superfície de leitura.

**Status:** 📋 Critérios definidos

**Dependências:** W-PROTO-PLAT-1 (scaffold com leitura de ROADMAPs)

### Funcionalidades:

#### 2.1: Kanban de estados por milestone

- **Descrição:** Colunas para todos os 8 estados, cards agrupados por milestone e atualizados ao recarregar a página.
- **Critérios de Aceite:**
  - Deve exibir todos os 8 estados como colunas (🌱 → ✅)
  - Deve agrupar cards por milestone dentro de cada coluna; épicos órfãos ficam em grupo "Sem milestone"
  - Cada card deve exibir: id, título e milestone de origem
  - Deve consolidar épicos de todos os ROADMAPs configurados numa única view
  - Deve atualizar ao recarregar a página (live refresh não obrigatório)
  - Deve ser navegável com 20+ épicos ativos sem degradação visual

---

#### ÉPICO W-PROTO-PLAT-3: Ações de implementação

**Milestone:** `PROTO-WORKFLOW-PLATAFORMA`

**Objetivo:** ações contextuais nos cards de estados de execução (🔍/🏗️/🔀/✅) para o operador despachar, acompanhar e revisar sem precisar sair da plataforma.

**Status:** 📋 Critérios definidos

**Dependências:** W-PROTO-PLAT-2 (kanban com cards clicáveis)

### Funcionalidades:

#### 3.1: Dispatch para épicos em 🔍

- **Descrição:** Ao clicar num card em 🔍, exibe prompt de dispatch clipboard-ready com o milestone e instrução de execução para colar no Claude Code Web.
- **Critérios de Aceite:**
  - Deve exibir prompt de dispatch clipboard-ready ao selecionar épico em 🔍
  - O prompt deve identificar o milestone e indicar o alvo em linguagem natural (padrão `dispatch.md`)
  - Deve ter botão de copiar para clipboard

#### 3.2: Status e links para 🏗️, 🔀 e ✅

- **Descrição:** Cards em 🏗️ exibem branch com link; cards em 🔀 exibem link para a PR; cards em ✅ exibem resumo sem ações.
- **Critérios de Aceite:**
  - Para 🏗️: deve exibir nome da branch associada com link para o GitHub
  - Para 🔀: deve exibir link direto para a PR (lido da anotação `🔀 Em revisão — PR #N` no ROADMAP)
  - Para ✅: deve exibir resumo do épico sem ações disponíveis

---

#### ÉPICO W-PROTO-PLAT-4: Direcionamento de refinamento

**Milestone:** `PROTO-WORKFLOW-PLATAFORMA`

**Objetivo:** ações contextuais nos cards de estados pré-execução (🌱/🧭/📐/📋) que orientam o operador sobre o próximo passo de refinamento e geram o prompt de sessão pronto para usar.

**Status:** 📋 Critérios definidos

**Dependências:** W-PROTO-PLAT-2 (kanban com cards clicáveis)

### Funcionalidades:

#### 4.1: Exibição de próximo passo por estado

- **Descrição:** Ao clicar num card em estado pré-execução, exibe o que falta para avançar ao próximo estado com base nas definições de `planning_guidelines.md`.
- **Critérios de Aceite:**
  - Para 🌱/🧭/📐: deve indicar que o próximo passo é refinamento e qual o alvo (📋 ou 🔍)
  - Para 📋: deve indicar que o próximo passo é atingir 🔍 e apontar para `autonomous_readiness.md` como checklist do alvo
  - Não deve listar arquivos para upload manual — o refinamento é delegado à PM skill ou sessão estratégica via plataforma

#### 4.2: Geração de prompt de refinamento clipboard-ready

- **Descrição:** Gera prompt de refinamento com o contexto mínimo necessário para abrir a sessão, sem executar o refinamento.
- **Critérios de Aceite:**
  - Deve gerar prompt incluindo: id do épico, estado atual, alvo de refinamento e lista dos arquivos a carregar na sessão
  - Para épicos em 📋: prompt deve mencionar `autonomous_readiness.md` como checklist do alvo 🔍
  - Deve ter botão de copiar para clipboard
  - Não executa refinamento — apenas prepara o contexto para o operador iniciar manualmente

---

### ⏳ Fase MVP

> **Milestones:** `MVP-WORKFLOW-PLATAFORMA` (W-MVP-PLAT-1..3) · `MVP-WORKFLOW-REFINADOR` (W-MVP-REF-1..2).

#### ÉPICO W-MVP-PLAT-1: Fila de decisões automática

**Milestone:** `MVP-WORKFLOW-PLATAFORMA`

**Objetivo:** fila populada automaticamente por eventos de estado — épico chegou em 🔍, PR aberta, agente escalou bloqueio — sem que o operador monte a fila à mão.

**Status:** 📐 Funcionalidades esboçadas

**Dependências:** PROTO-WORKFLOW-PLATAFORMA (scaffold e kanban como base)

### Funcionalidades (esboço):
- **1.1 Detecção de eventos de estado** — monitora mudanças nos ROADMAPs e estado de PRs e gera itens de fila correspondentes.
- **1.2 Shape mínimo de item de fila** — título, contexto, tipo (dispatch/review/escalação) e ação esperada.
- **1.3 Ordenação e exibição da fila** — operador vê itens em ordem de prioridade; limpa no próprio ritmo.

---

#### ÉPICO W-MVP-PLAT-2: Chat focado por item

**Milestone:** `MVP-WORKFLOW-PLATAFORMA`

**Objetivo:** clicar num item da fila abre sessão com contexto pré-montado para aquele item específico — sem o operador montar o contexto manualmente.

**Status:** 📐 Funcionalidades esboçadas

**Dependências:** W-MVP-PLAT-1 (fila com itens clicáveis)

### Funcionalidades (esboço):
- **2.1 Montagem de contexto por tipo de item** — para dispatch: milestone + dispatch.md; para refinamento: épico + 6 arquivos essenciais; para revisão: PR + épicos do milestone.
- **2.2 Abertura de chat com contexto carregado** — prompt pré-montado pronto para iniciar a sessão correspondente.

---

#### ÉPICO W-MVP-PLAT-3: Auto-regulação da fila

**Milestone:** `MVP-WORKFLOW-PLATAFORMA`

**Objetivo:** plataforma sinaliza quando a fila está próxima do limite e pausa criação de novos itens autônomos até o operador liberar espaço.

**Status:** 📐 Funcionalidades esboçadas

**Dependências:** W-MVP-PLAT-1 (fila existente)

### Funcionalidades (esboço):
- **3.1 Indicador de capacidade** — exibe contagem atual vs. limite (~20 itens); alerta visual ao se aproximar.
- **3.2 Pausa de criação autônoma** — quando limite atingido, novos itens autônomos não são criados até o operador reduzir a fila.

---

#### ÉPICO W-MVP-REF-1: Refinador autônomo

**Milestone:** `MVP-WORKFLOW-REFINADOR`

**Objetivo:** processo de fundo que pega épicos disponíveis (🌱/📐) e avança o refinamento até onde consegue sem aprovação, tomando microdecisões proporcionais ao estágio. Quando trava, escala para a fila.

**Status:** 📐 Funcionalidades esboçadas

**Dependências:** MVP-WORKFLOW-PLATAFORMA (fila como destino de escalações e resultados)

### Funcionalidades (esboço):
- **1.1 Seleção de épico disponível** — identifica épicos em 🌱/📐 sem claim do operador e com dependências satisfeitas.
- **1.2 Execução do refinamento autônomo** — avança o estado do épico aplicando as regras de planning_guidelines; toma microdecisões onde a visão é clara.
- **1.3 Escalação ao travar** — quando encontra decisão que requer o operador, para e deposita item de fila com contexto.

---

#### ÉPICO W-MVP-REF-2: Parada limpa e registro

**Milestone:** `MVP-WORKFLOW-REFINADOR`

**Objetivo:** ao encerrar ciclo (por conclusão ou bloqueio), refinador deposita resultado na fila como item de decisão e não deixa trabalho órfão.

**Status:** 📐 Funcionalidades esboçadas

**Dependências:** W-MVP-REF-1 (refinador autônomo existente), W-MVP-PLAT-1 (fila como destino)

### Funcionalidades (esboço):
- **2.1 Item de resultado na fila** — ao concluir ou bloquear, cria item de fila descrevendo o que foi feito e o que falta.
- **2.2 Registro de progresso** — atualiza estado do épico no ROADMAP ao encerrar ciclo; não deixa épico em estado inconsistente.

---

## 📚 Observações

**Regra:** fluxo manual exige épico em `📋 Critérios definidos`;
fluxo autônomo exige `🔍 Detalhes definidos`.

Os milestones da fase Protótipo `PROTO-WORKFLOW-ENCERRAMENTO`,
`PROTO-WORKFLOW-DOC` e `PROTO-WORKFLOW-AJUSTES` foram mergeados em
sequência (PRs #83, #90 e #93). `PROTO-WORKFLOW-PLATAFORMA` permanece
em `📋 Critérios definidos`. Os milestones MVP (`MVP-WORKFLOW-PLATAFORMA`
e `MVP-WORKFLOW-REFINADOR`) têm épicos esboçados em `📐` aguardando
refinamento estratégico após os milestones de Protótipo fecharem.

**Bootstrap manual da convenção "sessão = milestone coerente":** a
quebra da fase Protótipo em milestones temáticos foi aplicada
manualmente como aprendizado pós-W-POC-4. Para evitar o erro do
milestone-balaio, foi introduzido o "Checklist de coerência para
declarar um milestone" em
`docs/process/refinement/planning_guidelines.md`.

**Observação sobre evolução da EM skill.** A EM skill hoje decide
sobre tamanho (FIT/TIGHT/OVERFLOW) com base em LOC e risco, rodando
**depois** da PM skill no fluxo autônomo. Se o checklist estratégico
falhar e um milestone-balaio chegar ao dispatch, o refinamento
tático (PM) já foi executado antes da EM detectar o problema —
desperdiçando trabalho. Caminhos considerados e ainda não
formalizados em épico: (a) preflight de coerência na EM antes da PM;
(b) manter ordem atual aceitando o warning tardio; (c) nova skill
"Coherence" entre Dispatch e PM. Decisão adiada — vira épico quando
houver sinal real de necessidade.
