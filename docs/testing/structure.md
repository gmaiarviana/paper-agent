# Testing Structure

## Estrutura de Pastas

```
paper-agent/
├── tests/                      # Testes automatizados (pytest)
│   ├── __init__.py
│   ├── unit/                   # Testes unitários (mocks)
│   │   ├── __init__.py
│   │   ├── test_cost_tracker.py
│   │   ├── test_methodologist_state.py
│   │   ├── test_graph_nodes.py
│   │   └── test_json_extraction.py
│   ├── integration/            # Testes de integração (API real)
│   │   ├── __init__.py
│   │   └── test_anthropic_connection.py
│   └── conftest.py             # Fixtures compartilhadas
│
├── scripts/                    # Validação manual (dev local)
│   ├── __init__.py
│   ├── health_checks/          # Sanidade de ambiente e configs
│   │   ├── validate_api.py
│   │   ├── validate_agent_config.py
│   │   ├── validate_runtime_config.py
│   │   └── validate_system_prompt.py
│   ├── state_introspection/    # Nós isolados e estados
│   │   ├── validate_state.py
│   │   ├── validate_graph.py
│   │   └── validate_ask_user.py
│   ├── flows/                  # Cenários completos (consomem API)
│   │   ├── validate_cli.py
│   │   ├── validate_multi_agent_flow.py
│   │   └── validate_refinement_loop.py
│   └── debug/                  # Diagnóstico ad hoc
│       └── debug_multi_agent.py
```

---

## Fixtures Compartilhadas

**Arquivo:** `tests/conftest.py`

### Fixtures Disponíveis:

#### `anthropic_client`
Cliente real da Anthropic API (para integration tests)
- Requer `ANTHROPIC_API_KEY` no ambiente
- Pula teste se chave não estiver configurada

#### `cost_logger`
Logger para rastrear custos em testes
- Acumula custos de chamadas
- Exibe log formatado: `[INFO] Test cost: $0.00123`

---

## Cost Tracking

### Unit Tests
- Testam `CostTracker` isolado
- Validam cálculos sem API

### Integration Tests
- Rastreiam custos reais
- Logs exibem custos por teste

### Scripts
- Sempre exibem custos formatados
- Ajudam a entender custos de operações

---

**Versão:** 2.1
**Data:** 13/11/2025
