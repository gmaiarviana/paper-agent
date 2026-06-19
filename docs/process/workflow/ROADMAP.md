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
- **Status dos épicos:** W-PROTO-PLAT-1 ✅, W-PROTO-PLAT-2 ✅,
  W-PROTO-PLAT-3 ✅, W-PROTO-PLAT-4 ✅.
- **Implementado em:** PR https://github.com/gmaiarviana/paper-agent/pull/106 (merge `3a0fa70`, 2026-04-28).
- **Nota:** milestone refinado a `📋` em 2026-04-27 na branch
  `claude/refine-workflow-mvp-tu06p` e refinado a `🔍` em 2026-04-27
  na branch `claude/refine-workflow-milestone-pRAed`. Todos os
  épicos atendem ao checklist de
  [`autonomous_readiness.md`](../refinement/autonomous_readiness.md)
  e o milestone está apto ao fluxo autônomo. Localização do código
  da plataforma: `tools/workflow_platform/` (top-level novo, fora
  de `products/`, coerente com [`vision.md`](vision.md)).

### PROTO-WORKFLOW-FAXINA

- **Objetivo:** faxina documental do `docs/process/` — eliminar drift
  entre cópias da lista de estados de épico, retirar de
  `quality_rules.md` o que não é regra do fluxo, enxugar
  `copilot-instructions.md`, descontinuar a dicotomia "fluxo manual
  (Cursor) vs autônomo" que não reflete o uso real (operador roda
  100% via Claude Code Web), e consolidar o template de "comandos
  de validação local" duplicado em 3 docs. Faz a casa antes de
  avançar para a fila reativa.
- **Estágio:** Protótipo
- **Épicos agrupados:** W-PROTO-10, W-PROTO-11, W-PROTO-13, W-PROTO-15,
  W-PROTO-16
- **Dependências de core:** nenhuma
- **Branch associada:** `milestone/proto-workflow-faxina`
- **Status dos épicos:** W-PROTO-10 ✅, W-PROTO-11 ✅, W-PROTO-13 ✅,
  W-PROTO-15 ✅, W-PROTO-16 ✅.
- **Implementado em:** PR https://github.com/gmaiarviana/paper-agent/pull/117 (merge `a2e24d8`, 2026-04-29).
- **Ordem de execução interna:** W-PROTO-15 antes de W-PROTO-10 e
  W-PROTO-11 (varre fluxo manual primeiro, evita revisitar arquivos).
  W-PROTO-16 antes de W-PROTO-11.3 (congela a forma canônica do
  template de validação antes da reorganização do `quality_rules.md`).
  W-PROTO-13 e W-PROTO-14 (este último em PROTO-WORKFLOW-COPILOT-STACK)
  podem rodar em paralelo — tocam o mesmo arquivo mas seções
  disjuntas.
- **Decisões de refinamento estratégico (2026-04-29):**
  - **W-PROTO-12 absorvido por W-PROTO-15.** Premissa de cindir
    `implementation/overview.md` em "regras de interação" vs
    "Validação Híbrida" some quando 15.4 elimina a dicotomia
    manual/autônomo — o conteúdo útil de "Validação Híbrida" (sintaxe,
    imports) vale pra qualquer fluxo e fica no overview mesmo. Se
    "doc por responsabilidade" virar atrito real depois, vira épico
    próprio no MVP-WORKFLOW-DOC (W-MVP-DOC-1 já cobre o princípio).
  - **W-MVP-DOC-2 movido para cá como W-PROTO-16.** Os 4 arquivos com
    template de validação duplicado (`quality_rules.md`,
    `implementation/delivery.md`, `autonomous/delivery.md`,
    `implementation/overview.md`) são exatamente os arquivos que
    W-PROTO-11 e W-PROTO-15 já tocam — fazer junto evita revisitar.
    A funcionalidade original "2.3 Variantes por fluxo (manual vs
    autônomo)" cai junto com W-PROTO-15.
- **Nota:** milestone declarado em 2026-04-29 a partir dos órfãos da
  fase Protótipo levantados na revisão
  `claude/review-process-directory-J1v8v` (2026-04-28). Refinamento
  estratégico em 2026-04-29 levou os 5 épicos a `🔍` e absorveu/moveu
  os dois antes citados. Apto ao fluxo autônomo.

### PROTO-WORKFLOW-COPILOT-STACK

- **Objetivo:** alinhar `copilot-instructions.md` à mudança de stack do
  Ensaio (Streamlit → Reflex, ADR 001 de 2026-04-25). Ajuste pequeno e
  operacional — o Copilot hoje manda Streamlit pros dois produtos e a
  validação de branches do Ensaio quebra ou roda com comando errado.
- **Estágio:** Protótipo
- **Épicos agrupados:** W-PROTO-14
- **Dependências de core:** nenhuma. Comandos de Reflex já fixados pelo
  ADR 001 + `products/ensaio/rxconfig.py` (consultados no refinamento
  de 2026-04-29) — sem input pendente do dev.
- **Branch associada:** `milestone/proto-workflow-copilot-stack`
- **Status dos épicos:** W-PROTO-14 ✅.
- **Implementado em:** PR https://github.com/gmaiarviana/paper-agent/pull/115 (merge `636ee8c`, 2026-04-29).
- **Nota:** milestone declarado em 2026-04-29; refinado a `🔍` na mesma
  data. Escopo cirúrgico, independente da faxina documental — pode
  rodar em paralelo com qualquer outro milestone do Protótipo.
  Observação operacional: a seção §"Operação Windows / macOS / Linux"
  de `copilot-instructions.md` é tocada por W-PROTO-14.3 (ampliação
  do range de portas) e por W-PROTO-13.3 (faxina); a coordenação está
  declarada nos dois épicos.

### PROTO-WORKFLOW-FILA

- **Objetivo:** plataforma ganha fila reativa de decisões + chat focado
  por item + auto-regulação básica. Sinais óbvios do repo (épico em
  🔍 esperando dispatch, PR de milestone aberta, branch parada) viram
  itens de fila por regra determinística — sem agente proativo ainda.
  Operador atende na ordem que escolher; ordenação por recência da
  detecção. Fonte da verdade: markdown + estado git/GitHub. Sem
  persistência própria — fila é view derivada, reconstruída do zero
  a cada render.
- **Estágio:** Protótipo
- **Épicos agrupados:** W-PROTO-FILA-1, W-PROTO-FILA-2,
  W-PROTO-FILA-3, W-PROTO-FILA-4
- **Dependências de core:** nenhuma; depende de
  PROTO-WORKFLOW-PLATAFORMA (kanban e scaffold como base) e
  PROTO-WORKFLOW-FAXINA (faxina documental antes de seguir)
- **Branch associada:** `milestone/proto-workflow-fila`
- **Status dos épicos:** W-PROTO-FILA-1 ✅, W-PROTO-FILA-2 ✅,
  W-PROTO-FILA-3 ✅, W-PROTO-FILA-4 ✅.
