# Modelo Cognitivo

## Visão Geral

Este documento complementa `vision.md`, focando em **COMO** o pensamento do usuário evolui ao longo da conversa. Enquanto `vision.md` descreve o que o sistema faz e para quem, este documento explora a evolução dos artefatos cognitivos que representam o entendimento progressivo do argumento científico.

> **Nota:** Este documento descreve como pensamento **evolui** durante conversa.
> Para estrutura de dados técnica de Argumento, consulte `docs/architecture/argument_model.md`.
> Para ontologia completa (Conceito/Ideia/Argumento), consulte `docs/architecture/ontology.md`.

**Foco**: Evolução cognitiva durante conversa, não apenas funcionalidades ou fluxos.

**Relacionamento:**
- **cognitive_model.md (este doc):** Processo cognitivo (como pensamento evolui)
- **argument_model.md:** Estrutura técnica (como Argumento é persistido)
- **ontology.md:** Definições filosóficas (o que é Argumento)
- **epistemology.md:** Base filosófica (proposições, solidez, evidências)

**Relacionamento com vision.md**:
- `vision.md`: O que é, para quem, jornada do usuário, tipos de artigo
- `cognitive_model.md`: Como o pensamento evolui, quais artefatos cognitivos são construídos, como sistema provoca reflexão

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

## Evolução do Modelo

### Campos Começam Vazios

No início da conversa, a maioria dos campos está vazia ou com valores genéricos:

```python
# Turno 1 (início)
claim: "LLMs aumentam produtividade"  # vago
fundamentos: []  # Ainda sem proposições identificadas
open_questions: []
contradictions: []
evidências: []  # Ainda sem evidências
context: {
  "domain": "unclear",
  "technology": "unclear",
  "population": "not specified"
}
```

### Preenchimento Progressivo

Conforme a conversa evolui, campos são preenchidos:

```python
# Turno 3
claim: "Claude Code aumenta produtividade em equipes Python"
fundamentos: [
  ProposiçãoRef(
    id="prop-1",
    enunciado="Equipes Python existem",
    solidez=0.90  # Alta solidez: evidência direta da conversa
  ),
  ProposiçãoRef(
    id="prop-2",
    enunciado="Claude Code é usado em desenvolvimento",
    solidez=0.85  # Alta solidez: evidência direta
  ),
  ProposiçãoRef(
    id="prop-3",
    enunciado="Produtividade é mensurável",
    solidez=0.50  # Solidez média: algumas evidências, mas debate metodológico
  ),
  ProposiçãoRef(
    id="prop-4",
    enunciado="Resultado é generalizável",
    solidez=0.30  # Baixa solidez: poucas evidências (equivalente a "assumption")
  )
]
open_questions: ["Como medir produtividade?", "Qual é o baseline?"]
evidências: []  # Ainda sem evidências bibliográficas
context: {
  "domain": "software development",
  "technology": "Python, Claude Code",
  "population": "not specified"
}
```

### Claim Pode Mudar Radicalmente

Mudanças de direção são naturais e o sistema adapta:

```python
# Turno 5: Mudança de direção
claim: "Quero fazer revisão de literatura sobre LLMs e produtividade"
# Claim anterior abandonado, não mesclado
fundamentos: []  # Resetado para novo contexto
open_questions: ["Qual é o estado da arte?", "Quais são as lacunas na literatura?"]
evidências: []  # Resetado para novo contexto
context: {
  "domain": "software development",
  "technology": "LLMs, code assistants",
  "population": "not applicable for literature review",
  "article_type": "review"
}
```

### Sistema Provoca para Preencher Lacunas

O sistema identifica lacunas e provoca reflexão:

- **Lacuna detectada**: `open_questions` tem itens não respondidos
- **Ação**: Sistema pergunta: "Você mencionou produtividade, mas e QUALIDADE do código? Isso importa para sua pesquisa?"
- **Resultado**: Usuário responde → novas proposições adicionadas a `fundamentos` (com solidez inicial baixa se não houver evidências)

### Solidez Aumenta com Evidências

Conforme evidências são adicionadas, a solidez das proposições aumenta dinamicamente:

