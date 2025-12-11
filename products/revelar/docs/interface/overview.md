# Interface Web Conversacional - Visão Geral e Arquitetura

**Versão:** 1.0  
**Data:** 15/11/2025  
**Status:** Especificação para Épico 9 (POC → Protótipo → MVP)

> **📌 Documentação dividida:** Este documento contém visão geral e arquitetura.  
> Ver também: [`components.md`](./components.md) e [`flows.md`](./flows.md)

---

## 1. Visão Geral

- Interface web (Streamlit) como experiência principal do Paper Agent
- Chat conversacional com reasoning dos agentes visível ("Bastidores")
- Eventos consumidos via polling (POC) ou SSE (MVP)
- Backend compartilhado com CLI (LangGraph + EventBus)

---

## 1.1 Dashboard vs Chat

O sistema mantém **duas interfaces web** com propósitos distintos:

### Interface Principal: Chat (`products/revelar/app/chat.py`)
- **Propósito:** Experiência do usuário final
- **Foco:** Uma sessão ativa por vez
- **Bastidores:** Reasoning visível opcionalmente
- **Público:** Pesquisadores usando o sistema

### Interface de Debug: Dashboard (`products/revelar/app/dashboard.py`)
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

**Versão:** 1.0  
**Data:** 15/11/2025  
**Status:** Especificação completa para implementação

