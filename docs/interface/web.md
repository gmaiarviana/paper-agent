# Interface Web Conversacional - Especificação Técnica

**Versão:** 1.0  
**Data:** 15/11/2025  
**Status:** Especificação para Épico 9 (POC → Protótipo → MVP)

---

## 1. Visão Geral

- Interface web (Streamlit) como experiência principal do Paper Agent
- Chat conversacional com reasoning dos agentes visível ("Bastidores")
- Eventos consumidos via polling (POC) ou SSE (MVP)
- Backend compartilhado com CLI (LangGraph + EventBus)

---

## 1.1 Dashboard vs Chat

O sistema mantém **duas interfaces web** com propósitos distintos:

### Interface Principal: Chat (`app/chat.py`)
- **Propósito:** Experiência do usuário final
- **Foco:** Uma sessão ativa por vez
- **Bastidores:** Reasoning visível opcionalmente
- **Público:** Pesquisadores usando o sistema

### Interface de Debug: Dashboard (`app/dashboard.py`)
- **Propósito:** Monitoring e debug
- **Foco:** Visão global de todas as sessões
- **Eventos:** Timeline completa de todas as sessões
- **Público:** Desenvolvedores e administradores

**Diferenças técnicas:**
- **Chat:** Interface rica, conversação fluida, bastidores inline
- **Dashboard:** Visão consolidada, eventos agregados, telemetria
- **Backend:** Ambos usam LangGraph + EventBus (compartilhado)
- **Porta:** Ambos rodam em :8501 (apps separados, mesma porta)

---

## 2. Arquitetura

### Stack Técnico

**Frontend:**
- **Framework:** Streamlit
- **Componentes:** chat_input, chat_history, backstage, timeline, sidebar
- **Eventos:** Polling (1s) no POC, SSE no MVP (otimização)
- **Estado:** Streamlit session_state + LangGraph checkpoints

**Backend:**
- **Orquestração:** LangGraph (compartilhado com CLI)
- **Eventos:** EventBus (publica eventos de agentes)
- **Persistência:** SqliteSaver (LangGraph) ou localStorage (a definir)
- **API:** Anthropic Claude (Haiku/Sonnet)

**Comunicação:**
```
┌──────────────┐
│  Streamlit   │ 1. User input
│  (Frontend)  │────────────────┐
└──────────────┘                │
                                ▼
                        ┌──────────────┐
                        │  LangGraph   │
                        │  (Backend)   │
                        └──────┬───────┘
                               │ 2. Events
                               ▼
                        ┌──────────────┐
                        │  EventBus    │
                        │  (JSON files)│
                        └──────┬───────┘
                               │ 3. Polling (1s) ou SSE (MVP)
┌──────────────┐               │
│  Streamlit   │◄──────────────┘
│  (Update)    │ 4. UI updates
└──────────────┘
```

---

## 3. Layout da Interface