```python
# Estado inicial: proposição com baixa solidez (poucas evidências)
fundamentos: [
  ProposiçãoRef(
    id="prop-3",
    enunciado="Redução de tempo não compromete qualidade",
    solidez=0.25  # Baixa: apenas inferência do usuário
  )
]

# Após Pesquisador adicionar evidências bibliográficas
evidências: [
  {
    "id": "evid-5",
    "descricao": "Meta-análise de 15 estudos mostra correlação positiva entre uso de IA e qualidade",
    "fonte": "doi:10.5678/example",
    "forca": "forte",
    "tipo": "estudo",
    "apoia": ["prop-3"]
  }
]

# Solidez recalculada automaticamente
fundamentos: [
  ProposiçãoRef(
    id="prop-3",
    enunciado="Redução de tempo não compromete qualidade",
    solidez=0.70  # Aumentou: evidência forte adicionada
  )
]
```

**Importante**: Não há processo de "virar premissa após validação". Há evolução contínua de solidez conforme evidências são acumuladas.

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

> **Nota:** Para schema completo de Argument, consulte `docs/architecture/argument_model.md`.

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

## Dialética: Provocação + Estruturação

O sistema opera em um ciclo dialético: **provocação** (identificar lacunas) + **estruturação** (organizar ideias).

### Detecção Automática de Lacunas

**Opção A: LLM Analisa e Sugere** (implementação atual)
- Orquestrador analisa conversa e identifica lacunas
- Gera `reflection_prompt` quando detecta aspecto não explorado
- Exemplo: "Você mencionou produtividade, mas e QUALIDADE do código? Isso importa para sua pesquisa?"

**Opção B: Regras Determinísticas** (futuro, se necessário)
- Regras baseadas em tipo de artigo
- Exemplo: Artigo empírico requer população + métricas + baseline

### Estruturador Proativo Quando Contexto Claro

Quando contexto está claro o suficiente, Estruturador pode ser proativo:
- Sistema detecta: `claim` específico + `context` completo
- Sugere: "Posso chamar o Estruturador para organizar essa ideia em uma questão de pesquisa estruturada?"
- Usuário aprova → Estruturador identifica proposições e adiciona a `fundamentos`

### Fortalecimento/Enfraquecimento com Evidências

**Sistema não valida proposições**: Em vez de validar/refutar, o sistema fortalece ou enfraquece proposições através de evidências:
- Pesquisador adiciona evidências que apoiam ou refutam proposições
- Solidez é recalculada automaticamente
- Sistema alerta sobre fragilidades: "3 proposições têm solidez < 0.4"
- Pesquisador abre conversa sobre evidências, não retorna veredicto binário

### Ações Baratas vs. Caras

**Ações Baratas (Proativas)**:
- Organizar ideias (Estruturador)
- Detectar lacunas (Orquestrador)
- Validar lógica (Metodologista)
- Sistema pode sugerir sem pedir permissão explícita

**Ações Caras (Pedir Permissão)**:
- Pesquisar literatura (Pesquisador - custo de API + tempo)
- Gerar rascunho completo (Escritor - custo alto)
- Sistema sempre pede permissão antes de executar

## Detecção de Contradições (Não Determinístico)

### Processo de Detecção

1. **Metodologista analisa argumento**:
   - Compara proposições em `fundamentos`
   - Identifica conflitos entre proposições
   - Mapeia contextos que geram cada perspectiva
   - Calcula confiança (0-1)

2. **Se confidence > 80%**:
   - Sistema menciona conflito de forma natural
   - Não bloqueia ou impõe
   - Apenas provoca reflexão
   - **Não diz "isso está errado"**: Diz "estas proposições parecem em tensão"

3. **Formato da menção**:
   - Conversacional, não acusatório
   - Mapeia contextos: "A proposição X se aplica no contexto A, enquanto a proposição Y se aplica no contexto B"
   - Exemplo: "Notei que a proposição sobre aumento de produtividade parece em tensão com a proposição sobre aumento de bugs. Como você vê essa relação? São métricas separadas ou produtividade inclui qualidade? Em que contextos cada proposição se aplica?"

### Exemplo de Contradição Detectada

