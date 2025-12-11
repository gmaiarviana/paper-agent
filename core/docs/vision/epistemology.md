# Epistemologia do Paper Agent

## 1. Motivação

Em um mundo onde código está se tornando commodity e LLMs generalistas são acessíveis a todos, o diferencial de sistemas no futuro não será a capacidade técnica, mas as **crenças e filosofias** que guiam sua arquitetura.

Paper Agent não é apenas uma coleção de agentes e ferramentas. É um sistema guiado por uma epistemologia específica — uma forma particular de entender como conhecimento é construído, como argumentos são sustentados e como verdades emergem (ou não emergem) da evidência.

Esta epistemologia não é decorativa. Ela permeia cada decisão de design, cada interação com o usuário, cada forma como o sistema organiza e apresenta informação. É a fundação sobre a qual toda a arquitetura se constrói.

## 2. Princípio Central

**"Não existe verdade absoluta, apenas narrativas com diferentes graus de sustentação."**

Este princípio central desloca o sistema de uma lógica binária (verdadeiro/falso, certo/errado) para uma lógica de gradação (sólido/frágil, forte/fraco, com evidências/sem evidências).

### Desdobramentos

- **Nenhuma afirmação é "fato" ou "suposição" de forma binária**: Toda proposição existe em um espectro de solidez que varia conforme evidências acumuladas.

- **Toda afirmação tem um grau de solidez baseado em evidências**: Uma proposição não é inerentemente verdadeira ou falsa; ela é mais ou menos sustentada por evidências disponíveis.

- **O sistema não julga verdade, apenas mapeia sustentação**: Paper Agent não determina o que é "correto", mas sim o quão bem fundamentada uma afirmação está no momento atual.

- **Sólido/frágil substitui verdadeiro/falso**: Linguagem do sistema evita dicotomias absolutas, preferindo descrições de solidez relativa.

- **Forte/fraco substitui certo/errado**: Argumentos são avaliados por força de sustentação, não por correção binária.

- **Com evidências/sem evidências é o que importa**: O que diferencia uma proposição sólida de uma frágil não é sua natureza intrínseca, mas a presença e qualidade de evidências que a sustentam.

## 3. Princípio da Boa-Fé Epistemológica

**"Todos falam a verdade, baseado em seus pontos de observação."**

Este princípio assume boa-fé epistemológica: não existe afirmação "falsa" no sentido absoluto, apenas afirmações que emergem de contextos e pontos de observação diferentes.

### Implicações

- **Não existe afirmação "falsa", apenas afirmação com contexto/observação diferente**: O sistema não descarta perspectivas como incorretas, mas mapeia os contextos que as geram.

- **Ponto de observação importa**: "Terra orbita Sol" é verdadeiro se Sol é referência; "Sol orbita Terra" é verdadeiro se Terra é referência. A questão não é qual está "certo", mas qual referencial está sendo usado.

- **Sistema não descarta perspectivas, mapeia contextos**: Quando duas afirmações parecem conflitantes, o sistema não escolhe uma como correta, mas identifica os pontos de observação que geram cada perspectiva.

- **Conflito de afirmações = conflito de pontos de observação**: Tensões entre proposições são resolvidas não por julgamento de verdade, mas por exploração de contextos e referenciais.

## 4. Tudo São Narrativas

Argumentos científicos não são caminhos determinísticos para "verdade". São **storytelling estruturado** — narrativas que organizam evidências de forma coerente e persuasiva.

### Características das Narrativas

- **Argumentos são storytelling estruturado**: Um argumento científico é uma narrativa que conecta evidências, premissas e conclusões de forma lógica e convincente.

- **Não existe caminho determinístico para "verdade"**: Não há algoritmo que, dado um conjunto de evidências, produza uma única "verdade" correta. Há múltiplas narrativas possíveis.

- **Solidez emerge de evidências acumuladas, não de lógica binária**: Uma narrativa se torna mais sólida não porque passa por um teste de verdade, mas porque acumula evidências que a sustentam.

- **Uma narrativa pode ser fortalecida ou enfraquecida, nunca "provada"**: O sistema não busca provar ou refutar, mas fortalecer ou enfraquecer narrativas através de evidências e análise crítica.

## 5. O Sistema Como "Mente"

