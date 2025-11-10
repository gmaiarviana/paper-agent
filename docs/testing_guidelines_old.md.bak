# Testing Guidelines

## Visão Geral

Este documento define a estratégia de testes do Paper Agent, incluindo estrutura, tipos de testes, e quando usar cada abordagem.

---

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

## Estrutura de Testes

```
paper-agent/
├── tests/                      # Testes automatizados (pytest)
│   ├── __init__.py
│   ├── unit/                   # Testes unitários (mocks)
│   │   ├── __init__.py
│   │   └── test_cost_tracker.py
│   ├── integration/            # Testes de integração (API real)
│   │   ├── __init__.py
│   │   └── test_anthropic_connection.py
│   └── conftest.py             # Fixtures compartilhadas
│
├── scripts/                    # Validação manual (dev local)
│   ├── __init__.py
│   └── validate_api.py         # Health check manual
```

---

## Tipos de Testes

### 1. Unit Tests (`tests/unit/`)

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

**Exemplo:**
```python
# tests/unit/test_cost_tracker.py
def test_calculate_cost_haiku():
    result = CostTracker.calculate_cost(
        "claude-3-5-haiku-20241022",
        input_tokens=18,
        output_tokens=25
    )
    assert result["total_cost"] == pytest.approx(0.0001144)
```

**Rodar:**
```bash
pytest tests/unit/
```

---

### 2. Integration Tests (`tests/integration/`)

**O que são:**
- Testam **integração real** com serviços externos (Anthropic API)
- Usam **API real** com chave de teste
- **Mais lentos** (segundos)
- **Têm custo** (gastam tokens)

**Quando usar:**
- ✅ Validar contratos com APIs externas
- ✅ Testar fluxos críticos end-to-end
- ✅ Verificar comportamento real de agentes

**Exemplo:**
```python
# tests/integration/test_anthropic_connection.py
@pytest.mark.integration
def test_api_connection_real(anthropic_client):
    """Testa conexão real com Anthropic API."""
    response = anthropic_client.messages.create(
        model="claude-3-5-haiku-20241022",
        max_tokens=10,
        messages=[{"role": "user", "content": "Hi"}]
    )
    assert response.content[0].text
```

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

### 3. Health Checks (`scripts/`)

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

**Exemplo:**
```bash
# Roda com sua chave pessoal do .env
python scripts/validate_api.py
```

**Saída esperada:**
```
============================================================
CLAUDE API HEALTH CHECK
============================================================

✓ API key found
✓ Anthropic client initialized

📥 RESPONSE FROM CLAUDE
Hello! I'm Claude...

📊 TOKEN USAGE & COST ANALYSIS
  Input tokens:  18
  Output tokens: 25
  Total tokens:  43

  💰 Cost (Haiku rates):
     Total:  $0.00011440

✅ VALIDATION PASSED
```

---

## Mocks vs API Real: Quando Usar Cada Um?

### ✅ Use Mocks (Unit Tests) quando:
- Testar **lógica interna** (não integração)
- Desenvolvimento rápido (TDD)
- Custo zero
- Testes confiáveis (sem falhas de rede)

**Exemplo válido com mock:**
```python
# Validar que o código TRATA a resposta corretamente
@patch('anthropic.Anthropic')
def test_methodologist_parses_response(mock_client):
    mock_client.messages.create.return_value = MockResponse(...)
    result = methodologist.analyze("hipótese")
    assert result["status"] == "approved"
```

### ✅ Use API Real (Integration Tests) quando:
- Testar **contrato com API externa**
- Validar **comportamento real** de modelos
- Verificar **breaking changes** na API

**Exemplo válido com API real:**
```python
# Validar que a API Anthropic RESPONDE como esperado
def test_api_returns_valid_json():
    response = anthropic_client.messages.create(...)
    assert "content" in response
    assert response.usage.input_tokens > 0
```

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

**Exemplo de log em integration test:**
```python
def test_methodologist_analysis(cost_logger):
    result = methodologist.analyze("café melhora produtividade")
    cost_logger.log(result.usage)  # Registra custo
# Output: [INFO] Test cost: $0.00123 (45 tokens)
```

---

## Rodando Testes

### Todos os testes unitários
```bash
pytest tests/unit/
```

### Todos os testes de integração
```bash
pytest tests/integration/ -m integration
```

### Todos os testes (unit + integration)
```bash
pytest tests/
```

### Com coverage
```bash
pytest tests/unit/ --cov=utils --cov=agents --cov=orchestrator
```

### Health check manual
```bash
python scripts/validate_api.py
```

---

## Fixtures Pytest (`tests/conftest.py`)

Fixtures compartilhadas entre testes:

```python
import pytest
from anthropic import Anthropic
import os

@pytest.fixture
def anthropic_client():
    """Cliente real da Anthropic (para integration tests)."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        pytest.skip("ANTHROPIC_API_KEY not set")
    return Anthropic(api_key=api_key)

@pytest.fixture
def cost_logger():
    """Logger para rastrear custos em testes."""
    class CostLogger:
        def __init__(self):
            self.total_cost = 0.0

        def log(self, usage):
            cost = CostTracker.calculate_cost(
                "claude-3-5-haiku-20241022",
                usage.input_tokens,
                usage.output_tokens
            )
            self.total_cost += cost["total_cost"]
            print(f"[INFO] Test cost: ${cost['total_cost']:.5f}")

    return CostLogger()
```

---

## TDD Pragmático

Seguimos **TDD pragmático** (não dogmático):

### Escrever teste ANTES (Red → Green → Refactor)
- ✅ Lógica de negócio crítica
- ✅ APIs/endpoints
- ✅ Cálculos e validações
- ✅ Funções puras

### Implementar SEM teste (ou teste DEPOIS)
- ⚠️ UI/componentes visuais (validar manualmente)
- ⚠️ Configurações/setup
- ⚠️ Estilização

---

## CI/CD Strategy

### GitHub Actions (futuro)

```yaml
name: Tests

on: [push, pull_request]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: pip install -r requirements.txt
      - run: pytest tests/unit/ --cov

  integration-tests:
    runs-on: ubuntu-latest
    if: github.event_name == 'pull_request'
    env:
      ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_TEST_KEY }}
    steps:
      - uses: actions/checkout@v2
      - run: pip install -r requirements.txt
      - run: pytest tests/integration/ -m integration
```

---

## Boas Práticas

### ✅ DO
- Testes unitários rápidos (< 100ms cada)
- Nomes descritivos (`test_calculate_cost_with_zero_tokens`)
- Um assert por conceito
- Fixtures para setup repetitivo
- Mocks para dependências externas

### ❌ DON'T
- Testes que dependem de ordem de execução
- Testes que modificam estado global
- Testes lentos em unit tests (> 1s)
- Hard-coding de valores mágicos
- Testes que sempre passam

---

## Referências

- **Pirâmide de Testes**: Martin Fowler, "The Practical Test Pyramid"
- **Pytest Docs**: https://docs.pytest.org/
- **Mocking**: https://docs.python.org/3/library/unittest.mock.html
- **TDD**: Kent Beck, "Test Driven Development: By Example"

---

**Versão:** 1.0
**Data:** 07/11/2025
**Status:** Ativo - estrutura estabelecida para ÉPICO 1
