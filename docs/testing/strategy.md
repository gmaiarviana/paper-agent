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

### ❌ DON'T
- Testes que dependem de ordem de execução
- Testes que modificam estado global
- Testes lentos em unit tests (> 1s)
- Hard-coding de valores mágicos
- Testes que sempre passam

---

**Versão:** 2.0
**Data:** 10/11/2025
