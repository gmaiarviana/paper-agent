# Visão do Produto - Prisma Verbal

> **Nota:** Nome do produto pode ser revisto para "Camadas da Linguagem".

## 1. O Que É

Sistema que processa textos (livros, artigos, transcrições) e extrai essências abstraindo das palavras.

### Diferencial

- ❌ **Não resume texto** (palavras)
- ❌ **Não extrai keywords** (tokens)
- ✅ **Captura AFIRMAÇÕES sobre realidade**
- ✅ **Constrói genealogia de crenças**
- ✅ **Detecta convergências entre culturas/épocas**

## 2. Para Quem

- Pesquisadores comparando autores
- Filósofos mapeando convergências
- Qualquer pessoa querendo entender essência de textos

## 3. Objetivos

### Primário: Extrair Essência de Textos

- Sistema lê sequencialmente (como humano)
- Captura afirmações sobre realidade (#1, #2, #3...)
- Rastreia dependências entre conceitos

### Secundário: Biblioteca de Essências

- Conceitos globais (vetorizados)
- Permite aproximação semântica
- Exemplo: "justiça" (Marco) ≈ "dharma" (Krishna)

### Terciário: Treinar Modelo em Essências (não tokens)

- Key-value baseado em essências
- Comparação manual → treino automatizado

## 4. Exemplo Concreto (Sapiens)

Após processar livro:

### Conceitos Detectados

Big Bang, Física, Átomos, Moléculas, Química, Organismos, Biologia, Culturas, História

### Afirmações Extraídas

- #1: Big Bang originou universo
- #2: Física estuda características fundamentais
- [... até #9+]

### Genealogia

- #2 apoia-se em #1
- #3 apoia-se em #1
- #5 apoia-se em #3, #4

### Convergências Detectadas

- Harari (#2) ↔ Newton (física)
- Harari (#5) ↔ Lavoisier (química)

### Divergências Detectadas

- Harari (#1) ✗ Bíblia (criação)

## 5. Tipos de Texto (Próximas Sessões)

Placeholder para explorar:

- Textos filosóficos/espirituais (já começamos)
- Textos científicos (a explorar)
- Textos ficção (a explorar)
- Textos artísticos (a explorar)

## 6. Conexão com Core

Reutiliza infraestrutura:

- ChromaDB (vetores)
- SQLite (metadados)
- Conceito (biblioteca global)
- Proposição (afirmação com solidez)

### Diferença

- **Prisma**: texto estático
- **Paper-Agent**: conversa dinâmica

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

