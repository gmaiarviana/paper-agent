# Visão da Plataforma de Workflow

> A plataforma remove atrito de decisão no workflow de desenvolvimento agêntico: operador chega e o próximo passo já está esperando.

A plataforma é uma UI sobre o workflow de desenvolvimento — não é produto do super-sistema (Revelar, Ensaio e demais não a usam). É ferramenta de meta-workflow, complementar às skills que já existem em `skills/` (PM, EM, Scrum Master, Dev, QA, TL, PO, RTE). Serve ao operador humano que orquestra o sistema, não ao usuário final dos produtos.

## O que é

Quando o operador entra, encontra uma **fila** no centro de gravidade. Cada item é uma decisão pendente: aprovação de avanço de refinamento, dúvida escalada pelo agente autônomo, PR pronta pra validar, sugestão do proponente. O operador limpa a fila no próprio ritmo — não há SLA, há ordem.

A fila se autorregula por capacidade. Quando há por volta de vinte itens pendentes, o autônomo para de criar novos e espera o operador abrir espaço. O agente respeita o limite cognitivo do humano. A ordenação é dimensão a refinar — eixos candidatos incluem importância, urgência, severidade e tempo até a decisão expirar.

Ao lado da fila, um **kanban** dá a visão de estado: colunas pelos estados de épico (🌱→📐→📋→🔍→🏗️→✅), agrupadas por milestone, cards carregando labels de autonomia. É a leitura primária do sistema. Clicar num card abre o **chat focado** daquele épico — modo síncrono, opcional, que o operador entra quando quer acelerar algo específico. O chat tem dois shapes por dentro: condução de refinamento a partir do estado atual, ou resposta a uma escalação pontual do agente. Em ambos, chega com prompt pré-montado e contexto carregado — o operador não monta nada.

## O que roda por trás (sem operador precisar pensar)

Três processos rodam sem o operador precisar pensar.

O **agente autônomo de refinamento** pega épicos disponíveis e avança o máximo que consegue, tomando micro-decisões proporcionais ao estágio (POC tolera mais; MVP, menos). Antecipa decisões que vai precisar do humano e coloca na fila antes de travar, quando possível. Para limpo: encerra o ciclo, apresenta o resultado como item de fila, não deixa trabalho pendurado. Respeita a preferência humana — se o operador começar a mexer num épico, o agente solta.

O **proponente** é o orquestrador que olha para o sistema e propõe próximos movimentos. Não é capacidade nova — é um papel que combina as skills existentes (PM, EM, TL, PO, ...) para produzir sugestões. Uma vez por dia coloca uma proposta na fila. Exemplo: o operador menciona uma ideia que considera interessante na visão do produto; o proponente cruza com o backlog e oferece um experimento ("posso fazer uma POC disso") ou aponta dependências ("se você decidir X, isso destrava Y"). O formato é proativo no modo "se você quiser, posso fazer isso" — não "fiz isso, vê se gostou".

O **agente implementador** já existe (Claude Code Web hoje) e é invocado pela plataforma quando o épico está refinado. A plataforma é desacoplável do agente específico — Claude Code agora, outro amanhã.

## Extensibilidade

Adicionar novas skills é como o sistema cresce. A plataforma acomoda isso por design: o proponente passa a ter mais ferramentas, e novos tipos de proposta aparecem na fila. Refinamento e implementação são as primeiras skills atendidas; outras virão conforme necessidade — governança de código, auditoria de arquitetura, exploração de POCs, e o que mais o operador identificar ao longo do caminho.

## Restrições aceitas

Refinamento precede implementação, sem exceção; a UI não permite burlar. O autônomo é ousado, com guardrails por estágio, e labels por épico permitem travar caso a caso. Trabalho parcial do autônomo não é salvo para continuação manual — ou ele fecha e apresenta, ou é perdido. O operador tem preferência sobre o autônomo: mexeu num épico, o agente solta aquele. O markdown no repo é fonte da verdade; a UI é camada de leitura e direcionamento. E o agente de execução é desacoplável da plataforma.
