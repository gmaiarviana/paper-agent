# ROADMAP - Paper Agent

> **📖 Status Atual:** Para entender o estado atual do sistema (épicos concluídos, funcionalidades implementadas), consulte [README.md](README.md) e [ARCHITECTURE.md](ARCHITECTURE.md).

> **📖 Melhorias Técnicas:** Para funcionalidades planejadas não vinculadas a épicos, consulte [docs/backlog.md](docs/backlog.md).

> **📖 Visão de Produto:** Para entender tipos de artigo, fluxos adaptativos e jornada do usuário, consulte `docs/product/vision.md`.

---

## 📋 Status dos Épicos

### ✅ Épicos Concluídos
- **Épico 1-7**: Sistema multi-agente conversacional completo (ver [ARCHITECTURE.md](ARCHITECTURE.md))
- **ÉPICO 8**: Telemetria e Observabilidade (POC + Protótipo concluídos)
- **ÉPICO 9 POC**: Interface Web Conversacional (9.1-9.5 concluídos - 16/11/2025)
- **ÉPICO 9 Protótipo**: Bastidores avançados + localStorage (9.6-9.9 concluídos - 16/11/2025)

### 🟡 Épicos Em Andamento
- _Nenhum épico em andamento no momento_

### ⏳ Épicos Planejados
- **ÉPICO 9 MVP**: Sidebar + SqliteSaver (9.10-9.11)
- **ÉPICO 10**: Entidade Tópico e Persistência (não refinado)
- **ÉPICO 11+**: Agentes Avançados - Pesquisador, Escritor, Crítico (não refinado)

**Regra**: Claude Code só trabalha em funcionalidades de épicos refinados.

> Para fluxo completo de planejamento, consulte `planning_guidelines.md`.

---

## ÉPICO 8: Telemetria e Observabilidade

**Objetivo:** Instrumentar todos os agentes para capturar reasoning, decisões e métricas, e implementar streaming de eventos em tempo real.

**Status:** ✅ Concluído

**Dependências:**
- ✅ Épico 7 concluído (Orquestrador Conversacional)
- ✅ Épico 5.1 concluído (EventBus e Dashboard)
- ✅ Épico 6.2 concluído (MemoryManager)

---

### Progressão POC → Protótipo

#### ✅ POC (instrumentação básica)

**8.1: Instrumentar Estruturador** ✅ **CONCLUÍDO**

**Funcionalidades:**
- Publicação de eventos com reasoning no `structurer_node`
- Reasoning texto livre (modo inicial e refinamento)
- Dashboard exibe reasoning via expander

**Critérios de aceite:**
- ✅ Estruturador publica `agent_started` e `agent_completed` com reasoning
- ✅ Dashboard exibe reasoning via expander
- ✅ Formato consistente com EventBus
- ✅ Reasoning visível e compreensível

---

#### ✅ Protótipo (streaming e métricas) **CONCLUÍDO**

**8.2: Instrumentar Orquestrador e Metodologista** ✅ **CONCLUÍDO**
- ✅ Reasoning explícito no metadata para todos os agentes
- ✅ Orquestrador: extrai reasoning de `orchestrator_analysis`
- ✅ Metodologista: extrai reasoning de `justification`

**8.3: Métricas consolidadas** ✅ **CONCLUÍDO**
- ✅ Tokens reais capturados do MemoryManager (input, output, total)
- ✅ Custo calculado via CostTracker por agente
- ✅ Tempo de execução capturado (start → end)
- ✅ Tokens e custo total da sessão
- ✅ Exibição clara na interface web (painel consolidado)
- ✅ Atualização em tempo real via polling (1s)

**Critérios de aceite Protótipo:**
- ✅ Todos os agentes emitem reasoning
- ✅ Dashboard recebe eventos via polling (1s)
- ✅ Métricas consolidadas exibidas corretamente
- ✅ Performance: Polling com intervalo de 1s (suficiente para experiência)

---

## ÉPICO 9: Interface Web Conversacional

**Objetivo:** Criar interface web como experiência principal do sistema, com chat fluido, visualização de reasoning dos agentes ("bastidores"), e métricas de custo inline.

**Status:** ✅ Protótipo Concluído (9.1-9.9 implementados - 16/11/2025)

**Dependências:**
- ✅ Épico 8 Protótipo concluído (reasoning, tokens, custo, tempo instrumentados)
- ✅ Épico 7 concluído (Orquestrador Conversacional)

**Ver spec técnica completa em `docs/interface/web.md`**

**Progresso Atual (16/11/2025):**
- ✅ **POC (9.1-9.5) COMPLETO:** Chat funcional + backend integrado + métricas + polling
- ✅ **Protótipo (9.6-9.9) COMPLETO:** Modal com abas + localStorage + persistência
- ✅ **Épico 8 completo:** Backend pronto com reasoning, tokens, custo e tempo instrumentados
- ⏳ **MVP (9.10-9.11):** Sidebar + SqliteSaver (próxima etapa)

**Arquivos implementados:**
- `app/chat.py` - ✅ Layout 3 colunas funcional
- `app/components/chat_input.py` - ✅ **COMPLETO:** Input + LangGraph + métricas + localStorage
- `app/components/chat_history.py` - ✅ **COMPLETO:** Histórico + métricas + load localStorage
- `app/components/backstage.py` - ✅ **COMPLETO:** Reasoning + modal com abas + timeline
- `app/components/sidebar.py` - ⏳ Esqueleto para lista de sessões (MVP)
- `app/components/storage.py` - ✅ **COMPLETO:** Persistência localStorage

---

### Progressão POC → Protótipo → MVP

#### ✅ POC (chat básico funcionando) - CONCLUÍDA

