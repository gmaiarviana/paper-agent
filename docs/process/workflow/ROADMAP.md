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
    - **Limitação conhecida (multi-fatia) — em correção:** hoje a detecção é
      **atômica por milestone** (exige *todos* os épicos em 🔍) e o
      `any(... in {🏗️,🔀,✅})` barra o milestone **parcialmente entregue**
      (algumas fatias ✅ + resto 🔍), tornando a continuação invisível à fila
      (só dispatch manual). A correção está refinada em
      **`W-PILOTO-DISP-1`** (milestone `PILOTO-WORKFLOW-DISPATCH-EPICO`):
      dispatch/refino passam a ser **por épico**, gated por **predecessor
      bloqueante** — entrega faseada vira first-class. Enquanto DISP-1 não
      mergear, esta limitação vale.
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
  - `CLEANUP` — épico em ✅ de um milestone **inteiro fechado**
    (todos os épicos ✅) que ainda não passou pela faxina. Épico ✅
    de milestone ainda **aberto** (com irmão em estado ≠ ✅) **não**
    é CLEANUP — é janela de progresso intra-milestone, e
    `detect_cleanup_items` o ignora de propósito. Ação esperada:
    rodar a faxina de **duas fases** — transição `🔀→✅` (stub) por
    épico entregue; **remoção** do bloco só quando o milestone fecha
    inteiro. Mecânica canônica em
    [`epic_completion.md`](../refinement/epic_completion.md),
    aplicada pela [`skills/cleanup/skill.md`](../../../skills/cleanup/skill.md)
    no fold-in do dispatch seguinte (a Action pós-merge original foi
    aposentada). Resolve o ruído visual de "✅ acumulando no kanban"
    sem mexer em `EpicState`.
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
- **Status dos épicos:** W-PROTO-17 ✅.
- **Implementado em:** PR https://github.com/gmaiarviana/paper-agent/pull/123 (merge `49be823`, 2026-06-18).
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
> execução: **UX → Canal único → Proatividade**.
>
> **Decisão de stack (refinamento estratégico 2026-06-19, [ADR 001 do
> workflow](adr/001-stack-da-plataforma.md)):** a plataforma migra de
> Streamlit para **Reflex** a partir do Piloto. A migração é a fundação do
> `PILOTO-WORKFLOW-UX` (épico W-PILOTO-UX-1) e pré-requisito do
> `PILOTO-WORKFLOW-CANAL-UNICO` (disparo headless + progresso ao vivo é o
> driver decisivo). O miolo stack-independente (`parser`, `queue`,
> `prompts`, `config_loader`, `preferences`) é preservado — só a view migra.
> `PILOTO-WORKFLOW-UX` refinado a `📐` nesta sessão; demais épicos/milestones
> ficam para refinamento posterior.

### PILOTO-WORKFLOW-CANAL-UNICO

- **Objetivo:** a plataforma vira **canal único** — o dispatch (e o chat
  focado) acontece de dentro dela, chamando o agente headless por baixo
  dos panos, em vez de copiar prompt pra uma sessão externa. A plataforma
  deixa de ser só leitura e passa a **disparar a execução**; o resultado
  aparece como commits/PR. Runtime inicial: `claude` headless (ver
  §"Tooling de Desenvolvimento > Decisão de runtime").
- **Estágio:** Piloto
- **Épicos agrupados:** a refinar (alto nível — acoplamento
  plataforma↔runtime, disparo de dentro, leitura de progresso). **Inclui o
  redesenho do painel de detalhe para "ação = disparar"** (movido do
  `PILOTO-WORKFLOW-UX` no refinamento de 2026-06-19): a ação nova nasce aqui,
  então o shape do painel quando clicar dispara execução headless — em vez de
  copiar prompt — pertence a este milestone, não à frente de UX.
- **Dependências de core:** nenhuma; depende de PROTO-WORKFLOW-FILA
  mergeada, da fundação Reflex de `PILOTO-WORKFLOW-UX` (W-PILOTO-UX-1, [ADR
  001](adr/001-stack-da-plataforma.md) — streaming de segundo plano é o
  driver da migração) e da tese "Dispatch headless via CLI" (§Tooling).
- **Branch associada:** `milestone/piloto-workflow-canal-unico`
- **Status:** 🌱 Visão — aguarda refinamento estratégico.

### PILOTO-WORKFLOW-UX

- **Objetivo:** **reconstruir o cockpit em Reflex com o polimento embutido**
  — a plataforma agradável de usar todo dia. A migração de stack
  (Streamlit→Reflex, [ADR 001](adr/001-stack-da-plataforma.md)) é a
  **fundação** do milestone; sobre ela aterrissam as frições de UX já
  levantadas em uso real (painel de detalhe some abaixo da viewport com 15+
  itens; redundância card↔painel; valor do clique difere por tipo) e o
  polimento de cockpit invariante ao runtime. Frente distinta do runtime
  integrado (vision §"Eixo de Estágios"); o redesenho do painel para
  "ação = disparar" vive no `PILOTO-WORKFLOW-CANAL-UNICO`, não aqui.
- **Estágio:** Piloto
- **Épicos agrupados:** W-PILOTO-UX-1 (migração Reflex — fundação),
  W-PILOTO-UX-2 (co-visibilidade lista↔detalhe), W-PILOTO-UX-3 (densidade
  da fila), W-PILOTO-UX-4 (informação por tipo no painel).
- **Dependências de core:** nenhuma; depende de PROTO-WORKFLOW-FILA
  mergeada e da [ADR 001](adr/001-stack-da-plataforma.md).
