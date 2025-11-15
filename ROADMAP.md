# ROADMAP - Paper Agent

> **📖 Status Atual:** Para entender o estado atual do sistema (épicos concluídos, funcionalidades implementadas), consulte [README.md](README.md) e [ARCHITECTURE.md](ARCHITECTURE.md).

> **📖 Melhorias Técnicas:** Para funcionalidades planejadas não vinculadas a épicos, consulte [docs/backlog.md](docs/backlog.md).

> **📖 Visão de Produto:** Para entender tipos de artigo, fluxos adaptativos e jornada do usuário, consulte `docs/product/vision.md`.

---

## 📋 Status dos Épicos

### ✅ Épicos Concluídos
- **Épico 1-7**: Sistema multi-agente conversacional completo (ver [ARCHITECTURE.md](ARCHITECTURE.md))

### 🟡 Épicos Em Andamento
- **ÉPICO 8**: Telemetria e Observabilidade

### ⏳ Épicos Planejados
- **ÉPICO 9**: Interface Web Conversacional (refinado, pronto para implementação)
- **ÉPICO 10**: Entidade Tópico e Persistência (não refinado)
- **ÉPICO 11+**: Agentes Avançados - Pesquisador, Escritor, Crítico (não refinado)

**Regra**: Claude Code só trabalha em funcionalidades de épicos refinados.

> Para fluxo completo de planejamento, consulte `planning_guidelines.md`.

---

## ÉPICO 8: Telemetria e Observabilidade

**Objetivo:** Instrumentar todos os agentes para capturar reasoning, decisões e métricas, implementar streaming de eventos em tempo real, e fornecer ferramentas para análise e otimização do sistema.

**Status:** 🟡 Em Progresso

**Dependências:**
- ✅ Épico 7 concluído (Orquestrador Conversacional)
- ✅ Épico 5.1 concluído (EventBus e Dashboard)
- ✅ Épico 6.2 concluído (MemoryManager)

---

### Progressão POC → Protótipo → MVP

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

#### Protótipo (streaming e métricas)

**8.2: Instrumentar Orquestrador e Metodologista**
- Adicionar reasoning explícito no metadata para todos os agentes

**8.3: SSE (Server-Sent Events)**
- Ver spec técnica completa em `docs/interface/web.md`

**8.4: Métricas consolidadas**
- Tokens e custo por agente
- Tokens e custo total da sessão
- Tempo de execução por agente
- Exibição clara na interface web
- Atualização em tempo real via SSE

**Critérios de aceite Protótipo:**
- Todos os agentes emitem reasoning
- Dashboard recebe eventos em tempo real via SSE (ver spec técnica em `docs/interface/web.md`)
- Fallback para polling funciona
- Métricas consolidadas exibidas corretamente
- Performance: SSE não adiciona latência perceptível (< 100ms)

---

#### MVP (export e estatísticas)

**8.5: Export de Reasoning e Estatísticas**
- Export de histórico completo de reasoning (JSON, markdown)
- Estatísticas agregadas por sessão:
  - Agente mais usado
  - Custo total por tipo de agente
  - Distribuição de tokens (input vs output)
  - Tempo médio por agente
- Dados exportáveis para análise offline
- Visualização básica de padrões (opcional: gráficos com Plotly)

**Critérios de aceite MVP:**
- Usuário pode exportar histórico completo de reasoning (botão no Dashboard)
- Estatísticas básicas disponíveis e corretas
- Formato de export utilizável (JSON válido, Markdown legível)
- Dados permitem identificar oportunidades de otimização

---

## ÉPICO 9: Interface Web Conversacional

**Objetivo:** Criar interface web como experiência principal do sistema, com chat fluido, visualização de reasoning dos agentes ("bastidores"), e métricas de custo inline.

**Status:** ⏳ Planejado (refinado, pronto para implementação)

**Dependências:**
- ✅ Épico 8 POC concluído (reasoning instrumentado)
- ✅ Épico 7 concluído (Orquestrador Conversacional)

**Ver spec técnica completa em `docs/interface/web.md`**

---

### Progressão POC → Protótipo → MVP

#### POC (chat básico funcionando)

**9.1: Input de chat na interface**
**9.2: Backend conversacional integrado**
**9.3: Histórico de conversa visível**
**9.4: Métricas inline discretas**
**9.5: Polling de eventos (1s)**
- Interface faz polling no EventBus a cada 1 segundo
- Atualiza bastidores quando eventos chegam
- Delay aceitável (~1s) para POC
- **Persistência:** Apenas `st.session_state` (temporário - recarregar = perde tudo)

**Critérios de aceite POC:**
- Usuário pode conversar via web (input → output)
- Histórico preservado durante sessão
- Métricas visíveis mas discretas
- Backend compartilhado com CLI (LangGraph + EventBus)
- Bastidores atualizam via polling (delay de ~1s aceitável)

---

#### Protótipo (bastidores e transparência)

**9.6: Painel "Bastidores" (collapsible)**
**9.7: Reasoning resumido dos agentes**
- Mostra agente ativo (Orquestrador, Estruturador, Metodologista)
- Reasoning resumido (~280 chars)
- **Botão "📄 Ver raciocínio completo"** abre modal com JSON estruturado
- Tempo, tokens, custo do agente

**9.8: Timeline de agentes (histórico)**
**9.9: Persistência básica (localStorage)**
- Sessões sobrevivem reload da página
- Armazenamento no navegador via `localStorage`
- Recupera histórico ao recarregar página
- **Limitação:** Sessões por device (não compartilhadas entre navegadores)
- Implementação: ~20 linhas JavaScript via `st.components.v1.html`

**Critérios de aceite Protótipo:**
- Bastidores exibem reasoning via polling (1s)
- Timeline preserva histórico de raciocínio
- Usuário pode expandir para ver detalhes
- Experiência fluida apesar do delay do polling

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
- Polling otimizado (1s de intervalo - SSE movido para Backlog)
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
