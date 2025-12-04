# Testing Strategy

## Pirâmide de Testes

```
        /\
       /E2E\        ← Poucos, lentos, caros (Streamlit E2E, futuros)
      /------\
     /Integration\  ← Médio, API real, CI com secrets
    /------------\
   /  Unit Tests  \ ← Muitos, rápidos, mocks
  /----------------\
```

### Distribuição Ideal
- **70%** Unit Tests (rápidos, mocks, sempre rodam)
- **20%** Integration Tests (API real, CI com chave de teste)
- **10%** E2E Tests (fluxo completo, manual ou CI seletivo)

---

## Tipos de Testes

### Unit Tests (`tests/unit/`)

**O que são:**
- Testam **unidades isoladas** de código (funções, classes, métodos)
- Usam **mocks** para dependências externas (APIs, banco de dados)
- **Rápidos** (milissegundos)
- **Sem custos** (não chamam APIs reais)

**Quando usar:**
- ✅ Lógica de negócio (validações, cálculos, transformações)
- ✅ Funções puras (input → output determinístico)
- ✅ Parsers, formatadores, utilitários
- ✅ Classes auxiliares (`CostTracker`, `PromptBuilder`)

**Rodar:**
```bash
pytest tests/unit/
```

---

### Integration Tests (`tests/integration/`)

**O que são:**
- Testam **integração real** com serviços externos (Anthropic API)
- Usam **API real** com chave de teste
- **Mais lentos** (segundos)
- **Têm custo** (gastam tokens)

**Quando usar:**
- ✅ Validar contratos com APIs externas
- ✅ Testar fluxos críticos end-to-end
- ✅ Verificar comportamento real de agentes

**Rodar:**
```bash
# Requer ANTHROPIC_API_KEY no ambiente
pytest tests/integration/ -m integration
```

**CI/CD:**
- Roda apenas em PRs importantes
- Usa chave de teste (limite baixo) via GitHub Secrets
- Pode ser pulado em desenvolvimento local

---

### Health Checks (`scripts/`)

**O que são:**
- Scripts **manuais** para validação de ambiente
- Usam **chave pessoal** do desenvolvedor
- **Não são testes automatizados**
- Exibem resultados formatados (tokens, custos, logs)

**Quando usar:**
- ✅ Validar setup inicial do projeto
- ✅ Verificar conexão com API antes de desenvolver
- ✅ Debug de problemas de conectividade
- ✅ Testar custos reais de operações

**Rodar:**
```bash
# Roda com sua chave pessoal do .env
python scripts/health_checks/validate_api.py
```

---

## Mocks vs API Real: Quando Usar?

### ✅ Use Mocks (Unit Tests) quando:
- Testar **lógica interna** (não integração)
- Desenvolvimento rápido (TDD)
- Custo zero
- Testes confiáveis (sem falhas de rede)

### ✅ Use API Real (Integration Tests) quando:
- Testar **contrato com API externa**
- Validar **comportamento real** de modelos
- Verificar **breaking changes** na API

---

## Markers e Política de Execução

### Markers

- `@pytest.mark.unit` (opcional): testes rápidos, sem API real (padrão em `tests/unit/`).
- `@pytest.mark.integration`: testes que usam API real ou fluxo que depende de `ANTHROPIC_API_KEY`.
- `@pytest.mark.slow` (opcional): testes de integração mais pesados, que podem ser selecionados à parte.

### Falta de ANTHROPIC_API_KEY

- Se `ANTHROPIC_API_KEY` **não estiver definida**:
  - Ao rodar **`pytest` normal**:
    - Testes `@pytest.mark.integration` podem ser marcados como **skipped** com mensagem clara:
      - "Integration test skipped: ANTHROPIC_API_KEY not set (requires real API)".
  - Ao rodar **`pytest -m integration`**:
    - É aceitável **falhar explicitamente** (não apenas skip), pois o dev pediu integração.

### Comandos recomendados

- Unit tests (rápidos, sempre rodam):
  - `pytest tests/unit/`
- Integração (local, com chave configurada):
  - `pytest tests/integration/ -m integration`
- CI:
  - Sempre roda `@pytest.mark.integration` com `ANTHROPIC_API_KEY` de teste configurada via secrets.

---

## Cost Tracking em Testes

### Unit Tests
- ✅ Testam a **classe CostTracker** (cálculos corretos)
- ❌ Não fazem chamadas reais à API

