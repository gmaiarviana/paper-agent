# Planning Guidelines

> **📌 Localização:** `docs/process/refinement/planning_guidelines.md`.
> **📌 Público:** Claude Web (refinamento) e desenvolvedores (governança).
> **📌 Envio em sessão de refinamento:** junto com `docs/CONSTITUTION.md`, `docs/ROADMAP.md`, `docs/ARCHITECTURE.md` e o ROADMAP do produto em foco.
> **📌 Checklist para atingir `🔍 Detalhes definidos`:** `docs/process/refinement/autonomous_readiness.md`.
> **📌 Checklist de fechamento de épico:** `docs/process/refinement/epic_completion.md`.

## Filosofia de Desenvolvimento

Este projeto segue mentalidade **incremental e pragmática**:

### Progressão por Estágios

Definições trabalhadas para este projeto, no eixo **"quem usa"** (complementa o eixo técnico):

- **POC (Proof of Concept):** prova que a ideia faz sentido. Pode ser tosco, rodar só no ambiente do desenvolvedor, ter atalhos explícitos. Critério de saída: a ideia se sustenta o suficiente para justificar investimento em estabilidade.
- **Protótipo:** a ideia funciona e o **próprio desenvolvedor usa de verdade** — no fluxo real dele, não só em cenário de teste. Critério de saída: o desenvolvedor consegue usar sem se apoiar em conhecimento interno do código.
- **MVP:** **outros** (colegas próximos) usam **sem o desenvolvedor do lado**. Critério de saída: valor validado fora do autor.
- **Melhorias:** Expansão gradual baseada em feedback de uso real.

**Implicação prática:** decisões de stack, UX e robustez devem ser proporcionais ao estágio. POC tolera Streamlit e gambiarras; Protótipo exige fluxo navegável pelo próprio dev; MVP exige que outro ser humano consiga usar sem tutorial ao vivo.

## Processo de Refinamento com Claude Web

Este projeto usa Claude Web como consultor estratégico para refinar épicos e discutir comportamentos. O processo é documentado aqui para garantir consistência.

### Input Esperado
Você fornece ao Claude Web:
- Comportamento desejado OU problema existente
- Contexto: épico novo, ajuste de funcionalidade, ou discussão arquitetural
- 5 arquivos essenciais: docs/CONSTITUTION.md, docs/ROADMAP.md, products/revelar/ROADMAP.md, docs/ARCHITECTURE.md, planning_guidelines (este)

### Claude Web Deve

> **Nota — refinamento estratégico vs tático.** A partir da reforma em curso (milestone como unidade de entrega), o refinamento se divide em duas modalidades:
>
> - **Estratégico (Claude Web, externo ao repo):** quebra uma visão em milestones e/ou épicos em `🌱 Visão`/`📐 Funcionalidades esboçadas`, e leva épicos a `📋 Critérios definidos` ou `🔍 Detalhes definidos` **antes de existir milestone em execução**. É o processo descrito nesta seção.
> - **Tático (PM skill, dentro da branch do milestone):** leva épicos de um milestone já disparado que ainda estão em `🌱` ou `📐` até `🔍 Detalhes definidos`, aplicando o checklist de `autonomous_readiness.md`. A PM skill (a ser criada em M3b da reforma do fluxo) consome o mesmo checklist, mas opera dentro de sessão do Claude Code Web, com acesso direto ao repo, sem gerar prompts para Cursor.
>
> Ambos produzem o mesmo estado final no ROADMAP (épico em `🔍`). O que muda é **quem refina** e **onde o resultado é commitado** (fora da branch do milestone, no caso estratégico; dentro, no caso tático).

### Postura do Refinamento

Refinamento é **conversa**, não execução. O agente otimiza por **alinhamento contínuo com o usuário**, não por entregar o alvo declarado o mais rápido possível. Vários erros recorrentes (editar antes de aval, descer níveis prematuros, perguntar em bloco indiscriminado) são sintomas do mesmo padrão: tratar o refinamento como tarefa em vez de diálogo. Quatro regras operacionais:

**a) Hierarquia de camadas — subir antes de descer.**

Refinamento percorre quatro camadas e a ordem importa:

```
milestone (visão, jornada) → épico (objetivo, o que é/não é) → funcionalidade (esboço) → critério de aceite (testável)
```

