# Refactor Backlog — Fluxo de Desenvolvimento

> **📌 Localização:** `docs/process/refactor-backlog.md`
> **📌 Escopo:** backlog de melhorias do **processo de desenvolvimento autônomo** — skills, `docs/process/`, convenções de fluxo, templates operacionais.
> **📌 Não confundir com:**
> - `docs/ROADMAP.md` — épicos do **core** do produto.
> - `products/<produto>/ROADMAP.md` — épicos dos **produtos**.
>
> Este arquivo trata apenas do ferramental de desenvolvimento.

---

## Dívida aberta da reforma de milestone

A reforma do fluxo de desenvolvimento (branch `refactor/fluxo-milestone`) introduziu **milestone** como unidade de entrega do fluxo autônomo, criou as skills **PM** e **EM**, renomeou `planning → scrum-master` e `validation → rte`, e estruturou `docs/process/sizing/`. O escopo executado até o merge em `main` foi: **M1 + M2 + M3a + M3b + wrap-up mínimo**.

O restante da reforma foi pausado e documentado abaixo como dívida aberta. Retomar em sessões futuras.

### M4-restante — Fluxo autônomo por milestone (parcial)

**Objetivo:** reescrever o fluxo autônomo para operar sobre **milestone** (com N épicos) em vez de **funcionalidade** (X.Y), consolidar gates silenciosos e notificação única pela RTE no fim do milestone.

**O que falta fazer:**

- **`docs/process/autonomous/dispatch.md`** — substituir template de 40 linhas por padrões de dispatch em linguagem natural ("implementa a POC do Ensaio", "refina o Protótipo do Revelar", etc.). Documentar parser informal que Claude Code Web aplica.
- **`docs/process/autonomous/workflow.md`** — reescrever além do diagrama: seções dos gates hoje descrevem decisão per-funcionalidade; devem passar a descrever loop por épico dentro do milestone, com gates QA/TL/PO operando por funcionalidade dentro do loop, e o milestone fechando via RTE apenas no fim.
- **`docs/process/autonomous/overview.md`** — reescrever "dispara pela manhã / valida à noite" para refletir notificação única no fim do milestone. Atualizar tabela manual × autônomo.
- **`docs/process/autonomous/delivery.md`** — dev valida milestone inteiro, não funcionalidade. Mensagem final RTE consolida os N épicos.
- **`docs/process/autonomous/session_conventions.md`** — §2 "um commit por épico" deve explicitar que um milestone pode ter N commits e a branch só é "pronta" quando o último commit do último épico cair. Convenção de branch: `feature/X.Y-nome` → `milestone/<id-em-caixa-baixa>`.
- **Política de escalação de 3 reprovações** — descrição atualizada: 3 reprovações consecutivas no mesmo gate do mesmo épico aborta o milestone inteiro (decisão fixada da reforma).
- **Conteúdo operacional dos `skill.md`** — `skills/scrum-master/skill.md`, `skills/qa/skill.md`, `skills/tl/skill.md`, `skills/po/skill.md`, `skills/rte/skill.md`: ainda falam em "funcionalidade X.Y" como unidade. Reescrever para operar dentro do loop por épico de um milestone. Atualizar pré-checagens de cada um para consumir o novo shape de `current_implementation.md` (aninhado milestone → épicos → funcionalidades → gates).
- **Template de `current_implementation.md`** — em `skills/scrum-master/skill.md`, migrar do shape per-funcionalidade para o shape aninhado declarado na sessão 1 da reforma (ver `docs/process/current_implementation.md` atual como referência viva). Template deve acomodar N épicos e, dentro de cada épico, N funcionalidades com seus gates QA/TL/PO. Markers `[PM]` e `[EM]` já estão no topo da lista desde o wrap-up de M3b.

### M5 — Refinamento autônomo dentro da branch

**Objetivo:** atualizar `docs/process/refinement/` para distinguir, ao longo do corpo principal do texto, as duas modalidades de refinamento (estratégico via Claude Web, tático via PM skill) em vez de apenas um callout isolado.

**Arquivos a atualizar:**

