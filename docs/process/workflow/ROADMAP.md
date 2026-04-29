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

### PROTO-WORKFLOW-FILA

- **Objetivo:** plataforma ganha fila reativa de decisões + chat focado
  por item + auto-regulação básica. Sinais óbvios do repo (PR aberta,
  épico chegou em estado-gatilho, branch parou) viram itens de fila por
  regra determinística — sem agente proativo ainda. Operador atende na
  ordem que escolher; ordenação simples (recência ou manual).
- **Estágio:** Protótipo
- **Épicos agrupados:** W-PROTO-FILA-1, W-PROTO-FILA-2, W-PROTO-FILA-3
- **Dependências de core:** nenhuma; depende de
  PROTO-WORKFLOW-PLATAFORMA (kanban e scaffold como base)
- **Branch associada:** `milestone/proto-workflow-fila`
- **Status dos épicos:** W-PROTO-FILA-1 📐, W-PROTO-FILA-2 📐,
  W-PROTO-FILA-3 📐.
- **Tensões para refinamento estratégico:**
  - **(a) Quem cria itens "PR pra revisar"?** Inclinação: RTE no
    mesmo passo em que abre PR (W-PROTO-5 estendido). Alternativa:
    observador da plataforma detecta PR aberta via GitHub API.
  - **(b) Auto-regulação por capacidade (~20 itens).** No Protótipo,
    auto-regulação é simples (alerta visual ao se aproximar do limite)
    — gatilho duro de pausa só ganha sentido no MVP, quando há agente
    proativo criando itens.
  - **(c) Reconstrução da fila se plataforma cair.** Varrer markdown
    + estado de PRs deve reconstruir a fila deterministicamente —
    teste prático do princípio "markdown é fonte da verdade".
- **Nota:** milestone declarado em 2026-04-28 — absorve o conteúdo
  do antigo MVP-WORKFLOW-PLATAFORMA, reposicionado como Protótipo
  porque é fila **reativa** (regra determinística), não curada por
  agente. Curadoria por porta-voz vive no MVP.

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

**Objetivo:** regras determinísticas convertem sinais óbvios do repo em itens de fila com shape padronizado — PR aberta, épico chegou em estado-gatilho, branch parou. Sem julgamento agentic; só mapeamento sinal→item.

**Status:** 📐 Funcionalidades esboçadas

**Dependências:** PROTO-WORKFLOW-PLATAFORMA (scaffold e kanban como base)

### Funcionalidades (esboço):
- **1.1 Shape mínimo de item de fila** — título, contexto, tipo (dispatch/review/escalação), ação esperada, ponteiro pra origem (épico, PR, branch).
- **1.2 Detecção de eventos** — monitora ROADMAPs (mudanças de estado) + estado de PRs + branches abertas; gera itens correspondentes.
- **1.3 Reconstrução determinística** — varrer markdown + estado de PRs reconstrói a fila do zero (teste prático do princípio "markdown é fonte da verdade").

---

#### ÉPICO W-PROTO-FILA-2: Exibição da fila + chat focado por item

**Milestone:** `PROTO-WORKFLOW-FILA`

**Objetivo:** operador vê fila reativa na plataforma e, ao clicar num item, abre sessão com contexto pré-montado para aquele item.

**Status:** 📐 Funcionalidades esboçadas

**Dependências:** W-PROTO-FILA-1 (itens existentes)

### Funcionalidades (esboço):
- **2.1 View da fila** — lista ordenada (recência ou manual no Protótipo); cards com tipo, título, ação esperada.
- **2.2 Montagem de contexto por tipo** — pra dispatch: milestone + dispatch.md; pra refinamento: épico + pack inicial; pra revisão: PR + épicos do milestone.
- **2.3 Abertura de chat com contexto** — prompt pré-montado pronto para iniciar a sessão correspondente.

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

> **Épicos órfãos da Fase Protótipo (sem milestone declarado).** Saneamento documental do `docs/process/` levantado em revisão de 2026-04-28 (branch `claude/review-process-directory-J1v8v`). Aguardam agrupamento estratégico em milestone(s) — candidatos a balaio único ou split por afinidade (faxina de docs vs. operacionalização de stack).

#### ÉPICO W-PROTO-10: Centralizar definição dos estados de épico