- **Branch associada:** `milestone/piloto-workflow-ux`
- **Status dos épicos:** W-PILOTO-UX-1 ✅ (PR #135, merge `85edd30`),
  W-PILOTO-UX-2 🔍, W-PILOTO-UX-3 🔍, W-PILOTO-UX-4 🔍. **UX-1 (fundação Reflex)
  mergeada; a dependência declarada ("UX-2/3/4 aguardam UX-1 mergear") está
  satisfeita — as três fatias restantes ficam aptas ao próximo dispatch.**
  Milestone parcialmente entregue: continua **aberto** (UX-1 é stub `✅`, janela
  de progresso intra-milestone; poda só no fechamento — ver `epic_completion.md`).
- **Nota:** **absorve o antigo PILOTO-WORKFLOW-FILA-UX** (declarado
  2026-06-17 a partir da revisão da PR #121) e o seed `W-PILOTO-FILA-UX-1`,
  cujas duas frições foram redistribuídas (painel some → UX-2; redundância
  card↔painel → UX-4). Refinamento estratégico de 2026-06-19 (escada
  UX → Canal único → Proatividade): (a) reescopado para polimento invariante
  ao runtime + migração Reflex como fundação — UX primeiro entrega valor
  diário sem especular sobre a ação que o Canal único ainda vai construir;
  (b) o redesenho "ação = disparar" migrou para `PILOTO-WORKFLOW-CANAL-UNICO`,
  onde a ação nova nasce. Coerência de milestone: os 4 épicos tocam a mesma
  camada de view e o mesmo conceito (cockpit) — milestone único é adequado.
  W-PILOTO-UX-1 ganha nota de **spike de viabilidade do Reflex** antes de
  descer a `🔍`.
- **Refinamento tático (2026-06-20):** W-PILOTO-UX-1 (fundação Reflex) e
  W-PILOTO-UX-2 (co-visibilidade lista↔detalhe) levados a `📋 Critérios
  definidos` em passadas cirúrgicas (épico a épico). Decisões de fronteira
  registradas: (a) UX-1 porta o painel de detalhe (`card_detail`) com paridade
  de comportamento (rodapé incluso); o reposicionamento na co-visibilidade é
  de UX-2. (b) UX-2.3 fica no mínimo — cada aba preserva seleção própria,
  sem mapeamento cross-entidade Fila↔Kanban. UX-3/4 seguem em `📐`. Próximo
  passo natural: spike de viabilidade do Reflex e descida de UX-1 a `🔍`.
- **Refinamento a 🔍 (2026-07-04):** spike de viabilidade do Reflex **executado
  e aprovado** (two-pane sticky + tarefa de segundo plano cobertos por props
  nativas; detalhes do spike em `.claudecode.md` §2.6 após a entrega da UX-1). UX-1 descido a
  `🔍 Detalhes definidos` — apto ao fluxo autônomo. Correção de acoplamento
  registrada: o critério 1.4 deixa de "remover streamlit do requirements" e passa
  a "remover só os imports da plataforma" — a linha `streamlit>=1.30.0` é do
  Revelar.
- **Refinamento a 🔍 (2026-07-04, cont.):** UX-2, UX-3 e UX-4 também descidos a
  `🔍` na mesma sessão — **o milestone inteiro fica apto a dispatch**. UX-2
  (co-visibilidade) reusa o mecanismo sticky do spike; UX-3 (densidade) adiciona
  3 campos de estado de sessão (`collapsed_types`/`visible_types`/
  `actionable_only`) e **define "acionável" = `{DISPATCH,REVIEW,REFINE}`**
  (decisão de valor, revisável — ver épico); UX-4 (informação por tipo) é
  view-only reusando o roteamento por ponteiro de `render_queue_item_detail`.
  Decisões de fronteira registradas: filtro de tipo é de **sessão** (não
  `preferences.json`); card terso (UX-3.1) ↔ painel profundo (UX-4.2). Todos os 4
  dependem de UX-1 mergear (fundação Reflex) antes de implementar.
- **Refinamento de conteúdo (2026-07-06):** UX-3 (permanece em `🔍`, sem mudança
  de estado) refinado a partir da sessão de validação da W-PILOTO-UX-1. A "decisão
  de valor a confirmar" fica **confirmada**: a fila tem **duas naturezas** — Ações
  = `{DISPATCH,REVIEW,REFINE}` e Higiene = `{CLEANUP,STALE_BRANCH}` — e a UX-3.4
  vira **duas seções** (Ações vs Higiene), não mais um toggle "só acionável" que
  esconde; a Higiene segue **visível** sob sua seção. Registrado também que o
  regulador de carga (~20) conta só Ações e é mecanismo do fluxo autônomo (UX do
  limite adiada — vision §"Fila"), e o item B (coluna `✅` do Kanban não cresce sem
  fim) entra como UX-3.5, cross-ref `W-PILOTO-HIGIENE-1`. Canon espelhado na
  vision §"Fila". Docs-only, sem mudança de código.

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

### PILOTO-WORKFLOW-DISPATCH-EPICO

- **Objetivo:** dispatch **e** refino passam a operar por **épico**, não só por
  milestone — a plataforma deixa o operador disparar/refinar uma fatia isolada
  quando ela está no estágio certo (🔍 para dispatch; 📐/📋 para refino).
  Introduz o **predecessor bloqueante**: épico (ou milestone) que depende de
  outro ainda não `✅` **não** é oferecido como ação — some da Fila e aparece de
  forma discreta e comunicada no Kanban. Resolve de raiz o ponto cego da detecção
  atômica por milestone (milestone parcialmente entregue voltava invisível à
  fila) e é fundação da `PILOTO-WORKFLOW-PROATIVIDADE` (que auto-dispara o que a
  fila detecta como pronto).
- **Estágio:** Piloto
- **Épicos agrupados:** W-PILOTO-DISP-1 (dispatch/refino por épico + predecessor
  bloqueante — dado, detecção, prompts, plataforma).
- **Dependências de core:** W-PILOTO-UX-1 (fundação Reflex, já `✅`) e
  PROTO-WORKFLOW-FILA (detectores da fila). **Não** depende de UX-2/3/4.
- **Ordem na escada:** roda **após UX-1 (entregue) e antes de UX-2/3/4** — é o
  mecanismo pelo qual as próprias fatias UX-2/3/4 serão despachadas; pegada de
  view pequena (UX-2/3/4 reaproveitam por cima sem conflito grande).
- **Branch associada:** `milestone/piloto-workflow-dispatch-epico`
- **Status dos épicos:** W-PILOTO-DISP-1 `🔍`.
- **Nota:** declarado e refinado a `🔍` em 2026-07-06, na sessão que descobriu o
  ponto cego multi-fatia (dispatch da W-PILOTO-UX-1 entregue em fatia). Design
  completo no bloco do épico. Milestone de mecânica de fila/dispatch — separado
  do `PILOTO-WORKFLOW-UX` (polimento de cockpit invariante ao runtime) pela mesma
  régua que já mandou o redesenho "ação = disparar" para o `CANAL-UNICO`.

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

### MVP-WORKFLOW-DESACOPLE

- **Objetivo:** extrair o workflow para um **repo próprio** e provar que
  ele **sincroniza** — opera o mesmo fluxo de desenvolvimento contra um
  repo-alvo qualquer, começando pelo próprio paper-agent como primeiro
  alvo. Materializa o Horizonte da vision "Release a colegas e workflow
  como produto desacoplado" na parte **técnica** (o mecanismo de sync),
  deliberadamente **separada** do release a colegas (auth, multi-persona,
  ambiente corporativo — que ficam em `MVP-WORKFLOW-PROPONENTE`/Horizonte).
- **Natureza do acoplamento (o que este milestone realmente resolve):** o
  **código da plataforma já está desacoplado** do paper-agent — `config.yaml`
  externaliza `owner/repo` + lista de ROADMAPs e o `config_loader` acha o
  repo root por marcador; apontar pra outro repo é config. O que está
  acoplado é o **processo**: o dispatch emite `"implementa o <MILESTONE_ID>"`
  em linguagem natural, e isso só significa algo porque o repo-alvo contém
  as `skills/` e os `docs/process/` que ensinam o agente. Logo, "desacoplar
  e sincronizar" é sobre **fazer o processo viajar** pro alvo, não sobre
  limpar hardcode da plataforma.
- **Estágio:** MVP
- **Épicos agrupados:** a refinar (alto nível). O milestone se parte em
  **duas metades com dependências técnicas distintas** — a ordem importa:
  - **(A) Portabilidade do processo.** As skills (`skills/`) e a convenção
    de ROADMAP (estados de épico 🌱→✅) viajam pra um segundo repo e o
    agente roda **standalone** lá (Claude Code Web direto, como hoje). Não
    depende do canal único nem da plataforma multi-repo. É o **spike que
    torna a fronteira genérico-vs-paper-agent legível pelo uso** — e o que
    resolve a decisão de mecanismo (ver "Decisão em aberto"). De-riskável
    cedo (ver "Nota de timing").
  - **(B) Plataforma multi-repo.** A fila/kanban/dispatch da plataforma
    passa a operar sobre N repos: `config.yaml` multi-repo (fila por repo,
    dispatch sabe qual repo), auth/git access ao alvo. Depende de (A)
    resolvida e do **canal único** — a plataforma só dispara *em outro*
    repo depois de saber disparar *de dentro* de um.
- **Dependências de core:** nenhuma; depende de
  `PILOTO-WORKFLOW-CANAL-UNICO` (a metade B precisa do contrato de
  execução headless) e reusa o miolo stack-independent já isolado no
  [ADR 001](adr/001-stack-da-plataforma.md) (`parser`, `queue`, `prompts`,
  `config_loader`). A metade A não depende do Piloto.
- **Contrato de adoção do alvo (o que um repo-alvo precisa cumprir para
  entrar no fluxo):** três condições, a serem formalizadas no refinamento —
  (1) **ROADMAP na convenção** — markdown com o vocabulário de estados de
  épico (🌱→✅), que o `parser.py` (defensivo, baseado em convenção) já lê;
  (2) **skills alcançáveis do checkout** onde o agente roda — via o
  mecanismo escolhido na "Decisão em aberto"; (3) **auth/git access** ao
  alvo (hoje `owner/repo` é só string pra montar URL). Repo que cumpre as
  três → o mesmo fluxo roda igual; é isso que torna "replicável pra repo
  novo" verdadeiro. Este contrato é o **produto** do desacople — não a
  extração em si.
- **Branch associada:** `milestone/mvp-workflow-desacople`
- **Status:** 🌱 Visão — aguarda refinamento estratégico.
- **Decisão em aberto (para refinamento — NÃO decidir agora):** como as
  skills chegam ao repo-alvo. Três modelos avaliados na sessão de
  2026-07-05:
  - **Cópia (vendored)** — alvo guarda cópia das skills. Roda standalone
    ✅, mas gera N cópias com drift, sincronia manual e conflito de merge
    ao customizar. É o **status quo implícito** (paper-agent hoje).
  - **Injetado** — repo `workflow` monta as skills no checkout do alvo no
    dispatch. Fonte única ✅, mas **mata o dispatch standalone** (alvo
    passa a depender da plataforma de pé) e exige mecanismo de mount.
  - **Dependência versionada** *(candidata recomendada)* — alvo declara
    `workflow-skills @ vX.Y` e um passo de sync puxa a versão (subtree/
    submodule/package). Preserva standalone ✅ **e** dá fonte única ✅;
    customização vira override em camada, não edição da fonte (sem
    conflito de merge). Casa com a frase da vision "skills versionadas por
    destino". Preço: exige disciplina de release das skills (semver/
    changelog) — overhead só justificável a partir do segundo alvo real.
- **Nota de timing (refinamento 2026-07-05):** o milestone fica no MVP,
  mas a **metade A (spike de portabilidade) é de-riskável antes** — no fim
  do Piloto — porque não depende do canal único. É o experimento barato que
  torna a decisão de mecanismo legível pelo uso, contra um **segundo repo
  do próprio operador** (não um colega). O gatilho duro do movimento
  completo (extração + plataforma multi-repo) continua sendo o **primeiro
  alvo que não carrega as skills** — tipicamente o release a colegas, mas
  a costura de sync pode e deve ser provada antes disso, isolada do peso de
  auth/multi-persona. Se o Piloto estiver apertado, A escorrega pro início
  do MVP sem perda — é independente, não bloqueia nada.
- **Nota:** milestone declarado em 2026-07-05 a partir de sessão de
  refinamento estratégico sobre desacoplamento e sync (branch
  `claude/product-decoupling-sync-qvxxy6`). Alto nível — aguarda
  refinamento estratégico que quebre A e B em épicos.

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
- **Auth: assinatura Max do operador (login da conta), não API key.** Verificado nas docs do Claude Code (2026-06-19): `claude -p` (headless) funciona sob credenciais de assinatura. Exceção: o modo `--bare` (CI) ignora OAuth e exige `ANTHROPIC_API_KEY`/`apiKeyHelper` — não usar `--bare` no canal único.
- **Fallback por precedência de env var:** se `ANTHROPIC_API_KEY` está setada, ela tem precedência sobre a assinatura; `unset ANTHROPIC_API_KEY` volta pra assinatura. Trocar entre os dois é trivial, sem reescrita.
- **Ressalva para o auto-dispatch (`PILOTO-WORKFLOW-PROATIVIDADE`):** uso *agendado / não-assistido* é **medido à parte** do uso interativo — pool de créditos "autonomous" e, no caso de Scheduled Routines, teto de runs/dia (números a confirmar no billing oficial; fontes recentes citam ~15/dia e pool de ~US$100–200/mês no Max). O canal único (disparo pelo operador) é interativo e não tem essa contabilização. Conclusão: assinatura cobre baixo volume de auto-dispatch; se escalar, fallback de API só nessa fase.
- O caminho de migração para modelos locais (`opencode` contra OpenWebUI/Ollama) segue válido e encaixa no Horizonte "Runtime de agente sobre providers corporativos (estágio MVP)" — o runtime é trocável por contrato de execução, não reescrita.

**Configuração opencode (referência):**
- Provider em `opencode.json` (root): `@ai-sdk/openai-compatible` contra OpenWebUI
- Variáveis `.env`: `OPENWEBUI_API_KEY`, `OPENWEBUI_BASE_URL`
- Setup via `infra/llm-clients/setup-opencode.ps1`
- Modelos disponíveis: `gpt-oss:20b` (default), `qwen3.6:35b`, `llama3.2:3b`

---

## 📋 Épicos Planejados

### ⏳ Fase Piloto

> **Milestones:** `PILOTO-WORKFLOW-UX` (W-PILOTO-UX-1 `✅` mergeada — PR #135;
> UX-2/3/4 em `🔍`, aptas ao próximo dispatch) · `PILOTO-WORKFLOW-CANAL-UNICO` ·
> `PILOTO-WORKFLOW-PROATIVIDADE`.
> Escada de execução: **UX → Canal único → Proatividade**. Escopo macro de
> CANAL-UNICO e PROATIVIDADE nos cards de milestone acima (ainda `🌱`); só
> `PILOTO-WORKFLOW-UX` tem épicos refinados. Fundação Reflex (UX-1) implementada
> e em revisão (2026-07-04); UX-2/3/4 seguem para dispatch sobre a fundação
> mergeada. Seed órfão na fase (sem milestone):
> `W-PILOTO-HIGIENE-1` (cleanup efetivo / ROADMAP enxuto, `🌱`).

> **Nota de refinamento (2026-06-19).** O seed `W-PILOTO-FILA-UX-1` (🌱,
> herdado do antigo `PILOTO-WORKFLOW-FILA-UX`) foi absorvido pelos 4 épicos
> abaixo: a frição "painel some abaixo da viewport" virou W-PILOTO-UX-2 e
> "redundância card↔painel" virou W-PILOTO-UX-4. A migração de stack
> (Streamlit→Reflex, [ADR 001](adr/001-stack-da-plataforma.md)) entra como
> fundação (W-PILOTO-UX-1). O redesenho "clique dispara execução" saiu daqui
> para `PILOTO-WORKFLOW-CANAL-UNICO`.

#### ÉPICO W-PILOTO-UX-1: Migração da plataforma para Reflex (fundação + fatia fina)

**Milestone:** `PILOTO-WORKFLOW-UX`

**Status:** ✅ Implementado

**Entregue em:** PR [#135](https://github.com/gmaiarviana/paper-agent/pull/135) (merge `85edd30`, 2026-07-06) — camada de view da plataforma migrada de Streamlit para Reflex ([ADR 001](adr/001-stack-da-plataforma.md)): esqueleto `rx.State`, abas Fila/Kanban portadas, imports Streamlit da plataforma retirados. Miolo stack-independente preservado; subpacote `queue/` renomeado para `job_queue/` (fix de shadowing da stdlib no Windows). Descobertas de Reflex (spike two-pane sticky + tarefa de segundo plano, dataclasses tipados, gotchas do `reflex run`) extraídas para `.claudecode.md` §2.6 — contexto dos irmãos UX-2/3/4.

---

#### ÉPICO W-PILOTO-UX-2: Layout de cockpit — co-visibilidade lista↔detalhe

**Milestone:** `PILOTO-WORKFLOW-UX`

**Objetivo:** eliminar o atrito estrutural #1 do uso real — o painel de detalhe some abaixo da viewport quando a fila/kanban enche (hoje renderiza no rodapé, depois de todos os cards). Lista e detalhe convivem na tela; selecionar um item nunca exige rolar pra achar o detalhe. Viável nativamente no Reflex. Absorve a frição 1.1 do seed `W-PILOTO-FILA-UX-1`.

**Status:** 🔍 Detalhes definidos

**Dependências:** W-PILOTO-UX-1 (camada Reflex existente) — dura: UX-2 não
começa antes de UX-1 mergear.

### Refinamento a 🔍 (2026-07-04) — layout provado no spike

**Mecanismo sticky/two-pane — já provado no spike de UX-1** (2026-07-04, Reflex
0.9.0), com props nativas, sem hack:
`rx.hstack(lista, detalhe, align="start", height="100vh")`, cada coluna um
`rx.box` com `height="100vh"` + `overflow_y="auto"`, e a coluna de detalhe
somando `position="sticky"` + `top="0"`. `align="start"` (não `stretch`) é o que
habilita o sticky por coluna. Confirmado: `sticky`/`overflowY`/`top`/`100vh`
chegam ao render compilado.

**a) Termos.** Sem termo comportamental novo. "Co-visibilidade" = lista e
detalhe na mesma viewport; "ancorado/sticky" = `position: sticky` (CSS nativo
via prop Reflex).

**b) Dados e contratos.** UX-2 é view-only — **não adiciona campo de estado**.
Reusa os campos já definidos em UX-1 (`PlatformState`): `selected_item_id` (aba
Fila) e `selected_epic_id`/`selected_milestone_id` (aba Kanban), mais
`active_tab`. A continuidade de seleção (2.3) é **consequência** de os dois
campos serem independentes e persistirem no `rx.State` do servidor entre trocas
de aba — o handler `set_active_tab` não pode resetá-los. Placeholder de painel
vazio (2.1): `rx.cond(PlatformState.selected_item_id == "", placeholder(), detail())`.

