# Análise: EventBus e Visualização

**Data:** 2025-12-XX  
**Objetivo:** Analisar estrutura atual do EventBus e como adicionar eventos do Observador para timeline + painel dedicado

---

## 1. Eventos Existentes e Estrutura

### 1.1 Modelos de Eventos (`utils/event_models.py`)

O sistema possui **6 tipos de eventos** definidos como classes Pydantic:

#### Eventos Base
- **`BaseEvent`**: Classe base com campos comuns:
  - `session_id` (str): ID único da sessão
  - `timestamp` (str): ISO 8601 UTC (gerado automaticamente)
  - `event_type` (str): Tipo do evento

#### Eventos de Agentes
1. **`AgentStartedEvent`**
   - Campos: `agent_name`, `metadata` (opcional)
   - Emitido quando um agente inicia execução

2. **`AgentCompletedEvent`**
   - Campos: `agent_name`, `summary` (até 280 chars), `tokens_input`, `tokens_output`, `tokens_total`, `cost`, `duration`, `metadata`
   - Emitido quando um agente finaliza com sucesso
   - **Importante:** `metadata` contém `reasoning` completo do agente

3. **`AgentErrorEvent`**
   - Campos: `agent_name`, `error_message`, `error_type` (opcional), `metadata`
   - Emitido quando um agente falha

#### Eventos de Sessão
4. **`SessionStartedEvent`**
   - Campos: `user_input`, `metadata`
   - Emitido no início de uma sessão

5. **`SessionCompletedEvent`**
   - Campos: `final_status`, `tokens_total`, `metadata`
   - Emitido no fim de uma sessão

#### Eventos do Observador
6. **`CognitiveModelUpdatedEvent`** (Épico 10.2)
   - Campos: `turn_number`, `solidez`, `completude`, `claims_count`, `proposicoes_count`, `concepts_count`, `open_questions_count`, `contradictions_count`, `is_mature`, `metadata`
   - **Já existe!** Publicado pelo Observador a cada turno processado
   - Localização: `agents/observer/nodes.py::_publish_cognitive_model_event()`

### 1.2 Estrutura do EventBus

**Arquitetura Modular:**
```
utils/event_bus/
├── core.py          # EventBusCore: persistência (load/save JSON)
├── publishers.py    # EventBusPublishers: métodos publish_*
├── readers.py       # EventBusReaders: métodos get_* e list_*
└── singleton.py     # EventBus completo + get_event_bus()
```

**Armazenamento:**
- Localização: `{temp_dir}/paper-agent-events/events-{session_id}.json`
- Formato JSON:
```json
{
  "session_id": "cli-session-abc123",
  "events": [
    {...},  // AgentStartedEvent
    {...},  // AgentCompletedEvent
    {...}   // CognitiveModelUpdatedEvent
  ]
}
```

**Métodos de Publicação (`publishers.py`):**
- `publish_event(event: EventType)` - genérico
- `publish_agent_started(...)`
- `publish_agent_completed(...)`
- `publish_agent_error(...)`
- `publish_session_started(...)`
- `publish_session_completed(...)`
- `publish_cognitive_model_updated(...)` ✅ **Já existe!**

**Métodos de Leitura (`readers.py`):**
- `get_session_events(session_id)` → List[Dict]
- `list_active_sessions(max_age_minutes=60)` → List[str]
- `get_session_summary(session_id)` → Dict | None
- `clear_session(session_id)` → bool

---

## 2. Como o Painel Bastidores Consome Eventos

### 2.1 Estrutura do Painel (`app/components/backstage/`)

**Componentes:**
```
app/components/backstage/
├── __init__.py      # render_right_panel() - orquestrador
├── context.py       # render_context_section() - ideia ativa, custo
├── reasoning.py      # render_backstage() - reasoning dos agentes
├── timeline.py      # render_agent_timeline() - histórico
└── constants.py     # AGENT_EMOJIS
```

### 2.2 Fluxo de Consumo

#### 2.2.1 Reasoning (`reasoning.py`)

