# Visão do Workflow de Desenvolvimento

## Missão

Estabelecer um sistema de fluxos de desenvolvimento autônomo, onde tarefas
de naturezas distintas — implementar, refinar, observar, auditar,
reorganizar — são executadas por fluxos especializados, orquestrados por
uma priorização que escolhe o trabalho do dia a partir de um backlog
curado. O operador humano valida o resultado; a execução roda sem
supervisão contínua.

A forma materializada dessa missão é uma **plataforma** que remove atrito
de decisão: o operador chega e o próximo passo já está esperando. Esta
visão cobre tanto o processo (princípios, fluxos, estágios) quanto a
plataforma (fila, kanban, chat focado, processos de fundo).

## Princípios

- **Fluxos múltiplos, não pipeline única.** Tarefas de naturezas distintas
  passam por fluxos especializados. Implementar código tem um fluxo;
  refinar visão em etapas tem outro; observar crescimento desordenado da
  arquitetura tem outro. O operador não força tudo no mesmo trilho.
- **Workflow é processo, não produto (atualmente).** O fluxo de
  desenvolvimento serve a todos os produtos do paper-agent (Revelar,
  Ensaio, Prisma Verbal, ...) sem ser nenhum deles. Ver "Horizonte" pra
  evolução futura.
- **Operador valida, não supervisiona.** O ideal é: o fluxo roda sem
  supervisão contínua, produz um artefato, e o humano decide aprovar ou
  devolver. Supervisão contínua é passo intermediário até o fluxo ser
  confiável.
- **Markdown é fonte da verdade.** Documentação, refinamento e decisões
  persistentes vivem em markdown no repo. A plataforma é camada de
  leitura e direcionamento — não estado próprio.
- **Evolução incremental.** Primeiro fluxo entra em POC antes do segundo
  ser desenhado. Sem arquitetura especulativa.
- **A aposta é na clareza.** Objetivos bem definidos tornam a implementação
  o passo mais simples do processo — não o mais crítico. Este sistema
  concentra esforço onde o impacto é maior: no pensamento que antecede a
  execução.

## Eixo de Estágios

Workflow segue o eixo "quem usa" do CONSTITUTION, adaptado para processo:

- **POC:** um fluxo funciona ponta a ponta, disparado manualmente pelo
  operador, sem priorização autônoma. Operador escolhe o que rodar.
  Fechado em `POC-WORKFLOW`.
- **Protótipo:** o fluxo da POC está estável, o operador usa no dia a dia
  real. Fluxos adicionais começam a aparecer. Ainda sem priorização
  autônoma. Milestones em curso e roadmap detalhado em
  [ROADMAP.md](ROADMAP.md).
- **MVP:** priorização autônoma rodando, materializada como POC mínimo da
  plataforma. Operador só valida. Detalhado abaixo em "Forma da
  Plataforma".

## Forma da Plataforma

A plataforma é a UI sobre o workflow — ferramenta de meta-workflow,
complementar às skills em `skills/`. Serve ao operador humano que
orquestra o sistema, não ao usuário final dos produtos. Não é produto do
super-sistema (Revelar, Ensaio e demais não a usam).

### Fila

Quando o operador entra, encontra uma **fila** no centro de gravidade.
Cada item é uma decisão pendente, com **tipos diferentes convivendo**:

- aprovação de avanço de refinamento;
- dúvida escalada pelo agente autônomo;
- PR pronta pra validar;
- proposta do proponente;
- relatório executivo "trabalhamos isso hoje, faz sentido?".

Cada tipo segue um shape mínimo comum (título, contexto, ação esperada).
O operador limpa a fila no próprio ritmo — não há SLA, há ordem.

A fila se autorregula por capacidade. Quando há por volta de vinte itens
pendentes, o autônomo para de criar novos e espera o operador abrir
espaço. O agente respeita o limite cognitivo do humano. A ordenação é
dimensão a refinar — eixos candidatos incluem importância, urgência,
severidade e tempo até a decisão expirar.

### Kanban

Ao lado da fila, um **kanban** dá a visão de estado: colunas pelos sete
estados de épico (🌱→🧭→📐→📋→🔍→🏗️→✅), agrupadas por milestone,
cards carregando labels de autonomia. É a leitura primária do sistema.

### Chat focado

Clicar num card abre o **chat focado** daquele épico — modo síncrono,
opcional, que o operador entra quando quer acelerar algo específico. O
chat tem dois shapes por dentro: condução de refinamento a partir do
estado atual, ou resposta a uma escalação pontual do agente. Em ambos,
chega com prompt pré-montado e contexto carregado — o operador não
monta nada.

### Interação por voz (médio prazo)

A plataforma conversa com o operador. O modelo canônico é o briefing
proativo: ao entrar, o sistema relata o estado do dia em linguagem
natural — decisões pendentes com contexto e impacto, atualizações de
implementações em curso, novas ideias ou propostas — e pergunta onde
focar. O operador responde em voz ou texto; a plataforma mapeia a
intenção para a ação correspondente.

