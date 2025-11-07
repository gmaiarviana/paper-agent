Orchestrator Overview
=====================

Papel
-----
- Analisa input do usuário e decide entre responder diretamente ou delegar para um agente especializado.
- Mantém histórico da conversa em memória (via LangGraph) e registra cada decisão.
- Expõe método `decide(user_input: str) -> dict` que retorna:

```
{
  "action": "call_agent" | "respond_direct",
  "agent": "methodologist" | null,
  "message": "..."
}
```

Decisões
--------
- `respond_direct`: utilizado para saudações, conversas casuais ou perguntas fora do escopo científico.
- `call_agent`: utilizado para hipóteses ou solicitações que demandem avaliação metodológica. Ao escolher esta opção, o Orquestrador chama o agente correspondente e inclui a resposta formatada no retorno ao usuário.

Estado e LangGraph
------------------
- O estado da conversa está definido em `orchestrator/state.py` utilizando TypedDict.
- Campos principais:
  - `messages`: histórico completo trocado entre usuário, orquestrador e agentes
  - `current_agent`: nome do agente ativo (ou `None`)
  - `last_decision`: registro estruturado da decisão anterior
  - `metadata`: métricas auxiliares (tokens, duração, etc.)
- LangGraph é responsável por aplicar updates imutáveis ao estado, garantindo consistência.

Logs e Observabilidade
----------------------
- `INFO`: registra decisões tomadas e agentes acionados.
- `DEBUG`: inclui prompts completos e respostas brutas (ativado via flag `--verbose`).
- Estrutura JSON sugerida:

```
{
  "timestamp": "2025-11-06T10:30:00",
  "level": "INFO",
  "component": "orchestrator",
  "action": "decision",
  "data": {
    "input": "...",
    "decision": "call_agent",
    "agent": "methodologist"
  }
}
```

Tratamento de Erros
-------------------
- Sempre encapsule falhas de agentes e API em mensagens claras para a CLI.
- Utilize retry com backoff exponencial (3 tentativas) para conversas com a API.
- Se todas as tentativas falharem, registre em `ERROR` e retorne instruções amigáveis ao usuário para tentar novamente.

Evolução Prevista
-----------------
- Futuras integrações com LangGraph (Épico 5) devem ser documentadas em `docs/langgraph/examples.md`.
- Novos agentes devem ser cadastrados aqui com regras de roteamento específicas.

