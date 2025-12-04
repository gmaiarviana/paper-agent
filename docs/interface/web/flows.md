# Interface Web Conversacional - Fluxos e Implementação

**Versão:** 1.0  
**Data:** 15/11/2025  
**Status:** Especificação para Épico 9 (POC → Protótipo → MVP)

> **📌 Documentação dividida:** Este documento contém fluxos de interação e implementação técnica.  
> Ver também: [`overview.md`](./overview.md) e [`components.md`](./components.md)

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
4. Sistema mostra feedback visual forte:
   - Input desabilita imediatamente (opacidade 50%)
   - Barra inline aparece: "🤖 Sistema pensando..."
   - Texto dinâmico: "Analisando..." → "Orquestrador pensando..." → "Estruturando..."
   ↓
5. Backend processa via LangGraph
   ↓
6. EventBus publica eventos
   ↓
7. Interface atualiza (barra some, input habilita)
   ↓
8. Chat atualiza com resposta + métricas inline
   ↓
9. Bastidores atualizam com reasoning (se aberto)
   ↓
10. Loop: volta para passo 3
```

### 4.2 Fluxo de Bastidores
```
1. Usuário envia mensagem
   ↓
2. Bastidores atualiza card de pensamento (agente ativo)
   ↓
3. Indicador de novidade aparece se bastidores colapsado
   ↓
4. Timeline atualiza com novo evento
   ↓
5. Usuário pode expandir para ver detalhes
   ↓
6. Usuário clica "Ver completo" → modal com raciocínio completo
   ↓
7. Usuário clica "Ver histórico" → modal com timeline completa
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

### 4.4 Feedback Visual Durante Processamento

**Visual proposto:**
```
┌─────────────────────────────────────────────────┐
│  Você: "Observei que LLMs aumentam..."          │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │ 🤖 Sistema pensando...                  │   │ ← barra inline
│  │ ⚡ Analisando sua mensagem               │   │ ← texto dinâmico
│  └─────────────────────────────────────────┘   │
│                                                 │
│  [Input desabilitado - opacidade 50%]           │
└─────────────────────────────────────────────────┘
```

**Comportamento:**
1. Usuário envia mensagem → input desabilita
2. Barra inline aparece com animação suave
3. Texto muda dinamicamente:
   - "🤖 Analisando sua mensagem..."
   - "🎯 Orquestrador pensando..."
   - "📝 Estruturador organizando..."
   - "🔬 Metodologista validando..."
4. Resposta chega → barra some + input habilita

**Implementação (Streamlit):**
- `st.spinner()` customizado
- Disable input: `disabled=st.session_state.get("processing", False)`
- CSS customizado para opacidade

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
    # Usar st.chat_input (componente nativo Streamlit)
    user_input = st.chat_input("Digite sua mensagem:")
    
    if user_input:
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
        
        # st.chat_input limpa automaticamente após envio
        st.rerun()
```

**Arquivo: `app/components/backstage.py`**
```python
import streamlit as st

def render_backstage(session_id: str):
    # Header colapsável com indicador de novidade
    has_updates = check_new_updates(session_id)
    indicator = "🔴" if has_updates else ""
    
    with st.expander(f"📊 Bastidores {indicator}", expanded=False):
        # Buscar reasoning do agente ativo
        reasoning = get_latest_reasoning(session_id)
        
        if reasoning:
            # Card de pensamento
            st.markdown(f"### {get_agent_emoji(reasoning['agent'])} {reasoning['agent'].title()}")
            st.write(reasoning['summary'][:280])  # Resumido
            
            if st.button("Ver completo", key="view_reasoning"):
                show_reasoning_modal(reasoning)
            
            # Card de timeline
            st.markdown("### 📜 Timeline")
            timeline = get_timeline(session_id, limit=3)
            for event in timeline:
                st.write(f"● {get_agent_emoji(event['agent'])} {event['agent']} - {event['timestamp']}")
                st.caption(event['summary'][:100])
            
            if len(get_timeline(session_id)) > 3:
                if st.button("Ver histórico", key="view_timeline"):
                    show_timeline_modal(session_id)
        else:
            # Estado vazio
            st.markdown("🤖")
            st.markdown("Aguardando...")
