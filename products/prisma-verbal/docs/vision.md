# Fichamento - Produto

> **Nota:** Este documento descreve o produto fichamento especificamente.
> Para core universal, consulte `core/docs/architecture/vision/super_system.md`.
> Para como sistema processa texto (exemplo Sapiens), consulte `core/docs/examples/text_processing.md`.

## Visão Geral

Fichamento é **serviço desacoplado** que consome core para processar livros/textos e extrair ideias.

**O que faz:**
- Processa PDFs e extrai ideias automaticamente
- Mantém catálogo público de fichamentos (base)
- Permite customização por usuário
- Sistema aprende com customizações

**Diferença de paper-agent:**
- Paper-agent: conversa dinâmica, ideias emergem
- Fichamento: texto estático, ideias extraídas de uma vez

## Entidades Específicas do Fichamento

### Book
```python
Book:
  id: UUID
  title: str                    # "Sapiens"
  author: str                   # "Yuval Noah Harari"
  isbn: str
  language: str
  
  # Ideias extraídas (referencia core)
  ideas: list[UUID]
  
  # Estrutura original
  chapters: list[Chapter]
```

### Chapter
```python
Chapter:
  id: UUID
  book_id: UUID
  number: int
  title: str
  ideas: list[UUID]             # Ideias neste capítulo
```

### BaseFichamento (Catálogo Público)
```python
BaseFichamento:
  id: UUID
  book_id: UUID
  ideas: list[UUID]             # Ideias identificadas pelo sistema
  extraction_date: datetime
  confidence: float             # 0-1 (quão confiante sistema está)
  is_public: bool               # True (compartilhado)
```

### UserFichamento (Customização)
```python
UserFichamento:
  id: UUID
  user_id: UUID
  base_fichamento_id: UUID      # Referencia fichamento base
  
  # Customizações do usuário
  added_ideas: list[UUID]       # Ideias adicionadas
  removed_ideas: list[UUID]     # Ideias removidas
  annotations: list[dict]       # Notas pessoais
```

## Fluxo: Fichar Livro

### Opção A: Automático (Sistema Processa)
```
Usuário: [upload PDF "Sapiens"]

Sistema: "Processando livro... (pode levar 1-2min)"
         [lê todas as páginas]
         [divide em chunks]
         [agentes processam cada chunk]

Sistema: "Identifiquei 15 ideias principais:
          
          1. Cooperação humana via mitos compartilhados
          2. Revolução agrícola como armadilha
          3. Unificação da humanidade
          [...]
          
          Para cada ideia, extraí:
          - Claim principal
          - Argumentos que sustentam
          - Conceitos-chave
          
          Quer revisar alguma em particular?"
```

### Opção B: Conversacional (Usuário Guia)
```
Usuário: "Quero fichar o livro Sapiens"

Sistema: "Legal! Vamos fazer juntos. Me conta:
          qual a tese principal do autor?"

Usuário: "Que cooperação depende de mitos"

Sistema: "Interessante! E quais argumentos ele usa 
         para defender isso?"

[conversa guiada até estruturar todas ideias]
```

### Opção C: Híbrido (Padrão)
```
Sistema processa automaticamente (extração inicial)
Usuário revisa e refina via conversa
Sistema atualiza fichamento com refinamentos
```

## Catálogo Público vs Customização

### Catálogo Público (Base)

**Fichamento base:**
- Sistema extrai ideias
- Fica disponível para todos usuários
- Não precisa reprocessar livro para novo usuário

**Exemplo:**
```
Book: "Sapiens"
BaseFichamento:
  ideas: [
    "Cooperação via mitos",
    "Agricultura como armadilha",
    "Unificação da humanidade",
    ...
  ]
  used_by: [user_1, user_2, user_3]
```

### Customização Usuário

**Cada usuário pode:**
- Adicionar ideias (sistema não detectou)
- Remover ideias (não considera relevante)
- Anotar passagens
- Enfatizar aspectos

**Exemplo:**
```
UserFichamento (João):
  base: "Sapiens"
  added_ideas: ["Trabalho abstrato vs concreto"]  # enfatizou aspecto econômico
  annotations: ["Cap 2, pg 45: conexão com Marx"]

UserFichamento (Maria):
  base: "Sapiens"
  added_ideas: ["Religião como mito unificador"]  # enfatizou aspecto religioso
  removed_ideas: ["Unificação da humanidade"]     # não considerou relevante
```

## Sistema Aprende com Customizações

### Agregação de Customizações
```python
# Se múltiplos usuários adicionam mesma ideia
common_additions = aggregate_customizations()

# Exemplo
if 5+ usuários adicionaram "Trabalho abstrato":
    # Confidence > 80%
    # Sistema atualiza fichamento base
    base_fichamento.ideas.append("Trabalho abstrato")
    base_fichamento.confidence += 0.1
```

### Feedback Loop
```
Usuários customizam
    ↓
Sistema detecta padrões
    ↓
Fichamento base atualizado
    ↓
Novos usuários se beneficiam
```

## Navegação e Busca

### Buscar Livros por Conceito
```
Usuário: "Livros sobre cooperação"

Sistema: [busca via core - conceitos]
         "Encontrei 8 livros:
          
          1. Sapiens (Harari) - 'Cooperação via mitos'
          2. Sociedade sem Estado (Clastres) - 'Cooperação tribal'
          3. Capital Social (Putnam) - 'Cooperação cívica'
          ..."
```

### Buscar Ideias Relacionadas
```
Usuário: [lendo fichamento de Sapiens]
         "Ideias relacionadas a 'Cooperação via mitos'?"

Sistema: [busca via core - grafo de conhecimento]
         "Ideias similares em outros livros:
          
          - 'Religião como instituição social' (Durkheim)
          - 'Imaginário coletivo' (Benedict Anderson)
          - 'Contrato social' (Rousseau)"
```