### 3.1 Estrutura Geral (Desktop)
```
┌─────────────────────────────────────────────────────────────────┐
│  [Sidebar - 20%]      [Chat - 50%]       [Bastidores - 30%]    │
│                                                                 │
│  📂 Sessões            💬 Chat Principal   🔍 Ver raciocínio    │
│                                                                 │
│  • Conversa 1          Você: "..."        [Fechado por padrão] │
│  • Conversa 2          💰 $0.0012                              │
│  • Nova conversa                          [Quando aberto:]     │
│                        Sistema: "..."      🧠 Orquestrador     │
│                        [digitando...]      "Reasoning..."      │
│                                            [Ver completo]      │
│                                            ⏱️ 1.2s | 💰 $0.0012│
│                                                                 │
│                                            [Timeline colapsada]│
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 Componentes Detalhados

**A) Sidebar (Lista de Sessões)**
- Lista de conversas anteriores
- Formato: "Título da conversa · DD/MM/YYYY"
- Botão "+ Nova conversa"
- Sessão ativa destacada
- Scroll se muitas sessões

**B) Chat Principal (50-60% largura)**
```
┌──────────────────────────────────────┐
│  Você: "Observei que TDD reduz bugs" │
│  💰 $0.0012 · 215 tokens · 1.2s      │ ← inline, pequeno
│                                      │
│  Sistema: "Interessante! Em que...  │
│  💰 $0.0008 · 180 tokens · 0.9s      │
│                                      │
│  [Input de texto aqui]               │
│  [Enviar]                            │
└──────────────────────────────────────┘
```

**C) Bastidores (30-40% largura, collapsible)**

**Fechado (padrão):**
```
┌──────────────────────┐
│ [🔍 Ver raciocínio]  │ ← botão toggle
└──────────────────────┘
```

**Aberto:**
```
┌────────────────────────────────────┐
│ 🧠 Orquestrador (agora)            │
│                                    │
│ Usuário tem observação vaga.       │ ← resumo (280 chars)
│ Preciso contexto: onde observou... │
│                                    │
│ [📄 Ver raciocínio completo]       │ ← expande modal
│                                    │
│ ⏱️ 1.2s | 💰 $0.0012 | 📊 215 tokens│
│                                    │
│ ▼ Timeline de agentes anteriores   │ ← colapsado
└────────────────────────────────────┘
```

**Modal (raciocínio completo):**
```
┌──────────────────────────────────────────────┐
│ 🧠 Orquestrador - Raciocínio Completo        │
│                                              │
│ {                                            │
│   "agent": "orchestrator",                   │
│   "reasoning": "Analisei o input...",        │
│   "next_step": "explore",                    │
│   "message": "Interessante! Em que...",      │
│   "agent_suggestion": null,                  │
│   "tokens": {"input": 120, "output": 95},    │
│   "cost": 0.0012,                            │
│   "timestamp": "2025-11-15T10:30:00Z"        │
│ }                                            │
│                                              │
│ [Fechar]                                     │
└──────────────────────────────────────────────┘
```

---

## 4. Fluxo de Interação

### 4.1 Fluxo Principal (POC)
```
1. Usuário acessa interface web (localhost:8501)
   ↓
2. Sistema: "Olá! Me conte sobre sua ideia ou observação."
   ↓
3. Usuário digita mensagem no chat
   ↓
4. Sistema mostra "digitando..."
   ↓
5. Backend processa via LangGraph
   ↓
6. EventBus publica eventos em arquivo JSON (agent_started, agent_completed)
   ↓
7. Interface faz polling (1s) para buscar novos eventos
   ↓
8. Chat atualiza com resposta + métricas inline
   ↓
9. Bastidores atualizam com reasoning (se aberto)
   ↓
10. Loop: volta para passo 3
```

### 4.2 Fluxo de Bastidores
```
1. Usuário clica "🔍 Ver raciocínio"
   ↓
2. Painel expande (30-40% da tela)
   ↓
3. Mostra agente ativo + reasoning resumido
   ↓
4. Usuário clica "Ver raciocínio completo"
   ↓
5. Modal abre com JSON estruturado
   ↓
6. Usuário fecha modal
   ↓
7. Volta ao resumido
```

### 4.3 Fluxo de Sessões
```
1. Usuário clica "+ Nova conversa"
   ↓
2. Sistema cria novo thread_id
   ↓
3. Chat limpo (histórico vazio)
   ↓
4. Nova sessão aparece na sidebar
   ↓
5. Usuário pode alternar entre sessões
   ↓
6. Histórico de cada sessão preservado
```

---

## 5. Implementação Técnica

### 5.1 Componentes Streamlit

> **⚠️ NOTA:** Interface web conversacional (`app/chat.py`) será implementada no Épico 9. Este é um exemplo da arquitetura planejada.

**Arquivo: `app/chat.py` (principal - planejado)**
```python
import streamlit as st
from components.chat_input import render_chat_input
from components.chat_history import render_chat_history
from components.backstage import render_backstage
from components.sidebar import render_sidebar

def main():
    st.set_page_config(layout="wide")
    
    # Layout: 3 colunas
    sidebar, chat, backstage = st.columns([0.2, 0.5, 0.3])
    
    with sidebar:
        session_id = render_sidebar()
    
    with chat:
        render_chat_history(session_id)
        render_chat_input(session_id)
    
    with backstage:
        render_backstage(session_id)
```

**Arquivo: `app/components/chat_input.py`**
```python
import streamlit as st
from agents.multi_agent_graph import create_multi_agent_graph