**Função:** `render_backstage(session_id)`
- Expander "📊 Bastidores" (colapsado por padrão)
- Busca reasoning via `_get_latest_reasoning(session_id)`:
  1. Obtém eventos: `bus.get_session_events(session_id)`
  2. Filtra: `event_type == "agent_completed"`
  3. Pega último evento
  4. Extrai `reasoning` de `metadata["reasoning"]`
  5. Trunca para 280 chars (resumo)
- Renderiza:
  - Card de pensamento: emoji + nome + reasoning resumido
  - Link "Ver completo" → modal com 3 abas (Reasoning, Métricas, JSON)

#### 2.2.2 Timeline (`timeline.py`)

**Função:** `render_agent_timeline(session_id)`
- Busca eventos: `bus.get_session_events(session_id)`
- Filtra: `event_type == "agent_completed"`
- Remove último evento (já mostrado no card)
- Mostra últimos 2 eventos anteriores (formato: ● emoji + nome curto + horário)
- Botão "Ver histórico" → modal com lista completa

#### 2.2.3 Contexto (`context.py`)

**Função:** `render_context_section(session_id)`
- Busca eventos: `bus.get_session_events(session_id)`
- Filtra: `event_type == "agent_completed"`
- Calcula custo acumulado: soma de `cost` e `tokens_total`
- **Não consome eventos do Observador ainda!**

### 2.3 Padrão de Consumo Atual

**Características:**
- ✅ Leitura síncrona via `get_session_events()`
- ✅ Filtragem por `event_type` no código Python
- ✅ Processamento de `metadata` para extrair dados (ex: `reasoning`)
- ❌ **Não há consumo específico de `CognitiveModelUpdatedEvent`**

**Limitações:**
- Painel Bastidores foca apenas em `agent_completed` (reasoning)
- Timeline mostra apenas agentes (não turnos do Observador)
- Contexto não exibe métricas do Observador (solidez, completude)

---

## 3. Como Adicionar Novos Eventos do Observador

### 3.1 Evento Já Existe: `CognitiveModelUpdatedEvent`

**Status:** ✅ **Já implementado!**

**Onde é publicado:**
- Arquivo: `agents/observer/nodes.py`
- Função: `_publish_cognitive_model_event()` (linha 298)
- Chamada: `process_turn()` → linha 174 (se `session_id` fornecido)

**Dados disponíveis:**
```python
{
  "event_type": "cognitive_model_updated",
  "turn_number": 3,
  "solidez": 0.65,
  "completude": 0.50,
  "claims_count": 1,
  "proposicoes_count": 2,
  "concepts_count": 3,
  "open_questions_count": 1,
  "contradictions_count": 0,
  "is_mature": False,
  "metadata": {
    "claim": "LLMs aumentam produtividade",
    "maturity_reason": "..."
  }
}
```

### 3.2 Adicionar Timeline do Observador

**Objetivo:** Mostrar evolução do argumento ao longo dos turnos

**Implementação sugerida:**

#### 3.2.1 Novo componente: `app/components/backstage/observer_timeline.py`

```python
def render_observer_timeline(session_id: str) -> None:
    """
    Renderiza timeline de eventos do Observador (Épico X).
    
    Mostra evolução do argumento: solidez, completude, turnos.
    """
    bus = get_event_bus()
    events = bus.get_session_events(session_id)
    
    # Filtrar eventos do Observador
    observer_events = [
        e for e in events 
        if e.get("event_type") == "cognitive_model_updated"
    ]
    
    if not observer_events:
        st.caption("Nenhum turno processado ainda")
        return
    
    # Mostrar últimos 3 turnos
    recent_events = list(reversed(observer_events))[:3]
    
    for event in recent_events:
        turn = event.get("turn_number", 0)
        solidez = event.get("solidez", 0.0)
        completude = event.get("completude", 0.0)
        
        st.markdown(f"**Turno {turn}**")
        st.caption(f"🎯 Solidez: {solidez:.0%} | 📊 Completude: {completude:.0%}")
        st.progress(solidez, text=f"Solidez: {solidez:.0%}")
```

