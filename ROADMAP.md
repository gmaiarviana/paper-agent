# ROADMAP - Paper Agent

> **📖 Status Atual:** Para entender o estado atual do sistema (épicos concluídos, funcionalidades implementadas), consulte [README.md](README.md) e [ARCHITECTURE.md](ARCHITECTURE.md).

> **📖 Melhorias Técnicas:** Para funcionalidades planejadas não vinculadas a épicos, consulte [BACKLOG.md](BACKLOG.md).

> **📖 Visão de Produto:** Para entender tipos de artigo, fluxos adaptativos e jornada do usuário, consulte `docs/product/vision.md`.

---

## 📋 Status dos Épicos

### ✅ Épicos Refinados (Prontos para Implementação)
- ÉPICO 8: Telemetria e Observabilidade (POC concluída - 15/11/2025)
- ÉPICO 9: Interface Web Conversacional (refinado)

### ⚠️ Épicos Não-Refinados (Requerem Discussão Antes da Implementação)
- ÉPICO 10: Entidade Tópico e Persistência
- ÉPICO 11+: Agentes Avançados (Pesquisador, Escritor, Crítico)

**Regra**: Claude Code só trabalha em funcionalidades de épicos refinados.

> Para fluxo completo de planejamento, consulte `docs/process/planning_guidelines.md`.

---

## ÉPICO 8: Telemetria e Observabilidade

**Objetivo:** Instrumentar todos os agentes para capturar reasoning, decisões e métricas, implementar streaming de eventos em tempo real, e fornecer ferramentas para análise e otimização do sistema.

**Status:** 🟡 Refinado

**Dependências:**
- Épico 7 Protótipo concluído (Orquestrador Conversacional com transparência)
- Épico 5.1 concluído (EventBus e Dashboard - infraestrutura base)
- Épico 6.2 concluído (MemoryManager - rastreamento de tokens)

**Infraestrutura Existente:**
- ✅ EventBus implementado (`utils/event_bus.py`) com campo `metadata` livre
- ✅ Dashboard Streamlit com polling (auto-refresh 2s)
- ✅ Rastreamento de tokens já funcional (Épico 6.2)
- ✅ Orquestrador já publica eventos com metadata
- 👉 **POC 8.1 é replicar padrão existente para Estruturador**

---

### Progressão POC → Protótipo → MVP

#### POC (instrumentação básica)

**8.1: Instrumentar Estruturador** ✅ **CONCLUÍDO (15/11/2025)**
- ✅ Publicação de eventos no `structurer_node` (via wrapper `instrument_node`)
- ✅ Reasoning incluído via `metadata={"reasoning": "..."}`
- ✅ Reasoning texto livre implementado:
  - Modo inicial: "Estruturando V1 com base em: contexto, problema, contribuição"
  - Modo refinamento: "Refinando V{N} endereçando {X} gaps: [lista]"
- ✅ Dashboard exibe reasoning em expander para todos os agentes
- ✅ Função `_extract_reasoning()` implementada em `multi_agent_graph.py`
- ✅ Script de validação unitária criado: `scripts/flows/validate_epic8_poc_unit.py`

**Critérios de aceite POC:** ✅ **TODOS ATENDIDOS**
- ✅ Estruturador publica `agent_started` e `agent_completed` com reasoning
- ✅ Dashboard exibe reasoning do Estruturador (via expander)
- ✅ Polling funciona (já implementado no Épico 5.1)
- ✅ Formato consistente com eventos existentes (usa `metadata`)
- ✅ Reasoning visível e compreensível para usuário

**Arquivos modificados:**
- `agents/multi_agent_graph.py`: função `_extract_reasoning()` + metadata em eventos
- `app/dashboard.py`: expander para reasoning em `agent_completed`
- `scripts/flows/validate_epic8_poc_unit.py`: validação unitária (novo)
- `scripts/flows/validate_epic8_poc.py`: validação end-to-end com API (novo)

---

#### Protótipo (streaming e métricas)

**8.2: Instrumentar Orquestrador e Metodologista**
- Orquestrador: adicionar reasoning explícito no metadata (já publica eventos)
- Metodologista: adicionar publicação de eventos + reasoning no metadata
- Reasoning detalha processo de cada agente:
  - Orquestrador: análise contextual e decisões
  - Metodologista: processo de validação (complementa justification)
- Dashboard replica expander para todos os agentes
- **Nota técnica:** Orquestrador parcialmente instrumentado, Metodologista precisa adicionar publicação

**8.3: SSE (Server-Sent Events)**
- Implementar endpoint SSE: `/events/<session_id>` (FastAPI/Starlette)
- Interface web consome eventos via `EventSource` API
- Substituir polling por SSE (melhora experiência)
- Fallback automático para polling se SSE falhar
- Reconnect automático em caso de desconexão
- **Nota técnica:** Única parte complexa do Épico 8 (requer FastAPI)

**8.4: Métricas consolidadas**
- Tokens e custo por agente (ex: "Orquestrador: 500 tokens, $0.003")
- Tokens e custo total da sessão
- Tempo de execução por agente
- Exibição clara na interface web (sidebar ou painel dedicado)
- Atualização em tempo real via SSE
- **Nota técnica:** CostTracker já calcula custos, apenas agregar e exibir

