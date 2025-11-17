# ROADMAP - Paper Agent

> **📖 Status Atual:** Para entender o estado atual do sistema (épicos concluídos, funcionalidades implementadas), consulte [README.md](README.md) e [ARCHITECTURE.md](ARCHITECTURE.md).

> **📖 Melhorias Técnicas:** Para funcionalidades planejadas não vinculadas a épicos, consulte [docs/backlog.md](docs/backlog.md).

> **📖 Visão de Produto:** Para entender tipos de artigo, fluxos adaptativos e jornada do usuário, consulte `docs/product/vision.md`.

---

## 📋 Status dos Épicos

### 🟡 Épicos Em Andamento
- _Nenhum épico em andamento no momento_

### ⏳ Épicos Planejados
- **ÉPICO 11**: Modelagem Cognitiva (não refinado)
- **ÉPICO 12**: Persistência de Tópicos (não refinado)
- **ÉPICO 13**: Gestão de Múltiplos Tópicos (não refinado)
- **ÉPICO 14+**: Agentes Avançados - Pesquisador, Escritor, Crítico (não refinado)

**Regra**: Claude Code só trabalha em funcionalidades de épicos refinados.

> Para fluxo completo de planejamento, consulte `planning_guidelines.md`.

---

## ÉPICO 11: Modelagem Cognitiva

**Objetivo:** Implementar modelo cognitivo explícito que captura evolução do pensamento do usuário ao longo da conversa, permitindo rastreamento de premissas, suposições, dúvidas e contradições.

**Status:** ⏳ Planejado (não refinado)

**Dependências:**
- ✅ Épico 9 concluído (Interface Web Conversacional)
- ✅ Épico 7 concluído (Orquestrador Conversacional)

**Consulte:** 
- `docs/product/cognitive_model.md` - Modelo conceitual completo
- `docs/architecture/topic_argument_model.md` - Relação Tópico ↔ Argumento

---

## ÉPICO 12: Persistência de Tópicos

**Objetivo:** Permitir pausar/retomar conversas com contexto completo preservado, salvando modelo cognitivo no checkpoint do LangGraph.

**Status:** ⏳ Planejado (não refinado)

**Dependências:**
- Épico 11 concluído (Modelagem Cognitiva)

**Consulte:** 
- `docs/architecture/topic_argument_model.md` - Estrutura de dados e progressão POC → MVP
- `docs/product/vision.md` (Seção 4) - Entidade Tópico

---

## ÉPICO 13: Gestão de Múltiplos Tópicos

**Objetivo:** Permitir usuário gerenciar múltiplos tópicos em progresso, alternando entre eles via sidebar e buscando por título/stage.

**Status:** ⏳ Planejado (não refinado)

**Dependências:**
- Épico 12 concluído (Persistência de Tópicos)

**Consulte:** 
- `docs/architecture/topic_argument_model.md` - Casos de uso e estrutura de dados

---

## ÉPICO 14+: Agentes Avançados

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
