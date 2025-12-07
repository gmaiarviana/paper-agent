# ÉPICO 6: Limpeza de Testes

> **Objetivo:** Remover testes burocráticos e adicionar testes de integração reais onde há mocks superficiais.

---

## 📋 Visão Geral

**Problema atual:**
- Testes com mocks superficiais não validam comportamento real (`test_orchestrator.py`, `test_structurer.py`)
- Testes burocráticos que apenas testam bibliotecas externas ou estruturas sem lógica própria
- Testes verificam apenas estrutura (presença de campos), não comportamento real

**Solução:**
1. **Remover testes burocráticos** que não agregam valor
2. **Adicionar testes de integração reais** onde há mocks superficiais (comportamento real)
3. Manter testes unitários existentes que validam estrutura importante

---

## 🎯 Arquivos a Melhorar

### 1. Remover Testes Burocráticos

**Testes a remover:**
- `test_event_models.py` - Testa apenas Pydantic (biblioteca externa)
- Outros testes identificados que testam estrutura sem lógica

**Razão:** Estes testes não agregam valor, apenas testam bibliotecas externas ou estruturas sem lógica própria.

---

### 2. Adicionar Testes de Integração Reais

#### 1. `tests/unit/test_orchestrator.py` → `tests/integration/test_orchestrator_integration.py`

**Problema atual:**
- Mocks retornam exatamente o esperado
- Não testa se LLM realmente classifica corretamente
- Não valida comportamento real

**Solução:**
- Criar `tests/integration/test_orchestrator_integration.py`
- Testes com API real validando classificação real
- Manter `test_orchestrator.py` (valida estrutura, mocks são OK)

**Exemplo:**
```python
@pytest.mark.integration
def test_orchestrator_classifies_vague_input_real_api():
    """Testa classificação real com API (não mock)."""
    state = create_initial_multi_agent_state(
        "Observei que desenvolver com IA é mais rápido",
        session_id="test-real-1"
    )
    
    result = orchestrator_node(state)  # API real
    
    # Validar comportamento real
    assert result["next_step"] in ["explore", "clarify"]
    assert result["orchestrator_analysis"] is not None
    # Valida que LLM realmente classificou, não apenas estrutura
```

#### 2. `tests/unit/test_structurer.py` → `tests/integration/test_structurer_integration.py`

**Problema atual:**
- Mocks retornam exatamente o esperado
- Não testa se estruturação faz sentido

**Solução:**
- Criar `tests/integration/test_structurer_integration.py`
- Testes com API real validando estruturação real
- Manter `test_structurer.py` (valida estrutura, mocks são OK)

---

## ✅ Critérios de Aceite

### Remover Testes Burocráticos (6.1)
- [ ] Identificar e remover testes que apenas testam bibliotecas externas
- [ ] Remover `test_event_models.py` (testa apenas Pydantic)
- [ ] Identificar outros testes burocráticos que não agregam valor
- [ ] Documentar razão da remoção

### Testes de Integração Reais (6.2)
- [ ] Criar `tests/integration/test_orchestrator_integration.py` com testes de classificação real
- [ ] Criar `tests/integration/test_structurer_integration.py` com testes de estruturação real
- [ ] Testes devem usar API real (não mocks)
- [ ] Testes devem validar comportamento real (não apenas estrutura)
- [ ] Manter testes unitários existentes que validam estrutura importante

### Documentação (6.3)
- [ ] Atualizar `docs/testing/strategy.md` com seção sobre testes de integração reais
- [ ] Documentar estratégia de execução (local: `pytest -m integration`)

---

## 📝 Notas de Implementação

### Ordem de Implementação Recomendada

1. **Remover testes burocráticos primeiro** (6.1)
   - Identificar testes que apenas testam bibliotecas externas
   - Remover `test_event_models.py` e outros similares
   - Limpa a suite de testes

2. **Adicionar testes de integração reais** (6.2)
   - Criar `test_orchestrator_integration.py` e `test_structurer_integration.py`
   - Validar comportamento real (não mocks)
   - Resolve débito técnico imediato

### Manter Testes Existentes

- **NÃO remover** testes existentes que validam estrutura importante
- **REMOVER** apenas testes burocráticos que não agregam valor
- **ADICIONAR** novos testes de integração reais onde há mocks superficiais

---

**Versão:** 2.0  
**Data:** Dezembro 2025  
**Relacionado:** ÉPICO 6 no ROADMAP  
**Ver também:** ÉPICO 8 (Automação)

---

## 📝 Nota sobre Débito Técnico

Este épico resolve débito técnico identificado na análise de testes:
- **Testes burocráticos** → Remover testes que apenas testam bibliotecas externas
- **Mocks superficiais** → Adicionar testes de integração reais

**Não jogar para backlog:** Testes que não agregam valor devem ser corrigidos ou removidos, não ignorados.

---

## 📝 Nota sobre Automação

A automação de validação de qualidade com LLM-as-Judge foi movida para o **ÉPICO 8**.

Ver: `docs/testing/epic8_automation_strategy.md`

