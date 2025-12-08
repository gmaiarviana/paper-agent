# Épico 12: Observer - Integração Básica (MVP)

## Contexto

O Observer já está implementado em `agents/observer/` mas não integrado ao fluxo principal. Este épico integra o Observer ao multi-agent graph de forma que processe cada turno automaticamente em background, enriquecendo o Orquestrador com cognitive_model sem adicionar latência perceptível.

## Decisões Técnicas (Spikes 2025-12-08)

### Spike 1: Paralelismo LangGraph
**Resultado:** ❌ NÃO suportado
- `add_edge(START, ["orchestrator", "observer"])` falhou
- Erro: `unhashable type: 'list'`
- **Decisão:** Usar callback assíncrono (threading)

### Spike 2: CognitiveModel via Prompt
**Resultado:** ✅ VIÁVEL (80% score)
- Claude usa cognitive_model naturalmente via prompt
- Mencionou: solidez, completude, contradições, conceitos
- **Decisão:** Leitura de estado é SUFICIENTE (sem tool explícita)

## Arquitetura

### Fluxo Proposto
```
User input
↓
[Orchestrator] → Response (3s, latência principal)
↓
[Observer callback] → Background thread (2s, assíncrono)
↓
Atualiza state["cognitive_model"]
↓
Publica CognitiveModelUpdatedEvent
```

### Componentes Afetados

1. **`agents/multi_agent_graph.py`:**
   - Adicionar Observer como nó
   - Implementar callback assíncrono via modificação do `instrument_node` para orchestrator

2. **`agents/orchestrator/nodes.py`:**
   - Prompt atualizado para mencionar cognitive_model disponível
   - Claude analisa cognitive_model naturalmente no reasoning

3. **`agents/observer/nodes.py`:**
   - Já implementado, sem mudanças necessárias
   - Função `process_turn()` pronta para uso

4. **`app/components/backstage/timeline.py`:**
   - Adicionar indicador visual quando Observer processar turno
   - Consome evento `cognitive_model_updated` do EventBus

## Entregas

### 12.1: Callback Assíncrono Observer

**Objetivo:** Observer roda automaticamente após cada turno do Orquestrador (background)

**Implementação:**
```python
# agents/multi_agent_graph.py

import threading
from agents.observer.nodes import process_turn
from utils.event_bus import get_event_bus

def _create_observer_callback(state: MultiAgentState) -> None:
    """Executa Observer em background após turno do Orquestrador"""
    def _run_observer():
        try:
            # Extrair dados necessários do state
            user_input = state.get("user_input", "")
            conversation_history = state.get("conversation_history", [])
            previous_cognitive_model = state.get("cognitive_model")
            session_id = state.get("session_id", "unknown-session")
            turn_number = state.get("turn_count", 1)
            
            # Processar turno via Observer
            result = process_turn(
                user_input=user_input,
                conversation_history=conversation_history,
                previous_cognitive_model=previous_cognitive_model,
                session_id=session_id,
                turn_number=turn_number,
                idea_id=state.get("idea_id")  # Opcional
            )
            
            # Atualizar estado (thread-safe via lock ou state manager)
            # NOTA: LangGraph state pode ser thread-safe dependendo do checkpoint
            # Para MVP, usar acesso direto ao state (testar comportamento)
            cognitive_model = result.get("cognitive_model", {})
            state["cognitive_model"] = cognitive_model
            
            # Publicar evento via EventBus
            try:
                bus = get_event_bus()
                bus.publish_cognitive_model_updated(
                    session_id=session_id,
                    turn_number=turn_number,
                    solidez=cognitive_model.get("overall_solidez", 0.0),
                    completude=cognitive_model.get("overall_completude", 0.0),
                    claims_count=1 if cognitive_model.get("claim") else 0,
                    proposicoes_count=len(cognitive_model.get("proposicoes", [])),
                    concepts_count=len(cognitive_model.get("concepts_detected", [])),
                    open_questions_count=len(cognitive_model.get("open_questions", [])),
                    contradictions_count=len(cognitive_model.get("contradictions", [])),
                    is_mature=cognitive_model.get("overall_solidez", 0.0) > 0.70,
                    metadata={
                        "processing_time_ms": result.get("processing_time_ms", 0),
                        "observer_version": "1.0"
                    }
                )
            except Exception as e:
                logger.warning(f"Falha ao publicar evento Observer: {e}")
                
        except Exception as e:
            logger.error(f"Erro ao executar Observer em background: {e}")
    
    # Executar em thread separada (daemon = True para não bloquear shutdown)
    thread = threading.Thread(target=_run_observer, daemon=True)
    thread.start()
    logger.debug(f"Observer iniciado em background thread (session: {session_id})")

# Modificar instrument_node para adicionar callback após orchestrator
def instrument_node(node_func: Callable, agent_name: str) -> Callable:
    """Wrapper existente modificado para incluir Observer callback"""
    def wrapper(state: MultiAgentState, config: Optional[RunnableConfig] = None) -> MultiAgentState:
        # ... código existente de instrumentação ...
        
        # Executar nó original
        try:
            result = node_func(state, config)
            
            # ... código existente de eventos ...
            
            # DISPARAR OBSERVER APÓS ORCHESTRATOR
            if agent_name == "orchestrator":
                _create_observer_callback(result)  # Usar result (state atualizado)
            
            return result
        except Exception as error:
            # ... código existente de tratamento de erro ...
```

