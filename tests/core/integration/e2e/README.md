# E2E Tests

Complete multi-turn scenarios. Most expensive.

**Cost**: ~$0.05 per test  
**Speed**: 5-10s per test  
**When**: Manual (critical validations)

## Purpose

End-to-end tests validate complete user scenarios:
- Multi-turn conversations
- Full agent interactions
- Context preservation
- Complete workflows

## Running

```bash
# Run all E2E tests (requires ANTHROPIC_API_KEY)
pytest tests/integration/e2e/ -m e2e

# Run specific test
pytest tests/integration/e2e/test_multi_turn_flows.py
```

## Requirements

- `ANTHROPIC_API_KEY` must be set in `.env` file
- Tests use real API calls (expensive)
- Longest execution time
- Use sparingly for critical validations