- **Implementado em:** PR https://github.com/gmaiarviana/paper-agent/pull/121 (merge `6d67b47`, 2026-06-18).
- **Decisões de refinamento estratégico (2026-04-29):**
  - **(a) Detecção reativa unificada na própria plataforma.** Os 3
    tipos de item (DISPATCH, REVIEW, STALE_BRANCH) são detectados
    pelo módulo `tools/workflow_platform/queue/detect.py`, lendo
    apenas o estado-do-mundo (ROADMAPs parseados + `git ls-remote` /
    `git for-each-ref`). RTE **não** ganha responsabilidade nova de
    criar item de fila — coerente com o princípio "markdown é fonte
    da verdade": se o ROADMAP marca o épico em 🔀 com PR #N (já
    feito hoje pela RTE em W-PROTO-8), a detecção REVIEW resolve. A
    alternativa "RTE estendida" foi descartada porque (i) acopla
    criação de fila ao fechamento de milestone, (ii) duplica fonte
    da verdade (RTE escreve no ROADMAP **e** num registro de fila),
    (iii) fila não cobriria PRs abertas manualmente fora do fluxo
    autônomo.
  - **(b) Auto-regulação no Protótipo é alerta visual sem pausa
    dura.** Limite alvo declarado: 20 itens (vision §"Fila").
    Aproximação: 15 itens (75% — buffer de 5). Pausa real (gatilho
    duro que impede o agente de criar itens) só ganha sentido no
    MVP, quando há proponente criando itens proativamente. No
    Protótipo, todos os itens vêm de detecção determinística do
    estado-do-mundo — não dá pra "pausar a detecção", o que existe é
    o que existe.
  - **(c) Reconstrução determinística é propriedade do design, não
    funcionalidade separada.** Como a fila não tem persistência
    própria e cada render parte do estado-do-mundo, a reconstrução
    é trivial por construção. W-PROTO-FILA-1.3 vira o **teste**
    explícito desse invariante: fixture com snapshot do estado-do-
    mundo + asserção `detect_all(snapshot) == detect_all(snapshot)`.
    Garante que a detecção é função pura do estado.
- **Tipos de item (Protótipo):** cinco tipos cobrem todos os pontos
  de ação que o operador tem hoje sem proponente — implementação,
  revisão, manutenção de branches, refinamento tático, faxina
  pós-merge. Os tipos restantes da vision §"Fila" (escalada,
  proposta, relatório executivo) chegam no MVP com o
  proponente/porta-voz.
  - `DISPATCH` — milestone com todos épicos em 🔍 (apto a dispatch),
    sem épicos em 🏗️/🔀/✅. Ação esperada: copiar prompt de
    dispatch e rodar em sessão autônoma.
  - `REVIEW` — PR de milestone aberta (épicos em 🔀). Ação esperada:
    abrir PR, colar Seção 🎯 no Copilot, decidir merge.
  - `STALE_BRANCH` — branch ativa há mais de N dias (N configurável
    via `config.yaml`, default 7) sem PR aberta e sem épico em
    🏗️/🔀 referenciando-a. Ação esperada: confirmar se é trabalho
    concluído sem PR (abrir), abandonado (deletar) ou bloqueado
    (resgatar).
  - `REFINE` — épico em 📐 ou 📋 esperando refinamento tático para
    chegar a 🔍. Ação esperada: copiar prompt de refinamento (reuso
    de `build_refinement_prompt` de W-PROTO-PLAT-4.2) e rodar em
    sessão de refinamento. Estados 🌱/🧭 ficam fora — sinal de
    "pronto pra avançar" não é determinístico nesses estados,
    pedem sessão estratégica humana, não item reativo de fila.
  - `CLEANUP` — épico em ✅ que ainda não foi limpo do ROADMAP
    (Cleanup skill não rodou — automação pós-merge ainda não
    configurada no Protótipo). Ação esperada: rodar
    `skills/cleanup/skill.md` manualmente; ela move conteúdo
    histórico do épico para fora do ROADMAP e a coluna ✅ do kanban
    volta a ficar vazia. Resolve mecanicamente o ruído visual de
    "✅ acumulando no kanban" sem precisar mexer em `EpicState`.
- **Nota:** milestone declarado em 2026-04-28 — absorve o conteúdo
  do antigo MVP-WORKFLOW-PLATAFORMA, reposicionado como Protótipo
  porque é fila **reativa** (regra determinística), não curada por
  agente. Curadoria por porta-voz vive no MVP. FILA-1/2/3 refinados
  a `🔍` em 2026-04-29 na branch `claude/optimize-dev-workflow-aiYYj`.
  FILA-4 declarado na mesma sessão a partir de feedback real de uso
  da plataforma (escopo absorvido do que iria virar
  `PROTO-WORKFLOW-PLAT-UX` separado — sem dependência cross-milestone).
  Apto ao fluxo autônomo após FILA-4 chegar a `🔍` **e**
  `PROTO-WORKFLOW-FAXINA` mergear.

### PROTO-WORKFLOW-CLEANUP-TRIGGER

- **Objetivo:** corrigir a Action de cleanup pós-merge entregue em
  W-PROTO-6 — hoje o trigger só casa com branches `milestone/*`, mas
  as PRs reais do projeto usam nomes do harness do Claude Code Web
  (`claude/execute-project-workflow-*`, `claude/proto-workflow-faxina-*`,
  etc.) e nunca disparam. Consequência: ~10 épicos presos em 🔀 e
  ~12 em ✅ sem faxina automatizada. Inclui backfill manual das
  PRs já mergeadas via o `workflow_dispatch` que a Action já expõe.
