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
- **Status dos épicos:** W-PROTO-PLAT-1 🔀, W-PROTO-PLAT-2 🔀,
  W-PROTO-PLAT-3 🔀, W-PROTO-PLAT-4 🔀.
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
- **Status dos épicos:** W-PROTO-10 🔍, W-PROTO-11 🔍, W-PROTO-13 🔍,
  W-PROTO-15 🔍, W-PROTO-16 🔍.
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
- **Status dos épicos:** W-PROTO-14 🔍.
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
- **Épicos agrupados:** W-PROTO-FILA-1, W-PROTO-FILA-2, W-PROTO-FILA-3
- **Dependências de core:** nenhuma; depende de
  PROTO-WORKFLOW-PLATAFORMA (kanban e scaffold como base) e
  PROTO-WORKFLOW-FAXINA (faxina documental antes de seguir)
- **Branch associada:** `milestone/proto-workflow-fila`
- **Status dos épicos:** W-PROTO-FILA-1 🔍, W-PROTO-FILA-2 🔍,
  W-PROTO-FILA-3 📐 (refinamento tático em progresso —
  decisões estratégicas abaixo já fechadas).
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
- **Tipos de item (Protótipo):**
  - `DISPATCH` — milestone com todos épicos em 🔍 (apto a dispatch),
    sem épicos em 🏗️/🔀/✅. Ação esperada: copiar prompt de
    dispatch e rodar em sessão autônoma.
  - `REVIEW` — PR de milestone aberta (épicos em 🔀). Ação esperada:
    abrir PR, colar Seção 🎯 no Copilot, decidir merge.
  - `STALE_BRANCH` — branch ativa há mais de 7 dias sem PR aberta e
    sem épico em 🏗️/🔀 referenciando-a. Ação esperada: confirmar
    se é trabalho concluído sem PR (abrir), abandonado (deletar)
    ou bloqueado (resgatar).
- **Nota:** milestone declarado em 2026-04-28 — absorve o conteúdo
  do antigo MVP-WORKFLOW-PLATAFORMA, reposicionado como Protótipo
  porque é fila **reativa** (regra determinística), não curada por
  agente. Curadoria por porta-voz vive no MVP. Refinado a `🔍` em
  2026-04-29 na branch `claude/optimize-dev-workflow-aiYYj` —
  apto ao fluxo autônomo após `PROTO-WORKFLOW-FAXINA` mergear
  (dependência declarada).

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

### Claude Code CLI via OpenWebUI (proxy LiteLLM)

**Status:** 🌱 Visão (parcialmente operacional — texto sim; uso pesado com tool calling depende de modelo maior do que os disponíveis hoje)

**Escopo:** este item é sobre **a CLI do Claude Code rodando contra modelos do OpenWebUI da Atlântico** em vez da API Anthropic. **Não cobre** o uso de OpenWebUI dentro do produto Paper Agent — esse caminho é runtime de produto e está tratado em [`docs/ROADMAP.md`](../../ROADMAP.md) (ÉPICO 2).

**Estado atual:**
- `infra/litellm-proxy/` está montado, traduz Anthropic↔OpenAI e preserva tool calling end-to-end (validado por debug em 2026-04-28).
- Configurado via `.env`: `OPENWEBUI_API_KEY`, `OPENWEBUI_BASE_URL`, `ANTHROPIC_BASE_URL=http://localhost:4000`. `setup-claude-code.ps1` ativa a sessão.
- Pin obrigatório: LiteLLM 1.74.15 (1.83.x quebra em loop no Windows).
- `litellm-config.yaml` precisa de alias explícito por modelo do OpenWebUI (sem alias, LiteLLM strip o prefixo `ollama/` e o backend devolve 400). Aliases pra `ollama/ministral-3:14b` e `ollama/llama3.2:3b` foram adicionados em 2026-04-28 (commit `14bf827`).

**Limitação atual — capacidade do modelo:** com pipeline correto, o `ministral-3:14b` ainda apresenta saídas subótimas no Claude Code: responde conteúdo coerente em prompts triviais ("oi"), mas envelopa o texto em JSON serializado (ex.: `{"message": "Oi! 👋..."}`) em vez de emitir um `content[].text` puro pelo protocolo Anthropic. Hipótese: o modelo de 14B params se confunde tentando imitar formato estruturado quando o system prompt do CC traz 10+ tools (Read, Edit, Bash, Grep, Glob, etc.). Resultado prático: Claude Code via OpenWebUI fica usável pra conversa leve, **não** pra trabalho pesado de Read/Edit/Bash com fidelidade.

**Caminhos de evolução:**

*Caminho 1 — modelo maior no OpenWebUI:* checar com a Atlântico se há modelos 30B+ disponíveis (Llama 3.1 70B, Qwen 2.5 32B+, ou similar). Modelos maiores tipicamente lidam bem com 10+ tools simultâneas e respeitam o protocolo Anthropic nativo. Adotar = adicionar alias no yaml apontando pro novo modelo e re-testar. Sem modelo maior disponível, (B) fica como "best effort" pra texto e o uso pesado continua exigindo Anthropic direto.

