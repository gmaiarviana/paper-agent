# Modelo Cognitivo - Conceitos Fundamentais

## Visão Geral

Este documento complementa `vision.md`, focando em **COMO** o pensamento do usuário evolui ao longo da conversa. Enquanto `vision.md` descreve o que o sistema faz e para quem, este documento explora a evolução dos artefatos cognitivos que representam o entendimento progressivo do argumento científico.

> **Nota:** Este documento descreve como pensamento **evolui** durante conversa.
> Para estrutura de dados técnica de Argumento, consulte `../../architecture/data-models/argument_model.md`.
> Para ontologia completa (Conceito/Ideia/Argumento), consulte `../../architecture/data-models/ontology.md`.

**Foco**: Evolução cognitiva durante conversa, não apenas funcionalidades ou fluxos.

**Relacionamento:**
- **cognitive_model/core.md (este doc):** Conceitos fundamentais (artefatos, responsabilidades)
- **cognitive_model/evolution.md:** Processo de evolução (como pensamento evolui)
- **cognitive_model/examples.md:** Exemplos práticos de evolução
- **argument_model.md:** Estrutura técnica (como Argumento é persistido)
- **ontology.md:** Definições filosóficas (o que é Argumento)
- **epistemology.md:** Base filosófica (proposições, solidez, evidências)

**Relacionamento com vision.md**:
- `vision.md`: O que é, para quem, jornada do usuário, tipos de artigo
- `cognitive_model/`: Como o pensamento evolui, quais artefatos cognitivos são construídos, como sistema provoca reflexão

## Artefatos Cognitivos Explícitos

O sistema mantém um modelo explícito do pensamento do usuário, representado pelos seguintes campos:

### `claim`
**O que é**: O que o usuário está tentando dizer/defender no momento atual.

**Características**:
- Evolui a cada turno (pode mudar radicalmente)
- Pode começar vago ("LLMs aumentam produtividade")
- Pode se tornar específico ("Claude Code reduz tempo de sprint de 2h para 30min em equipes Python de 2-5 devs")
- Não é fixo: mudanças de direção são naturais

**Exemplo de evolução**:
- Turno 1: "LLMs aumentam produtividade"
- Turno 3: "Claude Code aumenta produtividade em equipes Python"
- Turno 5: "Claude Code reduz tempo de sprint em 30% em equipes de 2-5 devs"

### `claim_history`
**O que é**: Histórico de evolução do claim (sistema maduro).

**Características**:
- Registra mudanças significativas do claim
- Permite rastreabilidade: "Como chegamos aqui?"
- Útil para detectar padrões de mudança de direção
- Não é preenchido em versões iniciais do sistema

**Estrutura** (futuro):
```python
claim_history: [
  {
    "turn": 1,
    "claim": "LLMs aumentam produtividade",
    "reason": "Input inicial do usuário"
  },
  {
    "turn": 3,
    "claim": "Claude Code aumenta produtividade em equipes Python",
    "reason": "Usuário especificou ferramenta e contexto"
  },
  {
    "turn": 5,
    "claim": "Claude Code reduz tempo de sprint em 30% em equipes de 2-5 devs",
    "reason": "Usuário forneceu métricas e população"
  }
]
```

### `fundamentos`
**O que é**: Proposições que sustentam o argumento, cada uma com sua solidez derivada de evidências.

**Características**:
- Lista de referências a Proposições (ProposiçãoRef)
- Começa vazio, preenchido conforme conversa
- Representa fundamentos do argumento
- **Não há distinção entre "premise" e "assumption"**: Todas são proposições com solidez variável
- **Solidez é derivada automaticamente**: Não é definida manualmente, mas calculada a partir das evidências que apoiam cada proposição
- Proposições de baixa solidez (< 0.4) são equivalentes ao que antes eram "assumptions"
- Proposições de alta solidez (> 0.7) são equivalentes ao que antes eram "premises"
- Exemplos: "Equipes Python existem", "Tempo de sprint é mensurável", "Claude Code é usado em desenvolvimento"

