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

### [Multi-Agent](./multi_agent/)
Super-grafo multi-agente (Épico 3-4) — orquestração do sistema de agentes como um todo.

**Nota:** Para arquitetura e responsabilidades de cada agente individual, ver [../agents/](../agents/) (cada agente tem sua própria pasta com `responsibilities.md` e, quando aplicável, `architecture.md` / `design.md`).

### [Patterns](./patterns/)
Padrões e estratégias de design
- [Snapshots](./patterns/snapshots.md) - Quando e como criar snapshots
- [Refinement](./patterns/refinement.md) - Loop colaborativo de refinamento

### [Infrastructure](./infrastructure/)
Infraestrutura técnica (stack, ferramentas)
- [Tech Stack](./infrastructure/tech_stack.md) - ChromaDB, SQLite, sentence-transformers
- [Config System](./infrastructure/config_system.md) - YAML configs, memória, execution tracker

---

## 🔗 Referências Relacionadas

- [Visão e Filosofia](../vision/) - Filosofia, visão de longo prazo e super-sistema
- [Modelo Cognitivo](../vision/cognitive_model/) - Base epistemológica
- [Agentes](../agents/) - Pasta por agente com responsabilidades e design técnico
- [Produtos](../../../products/) - Revelar, Ensaio, etc
