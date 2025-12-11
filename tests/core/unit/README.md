# Unit Tests

Fast tests with mocks. No API calls. Run in CI on every PR.

**Cost**: $0  
**Speed**: < 1s per test  
**When**: Always (CI)

## Structure

- `agents/` - Agent logic tests (orchestrator, structurer, methodologist)
- `models/` - Data structure tests (states, cognitive_model)
- `memory/` - Memory system tests (config_loader, execution_tracker, memory_manager)
- `utils/` - Utility tests (cost_tracker, event_bus, json_extraction, currency)
- `database/` - Database operation tests

## Running

```bash
# Run all unit tests
pytest tests/unit/

# Run specific category
pytest tests/unit/agents/
pytest tests/unit/utils/
```