**Critérios de aceite Protótipo:**
- Todos os agentes (Orquestrador, Estruturador, Metodologista) emitem reasoning
- Dashboard recebe eventos em tempo real via SSE
- Fallback para polling funciona se SSE falhar
- Métricas consolidadas exibidas corretamente
- Performance: SSE não adiciona latência perceptível (< 100ms)

---

#### MVP (export e estatísticas)

**8.5: Export de Reasoning e Estatísticas**
- Export de histórico completo de reasoning (JSON, markdown)
- Estatísticas agregadas por sessão:
  - Agente mais usado na sessão
  - Custo total por tipo de agente
  - Distribuição de tokens (input vs output)
  - Tempo médio por agente
- Dados exportáveis para análise offline
- Visualização básica de padrões (opcional: gráficos simples com Plotly)
- **Nota técnica:** EventBus já persiste eventos em JSON, export é leitura + formatação

**Critérios de aceite MVP:**
- Usuário pode exportar histórico completo de reasoning (botão no Dashboard)
- Estatísticas básicas disponíveis e corretas
- Formato de export utilizável:
  - JSON: válido e bem estruturado
  - Markdown: legível e formatado
- Dados permitem identificar oportunidades de otimização (ex: agente mais caro)

---

## ÉPICO 9: Interface Web Conversacional

**Objetivo:** Criar interface web como experiência principal do sistema, com chat fluido, visualização de reasoning dos agentes ("bastidores"), e métricas de custo inline.

**Status:** 🟡 Refinado

**Dependências:**
- Épico 8 POC concluído (reasoning instrumentado)
- Épico 7 concluído (Orquestrador Conversacional)

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
- *Nota: Implementa funcionalidade 7.12 do Épico 7 (Reasoning Explícito das Decisões)*

**9.8: Timeline de agentes (histórico)**
- Lista de agentes executados (colapsado)
- Expandir para ver reasoning de passos anteriores
- Ordenado cronologicamente

**9.9: Reasoning completo (modal)**
- Botão "📄 Ver raciocínio completo" ao lado do resumo
- Modal/dialog com JSON estruturado
- Mostra todos os campos do agente
- *Nota: Implementa funcionalidade 7.12 do Épico 7 (Reasoning Explícito das Decisões)*

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

**Status:** ⚠️ Não refinado

**Dependências:**
- Épico 9 concluído (Interface Web)

**Consulte:** `docs/architecture/state_evolution.md` para detalhes de evolução de estado.

### Progressão POC → Protótipo → MVP

#### POC (persistência básica)

**10.1: Persistência básica de sessões (movido do Épico 9.10)**
- Sessões sobrevivem reload da página
- Implementação inicial: localStorage (navegador) OU SqliteSaver (backend)
- Thread_id vinculado à sessão
- Sidebar recupera lista de sessões ao recarregar

**10.2: Argumento Focal Persistente (movido do Épico 7.14)**
- Campo `focal_argument` salvo junto com sessão
- Recuperado ao retomar conversa
- Permite sistema entender contexto mesmo após dias

**10.3: Pausar e retomar sessão**
- Usuário pode fechar navegador e voltar depois
- Histórico completo preservado (mensagens + bastidores)
- State do LangGraph recuperado via thread_id

**Critérios de aceite POC:**
- Usuário pode fechar navegador e retomar sessão depois
- Histórico de mensagens preservado
- Argumento focal recuperado corretamente
- Sistema continua conversa de onde parou

#### Protótipo (múltiplas sessões)

**10.4: Múltiplas sessões persistidas**
- Sidebar exibe lista de todas as sessões salvas
- Usuário pode criar nova sessão a qualquer momento
- Alternar entre sessões (não simultâneo)

**10.5: Busca de sessões**
- Buscar por título da conversa
- Buscar por data (últimos 7 dias, último mês)
- Filtrar por estágio (se argumento focal incluir estágio)

**10.6: Artefatos versionados**
- Sistema salva versões de hipóteses (V1, V2, V3)
- Timeline mostra evolução de artefatos
- Usuário pode ver "como era antes" de cada refinamento

**10.7: Histórico de decisões do usuário (movido do Épico 7.13)**
- Sistema rastreia decisões: aceitou/refutou sugestões de agentes
- Identifica padrões de preferência (ex: usuário sempre prefere refinar antes de pesquisar)
- Adapta sugestões futuras baseado em histórico

**Critérios de aceite Protótipo:**
- Usuário gerencia múltiplas sessões
- Busca funciona corretamente
- Versões de hipóteses rastreadas
- Preferências do usuário influenciam sugestões

#### MVP (gestão completa)

**10.8: Export de conversas**
- Exportar conversa completa em markdown
- Incluir: mensagens + reasoning dos agentes + métricas
- Formato: `conversa_YYYYMMDD.md`

**10.9: Arquivar sessões concluídas**
- Marcar sessão como "concluída"
- Sessões concluídas movem para seção "Arquivadas"
- Não aparecem na lista principal (reduz poluição visual)

**10.10: Tags/labels customizáveis**
- Usuário pode adicionar tags (ex: "urgente", "revisão", "tese")
- Filtrar sessões por tags
- Busca inclui tags

**Critérios de aceite MVP:**
- Export funciona (markdown legível)
- Arquivamento organiza sessões
- Tags facilitam organização

---

## 📝 Observações

- Cada épico pode ser desenvolvido **isoladamente**
- Entrega **valor incremental**
- Pode ser **testado** antes do próximo
