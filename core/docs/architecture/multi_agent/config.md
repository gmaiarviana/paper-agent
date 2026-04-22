# Configuração de Agentes (Épico 6)

## Arquivos `config/agents/<papel>.yaml`

Um arquivo por agente, carregado no boot.

**Campos obrigatórios:**
- `name` (str): rótulo exibido na interface.
- `role` (str): identificador interno (`methodologist`, `structurer`, ...).
- `model` (str): id do modelo LLM.
- `prompt` (str): prompt base (texto multilinha).
- `tags` (list[str]): etiquetas para filtros/telemetria.
- `context_limit` (int): tokens máximos permitidos por chamada.
- `memory_window` (int): quantidade de eventos recentes preservados (`>=1`).
- `tools` (list[str]): nomes das ferramentas habilitadas (pode ser vazio).

**Campos opcionais:**
- `temperature` (float) e `top_p` (float) com defaults globais.
- `summary_template` (str) para personalizar resumo apresentado na interface.

**Validação ocorre na inicialização:**
- Mensagens de erro em PT-BR com caminho do arquivo e campo inválido.
- Falha aborta a execução antes de instanciar o grafo.

**Exemplo:**

```yaml
name: Metodologista
role: methodologist
model: gpt-4o-mini
prompt: |
  Você é o agente metodologista responsável por avaliar hipóteses...
tags:
  - core
  - validation
context_limit: 4096
memory_window: 5
tools:
  - ask_user
temperature: 0.2
```

---

## Histórico em Memória

- `MultiAgentState` passa a expor `agent_memory: dict[str, deque]`.
- Cada item mantém `event_id`, `timestamp`, `summary`, `tokens_input`, `tokens_output`, `tokens_total`.
- Tamanho do buffer por agente controlado por `memory_window` (default 5).
- Após cada evento, CLI persiste snapshot em `runtime/snapshots/<session_id>.json`:
  ```json
  {
    "session_id": "cli-session-123",
    "updated_at": "2025-11-12T10:35:30.000Z",
    "agents": {
      "methodologist": [
        {"event_id": "evt-0003", "summary": "...", "tokens_total": 728}
      ]
    }
  }
  ```
- Streamlit consome snapshots para métricas agregadas sem reprocessar todo o JSONL.

---

## Reset Global de Sessão

- CLI ganhará flag `--reset-session <session_id>` (ou menu interativo) que limpa `agent_memory`, snapshots e stream associado.
- Reset mantém o histórico já emitido na interface; apenas o estado ativo é limpo.
- Reset individual por agente fica registrado no backlog.

---

## Identificadores

- `session_id`: reaproveita o `thread_id` (`cli-session-<uuid>`).
- `event_id`: contador incremental por sessão (`evt-0001`, `evt-0002`...), gerenciado pelo orquestrador.
- Abordagem evita colisões e funciona com execuções concorrentes sem configuração extra.

---

## Referências

- **Estado completo:** [state.md](state.md)
- **Implementação dos nós:** [nodes.md](nodes.md)