```

**Arquivo: `app/components/sidebar.py` (Épico 12)**
```python
import streamlit as st
from datetime import datetime
from agents.multi_agent_graph import get_ideas, create_idea, get_idea
from agents.database.manager import get_argument

def render_sidebar():
    """
    Sidebar com gestão de ideias.
    Funcionalidades: listar, alternar, criar nova, buscar.
    """
    st.sidebar.header("📂 Ideias")
    
    # Busca (12.6)
    search_query = st.sidebar.text_input("🔍 Buscar ideias...")
    status_filter = st.sidebar.selectbox("Filtrar por status", 
                                         ["Todas", "Explorando", "Estruturada", "Validada"])
    
    # Listar ideias (12.2)
    ideas = get_ideas(search=search_query, status=status_filter, limit=10)
    active_idea_id = st.session_state.get("active_idea_id")
    
    for idea in ideas:
        # Destacar ativa
        is_active = (idea.id == active_idea_id)
        style = "font-weight: bold; background-color: #f0f0f0;" if is_active else ""
        
        # Exibir ideia
        with st.sidebar.container():
            col1, col2 = st.columns([0.8, 0.2])
            
            with col1:
                # Título + badge
                badge = {"exploring": "🔍", "structured": "📝", "validated": "✅"}
                st.markdown(f"<div style='{style}'>{badge[idea.status]} {idea.title}</div>", 
                           unsafe_allow_html=True)
            
            with col2:
                # Botão alternar
                if st.button("→", key=f"switch_{idea.id}"):
                    switch_idea(idea.id)  # 12.3
            
            # Explorador de argumentos (12.5 - expandível)
            if st.sidebar.checkbox(f"Ver argumentos ({len(idea.arguments)})", 
                                  key=f"expand_{idea.id}"):
                for arg in idea.arguments:
                    focal_badge = "[focal]" if arg.id == idea.current_argument_id else ""
                    st.caption(f"• V{arg.version} {focal_badge}: {arg.claim[:50]}...")
                    if st.button("Ver detalhes", key=f"details_{arg.id}"):
                        show_argument_modal(arg)  # Modal com claim, premises, etc
    
    # Botão criar nova (12.4)
    if st.sidebar.button("+ Nova Ideia"):
        new_idea = create_idea(title=f"Nova Ideia {datetime.now()}")
        st.session_state["active_idea_id"] = new_idea.id
        st.rerun()
    
    return st.session_state.get("active_idea_id")


def switch_idea(idea_id: str):
    """Alternar para outra ideia (12.3)"""
    # Carregar thread_id
    idea = get_idea(idea_id)
    st.session_state["active_idea_id"] = idea.id
    st.session_state["thread_id"] = idea.thread_id
    
    # Restaurar argumento focal
    if idea.current_argument_id:
        st.session_state["current_argument"] = get_argument(idea.current_argument_id)
    
    st.rerun()


def show_argument_modal(argument):
    """Modal com detalhes do argumento (12.5)"""
    with st.expander(f"Argumento V{argument.version} - Detalhes"):
        st.subheader("Claim")
        st.write(argument.claim)
        
        st.subheader("Fundamentos")
        for fundamento in argument.fundamentos:
            solidez = fundamento.solidez if hasattr(fundamento, 'solidez') else 'N/A'
            st.write(f"• {fundamento.enunciado} (Solidez: {solidez})")
        
        st.subheader("Open Questions")
        for question in argument.open_questions:
            st.write(f"❓ {question}")
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

**Evolução Atual (Épico 12):**
- ✅ Entidade Idea com metadados (título, status)
- ✅ Gestão de múltiplas ideias (listar, alternar, buscar)
- ✅ Argumento focal (current_argument_id)
- ⏳ Autenticação (Google OAuth) para filtrar ideias por usuário (futuro)

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

## 9. Referências

- `docs/vision/epistemology.md` - Por que mostramos solidez, não verdade/falsidade
- `docs/interface/navigation_philosophy.md` - Filosofia de navegação

---

**Versão:** 1.0  
**Data:** 15/11/2025  
**Status:** Especificação completa para implementação

