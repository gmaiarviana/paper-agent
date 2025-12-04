# Modelo Cognitivo - Evolução do Pensamento

> **Nota:** Para conceitos fundamentais (artefatos, responsabilidades), consulte `docs/vision/cognitive_model/core.md`.

Este documento descreve **como** o modelo cognitivo evolui durante a conversa, incluindo processos de provocação, estruturação, detecção de contradições e persistência.

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

- `docs/vision/cognitive_model/core.md` - Conceitos fundamentais (artefatos, responsabilidades)
- `docs/vision/cognitive_model/examples.md` - Exemplos práticos de evolução
- `docs/architecture/snapshot_strategy.md` - Implementação técnica de snapshots
- `docs/vision/epistemology.md` - Base filosófica (proposições, solidez, evidências)

