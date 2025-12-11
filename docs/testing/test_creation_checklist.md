# Checklist de Criação de Testes

**Objetivo:** Garantir que novos testes agregam valor real ao projeto.

## 📋 ANTES DE CRIAR QUALQUER TESTE

**Claude Code / Cursor:** Execute este checklist ANTES de escrever teste:

### 1. Validação de Necessidade
- [ ] Teste valida comportamento próprio (não biblioteca externa)
- [ ] Cobre edge cases reais (não apenas happy path)
- [ ] Justificativa clara: Posso explicar por que este teste é necessário
- [ ] Não é redundante: Não existe teste similar já

### 2. Validação de Qualidade
- [ ] Asserts substanciais: Validam conteúdo/comportamento (não apenas presença)
- [ ] Mocks realistas: Simulam variações reais (não retornam exatamente o esperado)
- [ ] Nome descritivo: `test_<comportamento>_<cenário>`
- [ ] Docstring: Explica por que teste existe (se não óbvio)

### 3. Validação de Manutenibilidade
- [ ] Teste é fácil de entender: Outro dev consegue ler e entender
- [ ] Teste é rápido: Unit test < 100ms, Integration test < 5s
- [ ] Teste é isolado: Não depende de ordem ou estado global
- [ ] Teste é determinístico: Sempre passa/falha pelo mesmo motivo

## ❌ SINAIS DE ALERTA (NÃO Criar)

Se qualquer item abaixo for verdade, **RECONSIDERE** criar o teste:

- ⚠️ Teste apenas valida que Pydantic/YAML/biblioteca funciona
- ⚠️ Mock retorna exatamente o que teste espera (sempre passa)
- ⚠️ Assert apenas verifica presença (`is not None`, `== True`)
- ⚠️ Teste é cópia de outro teste com pequenas variações
- ⚠️ Não consigo explicar por que teste é necessário
- ⚠️ Teste sempre passaria (não detecta bugs reais)

## ✅ EXEMPLOS DE BONS TESTES

### Exemplo 1: Lógica de Negócio (Edge Case)
```python
def test_cost_calculation_with_million_tokens():
    """Valida cálculo de custo com volume alto (1M tokens)."""
    result = calculate_cost("claude-3-5-haiku", 1_000_000, 1_000_000)
    assert result["total_cost"] == pytest.approx(4.80, rel=1e-6)
    assert result["input_cost"] < result["output_cost"]
```

**Por que é bom:**
- ✅ Testa lógica própria (cálculo de custo)
- ✅ Cobre edge case real (volume alto)
- ✅ Asserts substanciais (valor exato + relação input/output)

### Exemplo 2: Validação de Comportamento
```python
def test_orchestrator_handles_context_switch():
    """Valida que Orquestrador preserva contexto ao mudar de assunto."""
    state = create_state("Observei que X")
    result = orchestrator_node(state)
    assert result["focal_argument"]["subject"] == "X"
    
    # Mudança brusca de assunto
    state["messages"].append(HumanMessage("Na verdade, Y é mais importante"))
    result2 = orchestrator_node(state)
    
    assert result2["focal_argument"]["subject"] == "Y"
    assert "X" in str(result2["focal_argument"]["context"])
```

**Por que é bom:**
- ✅ Testa comportamento complexo (mudança de contexto)
- ✅ Asserts validam múltiplos aspectos (novo foco + contexto preservado)

## ❌ EXEMPLOS DE TESTES RUINS

### Exemplo 1: Teste de Biblioteca (Pydantic)
```python
def test_cognitive_model_has_fields():
    """❌ NÃO criar - apenas testa Pydantic"""
    model = CognitiveModel(claim="X", propositions=["Y"])
    assert model.claim == "X"
    assert model.propositions == ["Y"]
```

**Por que é ruim:**
- ❌ Apenas valida que Pydantic funciona (não nossa lógica)
- ❌ Sempre passa (não detecta bugs)

### Exemplo 2: Mock Superficial
```python
def test_orchestrator_classifies():
    """❌ NÃO criar - mock superficial"""
    mock_llm.return_value = '{"next_step": "explore"}'  # Retorna exato esperado
    result = orchestrator_node(state)
    assert result["next_step"] == "explore"  # Sempre passa!
```

**Por que é ruim:**
- ❌ Mock retorna exatamente o esperado
- ❌ Sempre passa (não detecta bugs)

### Exemplo 3: Assert Fraco
```python
def test_structurer_returns_something():
    """❌ NÃO criar - assert fraco"""
    result = structurer_node(state)
    assert result["structured_question"] is not None  # Aceita qualquer coisa!
```

**Por que é ruim:**
- ❌ Assert apenas verifica presença
- ❌ Passaria mesmo se retornasse string vazia

## 🔍 REVISÃO PÓS-CRIAÇÃO

Após criar teste, pergunte:
- Este teste já falhou? Se não, ele pode ser sempre verde
- Alguém entende o que este teste protege? Se não, adicionar docstring
- Teste é rápido? Se não, considerar mover para integration
- Teste seria útil em code review? Se não, pode ser removido

## 📚 Referências

- `docs/testing/strategy.md` - Estratégia geral de testes
- `docs/testing/structure.md` - Estrutura de pastas
- `docs/testing/inventory.md` - O que já está testado

