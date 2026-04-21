# Metodologista - Agente de Validação Lógica

**Status:** Em desenvolvimento (Épicos 2 → 4)  
**Versão:** 1.4  
**Data:** 13/11/2025

## Visão Geral
Agente especializado em avaliar **coerência lógica** de hipóteses e argumentos, independente do domínio. Valida solidez de fundamentos, identifica contradições e aponta lacunas no raciocínio.

**Contexto agnóstico:** Funciona tanto para hipóteses científicas quanto para hipóteses de negócio, postagens, decisões pessoais.

## Responsabilidades
- Avaliar coerência lógica (proposições não se contradizem?)
- Validar solidez de fundamentos (têm base?)
- Identificar contradições entre proposições
- Apontar lacunas no raciocínio (open questions)
- Sugerir fortalecimento de fundamentos frágeis
- **Adaptar rigor ao contexto** (científico vs negócio vs pessoal)

## Modo de Operação
Opera em modo **colaborativo**:
- `approved`: Argumentação sólida e coerente
- `needs_refinement`: Lacunas identificadas, sugere melhorias
- `rejected`: Contradição lógica fundamental

**Importante:** Metodologista não impõe formato acadêmico. Valida **lógica**, não **estilo**.

**⚠️ NOTA IMPORTANTE:** O Metodologista é chamado **automaticamente** pelo Orquestrador quando o contexto é suficiente para validação metodológica. O Orquestrador faz curadoria do resultado e apresenta ao usuário em tom coeso, sem necessidade de negociação prévia.

## Implementação Atual

### Modo Colaborativo (Épico 4)

**Objetivo:** Metodologista como PARCEIRO que ajuda a construir, não apenas validar.

**3 Modos de operação:**

1. **approved:**
   - Argumentação sólida e coerente
   - Fundamentos bem estabelecidos
   - Lógica consistente (sem contradições)
   - Contexto-adequado: rigor científico para pesquisa, pragmático para negócio/pessoal

2. **needs_refinement (NOVO):**
   - Ideia tem potencial mas falta clareza
   - Lacunas identificadas (proposições não explícitas, variáveis indefinidas)
   - Pode ser melhorada com refinamento
   - Campo `improvements` lista gaps específicos

3. **rejected:**
   - Contradição lógica fundamental
   - Fundamentos completamente ausentes
   - Impossível refinar (não há base para trabalhar)
   - Usado apenas em casos extremos

**Quando usar cada modo:**

| Input | Contexto | Modo | Razão |
|-------|----------|------|-------|
| "Método X reduz tempo em 30% em equipes 2-5 devs" | Negócio/Tech | approved | Testável, específico, fundamentado |
| "Vou mudar de carreira porque não me sinto realizado" | Pessoal | needs_refinement | Potencial, falta definir "realizado" e evidências |
| "Método X é mais rápido" | Negócio | needs_refinement | Potencial, falta população/métricas |
| "X é bom porque todo mundo sabe" | Qualquer | rejected | Apelo à crença, não-testável, sem fundamento |

### Estado (MethodologistState)

TypedDict gerenciado pelo LangGraph com os seguintes campos:

- `hypothesis` (str): Hipótese a ser avaliada
- `messages` (Annotated[list, add_messages]): Histórico de mensagens do grafo
- `clarifications` (dict[str, str]): Perguntas e respostas coletadas
- `status` (Literal["pending", "approved", "rejected"]): Status da análise
- `iterations` (int): Contador de perguntas feitas
- `max_iterations` (int): Limite de perguntas (padrão: 3)
- `justification` (str): Justificativa da decisão final
- `needs_clarification` (bool): Flag de controle de fluxo

**Checkpointer:** MemorySaver para persistência de sessão em memória

### Tools Implementadas

#### `ask_user(question: str) -> str`
- Permite agente fazer perguntas ao usuário
- Usa `interrupt()` do LangGraph para pausar execução
- Logging estruturado de perguntas e respostas
- **Localização:** `agents/methodologist/tools.py:18`

### Tools Planejadas (Futuro)

#### `validate_paper_methodology(paper_id: str, paper_content: dict) -> dict`

