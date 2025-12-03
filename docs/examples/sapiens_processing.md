# Exemplo: Processamento de Sapiens (Harari)

> **Nota:** Este documento ilustra como sistema processa texto estático.
> Para ontologia (Conceito/Ideia/Argumento), consulte `docs/architecture/ontology.md`.

## Trecho Original

**Livro:** Sapiens (Yuval Noah Harari)  
**Capítulo:** 2 - A Árvore do Conhecimento  
**Seção:** Cooperação e Mitos  

**Texto (parafraseado):**

> "Há cerca de 70 mil anos, organismos da espécie Homo sapiens começaram a formar estruturas ainda mais elaboradas chamadas culturas. O surgimento da linguagem permitiu aos sapiens transmitir informações sobre coisas que não existem de fato. Você nunca vai convencer um macaco a lhe dar uma banana prometendo que após a morte ele terá bananas ilimitadas no paraíso dos macacos. Mas por que isso é tão importante? A resposta é que a cooperação humana em massa depende de mitos compartilhados. Dois católicos que nunca se encontraram podem embarcar juntos numa cruzada porque ambos acreditam que Deus encarnou num corpo humano e se deixou crucificar. Dois sérvios que nunca se viram podem arriscar a vida para salvar um ao outro porque ambos acreditam na existência da nação sérvia. Duas pessoas que não se conhecem podem cooperar para estabelecer uma empresa porque ambas acreditam na existência do dinheiro e das empresas."

---

## Passo 1: Sistema Lê Frase por Frase

### Frase 1
**Texto:** "Há cerca de 70 mil anos, organismos da espécie Homo sapiens começaram a formar estruturas ainda mais elaboradas chamadas culturas."

**Sistema detecta:**
- Conceito: "Cultura"
- Conceito: "Homo sapiens"
- Contexto temporal: 70 mil anos atrás

**Ideia emergindo?** Não ainda (muito amplo)

---

### Frase 2
**Texto:** "O surgimento da linguagem permitiu aos sapiens transmitir informações sobre coisas que não existem de fato."

**Sistema detecta:**
- Conceito: "Linguagem"
- Conceito novo: "Ficção" (coisas que não existem)
- Relação: Linguagem → Ficção

**Ideia emergindo?** Sim, começando a estruturar

**Argumento nascente:**
- Fundamento: "Linguagem permite transmitir ficções"

---

### Frase 3-4: Exemplo do Macaco
**Texto:** "Você nunca vai convencer um macaco a lhe dar uma banana prometendo que após a morte ele terá bananas ilimitadas no paraíso dos macacos."

**Sistema detecta:**
- Evidência: Contraste humanos vs animais
- Reforça conceito: Humanos acreditam em ficções, animais não

**Ideia emergindo?** Sim, ficando mais claro

**Argumento evoluindo:**
- Fundamento: "Humanos acreditam em ficções, animais não"
- Evidence: "Exemplo do macaco e bananas"

---

### Frase 5: CLAIM Central
**Texto:** "A cooperação humana em massa depende de mitos compartilhados."

**Sistema detecta:**
- **CLAIM CENTRAL IDENTIFICADO!**
- Conceito: "Cooperação"
- Conceito: "Mitos" (= ficções compartilhadas)

**Ideia cristaliza:**
- Título: "Cooperação humana via mitos compartilhados"
- Claim: "Cooperação em massa depende de mitos compartilhados"
- Frases anteriores eram fundamentos/evidências

---

### Frases 6-8: Evidências
**Texto:** "Dois católicos... cruzada... Dois sérvios... nação... Duas pessoas... empresa..."

**Sistema detecta:**
- 3 evidências paralelas (religião, nacionalismo, economia)
- Todas seguem padrão: ficção compartilhada → cooperação

**Ideia completa!**

---

## Passo 2: Sistema Cristaliza

### Ideia Identificada
```python
Idea:
  id: "idea-sapiens-001"
  title: "Cooperação humana via mitos compartilhados"
  
  concepts: [
    concept_linguagem,
    concept_ficcao,
    concept_cooperacao,
    concept_mitos
  ]
  
  arguments: [argument_001]  # Um argumento principal
  
  context: {
    source_type: "book",
    source: "Sapiens, Capítulo 2",
    author: "Yuval Noah Harari",
    page_range: "27-28"
  }
  
  status: "extracted"
```

### Argumento Principal
```python
Argument:
  id: "argument-001"
  idea_id: "idea-sapiens-001"
  
  claim: "Cooperação humana em massa depende de mitos compartilhados"
  
  fundamentos: [
    ProposicaoRef(
      id="prop-1",
      enunciado="Linguagem humana permite transmitir ficções",
      solidez=0.85
    ),
    ProposicaoRef(
      id="prop-2",
      enunciado="Humanos acreditam em ficções, animais não",
      solidez=0.80
    ),
    ProposicaoRef(
      id="prop-3",
      enunciado="Culturas são estruturas elaboradas (70 mil anos)",
      solidez=0.75
    ),
    # Nota: Na nova ontologia, não há campo "assumptions".
    # Proposições com baixa solidez (< 0.4) cumprem esse papel.
    # Exemplo: "Causalidade é direta" teria solidez ~0.30
    ProposicaoRef(
      id="prop-4",
      enunciado="Causalidade: mitos → cooperação (sem confundidores)",
      solidez=0.35  # baixa solidez
    )
  ]
  
  evidence: [
    {
      type: "contrast",
      description: "Macaco não acredita em paraíso (contraste com humanos)",
      strength: "illustration"
    },
    {
      type: "example",
      description: "Católicos cooperam via crença em Deus encarnado",
      domain: "religião"
    },
    {
      type: "example",
      description: "Sérvios cooperam via crença em nação",
      domain: "nacionalismo"
    },
    {
      type: "example",
      description: "Pessoas cooperam via crença em dinheiro/empresas",
      domain: "economia"
    }
  ]
  
  concepts: [
    concept_linguagem,
    concept_ficcao,
    concept_cooperacao
  ]
```

