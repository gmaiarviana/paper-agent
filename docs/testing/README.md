# Testing Guidelines - Índice

## 📚 Documentação
- [**Inventory**](inventory.md) - 🆕 **CONSULTE PRIMEIRO** - O que já está testado
- [Strategy](strategy.md) - Pirâmide de testes, quando usar cada tipo
- [Structure](structure.md) - Estrutura de pastas e fixtures
- [Commands](commands.md) - Comandos pytest

## 🎯 Quick Start
```bash
# Unit tests (rápidos, sem custo) - CI
pytest tests/core/unit/

# Smoke tests (validação rápida, API real)
pytest tests/core/integration/smoke/ -m smoke

# Behavior tests (comportamentos específicos)
pytest tests/core/integration/behavior/ -m behavior

# E2E tests (cenários completos, mais caros)
pytest tests/core/integration/e2e/ -m e2e

# Todos os integration tests
pytest tests/core/integration/ -m integration
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

---

## 📚 Histórico de Épicos

Documentação histórica de épicos de testes:

- [Épico 6](epics/epic6/) - Limpeza de testes
- [Épico 7](epics/epic7/) - Validação de maturidade (manual)
- [Épico 8](epics/epic8/) - Sistema de testes maduro + reestruturação

Ver também: [Migração](migration/) - Reestruturação completa (Épico 8)

---

**Versão:** 3.0
**Data:** 15/01/2025
**Status:** Documentação atualizada para estrutura migrada (Épico 8)