**c) Código-alvo e integração.**

- **Modificar** (componentes criados por UX-1):
  - `web/components/queue.py` e `web/components/kanban.py` — encapsular
    lista + detalhe num `rx.hstack` de duas colunas. (Na fatia de UX-1 o detalhe
    é portado com paridade — no rodapé; UX-2 reposiciona para co-visibilidade.)
  - `web/components/detail.py` — adicionar o estado-vazio (placeholder) e as
    props de âncora (`position="sticky"`, `top="0"`, `overflow_y="auto"`).
- **Criar (opcional):** `web/components/layout.py` com um wrapper
  `two_pane(list, detail)` se a composição for compartilhada entre Fila e Kanban
  (evita duplicar o hstack); senão fica inline nos dois componentes.
- **Não tocar:** miolo e `web/state.py` (sem campo de estado novo).
- **Mecanismo de integração:** puramente composição de componentes + props CSS.
  Nenhuma lógica de detecção/estado nova.
- **Template de estilo:** `products/ensaio/app/app.py::index` (hstack de duas
  colunas full-height) + o spike registrado no épico UX-1.
- **Divisão de colunas (default, ajustável):** lista ~40% / detalhe ~60%
  (espelha o 60/40 do Ensaio). Não é canon — ajuste fino de proporção cabe na
  implementação sem novo refinamento.