def render_chat_input(session_id: str):
    user_input = st.text_input("Digite sua mensagem:", key="chat_input")
    
    if st.button("Enviar") or user_input:
        # Mostrar "digitando..."
        with st.spinner("Sistema está pensando..."):
            # Invocar LangGraph
            graph = create_multi_agent_graph()
            result = graph.invoke(
                {"user_input": user_input},
                config={"configurable": {"thread_id": session_id}}
            )
        
        # Atualizar histórico
        st.session_state.messages.append({
            "role": "user",
            "content": user_input,
            "tokens": result.get("tokens"),
            "cost": result.get("cost")
        })
        
        st.session_state.messages.append({
            "role": "assistant",
            "content": result["orchestrator_output"]["message"],
            "tokens": result.get("tokens"),
            "cost": result.get("cost")
        })
        
        # Limpar input
        st.rerun()
```

**Arquivo: `app/components/backstage.py`**
```python
import streamlit as st

def render_backstage(session_id: str):
    # Toggle
    show_backstage = st.toggle("🔍 Ver raciocínio", value=False)
    
    if not show_backstage:
        return
    
    # Buscar reasoning do agente ativo
    reasoning = get_latest_reasoning(session_id)
    
    if reasoning:
        st.subheader(f"🧠 {reasoning['agent'].title()}")
        st.write(reasoning['summary'][:280])  # Resumido
        
        if st.button("📄 Ver raciocínio completo"):
            with st.expander("Raciocínio Completo"):
                st.json(reasoning)
        
        # Métricas
        col1, col2, col3 = st.columns(3)
        col1.metric("Tempo", f"{reasoning['duration']:.1f}s")
        col2.metric("Custo", f"${reasoning['cost']:.4f}")
        col3.metric("Tokens", reasoning['tokens'])
        
        # Timeline colapsada
        with st.expander("▼ Timeline de agentes anteriores"):
            timeline = get_timeline(session_id)
            for event in timeline:
                st.write(f"**{event['agent']}** ({event['timestamp']})")
                st.caption(event['summary'][:100])
```

### 5.2 Polling de Eventos (POC)

**Arquivo:** `app/components/backstage.py`
```python
import streamlit as st
import time
from utils.event_bus import get_event_bus

def render_backstage_polling(session_id: str):
    """
    Atualiza bastidores via polling (POC).
    MVP migra para SSE.
    """
    event_bus = get_event_bus()
    
    # Polling a cada 1 segundo
    while True:
        # Buscar novos eventos
        new_events = event_bus.get_new_events(session_id)
        
        if new_events:
            # Atualizar UI
            for event in new_events:
                if event['type'] == 'agent_started':
                    st.write(f"🤖 {event['agent']} iniciou...")
                elif event['type'] == 'agent_completed':
                    st.write(f"✅ {event['agent']} concluiu")
                    st.json(event['reasoning'])
        
        time.sleep(1)  # Poll a cada 1s
        st.rerun()  # Força atualização da UI
```

**Limitações do Polling:**
- ⚠️ Delay de ~1s (usuário pode notar)
- ⚠️ Mais requests (poll a cada 1s vs evento quando ocorre)
- ✅ Simples de implementar (EventBus já existe)
- ✅ Suficiente para POC (valida valor da interface)

**Otimização no Protótipo e MVP:**
- Intervalo mantido em 1s (suficiente para experiência)
- SSE planejado movido para Backlog (ver BACKLOG.md)
- Decisão: Simplicidade > Performance prematura

### 5.3 SSE (Server-Sent Events) - MVP

> **📌 Status:** Funcionalidade movida para Backlog (BACKLOG.md).  
> MVP usa polling otimizado (1s). SSE será implementado se/quando delay se tornar problema na prática.

---

**Arquivo: `app/sse.py`**
```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio
import json
from utils.event_bus import get_event_bus

app = FastAPI()

@app.get("/events/{session_id}")
async def stream_events(session_id: str):
    event_bus = get_event_bus()
    
    async def event_generator():
        while True:
            # Buscar novos eventos
            events = event_bus.get_new_events(session_id)
            
            for event in events:
                yield f"data: {json.dumps(event)}\n\n"
            
            await asyncio.sleep(1)  # Poll a cada 1s
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )
```

**Consumo no Streamlit:**
```python
import streamlit as st
import requests
import json