### Estrutura Atualizada (Nova Ontologia)

```python
# Estrutura atualizada com ProposicaoRef e solidez
fundamentos: [
  ProposicaoRef(
    id="prop-1",
    enunciado="Linguagem permite transmitir ficções",
    solidez=0.85
  ),
  ProposicaoRef(
    id="prop-2",
    enunciado="Causalidade: mitos → cooperação",
    solidez=0.35  # baixa solidez - cumpre papel de "assumption"
  )
]
```

**Nota:** Na nova ontologia:
- `premises` → `fundamentos` (lista de `ProposicaoRef`)
- `assumptions` → removido (proposições com baixa solidez `< 0.4` cumprem esse papel)
- Cada `ProposicaoRef` inclui `id`, `enunciado` e `solidez` (0.0 a 1.0)

### Conceitos Detectados
```python
Concept: "Ficção/Mito"
  label: "Ficção compartilhada"
  essence: "Realidade imaginada que grupos acreditam coletivamente"
  
  variations: [
    "ficção",
    "mito",
    "crença compartilhada",
    "realidade imaginada",
    "shared fiction" (inglês)
  ]
  
  semantic_vector: [0.23, 0.87, -0.45, ...]  # embedding
  
  contexts: [
    {context: "religião", nuance: "divindades, paraíso"},
    {context: "política", nuance: "nação, Estado"},
    {context: "economia", nuance: "dinheiro, corporações"}
  ]

---

Concept: "Cooperação"
  label: "Cooperação"
  essence: "Ação coordenada de múltiplos agentes"
  
  variations: [
    "cooperação",
    "colaboração",
    "trabalho em conjunto",
    "ação coletiva",
    "coordination" (inglês)
  ]
  
  semantic_vector: [0.45, 0.21, 0.67, ...]
  
  contexts: [
    {context: "biologia", nuance: "altruísmo evolutivo"},
    {context: "sociologia", nuance: "ação coletiva coordenada"},
    {context: "economia", nuance: "teoria dos jogos"}
  ]
```

---

## Passo 3: Relacionamentos

### Ideia ↔ Conceitos (N:N)
```python
# Ideia usa múltiplos conceitos
idea_sapiens_001.concepts = [
  concept_linguagem,
  concept_ficcao,
  concept_cooperacao
]

# Conceito "Cooperação" usado em múltiplas ideias
concept_cooperacao.used_in_ideas = [
  idea_sapiens_001,
  idea_outro_livro_023,
  idea_artigo_usuario_045
]
```

### Busca Semântica (Futuro)
```python
# Usuário busca "trabalho em equipe"
query_vector = encoder.encode("trabalho em equipe")

# Sistema encontra conceito similar
similar_concepts = chroma.query(query_vector)
# Retorna: concept_cooperacao (similarity: 0.89)

# Sistema sugere ideias relacionadas
related_ideas = get_ideas_with_concept(concept_cooperacao)
# Retorna: [idea_sapiens_001, idea_outro_livro_023, ...]
```

---

## Passo 4: Hierarquia (Livro Completo)

Se processarmos o livro inteiro, estrutura seria:
```python
Ideia macro: "Revoluções que transformaram Sapiens"
  ├─ Sub-ideia 1: "Revolução Cognitiva"
  │   ├─ Ideia específica: "Cooperação via mitos" ← este exemplo
  │   └─ Ideia específica: "Linguagem como diferencial"
  │
  ├─ Sub-ideia 2: "Revolução Agrícola"
  │   └─ Ideia específica: "Agricultura como armadilha"
  │
  └─ Sub-ideia 3: "Revolução Científica"
      └─ Ideia específica: "Ignorância como motor"
```

Sistema identifica hierarquia automaticamente processando capítulos.

---

## Comparação: Texto Estático vs Conversa Dinâmica

### Texto Estático (Fichamento)
```
Sistema lê todo o texto de uma vez
Extrai todas as ideias
Apresenta lista completa
Usuário revisa depois
```

**Exemplo deste documento:** Sapiens já escrito, ideias já estruturadas.

### Conversa Dinâmica (Paper-Agent)
```
Ideias emergem aos poucos
Sistema cristaliza conforme conversa evolui
Dashboard atualiza em tempo real
Usuário participa da construção
```

**Contraste:** Paper-agent não "lê livro", co-constrói ideia com usuário.

---

## Referências

- `docs/architecture/ontology.md` - Definições de Conceito/Ideia/Argumento
- `docs/architecture/idea_model.md` - Estrutura técnica de Ideia
- `docs/architecture/concept_model.md` - Vetores semânticos
- `docs/products/paper_agent.md` - Como fichamento usa esse processamento

