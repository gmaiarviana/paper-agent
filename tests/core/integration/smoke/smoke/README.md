# Smoke Tests

Quick validation with minimal API calls.

**Cost**: ~$0.01 per test  
**Speed**: 1-2s per test  
**When**: Manual or CI (selective)

## Purpose

Smoke tests validate basic functionality with minimal API usage. They are:
- Fast execution
- Low cost
- Good for quick sanity checks
- Suitable for selective CI runs

## Running

```bash
# Run all smoke tests (requires ANTHROPIC_API_KEY)
pytest tests/integration/smoke/ -m smoke

# Run specific test
pytest tests/integration/smoke/test_structurer_smoke.py
```

## Requirements

- `ANTHROPIC_API_KEY` must be set in `.env` file
- Tests use real API calls (minimal, but real)

