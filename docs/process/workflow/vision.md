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

**Norte de curto prazo (estágio Piloto).** O valor imediato é a
plataforma virar o cockpit real de uso diário: o operador dispara o
trabalho de um produto do paper-agent — hoje o Ensaio — e acompanha o
avanço de dentro dela, sem alternar janelas. Esse uso já acontece de
forma reativa (operador dispara, operador monitora); o foco do Piloto é
torná-lo fluido e agradável — UX de verdade e runtime de agente
integrado, tratados como frentes distintas (ver "Forma da Plataforma").
"Usar de verdade, obter valor de verdade" é o critério. Multi-projeto e
proatividade plena são arcos seguintes — não o curto prazo.

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
- **Skills são portáveis entre runtimes e providers.** O contrato
  (`skill.md`) não depende de CLI nem provider específico. Hoje as skills
  carregam em Claude Code Web contra a API Anthropic; no Piloto/MVP
  devem rodar em outros runtimes (opencode, agent SDK próprio) e contra
  outros providers (OpenWebUI/Ollama corporativo, OpenAI). Limita o que
  entra na skill: nenhuma instrução depende de tool específica do CC
  (`TodoWrite`, etc.) ou de protocolo de provider específico. O caminho
  evolutivo aparece em "Horizonte".

## Eixo de Estágios

Workflow segue o eixo de **maturidade da solução** do CONSTITUTION,
adaptado para processo:

- **POC — primeiro fluxo ponta a ponta.** Um fluxo (implementação) roda
  manualmente disparado pelo operador, sem priorização autônoma. Prova
  que o conceito de fluxo orquestrado por skills se sustenta. Fechado em
  `POC-WORKFLOW`.
- **Protótipo — estrutura visível.** A plataforma reativa entra em cena:
  kanban + fila populada por sinais óbvios do repo (PR aberta, épico
  chegou em estado-gatilho, branch parou) + chat focado por item +
  ações contextuais. Estrutura completa o suficiente para o trabalho do
  dia a dia se apoiar nela, ainda sem agentes proativos — sinais viram
  itens de fila por regra, não por julgamento. Milestones em curso e
  roadmap detalhado em [ROADMAP.md](ROADMAP.md).