```python
# Estado atual
claim: "Claude Code aumenta produtividade em 30%"
fundamentos: [
  ProposiçãoRef(id="prop-1", enunciado="Produtividade é medida por tempo de sprint", solidez=0.70),
  ProposiçãoRef(id="prop-2", enunciado="Qualidade não é afetada", solidez=0.35)
]

# Metodologista detecta
contradictions: [
  {
    "description": "Proposição 'Claude Code aumenta produtividade' parece em tensão com proposição 'Claude Code aumenta bugs'",
    "proposicoes_envolvidas": ["prop-1", "prop-3"],
    "confidence": 0.85,
    "contextos": {
      "prop-1": "Contexto: métricas de tempo de sprint",
      "prop-3": "Contexto: métricas de qualidade de código (bugs)"
    },
    "suggested_resolution": "Produtividade pode incluir qualidade? Ou são métricas separadas? Como mapear contextos onde cada proposição se aplica?"
  }
]

# Sistema menciona (não bloqueia)
"Notei que a proposição sobre aumento de produtividade parece em tensão com a proposição sobre aumento de bugs. Como você vê essa relação? São métricas separadas ou produtividade inclui qualidade?"
```

## Objetivo Final: "Flecha Penetrante"

O objetivo do sistema é ajudar o usuário a construir um **argumento sólido com respaldo bibliográfico**, sem premissas frágeis, sem dúvidas não examinadas. A clareza emerge da elaboração.

### Características do Argumento Maduro

- **`claim` estável e específico**: Não muda radicalmente a cada turno
- **`fundamentos` com solidez média-alta**: Proposições principais com solidez > 0.6
- **Evidências suficientes**: Fundamentos principais têm evidências que os sustentam
- **`open_questions` respondidas**: Lacunas foram exploradas
- **`contradictions` resolvidas**: Tensões entre proposições foram endereçadas
- **`evidências` presente**: Evidência bibliográfica encontrada e vinculada a proposições

### Exemplo de Argumento Maduro

```python
claim: "Claude Code reduz tempo de sprint em 30% (de 2h para 1.4h) em equipes Python de 2-5 devs, sem comprometer qualidade do código (medida por bugs por sprint)"

fundamentos: [
  ProposiçãoRef(
    id="prop-1",
    enunciado="Equipes Python de 2-5 devs existem e são representativas",
    solidez=0.85  # Alta: evidência direta da conversa
  ),
  ProposiçãoRef(
    id="prop-2",
    enunciado="Tempo de sprint é métrica válida de produtividade",
    solidez=0.75  # Alta: evidências bibliográficas
  ),
  ProposiçãoRef(
    id="prop-3",
    enunciado="Bugs por sprint é métrica válida de qualidade",
    solidez=0.70  # Alta: evidências bibliográficas
  ),
  ProposiçãoRef(
    id="prop-4",
    enunciado="Redução de tempo não compromete qualidade",
    solidez=0.75  # Alta: evidências bibliográficas + dados do usuário
  ),
  ProposiçãoRef(
    id="prop-5",
    enunciado="Resultado é generalizável para outras linguagens",
    solidez=0.40  # Média-baixa: poucas evidências (hipótese a testar)
  )
]

open_questions: []  # Todas respondidas

contradictions: []  # Nenhuma detectada

evidências: [
  {
    "id": "evid-1",
    "descricao": "Smith et al. (2023) encontraram redução de 25-40% em tempo de tarefa",
    "fonte": "doi:10.1234/example",
    "forca": "forte",
    "tipo": "estudo",
    "apoia": ["prop-2", "prop-4"]
  },
  {
    "id": "evid-2",
    "descricao": "Meta-análise de 15 estudos mostra correlação positiva entre uso de IA e qualidade",
    "fonte": "doi:10.5678/example",
    "forca": "forte",
    "tipo": "estudo",
    "apoia": ["prop-4"]
  }
]

context: {
  "domain": "software development",
  "technology": "Python, Claude Code",
  "population": "teams of 2-5 developers",
  "metrics": "time per sprint, bugs per sprint",
  "article_type": "empirical"
}
```

## Indicadores de Maturidade (Internos)

