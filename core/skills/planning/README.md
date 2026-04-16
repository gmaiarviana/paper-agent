# Planning Skill

> **📌 Localização:** `core/skills/planning/`
> **📌 Etapa do fluxo:** primeira (antes do Dev) — `docs/process/autonomous/workflow.md` §1
> **📌 Pré-requisito:** funcionalidade pertence a épico **refinado** no ROADMAP.

---

## 1. QUANDO USAR

Use quando o dispatch autônomo (`AUTONOMOUS_DISPATCH.md`) é recebido e antes de qualquer linha de código ser escrita.

**Não usar se:**
- ❌ Funcionalidade está em épico não-refinado (refinamento é manual via Claude Web)
- ❌ Há decisão arquitetural em aberto (devolver ao dev)
- ❌ `docs/process/current_implementation.md` já existe (épico anterior não fechou)

---

## 2. COMO FUNCIONA

A skill executa, em ordem:

1. **Leitura de contexto** — ROADMAP (core ou produto), ARCHITECTURE.md, `docs/CONTEXT_INDEX.md`, specs do tema afetado.
2. **Quebra em tasks** — divide a funcionalidade em tarefas curtas e ordenadas por dependência técnica.
3. **Detecção de ambiguidades** — varre critérios de aceite e contexto técnico em busca de pontos abertos.
4. **Resolução por consulta** — para cada ambiguidade, tenta resolver via docs antes de assumir.
5. **Bloco de perguntas** — se sobrar dúvida, **PARA** e devolve ao dev em bloco único (não fragmentado).
6. **Domain tags** — anota domínio de cada task (`backend`, `frontend`, `data`, `docs`, `tests`) para evitar conflitos em paralelização futura.
7. **Persistência do plano** — escreve em `docs/process/current_implementation.md` no formato canônico (template em `skill.md`).

**Princípio:** a skill **clarifica TUDO antes de iniciar**. Qualquer ambiguidade não resolvida é bloqueio explícito, não suposição silenciosa.

---

## 3. INPUT ESPERADO

- Funcionalidade `X.Y` (id do ROADMAP)
- Branch alvo (`feature/X.Y-nome`)
- Roadmap aplicável (`core/ROADMAP.md` ou `products/<produto>/ROADMAP.md`)

Geralmente vem preenchido via `AUTONOMOUS_DISPATCH.md`.

---

## 4. OUTPUT PRODUZIDO

- ✅ `docs/process/current_implementation.md` criado com plano completo
- ✅ Lista de tasks com domain tags
- ✅ Estimativa por task (LOC aproximado, risco baixo/médio/alto)
- ✅ Lista de arquivos esperados (criados/modificados)
- ✅ Bloco de esclarecimentos (vazio se nada ficou em aberto)

Estrutura detalhada em [skill.md](skill.md).

---

## 5. EXEMPLOS

- [examples/clarification-example.md](examples/clarification-example.md) — caso típico onde a skill identifica 3 ambiguidades, resolve 2 via docs e devolve 1 ao dev.

---

## 6. INTERAÇÃO COM OUTRAS SKILLS

| Skill seguinte | Como recebe input |
|----------------|-------------------|
| **Dev** | Lê `current_implementation.md` (tasks + arquivos esperados) |
| **PO** (depois) | Reusa o mapeamento crítério-de-aceite ↔ task que Planning produziu |

Quando **PO reprova** por gap de plano (não de implementação), o fluxo volta para Planning revisar.

---

**Ver também:**
- Prompt operacional → [skill.md](skill.md)
- Etapa no fluxo geral → `docs/process/autonomous/workflow.md` §1
- Estrutura geral de skills → `core/skills/README.md`
