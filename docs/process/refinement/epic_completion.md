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

Três movimentos em ordem: **extração** (conhecimento permanente sai do épico), **enxugamento** (o que restou no épico é podado), **transição de estado** (épico assume `✅ Implementado`).

### Extração

- [ ] Comportamento novo de agente documentado em `core/docs/agents/<agente>/`.
- [ ] Decisão arquitetural registrada em `docs/ARCHITECTURE.md` ou `core/docs/architecture/`.
- [ ] Novo fluxo ou padrão documentado no doc técnico relevante.
- [ ] Alteração de visão atualizada em `products/<produto>/docs/vision.md` ou `core/docs/vision/`.

### Enxugamento

- [ ] Épico no ROADMAP reduzido a: título, 1-2 linhas de resumo do que entregou, data de conclusão, links para docs permanentes e PRs relevantes.
- [ ] Funcionalidades individuais com critérios de aceite removidas do ROADMAP.
- [ ] Detalhes de execução (shapes, caminhos, mecanismos) removidos do ROADMAP.

### Transição de estado

- [ ] Épico marcado como `✅ Implementado` no ROADMAP somente após extração e enxugamento completos.

## Quando Aplicar

Ao final da implementação de um épico, depois que o código foi mergeado e validado, e antes de transitar o status no ROADMAP para `✅ Implementado`. Enquanto o ciclo não for completado, o épico permanece em `🏗️ Em andamento` — mesmo que o código já esteja em `main`.

## Retroatividade

O ciclo aplica apenas a épicos fechados a partir da introdução deste processo. Épicos anteriormente marcados como concluídos permanecem no estado em que estão; não há migração retroativa.

## Referência Cruzada

- **Entrada em implementação (critérios que o épico deve cobrir):** `docs/process/refinement/autonomous_readiness.md`
- **Saída da implementação (este documento):** extração + enxugamento + transição
- **Modelo completo de estados:** `docs/process/refinement/planning_guidelines.md`