- **`docs/process/refinement/planning_guidelines.md`** — promover o callout sobre estratégico vs tático (adicionado em M1) a seção própria; adicionar sub-seção "Processo de Refinamento Autônomo (PM Skill)" como irmã de "Processo de Refinamento com Claude Web"; revisar os exemplos de refinamento para cobrir ambos os caminhos.
- **`docs/process/refinement/starter.md`** — deixar explícito que o pack inicial de 6 arquivos cobre apenas o refinamento estratégico via Claude Web. Adicionar breve seção "Contexto consumido pela PM skill" (PM tem acesso ao repo, não precisa do pack).
- **`docs/process/refinement/overview.md`** — atualizar "Quando usar" para refletir os dois contextos.
- **`docs/process/refinement/autonomous_readiness.md`** — ajuste pontual deixando claro que o checklist agora é consumido pela PM skill como programa executável (além de guia humano).
- **`docs/process/refinement/epic_completion.md`** — ajuste pontual: ciclo pode ser acionado pela RTE ao fechar milestone, em bulk para todos os épicos do milestone.

### M6 — Integrações e cross-references

**Objetivo:** fechar pontas periféricas para que o grep do repositório fique coerente e a reforma não deixe ponteiros quebrados.

**Arquivos a atualizar:**

- **`docs/CONTEXT_INDEX.md`** — TEMA "Desenvolvimento e Processo" deve listar as 7 skills (PM, EM, Scrum Master, Dev, QA, TL, PO, RTE) e referenciar `docs/process/sizing/`. Adicionar linha no MAPA RÁPIDO DE DECISÃO para "Implementar milestone de produto → `docs/process/autonomous/`".
- **`docs/ARCHITECTURE.md`** — seção "Estrutura do Projeto" lista `skills/` com 5 entradas; atualizar para 7 e adicionar `docs/process/sizing/`.
- **`.github/copilot-instructions.md`** — Modo A deve referenciar o shape novo de `current_implementation.md` (ciclo de milestone); exemplo "C-ENSAIO-2" pode ser substituído por "POC-ENSAIO" ou similar.
- **`README.md`** — linha 195 ("refinement, implementation, autonomous") pode ganhar menção a `sizing/` se oportuno.
- **`docs/process/implementation/overview.md`** — adicionar nota curta no topo declarando que o fluxo manual opera em funcionalidade/épico e é complementar ao autônomo (que opera em milestone).
- **Varredura final** — `grep -rn` por "Planning Skill", "Validation Skill", "planning/skill.md", "validation/skill.md", "dispatch.md" (só as menções operacionais), "feature/X.Y-" e corrigir o que sobrou após M4.

### Micro-dívidas detectadas ao longo da reforma

Pequenos itens de consistência textual que não bloqueiam o merge mas devem ser resolvidos junto com M6:

- **Typo `IImplementado`** em algum ponto do texto pós-M1 (apontado pelo dev em feedback; manter em M6 para não fragmentar commits).
- **`docs/process/refinement/planning_guidelines.md` linha 32** fala em "5 arquivos essenciais" enquanto `starter.md` define o pack com 6. Inconsistência anterior à reforma; saneamento em M5 ou M6.
- **`products/revelar/README.md:21`** fala em "Épicos 1-16" mas o ROADMAP só lista 1 e 2 ativos (concluídos foram podados). Fora do escopo desta reforma, mas vale registrar para saneamento do README do Revelar fora-da-reforma.

---

## Outras melhorias (a serem trazidas em próximas sessões)

_A preencher. Este espaço absorve ideias de melhoria de processo que surgirem após o merge da reforma de milestone._

---

## Como usar este backlog

- Itens de dívida da reforma de milestone permanecem aqui até que uma sessão dedicada os atake.
- Ao disparar uma sessão para retomar M4/M5/M6, referenciar explicitamente o bloco daqui para delimitar o escopo.
- Itens novos entram sob "Outras melhorias" e sobem para seção de trabalho ativo quando priorizados.
- Quando um bloco fecha, resumir em 1-2 linhas e mover para uma seção "Concluído recentemente" (criar quando acumular).
