# Processo de Leitura

Documentação de como o sistema Prisma Verbal lê textos sequencialmente, extrai proposições e rastreia a evolução de conceitos.

## 1. Leitura Sequencial (Ordem Importa)

### Princípio

Sistema lê como humano - sentença por sentença, acumulando contexto.

### Por que ordem importa

- **Conceito X (parágrafo 2) depende de conceito Y (parágrafo 1)**
  - Autor estabelece fundamentos antes de elaborar
  - Dependências conceituais seguem ordem de apresentação

- **Autor elabora progressivamente (não dá tudo de uma vez)**
  - Conceitos são introduzidos vagamente e refinados ao longo do texto
  - Significado completo emerge através de múltiplas menções

- **Contexto acumula (significado de "física" fica claro conforme texto avança)**
  - Primeira menção: conceito vago
  - Menções subsequentes: adicionam especificidade
  - Contexto histórico e dependências se tornam claros progressivamente

### Exemplo

**Parágrafo 1:** "Big Bang originou universo"
  → Sistema registra: #1

**Parágrafo 2:** "Física estuda características fundamentais"
  → Sistema conecta: #2 apoia-se em #1

### Não fazer

❌ Quebrar em tokens e processar fora de ordem
- Perde dependências conceituais
- Quebra fluxo de elaboração progressiva

❌ Resumir texto antes de ler
- Perde nuances e contexto acumulado
- Remove informações necessárias para dependências

❌ Pular parágrafos "menos importantes"
- Importância só fica clara após leitura completa
- Parágrafos "menores" podem conter elos críticos

## 2. Extração de Proposições

### O que é proposição (no contexto Prisma)

**Proposição** = Afirmação sobre como realidade funciona

- **Pode ser explícita:** "Big Bang originou universo"
  - Afirmação direta e clara
  - Fácil de identificar e extrair

- **Pode ser implícita:** "Física estuda..." (assume universo tem características estudáveis)
  - Afirmação inferida do contexto
  - Requer análise de pressupostos

### Como extrair

1. **Ler sentença**
   - Processar uma sentença completa por vez
   - Manter contexto das sentenças anteriores

2. **Identificar afirmação sobre realidade**
   - O que o autor está dizendo que é verdade?
   - Qual afirmação sobre o mundo está sendo feita?

3. **Identificar conceitos mencionados**
   - Quais conceitos aparecem na proposição?
   - Como eles se relacionam?

4. **Identificar dependências (apoia-se em quais proposições anteriores?)**
   - Esta proposição assume que outras proposições são verdadeiras?
   - Quais proposições anteriores são necessárias para esta fazer sentido?

### Exemplo

**Sentença:** "Átomos são estruturas de matéria e energia"

  ↓

**Proposição:** #3
- **Conceitos:** [Átomos, matéria, energia, estruturas]
- **Depende de:** #1 (matéria e energia existem)

## 3. Evolução de Conceitos

### Princípio

Conceito nasce vago → ganha contexto → fica claro

### Processo de Evolução

Conceitos não são definidos completamente na primeira menção. Eles evoluem através de múltiplas referências ao longo do texto.

### Exemplo: Evolução do conceito "Física"

**Turno 1 (introdução):**
- **Conceito:** Física
- **Contexto:** "estuda características fundamentais"
- **Status:** Vago (não sabemos QUAIS características)

**Turno 5 (elaboração - hipotético):**
- **Conceito:** Física
- **Contexto:** "massa, energia, tempo, espaço"
- **Status:** Mais claro (exemplos dados)

**Turno 20 (detalhamento - hipotético):**
- **Conceito:** Física
- **Contexto:** "leis como gravidade, termodinâmica"
- **Status:** Específico

### Rastreamento

Sistema mantém histórico de como cada conceito evolui:
- Primeira menção: contexto inicial
- Menções subsequentes: adições e refinamentos
- Estado atual: contexto acumulado completo

## 4. Rastreamento de Dependências

### Princípio

Cada proposição pode depender de proposições anteriores.

### Estrutura de Dependências

```
#1: Big Bang originou universo
  └─ Dependências: Nenhuma (base)

#2: Física estuda características fundamentais
  └─ Depende de: #1 (assume universo tem características)

#3: Átomos = estruturas de matéria/energia
  └─ Depende de: #1 (matéria/energia existem)

#4: Moléculas = átomos combinados
  └─ Depende de: #3 (átomos existem)
```

