# ROADMAP - Core Universal

Épicos e melhorias do sistema core que serve todos os produtos.

> **📖 Status Atual:** Para entender o estado atual do core, consulte [ARCHITECTURE.md](../../ARCHITECTURE.md) e [core/docs/](../../core/docs/).

> **📖 Visão:** Para entender a filosofia do sistema, consulte [core/docs/vision/system_philosophy.md](docs/vision/system_philosophy.md).

---

## 📋 Épicos Planejados

### ⏳ Épicos Planejados (não refinados)

#### ÉPICO 1: Pesquisador

**Objetivo:** Agente para busca e síntese de literatura científica. Introduz Evidência como entidade prática.

**Status:** ⏳ Planejado (não refinado)

**Dependências:**
- Revelar ÉPICO 2 (Catálogo de Conceitos)

**Nota:** Pesquisador pode usar catálogo de conceitos para buscar papers relacionados.

**Próximos Passos:**
- Discutir comportamento e interface antes do refinamento
- Definir integração com Observer e catálogo de conceitos

---

#### ÉPICO 2: Escritor

**Objetivo:** Agente para compilação de seções do artigo científico.

**Status:** ⏳ Planejado (não refinado)

**Dependências:**
- ÉPICO 1 (Pesquisador)

**Próximos Passos:**
- Discutir comportamento e integração com outros agentes antes do refinamento

---

> **📖 Melhorias Técnicas:** Para melhorias técnicas não vinculadas a épicos, consulte [docs/backlog.md](../../docs/backlog.md).

---

## 📚 Documentação

- `core/docs/vision/system_philosophy.md` - Filosofia do sistema
- `core/docs/architecture/` - Estrutura técnica
- `core/docs/agents/` - Especificações dos agentes

---

## 📝 Observações

**Regra:** Claude Code só trabalha em funcionalidades de épicos refinados.

> Para fluxo completo de planejamento, consulte [planning_guidelines.md](../../docs/process/refinement/planning_guidelines.md).

- Cada épico pode ser desenvolvido **isoladamente**
- Entrega **valor incremental**
- Pode ser **testado** antes do próximo
- Épicos não refinados requerem discussão antes da implementação
