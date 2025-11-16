# Modelo Cognitivo

## Visão Geral

Este documento complementa `vision.md`, focando em **COMO** o pensamento do usuário evolui ao longo da conversa. Enquanto `vision.md` descreve o que o sistema faz e para quem, este documento explora a evolução dos artefatos cognitivos que representam o entendimento progressivo do argumento científico.

**Foco**: Evolução cognitiva durante conversa, não apenas funcionalidades ou fluxos.

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

### `premises`
**O que é**: O que assumimos como verdadeiro para o argumento fazer sentido.

**Características**:
- Começa vazio, preenchido conforme conversa
- Representa fundamentos do argumento
- Exemplos: "Equipes Python existem", "Tempo de sprint é mensurável", "Claude Code é usado em desenvolvimento"

**Exemplo**:
```python
premises: [
  "Equipes de desenvolvimento Python usam ferramentas de IA",
  "Tempo de sprint é uma métrica válida de produtividade",
  "Redução de tempo não compromete qualidade (assumido)"
]
```

### `assumptions`
**O que é**: Hipóteses não verificadas que sustentam o argumento.

**Características**:
- Diferente de `premises`: assumptions são hipóteses que precisam validação
- Sistema detecta assumptions implícitas
- Podem virar `premises` após validação (quando aplicável)
- Exemplos: "Qualidade não é afetada", "Resultado é generalizável", "Causalidade é direta"

**Exemplo**:
```python
assumptions: [
  "Redução de tempo não compromete qualidade do código",
  "Resultado é generalizável para outras linguagens",
  "Causalidade: Claude Code → redução de tempo (não confundidores)"
]
```

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
**O que é**: Tensões internas do argumento detectadas pelo sistema.

**Características**:
- Não determinístico: LLM julga confiança (confidence > 80% → menciona)
- Sistema menciona de forma natural, não bloqueia
- Exemplos: "Mencionou aumento de produtividade mas também aumento de bugs", "População é específica mas quer generalizar"

**Exemplo**:
```python
contradictions: [
  {
    "description": "Usuário mencionou aumento de produtividade mas também aumento de bugs",
    "confidence": 0.85,
    "suggested_resolution": "Produtividade pode incluir qualidade? Ou são métricas separadas?"
  }
]
```

### `solid_grounds`
**O que é**: Argumentos com base estudada (evidência bibliográfica).

**Características**:
- Preenchido pelo Pesquisador (futuro) após busca
- Representa evidência encontrada na literatura
- Diferencia argumento de opinião vs. argumento fundamentado
- Exemplos: "Estudo X mostra que...", "Meta-análise Y confirma que..."

**Exemplo** (após pesquisa):
```python
solid_grounds: [
  {
    "claim": "Ferramentas de IA aumentam produtividade em desenvolvimento",
    "evidence": "Smith et al. (2023) encontraram redução de 25-40% em tempo de tarefa",
    "source": "doi:10.1234/example"
  }
]
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
premises: []
assumptions: []
open_questions: []
contradictions: []
solid_grounds: []
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
premises: ["Equipes Python existem", "Claude Code é usado em desenvolvimento"]
assumptions: ["Produtividade é mensurável", "Resultado é generalizável"]
open_questions: ["Como medir produtividade?", "Qual é o baseline?"]
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
premises: []  # Resetado para novo contexto
assumptions: []
open_questions: ["Qual é o estado da arte?", "Quais são as lacunas na literatura?"]
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
- **Resultado**: Usuário responde → `assumptions` ou `premises` atualizados

### Suposições Viram Premissas Após Validação

Quando aplicável, `assumptions` podem virar `premises`:

```python
# Antes da validação
assumptions: ["Redução de tempo não compromete qualidade"]