O alvo declarado (`📋`, `🔍`) define a **profundidade final**; a **ordem de subida** começa sempre na camada mais alta. Refinar critério de aceite antes de alinhar jornada/objetivo gera retrabalho — se a camada superior muda, tudo abaixo muda junto. Sintoma típico do erro: usuário interrompe pedindo "conversa em camada mais alto".

**b) Confirmação conversacional antes de edit.**

Antes de escrever em qualquer arquivo (ROADMAP, vision.md, spec), confirmar conversacionalmente o que vai ser escrito: *"vou registrar X, Y, Z, segue?"*. Não é cerimônia pesada (não exige palavra-chave nem recap formal) — é checagem leve para capturar desalinhamento antes do edit. Custo zero quando alinhamento existe; salva retrabalho quando não existe.

**c) Pergunta por qualidade, não por quantidade.**

Pergunta legítima é a que **altera um resultado de forma cara de reverter** — decisão arquitetural, recorte de escopo, quebra de premissa da visão. Detalhes viram proposta com default; usuário corrige no review. Sem teto numérico fixo: zero perguntas é aceitável se os defaults forem sólidos; oito perguntas heterogêneas costuma ser sintoma de não-filtro entre "decisão estrutural" e "detalhe assumível".

**d) Centralidade da visão como restrição dura.**

Antes de iniciar refinamento, identificar o que a visão do produto declara como **central** para o estágio alvo (POC/Protótipo/MVP). Itens centrais são restrição **não-negociável** — não podem ser cortados nem reduzidos por proposta do agente durante a sessão; só pelo usuário. Pergunta direta no início: *"o que a visão declara central no estágio alvo, e portanto não é negociável?"*. Sintoma do erro: agente reabre item declarado central no meio da sessão como se fosse opcional.

1. **Análise Contextual:** Consultar vision.md, docs/ROADMAP.md ou products/revelar/ROADMAP.md (épicos anteriores), specs técnicas via mapa
2. **Clarificação:** Fazer perguntas específicas, validar entendimento, apontar trade-offs
3. **Recomendação:** Oferecer opções + recomendação balizada por vision.md e guidelines
4. **Gerar Prompts:** Múltiplos prompts (1 por arquivo), instruções enxutas, manter padrões
5. **Validação:** Confirmar que prompts fazem sentido

### Output Gerado
Claude Web gera prompts separados para Cursor executar:
- PROMPT 1: docs/ROADMAP.md ou products/revelar/ROADMAP.md (dependendo do épico)
- PROMPT 2: docs/[spec técnica]
- PROMPT 3: docs/ARCHITECTURE.md (se necessário)

Cada prompt é enxuto mas claro, deixando Cursor pensar também.

### Otimização do Workflow: Usando Cursor para Análises

**Ao invés de enviar todos os arquivos de contexto ao Claude Web**, você pode solicitar ao Cursor para fazer análises do código e gerar insights que facilitam o refinamento:

**Estratégia:**
- **Antes de ir ao Claude Web:** Use o Cursor para escanear o repositório e fazer análises específicas
- **Envie ao Claude Web:** Os insights gerados pelo Cursor + os 4 arquivos essenciais (CONSTITUTION, ROADMAP, ARCHITECTURE, planning_guidelines)

**Exemplos de prompts para o Cursor:**
- "Analise a estrutura atual do sistema de persistência e identifique pontos de extensão para suportar pausar/retomar conversas"
- "Escanee o código do orquestrador e identifique como ele gerencia estado atualmente"
- "Analise os padrões de implementação dos agentes existentes para manter consistência no novo épico"
- "Revise a arquitetura de eventos e sugira como integrar nova funcionalidade X"

**Benefícios:**
- ✅ Reduz o volume de arquivos enviados ao Claude Web
- ✅ Cursor tem acesso completo ao código e pode fazer análises profundas
- ✅ Insights técnicos específicos facilitam decisões no refinamento
- ✅ Claude Web recebe contexto já processado e focado

**Fluxo recomendado:**
1. Cursor faz análise técnica do código relevante
2. Claude Web recebe insights + documentos essenciais para refinamento estratégico
3. Claude Web gera prompts para Cursor implementar

### Exemplo de Refinamento Bem Feito

**Cenário:** Refinar Épico 10 - Persistência

**Input do usuário:**
"Vamos refinar Épico 10. Quero pausar/retomar conversas com contexto preservado."