Valida qualidade metodológica de paper encontrado pelo Pesquisador (nível 2 da curadoria).

**Input:**
```python
{
  "paper_id": "paper-123",
  "title": "Impact of AI Tools on Development Productivity",
  "authors": ["Smith, J.", "Doe, A."],
  "abstract": "...",
  "methodology_section": "...",  # Extraído do paper
  "sample_size": 100,
  "study_design": "experimental"
}
```

**Output:**
```python
{
  "methodology_quality": "alta" | "média" | "baixa",
  "peer_review": true | false,
  "sample_adequacy": {
    "size": 100,
    "adequacy": "adequada" | "pequena" | "insuficiente",
    "justification": "Amostra suficiente para generalização..."
  },
  "methodology_description": {
    "clarity": "clara" | "parcial" | "vaga",
    "justification": "Metodologia descrita detalhadamente..."
  },
  "statistical_analysis": {
    "appropriate": true | false,
    "justification": "Testes estatísticos adequados..."
  },
  "recommendation": "avançar" | "avisar_limitações" | "descartar",
  "justification": "Paper tem metodologia robusta...",
  "limitations": ["Amostra limitada a equipes Python", "Contexto específico..."]
}
```

**Critérios de validação:**
1. **Peer review:** Paper passou por revisão por pares?
2. **Metodologia descrita:** Método está claro e replicável?
3. **Amostragem:** Tamanho adequado para generalização?
4. **Análise estatística:** Testes apropriados foram usados?
5. **Vieses identificados:** Autores reconhecem limitações?

**Decisão de qualidade:**
- **Alta:** Todos os critérios satisfeitos → avançar para nível 3
- **Média:** Maioria satisfeita, algumas limitações → avisar usuário, perguntar se avança
- **Baixa:** Critérios críticos não satisfeitos → descartar

#### `check_peer_review(paper_id: str, source: str) -> dict`

Verifica se paper passou por peer review consultando metadados da fonte.

**Input:**
```python
{
  "paper_id": "paper-123",
  "source": "Google Scholar" | "PubMed" | "ArXiv"
}
```

**Output:**
```python
{
  "peer_reviewed": true | false,
  "journal": "Journal of Software Engineering",
  "impact_factor": 3.5,  # Se disponível
  "justification": "Publicado em journal peer-reviewed com IF 3.5"
}
```

#### `compare_methodologies(paper_ids: list[str]) -> dict`

Compara metodologias de múltiplos papers para identificar padrões e discrepâncias.

**Input:**
```python
{
  "paper_ids": ["paper-123", "paper-456", "paper-789"],
  "aspect": "sample_size" | "study_design" | "statistical_test"
}
```

**Output:**
```python
{
  "comparison": [
    {
      "paper_id": "paper-123",
      "sample_size": 100,
      "study_design": "experimental"
    },
    {
      "paper_id": "paper-456",
      "sample_size": 20,  # ⚠️ Discrepância
      "study_design": "observational"  # ⚠️ Diferente
    }
  ],
  "patterns": "Maioria usa design experimental",
  "discrepancies": ["Paper-456 tem amostra significativamente menor"],
  "recommendation": "Dar mais peso a papers com amostra > 50"
}
```

### Integração com Pesquisador

**Fluxo de chamada:**
```
Pesquisador (nível 2 da curadoria):
  ↓
  "Valide este paper antes de processar"
  ↓
Metodologista:
  validate_paper_methodology(paper_id, paper_content)
  ↓
  {
    "methodology_quality": "alta",
    "recommendation": "avançar",
    "limitations": [...]
  }
  ↓
Pesquisador:
  [decide se paper avança para nível 3 - Prisma]
```

**Responsabilidade clara:**
- Metodologista valida QUALIDADE do paper (metodologia científica)
- Pesquisador decide SE e QUANDO acionar Metodologista
- Prisma extrai PROPOSIÇÕES do paper (após validação)

### Nós do Grafo

#### 1. `analyze` (agents/methodologist/nodes.py:38)
**Responsabilidade:** Avaliar hipótese e decidir se precisa de clarificações