def consume_sse(session_id: str):
    url = f"http://localhost:8000/events/{session_id}"
    
    with requests.get(url, stream=True) as response:
        for line in response.iter_lines():
            if line.startswith(b"data: "):
                event = json.loads(line[6:])
                # Atualizar UI com evento
                update_ui(event)
```

---

## 6. Persistência de Sessões

### Progressão POC → Protótipo → MVP

**POC (9.1-9.5):**
- **Armazenamento:** `st.session_state` (temporário)
- **Comportamento:** Recarregar página = perde histórico completo
- **Justificativa:** Validar UX de chat antes de complicar com persistência
- **Código:** Nativo Streamlit (sem dependências extras)

**Protótipo (9.6-9.9):**
- **Armazenamento:** `localStorage` (navegador)
- **Comportamento:** Sessões sobrevivem reload da página
- **Limitação:** Sessões por device (não compartilhadas entre navegadores)
- **Implementação:** ~20 linhas JavaScript via `st.components.v1.html`
```python
# Exemplo Protótipo - localStorage
import streamlit.components.v1 as components

def save_to_localstorage(session_id, data):
    components.html(f"""
    <script>
    localStorage.setItem('{session_id}', JSON.stringify({data}));
    </script>
    """, height=0)

def load_from_localstorage(session_id):
    result = components.html(f"""
    <script>
    const data = localStorage.getItem('{session_id}');
    window.parent.postMessage(data, '*');
    </script>
    """, height=0)
    return json.loads(result) if result else None
```

**MVP (9.10-9.11):**
- **Armazenamento:** `SqliteSaver` (backend LangGraph)
- **Comportamento:** Sessões persistem entre visitas/dispositivos
- **Limitação:** Sem autenticação - todas as sessões compartilhadas
- **Sidebar:** Últimas 10 sessões do banco (query ordenada por data)
```python
# Exemplo MVP - SqliteSaver
from langgraph.checkpoint.sqlite import SqliteSaver

# Setup
checkpointer = SqliteSaver.from_conn_string("checkpoints.db")
graph = create_multi_agent_graph().compile(checkpointer=checkpointer)

# Listar sessões recentes
def get_recent_sessions(limit=10):
    # Query no SqliteSaver para últimas sessões
    return checkpointer.list_sessions(limit=limit)

# Carregar sessão específica
def load_session(thread_id):
    config = {"configurable": {"thread_id": thread_id}}
    return graph.get_state(config)
```

**Evolução Futura (Épico 10):**
- Entidade `Topic` com metadados (título, tipo artigo, estágio)
- Autenticação (Google OAuth) para filtrar sessões por usuário
- Persistência cross-device real (não apenas compartilhada)

---

## 7. Progressão POC → MVP

### POC (Épico 9.1-9.5)
- ✅ Chat funciona (input → output)
- ✅ Histórico visível
- ✅ Métricas inline
- ✅ Backend compartilhado
- ✅ Polling (1s)
- ⚠️ **Persistência:** session_state apenas (temporário)

### Protótipo (Épico 9.6-9.9)
- ✅ Bastidores (collapsible)
- ✅ Reasoning resumido + completo (modal)
- ✅ Timeline de agentes
- ✅ **Persistência:** localStorage (sobrevive reload)
- ✅ Mantém polling

### MVP (Épico 9.10-9.11)
- ✅ **Persistência:** SqliteSaver (backend)
- ✅ Sidebar (últimas 10 sessões)
- ✅ Métricas consolidadas
- ✅ Polling otimizado (1s mantido)
- ❌ **SSE movido para Backlog**

---

## 8. Melhorias Futuras (Backlog)

- Mobile responsivo (bastidores como modal)
- Export de conversas (markdown, PDF)
- Replay de sessão (passo a passo)
- Temas (claro/escuro)
- Atalhos de teclado
- Busca em conversas antigas
- Favoritar mensagens importantes

---

**Versão:** 1.0  
**Data:** 15/11/2025  
**Status:** Especificação completa para implementação