**Exemplo**:
```python
fundamentos: [
  ProposiçãoRef(
    id="prop-1",
    enunciado="Equipes de desenvolvimento Python usam ferramentas de IA",
    solidez=0.75  # Derivado de evidências: estudos + exemplos
  ),
  ProposiçãoRef(
    id="prop-2",
    enunciado="Tempo de sprint é uma métrica válida de produtividade",
    solidez=0.65  # Algumas evidências, mas debate metodológico
  ),
  ProposiçãoRef(
    id="prop-3",
    enunciado="Redução de tempo não compromete qualidade do código",
    solidez=0.35  # Poucas evidências = proposição frágil (equivalente a "assumption")
  )
]
```

**Importante**: Solidez evolui dinamicamente. Conforme evidências são adicionadas, a solidez aumenta ou diminui automaticamente. Não há processo de "virar premissa após validação" - há "aumentar solidez com evidências".

### `open_questions`
**O que é**: O que não sabemos ainda, mas é relevante para o argumento.

**Características**:
- Lacunas identificadas pelo sistema
- Sistema provoca para preencher
- Podem ser respondidas pelo usuário ou pela pesquisa
- Exemplos: "Qual é o baseline?", "Como medir qualidade?", "Qual é o tamanho da amostra?"

**Exemplo**:
```python
open_questions: [
  "Qual é o baseline de tempo de sprint sem Claude Code?",
  "Como medir qualidade do código além de tempo?",
  "Qual é o tamanho da amostra necessária para generalização?"
]
```

### `contradictions`
**O que é**: Conflitos entre proposições detectados pelo sistema.

**Características**:
- Não determinístico: LLM julga confiança (confidence > 80% → menciona)
- Sistema menciona de forma natural, não bloqueia
- **Não há "isso está errado"**: Há "estas proposições parecem em tensão"
- Sistema mapeia contextos que geram cada perspectiva
- Exemplos: "Proposição sobre aumento de produtividade vs. proposição sobre aumento de bugs", "Proposição sobre população específica vs. proposição sobre generalização"

**Exemplo**:
```python
contradictions: [
  {
    "description": "Proposição 'Claude Code aumenta produtividade' parece em tensão com proposição 'Claude Code aumenta bugs'",
    "proposicoes_envolvidas": ["prop-1", "prop-4"],
    "confidence": 0.85,
    "contextos": {
      "prop-1": "Contexto: métricas de tempo de sprint",
      "prop-4": "Contexto: métricas de qualidade de código"
    },
    "suggested_resolution": "Produtividade pode incluir qualidade? Ou são métricas separadas? Como mapear contextos onde cada proposição se aplica?"
  }
]
```

### `evidências`
**O que é**: Evidências que apoiam ou refutam as proposições dos fundamentos.

**Características**:
- Preenchido pelo Pesquisador após busca bibliográfica
- Representa evidência encontrada na literatura ou fornecida pelo usuário
- **Vinculadas a proposições**: Cada evidência apoia ou refuta proposições específicas
- **Afetam solidez automaticamente**: Quando evidências são adicionadas, a solidez das proposições relacionadas é recalculada
- Diferencia argumento de opinião vs. argumento fundamentado
- Exemplos: "Estudo X mostra que...", "Meta-análise Y confirma que...", "Experiência pessoal indica que..."

**Exemplo** (após pesquisa):
```python
evidências: [
  {
    "id": "evid-1",
    "descricao": "Smith et al. (2023) encontraram redução de 25-40% em tempo de tarefa",
    "fonte": "doi:10.1234/example",
    "forca": "forte",
    "tipo": "estudo",
    "apoia": ["prop-1"],  # Apoia proposição sobre produtividade
    "refuta": []
  },
  {
    "id": "evid-2",
    "descricao": "Experiência pessoal: aumento de bugs em 15% dos casos",
    "fonte": "conversa com usuário",
    "forca": "fraca",
    "tipo": "experiência",
    "apoia": [],
    "refuta": ["prop-3"]  # Refuta proposição sobre qualidade não comprometida
  }
]
# Após adicionar evidências, solidez de prop-1 aumenta, solidez de prop-3 diminui
```

### `context`
**O que é**: Domínio, tecnologia, população inferidos pelo sistema.