**Processo:**
1. Analisa hipótese fornecida
2. Considera clarificações já coletadas
3. Usa LLM (claude-3-5-haiku-20241022) para decidir se tem informação suficiente
4. Atualiza `needs_clarification` para controlar fluxo

**Output:**
```python
{
    "messages": [AIMessage],  # Análise do LLM
    "needs_clarification": bool  # True se precisa de mais info
}
```

#### 2. `ask_clarification` (agents/methodologist/nodes.py:119)
**Responsabilidade:** Solicitar clarificação ao usuário

**Processo:**
1. Verifica se atingiu `max_iterations`
2. Usa LLM para formular pergunta específica sobre aspectos metodológicos
3. Chama `ask_user()` para obter resposta
4. Registra em `clarifications`
5. Incrementa `iterations`

**Output:**
```python
{
    "clarifications": dict,  # Pergunta/resposta adicionada
    "iterations": int,  # Contador incrementado
    "messages": [AIMessage, HumanMessage]
}
```

#### 3. `decide` (agents/methodologist/nodes.py:215)
**Responsabilidade:** Tomar decisão final sobre a hipótese

**Processo:**
1. Analisa toda informação coletada (hipótese + clarificações)
2. Avalia segundo critérios lógicos (adaptados ao contexto):
   - Coerência lógica (proposições não se contradizem?)
   - Solidez de fundamentos (têm base?)
   - Especificidade adequada ao contexto (científico: rigoroso; negócio: pragmático; pessoal: claro)
   - Operacionalização quando aplicável (testável para pesquisa/negócio)
3. Define status (approved/needs_refinement/rejected)
4. Gera justificativa detalhada

### Output (atualizado - Épico 4)

**Estrutura:**
```python
{
    "status": "approved" | "needs_refinement" | "rejected",
    "justification": str,
    "improvements": [  # NOVO - apenas se needs_refinement
        {
            "aspect": "população" | "métricas" | "variáveis" | "testabilidade",
            "gap": str,
            "suggestion": str
        }
    ],
    "clarifications": dict  # Mantido do Épico 2
}
```

**Exemplos de needs_refinement:**

**Contexto científico:**
```python
{
    "status": "needs_refinement",
    "justification": "Ideia central clara (método incremental impacta velocidade), mas falta operacionalização para teste empírico.",
    "improvements": [
        {
            "aspect": "população",
            "gap": "Não especificada",
            "suggestion": "Definir população-alvo (ex: equipes de 2-5 desenvolvedores com experiência em LangGraph)"
        },
        {
            "aspect": "métricas",
            "gap": "Velocidade não mensurável",
            "suggestion": "Operacionalizar velocidade (ex: tempo por sprint, bugs por deploy, taxa de retrabalho)"
        }
    ],
    "clarifications": {}
}
```

**Contexto negócio:**
```python
{
    "status": "needs_refinement",
    "justification": "Hipótese de que mudança de preço aumenta receita tem potencial, mas falta definir variáveis-chave.",
    "improvements": [
        {
            "aspect": "variáveis",
            "gap": "Não especificado quanto aumentar preço nem segmento-alvo",
            "suggestion": "Definir: aumento de 10% em produtos premium, mantendo produtos básicos"
        },
        {
            "aspect": "fundamentos",
            "gap": "Falta evidência de elasticidade de demanda",
            "suggestion": "Verificar dados históricos ou pesquisa de mercado sobre sensibilidade a preço"
        }
    ],
    "clarifications": {}
}
```

**Contexto pessoal:**
```python
{
    "status": "needs_refinement",
    "justification": "Decisão de mudar de carreira tem base emocional válida, mas falta clareza sobre critérios de sucesso.",
    "improvements": [
        {
            "aspect": "variáveis",
            "gap": "'Realização' não está definida",
            "suggestion": "Especificar: o que significa realização para você? (autonomia, impacto, criatividade?)"
        },
        {
            "aspect": "fundamentos",
            "gap": "Falta evidência de que nova carreira atenderá critérios",
            "suggestion": "Conversar com profissionais da área, fazer projeto piloto (freelance, voluntariado)"
        }
    ],
    "clarifications": {}
}
```

### Knowledge Base

