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

## 5. Exemplo: O Poder do Agora (Mais Claro)

**Capítulo 1 - VOCÊ NÃO É A SUA MENTE**

**Resumo:**
Anedota do mendigo com tesouro dentro. Autor se posiciona como estranho apontando tesouro ao leitor.

**Conceitos que emergem:**
- Quem não encontrou alegria do Ser é mendigo espiritual
- Iluminação = estado natural de unidade com o Ser, fim do sofrimento
- Paradoxo: Ser é essencialmente o indivíduo
- Incapacidade de conexão → sensação de separação

**Diferencial deste exemplo:**
- Texto filosófico (não ficção narrativa como Sapiens)
- "Resumo" captura ilustrações/exemplos (não eventos)
- Conceitos são mais abstratos (metafísicos vs sociais)

## 6. Tipos de Texto (Próximas Sessões)

Placeholder para explorar:

- Textos filosóficos/espirituais (já começamos)
- Textos científicos (a explorar)
- Textos ficção (a explorar)
- Textos artísticos (a explorar)

## 7. Checkpoint Multinível

Sistema cria checkpoints em múltiplos níveis conforme estrutura do livro:
- **Parágrafo:** Se ideia completa emerge
- **Sub-seção:** Agrupamento temático
- **Capítulo:** Síntese completa

**Decisão é dinâmica**, baseada em:
- Completude da ideia
- Distância do início/fim de seção
- Mudança temática

Exemplo: Capítulo pode ter 1 checkpoint (se linear) ou 5 checkpoints (se denso).

## 8. Separação: Leitura vs Contextualização

**Princípio central:** Contexto externo NÃO contamina leitura base.

**FASE 1 - LEITURA (foco do sistema):**
- Extrair o que livro diz
- Sem contexto externo (biografia, época, paralelos históricos)
- Apenas: texto → conceitos/ideias

**FASE 2 - CONTEXTUALIZAÇÃO (futuro, camada separada):**
- Conectar com biografia do autor
- Relacionar com época/cultura
- Paralelos históricos (ex: Revolução dos Bichos ↔ Revolução Russa)
- Usuário ou sistema adiciona essa camada **depois**

**Exemplo:**

```python
# FASE 1 (Leitura - agora)
Conceito: "Oprimidos devem se revoltar contra opressor"
Livro: Revolução dos Bichos

# FASE 2 (Contextualização - depois)
Contexto externo: "Orwell escreveu alegoria da Revolução Russa"
Paralelo: Major = Marx/Lenin
Época: Pós-Segunda Guerra, crítica ao stalinismo
```

**Benefício:** Sistema não impõe viés externo na leitura inicial.

## 9. Conexão com Core

Reutiliza infraestrutura:

- ChromaDB (vetores)
- SQLite (metadados)
- Conceito (biblioteca global)
- Proposição (afirmação com solidez)

### Diferença

- **Prisma**: texto estático
- **Paper-Agent**: conversa dinâmica

## 10. Filosofia do Sistema

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

## 11. Diferenciação: Prisma Verbal vs Paper-Agent

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