# Após usuário confirmar ou pesquisa validar
premises: ["Redução de tempo não compromete qualidade (validado pelo usuário)"]
assumptions: []  # Removido de assumptions
```

## Responsabilidades (Quem Atualiza Cada Campo)

| Campo | Responsável | Quando Atualiza |
|-------|-------------|-----------------|
| `claim` | Orquestrador | Extrai a cada turno da conversa |
| `claim_history` | Orquestrador | Quando claim muda significativamente (sistema maduro) |
| `premises` | Estruturador | Organiza ideias e identifica fundamentos do argumento |
| `assumptions` | Orquestrador | Detecta hipóteses implícitas não verificadas |
| `open_questions` | Orquestrador + Metodologista | Identifica lacunas na conversa ou validação |
| `contradictions` | Metodologista | Valida lógica e detecta tensões internas |
| `solid_grounds` | Pesquisador | Após busca bibliográfica (futuro) |
| `context` | Orquestrador | Infere domínio, tecnologia, população da conversa |

### Detalhamento das Responsabilidades

**Orquestrador**:
- Extrai `claim` a cada turno analisando input + histórico
- Atualiza `claim_history` quando detecta mudança significativa
- Detecta `assumptions` implícitas através de análise conversacional
- Identifica `open_questions` quando detecta lacunas
- Infere `context` a partir de menções na conversa

**Estruturador**:
- Organiza `premises` quando estrutura argumento
- Identifica fundamentos lógicos do argumento
- Pode sugerir `open_questions` quando estrutura questão de pesquisa

**Metodologista**:
- Valida lógica e detecta `contradictions`
- Pode identificar `open_questions` relacionadas a rigor científico
- Sugere refinamentos que podem atualizar `premises` ou `assumptions`

**Pesquisador** (futuro):
- Preenche `solid_grounds` após busca bibliográfica
- Pode validar `assumptions` transformando-as em `premises`
- Pode identificar novas `open_questions` baseadas em lacunas da literatura

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
- Usuário aprova → Estruturador organiza `premises` e estrutura argumento

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
   - Compara `claim` com `premises` e `assumptions`
   - Identifica tensões lógicas
   - Calcula confiança (0-1)

2. **Se confidence > 80%**:
   - Sistema menciona contradição de forma natural
   - Não bloqueia ou impõe
   - Apenas provoca reflexão

3. **Formato da menção**:
   - Conversacional, não acusatório
   - Exemplo: "Notei que você mencionou aumento de produtividade mas também aumento de bugs. Como você vê essa relação? São métricas separadas ou produtividade inclui qualidade?"

### Exemplo de Contradição Detectada

```python
# Estado atual
claim: "Claude Code aumenta produtividade em 30%"
premises: ["Produtividade é medida por tempo de sprint"]
assumptions: ["Qualidade não é afetada"]

# Metodologista detecta
contradictions: [
  {
    "description": "Usuário mencionou aumento de produtividade mas também aumento de bugs em turno anterior",
    "confidence": 0.85,
    "suggested_resolution": "Produtividade pode incluir qualidade? Ou são métricas separadas?"
  }
]

# Sistema menciona (não bloqueia)
"Notei que você mencionou aumento de produtividade mas também aumento de bugs. Como você vê essa relação?"
```

## Objetivo Final: "Flecha Penetrante"

O objetivo do sistema é ajudar o usuário a construir um **argumento sólido com respaldo bibliográfico**, sem premissas frágeis, sem dúvidas não examinadas. A clareza emerge da elaboração.

### Características do Argumento Maduro

- **`claim` estável e específico**: Não muda radicalmente a cada turno
- **`premises` sólidas**: Fundamentos claros e verificáveis
- **`assumptions` baixas**: Poucas hipóteses não verificadas
- **`open_questions` respondidas**: Lacunas foram exploradas
- **`contradictions` resolvidas**: Tensões foram endereçadas
- **`solid_grounds` presente**: Evidência bibliográfica encontrada

### Exemplo de Argumento Maduro

```python
claim: "Claude Code reduz tempo de sprint em 30% (de 2h para 1.4h) em equipes Python de 2-5 devs, sem comprometer qualidade do código (medida por bugs por sprint)"

premises: [
  "Equipes Python de 2-5 devs existem e são representativas",
  "Tempo de sprint é métrica válida de produtividade",
  "Bugs por sprint é métrica válida de qualidade",
  "Redução de tempo não compromete qualidade (validado por dados do usuário)"
]

assumptions: [
  "Resultado é generalizável para outras linguagens (hipótese a testar)"
]

open_questions: []  # Todas respondidas

contradictions: []  # Nenhuma detectada