**Claude Web:**
1. Consulta vision.md (entidade Tópico), ROADMAP (padrão de épicos anteriores)
2. Pergunta: "Persistência local (SqliteSaver) ou remota (PostgreSQL)? Trade-off: simplicidade vs escalabilidade"
3. Recomenda: "Começar com SqliteSaver (POC), migrar pra PostgreSQL (MVP se necessário)"
4. Propõe funcionalidades 10.1-10.5 com critérios de aceite claros
5. Gera prompts pra Cursor atualizar ROADMAP + criar `docs/architecture/persistence.md` (arquivo será criado durante refinamento, não existe ainda)

> **📌 Nota:** Este é um exemplo hipotético de refinamento. O arquivo `docs/architecture/persistence.md` será criado quando o Épico 10 for refinado.

**Resultado:** Épico em `📋 Critérios definidos`, specs criadas, pronto para implementação via fluxo manual. Antes do dispatch autônomo, uma nova sessão de refinamento com alvo `🔍 Detalhes definidos` aplica o checklist de `autonomous_readiness.md`.

---

### Princípios de Planejamento
1. **Refinar apenas o que está claro**
   - Épicos só são refinados quando se tornam prioritários
   - Refinamento requer compreensão técnica do estado atual do sistema
   - Funcionalidades detalhadas só após sessão de refinamento dedicada

2. **Fazer > Planejar demais**
   - Implementar POC mínimo e validar antes de expandir
   - Aprender com código real, não especulação
   - Ajustar plano baseado em implementação, não o contrário

3. **Validar > Assumir**
   - Cada estágio (POC/Protótipo/MVP) deve ser validado antes do próximo
   - Validação = rodar sistema com cenários reais, não apenas testes passando
   - Feedback de validação informa refinamento do próximo estágio

4. **Iterar > Acertar de primeira**
   - Versão 1.0 de qualquer funcionalidade será imperfeita
   - Sistema evolui através de iterações sucessivas
   - Aceitamos limitações conhecidas em versões iniciais

5. **Funcionalidade mínima > Feature completa**
   - Entregar valor incremental cedo e frequentemente
   - Preferir funcionalidade simples que funciona a feature complexa incompleta
   - Expandir apenas quando mínimo está sólido

### Gestão do Backlog
- **Backlog = Desejo, não compromisso**
- Ideias vão para backlog sem serem épicos formais
- Épicos em `🌱 Visão` aguardam priorização + clareza técnica
- Remover do backlog é tão válido quanto adicionar (não há apego)

### Seis Estados de Refinamento

Um épico percorre até seis estados no ROADMAP. Os quatro primeiros são de refinamento progressivo; os dois últimos são de execução e fechamento. Cada estado é o anterior acrescido de conteúdo.

> **Nota — onde o refinamento acontece.** Até `📋 Critérios definidos`, o refinamento sempre é estratégico, via Claude Web, antes de qualquer milestone em execução. Já a transição de `🌱`/`📐`/`📋` para `🔍 Detalhes definidos` pode acontecer em duas situações distintas: (a) externamente, via Claude Web, como preparação antecipada; ou (b) dentro da branch de um milestone já disparado, via PM skill (skill a ser criada em M3b da reforma do fluxo), como parte do próprio fluxo autônomo. Ambos caminhos usam o mesmo checklist (`autonomous_readiness.md`) e produzem o mesmo estado final no ROADMAP.

**`🌱 Visão`** — apenas objetivo definido.
Estado inicial de qualquer épico promovido a partir do backlog ou produzido por uma sessão do tipo "me quebra essa ideia em épicos a partir da visão". Captura intenção e valor de negócio; não é executável por nenhum fluxo.

**`📐 Funcionalidades esboçadas`** — lista de funcionalidades com descrição curta, sem critérios de aceite.
Estado intermediário útil quando um épico foi quebrado a partir de uma visão e as funcionalidades já emergiram, mas os critérios de aceite ainda não foram discutidos funcionalidade a funcionalidade. Não é executável por nenhum fluxo.

**`📋 Critérios definidos`** — funcionalidades com critérios de aceite claros e testáveis.
Épico tem funcionalidades delimitadas, critérios de aceite observáveis, trade-offs discutidos. **Suficiente para o fluxo manual via Cursor**, onde o desenvolvedor resolve ambiguidades de execução à medida que aparecem.

**`🔍 Detalhes definidos`** — passou pelo checklist em `docs/process/refinement/autonomous_readiness.md`.
Além dos critérios de aceite, tem contratos de dados explicitados, arquivos-alvo listados, mecanismo de integração descrito, acoplamentos verificados e escopo de testes definido. **Pré-requisito para o fluxo autônomo via Claude Code Web**, onde o agente não deve tomar decisões arquiteturais em tempo de implementação.