*Caminho 2 — trocar a CLI por `opencode`:* [`sst/opencode`](https://github.com/sst/opencode) fala OpenAI-compatible nativamente, sem proxy de tradução. Configuração via `opencode.json` no root com provider custom `@ai-sdk/openai-compatible` ([docs](https://opencode.ai/docs/providers/#custom)). Trade-off contra adoção total: skills atuais em `skills/<nome>/skill.md` não plugam no discovery do opencode (espera `.opencode/skills/<nome>/SKILL.md` em caps com frontmatter `name`/`description`). `CLAUDE.md`/`.claudecode.md`/permissões portam via `AGENTS.md` + `opencode.json` com pouca fricção. Adoção = épico próprio com pacote de migração das skills. Mantém o mesmo trade-off de capacidade do modelo se rodar contra Ollama pequeno.

*Manutenção preventiva:* atualizar LiteLLM pra v1.81.16 herda fixes de tool calling acumulados sem cair na regressão de Prisma/DB de 1.82.x/1.83.x ([#25260](https://github.com/BerriAI/litellm/issues/25260)). Não bloqueador no estado atual.

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

> **Milestones:** `PROTO-WORKFLOW-ENCERRAMENTO` (W-PROTO-5, 6, 7) · `PROTO-WORKFLOW-DOC` (W-PROTO-DOC-1, 2, 3) · `PROTO-WORKFLOW-AJUSTES` (W-PROTO-8, W-PROTO-9) · `PROTO-WORKFLOW-PLATAFORMA` (W-PROTO-PLAT-1..4) · `PROTO-WORKFLOW-FILA` (W-PROTO-FILA-1..3).

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

**Status:** 🔀 Em revisão — PR #106 (https://github.com/gmaiarviana/paper-agent/pull/106)

**Branch:** `claude/implement-workflow-prototype-BtiaJ`

**Dependências:** nenhuma

**Localização:** todo o código vive em `tools/workflow_platform/` — top-level novo, fora de `products/`, coerente com [vision.md](vision.md) ("workflow é processo, não produto"). Stack: Streamlit (já em `requirements.txt`).

### Funcionalidades:

#### 1.1: App Streamlit com configuração, modelo e parser

- **Descrição:** App Streamlit estruturado com arquivo de configuração declarando quais ROADMAPs ler, modelo de dados (Epic, Milestone, EpicState), parser defensivo de ROADMAP markdown e entrypoint que renderiza placeholder do kanban (preenchido em W-PROTO-PLAT-2). Esta funcionalidade entrega o substrato comum consumido pelos épicos seguintes.
- **Critérios de Aceite:**
  1. Deve iniciar com `streamlit run tools/workflow_platform/app.py` a partir do repo raiz sem erros
  2. Deve ler ROADMAPs configurados sem travar se algum estiver ausente ou malformado (registra warning no UI e segue)
  3. Deve ter arquivo de configuração `tools/workflow_platform/config.yaml` declarando lista de ROADMAPs (paths relativos ao repo root) e repo GitHub (`owner/repo`)
  4. Deve expor função `parse_roadmap(path: str) -> ParsedRoadmap` com saída tipada (Epic, Milestone)
  5. Deve funcionar em modo local sem dependência de serviço externo (acesso de leitura ao GitHub é só via URL nos cards, não via API)
  6. Parser deve reconhecer os 8 estados via emoji prefix do campo `**Status:** <emoji> ...` e extrair PR URL do estado `🔀 Em revisão — PR #N (URL)`
- **Detalhes de execução:**
  - **Arquivos a criar:**
    - `tools/__init__.py`
    - `tools/workflow_platform/__init__.py`
    - `tools/workflow_platform/app.py`
    - `tools/workflow_platform/config.yaml`
    - `tools/workflow_platform/config_loader.py`
    - `tools/workflow_platform/models.py`
    - `tools/workflow_platform/parser.py`
    - `tests/tools/__init__.py`
    - `tests/tools/workflow_platform/__init__.py`
    - `tests/tools/workflow_platform/test_parser.py`
    - `tests/tools/workflow_platform/test_config_loader.py`
  - **Arquivos a modificar:** nenhum
  - **Contratos/Shapes:**
    ```python
    # tools/workflow_platform/models.py
    from dataclasses import dataclass, field
    from enum import Enum

    class EpicState(Enum):
        VISION = "🌱"          # 🌱 Visão
        ALIGNED = "🧭"         # 🧭 Jornada alinhada
        SKETCHED = "📐"        # 📐 Funcionalidades esboçadas
        CRITERIA = "📋"        # 📋 Critérios definidos
        DETAILED = "🔍"        # 🔍 Detalhes definidos
        IN_PROGRESS = "🏗️"     # 🏗️ Em andamento
        IN_REVIEW = "🔀"       # 🔀 Em revisão
        DONE = "✅"            # ✅ Implementado

    @dataclass
    class Epic:
        id: str                       # ex: "W-PROTO-PLAT-1"
        title: str                    # ex: "Scaffold da plataforma"
        state: EpicState
        roadmap_path: str             # path do ROADMAP de origem
        milestone_id: str | None      # do campo `**Milestone:** <id>`; None se ausente
        branch: str | None            # do campo `**Branch:** <branch>`; só em 🏗️/🔀
        pr_number: int | None         # extraído de "PR #N" no status; só em 🔀
        pr_url: str | None            # extraído de URL no status; só em 🔀
        raw_status_line: str          # linha original `**Status:** ...` para debug

    @dataclass
    class Milestone:
        id: str                       # ex: "PROTO-WORKFLOW-PLATAFORMA"
        roadmap_path: str
        objective: str | None         # campo `**Objetivo:**` do bloco
        epic_ids: list[str] = field(default_factory=list)

    @dataclass
    class ParsedRoadmap:
        path: str
        epics: list[Epic]
        milestones: list[Milestone]
        warnings: list[str]           # malformações tolerada (status faltando, etc.)
    ```
    ```yaml
    # tools/workflow_platform/config.yaml — default
    github:
      owner: gmaiarviana
      repo: paper-agent
    roadmaps:
      - docs/ROADMAP.md
      - docs/process/workflow/ROADMAP.md
      - products/revelar/ROADMAP.md
      - products/ensaio/ROADMAP.md
      - products/prisma-verbal/ROADMAP.md
      - products/produtor-cientifico/ROADMAP.md
    ```
    ```python
    # tools/workflow_platform/config_loader.py
    @dataclass
    class PlatformConfig:
        github_owner: str
        github_repo: str
        roadmaps: list[str]            # paths absolutos resolvidos a partir do repo root

    def load_config(repo_root: Path | None = None) -> PlatformConfig: ...
    ```
    ```python
    # tools/workflow_platform/parser.py
    def parse_roadmap(path: str) -> ParsedRoadmap: ...
    # Implementação: regex sobre linhas do markdown.
    # Marcadores reconhecidos:
    #   ^#### ÉPICO (?P<id>[A-Z][A-Z0-9-]+): (?P<title>.+)$  ou
    #   ^### ✅ ÉPICO ...                                     ou
    #   ^## ✅ ÉPICO ...                                      (cabeçalhos legados)
    #   ^\*\*Status:\*\* (?P<emoji>🌱|🧭|📐|📋|🔍|🏗️|🔀|✅)
    #   ^\*\*Milestone:\*\* `?(?P<id>[A-Z0-9-]+)`?
    #   ^\*\*Branch:\*\* `?(?P<branch>[^`\n]+)`?
    # Status em 🔀 contém "PR #(?P<n>\d+)" e opcionalmente "(?P<url>https?://[^)]+)".
    # Épico sem **Status:** vira warning e é ignorado.
    # Milestones lidos de "### <ID>" sob "## 🎯 Milestones" se existir; senão lista vazia.
    ```
  - **Integração:** `app.py` carrega config via `load_config()`, itera `config.roadmaps` chamando `parse_roadmap(path)`, agrega `list[ParsedRoadmap]` em `st.session_state` e renderiza placeholder de kanban (preenchido em W-PROTO-PLAT-2). Warnings são exibidos em `st.sidebar.expander("Avisos do parser")`.
  - **Template de referência:** `products/revelar/app/dashboard.py` — entrypoint Streamlit com `st.set_page_config`, sidebar e funções `render_*`. Reusar a mesma estrutura (header, sidebar, área principal); estado em `st.session_state`.
  - **Acoplamentos verificados:**
    - `streamlit>=1.30.0` (já em `requirements.txt`)
    - `pyyaml` (não está em `requirements.txt`) — **adicionar `pyyaml>=6.0` à `requirements.txt`** como sub-tarefa desta funcionalidade
    - **Produto afetado:** nenhum. Top-level novo, isolado de `products/`, `core/` e `skills/`.
    - **ROADMAPs lidos:** mudanças nos ROADMAPs existentes não são feitas por este épico — apenas leitura. Padronização do campo `**Milestone:** <id>` em ROADMAPs de produtos (Revelar, core) fica registrada como observação no fim do milestone e não é dependência (parser tolera ausência).
  - **Dependências de ordem:** primeiro a executar; W-PROTO-PLAT-2/3/4 dependem desta funcionalidade.
  - **Escopo de teste:**
    - **Unit:** `tests/tools/workflow_platform/test_parser.py` — fixture com markdown sintético cobrindo (a) épico em cada um dos 8 estados; (b) status `🔀 Em revisão — PR #93 (https://github.com/gmaiarviana/paper-agent/pull/93)` extrai `pr_number=93` e `pr_url`; (c) épico sem `**Milestone:**` produz `milestone_id=None`; (d) ROADMAP malformado (sem cabeçalho de épico, sem status) gera warning sem exceção; (e) ROADMAP do core (`docs/ROADMAP.md`) não tem seção `## 🎯 Milestones` → `milestones=[]` sem warning. `tests/tools/workflow_platform/test_config_loader.py` — config.yaml válido carrega; campos faltando geram exceção clara.
    - **Validação manual:** `streamlit run tools/workflow_platform/app.py` exibe header, lista os 6 ROADMAPs configurados na sidebar, exibe contagem total de épicos parseados e expander de warnings. Roteiro registrado inline na docstring do `app.py`.

---

#### ÉPICO W-PROTO-PLAT-2: Kanban completo

**Milestone:** `PROTO-WORKFLOW-PLATAFORMA`

**Objetivo:** view com todos os épicos de todos os ROADMAPs configurados organizados por estado e milestone, numa única superfície de leitura.

**Status:** 🔀 Em revisão — PR #106 (https://github.com/gmaiarviana/paper-agent/pull/106)

**Branch:** `claude/implement-workflow-prototype-BtiaJ`

**Dependências:** W-PROTO-PLAT-1 (scaffold com leitura de ROADMAPs)

### Funcionalidades:

#### 2.1: Kanban de estados por milestone

- **Descrição:** Colunas para todos os 8 estados, cards agrupados por milestone dentro de cada coluna, e atualização ao recarregar a página. Card é selecionável (st.button) e dispara as ações contextuais de W-PROTO-PLAT-3/4.
- **Critérios de Aceite:**
  1. Deve exibir todas as 8 colunas na ordem `🌱 → 🧭 → 📐 → 📋 → 🔍 → 🏗️ → 🔀 → ✅`
  2. Deve agrupar cards por milestone dentro de cada coluna; épicos com `milestone_id=None` ficam num grupo final "Sem milestone"
  3. Cada card deve exibir: `id`, `title`, e `milestone_id` (ou "Sem milestone")
  4. Deve consolidar épicos de todos os ROADMAPs configurados numa única view
  5. Deve atualizar ao recarregar a página (live refresh não obrigatório; botão "🔄 Recarregar" na sidebar invalida `st.session_state` e re-parseia)
  6. Deve ser navegável com 20+ épicos ativos sem degradação visual (validação manual com fixture sintética)
  7. Card clicado guarda `selected_epic_id` em `st.session_state` e abre painel de detalhe lateral via `st.expander` ou área inferior (consumido por W-PROTO-PLAT-3/4)
- **Detalhes de execução:**
  - **Arquivos a criar:** `tools/workflow_platform/views/__init__.py`, `tools/workflow_platform/views/kanban.py`
  - **Arquivos a modificar:** `tools/workflow_platform/app.py` — substituir o placeholder pelo `render_kanban()` real
  - **Contratos/Shapes:**
    ```python
    # tools/workflow_platform/views/kanban.py
    KANBAN_COLUMN_ORDER: list[EpicState] = [
        EpicState.VISION, EpicState.ALIGNED, EpicState.SKETCHED,
        EpicState.CRITERIA, EpicState.DETAILED,
        EpicState.IN_PROGRESS, EpicState.IN_REVIEW, EpicState.DONE,
    ]

    def render_kanban(roadmaps: list[ParsedRoadmap]) -> None:
        """Renderiza 8 colunas; em cada coluna, agrupa epics por milestone_id.
        Clique num card grava st.session_state['selected_epic_id'] e
        st.session_state['selected_milestone_id'] (= milestone_id do épico)."""
    ```
  - **Integração:** `app.py` chama `render_kanban(parsed_roadmaps)` na área principal. Após o kanban, se houver `selected_epic_id` em `session_state`, chama `render_card_detail(selected_epic, ...)` (definido em W-PROTO-PLAT-3/4).
  - **Template de referência:** `products/revelar/app/dashboard.py` — uso de `st.columns()` e `st.container()` por bloco; cards visuais via `st.markdown` com leve estilização inline.
  - **Acoplamentos verificados:**
    - `tools/workflow_platform/models.py` (EpicState, Epic, Milestone) — definido em W-PROTO-PLAT-1
    - `tools/workflow_platform/parser.py` (ParsedRoadmap) — definido em W-PROTO-PLAT-1
    - **Produto afetado:** nenhum. View nova, isolada do código de produtos.
  - **Dependências de ordem:** depende de W-PROTO-PLAT-1.1 (parser e models existentes); precede W-PROTO-PLAT-3.1/3.2/4.1/4.2 (que rodam dentro do painel de detalhe acionado pelo card).
  - **Escopo de teste:**
    - **Unit:** sem teste automatizado para a função de render (UI Streamlit). Testar apenas helper de agrupamento se for extraído (ex.: `group_by_milestone(epics: list[Epic]) -> dict[str | None, list[Epic]]` em `tools/workflow_platform/views/kanban.py`) em `tests/tools/workflow_platform/test_kanban.py`.
    - **Validação manual:** roteiro inline na docstring de `render_kanban` — (a) abrir o app com config default; verificar 8 colunas visíveis; (b) verificar que épicos do workflow ROADMAP aparecem agrupados em "PROTO-WORKFLOW-PLATAFORMA"; (c) verificar que épicos do Revelar (sem campo `**Milestone:**`) aparecem em "Sem milestone"; (d) carregar fixture com 25 épicos sintéticos e confirmar layout legível.

---

#### ÉPICO W-PROTO-PLAT-3: Ações de implementação

**Milestone:** `PROTO-WORKFLOW-PLATAFORMA`

**Objetivo:** ações contextuais nos cards de estados de execução (🔍/🏗️/🔀/✅) para o operador despachar, acompanhar e revisar sem precisar sair da plataforma.

**Status:** 🔀 Em revisão — PR #106 (https://github.com/gmaiarviana/paper-agent/pull/106)

**Branch:** `claude/implement-workflow-prototype-BtiaJ`

**Dependências:** W-PROTO-PLAT-2 (kanban com cards clicáveis)

### Funcionalidades:

#### 3.1: Dispatch (sempre por milestone) para épicos em 🔍

- **Descrição:** Ao selecionar um card em `🔍`, o painel de detalhe gera prompt de dispatch clipboard-ready do **milestone-pai** do épico (não do épico individual). Coerente com [`dispatch.md`](../autonomous/dispatch.md), que opera sempre sobre milestone inteiro. Se o milestone do épico tem outros épicos em estados pré-`🔍` (`🌱`/`🧭`/`📐`/`📋`), o prompt vem com aviso "PM skill será disparada para refinar X, Y antes de EM"; se algum estiver em `🏗️`/`🔀`/`✅`, exibe alerta "milestone em execução/concluído — dispatch não recomendado" e desabilita o botão.
- **Critérios de Aceite:**
  1. Deve exibir prompt de dispatch clipboard-ready ao selecionar épico em `🔍`
  2. O prompt deve referenciar o `milestone_id` (não o `epic.id`) e usar linguagem natural conforme [`dispatch.md`](../autonomous/dispatch.md) §1 (ex.: ``"implementa o `<MILESTONE_ID>`"``)
  3. Se algum épico do mesmo milestone está em `🌱`/`🧭`/`📐`/`📋`, listar esses ids no prompt como "PM skill refinará: <ids>"
  4. Se algum épico do mesmo milestone está em `🏗️`/`🔀`/`✅`, exibir alerta visual e desabilitar botão de copy
  5. Se o épico tem `milestone_id=None`, exibir mensagem "épico sem milestone declarado — não pode ser despachado"; sem prompt
  6. Deve ter botão "📋 Copiar prompt" usando `st.code(...)` ou componente equivalente que permita seleção/cópia
- **Detalhes de execução:**
  - **Arquivos a criar:** `tools/workflow_platform/prompts/__init__.py`, `tools/workflow_platform/prompts/dispatch.py`, `tools/workflow_platform/views/card_detail.py`, `tests/tools/workflow_platform/test_dispatch_prompt.py`
  - **Arquivos a modificar:** `tools/workflow_platform/app.py` — invocar `render_card_detail(selected_epic, all_epics, config)` após o kanban
  - **Contratos/Shapes:**
    ```python
    # tools/workflow_platform/prompts/dispatch.py
    @dataclass
    class DispatchPromptResult:
        prompt_text: str | None        # None se milestone_id ausente ou em execução
        warnings: list[str]            # ex.: "milestone tem épicos em 📋: W-PROTO-PLAT-2"
        blocked: bool                  # True se há épico em 🏗️/🔀/✅ no milestone

    def build_dispatch_prompt(
        epic: Epic,
        all_epics_in_milestone: list[Epic],
    ) -> DispatchPromptResult: ...
    ```
    Exemplo de prompt produzido para `epic.milestone_id="PROTO-WORKFLOW-PLATAFORMA"` com todos em `🔍`:
    ```
    implementa o PROTO-WORKFLOW-PLATAFORMA
    ```
    Com épicos em `📋`:
    ```
    implementa o PROTO-WORKFLOW-PLATAFORMA

    Nota: PM skill refinará os épicos abaixo (📋 → 🔍) antes da EM rodar:
    - W-PROTO-PLAT-3
    ```
  - **Integração:** `views/card_detail.py` chama `build_dispatch_prompt()` quando `selected_epic.state == EpicState.DETAILED`. Filtra `all_epics_in_milestone = [e for e in epics if e.milestone_id == selected_epic.milestone_id]`.
  - **Template de referência:** sem análogo direto. Estrutura similar a um helper puro: input dataclass → output dataclass com warnings, sem side effects (espelha `tools/` puro).
  - **Acoplamentos verificados:**
    - `tools/workflow_platform/models.py` (Epic, EpicState) — W-PROTO-PLAT-1
    - `docs/process/autonomous/dispatch.md` — formato textual `"implementa o <ID>"` é cópia direta dos exemplos do dispatch.md
    - **Produto afetado:** nenhum
  - **Dependências de ordem:** depende de W-PROTO-PLAT-2.1 (kanban com card clicável). 3.1 e 3.2 podem ser implementadas em paralelo (ambas vivem em `views/card_detail.py`).
  - **Escopo de teste:**
    - **Unit:** `test_dispatch_prompt.py` — (a) milestone com todos em `🔍` produz prompt simples sem aviso e `blocked=False`; (b) milestone com 1 épico em `📋` adiciona seção "PM skill refinará"; (c) milestone com 1 épico em `🏗️` retorna `blocked=True`; (d) `milestone_id=None` retorna `prompt_text=None` com warning.
    - **Validação manual:** clicar em card de épico em `🔍` no app rodando; verificar prompt clipboard-ready coerente com `dispatch.md`.

#### 3.2: Status e links para 🏗️, 🔀 e ✅

- **Descrição:** Painel de detalhe exibe links de acompanhamento conforme estado: `🏗️` → branch no GitHub; `🔀` → PR no GitHub; `✅` → resumo enxuto do épico (texto pós-cleanup do ROADMAP) sem ações.
- **Critérios de Aceite:**
  1. Para `🏗️`: exibe `epic.branch` como link `https://github.com/<owner>/<repo>/tree/<branch>` (owner/repo do `config.yaml`)
  2. Para `🔀`: exibe link para `epic.pr_url` (se parseado), ou monta `https://github.com/<owner>/<repo>/pull/<epic.pr_number>` se só `pr_number` estiver disponível
  3. Para `✅`: exibe título e resumo (corpo do bloco do épico no ROADMAP, primeiros 500 chars) sem botões de ação
  4. Se `epic.branch=None` em `🏗️`: exibe aviso "branch não declarada no ROADMAP — verifique campo `**Branch:**`" sem quebrar
  5. Se `epic.pr_url=None` e `epic.pr_number=None` em `🔀`: exibe aviso análogo
- **Detalhes de execução:**
  - **Arquivos a criar:** já cobertos por 3.1 (`tools/workflow_platform/views/card_detail.py`)
  - **Arquivos a modificar:** `tools/workflow_platform/views/card_detail.py` — adicionar branches por estado dentro do mesmo `render_card_detail`. `tools/workflow_platform/parser.py` — estender para guardar `body_excerpt: str` em `Epic` (primeiros 500 chars do bloco do épico) usado pelo branch `✅`.
  - **Contratos/Shapes:**
    ```python
    # extensão em models.py
    @dataclass
    class Epic:
        # ... campos definidos em W-PROTO-PLAT-1.1
        body_excerpt: str = ""        # primeiros ~500 chars do bloco; usado em ✅
    ```
    ```python
    # tools/workflow_platform/views/card_detail.py
    def render_card_detail(
        epic: Epic,
        all_epics_in_milestone: list[Epic],
        config: PlatformConfig,
    ) -> None:
        """Roteia por epic.state. Estados pré-execução chamam W-PROTO-PLAT-4.x;
        🔍 chama build_dispatch_prompt + botão copy; 🏗️/🔀/✅ rendem links/resumo."""
    ```
    Helper puro para construir URLs:
    ```python
    def github_branch_url(owner: str, repo: str, branch: str) -> str:
        return f"https://github.com/{owner}/{repo}/tree/{branch}"

    def github_pr_url(owner: str, repo: str, pr_number: int) -> str:
        return f"https://github.com/{owner}/{repo}/pull/{pr_number}"
    ```
  - **Integração:** `card_detail.render_card_detail` é o único ponto de entrada do painel; faz dispatch interno por `epic.state`. URLs construídas a partir de `config.github_owner` e `config.github_repo`.
  - **Template de referência:** uso de `st.link_button` ou `st.markdown` com link clicável (padrão Streamlit; ver `products/revelar/app/dashboard.py`).
  - **Acoplamentos verificados:**
    - `tools/workflow_platform/models.py` e `config_loader.py` — W-PROTO-PLAT-1
    - **Mudança no parser:** adicionar `body_excerpt` é extensão, não breaking change — testes do parser de 1.1 continuam passando, novo teste cobre o campo
    - **Produto afetado:** nenhum
  - **Dependências de ordem:** depende de W-PROTO-PLAT-2.1 e da parte do parser de W-PROTO-PLAT-1.1. A extensão de `body_excerpt` é dependência interna desta funcionalidade.
  - **Escopo de teste:**
    - **Unit:** `test_parser.py` (extensão) — `body_excerpt` capturado para épico em `✅`. Helpers `github_branch_url`/`github_pr_url` testados via fixture.
    - **Validação manual:** rodar app; clicar em épico real em `🔀` (qualquer dos PROTO-WORKFLOW-* já mergeados); confirmar link da PR abre o GitHub.

---

#### ÉPICO W-PROTO-PLAT-4: Direcionamento de refinamento

**Milestone:** `PROTO-WORKFLOW-PLATAFORMA`

**Objetivo:** ações contextuais nos cards de estados pré-execução (🌱/🧭/📐/📋) que orientam o operador sobre o próximo passo de refinamento e geram o prompt de sessão pronto para usar.

**Status:** 🔀 Em revisão — PR #106 (https://github.com/gmaiarviana/paper-agent/pull/106)

**Branch:** `claude/implement-workflow-prototype-BtiaJ`

**Dependências:** W-PROTO-PLAT-2 (kanban com cards clicáveis)

### Funcionalidades:

#### 4.1: Exibição de próximo passo por estado

- **Descrição:** Ao selecionar um card em estado pré-execução, o painel de detalhe exibe o próximo estado-alvo do épico e qual fluxo de refinamento se aplica, com base no mapa fixo de transições de [`planning_guidelines.md`](../refinement/planning_guidelines.md).
- **Critérios de Aceite:**
  1. Para `🌱`: exibe "Próximo alvo: `🧭 Jornada alinhada` ou `📐 Funcionalidades esboçadas`. Refinamento via PM skill (no fluxo autônomo) ou sessão estratégica."
  2. Para `🧭`: exibe "Próximo alvo: `📐 Funcionalidades esboçadas` ou `📋 Critérios definidos`. Refinamento via PM skill ou sessão estratégica."
  3. Para `📐`: exibe "Próximo alvo: `📋 Critérios definidos`. Refinamento via PM skill ou sessão estratégica."
  4. Para `📋`: exibe "Próximo alvo: `🔍 Detalhes definidos` (apto ao fluxo autônomo). Checklist do alvo: [`autonomous_readiness.md`](../refinement/autonomous_readiness.md)."
  5. Não deve listar arquivos para upload manual — refinamento é delegado à PM skill ou sessão estratégica via plataforma
  6. Texto de cada estado deve apontar via link para o ponto correspondente em `planning_guidelines.md`
- **Detalhes de execução:**
  - **Arquivos a criar:** `tools/workflow_platform/prompts/refinement.py` (compartilhado com 4.2 — define o mapa de transições + builder do prompt), `tests/tools/workflow_platform/test_refinement_prompt.py`
  - **Arquivos a modificar:** `tools/workflow_platform/views/card_detail.py` — adicionar branch por estado pré-execução (`🌱`/`🧭`/`📐`/`📋`)
  - **Contratos/Shapes:**
    ```python
    # tools/workflow_platform/prompts/refinement.py
    @dataclass
    class NextStepInfo:
        target_states: list[EpicState]    # ex.: [SKETCHED, CRITERIA] para 🧭
        guidance_text: str                # texto curto exibido no painel
        readiness_checklist: bool         # True para 📋 (aponta autonomous_readiness.md)

    NEXT_STEP_MAP: dict[EpicState, NextStepInfo] = {
        EpicState.VISION:    NextStepInfo(target_states=[EpicState.ALIGNED, EpicState.SKETCHED], ...),
        EpicState.ALIGNED:   NextStepInfo(target_states=[EpicState.SKETCHED, EpicState.CRITERIA], ...),
        EpicState.SKETCHED:  NextStepInfo(target_states=[EpicState.CRITERIA], ...),
        EpicState.CRITERIA:  NextStepInfo(target_states=[EpicState.DETAILED], readiness_checklist=True, ...),
    }

    def get_next_step(epic: Epic) -> NextStepInfo | None:
        """Retorna NextStepInfo para estados pré-execução; None caso contrário."""
    ```
  - **Integração:** `views/card_detail.py` chama `get_next_step(epic)` quando o estado está em `{🌱, 🧭, 📐, 📋}`; renderiza `guidance_text` e link condicional para `autonomous_readiness.md`.
  - **Template de referência:** sem análogo direto. Padrão "estado → info" via dict imutável é convencional.
  - **Acoplamentos verificados:**
    - `tools/workflow_platform/models.py` (Epic, EpicState) — W-PROTO-PLAT-1
    - `docs/process/refinement/planning_guidelines.md` — fonte canônica das transições; mudanças no mapa de estados exigem atualização aqui (registrar como nota inline em `refinement.py`)
    - **Produto afetado:** nenhum
  - **Dependências de ordem:** 4.1 e 4.2 dividem `prompts/refinement.py`; 4.1 entrega `NEXT_STEP_MAP` + `get_next_step`, 4.2 reusa para gerar prompt. Implementar 4.1 primeiro.
  - **Escopo de teste:**
    - **Unit:** `test_refinement_prompt.py` — (a) `get_next_step(epic_em_📋)` retorna `target_states=[DETAILED]` e `readiness_checklist=True`; (b) `get_next_step(epic_em_🏗️)` retorna `None`; (c) `NEXT_STEP_MAP` cobre os 4 estados pré-execução.
    - **Validação manual:** clicar em épicos em cada um dos 4 estados pré-execução no app; verificar texto e link.

#### 4.2: Geração de prompt de refinamento clipboard-ready

- **Descrição:** Gera prompt de refinamento com o contexto mínimo para o operador abrir uma sessão de refinamento (estratégica ou via PM skill em Claude Code Web). Inclui `epic.id`, estado atual, alvo, `roadmap_path` e ponteiros para os documentos canônicos. **Não executa o refinamento** — só monta o texto.
- **Critérios de Aceite:**
  1. Deve gerar prompt incluindo: `epic.id`, `epic.title`, `epic.state.name`, alvo (`NextStepInfo.target_states`), `epic.roadmap_path` e ponteiros para `planning_guidelines.md` e `starter.md`
  2. Para épico em `📋`: prompt cita explicitamente `autonomous_readiness.md` como checklist do alvo `🔍`
  3. Deve ter botão "📋 Copiar prompt" via `st.code(...)` (mesmo padrão de 3.1)
  4. Não executa refinamento — apenas prepara o contexto
  5. Para épicos em estados de execução (`🔍`/`🏗️`/`🔀`/`✅`): função retorna `None` e a UI não exibe o painel de refinamento
- **Detalhes de execução:**
  - **Arquivos a criar:** já cobertos por 4.1 (`tools/workflow_platform/prompts/refinement.py`, `tests/.../test_refinement_prompt.py`)
  - **Arquivos a modificar:** `tools/workflow_platform/prompts/refinement.py` — adicionar `build_refinement_prompt`. `tools/workflow_platform/views/card_detail.py` — exibir prompt + botão copy nos estados pré-execução.
  - **Contratos/Shapes:**
    ```python
    # tools/workflow_platform/prompts/refinement.py
    def build_refinement_prompt(epic: Epic) -> str | None:
        """Retorna prompt textual; None para estados de execução.
        Template fixo, sem invocação de LLM."""
    ```
    Exemplo de prompt produzido para `epic.id="W-PROTO-PLAT-1"`, `state=📋`:
    ```
    Refinar o épico W-PROTO-PLAT-1 ("Scaffold da plataforma") até 🔍 Detalhes definidos.

    Estado atual: 📋 Critérios definidos
    Alvo: 🔍 Detalhes definidos
    ROADMAP de origem: docs/process/workflow/ROADMAP.md

    Aplicar checklist em docs/process/refinement/autonomous_readiness.md.
    Convenções da sessão em docs/process/refinement/planning_guidelines.md.
    Pack inicial de contexto em docs/process/refinement/starter.md.
    ```
  - **Integração:** `views/card_detail.py` chama `build_refinement_prompt(epic)` quando `get_next_step(epic) is not None`. Exibe via `st.code()` com botão de copy no canto superior direito (padrão Streamlit).
  - **Template de referência:** `tools/workflow_platform/prompts/dispatch.py` (W-PROTO-PLAT-3.1) — mesma estrutura de helper puro retornando texto.
  - **Acoplamentos verificados:**
    - `tools/workflow_platform/models.py` e `prompts/refinement.NEXT_STEP_MAP` — definidos em W-PROTO-PLAT-1 e 4.1
    - Paths `planning_guidelines.md`, `autonomous_readiness.md`, `starter.md` — caminhos relativos fixos no template; mudança nesses caminhos quebra prompts (registrar como nota inline)
    - **Produto afetado:** nenhum
  - **Dependências de ordem:** depende de 4.1 (`NEXT_STEP_MAP`)
  - **Escopo de teste:**
    - **Unit:** `test_refinement_prompt.py` (extensão) — (a) prompt para épico em `📋` contém "autonomous_readiness.md"; (b) prompt para épico em `🌱` não menciona `autonomous_readiness.md`; (c) `build_refinement_prompt(epic_em_🏗️)` retorna `None`; (d) prompt contém `epic.id`, `epic.title` e `roadmap_path`.
    - **Validação manual:** clicar em épicos em cada estado pré-execução no app; copiar o prompt; colar em editor e conferir conteúdo.

---

#### ÉPICO W-PROTO-FILA-1: Detecção reativa de eventos e shape de item

**Milestone:** `PROTO-WORKFLOW-FILA`

**Objetivo:** módulo de detecção lê estado-do-mundo (ROADMAPs parseados + branches do remote) e produz lista determinística de itens de fila por regra fixa. Sem persistência própria — fila é função pura do estado. Cobre 3 tipos no Protótipo: DISPATCH (milestone apto), REVIEW (PR aberta), STALE_BRANCH (branch parada).

**Status:** 🔍 Detalhes definidos

**Dependências:** W-PROTO-PLAT-1 (parser de ROADMAP + `Epic`/`Milestone`/`ParsedRoadmap`); decisões estratégicas no bloco do milestone PROTO-WORKFLOW-FILA (3 tipos de item, fonte determinística).

### Termos e contratos

- **Item de fila:** entrada tipada produzida pela detecção; carrega ponteiro tipado pra origem (`SourcePointer`) e instruções de ação esperada para o operador.
- **Estado-do-mundo:** união de (a) `list[ParsedRoadmap]` carregada pelo scaffold + (b) lista de branches do remote com timestamp do último commit (via `git for-each-ref` em refs `refs/remotes/origin/`).
- **Detecção determinística:** função pura `state → list[QueueItem]`, sem efeitos colaterais nem leitura de relógio (a não ser para `detected_at`, que é parte da entrada lógica e não da função).

### Funcionalidades:

#### 1.1: Shape mínimo de item de fila

- **Descrição:** Define `QueueItem`, `ItemType` e `SourcePointer` (tagged union). `QueueItem` carrega título, contexto curto, ação esperada, ponteiro tipado e timestamp. Shape único pra os 3 tipos do Protótipo, com ponteiro discriminado por tipo.
- **Critérios de Aceite:**
  1. Deve definir `ItemType` enum com os 3 valores: `DISPATCH`, `REVIEW`, `STALE_BRANCH`
  2. Deve definir `QueueItem` dataclass com campos `id`, `type`, `title`, `context`, `expected_action`, `source_pointer`, `detected_at`
  3. `id` deve ser estável e derivado do gatilho (ex.: `"dispatch:PROTO-WORKFLOW-FAXINA"`, `"review:pr-93"`, `"stale:claude/foo-bar"`) — duas chamadas de detecção sobre o mesmo estado produzem mesmo `id`
  4. `source_pointer` deve ser tagged union (`EpicPointer` | `PRPointer` | `BranchPointer`) com tipo coerente com `ItemType` (DISPATCH→`EpicPointer`, REVIEW→`PRPointer`, STALE_BRANCH→`BranchPointer`)
  5. Tentar instanciar `QueueItem(type=DISPATCH, source_pointer=BranchPointer(...))` deve falhar via runtime check em `__post_init__` ou validação pydantic-style (não silenciar inconsistência)
- **Detalhes de execução:**
  - **Arquivos a criar:** `tools/workflow_platform/queue/__init__.py`, `tools/workflow_platform/queue/models.py`, `tests/tools/workflow_platform/test_queue_models.py`
  - **Arquivos a modificar:** nenhum
  - **Contratos/Shapes:**
    ```python
    # tools/workflow_platform/queue/models.py
    from dataclasses import dataclass
    from datetime import datetime
    from enum import Enum

    class ItemType(Enum):
        DISPATCH = "dispatch"
        REVIEW = "review"
        STALE_BRANCH = "stale_branch"

    @dataclass(frozen=True)
    class EpicPointer:
        milestone_id: str
        roadmap_path: str
        epic_ids: list[str]            # todos os épicos do milestone (DISPATCH é por milestone)

    @dataclass(frozen=True)
    class PRPointer:
        pr_number: int
        pr_url: str
        milestone_id: str | None       # se identificável; senão None

    @dataclass(frozen=True)
    class BranchPointer:
        branch_name: str
        last_commit_at: datetime
        days_stale: int

    SourcePointer = EpicPointer | PRPointer | BranchPointer

    @dataclass(frozen=True)
    class QueueItem:
        id: str
        type: ItemType
        title: str
        context: str
        expected_action: str
        source_pointer: SourcePointer
        detected_at: datetime

        def __post_init__(self) -> None:
            expected = {
                ItemType.DISPATCH: EpicPointer,
                ItemType.REVIEW: PRPointer,
                ItemType.STALE_BRANCH: BranchPointer,
            }[self.type]
            if not isinstance(self.source_pointer, expected):
                raise TypeError(f"{self.type} expects {expected.__name__}")
    ```
  - **Integração:** módulo puro de modelos. Consumido por `queue/detect.py` (1.2) e `views/queue.py` (W-PROTO-FILA-2).
  - **Template de referência:** `tools/workflow_platform/models.py` (`Epic`, `Milestone`, `ParsedRoadmap` em W-PROTO-PLAT-1) — mesmo padrão de dataclasses imutáveis.
  - **Acoplamentos verificados:**
    - Stdlib only (`dataclasses`, `datetime`, `enum`); sem deps novas.
    - **Produto afetado:** nenhum.
  - **Dependências de ordem:** primeiro do épico; precede 1.2 e 1.3.
  - **Escopo de teste:**
    - **Unit:** `test_queue_models.py` — (a) `QueueItem(type=DISPATCH, source_pointer=EpicPointer(...))` instancia; (b) `QueueItem(type=DISPATCH, source_pointer=BranchPointer(...))` levanta `TypeError`; (c) dois `QueueItem` com mesmo `id`+campos são iguais (frozen+`@dataclass(eq=True)` default).

#### 1.2: Detecção dos 3 tipos a partir do estado-do-mundo

- **Descrição:** módulo `queue/detect.py` expõe função `detect_all_items(state) -> list[QueueItem]` que internamente chama `detect_dispatch_items`, `detect_review_items` e `detect_stale_branch_items`. Cada detector é função pura sobre o input. Lista de branches do remote vem via helper que encapsula `git for-each-ref`.
- **Critérios de Aceite:**
  1. `detect_dispatch_items(roadmaps)` deve gerar 1 item por milestone com **todos** os épicos em `🔍` e nenhum em `🏗️`/`🔀`/`✅`; milestones sem milestone_id ou com pelo menos 1 épico em estado de execução não geram item
  2. `detect_review_items(roadmaps)` deve gerar 1 item por PR número-distinto encontrado no estado `🔀` dos épicos; agrupa épicos do mesmo `pr_number` num só item (lista de `epic_ids` no contexto)
  3. `detect_stale_branch_items(branches, threshold_days=7)` deve gerar item para cada branch do remote com `last_commit_at` há > `threshold_days`, **excluindo** branches referenciadas por algum épico em `🏗️`/`🔀` (campo `**Branch:**`) e excluindo `main`
  4. `detect_all_items(state)` deve retornar união ordenada por `detected_at` desc, depois `type` (DISPATCH primeiro, depois REVIEW, depois STALE_BRANCH); se múltiplos itens têm mesmo `detected_at`, ordem por `id` lexicográfico
  5. Função helper `list_remote_branches() -> list[RemoteBranch]` deve usar `subprocess.run(["git", "for-each-ref", "--format=%(refname:short)|%(committerdate:iso8601)", "refs/remotes/origin/"])` e parsear `(name, last_commit_at)`; falhas de subprocess são propagadas (não silenciadas)
  6. `detect_all_items` deve ser **idempotente sobre estado fixo:** chamar com mesmo `state` produz lista igual em conteúdo (ignorando `detected_at` que recebe `now()` da chamada — ver 1.3 para fix de determinismo total)
- **Detalhes de execução:**
  - **Arquivos a criar:** `tools/workflow_platform/queue/detect.py`, `tools/workflow_platform/queue/git_helper.py`, `tests/tools/workflow_platform/test_queue_detect.py`
  - **Arquivos a modificar:** nenhum
  - **Contratos/Shapes:**
    ```python
    # tools/workflow_platform/queue/git_helper.py
    @dataclass(frozen=True)
    class RemoteBranch:
        name: str                      # ex.: "claude/foo-bar" (sem prefixo "origin/")
        last_commit_at: datetime

    def list_remote_branches() -> list[RemoteBranch]:
        """git for-each-ref --format=%(refname:short)|%(committerdate:iso8601) refs/remotes/origin/"""

    # tools/workflow_platform/queue/detect.py
    @dataclass(frozen=True)
    class WorldState:
        roadmaps: list[ParsedRoadmap]
        remote_branches: list[RemoteBranch]
        now: datetime                  # injetado para determinismo (ver 1.3)

    def detect_dispatch_items(state: WorldState) -> list[QueueItem]: ...
    def detect_review_items(state: WorldState) -> list[QueueItem]: ...
    def detect_stale_branch_items(state: WorldState, threshold_days: int = 7) -> list[QueueItem]: ...
    def detect_all_items(state: WorldState, threshold_days: int = 7) -> list[QueueItem]: ...
    ```
  - **Integração:** o caller (`views/queue.py` em W-PROTO-FILA-2) constrói `WorldState` agregando `parsed_roadmaps` (já em `st.session_state` via PLAT-1) + `list_remote_branches()` + `datetime.now()`. Chama `detect_all_items(state)`. Sem cache; reconstrução por render é o método primário.
  - **Template de referência:** `tools/workflow_platform/prompts/dispatch.py` (W-PROTO-PLAT-3.1) — mesmo padrão "input dataclass → output tipado, sem side effect".
  - **Acoplamentos verificados:**
    - `tools/workflow_platform/models.py` (Epic, EpicState, ParsedRoadmap) — W-PROTO-PLAT-1.
    - `tools/workflow_platform/queue/models.py` (QueueItem etc.) — FILA-1.1.
    - `subprocess` (stdlib) para `git for-each-ref`; sem deps externas novas.
    - **`git fetch` é responsabilidade do caller**, não do detector. View (FILA-2.1) chama `git fetch origin --prune` antes de instanciar `WorldState`. Detector lê o que está no remote local.
    - **Produto afetado:** nenhum.
  - **Dependências de ordem:** depende de 1.1; precede 1.3.
  - **Escopo de teste:**
    - **Unit:** `test_queue_detect.py` — (a) milestone com todos `🔍` gera 1 DISPATCH com `EpicPointer.epic_ids` populado; (b) milestone com 1 épico em `🏗️` não gera DISPATCH; (c) 2 épicos do mesmo milestone em `🔀` com mesmo `pr_number=93` geram **1** REVIEW (não 2); (d) branch com `last_commit_at` há 10 dias gera STALE; branch com 3 dias não gera; (e) branch referenciada por épico em `🏗️` é excluída de STALE; (f) `main` é sempre excluída; (g) ordenação: DISPATCH antes de REVIEW antes de STALE quando `detected_at` é igual.
    - **Integration:** sem teste de integração; helper `list_remote_branches` é mockável via `monkeypatch.setattr(subprocess, "run", ...)`.

#### 1.3: Garantia de determinismo via fixture-snapshot

- **Descrição:** teste explícito do invariante "detect_all_items é função pura do estado". Fixture com `WorldState` fixo (ROADMAPs sintéticos + branches mockadas + `now` cravado) é passada duas vezes ao detector; resultado precisa ser idêntico item-a-item. Materializa o princípio "markdown é fonte da verdade".
- **Critérios de Aceite:**
  1. Fixture `make_world_state_fixture()` em `tests/tools/workflow_platform/fixtures/world_state.py` retorna `WorldState` com pelo menos: 2 ROADMAPs sintéticos (1 com milestone apto a DISPATCH, 1 com épicos em `🔀` pareados a PR), 4 branches mockadas (2 stale, 1 ativa, 1 referenciada por épico em `🏗️`), `now` fixo (`datetime(2026, 4, 29, 12, 0, 0)`)
  2. Teste `test_detect_is_deterministic` chama `detect_all_items(state)` duas vezes consecutivas e afirma `result_a == result_b` (campos completos, incluindo `detected_at`)
  3. Teste `test_detect_snapshot` compara saída com snapshot esperado serializado (lista de `QueueItem` com 3 itens: 1 DISPATCH, 1 REVIEW, 1 STALE_BRANCH); snapshot vive em `tests/tools/workflow_platform/fixtures/expected_queue_snapshot.json`
  4. Mudança no código de detecção que altera shape ou regra deve quebrar `test_detect_snapshot` — atualizar snapshot é decisão consciente, não acidental
- **Detalhes de execução:**
  - **Arquivos a criar:** `tests/tools/workflow_platform/fixtures/__init__.py`, `tests/tools/workflow_platform/fixtures/world_state.py`, `tests/tools/workflow_platform/fixtures/expected_queue_snapshot.json`, `tests/tools/workflow_platform/test_queue_determinism.py`
  - **Arquivos a modificar:** nenhum
  - **Contratos/Shapes:**
    ```python
    # tests/tools/workflow_platform/fixtures/world_state.py
    def make_world_state_fixture() -> WorldState: ...

    # tests/tools/workflow_platform/test_queue_determinism.py
    def test_detect_is_deterministic():
        state = make_world_state_fixture()
        assert detect_all_items(state) == detect_all_items(state)

    def test_detect_snapshot():
        state = make_world_state_fixture()
        actual = [_serialize(item) for item in detect_all_items(state)]
        expected = json.loads(SNAPSHOT_PATH.read_text())
        assert actual == expected
    ```
  - **Integração:** teste-only. Snapshot é commitado no repo; atualização exige rodar script `python -m tests.tools.workflow_platform.fixtures.regenerate_snapshot` (helper documentado inline no teste).
  - **Template de referência:** snapshot testing convencional; sem dep de `pytest-snapshot` ou `syrupy` — usar `json.dumps(..., sort_keys=True, indent=2)` direto pra evitar dep nova.
  - **Acoplamentos verificados:**
    - `tools/workflow_platform/queue/detect.py` e `models.py` — FILA-1.1, 1.2.
    - **Produto afetado:** nenhum.
  - **Dependências de ordem:** depende de 1.1 e 1.2.
  - **Escopo de teste:**
    - **Unit:** os próprios testes desta funcionalidade.
    - **Validação manual:** rodar `pytest tests/tools/workflow_platform/test_queue_determinism.py -v` localmente; ambos testes passam.

**Fora do escopo:**
- Ordenação avançada (importância, urgência) — Protótipo é só `detected_at` desc + tipo.
- Persistência de "claim do operador" (mexeu num épico, agente solta) — escopo MVP.
- Tipos de item adicionais (escalação, proposta do proponente) — chegam no MVP.

---

#### ÉPICO W-PROTO-FILA-2: Exibição da fila + prompt focado por item

**Milestone:** `PROTO-WORKFLOW-FILA`

**Objetivo:** plataforma ganha tab "📋 Fila" (default ao abrir o app) que renderiza os `QueueItem`s detectados em FILA-1 como cards clicáveis. Clicar num item abre painel de detalhe com prompt clipboard-ready específico do tipo, reusando os builders de prompt de PLAT-3.1 (DISPATCH) e adicionando builders novos para REVIEW e STALE_BRANCH. **Sem chat embutido** — o "chat focado" do Protótipo é prompt pronto + instrução de colar em sessão autônoma; chat real é MVP.

**Status:** 🔍 Detalhes definidos

**Dependências:** W-PROTO-FILA-1 (modelos e detecção); W-PROTO-PLAT-2.1 (estrutura de tabs / sidebar do app); W-PROTO-PLAT-3.1 (`build_dispatch_prompt` reusado).

### Funcionalidades:

#### 2.1: View da fila como tab default

- **Descrição:** `app.py` ganha layout de tabs `st.tabs(["📋 Fila", "🗂️ Kanban"])` — fila default. View da fila chama `detect_all_items(state)` a cada render, agrupa visualmente por tipo (DISPATCH primeiro, REVIEW depois, STALE_BRANCH por último), e renderiza cards. Botão "🔄 Recarregar fila" na sidebar invalida `st.session_state.queue_world_state` e força re-detecção (incluindo `git fetch origin --prune`).
- **Critérios de Aceite:**
  1. App abre com tab "📋 Fila" ativa por default; tab "🗂️ Kanban" continua acessível em segundo plano com renderização inalterada
  2. Cada card exibe: emoji do tipo (`📤` DISPATCH / `🔀` REVIEW / `🌱` STALE_BRANCH), `title`, `context` (1-2 linhas), `expected_action` (em destaque)
  3. Cards são clicáveis (`st.button` com chave única `f"queue_card_{item.id}"`); clique grava `st.session_state["selected_queue_item_id"]` e abre painel de detalhe inline (expander ou área inferior, espelhando padrão do kanban em PLAT-2)
  4. Cards são agrupados visualmente por `ItemType` com cabeçalho de seção (`st.subheader("📤 Dispatch (N)")`); cada cabeçalho mostra contagem do tipo
  5. Botão "🔄 Recarregar fila" na sidebar limpa `st.session_state.queue_world_state` e re-instancia `WorldState` (incluindo subprocess `git fetch origin --prune`); falha de fetch é exibida em `st.warning` mas não impede renderização (usa state local)
  6. Fila vazia exibe placeholder amigável: "Sem itens na fila — nada esperando ação no momento."
- **Detalhes de execução:**
  - **Arquivos a criar:** `tools/workflow_platform/views/queue.py`, `tests/tools/workflow_platform/test_queue_view.py` (apenas helpers puros — render Streamlit não é testado direto, igual W-PROTO-PLAT-2)
  - **Arquivos a modificar:** `tools/workflow_platform/app.py` — substituir chamada direta a `render_kanban` pelo bloco de tabs; adicionar botão de recarga na sidebar; gerenciar `st.session_state.queue_world_state` (lazy load).
  - **Contratos/Shapes:**
    ```python
    # tools/workflow_platform/views/queue.py
    TYPE_HEADERS: dict[ItemType, tuple[str, str]] = {
        ItemType.DISPATCH:     ("📤", "Dispatch"),
        ItemType.REVIEW:       ("🔀", "Review"),
        ItemType.STALE_BRANCH: ("🌱", "Stale branches"),
    }

    def render_queue(items: list[QueueItem], config: PlatformConfig) -> None:
        """Renderiza fila agrupada por tipo. Clique grava selected_queue_item_id."""

    def group_by_type(items: list[QueueItem]) -> dict[ItemType, list[QueueItem]]:
        """Helper puro testável; preserva ordenação interna."""

    def build_world_state(roadmaps: list[ParsedRoadmap]) -> WorldState:
        """Wrapper que chama list_remote_branches() e datetime.now()."""
    ```
  - **Integração:** `app.py` carrega `parsed_roadmaps` (via PLAT-1), monta tabs, na tab fila chama `build_world_state` (com cache em `session_state`) → `detect_all_items` → `render_queue`. Após `render_queue`, se há `selected_queue_item_id`, chama `render_queue_item_detail` (definido em 2.2).
  - **Template de referência:** `tools/workflow_platform/views/kanban.py` (W-PROTO-PLAT-2.1) — uso de `st.session_state` para seleção de card, padrão de `render_*` puro.
  - **Acoplamentos verificados:**
    - `tools/workflow_platform/queue/{models,detect}.py` — FILA-1.1/1.2.
    - `tools/workflow_platform/views/kanban.py` (PLAT-2) — coexistência via tabs; render do kanban inalterado.
    - **Produto afetado:** nenhum.
  - **Dependências de ordem:** depende de FILA-1.1/1.2; precede 2.2.
  - **Escopo de teste:**
    - **Unit:** `test_queue_view.py` — `group_by_type` retorna dict com 3 chaves (mesmo se vazias); ordem interna preservada do input.
    - **Validação manual:** abrir app com fixture sintética (mesmo de FILA-1.3); verificar (a) tab fila default; (b) cards agrupados; (c) clique seleciona; (d) recarga dispara fetch.

#### 2.2: Builders de prompt por tipo de item

- **Descrição:** módulo `prompts/queue_item.py` expõe `build_prompt_for_item(item) -> str` que despacha por `item.type`. DISPATCH reusa `build_dispatch_prompt` (PLAT-3.1) chamado com o `Epic` reconstruído a partir do `EpicPointer`. REVIEW e STALE_BRANCH têm builders novos com texto fixo parametrizado pelos campos do pointer. Painel de detalhe (`render_queue_item_detail`) exibe o prompt em `st.code()` com botão copy nativo do Streamlit.
- **Critérios de Aceite:**
  1. `build_prompt_for_item(item)` retorna string copy-pasteável; nunca `None` (item válido sempre tem prompt)
  2. Para DISPATCH: prompt é o output de `build_dispatch_prompt` (formato `"implementa o <MILESTONE_ID>"` + nota de PM skill se aplicável); reusa builder de PLAT-3.1 sem duplicação de lógica
  3. Para REVIEW: prompt contém literal `"Revisar PR #<N>: <URL>"` + instrução `"Abra a PR, copie a Seção 🎯 Validação do body, cole no GitHub Copilot, e decida merge."`
  4. Para STALE_BRANCH: prompt contém literal `"Branch <NAME> parada há <DAYS> dias sem PR aberta."` + 3 opções enumeradas: `(a) trabalho concluído sem PR — abrir PR / (b) abandonado — git push origin --delete <NAME> / (c) bloqueado — resgatar contexto e seguir`
  5. `render_queue_item_detail(item, config, all_epics)` exibe prompt via `st.code(prompt, language=None)` (botão copy nativo do Streamlit) + título do item + ponteiro tipado renderizado como link (PR URL clicável, branch link via `github_branch_url` de PLAT-3.2, milestone como referência ao kanban)
- **Detalhes de execução:**
  - **Arquivos a criar:** `tools/workflow_platform/prompts/queue_item.py`, `tests/tools/workflow_platform/test_queue_item_prompt.py`
  - **Arquivos a modificar:** `tools/workflow_platform/views/queue.py` — adicionar `render_queue_item_detail`.
  - **Contratos/Shapes:**
    ```python
    # tools/workflow_platform/prompts/queue_item.py
    def build_prompt_for_item(
        item: QueueItem,
        all_epics_by_milestone: dict[str, list[Epic]] | None = None,
    ) -> str:
        """Despacha por item.type. DISPATCH precisa de all_epics_by_milestone
        para reusar build_dispatch_prompt; REVIEW e STALE_BRANCH ignoram."""

    def _build_review_prompt(p: PRPointer) -> str: ...
    def _build_stale_branch_prompt(p: BranchPointer) -> str: ...
    ```
    Exemplo de prompt REVIEW:
    ```
    Revisar PR #93: https://github.com/gmaiarviana/paper-agent/pull/93

    Abra a PR, copie a Seção 🎯 Validação do body, cole no GitHub Copilot,
    e decida merge.
    ```
    Exemplo de prompt STALE_BRANCH:
    ```
    Branch claude/foo-bar parada há 12 dias sem PR aberta.

    Decida:
    (a) trabalho concluído sem PR — abrir PR via interface do GitHub
    (b) abandonado — `git push origin --delete claude/foo-bar`
    (c) bloqueado — resgatar contexto e seguir
    ```
  - **Integração:** `views/queue.py::render_queue_item_detail` recebe o item selecionado e chama `build_prompt_for_item`. Para DISPATCH, monta `all_epics_by_milestone` a partir dos `parsed_roadmaps` em `session_state`.
  - **Template de referência:** `tools/workflow_platform/prompts/dispatch.py` (PLAT-3.1) — mesmo shape de helper puro retornando string.
  - **Acoplamentos verificados:**
    - `tools/workflow_platform/prompts/dispatch.py` (PLAT-3.1): `build_dispatch_prompt` reusado para DISPATCH.
    - `tools/workflow_platform/queue/models.py` (FILA-1.1): `QueueItem`, `SourcePointer`.
    - `tools/workflow_platform/views/card_detail.py` helpers `github_branch_url`/`github_pr_url` (PLAT-3.2): reusados para links.
    - **Produto afetado:** nenhum.
  - **Dependências de ordem:** depende de 2.1 (`render_queue_item_detail` é chamado por `render_queue`); depende de PLAT-3.1.
  - **Escopo de teste:**
    - **Unit:** `test_queue_item_prompt.py` — (a) DISPATCH delega corretamente: stub de `build_dispatch_prompt` é chamado com `Epic` esperado; (b) REVIEW contém PR número e URL literais; (c) STALE_BRANCH contém nome, dias e as 3 opções; (d) prompt nunca tem placeholder não-substituído (`re.search(r"<[A-Z_]+>", prompt)` não encontra match).
    - **Validação manual:** clicar em itens da fila no app (DISPATCH/REVIEW/STALE_BRANCH); copiar cada prompt; conferir conteúdo.

**Fora do escopo:**
- Chat embutido na plataforma (sessão de Claude Code dentro do app) — escopo MVP.
- Browser automation pra abrir sessão autônoma direto do clique — escopo MVP.
- Edição/cancelamento manual de itens da fila — fila é derivada, mexer no estado-do-mundo (ROADMAP, branch) já basta.

---

#### ÉPICO W-PROTO-FILA-3: Auto-regulação básica (alerta visual)

**Milestone:** `PROTO-WORKFLOW-FILA`

**Objetivo:** plataforma sinaliza visualmente quando a fila se aproxima do limite cognitivo (~20 itens). Sem pausa dura — só alerta. Pausa real só faz sentido no MVP, quando há agente proativo criando itens.

**Status:** 📐 Funcionalidades esboçadas

**Dependências:** W-PROTO-FILA-1 (fila existente)

### Funcionalidades (esboço):
- **3.1 Contagem e indicador** — exibe contagem atual vs. limite alvo (~20 itens) na sidebar.
- **3.2 Alerta de aproximação** — sinalização visual ao chegar perto do limite; sem ação automática.

---

> **Milestones de saneamento documental** (`PROTO-WORKFLOW-FAXINA` e `PROTO-WORKFLOW-COPILOT-STACK`) declarados em 2026-04-29 a partir dos épicos levantados na revisão `claude/review-process-directory-J1v8v` (2026-04-28); refinados a `🔍 Detalhes definidos` em 2026-04-29 (sessão `claude/refine-workflow-stacks-6JOH6`). Faxina antes de seguir para `PROTO-WORKFLOW-FILA`.

#### ÉPICO W-PROTO-10: Centralizar definição dos estados de épico

**Milestone:** `PROTO-WORKFLOW-FAXINA`

**Objetivo:** eliminar drift entre as três cópias da lista canônica dos 8 estados de épico em `docs/process/refinement/planning_guidelines.md` (§"Estados de Refinamento" linhas 176-205, §"Categorias de Épicos" linhas 253-269, §"PRÓXIMOS PASSOS" linhas 331-358). Drift entre cópias gerou as 3 contradições corrigidas em 2026-04-28; próxima skill que ler cópia desatualizada repete o erro.

**Status:** 🔍 Detalhes definidos

**Dependências:** rodar **depois** de W-PROTO-15 — 15.1 já reescreve `📋 Critérios definidos` ("apto ao fluxo manual" → passo intermediário) na fonte. Centralizar antes faz a edição duas vezes.

### Funcionalidades:

#### 10.1 Bloco canônico único em `planning_guidelines.md`

**Critério de aceite:** uma única seção em `planning_guidelines.md` define os 8 estados (🌱 Visão, 🧭 Jornada alinhada, 📐 Funcionalidades esboçadas, 📋 Critérios definidos, 🔍 Detalhes definidos, 🏗️ Em andamento, 🔀 Em revisão, ✅ Implementado) com nome, descrição curta (1-3 frases), gatilho de transição e responsável. As outras duas seções dentro do mesmo arquivo são apagadas e referências internas apontam pra fonte canônica via âncora markdown.

**Decisão de fonte canônica:** usar §"Categorias de Épicos" (linhas 253-269 hoje) como base — formato bullet paralelizado, mais mantível que parágrafos. Renomear para §"Estados de Épico" e mover para perto do início do doc (depois da introdução) pra ser fácil de achar. Apagar §"Estados de Refinamento" (linhas 176-205) e a re-listagem em §"PRÓXIMOS PASSOS" (linhas 335-342).

**Arquivos a modificar:**
- `docs/process/refinement/planning_guidelines.md` — seção canônica + apagar duplicatas + ajustar referências internas (links de âncora `#estados-de-épico`).

**Validação:** `grep -n "🌱.*Visão.*🧭.*Jornada\|🌱 Visão$" docs/process/refinement/planning_guidelines.md` retorna no máximo 1 bloco de definição completa.

#### 10.2 Limpeza de drift cross-doc

**Critério de aceite:** arquivos abaixo deixam de ter definição dos 8 estados (texto duplicado) e passam a apontar pra fonte canônica em `planning_guidelines.md#estados-de-épico` na primeira menção do contexto. Menções pontuais a estados específicos (ex: "épico em `🔍`") permanecem como estão — não precisam de link.

**Arquivos a modificar:**

| Arquivo | Linhas-alvo (hoje) | Ação |
|---|---|---|
| `docs/process/refinement/starter.md` | 41-77 (§"Alvos de Refinamento") | manter conteúdo pedagógico (5 alvos com pergunta-chave); adicionar nota com link pra fonte canônica logo no início da seção |
| `docs/CONSTITUTION.md` | 17 (linha enumeradora) e 328-331 (§"Estrutura de Épicos") | manter linha 17 com link já existente; reduzir 328-331 a 1 frase + link |
| `docs/process/autonomous/workflow.md` | tabela "Estado mínimo do épico" (~linha 50) | nota com link na introdução da seção |
| `docs/process/workflow/vision.md` | 1ª menção de estado (~linha 100) | nota com link na introdução |
| `skills/pm/README.md` | 1ª menção de estado | nota com link |
| `docs/process/refinement/autonomous_readiness.md` | já tem link (linha 3) | nada a fazer |

**Validação:**
- `grep -l "🌱.*🧭.*📐.*📋.*🔍.*🏗\|🌱 Visão.*🧭 Jornada" docs/ skills/` retorna apenas `docs/process/refinement/planning_guidelines.md` e a tabela `EpicState` em `docs/process/workflow/ROADMAP.md` (estrutura de dado, não texto).
- Inspeção visual: arquivos da tabela acima abrem com link pra fonte canônica antes de qualquer menção a estado.

**Acoplamento com `EpicState` enum no parser:** o enum em `docs/process/workflow/ROADMAP.md` linhas ~519-537 (parser de W-PROTO-PLAT-1.1) é estrutura de dado, não cópia textual da definição. Mantém-se intacto. Nota explícita na fonte canônica: "Os emojis e nomes aqui são fonte da verdade tanto para texto quanto para o `EpicState` enum em W-PROTO-PLAT-1.1."

**Fora do escopo:**
- Quebrar `planning_guidelines.md` em arquivos separados — escopo de W-MVP-DOC-1.
- Atualizar referências em PRs históricas, commits, ou ROADMAPs de milestones já fechados.

---

#### ÉPICO W-PROTO-11: Faxina de `quality_rules.md`

**Milestone:** `PROTO-WORKFLOW-FAXINA`

**Objetivo:** tirar de `docs/process/implementation/quality_rules.md` (397 linhas hoje) o que não é regra de processo do fluxo. Mistura princípios + lessons learned do produto Revelar + tutorial defensivo de git pra Windows. Skill que segue esse doc pode aplicar regra fora de contexto. Saída: doc com ~185 linhas focado em princípios + anti-redundância + comandos.

**Status:** 🔍 Detalhes definidos

**Dependências:** rodar **depois** de W-PROTO-15 (limpa "Cursor Background" nas linhas 144 e 382 antes do 11.3 reorganizar) e **depois** de W-PROTO-16 (congela o template canônico em linhas 105-128 antes do 11.3 reorganizar).

### Funcionalidades:

#### 11.1 Apagar §"Verificação de Conflitos e Prevenção de Perda de Trabalho"

**Critério de aceite:** seção inteira (linhas 230-369 hoje, 140 linhas) é apagada de `quality_rules.md`. Tutorial defensivo de git nasceu de incidente concreto e ficou; não é regra de qualidade do processo. Subseções afetadas: 🚨 Problema Identificado, ✅ Processo de Verificação, 📋 Checklist Antes de Editar ROADMAP.md, 🔍 Verificação de Arquivos Modificados, 🛡️ Prevenção, 📝 Template de Verificação, ⚠️ Sinais de Alerta.

**Arquivos a modificar:** `docs/process/implementation/quality_rules.md` (apagar seção).

**Validação:** `grep -n "Verificação de Conflitos\|Prevenção de Perda" docs/process/implementation/quality_rules.md` retorna 0 linhas.

#### 11.2 Mover §"Diretrizes Aprendidas em Produção" para `products/revelar/docs/`

**Critério de aceite:** seção (linhas 29-73 hoje, 45 linhas, com 3 subseções: Sistemas Conversacionais com LLMs, Validação e Testes, Arquitetura e Design) é apagada de `quality_rules.md` e migrada para arquivo novo `products/revelar/docs/llm_implementation_lessons.md`. Conteúdo é específico do Revelar (produto conversacional com LLMs); fica órfão em `quality_rules.md`.

**Decisão de destino:** `products/revelar/docs/llm_implementation_lessons.md` em vez de `core/docs/agents/`. Razão: as 3 subseções são específicas da jornada do Revelar (não regras universais para qualquer agente). `core/docs/agents/orchestrator/conversational/` já tem 9 arquivos sobre arquitetura conversacional; misturar lessons learned ali criaria grab-bag.

**Arquivos a modificar:**
- `docs/process/implementation/quality_rules.md` — apagar linhas 29-73.
- `products/revelar/docs/llm_implementation_lessons.md` — arquivo novo com o conteúdo migrado, prefixado por header curto: "Lições aprendidas implementando o Revelar (sistema conversacional com LLMs). Migrado de `docs/process/implementation/quality_rules.md` em PROTO-WORKFLOW-FAXINA, 2026-04-29."

**Acoplamentos:** nenhum link cruzado precisa ser ajustado — o conteúdo era órfão em `quality_rules.md`, sem âncoras referenciadas externamente.

**Validação:** `grep -n "Diretrizes Aprendidas em Produção\|Sistemas Conversacionais com LLMs" docs/process/implementation/quality_rules.md` retorna 0 linhas. `ls products/revelar/docs/llm_implementation_lessons.md` existe com >40 linhas.

#### 11.3 Reorganizar o que sobra em ordem coerente

**Critério de aceite:** após 11.1 + 11.2 + W-PROTO-15.4 (limpa "Cursor Background" nas linhas 144, 382) + W-PROTO-16 (congela template canônico), as seções remanescentes são reorganizadas na ordem abaixo, sem grab-bag.

**Estrutura final do `quality_rules.md`:**
1. **Princípios Gerais** (lines 3-26 hoje) — Incremental e Seguro, TDD Pragmático, Autônomo mas Transparente, Documentação Viva.
2. **Regras Anti-Redundância** (lines 76-95 hoje) — tabela de responsabilidade por documento + regras de ouro.
3. **Comandos e Validação** (lines 98-137 hoje) — fica como **âncora canônica** para W-PROTO-16; mantém §Template de validação + §Observações.
4. **Exemplo de Fluxo Completo** (lines 140-227 hoje) — fica, mas com "Cursor Background" removido em W-PROTO-15.4 e exemplo adaptado pra fluxo único.
5. **Observações Finais** (lines 373-396 hoje) — fica, com seção "Para o Agente (Claude Code / Cursor Background)" reescrita em W-PROTO-15.4.

Não há reordenação radical — a ordem atual já é coerente. 11.3 valida que após as remoções/limpezas o fluxo do doc lê limpo.

**Arquivos a modificar:** `docs/process/implementation/quality_rules.md` (apenas se 11.1 + 11.2 + 15.4 + 16 deixaram lacunas visuais ou seções desbalanceadas).

**Validação:**
- `wc -l docs/process/implementation/quality_rules.md` retorna ~180-200 linhas.
- Inspeção visual: leitura sequencial do doc não tem saltos abruptos de tema.

**Fora do escopo:**
- Quebrar `quality_rules.md` em arquivos por responsabilidade (escopo de W-MVP-DOC-1 / futuro).
- Reescrever os princípios — apenas reorganizar o que sobra.

---

> **Nota — W-PROTO-12 absorvido por W-PROTO-15.** Refinamento estratégico de
> 2026-04-29 decidiu não cindir `implementation/overview.md`. A premissa
> ("isolar conteúdo do fluxo manual") some quando 15.4 elimina a dicotomia;
> o conteúdo útil de §"Validação Híbrida" (sintaxe, imports) vale pra qualquer
> fluxo e fica no overview mesmo. Se "doc por responsabilidade" virar atrito
> real depois, vira épico próprio no MVP-WORKFLOW-DOC.

---

#### ÉPICO W-PROTO-13: Faxina do `copilot-instructions.md` (concisão pra agente)

**Milestone:** `PROTO-WORKFLOW-FAXINA`

**Objetivo:** aplicar princípio "documentação para agente é concisa, não defensiva" — agente trabalha do traceback, não consulta catálogo de erros típicos. Doc hoje (143 linhas) carrega seções defensivas residuais que confundem o Copilot ao invés de ajudar.

**Status:** 🔍 Detalhes definidos

**Nota factual sobre seções declaradas no esboço inicial:** §"Erros típicos e orientação" (alvo original 13.1) e §"Checklist mínimo de POC do Ensaio" (alvo original 13.2) **não existem** mais no arquivo — foram apagadas em refinamentos anteriores (mais recente: PROTO-WORKFLOW-AJUSTES, PR #93). Funcionalidades 13.1 e 13.2 viraram **no-ops verificados**; escopo real do épico é 13.3 + sobreposição com W-PROTO-14.

**Dependências:** coordena com W-PROTO-14 — ambos tocam §"Operação Windows / macOS / Linux" (linhas 120-127) e §3 "Subir a app" (linhas 68-96). Ordem segura: W-PROTO-13 primeiro (apaga seção que vai ser substituída por conteúdo novo de W-PROTO-14), depois W-PROTO-14. Se rodarem na mesma sessão, o agente faz as duas operações coerentemente sem conflito.

### Funcionalidades:

#### 13.1 §"Erros típicos e orientação" — no-op (já apagada)

**Critério de aceite:** `grep -c "Erros típicos\|orientação" .github/copilot-instructions.md` retorna 0 ocorrências do título de seção. Verificação documental: nenhum trabalho a fazer; a feature fecha com nota explícita no `current_implementation.md` ("seção já apagada em refinamento anterior; nada a fazer").

#### 13.2 §"Checklist mínimo de POC do Ensaio" — no-op (já apagada)

**Critério de aceite:** `grep -c "Checklist mínimo.*POC\|POC do Ensaio" .github/copilot-instructions.md` retorna 0 ocorrências. Verificação documental: nenhum trabalho a fazer; a feature fecha com nota explícita no `current_implementation.md`.

#### 13.3 Apagar §"Operação Windows / macOS / Linux"; manter §"Quando o dev disser 'deu erro'"

**Critério de aceite:** §"Operação Windows / macOS / Linux" (linhas 120-127, 8 linhas) é apagada. Conteúdo é redundante: (a) trecho `.venv/` aparece também na §1 Sincronizar (linhas 44-48); (b) trecho Streamlit + porta 8501 é substituído pela detecção de stack de W-PROTO-14.1 + comando + range de portas (W-PROTO-14.2/14.3); (c) "foreground sempre + traceback → reportar" já está em §3 (linhas 94-95).

§"Quando o dev disser 'deu erro'" (linhas 130-135, 6 linhas) **fica intacta**. Decisão de manter: o conteúdo é genérico (coletar log, identificar causa raiz no traceback, não editar código) e operacional — descreve postura, não erros específicos. Não é padrão defensivo.

**Arquivos a modificar:**
- `.github/copilot-instructions.md` — apagar bloco linhas 120-127 (incluindo o `---` separador acima ou abaixo, conforme leitura pós-edição).

**Validação:**
- `grep -n "Operação Windows" .github/copilot-instructions.md` retorna 0.
- `grep -n "Quando o dev disser" .github/copilot-instructions.md` retorna 1 (mantida).
- `wc -l .github/copilot-instructions.md` retorna ~135 linhas (vs 143 hoje).

**Fora do escopo:**
- Reescrita da §3 "Subir a app" (linhas 68-96) — escopo de W-PROTO-14.
- Mudanças na §1 Sincronizar / §2 Resumo / §"Output fixo" — sem sinal de atrito.

---

#### ÉPICO W-PROTO-14: Operacionalizar Reflex no fluxo de validação do Copilot

**Milestone:** `PROTO-WORKFLOW-COPILOT-STACK`

**Objetivo:** o Ensaio migrou para Reflex no Protótipo (ADR 001 de 2026-04-25), mas `copilot-instructions.md` ainda manda Streamlit pros dois produtos (linhas 70, 82, 92, 125). Validação de branches do Ensaio quebra ou roda com comando errado.

**Status:** 🔍 Detalhes definidos

**Dependências:**
- ADR 001 (`products/ensaio/docs/adr/001-stack-do-prototipo.md`) — comandos e portas de Reflex já fixados; sem input pendente do dev.
- `products/ensaio/rxconfig.py` — fonte da verdade para `backend_port=8000` e `frontend_port=3000`.
- Coordena com W-PROTO-13.3: ambos tocam linhas 120-127. Ordem: 13.3 apaga primeiro, 14 reescreve §3 depois.

### Termos e contratos

**Detecção de stack** (termo novo introduzido por este épico): regra determinística que mapeia caminho de arquivo no diff → stack do produto → comando de subida → portas. Tabela canônica:

| Produto | Caminho-gatilho | Stack | Comando de subida | Portas a liberar |
|---|---|---|---|---|
| Revelar | `products/revelar/app/**` | Streamlit | `python -m streamlit run <entrypoint>` | 8501-8503 |
| Ensaio | `products/ensaio/app/**` | Reflex | `cd products/ensaio && reflex run` | 3000 (frontend), 8000 (backend) |
| Futuros | `products/<novo>/app/**` | a declarar | a declarar | a declarar |

### Funcionalidades:

#### 14.1 Detecção de stack por produto

**Critério de aceite:** `.github/copilot-instructions.md` ganha tabela explícita produto → stack → entrypoint → comando → portas, posicionada como §"Stacks por produto" entre §"Pré-condição" (linhas 19-31) e §"Fluxo (3 passos)" (linha 35). Detecção pelo diff (`git diff --name-only origin/main | grep products/`) usa essa tabela como fonte. Se o diff toca produto sem entrada na tabela, o agente para e reporta — não improvisa.

**Conteúdo da seção (verbatim a inserir):**

```markdown
## Stacks por produto

A validação por aqui detecta o produto pelo diff e usa a stack correspondente.
Se a branch toca produto fora desta tabela, **pare e reporte** — não improvise.

| Produto | Caminho-gatilho        | Stack     | Entrypoint                                  | Portas      |
|---------|------------------------|-----------|---------------------------------------------|-------------|
| Revelar | products/revelar/app/  | Streamlit | products/revelar/app/chat.py (ou dashboard) | 8501-8503   |
| Ensaio  | products/ensaio/app/   | Reflex    | products/ensaio/ (reflex run a partir daí) | 3000, 8000  |

Se a branch mexe em mais de um produto, perguntar ao dev qual subir primeiro.
Se a branch só mexe em `core/` ou `docs/`, não há app para subir — pular §3.
```

**Arquivos a modificar:**
- `.github/copilot-instructions.md` — inserir seção nova entre linhas 31 e 35.

#### 14.2 Comando de subida por stack na §3

**Critério de aceite:** §3 "Subir a app afetada" (linhas 68-96 hoje) é reescrita pra ramificar por stack detectada em 14.1. Comando de Reflex é foreground, com log visível, encerramento via Ctrl+C — mesma postura do Streamlit.

**Conteúdo da §3 (substituir linhas 68-96 por):**

```markdown
### 3. Subir a app afetada

Antes de qualquer coisa, libere as portas da stack detectada (ver §"Stacks
por produto" + §"Liberação de portas" abaixo). Não mate processos em geral —
mate apenas quem está escutando nas portas-alvo.

Detectar produto pelo diff (`git diff --name-only origin/main | grep products/`):
- `products/<produto>/app/**` → subir a stack do produto
- Se a branch mexeu em mais de um produto, perguntar ao dev qual subir primeiro
- Se a branch não mexeu em nenhum produto: avisar e pular esta etapa.

**Streamlit (Revelar):**

```bash
python -m streamlit run <entrypoint>     # ex: products/revelar/app/chat.py
```

**Reflex (Ensaio):**

```bash
cd products/ensaio
reflex run                               # backend :8000, frontend :3000
```

Subir em **foreground** e deixar rodando — o dev vai abrir no navegador.
Se o log mostrar traceback no start → parar, reportar o erro, não tentar consertar.
```

**Arquivos a modificar:** `.github/copilot-instructions.md` (substituir linhas 68-96).

#### 14.3 Liberação de portas por stack

**Critério de aceite:** o bloco de liberação de portas (linhas 70-83 hoje, hardcoded em 8501-8503) é reescrito pra cobrir Streamlit (8501-8503) **e** Reflex (3000, 8000). Detecção da stack reusa 14.1 e libera apenas as portas relevantes — não mata processos em geral.

**Conteúdo do bloco (substituir linhas 70-83 por):**

```markdown
**Antes de qualquer coisa:** liberar as portas da stack detectada matando
apenas quem está escutando nelas.

Para Streamlit (Revelar): portas 8501-8503.
Para Reflex (Ensaio): portas 3000 (frontend) e 8000 (backend).

```powershell
# Windows (PowerShell) — cirúrgico por porta. Adapte $ports à stack detectada.
$ports = @(8501, 8502, 8503)         # Streamlit (Revelar)
# $ports = @(3000, 8000)             # Reflex (Ensaio)
foreach ($port in $ports) {
    Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue |
        ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }
}
```

```bash
# Linux/Mac — filtra pelo entrypoint do projeto
pkill -f "streamlit.*products/revelar/app/" 2>/dev/null || true   # Revelar
pkill -f "reflex.*products/ensaio" 2>/dev/null || true            # Ensaio
```
```

**Arquivos a modificar:** `.github/copilot-instructions.md` (substituir linhas 70-83).

### Acoplamentos verificados

- **`products/revelar/app/`** existe com `chat.py` + `dashboard.py` + componentes. Comando atual `python -m streamlit run` permanece válido.
- **`products/ensaio/app/`** existe com Reflex; `rxconfig.py` confirma portas 3000/8000 e `app_name="app"`.
- **`scripts/`**: nenhum script roda os apps — comandos vivem só na doc do Copilot.
- **Outros docs** que mencionam Streamlit/Reflex (tabela do mapeamento exaustivo: `docs/ARCHITECTURE.md`, `docs/CONSTITUTION.md` linha 295, `docs/CONTEXT_INDEX.md`, `products/ensaio/README.md`, `core/docs/tools/cli.md`) — referências contextuais (descrição do produto), não comandos de validação. **Fora do escopo** deste épico.

### Validação

- `grep -n "reflex run" .github/copilot-instructions.md` retorna ≥1 linha.
- `grep -n "products/ensaio" .github/copilot-instructions.md` retorna ≥1 linha.
- `grep -nE "8501|8502|8503|3000|8000" .github/copilot-instructions.md` retorna linhas em §"Liberação de portas".
- Inspeção visual: §3 ramifica claramente entre Streamlit e Reflex.

**Fora do escopo:**
- Detecção automatizada via script — instrução textual é suficiente para o Copilot.
- Reescrita da nota de erros típicos / debug — coberto por W-PROTO-13.
- Mudança no parser de portas em outras ferramentas (workflow_platform usa Streamlit também, mas tem porta própria).

---

#### ÉPICO W-PROTO-15: Descontinuar fluxo manual / Cursor / Claude Web do desenho

**Milestone:** `PROTO-WORKFLOW-FAXINA`

**Objetivo:** o desenho atual carrega dicotomia "fluxo manual (Cursor) vs fluxo autônomo (Claude Code Web)" em ~140 menções espalhadas em 16 arquivos. Na prática, o operador opera 100% via Claude Code Web — implementação **e** refinamento estratégico. Cursor não está instalado no ambiente atual; Claude Web persiste como ferramenta de refinamento estratégico em sessão externa quando há decisão de alto nível, mas não como executor. A documentação ficou desalinhada do uso real e impõe ao agente leitor o custo de filtrar "o que aplica ao meu contexto". Este épico **absorve W-PROTO-12** (cindir `implementation/overview.md`) — a premissa do W-PROTO-12 some quando 15.4 elimina a dicotomia.

**Status:** 🔍 Detalhes definidos

### Termos e conceitos

- **Refinamento estratégico** — sessão com operador para decisões de alto nível (visão → milestones, tensões arquiteturais, escopo de fase). Pode rodar via Claude Code Web (caminho principal, com acesso direto ao repo) ou via Claude Web em sessão externa quando o operador escolher (ferramenta secundária; não desaparece). Definição canônica → `docs/process/refinement/planning_guidelines.md` §"Modalidades de refinamento" (após reescrita 15.2).
- **Refinamento tático** — PM skill dentro da branch do milestone; leva épicos de `🌱`/`📐` até `🔍`. Definição → `skills/pm/skill.md` (sem alteração necessária).
- **Fluxo único de execução** — Claude Code Web autônomo, com gates QA/TL/PO/RTE atuando como aprovações no lugar do dev acompanhando checkpoint a checkpoint. Definição → `docs/process/autonomous/overview.md` (após reescrita 15.1).

### Surface afetada (mapeamento exaustivo)

Levantamento feito em 2026-04-29 (revisão `claude/refine-workflow-stacks-6JOH6`). Cada arquivo abaixo tem ação declarada e linhas-alvo nominais (linhas podem deslocar conforme as edições rodam — usar grep para localizar).

| Arquivo | Menções | Ação principal |
|---|---:|---|
| `docs/CONSTITUTION.md` | 30 | reescrever §Fluxos Disponíveis, apagar §Cursor (Atualizador de Documentações), atualizar glossário (épico, funcionalidade), remover §"Gerar Prompts para fluxo manual" |
| `docs/process/refinement/planning_guidelines.md` | 27-28 | reescrever §"Otimização do Workflow" (linhas ~99-140) como §"Modalidades de Refinamento"; atualizar rótulo de `📋` (linha 260, 338); apagar §"Claude Web gera prompts separados para Cursor" (linhas 77-82) |
| `docs/process/refinement/starter.md` | 10 | atualizar rótulo de `📋` (linha 68); generalizar instruções de "Contexto enviado ao Claude Web" pra incluir caminho via Claude Code Web; remover "(via Cursor)" da inspeção de código (linha 74) |
| `docs/process/autonomous/overview.md` | 9 | apagar tabela "Fluxo Manual vs Autônomo" (linhas 48-55); apagar §"Use o Fluxo Manual (Cursor) quando..." (linhas 61-68); remover contraste manual/autônomo da intro (linha 13); reescrever menção em §6 (linha 86) |
| `docs/process/refinement/overview.md` | 2-3 | atualizar nota de evolução (linha 3); corrigir bullet de "implementação manual via Cursor" (linha 26) |
| `docs/process/autonomous/delivery.md` | 4 | substituir fallback "trazer para Cursor (fluxo manual)" por "devolver para PM skill / Claude Web" (linhas 23, 100); remover qualificador "compartilhada com fluxo manual" (linha 131) |
| `docs/process/implementation/overview.md` | 3 | reescrever cabeçalho linha 3 (de "Claude Code / Cursor Background" → "Claude Code Web"); apagar nota corretiva linhas 88-91 sobre "fluxo manual"; **manter** §"Validação Híbrida" intacta (absorção W-PROTO-12) |
| `docs/process/implementation/quality_rules.md` | 2 | atualizar cabeçalho linhas 144 e 382 (de "Claude Code / Cursor Background" → "Claude Code Web"). Coordenado com W-PROTO-11.3 |
| `skills/pm/skill.md` | 5 | nenhuma edição — guardrails "não substitui Claude Web" continuam corretos (Claude Web segue como caminho secundário de refinamento estratégico) |
| `skills/em/skill.md` | 3 | nenhuma edição — mesmo motivo |
| `skills/rte/skill.md` | 1 | remover qualificador "compartilhada com fluxo manual" (linha 420) |
| `skills/rte/templates/delivery-report.md` | 1 | atualizar fallback "OU traga para Cursor" → "refine com PM skill" |
| `docs/CONTEXT_INDEX.md` | 2 | atualizar bullets "manual via Cursor" → "via Claude Code Web" (linhas 211, 219) |
| `README.md` | 1 | atualizar rótulo "(Claude, Cursor, Claude Code)" → "(Claude Web, Claude Code Web)" (linha 219) |
| `CLAUDE.md` | 4 | reescrever bullet de "Fluxo manual (Cursor)" (linhas 39-40) e remover referência a `.cursorrules` (linha 52) — coordenado com 15.6 e com adição da regra "sugestão com trade-offs" (escopo desta sessão de refinamento) |
| `.claudecode.md` | 0 | nenhuma menção — sem edição |
| `.cursorrules` | n/a | apagar arquivo (60 linhas) |

### Funcionalidades:

#### 15.1 Reescrever `autonomous/overview.md` para fluxo único

**Critério de aceite:** arquivo descreve **um** fluxo (autônomo via Claude Code Web). Tabela "Fluxo Manual vs Autônomo" (linhas 48-55) some. Seção "Use o Fluxo Manual (Cursor) quando..." (linhas 61-68) some. Intro (linha 13) e §6 (linha 86) deixam de contrastar com fluxo manual. Estado `📋 Critérios definidos` é descrito como "passo intermediário até `🔍`" (não como "apto ao fluxo manual").

**Arquivos a modificar:** `docs/process/autonomous/overview.md`.

**Validação:** `grep -ni "fluxo manual\|cursor" docs/process/autonomous/overview.md` retorna 0.

#### 15.2 Reescrever §"Otimização do Workflow" em `planning_guidelines.md` como §"Modalidades de Refinamento"

**Critério de aceite:** §"Otimização do Workflow: Usando Cursor para Análises" (linhas 99-140 hoje) é apagada e substituída por §"Modalidades de Refinamento", que descreve três modalidades:

1. **Estratégico (sessão externa com operador, via Claude Web ou equivalente)** — ferramenta secundária, usada em decisões estruturais que exigem alinhamento humano. Contexto suprido por upload manual ou pela plataforma (W-MVP-PLAT-2 quando existir).
2. **Estratégico (Claude Code Web na branch do repo)** — caminho principal hoje. Acesso direto ao repo; refina e materializa no ROADMAP em sessão única.
3. **Tático (PM skill dentro da branch do milestone)** — refinamento mecânico de épicos `🌱`/`📐` até `🔍` quando o milestone é disparado.

Pipeline tripartite "Cursor escaneia → Claude Web refina → Cursor executa" desaparece — premissa obsoleta (Claude Code Web já tem acesso ao código).

**Arquivos a modificar:**
- `docs/process/refinement/planning_guidelines.md` — substituir linhas 99-140 + apagar §"Claude Web gera prompts separados para Cursor" (linhas 77-82).
- Ajustar rótulos de `📋` em linhas 260, 338, 350 ("apto ao fluxo manual" → "passo intermediário até `🔍`"). Linha 269 ("Claude Code só implementa épicos em `📋` (manual) ou `🔍` (autônomo)") vira "épicos em `🔍`".

**Validação:** `grep -ni "Otimização do Workflow.*Cursor\|prompts separados para Cursor\|apto ao fluxo manual" docs/process/refinement/planning_guidelines.md` retorna 0.

#### 15.3 Limpar `CONSTITUTION.md`

**Critério de aceite:** as 30 menções caem por:
- Reescrever §Fluxos Disponíveis (linhas 36-45) como §"Requisitos de Refinamento" (descreve `📋` → `🔍` como progressão obrigatória antes da execução).
- Apagar §"Cursor (Atualizador de Documentações)" (linhas 66-77) inteiramente.
- Atualizar glossário: definição de Épico (linha 328), Funcionalidade (linha 331), e linha enumeradora 17 que mantém link já existente.
- Reescrever §"Gerar Prompts" da sessão de refinamento (linhas 128-159) — Formato A (lista de milestones/épicos) fica; Formato B (prompts pra Cursor) sai.
- Linha 11 (definição da dicotomia) some — premissa não vale mais.

**Arquivos a modificar:** `docs/CONSTITUTION.md`.

**Validação:** `grep -ni "cursor\|fluxo manual" docs/CONSTITUTION.md` retorna 0 (apenas menção possível: link pra `.cursorrules`, mas ele será apagado em 15.6 → 0 menções).

#### 15.4 Limpar `implementation/overview.md` e `quality_rules.md` (absorve W-PROTO-12)

**Critério de aceite:** ambos os arquivos perdem o rótulo "Cursor Background" e a contrastação com "fluxo manual".

Em `implementation/overview.md`:
- Reescrever cabeçalho linha 3: "(Claude Code / Cursor Background)" → "(Claude Code Web)".
- Apagar nota linhas 88-91 (que contrasta o fluxo autônomo com manual via Cursor).
- **Manter §"Validação Híbrida" (linhas 30-92)** — conteúdo (sintaxe, imports, comandos) vale pra qualquer agente, não é específico de fluxo manual. **Esta é a absorção de W-PROTO-12**: cindir o doc deixa de fazer sentido quando a dicotomia some.

Em `quality_rules.md`:
- Reescrever cabeçalho linha 144: "Agente (Claude Code / Cursor Background):" → "Agente (Claude Code Web):".
- Reescrever cabeçalho linha 382: "Para o Agente (Claude Code / Cursor Background)" → "Para o Agente (Claude Code Web)".

**Arquivos a modificar:** `docs/process/implementation/overview.md`, `docs/process/implementation/quality_rules.md`.

**Validação:** `grep -ni "Cursor Background\|fluxo manual" docs/process/implementation/overview.md docs/process/implementation/quality_rules.md` retorna 0.

#### 15.5 Limpar `refinement/starter.md`, `refinement/overview.md`, `autonomous/delivery.md`, `skills/rte/skill.md`, `skills/rte/templates/delivery-report.md`

**Critério de aceite:** menções remanescentes são atualizadas conforme tabela "Surface afetada" acima. PM e EM skills **não são tocadas** — guardrails "não substitui Claude Web" continuam válidos (Claude Web segue como caminho secundário em refinamento estratégico).

**Arquivos a modificar:**
- `docs/process/refinement/starter.md` (linha 68 + 74).
- `docs/process/refinement/overview.md` (linhas 3, 26).
- `docs/process/autonomous/delivery.md` (linhas 23, 100, 131).
- `skills/rte/skill.md` (linha 420).
- `skills/rte/templates/delivery-report.md` (linha ~130).

**Validação:** `grep -ni "fluxo manual\|via Cursor" docs/process/refinement/starter.md docs/process/refinement/overview.md docs/process/autonomous/delivery.md skills/rte/skill.md skills/rte/templates/delivery-report.md` retorna 0.

#### 15.6 Deletar `.cursorrules`

**Critério de aceite:** arquivo `.cursorrules` (60 linhas, 1928 bytes) é apagado integralmente. Conteúdo aplicável (regras de comportamento como "confirmar antes de criar arquivos", "usar PowerShell no Windows") já vive em CLAUDE.md e `.claudecode.md` direcionadas a Claude Code Web — sem migração necessária.

**Arquivos a modificar:** apagar `.cursorrules`.

**Validação:** `ls .cursorrules 2>/dev/null` retorna vazio.

#### 15.7 Atualizar `CLAUDE.md`, `.claudecode.md`, `docs/CONTEXT_INDEX.md`, `README.md`

**Critério de aceite:**

Em `CLAUDE.md`:
- Linha 6: remover referência cruzada a `.cursorrules`.
- Linhas 39-40: bullet "Fluxo manual (Cursor, sessão de refinamento) — defaults restritos do harness e do `.cursorrules` continuam valendo" → reescrever como "Refinamento estratégico em sessão externa com Claude Web — defaults restritos do harness continuam valendo nessas sessões".
- Linha 52: remover bullet "Regras do fluxo manual (Cursor) → `.cursorrules`".

Em `.claudecode.md`: nenhuma edição (zero menções).

Em `docs/CONTEXT_INDEX.md`: linhas 211 e 219 — "manual via Cursor" → "via Claude Code Web".

Em `README.md`: linha 219 — "(Claude, Cursor, Claude Code)" → "(Claude Web, Claude Code Web)".

**Arquivos a modificar:** `CLAUDE.md`, `docs/CONTEXT_INDEX.md`, `README.md`.

**Validação:** `grep -ni "cursor" CLAUDE.md docs/CONTEXT_INDEX.md README.md` retorna 0.

#### 15.8 Varredura final

**Critério de aceite:**

```bash
grep -rni "cursor\|fluxo manual\|claude web.*cursor" \
  --include="*.md" \
  --exclude-dir=.git \
  --exclude="ROADMAP.md" \
  docs/ skills/ products/ core/ tools/ tests/ scripts/ \
  CLAUDE.md README.md
```

Retorna 0 menções, com as exceções declaradas:

- `docs/process/workflow/ROADMAP.md` — épicos históricos (W-PROTO-12 absorvido, W-PROTO-15 e este próprio bloco) e nota de Observações; mantém referência por integridade histórica.
- ROADMAPs de milestones já fechados (`PROTO-WORKFLOW-AJUSTES`, `PROTO-WORKFLOW-DOC`, `PROTO-WORKFLOW-ENCERRAMENTO`) — não tocar.
- `skills/pm/skill.md` e `skills/em/skill.md` — menção a "Claude Web" como caminho secundário de refinamento (correto, fica).

Adicionalmente:
- `ls .cursorrules` retorna vazio.
- `wc -l docs/CONSTITUTION.md docs/process/refinement/planning_guidelines.md docs/process/autonomous/overview.md` mostra redução compatível com as remoções (ordem de grandeza: -50 a -80 linhas total).

### Ordem interna de execução

1. **15.1 + 15.2 + 15.3 em paralelo** — três docs grandes, edições disjuntas.
2. **15.4** — depende conceitualmente de 15.1/15.2/15.3 estarem coerentes (mesmo paradigma de fluxo único).
3. **15.5** — pode rodar em paralelo com 15.4.
4. **15.6** — independente.
5. **15.7** — depois de 15.6 (referência a `.cursorrules` em CLAUDE.md sai junto).
6. **15.8** — última, valida o todo.

### Acoplamentos com outros épicos

- **W-PROTO-10** (centralizar estados) — 15.2 toca o rótulo de `📋` na fonte que 10.1 vai centralizar. Ordem: **15 antes de 10** — vale a pena consolidar a fonte canônica depois das remoções.
- **W-PROTO-11** (faxina `quality_rules.md`) — 15.4 limpa "Cursor Background" antes da reorganização do 11.3. Ordem: **15 antes de 11**.
- **W-PROTO-13/14** (copilot-instructions) — não há sobreposição. Podem rodar em qualquer ordem.
- **W-PROTO-16** (consolidar comandos de validação) — 15.4 não toca o template canônico em `quality_rules.md` (linhas 105-128). Ordem: **15 ou 16 primeiro, indiferente**.

### Fora do escopo

- Refinamento autônomo nativo da plataforma (visão futura — W-MVP-REF-1).
- Integração Claude Code + OpenWebUI (em estudo, não desenhado).
- Limpeza de menções históricas em PRs mergeadas, commits, ou ROADMAPs de milestones já fechados.

---

#### ÉPICO W-PROTO-16: Consolidar template de "comandos de validação local"

**Milestone:** `PROTO-WORKFLOW-FAXINA`

**Objetivo:** o template "git fetch / checkout / venv / pytest / [run app]" aparece em 4 arquivos com formatos divergentes (`quality_rules.md` linhas 105-128, `implementation/delivery.md` linhas 14-44 e 92-149, `autonomous/delivery.md` linhas 57-81, `implementation/overview.md` linhas 60-72). Risco de drift médio prazo + carga cognitiva pra o agente que precisa decidir qual versão é canônica. Consolida em fonte única e substitui as cópias por referência.

**Status:** 🔍 Detalhes definidos

**Origem:** declarado originalmente como `W-MVP-DOC-2` em `MVP-WORKFLOW-DOC` (2026-04-29). Movido para `PROTO-WORKFLOW-FAXINA` no refinamento estratégico de 2026-04-29 (`claude/refine-workflow-stacks-6JOH6`) — 3 dos 4 arquivos com cópia são exatamente os que W-PROTO-11 e W-PROTO-15 já tocam, justificando antecipar.

**Dependências:** rodar **antes** de W-PROTO-11.3 (para que a reorganização do `quality_rules.md` parta da forma canônica congelada). Sem dependência com W-PROTO-15 (15.4 não toca o template canônico em linhas 105-128).

### Funcionalidades:

#### 16.1 Eleger fonte canônica em `quality_rules.md`

**Critério de aceite:** §"Comandos e Validação" de `docs/process/implementation/quality_rules.md` (linhas 98-137 hoje) é declarada fonte canônica do template. Recebe uma âncora explícita (cabeçalho `### Template de validação local`) com identificador navegável (`#template-de-validação-local`) referenciado pelos outros docs.

**Decisão de fonte:** `quality_rules.md` é a escolha por já ser o documento mais completo (variantes Linux/Mac vs Windows, observações de contexto sobre quando incluir cada passo, marcação explícita "Template de validação para mensagem final ao dev"). Alternativa rejeitada: `autonomous/delivery.md` é mais curto e contextualizado ao fluxo autônomo, mas tem inconsistência `.venv/` vs `venv/` e menos observações.

**Conteúdo canônico (mantém o bloco bash de linhas 106-128 hoje, com pequenos ajustes pós-W-PROTO-14):**

```bash
# 0. Fazer checkout da branch (SEMPRE incluir este passo)
git fetch origin
git checkout <branch-name>

# 1. Ativar ambiente virtual (se aplicável)
source .venv/bin/activate              # Linux/Mac
# .\.venv\Scripts\Activate.ps1         # Windows

# 2. Instalar/atualizar dependências (se requirements mudaram)
pip install -r requirements.txt

# 3. Testes unitários
python -m pytest tests/core/unit/ -v

# 4. Validação manual (script - RECOMENDADO!)
python scripts/core/<categoria>/validate_*.py

# 5. (se a branch mexeu em produto) Subir a app
# Stack detectada via products/<produto>/app/ — ver
# .github/copilot-instructions.md §"Stacks por produto" (W-PROTO-14)
```

Padronização incluída:
- `.venv/` (com ponto) — alinhado com `.github/copilot-instructions.md` (linhas 45-46).
- Passo 5 referencia W-PROTO-14 ao invés de hardcodar `streamlit run` — evita drift quando outros produtos forem adicionados.
- Observações pós-bloco (passos opcionais, ❌ NÃO usar PYTHONPATH, etc.) ficam abaixo do template como hoje.

**Arquivos a modificar:** `docs/process/implementation/quality_rules.md` (ajustes mínimos no bloco existente: padronizar `.venv/`, adicionar passo 5 referenciando W-PROTO-14, declarar âncora `### Template de validação local`).

#### 16.2 Substituir cópias por referência

**Critério de aceite:** os 3 arquivos com cópia divergente apontam pra fonte canônica em `quality_rules.md` via link, **sem repetir o bloco**.

**Arquivos a modificar:**

| Arquivo | Linhas-alvo | Ação |
|---|---|---|
| `docs/process/implementation/delivery.md` | 14-44 | mantém (é template de **formato de mensagem**, não bloco de validação) — sem mudança |
| `docs/process/implementation/delivery.md` | 92-149 | substitui o bloco PowerShell + exemplos genéricos (npm/docker/pytest) por: "Ver [template canônico em quality_rules.md](../implementation/quality_rules.md#template-de-validação-local). Para subir a app, detectar stack via [`.github/copilot-instructions.md` §Stacks por produto](../../../.github/copilot-instructions.md)." |
| `docs/process/autonomous/delivery.md` | 57-81 | substitui o bloco bash por: "RTE entrega o bloco pronto na PR seguindo [template canônico em quality_rules.md](../implementation/quality_rules.md#template-de-validação-local). Stack do passo 5 detectada via [§Stacks por produto](../../../.github/copilot-instructions.md)." |
| `docs/process/implementation/overview.md` | 60-72 | mantém (exemplo simplificado dentro do exemplo de checkpoint), adiciona nota de uma linha: "(Exemplo simplificado; template completo em [quality_rules.md](quality_rules.md#template-de-validação-local).)" |

**Validação:**
- `grep -n "git fetch origin\|git checkout" docs/process/implementation/delivery.md docs/process/autonomous/delivery.md` retorna 0 linhas em blocos de código (apenas em texto que referencie o template).
- Os 3 docs alvo abrem com link pra `quality_rules.md#template-de-validação-local`.
- `grep -n "Template de validação local" docs/process/implementation/quality_rules.md` retorna 1 linha (cabeçalho).

### Fora do escopo

- Funcionalidade originalmente esboçada como "2.3 Variantes por fluxo (manual vs autônomo)" — cai junto com W-PROTO-15 (não há mais dois fluxos pra distinguir).
- Variantes por stack (Streamlit vs Reflex) — vivem em `.github/copilot-instructions.md` via W-PROTO-14, referenciadas pelo passo 5 do template.
- Reescrever templates de teste em `docs/testing/` — sem sinal de atrito (público diferente: documentação de teste, não de validação local pré-merge).

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