- **Estágio:** Protótipo
- **Épicos agrupados:** W-PROTO-17
- **Dependências de core:** nenhuma; revisita W-PROTO-6 entregue em
  PROTO-WORKFLOW-ENCERRAMENTO (PR #83).
- **Branch associada:** `milestone/proto-workflow-cleanup-trigger`
- **Status dos épicos:** W-PROTO-17 🔀 Em revisão — PR #123.
- **Nota:** milestone declarado em 2026-06-17 a partir de revisão
  técnica subsequente à entrega de PROTO-WORKFLOW-FILA (PR #121).
  Defeito não foi pego antes porque a Action exige merge real para
  observar — só ficou visível quando 3 milestones consecutivos
  fecharam sem disparar cleanup. Refinado a `🔍` em 2026-06-18: o
  trigger passa a resolver o milestone pelo **estado do ROADMAP**
  (join pelo número da PR via `tools/workflow_platform/parser.py`),
  não pelo nome da branch — sem peça nova na RTE. Backfill dos
  já-mergeados (#106/#115/#117/#121) já executado manualmente na
  mesma sessão; o escopo de implementação reduz-se ao fix do trigger.
  Apto ao fluxo autônomo.

> **Fase Piloto — escopo em altíssimo nível (declarado 2026-06-19).**
> Três milestones materializam o estágio Piloto definido na vision
> (§"Eixo de Estágios": "Cockpit + proatividade mecânica"). Escada de
> execução: **UX → Canal único → Proatividade**. Épicos e funcionalidades
> ficam para refinamento estratégico posterior — aqui só o escopo macro.

### PILOTO-WORKFLOW-CANAL-UNICO

- **Objetivo:** a plataforma vira **canal único** — o dispatch (e o chat
  focado) acontece de dentro dela, chamando o agente headless por baixo
  dos panos, em vez de copiar prompt pra uma sessão externa. A plataforma
  deixa de ser só leitura e passa a **disparar a execução**; o resultado
  aparece como commits/PR. Runtime inicial: `claude` headless (ver
  §"Tooling de Desenvolvimento > Decisão de runtime").
- **Estágio:** Piloto
- **Épicos agrupados:** a refinar (alto nível — acoplamento
  plataforma↔runtime, disparo de dentro, leitura de progresso).
- **Dependências de core:** nenhuma; depende de PROTO-WORKFLOW-FILA
  mergeada e da tese "Dispatch headless via CLI" (§Tooling).
- **Branch associada:** `milestone/piloto-workflow-canal-unico`
- **Status:** 🌱 Visão — aguarda refinamento estratégico.

### PILOTO-WORKFLOW-UX

- **Objetivo:** **UX de verdade** — a plataforma agradável de usar todo
  dia como cockpit. Absorve as frições de UX da fila reativa já levantadas
  (painel de detalhe some abaixo da viewport com 15+ itens; valor do
  clique difere por tipo de item) e amplia para o polimento geral. Frente
  distinta do runtime integrado (vision §"Eixo de Estágios").
- **Estágio:** Piloto
- **Épicos agrupados:** W-PILOTO-FILA-UX-1 (frições da fila — seed) +
  a refinar.
- **Dependências de core:** nenhuma; depende de PROTO-WORKFLOW-FILA
  mergeada.
- **Branch associada:** `milestone/piloto-workflow-ux`
- **Status dos épicos:** W-PILOTO-FILA-UX-1 🌱.
- **Nota:** **absorve o antigo PILOTO-WORKFLOW-FILA-UX** (declarado
  2026-06-17 a partir da revisão da PR #121), reescopado em 2026-06-19
  para a frente ampla de UX do Piloto. As frições da fila convergem com a
  transição Protótipo→Piloto: clicar o card deixa de copiar prompt e
  passa a disparar execução headless — repensar o shape do painel quando
  "ação = disparar". Demais épicos a refinar.

### PILOTO-WORKFLOW-PROATIVIDADE

- **Objetivo:** **proatividade mecânica (fase 1)** — a plataforma
  auto-aciona, em execução de segundo plano, o que a fila reativa **já
  detecta** como despachável (item `DISPATCH`: milestone com todos os
  épicos em 🔍). Sem agente de julgamento: roda só o que já está pronto
  de forma determinística. Guardrails da vision §"Proatividade e execução
  em segundo plano": teto baixo de fluxos simultâneos, não repetir
  trabalho em curso (idempotência por estado), branch isolada, PR como
  único portão. Campo de prova: Ensaio.
- **Estágio:** Piloto
- **Épicos agrupados:** a refinar (alto nível — gatilho agendado, guard
  de não-duplicação, teto de concorrência).
- **Dependências de core:** nenhuma; depende de PILOTO-WORKFLOW-CANAL-UNICO
  (disparo de dentro precede o disparo automático) e reusa a detecção
  `DISPATCH` de PROTO-WORKFLOW-FILA.
- **Branch associada:** `milestone/piloto-workflow-proatividade`
- **Status:** 🌱 Visão — aguarda refinamento estratégico.
- **Nota:** último degrau da escada do Piloto. O número do teto de
  concorrência e a cadência do agendamento ficam pro refinamento —
  default candidato: teto = 1. Julgamento (proponente/porta-voz) é MVP,
  não entra aqui.

### MVP-WORKFLOW-DOC

- **Objetivo:** faxina documental da fase MVP — quebrar o
  `planning_guidelines.md` (634 linhas hoje) por responsabilidade.
  Reduz custo de leitura para agentes e elimina drift médio prazo.
- **Estágio:** MVP
- **Épicos agrupados:** W-MVP-DOC-1
- **Dependências de core:** nenhuma; pode rodar em paralelo com os
  demais milestones do MVP.
- **Branch associada:** `milestone/mvp-workflow-doc`
- **Status dos épicos:** W-MVP-DOC-1 📐.
- **Nota:** milestone declarado em 2026-04-29. O épico irmão
  W-MVP-DOC-2 (consolidar template de "comandos de validação local")
  foi movido para `PROTO-WORKFLOW-FAXINA` como W-PROTO-16 no
  refinamento estratégico de 2026-04-29 — overlapping de arquivos com
  W-PROTO-11 e W-PROTO-15 justificou antecipar. W-MVP-DOC-1 fica no
  MVP porque é redesign estrutural, não faxina; depende
  conceitualmente de W-PROTO-10 (centralização da definição de
  estados) ter rodado primeiro pra ver melhor o que extrair.

### MVP-WORKFLOW-REFINAMENTO

- **Objetivo:** fluxo de refinamento autônomo standalone — PM skill
  desacoplada do dispatch de implementação, operando em sessão própria.
  Avança épicos pré-🔍 em saltos pequenos (um estado por vez), branch
  persiste por épico em refinamento, PR por épico ao chegar no alvo.
  Qualidade do refinamento (exemplos canônicos, modo iterativo, registro
  de feedback) embutida no escopo.
- **Estágio:** MVP
- **Épicos agrupados:** W-MVP-REF-1, W-MVP-REF-2
- **Dependências de core:** nenhuma; depende de
  PROTO-WORKFLOW-FILA (fila reativa como destino de bloqueios e
  conclusões)
- **Branch associada:** `milestone/mvp-workflow-refinamento`
- **Status dos épicos:** W-MVP-REF-1 📐, W-MVP-REF-2 📐.
- **Princípios não-negociáveis (vindos da vision):**
  - Saltos pequenos — um estado por vez, sem pular 🌱→🔍 numa passada.
  - Branch persiste por épico em refinamento.
  - PR por épico (não por milestone) ao concluir; exceção declarada
    para coerência cross-épico do mesmo milestone.
  - Pacing por bandwidth do operador — autônomo não acelera o que o
    operador não consegue revisar com qualidade.
- **Nota:** milestone declarado em 2026-04-27 (originalmente como
  MVP-WORKFLOW-REFINADOR), reescopado em 2026-04-28 para refletir o
  modelo papéis-vs-fluxos. Refinador deixa de ser "papel" — é executor
  do fluxo de refinamento. Épicos em `📐 Funcionalidades esboçadas` —
  aguardam refinamento estratégico antes do dispatch.

### MVP-WORKFLOW-PROPONENTE

- **Objetivo:** introduz os dois papéis novos do MVP — proponente
  (orquestrador proativo que escolhe e dispara fluxos ~1×/dia) +
  porta-voz (curador de atenção com agência decisória sobre bloqueios
  pequenos). Mecânica de bloqueio proponente↔porta-voz operando.
  Priorização autônoma rodando.
- **Estágio:** MVP
- **Épicos agrupados:** W-MVP-PROP-1, W-MVP-PROP-2
- **Dependências de core:** nenhuma; depende de
  MVP-WORKFLOW-REFINAMENTO (proponente precisa do fluxo de
  refinamento standalone como uma das opções de disparo) e
  PROTO-WORKFLOW-FILA (fila como destino do que o porta-voz escala)
- **Branch associada:** `milestone/mvp-workflow-proponente`
- **Status dos épicos:** W-MVP-PROP-1 📐, W-MVP-PROP-2 📐.
- **Tensões para refinamento estratégico:**
  - **(a) Onde vive o repertório do porta-voz?** Markdown único
    (`docs/process/workflow/portavoz_repertorio.md`), distribuído por
    tema, ou consultado sob demanda dos docs existentes (filosofia,
    visão, orientações)? Princípio: markdown é fonte da verdade — mas
    formato canônico precisa ser definido.
  - **(b) Cadência do proponente.** Vision diz ~1×/dia. Cron, gatilho
    de evento, ou disparo manual do operador? POC pode ser manual.
  - **(c) Auto-regulação dura no MVP.** Quando o agente proativo cria
    itens, faz sentido endurecer o limite (~20 itens) — pausa real,
    não só alerta.
- **Nota:** milestone declarado em 2026-04-28. Substitui o antigo
  MVP-WORKFLOW-PLATAFORMA conceitualmente — papéis novos, não fila
  nova. Épicos em `📐 Funcionalidades esboçadas` — aguardam refinamento
  estratégico antes do dispatch.

## 🛠️ Tooling de Desenvolvimento

### Dispatch headless via CLI

**Status:** 🧭 Tese validada (2026-05-01) — dispatch por comando único é viável; runtime inicial do Piloto **definido em 2026-06-19**: `claude` headless sob assinatura Max (ver "Decisão de runtime" abaixo).

**Tese:** a plataforma dispara fluxos de implementação e refinamento invocando um agente em modo headless por linha de comando — sem UI, sem operador presente, resultado aparece como commits na branch. O binário concreto é trocável (`claude` headless ou [`opencode`](https://opencode.ai/) hoje, outro amanhã); o que importa é o contrato de execução.

**Validado em 2026-05-01:**
- ✅ Comando único dispara execução em background, lê contexto do repo, executa, persiste resultado.
- Provado em duas pilhas independentes na mesma tarefa (`E-PROTO2-4`, accordion no Ensaio):
  - `opencode run` contra `gpt-oss:20b` via OpenWebUI (modelo local, $0)
  - `claude` headless contra Opus 4.7 (Anthropic, ~$1.66 / 232s / 37 turnos)

**Aberto:**
- Qualidade do opencode com modelos locais: falhas intermitentes em tool-calling (parser do Ollama rejeita formato emitido pelo modelo). Mais rodadas necessárias antes de mapear guardrails.
- Próximo teste real é disparar **skill chain completo** (dispatch de implementação ponta a ponta), não tarefa direta.

**Decisão de runtime (2026-06-19): `claude` headless, auth pela assinatura Max.**
- Começar com Claude Code CLI pela qualidade conhecida — o foco do Piloto fica no acoplamento plataforma↔agente, não em domar o modelo.
- **Auth preferencial: assinatura Max do operador (login da conta), não API key** — se viável. API key fica como **fallback** caso a assinatura não cubra o uso.
- O caminho de migração para modelos locais (`opencode` contra OpenWebUI/Ollama) segue válido e encaixa no Horizonte "Runtime de agente sobre providers corporativos (estágio MVP)" — o runtime é trocável por contrato de execução, não reescrita.
- **A confirmar na implementação:** uso *agendado / não-assistido* (auto-dispatch da `PILOTO-WORKFLOW-PROATIVIDADE`) sob assinatura Max pode esbarrar em limites/termos pensados pra uso interativo. O canal único (disparo pelo operador) é uso interativo e não tem esse risco; se o agendado exigir, cai pro fallback de API só nessa fase.

**Configuração opencode (referência):**
- Provider em `opencode.json` (root): `@ai-sdk/openai-compatible` contra OpenWebUI
- Variáveis `.env`: `OPENWEBUI_API_KEY`, `OPENWEBUI_BASE_URL`
- Setup via `infra/llm-clients/setup-opencode.ps1`
- Modelos disponíveis: `gpt-oss:20b` (default), `qwen3.6:35b`, `llama3.2:3b`

---

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

> **Milestones:** `PROTO-WORKFLOW-ENCERRAMENTO` (W-PROTO-5, 6, 7) · `PROTO-WORKFLOW-DOC` (W-PROTO-DOC-1, 2, 3) · `PROTO-WORKFLOW-AJUSTES` (W-PROTO-8, W-PROTO-9) · `PROTO-WORKFLOW-PLATAFORMA` (W-PROTO-PLAT-1..4) · `PROTO-WORKFLOW-FILA` (W-PROTO-FILA-1..3) · `PROTO-WORKFLOW-CLEANUP-TRIGGER` (W-PROTO-17).

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

**Milestone:** PROTO-WORKFLOW-PLATAFORMA

**Status:** ✅ Implementado

**Entregue em:** PR https://github.com/gmaiarviana/paper-agent/pull/106 (merge `3a0fa70`, 2026-04-28) — scaffold da plataforma de workflow em `tools/workflow_platform/` — app Streamlit, `config.yaml`, parser defensivo de ROADMAP e modelos tipados (Epic, Milestone, EpicState).

---

#### ÉPICO W-PROTO-PLAT-2: Kanban completo

**Milestone:** PROTO-WORKFLOW-PLATAFORMA

**Status:** ✅ Implementado

**Entregue em:** PR https://github.com/gmaiarviana/paper-agent/pull/106 (merge `3a0fa70`, 2026-04-28) — kanban com as 8 colunas (🌱→✅) consolidando épicos de todos os ROADMAPs configurados, com cards agrupados por milestone.

---

#### ÉPICO W-PROTO-PLAT-3: Ações de implementação

**Milestone:** PROTO-WORKFLOW-PLATAFORMA

**Status:** ✅ Implementado

**Entregue em:** PR https://github.com/gmaiarviana/paper-agent/pull/106 (merge `3a0fa70`, 2026-04-28) — ações contextuais de implementação no painel do épico — prompt de dispatch clipboard-ready para 🔍 e links para branch/PR/resumo em 🏗️/🔀/✅.

---

#### ÉPICO W-PROTO-PLAT-4: Direcionamento de refinamento

**Milestone:** PROTO-WORKFLOW-PLATAFORMA

**Status:** ✅ Implementado

**Entregue em:** PR https://github.com/gmaiarviana/paper-agent/pull/106 (merge `3a0fa70`, 2026-04-28) — direcionamento de refinamento por estado pré-execução (🌱/🧭/📐/📋), com prompt de refinamento clipboard-ready reusável.

---

#### ÉPICO W-PROTO-FILA-1: Detecção reativa de eventos e shape de item

**Milestone:** PROTO-WORKFLOW-FILA

**Status:** ✅ Implementado

**Entregue em:** PR https://github.com/gmaiarviana/paper-agent/pull/121 (merge `6d67b47`, 2026-06-18) — detecção reativa dos 5 tipos de item (DISPATCH, REVIEW, REFINE, CLEANUP, STALE_BRANCH) em `queue/models.py` + `queue/detect.py`, com snapshot determinístico do estado-do-mundo.

---

#### ÉPICO W-PROTO-FILA-2: Exibição da fila + prompt focado por item

**Milestone:** PROTO-WORKFLOW-FILA

**Status:** ✅ Implementado

**Entregue em:** PR https://github.com/gmaiarviana/paper-agent/pull/121 (merge `6d67b47`, 2026-06-18) — tab "📋 Fila" como default, cards clicáveis por item e builders de prompt clipboard-ready por tipo (reusando os builders de PLAT-3.1 e PLAT-4.2).

---

#### ÉPICO W-PROTO-FILA-3: Auto-regulação básica (alerta visual)

**Milestone:** PROTO-WORKFLOW-FILA

**Status:** ✅ Implementado

**Entregue em:** PR https://github.com/gmaiarviana/paper-agent/pull/121 (merge `6d67b47`, 2026-06-18) — auto-regulação básica via badge de carga na sidebar (`<n>/20`) e banner OVER_LIMIT — alerta visual sem pausa dura.

---

#### ÉPICO W-PROTO-FILA-4: Configuração persistente + sidebar como painel

**Milestone:** PROTO-WORKFLOW-FILA

**Status:** ✅ Implementado

**Entregue em:** PR https://github.com/gmaiarviana/paper-agent/pull/121 (merge `6d67b47`, 2026-06-18) — preferências persistidas localmente (`preferences.json` git-ignored), filtro por ROADMAP e sidebar transformada em painel de filtros + status.

---

#### ÉPICO W-PROTO-10: Centralizar definição dos estados de épico

**Milestone:** PROTO-WORKFLOW-FAXINA

**Status:** ✅ Implementado

**Entregue em:** PR https://github.com/gmaiarviana/paper-agent/pull/117 (merge `a2e24d8`, 2026-04-29) — definição dos 8 estados de épico centralizada numa seção canônica de `planning_guidelines.md`, com as cópias divergentes cross-doc eliminadas.

---

#### ÉPICO W-PROTO-11: Faxina de `quality_rules.md`

**Milestone:** PROTO-WORKFLOW-FAXINA

**Status:** ✅ Implementado

**Entregue em:** PR https://github.com/gmaiarviana/paper-agent/pull/117 (merge `a2e24d8`, 2026-04-29) — faxina de `quality_rules.md` (397→213 linhas) — tutorial defensivo de git removido e lessons learned do Revelar migradas para `products/revelar/docs/llm_implementation_lessons.md`.

---

#### ÉPICO W-PROTO-13: Faxina do `copilot-instructions.md` (concisão pra agente)

**Milestone:** PROTO-WORKFLOW-FAXINA

**Status:** ✅ Implementado

**Entregue em:** PR https://github.com/gmaiarviana/paper-agent/pull/117 (merge `a2e24d8`, 2026-04-29) — faxina de `.github/copilot-instructions.md` — seção "Operação Windows / macOS / Linux" removida.

---

#### ÉPICO W-PROTO-14: Operacionalizar Reflex no fluxo de validação do Copilot

**Milestone:** PROTO-WORKFLOW-COPILOT-STACK

**Status:** ✅ Implementado

**Entregue em:** PR https://github.com/gmaiarviana/paper-agent/pull/115 (merge `636ee8c`, 2026-04-29) — `.github/copilot-instructions.md` operacionalizado para Reflex (Ensaio) vs Streamlit (Revelar) conforme ADR 001 — tabela de stack por produto, comandos de subida e liberação de portas por stack.

---

#### ÉPICO W-PROTO-15: Descontinuar fluxo manual / Cursor / Claude Web do desenho

**Milestone:** PROTO-WORKFLOW-FAXINA

**Status:** ✅ Implementado

**Entregue em:** PR https://github.com/gmaiarviana/paper-agent/pull/117 (merge `a2e24d8`, 2026-04-29) — dicotomia "fluxo manual (Cursor) vs autônomo" descontinuada do desenho do processo (~140 menções em 16 arquivos), com `.cursorrules` removido — um único fluxo via Claude Code Web.

---

#### ÉPICO W-PROTO-16: Consolidar template de "comandos de validação local"

**Milestone:** PROTO-WORKFLOW-FAXINA

**Status:** ✅ Implementado

**Entregue em:** PR https://github.com/gmaiarviana/paper-agent/pull/117 (merge `a2e24d8`, 2026-04-29) — template de "comandos de validação local" consolidado numa fonte canônica em `quality_rules.md`, com as 3 cópias divergentes substituídas por link.

---

#### ÉPICO W-PROTO-17: Trigger da Action de cleanup não casa com branches harness-assigned

**Milestone:** `PROTO-WORKFLOW-CLEANUP-TRIGGER`

**Objetivo:** corrigir o defeito que impediu a Action `.github/workflows/milestone-cleanup.yml` (entregue em W-PROTO-6 / PROTO-WORKFLOW-ENCERRAMENTO) de disparar em qualquer milestone real do projeto. O trigger passa a identificar a PR de milestone **pelo estado do ROADMAP** (join pelo número da PR), não pelo nome da branch — restaurando o cleanup automático pós-merge. (O backfill dos já-mergeados — escopo (b) original — já foi executado manualmente nesta sessão; ver "Fora do escopo".)

**Status:** 🔀 Em revisão — PR #123 (https://github.com/gmaiarviana/paper-agent/pull/123)

**Branch:** `claude/clever-brown-6nh76f`

**Dependências:** revisita W-PROTO-6 (PR #83). Reusa o parser e o modelo de dados de W-PROTO-PLAT-1 (`tools/workflow_platform/parser.py`, `models.Epic.pr_number`, `config_loader.load_config`) e o padrão de join por `pr_number` de W-PROTO-FILA-1 (`queue/detect.py::detect_review_items`).

### Diagnóstico (verbatim da revisão técnica 2026-06-17)

- `.github/workflows/milestone-cleanup.yml` (~linha 49) só dispara quando a branch da PR começa com `milestone/`. As PRs reais usam nomes do harness do Claude Code Web (`claude/execute-project-workflow-*`, `claude/proto-workflow-faxina-*`, `claude/implement-copilot-stack-*`), que nunca casam.
- Consequência: o cleanup automático **nunca rodou**. ROADMAP do workflow acumulou ~10 épicos presos em 🔀 após o merge das PRs #106 (PLATAFORMA), #115 (W-PROTO-14), #117 (FAXINA), e ~12 épicos em ✅ sem faxina.
- Defeito secundário: mesmo se o trigger casasse, a derivação de `MILESTONE_ID` (~linha 69, strip de `milestone/`) produziria valor errado num branch `claude/*`.

### Decisão de refinamento (2026-06-18)

- **Trigger pela fonte da verdade (ROADMAP), não pela branch.** No merge de
  uma PR para `main`, a Action resolve o milestone lendo os ROADMAPs
  configurados (`tools/workflow_platform/config.yaml`) e casando os épicos em
  `🔀 Em revisão` cujo `PR #N` é igual ao número da PR mergeada. O
  `milestone_id` desses épicos é o alvo do cleanup. Se nenhum épico casa →
  não é PR de milestone → Action pula antes de invocar o Claude.
  - **Por quê:** o número da PR já é escrito no ROADMAP pela RTE
    (`🔀 Em revisão — PR #N`, W-PROTO-8) e o parser já o extrai (`pr_number`).
    É o mesmo join que a fila usa em `detect_review_items`. Independente do
    nome da branch (resolve o defeito-raiz) e sem peça nova na RTE — nem
    label, nem contrato de formato de body.
  - **Trade-off:** a Action passa a fazer checkout + parse a cada merge para
    `main` (custo trivial; merges sem match saem antes do passo do Claude).
    Descartados: label na PR (passo novo na RTE, falha silenciosa se a RTE
    esquecer) e parse do body (texto livre, editável por humano, frágil).
  - `MILESTONE_ID` deixa de ser derivado por strip de `milestone/`; vem do
    épico resolvido.

### Termos e contratos

- **Função pura nova** em `tools/workflow_platform/cleanup_trigger.py`:

  ```python
  def resolve_milestone_for_merged_pr(
      pr_number: int, roadmap_paths: list[str]
  ) -> str | None:
      """Milestone a limpar para a PR mergeada, ou None se não é PR de milestone.

      Parseia cada ROADMAP (parser.parse_roadmap), coleta épicos em
      EpicState.IN_REVIEW com epic.pr_number == pr_number e devolve o
      milestone_id único desses épicos. Devolve None se 0 épicos casam.
      Levanta ValueError se os épicos casados divergem no milestone_id
      (>1 distinto) ou têm milestone_id ausente (ROADMAP inconsistente —
      não silenciar).
      """
  ```

- **CLI** invocável pela Action: `python -m tools.workflow_platform.cleanup_trigger <pr_number>`
  — resolve os roadmaps via `config_loader.load_config().roadmaps`, chama a
  função e imprime o `milestone_id` em stdout (string vazia se `None`), exit 0.
  Erro de consistência → stderr + exit != 0.

### Funcionalidades:

#### 17.1 — Resolver milestone do PR mergeado a partir do ROADMAP

- **Domain:** backend
- **Estimativa:** ~120 linhas | risco: baixo
- **Arquivos a criar:**
  - `tools/workflow_platform/cleanup_trigger.py`
  - `tests/tools/workflow_platform/test_cleanup_trigger.py`
- **Arquivos a modificar:** nenhum
- **Padrão a seguir:** `tools/workflow_platform/queue/detect.py::detect_review_items`
  (join por `pr_number`, derivação de `milestone_id` único) e
  `tools/workflow_platform/config_loader.py` (helper puro + paths resolvidos).
- **Mecanismo de integração:** módulo standalone, import-safe (só
  `re`/`pathlib`/`.parser`/`.models`/`.config_loader` — nenhum import de
  Streamlit), executável como `python -m tools.workflow_platform.cleanup_trigger`
  a partir do repo root no runner.
- **Critérios de aceite:**
  1. `resolve_milestone_for_merged_pr(N, paths)` devolve o `milestone_id` quando
     ≥1 épico em `🔀` tem `pr_number == N` e todos concordam no `milestone_id`.
  2. Devolve `None` quando nenhum épico em `🔀` casa o número (PR fora do fluxo
     de milestone).
  3. Levanta `ValueError` quando os épicos casados divergem no `milestone_id`
     ou têm `milestone_id` ausente.
  4. Épicos já em `✅` com o mesmo `PR #N` **não** casam (só `IN_REVIEW`) —
     garante idempotência: re-trigger não re-limpa milestone já fechado.
  5. CLI imprime o `milestone_id` em stdout (vazio se `None`) e sai 0;
     inconsistência → exit != 0.
- **Validação:** `pytest tests/tools/workflow_platform/test_cleanup_trigger.py -v`
  — fixtures: ROADMAP com milestone inteiro em 🔀 sob PR #N; PR não referenciada;
  PR com épicos em milestones divergentes; PR já em ✅.

#### 17.2 — Reescrever trigger e derivação de `MILESTONE_ID` na Action

- **Domain:** infra (CI)
- **Estimativa:** ~60 linhas de diff | risco: médio (toca workflow real)
- **Arquivos a modificar:**
  - `.github/workflows/milestone-cleanup.yml`
- **Mecanismo de integração:**
  - Remover do `if` do job a condição
    `startsWith(github.event.pull_request.head.ref, 'milestone/')`. Manter
    `github.event.pull_request.merged == true` (e o caminho `workflow_dispatch`).
  - Novo passo "Resolver milestone" (após o checkout de `main`): `setup-python`
    + `pip install pyyaml` +
    `python -m tools.workflow_platform.cleanup_trigger ${{ github.event.pull_request.number }}`
    → grava `milestone_id` em `$GITHUB_OUTPUT`.
  - Passo "Extrair variáveis": no caminho `pull_request`, `MILESTONE_ID` vem do
    output do passo resolver (não mais do strip de `head.ref`).
    `MERGED_PR_URL`/`MERGE_SHA` seguem de `html_url`/`merge_commit_sha`.
    `workflow_dispatch` inalterado.
  - Os passos de cleanup (Claude action, commit, log) ficam **gated** em
    `milestone_id != ''` — merge sem match não chega no passo do Claude (sem
    custo de API).
- **Critérios de aceite:**
  1. Job dispara em `pull_request closed` para `main` independentemente do nome
     da branch.
  2. Para PR de milestone (épicos 🔀 com `PR #N` no ROADMAP), `MILESTONE_ID`
     resolvido = milestone correto; passos de cleanup executam.
  3. Para PR sem épicos em 🔀 referenciando-a, o passo resolver devolve vazio e
     os passos de cleanup são pulados (sem invocar o Claude).
  4. Caminho `workflow_dispatch` (3 inputs manuais) permanece funcional e
     inalterado.
  5. Nenhuma referência a `milestone/` na derivação de `MILESTONE_ID` resta no
     arquivo.
- **Validação:** (i) inspeção do YAML; (ii)
  `python -m tools.workflow_platform.cleanup_trigger <PR>` contra o ROADMAP
  atual devolve vazio para PRs já limpas (#106/#115/#117/#121 já em ✅) —
  regressão: não re-limpa; (iii) dry-run documentado via `workflow_dispatch` no
  fechamento.

### Ordem de execução

17.1 antes de 17.2 (a Action chama o módulo).

### Fora do escopo

- **Backfill dos já-mergeados — já executado manualmente nesta sessão**
  (commit de faxina backfill, 2026-06-18): #106, #115, #117 e #121 enxugados e
  transitados para ✅ no ROADMAP do workflow. O escopo (b) original do épico
  está satisfeito; a Action corrigida cobre apenas milestones futuros.
- Refatorar a Cleanup skill (`skills/cleanup/skill.md`) em si — escopo é o
  trigger e a derivação de `MILESTONE_ID`, não o que a skill faz depois.
- Política nova de nomenclatura de branches do harness — incompatibilidade é
  assimétrica (custoso mudar o harness; trivial mudar o trigger).
- Substituir a Action por outro runtime — escopo é fix de regressão, não redesign.
- Reasoning de "próximo passo" como engine separado: a detecção reativa já vive
  na fila (`queue/detect.py`); este épico reusa o mesmo princípio (markdown =
  fonte da verdade) sem construir engine nova.

---

### ⏳ Fase Piloto

> **Milestones:** `PILOTO-WORKFLOW-CANAL-UNICO` · `PILOTO-WORKFLOW-UX`
> (W-PILOTO-FILA-UX-1 + a refinar) · `PILOTO-WORKFLOW-PROATIVIDADE`.
> Escopo macro nos cards de milestone acima; só `W-PILOTO-FILA-UX-1` tem
> esboço de épico (herdado do antigo `PILOTO-WORKFLOW-FILA-UX`).

#### ÉPICO W-PILOTO-FILA-UX-1: Refinamento de UX da fila reativa

**Milestone:** `PILOTO-WORKFLOW-UX`

**Objetivo:** reduzir duas frições identificadas em uso real da fila reativa entregue em PROTO-WORKFLOW-FILA (PR #121) — painel de detalhe que some abaixo da viewport quando a fila enche; e cards de REVIEW/CLEANUP/STALE_BRANCH que duplicam no detalhe o que já está no card.

**Status:** 🌱 Visão

**Dependências:** PROTO-WORKFLOW-FILA mergeada; coordena com a transição "clique do card dispara execução" registrada em §"Tooling de Desenvolvimento" (tese validada 2026-05-01).

### Funcionalidades (esboço):

- **1.1 Posição do painel de detalhe** — hoje renderiza no rodapé, depois de TODOS os cards (`tools/workflow_platform/app.py`, função `main`, dentro da `tab_queue`). Com fila cheia (15+ itens) o operador não vê o painel sem scroll. Alvos plausíveis: coluna lateral à fila (coerente com vision §"Fila / Kanban"), topo, ou painel fixo via `st.expander` sticky. Refinar trade-offs em sessão estratégica.

- **1.2 Card não duplicar o prompt em REVIEW/CLEANUP/STALE_BRANCH** — para esses tipos `expected_action` já é a instrução inteira; abrir o detalhe não acrescenta nada além do `st.code` do mesmo texto. Diferenciar shape: card com ação curta e copiável direto; painel de detalhe agregando valor real só em DISPATCH/REFINE, onde o prompt é artefato grande gerado por `build_dispatch_prompt`/`build_refinement_prompt`. Refinar critério "abre painel ou não" no épico.

**Nota de convergência:** ambas as funcionalidades pegam carona na transição Protótipo→Piloto registrada em §"Dispatch headless via CLI" — no Piloto, clicar o card deixa de copiar prompt e passa a disparar execução headless do agente (`claude` ou `opencode`). UX da fila no Piloto pode reconsiderar shape do painel quando "ação esperada = disparar", não "ação esperada = copiar". Refinar antes do dispatch se a transição já está consolidada no momento da sessão estratégica, ou registrar dependência cross-épico se não.

### Fora do escopo

- Implementar o clique-dispara-execução em si — é trabalho do épico de transição Protótipo→Piloto registrado em §"Tooling de Desenvolvimento", não desta UX.
- Reescrever o layout do kanban — escopo é só a tab Fila.
- Personalização por operador (tamanho do painel, qual coluna) — sem sinal de atrito; entra se virar.

---

### ⏳ Fase MVP

> **Milestones:** `MVP-WORKFLOW-REFINAMENTO` (W-MVP-REF-1..2) · `MVP-WORKFLOW-PROPONENTE` (W-MVP-PROP-1..2).

#### ÉPICO W-MVP-REF-1: Fluxo de refinamento autônomo standalone

**Milestone:** `MVP-WORKFLOW-REFINAMENTO`

**Objetivo:** PM skill operando em sessão própria (desacoplada do dispatch de implementação), avançando épico pré-🔍 em saltos pequenos — um estado por vez, com commits intermediários na branch do épico. Sessão pode ser disparada manualmente (ponto de partida) e, depois, pelo proponente.

**Status:** 📐 Funcionalidades esboçadas

**Dependências:** PROTO-WORKFLOW-FILA (fila reativa como destino de bloqueios e conclusões)

### Funcionalidades (esboço):
- **1.1 PM skill standalone** — extrai PM skill do dispatch de implementação; cria modo de operação isolado, com sessão e branch próprias por épico.
- **1.2 Saltos pequenos com commit por estado** — agente avança um estado por vez (ex.: 📐→📋), comita progresso, e segue. Não pula 🌱→🔍 numa passada.
- **1.3 Branch persiste por épico em refinamento** — múltiplas sessões podem comitar estado intermediário na mesma branch; não se cria branch nova por sessão.
- **1.4 Qualidade do refinamento** — exemplos canônicos, modo iterativo, registro de feedback do operador como repertório consultável em sessões seguintes.

---

#### ÉPICO W-MVP-REF-2: Parada limpa, PR por épico, registro

**Milestone:** `MVP-WORKFLOW-REFINAMENTO`

**Objetivo:** ao concluir refinamento (chegou no alvo) ou ao travar, agente para limpo. Conclusão = abre PR por épico (default) ou PR cross-épico declarada (exceção). Bloqueio = commit do estado parcial + chama porta-voz (mecânica que vive em MVP-WORKFLOW-PROPONENTE).

**Status:** 📐 Funcionalidades esboçadas

**Dependências:** W-MVP-REF-1 (fluxo standalone existente)

### Funcionalidades (esboço):
- **2.1 PR por épico ao concluir** — quando épico chega no alvo com clareza, abre PR (granularidade que cabe na bandwidth de revisão do operador). Body da PR descreve saltos de estado feitos e decisões tomadas.
- **2.2 Exceção PR cross-épico** — quando refinamento de A revela ajuste necessário em B (mesmo milestone), agente declara explicitamente; PR cobre A + ajustes mínimos em B; body da PR sinaliza coerência cross-épico.
- **2.3 Bloqueio = commit + sinal** — ao travar, agente comita estado parcial e gera sinal pro porta-voz (mecânica em W-MVP-PROP-2). No MVP-WORKFLOW-REFINAMENTO sozinho (antes do proponente existir), bloqueio cai como item de fila reativa do Protótipo.
- **2.4 Pacing por bandwidth** — agente respeita limite de épicos em refinamento ativo simultâneo (configurável); não inicia novo se o operador já tem N PRs de refinamento esperando revisão.

---

#### ÉPICO W-MVP-PROP-1: Proponente — orquestrador proativo

**Milestone:** `MVP-WORKFLOW-PROPONENTE`

**Objetivo:** papel novo (não agente novo) que olha o sistema (visão, backlog, ROADMAPs, sinais do dia) e propõe o próximo movimento ~1×/dia, escolhendo e disparando o fluxo apropriado na prioridade certa. Combina as skills existentes para produzir trabalho útil.

**Status:** 📐 Funcionalidades esboçadas

**Dependências:** MVP-WORKFLOW-REFINAMENTO (proponente precisa do fluxo de refinamento standalone como uma das opções de disparo) · PROTO-WORKFLOW-FILA (fila como destino das propostas e relatórios)

### Funcionalidades (esboço):
- **1.1 Leitura do sistema** — varre ROADMAPs, backlog, branches abertas, fila atual; identifica oportunidades por prioridade declarada (implementar refinado > refinar pré-🔍 > transformar visão em backlog).
- **1.2 Disparo de fluxo apropriado** — para cada oportunidade priorizada, escolhe entre fluxo de refinamento ou de implementação; dispara como sessão autônoma com escopo declarado.
- **1.3 Catálogo de tipos de proposta** — implementar épico em 🔍, refinar épico pré-🔍, transformar item da visão em épico novo, propor POC de ideia mencionada, mapear dependências entre épicos, gerar relatório executivo do dia.
- **1.4 Cadência configurável** — POC pode ser disparo manual; MVP avança para schedule (cron) ou gatilho de evento. A definir no refinamento.

---

#### ÉPICO W-MVP-PROP-2: Porta-voz — curador de atenção com agência

**Milestone:** `MVP-WORKFLOW-PROPONENTE`

**Objetivo:** filtro inteligente entre o sistema e o operador. Recebe consultas do proponente em bloqueios; lê estado-do-mundo; cura a fila. Tem agência decisória sobre bloqueios pequenos, baseada em filosofia/visão/orientações acumuladas. Escala apenas o que escapa do repertório.

**Status:** 📐 Funcionalidades esboçadas

**Dependências:** W-MVP-PROP-1 (proponente existente, gerando bloqueios) · PROTO-WORKFLOW-FILA (fila como destino do que escala)

### Funcionalidades (esboço):
- **2.1 Mecânica de bloqueio proponente↔porta-voz** — proponente chama porta-voz com contexto do bloqueio + pede recomendação; porta-voz responde "siga com X", "abra alternativa Y" ou "escala para operador".
- **2.2 Repertório consultável do porta-voz** — markdown canônico (formato a definir no refinamento) com filosofia, visão, orientações acumuladas. Resposta do operador a escalações vira repertório novo.
- **2.3 Curadoria da fila** — porta-voz ordena/agrupa/filtra itens; aplica auto-regulação dura (~20 itens) — pausa real, não só alerta como no Protótipo.
- **2.4 Temporização** — porta-voz decide quando interromper o operador; junta perguntas correlatas; escala atenção certa na hora certa.

---

> **Milestone de saneamento documental do MVP** (`MVP-WORKFLOW-DOC`) declarado em 2026-04-29; reduzido a W-MVP-DOC-1 no refinamento estratégico de 2026-04-29 (`claude/refine-workflow-stacks-6JOH6`) — W-MVP-DOC-2 migrou para `PROTO-WORKFLOW-FAXINA` como W-PROTO-16.

#### ÉPICO W-MVP-DOC-1: Quebrar `planning_guidelines.md` por responsabilidade

**Milestone:** `MVP-WORKFLOW-DOC`

**Objetivo:** o arquivo (634 linhas) absorveu definição de estados, processo de sessão, glossário, anti-padrões, exemplos, templates de épico/funcionalidade. Cabe num doc só, mas a leitura cansa e a navegação é ruim.

**Status:** 📐 Funcionalidades esboçadas

### Funcionalidades (esboço):
- **1.1 Definir corte natural** — candidatos: definições de estado / processo de sessão / templates / anti-padrões. Critério: cada arquivo respondendo uma pergunta única.
- **1.2 Mover seções para arquivos novos** — preservar links externos via redirect (nota no original) ou ajuste sistemático cross-repo.
- **1.3 `planning_guidelines.md` vira índice** — overview curto + apontadores para os arquivos derivados.

---

> **Nota — W-MVP-DOC-2 movido para `PROTO-WORKFLOW-FAXINA` como W-PROTO-16.**
> Refinamento estratégico de 2026-04-29 (`claude/refine-workflow-stacks-6JOH6`)
> antecipou a consolidação porque 3 dos 4 arquivos com template duplicado são
> exatamente os tocados por W-PROTO-11 e W-PROTO-15 — fazer junto evita
> revisitar. A funcionalidade originalmente esboçada "2.3 Variantes por fluxo
> (manual vs autônomo)" cai junto com W-PROTO-15.

---

## 💡 Ideias Futuras

Itens que ainda não justificam virar épico — registrados aqui pra não perder, viram épico quando houver sinal real de atrito.

- **Mover `language_guidelines.md` para fora de `docs/process/`.** Guia de bilinguismo (PT-BR para mensagens, EN para código) é regra do código todo do paper-agent, não específica do processo de implementação. Destino candidato: `docs/` raiz ou `core/docs/`. Vira épico quando alguém procurar fora de `process/` e não achar.

- **Decidir destino de `refinement/overview.md` e `workflow/README.md`.** Índices curtos que repetem informação dos arquivos pra que apontam. Custo zero pra leitor familiarizado; ganho marginal de apagar. Vira épico só se a navegação da pasta `process/` for repensada.

---

## 📚 Observações

**Regra:** épico precisa estar em `🔍 Detalhes definidos` para o fluxo
autônomo. (A regra antiga "fluxo manual exige `📋 Critérios definidos`"
some quando `PROTO-WORKFLOW-FAXINA`/W-PROTO-15 fecha — a partir daí
`📋` é apenas passo intermediário até `🔍`.)

Os milestones da fase Protótipo `PROTO-WORKFLOW-ENCERRAMENTO`,
`PROTO-WORKFLOW-DOC` e `PROTO-WORKFLOW-AJUSTES` foram mergeados em
sequência (PRs #83, #90 e #93). `PROTO-WORKFLOW-PLATAFORMA` está em
`🔍 Detalhes definidos` — apto ao fluxo autônomo.
`PROTO-WORKFLOW-FAXINA` e `PROTO-WORKFLOW-COPILOT-STACK` foram
declarados em 2026-04-29 (agrupando os antigos órfãos da fase
Protótipo) e refinados a `🔍` na mesma data
(`claude/refine-workflow-stacks-6JOH6`); a faxina precede
`PROTO-WORKFLOW-FILA` para fazer a casa antes da fila reativa.
`PROTO-WORKFLOW-FILA` (absorve o conteúdo do antigo
MVP-WORKFLOW-PLATAFORMA, reposicionado como Protótipo) tem épicos em
`📐` aguardando refinamento estratégico após
`PROTO-WORKFLOW-PLATAFORMA` e `PROTO-WORKFLOW-FAXINA` fecharem. Os
milestones MVP (`MVP-WORKFLOW-DOC` agora reduzido a 1 épico após
W-MVP-DOC-2 ter migrado para `PROTO-WORKFLOW-FAXINA` como W-PROTO-16,
`MVP-WORKFLOW-REFINAMENTO` e `MVP-WORKFLOW-PROPONENTE`) têm épicos em
`📐` aguardando refinamento estratégico — `MVP-WORKFLOW-DOC` pode
rodar em paralelo (mas se beneficia de W-PROTO-10 ter rodado primeiro);
os outros dois aguardam `PROTO-WORKFLOW-FILA` fechar.

**Refinamento estratégico de 2026-04-29
(`claude/refine-workflow-stacks-6JOH6`):**
levou `PROTO-WORKFLOW-FAXINA` (W-PROTO-10, 11, 13, 15, 16) e
`PROTO-WORKFLOW-COPILOT-STACK` (W-PROTO-14) a `🔍 Detalhes definidos`,
absorveu W-PROTO-12 em W-PROTO-15 (premissa de cindir
`implementation/overview.md` some quando a dicotomia manual/autônomo
some), e moveu W-MVP-DOC-2 para `PROTO-WORKFLOW-FAXINA` como
W-PROTO-16 (3 dos 4 arquivos com template de validação duplicado são
exatamente os tocados pelos outros épicos da faxina). Apto ao
disparo autônomo dos dois milestones.

**Reorganização 2026-04-28 (papéis vs fluxos).** A vision foi reescrita
para separar **papéis** (operador, proponente, porta-voz) de **fluxos**
(refinamento, implementação, encerramento, futuros). Antes o
"refinador autônomo" e o "implementador" apareciam como papéis; agora
são executores de fluxos via skills. Consequências no ROADMAP:
- antigo `MVP-WORKFLOW-PLATAFORMA` foi movido pra Protótipo como
  `PROTO-WORKFLOW-FILA` (fila reativa, sem agente proativo);
- antigo `MVP-WORKFLOW-REFINADOR` virou `MVP-WORKFLOW-REFINAMENTO`
  (fluxo standalone, princípios novos: saltos pequenos, branch
  persiste, PR por épico);
- novo `MVP-WORKFLOW-PROPONENTE` introduz os dois papéis novos
  (proponente + porta-voz) com mecânica de bloqueio entre eles.

**Padronização do campo `**Milestone:**` em ROADMAPs.** O parser
de W-PROTO-PLAT-1.1 trata épicos sem campo `**Milestone:** <id>`
como órfãos ("Sem milestone"). Hoje os ROADMAPs do Revelar e do
core (`docs/ROADMAP.md`) não usam o campo de forma consistente —
ROADMAPs do workflow e do Ensaio já usam. Padronizar é trabalho
fora deste milestone; vira épico próprio quando houver atrito real
no uso da plataforma.

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
