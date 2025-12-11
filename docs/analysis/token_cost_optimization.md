# Análise: Otimização de Custos de Tokens

**Data:** 2025-01-27  
**Contexto:** Análise de oportunidades de economia de custos de tokens baseada na visão do produto  
**Última atualização:** Revisão completa do código atual para identificar status de implementação

---

## 📋 Resumo Executivo

**Oportunidades Críticas de Otimização:**

1. ⚠️ **Histórico não truncado no Orquestrador** - Envia todas as mensagens a cada turno
2. ⚠️ **max_tokens não aplicado** - Respostas podem ser mais longas que necessário
3. ⚠️ **JSON indentado em contextos** - Adiciona ~30% de tokens desnecessários
4. ⚠️ **Prompt muito longo** - ~615 linhas com exemplos redundantes

**Economia Potencial:** 40-60% em conversas longas (>10 turnos) com implementação da Fase 1.

---

## 🎯 Visão do Produto: Foco Estratégico

**Princípio central:** "Lapidar UMA ideia por conversa" (não assistente genérico)

Esta filosofia permite otimizações agressivas que não seriam possíveis em sistemas generalistas:

- ✅ **Foco estreito** = menos contexto necessário
- ✅ **Uma ideia por sessão** = histórico pode ser mais agressivamente truncado
- ✅ **Dialética socrática** = respostas curtas e provocativas (não explicações longas)
- ✅ **Agentes especializados** = cada um pode ter limites específicos

---

## 💰 Custos Atuais (USD por 1M tokens)

| Modelo | Input | Output | Ratio Output/Input |
|--------|-------|--------|-------------------|
| **Haiku** | $0.80 | $4.00 | 5x |
| **Sonnet** | $3.00 | $15.00 | 5x |
| **Opus** | $15.00 | $75.00 | 5x |

**Insight crítico:** Output é 5x mais caro que input. Reduzir tokens de saída tem impacto 5x maior.

---

## 🔍 Análise de Oportunidades

### 1. **Histórico de Conversas Cresce Indefinidamente** ⚠️ CRÍTICO

**Problema atual:**
```python
# agents/orchestrator/nodes.py:600
messages = state.get("messages", [])
if messages:
    context_parts.append("HISTÓRICO DA CONVERSA:")
    for msg in messages:  # ❌ TODAS as mensagens, sem limite
        context_parts.append(f"[Usuário]: {msg.content}")
```

**Impacto:**
- Conversas longas enviam todo o histórico a cada chamada
- 20 turnos = ~10k tokens de histórico repetido
- Custo acumula exponencialmente

**Solução recomendada:**
1. **Truncamento inteligente:** Últimas N mensagens + resumo do restante
2. **Resumo incremental:** A cada 10 turnos, resumir mensagens antigas
3. **Foco no argumento focal:** Usar `focal_argument` como contexto principal

**Economia estimada:** 30-50% em conversas longas (>10 turnos)

---

### 2. **Prompt do Orquestrador é Muito Longo** 📝 MÉDIO IMPACTO

**Problema atual:**
```python
# utils/prompts/orchestrator.py
ORCHESTRATOR_SOCRATIC_PROMPT_V1 = """Você é o Orquestrador Socrático...
[~615 linhas de prompt]
"""
```

**Análise:**
- Prompt tem ~615 linhas (~15k tokens)
- Múltiplos exemplos (7 exemplos completos)
- Instruções repetidas em diferentes seções
- Formato com muitas linhas em branco

**Oportunidades:**
1. **Consolidar exemplos:** Manter apenas 2-3 melhores (reduzir ~40%)
2. **Remover redundâncias:** Instruções repetidas sobre provocação socrática
3. **Formato mais denso:** Reduzir linhas em branco desnecessárias
4. **Seções opcionais:** Mover exemplos detalhados para referência externa

**Economia estimada:** 20-30% em tokens de input do prompt base (~3-4.5k tokens)

---

### 3. **JSON Indentado em Contextos** 📊 MÉDIO IMPACTO