**`🏗️ Em andamento`** — épico em implementação.
Permanece neste estado desde o momento em que o dev pega o épico até o ciclo de fechamento descrito em `docs/process/refinement/epic_completion.md` ser completado.

**`✅ Implementado`** — código entregue e ciclo de fechamento executado.
Checklist em `docs/process/refinement/epic_completion.md` foi aplicado na íntegra.

### Alvo de Refinamento

Toda sessão de refinamento começa com um **alvo declarado** — o estado ao qual o épico deve chegar ao fim da sessão.

Formas típicas de declarar o alvo:
- "Quebrar esta visão em N épicos em `🌱 Visão` ou `📐 Funcionalidades esboçadas`."
- "Levar Épico X até `📋 Critérios definidos`."
- "Levar Épico X até `🔍 Detalhes definidos`."

O Claude Web conduz as perguntas até chegar ao alvo declarado, sem parar em estados intermediários. O alvo define:

- **Quanto contexto enviar:** pack inicial de 6 arquivos basta para alvos até `📋 Critérios definidos`; chegar a `🔍 Detalhes definidos` exige também inspeção de código e consulta a `autonomous_readiness.md`.
- **Quais artefatos são produzidos:** funcionalidades, critérios, detalhes de execução — proporcionais ao alvo.
- **Qual fluxo de execução o épico habilita ao final:** manual via Cursor a partir de `📋 Critérios definidos`; autônomo via Claude Code Web a partir de `🔍 Detalhes definidos`.

### Quando Refinar um Épico

**Refinamento em massa — visão → múltiplos épicos.**
Alvo típico: `🌱 Visão` ou `📐 Funcionalidades esboçadas` para cada épico produzido. Útil ao abrir um ROADMAP novo ou ao quebrar uma visão de produto em itens trabalháveis. Não tenta amadurecer cada épico individualmente.

**Refinamento profundo — épico por épico.**
Alvo típico: `📋 Critérios definidos` ou `🔍 Detalhes definidos`. Acontece quando o épico se aproxima de ser trabalhado: dependências técnicas foram implementadas e validadas, valor e viabilidade estão claros. Tenta amadurecer um épico específico até o alvo declarado, não preventivamente.

### Ajuste de Profundidade por Estágio (POC / Protótipo / MVP)

O nível de detalhe exigido para atingir `🔍 Detalhes definidos` varia por estágio:

- **POC:** tolera simplificações explícitas — persistência em memória, ausência de testes automatizados para UI, atalhos de autenticação, stubs em lugar de integrações reais. As simplificações ficam registradas como tal no épico, não como dívida oculta.
- **Protótipo:** exige checklist integral de `autonomous_readiness.md`.
- **MVP:** exige checklist integral de `autonomous_readiness.md` + adequação ao uso por terceiros (tratamento de erro, mensagens, tolerância a entrada ruim).

Os detalhes específicos de cada ajuste por estágio moram em `docs/process/refinement/autonomous_readiness.md`.

---

## Princípio Fundamental

**Roadmap = FUTURO** (próximos passos + ideias)
**Documentação Técnica = PRESENTE** (estado atual do sistema)

---

## Categorias de Épicos

### Estados de Refinamento (antes do código)

- **`🌱 Visão`** — apenas objetivo. Aguarda refinamento. Nenhum fluxo de execução disponível.
- **`📐 Funcionalidades esboçadas`** — funcionalidades listadas sem critérios de aceite. Aguarda refinamento. Nenhum fluxo de execução disponível.
- **`📋 Critérios definidos`** — critérios de aceite definidos. Apto ao fluxo manual via Cursor.
- **`🔍 Detalhes definidos`** — checklist de `autonomous_readiness.md` aplicado. Apto ao fluxo autônomo via Claude Code Web.

### Estados de Execução

- **`🏗️ Em andamento`** — épico em implementação (inclui o ciclo de fechamento até sua conclusão).
- **`✅ Implementado`** — ciclo de fechamento executado. Ver `docs/process/refinement/epic_completion.md`.

**Claude Code só implementa funcionalidades de épicos em `📋 Critérios definidos` (fluxo manual) ou `🔍 Detalhes definidos` (fluxo autônomo). Ao iniciar a implementação, o épico transita para `🏗️ Em andamento`; ao final do ciclo de fechamento, para `✅ Implementado`.**

---

## Estrutura do Roadmap

