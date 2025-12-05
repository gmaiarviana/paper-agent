# ÉPICO 8: Validação de Maturidade do Sistema - Automação

> **Objetivo:** Automatizar validação de qualidade conversacional com LLM-as-Judge para prevenir regressões futuras.

---

## 📋 Visão Geral

**Dependência:** Épico 7 deve estar concluído (identificar problemas reais primeiro)

**Problema:**
- Épico 7 validou sistema manualmente e identificou problemas reais
- Validação manual não é escalável (não previne regressões)
- Precisamos garantir que correções não quebrem comportamentos que funcionam

**Solução:**
- Implementar infraestrutura LLM-as-Judge
- Criar testes automatizados para problemas identificados no Épico 7
- Testes validam **qualidade conversacional**, não apenas estrutura

**Resultado Esperado:**
- Testes automatizados que previnem regressões
- Validação de qualidade (não apenas presença de campos)
- Execução rápida e custo baixo (~$0.01-0.02 por execução completa)

---

## 🎯 O Que Automatizar

**Princípio:** Automatizar validação de **problemas reais identificados no Épico 7**

**NÃO automatizar:**
- ❌ Problemas hipotéticos não encontrados no Épico 7
- ❌ Validação de estrutura (testes unitários já fazem isso)
- ❌ Testes determinísticos (usar testes de integração normais)

**Automatizar:**
- ✅ Qualidade conversacional (fluidez, integração)
- ✅ Comportamento socrático (provocação genuína)
- ✅ Preservação de contexto (não se perde entre transições)
- ✅ Decisões coerentes (não arbitrárias)

---

## 🛠️ Infraestrutura LLM-as-Judge

### 1. Fixture `llm_judge`

**Localização:** `tests/conftest.py`

**Especificação:**
```python
@pytest.fixture
def llm_judge():
    """
    Fixture para LLM-as-judge (avaliador de qualidade).
    
    Usa Claude Haiku para custo-benefício.
    Temperature=0 para determinismo.
    """
    import os
    from langchain_anthropic import ChatAnthropic
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        pytest.skip("LLM-as-judge test skipped: ANTHROPIC_API_KEY not set")
    
    return ChatAnthropic(
        model="claude-3-5-haiku-20241022",
        temperature=0
    )
```

**Características:**
- Usa Haiku (custo-benefício)
- Temperature=0 (determinístico)
- Pula testes se API key não está definida (não falha)

---

### 2. Prompts de Avaliação

**Localização:** `utils/test_prompts.py`

**5 Prompts Necessários:**

#### 2.1 Fluidez Conversacional
```python
FLUENCY_PROMPT = """
Avalie a fluidez da mensagem do sistema:

1. Não pergunta permissão ("Posso chamar X?")
2. Integração natural de outputs de agentes
3. Tom conversacional (não burocrático)

Mensagem: {message}

Avalie de 1-5 (5 = completamente fluida):
Justificativa:
"""
```

#### 2.2 Integração Entre Agentes
```python
INTEGRATION_QUALITY_PROMPT = """
Avalie a qualidade da integração entre agentes:

1. Transições naturais (sem quebras)
2. Contexto preservado (referências a turnos anteriores)
3. Experiência coesa (não parece sistema desconexo)

Orquestrador: {orchestrator_output}
Estruturador: {structurer_output}
Metodologista: {methodologist_output}
Mensagens ao usuário: {messages}

Avalie de 1-5 (5 = integração excelente):
Justificativa:
"""
```

#### 2.3 Provocação Socrática
```python
SOCRATIC_BEHAVIOR_PROMPT = """
Avalie se a resposta do sistema demonstra comportamento socrático genuíno:

1. Provocação genuína (expõe assumptions, não coleta burocrática)
2. Timing natural (não regras fixas)
3. Parada inteligente (não insiste infinitamente)

Resposta: {response}
Reflection prompt: {reflection_prompt}

Avalie de 1-5 (5 = excelente comportamento socrático):
Justificativa:
"""
```

#### 2.4 Preservação de Contexto
```python
CONTEXT_PRESERVATION_PROMPT = """
Avalie se o contexto foi preservado entre transições de agentes:

1. Focal argument evolui coerentemente
2. Informações de turnos anteriores são referenciadas
3. Não há perda de contexto (agente não "esquece" informações)

Focal argument (antes): {focal_before}
Focal argument (depois): {focal_after}
Mensagens: {messages}

Avalie de 1-5 (5 = contexto perfeitamente preservado):
Justificativa:
"""
```

