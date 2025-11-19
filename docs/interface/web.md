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
│  📂 Ideias             💬 Chat Principal   🔍 Ver raciocínio    │
│                                                                 │
│  • Ideia 1 🔍          Você: "..."        [Fechado por padrão] │
│  • Ideia 2 📝 (ativa)  💰 $0.0012                              │
│  • Ideia 3 ✅                             [Quando aberto:]     │
│  [+ Nova Ideia]        Sistema: "..."      🧠 Orquestrador     │
│                        [digitando...]      "Reasoning..."      │
│                                            [Ver completo]      │
│                                            ⏱️ 1.2s | 💰 $0.0012│
│                                                                 │
│                                            [Timeline colapsada]│
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 Componentes Detalhados

**A) Sidebar (Conversas Recentes)**

**Conversas (últimas 5):**
- Formato: "Título da conversa · Timestamp relativo"
- Timestamp: "5min atrás", "2h atrás", "ontem", "3 dias atrás"
- Conversa ativa destacada (bold, background diferente)
- Collapsible (toggle on/off)

**Visual:**
```
💬 Conversas                [⌄ toggle]

- LLMs em produtividade (ativa)
  5min atrás

- Semana de 4 dias
  2h atrás

- Drones em obras
  ontem

[+ Nova Conversa]
[📖 Meus Pensamentos]  ← botão redireciona
[🏷️ Catálogo]         ← botão redireciona
```

**Alternar Entre Conversas:**
- Clicar em conversa → carrega thread_id (SqliteSaver)
- Restaura histórico de mensagens
- Atualiza contexto no chat

**Criar Nova Conversa:**
- Botão "[+ Nova Conversa]"
- Cria novo thread_id
- Chat limpo
- Nova conversa aparece como ativa

**B) Página: Meus Pensamentos (Nova)**

**Localização:** `/pensamentos`

**Layout:**
```
┌─────────────────────────────────────────────────┐
│ 📖 Meus Pensamentos                              │
│                                                 │
│ [🔍 Buscar ideias...]                           │
│ [Status ▼] [Conceitos ▼]                        │
│                                                 │
│ ┌─────────────────────┐ ┌─────────────────────┐│
│ │💡 LLMs em produtiv. │ │💡 Semana 4 dias     ││
│ │                     │ │                     ││
│ │ 📝 Estruturada      │ │ ✅ Validada         │
│ │ 3 argumentos        │ │ 2 argumentos        │
│ │ 5 conceitos         │ │ 4 conceitos         │
│ │                     │ │                     ││
│ │ 2h atrás            │ │ 1 dia atrás         │
│ │ [Ver detalhes →]    │ │ [Ver detalhes →]    │
│ └─────────────────────┘ └─────────────────────┘│
└─────────────────────────────────────────────────┘
```

**Funcionalidades:**
- Grid de cards (2 colunas, responsivo)
- Busca por título (LIKE query, case-insensitive)
- Filtros: status (exploring, structured, validated)
- Card clicável → redireciona pra `/pensamentos/{idea_id}`

**Badges de Status:**
- 🔍 Explorando (amarelo)
- 📝 Estruturada (azul)
- ✅ Validada (verde)

**C) Página: Detalhes da Ideia (Nova)**

**Localização:** `/pensamentos/{idea_id}`

**Layout:**
```
┌─────────────────────────────────────────────────┐
│ [← Voltar] 💡 LLMs em produtividade             │
│                                                 │
│ Status: 📝 Estruturada                          │
│ Atualizado: 2h atrás                            │
│                                                 │
│ ─────────────────────────────────────────────   │
│                                                 │
│ 📊 Argumentos (3):                              │
│   • V3 (focal): "Claude Code reduz tempo..."    │
│   • V2: "LLMs aumentam produtividade..."        │
│   • V1: "Observação inicial"                    │
│   [Ver detalhes de V3 →]                        │
│                                                 │
│ 🏷️ Conceitos (5):                               │
│   • Produtividade  • LLMs  • Desenvolvimento    │
│                                                 │
│ 💬 Conversas relacionadas:                      │
│   • Conversa 1 (18/11, 14:56)                   │
│                                                 │
│ ─────────────────────────────────────────────   │
│                                                 │
│ [🔄 Continuar explorando]  ← abre chat         │
│ [📝 Editar título]                              │
└─────────────────────────────────────────────────┘
```