**Problema atual:**
```python
# agents/orchestrator/nodes.py:633
context_parts.append(json.dumps(structurer_output, indent=2, ensure_ascii=False))
```

**Oportunidade:**
- `indent=2` adiciona ~30% de tokens (espaços/linhas)
- Para curadoria, formato compacto é suficiente
- Manter indent apenas para logs/debugging

**Economia estimada:** 5-10% em tokens de input

---

### 4. **Respostas do Orquestrador Não Têm max_tokens** ⚠️ ALTO IMPACTO

**Problema atual:**
```python
# agents/orchestrator/nodes.py:778-780
llm = create_anthropic_client(model=model_name, temperature=0)
messages = [HumanMessage(content=conversational_prompt)]
response = invoke_with_retry(llm=llm, messages=messages, agent_name="orchestrator")
# ❌ max_tokens não está sendo passado, mesmo com limite definido no YAML
```

**Análise:**
- YAML define `max_output_tokens: 1500` mas não é aplicado
- `create_anthropic_client()` suporta `max_tokens` mas não é usado
- Respostas podem ser mais longas que necessário para provocações socráticas
- Filosofia socrática: Provocações devem ser curtas e diretas (1-2 frases)

**Solução:**
```python
# agents/orchestrator/nodes.py
from agents.memory.config_loader import get_agent_context_limits

limits = get_agent_context_limits("orchestrator")
llm = create_anthropic_client(
    model=model_name, 
    temperature=0,
    max_tokens=limits["max_output_tokens"]  # ✅ Aplicar limite do YAML
)
```

**Economia estimada:** 20-30% em tokens de output (5x impacto = 100-150% equivalente)

---

**Problema atual:**
```python
# agents/orchestrator/nodes.py:633, 640, 750
json.dumps(structurer_output, indent=2, ensure_ascii=False)
json.dumps(methodologist_output, indent=2, ensure_ascii=False)
json.dumps(previous_focal, indent=2, ensure_ascii=False)
```

**Análise:**
- `indent=2` adiciona ~30% de tokens (espaços/linhas)
- Usado em 3+ locais no código
- Para curadoria, formato compacto é suficiente
- Indent só necessário para logs/debugging

**Solução:**
```python
# Para contexto (compacto):
json.dumps(data, ensure_ascii=False)  # Sem indent

# Para logs (legível):
json.dumps(data, indent=2, ensure_ascii=False)  # Com indent
```

**Economia estimada:** 5-10% em tokens de input (acumulado)

---

### 5. **Cache de Respostas Similares** 🔄 BAIXO IMPACTO (Futuro)

**Oportunidade:**
- Se usuário faz pergunta similar a anterior, retornar resposta cached
- Útil para perguntas frequentes sobre o sistema

**Complexidade:** Alta (requer sistema de cache + similaridade semântica)  
**Prioridade:** Baixa (foco em otimizações mais simples primeiro)

---

## 📊 Priorização de Implementação

### Fase 1: Quick Wins (Alto Impacto, Baixa Complexidade)
1. **Truncar histórico de conversas no Orquestrador** (últimas 10 mensagens + resumo)
2. **Aplicar max_tokens nas respostas do Orquestrador** (usar limite do YAML)
3. **JSON compacto em contextos** (sem indent em 3 locais)

**Economia estimada:** 40-60% em conversas longas

### Fase 2: Otimizações de Prompt (Médio Impacto, Média Complexidade)
4. **Otimizar prompt do Orquestrador** (reduzir de 615 para ~400 linhas)
   - Consolidar exemplos (7 → 3)
   - Remover redundâncias
   - Formato mais denso

**Economia estimada:** +20-30% adicional em tokens de input

### Fase 3: Otimizações Avançadas (Médio Impacto, Alta Complexidade)
5. **Resumo incremental de histórico** (a cada 10 turnos)
6. **Cache de respostas** (futuro)

---

## 🎯 Recomendações Específicas

### 1. Truncamento de Histórico

