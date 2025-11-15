# ROADMAP - Paper Agent

> **📖 Status Atual:** Para entender o estado atual do sistema (épicos concluídos, funcionalidades implementadas), consulte [README.md](README.md) e [ARCHITECTURE.md](ARCHITECTURE.md).

> **📖 Melhorias Técnicas:** Para funcionalidades planejadas não vinculadas a épicos, consulte [BACKLOG.md](BACKLOG.md).

> **📖 Visão de Produto:** Para entender tipos de artigo, fluxos adaptativos e jornada do usuário, consulte `docs/product/vision.md`.

---

## 📋 Status dos Épicos

### ✅ Épicos Concluídos
- **Épico 1-7**: Sistema multi-agente conversacional completo (ver [ARCHITECTURE.md](ARCHITECTURE.md))
  - Orquestrador conversacional MVP
  - Estruturador com refinamento colaborativo
  - Metodologista com validação científica
  - EventBus e Dashboard
  - Configuração externa e MemoryManager

### 🚀 Épicos Ativos
- **ÉPICO 8**: Telemetria e Observabilidade (POC 8.1 concluída - 15/11/2025)

### 📋 Épicos Planejados
- **ÉPICO 9**: Interface Web Conversacional (refinado, pronto para implementação)
- **ÉPICO 10**: Entidade Tópico e Persistência (não refinado)
- **ÉPICO 11+**: Agentes Avançados - Pesquisador, Escritor, Crítico (não refinado)

**Regra**: Claude Code só trabalha em funcionalidades de épicos refinados.

> Para fluxo completo de planejamento, consulte `docs/process/planning_guidelines.md`.

---

## ÉPICO 8: Telemetria e Observabilidade

**Objetivo:** Instrumentar todos os agentes para capturar reasoning, decisões e métricas, implementar streaming de eventos em tempo real, e fornecer ferramentas para análise e otimização do sistema.

**Status:** 🟡 Em Progresso (POC concluída)

**Dependências:**
- ✅ Épico 7 concluído (Orquestrador Conversacional)
- ✅ Épico 5.1 concluído (EventBus e Dashboard)
- ✅ Épico 6.2 concluído (MemoryManager)

**Infraestrutura Existente:**
- ✅ EventBus implementado (`utils/event_bus.py`) com campo `metadata` livre
- ✅ Dashboard Streamlit com polling (auto-refresh 2s)
- ✅ Rastreamento de tokens já funcional (Épico 6.2)
- ✅ Wrapper `instrument_node()` instrumenta todos os agentes

---

### Progressão POC → Protótipo → MVP

#### ✅ POC (instrumentação básica) - CONCLUÍDA

**8.1: Instrumentar Estruturador** ✅ **CONCLUÍDO (15/11/2025)**

**Implementação:**
- ✅ Publicação de eventos no `structurer_node` (via wrapper `instrument_node`)
- ✅ Reasoning incluído via `metadata={"reasoning": "..."}`
- ✅ Reasoning texto livre implementado:
  - Modo inicial: "Estruturando V1 com base em: contexto, problema, contribuição"
  - Modo refinamento: "Refinando V{N} endereçando {X} gaps: [lista]"
- ✅ Dashboard exibe reasoning em expander para todos os agentes
- ✅ Função `_extract_reasoning()` implementada em `multi_agent_graph.py`
- ✅ Scripts de validação criados e passando

**Critérios de aceite:** ✅ **TODOS ATENDIDOS**
- ✅ Estruturador publica `agent_started` e `agent_completed` com reasoning
- ✅ Dashboard exibe reasoning via expander
- ✅ Polling funciona (Épico 5.1)
- ✅ Formato consistente com EventBus
- ✅ Reasoning visível e compreensível

**Arquivos modificados:**
- `agents/multi_agent_graph.py`: função `_extract_reasoning()` + metadata em eventos
- `app/dashboard.py`: expander para reasoning em `agent_completed`
- `scripts/flows/validate_epic8_poc_unit.py`: validação unitária (novo)
- `scripts/flows/validate_epic8_poc.py`: validação end-to-end (novo)

**Validação:**
```bash
# Validação unitária (sem API)
python scripts/flows/validate_epic8_poc_unit.py

# Validação end-to-end (com API)
python scripts/flows/validate_epic8_poc.py
```

---

#### Protótipo (streaming e métricas) - PRÓXIMO

**8.2: Instrumentar Orquestrador e Metodologista**
- Orquestrador: ✅ Reasoning já implementado (usa `orchestrator_analysis`)
- Metodologista: Adicionar reasoning explícito no metadata
- Dashboard: ✅ Expander já funciona para todos os agentes

**8.3: SSE (Server-Sent Events)**
- Implementar endpoint SSE: `/events/<session_id>` (FastAPI/Starlette)
- Interface web consome eventos via `EventSource` API
- Substituir polling por SSE (melhora experiência)
- Fallback automático para polling se SSE falhar
- Reconnect automático em caso de desconexão