**Considerações:**
- Thread daemon não bloqueia shutdown do processo
- State atualização: Verificar se LangGraph state é thread-safe
- Fallback: Se state não for thread-safe, usar evento assíncrono para atualização

**Testes:**
- `tests/unit/test_observer_callback.py`: Testa callback disparado após orchestrator
- `tests/integration/test_observer_state_update.py`: Valida atualização de state em thread separada
- `tests/integration/test_observer_event_publishing.py`: Verifica publicação de eventos

**Validação:**
```bash
python scripts/validate_observer_integration.py
# Espera: Observer processa em <3s após resposta do Orquestrador
# Espera: cognitive_model atualizado no state
# Espera: Evento publicado no EventBus
```

---

### 12.2: CognitiveModel no Estado e Prompt do Orquestrador

**Objetivo:** Orquestrador acessa cognitive_model via prompt e usa naturalmente

**Implementação:**

1. **Garantir que cognitive_model está no MultiAgentState:**
   - Campo já existe em `agents/orchestrator/state.py` (linha 114)
   - Tipo: `Optional[dict]`
   - Inicializado como `None`

2. **Atualizar prompt do Orquestrador:**
```python
# agents/orchestrator/nodes.py

def _build_context(state: MultiAgentState) -> str:
    """Constrói contexto incluindo cognitive_model quando disponível"""
    context_parts = []
    
    # ... código existente de contexto ...
    
    # ADICIONAR SEÇÃO DE COGNITIVE MODEL
    cognitive_model = state.get("cognitive_model")
    if cognitive_model:
        context_parts.append(_build_cognitive_model_context(cognitive_model))
    
    return "\n".join(context_parts)

def _build_cognitive_model_context(cognitive_model: dict) -> str:
    """Formata cognitive_model para o prompt"""
    parts = ["## COGNITIVE MODEL DISPONÍVEL"]
    parts.append("\nO Observador analisou o diálogo e extraiu:")
    parts.append("")
    
    # Afirmação atual
    claim = cognitive_model.get("claim", "")
    if claim:
        parts.append(f"**Afirmação atual:** {claim}")
        parts.append("")
    
    # Fundamentos (proposições)
    proposicoes = cognitive_model.get("proposicoes", [])
    if proposicoes:
        parts.append("**Fundamentos (com solidez):**")
        for prop in proposicoes[:5]:  # Limitar a 5 para não sobrecarregar prompt
            texto = prop.get("texto", "") if isinstance(prop, dict) else getattr(prop, "texto", "")
            solidez = prop.get("solidez", 0.0) if isinstance(prop, dict) else getattr(prop, "solidez", 0.0)
            parts.append(f"- {texto} (solidez: {solidez:.2f})")
        if len(proposicoes) > 5:
            parts.append(f"- ... e mais {len(proposicoes) - 5} fundamentos")
        parts.append("")
    
    # Conceitos
    concepts = cognitive_model.get("concepts_detected", [])
    if concepts:
        parts.append(f"**Conceitos detectados:** {', '.join(concepts[:10])}")
        parts.append("")
    
    # Contradições
    contradictions = cognitive_model.get("contradictions", [])
    if contradictions:
        parts.append("**Contradições detectadas:**")
        for c in contradictions[:3]:  # Limitar a 3
            desc = c.get("description", "") if isinstance(c, dict) else str(c)
            parts.append(f"- {desc}")
        parts.append("")
    
    # Questões em aberto
    open_questions = cognitive_model.get("open_questions", [])
    if open_questions:
        parts.append("**Questões em aberto:**")
        for q in open_questions[:5]:  # Limitar a 5
            parts.append(f"- {q}")
        parts.append("")
    
    # Métricas
    solidez = cognitive_model.get("overall_solidez", 0.0)
    completude = cognitive_model.get("overall_completude", 0.0)
    parts.append("**Métricas:**")
    parts.append(f"- Solidez: {solidez:.2f} (quão bem fundamentada está a afirmação)")
    parts.append(f"- Completude: {completude:.2f} (quanto do argumento foi desenvolvido)")
    parts.append("")
    parts.append("Analise naturalmente e use quando útil para decidir próximo passo.")
    
    return "\n".join(parts)
```