Os indicadores de maturidade são **não determinísticos** e **não avisam o usuário diretamente**. O sistema usa para sugerir próximos passos, não para impor.

### Sinais de Maturidade

1. **`claim` estável**: Não muda significativamente por 3+ turnos
2. **Fundamentos com solidez média-alta**: Proposições principais com solidez > 0.6
3. **Evidências suficientes**: Fundamentos principais têm evidências que os sustentam
4. **`open_questions` respondidas**: Lista vazia ou apenas questões secundárias
5. **`contradictions` resolvidas**: Nenhum conflito entre proposições detectado
6. **`evidências` presente**: Evidência bibliográfica encontrada e vinculada a proposições (quando aplicável)

### Como Sistema Usa Indicadores

Sistema não diz: "Seu argumento está maduro!"  
Sistema apresenta resultado: "Validei o rigor científico: [resultado]. Faz sentido?" ou "Temos uma boa base. Para compilar o artigo completo, preciso fazer chamadas de API que podem ter custo. Quer que eu chame o Escritor agora?"

**Exemplo de sugestão baseada em maturidade**:
```python
# Sistema detecta maturidade
claim_stable: True
fundamentos_solidos: True  # Proposições principais com solidez > 0.6
evidencias_suficientes: True  # Fundamentos principais têm evidências
open_questions_empty: True
contradictions_resolved: True

# Sistema sugere (não impõe)
"Parece que temos uma hipótese bem estruturada. Quer validar rigor científico com o Metodologista?"
```

## Exemplo Completo: "Levantamento de Obra com IA"

### Turno 1: Claim Vago, Assumptions Detectadas

**Input do usuário**: "Quero fazer um artigo sobre levantamento de obra com IA"

**Estado cognitivo**:
```python
claim: "Artigo sobre levantamento de obra com IA"
fundamentos: [
  ProposiçãoRef(
    id="prop-1",
    enunciado="Levantamento de obra é um problema relevante",
    solidez=0.30  # Baixa: apenas inferência inicial
  ),
  ProposiçãoRef(
    id="prop-2",
    enunciado="IA pode ajudar em levantamento de obra",
    solidez=0.25  # Baixa: hipótese inicial
  ),
  ProposiçãoRef(
    id="prop-3",
    enunciado="Há contribuição acadêmica possível",
    solidez=0.20  # Muito baixa: hipótese não explorada
  )
]
open_questions: [
  "O que é levantamento de obra?",
  "Como IA pode ajudar?",
  "Qual é o problema específico?",
  "Qual tipo de artigo? (empírico, revisão, teórico)"
]
contradictions: []
evidências: []
context: {
  "domain": "construction",
  "technology": "AI (unclear which)",
  "population": "not specified",
  "article_type": "unclear"
}
```

**Ação do sistema**: Orquestrador explora contexto
- "Interessante! Me conta mais: o que é levantamento de obra para você? E como você imagina que IA pode ajudar?"

### Turno 3: Claim Muda, Fundamentos Adicionados, Sistema Provoca

**Input do usuário**: "Levantamento de obra é medir quantidades de materiais. Quero usar visão computacional para automatizar"

**Estado cognitivo**:
```python
claim: "Usar visão computacional para automatizar levantamento de quantidades de materiais em obras"
fundamentos: [
  ProposiçãoRef(
    id="prop-4",
    enunciado="Levantamento de obra envolve medir quantidades de materiais",
    solidez=0.70  # Média-alta: evidência direta da conversa
  ),
  ProposiçãoRef(
    id="prop-5",
    enunciado="Visão computacional pode identificar materiais em imagens",
    solidez=0.60  # Média: conhecimento técnico geral
  ),
  ProposiçãoRef(
    id="prop-6",
    enunciado="Automatização é desejável",
    solidez=0.50  # Média: inferência do contexto
  ),
  ProposiçãoRef(
    id="prop-7",
    enunciado="Visão computacional é precisa o suficiente para quantificar materiais",
    solidez=0.35  # Baixa: hipótese não verificada
  ),
  ProposiçãoRef(
    id="prop-8",
    enunciado="Automatização reduz tempo/custo sem comprometer precisão",
    solidez=0.30  # Baixa: hipótese não verificada
  ),
  ProposiçãoRef(
    id="prop-9",
    enunciado="Há contribuição acadêmica (não é apenas aplicação direta)",
    solidez=0.25  # Baixa: hipótese não explorada
  )
]
open_questions: [
  "Qual é a precisão atual de métodos manuais?",
  "Qual é o baseline de tempo/custo?",
  "Como validar precisão da IA?",
  "Qual tipo de materiais? (tijolos, concreto, etc.)"
]
contradictions: []
evidências: []
context: {
  "domain": "construction, quantity surveying",
  "technology": "computer vision, AI",
  "population": "not specified",
  "article_type": "unclear"  # Pode ser empírico (testar) ou metodológico (validar método)
}
```

