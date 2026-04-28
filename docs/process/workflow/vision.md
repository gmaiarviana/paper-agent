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
- **Pacing por bandwidth do operador.** O autônomo não acelera o que o
  operador não consegue revisar com qualidade. Refinamento é delicado —
  saltos pequenos e revisões cabíveis na atenção do dia previnem que a
  benção da automação vire maldição da auditoria.
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
  real. **Plataforma reativa entra em cena**: kanban + fila populada por
  sinais óbvios do repo (PR aberta, épico chegou em estado-gatilho, branch
  parou) + chat focado por item + ações contextuais. Ainda sem agentes
  proativos — sinais viram itens de fila por regra, não por julgamento.
  Milestones em curso e roadmap detalhado em [ROADMAP.md](ROADMAP.md).
- **MVP:** priorização autônoma rodando — fluxo de refinamento autônomo
  standalone disponível, proponente orquestrando, porta-voz curando
  atenção. Operador só valida. Detalhado abaixo em "Papéis" e "Fluxos".

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

A fila tem dois modos conforme o estágio. **No Protótipo**, é populada
**reativamente** — regras determinísticas convertem sinais óbvios do repo
(PR aberta, épico chegou em estado-gatilho, branch parou) em itens.
Operador atende na ordem que escolher; ordenação é simples (recência ou
manual). **No MVP**, o porta-voz passa a curar a fila — ordena, agrupa,
filtra, escala apenas o que escapa do seu repertório. Ver "Papéis"
abaixo.

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

## Papéis

Três papéis ativos no sistema. Operador é humano; proponente e porta-voz
são agentes que aparecem no MVP. Refinamento e implementação **não** são
papéis — são fluxos (próxima seção).

### Operador (humano, no próprio ritmo)

Limpa fila como quiser, sem SLA. Tem preferência sobre o autônomo: mexeu
num épico, o agente solta aquele. Valida o trabalho — não supervisiona
continuamente.

### Proponente (orquestrador, proativo, ~1×/dia)

Olha o sistema (visão, backlog, ROADMAPs, sinais do dia) e propõe o
próximo movimento. **Não é agente novo** — é um papel que escolhe e
dispara o fluxo apropriado, na prioridade certa. Combina as skills
existentes (PM, EM, Scrum Master, QA, TL, PO, RTE, Cleanup) para produzir
trabalho útil.

Prioridade de proposta:

1. **Implementar o que está refinado** (épico em 🔍 esperando dispatch).
2. **Refinar o que ainda não está refinado** (épico pré-🔍 com sinal de
   prontidão).
3. **Transformar item da visão em backlog** (ideia mencionada vira épico
   novo) — condicional ao operador autorizar.

Exemplos do que propõe:

- "Implementar o épico X que está em 🔍" (prioridade máxima)
- "Refinar o épico Y que está em 📋" (refinamento tático)
- "Fazer uma POC dessa ideia que você mencionou" (proposta proativa)
- "Se você decidir X, isso destrava Y" (mapeamento de dependência)
- "Trabalhamos isso hoje, faz sentido?" (relatório executivo)

Quando o fluxo disparado trava, o proponente **chama o porta-voz** com
contexto do bloqueio e pede recomendação. Não escala diretamente ao
operador — o porta-voz decide se desbloqueia ou escala.

### Porta-voz (curador de atenção)

Filtro inteligente entre o sistema e o operador. Recebe consultas do
proponente em bloqueios; lê estado-do-mundo (branches abertas, PRs,
claims); cura a fila do operador. **Tem agência decisória** sobre
bloqueios pequenos, baseada em filosofia, visão e orientações
acumuladas.

Funções:

- **Filtra**: traz apenas o que foi acordado que precisa ser só com o
  operador.
- **Prioriza**: ordena fila por importância/urgência/severidade/
  expiração.
- **Agrupa**: junta perguntas correlatas pra não fragmentar atenção.
- **Resolve antes de escalar**: usa repertório acumulado (filosofia,
  visão, orientações do operador) para destravar bloqueios pequenos sem
  chamar o humano.
- **Temporiza**: decide quando interromper — atenção certa na hora
  certa, deixar fluir ao máximo.

Quando o porta-voz não tem repertório pra decidir, escala. A resposta
do operador alimenta repertório novo (markdown como sempre) que o
porta-voz consulta na próxima vez.

## Fluxos

Cada tipo de trabalho tem um fluxo especializado, executado via
sequência de skills. Fluxos **não são papéis** — são modos de trabalho.
Disparados pelo proponente (autônomo) ou pelo operador (manual).

### Refinamento

Avança épico em estados pré-execução até alvo declarado (normalmente
🔍). Skills: **PM** (refinamento tático), **EM** (preflight de tamanho).

