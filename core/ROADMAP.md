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

### ⏳ Épicos Motivados pelo Ensaio (não refinados)

> **Nota:** Estes épicos são **motivados pelo produto Ensaio** (primeiro produto com necessidades além das do Revelar) mas **pertencem ao core** — serão reusados por outros produtos, especialmente Produtor Científico. O prefixo `C-ENSAIO-` identifica a motivação; o código fica no core e respeita o desacoplamento descrito em [core/docs/architecture/vision/super_system.md](docs/architecture/vision/super_system.md).

#### ÉPICO C-ENSAIO-1: Parametrização de Contexto de Produto nos Agentes

**Objetivo:** Agentes do core (Orquestrador e futuros) aceitam foco/domínio passado por produtos externos sem que o core conheça os produtos. Mecanismo de configuração a definir no refinamento.

**Status:** ⏳ Planejado (não refinado)

**Consulte:** [core/docs/architecture/vision/super_system.md](docs/architecture/vision/super_system.md) (seção "Injeção de Contexto de Produto")

---

#### ÉPICO C-ENSAIO-2: Writer (Versão Inicial)

**Objetivo:** Novo agente no core que recebe contexto conversacional e cognitive_model, devolve markdown estruturado. Nasce simples. Organizado para generalização futura (Produtor Científico reusará).

**Status:** ⏳ Planejado (não refinado)

**Decisões arquiteturais já tomadas:** ver [core/docs/architecture/agents/writer.md](docs/architecture/agents/writer.md)
- Nasce no core (não no Ensaio)
- Começa simples: nó que recebe contexto e devolve markdown
- Estruturas de artigo vivem no prompt do Writer (não em enum/schema)
- Organização inicial antecipa generalização para o Produtor Científico

**Próximos Passos:**
- Refinar critérios de aceite e interface (inputs/outputs estruturados) antes da implementação

---

#### ÉPICO C-ENSAIO-3: Writer Gera por Seção (Evolução)

**Objetivo:** Writer evolui para gerar artigo seção por seção em vez de bloco único, permitindo refinamento granular.

**Status:** ⏳ Planejado (não refinado)

**Dependências:**
- C-ENSAIO-2 (Writer versão inicial)

---

#### ÉPICO C-ENSAIO-4: Ingestão de Arquivos Anexados (Core)

**Objetivo:** Mecanismo genérico para agentes do core consumirem conteúdo de arquivos anexados (notebook, markdown, CSV, imagens). Detalhes de parsing/extração a definir no refinamento.

**Status:** ⏳ Planejado (não refinado)

---

#### ÉPICO C-ENSAIO-5: Promoção de Entidade Pendência para o Core (Condicional)

**Objetivo:** Pendência nasce no produto Ensaio; promover para o core quando segundo produto precisar (provavelmente Produtor Científico). Épico condicionado à existência de segundo caso de uso.

**Status:** ⏳ Planejado (não refinado, condicional)

**Consulte:** [core/docs/architecture/data-models/ontology.md](docs/architecture/data-models/ontology.md) (seção "Entidades em Incubação")

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
