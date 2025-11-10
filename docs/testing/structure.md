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
│   ├── validate_api.py         # Health check manual
│   ├── validate_state.py
│   ├── validate_ask_user.py
│   └── validate_graph.py
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

**Versão:** 2.0
**Data:** 10/11/2025
