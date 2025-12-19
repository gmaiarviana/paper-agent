# Filosofia do Sistema - Core Universal

## Visão Geral

Este documento descreve a filosofia e princípios universais do core, aplicáveis a todos os produtos.

## Filosofia Epistemológica

Paper Agent é guiado por uma epistemologia específica: não existe verdade absoluta, apenas narrativas com diferentes graus de sustentação. Isso significa:
- Sistema não julga verdade, mapeia sustentação
- Proposições têm solidez (não são "verdadeiras" ou "falsas")
- Pesquisa fortalece/enfraquece, não valida/refuta
- Ver detalhes em `core/docs/vision/epistemology.md`

## Problema Moderno: Excesso de Informação

### Mudança de Paradigma

**Passado (até anos 2000):**
- Problema: **falta de informação**
- Bibliotecas limitadas, papers inacessíveis
- Desafio: encontrar informação relevante
- Solução: ampliar acesso (digitalização, internet)

**Presente (2020+):**
- Problema: **excesso de informação**
- Milhares de papers publicados mensalmente
- Qualidade variável (nem tudo é confiável)
- Desafio: distinguir sinal de ruído

### Implicações para o Sistema

**Sistema não apenas busca informação:**
- ❌ Trazer tudo que existe sobre tema (saturação)
- ❌ Assumir que mais informação = melhor resultado

**Sistema filtra e curadora:**
- ✅ Distinguir informação relevante de irrelevante (sinal vs ruído)
- ✅ Avaliar qualidade metodológica (fonte confiável?)
- ✅ Extrair proposições específicas (não ler tudo)
- ✅ Avaliar solidez baseada em coerência interna

**Capacidade que usuário não teria sozinho:**

Sem sistema:
- Encontra 50 papers → lê todos (semanas de trabalho)
- Qualidade variável → risco de bases fracas
- Sem critério claro → viés de confirmação

Com sistema:
- 50 papers → 10 candidatos → 3 papers confiáveis (horas)
- Validação metodológica automática → apenas papers sólidos
- Proposições extraídas com solidez → foco no relevante

## Memory em Camadas

O sistema utiliza uma arquitetura de memória inspirada na memória humana, onde informação recente é mais acessível que informação antiga:

**3 Camadas de Memória:**

- **Superficial (recente):** resumos condensados, busca rápida, últimos dias/semanas. Acesso imediato para contexto conversacional atual.
- **Intermediária:** snapshots de CognitiveModel, evolução da ideia ao longo do tempo. Acesso moderado, útil para revisar progresso.
- **Profunda (antiga):** mensagens literais, acesso mais lento, pode ser compactada periodicamente. Arquivo histórico completo.

**Degradação temporal natural:**
Informação de ontem está mais acessível que de mês passado. O sistema prioriza recência sem perder histórico, seguindo padrão natural de memória humana.

**Futuro:**
Compactação/arquivamento periódico (ex: anual) para manter performance sem perder rastreabilidade completa.

## Super-Sistema: Core Universal

> **Nota:** Para arquitetura completa do super-sistema, consulte `../architecture/vision/super_system.md`.

Paper Agent não é apenas um produto isolado. É a **primeira aplicação** de um super-sistema com core universal que serve múltiplos produtos.

**Produtos planejados:**
- **Revelar:** Clareza de ideias via diálogo (atual)
  - Interface: diálogo socrático
  - Entrada: conversa com usuário
  - Saída: Ideia clara e fundamentada
  
- **Prisma Verbal:** Extração de conceitos de textos (atual)
  - Interface: processamento de texto estático
  - Entrada: livros, papers, documentos
  - Saída: Argumentos extraídos e estruturados
  
- **Camadas da Linguagem:** Estruturação de mensagens (novo)
  - Interface: estruturação de ideias
  - Entrada: Ideia
  - Saída: Mensagem estruturada
  
- **Expressão:** Produção de conteúdo em formas diversas (novo)
  - Interface: produção de conteúdo
  - Entrada: Mensagem
  - Saída: Conteúdo (post, email, artigo, etc.)
  