#### 3.2.2 Integrar no `reasoning.py`

Adicionar após `render_agent_timeline()`:

```python
# Timeline do Observador
st.markdown("---")
from .observer_timeline import render_observer_timeline
render_observer_timeline(session_id)
```

### 3.3 Adicionar Painel Dedicado do Observador

**Objetivo:** Painel expandido com métricas detalhadas do Observador

**Implementação sugerida:**

#### 3.3.1 Novo componente: `app/components/backstage/observer_panel.py`

```python
def render_observer_panel(session_id: str) -> None:
    """
    Renderiza painel dedicado do Observador (Épico X).
    
    Expander "👁️ Observador" com:
    - Métricas atuais (solidez, completude)
    - Gráfico de evolução (se houver múltiplos turnos)
    - Detalhes do último turno
    """
    with st.expander("👁️ Observador", expanded=False):
        bus = get_event_bus()
        events = bus.get_session_events(session_id)
        
        # Buscar último evento do Observador
        observer_events = [
            e for e in events 
            if e.get("event_type") == "cognitive_model_updated"
        ]
        
        if not observer_events:
            st.info("Aguardando processamento do Observador...")
            return
        
        latest = observer_events[-1]
        
        # Métricas principais
        col1, col2 = st.columns(2)
        with col1:
            st.metric("🎯 Solidez", f"{latest['solidez']:.0%}")
            st.progress(latest['solidez'], text=f"Solidez: {latest['solidez']:.0%}")
        with col2:
            st.metric("📊 Completude", f"{latest['completude']:.0%}")
            st.progress(latest['completude'], text=f"Completude: {latest['completude']:.0%}")
        
        # Estatísticas
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Claims", latest.get("claims_count", 0))
        with col2:
            st.metric("Proposições", latest.get("proposicoes_count", 0))
        with col3:
            st.metric("Conceitos", latest.get("concepts_count", 0))
        with col4:
            st.metric("Questões Abertas", latest.get("open_questions_count", 0))
        
        # Maturidade
        if latest.get("is_mature", False):
            st.success("✅ Argumento maduro")
        else:
            st.info("🔄 Argumento em desenvolvimento")
        
        # Gráfico de evolução (se houver múltiplos turnos)
        if len(observer_events) > 1:
            st.markdown("---")
            st.subheader("📈 Evolução")
            
            import pandas as pd
            df = pd.DataFrame([
                {
                    "Turno": e.get("turn_number", 0),
                    "Solidez": e.get("solidez", 0.0),
                    "Completude": e.get("completude", 0.0)
                }
                for e in observer_events
            ])
            
            st.line_chart(df.set_index("Turno"))
```

#### 3.3.2 Integrar no `__init__.py`

Adicionar nova seção no `render_right_panel()`:

```python
def render_right_panel(session_id: str) -> None:
    # Seção 1: Contexto
    render_context_section(session_id)
    
    # Seção 2: Observador (NOVO)
    from .observer_panel import render_observer_panel
    render_observer_panel(session_id)
    
    # Seção 3: Bastidores
    render_backstage(session_id)
```

### 3.4 Resumo: O Que Fazer

**✅ Já existe:**
- Modelo `CognitiveModelUpdatedEvent`
- Publicação automática pelo Observador
- Métodos de leitura no EventBus

**📝 Precisa implementar:**
1. Componente `observer_timeline.py` - timeline de turnos
2. Componente `observer_panel.py` - painel dedicado
3. Integração nos componentes existentes
4. Filtragem de eventos `cognitive_model_updated` no consumo

---

## 4. Infraestrutura de Polling

### 4.1 Polling Atual

**Status:** ✅ **Já implementado!**

**Localização:** `app/dashboard.py` (linhas 519-528)