**Localização:** `core/docs/agents/methodologist/knowledge.md`

**Conteúdo:**
- Diferença entre lei, teoria e hipótese
- Critérios de testabilidade e falseabilidade (Popper)
- Princípios de coerência lógica e solidez de fundamentos
- Exemplos práticos de hipóteses boas vs ruins em diferentes contextos:
  - **Científico:** Cafeína e desempenho cognitivo; Música e crescimento de plantas
  - **Negócio:** Mudança de preço e receita; Automação e produtividade
  - **Pessoal:** Mudança de carreira e realização; Relacionamento e felicidade

**Nota:** Knowledge base micro para MVP. Versão completa será implementada futuramente com tool `consult_methodology`.

### System Prompt

**Localização:** `utils/prompts/methodologist.py`
**Constante:** `METHODOLOGIST_AGENT_SYSTEM_PROMPT_V1`

**Características:**
- Linguagem direta e concisa (265 palavras)
- Instruções explícitas sobre uso da tool `ask_user`
- Define output JSON: `{"status": "approved|needs_refinement|rejected", "justification": "..."}`
- Critérios lógicos adaptáveis ao contexto: coerência, solidez de fundamentos, especificidade adequada
- Exemplos práticos de aprovação, refinamento e rejeição em diferentes contextos

**Validação:** `scripts/health_checks/validate_system_prompt.py`

### Prompt Colaborativo (Épico 4)

**Localização:** `utils/prompts/methodologist.py` - `METHODOLOGIST_DECIDE_PROMPT_V2`

**Instruções adicionadas:**
```
MODO COLABORATIVO (Épico 4):

Você é um PARCEIRO que ajuda a CONSTRUIR hipóteses, não apenas validar
Use "needs_refinement" quando a ideia tem potencial mas falta especificidade
Use "rejected" APENAS quando não há base científica (crença popular, impossível testar)
Campo "improvements": seja ESPECÍFICO sobre gaps e como preencher

DECISÃO DE STATUS:

approved: Coerente + fundamentado + específico (adequado ao contexto)
needs_refinement: Potencial + falta elementos (proposições, variáveis, evidências)
rejected: Contradição lógica fundamental + impossível refinar

ADAPTE RIGOR AO CONTEXTO:
- Científico: rigor metodológico, testabilidade, falseabilidade
- Negócio: pragmático, métricas mensuráveis, viabilidade
- Pessoal: clareza de critérios, evidências subjetivas válidas

CAMPO "improvements" (needs_refinement):
[
{
"aspect": "população" | "métricas" | "variáveis" | "testabilidade" | "fundamentos" | "coerência",
"gap": "Descrição clara do que falta",
"suggestion": "Como preencher (exemplo concreto)"
}
]
EXEMPLOS:
Input: "Método X é melhor" (negócio)
Output: {
"status": "needs_refinement",
"improvements": [
{"aspect": "métricas", "gap": "Melhor não mensurável", "suggestion": "Definir: reduz tempo em X%, aumenta qualidade em Y%"}
]
}

Input: "Vou mudar de carreira porque não me sinto realizado" (pessoal)
Output: {
"status": "needs_refinement",
"improvements": [
{"aspect": "variáveis", "gap": "'Realizado' não definido", "suggestion": "Especificar critérios: autonomia? impacto? criatividade?"},
{"aspect": "fundamentos", "gap": "Falta evidência de que nova carreira atenderá", "suggestion": "Conversar com profissionais, fazer projeto piloto"}
]
}
```

### Fluxo de Execução (Interno do Metodologista)

```
┌─────────────┐
│   START     │
└─────┬───────┘
      │
      ▼
┌─────────────┐     needs_clarification=true    ┌──────────────────┐
│   analyze   │────────────────────────────────▶│ ask_clarification│
└─────┬───────┘                                 └────────┬─────────┘
      │                                                  │
      │ needs_clarification=false                        │
      │                 ◀────────────────────────────────┘
      │                      (loop até max_iterations)
      ▼
┌─────────────┐
│   decide    │
└─────┬───────┘
      │
      ▼
┌─────────────┐
│     END     │
└─────────────┘
```