**d) Acoplamentos.** Depende inteiramente da camada Reflex de UX-1 — dependência
dura declarada. Não toca `core/` nem `products/`; sem consumidor compartilhado.
Ressalva verificada no spike: o container-pai não pode forçar `overflow: hidden`
cortando a coluna — funciona com `overflow_y="auto"` por coluna + `align="start"`
no hstack.

**e) Sequência e testes.**

- **Ordem:** 2.1 (duas colunas + placeholder) → 2.2 (âncora sticky + scroll
  independente) → 2.3 (continuidade de seleção). 2.3 é asserção sobre estado,
  independente do CSS.
- **Layout/sticky (2.1, 2.2):** validação **manual** via `reflex run` — roteiro:
  encher a fila com 15+ itens, selecionar um item no topo, rolar a lista até o
  fim, confirmar que o painel segue visível; alternar Fila↔Kanban e voltar,
  confirmar seleção preservada em cada aba. CSS/layout não tem teste automatizado
  observável — declarado como validação manual (padrão da camada de view no
  Protótipo).
- **Continuidade de seleção (2.3):** automatizável em
  `tests/tools/workflow_platform/test_platform_state.py` — setar
  `selected_item_id` e `selected_epic_id`, chamar `set_active_tab` ida-e-volta,
  assertar que ambos persistem (sem subir frontend).