**Funcionalidades:**
- Mostra claim, premises, assumptions do argumento focal
- Lista versões de argumentos (V1, V2, V3)
- Conceitos clicáveis → redireciona pro Catálogo
- Botão "Continuar explorando" → cria novo thread_id e volta pro chat

**D) Chat Principal (50-60% largura)**
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

**E) Bastidores (30-40% largura, collapsible)**

**Agentes Visíveis:**
- Sistema mostra qual agente está ativo:
  - 🎯 Orquestrador (provocador socrático)
  - 📝 Estruturador (organizador lógico)
  - 🔬 Metodologista (validador de rigor)
- Raciocínio resumido (1 frase, ~280 chars)
- Link "Ver raciocínio completo" → modal com detalhes
- Diferencial: usuário entende QUE tipo de análise está sendo feita

**Futuro (Épico 16):**
- Agentes customizáveis como personas (Sócrates, Aristóteles, Popper)
- Botão "Customizar persona" ao lado de cada agente
- Ver: `docs/vision/agent_personas.md`

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

### 3.3 Mostrar Status da Ideia (Épico 12.1)

**Localização:** Bastidores (painel direito), topo

**Visual:**
```
┌────────────────────────────────────┐
│ 💡 Ideia Atual                     │
│                                    │
│ 📝 Semana de 4 dias                │ ← título
│ [Estruturada]                      │ ← badge
│                                    │
│ 3 argumentos (V3 focal)             │ ← metadados
│ Última atualização: 10min atrás    │
│                                    │
│ ─────────────────────────          │
│                                    │
│ 🧠 Orquestrador (agora)            │
│ [reasoning...]                     │
└────────────────────────────────────┘
```

**Funcionalidades:**
- Badge de status inferido do modelo cognitivo (não manual)
- Status atualiza em tempo real conforme conversa evolui
- Badges visuais:
  - 🔍 Explorando (amarelo)
  - 📝 Estruturada (azul)
  - ✅ Validada (verde)
- Metadados: # argumentos, argumento focal, timestamp

**Critérios de inferência de status:**
- **Explorando:** claim vago, premises vazias, open_questions muitas
- **Estruturada:** claim específico, premises preenchidas, open_questions < 3
- **Validada:** Metodologista aprovou, contradictions vazias, assumptions baixas

---

## 3.4 Layout: Checklist de Progresso

📌 **NOTA:** Checklist de Progresso foi movido do Épico 11 (backend) para Épico 14 (frontend/UX).  
Backend (indicadores de maturidade) implementado no Épico 11.5.  
Frontend (checklist visual) implementado no Épico 14.6.

**Localização:** Header do chat (discreto, expansível ao clicar)

**Visual (minimizado):**
```
Chat                           [⚪⚪🟡⚪⚪] ← clica expande
```

**Visual (expandido):**
```
Progresso do Argumento:
⚪ 1. Definir escopo
⚪ 2. Identificar população  
🟡 3. Definir métricas ← em progresso
⚪ 4. Estruturar argumento
⚪ 5. Validar rigor científico
```

**Funcionalidades:**
- Checklist adaptativo (muda conforme tipo de artigo detectado)
- Bolinhas de status: ⚪ (pendente) 🟡 (em progresso) 🟢 (completo)
- Sempre minimizado por padrão (menos poluição visual)
- Expansível ao clicar (mostrar detalhes)
- Sincroniza com modelo cognitivo (claim, premises, open_questions, ...)

**Exemplos de checklists adaptativos:**

**Artigo Empírico:**
⚪ Definir hipótese
⚪ Identificar população
⚪ Definir métricas
⚪ Desenho experimental
⚪ Validar rigor

**Artigo de Revisão:**
⚪ Definir questão PICO
⚪ Estratégia de busca
⚪ Critérios inclusão/exclusão
⚪ Protocolo de extração
⚪ Síntese de evidências

**Implementação:**
- POC: Checklist fixo (mesmos passos para todos)
- Protótipo: Sistema detecta tipo de artigo, ajusta checklist
- MVP: Checklist adaptativo + status sincronizado com modelo cognitivo

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
        
        st.subheader("Premises")
        for premise in argument.premises:
            st.write(f"• {premise}")
        
        st.subheader("Assumptions")
        for assumption in argument.assumptions:
            st.write(f"⚠️ {assumption}")
        
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

**Versão:** 1.0  
**Data:** 15/11/2025  
**Status:** Especificação completa para implementação