### 💡 IDEIAS FUTURAS
Ideias abstratas que ainda não viraram épicos. Aguardando maturação.

### 🎯 MILESTONES

Um **milestone** agrupa épicos relacionados dentro de um mesmo estágio (POC/Protótipo/MVP) = uma sessão de trabalho coerente. É a unidade de entrega do **fluxo autônomo** — disparo por linguagem natural ("implementa a POC do Ensaio"), execução na branch `milestone/<id>`, merge em main apenas com aval humano. Definição canônica em [docs/CONSTITUTION.md §9](../../CONSTITUTION.md).

**Quem decide o agrupamento em milestones.** O agrupamento de épicos em milestones é **output do refinamento estratégico** (Claude Web, fora da branch), junto da declaração dos próprios épicos. Não é decisão da PM skill (que faz refinamento tático dentro da branch sobre um milestone já declarado) nem da EM skill (que só faz sizing do milestone declarado). Quando o refinamento estratégico descobre acoplamento entre épicos, declara-os no mesmo milestone; quando detecta que épicos do mesmo estágio são independentes, declara milestones separados.

**Convenção de id:** `<ESTAGIO>-<PRODUTO>` em caixa alta, com hífen. Ex.: `POC-ENSAIO`, `PROTO-REVELAR`, `MVP-ENSAIO`. Quando um estágio precisa ser quebrado em mais de um milestone, acrescentar sufixo semântico ou ordinal: `POC-ENSAIO-ALPHA`, `POC-ENSAIO-BETA`, `PROTO-WORKFLOW-ENCERRAMENTO`. Nome da branch associada em caixa baixa: `milestone/poc-ensaio`, `milestone/proto-workflow-encerramento`.

**Quando dividir um estágio em múltiplos milestones.** Dois gatilhos:

1. **Proativo (refinamento estratégico):** o próprio agrupamento estratégico separa milestones quando os épicos são independentes ou quando o escopo total do estágio é maior que uma sessão coerente. Este é o caminho normal.
2. **Reativo (EM skill no sizing):** milestone cujo sizing retornar OVERFLOW **nunca** é executado como está — a EM skill devolve ao dev com proposta de quebra; a decisão efetiva volta ao refinamento estratégico para re-agrupar. Milestones com sizing TIGHT seguem sem aval adicional.

Template mínimo para cada milestone no ROADMAP do produto:

```markdown
### <ID>  <!-- ex: POC-ENSAIO -->

- **Objetivo:** <o que esse milestone entrega em 1-2 linhas, focado em valor de negócio>
- **Estágio:** <POC | Protótipo | MVP>
- **Produto:** <nome do produto>
- **Épicos agrupados:** <lista dos ids dos épicos, ex: E-POC-1, E-POC-2, E-POC-3>
- **Dependências de core:** <lista de épicos C-<PRODUTO>-* ou ÉPICO N do core; "nenhuma" se for o caso>
- **Branch associada:** `milestone/<id-em-caixa-baixa>`
- **Status dos épicos:** <resumo dos estados atuais dos épicos agrupados>
- **Feedback do estágio anterior endereçado:** <itens vindos da validação manual do estágio anterior que este milestone resolve. Para cada item: de onde vem (ex.: validação pós-merge do milestone X) e como é endereçado (épico Y cobre; trabalho preparatório fora de épico; etc.). "Nenhum" se o milestone não inclui higiene pós-validação. Bucket existe para evitar que dívidas pós-validação se percam entre ficha técnica e ROADMAP.>
- **Nota:** <se stub: declarar que é declarativo; se houver épicos ainda em 🌱/📐, mencionar refinamento tático pela PM skill dentro da branch>
```

Milestones vivem na seção `## 🎯 Milestones` de cada ROADMAP de produto, logo antes de `## 📋 Épicos Planejados`. O core (`docs/ROADMAP.md`) não tem milestones próprios — usa uma tabela `## 🎯 Épicos Core × Milestones de Produto` para declarar quais épicos core entram em qual milestone de produto (ver lá).

**Épicos podem ficar órfãos na fase.** O ROADMAP aceita épicos listados dentro de uma fase (`### ⏳ Fase <Estágio>`) **sem atribuição de milestone** — é o estado natural de um épico em `🌱 Visão` ou `📐 Funcionalidades esboçadas` que ainda não foi agrupado. Forçar a atribuição prematura empurra o erro de acoplar épicos desconexos num mesmo milestone. Milestone só é declarado quando o refinamento estratégico identifica um **agrupamento coeso**.