**f) Centralidade da visão.** Ataca o atrito estrutural #1 do uso real (vision
§"Norte de curto prazo": cockpit agradável de usar todo dia). Preserva a
fronteira já declarada em 2.3 (mapeamento cross-aba fora de escopo). Nada central
cortado.

### Funcionalidades:

#### 2.1 Layout de duas colunas (lista | detalhe)

- **Descrição:** lista e painel de detalhe lado a lado na mesma tela, nas abas Fila e Kanban; selecionar atualiza o painel sem rolar.
- **Critérios de Aceite:**
  - Em ambas as abas (Fila e Kanban), lista e detalhe devem renderizar lado a lado na mesma viewport — fim do detalhe no rodapé.
  - Selecionar um item/épico na lista deve atualizar o painel sem deslocar a posição de rolagem da lista.
  - Sem item selecionado, o painel deve mostrar um estado vazio claro (placeholder), sem colapsar o layout.

#### 2.2 Painel de detalhe ancorado

- **Descrição:** o painel permanece visível ao rolar a lista longa (sticky); as colunas rolam de forma independente.
- **Critérios de Aceite:**
  - Com 15+ itens na lista, rolar a lista deve manter o painel de detalhe visível (ancorado), sem precisar caçá-lo.
  - Lista e painel devem ter rolagem independente (scroll por coluna).

#### 2.3 Continuidade de seleção entre Fila e Kanban

- **Descrição:** alternar entre abas não perde a seleção feita em cada uma.
- **Critérios de Aceite:**
  - Cada aba (Fila, Kanban) deve preservar sua própria seleção ao alternar para a outra aba e voltar.
  - Mapeamento cross-aba (item da Fila ↔ épico no Kanban) fica **fora de escopo** — as seleções são independentes por aba. Item da Fila e épico do Kanban são entidades distintas e o mapeamento é 1:N ou indefinido para vários tipos (`DISPATCH`, `STALE_BRANCH`); reabre só com sinal de atrito real.

---

#### ÉPICO W-PILOTO-UX-3: Densidade e escaneabilidade da fila

**Milestone:** `PILOTO-WORKFLOW-UX`

**Objetivo:** fila escaneável com 15+ itens — o operador vê "o que pede ação agora" num olhar, sem ler card a card.

**Status:** 🔍 Detalhes definidos

**Dependências:** W-PILOTO-UX-1 (camada Reflex existente) — dura. Coordena com
W-PILOTO-UX-4 na fronteira card↔painel (ver Acoplamentos).

### Refinamento a 🔍 (2026-07-04)

**a) Termos.** Duas **naturezas** de item, confirmadas como categorias distintas
(operador, 2026-07-06): **Ações** — avanço de trabalho que o operador dispara
agora — `DISPATCH`, `REVIEW`, `REFINE` — e **Higiene** — manutenção/triagem —
`CLEANUP`, `STALE_BRANCH`. `STALE_BRANCH` ainda pede olho humano, mas é natureza
diferente de "avançar/resolver"; por isso segue **visível**, sob Higiene, e não
escondido. A distinção é canon da vision (§"Fila"). "Grupo por tipo" = os 5
buckets já fixados em `views/queue.py::_TYPE_ORDER`
(`DISPATCH→REVIEW→REFINE→CLEANUP→STALE_BRANCH`); as duas seções (3.4) agrupam
esses buckets pelas duas naturezas.

**b) Dados e contratos — 2 campos de estado novos em `PlatformState` (UX-1).**
UX-3 é view-only sobre a detecção; **não muda `QueueItem` nem `queue/detect.py`**.

| campo | tipo | default | funcionalidade |
|---|---|---|---|
| `collapsed_types` | `list[str]` | `[]` | 3.2 (grupos recolhidos) |
| `visible_types` | `list[str] \| None` | `None` (todos) | 3.4 (filtro por tipo, opcional) |

O split em duas seções por natureza (3.4) é render-time — **não precisa de flag
de estado**: as seções Ações e Higiene sempre renderizam. Some por isso o antigo
campo `actionable_only` (o "toggle que esconde" foi substituído por "duas
seções"). Ordenação (3.3): dentro de cada grupo, por `QueueItem.detected_at` desc
— campo **já existe** no shape (`queue/models.py`); a ordenação é da view, sem
lógica de detecção nova. Seções (3.4): a view parte `queue_items` em **Ações**
(`DISPATCH`/`REVIEW`/`REFINE`) e **Higiene** (`CLEANUP`/`STALE_BRANCH`); o filtro
por tipo opcional (`visible_types`, via `@rx.var` `visible_queue_items`) recorta
dentro das seções. Split e filtro são funções puras do estado.

**c) Código-alvo e integração.**

- **Modificar** (componentes criados por UX-1):
  - `web/components/queue.py` — cards compactos (3.1), cabeçalho de grupo
    clicável p/ colapsar (3.2), legenda de ordenação no header (3.3), e a fila
    partida em **duas seções** (Ações e Higiene), cada uma com seus grupos por
    tipo, consumindo `visible_queue_items` no lugar de `queue_items` (3.4).
  - `web/components/sidebar.py` — controle de filtro por tipo opcional, ao lado do
    filtro por ROADMAP já entregue em FILA-4.3.
  - `web/state.py` — os 2 campos acima + handlers `toggle_type_collapse(t)`,
    `set_visible_types(list)` + `@rx.var` `visible_queue_items`.
- **Não tocar:** miolo (`queue/detect.py`, `queue/models.py`, `parser.py`).
- **Mecanismo:** filtro/ordenação/colapso vivem inteiramente na view + estado.
  Nenhuma peça nova no pipeline de detecção.
- **Template de estilo:** o `render_queue`/`group_by_type` atuais
  (`views/queue.py`) — mesma lógica de agrupamento, reescrita compacta em Reflex.

