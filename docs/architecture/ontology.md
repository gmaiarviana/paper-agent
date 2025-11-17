# Ontologia do Sistema

## Visão Geral

Este documento é o **Single Source of Truth (SSoT)** que define a ontologia do super-sistema. Ele estabelece o que são Conceito, Ideia e Argumento do ponto de vista filosófico, e como essas entidades se relacionam entre si.

Outros documentos de arquitetura referenciam este documento como base para entender as entidades fundamentais do sistema.

## As Três Entidades Fundamentais

### Conceito (Abstrato, Reutilizável)

**O que é:** Núcleo semântico abstrato que pode assumir diferentes formas linguísticas.

**Características:**
- Transcende palavras específicas
- Reutilizável entre diferentes ideias
- Tem variações linguísticas (produtividade, eficiência, performance = mesma essência)

**Exemplos:**
- Conceito: "Cooperação" 
  - Essência: Ação coordenada de múltiplos agentes
  - Variações: cooperação, colaboração, teamwork, coopération (francês)

### Ideia (Território, Contextual)

**O que é:** Pensamento articulado que reúne conceitos e argumentos em contexto específico.

**Características:**
- Usa múltiplos conceitos
- Pode ter múltiplos argumentos (diferentes lentes)
- Evolui ao longo de conversa
- Contextual (não necessariamente universal)

**Exemplos:**
- Ideia: "Cooperação humana via mitos compartilhados"
  - Conceitos usados: [Cooperação, Ficção, Linguagem]
  - Argumentos: [Religião permite cooperação, Nacionalismo permite cooperação]

### Argumento (Lente, Estrutura Lógica)

**O que é:** Uma forma de ver/defender uma ideia através de estrutura lógica (claim + premises).

**Características:**
- Estrutura: claim → premises → assumptions → evidências
- Múltiplos argumentos podem defender mesma ideia (diferentes ângulos)
- Argumento = mapa, Ideia = território

**Exemplos:**
- Ideia: "Semana de 4 dias"
  - Argumento 1 (lente produtividade): "Aumenta produtividade via descanso"
  - Argumento 2 (lente retenção): "Reduz turnover em 20%"

## Relações Entre Entidades

### Ideia ↔ Conceito (N:N)
- Ideia usa múltiplos conceitos
- Mesmo conceito aparece em múltiplas ideias
- Sistema detecta conceitos compartilhados via vetor semântico

### Ideia ↔ Argumento (1:N)
- Ideia pode ter múltiplos argumentos (diferentes lentes)
- Argumento pertence a uma ideia

### Argumento ↔ Conceito (N:N)
- Argumento usa conceitos nas premises

## Exemplo Completo: Sapiens (Harari)

**Texto original:**
"Cooperação humana em massa depende de mitos compartilhados. Dois católicos que nunca se encontraram podem embarcar juntos numa cruzada porque ambos acreditam que Deus encarnou num corpo humano."

**Sistema cristaliza:**

```python
Ideia: "Cooperação humana via mitos compartilhados"

Conceitos centrais:
- Ficção/Mito (vetor semântico)
- Cooperação (vetor semântico)
- Linguagem (vetor semântico)

Argumento principal:
claim: "Cooperação em massa depende de mitos compartilhados"
premises: ["Linguagem permite transmitir ficções"]
evidências: [
  "Religião: católicos cooperam via crença em Deus",
  "Nacionalismo: sérvios cooperam via crença em nação"
]
```

## Hierarquia (Ideias dentro de Ideias)

Livros/textos complexos podem ter estrutura hierárquica:

```
Ideia macro: "Revoluções que transformaram Sapiens"
├─ Sub-ideia 1: "Revolução Cognitiva"
│   └─ Ideia específica: "Cooperação via mitos"
├─ Sub-ideia 2: "Revolução Agrícola"
│   └─ Ideia específica: "Agricultura como armadilha"
```

Sistema identifica hierarquia automaticamente processando conteúdo.

## Referências

- `docs/architecture/concept_model.md` - Estrutura de dados técnica de Conceito
- `docs/architecture/idea_model.md` - Estrutura de dados técnica de Ideia
- `docs/architecture/argument_model.md` - Estrutura de dados técnica de Argumento
- `docs/vision/cognitive_model.md` - Como pensamento evolui (claim → premises)

