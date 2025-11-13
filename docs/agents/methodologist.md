Methodologist Agent
===================

**Status:** Em desenvolvimento (Épicos 2 → 4)
**Versão:** 1.3
**Data:** 11/11/2025

## Resumo

Agente especializado em avaliar rigor científico de hipóteses. Implementado como agente autônomo usando LangGraph, capaz de:
- Fazer perguntas ao usuário para obter clarificações
- Tomar decisões com raciocínio explícito
- Avaliar hipóteses segundo critérios metodológicos (testabilidade, falseabilidade, especificidade)

## Implementação Atual

### Modo Colaborativo (Épico 4)

**Objetivo:** Metodologista como PARCEIRO que ajuda a construir, não apenas validar.

**3 Modos de operação:**

1. **approved:**
   - Hipótese testável, falseável, específica, operacionalizada
   - Estrutura científica sólida
   - Pronta para desenho experimental

2. **needs_refinement (NOVO):**
   - Ideia tem potencial científico
   - Falta especificidade (população, métricas, variáveis)
   - Pode ser melhorada com refinamento
   - Campo `improvements` lista gaps específicos

3. **rejected:**
   - Sem base científica (crença popular, impossível testar)
   - Vagueza extrema que refinamento não resolve
   - Usado apenas em casos extremos

**Quando usar cada modo:**

| Input | Modo | Razão |
|-------|------|-------|
| "Método X reduz tempo em 30% em equipes 2-5 devs" | approved | Testável, específico |
| "Método X é mais rápido" | needs_refinement | Potencial, falta população/métricas |
| "X é bom porque todo mundo sabe" | rejected | Apelo à crença, não-testável |

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
- **Localização:** `agents/methodologist.py:79`

### Nós do Grafo

#### 1. `analyze` (agents/methodologist.py:175)
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

#### 2. `ask_clarification` (agents/methodologist.py:255)
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

#### 3. `decide` (agents/methodologist.py:346)
**Responsabilidade:** Tomar decisão final sobre a hipótese

**Processo:**
1. Analisa toda informação coletada (hipótese + clarificações)
2. Avalia segundo critérios científicos:
   - Testabilidade
   - Falseabilidade
   - Especificidade
   - Operacionalização
3. Define status (approved/rejected)
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

**Exemplo de needs_refinement:**
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

### Knowledge Base

**Localização:** `agents/methodologist_knowledge.md`

**Conteúdo:**
- Diferença entre lei, teoria e hipótese
- Critérios de testabilidade e falseabilidade (Popper)
- Exemplos práticos de hipóteses boas vs ruins:
  - Cafeína e desempenho cognitivo
  - Música e crescimento de plantas

**Nota:** Knowledge base micro para MVP. Versão completa será implementada futuramente com tool `consult_methodology`.

### System Prompt

**Localização:** `utils/prompts.py`
**Constante:** `METHODOLOGIST_AGENT_SYSTEM_PROMPT_V1`

**Características:**
- Linguagem direta e concisa (265 palavras)
- Instruções explícitas sobre uso da tool `ask_user`
- Define output JSON: `{"status": "approved|rejected", "justification": "..."}`
- Critérios científicos claros: testabilidade, falseabilidade, especificidade, operacionalização
- Exemplos práticos de aprovação e rejeição

**Validação:** `scripts/health_checks/validate_system_prompt.py`

### Prompt Colaborativo (Épico 4)

**Localização:** `utils/prompts.py` - `METHODOLOGIST_AGENT_SYSTEM_PROMPT_V2`

**Instruções adicionadas:**
```
MODO COLABORATIVO (Épico 4):

Você é um PARCEIRO que ajuda a CONSTRUIR hipóteses, não apenas validar
Use "needs_refinement" quando a ideia tem potencial mas falta especificidade
Use "rejected" APENAS quando não há base científica (crença popular, impossível testar)
Campo "improvements": seja ESPECÍFICO sobre gaps e como preencher

DECISÃO DE STATUS:

approved: Testável + específico + operacionalizado
needs_refinement: Potencial + falta elementos (população, métricas, variáveis)
rejected: Sem base científica + impossível refinar

CAMPO "improvements" (needs_refinement):
[
{
"aspect": "população" | "métricas" | "variáveis" | "testabilidade",
"gap": "Descrição clara do que falta",
"suggestion": "Como preencher (exemplo concreto)"
}
]
EXEMPLOS:
Input: "Método X é melhor"
Output: {
"status": "needs_refinement",
"improvements": [
{"aspect": "métricas", "gap": "Melhor não mensurável", "suggestion": "Definir: reduz tempo em X%, aumenta qualidade em Y%"}
]
}
```

### Fluxo de Execução

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

### LLM Utilizado

**Modelo:** claude-3-5-haiku-20241022
**Justificativa:** Custo-efetivo para MVP, suficiente para análise metodológica e geração de JSON estruturado
**Temperature:** 0 (determinístico)

## Testes

### Testes Unitários
- **Estado:** `tests/unit/test_methodologist_state.py` (6/6)
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
- ✅ Integrado no loop de refinamento
- ✅ Decisão forçada após limite

**Futuras melhorias (pós-Épico 4):**
- Tool `consult_methodology` para knowledge base ampliada
- Sugestões de desenho experimental
- Validação de testes estatísticos

