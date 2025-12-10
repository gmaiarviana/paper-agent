# Statement do Problema: Agente de Memória para Otimização de Contexto

**Data:** 2025-01-27  
**Contexto:** Otimização de uso de tokens através de seleção inteligente de contexto  
**Status:** Proposta arquitetural para discussão

---

## 🎯 Problema Atual

### Situação

O Orquestrador envia **TODO o histórico de mensagens** a cada turno para o LLM:

```python
# agents/orchestrator/nodes.py:600-620
def _build_context(state: MultiAgentState) -> str:
    messages = state.get("messages", [])
    if messages:
        context_parts.append("HISTÓRICO DA CONVERSA:")
        for msg in messages:  # ❌ TODAS as mensagens, sem limite
            context_parts.append(f"[Usuário]: {msg.content}")
```

### Impacto

- **Conversas longas (>10 turnos):** ~10k tokens de histórico repetido a cada chamada
- **Custo exponencial:** 20 turnos = 200k tokens de histórico acumulado
- **Dilema:**
  - ❌ Truncar tudo = risco de perder detalhes importantes
  - ❌ Manter tudo = custo proibitivo

### Infraestrutura Existente

**Já temos:**
- ✅ **Observer:** Extrai semântica (claims, conceitos, proposições)
- ✅ **Cognitive Model:** Representação condensada do argumento (já limitado: 5 proposições, 10 conceitos)
- ✅ **focal_argument:** Resumo estruturado (intent, subject, population, metrics)
- ✅ **Embeddings:** Observer já extrai conceitos (pode usar para busca semântica)

**Não temos:**
- ❌ Seleção inteligente de mensagens relevantes
- ❌ Agente dedicado para gerenciar memória/contexto
- ❌ Mecanismo para recuperar mensagens antigas por relevância semântica

---

## 💡 Proposta: Agente de Memória Dedicado

### Arquitetura Proposta

```
┌─────────────┐
│ Orquestrador│ ──> "Preciso contexto para responder ao usuário"
└─────────────┘
       │
       v
┌─────────────┐
│ Memory Agent│ ──> Seleciona contexto relevante
│             │     1. Analisa user_input atual
│             │     2. Identifica conceitos-chave (via Observer)
│             │     3. Busca mensagens relevantes (semântica + temporal)
│             │     4. Retorna contexto otimizado
└─────────────┘
       │
       v
┌─────────────┐
│   Contexto  │ ──> Apenas mensagens relevantes
│  Selecionado│     + Cognitive Model (já condensado)
│             │     + focal_argument (resumo estruturado)
└─────────────┘
```

### Responsabilidades do Memory Agent

1. **Seleção Temporal:**
   - Últimas N mensagens (sempre recente)
   - Mensagens antigas apenas se relevantes

2. **Seleção Semântica:**
   - Usar conceitos do Cognitive Model
   - Buscar mensagens por similaridade (embeddings)
   - Priorizar mensagens que mencionam conceitos-chave

3. **Resumo Incremental:**
   - A cada 10 turnos, resumir mensagens antigas
   - Manter resumo + últimas N mensagens completas

4. **Preservação de Detalhes:**
   - Mensagens que definem conceitos importantes (não perder)
   - Mensagens que estabelecem contexto (população, métricas)
   - Mensagens que resolvem contradições

### Interface Proposta

```python
class MemoryAgent:
    def select_context(
        self,
        user_input: str,
        all_messages: List[Message],
        cognitive_model: Dict[str, Any],
        focal_argument: Dict[str, Any],
        max_tokens: int = 4000
    ) -> Dict[str, Any]:
        """
        Seleciona contexto relevante para o Orquestrador.
        
        Returns:
            {
                "recent_messages": List[Message],  # Últimas 10
                "relevant_old_messages": List[Message],  # Por semântica
                "summary_old_messages": str,  # Resumo de mensagens antigas
                "cognitive_model_snapshot": Dict,  # Já limitado
                "focal_argument": Dict,  # Resumo estruturado
                "selection_reasoning": str  # Por que selecionou essas mensagens
            }
        """
```

---

## ⚖️ Trade-offs

### Prós

✅ **Seleção Contextual Inteligente**
- Não perde detalhes importantes
- Remove ruído de mensagens irrelevantes
- Escalável para conversas muito longas

✅ **Economia de Tokens**
- Envia apenas o necessário
- Reduz custo exponencialmente em conversas longas
- Mantém qualidade (não perde contexto relevante)

