# Paper Agent — a visão, em resumo

> Resumo da visão do repositório `paper-agent`, para dar a quem não tem o
> repositório em mãos uma noção fiel **do que é e por que existe** — sem
> despejar arquivo por arquivo. Conciso, mas mostrando a profundidade.

---

## A ideia central

Paper Agent não é um app — é um **ecossistema**. Um **core universal** (a
máquina cognitiva) sustenta **vários produtos**, e todos giram em torno de um
mesmo eixo: **a relação entre ideia e palavra**.

Da ideia para a palavra é o caminho natural — pegar algo nebuloso na cabeça de
alguém e levá-lo até um texto claro, estruturado, publicável. Mas há também o
**caminho inverso**, que é o que dá ao projeto sua ambição maior: partir das
**palavras** e recuperar as **ideias, conceitos e crenças** que estão por trás
delas. Reconhecer que dois textos com vocabulário completamente diferente podem
estar dizendo a mesma coisa — e que essa essência transcende as palavras
usadas. É um problema que vale para religião, política, qualquer domínio de
pensamento. É um **projeto de longo prazo, de vida** — e o repositório é a
fundação que vai sendo construída em direção a isso.

## A filosofia que dá profundidade

O que separa Paper Agent de "mais um wrapper de LLM" é a postura epistemológica,
declarada de forma explícita no core:

- **O sistema não julga verdade — mapeia sustentação.** Uma proposição não é
  "verdadeira" ou "falsa": ela tem **solidez**. Pesquisar **fortalece ou
  enfraquece** um argumento; não "valida ou refuta". Isso muda o comportamento
  de todos os produtos — eles não dão veredito, eles expõem fundamentação.
- **A clareza é onde mora o esforço.** A aposta é que, com objetivos bem
  definidos, a execução vira o passo mais fácil. Por isso o sistema concentra
  energia no **pensamento que antecede a escrita**, não na geração em si.
- **As essências transcendem as palavras.** "Alinhamento", "coordenação",
  "sincronização" podem ser a mesma ideia. O sistema persegue essa abstração —
  detectar similaridade semântica entre conceitos, não casar strings.

## O core: a máquina compartilhada

Todos os produtos herdam a mesma base, e é isso que torna o ecossistema coerente
em vez de uma coleção de ferramentas soltas:

- Um sistema **multi-agente conversacional**, onde agentes especializados
  **negociam o caminho junto com o usuário** em vez de devolver uma resposta
  fechada. Os papéis centrais: o **Orquestrador** (facilita, provoca, expõe
  suposições implícitas), o **Estruturador** (organiza e cristaliza argumentos)
  e o **Metodologista** (guarda o rigor lógico). Outros agentes — Writer,
  Researcher, Curator — entram conforme os produtos amadurecem.
- Uma **ontologia** comum — Conceito, Ideia, Argumento — e uma **biblioteca
  vetorial** de conceitos que cresce com tudo que passa pelo sistema. O
  conhecimento articulado num produto fica disponível para os outros.
- Uma separação dura: **a inteligência vive no core; a interface de cada produto
  é "burra"**, só renderiza e chama o core. Trocar a cara de um produto não
  toca na regra de negócio.

## Os produtos (o pipeline)

A visão é um **pipeline** de produtos paralelos que compartilham o core, cada um
cobrindo uma etapa da jornada ideia ↔ palavra:

- **Revelar** *(o mais maduro)* — **clareza de pensamento**. Um diálogo
  socrático que transforma confusão mental em conceitos claros. Não escreve o
  texto final: entrega a ideia lapidada (claim, fundamentos, solidez). É o
  ateliê onde a ideia bruta vira diamante.
- **Prisma Verbal** *(o caminho inverso)* — **fichamento**. Parte de textos
  estáticos (livros, papers, PDFs) e extrai as ideias e conceitos por trás
  deles. É o produto que materializa a ambição maior do projeto: abstrair das
  palavras para a essência, e conectar textos pela ideia que carregam, não pelo
  vocabulário. Mantém um catálogo que aprende com o uso.
- **Camadas da Linguagem** *(futuro)* — pega a ideia clara e a **estrutura como
  mensagem** para um interlocutor.
- **Expressão** *(futuro)* — dá **forma** à mensagem em conteúdo (formatos
  diversos).
- **Produtor Científico** *(futuro)* — especialização de Expressão para o
  **artigo acadêmico genérico**.
- **Ensaio** *(o foco atual)* — ver abaixo.

## Ensaio: o produto em foco

Ensaio transforma **experimentos de código em artigos técnico-científicos**. O
experimento acontece no repositório; o artigo **emerge da conversa** entre o
pesquisador e o sistema. O problema que ataca é concreto: o ritmo dos
experimentos supera a capacidade de escrever sobre eles, e o aprendizado se
perde no código.

O diferencial é a **postura crítica e proativa**. O sistema não espera o usuário
saber o que dizer — ele **provoca**: identifica lacunas no argumento e cobra
métricas, evidências e informações que o artigo vai exigir. Os agentes
**perguntam para ter clareza**, e esse grau de criticidade é **calibrado por
engenharia de prompt e de arquitetura** — o trabalho fino é justamente garantir
que o sistema seja criterioso nas análises e nas recomendações, e que entregue,
no fim, um artigo com rigor real. A autoria continua sendo do pesquisador; o
sistema é o laboratório de escrita.

A visão amadurece por estágios — de uma sessão única que prova o conceito até um
**fluxo assíncrono** onde o artigo evolui ao longo de semanas, com o sistema
trabalhando entre as sessões e o usuário voltando para encontrar pendências e
rascunhos esperando por ele.

## A plataforma de workflow: o produto que nasceu do processo

Há ainda uma frente que surgiu **de dentro do próprio desenvolvimento** do Paper
Agent e está virando produto próprio. Para construir o ecossistema com agentes,
o projeto formalizou seus fluxos de trabalho — refinar, implementar, encerrar —
como **skills** orquestradas. A percepção é que isso é, em si, um produto: uma
**plataforma de humano-no-loop**.

A forma da visão: os **agentes trabalham em segundo plano**, em branches
isoladas, e o **humano chega para validar, opinar e destravar** — sem
supervisão contínua. O operador encontra uma **fila** de decisões pendentes, um
**kanban** do estado do trabalho e um **chat focado** por item; o modelo é
*pull* (chega e vê), não alerta que interrompe, e a aprovação de PR é o único
portão humano. O **Ensaio é o campo de prova** dessa plataforma — o primeiro
caso de uso real. A médio prazo, a plataforma se desacopla do paper-agent e vira
ferramenta própria, usável contra outros repositórios.

## O fio que liga tudo

O eixo é sempre o mesmo: **dar fluidez à entrada e à saída de informação** — ler
e fichar de um lado (Prisma Verbal, Curator), produzir e escrever do outro
(Ensaio, Expressão), com um core que trata pensamento como algo a ser
estruturado e sustentado, não como texto a ser gerado. É infraestrutura para
pensar e produzir conhecimento de forma contínua. O resto do ecossistema são as
faces dessa mesma intenção, e a ambição de fundo — abstrair das palavras para as
ideias — é o norte que justifica a complexidade.