### Benefícios

**Sistema sabe genealogia de crenças:**
- Se #1 for questionado, todas dependentes são afetadas
- Permite mapear: "Essa afirmação se apoia em qual crença base?"

**Análise de fundamentos:**
- Identificar proposições base (sem dependências)
- Identificar proposições derivadas (com dependências)
- Mapear cadeias de raciocínio

**Validação de consistência:**
- Detectar contradições em proposições base
- Rastrear impacto de mudanças em proposições fundamentais

## 5. Checkpoints (Não Só No Final)

### Princípio

Ideias emergem progressivamente, não apenas no final do livro.

### Quando criar checkpoint

Sistema detecta que:
- **Proposições suficientes conectadas**
  - Padrão ou estrutura conceitual emergiu
  - Dependências formam um grafo coerente

- **Conceitos foram elaborados o suficiente**
  - Conceitos principais têm contexto adequado
  - Evolução chegou a um ponto de clareza

- **Padrão emergiu** (ex: hierarquia de ciências)
  - Estrutura ou organização conceitual identificada
  - Relações entre conceitos ficaram claras

### Exemplo: Sapiens (Introdução)

**Checkpoint 1 (após 5 proposições):**
- **Ideia parcial:** "Harari estabelece hierarquia de ciências"
- **Status:** Fundação estabelecida
- **Aguardar:** Próximos parágrafos para ideia profunda

### Múltiplas Ideias

Livro pode ter dezenas de ideias:
- Cada capítulo pode cristalizar 1-3 ideias
- Ideias se conectam (hierarquia de ciências → revolução cognitiva)
- Sistema não espera livro inteiro terminar

### Benefícios

- **Captura progressiva:** Não perde ideias que emergem cedo
- **Eficiência:** Processa em blocos, não apenas no final
- **Rastreabilidade:** Histórico de como ideias emergiram

## 6. Convergências/Divergências (Não Foco Inicial)

### Nota

Sistema detecta, mas não é prioridade na leitura sequencial.

### Quando detectar

**Proposição converge com autor conhecido:**
- Harari #2 ↔ Newton (mesma visão sobre física)
- Identificar alinhamento conceitual

**Proposição diverge de crença estabelecida:**
- Harari #1 ✗ Bíblia (visões diferentes sobre origem)
- Identificar contradições ou perspectivas alternativas

### Como usar

**Enriquecer contexto do conceito:**
- Adicionar informações sobre alinhamentos/divergências
- Não interrompe fluxo de leitura principal

**Preparar para comparações futuras (objetivo secundário):**
- Marcar pontos de convergência/divergência
- Usar em análises comparativas posteriores

### Prioridade

- **Primária:** Leitura sequencial e extração de proposições
- **Secundária:** Detecção de convergências/divergências
- **Não interrompe:** Fluxo de leitura sequencial

## 7. Princípios de Leitura Humana

### Trabalhar Apenas com O Que Foi Dito

**Princípio:** Sistema NÃO infere, NÃO assume, NÃO subentende.

**Fazer:**

- ✅ Extrair afirmações literais do texto

- ✅ Identificar conceitos mencionados explicitamente

- ✅ Rastrear dependências explícitas

**Não fazer:**

- ❌ "Harari provavelmente quer dizer X"

- ❌ "Por contexto cultural, Y deve significar Z"

- ❌ "Autor não disse, mas é óbvio que..."

**Exemplo:**

```
Texto: "Culturas são estruturas elaboradas"

Sistema registra:
  ✅ Culturas = estruturas elaboradas
  ✅ Criadas por Homo sapiens
  ✅ Surgiram há 70 mil anos

Sistema NÃO assume:
  ❌ O que são essas estruturas
  ❌ Por que são importantes
  ❌ Como funcionam
  
Sistema marca: Conceito parcial, aguardar elaboração
```

### Respeitar Limitações da Linguagem

**Princípio:** Se texto é confuso, evidência que texto É confuso.

**Quando texto é claro:**

- Sistema registra afirmação com alta confiança

- Conecta com proposições anteriores

- Avança na leitura

**Quando texto é vago:**

- Sistema marca: "Conceito vago/incompleto"

- Aguarda autor elaborar

- Não inventa contexto

**Quando texto é contraditório:**