### Integration Tests
- ✅ Rastreiam custos de chamadas reais
- ✅ Logs exibem custos por teste
- ✅ CI falha se custo ultrapassar threshold

### Scripts
- ✅ Sempre exibem custos formatados
- ✅ Ajudam dev a entender custos de operações

---

## Boas Práticas

### ✅ DO
- Testes unitários rápidos (< 100ms cada)
- Nomes descritivos (`test_calculate_cost_with_zero_tokens`)
- Um assert por conceito
- Fixtures para setup repetitivo
- Mocks para dependências externas
- **Teste lógica própria, não bibliotecas**
- **Teste comportamento, não apenas estrutura**
- **Valide qualidade quando relevante (LLM-as-Judge)**

### ❌ DON'T
- Testes que dependem de ordem de execução
- Testes que modificam estado global
- Testes lentos em unit tests (> 1s)
- Hard-coding de valores mágicos
- Testes que sempre passam
- **Testar bibliotecas externas (Pydantic, YAML, etc.)**
- **Mocks que retornam exatamente o esperado**
- **Asserts que verificam apenas presença (`is not None`)**

---

## Critérios para Remover/Criar Testes

### ❌ Remover se:
- Testa comportamento padrão de biblioteca (Pydantic, YAML, etc.)
- Verifica apenas estrutura de dados (sem lógica)
- Mock retorna exatamente o esperado (não testa lógica)
- Assert verifica apenas presença (`is not None`)
- Teste sempre passa (não cobre edge cases)

### ✅ Criar quando:
- Testa lógica de negócio própria
- Cobre edge cases reais
- Valida cálculos ou transformações
- Testa integração entre componentes
- Detecta bugs reais
- **Valida qualidade conversacional (LLM-as-Judge)**

---

## Exemplos Práticos

### ❌ Teste Ruim (Burocrático)
```python
def test_event_has_fields():
    event = AgentStartedEvent(session_id="s1", agent_name="orch")
    assert event.session_id == "s1"
    assert event.agent_name == "orch"
    # Testa apenas estrutura - Pydantic já valida isso!
```

### ✅ Teste Bom (Agrega Valor)
```python
def test_cost_calculation_large_volume():
    """Testa cálculo com 1M tokens (edge case real)."""
    result = CostTracker.calculate_cost("claude-3-5-haiku-20241022", 1_000_000, 1_000_000)
    assert result["total_cost"] == pytest.approx(4.80, rel=1e-6)
    # Testa lógica real, edge case importante!
```

### ❌ Mock Superficial
```python
def test_orchestrator_vague_input():
    mock_response.content = '{"next_step": "explore"}'  # Retorna exatamente o esperado
    result = orchestrator_node(state)
    assert result["next_step"] == "explore"  # Sempre passa!
    # Não testa se o LLM realmente classifica corretamente!
```

### ✅ Teste de Integração Real
```python
@pytest.mark.integration
def test_orchestrator_classifies_vague_input():
    state = create_initial_multi_agent_state("Observei que X é interessante")
    result = orchestrator_node(state)  # API real
    assert result["next_step"] in ["explore", "clarify"]
    # Testa comportamento real!
```

### ❌ Assert Fraco
```python
def test_multi_agent_flow():
    result = multi_agent_graph.invoke(state)
    assert result["orchestrator_analysis"] is not None  # Aceita qualquer coisa!
```

### ✅ Validação de Qualidade (LLM-as-Judge)
```python
@pytest.mark.llm_judge
def test_socratic_provocation_quality():
    result = orchestrator_node(state)
    evaluation = llm_judge.invoke(
        SOCRATIC_BEHAVIOR_PROMPT.format(response=result['message'])
    )
    score = extract_score(evaluation.content)
    assert score >= 4, "Provocação não é suficientemente socrática"
    # Valida qualidade real!
```

---

## Referências

- **LLM-as-Judge:** `docs/analysis/llm_judge_strategy.md` - Estratégia completa para testes de qualidade
- **Inventário:** `docs/testing/inventory.md` - O que já está testado
- **Estrutura:** `docs/testing/structure.md` - Organização de pastas e fixtures
- **Comandos:** `docs/testing/commands.md` - Comandos pytest

---

**Versão:** 3.1
**Data:** Dezembro 2025