## Interface: Upload → Revisão → Navegação

### Upload
```
[Drag & drop PDF]
[Sistema processa]
[Progresso: 45%... 78%... 100%]
```

### Revisão
```
[Lista de ideias extraídas]
[Usuário pode:]
  - Ver reasoning (como sistema chegou naquela ideia)
  - Adicionar ideia (formulário)
  - Remover ideia (confirmar)
  - Anotar (editor de texto)
```

### Navegação
```
[Biblioteca de livros]
[Busca por:]
  - Título/autor
  - Conceito
  - Ideia similar
  
[Filtros:]
  - Fichamento completo
  - Apenas customizados por mim
  - Catálogo público
```

## Integração com Core

### Fichamento NÃO reimplementa:

❌ Extração de ideias (core faz)  
❌ Detecção de conceitos (core faz)  
❌ Estruturação de argumentos (core faz)  
❌ Busca semântica (core faz)  

### Fichamento ADICIONA:

✅ Entidade `Book` e `Chapter`  
✅ Catálogo público de fichamentos  
✅ Customização por usuário  
✅ Sistema de aprendizado (agregação)  
✅ Interface de upload e revisão  

## Referências

- `core/docs/architecture/vision/super_system.md` - Core → Produtos
- `core/docs/architecture/data-models/idea_model.md` - Ideias extraídas de livros
- `core/docs/architecture/data-models/concept_model.md` - Conceitos detectados em livros
- `core/docs/examples/text_processing.md` - Exemplo concreto de processamento

## 7. Filosofia do Sistema

### Palavras São Escolhas Contextuais

**Princípio central:** Cada cultura/época usa palavras diferentes para apontar essências similares.

**Exemplos:**

- Marco Aurélio (romano, ~180 DC): "justiça" = ordem cósmica distributiva

- Krishna (védico, ~500 AC): "dharma" = ordem universal, dever cósmico

- Confúcio (chinês, ~500 AC): "harmonia" = equilíbrio natural

**Mesma essência, palavras diferentes.** Sistema abstrai das palavras para capturar o que está sendo APONTADO.

### Essências Transcendem Palavras

**O que sistema busca:**

- Não: definição de dicionário

- Não: tradução literal

- Sim: **Afirmação sobre como realidade funciona**

**Exemplo:**

```
"Justiça" (Marco) ≠ tradução de "dharma" (Krishna)

Mas ambos apontam estrutura similar:

  "Há ordem anterior ao caos, 

   seguir essa ordem = virtude/dever"
```

### Entidade Central: Ideia Específica

**Sistema NÃO cataloga conceitos genéricos:**

- ❌ "Cooperação" (muito amplo)

- ❌ "Mitos" (muito amplo)

**Sistema cataloga IDEIAS específicas:**

- ✅ "Cooperação humana em massa depende de mitos compartilhados"

- ✅ "Determinismo cósmico via razão universal" (Marco)

- ✅ "Unidade subjacente à multiplicidade aparente" (Krishna/Jesus/Plotino)

**Ideia = combinação específica de conceitos com afirmação sobre realidade.**

### Genealogia de Crenças (Visão de Longo Prazo)

**Objetivo futuro:** Rastrear origem de comportamentos através de crenças.

**Exemplo:**

```
Comportamento: Humano come carne

  ↓

Crença 1: Animais são inferiores a humanos

  ↓

Possível origem: "Deus criou animais para servir humanos" (Bíblia)

  ↓

Pessoa pode nunca ter lido Bíblia, mas cultura incorporou crença
```

**Sistema mapeia:** Genealogia de como crenças culturais se propagam.

**Nota:** Este produto (Prisma Verbal) foca na CAPTURA. Outro produto futuro fará CONEXÕES genealógicas.

## 8. Diferenciação: Prisma Verbal vs Paper-Agent

### Texto Estático vs Conversa Dinâmica

**Prisma Verbal:**

- Input: Livro completo, artigo, transcrição

- Processamento: Leitura sequencial automática

- Output: Ideias extraídas + genealogia de afirmações

- Interação: Usuário consulta resultado (não co-constrói)

**Paper-Agent:**

- Input: Conversa com usuário

- Processamento: Co-construção iterativa

- Output: Argumento científico refinado

- Interação: Sistema + usuário negociam caminho

### Vetorização vs Solidez por Evidências

**Prisma Verbal:**

- Solidez = convergência entre autores

- "Harari #1 converge com Newton" → aumenta solidez

- "Harari #1 diverge de Bíblia" → tensão registrada

- Vetorização semântica para aproximar conceitos

**Paper-Agent:**

- Solidez = evidências bibliográficas científicas

- Proposição com 3 estudos → solidez 0.75

- Proposição sem evidências → solidez 0.30

- Pesquisador busca literatura para fortalecer

### Checkpoints vs Snapshots

**Prisma Verbal:**

- Checkpoints automáticos durante leitura

- Sistema detecta: "Ideia suficientemente madura"

- Livro pode ter dezenas de checkpoints

- Não espera fim do texto

**Paper-Agent:**

- Snapshots durante conversa

- Sistema detecta: "Argumento amadureceu"

- Silencioso (usuário não vê)

- Versionamento (V1, V2, V3...)

### Interface

**Prisma Verbal (não conversacional):**

- Upload de texto → Sistema processa → Mostra resultado

- Navegação por conceitos/ideias extraídas

- Hover profundo em conceitos (herança de Camadas)

- Comparação entre autores

**Paper-Agent (conversacional):**

- Chat interativo

- Sistema + usuário refinam argumento juntos

- Bastidores transparentes (reasoning visível)

