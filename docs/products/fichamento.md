# Fichamento - Produto

> **Nota:** Este documento descreve o produto fichamento especificamente.
> Para core universal, consulte `docs/architecture/super_system_vision.md`.
> Para como sistema processa texto (exemplo Sapiens), consulte `docs/examples/sapiens_processing.md`.

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

- `docs/architecture/super_system_vision.md` - Core → Produtos
- `docs/architecture/idea_model.md` - Ideias extraídas de livros
- `docs/architecture/concept_model.md` - Conceitos detectados em livros
- `docs/examples/sapiens_processing.md` - Exemplo concreto de processamento

