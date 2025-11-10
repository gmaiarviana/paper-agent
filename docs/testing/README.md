# Testing Guidelines - Índice

## 📚 Documentação
- [Strategy](strategy.md) - Pirâmide de testes, quando usar cada tipo
- [Structure](structure.md) - Estrutura de pastas e fixtures
- [Commands](commands.md) - Comandos pytest

## 🎯 Quick Start

```bash
# Rodar todos os testes unitários
pytest tests/unit/

# Rodar testes de integração
pytest tests/integration/ -m integration

# Health check manual
python scripts/validate_api.py
```

## 💡 TL;DR

- **Unit tests (70%)**: lógica isolada, mocks, rápidos
- **Integration tests (20%)**: API real, CI
- **E2E tests (10%)**: fluxo completo, manual

---

**Versão:** 2.0
**Data:** 10/11/2025
**Status:** Documentação modularizada e enxuta