### Uso no Fluxo Multi-Agente (Transição Fluida)

**⚠️ IMPORTANTE:** O Metodologista é chamado automaticamente pelo Orquestrador
quando o contexto é suficiente para validação metodológica. O Orquestrador
faz curadoria do resultado e apresenta ao usuário em tom coeso.

**Fluxo:**

1. Orquestrador detecta contexto suficiente (hipótese estruturada)
2. Metodologista é chamado automaticamente (bastidores)
3. Metodologista valida: approved | needs_refinement | rejected
4. Orquestrador recebe resultado e faz curadoria
5. Orquestrador apresenta: "Validei sua hipótese: [resultado]. Faz sentido?"

**Exemplos completos:**

**Contexto científico:**
```
Orquestrador: "Validei sua hipótese. Ela atende critérios de testabilidade
              e falseabilidade. Identifiquei que falta definir baseline.
              Isso faz sentido para você?"
[Bastidores: 🔬 Metodologista validou → 🎯 Orquestrador curou]
↓
Usuário: "Faz sentido, mas como definir baseline?"
↓
Orquestrador: "Podemos usar métricas históricas da equipe ou benchmark
              da literatura. Qual prefere?"
```

**Contexto negócio:**
```
Orquestrador: "Analisei sua ideia de aumentar preços. A lógica é sólida,
              mas falta definir quanto aumentar e em quais produtos.
              Quer refinar isso?"
[Bastidores: 🔬 Metodologista validou → 🎯 Orquestrador curou]
↓
Usuário: "Sim, como faço?"
↓
Orquestrador: "Podemos começar definindo segmento (premium vs básico)
              e percentual de aumento. Qual faz mais sentido para seu negócio?"
```

**Contexto pessoal:**
```
Orquestrador: "Entendi sua decisão de mudar de carreira. A motivação
              está clara, mas falta definir o que 'realização' significa
              para você. Quer explorar isso?"
[Bastidores: 🔬 Metodologista validou → 🎯 Orquestrador curou]
↓
Usuário: "Como?"
↓
Orquestrador: "Podemos listar critérios: autonomia, impacto social,
              criatividade, estabilidade. Quais são mais importantes para você?"
```

**Princípios:**
- ✅ Metodologista trabalha **automaticamente** quando contexto suficiente
- ✅ Refinamento é **automático** quando necessário
- ✅ Orquestrador **cura resposta final** (tom unificado)
- ✅ Transparência nos **bastidores** (usuário pode ver quem trabalhou)
- ✅ Usuário pode **mudar de direção** a qualquer momento

### LLM Utilizado

**Modelo:** claude-3-5-haiku-20241022
**Justificativa:** Custo-efetivo para MVP, suficiente para análise metodológica e geração de JSON estruturado
**Temperature:** 0 (determinístico)

## Testes

### Testes Unitários
- **Estado:** `tests/unit/test_methodologist_state.py` (4/4)
- **Tool ask_user:** `tests/unit/test_ask_user_tool.py` (10/10)
- **Nós do grafo:** `tests/unit/test_graph_nodes.py` (16/16)

### Scripts de Validação Manual
- `scripts/state_introspection/validate_state.py`: Valida estado e checkpointer
- `scripts/state_introspection/validate_ask_user.py`: Valida tool ask_user
- `scripts/state_introspection/validate_graph_nodes.py`: Valida nós do grafo

## Evolução (Épicos 2 → 4)

**Épico 2:** Metodologista validador
- ✅ Analisa hipótese
- ✅ Faz perguntas (ask_user)
- ✅ Decide: approved/rejected

**Épico 4:** Metodologista colaborativo
- ✅ Modo "needs_refinement" (novo)
- ✅ Campo "improvements" com gaps específicos
- ✅ Integrado no fluxo conversacional (não automático)
- ⚠️ **Refinamento sob demanda** (usuário decide quando refinar)
- ❌ Decisão forçada removida (usuário controla iterações)

**Futuras melhorias (pós-Épico 4):**
- Tool `consult_methodology` para knowledge base ampliada
- Sugestões de desenho experimental
- Validação de testes estatísticos

