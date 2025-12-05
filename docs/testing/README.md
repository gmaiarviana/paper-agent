# Testing Guidelines - Índice

## 📚 Documentação
- [**Inventory**](inventory.md) - 🆕 **CONSULTE PRIMEIRO** - O que já está testado
- [Strategy](strategy.md) - Pirâmide de testes, quando usar cada tipo
- [Structure](structure.md) - Estrutura de pastas e fixtures
- [Commands](commands.md) - Comandos pytest

## 🎯 Quick Start
```bash
# Unit tests (rápidos, sem custo) - CI
pytest tests/unit/

# Smoke tests (validação rápida, API real)
pytest tests/integration/smoke/ -m smoke

# Behavior tests (comportamentos específicos)
pytest tests/integration/behavior/ -m behavior

# E2E tests (cenários completos, mais caros)
pytest tests/integration/e2e/ -m e2e

# Todos os integration tests
pytest tests/integration/ -m integration
```

## 💡 TL;DR

**Estrutura por Cenário:**
- **unit/** - Lógica isolada, mocks, $0, CI sempre
- **integration/smoke/** - Validação rápida, API real, ~$0.01
- **integration/behavior/** - Comportamentos específicos, ~$0.02-0.03
- **integration/e2e/** - Cenários completos multi-turn, ~$0.05

**Resultado da Migração (Épico 8):**
- ✅ 226 unit tests, 11 smoke tests
- ✅ 0 falhas
- ✅ Estrutura modular por categoria

---

**Versão:** 3.0
**Data:** 15/01/2025
**Status:** Documentação atualizada para estrutura migrada (Épico 8)
