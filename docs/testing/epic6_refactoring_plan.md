# ÉPICO 6: Melhorar Testes - Integração Real + Validação de Qualidade

> **Objetivo:** Resolver débito técnico: adicionar testes de integração reais onde há mocks superficiais e validação de qualidade conversacional com LLM-as-Judge.

---

## 📋 Visão Geral

**Problema atual:**
- Testes com mocks superficiais não validam comportamento real (`test_orchestrator.py`, `test_structurer.py`)
- Testes verificam apenas estrutura (presença de campos), não qualidade
- Comportamento socrático impossível de testar deterministicamente
- Sem garantia de que transições são realmente "fluidas"
- Sem validação de que perguntas são socráticas vs burocráticas

**Solução:**
1. **Adicionar testes de integração reais** onde há mocks superficiais (comportamento real)
2. **Implementar infraestrutura LLM-as-Judge** (validação de qualidade)
3. **ADICIONAR** validação de qualidade em 6 testes prioritários (conforme `llm_judge_strategy.md`)
4. Manter testes unitários existentes (estrutura) + adicionar camadas de validação

---

## 🎯 Arquivos a Melhorar

### Fase 1: Adicionar Testes de Integração Reais

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

### Fase 2: Adicionar Validação LLM-as-Judge

> **Nota:** Estes arquivos foram identificados em `docs/analysis/llm_judge_strategy.md` como candidatos prioritários para LLM-as-Judge. O objetivo é **ADICIONAR** validação de qualidade, não refatorar completamente.

#### Prioridade ALTA (6 arquivos)

#### 1. `tests/integration/test_multi_agent_smoke.py`

**Problema atual:**
```python
def test_vague_idea_full_flow(multi_agent_graph):
    result = multi_agent_graph.invoke(state)
    assert result["orchestrator_analysis"] is not None  # ❌ Aceita qualquer coisa!
    assert result["next_step"] in ["explore", "suggest_agent", "clarify"]  # ❌ Muito fraco!
```

**Refatoração:**
```python
@pytest.mark.llm_judge
def test_vague_idea_full_flow_quality(multi_agent_graph, llm_judge):
    """Valida qualidade da experiência conversacional end-to-end."""
    result = multi_agent_graph.invoke(state)
    
    # Validação estrutural (mantém)
    assert result["orchestrator_analysis"] is not None
    assert result["next_step"] in ["explore", "suggest_agent", "clarify"]
    
    # Validação de qualidade (NOVO)
    evaluation = llm_judge.invoke(
        CONVERSATION_QUALITY_PROMPT.format(
            response=result.get("messages", [])[-1].content if result.get("messages") else "",
            history=result.get("conversation_history", []),
            orchestrator_analysis=result.get("orchestrator_analysis", "")
        )
    )
    score = extract_score(evaluation.content)
    assert score >= 4, f"Experiência conversacional não é suficientemente fluida (score: {score})"
```

**O que validar:**
- Fluidez (sem "Posso chamar X?")
- Integração natural de outputs
- Confirmação de entendimento

---

#### 2. `tests/integration/test_methodologist_smoke.py`

**Problema atual:**
```python
def test_methodologist_flow():
    result = methodologist_graph.invoke(state)
    assert result["status"] in ["approved", "rejected", "pending"]  # ❌ Aceita qualquer decisão!
```

**Adicionar validação LLM-as-Judge:**
```python
@pytest.mark.llm_judge
def test_methodologist_questions_quality(methodologist_graph, llm_judge):
    """Valida que perguntas são socráticas, não burocráticas."""
    result = methodologist_graph.invoke(state)
    
    if result.get("status") == "pending":
        # Validar qualidade das perguntas
        clarifications = result.get("clarifications", [])
        for question in clarifications:
            evaluation = llm_judge.invoke(
                SOCRATIC_QUESTION_PROMPT.format(question=question)
            )
            score = extract_score(evaluation.content)
            assert score >= 4, f"Pergunta não é suficientemente socrática: {question} (score: {score})"
```

**O que validar:**
- Perguntas são socráticas (expõem assumptions) vs burocráticas
- Timing natural (não regras fixas)

---

#### 3. `scripts/flows/validate_socratic_behavior.py`

**Problema atual:**
- Valida apenas presença de palavras-chave (regex/contains)
- Não valida qualidade da provocação

**Adicionar validação LLM-as-Judge:**
```python
@pytest.mark.llm_judge
def test_socratic_provocation_quality():
    """Valida que provocação é genuinamente socrática."""
    result = orchestrator_node(state)
    
    evaluation = llm_judge.invoke(
        SOCRATIC_BEHAVIOR_PROMPT.format(
            response=result.get("messages", [])[-1].content,
            reflection_prompt=result.get("reflection_prompt", "")
        )
    )
    score = extract_score(evaluation.content)
    assert score >= 4, f"Provocação não é suficientemente socrática (score: {score})"
```

**O que validar:**
- Provocação expõe assumptions (não coleta burocrática)
- Timing é natural (não regras fixas)
- Parada é inteligente (não insiste infinitamente)

---