**Ação do sistema**: Orquestrador provoca reflexão
- "Você mencionou automatização, mas e a PRECISÃO? Como você validaria que a IA é tão precisa quanto métodos manuais?"

### Turno 5: Pesquisador Busca, Evidências Adicionadas, Modelo Amadurece

**Input do usuário**: "Quero testar se visão computacional é mais rápida e precisa que métodos manuais"

**Estado cognitivo** (após Pesquisador buscar literatura):
```python
claim: "Visão computacional é mais rápida e precisa que métodos manuais para levantamento de quantidades de materiais em obras"
fundamentos: [
  ProposiçãoRef(
    id="prop-4",
    enunciado="Levantamento de obra envolve medir quantidades de materiais",
    solidez=0.70  # Mantida: evidência direta
  ),
  ProposiçãoRef(
    id="prop-5",
    enunciado="Visão computacional pode identificar materiais em imagens",
    solidez=0.75  # Aumentou: evidência bibliográfica adicionada
  ),
  ProposiçãoRef(
    id="prop-10",
    enunciado="Métodos manuais existem e têm precisão conhecida",
    solidez=0.80  # Alta: evidência bibliográfica forte
  ),
  ProposiçãoRef(
    id="prop-11",
    enunciado="Comparação de métodos é válida academicamente",
    solidez=0.70  # Média-alta: padrão metodológico
  ),
  ProposiçãoRef(
    id="prop-7",
    enunciado="Visão computacional é precisa o suficiente para quantificar materiais",
    solidez=0.65  # Aumentou: evidência bibliográfica (85% precisão)
  ),
  ProposiçãoRef(
    id="prop-12",
    enunciado="Resultado é generalizável para diferentes tipos de obras",
    solidez=0.40  # Média-baixa: poucas evidências
  ),
  ProposiçãoRef(
    id="prop-13",
    enunciado="Precisão da IA é suficiente para uso prático",
    solidez=0.60  # Média: evidência parcial (85% é alto, mas contexto específico)
  )
]
open_questions: [
  "Qual é o tamanho da amostra necessária?",
  "Como definir 'mais preciso'? (margem de erro aceitável?)",
  "Quais tipos de materiais testar? (tijolos, concreto, aço?)"
]
contradictions: []
evidências: [
  {
    "id": "evid-3",
    "descricao": "Zhang et al. (2022) aplicaram YOLO para detecção de materiais com 85% de precisão",
    "fonte": "doi:10.1234/construction-ai",
    "forca": "forte",
    "tipo": "estudo",
    "apoia": ["prop-5", "prop-7", "prop-13"]
  },
  {
    "id": "evid-4",
    "descricao": "Revisão sistemática de 20 estudos mostra erro médio de 7.5% em levantamentos manuais",
    "fonte": "doi:10.5678/manual-survey",
    "forca": "forte",
    "tipo": "estudo",
    "apoia": ["prop-10"]
  }
]
# Solidez de prop-5, prop-7 e prop-13 aumentou após adicionar evid-3
# Solidez de prop-10 aumentou após adicionar evid-4
context: {
  "domain": "construction, quantity surveying",
  "technology": "computer vision, YOLO, deep learning",
  "population": "construction projects (not specified: residential, commercial, etc.)",
  "metrics": "speed (time), accuracy (error margin)",
  "article_type": "empirical"  # Agora claro: quer testar hipótese
}
```

