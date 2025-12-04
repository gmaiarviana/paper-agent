# Ontologia do Sistema

## Visão Geral

Este documento é o **Single Source of Truth (SSoT)** que define a ontologia do super-sistema. Ele estabelece o que são Conceito, Ideia, Argumento, Proposição e Evidência do ponto de vista filosófico, e como essas entidades se relacionam entre si.

A ontologia reflete uma filosofia epistemológica onde não existe distinção binária entre "fato" e "suposição", mas sim proposições com diferentes graus de solidez baseados em evidências. Para entender a base filosófica completa, consulte `docs/vision/epistemology.md`.

Outros documentos de arquitetura referenciam este documento como base para entender as entidades fundamentais do sistema.

## Entidades Fundamentais

### Conceito (Abstrato, Reutilizável, Atemporal)

**O que é:** Núcleo semântico abstrato que pode assumir diferentes formas linguísticas.

**Características:**
- Transcende palavras específicas
- Reutilizável entre diferentes ideias
- Tem variações linguísticas (produtividade, eficiência, performance = mesma essência)
- **Atemporal**: Conceitos existem independentemente de tempo, contexto ou usuário
- **Não possui solidez**: Conceitos são rótulos semânticos, não afirmações sobre o mundo
- **Origem flexível**: Podem vir de usuário, literatura, múltiplos usuários ou emergir do sistema

#### Biblioteca Global de Conceitos

**Natureza independente:**
- Conceitos existem independentemente de ideias
- Sistema mantém vocabulário compartilhado (dicionário universal)
- Múltiplas ideias referenciam o mesmo conceito da biblioteca global
- Conceito existe uma vez na biblioteca, usado por N ideias
- **Conceitos são atemporais**: Existem independente de quem os usa ou quando foram criados
- **Conceitos não têm "solidez"**: São rótulos semânticos, não afirmações que podem ser verdadeiras ou falsas

**Exemplos de globalidade:**

Conceito "Cooperação" (global, único na biblioteca):
- Essência: Ação coordenada de múltiplos agentes
- Variações linguísticas: cooperação, colaboração, teamwork, coopération (francês)
- Referenciado por Ideia 1: "Cooperação via mitos" (Sapiens)
- Referenciado por Ideia 2: "Cooperação tribal" (Clastres)
- Referenciado por Ideia 3: "Cooperação cívica" (Putnam)

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

### Proposição (Unidade Base de Conhecimento)

**O que é:** Afirmação sobre o mundo que pode ser sustentada ou refutada por evidências. É a unidade base de conhecimento no sistema.

**Estrutura:**
```python
Proposição:
  id: UUID
  enunciado: str                    # "Qualidade de código é mensurável"
  evidencias_apoiam: [Evidência]    # Lista de evidências que apoiam
  evidencias_refutam: [Evidência]   # Lista de evidências que refutam
  solidez: float                    # 0-1, DERIVADO (não definido manualmente)
  usos: [ArgumentoRef]              # Onde é usada como fundamento
```

**Características fundamentais:**
- **Não existe "fato" vs "suposição"**: Todas são proposições com diferentes graus de solidez
- **Solidez é calculada**: Derivada automaticamente das evidências (quantidade, qualidade, fonte)
- **Reutilizável**: Uma proposição pode ser usada como fundamento em múltiplos argumentos
- **Evolutiva**: Solidez muda conforme novas evidências são adicionadas

**Exemplos:**
- Proposição: "Linguagem permite transmitir ficções"
  - Solidez: 0.85 (múltiplas evidências de estudos linguísticos)
  - Usada em: Argumento sobre cooperação via mitos
  
- Proposição: "Qualidade de código é mensurável"
  - Solidez: 0.60 (algumas evidências, mas debate metodológico)
  - Usada em: Argumento sobre métricas de produtividade

**Importante:** "Premissa" agora é um **PAPEL**, não um tipo. Premissa = proposição sendo usada como fundamento de um argumento específico. Não há mais distinção entre premise/assumption - apenas proposições com solidez diferente.

### Evidência (Sustentação de Proposições)

**O que é:** Informação que apoia ou refuta uma proposição.

**Estrutura:**
```python
Evidência:
  id: UUID
  descricao: str                    # "Estudo de Smith et al. (2023)"
  fonte: str                        # DOI, URL, referência
  forca: str                        # "forte", "moderada", "fraca"
  tipo: str                         # "estudo", "exemplo", "autoridade", "experiência"
  contexto: str                     # Em que contexto essa evidência se aplica
```

**Características:**
- **Pode apoiar ou refutar**: Uma evidência pode fortalecer ou enfraquecer uma proposição
- **Força variável**: Evidências têm diferentes graus de força (forte, moderada, fraca)
- **Tipos diversos**: Estudos empíricos, exemplos, autoridade, experiência pessoal
- **Contexto importa**: Evidências são válidas em contextos específicos

**Exemplos:**
- Evidência (apoia): "Estudo de Smith et al. (2023) com 1000 desenvolvedores mostra correlação entre TDD e redução de bugs"
  - Tipo: estudo
  - Força: forte
  - Fonte: DOI: 10.1234/example

- Evidência (refuta): "Experiência pessoal: TDD aumentou tempo de desenvolvimento em 30%"
  - Tipo: experiência
  - Força: fraca
  - Contexto: equipe pequena, projeto específico