**Objetivo:** eliminar drift entre as quatro cópias da lista canônica de estados de épico em `docs/process/refinement/planning_guidelines.md` (§"Estados de Refinamento", §"Categorias de Épicos", §"📍 PRÓXIMOS PASSOS", e templates). Drift entre cópias gerou as 3 contradições C corrigidas em 2026-04-28; próxima skill que ler cópia desatualizada repete o erro.

**Status:** 📐 Funcionalidades esboçadas

### Funcionalidades (esboço):
- **10.1 Bloco canônico único** — escolher uma seção de `planning_guidelines.md` como fonte da verdade (definição + transição + responsável); demais viram referências curtas com âncora.
- **10.2 Limpeza de drift cross-doc** — varrer `vision.md`, `starter.md`, `autonomous/overview.md`, `autonomous/workflow.md` e substituir definição duplicada por link.

---

#### ÉPICO W-PROTO-11: Faxina de `quality_rules.md`

**Objetivo:** tirar de `docs/process/implementation/quality_rules.md` o que não é regra de processo do fluxo. Hoje (~400 linhas) mistura princípios + lessons learned do produto Revelar + tutorial defensivo de git pra Windows. Skill que segue esse doc pode aplicar regra fora de contexto.

**Status:** 📐 Funcionalidades esboçadas

### Funcionalidades (esboço):
- **11.1 Apagar §"Verificação de Conflitos e Prevenção de Perda de Trabalho"** (~140 linhas) — tutorial defensivo de git nasceu de incidente concreto e ficou; não é regra de qualidade do processo.
- **11.2 Mover §"Diretrizes Aprendidas em Produção"** (~45 linhas) — lessons learned específicas de sistemas conversacionais com LLMs do Revelar; destino: `products/revelar/docs/` ou `core/docs/agents/`.
- **11.3 Reorganizar o que sobra** — princípios + regras anti-redundância + comandos de validação numa ordem coerente, sem grab-bag.

---

#### ÉPICO W-PROTO-12: Cindir `implementation/overview.md`

**Objetivo:** separar regras de interação com dev (genéricas, valem pros dois fluxos) de regras de validação híbrida (específicas do fluxo manual via Cursor). Hoje o doc mistura os dois e a nota corretiva de linha 88-91 já admite o problema. Agente leitor tem que filtrar mentalmente o que aplica ao contexto.

**Status:** 📐 Funcionalidades esboçadas

### Funcionalidades (esboço):
- **12.1 Extrair "Validação Híbrida" para arquivo próprio** — escopo: fluxo manual; conteúdo: validação automática (sintaxe, imports), comandos por checkpoint.
- **12.2 Manter no overview só regras de interação** — aprovação explícita, papel do agente, sinais de aprovação válidos (referência canônica deduplicada em `claude/review-process-directory-J1v8v`).
- **12.3 Reapontar referências** — ajustar links em `workflow.md`, `delivery.md`, `blockers.md`.

---

#### ÉPICO W-PROTO-13: Faxina do `copilot-instructions.md` (concisão pra agente)

**Objetivo:** aplicar princípio "documentação para agente é concisa, não defensiva" — agente trabalha do traceback, não consulta catálogo de erros típicos. Doc hoje carrega seções defensivas que confundem o Copilot ao invés de ajudar.

**Status:** 📐 Funcionalidades esboçadas

### Funcionalidades (esboço):
- **13.1 Apagar §"Erros típicos e orientação"** — agente lê traceback e age; não consulta lista pré-cozida.
- **13.2 Apagar §"Checklist mínimo de POC do Ensaio"** — Ensaio migrou para Reflex (ADR 001); checklist baseado na app antiga não tem mais função e o Modo A já cobre validação por critérios extraídos do `current_implementation.md`.
- **13.3 Varredura de outros padrões defensivos** — verificar se §"Operação Windows / macOS / Linux" e §"Quando o dev disser 'deu erro'" carregam regras ainda ativas ou são entulho.

---

#### ÉPICO W-PROTO-14: Operacionalizar Reflex no fluxo de validação do Copilot

**Objetivo:** o Ensaio migrou para Reflex no Protótipo (ADR 001 de 2026-04-25), mas `copilot-instructions.md` ainda manda Streamlit pros dois produtos. Validação de branches do Ensaio quebra ou roda com comando errado.

**Status:** 📐 Funcionalidades esboçadas