#### Checklist de coerência para declarar um milestone

Antes de declarar um milestone no ROADMAP (refinamento estratégico), aplicar este checklist aos épicos candidatos:

1. **Compartilham arquivos-alvo ou código?** Épicos que tocam os mesmos módulos, configs ou contratos são fortes candidatos a milestone único.
2. **Compartilham conceitos centrais ou rito?** Ex.: W-PROTO-5/6/7 dividem o rito de `epic_completion.md` — coupling conceitual, mesmo sem compartilhar código. W-PROTO-1/2/3/4 são dívida documental que não toca os mesmos arquivos nem conceitos — coupling zero.
3. **Cabem numa sessão (sizing tentativo FIT ou TIGHT)?** Estimativa grosseira via heurística de `docs/process/sizing/heuristic.md`; OVERFLOW antecipado → declarar dois milestones de saída.

**Regra:** 2+ respostas negativas → declarar milestones separados. 2+ respostas positivas → milestone único é adequado.

#### Anti-padrão: milestone-balaio

Declarar um milestone com **todos os épicos remanescentes de uma fase** sem aplicar o checklist acima. Resultado: milestone inchado, baixo acoplamento interno, sessão autônoma inviável — split retroativo vira obrigatório, desperdiçando refinamento tático já executado.

**Exemplo canônico:** `PROTO-WORKFLOW` foi declarado em 2026-04 com 7 épicos heterogêneos (W-PROTO-1..7) sob a heurística implícita "1 estágio = 1 milestone". Durante o refinamento dos épicos em 2026-04-24, o desacoplamento ficou visível e o milestone foi splittado retroativamente em `PROTO-WORKFLOW-ENCERRAMENTO` (W-PROTO-5/6/7, coupling de rito) e `PROTO-WORKFLOW-DOC` (W-PROTO-1/2/3/4, coupling zero entre si e com os outros). O checklist acima foi introduzido nesta reforma como prevenção.

#### Defesa secundária: sinalização tardia

O checklist estratégico é a primeira linha de defesa — quando falha, a **EM skill** (sizing dentro da branch do milestone) é a última oportunidade de detectar o erro antes de desperdiçar implementação. Hoje a EM decide sobre tamanho (FIT/TIGHT/OVERFLOW); num cenário futuro pode ganhar heurística de coerência (detectar baixo acoplamento entre épicos do milestone e emitir warning pro dev avaliar split). Essa evolução da EM é registrada como observação no ROADMAP do workflow e vira épico quando houver sinal real de necessidade (um erro recorrente que o checklist estratégico não pega).

### 📍 PRÓXIMOS PASSOS

**Épicos percorrem até seis estados:**

- **`🌱 Visão`** — apenas objetivo definido. Aguarda refinamento.
- **`📐 Funcionalidades esboçadas`** — funcionalidades listadas sem critérios de aceite. Aguarda refinamento.
- **`📋 Critérios definidos`** — critérios de aceite definidos. Pronto para fluxo manual via Cursor.
- **`🔍 Detalhes definidos`** — checklist de `autonomous_readiness.md` aplicado. Pronto para fluxo autônomo via Claude Code Web.
- **`🏗️ Em andamento`** — implementação em curso (até concluir o ciclo de fechamento).
- **`✅ Implementado`** — ciclo de fechamento executado (ver `epic_completion.md`).

**Fluxo:**
```
Ideia → Épico (🌱 Visão)
      → refinamento com alvo 📐
      → Épico (📐 Funcionalidades esboçadas)
      → refinamento com alvo 📋
      → Épico (📋 Critérios definidos) — executável em fluxo manual
      → refinamento com alvo 🔍 (checklist autonomous_readiness)
      → Épico (🔍 Detalhes definidos) — executável em fluxo autônomo
      → dev pega
      → Épico (🏗️ Em andamento)
      → ciclo de fechamento (epic_completion)
      → Épico (✅ Implementado)
```

**Atalhos permitidos no fluxo:**
- Um épico pode pular direto de `🌱 Visão` para `📋 Critérios definidos` em uma única sessão com alvo `📋`, sem passar explicitamente por `📐`.
- Um épico pode pular direto para `🔍 Detalhes definidos` a partir de `🌱 Visão` ou `📐 Funcionalidades esboçadas` em uma sessão com alvo `🔍`, desde que o checklist de `autonomous_readiness.md` seja aplicado ao final.

### ✅ CONCLUÍDO RECENTEMENTE
Resumo enxuto (1-2 linhas) dos últimos épicos. Remove manualmente quando acumular.

