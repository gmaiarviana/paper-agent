# Behavior Tests

Validate specific behaviors (socratic, refinement, conversation flow).

**Cost**: ~$0.02-0.03 per test  
**Speed**: 2-5s per test  
**When**: Manual (before releases)

## Purpose

Behavior tests validate specific system behaviors and interactions:
- Socratic questioning behavior
- Refinement loops
- Conversation flows
- Integration between components

## Running

```bash
# Run all behavior tests (requires ANTHROPIC_API_KEY)
pytest tests/core/integration/behavior/ -m behavior

# Run specific test
pytest tests/core/integration/behavior/test_socratic_behavior.py
```

## Requirements

- `ANTHROPIC_API_KEY` must be set in `.env` file
- Tests use real API calls
- May take longer to execute