**d) Acoplamentos.**
- **Persistência do filtro — decisão registrada: sessão, não `preferences.json`.**
  O filtro por ROADMAP (FILA-4) é durável (quais projetos me importam); o filtro
  por tipo (`visible_types`) é **foco do momento** (o que olho agora) — fica no
  `rx.State` da sessão, reseta no reload. Evita tocar o miolo `preferences.py`.
  Revisável se o operador pedir persistência. As duas seções (Ações/Higiene) são
  **estruturais**, não preferência — sempre renderizam, sem estado a persistir.
- **Fronteira com UX-4 (coordenação):** UX-3.1 torna o **card** compacto (título
  + emoji + contexto terso, sem o prompt grande); UX-4.2 decide o que o **painel**
  aprofunda. Card terso ↔ painel profundo é a fronteira; ambos os épicos a
  declaram. Sem dupla-fonte: a "Ação esperada" longa sai do card e vive no painel.
- Não toca `core/`/`products/`; sem consumidor compartilhado.

**e) Sequência e testes.**
- **Ordem:** 3.1 (cards) → 3.2 (colapso) → 3.3 (ordenação) → 3.4 (filtro).
  Independentes entre si; nenhuma bloqueia a outra.
- **Automatizável** (`tests/tools/workflow_platform/test_platform_state.py`):
  o split por natureza é função pura — assertar que a seção **Ações** contém só
  `DISPATCH`/`REVIEW`/`REFINE` e a seção **Higiene** só `CLEANUP`/`STALE_BRANCH`,
  ambas presentes (nenhum tipo some); `visible_queue_items` (filtro por tipo)
  recorta dentro das seções; `toggle_type_collapse` muta `collapsed_types`.
- **Manual** (`reflex run`): densidade dos cards (3.1) e ordenação legível (3.3)
  — inspeção visual com fila de 15+ itens.

**f) Centralidade da visão.** Vision §"Fila" pede escaneabilidade e agora nomeia
as duas naturezas (Ações vs Higiene); UX-3 materializa a distinção como **duas
seções**, sem cortar tipo nenhum — a Higiene fica visível na sua própria seção e
a detecção dos 5 tipos permanece intacta.

**Decisão de valor — confirmada (operador, 2026-07-06):** as duas naturezas são
**Ações** = `{DISPATCH, REVIEW, REFINE}` e **Higiene** = `{CLEANUP, STALE_BRANCH}`.
Racional: Ações avançam trabalho; `CLEANUP` é o ruído que `W-PILOTO-HIGIENE-1`
quer dissolver na fonte, e `STALE_BRANCH` é triagem que ainda pede olho humano —
por isso Higiene fica **visível**, sob sua seção, e não escondida. A distinção
vira **seção**, não filtro de esconder: a fila renderiza Ações e Higiene lado a
lado. Canon espelhado na vision §"Fila".

**Regulador de carga (limite ~20) — nota de escopo (2026-07-06):** quando o badge
de carga / limite ~20 for (re)desenhado, ele conta **só Ações** — Higiene nunca
entra na conta. E o regulador é mecanismo do **fluxo autônomo**: no Protótipo
reativo de hoje não há autônomo criando itens a segurar, então a UX de como (ou
se) exibir o limite fica para quando o autônomo chegar — não se desenha aqui.
Canon na vision §"Fila". (O badge `n/20` + banner OVER_LIMIT já entregues em
PROTO-WORKFLOW-FILA são, sob essa leitura, prematuros no Protótipo; sua revisão
pertence ao momento do fluxo autônomo, não a este épico.)

**Item B — exibição do "done" no Kanban (refinamento de view, 2026-07-06):** a
coluna `✅` do Kanban cresce hoje sem limite — mesmo princípio das duas naturezas,
aplicado ao eixo **presente vs passado**: ação presente não deve dividir espaço
com histórico de entrega. O tratamento é de **exibição** (colapsar/resumir/paginar
o passado), não de vision — o Kanban de 8 colunas por estado, `✅` incluída, segue
canônico (vision §"Kanban"). A **raiz** (podar `✅` do ROADMAP na fonte) é
`W-PILOTO-HIGIENE-1`; aqui fica só o cuidado de exibição, cross-ref a HIGIENE-1 e
às duas categorias. Materializado como funcionalidade 3.5 abaixo.

### Funcionalidades:

- **3.1 Cards compactos** — título + emoji de tipo + contexto terso numa altura
  reduzida; a "Ação esperada" longa migra para o painel (UX-4). **Aceite:** com
  15+ itens, um card ocupa menos altura vertical que a versão Streamlit; sem o
  bloco de ação longo dentro do card.
- **3.2 Colapsar/expandir grupos por tipo** — cabeçalho de grupo alterna
  recolhido/expandido; `collapsed_types` guarda o estado. **Aceite:** clicar no
  cabeçalho de um tipo recolhe seus cards; o estado persiste durante a sessão;
  demais grupos inalterados.
- **3.3 Ordenação legível** — dentro de cada grupo, itens por `detected_at` desc;
  cabeçalho informa o critério. **Aceite:** o header de cada grupo declara
  "ordenado por detecção (mais recente primeiro)"; a ordem observada bate.
- **3.4 Duas seções: Ações vs Higiene** — a fila renderiza em duas seções por
  natureza: **Ações** (`DISPATCH`/`REVIEW`/`REFINE`) e **Higiene**
  (`CLEANUP`/`STALE_BRANCH`), ambas **sempre visíveis** (Higiene não é escondida —
  `STALE_BRANCH` ainda pede revisão humana). Filtro por tipo opcional na sidebar
  recorta dentro das seções, ao lado do filtro por ROADMAP (FILA-4). **Aceite:** a
  fila mostra as duas seções separadas; `CLEANUP`/`STALE_BRANCH` aparecem sob
  Higiene (não somem); desmarcar um tipo o remove da vista (contagem cai); tudo
  opera sobre `visible_queue_items` sem alterar a detecção subjacente.
- **3.5 Exibição do "done" no Kanban** — a coluna `✅` não deve crescer sem fim
  (item B; mesmo princípio presente vs passado). Tratamento de **exibição**
  (colapsar/resumir/paginar o passado), sem tocar `EpicState` nem a detecção; a
  poda de `✅` na fonte é `W-PILOTO-HIGIENE-1`. **Aceite:** com muitos `✅`
  acumulados, a coluna não empurra as colunas de estado ativo para fora da
  viewport; o passado fica recolhido/resumido por padrão, expansível sob demanda;
  as 8 colunas por estado permanecem canônicas.

---

#### ÉPICO W-PILOTO-UX-4: Painel de detalhe — informação certa por tipo

