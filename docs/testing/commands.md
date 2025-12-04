# Testing Commands

## Rodar Testes

### Todos os testes unitários (bateria rápida - recomendado após refatorações)
```bash
pytest tests/unit/ -v
```

### Todos os testes de integração
```bash
pytest tests/integration/ -m integration
```

### Todos os testes (unit + integration)
```bash
pytest tests/
```

### Bateria completa (unit + integration, verbose)
```bash
pytest tests/ -v --tb=short
```

### Com coverage
```bash
pytest tests/unit/ --cov=utils --cov=agents --cov=orchestrator
```

### Health checks (rápidos, sem fluxo completo)
```bash
python scripts/health_checks/validate_api.py
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

**Versão:** 2.1
**Data:** 13/11/2025