**Ação do sistema**: Orquestrador apresenta resultado
- "Temos uma boa base! Encontrei estudos relevantes. Validei o desenho experimental dessa comparação: [resultado]. Faz sentido?"
[Bastidores: 🔬 Metodologista validou → 🎯 Orquestrador curou]

### Turno 7: Modelo Maduro, Pronto para Estruturação

**Estado cognitivo** (após Metodologista validar):
```python
claim: "Visão computacional (YOLO) é mais rápida (redução de 60% no tempo) e mais precisa (erro de 3% vs 7.5% manual) que métodos manuais para levantamento de quantidades de tijolos em obras residenciais"

fundamentos: [
  ProposiçãoRef(
    id="prop-4",
    enunciado="Levantamento de obra envolve medir quantidades de materiais",
    solidez=0.70  # Mantida
  ),
  ProposiçãoRef(
    id="prop-14",
    enunciado="Visão computacional (YOLO) pode identificar tijolos em imagens",
    solidez=0.80  # Alta: evidências + validação metodológica
  ),
  ProposiçãoRef(
    id="prop-10",
    enunciado="Métodos manuais têm erro médio de 7.5%",
    solidez=0.80  # Alta: evidência bibliográfica forte
  ),
  ProposiçãoRef(
    id="prop-11",
    enunciado="Comparação experimental é válida academicamente",
    solidez=0.75  # Alta: validação metodológica
  ),
  ProposiçãoRef(
    id="prop-15",
    enunciado="Obras residenciais são contexto representativo",
    solidez=0.65  # Média-alta: justificativa metodológica
  ),
  ProposiçãoRef(
    id="prop-16",
    enunciado="Resultado é generalizável para outros materiais",
    solidez=0.35  # Baixa: hipótese futura, poucas evidências
  )
]

open_questions: []  # Todas respondidas

contradictions: []  # Nenhuma detectada

evidências: [
  # ... (mesmo do turno 5, mais evidências adicionadas)
]

context: {
  "domain": "construction, quantity surveying",
  "technology": "computer vision, YOLO, deep learning",
  "population": "residential construction projects",
  "metrics": "speed (time reduction %), accuracy (error margin %)",
  "article_type": "empirical"
}
```

**Ação do sistema**: Apresentação de resultado
- "Hipótese validada! Organizei em uma questão de pesquisa estruturada: [resultado]. Podemos seguir com: 1) definir desenho experimental, 2) pesquisar literatura, ou 3) algo diferente?"
[Bastidores: 📝 Estruturador estruturou → 🎯 Orquestrador curou]

## Persistência Silenciosa (Snapshots)

O sistema mantém uma estratégia de **persistência silenciosa** que captura o progresso do pensamento do usuário sem interromper o fluxo conversacional. A cada mensagem, o sistema avalia se o `CognitiveModel` contribuiu com algo novo e, caso positivo, cria ou atualiza um snapshot automaticamente.

### O que é um Snapshot

Um **snapshot** é a persistência do `CognitiveModel` quando ele contribui com algo novo ao argumento em construção. Representa um ponto de salvamento do progresso cognitivo, permitindo que o usuário retome a conversa de onde parou sem perder evolução significativa.

**Características**:
- **Persistência automática**: Sistema avalia e decide criar snapshot sem intervenção do usuário
- **Versionamento automático**: Cada snapshot recebe versão incremental (V1, V2, V3...)
- **Silencioso**: Usuário não vê notificação ou interrupção no fluxo conversacional
- **Materialização**: Snapshot vira entidade `Argument` no banco de dados

### Avaliação Contínua

A cada mensagem do usuário, o sistema avalia se deve criar ou atualizar snapshot:

```python
# Fluxo de avaliação (a cada turno)
1. Usuário envia mensagem
2. Sistema atualiza CognitiveModel (claim, fundamentos, etc.)
3. Sistema avalia maturidade do modelo:
   - CognitiveModel contribuiu com algo novo?
   - Argumento atingiu maturidade suficiente?
   - Há critérios que impedem snapshot?
4. Se avaliação positiva → cria/atualiza snapshot silenciosamente
```

### Critérios para NÃO Atualizar Snapshot