- **Produtor Científico:** Artigos acadêmicos (especialização de Expressão)
  - Interface: produção de artigos acadêmicos
  - Entrada: Mensagem
  - Saída: Artigo acadêmico formatado

**Core compartilhado:**
- Motor Vetorial (operações vetoriais, inferências)
- Biblioteca Vetorial (Conceitos, Argumentos, Ideias, Proposições)
- Ontologia (Conceito, Ideia, Argumento, Proposição, Evidência)
- Modelo cognitivo (claim → fundamentos (com solidez variável))
- Agentes (Orquestrador, Estruturador, Metodologista, Pesquisador)
- Infraestrutura (LangGraph, ChromaDB, embeddings)

Produtos são **serviços desacoplados** que consomem core via APIs.

## Informação vs Dados (Filosofia Orientadora)

### Princípio Central
Sistema extrai **informação** (proposições específicas com contexto), não acumula **dados** (catálogos redundantes).

### O Que É Informação
- **Proposição específica:** "Smith et al. (2023) afirma que LLMs reduzem tempo em 30% em equipes Python (solidez: 0.85)"
- **Não é:** "Paper X fala sobre LLMs e produtividade"

### O Que É Dado
- Catálogo genérico sem contexto
- Referência sem extração de conhecimento
- Acúmulo sem síntese

### Como Sistema Captura Isso
**Prisma Verbal:**
- Processa texto e extrai proposições específicas
- Avalia solidez de cada proposição
- Rastreia genealogia (qual proposição apoia qual)

**Revelar:**
- Co-constrói proposições com usuário
- Refina até proposição ter contexto claro
- Conecta com conceitos da biblioteca global

### Objetivo
- **Registrar apenas contribuições novas** (não redundância)
- **Extrair essência** dos textos (não resumir palavras)
- **Conectar conhecimento** (não isolar papers)

### Nota Importante
Este é princípio **orientador**, não bloqueio técnico. Sistema facilita criação de informação nova, mas não impede registro se usuário decidir.

## Motor Vetorial (Visão Central)

### Essências Como Unidade de Treino

A arquitetura atual de LLMs opera sobre **tokens** - fragmentos linguísticos que carregam peso estatístico mas não necessariamente significado. O motor vetorial propõe uma mudança paradigmática: um modelo treinado em **essências**, não em palavras.

**Limitação dos modelos atuais:**
- Tokenização fragmenta conceitos em pedaços arbitrários
- Peso estatístico ≠ relevância semântica
- Mesma ideia em línguas diferentes = representações completamente distintas
- Vocabulário especializado vs coloquial = compreensão inconsistente

**Proposta: Key-Value Semântico**

Em vez de embeddings baseados em co-ocorrência de tokens, sistema armazena pares estruturados:

```
{
  "essência": <abstração semântica pura>,
  "manifestações": [
    {resposta_literal_1, contexto_cultural_1},
    {resposta_literal_2, contexto_cultural_2},
    ...
  ]
}
```

### Inferências Via Operações Vetoriais

O motor vetorial realiza inferências através de **operações vetoriais**, não via chamadas a LLM:
- **Similaridade:** comparação de vetores (cosine similarity, distância euclidiana)
- **Composição:** combinação de vetores para formar conceitos complexos
- **Decomposição:** extração de componentes essenciais de vetores compostos
- **Projeção:** mapeamento entre espaços vetoriais de diferentes níveis de abstração

**Exemplo:**
```
Conceito "Justiça" (vetor) + Conceito "Distributiva" (vetor) 
  → Operação de composição vetorial
  → Resultado: "Justiça Distributiva" (novo vetor)
  → Busca por similaridade na biblioteca
  → Encontra: "Retribuição Proporcional" (similaridade 0.92)
```

### Metodologia de Treino

