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
- [Orchestrator](./agents/orchestrator/) - Implementações do Orquestrador
  - [Conversational](./agents/orchestrator/conversational/) - Orquestrador Conversacional (Épico 7)
  - [Socratic](./agents/orchestrator/socratic.md) - Orquestrador Socrático (Épico 10)
- [Multi-Agent](./agents/multi_agent/) - Super-grafo multi-agente (Épico 3-4)

**Nota:** Para visão conceitual dos agentes (papel, responsabilidades), ver [../agents/overview.md](../agents/overview.md)

### [Patterns](./patterns/)
Padrões e estratégias de design
- [Snapshots](./patterns/snapshots.md) - Quando e como criar snapshots
- [Refinement](./patterns/refinement.md) - Loop colaborativo de refinamento

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
- [Produtos](../../../products/) - Paper-agent, Fichamento, etc

