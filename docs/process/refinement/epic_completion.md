# Epic Completion Checklist

> **Propósito:** descreve como extrair conhecimento permanente de um épico implementado e enxugar o ROADMAP antes de marcá-lo como `✅ Implementado`. Checklist de **saída** da implementação, complementar ao de **entrada** em `docs/process/refinement/autonomous_readiness.md`.

## Contexto

ROADMAP descreve o futuro — épicos, critérios e detalhes que ainda não existem como código. Documentação de spec e arquitetura descreve o presente — o que o sistema é hoje. Quando um épico é implementado, parte do seu conteúdo migra para docs permanentes, parte some e o que sobra no ROADMAP é registro mínimo de que aquilo foi entregue.

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

Dois movimentos determinísticos em ordem: **enxugamento** (o que restou no épico é podado) e **transição de estado** (épico assume `✅ Implementado`).

> **Onde foi parar a Extração? (W-PROTO-7).** A extração de conhecimento permanente (novo padrão em `docs/ARCHITECTURE.md`/`core/docs/architecture/`, comportamento em `core/docs/agents/<agente>/`, notas em `.claudecode.md`) **deixou de ser passo do rito pós-merge** e virou responsabilidade da fase de implementação. Ato distribuído:
>
> - **TL identifica** o que merece virar conhecimento permanente (sub-seção 3.5 de `skills/tl/skill.md`) e registra item no bloco `## Extração pendente` de `current_implementation.md` ao aprovar cada funcionalidade. Item vazio é declarado explicitamente por épico.
> - **Dev executa** as edições, antes de iniciar a próxima funcionalidade ou no último commit do épico, marcando `[x]` no bloco "Extração pendente".
> - **RTE confirma** no Passo 1 (gate de entrada) que o bloco "Extração pendente" não tem `- [ ]` aberto. Se houver, aborta e devolve ao Dev.
>
> Quando o ciclo abaixo roda (pós-merge), todo conhecimento permanente já foi gravado.

### Enxugamento

- [ ] Épico no ROADMAP reduzido a: título, 1-2 linhas de resumo do que entregou, data de conclusão, links para docs permanentes e PRs relevantes.
- [ ] Funcionalidades individuais com critérios de aceite removidas do ROADMAP.
- [ ] Detalhes de execução (shapes, caminhos, mecanismos) removidos do ROADMAP.

### Transição de estado

- [ ] Épico marcado como `✅ Implementado` no ROADMAP somente após enxugamento completo.

> **Automação (W-PROTO-6).** Os dois passos acima — Enxugamento e Transição de estado — são **executados automaticamente** pela skill `skills/cleanup/skill.md` via `.github/workflows/milestone-cleanup.yml` no merge da PR de milestone. A Action carrega Claude Code, aplica as regras determinísticas a partir das variáveis `MILESTONE_ID`, `MERGED_PR_URL`, `MERGE_SHA` extraídas do evento, e commita o resultado (modo A direto em main; modo B via PR secundária se branch protection bloquear).
>
> **Fallback manual:** se a Action falhar (timeout, branch protection inesperada, erro de API, secret `ANTHROPIC_API_KEY` ausente), o dev pode rodar a mesma skill em sessão Claude Code Web sobre `main` pós-merge:
> 1. Carregar `skills/cleanup/skill.md` + `docs/process/current_implementation.md` (no commit do merge).
> 2. Passar manualmente as três variáveis (`MILESTONE_ID`, `MERGED_PR_URL`, `MERGE_SHA`).
> 3. Skill aplica os mesmos passos; dev autoriza o commit direto em main.
>
> A skill é idempotente — segunda execução é no-op nos blocos já enxugados, então rodar Action + fallback é seguro.

## Quando Aplicar

Ao final da implementação de um milestone, depois que o código foi mergeado e validado, e antes de transitar o status dos épicos no ROADMAP para `✅ Implementado`. Enquanto o ciclo não for completado, os épicos do milestone permanecem em `🏗️ Em andamento` — mesmo que o código já esteja em `main`.

> **Estado terminal da fase de implementação (W-PROTO-5):** a sessão autônoma encerra quando a RTE abre a PR com o body padronizado contendo a Seção 🎯 Validação. A revisão humana acontece **na própria PR** (dev cola a Seção 🎯 no Copilot, aprova e mergeia). **Não há mais "validação local antes da PR"** como gate de saída da fase de implementação. Comandos de validação local versionados em `validation-<milestone-id>.md` continuam disponíveis como ferramenta opcional do revisor.
>
> O ciclo descrito neste documento (extração + enxugamento + transição) acontece **depois do merge** da PR de milestone — é a "fase de higiene" — e pode ser acionado pela RTE em bulk para todos os épicos do milestone.

## Retroatividade

O ciclo aplica apenas a épicos fechados a partir da introdução deste processo. Épicos anteriormente marcados como concluídos permanecem no estado em que estão; não há migração retroativa.

> **Retroatividade de W-PROTO-7.** Épicos já em `🏗️ Em andamento` no momento da implementação de W-PROTO-7 ficaram sem o bloco "Extração pendente" no `current_implementation.md` (template já havia sido gerado). Não há aplicação retroativa: dev segue o rito antigo (extração manual no fechamento) para esses casos. A partir do primeiro milestone disparado pós-W-PROTO-7, o template gerado pela Scrum Master Skill já inclui o bloco — então TL/Dev/RTE seguem o novo contrato.

## Referência Cruzada

- **Entrada em implementação (critérios que o épico deve cobrir):** `docs/process/refinement/autonomous_readiness.md`
- **Saída da implementação (este documento):** extração + enxugamento + transição
- **Modelo completo de estados:** `docs/process/refinement/planning_guidelines.md`