**Fase 1: Comparação Manual (presente)**
- Humanos identificam: "Esta frase de Marco Aurélio e esta de Confúcio apontam para a mesma essência"
- Sistema registra par: (texto_literal → proposição_fundamental)
- Curadoria intensiva, alto custo, alta qualidade

**Fase 2: Semi-Automatizado (médio prazo)**
- Modelo assiste humano na detecção de candidatos
- Humano valida/corrige pares sugeridos
- Loop de feedback refina heurísticas

**Fase 3: Automatizado (longo prazo)**
- Modelo generaliza padrões de abstração
- Detecta essências em textos novos sem supervisão
- Humano audita amostragens, não 100%

### O Diferencial: Abstração de Contexto

Modelo aprende a **transcender**:
- **Vocabulário:** "justiça", "dharma", "harmonia" → mesma essência
- **Cultura:** romano, védico, chinês → convergência detectada
- **Época:** 500 AC, 180 DC, 2024 DC → padrões atemporais
- **Idade/estilo:** acadêmico, coloquial, poético → essência preservada

**Exemplo concreto:**
```
Input: "Cada um leva o que merece" (coloquial, 2024)
       "A cada um segundo suas obras" (bíblico)
       "Karma é lei" (védico)
       "Justiça distributiva" (aristotélico)

Output: Essência → [RETRIBUIÇÃO_PROPORCIONAL]
        Solidez: alta (convergência transcultural)
```

### Conexão com Filosofia do Sistema

Esta visão é extensão natural do princípio "Essências transcendem palavras" (ver seção Convergência). Enquanto o sistema atual usa embeddings para detectar similaridade semântica (threshold 0.80+), o modelo próprio internalizaria essa capacidade de abstração como seu modo fundamental de operação.

**Implicação prática:**
- Usuário articula ideia em português coloquial
- Sistema reconhece essência, não palavras
- Conecta com Aristóteles (grego), Lao Tzu (chinês), paper recente (inglês acadêmico)
- Tudo sem tradução literal - via essência compartilhada

### Status e Horizonte

**Status:** Visão estruturante do sistema, agnóstica a prazo.

**Dependências:**
- Corpus curado de pares (literal → essência)
- Arquitetura de modelo adequada (não transformer padrão?)
- Métricas de avaliação para "abstração correta"

**Horizonte:** Estado futuro ideal do sistema. Documentado aqui para orientar decisões arquiteturais que não fechem portas para essa evolução.

## Espectro Matéria ↔ Espírito

O sistema unifica as "camadas" de interpretação com camadas de abstração vetorial através de um espectro contínuo que vai do material (forma) ao essencial (espírito):

```
MATERIAL (forma)                                    ESSENCIAL (espírito)
     │                                                      │
palavras → contexto → proposições → argumentos → ideias → conceitos
     │                                                      │
  específico                                           universal
  temporal                                             atemporal
  idioma-dependente                                    idioma-agnóstico
```

### Lado Material (Esquerda do Espectro)

- **Palavras:** unidades linguísticas específicas, dependentes de idioma
- **Contexto:** significado situacional, temporal, cultural
- **Proposições:** unidades de texto que podem virar argumentos conforme contexto e intenção
- **Características:** específico, temporal, idioma-dependente

### Lado Essencial/Espiritual (Direita do Espectro)

- **Argumentos:** estruturas lógicas reutilizáveis que emergem de conceitos
- **Ideias:** específicas, contextuais, pessoais (conjuntos de argumentos)
- **Conceitos:** padrões universais, atemporais, idioma-agnósticos
- **Características:** universal, atemporal, idioma-agnóstico

### Princípio Fundamental

Quanto mais à direita no espectro, mais agnóstico à forma linguística. O motor vetorial opera preferencialmente nas camadas mais à direita (conceitos, argumentos, ideias), abstraindo das palavras específicas para capturar essências compartilhadas.

**Exemplo:**
```
Material: "A justiça distributiva requer que cada um receba segundo suas contribuições"
  ↓ (abstração vetorial)
Essencial: Conceito "Justiça" + Conceito "Distributiva" + Argumento "Retribuição Proporcional"
  ↓ (recomposição)
Material: "Karma é lei" (védico) ou "A cada um segundo suas obras" (bíblico)
```

