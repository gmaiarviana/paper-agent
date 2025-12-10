# Análise: Otimização de Custos de Tokens

**Data:** 2025-01-XX  
**Contexto:** Análise de oportunidades de economia de custos de tokens baseada na visão do produto

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

### 2. **Metodologista Usa Sonnet (5x Mais Caro)** ⚠️ ALTO IMPACTO

**Situação atual:**
```yaml
# config/agents/methodologist.yaml:69
model: claude-sonnet-4-20250514  # $3/$15 por 1M tokens
```

**Análise:**
- Metodologista valida hipóteses (tarefa estruturada)
- Haiku pode ser suficiente para validação estruturada
- Sonnet só necessário se raciocínio muito complexo

**Recomendação:**
1. **Testar Haiku primeiro:** Validar se qualidade é suficiente
2. **Fallback para Sonnet:** Apenas se Haiku falhar consistentemente
3. **Híbrido:** Haiku para validação simples, Sonnet para casos complexos

**Economia estimada:** 80% do custo do Metodologista (se migrar para Haiku)

---

### 3. **Prompts Podem Ser Mais Concisos** 📝 MÉDIO IMPACTO

**Exemplo atual:**
```python
# utils/prompts/orchestrator.py:14
ORCHESTRATOR_SOCRATIC_PROMPT_V1 = """Você é o Orquestrador Socrático...
[~600 linhas de prompt]
"""
```

**Oportunidades:**
- Remover exemplos redundantes (manter apenas 1-2 melhores)
- Consolidar instruções repetidas
- Usar formato mais denso (menos linhas em branco)

**Economia estimada:** 10-15% em tokens de input

---

### 4. **Limites de Cognitive Model Já Existem** ✅ BOM

**Implementação atual:**
```python
# agents/orchestrator/nodes.py:243-247
# Limites para evitar sobrecarga do prompt:
# - Proposições: 5 primeiras (ordenadas por solidez)
# - Conceitos: 10 primeiros
# - Contradições: 3 primeiras
# - Questões abertas: 5 primeiras
```

**Status:** ✅ Já otimizado. Manter como está.

---

### 5. **Outputs de Agentes em JSON Completo** 📊 MÉDIO IMPACTO

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

### 6. **Respostas do Orquestrador Podem Ser Mais Curtas** 💬 ALTO IMPACTO

**Filosofia socrática:** Provocações devem ser curtas e diretas.

**Recomendação:**
- Adicionar `max_tokens` explícito nas chamadas
- Prompt: "Seja conciso. Provocações devem ter 1-2 frases."
- Limitar output a 300-500 tokens (suficiente para provocação)

**Economia estimada:** 20-30% em tokens de output (5x impacto = 100-150% equivalente)

---

### 7. **Cache de Respostas Similares** 🔄 BAIXO IMPACTO (Futuro)

**Oportunidade:**
- Se usuário faz pergunta similar a anterior, retornar resposta cached
- Útil para perguntas frequentes sobre o sistema

**Complexidade:** Alta (requer sistema de cache + similaridade semântica)  
**Prioridade:** Baixa (foco em otimizações mais simples primeiro)

---

## 📊 Priorização de Implementação

### Fase 1: Quick Wins (Alto Impacto, Baixa Complexidade)
1. ✅ **Truncar histórico de conversas** (últimas 10 mensagens + resumo)
2. ✅ **Adicionar max_tokens nas respostas do Orquestrador** (300-500 tokens)
3. ✅ **JSON compacto** (sem indent em contexto)

**Economia estimada:** 40-60% em conversas longas

### Fase 2: Testes de Modelo (Alto Impacto, Média Complexidade)
4. ✅ **Testar Haiku no Metodologista** (validar qualidade)
5. ✅ **Otimizar prompts** (remover redundâncias)

**Economia estimada:** +20-30% adicional

### Fase 3: Otimizações Avançadas (Médio Impacto, Alta Complexidade)
6. ⏳ **Resumo incremental de histórico** (a cada 10 turnos)
7. ⏳ **Cache de respostas** (futuro)

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

### 2. Limitar Output do Orquestrador

```python
# agents/orchestrator/nodes.py
response = llm.invoke(
    messages,
    max_tokens=400  # Provocações curtas (socrático)
)
```

### 3. Testar Haiku no Metodologista

```yaml
# config/agents/methodologist.yaml
model: claude-3-5-haiku-20241022  # Testar primeiro
# Fallback para Sonnet apenas se necessário
```

---

## 📈 Projeção de Economia

**Cenário base (conversa de 20 turnos):**
- Input: ~15k tokens/turno × 20 = 300k tokens
- Output: ~500 tokens/turno × 20 = 10k tokens
- **Custo (Haiku):** $0.24 + $0.04 = **$0.28**

**Cenário otimizado (Fase 1 + 2):**
- Input: ~8k tokens/turno × 20 = 160k tokens (truncamento + JSON compacto)
- Output: ~300 tokens/turno × 20 = 6k tokens (max_tokens)
- **Custo (Haiku):** $0.13 + $0.024 = **$0.154**

**Economia:** ~45% por conversa longa

**Se Metodologista migrar para Haiku:**
- Economia adicional: ~80% do custo do Metodologista
- **Total:** ~60-70% de economia em sessões completas

---

## ✅ Checklist de Implementação

- [ ] Implementar truncamento de histórico (últimas 10 + resumo)
- [ ] Adicionar max_tokens=500 nas respostas do Orquestrador
- [ ] JSON compacto em contextos (sem indent)
- [ ] Migrar Metodologista para Haiku
- [ ] Otimizar prompts (remover redundâncias)
- [ ] Monitorar métricas de custo após mudanças
- [ ] Documentar trade-offs (qualidade vs custo)

---

## 🔗 Referências

- Visão do produto: `docs/vision/vision.md`
- Cost tracker: `utils/cost_tracker.py`
- Orquestrador: `agents/orchestrator/nodes.py`
- Configurações: `config/agents/*.yaml`