#### 4. `scripts/flows/validate_conversation_flow.py`

**Problema atual:**
- Valida apenas regex/contains
- Não valida fluidez real

**Adicionar validação LLM-as-Judge:**
```python
@pytest.mark.llm_judge
def test_conversation_fluidity():
    """Valida fluidez conversacional (sem "Posso chamar X?")."""
    # Executar fluxo conversacional
    result = multi_agent_graph.invoke(state)
    
    # Validar que não há perguntas de permissão
    messages = result.get("messages", [])
    for msg in messages:
        if isinstance(msg, AIMessage):
            evaluation = llm_judge.invoke(
                FLUENCY_PROMPT.format(message=msg.content)
            )
            score = extract_score(evaluation.content)
            assert score >= 4, f"Mensagem não é suficientemente fluida: {msg.content[:50]}... (score: {score})"
```

**O que validar:**
- Sem "Posso chamar X?"
- Integração natural de outputs
- Confirmação de entendimento

---

#### 5. `scripts/flows/validate_multi_agent_flow.py`

**Problema atual:**
- Valida apenas estrutura
- Não valida qualidade da integração

**Adicionar validação LLM-as-Judge:**
```python
@pytest.mark.llm_judge
def test_multi_agent_integration_quality():
    """Valida que transições entre agentes são naturais."""
    result = multi_agent_graph.invoke(state)
    
    evaluation = llm_judge.invoke(
        INTEGRATION_QUALITY_PROMPT.format(
            orchestrator_output=result.get("orchestrator_analysis", ""),
            structurer_output=result.get("structurer_output", {}).get("structured_question", ""),
            methodologist_output=result.get("methodologist_output", {}).get("status", ""),
            messages=[msg.content for msg in result.get("messages", []) if isinstance(msg, AIMessage)]
        )
    )
    score = extract_score(evaluation.content)
    assert score >= 4, f"Integração entre agentes não é suficientemente natural (score: {score})"
```

**O que validar:**
- Transições são naturais
- Contexto preservado
- Experiência coesa

---

#### 6. `scripts/flows/validate_refinement_loop.py`

**Problema atual:**
- Valida apenas que gaps foram endereçados
- Não valida qualidade das melhorias

**Adicionar validação LLM-as-Judge:**
```python
@pytest.mark.llm_judge
def test_refinement_quality():
    """Valida que refinamentos endereçam gaps de forma significativa."""
    # Executar loop de refinamento
    initial = structurer_node(state)
    refined = structurer_refinement_node(state)
    
    evaluation = llm_judge.invoke(
        REFINEMENT_QUALITY_PROMPT.format(
            initial_question=initial.get("structured_question", ""),
            refined_question=refined.get("structured_question", ""),
            gaps=initial.get("gaps", [])
        )
    )
    score = extract_score(evaluation.content)
    assert score >= 4, f"Refinamento não endereça gaps de forma significativa (score: {score})"
```

**O que validar:**
- Refinamentos endereçam gaps significativamente
- Evolução é coerente

---

## 🛠️ Infraestrutura Necessária

### 1. Fixture LLM-as-Judge (`tests/conftest.py`)

```python
@pytest.fixture
def llm_judge():
    """Fixture para LLM-as-judge (avaliador de qualidade)."""
    import os
    from langchain_anthropic import ChatAnthropic
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        pytest.skip("LLM-as-judge test skipped: ANTHROPIC_API_KEY not set")
    
    return ChatAnthropic(
        model="claude-3-5-haiku-20241022",  # Custo-benefício
        temperature=0  # Determinístico
    )
```

### 2. Prompts de Avaliação (`utils/test_prompts.py`)

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

CONVERSATION_QUALITY_PROMPT = """
Avalie a qualidade da conversação:

1. Fluidez (sem "Posso chamar X?", integração natural)
2. Confirmação de entendimento
3. Coerência com contexto

Resposta: {response}
Histórico: {history}
Análise do orquestrador: {orchestrator_analysis}

Avalie de 1-5 (5 = excelente experiência conversacional):
Justificativa:
"""

SOCRATIC_QUESTION_PROMPT = """
Avalie se a pergunta é socrática (expõe assumptions) ou burocrática (coleta informação):

Pergunta: {question}

Avalie de 1-5 (5 = pergunta genuinamente socrática):
Justificativa:
"""

FLUENCY_PROMPT = """
Avalie a fluidez da mensagem:

1. Não pergunta permissão ("Posso chamar X?")
2. Integração natural
3. Tom conversacional

Mensagem: {message}

Avalie de 1-5 (5 = completamente fluida):
Justificativa:
"""

INTEGRATION_QUALITY_PROMPT = """
Avalie a qualidade da integração entre agentes:

1. Transições naturais
2. Contexto preservado
3. Experiência coesa

Orquestrador: {orchestrator_output}
Estruturador: {structurer_output}
Metodologista: {methodologist_output}
Mensagens: {messages}

Avalie de 1-5 (5 = integração excelente):
Justificativa:
"""