**Milestone:** `PILOTO-WORKFLOW-UX`

**Objetivo:** cada tipo de item/épico mostra no painel o contexto que importa pra decidir, sem ruído nem redundância com o card — a parte do "valor do clique" invariante ao runtime. O redesenho do mecanismo de ação ("ação = disparar") vive no `PILOTO-WORKFLOW-CANAL-UNICO`, não aqui. Absorve a frição 1.2 do seed `W-PILOTO-FILA-UX-1`.

**Status:** 🔍 Detalhes definidos

**Dependências:** W-PILOTO-UX-1 (camada Reflex existente) — dura; coordena com
W-PILOTO-UX-2 (o painel é o detalhe da co-visibilidade) e W-PILOTO-UX-3 (fronteira
card terso ↔ painel profundo).

### Refinamento a 🔍 (2026-07-04)

**a) Termos.** Sem termo comportamental novo. Reusa os 5 tipos e o tagged-union
de ponteiros (`queue/models.py`: `EpicPointer`, `PRPointer`, `BranchPointer`,
`RefinePointer`, `CleanupPointer`). "Valor do clique invariante ao runtime" =
conteúdo informacional do painel, sem o mecanismo de disparo (que é do
`PILOTO-WORKFLOW-CANAL-UNICO`).

**b) Dados e contratos.** UX-4 é **view-only, sem campo de estado novo**. Consome
o que já existe:
- `QueueItem.source_pointer` (discriminado por tipo) → roteamento do painel (4.1);
- `QueueItem.context` → o sinal determinístico do "porquê" (4.3), **já preenchido**
  por `queue/detect.py` (ex.: "milestone X com todos os épicos em 🔍");
- builders puros `build_prompt_for_item` / `build_dispatch_prompt` /
  `build_refinement_prompt` → o artefato profundo (4.2). Nenhum builder novo.

Contrato de roteamento por tipo (4.1) — **destaque do painel por ponteiro:**

| tipo | ponteiro | painel destaca |
|---|---|---|
| `DISPATCH` | `EpicPointer` | `milestone_id`, `roadmap_path`, épicos; prompt de dispatch (profundo) |
| `REVIEW` | `PRPointer` | link `PR #N` |
| `REFINE` | `RefinePointer` | `epic_id`, `current_state → target_state`; prompt de refinamento (profundo) |
| `CLEANUP` | `CleanupPointer` | `epic_id`, `title`, `roadmap_path` |
| `STALE_BRANCH` | `BranchPointer` | `branch_name` (link GitHub), `days_stale` |

Esse roteamento **já existe parcialmente** em
`views/queue.py::render_queue_item_detail` (roteia por `isinstance` do ponteiro)
e em `views/card_detail.py` (roteia épico do Kanban por `epic.state`). UX-4
consolida os dois roteadores na camada Reflex.

**c) Código-alvo e integração.**
- **Modificar** (componente criado por UX-1):
  - `web/components/detail.py` — roteador por tipo de ponteiro (item de Fila) e
    por estado (épico de Kanban); destaque do `context` no topo (4.3); poda da
    redundância com o card (4.2).
- **Sugestão (opcional, p/ testabilidade):** extrair
  `panel_fields_for(item) -> dict` como função pura (que campos o painel mostra
  por tipo), deixando o componente Reflex fino. Permite teste unit sem frontend.
- **Não tocar:** miolo; nenhum builder de prompt novo (reusa os existentes).
- **Mecanismo:** composição de componentes + roteamento por tipo. Sem lógica de
  detecção/estado nova.
- **Template de estilo:** `views/queue.py::render_queue_item_detail`
  (roteamento por ponteiro, já feito) + `views/card_detail.py` (roteamento por
  estado no Kanban).

**d) Acoplamentos.**
- **Coordena UX-2** (o painel é o detalhe da co-visibilidade — mesmo container) e
  **UX-3.1** (card terso): a "Ação esperada" longa e o prompt grande vivem **no
  painel** (UX-4), não no card. Fronteira declarada nos dois épicos.
- **Fila vs Kanban:** o painel serve as duas abas — item de Fila roteia por
  ponteiro; épico de Kanban roteia por estado (`card_detail`). UX-4 cobre os dois
  roteadores.
- Reusa builders puros; não toca detecção nem `core/`/`products/`. Sem consumidor
  compartilhado.

**e) Sequência e testes.**
- **Ordem:** 4.1 (roteamento por tipo) → 4.2 (redução de redundância, coordena
  UX-3.1) → 4.3 (destaque do "porquê"). 4.3 é trivial (surface de `item.context`).
- **Automatizável** (se `panel_fields_for` for extraída):
  `tests/tools/workflow_platform/` — para um `QueueItem` de cada tipo, assertar
  que o dict de campos traz o esperado (link PR p/ REVIEW, `days_stale` p/
  STALE_BRANCH, prompt p/ DISPATCH/REFINE). Os builders já têm testes próprios.
- **Manual** (`reflex run`): selecionar um item de cada tipo e confirmar o painel
  — link certo, sem repetir o card, `context` visível no topo.

**f) Centralidade da visão.** Vision §"Chat focado"/"Forma da Plataforma": o
clique entrega contexto certo pra decidir. Preserva a fronteira declarada — o
redesenho "ação = disparar" fica no `PILOTO-WORKFLOW-CANAL-UNICO`, não aqui. UX-4
cuida só do conteúdo informacional. Nada central cortado.

### Funcionalidades:

- **4.1 Contexto por tipo** — o painel roteia por tipo/ponteiro (tabela acima),
  destacando o que importa por tipo. **Aceite:** selecionar um item de cada um
  dos 5 tipos mostra o campo-chave correspondente (link PR, idade da branch,
  transição de estado, milestone, título) sem os campos irrelevantes dos outros
  tipos.
- **4.2 Redução de redundância card↔painel** — card resume + ação curta; painel
  aprofunda só onde agrega (prompt grande de `DISPATCH`/`REFINE`). **Aceite:** o
  prompt clipboard-ready grande aparece **só** no painel, não no card; o card não
  repete o bloco de ação longo (coordena com UX-3.1).
- **4.3 Legibilidade do "porquê este item existe"** — o painel exibe
  `QueueItem.context` (sinal determinístico) com destaque. **Aceite:** o painel de
  qualquer item mostra, no topo, o motivo determinístico da detecção (ex.:
  "milestone X com todos os épicos em 🔍").

---

#### ÉPICO W-PILOTO-HIGIENE-1: Cleanup efetivo e ROADMAP enxuto

**Milestone:** _(órfão — sem milestone; aguarda refinamento estratégico para
agrupar ou seguir solo)_

