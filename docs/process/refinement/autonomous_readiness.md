# Autonomous Readiness Checklist

> **Propósito:** checklist da **segunda passada de refinamento** — transição de `📋 Critérios definidos` para `✅ Detalhes definidos`. Aplicado pouco antes de disparar o fluxo autônomo para um épico específico.

## Contexto

O refinamento tem duas passadas. A primeira estabelece objetivo, funcionalidades, critérios de aceite e trade-offs — é suficiente para o fluxo manual via Cursor, onde o desenvolvedor resolve ambiguidades à medida que aparecem. A segunda passada elimina decisões de execução que forçariam o agente autônomo a inventar. Este checklist é da segunda passada.

A pergunta da primeira passada é "isso faz sentido e gera valor?". A pergunta desta segunda passada é "um agente sem contexto do problema consegue executar isto sem inventar?".

## Checklist

### a) Termos e conceitos

Vocabulário comportamental do épico é ancorado em definições permanentes.

- Todo termo comportamental novo introduzido pelos critérios de aceite tem definição em doc permanente (core ou produto), com link explícito no épico.
- Termos reusados do domínio compartilhado apontam para o doc conhecido onde a definição já existe.

### b) Dados e contratos

Formatos concretos de dado estão fixados antes do dispatch.

- Shape dos estados compartilhados relevantes está explicitado — chaves e tipos.
- Shape dos inputs e outputs das funções e agentes alvo está explicitado.
- Divergências conscientes com o padrão existente estão declaradas no épico (ex: "este fluxo não usa o campo X do estado padrão").

### c) Código-alvo e integração

Superfície de código está delimitada, e o mecanismo de integração é descritivo o suficiente para ser executado sem arbitrar.

- Arquivos a criar listados com caminho completo.
- Arquivos a modificar listados com caminho completo.
- Mecanismo de integração descrito além do "o que muda": onde o código entra, como é carregado, como é invocado pelo caller.
- Agente ou componente existente apontado como template de estilo e estrutura para o código novo.

### d) Acoplamentos

Interação com o que já existe foi verificada, não assumida.

- Código existente que será lido ou importado foi inspecionado durante o refinamento.
- O acoplamento resultante está declarado viável para o escopo do épico (imports, dependências transitivas, estado compartilhado).
- Refatorações prévias necessárias viraram dependência explícita no épico ou épico próprio no ROADMAP.

### e) Sequência e testes

Ordem de execução e critério de "pronto" são observáveis.

- Dependências entre épicos, e entre funcionalidades do mesmo épico, estão declaradas com ordem de execução.
- Escopo de teste por funcionalidade está definido: unit, integration, validação manual via script.
- Critérios de aceite são observáveis por teste automatizado ou script de validação.

## Quando aplicar

Pouco antes do dispatch autônomo, para o épico específico que vai ser disparado. Aplicar preventivamente em todos os épicos do ROADMAP é desperdício — o trabalho morre se o épico for repriorizado ou mudar antes de ser implementado. A segunda passada se paga no momento do disparo.

## Saída

Épico marcado como `✅ Detalhes definidos` no ROADMAP correspondente (`docs/ROADMAP.md` ou `products/<produto>/ROADMAP.md`). Esse estado é o pré-requisito para o dispatch autônomo (`docs/process/autonomous/dispatch.md`). Épicos em `📋 Critérios definidos` continuam elegíveis para o fluxo manual via Cursor.

## Referências

- Primeira passada do refinamento → `docs/process/refinement/planning_guidelines.md`
- Visão geral do refinamento → `docs/process/refinement/overview.md`
- Starter pack de contexto inicial → `docs/process/refinement/starter.md`
- Dispatch do fluxo autônomo → `docs/process/autonomous/dispatch.md`
