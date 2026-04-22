# Testing Commands

## Dois Perfis de Validação

O projeto tem **dois perfis** de instalação e execução de testes. Escolha conforme o objetivo.

### Perfil A — Unit (rápido, $0, CI)

Uso: pre-commit local, pipeline de CI, validação rápida de PR.
Não faz chamadas LLM nem baixa modelos. Alguns testes que dependem de `langgraph-checkpoint-sqlite` pulam silenciosamente — é esperado.

```bash
# 1. Instalar dependências de teste (minimal)
pip install -r requirements-test.txt

# 2. Rodar
pytest tests/core/unit/ -q
```

**Esperado:** ~412 passed, ~10-19 skipped (skips = modelo HuggingFace ou sqlite checkpoint ausentes).

### Perfil B — Full Integration (local, pago, requer API/rede)

Uso: validação ponta-a-ponta antes de merge, debug de comportamento real do LLM.

Pré-requisitos:
- `ANTHROPIC_API_KEY` no `.env` ou exportada
- Conexão de internet (primeira execução baixa o modelo `all-MiniLM-L6-v2` — ~80MB — e cacheia em `~/.cache/huggingface/`)

```bash
# 1. Instalar dependências completas
pip install -r requirements.txt

# 2. Rodar integration tests
pytest tests/core/integration/ -m integration -q --maxfail=1
```

**Custo estimado:** ~$0.10 para a suite completa (Haiku).

---

## Comandos Granulares

### Unit por categoria
```bash
pytest tests/core/unit/agents/ -q
pytest tests/core/unit/memory/ -q
pytest tests/core/unit/utils/ -q
pytest tests/core/unit/models/ -q
```

### Integration por tipo
```bash
# Smoke (validação rápida de componentes principais)
pytest tests/core/integration/smoke/ -m smoke -q

# Behavior (comportamentos específicos com API real)
pytest tests/core/integration/behavior/ -m behavior -q

# E2E (cenários completos multi-turn)
pytest tests/core/integration/e2e/ -m e2e -q
```

### Teste específico
```bash
pytest tests/core/unit/agents/orchestrator/test_node.py -v
pytest tests/core/integration/behavior/test_embedding_quality.py -v
```

---

## Scripts de Validação Manual

### Health checks (sem API)
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

### Cenários E2E scriptados
```bash
python scripts/core/testing/run_scenario.py
python scripts/core/testing/run_all_scenarios.py
python scripts/core/testing/replay_session.py
```

---

## Flags Úteis

```bash
pytest -v          # Verbose (cada teste)
pytest -x          # Para no primeiro erro
pytest -s          # Mostra prints
pytest --lf        # Só os que falharam na última run
pytest -k "X"      # Filtra por substring do nome
```

### Markers
```bash
pytest -m integration        # Só integration
pytest -m "not integration"  # Tudo exceto integration
pytest -m "smoke or behavior" # Combinação
```
