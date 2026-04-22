# Testing Commands

## Rodar Testes

### Por Categoria
```bash
# Unit tests (sempre rodam - $0)
pytest tests/core/unit/ -v

# Smoke tests (validação rápida - ~$0.01)
pytest tests/core/integration/smoke/ -v -m smoke

# Behavior tests (comportamentos específicos - ~$0.02-0.03)
pytest tests/core/integration/behavior/ -v -m behavior

# E2E tests (cenários completos - ~$0.05)
pytest tests/core/integration/e2e/ -v -m e2e

# Todos os integration tests
pytest tests/core/integration/ -v -m integration
```

### Por Componente
```bash
# Testar apenas agentes
pytest tests/core/unit/agents/ -v

# Testar apenas memória
pytest tests/core/unit/memory/ -v

# Testar apenas utils
pytest tests/core/unit/utils/ -v
```

### Exemplos Específicos
```bash
# Executar todos os testes do orquestrador
pytest tests/core/unit/agents/orchestrator/ -v

# Executar teste específico
pytest tests/core/unit/agents/orchestrator/test_node.py -v

# Testar comportamento socrático
pytest tests/core/integration/behavior/test_socratic_behavior.py -v

# Testar fluxos multi-turn
pytest tests/core/integration/e2e/test_multi_turn_flows.py -v
```

---

## Scripts de Validação Manual

### Health checks (conexão com API, configs)
```bash
python scripts/core/health_checks/validate_api.py
python scripts/core/health_checks/validate_agent_config.py
python scripts/core/health_checks/validate_execution_tracker.py
python scripts/core/health_checks/validate_orchestrator_json_parsing.py
python scripts/core/health_checks/validate_runtime_config_simple.py
python scripts/core/health_checks/validate_syntax.py
python scripts/core/health_checks/validate_system_prompt.py
```

### Debug
```bash
python scripts/core/debug/check_events.py
python scripts/core/debug/debug_multi_agent.py
```

### Inspeção de banco
```bash
python scripts/core/inspect_database.py
```

### Cenários E2E (scripts/core/testing/)
```bash
python scripts/core/testing/run_scenario.py
python scripts/core/testing/run_all_scenarios.py
python scripts/core/testing/replay_session.py
```

---

## Testes por Módulo

### CostTracker
```bash
pytest tests/core/unit/utils/test_cost_tracker.py -v
```

### Extração de JSON
```bash
pytest tests/core/unit/utils/test_json_extraction.py -v
```

### Metodologista (grafo e nós)
```bash
pytest tests/core/unit/agents/test_methodologist_graph.py -v
pytest tests/core/unit/agents/test_methodologist_nodes.py -v
```

---

## Flags Úteis

### Verbose (mostra cada teste)
```bash
pytest -v
```

### Stop no primeiro erro
```bash
pytest -x
```

### Mostrar prints
```bash
pytest -s
```

### Rodar teste específico
```bash
pytest tests/core/unit/utils/test_cost_tracker.py::test_calculate_cost_haiku -v
```

### Markers
```bash
# Rodar apenas testes marcados como integration
pytest -m integration

# Rodar tudo exceto integration
pytest -m "not integration"
```
