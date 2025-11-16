# ROADMAP - Paper Agent

> **📖 Status Atual:** Para entender o estado atual do sistema (épicos concluídos, funcionalidades implementadas), consulte [README.md](README.md) e [ARCHITECTURE.md](ARCHITECTURE.md).

> **📖 Melhorias Técnicas:** Para funcionalidades planejadas não vinculadas a épicos, consulte [docs/backlog.md](docs/backlog.md).

> **📖 Visão de Produto:** Para entender tipos de artigo, fluxos adaptativos e jornada do usuário, consulte `docs/product/vision.md`.

---

## 📋 Status dos Épicos

### ✅ Épicos Concluídos
- **Épico 1-8**: Sistema multi-agente conversacional completo (ver [ARCHITECTURE.md](ARCHITECTURE.md))

### 🟡 Épicos Em Andamento
- _Nenhum épico em andamento no momento_

### ⏳ Épicos Planejados
- **ÉPICO 9**: Interface Web Conversacional (refinado, pronto para implementação)
- **ÉPICO 10**: Modelagem Cognitiva (não refinado)
- **ÉPICO 11**: Persistência de Tópicos (não refinado)
- **ÉPICO 12**: Gestão de Múltiplos Tópicos (não refinado)
- **ÉPICO 13+**: Agentes Avançados - Pesquisador, Escritor, Crítico (não refinado)

**Regra**: Claude Code só trabalha em funcionalidades de épicos refinados.

> Para fluxo completo de planejamento, consulte `planning_guidelines.md`.

---

## ÉPICO 9: Interface Web Conversacional

**Objetivo:** Criar interface web como experiência principal do sistema, com chat fluido, visualização de reasoning dos agentes ("bastidores"), e métricas de custo inline.

**Status:** 🟡 Em Progresso Parcial (scaffold criado, pronto para integração)

**Dependências:**
- ✅ Épico 7 concluído (Orquestrador Conversacional)

**Ver spec técnica completa em `docs/interface/web.md`**

**Progresso Atual (16/11/2025):**
- ✅ **Scaffold completo:** `app/chat.py` + componentes base criados
- ✅ **9.9 completo:** `storage.py` com localStorage funcional (Protótipo)
- ⏳ **9.1-9.8:** Pronto para implementação com backend instrumentado

**Arquivos criados:**
- `app/chat.py` - Layout 3 colunas + integração de componentes
- `app/components/chat_input.py` - Esqueleto para input de mensagens
- `app/components/chat_history.py` - Esqueleto para histórico
- `app/components/backstage.py` - Esqueleto para painel de reasoning
- `app/components/sidebar.py` - Esqueleto para lista de sessões
- `app/components/storage.py` - **Funcional:** Persistência localStorage

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
- Polling otimizado (1s de intervalo)
- Métricas consolidadas visíveis
- Todas as sessões compartilhadas (sem autenticação)

---

## ÉPICO 10: Modelagem Cognitiva

**Objetivo:** Implementar modelo cognitivo explícito que captura evolução do pensamento do usuário ao longo da conversa, permitindo rastreamento de premissas, suposições, dúvidas e contradições.

**Status:** ⏳ Planejado (não refinado)

**Dependências:**
- ✅ Épico 9 concluído (Interface Web Conversacional)
- ✅ Épico 7 concluído (Orquestrador Conversacional)

**Consulte:** 
- `docs/product/cognitive_model.md` - Modelo conceitual completo
- `docs/architecture/topic_argument_model.md` - Relação Tópico ↔ Argumento

---

## ÉPICO 11: Persistência de Tópicos

**Objetivo:** Permitir pausar/retomar conversas com contexto completo preservado, salvando modelo cognitivo no checkpoint do LangGraph.

**Status:** ⏳ Planejado (não refinado)

**Dependências:**
- Épico 10 concluído (Modelagem Cognitiva)

**Consulte:** 
- `docs/architecture/topic_argument_model.md` - Estrutura de dados e progressão POC → MVP
- `docs/product/vision.md` (Seção 4) - Entidade Tópico

---

## ÉPICO 12: Gestão de Múltiplos Tópicos

**Objetivo:** Permitir usuário gerenciar múltiplos tópicos em progresso, alternando entre eles via sidebar e buscando por título/stage.

**Status:** ⏳ Planejado (não refinado)

**Dependências:**
- Épico 11 concluído (Persistência de Tópicos)

**Consulte:** 
- `docs/architecture/topic_argument_model.md` - Casos de uso e estrutura de dados

---

## ÉPICO 13+: Agentes Avançados

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
