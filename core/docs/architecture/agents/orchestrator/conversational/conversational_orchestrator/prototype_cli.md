# Protótipo: CLI Conversacional (Épico 7.5-7.7)

## Mudanças Implementadas

**POC → Protótipo:**
- ✅ POC: Backend conversacional implementado (Orquestrador analisa contexto)
- ✅ Protótipo: Frontend conversacional (CLI com múltiplos turnos)

## CLI Conversacional (7.5)

**Problema resolvido:** CLI do POC não mantinha conversa - voltava para "Digite sua hipótese" após cada resposta.

**Solução:**
- Loop conversacional contínuo
- Thread ID preservado ao longo da sessão
- Contexto acumulado via `conversation_history`

**Fluxo implementado:**
```
Sistema: Olá! Me conte sobre sua ideia.
Você: tdd reduz bugs
Sistema: Em que contexto?
Você: equipe Python
Sistema: Como mediu?
Você: impressão geral
Sistema: Vou organizar isso em uma questão de pesquisa.
[chama Estruturador automaticamente...]
Sistema: Organizei assim: "TDD reduz bugs?" Isso captura o que você quer?
```

**Código:**
```python
thread_id = f"cli-session-{uuid.uuid4()}"
while True:
    user_input = input("Você: ")
    result = graph.invoke(
        {"user_input": user_input},
        config={"configurable": {"thread_id": thread_id}}
    )
    print(f"Sistema: {result['orchestrator_output']['message']}")
```

## Detecção Inteligente (7.6)

**Abordagem não-determinística:**
- LLM julga "momento certo" baseado em contexto
- Não usa checklist rígida de campos obrigatórios
- Considera qualidade e quantidade de informação

**Prompt do Orquestrador (atualizado):**
```
Analise o histórico completo. Você tem CONTEXTO SUFICIENTE para sugerir
agente quando:

- Conversa acumulou detalhes relevantes
- Chamar agente agregaria valor real
- Não precisa estar perfeito, apenas útil

Use julgamento contextual, não protocolo fixo.

Se contexto suficiente:
  next_step = "suggest_agent"
  agent_suggestion = {"agent": "nome", "justification": "..."}

Se precisa mais info:
  next_step = "explore"
  message = "Pergunta esclarecedora específica"
```

**Output esperado:**
```json
{
  "reasoning": "Análise do contexto acumulado...",
  "next_step": "call_agent",
  "message": "Organizei sua ideia em uma questão estruturada: [resultado curado]. Isso captura o que você quer explorar?",
  "agent_call": {
    "agent": "structurer",
    "justification": "Usuário tem observação + contexto, falta estruturação"
  }
}
```

**Nota:** `next_step: "call_agent"` significa chamar automaticamente. `message` é resultado curado, não pergunta de permissão.

## Transparência do Raciocínio (7.7)

**3 níveis implementados:**

1. **CLI Padrão** (limpo): Apenas mensagem
2. **CLI Verbose** (`--verbose`): Mensagem + reasoning inline
3. **Dashboard** (sempre): Timeline com reasoning completo

**Implementação:**
```python
# CLI
if args.verbose:
    print(f"🧠 {orchestrator_output['reasoning']}")
print(f"Sistema: {orchestrator_output['message']}")

# EventBus
event_bus.publish_agent_completed(
    session_id=thread_id,
    agent="orchestrator",
    summary=orchestrator_output['message'],
    metadata={"reasoning": orchestrator_output['reasoning']}
)
```

**Benefícios:**
- CLI mantém experiência limpa por padrão
- Reasoning disponível sob demanda (verbose)
- Dashboard sempre mostra transparência completa
- Usa infraestrutura existente (Épico 5)

## Diferenças POC → Protótipo

| Aspecto | POC | Protótipo |
|---------|-----|-----------|
| **CLI** | Loop único | Chat contínuo |
| **Contexto** | Não preservado | Preservado via thread_id |
| **Turnos** | 1 (input → fim) | N (conversa fluida) |
| **Detecção** | Básica | Inteligente (LLM julga) |
| **Transparência** | Apenas logs | 3 níveis (CLI/verbose/dashboard) |
| **Experiência** | Quebrada | Fluida e natural |

## Próximos Passos (MVP)

- 7.8: Argumento Focal Explícito (campo no state)
- 7.9: Provocação de Reflexão (versão simples)
- 7.10: Detecção Emergente de Estágio

**Nota:** Funcionalidades 7.12-7.14 foram movidas para outros épicos:
- 7.12: Reasoning Explícito das Decisões → Épico 9.6/9.7 (Interface Web)
- 7.13: Histórico de Decisões → Épico 10.7 (Persistência)
- 7.14: Argumento Focal Persistente → Épico 10.2 (Persistência)

**Especificação técnica completa:** `docs/core/tools/conversational_cli.md`

---

**Próximas seções:**
- [Visão Geral](./overview.md) - Status e dependências
- [Progressão](./progression.md) - Evolução completa

