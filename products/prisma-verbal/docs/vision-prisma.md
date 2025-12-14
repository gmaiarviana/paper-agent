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

