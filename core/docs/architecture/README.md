# Arquitetura do Core

Documentação técnica da arquitetura do sistema core (universal, compartilhado entre produtos).

## 📋 Estrutura

### [Data Models](./data-models/)
Modelagem de dados - ontologia, schemas, persistência
- [Ontologia](./data-models/ontology.md) - SSoT filosófico (Conceito, Ideia, Argumento, Proposição, Evidência)
- [Idea Model](./data-models/idea_model.md) - Schema técnico de Ideia
- [Argument Model](./data-models/argument_model.md) - Schema técnico de Argumento
- [Concept Model](./data-models/concept_model.md) - Schema técnico de Conceito
- [Persistence](./data-models/persistence.md) - SQLite, checkpointer, schema base

### [Agents](./agents/)
Arquitetura técnica dos agentes do core
- [Observer](./agents/observer/architecture.md) - Implementação técnica do Observador

**Nota:** Para visão conceitual dos agentes (papel, responsabilidades), ver [../agents/overview.md](../agents/overview.md)

**Nota:** Para documentação de orchestrator e multi-agent, ver [../../orchestration/](../../orchestration/)

### [Patterns](./patterns/)
Padrões e estratégias de design
- [Snapshots](./patterns/snapshots.md) - Quando e como criar snapshots

### [Infrastructure](./infrastructure/)
Infraestrutura técnica (stack, ferramentas)
- [Tech Stack](./infrastructure/tech_stack.md) - ChromaDB, SQLite, sentence-transformers

### [Vision](./vision/)
Visão arquitetural de longo prazo
- [Super System](./vision/super_system.md) - Core universal → Múltiplos produtos

---

## 🔗 Referências Relacionadas

- [Visão do Produto](../../vision/) - Filosofia e visão de longo prazo
- [Modelo Cognitivo](../../vision/cognitive_model/) - Base epistemológica
- [Agentes (Conceitual)](../agents/) - Papel e responsabilidades dos agentes
- [Orquestração](../../orchestration/) - Documentação de orchestrator e multi-agent

