# Testing Commands

## Rodar Testes

### Por Categoria (Nova Estrutura)
```bash
# Unit tests (sempre rodam - $0)
pytest tests/unit/ -v

# Smoke tests (validação rápida - ~$0.01)
pytest tests/integration/smoke/ -v -m smoke

# Behavior tests (comportamentos específicos - ~$0.02-0.03)
pytest tests/integration/behavior/ -v -m behavior

# E2E tests (cenários completos - ~$0.05)
pytest tests/integration/e2e/ -v -m e2e

# Todos os integration tests
pytest tests/integration/ -v -m integration
```

### Por Componente
```bash
# Testar apenas agentes
pytest tests/unit/agents/ -v

# Testar apenas memória
pytest tests/unit/memory/ -v

# Testar apenas utils
pytest tests/unit/utils/ -v
```

### Exemplos Específicos
```bash
# Testar apenas Orquestrador
pytest tests/unit/agents/test_orchestrator_logic.py -v

# Testar comportamento socrático
pytest tests/integration/behavior/test_socratic_behavior.py -v

# Testar fluxos multi-turn
pytest tests/integration/e2e/test_multi_turn_flows.py -v
```

---

## Scripts de Validação Manual

### State introspection (sem chamadas reais à API)
```bash
python scripts/state_introspection/validate_state.py
```

```bash
python scripts/state_introspection/validate_graph.py
```

```bash
python scripts/state_introspection/validate_graph_nodes.py
```

```bash
python scripts/state_introspection/validate_ask_user.py
```

### Flows completos (consomem API)
```bash
python scripts/flows/validate_cli.py
```

```bash
python scripts/flows/validate_cli_integration.py
```

```bash
python scripts/flows/validate_dashboard.py
```

```bash
python scripts/flows/validate_memory_integration.py
```

```bash
python scripts/flows/validate_multi_agent_flow.py
```

```bash
python scripts/flows/validate_orchestrator.py
```

```bash
python scripts/flows/validate_refinement_loop.py
```

```bash
python scripts/flows/validate_structurer.py
```

```bash
python scripts/flows/validate_structurer_refinement.py
```

```bash
python scripts/flows/validate_build_context.py
```

### Health checks adicionais
```bash
python scripts/health_checks/validate_execution_tracker.py
```

```bash
python scripts/health_checks/validate_orchestrator_json_parsing.py
```

### Debug
```bash
python scripts/debug/check_events.py
```

---

## Testes por Módulo

### Testar apenas CostTracker
```bash
pytest tests/unit/test_cost_tracker.py -v
```

### Testar apenas nós do grafo
```bash
pytest tests/unit/test_graph_nodes.py -v
```

### Testar apenas extração de JSON
```bash
pytest tests/unit/test_json_extraction.py -v
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
pytest tests/unit/test_cost_tracker.py::test_calculate_cost_haiku -v
```

### Markers
```bash
# Rodar apenas testes marcados como integration
pytest -m integration

# Rodar tudo exceto integration
pytest -m "not integration"
```

---

**Versão:** 3.0
**Data:** 15/01/2025