Este espectro unifica as "camadas" de interpretação com camadas de abstração vetorial, permitindo que o sistema trabalhe com essências independentemente da forma linguística específica.

## Biblioteca Vetorial

Todos os elementos do sistema (conceitos, argumentos, ideias, proposições) vivem no mesmo **espaço vetorial compartilhado**, formando uma biblioteca que cresce organicamente.

### Conceitos

**Definição:** Padrões universais, atemporais, idioma-agnósticos.

**Exemplos:** amor, família, segurança, justiça, cooperação, coordenação, harmonia, retribuição.

**Características:**
- Transcendem vocabulário específico
- Detectados por similaridade vetorial (threshold > 0.80)
- Podem ter múltiplas "variations" (diferentes palavras apontando para mesma essência)
- Formam a base sobre a qual argumentos emergem

### Argumentos

**Definição:** Estruturas lógicas reutilizáveis que emergem de conceitos.

**Características:**
- Compostos de conceitos relacionados
- Reutilizáveis entre diferentes ideias
- Podem ser combinados para formar ideias complexas
- Exemplo: "Justiça distributiva" = Conceito "Justiça" + Conceito "Distributiva"

### Ideias

**Definição:** Específicas, contextuais, pessoais. São conjuntos de argumentos.

**Características:**
- Combinam múltiplos argumentos
- Contextuais (dependem de situação específica)
- Pessoais (refletem visão de mundo do usuário)
- Podem evoluir ao longo do tempo (via diálogo no Revelar)

### Proposições

**Definição:** Unidades de texto que podem virar argumentos conforme contexto e intenção.

**Características:**
- Extraídas de textos estáticos (via Prisma Verbal)
- Ou co-construídas em diálogo (via Revelar)
- Ganham estrutura de argumento quando conectadas a conceitos
- Podem ser fundamentos de outros argumentos (genealogia)

### Padrões Emergentes

A biblioteca vetorial revela padrões interessantes:
- **Muitos argumentos/conceitos se repetem entre usuários:** "Coordenação", "Cooperação", "Justiça" aparecem frequentemente
- **Deduplicação automática:** Sistema detecta similaridade e sugere conexão com conceitos existentes
- **Crescimento orgânico:** Biblioteca cresce conforme produtos processam textos e conversas
- **Reutilização:** Argumentos de um usuário podem enriquecer a biblioteca para outros

**Exemplo de padrão emergente:**
```
Conceito "Coordenação" (biblioteca global)
  ├─ Argumento: "Coordenação requer comunicação frequente"
  │   └─ Usado em: Ideia "Reuniões síncronas aumentam alinhamento" (usuário A)
  │   └─ Usado em: Ideia "Stand-ups diários melhoram coordenação" (usuário B)
  ├─ Argumento: "Coordenação depende de objetivos compartilhados"
  │   └─ Usado em: Ideia "Visão compartilhada reduz conflitos" (usuário C)
  └─ Variations: coordenação, alinhamento, sincronização, harmonização
```

## Convergência Entre Produtos

### Pipeline Completo

Produtos do super-sistema formam um pipeline onde cada etapa transforma entrada em saída, todas compartilhando o mesmo motor vetorial:

**Interfaces de Entrada (para o Motor Vetorial):**
- **Revelar:** Diálogo → Ideia (clareza)
  - Co-constrói ideias com usuário via diálogo socrático
  - Proposições emergem da conversa
  - Solidez evolui conforme usuário elabora
  - Sistema provoca reflexão sobre lacunas
  