---

## Template: Épico nos Seis Estados

O épico evolui acumulando conteúdo a cada estado. Cada estado é o anterior acrescido de novo bloco.

### Estado `🌱 Visão`

Saída de uma sessão "me quebra essa visão em épicos" ou da promoção de uma ideia para épico formal.

```markdown
## ÉPICO X: Nome Descritivo
**Status:** 🌱 Visão

**Objetivo:** [O que queremos alcançar com este épico. Foco no valor de negócio.]
```

### Estado `📐 Funcionalidades esboçadas`

Saída típica de refinamento em massa (visão → N épicos), quando as funcionalidades já emergiram em descrição curta.

```markdown
## ÉPICO X: Nome Descritivo
**Status:** 📐 Funcionalidades esboçadas

**Objetivo:** [...]

### Funcionalidades (esboço):
- X.1 Nome da Funcionalidade — [descrição em 1 frase]
- X.2 Nome da Funcionalidade — [descrição em 1 frase]
- X.3 Nome da Funcionalidade — [descrição em 1 frase]
```

### Estado `📋 Critérios definidos`

Saída de refinamento com alvo `📋`. Cada funcionalidade ganha descrição completa e critérios de aceite.

```markdown
## ÉPICO X: Nome Descritivo
**Status:** 📋 Critérios definidos

**Objetivo:** [...]

### Funcionalidades:
#### X.1 Nome da Funcionalidade
- **Descrição:** [1-2 frases]
- **Critérios de Aceite:**
  - Deve [comportamento observável]
  - Deve [comportamento observável]

#### X.2 Nome da Funcionalidade
[...]
```

### Estado `🔍 Detalhes definidos`

Saída de refinamento com alvo `🔍`. Todo o conteúdo de `📋 Critérios definidos`, acrescido de uma seção de detalhes de execução para cada funcionalidade (checklist em `autonomous_readiness.md`).

```markdown
## ÉPICO X: Nome Descritivo
**Status:** 🔍 Detalhes definidos

**Objetivo:** [...]

### Funcionalidades:
#### X.1 Nome da Funcionalidade
- **Descrição:** [...]
- **Critérios de Aceite:** [...]
- **Detalhes de execução:**
  - **Arquivos a criar:** `<caminho/completo>`
  - **Arquivos a modificar:** `<caminho/completo>`
  - **Contratos/Shapes:** [estados compartilhados, inputs/outputs relevantes]
  - **Integração:** [onde o código entra, como é carregado, como é invocado]
  - **Template de referência:** [agente/componente análogo existente]
  - **Acoplamentos verificados:** [imports, dependências; refatorações prévias se houver]
  - **Dependências de ordem:** [funcionalidades/épicos que precisam vir antes]
  - **Escopo de teste:** [unit / integration / validação manual]
  - **Simplificações (se POC):** [simplificações explícitas assumidas, ex: persistência em memória]
```

### Estado `🏗️ Em andamento`

Dev pegou o épico. Status atualizado ao iniciar a implementação; permanece até o ciclo de fechamento em `epic_completion.md` ser concluído.

```markdown
## ÉPICO X: Nome Descritivo
**Status:** 🏗️ Em andamento — desde YYYY-MM-DD
**Branch:** feature/X.Y-nome (ou conjunto de branches, conforme o caso)

**Objetivo:** [...]

### Funcionalidades:
[conteúdo do estado anterior preservado — critérios + detalhes de execução]
```

### Estado `✅ Implementado`

Ciclo de fechamento executado. Ver `docs/process/refinement/epic_completion.md`.

```markdown
## ✅ ÉPICO X: Nome Descritivo
Resumo enxuto (1-2 linhas) do que foi entregue. Detalhes, critérios e execução saem do roadmap ativo ao entrar para "Concluído Recentemente".
```

**Qual alvo declarar em cada sessão de refinamento?** Ver seção "Seis Estados de Refinamento" e "Alvo de Refinamento" acima.

---

## Exemplo de Épico

```markdown
## ÉPICO 3: Autenticação Google

**Objetivo:** Simplificar acesso ao sistema substituindo email/senha por autenticação Google, melhorando segurança e experiência do usuário.

### Funcionalidades:
#### 3.1 Implementação de Google OAuth
#### 3.2 Controle de Acesso via Gestores Cadastrados
#### 3.3 Preparação da Estrutura de Dados
```

---

## Critérios de Qualidade para Épicos

