# Exemplo: Clarificação Bem-Sucedida

> **Contexto:** caso real (anonimizado) onde a Planning Skill identificou 3 ambiguidades, resolveu 2 via consulta a docs e devolveu 1 ao dev em bloco único.

---

## Dispatch Recebido

```
Dispatch Autônomo - Funcionalidade 11.3

Funcionalidade: 11.3 - Detecção de Maturidade via Snapshots
Roadmap: core/ROADMAP.md
Branch: feature/11.3-snapshot-detection
Modo: Autônomo
```

---

## Critérios de Aceite (extraídos do ROADMAP)

- Deve criar snapshot do estado da Ideia em cada turno relevante
- Deve detectar quando a Ideia atinge maturidade conforme heurística definida
- Deve persistir snapshots de forma consultável
- Não deve disparar snapshot em turnos puramente conversacionais

---

## Ambiguidades Detectadas (Passo 4)

### Ambiguidade #1 — "turno relevante"
**O que é "relevante"?** Critério não está nos critérios de aceite literais.

**Tentativa de resolução (Passo 5):**
- Consultei `core/docs/architecture/patterns/snapshots.md` → encontrei definição: "turno relevante = turno em que houve mudança em ≥1 campo do `CognitiveModel`"
- ✅ **Resolvido via doc.** Fonte: `core/docs/architecture/patterns/snapshots.md:42`

### Ambiguidade #2 — heurística de maturidade
**Qual heurística?** Critério cita "heurística definida" sem explicitar.

**Tentativa de resolução:**
- Consultei `core/agents/persistence/snapshot_manager.py` → função `is_mature()` já existe e usa contagem de fundamentos sólidos
- Consultei `core/docs/vision/cognitive_model/` → confirma critério (≥3 fundamentos com `confidence >= 0.7`)
- ✅ **Resolvido via doc + código.** Fonte: `core/agents/persistence/snapshot_manager.py:88` + `core/docs/vision/cognitive_model/maturity.md`

### Ambiguidade #3 — formato de persistência
**Snapshots em SQLite ou ChromaDB?** Critério diz "consultável" mas não especifica backend.

**Tentativa de resolução:**
- Consultei `core/docs/architecture/data-models/persistence.md` → menciona ambos sem regra clara
- Consultei `core/agents/database/schema.py` → não tem tabela de snapshots
- Consultei `tech_stack.md` → SQLite para estruturado, ChromaDB para vetorial; snapshot é estruturado
- ⚠️ **Inferência possível** (SQLite), mas a doc não fecha — duas instalações análogas usaram caminhos diferentes
- ❌ **Não resolvido.** Devolvido ao dev.

---

## Bloco de Perguntas Devolvido ao Dev (Passo 7)

```
🛑 Planning bloqueado — esclarecimentos necessários

Funcionalidade: 11.3 - Detecção de Maturidade via Snapshots
Branch alvo: feature/11.3-snapshot-detection

Já consultei:
- core/ROADMAP.md (funcionalidade 11.3)
- core/docs/architecture/patterns/snapshots.md
- core/docs/architecture/data-models/persistence.md
- core/docs/architecture/infrastructure/tech_stack.md
- core/agents/persistence/snapshot_manager.py
- core/agents/database/schema.py

Resolvi via consulta:
- ✅ Definição de "turno relevante" — fonte: snapshots.md:42
- ✅ Heurística de maturidade — fonte: snapshot_manager.py:88 + cognitive_model/maturity.md

Perguntas que preciso responder antes de gerar o plano:

1. Backend de persistência dos snapshots: SQLite (nova tabela) ou ChromaDB?
   - SQLite: consultas estruturadas mais simples, mas exige migration do schema
   - ChromaDB: reuso da infra vetorial existente, mas snapshot não é dado vetorial natural
   - tech_stack.md sugere SQLite para estruturado, mas tem precedente em ChromaDB também

Sem essa resposta não posso definir Task de schema/migration nem padrão de retrieval.
```

---

## Resposta do Dev

> "Vai de SQLite, nova tabela `snapshots`. ChromaDB fica fora do escopo dessa funcionalidade."

---

## Resultado

A Planning Skill incorporou a resposta no bloco de Esclarecimentos, gerou plano completo em `current_implementation.md` com 4 tasks (3 backend + 1 data) e seguiu para o Dev sem deixar suposição.

**Sem essa clarificação**, o Dev teria 50% de chance de implementar o backend errado e o PO reprovaria por divergência de arquitetura — perdendo um ciclo inteiro do gate.

---

## O QUE ESTE EXEMPLO ENSINA

- ✅ **Consulta vem antes da pergunta.** 2 das 3 ambiguidades foram resolvidas sem custar nada ao dev.
- ✅ **Bloco único.** A pergunta foi entregue de uma vez, com o trabalho de pesquisa explícito (mostra que não é preguiça).
- ✅ **Trade-offs explicitados.** A pergunta inclui as opções e por que cada uma é plausível — facilita decisão do dev.
- ❌ **Antipadrão evitado:** assumir SQLite porque "parecia mais comum" e descobrir o erro só no gate de TL.