```python
# agents/orchestrator/nodes.py
def _build_context(state: MultiAgentState, max_recent_messages: int = 10) -> str:
    messages = state.get("messages", [])
    
    if len(messages) > max_recent_messages:
        # Últimas N mensagens completas
        recent = messages[-max_recent_messages:]
        # Resumo do restante
        old_summary = _summarize_old_messages(messages[:-max_recent_messages])
        context_parts.append(f"RESUMO DE CONVERSA ANTERIOR: {old_summary}")
        context_parts.append("HISTÓRICO RECENTE:")
        # ... adicionar recent
    else:
        # ... código atual
```

### 2. Aplicar max_tokens no Orquestrador

```python
# agents/orchestrator/nodes.py
from agents.memory.config_loader import get_agent_context_limits

# Carregar limites do YAML
limits = get_agent_context_limits("orchestrator")
max_output_tokens = limits.get("max_output_tokens", 1500)

# Aplicar na chamada
llm = create_anthropic_client(
    model=model_name, 
    temperature=0,
    max_tokens=max_output_tokens  # ✅ Usar limite do YAML
)
```

### 3. JSON Compacto em Contextos

```python
# agents/orchestrator/nodes.py
# ❌ ANTES (indentado):
context_parts.append(json.dumps(structurer_output, indent=2, ensure_ascii=False))

# ✅ DEPOIS (compacto):
context_parts.append(json.dumps(structurer_output, ensure_ascii=False))

# Para logs (manter indent):
logger.debug(f"Focal argument: {json.dumps(focal_argument, indent=2, ensure_ascii=False)}")
```

---

## 📈 Projeção de Economia

**Cenário base atual (conversa de 20 turnos):**
- Input: ~15k tokens/turno × 20 = 300k tokens
  - Prompt base: ~15k tokens (ORCHESTRATOR_SOCRATIC_PROMPT_V1)
  - Histórico completo: ~10k tokens (todos os turnos)
  - JSON indentado: ~1k tokens
- Output: ~500 tokens/turno × 20 = 10k tokens (sem limite)
- **Custo (Haiku):** $0.24 + $0.04 = **$0.28**

**Cenário otimizado (Fase 1 + 2):**
- Input: ~8k tokens/turno × 20 = 160k tokens
  - Prompt otimizado: ~10k tokens (redução de 33%)
  - Histórico truncado: ~3k tokens (últimas 10 + resumo)
  - JSON compacto: ~700 tokens (redução de 30%)
- Output: ~300 tokens/turno × 20 = 6k tokens (max_tokens aplicado)
- **Custo (Haiku):** $0.13 + $0.024 = **$0.154**

**Economia:** ~45% por conversa longa

---

## ✅ Checklist de Implementação

### Crítico (Fase 1)
- [ ] **Truncar histórico no Orquestrador** (`agents/orchestrator/nodes.py:600-620`)
  - Implementar lógica similar ao Observer (últimas 10 mensagens)
  - Adicionar resumo de mensagens antigas se > 10
- [ ] **Aplicar max_tokens no Orquestrador** (`agents/orchestrator/nodes.py:778`)
  - Carregar limite do YAML via `get_agent_context_limits("orchestrator")`
  - Passar `max_tokens` para `create_anthropic_client()`
- [ ] **JSON compacto em contextos** (`agents/orchestrator/nodes.py:633, 640, 750`)
  - Remover `indent=2` de contextos (manter apenas em logs)

### Importante (Fase 2)
- [ ] **Otimizar prompt do Orquestrador** (`utils/prompts/orchestrator.py`)
  - Reduzir exemplos de 7 para 3
  - Consolidar instruções repetidas
  - Formato mais denso (menos linhas em branco)

### Monitoramento
- [ ] Monitorar métricas de custo após mudanças
- [ ] Validar qualidade das respostas após otimizações
- [ ] Documentar trade-offs (qualidade vs custo)

---

## 🔗 Referências

- Visão do produto: `products/revelar/docs/vision.md`
- Cost tracker: `utils/cost_tracker.py`
- Orquestrador: `agents/orchestrator/nodes.py`
- Configurações: `config/agents/*.yaml`

