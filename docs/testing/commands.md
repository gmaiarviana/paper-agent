# Testing Commands

## Rodar Testes

### Todos os testes unitários
```bash
pytest tests/unit/
```

### Todos os testes de integração
```bash
pytest tests/integration/ -m integration
```

### Todos os testes (unit + integration)
```bash
pytest tests/
```

### Com coverage
```bash
pytest tests/unit/ --cov=utils --cov=agents --cov=orchestrator
```

### Health check manual
```bash
python scripts/validate_api.py
```

---

## Scripts de Validação Manual

### Validar estado do Metodologista
```bash
python scripts/validate_state.py
```

### Validar tool ask_user
```bash
python scripts/validate_ask_user.py
```

### Validar nós do grafo
```bash
python scripts/validate_graph_nodes.py
```

### Validar construção do grafo
```bash
python scripts/validate_graph.py
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

**Versão:** 2.0
**Data:** 10/11/2025
