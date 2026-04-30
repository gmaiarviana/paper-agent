# Autonomous Readiness Checklist

> **Propósito:** este checklist descreve os itens que uma sessão de refinamento com alvo `🔍 Detalhes definidos` deve cobrir. Atingir `🔍 Detalhes definidos` é pré-requisito para o fluxo autônomo.

## Contexto

Um épico atinge `🔍 Detalhes definidos` quando um agente sem contexto do problema consegue executá-lo sem inventar decisões. Este checklist é a materialização dessa condição — os itens abaixo são critérios, não etapas sequenciais. Uma sessão de refinamento pode cobri-los toda de uma vez, ou uma sequência de sessões pode convergir ao mesmo alvo; o que importa é que ao fim todos os critérios aplicáveis estejam atendidos.

Este checklist é **complementar** ao `docs/process/refinement/epic_completion.md` — aqui descrevemos os critérios de **entrada** em implementação; lá, os de **saída**.

## Checklist (seis categorias)

### a) Termos e conceitos

Vocabulário comportamental do épico é ancorado em definições permanentes.

- Todo termo comportamental novo introduzido pelos critérios de aceite tem definição em doc permanente (core ou produto), com link explícito no épico.
- Termos reusados do domínio compartilhado apontam para o doc conhecido onde a definição já existe.

### b) Dados e contratos

Formatos concretos de dado estão fixados no épico.

- Shape dos estados compartilhados relevantes está explicitado — chaves e tipos.
- Shape dos inputs e outputs das funções e agentes alvo está explicitado.
- Divergências conscientes com o padrão existente estão declaradas no épico (ex: "este fluxo não usa o campo X do estado padrão").

### c) Código-alvo e integração

Superfície de código está delimitada e o mecanismo de integração é descritivo o suficiente para ser executado sem arbitrar.

- Arquivos a criar listados com caminho completo.
- Arquivos a modificar listados com caminho completo.
- Mecanismo de integração descrito além do "o que muda": onde o código entra, como é carregado, como é invocado pelo caller.
- Agente ou componente existente apontado como template de estilo e estrutura para o código novo.

### d) Acoplamentos

Interação com o que já existe foi verificada, não assumida.

- Código existente que será lido ou importado foi inspecionado durante o refinamento.
- O acoplamento resultante está declarado viável para o escopo do épico (imports, dependências transitivas, estado compartilhado).
- Refatorações prévias necessárias viraram dependência explícita no épico ou épico próprio no ROADMAP.
- **Mudanças em código compartilhado entre produtos** (`core/`, módulos cross-produto) listam **todos os produtos consumidores afetados** e declaram como cada um foi verificado contra regressão (teste automatizado, inspeção manual, validação no fluxo do produto). Mudança em prompt/agente do core sem essa lista é defeito do refinamento — produto compartilhador pode quebrar silenciosamente.

### e) Sequência e testes

Ordem de execução e critério de "pronto" são observáveis.

- Dependências entre épicos, e entre funcionalidades do mesmo épico, estão declaradas com ordem de execução.
- Escopo de teste por funcionalidade está definido: unit, integration, validação manual via script.
- Critérios de aceite são observáveis por teste automatizado ou script de validação.

### f) Centralidade da visão respeitada

O que a visão do produto declara como central para o estágio alvo permanece intacto.

- Itens declarados **centrais** na vision.md do produto para o estágio (POC/Protótipo/Piloto/MVP) estão preservados ou avançados pelo épico — nunca cortados nem reduzidos.
- Quando o refinamento propõe ajuste de algo central, o ajuste foi explicitamente autorizado pelo usuário (registrado no épico ou em comentário), não absorvido como detalhe.

## Ajuste por Estágio (POC / Protótipo / Piloto / MVP)

O nível de detalhe exigido varia por estágio do produto. As três listas abaixo aplicam-se **sobre** as seis categorias acima: indicam quais itens são incondicionais e quais podem ser simplificados.

### Aplicáveis em todos os estágios

Estes itens são exigência mínima, mesmo em POC:

- Termos e conceitos com definição linkada.
- Shape dos inputs e outputs de funções e agentes alvo.
- Arquivos a criar e modificar listados com caminho.
- Mecanismo de integração descrito.
- Acoplamentos com código existente inspecionados.
- Mudanças em código compartilhado entre produtos listam consumidores impactados.
- Dependências entre épicos e funcionalidades declaradas com ordem.
- Centralidade da visão respeitada (itens centrais não foram cortados sem autorização explícita).

### Aplicáveis a Protótipo, Piloto e MVP

Estes itens ficam rígidos a partir do Protótipo:

- Shape completo de estados compartilhados.
- Escopo de teste formal: unit, integration, validação manual.
- Critérios de aceite observáveis por teste automatizado.
- Refatorações prévias necessárias viraram épico próprio ou dependência explícita no ROADMAP.

### Simplificáveis em POC

Em estágio POC, estas simplificações são permitidas — desde que declaradas como tal no campo "Simplificações" do épico, não escondidas como dívida:

- Testes automatizados podem ser substituídos por validação manual via script.
- Shapes complexos podem ser descritos em prosa quando o código ainda está em exploração.
- Refatorações pequenas podem ser absorvidas no próprio épico em vez de virar épico separado.

## Quando Aplicar

Sob demanda, quando uma sessão de refinamento declara alvo `🔍 Detalhes definidos` — tipicamente pouco antes de disparar o fluxo autônomo para o épico específico. Aplicar preventivamente em todos os épicos do ROADMAP é desperdício: o trabalho morre se o épico for repriorizado ou mudar antes de ser implementado.

## Saída

Épico marcado como `🔍 Detalhes definidos` no ROADMAP correspondente (`docs/ROADMAP.md` ou `products/<produto>/ROADMAP.md`). Esse estado é o pré-requisito do dispatch (`docs/process/autonomous/dispatch.md`) — `📋 Critérios definidos` é passo intermediário e ainda não habilita execução.

## Referências

- Modelo completo de estados e alvos de refinamento → `docs/process/refinement/planning_guidelines.md`
- Visão geral do refinamento → `docs/process/refinement/overview.md`
- Starter pack de contexto inicial → `docs/process/refinement/starter.md`
- Checklist complementar de fechamento de épico (saída) → `docs/process/refinement/epic_completion.md`
- Dispatch do fluxo autônomo → `docs/process/autonomous/dispatch.md`
