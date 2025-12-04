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
│  [Sidebar]              [Chat]                      [Direita]   │
│                                                                 │
│  📖 Pensamentos         Conversa...           ┌───────────────┐ │
│  🏷️ Catálogo                                 │ 💡 Contexto   │ │
│  💬 Conversas                                 │ (ideia ativa) │ │
│  [+ Nova conversa]                            └───────────────┘ │
│                                               ┌───────────────┐ │
│                                               │📊 Bastidores  │ │
│                                               │ (pensamento)  │ │
│                                               │ (timeline)    │ │
│                                               └───────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

**Layout com 3 elementos:**
- **Sidebar:** Links de navegação (sem lista de conversas)
- **Chat (50-60%):** Conversação principal
- **Painel Direito:** Dividido em Contexto (acima) + Bastidores (abaixo)

### 3.2 Componentes Detalhados

**A) Sidebar (Links de Navegação)**

```
┌─────────────────────────┐
│ 📖 Pensamentos          │ → /pensamentos
│ 🏷️ Catálogo            │ → /catalogo (desabilitado)
│ 💬 Conversas            │ → /historico
│                         │
│ [+ Nova conversa]       │ → inicia chat novo
└─────────────────────────┘
```

**Funcionalidades:**
- Links com ícones para páginas dedicadas
- Botão "+ Nova conversa" inicia chat novo
- Sem lista de conversas recentes (histórico em página dedicada)
- Sem header/logo (minimalista)

**B) Página: Minhas Ideias**

**Localização:** `/pensamentos` (URL mantida para compatibilidade, mas interface mostra "Minhas Ideias")