solid_grounds: [
  {
    "claim": "Ferramentas de IA aumentam produtividade em desenvolvimento",
    "evidence": "Smith et al. (2023) encontraram redução de 25-40% em tempo de tarefa",
    "source": "doi:10.1234/example"
  },
  {
    "claim": "Qualidade não é comprometida quando ferramentas são usadas corretamente",
    "evidence": "Meta-análise de 15 estudos mostra correlação positiva entre uso de IA e qualidade",
    "source": "doi:10.5678/example"
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
2. **`premises` sólidas**: Fundamentos claros e verificáveis
3. **`assumptions` baixas**: Poucas hipóteses não verificadas (< 2)
4. **`open_questions` respondidas**: Lista vazia ou apenas questões secundárias
5. **`contradictions` resolvidas**: Nenhuma contradição detectada
6. **`solid_grounds` presente**: Evidência bibliográfica encontrada (quando aplicável)

### Como Sistema Usa Indicadores

Sistema não diz: "Seu argumento está maduro!"  
Sistema sugere: "Quer validar rigor científico com o Metodologista?" ou "Temos uma boa base. Quer que eu chame o Escritor para compilar o artigo?"

**Exemplo de sugestão baseada em maturidade**:
```python
# Sistema detecta maturidade
claim_stable: True
premises_solid: True
assumptions_low: True
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
premises: []
assumptions: [
  "Levantamento de obra é um problema relevante",
  "IA pode ajudar em levantamento de obra",
  "Há contribuição acadêmica possível"
]
open_questions: [
  "O que é levantamento de obra?",
  "Como IA pode ajudar?",
  "Qual é o problema específico?",
  "Qual tipo de artigo? (empírico, revisão, teórico)"
]
contradictions: []
solid_grounds: []
context: {
  "domain": "construction",
  "technology": "AI (unclear which)",
  "population": "not specified",
  "article_type": "unclear"
}
```

**Ação do sistema**: Orquestrador explora contexto
- "Interessante! Me conta mais: o que é levantamento de obra para você? E como você imagina que IA pode ajudar?"

### Turno 3: Claim Muda, Premises Adicionadas, Sistema Provoca

**Input do usuário**: "Levantamento de obra é medir quantidades de materiais. Quero usar visão computacional para automatizar"

**Estado cognitivo**:
```python
claim: "Usar visão computacional para automatizar levantamento de quantidades de materiais em obras"
premises: [
  "Levantamento de obra envolve medir quantidades de materiais",
  "Visão computacional pode identificar materiais em imagens",
  "Automatização é desejável"
]
assumptions: [
  "Visão computacional é precisa o suficiente para quantificar materiais",
  "Automatização reduz tempo/custo sem comprometer precisão",
  "Há contribuição acadêmica (não é apenas aplicação direta)"
]
open_questions: [
  "Qual é a precisão atual de métodos manuais?",
  "Qual é o baseline de tempo/custo?",
  "Como validar precisão da IA?",
  "Qual tipo de materiais? (tijolos, concreto, etc.)"
]
contradictions: []
solid_grounds: []
context: {
  "domain": "construction, quantity surveying",
  "technology": "computer vision, AI",
  "population": "not specified",
  "article_type": "unclear"  # Pode ser empírico (testar) ou metodológico (validar método)
}
```

**Ação do sistema**: Orquestrador provoca reflexão
- "Você mencionou automatização, mas e a PRECISÃO? Como você validaria que a IA é tão precisa quanto métodos manuais?"

### Turno 5: Pesquisador Busca, Solid_Grounds Adicionadas, Modelo Amadurece

**Input do usuário**: "Quero testar se visão computacional é mais rápida e precisa que métodos manuais"

**Estado cognitivo** (após Pesquisador buscar literatura):
```python
claim: "Visão computacional é mais rápida e precisa que métodos manuais para levantamento de quantidades de materiais em obras"
premises: [
  "Levantamento de obra envolve medir quantidades de materiais",
  "Visão computacional pode identificar materiais em imagens",
  "Métodos manuais existem e têm precisão conhecida",
  "Comparação de métodos é válida academicamente"
]
assumptions: [
  "Resultado é generalizável para diferentes tipos de obras",
  "Precisão da IA é suficiente para uso prático"
]
open_questions: [
  "Qual é o tamanho da amostra necessária?",
  "Como definir 'mais preciso'? (margem de erro aceitável?)",
  "Quais tipos de materiais testar? (tijolos, concreto, aço?)"
]
contradictions: []
solid_grounds: [
  {
    "claim": "Visão computacional tem sido usada em construção",
    "evidence": "Zhang et al. (2022) aplicaram YOLO para detecção de materiais com 85% de precisão",
    "source": "doi:10.1234/construction-ai"
  },
  {
    "claim": "Métodos manuais têm margem de erro de 5-10%",
    "evidence": "Revisão sistemática de 20 estudos mostra erro médio de 7.5% em levantamentos manuais",
    "source": "doi:10.5678/manual-survey"
  }
]
context: {
  "domain": "construction, quantity surveying",
  "technology": "computer vision, YOLO, deep learning",
  "population": "construction projects (not specified: residential, commercial, etc.)",
  "metrics": "speed (time), accuracy (error margin)",
  "article_type": "empirical"  # Agora claro: quer testar hipótese
}
```

**Ação do sistema**: Orquestrador sugere próximo passo
- "Temos uma boa base! Encontrei estudos relevantes. Quer que eu chame o Metodologista para validar o desenho experimental dessa comparação?"

### Turno 7: Modelo Maduro, Pronto para Estruturação

**Estado cognitivo** (após Metodologista validar):
```python
claim: "Visão computacional (YOLO) é mais rápida (redução de 60% no tempo) e mais precisa (erro de 3% vs 7.5% manual) que métodos manuais para levantamento de quantidades de tijolos em obras residenciais"

premises: [
  "Levantamento de obra envolve medir quantidades de materiais",
  "Visão computacional (YOLO) pode identificar tijolos em imagens",
  "Métodos manuais têm erro médio de 7.5% (evidência bibliográfica)",
  "Comparação experimental é válida academicamente",
  "Obras residenciais são contexto representativo"
]

assumptions: [
  "Resultado é generalizável para outros materiais (hipótese futura)"
]

open_questions: []  # Todas respondidas

contradictions: []  # Nenhuma detectada

solid_grounds: [
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

**Ação do sistema**: Sugestão de maturidade
- "Hipótese validada! Temos todos os elementos. Quer que eu chame o Estruturador para organizar isso em uma questão de pesquisa estruturada, ou prefere começar a definir o desenho experimental?"

## Referências

- `vision.md`: Visão de produto, jornada do usuário, tipos de artigo
- `topic_argument_model.md`: Modelo de dados do argumento (será criado)
- `conversation_patterns.md`: Padrões de conversação e argumento focal