**9.1: Input de chat na interface** ✅ **CONCLUÍDO**
- Campo de texto com form (permite Enter para enviar)
- Botão "Enviar" integrado
- Spinner durante processamento

**9.2: Backend conversacional integrado** ✅ **CONCLUÍDO**
- Integração completa com LangGraph via `create_multi_agent_graph()`
- Estado criado com `create_initial_multi_agent_state()`
- Config com thread_id para persistência de contexto entre turnos
- Extração de resposta do orquestrador (`orchestrator_output.message`)

**9.3: Histórico de conversa visível** ✅ **CONCLUÍDO**
- Mensagens armazenadas em `st.session_state.messages`
- Renderização via `st.chat_message()` com avatars
- Formatação diferenciada para usuário vs sistema

**9.4: Métricas inline discretas** ✅ **CONCLUÍDO**
- Tokens (input, output, total) exibidos como caption
- Custo em USD (formato: $0.0012)
- Tempo de execução em segundos
- Layout: `💰 $0.0012 · 215 tokens · 1.2s`

**9.5: Polling de eventos** ✅ **CONCLUÍDO**
- Bastidores consomem EventBus via `get_session_events()`
- Reasoning extraído de `metadata.reasoning`
- Timeline de agentes anteriores com expander
- Auto-refresh quando bastidores abertos
- **Persistência:** `st.session_state` (temporário - recarregar = perde tudo)

**Critérios de aceite POC:** ✅ **TODOS ATENDIDOS**
- ✅ Usuário pode conversar via web (input → output)
- ✅ Histórico preservado durante sessão
- ✅ Métricas visíveis mas discretas
- ✅ Backend compartilhado com CLI (LangGraph + EventBus)
- ✅ Bastidores exibem reasoning dos agentes

---

#### ✅ Protótipo (bastidores e transparência) - CONCLUÍDO

**9.6: Painel "Bastidores" (collapsible)** ✅ **CONCLUÍDO**
- Toggle "🔍 Ver raciocínio" (fechado por padrão)
- Painel collapsible na coluna direita

**9.7: Reasoning resumido dos agentes** ✅ **CONCLUÍDO**
- Mostra agente ativo (Orquestrador, Estruturador, Metodologista)
- Reasoning resumido (~280 chars)
- **Modal real com abas** (em vez de expander):
  * Aba 1: Reasoning formatado (markdown)
  * Aba 2: Métricas detalhadas (tempo, tokens, custo, custo/1K)
  * Aba 3: JSON completo (evento completo)
- Botões para copiar reasoning e JSON
- Tempo, tokens, custo do agente exibidos

**9.8: Timeline de agentes (histórico)** ✅ **CONCLUÍDO**
- Expander colapsado com histórico de agentes anteriores
- Mostra summary, métricas e timestamp de cada evento

**9.9: Persistência básica (localStorage)** ✅ **CONCLUÍDO**
- Sessões sobrevivem reload da página
- Armazenamento via `storage.py` (usa `st.components.v1.html`)
- Recupera histórico ao recarregar página automaticamente
- Auto-geração de título da sessão (primeiros 50 chars do input)
- Metadados salvos: título, created_at, last_activity, message_count
- **Limitação:** Sessões por device (não compartilhadas entre navegadores)

**Critérios de aceite Protótipo:** ✅ **TODOS ATENDIDOS**
- ✅ Bastidores exibem reasoning via polling
- ✅ Timeline preserva histórico de raciocínio
- ✅ Usuário pode expandir para ver detalhes (modal com abas)
- ✅ Experiência fluida com modal profissional
- ✅ Persistência funciona (reload mantém histórico)

---

#### MVP (experiência completa)

**9.10: Sidebar com lista de sessões**
- Migração de `localStorage` para `SqliteSaver` (backend)
- Lista das últimas 10 sessões do banco
- Usuário pode alternar entre sessões (uma ativa por vez)
- Botão "+ Nova conversa"
- **Limitação:** Sem autenticação - todas as sessões compartilhadas entre usuários
**9.11: Métricas consolidadas**

**Critérios de aceite MVP:**
- Sessões persistem entre visitas (SqliteSaver backend)
- Sidebar gerencia múltiplas sessões
- Uma sessão ativa por vez (alternar via sidebar)
- Polling otimizado (1s de intervalo)
- Métricas consolidadas visíveis
- Todas as sessões compartilhadas (sem autenticação)

---

## ÉPICO 10: Entidade Tópico e Persistência

**Objetivo:** Permitir pausar/retomar conversas com contexto completo preservado, suportando múltiplos tópicos em evolução e persistência entre sessões.

**Status:** ⏳ Planejado (não refinado)

**Dependências:**
- Épico 9 concluído (Interface Web)

**Consulte:** 
- `docs/product/vision.md` (Seção 4) - Modelo conceitual da entidade Tópico e estágios de maturidade
- `docs/orchestration/multi_agent_architecture.md` - Schema completo do MultiAgentState e gerenciamento de estado
- `ARCHITECTURE.md` - Visão geral da entidade Tópico e evolução fluida

---

## ÉPICO 11+: Agentes Avançados

**Objetivo:** Expandir sistema com agentes especializados para pesquisa, redação e revisão de artigos científicos.

**Status:** ⏳ Planejado (não refinado)

**Agentes Planejados:**
- **Pesquisador**: Busca e análise de literatura científica
- **Escritor**: Redação de seções do artigo
- **Crítico**: Revisão e feedback construtivo

**Consulte:** `docs/agents/overview.md` para mapa completo de agentes planejados.

---

## 📝 Observações

- Cada épico pode ser desenvolvido **isoladamente**
- Entrega **valor incremental**
- Pode ser **testado** antes do próximo
- Épicos não refinados requerem discussão antes da implementação