✅ **Separação de Responsabilidades**
- Memory Agent = gerenciar contexto
- Orchestrator = facilitar conversa
- Observer = extrair semântica

### Contras

❌ **Complexidade Adicional**
- Novo agente para manter
- Nova interface para testar
- Mais pontos de falha

❌ **Custo de Seleção**
- Se usar LLM para seleção: custo adicional
- Se usar embeddings: latência adicional
- Trade-off: custo de seleção vs economia de tokens

❌ **Risco de Seleção Errada**
- Pode omitir mensagem importante
- Pode incluir mensagem irrelevante
- Requer validação/testes extensivos

---

## 🔍 Questões para Decisão

### 1. Método de Seleção

**Opção A: LLM-based (mais inteligente, mais caro)**
- LLM analisa user_input e seleciona mensagens relevantes
- Custo: ~500-1000 tokens por seleção
- Vantagem: Entende contexto semântico profundo

**Opção B: Embedding-based (mais rápido, menos inteligente)**
- Busca por similaridade de embeddings
- Custo: ~100 tokens (apenas busca)
- Vantagem: Rápido e barato

**Opção C: Híbrida**
- Embeddings para pré-seleção
- LLM para validação/refinamento
- Custo: ~300-500 tokens

### 2. Quando Selecionar

**Opção A: Sempre (todo turno)**
- Máxima otimização
- Custo de seleção em todo turno

**Opção B: Condicional (apenas se >N mensagens)**
- Seleção apenas quando necessário
- Exemplo: Se >15 mensagens, então seleciona

**Opção C: Incremental (a cada N turnos)**
- Resumo a cada 10 turnos
- Seleção apenas quando histórico cresce muito

### 3. Integração com Observer

**Opção A: Memory Agent independente**
- Não depende do Observer
- Pode usar Observer como fonte de conceitos

**Opção B: Memory Agent como extensão do Observer**
- Observer já tem semântica
- Memory Agent usa Cognitive Model do Observer

**Opção C: Observer como Memory Agent**
- Observer assume responsabilidade de seleção
- Menos separação de responsabilidades

---

## 📊 Estimativa de Impacto

### Cenário: Conversa de 20 turnos

**Atual (sem seleção):**
- Input: ~15k tokens/turno (histórico completo)
- 20 turnos = 300k tokens de input
- Custo: $0.24 (Haiku)

**Com Memory Agent (seleção inteligente):**
- Input: ~8k tokens/turno (contexto selecionado)
- 20 turnos = 160k tokens de input
- Custo de seleção: ~200 tokens × 20 = 4k tokens (se embedding-based)
- **Total: 164k tokens = $0.13**
- **Economia: ~45%**

**Com Memory Agent (LLM-based):**
- Custo de seleção: ~800 tokens × 20 = 16k tokens
- **Total: 176k tokens = $0.14**
- **Economia: ~42%**

---

## 🎯 Recomendação Inicial

### Fase 1: MVP Simples (sem novo agente)

1. **Truncamento inteligente básico:**
   - Últimas 10 mensagens (sempre)
   - Cognitive Model (já condensado)
   - focal_argument (resumo estruturado)

2. **Avaliar impacto:**
   - Medir economia real
   - Validar que não perde contexto crítico

### Fase 2: Memory Agent (se necessário)

Se Fase 1 não for suficiente:

1. **Memory Agent com embeddings:**
   - Busca semântica por conceitos
   - Custo baixo (~100 tokens)
   - Implementação simples

2. **Avaliar necessidade de LLM:**
   - Se embeddings não forem suficientes
   - Adicionar LLM para refinamento

---

## ❓ Questões para Discussão

1. **Vale a pena a complexidade?**
   - Truncamento simples resolve 80% do problema?
   - Memory Agent resolve os 20% restantes?

2. **Qual método de seleção?**
   - Embeddings são suficientes?
   - LLM é necessário para qualidade?

3. **Quando implementar?**
   - Agora (otimização crítica)?
   - Depois (após validar truncamento simples)?

4. **Como validar?**
   - Métricas de qualidade (não perder contexto)?
   - Métricas de economia (tokens reduzidos)?

---

## 📚 Referências

- Arquitetura atual: `agents/orchestrator/nodes.py:_build_context()`
- Observer: `agents/observer/` (já extrai semântica)
- Cognitive Model: `agents/models/cognitive_model.py`
- Análise de tokens: `docs/analysis/token_cost_optimization.md`

