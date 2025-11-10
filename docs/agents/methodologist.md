Methodologist Agent
===================

**Status:** Em desenvolvimento (Épico 2)
**Versão:** 1.2
**Data:** 10/11/2025

## Resumo

Agente especializado em avaliar rigor científico de hipóteses. Implementado como agente autônomo usando LangGraph, capaz de:
- Fazer perguntas ao usuário para obter clarificações
- Tomar decisões com raciocínio explícito
- Avaliar hipóteses segundo critérios metodológicos (testabilidade, falseabilidade, especificidade)

## Implementação Atual

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

**Output:**
```python
{
    "status": "approved" | "rejected",
    "justification": str,  # Explicação detalhada
    "messages": [AIMessage]
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

## Pendências (Épico 2)

- [ ] **Task 2.5:** Construção do grafo (StateGraph + roteamento condicional)
- [ ] **Task 2.6:** System prompt versionado em `utils/prompts.py`
- [ ] **Task 2.7:** CLI para interação
- [ ] **Task 2.8:** Teste de fumaça end-to-end

## Testes

### Testes Unitários
- **Estado:** `tests/unit/test_methodologist_state.py` (6/6)
- **Tool ask_user:** `tests/unit/test_ask_user_tool.py` (10/10)
- **Nós do grafo:** `tests/unit/test_graph_nodes.py` (16/16)

### Scripts de Validação Manual
- `scripts/validate_state.py`: Valida estado e checkpointer
- `scripts/validate_ask_user.py`: Valida tool ask_user
- `scripts/validate_graph_nodes.py`: Valida nós do grafo

## Futuras Melhorias (Pós-MVP)

- Tool `consult_methodology` para busca em knowledge base ampliada
- Knowledge base completa (10+ páginas)
- Nó `consult_knowledge` para interpretar knowledge base
- Métricas: tempo de resposta, tokens consumidos
- Logs estruturados em JSON
- Retry logic para falhas de API