#### 2.5 Qualidade de Decisões
```python
DECISION_QUALITY_PROMPT = """
Avalie a qualidade da decisão do agente:

1. Decisão é coerente com contexto fornecido
2. Justificativa é clara e específica
3. Não é arbitrária (usa critérios explícitos)

Contexto: {context}
Decisão: {decision}
Justificativa: {justification}

Avalie de 1-5 (5 = decisão excelente):
Justificativa:
"""
```

---

### 3. Helper `extract_score`

**Localização:** `utils/test_helpers.py`

**Especificação:**
```python
import re

def extract_score(evaluation_content: str) -> int:
    """
    Extrai score (1-5) da avaliação do LLM-as-judge.
    
    Procura por padrões:
    - "Avalie de 1-5: 4"
    - "score: 3"
    - "4/5"
    - Apenas número na linha
    
    Args:
        evaluation_content: Conteúdo da avaliação do LLM
        
    Returns:
        int: Score de 1-5
        
    Raises:
        ValueError: Se não encontrar score válido
    """
    patterns = [
        r"Avalie de 1-5.*?(\d)",
        r"score.*?(\d)",
        r"(\d)\s*/\s*5",
        r"(\d)\s*=\s*(?:excelente|ótimo|bom)",
        r"^(\d)$"  # Apenas número na linha
    ]
    
    for pattern in patterns:
        match = re.search(pattern, evaluation_content, re.IGNORECASE | re.MULTILINE)
        if match:
            score = int(match.group(1))
            if 1 <= score <= 5:
                return score
    
    raise ValueError(f"Não foi possível extrair score válido de: {evaluation_content}")
```

---

### 4. Marker no `pytest.ini`

**Adicionar:**
```ini
[pytest]
markers =
    unit: Testes unitários (mocks)
    integration: Testes de integração (API real)
    llm_judge: Testes que usam LLM-as-judge (requer API key)
    slow: Testes lentos (opcional)
```

---

## 📝 Testes Automatizados

### Princípio: Adicionar Validação de Qualidade

**NÃO substituir testes existentes**  
**ADICIONAR** função de teste com `@pytest.mark.llm_judge`

**Exemplo:**
```python
# Teste existente (estrutura)
def test_multi_agent_flow(multi_agent_graph):
    result = multi_agent_graph.invoke(state)
    assert result["orchestrator_analysis"] is not None
    assert result["next_step"] in ["explore", "suggest_agent"]

# ADICIONAR: Teste de qualidade
@pytest.mark.llm_judge
def test_multi_agent_flow_quality(multi_agent_graph, llm_judge):
    """Valida qualidade da experiência conversacional."""
    result = multi_agent_graph.invoke(state)
    
    # Validação estrutural (mantém)
    assert result["orchestrator_analysis"] is not None
    
    # NOVO: Validação de qualidade
    evaluation = llm_judge.invoke(
        CONVERSATION_QUALITY_PROMPT.format(
            response=result.get("messages", [])[-1].content,
            history=result.get("conversation_history", [])
        )
    )
    score = extract_score(evaluation.content)
    assert score >= 4, f"Qualidade conversacional insuficiente (score: {score})"
```

---

### Arquivos a Adicionar Testes

Baseado no **Épico 7** (problemas identificados), adicionar testes em:

#### 1. `tests/integration/test_multi_agent_smoke.py`
**Validar:**
- Fluidez conversacional (sem "Posso chamar X?")
- Integração entre agentes (transições naturais)
- Preservação de contexto (focal_argument evolui)

**Exemplo:**
```python
@pytest.mark.llm_judge
def test_conversational_fluency(multi_agent_graph, llm_judge):
    """Valida que sistema não pede permissão para transições."""
    state = create_initial_multi_agent_state(
        "Observei que LLMs aumentam produtividade",
        session_id="test-fluency-1"
    )
    
    result = multi_agent_graph.invoke(state)
    
    # Extrair mensagens ao usuário
    user_messages = [
        msg.content for msg in result.get("messages", [])
        if isinstance(msg, AIMessage)
    ]
    
    # Validar cada mensagem
    for message in user_messages:
        evaluation = llm_judge.invoke(
            FLUENCY_PROMPT.format(message=message)
        )
        score = extract_score(evaluation.content)
        assert score >= 4, f"Mensagem não é fluida: {message[:50]}... (score: {score})"
```

---

#### 2. `tests/integration/test_methodologist_smoke.py`
**Validar:**
- Perguntas são socráticas (não burocráticas)
- Decisões têm critérios claros (não arbitrárias)