**8.4: Métricas consolidadas**
- Tokens e custo por agente (ex: "Orquestrador: 500 tokens, $0.003")
- Tokens e custo total da sessão
- Tempo de execução por agente
- Exibição clara na interface web
- Atualização em tempo real via SSE

**Critérios de aceite Protótipo:**
- Todos os agentes emitem reasoning
- Dashboard recebe eventos em tempo real via SSE
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

**Status:** 📋 Refinado (pronto para implementação)

**Dependências:**
- ✅ Épico 8 POC concluído (reasoning instrumentado)
- ✅ Épico 7 concluído (Orquestrador Conversacional)

**Consulte:** `docs/interface/web.md` para especificação técnica completa

### Progressão POC → Protótipo → MVP

#### POC (chat básico funcionando)

**9.1: Input de chat na interface Streamlit**
- Campo de texto para enviar mensagens
- Botão "Enviar" ou Enter para submeter
- Estado de "digitando..." enquanto processa

**9.2: Backend conversacional integrado**
- Mensagens enviadas para LangGraph (mesmo backend do CLI)
- Orquestrador processa via thread_id único por sessão
- Resposta retorna para interface

**9.3: Histórico de conversa visível**
- Exibir mensagens anteriores (Você: / Sistema:)
- Scroll automático para última mensagem
- Layout limpo e legível

**9.4: Métricas inline discretas**
- Custo e tokens por mensagem (pequeno, após resposta)
- Formato: "💰 $0.0012 · 215 tokens · 1.2s"
- Não distrai da conversa

**9.5: Polling de eventos (1s)**
- EventBus publica eventos em arquivos JSON (infraestrutura existente)
- Interface faz polling a cada 1 segundo para buscar novos eventos
- Atualiza bastidores e timeline quando eventos chegam
- Simples e funcional para POC

**Critérios de aceite POC:**
- Usuário pode conversar via web (input → output)
- Histórico preservado durante sessão
- Métricas visíveis mas discretas
- Backend compartilhado com CLI (LangGraph + EventBus)
- Bastidores atualizam via polling (delay de ~1s aceitável)

#### Protótipo (bastidores e transparência)

**9.6: Painel "Bastidores" (collapsible)**
- Sidebar ou painel lateral (40% da tela)
- Botão "🔍 Ver raciocínio" (fechado por padrão)
- Abre/fecha com toggle

**9.7: Reasoning resumido dos agentes**
- Mostra agente ativo (Orquestrador, Estruturador, Metodologista)
- Reasoning resumido (~280 chars)
- Tempo, tokens, custo do agente

**9.8: Timeline de agentes (histórico)**
- Lista de agentes executados (colapsado)
- Expandir para ver reasoning de passos anteriores
- Ordenado cronologicamente

**9.9: Reasoning completo (modal)**
- Botão "📄 Ver raciocínio completo" ao lado do resumo
- Modal/dialog com JSON estruturado
- Mostra todos os campos do agente

**Critérios de aceite Protótipo:**
- Bastidores exibem reasoning via polling (1s)
- Timeline preserva histórico de raciocínio
- Usuário pode expandir para ver detalhes
- Experiência fluida apesar do delay do polling

#### MVP (experiência completa)

**9.10: SSE (Server-Sent Events) para streaming**
- Implementar endpoint SSE: `/events/<session_id>`
- Interface consome eventos em tempo real (não polling)
- Fallback para polling se SSE falhar
- Reconnect automático em caso de falha
- Melhora experiência (sem delay de 1s do polling)

**9.11: Sidebar com lista de sessões**
- Lista de conversas anteriores (título, data)
- Criar nova sessão
- Alternar entre sessões (não simultâneo)

**9.12: Métricas consolidadas**
- Total de tokens e custo da sessão
- Breakdown por agente (Orquestrador: X tokens, Metodologista: Y tokens)
- Exibido em painel ou tooltip

**Critérios de aceite MVP:**
- SSE funciona (streaming em tempo real, sem delay)
- Múltiplas sessões gerenciadas pela sidebar
- Sessões NÃO persistem entre reloads (temporárias)
- Métricas consolidadas visíveis
- Fallback para polling se SSE falhar

---

## ÉPICO 10: Entidade Tópico e Persistência

**Objetivo:** Permitir pausar/retomar conversas com contexto completo preservado, suportando múltiplos tópicos em evolução e persistência entre sessões.

**Status:** ⚠️ Não refinado (requer discussão)

**Dependências:**
- Épico 9 concluído (Interface Web)

**Consulte:** `docs/architecture/state_evolution.md` para detalhes de evolução de estado.

### Funcionalidades Planejadas (não refinadas)

- **10.1**: Persistência básica de sessões (localStorage ou SqliteSaver)
- **10.2**: Argumento Focal Persistente
- **10.3**: Pausar e retomar sessão
- **10.4-10.7**: Múltiplas sessões, busca, versionamento de artefatos
- **10.8-10.10**: Export, arquivamento, tags customizáveis

---

## ÉPICO 11+: Agentes Avançados

**Status:** ⚠️ Não refinado (requer discussão)

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