Paper Agent funciona como a mente de uma pessoa analisando informações: não julga, organiza; não prova, mapeia sustentação; não descarta, rastreia fragilidades; não conclui, provoca reflexão.

### Metáfora da Mente

- **Não julga, organiza**: O sistema não determina o que é correto ou incorreto, mas organiza informações de forma que padrões de sustentação fiquem visíveis.

- **Não prova, mapeia sustentação**: Em vez de buscar provas definitivas, o sistema mapeia quão bem cada proposição é sustentada por evidências disponíveis.

- **Não descarta, rastreia fragilidades**: Proposições frágeis não são eliminadas, mas marcadas com suas fragilidades para que o usuário possa decidir como lidar com elas.

- **Não conclui, provoca reflexão**: O sistema não fecha questões com conclusões definitivas, mas abre novas questões que provocam reflexão e refinamento.

## 6. Implicações Para a Arquitetura

A epistemologia do sistema se materializa em decisões arquiteturais específicas que permeiam toda a implementação.

### Proposições Substituem Premise/Assumption

- **Não há tipos binários**: O sistema não classifica proposições como "premise" (verdadeira) ou "assumption" (hipotética). Todas são proposições com diferentes graus de solidez.

- **Estrutura unificada**: Ver `../architecture/data-models/ontology.md` para estrutura de Proposição que unifica o que antes eram tipos distintos.

### Solidez Derivada de Evidências

- **Não definida manualmente**: A solidez de uma proposição não é atribuída pelo usuário ou sistema, mas derivada automaticamente das evidências que a sustentam.

- **Evolução dinâmica**: Conforme novas evidências são adicionadas ou contradições são identificadas, a solidez é recalculada dinamicamente.

- **Rastreabilidade**: Ver `core/docs/vision/cognitive_model/evolution.md` para como solidez evolui na conversa através de evidências acumuladas.

### Rastreabilidade de Fragilidade

- **Propagação de fragilidade**: Quando uma proposição é identificada como frágil, o sistema rastreia quais argumentos dependem dela e indica como essa fragilidade afeta a solidez geral.

- **Dependências explícitas**: A arquitetura mantém rastreabilidade clara de como fragilidades em proposições base afetam argumentos que dependem delas.

### Pesquisa Não Valida/Refuta

- **Fortalecimento/enfraquecimento**: Quando o Pesquisador busca literatura, o resultado não é "validação" ou "refutação" binária, mas fortalecimento ou enfraquecimento da narrativa através de evidências encontradas.

- **Múltiplas perspectivas**: A pesquisa pode encontrar evidências que fortalecem alguns aspectos e enfraquecem outros, sem produzir um veredicto único.

## 7. Implicações Para UX

A epistemologia do sistema se manifesta diretamente na experiência do usuário, guiando como o sistema comunica e interage.

### Linguagem Não-Julgadora

- **Sistema nunca diz "isso é falso"**: Em vez de julgamentos binários, o sistema apresenta observações sobre sustentação: "Essa proposição tem poucas evidências que a sustentam no momento."

- **Sistema diz "essa proposição tem poucas evidências"**: A linguagem descreve estado de sustentação, não correção absoluta.

### Visualização de Graus de Solidez

- **Usuário vê graus de solidez, não checkmarks binários**: A interface apresenta proposições com indicadores visuais de solidez (cores, barras, ícones) que refletem graus de sustentação, não estados binários de verdade/falsidade.

- **Espectro contínuo**: Em vez de "verificado" ou "não verificado", o usuário vê um espectro que vai de "muito sólido" a "muito frágil".

### Pesquisa Como Conversa, Não Veredicto

- **"Fortalecer com pesquisa" abre conversa, não retorna veredicto**: Quando o usuário solicita pesquisa, o resultado não é um "sim, está correto" ou "não, está errado", mas uma conversa sobre como as evidências encontradas fortalecem ou enfraquecem diferentes aspectos da narrativa.

- **Exploração contínua**: A pesquisa não fecha questões, mas abre novas linhas de exploração e refinamento.

## Referências

- `../architecture/data-models/ontology.md` - Estrutura de Proposição e como solidez é representada na ontologia
- `core/docs/vision/cognitive_model/evolution.md` - Como solidez evolui na conversa através de evidências acumuladas e refinamento progressivo