✅ Objetivo claro: Foca no valor de negócio, não em implementação técnica
✅ Coeso: Funcionalidades relacionadas que fazem sentido juntas
✅ Tamanho adequado: 2-5 funcionalidades (nem muito pequeno, nem gigante)
✅ Incremental: Entrega valor mesmo se parar no meio

---

## Template: Funcionalidade

```markdown
#### X.Y Nome Específico da Funcionalidade

- **Descrição:** [O que é esta funcionalidade em 1-2 frases]
- **Critérios de Aceite:**
  - Deve [comportamento esperado específico e testável]
  - Deve [comportamento esperado específico e testável]
  - Não deve [comportamento indesejado se relevante]
```

---

## Exemplo de Funcionalidade

```markdown
#### 3.1 Implementação de Google OAuth

- **Descrição:** Configurar autenticação via Google OAuth no backend e frontend
- **Critérios de Aceite:**
  - Página de login deve ter apenas botão "Entrar com Google"
  - Após autenticação Google, verificar se email está na lista autorizada
  - Se email autorizado: criar/atualizar usuário e gerar JWT
  - Se email não autorizado: exibir mensagem de acesso negado
```

---

## Critérios de Qualidade para Funcionalidades

✅ Testável: Critérios de aceite observáveis e validáveis
✅ Incremental: Entrega valor sozinha
✅ Específica: Escopo claro
✅ Valor claro: Benefício concreto
✅ Única: Não se sobrepõe a outras funcionalidades

---

## Manutenção do Roadmap

Ao iniciar implementação: status do épico transita para `🏗️ Em andamento`.

Ao concluir o ciclo de fechamento descrito em `docs/process/refinement/epic_completion.md`:
1. Marque o título do épico com ✅ e atualize status para `✅ Implementado`
2. Resuma em 1-2 linhas o que foi entregue
3. Remova detalhes (objetivo, critérios, sub-funcionalidades)
4. Mova para "✅ Concluído Recentemente"

Exemplo:

```markdown
## ✅ ÉPICO 2: Padronização da Interface de Resumos
Sistema com layout consistente entre páginas de resumo, exibindo dados completos do projeto via API.
```

---

## Tarefas

Uma tarefa é um conjunto incremental de atividades relacionadas que:
- ✅ É curta e focada
- ✅ Agrega valor imediatamente
- ✅ É testável
- ✅ Pode ser comitada independentemente
- ✅ Permite rollback fácil

### Mentalidade Incremental
Progresso contínuo: **POC → Protótipo → MVP → Melhorias**

Processo: Fazer → Validar → Commit → Iterar

---

## Workflow do Claude Code

### Antes de Começar
1. Verifique dúvidas ou decisões em aberto
2. Confirme o estado do épico no ROADMAP:
   - **Fluxo manual via Cursor:** mínimo `📋 Critérios definidos`
   - **Fluxo autônomo via Claude Code Web:** exige `🔍 Detalhes definidos` (checklist `autonomous_readiness.md` aplicado)
3. Alinhe o escopo com o usuário
4. Ao iniciar, atualize o status do épico para `🏗️ Em andamento`

### Durante Implementação
- Trabalhe em funcionalidades (não épicos inteiros)
- Commits incrementais
- PR/merge só ao final da funcionalidade

### Comunicação
- Pergunte quando algo não estiver claro
- Evite assumir decisões de arquitetura

---

## Quando Parar e Perguntar
- Falta de informação
- Decisões arquiteturais abertas
- Múltiplas abordagens possíveis
- Épico em `🌱 Visão` ou `📐 Funcionalidades esboçadas` (exige refinamento com alvo mínimo `📋 Critérios definidos`)
- Fluxo autônomo disparado sobre épico em `📋 Critérios definidos` (exige refinamento com alvo `🔍 Detalhes definidos`, guiado por `autonomous_readiness.md`)

---

## Git Workflow
- Branches flexíveis no início
- Commits frequentes e descritivos
- Uma funcionalidade por PR
- Conflitos resolvidos com apoio do usuário

---

## Estratégia de Testes
- TDD pragmático (lógica crítica primeiro)
- Reavalie a estratégia conforme o projeto evolui
- **Detalhes técnicos**: `docs/testing/README.md` (pirâmide de testes, mocks vs API real, estrutura)

---

## Retrospectiva de Sessão
- Documente bloqueios, perdas de eficiência e melhorias sugeridas
- Sempre alinhe antes de atualizar documentação compartilhada