**Objetivo:** garantir que épicos concluídos saiam do ROADMAP ativo de forma
confiável — ROADMAP = **presente + futuro**, sem histórico de entrega (que
vive no git/PR). Hoje ~34 épicos em `✅` permanecem inteiros nos ROADMAPs
lidos pela plataforma (`Status: ✅` + `Entregue em: PR #X`), inchando o
ROADMAP e inundando a fila com um item `CLEANUP` por épico.

**Status:** 🌱 Visão

**Decisão de princípio registrada (operador, 2026-06-20):** ROADMAP enxuto,
sem trilha de auditoria; concluído é removido/resumido, não mantido inline.
Bifurcação "manter histórico vs. enxugar" resolvida para **enxugar**.

**Camadas a decompor no refinamento (pode virar 1 ou 2 épicos):**
- **Processual** — o cleanup poda `✅` do ROADMAP ativo de forma confiável.
  Toca processo **fora da plataforma**: `docs/process/refinement/epic_completion.md`,
  `docs/process/refinement/planning_guidelines.md` (modelo de estados /
  "Concluído Recentemente") e `skills/cleanup/skill.md`.
- **Plataforma** — enquanto houver `✅` residual, exibir sem inundar a fila
  (`tools/workflow_platform/queue/detect.py` `detect_cleanup_items` dispara
  1 item/épico; rever granularidade ou se `✅` deve gerar item de fila).
  Esta camada é **downstream** da processual: cleanup pontual dissolve a
  maior parte do flooding.

**Suspeita de causa raiz:** o mecanismo de faxina não roda / não cobre tudo
(automação histórica quebrada — cf. W-PROTO-17 / PR #123; fold-in de dispatch
do `workflow.md` §"Faxina como fold-in" não pega ROADMAPs sem dispatch novo).

**Origem:** atrito levantado pelo operador na sessão de refinamento de
2026-06-20 (refino do `PILOTO-WORKFLOW-UX`), ao notar a coluna/itens de
CLEANUP exibindo trabalho já concluído. Capturado como seed em vez de fix
direto no `detect.py` — a raiz é processual, não de exibição.

---

#### ÉPICO W-PILOTO-DISP-1: Dispatch e refino por épico, com predecessor bloqueante

**Milestone:** `PILOTO-WORKFLOW-DISPATCH-EPICO`

**Status:** 🔍 Detalhes definidos

**Objetivo:** tornar dispatch e refino ações **por épico** e introduzir o
**predecessor bloqueante** como gate de acionabilidade. Hoje `detect_dispatch` é
atômico por milestone (exige todos os épicos em 🔍) e `build_dispatch_prompt`
bloqueia se qualquer irmão está em 🏗️/🔀/✅ — o que torna um milestone
parcialmente entregue invisível/impossível de continuar pela plataforma. Depois
deste épico, cada épico 🔍 (dispatch) ou pré-🔍 (refino) é ação própria, e a única
coisa que a suprime é um predecessor declarado ainda não `✅`.

### Conceito: predecessor bloqueante

Campo novo, opcional, no bloco do épico (e, quando fizer sentido, do milestone):

```
**Predecessor bloqueante:** W-PILOTO-UX-1
```

- Aceita 1+ IDs (épico ou milestone), separados por vírgula. Ausente/vazio = sem bloqueio.
- **Satisfeito** quando o predecessor está em `✅` (DONE). Em qualquer outro estado
  (inclusive 🔀 Em revisão — PR aberta mas não mergeada), o dependente está **bloqueado**.
- Uma regra compartilhada (`is_blocked_by_predecessor`) serve dispatch **e** refino.

### Funcionalidades:

#### 1.1 Dado — campo `**Predecessor bloqueante:**` (parser + modelo)
- **Descrição:** o parser lê o campo e popula `Epic.blocking_predecessors: list[str]`.
- **Critérios de Aceite:**
  - Campo ausente → lista vazia; presente → IDs parseados (trim + split por vírgula).
  - Campo desconhecido não gera warning espúrio (paridade com os campos atuais do épico).
  - Registrar os predecessores já existentes na fonte: UX-2, UX-3, UX-4 → `W-PILOTO-UX-1`.

#### 1.2 Detecção por épico + gate de predecessor
- **Descrição:** `detect_dispatch_items` e `detect_refine_items` passam a emitir
  **1 item por épico** e a suprimir os bloqueados.
- **Critérios de Aceite:**
  - `detect_dispatch`: 1 item por épico em 🔍 cujos predecessores estão **todos ✅**.
    Épico 🔍 com predecessor não-✅ **não** gera item. (Substitui a lógica atômica por
    milestone — milestone parcialmente entregue passa a surfaçar as fatias 🔍 restantes.)
  - `detect_refine`: 1 item por épico em 📐/📋 cujos predecessores estão todos ✅;
    bloqueado não gera item.
  - REVIEW / CLEANUP / STALE_BRANCH **não** mudam — não são "começar trabalho em X".

#### 1.3 Prompts por épico
- **Descrição:** `build_dispatch_prompt` e `build_refinement_prompt` operam sobre o épico-alvo.
- **Critérios de Aceite:**
  - Dispatch: prompt `"implementa o épico <ID>"`; predecessor não-✅ → `blocked=True`,
    sem prompt, com motivo ("bloqueado por <ID> — precisa estar ✅").
  - Refino: idem, sobre o épico.
  - O prompt **não** bloqueia mais só porque um irmão do milestone está em 🏗️/🔀/✅.

#### 1.4 Plataforma — Fila oculta, Kanban comunica
- **Descrição:** a Fila deixa de listar o bloqueado; o Kanban o mantém visível **com
  comunicação de bloqueio**.
- **Critérios de Aceite:**
  - **Fila:** épico bloqueado **não** aparece como item de ação.
  - **Kanban:** o card do bloqueado (na coluna 🔍/📐) exibe selo discreto (🔒 +
    "aguardando <ID>") e **permanece clicável**.
  - **Painel de detalhe:** bloqueado → sem botão/prompt de ação; no lugar,
    "🔒 Bloqueado por <ID> (precisa estar ✅)".

### Fora do escopo
- Disparar de dentro da plataforma (headless) — é `PILOTO-WORKFLOW-CANAL-UNICO`.
- Auto-dispatch do que está pronto — é `PILOTO-WORKFLOW-PROATIVIDADE`.
- Grafo de dependências rico / ordenação topológica — só o predecessor bloqueante
  direto ("está ✅ ou não").

---

### ⏳ Fase MVP

> **Milestones:** `MVP-WORKFLOW-DOC` (W-MVP-DOC-1) · `MVP-WORKFLOW-REFINAMENTO` (W-MVP-REF-1..2) · `MVP-WORKFLOW-PROPONENTE` (W-MVP-PROP-1..2).

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