**Prompt do Orquestrador (adicionar instrução):**
```python
# agents/orchestrator/prompts.py ou similar

ORCHESTRATOR_SYSTEM_PROMPT = """
Você é o Orquestrador Socrático...

## USO DO COGNITIVE MODEL

Quando o Cognitive Model estiver disponível no contexto, use-o para:
- Entender a evolução do argumento
- Identificar lacunas e contradições
- Decidir se aprofundar ou esclarecer
- Sugerir próximo passo baseado em solidez/completude

O Cognitive Model é uma análise automática do diálogo. Use-o como insight, não como restrição.
"""
```

**Testes:**
- `tests/unit/test_orchestrator_cognitive_access.py`: Valida leitura de cognitive_model do state
- `tests/integration/test_orchestrator_uses_cognitive_model.py`: Verifica que Claude menciona cognitive_model no reasoning

---

### 12.3: Timeline Visual

**Objetivo:** Mostrar quando Observer processou turno na timeline

**Implementação:**
```python
# app/components/backstage/timeline.py

def render_agent_timeline(session_id: str) -> None:
    """Renderiza histórico incluindo eventos do Observer"""
    try:
        bus = get_event_bus()
        events = bus.get_session_events(session_id)
        
        # Filtrar eventos agent_completed E cognitive_model_updated
        completed_events = [e for e in events if e.get("event_type") == "agent_completed"]
        observer_events = [e for e in events if e.get("event_type") == "cognitive_model_updated"]
        
        # ... código existente para completed_events ...
        
        # ADICIONAR EVENTOS DO OBSERVER
        if observer_events:
            st.markdown("---")
            st.markdown("**👁️ Observador**")
            
            for event in observer_events[-3:]:  # Últimos 3 eventos do Observer
                turn_number = event.get("metadata", {}).get("turn_number", 0)
                solidez = event.get("metadata", {}).get("solidez", 0.0)
                concepts_count = event.get("metadata", {}).get("concepts_count", 0)
                timestamp = event.get("timestamp", "")
                
                st.markdown(f"👁️ **Turno {turn_number}** processado")
                st.caption(f"🧠 {concepts_count} conceitos · Solidez: {solidez:.2f} · {timestamp}")
                
except Exception as e:
    logger.error(f"Erro ao renderizar timeline: {e}")
```

**Alternativa (seção separada):**
```python
# Adicionar seção colapsável "👁️ Observador" separada
with st.expander("👁️ Observador", expanded=False):
    if observer_events:
        for event in observer_events[-5:]:  # Últimos 5 eventos
            # ... renderizar evento ...
    else:
        st.caption("Observer ainda não processou turnos")
```

**Testes:**
- Validação visual manual (testar em interface web)
- `tests/integration/test_timeline_observer_events.py`: Verifica que eventos são renderizados

## Estimativas

- **LOC:** ~600 linhas
- **Tempo:** 2h
- **Risco:** Baixo (spikes validaram viabilidade)

## Critérios de Aceitação

1. ✅ Observer processa cada turno automaticamente após Orquestrador
2. ✅ Latência do usuário não aumenta (Observer em background, <3s)
3. ✅ cognitive_model atualizado no state após processamento
4. ✅ Orquestrador menciona cognitive_model no reasoning quando disponível
5. ✅ Timeline mostra atividade do Observer
6. ✅ Eventos `cognitive_model_updated` publicados no EventBus
7. ✅ Testes passam (unit + integration)

## Riscos e Mitigações

### Risco 1: State não thread-safe
**Mitigação:** 
- Testar comportamento com LangGraph checkpoint
- Se não for thread-safe, usar fila de eventos para atualização assíncrona
- Alternativa: Usar asyncio ao invés de threading

### Risco 2: Latência perceptível
**Mitigação:**
- Observer roda em background (não bloqueia resposta)
- Se latência for >3s, considerar otimizações (processar apenas conceitos essenciais)
- Adicionar timeout (5s) para não travar sistema

### Risco 3: Observer falha silenciosamente
**Mitigação:**
- Try/except completo no callback
- Logging de erros
- Evento de erro publicado no EventBus
- Fallback: continuar sem cognitive_model (não quebra sistema)

## Referências

- Código Observer: `agents/observer/`
- Multi-agent graph: `agents/multi_agent_graph.py`
- Estado: `agents/orchestrator/state.py`
- Spikes: 
  - `scripts/spikes/validate_langgraph_parallel.py`
  - `scripts/spikes/validate_cognitive_model_access.py`
- EventBus: `utils/event_bus/`
- Timeline: `app/components/backstage/timeline.py`
- Documentação Observer: `docs/agents/observer.md`


