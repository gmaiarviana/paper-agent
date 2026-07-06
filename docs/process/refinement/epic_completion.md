# Epic Completion Checklist

> **Propósito:** descreve como extrair conhecimento permanente de um épico implementado e enxugar o ROADMAP antes de marcá-lo como `✅ Implementado`. Checklist de **saída** da implementação, complementar ao de **entrada** em `docs/process/refinement/autonomous_readiness.md`.

## Contexto

ROADMAP descreve o futuro — épicos, critérios e detalhes que ainda não existem como código. Documentação de spec e arquitetura descreve o presente — o que o sistema é hoje. Quando um épico é implementado, parte do seu conteúdo migra para docs permanentes, parte some e o que sobra no ROADMAP depende de **em que fase o milestone está**.

**Modelo de duas fases.** O bloco `#### ÉPICO` não sobrevive como stub permanente:

- **Milestone ainda aberto** (tem épico irmão em estado ≠ `✅`): o épico entregue transita para `✅` e fica como **stub mínimo** (título + status + `Entregue em:`). É a **janela de progresso intra-milestone** — mostra o que já shippou de um milestone multi-fatia sem inflar o ROADMAP.
- **Milestone inteiro fechado** (todos os épicos em `✅`): os blocos `#### ÉPICO` do milestone são **removidos** do ROADMAP. O registro cronológico de entrega passa a viver **só na declaração do milestone** (`### <MILESTONE_ID>` em `## 🎯 Milestones`), transitada para `✅` com `Implementado em: PR/sha/data`. Essa declaração é o **ledger** — grão de milestone, escaneável, in-repo. Conhecimento permanente (o que o sistema *é*) já foi extraído para `ARCHITECTURE.md`/`core-docs`/ADRs pela fase de implementação (W-PROTO-7); a declaração do milestone guarda o *quê/quando/qual PR*, que nenhuma dessas docs registra.

Por que não manter o stub `✅` para sempre: o detector de fila `detect_cleanup_items` sinaliza épico `✅` de milestone fechado como faxina pendente justamente para que ele saia do ROADMAP — stub permanente vira ruído fantasma na fila. O detector só ignora `✅` cujo milestone ainda está aberto (a janela legítima).

## Três Tipos de Conteúdo e Seus Destinos

### a) Objetivo e motivação

- Se o objetivo virou parte da visão do produto ou do core, já está refletido em `products/<produto>/docs/vision.md` ou `core/docs/vision/` — nada a migrar.
- Se foi apenas contexto de refinamento que justificou priorização, **some**.

### b) Critérios de aceite

- Se descrevem comportamento testável, viram testes automatizados ou scripts de validação. O código testado é o critério materializado.
- Se descrevem comportamento que o código sozinho não expressa (ex: "sistema provoca o usuário em tais situações"), viram doc de comportamento em `core/docs/agents/<agente>/` ou `products/<produto>/docs/ux/`.

### c) Detalhes de execução

- Caminhos de arquivo e shapes concretos são expressos pelo próprio código — **somem do ROADMAP**.
- Decisões arquiteturais relevantes para futuros leitores viram entrada em `docs/ARCHITECTURE.md` ou `core/docs/architecture/`.
- Instruções passo-a-passo, trade-offs já resolvidos e justificativas contextuais **somem**.

## Checklist de Fechamento

Dois momentos determinísticos, disparados por fases diferentes do milestone: **transição para `✅`** (ao entregar o épico — vira stub mínimo, janela intra-milestone) e **remoção do bloco** (quando o milestone inteiro fecha — bloco sai, declaração do milestone vira o ledger).

> **Onde foi parar a Extração? (W-PROTO-7).** A extração de conhecimento permanente (novo padrão em `docs/ARCHITECTURE.md`/`core/docs/architecture/`, comportamento em `core/docs/agents/<agente>/`, notas em `.claudecode.md`) **deixou de ser passo do rito pós-merge** e virou responsabilidade da fase de implementação. Ato distribuído:
>
> - **TL identifica** o que merece virar conhecimento permanente (sub-seção 3.5 de `skills/tl/skill.md`) e registra item no bloco `## Extração pendente` de `current_implementation.md` ao aprovar cada funcionalidade. Item vazio é declarado explicitamente por épico.
> - **Dev executa** as edições, antes de iniciar a próxima funcionalidade ou no último commit do épico, marcando `[x]` no bloco "Extração pendente".
> - **RTE confirma** no Passo 1 (gate de entrada) que o bloco "Extração pendente" não tem `- [ ]` aberto. Se houver, aborta e devolve ao Dev.
>
> Quando o ciclo abaixo roda (pós-merge), todo conhecimento permanente já foi gravado.

### Fase 1 — Entrega do épico (milestone ainda aberto)

- [ ] Épico no ROADMAP reduzido a stub mínimo: título, `**Status:** ✅ Implementado`, linha `**Entregue em:** PR <URL> (merge <sha>, <data>) — 1-2 linhas de resumo`.
- [ ] Funcionalidades individuais com critérios de aceite removidas do ROADMAP.
- [ ] Detalhes de execução (shapes, caminhos, mecanismos) removidos do ROADMAP.
- [ ] Enquanto o milestone tiver épico irmão em estado ≠ `✅`, o stub **permanece** como janela de progresso intra-milestone.