O sistema **não cria ou atualiza** snapshot quando detecta:

1. **Usuário fugiu do assunto**:
   - Mudança radical de tópico não relacionada ao argumento atual
   - Claim muda para área completamente diferente
   - Contexto não relacionado ao progresso cognitivo anterior

2. **Repetiu sem novidade**:
   - Mesma informação já capturada em snapshot anterior
   - Reafirmação sem novos detalhes ou refinamentos
   - `claim` idêntico ao snapshot mais recente

3. **Pergunta sem contribuição**:
   - Perguntas que não agregam ao argumento em construção
   - Dúvidas que não levam a evolução do pensamento
   - Exploração que não resulta em novos `fundamentos` ou refinamento de `claim`

**Exemplo de avaliação**:
```python
# Turno anterior: Snapshot V2 criado
cognitive_model.claim = "LLMs aumentam produtividade em equipes Python"

# Turno atual: Usuário pergunta sem agregar
user_input = "Como funciona Python?"
# Sistema avalia: não há novidade ao argumento → não cria snapshot

# Turno seguinte: Usuário refina claim
user_input = "Especificamente, Claude Code reduz tempo de sprint em 30%"
cognitive_model.claim = "Claude Code reduz tempo de sprint em 30% em equipes Python"
# Sistema avalia: contribuição nova → cria Snapshot V3
```

### Silêncio no Fluxo Conversacional

Snapshots são **completamente silenciosos** do ponto de vista do usuário:

- **Sem notificações**: Usuário não é informado quando snapshot é criado
- **Sem interrupções**: Fluxo conversacional continua normalmente
- **Sem confirmações**: Sistema não pede permissão para persistir
- **Transparente**: Persistência acontece em background

O objetivo é capturar progresso sem quebrar o ritmo do pensamento do usuário. Ele continua explorando e refinando ideias enquanto o sistema salva automaticamente pontos de maturidade.

### Versionamento Automático

Cada snapshot recebe uma versão automática e incremental:

- **V1**: Primeiro snapshot criado quando argumento atinge maturidade inicial
- **V2**: Snapshot subsequente quando argumento evolui significativamente
- **V3, V4, V5...**: Versões seguintes conforme argumento amadurece

O versionamento permite:
- **Rastreabilidade**: Ver evolução do argumento ao longo do tempo
- **Comparação**: Comparar diferentes versões do mesmo argumento
- **Recuperação**: Retomar conversa de qualquer versão anterior

```python
# Exemplo de versionamento
idea_id = "uuid-idea-123"
snapshot_v1 = create_snapshot(idea_id, cognitive_model_v1)  # version=1
snapshot_v2 = create_snapshot(idea_id, cognitive_model_v2)  # version=2
snapshot_v3 = create_snapshot(idea_id, cognitive_model_v3)  # version=3
```

### Trigger para Épico 13: Detecção de Conceitos

Quando um snapshot é criado, o sistema automaticamente dispara o **pipeline de detecção de conceitos** (Épico 13):

```python
# Fluxo completo
1. Snapshot é criado (CognitiveModel → Argument persistido)
2. Pipeline de detecção é acionado automaticamente
3. LLM extrai conceitos-chave do snapshot
4. Sistema gera embeddings e busca conceitos similares
5. Cria novos conceitos ou vincula a conceitos existentes
6. Links Idea ↔ Concept são criados
```

Esta integração permite que conceitos sejam detectados e organizados automaticamente sempre que um argumento atinge maturidade, construindo progressivamente a biblioteca global de conceitos do sistema.

> **Nota técnica**: Para detalhes sobre implementação técnica de snapshots, critérios de maturidade e integração com detecção de conceitos, consulte `docs/architecture/snapshot_strategy.md`.

## Referências

- `docs/vision/epistemology.md` - Base filosófica (proposições, solidez, evidências)
- `docs/architecture/ontology.md` - Ontologia: Conceito, Ideia, Argumento, Proposição, Evidência
- `docs/architecture/argument_model.md` - Estrutura técnica de Argument
- `docs/architecture/idea_model.md` - Como Ideia possui Argumentos
- `docs/product/vision.md` (Seção 4) - Entidade Ideia

