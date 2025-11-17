# Fundação de Persistência

## Visão Geral

Infraestrutura básica de persistência usando SQLite local + SqliteSaver do LangGraph.

## Decisões Arquiteturais

- **SQLite** local (agora) → **PostgreSQL** cloud (futuro)
- **SqliteSaver** do LangGraph para checkpoints de conversa
- **Tabelas customizadas** para entidades (ideas, arguments)

## SqliteSaver (LangGraph Checkpoints)

- Arquivo: `checkpoints.db`
- Gerencia: Histórico de mensagens, estado da conversa
- Permite: Pausar/retomar sessões
- Código básico:
```python
from langgraph.checkpoint.sqlite import SqliteSaver
checkpointer = SqliteSaver.from_conn_string("checkpoints.db")
```

## Schema SQLite Inicial

### Tabela: ideas
- id (UUID, PK)
- title (TEXT)
- status (TEXT) - "exploring" | "structured" | "validated"
- current_argument_id (UUID, FK NULLABLE → arguments.id)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)

### Tabela: arguments
- id (UUID, PK)
- idea_id (UUID, FK → ideas.id)
- claim (TEXT)
- premises (JSON)
- assumptions (JSON)
- open_questions (JSON)
- contradictions (JSON)
- solid_grounds (JSON)
- context (JSON)
- version (INT) - auto-incrementa por idea_id
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)

### Constraints
- FOREIGN KEY (idea.current_argument_id) REFERENCES arguments(id)
- FOREIGN KEY (argument.idea_id) REFERENCES ideas(id)

## Estratégia de Migração Futura

### SQLite → PostgreSQL
Quando escalar para produção:
1. Script de migração de dados
2. Ajustar connection strings
3. Aproveitar índices do PostgreSQL
4. Manter compatibilidade de schema

### Sem Breaking Changes
- Schema SQLite = Schema PostgreSQL
- Mesmas queries funcionam em ambos
- Migration path documentado mas não implementado ainda

## Referências
- `docs/architecture/idea_model.md` - Schema de Idea
- `docs/architecture/argument_model.md` - Schema de Argument