### Fase 2 — Fechamento do milestone (todos os épicos em `✅`)

- [ ] Blocos `#### ÉPICO` de todos os épicos do milestone **removidos** do ROADMAP.
- [ ] Declaração do milestone (`### <MILESTONE_ID>`) transitada para `✅`: campo `**Status dos épicos:**` com todos os épicos em `✅` e campo `**Implementado em:** PR <URL> (merge <sha>, <data>)`.
- [ ] Declaração do milestone **preservada** — é o ledger de entrega. Nunca é apagada.

> **Automação (W-PROTO-6, revisada).** As duas fases acima são **executadas pela skill** `skills/cleanup/skill.md` no **fold-in do dispatch seguinte** (`docs/process/autonomous/dispatch.md` §4.5): ao iniciar um milestone novo, o implementador detecta **todas** as faxinas pendentes (`python -m tools.workflow_platform.cleanup_trigger --list`), roda a skill por milestone e commita a faxina na branch da PR — entrando num diff revisado por humano. A skill transita `🔀`→`✅` (Fase 1) e, quando o milestone fica inteiro `✅`, remove os blocos de épico mantendo a declaração do milestone (Fase 2). (A automação original via GitHub Action `.github/workflows/milestone-cleanup.yml` foi **aposentada**: falhava por OIDC e não tinha revisão humana. O resolver determinístico que ela usava sobrevive em `tools/workflow_platform/cleanup_trigger.py`.)
>
> **Fallback manual (e milestone terminal):** o **último** milestone não tem "próximo dispatch" para carregar sua faxina. O dev roda a mesma skill em sessão Claude Code Web sobre `main` pós-merge:
> 1. Carregar `skills/cleanup/skill.md` + `docs/process/current_implementation.md` (no commit do merge).
> 2. Listar pendências via `cleanup_trigger --list`; passar as três variáveis por faxina (`MILESTONE_ID`, `MERGED_PR_URL`, `MERGE_SHA`).
> 3. Skill aplica os mesmos passos; dev autoriza o commit direto em main.
>
> A skill é idempotente — milestone já transitado tem épicos em `✅` (não `🔀`), então não reaparece em `--list`; milestone já fechado teve os blocos removidos, então não há o que repodar. Rodar fold-in + fallback é seguro.

## Quando Aplicar

Ao final da implementação de um milestone, depois que o código foi mergeado e validado, e antes de transitar o status dos épicos no ROADMAP para `✅ Implementado`. Enquanto o ciclo não for completado, os épicos do milestone permanecem em `🏗️ Em andamento` — mesmo que o código já esteja em `main`.

> **Estado terminal da fase de implementação (W-PROTO-5):** a sessão autônoma encerra quando a RTE abre a PR com o body padronizado contendo a Seção 🎯 Validação. A revisão humana acontece **na própria PR** (dev cola a Seção 🎯 no Copilot, aprova e mergeia). **Não há mais "validação local antes da PR"** como gate de saída da fase de implementação. Comandos de validação local em `docs/process/current_validation.md` (rotativo) continuam disponíveis como ferramenta opcional do revisor.
>
> O ciclo descrito neste documento (extração + enxugamento + transição) acontece **depois do merge** da PR de milestone — é a "fase de higiene" — e pode ser acionado pela RTE em bulk para todos os épicos do milestone.

## Retroatividade

O ciclo de **transição** (Fase 1) aplica apenas a épicos fechados a partir da introdução deste processo. Já a **remoção de bloco no fechamento do milestone** (Fase 2) foi aplicada **retroativamente uma vez** aos milestones já fechados quando o modelo de duas fases foi introduzido — o backfill único removeu os stubs `✅` acumulados dos milestones fechados do workflow e do ensaio, mantendo cada declaração de milestone como ledger. A partir daí, todo milestone que fecha segue a Fase 2 no fold-in.

> **Nota:** a antiga regra "não há migração retroativa" valia para o modelo de stub permanente. Sob o modelo de duas fases, stub `✅` de milestone fechado é ruído (o `detect_cleanup_items` o sinaliza como faxina) — por isso o backfill único foi feito em vez de preservar o passado inconsistente.

> **Retroatividade de W-PROTO-7.** Épicos já em `🏗️ Em andamento` no momento da implementação de W-PROTO-7 ficaram sem o bloco "Extração pendente" no `current_implementation.md` (template já havia sido gerado). Não há aplicação retroativa: dev segue o rito antigo (extração manual no fechamento) para esses casos. A partir do primeiro milestone disparado pós-W-PROTO-7, o template gerado pela Scrum Master Skill já inclui o bloco — então TL/Dev/RTE seguem o novo contrato.

## Referência Cruzada

- **Entrada em implementação (critérios que o épico deve cobrir):** `docs/process/refinement/autonomous_readiness.md`
- **Saída da implementação (este documento):** extração + transição para `✅` (Fase 1) + remoção de bloco no fechamento do milestone (Fase 2)
- **Modelo completo de estados:** `docs/process/refinement/planning_guidelines.md`
