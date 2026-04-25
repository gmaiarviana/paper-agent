# Visão do Workflow de Desenvolvimento

## Missão

Estabelecer um sistema de fluxos de desenvolvimento autônomo, onde tarefas
de naturezas distintas — implementar, refinar, observar, auditar, reorganizar
— são executadas por fluxos especializados, orquestrados por uma priorização
que escolhe o trabalho do dia a partir de um backlog curado. O operador humano
valida o resultado; a execução roda sem supervisão contínua.

## Princípios

- **Fluxos múltiplos, não pipeline única.** Tarefas de naturezas distintas
  passam por fluxos especializados. Implementar código tem um fluxo;
  refinar visão em etapas tem outro; observar crescimento desordenado da
  arquitetura tem outro. O operador não força tudo no mesmo trilho.
- **Workflow é processo, não produto.** O fluxo de desenvolvimento não é
  um produto do super-sistema. Serve a todos os produtos (Revelar, Ensaio,
  Prisma Verbal, ...) sem ser nenhum deles.
- **Operador humano valida, não supervisiona.** O ideal é: o fluxo roda
  sem supervisão contínua, produz um artefato, e o humano decide
  aprovar ou devolver. Supervisão contínua é passo intermediário até o
  fluxo ser confiável.
- **Evolução incremental.** Primeiro fluxo entra em POC antes do segundo
  ser desenhado. Sem arquitetura especulativa.

## Eixo de Estágios

Workflow segue o eixo "quem usa" do CONSTITUTION, adaptado para processo:

- **POC:** um fluxo funciona ponta a ponta, disparado manualmente pelo
  operador, sem priorização autônoma. Operador escolhe o que rodar.
- **Protótipo:** o fluxo da POC está estável, o operador usa no dia a dia
  real. Fluxos adicionais começam a aparecer. Ainda sem priorização autônoma.
- **MVP:** priorização autônoma rodando. Claude Code Routine entrega
  proposta no inbox do operador uma vez por dia. Operador só valida.

## Distinção com Produtos

Produtos (Revelar, Ensaio, ...) são o que o paper-agent entrega ao usuário
final. Workflow é como o paper-agent é construído. Agentes do core
(Orquestrador, Metodologista, ...) são runtime do produto. Skills
(Scrum Master, QA, TL, PO, RTE, PM, EM, Cleanup) são ferramentas do workflow.

Skills não viram agentes do core. Agentes do core não viram skills. Estão
em eixos diferentes.

## Padrão Emergente: Skill em Action

Introduzido em W-PROTO-6 com `skills/cleanup/`. **Primeira skill** do
paper-agent que não é carregada por Claude Code Web durante o fluxo de
implementação, mas por uma GitHub Action (`.github/workflows/milestone-cleanup.yml`)
disparada por evento de repositório (no caso, merge de PR de milestone).

A skill em si (`skill.md`) permanece autocontida — pode rodar em Claude Code
Web manualmente como fallback. O que muda é o trigger: evento → Action →
Claude Code → skill, em vez de dev → Claude Code Web → skill.

**Quando usar o padrão:**
- Tarefa é determinística o suficiente pra rodar sem operador presente.
- Trigger é um evento de repositório (merge, push, schedule cron, label).
- Output é confinado a arquivos específicos (escopo de escrita explícito na skill).

**Quando NÃO usar:**
- Tarefa exige julgamento arquitetural ou negociação com dev (extração de
  conhecimento permanente é o exemplo canônico — TL/Dev decidem na fase de
  implementação, W-PROTO-7).
- Output é amplo o suficiente pra arriscar reescrita criativa.

Candidatas futuras (não desenhadas — virarão épicos quando houver sinal):
varredura de débito técnico em schedule, atualização de
`docs/process/sizing/history.jsonl` com `loc_actual` real após merge,
sinalização de drift em ROADMAPs. Cada uma vira épico próprio quando
oportunidade real surgir.

## Relação com o Formato de Tarefa Diária (visão de MVP)

Na visão de MVP, uma rotina diária executa uma tarefa autônoma e entrega
um relatório ao operador no formato:

> "Isso aqui foi o que trabalhamos hoje. Você acha que faz sentido? Para
> validar você deve fazer XYZ, segue os detalhes abaixo."

A tarefa do dia pode ser: implementação de algo refinado, refinamento de algo
em visão, detecção de débito técnico, proposta de reorganização, POC de uma
ideia nova, relatório de auditoria, qualquer coisa que agregue valor. O que
muda é o fluxo executado — não o formato do relatório.