**Mecanismo:**
```python
# Auto-refresh control (sidebar)
auto_refresh = st.sidebar.checkbox("Ativar atualização automática", ...)
refresh_interval = st.sidebar.slider("Intervalo (segundos)", 1, 10, 1)

# Auto-refresh mechanism (final do main)
if auto_refresh:
    current_time = time.time()
    elapsed = current_time - st.session_state.last_refresh_time
    
    if elapsed >= refresh_interval:
        st.session_state.last_refresh_time = current_time
        time.sleep(0.1)
        st.rerun()  # Re-executa o script inteiro
```

**Características:**
- ✅ Configurável via sidebar (checkbox + slider)
- ✅ Intervalo padrão: 1 segundo
- ✅ Usa `st.rerun()` para re-executar o script
- ✅ Funciona para qualquer componente que leia do EventBus

### 4.2 Polling no Chat (`app/chat.py`)

**Status:** ✅ **Já implementado!**

**Comentário no código (linha 109):**
```python
# Consumir eventos do EventBus via polling (1s)
```

**Inferência:** O chat também usa polling similar (provavelmente via `st.rerun()` ou componente Streamlit).

### 4.3 Polling no Painel Bastidores

**Status:** ⚠️ **Não há polling específico**

**Comportamento atual:**
- Componentes leem eventos via `get_session_events()` a cada renderização
- Se o dashboard/chat tem auto-refresh, o painel é atualizado automaticamente
- **Não há polling independente no painel**

**Conclusão:**
- ✅ **Não precisa criar nova infraestrutura de polling**
- ✅ **Reutilizar auto-refresh do dashboard/chat**
- ✅ **Componentes já são reativos** (leem eventos a cada render)

### 4.4 Otimizações Futuras (Backlog)

**SSE (Server-Sent Events):**
- Documentado em `docs/interface/web/flows.md` (linhas 346-398)
- Status: Movido para Backlog
- Justificativa: Polling de 1s é suficiente para POC/MVP

**Método `get_new_events()`:**
- Mencionado na documentação (linha 320 de `flows.md`)
- **Não existe no código atual!**
- Seria útil para evitar reprocessar eventos antigos

**Sugestão (opcional):**
Adicionar método `get_new_events(session_id, last_event_index)` em `readers.py`:
```python
def get_new_events(self, session_id: str, last_index: int = 0) -> List[Dict[str, Any]]:
    """
    Obtém apenas eventos novos desde um índice.
    
    Útil para polling otimizado (não reprocessa eventos antigos).
    """
    events = self.get_session_events(session_id)
    return events[last_index:]
```

---

## 5. Resumo Executivo

### ✅ O Que Já Existe

1. **EventBus completo:**
   - 6 tipos de eventos (incluindo `CognitiveModelUpdatedEvent`)
   - Publicação e leitura funcionais
   - Persistência em JSON

2. **Observador publica eventos:**
   - `CognitiveModelUpdatedEvent` a cada turno
   - Dados completos (solidez, completude, métricas)

3. **Polling implementado:**
   - Auto-refresh no dashboard (1s configurável)
   - Reativo a `st.rerun()`

4. **Painel Bastidores:**
   - Consome eventos de agentes (`agent_completed`)
   - Timeline de agentes
   - Reasoning completo

### 📝 O Que Precisa Ser Feito

1. **Criar componentes para Observador:**
   - `observer_timeline.py` - timeline de turnos
   - `observer_panel.py` - painel dedicado

2. **Integrar componentes:**
   - Adicionar timeline do Observador no `reasoning.py`
   - Adicionar painel do Observador no `__init__.py`

3. **Filtrar eventos:**
   - Usar `event_type == "cognitive_model_updated"` nos novos componentes

4. **Opcional (otimização):**
   - Adicionar `get_new_events()` para polling otimizado

### 🎯 Próximos Passos

1. Implementar `observer_timeline.py`
2. Implementar `observer_panel.py`
3. Integrar nos componentes existentes
4. Testar com eventos reais do Observador
5. Validar atualização em tempo real via polling

---

**Conclusão:** A infraestrutura está pronta. Basta criar os componentes de visualização para consumir os eventos `CognitiveModelUpdatedEvent` que já estão sendo publicados pelo Observador.