**Exemplo:**
```python
@pytest.mark.llm_judge
def test_socratic_questions_quality(methodologist_graph, llm_judge):
    """Valida que perguntas do Metodologista são socráticas."""
    state = create_initial_methodologist_state(
        "Café aumenta produtividade"
    )
    
    result = methodologist_graph.invoke(state)
    
    if result.get("status") == "pending":
        clarifications = result.get("clarifications", {})
        
        for question in clarifications.keys():
            evaluation = llm_judge.invoke(
                SOCRATIC_QUESTION_PROMPT.format(question=question)
            )
            score = extract_score(evaluation.content)
            assert score >= 4, f"Pergunta não é socrática: {question} (score: {score})"
```

---

#### 3. `scripts/flows/validate_socratic_behavior.py` → Converter para teste automatizado
**Validar:**
- Provocação socrática genuína (expõe assumptions)
- Timing natural (não regras fixas)
- Parada inteligente (não insiste infinitamente)

**Exemplo:**
```python
@pytest.mark.llm_judge
def test_socratic_provocation_quality(orchestrator_node, llm_judge):
    """Valida que provocação socrática é genuína."""
    state = create_state_with_vague_metric(
        "Quero medir produtividade"
    )
    
    result = orchestrator_node(state)
    
    reflection_prompt = result.get("reflection_prompt", "")
    response = result.get("messages", [])[-1].content
    
    evaluation = llm_judge.invoke(
        SOCRATIC_BEHAVIOR_PROMPT.format(
            response=response,
            reflection_prompt=reflection_prompt
        )
    )
    score = extract_score(evaluation.content)
    assert score >= 4, f"Provocação não é socrática (score: {score})"
```

---

#### 4. `scripts/flows/validate_conversation_flow.py` → Converter para teste automatizado
**Validar:**
- Fluidez conversacional end-to-end
- Não há quebras entre transições

---

#### 5. `scripts/flows/validate_multi_agent_flow.py` → Converter para teste automatizado
**Validar:**
- Integração natural entre agentes
- Contexto preservado durante transições

---

#### 6. `scripts/flows/validate_refinement_loop.py` → Converter para teste automatizado
**Validar:**
- Refinamentos endereçam gaps de forma significativa
- Evolução é coerente (não apenas mudança cosmética)

---

## 📊 Estratégia de Execução

### Desenvolvimento Local
```bash
# Rodar apenas testes LLM-as-Judge
pytest -m llm_judge

# Rodar testes LLM-as-Judge + estruturais
pytest tests/integration/ -m "integration or llm_judge"
```

### CI/CD (futuro - não implementado)
- Rodar LLM-as-Judge apenas em PRs relevantes (quando toca código de agentes)
- Usar `ANTHROPIC_API_KEY` de teste via GitHub Secrets
- Limite de custo: ~$0.02 por PR

### Custo Estimado
- **Por teste LLM-as-Judge:** ~$0.001-0.002 (Haiku)
- **Suite completa (10-15 testes):** ~$0.01-0.02
- **CI/CD mensal (30 PRs):** ~$0.30-0.60

---

## 🎯 Critérios de Aceite do Épico 8

### 8.1 Infraestrutura Implementada
- [ ] Fixture `llm_judge` criada em `tests/conftest.py`
- [ ] 5 prompts de avaliação criados em `utils/test_prompts.py`
- [ ] Função `extract_score` criada em `utils/test_helpers.py`
- [ ] Marker `@pytest.mark.llm_judge` adicionado em `pytest.ini`
- [ ] Testes pulam se `ANTHROPIC_API_KEY` não está definida

### 8.2 Testes Automatizados Criados
- [ ] Testes adicionados em `test_multi_agent_smoke.py` (fluidez, integração)
- [ ] Testes adicionados em `test_methodologist_smoke.py` (socrático, decisões)
- [ ] Scripts de validação convertidos para testes automatizados:
  - [ ] `validate_socratic_behavior.py`
  - [ ] `validate_conversation_flow.py`
  - [ ] `validate_multi_agent_flow.py`
  - [ ] `validate_refinement_loop.py`
- [ ] Cada teste valida qualidade (score >= 4) além de estrutura
- [ ] Testes cobrem problemas identificados no Épico 7

### 8.3 Documentação Atualizada
- [ ] `docs/testing/strategy.md` atualizado com seção sobre LLM-as-Judge
- [ ] Custos estimados documentados (~$0.01-0.02 por execução)
- [ ] Estratégia de execução documentada (local, CI/CD)
- [ ] Como adicionar novos testes LLM-as-Judge documentado

---

## 📚 Referências

- `docs/testing/epic7_validation_strategy.md` - Validação manual (Fase 1)
- `docs/analysis/llm_judge_strategy.md` - Análise completa de estratégia
- `docs/testing/strategy.md` - Estratégia geral de testes

---

**Versão:** 1.0  
**Data:** Dezembro 2025  
**Relacionado:** ÉPICO 8 no ROADMAP

