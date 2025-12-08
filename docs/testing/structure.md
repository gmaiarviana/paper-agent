# Testing Structure

## Estrutura de Pastas
```
paper-agent/
├── tests/
│   ├── unit/                       # Testes rápidos, sem API ($0)
│   │   ├── agents/                 # Lógica de agentes
│   │   │   ├── orchestrator/       # Testes do Orquestrador (modularizado)
│   │   │   │   ├── test_node.py
│   │   │   │   ├── test_router.py
│   │   │   │   ├── test_state.py
│   │   │   │   ├── test_context.py
│   │   │   │   ├── test_cognitive_model.py
│   │   │   │   └── test_integration.py
│   │   │   ├── test_structurer.py
│   │   │   ├── test_methodologist_*.py
│   │   │   └── ...
│   │   ├── models/                 # Estruturas de dados (1 arquivo)
│   │   │   └── test_cognitive_model.py
│   │   ├── memory/                 # Sistema de memória (3 arquivos)
│   │   │   ├── test_config_loader.py
│   │   │   ├── test_execution_tracker.py
│   │   │   └── test_memory_manager.py
│   │   ├── utils/                  # Utilitários (5 arquivos)
│   │   │   ├── test_cost_tracker.py
│   │   │   ├── test_event_bus.py
│   │   │   ├── test_json_extraction.py
│   │   │   └── ...
│   │   └── database/               # Database (1 arquivo)
│   │       └── test_database_manager.py
│   │
│   ├── integration/
│   │   ├── smoke/                  # Validação rápida (3 arquivos, ~$0.01)
│   │   │   ├── test_methodologist_smoke.py
│   │   │   ├── test_multi_agent_smoke.py
│   │   │   └── test_structurer_smoke.py
│   │   │
│   │   ├── behavior/               # Comportamentos (15 arquivos, ~$0.02-0.03)
│   │   │   ├── test_socratic_behavior.py
│   │   │   ├── test_refinement_loop.py
│   │   │   ├── test_conversation_flow.py
│   │   │   ├── test_cognitive_evolution.py
│   │   │   └── ...
│   │   │
│   │   └── e2e/                    # Cenários completos (1 arquivo, ~$0.05)
│   │       └── test_multi_turn_flows.py
│   │
│   └── conftest.py                 # Fixtures compartilhadas
│
└── scripts/
    ├── debug/                      # Ferramentas de debug (Épico 8)
    │   ├── check_events.py
    │   └── debug_multi_agent.py
    │
    ├── health_checks/              # Health checks de setup
    │   ├── validate_api.py
    │   ├── validate_agent_config.py
    │   └── ...
    │
    └── testing/                    # Utilitários de teste (Épico 8)
        ├── execute_scenario.py
        ├── debug_scenario.py
        ├── replay_session.py
        └── ...
```

---

## Categorias de Testes

### Unit Tests (`tests/unit/`)
- **Custo:** $0
- **Velocidade:** < 1s por teste
- **Quando:** CI em todo PR
- **Total:** 226 testes

### Smoke Tests (`tests/integration/smoke/`)
- **Custo:** ~$0.01 por teste
- **Velocidade:** 1-2s por teste
- **Quando:** Manual ou CI seletivo
- **Total:** 11 testes

### Behavior Tests (`tests/integration/behavior/`)
- **Custo:** ~$0.02-0.03 por teste
- **Velocidade:** 2-5s por teste
- **Quando:** Manual (antes de releases)
- **Total:** 15 arquivos

### E2E Tests (`tests/integration/e2e/`)
- **Custo:** ~$0.05 por teste
- **Velocidade:** 5-10s por teste
- **Quando:** Manual (validações críticas)
- **Total:** 1 arquivo

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

**Versão:** 3.1 (Refatorado - modularizado)
**Data:** 14/12/2025
**Nota:** Testes do Orquestrador foram modularizados em `tests/unit/agents/orchestrator/` para melhor organização.