Princípios do refinamento autônomo (chega no MVP):

- **Saltos pequenos.** Agente avança um estado por vez (ex.: 📐→📋),
  comita progresso na branch, e segue. Não tenta saltar 🌱→🔍 numa só
  passada.
- **Branch persiste por épico em refinamento.** Múltiplas sessões podem
  comitar estado intermediário. Bloqueio = commit do estado parcial +
  proponente avisa porta-voz.
- **PR por épico ao concluir.** Quando o épico chega no alvo com
  clareza, abre-se PR. Default: 1 PR por épico (granularidade que cabe
  na bandwidth de revisão do operador). Exceção declarada: PR cobre
  épicos correlatos do mesmo milestone quando coerência exige —
  registrado no body da PR. Diferente da implementação, que mantém PR
  por milestone (modelo consolidado pela RTE).

Hoje a PM skill só roda como sub-passo do dispatch de implementação
(carregada antes da EM se há épico pré-🔍 no milestone) — é resíduo de
quando os fluxos eram unidos. O fluxo de refinamento standalone vai
desacoplar isso.

### Implementação

Avança épico em 🔍 até ✅. Skills: **Scrum Master**, **QA**, **TL**,
**PO**, **RTE**. Já existe e funciona — Claude Code Web é o executor
atual. A plataforma é desacoplável do agente específico — Claude Code
agora, outro amanhã.

### Encerramento

Faxina pós-merge. Skills: **Cleanup**. Já existe — disparado por GitHub
Action quando PR de milestone é mergeada (ver "Padrão Emergente: Skill
em Action" abaixo).

### Futuros (não desenhados)

Outros fluxos esperados conforme sinal de necessidade: revisão de
arquitetura para débito técnico, auditoria de boas práticas,
verificação de segurança, criação de cobertura de teste, análise de
uso de componentes para modularizar. Cada fluxo novo é uma sequência
de skills, possivelmente reusando as existentes ou adicionando novas.
Cada vira épico próprio quando a oportunidade real surgir.

## Substrato Técnico

- **Markdown no repo é fonte da verdade.** ROADMAP,
  `current_implementation.md`, refinamento estratégico — tudo persistente
  em markdown.
- **Plataforma é view derivada.** Fila, kanban e chat focado leem do
  markdown e do estado de PRs. Estado próprio só pra ordem da fila e
  claims do operador.
- **Branch persiste por épico em fluxo ativo.** Sessões múltiplas
  (refinamento ou implementação) comitam estado intermediário na branch
  do épico/milestone. PR só na conclusão. Branch aberta = sinal de
  trabalho parado/em curso, legível como estado-do-mundo.
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
- **Trabalho parcial: fechar e registrar.** Bloqueio vira commit do
  estado parcial + proponente chama o porta-voz. Se o porta-voz não
  resolve, vira item de fila (decisão pendente). Vale pra agente
  autônomo e pra refinamento estratégico — a regra é "não deixar
  trabalho órfão", não "perder se não terminar".
- **Granularidade de PR depende do fluxo.** Implementação continua com
  PR por milestone (RTE consolida N épicos numa só PR — modelo
  comprovado). Refinamento autônomo opera com PR por épico, com exceção
  declarada para épicos correlatos do mesmo milestone quando coerência
  exige.
- **Operador tem preferência sobre o autônomo.** Mexeu num épico, o
  agente solta aquele.
- **Markdown é fonte da verdade.** A UI é camada de leitura e
  direcionamento.
- **Executor de fluxo é desacoplável** da plataforma. Claude Code Web
  hoje, outro agente amanhã.

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

- **Outros fluxos do workflow** (ver "Fluxos > Futuros" acima). Cada um
  vira épico próprio conforme sinal de necessidade — não estruturam
  decisões atuais.
- **Workflow como produto desacoplado multi-repo.** Tendência futura: a
  plataforma deixa de ser meta-workflow só do paper-agent e atende
  múltiplos repositórios. Implicações arquiteturais (fila por repo,
  dispatch sabe qual repo, skills versionadas por destino) ficam pra
  refinamento quando o sinal aparecer concretamente. Não estrutura
  nenhuma decisão atual.
- **Autonomia crescente além do MVP.** O fluxo de refinamento autônomo
  do MVP cobre saltos pequenos com revisão humana frequente. Maturidade
  futura amplia o repertório do porta-voz e do proponente — mais
  decisões pequenas resolvidas sem operador, escalações mais raras e
  mais bem direcionadas. Guardrails e ambientes de experimentação fazem
  parte dessa evolução. Expansão passo a passo, guiada pela experiência
  real.