REFINEMENT_QUALITY_PROMPT = """
Avalie a qualidade do refinamento:

1. Endereça gaps de forma significativa
2. Evolução coerente
3. Melhoria real (não apenas mudança cosmética)

Questão inicial: {initial_question}
Questão refinada: {refined_question}
Gaps identificados: {gaps}

Avalie de 1-5 (5 = refinamento excelente):
Justificativa:
"""
```

### 3. Função Helper (`utils/test_helpers.py`)

```python
import re

def extract_score(evaluation_content: str) -> int:
    """Extrai score (1-5) da avaliação do LLM-as-judge."""
    # Procura por padrões como "5", "score: 4", "Avalie de 1-5: 3"
    patterns = [
        r"Avalie de 1-5.*?(\d)",
        r"score.*?(\d)",
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

### 4. Marker no `pytest.ini`

```ini
[pytest]
markers =
    unit: Testes unitários (mocks)
    integration: Testes de integração (API real)
    llm_judge: Testes que usam LLM-as-judge (requer API key)
```

---

## 📊 Estratégia de Execução

### Desenvolvimento Local
```bash
# Rodar apenas testes LLM-as-Judge
pytest -m llm_judge

# Rodar todos os testes (incluindo LLM-as-Judge)
pytest tests/
```

### Estratégia de Execução

**Desenvolvimento Local:**
- Rodar seletivamente: `pytest -m llm_judge`
- Requer `ANTHROPIC_API_KEY` no ambiente
- Pode ser pulado (skip automático se chave não estiver definida)

**CI/CD (futuro - não implementado):**
- Atualmente não há workflow para testes de integração
- Quando implementado: rodar apenas em PRs relevantes, usar chave de teste via GitHub Secrets

### Custo Estimado
- Por execução de teste LLM-as-Judge: ~$0.001-0.002 (usando Haiku)
- Suite completa (6 testes): ~$0.01-0.02 por execução

---

## ✅ Critérios de Aceite

### Testes de Integração Reais (6.1)
- [ ] Criar `tests/integration/test_orchestrator_integration.py` com testes de classificação real
- [ ] Criar `tests/integration/test_structurer_integration.py` com testes de estruturação real
- [ ] Testes devem usar API real (não mocks)
- [ ] Testes devem validar comportamento real (não apenas estrutura)
- [ ] Manter testes unitários existentes (não remover)

### Infraestrutura LLM-as-Judge (6.2)
- [ ] Fixture `llm_judge` criada em `tests/conftest.py`
- [ ] Prompts de avaliação criados em `utils/test_prompts.py`
- [ ] Função `extract_score` criada em `utils/test_helpers.py`
- [ ] Marker `@pytest.mark.llm_judge` adicionado em `pytest.ini`

### Validação de Qualidade (6.3)
- [ ] `test_multi_agent_smoke.py` - Adicionar validação de qualidade conversacional
- [ ] `test_methodologist_smoke.py` - Adicionar validação de perguntas socráticas
- [ ] `validate_socratic_behavior.py` - Adicionar validação de provocação socrática
- [ ] `validate_conversation_flow.py` - Adicionar validação de fluidez
- [ ] `validate_multi_agent_flow.py` - Adicionar validação de integração
- [ ] `validate_refinement_loop.py` - Adicionar validação de refinamento

### Documentação (6.4)
- [ ] Atualizar `docs/testing/strategy.md` com seção sobre testes de integração reais e LLM-as-Judge
- [ ] Documentar custos estimados
- [ ] Documentar estratégia de execução (local: `pytest -m integration`, `pytest -m llm_judge`)

---

## 📝 Notas de Implementação

### Ordem de Implementação Recomendada

1. **Testes de integração reais primeiro** (6.1)
   - Criar `test_orchestrator_integration.py` e `test_structurer_integration.py`
   - Validar comportamento real (não mocks)
   - Resolve débito técnico imediato

2. **Infraestrutura LLM-as-Judge** (6.2)
   - Criar fixture, prompts, helper
   - Testar com um teste simples antes de adicionar nos 6 arquivos

3. **Validação de qualidade** (6.3)
   - Começar com `test_multi_agent_smoke.py` e `test_methodologist_smoke.py`
   - São mais simples (já são testes de integração)
   - **ADICIONAR** função de teste com `@pytest.mark.llm_judge` (não substituir teste existente)
   - Depois adicionar nos scripts de validação (itens 3-6)

### Manter Testes Existentes

- **NÃO remover** testes existentes (validam estrutura)
- **ADICIONAR** novos testes com validação de qualidade (LLM-as-Judge)
- Testes estruturais + testes de qualidade = cobertura completa

---

**Versão:** 2.0  
**Data:** Dezembro 2025  
**Relacionado:** ÉPICO 6 no ROADMAP

---

## 📝 Nota sobre Débito Técnico

Este épico resolve débito técnico identificado na análise de testes:
- **Mocks superficiais** → Adicionar testes de integração reais (Fase 1)
- **Asserts fracos** → Adicionar validação de qualidade (Fase 2)

**Não jogar para backlog:** Testes que não agregam valor devem ser corrigidos ou removidos, não ignorados.