**Características**:
- Inferido pelo Orquestrador a partir da conversa
- Evolui conforme usuário fornece mais informação
- Exemplos: domínio="desenvolvimento de software", tecnologia="Python + Claude Code", população="equipes de 2-5 devs"

**Exemplo**:
```python
context: {
  "domain": "software development",
  "technology": "Python, Claude Code",
  "population": "teams of 2-5 developers",
  "metrics": "time per sprint",
  "article_type": "empirical"
}
```

## Responsabilidades (Quem Atualiza Cada Campo)

| Campo | Responsável | Quando Atualiza |
|-------|-------------|-----------------|
| `claim` | Orquestrador | Extrai a cada turno da conversa |
| `claim_history` | Orquestrador | Quando claim muda significativamente (sistema maduro) |
| `fundamentos` | Estruturador | Identifica proposições que sustentam o argumento |
| `solidez` (de cada fundamento) | Sistema | Derivado automaticamente de evidências |
| `evidências` | Pesquisador | Após busca bibliográfica ou fornecida pelo usuário |
| `open_questions` | Orquestrador + Metodologista | Identifica lacunas |
| `contradictions` | Metodologista | Detecta conflitos entre proposições |
| `context` | Orquestrador | Infere domínio, tecnologia, população da conversa |

### Detalhamento das Responsabilidades

**Orquestrador**:
- Extrai `claim` a cada turno analisando input + histórico
- Atualiza `claim_history` quando detecta mudança significativa
- Identifica `open_questions` quando detecta lacunas
- Infere `context` a partir de menções na conversa

**Estruturador**:
- Identifica proposições que sustentam o argumento e adiciona a `fundamentos`
- Organiza fundamentos lógicos do argumento
- Pode sugerir `open_questions` quando estrutura questão de pesquisa

**Metodologista**:
- Detecta `contradictions` (conflitos entre proposições)
- Pode identificar `open_questions` relacionadas a rigor científico
- Sugere refinamentos que podem resultar em novas proposições em `fundamentos`

**Pesquisador**:
- Adiciona `evidências` após busca bibliográfica
- Evidências são vinculadas a proposições específicas
- **Não valida/refuta**: Fortalece ou enfraquece proposições através de evidências
- Pode identificar novas `open_questions` baseadas em lacunas da literatura

**Sistema** (automático):
- Calcula `solidez` de cada proposição em `fundamentos` baseado nas evidências que a apoiam/refutam
- Recalcula solidez dinamicamente quando novas evidências são adicionadas

## Conexão com Argumento (Entidade Técnica)

> **Nota:** Para schema completo de Argument, consulte `../../architecture/data-models/argument_model.md`.

O modelo cognitivo descrito aqui é materializado tecnicamente como entidade `Argument`:
```python
# Durante conversa (em memória)
cognitive_model = {
  "claim": "...",
  "fundamentos": [...],  # Lista de ProposiçãoRef
  "open_questions": [...],
  "contradictions": [...],
  "evidências": [...]  # Lista de Evidência
}

# Ao persistir (banco de dados)
argument = Argument(
  id=UUID,
  idea_id=UUID,
  claim=cognitive_model["claim"],
  fundamentos=cognitive_model["fundamentos"],  # Referências a Proposições
  evidencias=cognitive_model["evidências"]  # Referências a Evidências
)
```

**Diferença:**
- **cognitive_model:** Estado volátil durante conversa
- **Argument:** Entidade persistida no banco

Uma **Ideia** pode ter múltiplos **Argumentos** (diferentes lentes do mesmo território).

## Referências

- `core/docs/vision/cognitive_model/evolution.md` - Processo de evolução do pensamento
- `core/docs/vision/cognitive_model/examples.md` - Exemplos práticos de evolução
- `core/docs/vision/epistemology.md` - Base filosófica (proposições, solidez, evidências)
- `../../architecture/data-models/ontology.md` - Ontologia: Conceito, Ideia, Argumento, Proposição, Evidência
- `../../architecture/data-models/argument_model.md` - Estrutura técnica de Argument
- `../../architecture/data-models/idea_model.md` - Como Ideia possui Argumentos
- `products/revelar/docs/vision.md` (Seção 4) - Entidade Ideia

