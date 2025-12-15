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
- **Paper-agent:** Auxílio em produção científica (atual)
- **Fichamento:** Catálogo de livros com ideias extraídas (futuro próximo)
- **Rede Social:** Conexão por cosmovisões compartilhadas (futuro distante)

**Core compartilhado:**
- Ontologia (Conceito, Ideia, Argumento)
- Modelo cognitivo (claim → fundamentos (com solidez variável))
- Agentes (Orquestrador, Estruturador, Metodologista, Pesquisador)
- Infraestrutura (LangGraph, ChromaDB, embeddings)

Produtos são **serviços desacoplados** que consomem core via APIs.

## Convergência Entre Produtos

### Arquitetura Compartilhada

Produtos do super-sistema (Revelar, Prisma Verbal) compartilham infraestrutura técnica, mas têm contextos diferentes:

**Infraestrutura Compartilhada:**
- ✅ **Conceitos globais:** Biblioteca única (ChromaDB)
- ✅ **Detecção de solidez:** Coerência, fundamentação, lacunas
- ✅ **Rastreamento de proposições:** Genealogia de afirmações
- ✅ **Ontologia:** Conceito, Ideia, Argumento, Proposição, Evidência

**Contextos Diferentes:**
- **Prisma Verbal:** Extrai proposições de textos estáticos (livros, papers)
  - Leitura sequencial (como humano)
  - Extrai proposições (#1, #2, #3...)
  - Avalia solidez baseada em coerência interna
  - Detecta dependências (proposição X apoia-se em Y)
  
- **Revelar:** Co-constrói proposições com usuário (conversa dinâmica)
  - Diálogo socrático
  - Proposições emergem da conversa
  - Solidez evolui conforme usuário elabora
  - Sistema provoca reflexão sobre lacunas

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

