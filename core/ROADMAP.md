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

#### ÉPICO 2: Escritor (Writer)

**Objetivo:** Agente para compilação de texto. Primeiro a ser implementado dos três agentes core planejados, motivado pelo produto Ensaio e compartilhado futuramente com o Produtor Científico.

**Status:** ⏳ Planejado (não refinado)

**Dependências:**
- Nenhuma (pode iniciar antes do Pesquisador, pois é tracionado pelo Ensaio)

**Decisões arquiteturais já tomadas:** ver `core/docs/architecture/agents/writer.md`
- Nasce no core (não no Ensaio)
- Começa simples: nó que recebe contexto e devolve markdown
- Estruturas de artigo vivem no prompt do Writer (não em enum/schema)
- Organização inicial antecipa generalização para o Produtor Científico

**Próximos Passos:**
- Refinar critérios de aceite e interface (inputs/outputs estruturados) antes da implementação

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