- **Prisma Verbal:** Texto estático → Argumentos (extração)
  - Processa textos estáticos (livros, papers)
  - Leitura sequencial (como humano)
  - Extrai proposições (#1, #2, #3...)
  - Avalia solidez baseada em coerência interna
  - Detecta dependências (proposição X apoia-se em Y)

**Estruturação e Forma:**
- **Camadas da Linguagem:** Ideia → Mensagem (estruturação)
  - Recebe Ideia como entrada
  - Estrutura em Mensagem (organização lógica, hierarquia de argumentos)
  - Aplica princípios de comunicação efetiva

- **Expressão:** Mensagem → Conteúdo (forma)
  - Recebe Mensagem como entrada
  - Produz Conteúdo em formas diversas (post, email, artigo, etc.)
  - Adapta tom, estilo e formato conforme necessidade

- **Produtor Científico:** Fork de Expressão especializado em artigos acadêmicos
  - Recebe Mensagem como entrada
  - Produz artigos acadêmicos com estrutura formal
  - Aplica normas de citação e formatação científica

### Arquitetura Compartilhada

Todos os produtos compartilham a mesma infraestrutura técnica:

**Infraestrutura Compartilhada:**
- ✅ **Motor Vetorial:** Operações vetoriais (similaridade, composição, decomposição)
- ✅ **Conceitos globais:** Biblioteca única (ChromaDB)
- ✅ **Detecção de solidez:** Coerência, fundamentação, lacunas
- ✅ **Rastreamento de proposições:** Genealogia de afirmações
- ✅ **Ontologia:** Conceito, Ideia, Argumento, Proposição, Evidência

**Diferença está na interface, não no motor:**
- Backend comum: Motor Vetorial, Biblioteca Vetorial, Ontologia
- Frontend específico: cada produto adapta interface conforme necessidade do usuário

### Como Produtos Trabalham Juntos

**Exemplo de fluxo integrado:**
```
1. Usuário articula ideia no Revelar:
   "Reuniões síncronas aumentam alinhamento"
   ↓
2. Revelar detecta conceito: "Coordenação" (biblioteca global)
   ↓
3. Sistema sugere:
   "Isso parece relacionado ao conceito 'Coordenação' na biblioteca,
    usado em:
    - March & Simon (Teoria Organizacional)
    - Scrum/XP (Desenvolvimento Ágil)
    - Rosenberg (Comunicação Não-Violenta)
    Quer explorar como esses autores abordam coordenação?"
   ↓
4. Usuário confirma interesse
   ↓
5. Pesquisador (Revelar) aciona Prisma para processar textos relevantes
   ↓
6. Prisma extrai proposições de March & Simon (1958):
   - Proposição #12: "Coordenação requer comunicação frequente"
   - Solidez: 0.85 (bem fundamentada no texto)
   ↓
7. Revelar apresenta ao usuário:
   "March & Simon (1958) afirmam que coordenação requer comunicação frequente.
    Isso apoia sua ideia sobre reuniões síncronas. Quer incorporar?"
```

### Essências Transcendem Palavras

**Princípio:** Cada cultura/época usa palavras diferentes para apontar essências similares.

**Exemplo:**
- Marco Aurélio (romano, ~180 DC): "justiça" = ordem cósmica distributiva
- Krishna (védico, ~500 AC): "dharma" = ordem universal, dever cósmico
- Confúcio (chinês, ~500 AC): "harmonia" = equilíbrio natural

**Mesma essência, palavras diferentes.**

Sistema abstrai das palavras para capturar o que está sendo APONTADO.

**Como sistema detecta similaridade:**
- Embeddings semânticos (ChromaDB)
- Threshold de similaridade (> 0.80)
- Biblioteca global cresce com:
  - Prisma processa textos estáticos → adiciona conceitos
  - Revelar capta conceitos de conversas → adiciona à biblioteca
  - Deduplicação automática (conceitos similares = variations)

**Benefício:**
Usuário não está "inventando a roda" - há conhecimento acumulado sob nomenclaturas diferentes.
Sistema conecta o que usuário está articulando com o que já foi dito antes (por outros autores, em outras palavras).

### Biblioteca Global em Evolução

**Como biblioteca cresce:**

**Via Prisma Verbal:**
```
1. Prisma processa "Sapiens" (Harari)
   → Extrai conceito "Cooperação via mitos" (solidez 0.85)
   → Salva na biblioteca global
   
2. Prisma processa "Sociedade sem Estado" (Clastres)
   → Extrai conceito "Cooperação tribal" (solidez 0.80)
   → Detecta similaridade com conceito existente (0.87)
   → Adiciona como variation de "Cooperação"
```

**Via Revelar:**
```
3. Usuário articula "trabalho em equipe"
   → Revelar detecta similaridade com "Cooperação" (0.91)
   → Sugere: "Isso se relaciona com conceito 'Cooperação' da biblioteca"
   → Adiciona "trabalho em equipe" como variation
```

**Resultado:**
```
Conceito: "Cooperação" (biblioteca global)
  Variations:
    - cooperação (Harari, Sapiens)
    - colaboração (usuário, Revelar)
    - teamwork (inglês)
    - trabalho em equipe (usuário, Revelar)
  Usado em:
    - Ideia: "Cooperação via mitos" (Sapiens)
    - Ideia: "Cooperação tribal" (Clastres)
    - Ideia: "Trabalho em equipe aumenta produtividade" (usuário)
```

**Deduplicação automática garante catálogo limpo:**
- Threshold > 0.90: adiciona automaticamente como variation
- Threshold 0.80-0.90: pergunta ao usuário
- Threshold < 0.80: conceito novo

## Visão Futura: Separação Comunicador/Orquestrador

**Status:** Conceitual, para implementação futura.

**Separação planejada (não implementada ainda):**

- **Orquestrador:** coordenação lógica, decisões, sem linguagem natural. Trabalha com estruturas de dados, estados, fluxos. Neutro e técnico.
- **Comunicador:** interface linguística, tradução para/de usuário, aplicação de personas. Responsável por toda interação em linguagem natural.

**Benefícios:**
- **Neutralidade:** Orquestrador não carrega vieses de comunicação, foca em lógica pura
- **Customização:** Diferentes comunicadores podem aplicar diferentes estilos (Sócrates, Popper, etc.) sem mudar lógica de orquestração
- **Rastreabilidade:** Decisões lógicas separadas de apresentação linguística, facilitando debug e validação

**Relação com Épico 18:**
Personas customizáveis serão implementadas no Comunicador, permitindo que usuários escolham estilos de argumentação sem afetar a coordenação interna do sistema.

**Implementação futura:**
Separação completa permitirá múltiplos canais de comunicação (web, CLI, API) todos consumindo o mesmo Orquestrador neutro.

**Resultado esperado:**
"Flecha penetrante" / "Ideia irresistível" - argumento sólido com respaldo bibliográfico, sem premissas frágeis, sem dúvidas não examinadas. Às vezes o usuário nem sabe onde quer chegar, mas ao elaborar, a clareza aparece.

**Ver detalhes sobre evolução cognitiva em:** `core/docs/vision/cognitive_model/`

## Princípios de Design

- **Inteligente, não determinístico**: adapta fluxos e respostas conforme contexto em vez de seguir roteiros fixos.
- **Colaborativo**: agentes constroem junto ao pesquisador, estimulando coautoria e reflexão crítica.
- **Transparente**: reasoning dos agentes exposto, integrando explicações curtas ou links para aprofundamento.
- **Incremental**: começa com entregáveis mínimos e expande funcionalidades à medida que aprende com o uso.
- **Escalável**: arquitetura previsa integração de novos tipos de artigo, agentes e extensões (ver `ARCHITECTURE.md` para detalhes técnicos).
- **Epistemologicamente honesto**: não existe verdade absoluta; sistema mapeia graus de sustentação baseados em evidências, não julgamentos binários de verdade/falsidade.

## Referências

- `core/docs/vision/epistemology.md` - Base filosófica detalhada
- `../architecture/vision/super_system.md` - Arquitetura do super-sistema
- `core/docs/vision/cognitive_model/` - Como pensamento evolui