- **Piloto — estrutura funcionando bem.** **A plataforma vira canal
  único** (ver "Forma da Plataforma"): o dispatch e o chat focado
  acontecem dentro dela, com chamada à camada de agente por API/CLI por
  baixo dos panos — a plataforma deixa de ser só leitura e passa a
  disparar a execução. Sobre esse canal, entra a **proatividade
  mecânica**: a plataforma auto-aciona o que a fila reativa já detecta
  como despachável (milestone em 🔍), em execução de segundo plano com
  teto baixo e PR como único portão (ver "Proatividade e execução em
  segundo plano"). Duas frentes distintas sustentam o uso real:
  **qualidade de UX** (a plataforma agradável de usar todo dia) e
  **runtime de agente integrado** (REPL/headless chamado de dentro dela).
  O **Ensaio é o campo de prova** — o uso diário contra ele valida o
  estágio. A camada de julgamento (proponente, porta-voz) e o refinamento
  autônomo standalone ficam no MVP.
- **MVP — solução robusta, release a colegas.** Quando a estrutura do
  Piloto se mostra sólida, a robustez vira foco: tratamento de erros do
  agente e da plataforma, comportamento previsível em borda, mensagens
  claras. É também no MVP que entra a **camada de autonomia por
  julgamento** — proponente escolhendo o próximo movimento, porta-voz
  curando atenção — e o **fluxo de refinamento autônomo standalone**
  (cobrir estados pré-🔍), sobre o cockpit que o Piloto consolidou. Junto
  com o release a colegas — o workflow se desacopla do
  paper-agent: é **extraído para um repo novo**, próprio, e passa a ser
  usado contra outros repositórios e por outras pessoas (não se pede que
  um colega use contra o repo do paper-agent). Implicações estruturais —
  multi-persona no chat focado e na
  fila, runtime de agente sobre providers corporativos (OpenWebUI/Ollama),
  workflow como produto multi-repo — vivem em "Horizonte". O gatilho do
  desacoplamento é o release, não o Piloto.

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

Sobre esses tipos corre uma distinção de **natureza**, que agrupa a fila
em duas categorias: **Ações** — itens que avançam trabalho (aprovar um
refinamento, validar uma PR, decidir uma escalação) — e **Higiene** —
manutenção e triagem que ainda pede olho humano mas não faz o trabalho
andar (limpar concluído, revisar uma branch parada). A Higiene continua
visível — não é ruído a esconder —, só que sob sua própria seção, separada
das Ações.

A fila se autorregula por capacidade. Quando há por volta de vinte itens
pendentes, o autônomo para de criar novos e espera o operador abrir
espaço. O agente respeita o limite cognitivo do humano. O regulador conta
**só Ações** — Higiene nunca entra na conta do limite, porque não é
trabalho a segurar. A ordenação é dimensão a refinar — eixos candidatos
incluem importância, urgência, severidade e tempo até a decisão expirar.

Esse regulador é mecanismo do **modo autônomo** (ver "dois modos" logo
abaixo): existe para segurar um curador que cria itens por conta própria.
No Protótipo de hoje, reativo, não há autônomo populando a fila — logo não
há o que regular de fato, e a UX de como (ou se) exibir o limite fica em
aberto, para quando o fluxo autônomo chegar. Não se desenha esse controle
agora.

A fila tem dois modos conforme o estágio. **No Protótipo**, é populada
**reativamente** — regras determinísticas convertem sinais óbvios do repo
(PR aberta, épico chegou em estado-gatilho, branch parou) em itens.
Operador atende na ordem que escolher; ordenação é simples (recência ou
manual). **No MVP**, o porta-voz passa a curar a fila — ordena, agrupa,
filtra, escala apenas o que escapa do seu repertório. Ver "Papéis"
abaixo.

### Kanban

Ao lado da fila, um **kanban** dá a visão de estado: colunas pelos oito
estados de épico (definição canônica em [`planning_guidelines.md` §Estados
de Épico](../refinement/planning_guidelines.md#estados-de-épico)), agrupadas
por milestone, cards carregando labels de autonomia. É a leitura primária
do sistema.

### Chat focado

Clicar num card abre o **chat focado** daquele épico — modo síncrono,
opcional, que o operador entra quando quer acelerar algo específico. O
chat tem dois shapes por dentro: condução de refinamento a partir do
estado atual, ou resposta a uma escalação pontual do agente. Em ambos,
chega com prompt pré-montado e contexto carregado — o operador não
monta nada.

### Plataforma como canal único (estágio Piloto)

Hoje o chat focado pode ser realizado abrindo sessão do Claude Code Web
fora da plataforma — ela monitora, direciona e prepara contexto, mas o
trabalho acontece em outra janela. **No Piloto**, a plataforma absorve
esse canal: a conversa de refinamento e o dispatch acontecem **dentro**
dela, e o agente (Claude Code Web hoje, outro runtime amanhã) é chamado
por API/CLI por baixo dos panos. Operador deixa de alternar entre
janelas — entra na plataforma e tudo acontece ali. Botão de dispatch
deixa de ser comando para humano abrir sessão; vira chamada que a
plataforma faz à camada de agente.

Implicação técnica: a plataforma evolui de view sobre markdown e estado
de PRs (Protótipo) para integradora da camada de agente (Piloto).
Combinada com o princípio de portabilidade de skills, o runtime é
trocável — o que a plataforma chama é um contrato de execução de fluxo,
não um CLI específico. Construir esse acoplamento já no Piloto, mesmo
que o runtime inicial seja Claude Code, é o que destrava a substituição
de agente+modelo no MVP (release a colegas no ambiente corporativo).

### Interação por voz (longo prazo)

A plataforma conversa com o operador. O modelo canônico é o briefing
**sob demanda** (pull, não push): quando o operador entra e pede, o
sistema relata o estado do dia em linguagem natural — decisões pendentes
com contexto e impacto, atualizações de implementações em curso, novas
ideias ou propostas — e pergunta onde focar. O operador responde em voz
ou texto; a plataforma mapeia a intenção para a ação correspondente. A
voz é canal de briefing sob demanda — não um alerta que interrompe o
dia.

A voz é o canal do briefing e do diálogo, o espaço onde a decisão se
forma. A execução tem botão; o pensamento tem voz.

## Papéis

Três papéis ativos no sistema. Operador é humano; proponente e porta-voz
são agentes que aparecem no MVP (o Piloto tem proatividade mecânica, sem
julgamento — ver "Eixo de Estágios" e "Proatividade e execução em
segundo plano"). Refinamento e implementação **não** são papéis — são
fluxos (próxima seção).

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

## Proatividade e execução em segundo plano

A proatividade chega em dois degraus. **No Piloto é mecânica:** a
plataforma auto-aciona o que a fila reativa já detecta como despachável
(milestone em 🔍) — execução de segundo plano sobre trabalho já
refinado, sem agente de julgamento escolhendo o quê. **No MVP ganha
julgamento:** o **proponente** (~1×/dia) escolhe o próximo movimento e
**dispara** — não só propõe — cobrindo todos os estados de épico, não
apenas dispatch de 🔍: pode avançar o refinamento de um épico pré-🔍 (um
salto de estado) ou implementar o que já está refinado. A prioridade
entre essas opções é a declarada em "Papéis > Proponente".

Os guardrails abaixo valem para os dois degraus.

**Não repetir trabalho em curso.** Antes de disparar, o autônomo lê o
estado-do-mundo e pula o que já está em andamento: épico com branch
ativa, PR aberta, ou em 🏗️/🔀 já tem dono (humano ou agente). A
idempotência é por **estado**, não por histórico — a mesma leitura
determinística que a fila usa (branch aberta como sinal, "Substrato
Técnico"; claim em "Detecção de Claim do Operador"). O agente nunca abre
uma segunda frente sobre o mesmo épico.

**Um movimento por vez, não tudo de uma vez.** Dispara-se *um* próximo
movimento — nunca uma frente ampla tentando resolver tudo num ciclo.
Vale o princípio "Pacing por bandwidth do operador": o
sistema não gera mais revisão (PRs) do que o operador absorve com
qualidade. Há um teto de fluxos ativos simultâneos — baixo nas fases
iniciais, ajustável por estágio/config (número fica no ROADMAP, não
aqui) — e o refinamento segue em saltos pequenos, um estado por vez.
Querer resolver tudo de uma vez é antipadrão explícito.

**Execução em branch isolada, PR como único portão.** O agente comita o
avanço numa branch própria do épico/milestone sem o operador presente
(coerente com "Substrato Técnico > Branch persiste por épico em fluxo
ativo"). O único portão humano é a **aprovação da PR** — o operador
revisa e mergeia; nada entra em `main` sem esse aval. Não há merge
automático.

**Sem push: a plataforma não interrompe.** O secretário não notifica. O
avanço e a "decisão mais valiosa" ficam visíveis quando o operador abre
a plataforma — fila, kanban, PRs aguardando revisão (e, no MVP, a fila
já curada pelo porta-voz). O modelo é pull (operador chega e vê), não
alerta que interrompe o dia.

**Rollout em fases validáveis.** Os dois degraus — proatividade mecânica
(Piloto) e julgamento (MVP) — ligam em incrementos testáveis; guardrails
por estágio e label por épico permitem travar caso a caso, antes de
cobrir todos os estados sem supervisão. Cada fase é validada no uso real
(Ensaio) antes da próxima. A sequência concreta das fases vive no
ROADMAP, não aqui.

## Fluxos

Cada tipo de trabalho tem um fluxo especializado, executado via
sequência de skills. Fluxos **não são papéis** — são modos de trabalho.
Disparados pela plataforma/proponente (autônomo) ou pelo operador
(manual).

### Refinamento

Avança épico em estados pré-execução até alvo declarado (normalmente
🔍). Skills: **PM** (refinamento tático), **EM** (preflight de tamanho).

Princípios do refinamento autônomo (standalone chega no MVP):

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
paper-agent que não seria carregada por Claude Code Web durante o fluxo de
implementação, mas por uma GitHub Action (`.github/workflows/milestone-cleanup.yml`)
disparada por evento de repositório (merge de PR de milestone).

> **⚠️ Status (atualizado):** o caso piloto — cleanup pós-merge — **abandonou
> este padrão**. A Action falhou em produção por OIDC (`id-token: write`
> ausente) e o desenho "agente commitando em `main` sem revisão" tinha
> resistência. A faxina migrou para o **fold-in do dispatch** (roda no runtime
> autenticado do agente, dentro de um diff revisado): ver
> `docs/process/autonomous/dispatch.md` §4.5. O padrão "skill em Action" segue
> documentado abaixo como aprendizado — mas a lição do piloto é que tarefas que
> mutam `main` querem revisão humana, o que empurra para fold-in em vez de CI
> autônomo.

A skill em si (`skill.md`) permanece autocontida — pode rodar em Claude Code
Web manualmente. O que mudaria com o padrão é o trigger: evento → Action →
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
- **Release a colegas e workflow como produto desacoplado (estágio
  MVP).** No MVP, a plataforma deixa de ser meta-workflow só do
  paper-agent e passa a ser usada por outras pessoas em outros
  repositórios. O desacoplamento é uma **extração para um repo novo**,
  próprio do workflow. Os dois movimentos são **distintos e
  sequenciáveis**: a **costura técnica de sync** (extração + operar o
  fluxo contra um repo-alvo) pode e deve ser provada antes, contra um
  segundo repo do próprio operador; o release a colegas é o gatilho da
  **adoção externa** (auth, multi-persona, ambiente corporativo), não da
  costura de sync. O gatilho duro do desacople é o primeiro alvo que
  **não carrega as skills** — tipicamente o release, mas o mecanismo
  antecede o gatilho. Materializado no ROADMAP como `MVP-WORKFLOW-DESACOPLE`.
  Implicações arquiteturais (fila por repo, dispatch sabe qual repo,
  skills versionadas por destino, auth) ficam pra refinamento quando o
  sinal aparecer concretamente. Não estrutura decisões do Piloto.
- **Personas humanas plurais no chat focado e na fila (estágio MVP).**
  PMs e POs passam visão de funcionalidade e regras de negócio;
  engenheiros e arquitetos tomam decisões técnicas. Cada persona vê o
  pedaço apropriado do refinamento — extensão simétrica do split que as
  skills PM e EM já fazem do lado agente. Gatilho: 1+ colega usando
  regularmente. Decisões dependentes (auth, escopo por persona,
  multi-tenancy) ficam pra refinamento quando o sinal aparecer.
- **Runtime de agente sobre providers corporativos (estágio MVP).**
  Suportado pelo princípio de portabilidade de skills. Quando o release
  a colegas acontecer no ambiente corporativo da Atlântico, o runtime
  que a plataforma chama precisa rodar contra OpenWebUI/Ollama (modelos
  OpenAI-compatible servidos internamente) sem reescrever skill por
  skill. Caminhos candidatos hoje: Claude Code CLI via proxy LiteLLM
  (parcial — depende de modelo grande), opencode com provider OpenAI
  custom, agent SDK próprio. Decisão de runtime fica pra quando a
  capacidade dos modelos corporativos estiver clara. Pré-requisito
  técnico — o acoplamento plataforma↔agente via API/CLI — é gate do
  Piloto, não do MVP.
- **Modelos heterogêneos por skill.** Longo prazo, depois do release a
  colegas estabilizado. Skills baratas e curtas (ex.: PM extraindo
  detalhes de um épico) rodam em modelo local pequeno; skills caras e
  cuidadosas (ex.: TL avaliando arquitetura) rodam em modelo robusto.
  Heterogeneidade só entra quando o ganho de custo ou qualidade for
  mensurável — sem virar otimização prematura.
- **Skills evoluem para sistema multi-agente.** Longo prazo. Hoje as
  skills são markdown carregado sequencialmente no mesmo runtime do
  Claude Code Web, partilhando contexto. Maturidade futura: cada skill
  é agente independente com contexto curado, possivelmente modelo
  próprio (ver item anterior), orquestrado pela plataforma. Trade-off
  com o estado atual: ganha isolamento e especialização, perde a
  simplicidade do "Claude Code carrega tudo no mesmo contexto". O
  caminho passa por desacoplar carregamento de skill do CLI (já gate do
  Piloto) e por ter um orquestrador explícito (proponente + porta-voz
  já apontam pra ele).
- **Autonomia crescente além do MVP.** O fluxo de refinamento autônomo
  do MVP cobre saltos pequenos com revisão humana frequente.
  Maturidade futura amplia o repertório do porta-voz e do proponente —
  mais decisões pequenas resolvidas sem operador, escalações mais raras
  e mais bem direcionadas. Guardrails e ambientes de experimentação
  fazem parte dessa evolução. Expansão passo a passo, guiada pela
  experiência real.