**Dependências:** input do dev sobre comandos exatos de Reflex no ambiente Windows (stack alvo do Copilot).

### Funcionalidades (esboço):
- **14.1 Detecção de stack por produto** — tabela explícita: `products/revelar/app/**` → Streamlit; `products/ensaio/app/**` → Reflex; futuros produtos com nota de detecção.
- **14.2 Comando de subida do Reflex** — comando padrão validado (foreground, foco no log, encerramento limpo).
- **14.3 Liberação de portas por stack** — range hardcoded hoje (8501-8503) precisa cobrir as portas do Reflex.

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

> **Épicos órfãos da Fase MVP (sem milestone declarado).** Saneamento documental levantado em 2026-04-28; aguardam agrupamento estratégico.

#### ÉPICO W-MVP-DOC-1: Quebrar `planning_guidelines.md` por responsabilidade

**Objetivo:** o arquivo (634 linhas) absorveu definição de estados, processo de sessão, glossário, anti-padrões, exemplos, templates de épico/funcionalidade. Cabe num doc só, mas a leitura cansa e a navegação é ruim.

**Status:** 📐 Funcionalidades esboçadas

### Funcionalidades (esboço):
- **1.1 Definir corte natural** — candidatos: definições de estado / processo de sessão / templates / anti-padrões. Critério: cada arquivo respondendo uma pergunta única.
- **1.2 Mover seções para arquivos novos** — preservar links externos via redirect (nota no original) ou ajuste sistemático cross-repo.
- **1.3 `planning_guidelines.md` vira índice** — overview curto + apontadores para os arquivos derivados.

---

#### ÉPICO W-MVP-DOC-2: Consolidar templates de "comandos de validação local"

**Objetivo:** o bloco "git fetch / checkout / venv / pytest / streamlit run" aparece em 3-4 lugares (`implementation/delivery.md`, `quality_rules.md`, `autonomous/delivery.md`, `implementation/overview.md`) com formatos divergentes. Risco de drift médio prazo.

**Status:** 📐 Funcionalidades esboçadas

### Funcionalidades (esboço):
- **2.1 Identificar template canônico** — escolher um arquivo como fonte; demais referenciam por âncora.
- **2.2 Eliminar duplicação verbatim** — substituir blocos por links.
- **2.3 Variantes por fluxo** — manual (dev cria PR) vs autônomo (dev valida em PR aberta) ficam como subseções do canônico.

---

## 💡 Ideias Futuras

Itens que ainda não justificam virar épico — registrados aqui pra não perder, viram épico quando houver sinal real de atrito.

- **Mover `language_guidelines.md` para fora de `docs/process/`.** Guia de bilinguismo (PT-BR para mensagens, EN para código) é regra do código todo do paper-agent, não específica do processo de implementação. Destino candidato: `docs/` raiz ou `core/docs/`. Vira épico quando alguém procurar fora de `process/` e não achar.

- **Decidir destino de `refinement/overview.md` e `workflow/README.md`.** Índices curtos que repetem informação dos arquivos pra que apontam. Custo zero pra leitor familiarizado; ganho marginal de apagar. Vira épico só se a navegação da pasta `process/` for repensada.

---

## 📚 Observações

**Regra:** fluxo manual exige épico em `📋 Critérios definidos`;
fluxo autônomo exige `🔍 Detalhes definidos`.

Os milestones da fase Protótipo `PROTO-WORKFLOW-ENCERRAMENTO`,
`PROTO-WORKFLOW-DOC` e `PROTO-WORKFLOW-AJUSTES` foram mergeados em
sequência (PRs #83, #90 e #93). `PROTO-WORKFLOW-PLATAFORMA` está em
`🔍 Detalhes definidos` — apto ao fluxo autônomo. `PROTO-WORKFLOW-FILA`
(absorve o conteúdo do antigo MVP-WORKFLOW-PLATAFORMA, reposicionado
como Protótipo) tem épicos em `📐` aguardando refinamento estratégico
após `PROTO-WORKFLOW-PLATAFORMA` fechar. Os milestones MVP
(`MVP-WORKFLOW-REFINAMENTO` e `MVP-WORKFLOW-PROPONENTE`) têm épicos
em `📐` aguardando refinamento estratégico após `PROTO-WORKFLOW-FILA`
fechar.

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