A voz é o canal do briefing e do diálogo, o espaço onde a decisão se
forma. A execução tem botão; o pensamento tem voz.

## Processos de Fundo

Cada processo tem **cadência própria**:

- **Refinador autônomo (contínuo, com auto-regulação).** Pega épicos
  disponíveis e avança o máximo que consegue, tomando micro-decisões
  proporcionais ao estágio (POC tolera mais; MVP, menos). Antecipa
  decisões que vai precisar do humano e coloca na fila antes de travar,
  quando possível. Para limpo: encerra o ciclo, apresenta o resultado
  como item de fila, não deixa trabalho pendurado.
- **Proponente (1×/dia).** Orquestrador que olha para o sistema e propõe
  próximos movimentos. Não é capacidade nova — é um papel que combina as
  skills existentes (PM, EM, TL, PO, ...) para produzir sugestões. Uma
  vez por dia coloca uma proposta na fila. Exemplo: o operador menciona
  uma ideia interessante na visão do produto; o proponente cruza com o
  backlog e oferece um experimento ("posso fazer uma POC disso") ou
  aponta dependências ("se você decidir X, isso destrava Y"). Formato
  proativo "se você quiser, posso fazer isso".
- **Implementador (on-demand quando épico em 🔍).** Já existe (Claude
  Code Web hoje) e é invocado pela plataforma quando o épico está
  refinado. A plataforma é desacoplável do agente específico — Claude
  Code agora, outro amanhã.
- **Operador (no próprio ritmo, sem SLA).** Limpa fila como quiser. Tem
  preferência sobre o autônomo: mexeu num épico, o agente solta aquele.

## Substrato Técnico

- **Markdown no repo é fonte da verdade.** ROADMAP,
  `current_implementation.md`, refinamento estratégico — tudo persistente
  em markdown.
- **Plataforma é view derivada.** Fila, kanban e chat focado leem do
  markdown e do estado de PRs. Estado próprio só pra ordem da fila e
  claims do operador.
- **Banco efêmero não tem valor.** Estado runtime que some não justifica
  infra. Banco persistente (com auditoria, história) fica em aberto pra
  caso de uso concreto onde git não cobrir bem — discussão a retomar
  quando o sinal aparecer.

## Detecção de Claim do Operador

Operador sinaliza explicitamente que assumiu um épico — clique no card
do kanban, abertura de chat focado, ou label específica. Sem heurística
por commit ou atividade de branch. Ao receber o sinal, o autônomo solta
o épico até o operador devolver.

## Restrições Aceitas

- **Refinamento precede implementação, sem exceção.** A UI não permite
  burlar.
- **Autônomo é ousado, com guardrails por estágio.** Labels por épico
  permitem travar caso a caso.
- **Trabalho parcial: fechar e registrar.** Bloqueio vira item de fila
  (decisão pendente). Vale pra agente autônomo e pra refinamento
  estratégico — a regra é "não deixar trabalho órfão", não "perder se
  não terminar".
- **Operador tem preferência sobre o autônomo.** Mexeu num épico, o
  agente solta aquele.
- **Markdown é fonte da verdade.** A UI é camada de leitura e
  direcionamento.
- **Implementador é desacoplável** da plataforma.

## Distinção com Produtos

Produtos (Revelar, Ensaio, ...) são o que o paper-agent entrega ao usuário
final. Workflow é como o paper-agent é construído. Agentes do core
(Orquestrador, Metodologista, ...) são runtime do produto. Skills (Scrum
Master, QA, TL, PO, RTE, PM, EM, Cleanup) são ferramentas do workflow.

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

## Horizonte

- **Outros fluxos do workflow.** Observar crescimento desordenado da
  arquitetura, auditar débito técnico, reorganizar — esboçados na missão,
  mas fora do MVP. Backlog futuro, conforme sinal de necessidade.
- **Workflow como produto desacoplado multi-repo.** Tendência futura: a
  plataforma deixa de ser meta-workflow só do paper-agent e atende
  múltiplos repositórios. Implicações arquiteturais (fila por repo,
  dispatch sabe qual repo, skills versionadas por destino) ficam pra
  refinamento quando o sinal aparecer concretamente. Não estrutura
  nenhuma decisão atual.
- **Refinamento autônomo com autonomia crescente.** O refinador ganha
  capacidade de tomar pequenas decisões com base na filosofia, visão de
  produto e padrões acumulados do operador — chegando ao operador apenas
  quando a decisão realmente importa. A autonomia cresce com a maturidade
  dos produtos e a confiança que se acumula. Guardrails e ambientes de
  experimentação fazem parte dessa evolução — espaço para o sistema
  arriscar com segurança. A autonomia se expande passo a passo, guiada
  pela experiência real com os produtos.