### Argumento (Lente, Estrutura Lógica)

**O que é:** Uma forma de ver/defender uma ideia através de estrutura lógica (claim + fundamentos).

**Características:**
- Estrutura: claim → fundamentos (proposições) → evidências
- Múltiplos argumentos podem defender mesma ideia (diferentes ângulos)
- Argumento = mapa, Ideia = território
- **Fundamentos são proposições**: Não há mais distinção entre premises/assumptions

**Estrutura atualizada:**
```python
Argumento:
  id: UUID
  idea_id: UUID
  claim: str                        # Afirmação principal
  fundamentos: [ProposicaoRef]      # Proposições que sustentam o argumento
  evidencias: [EvidenciaRef]        # Evidências diretas do argumento
```

**Exemplos:**
- Ideia: "Semana de 4 dias"
  - Argumento 1 (lente produtividade): 
    - Claim: "Aumenta produtividade via descanso"
    - Fundamentos: [Proposição: "Descanso aumenta foco", Proposição: "Foco aumenta produtividade"]
  - Argumento 2 (lente retenção):
    - Claim: "Reduz turnover em 20%"
    - Fundamentos: [Proposição: "Satisfação aumenta retenção"]

## Relações Entre Entidades

### Ideia ↔ Conceito (N:N)
- **Relacionamento é referência, não posse**: Ideia referencia múltiplos conceitos da biblioteca global
- Ideia não possui conceitos, apenas referencia entidades globais existentes
- Mesmo conceito da biblioteca aparece em múltiplas ideias (reutilização)
- Sistema detecta conceitos compartilhados via vetor semântico
- Conceito existe independentemente: mesmo que todas as ideias que o referenciam sejam removidas, o conceito permanece na biblioteca global

### Ideia ↔ Argumento (1:N)
- Ideia pode ter múltiplos argumentos (diferentes lentes)
- Argumento pertence a uma ideia

### Argumento ↔ Conceito (N:N)
- Argumento usa conceitos nos fundamentos (proposições contêm conceitos)

### Argumento ↔ Proposição (N:N)
- Argumento usa proposições como fundamentos
- Uma proposição pode ser usada em múltiplos argumentos

### Proposição ↔ Evidência (N:N)
- Proposição tem evidências que apoiam e evidências que refutam
- Evidência pode apoiar ou refutar múltiplas proposições

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

Proposições:
- P1: "Linguagem permite transmitir ficções" (solidez: 0.85)
- P2: "Mitos compartilhados permitem cooperação em massa" (solidez: 0.75)

Evidências:
- E1: "Católicos cooperam via crença em Deus" (apoia P2, tipo: exemplo, força: moderada)
- E2: "Sérvios cooperam via crença em nação" (apoia P2, tipo: exemplo, força: moderada)
- E3: "Estudos linguísticos mostram capacidade de transmitir abstrações" (apoia P1, tipo: estudo, força: forte)

Argumento principal:
claim: "Cooperação em massa depende de mitos compartilhados"
fundamentos: [P1, P2]  # Proposições usadas como fundamentos
evidências: [E1, E2, E3]
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

## Rastreabilidade

### Propagação de Solidez

Quando uma proposição é usada como fundamento em múltiplos argumentos, sua solidez afeta todos eles:

- **Fragilidade se propaga**: Se uma proposição base tem baixa solidez, todos os argumentos que dependem dela são afetados
- **Fortalecimento se propaga**: Fortalecer uma proposição fortalece todos os argumentos que dependem dela
- **Alertas automáticos**: Sistema pode alertar: "3 argumentos dependem de proposição com baixa solidez (0.35)"

**Exemplo:**
```
Proposição P: "Qualidade de código é mensurável" (solidez: 0.40)
  └─ Usada em Argumento A1: "Métricas de qualidade validam TDD"
  └─ Usada em Argumento A2: "Code review reduz bugs"
  └─ Usada em Argumento A3: "Refactoring melhora manutenibilidade"

Sistema alerta: "3 argumentos dependem de proposição com baixa solidez. 
Fortalecer P fortaleceria A1, A2 e A3."
```

### Dependências Explícitas

O sistema mantém rastreabilidade clara de:
- Quais argumentos dependem de cada proposição
- Quais proposições são fundamentais (usadas em muitos argumentos)
- Como fragilidades em proposições base afetam a solidez geral do conhecimento

### Estratégia de Fortalecimento

Quando uma proposição é identificada como frágil:
1. Sistema identifica todos os argumentos que dependem dela
2. Sugere buscar evidências para fortalecer a proposição
3. Mostra impacto: "Fortalecer esta proposição afetaria 5 argumentos"

## Referências

- `docs/vision/epistemology.md` - Fundamento filosófico da ontologia (proposições, solidez, evidências)
- `docs/architecture/concept_model.md` - Estrutura de dados técnica de Conceito
- `docs/architecture/idea_model.md` - Estrutura de dados técnica de Ideia
- `docs/architecture/argument_model.md` - Estrutura de dados técnica de Argumento
- `docs/vision/cognitive_model/core.md` - Conceitos fundamentais (artefatos, solidez)
- `docs/vision/cognitive_model/evolution.md` - Como pensamento evolui e solidez é calculada