**Layout:**
```
┌─────────────────────────────────────────────────┐
│ 💡 Minhas Ideias                                 │
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

**C) Página: Detalhes da Ideia**

**Localização:** `/pensamentos/{idea_id}`

**Layout:**
```
┌─────────────────────────────────────────────────┐
│ [← Voltar] 💡 LLMs em produtividade             │
│                                                 │
│ Solidez geral: ██████░░ 65%                     │
│                                                 │
│ ─────────────────────────────────────────────   │
│                                                 │
│ 📊 Fundamentos:                                 │
│   • "LLMs reduzem tempo de código"              │
│     Solidez: ████████ 80% (3 evidências)        │
│   • "Qualidade não é afetada"                   │
│     Solidez: ███░░░░░ 35% (1 evidência fraca)   │ ← alerta visual
│     [🔍 Fortalecer com pesquisa]                │
│                                                 │
│ 💬 Conversas associadas:                        │
│   • Conversa 1 (18/11, 14:56)                   │
│   • Conversa 2 (19/11, 10:30)                   │
│                                                 │
│ ─────────────────────────────────────────────   │
│                                                 │
│ [💬 Continuar elaborando]  ← novo chat          │
│ [📝 Criar conteúdo]        ← se madura          │
└─────────────────────────────────────────────────┘
```

**Funcionalidades:**
- Mostra solidez geral da ideia (barra de progresso)
- Lista fundamentos (proposições) com suas solidezes individuais
- Alertas visuais para fundamentos frágeis (< 40%)
- Botão "Fortalecer com pesquisa" para fundamentos frágeis
- Contador: "2 fundamentos precisam fortalecimento"
- Conversas associadas à ideia
- Botão "Continuar elaborando" → cria novo thread_id e volta pro chat
- Botão "Criar conteúdo" → disponível quando ideia tem solidez >= 60%

**D) Chat Principal (50-60% largura)**
```
┌──────────────────────────────────────┐
│  Você: "Observei que TDD reduz bugs" │
│  ℹ️                                  │ ← ícone pequeno (clicável)
│                                      │
│  Sistema: "Interessante! Em que...  │
│  ℹ️                                  │ ← ícone pequeno (clicável)
│                                      │
│  [Input de texto aqui]               │ ← st.chat_input (nativo)
└──────────────────────────────────────┘
```

**Métricas por mensagem:**
- Ícone pequeno (ℹ️) após cada mensagem do sistema
- Clique no ícone abre popover com métricas
- Formato: "💰 R$0,02 · 215 tokens · 1.2s"
- Métricas NÃO ficam sempre visíveis (reduz ruído)

**Input de chat:**
- Usar `st.chat_input` (componente nativo Streamlit)
- Enter envia mensagem

**E) Bastidores (Painel Direito - Abaixo)**

**Propósito:** Mostrar o sistema pensando (reasoning dos agentes).

**Estrutura:**
```
┌──────────────────────────────┐
│ 📊 Bastidores            🔴  │ ← header clicável + indicador
├──────────────────────────────┤
│                              │
│ ┌──────────────────────────┐ │
│ │ 🎯 Orquestrador          │ │ ← Card de pensamento
│ │ "Analisando contexto..." │ │
│ │ [Ver completo]           │ │
│ └──────────────────────────┘ │
│                              │
│ ┌──────────────────────────┐ │
│ │ 📜 Timeline              │ │ ← Card de timeline
│ │ ● 🎯 Orq. - 10:32        │ │
│ │ ● 📝 Est. - 10:31        │ │
│ │ ● 🎯 Orq. - 10:30        │ │
│ │ [Ver histórico]          │ │
│ └──────────────────────────┘ │
└──────────────────────────────┘
```

**Comportamento:**
- Header clicável para expandir/colapsar seção inteira
- Indicador de novidade (🔴 ou "+2") quando há atualizações
- Indicador some ao expandir
- Não expande automaticamente (não distrai usuário)

**Estado vazio:**
```
┌──────────────────────────────┐
│ 📊 Bastidores                │
│                              │
│           🤖                 │
│       Aguardando...          │
│                              │
└──────────────────────────────┘
```

**Card de Pensamento:**
- Emoji + nome do agente ativo
- Pensamento resumido (~280 chars)
- Link "Ver completo" → modal com raciocínio completo

**Card de Timeline:**
- Últimos 3 agentes (atual + 2 anteriores)
- Formato: emoji + nome + resumo curto + horário
- Link "Ver histórico" → modal com lista completa

**Modal de Timeline:**
- Lista completa de todos os agentes que trabalharam
- Mesmo formato: emoji + nome + resumo + horário
- Ordenado por mais recente primeiro

**Futuro (Épico 18):**
- Agentes customizáveis como personas (Sócrates, Aristóteles, Popper)
- Botão "Customizar persona" ao lado de cada agente
- Ver: `docs/vision/agent_personas.md`

**F) Contexto (Painel Direito - Acima)**

**Propósito:** Mostrar informações sobre a ideia e conversa ativa.

**Estrutura:**
```
┌──────────────────────────────┐
│ 💡 Contexto              [↗] │ ← header clicável
├──────────────────────────────┤
│ 📝 "LLMs e produtividade"    │ ← título da ideia
│ Status: Estruturada          │
│ Solidez: ██████░░ 65%        │
│                              │
│ 💰 R$ 0,15 total             │ ← custo acumulado (clicável)
└──────────────────────────────┘
```

**Comportamento:**
- Header clicável para expandir/colapsar
- Clique no custo abre modal com detalhes
- Atualiza em tempo real

**Estado vazio (sem ideia associada):**
- Seção em branco ou não aparece
- Só mostra custo acumulado

**Modal de detalhes:**
- Ideia completa (título, status, argumentos)
- Custo detalhado por mensagem
- Modelo usado
- Total de tokens

**Chat iniciado de página de ideia:**
- Já começa com ideia associada no Contexto

---

### 3.3 Fluxo "Criar Conteúdo"

**Trigger:** Botão "Criar conteúdo" disponível quando ideia tem solidez >= 60%

**Fluxo:**

```
Usuário clica "Criar conteúdo"
↓
Abre chat com prompt inicial:
Sistema: "Vamos criar conteúdo a partir dessa ideia!
Que formato você prefere?

• Artigo acadêmico
• Post de blog
• Thread de Twitter
• Outro"
↓
Conversa curta para definir:

• Formato
• Tom/estilo
• Ênfase (qual fundamento destacar)
• Público-alvo
↓
Orquestrador chama Escritor
↓
Conteúdo gerado baseado em:

• Claim da ideia
• Fundamentos (proposições)
• Evidências
• Preferências definidas na conversa
```

**Implementação:**
- Botão "Criar conteúdo" aparece condicionalmente (solidez >= 60%)
- Abre novo chat com contexto pré-carregado da ideia
- Orquestrador detecta intenção de criar conteúdo e chama Escritor
- Escritor gera conteúdo usando metadados já elaborados (claim, fundamentos, evidências)
- Usuário pode revisar e ajustar antes de exportar

---

### 3.4 Indicadores Visuais

**A) Solidez (novo)**

- Barra de progresso colorida
- Verde (>70%): sólido
- Amarelo (40-70%): moderado
- Vermelho (<40%): frágil

**Visual:**
```
Solidez geral: ████████░░ 80%  ← verde
Solidez: ██████░░ 65%            ← amarelo
Solidez: ███░░░░░ 35%            ← vermelho
```

**B) Alertas de Fragilidade**

- Fundamentos com solidez < 40% mostram alerta visual
- Botão "Fortalecer com pesquisa" disponível
- Contador: "2 fundamentos precisam fortalecimento"

**Visual:**
```
📊 Fundamentos:
  • "LLMs reduzem tempo de código"
    Solidez: ████████ 80% (3 evidências)  ← verde
    
  ⚠️ • "Qualidade não é afetada"
    Solidez: ███░░░░░ 35% (1 evidência fraca)  ← vermelho + alerta
    [🔍 Fortalecer com pesquisa]
    
  ⚠️ • "Custo-benefício é positivo"
    Solidez: ██░░░░░░ 25% (0 evidências)  ← vermelho + alerta
    [🔍 Fortalecer com pesquisa]
    
[2 fundamentos precisam fortalecimento]
```

---

### 3.5 Status da Ideia

**Nota:** Conteúdo movido para seção "Contexto" (3.2 F). Ver detalhes acima.

---

### 3.6 Painel Progress (Checklist)

> **📌 Status atual:** Backend implementado, frontend NÃO integrado.  
> **Integração:** Épico 15.  
> **Referência:** `agents/checklist/progress_tracker.py`

> **🔍 DIFERENÇA CHAVE:** Progress mostra **onde o usuário está na jornada** (estado atual do argumento).  
> Bastidores mostra o **sistema pensando** (reasoning em tempo real).

**Localização:** Borda direita do chat, flutuante/fixo

**Visual:**
```
┌──────────────────────┐
│ 📊 Progresso         │
│                      │
│ ⚪ 1. Escopo definido │
│ ⚪ 2. População       │
│ 🟡 3. Métricas        │ ← em progresso
│ ⚪ 4. Metodologia     │
│ ⚪ 5. Baseline        │
│                      │
│ [🔄 Atualizar]       │
└──────────────────────┘
```

**Comportamento:**
- Lista vertical de itens com status (⚪ pendente, 🟡 em progresso, 🟢 completo)
- Acompanha scroll da conversa (fixo/flutuante na borda direita)
- Adapta conforme tipo de artigo detectado (empírico, revisão, teórico)
- Sincroniza com modelo cognitivo (`CognitiveModel`) em tempo real
- Atualiza automaticamente conforme argumento evolui

**Checklists Adaptativos:**

**Artigo Empírico:**
- ⚪ Escopo definido (claim específico)
- ⚪ População identificada
- ⚪ Métricas definidas
- ⚪ Metodologia estruturada
- ⚪ Baseline definido

**Artigo de Revisão:**
- ⚪ Questão de pesquisa (PICO/SPIDER)
- ⚪ Estratégia de busca
- ⚪ Critérios de inclusão/exclusão
- ⚪ Síntese de evidências
- ⚪ Lacunas identificadas

**Artigo Teórico:**
- ⚪ Problema conceitual
- ⚪ Framework proposto
- ⚪ Consistência lógica
- ⚪ Contribuições claras
- ⚪ Implicações discutidas

**Artigo Genérico (padrão):**
- ⚪ Afirmação clara
- ⚪ Contexto definido
- ⚪ Fundamentos sólidos
- ⚪ Suposições baixas
- ⚪ Lacunas respondidas

**Implementação Técnica:**
- Backend: `ProgressTracker` avalia `CognitiveModel` e retorna `List[ChecklistItem]`
- Status inferido de campos do modelo (claim, fundamentos, context, etc.)
- Frontend: Componente Streamlit que consome checklist do backend
- Atualização: Polling ou SSE (conforme implementação de eventos)

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

