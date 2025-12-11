# Scripts Históricos

Scripts de validação manual que foram substituídos por testes automatizados.

## Arquivados

### `validate_clarification_questions.py`

- **Propósito:** Validação manual do Épico 14 (clarification)
- **Substituído por:** `tests/core/unit/models/test_clarification.py` (38 testes)
- **Motivo:** Épico concluído, testes automatizados cobrem funcionalidade

### `validate_observer_integration.py`

- **Propósito:** Validação manual do Épico 12 (Observer integration)
- **Substituído por:** `tests/core/unit/agents/observer/` (5 arquivos, ~97 testes)
- **Motivo:** Épico concluído, testes automatizados cobrem funcionalidade

## Quando Usar Scripts Históricos

✅ **Como referência** para entender estrutura de épicos antigos
✅ **Para debugging** se comportamento mudou inesperadamente
❌ **NÃO usar para validação** (usar testes automatizados)