- Sistema marca: "Tensão detectada entre #X e #Y"

- Não resolve contradição

- Aguarda autor esclarecer

**Exemplo:**

```
Parágrafo vago:
  "A essência do ser humano está em sua capacidade única"
  
Sistema:
  Conceito: "capacidade única humana"
  Status: VAGO (não especificou qual capacidade)
  Ação: Aguardar próximos parágrafos
  
Se autor NÃO elaborar:
  Evidência: Texto deixou lacuna
  Sistema: Preserva lacuna (não inventa)
```

### Acumulação de Contexto (Memória de Leitura)

**Princípio:** Humano lembra o que foi dito antes. Sistema também.

**Parágrafo 1 estabelece fundação:**

```
"Big Bang originou matéria e energia"
  → Sistema registra: #1
```

**Parágrafo 2 ASSUME parágrafo 1:**

```
"Física estuda características fundamentais do universo"
  → Sistema conecta: #2 depende de #1
  → Não precisa re-explicar "universo" (já estabelecido)
```

**Parágrafo 10 pode referenciar parágrafo 1:**

```
"Conforme vimos, matéria e energia surgiram no Big Bang"
  → Sistema reconhece: Autor referenciando #1
  → Não cria proposição nova, vincula à existente
```

**Memória permite:**

- ✅ Detectar quando conceito foi introduzido

- ✅ Rastrear evolução de conceito ao longo do texto

- ✅ Identificar quando autor referencia algo já dito

- ✅ Marcar quando autor referencia algo NÃO dito

### Elaboração vs Referência vs Lacuna

**Sistema diferencia três casos:**

**Caso 1: Autor ELABORA conceito**

```
Parágrafo 1: "Culturas são estruturas elaboradas"
Parágrafo 5: "Essas estruturas incluem mitos, leis, instituições"
  
Sistema: Conceito "culturas" EVOLUIU
  Status inicial: Vago
  Status atualizado: Mais claro (exemplos dados)
```

**Caso 2: Autor REFERENCIA conceito externo**

```
Parágrafo 10: "Como Darwin demonstrou..."
  
Sistema: Autor referencia Darwin (não incluído no texto)
  Ação: Criar link externo
  Tipo: Convergência com autor conhecido
```

**Caso 3: Autor deixa LACUNA**

```
Parágrafo 1: "A essência humana está em sua capacidade única"
Parágrafo 2: [muda de assunto sem explicar]
  
Sistema: Conceito "capacidade única" ficou INCOMPLETO
  Evidência: Texto tem lacuna
  Ação: Marcar lacuna, não inventar contexto
```

## 8. Anti-Padrões (O Que NÃO Fazer)

### ❌ Quebrar em Tokens Aleatórios

**Errado:**

```
Processar: ["Big", "Bang", "originou", "universo"]
Ordem: Embaralhar tokens
Resultado: Perde contexto sequencial
```

**Correto:**

```
Processar: "Big Bang originou universo" (sentença completa)
Ordem: Sequencial (parágrafo 1 → 2 → 3)
Resultado: Preserva contexto acumulativo
```

### ❌ Resumir Antes de Ler

**Errado:**

```
1. Gerar resumo do livro
2. Extrair conceitos do resumo
Problema: Perde elaboração progressiva
```

**Correto:**

```
1. Ler sequencialmente
2. Extrair conceitos conforme aparecem
3. Conceitos evoluem ao longo da leitura
Benefício: Captura evolução, não apenas estado final
```

### ❌ Pular Parágrafos "Menos Importantes"

**Errado:**

```
Detectar: Parágrafo é "só exemplo"
Ação: Pular
Problema: Exemplo pode conter elaboração crucial
```

**Correto:**

```
Processar: Todos parágrafos sequencialmente
Decisão: Sistema decide se parágrafo contribui
  - Se elabora conceito → registra evolução
  - Se é repetição → não cria proposição nova
  - Se é exemplo → vincula a proposição que ilustra
```

### ❌ Assumir Significado por Contexto Cultural

**Errado:**

```
Texto: "justiça"
Sistema assume: "Definição moderna ocidental"
Problema: Autor pode ter contexto diferente
```

**Correto:**

```
Texto: "justiça"
Sistema registra: Conceito mencionado
Sistema aguarda: Autor elaborar O QUE significa "justiça"
Se autor não elabora: Conceito fica vago/incompleto
```

