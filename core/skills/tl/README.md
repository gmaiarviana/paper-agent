# TL Skill (Tech Lead)

> **📌 Localização:** `core/skills/tl/`
> **📌 Etapa do fluxo:** quarta (após QA) — `docs/process/autonomous/workflow.md` §4
> **📌 Pré-requisito:** QA Skill aprovou.

---

## 1. PAPEL

A TL Skill é o **gate arquitetural**. Decide **binariamente** se a implementação está alinhada com os padrões técnicos do projeto.

**Princípio:** funcionar não basta — tem que estar no padrão. Divergência arquitetural sem justificativa documentada = rejeição.

---

## 2. CRITÉRIOS DE APROVAÇÃO

Aprova **APENAS** quando **TODOS** os itens forem verdadeiros:

- ✅ Decisões alinhadas com `ARCHITECTURE.md`
- ✅ Padrões dos módulos análogos preservados (estrutura de pastas, nomenclatura, contratos)
- ✅ Sem duplicação de informação entre docs (CONSTITUTION §6 e `.claudecode.md`)
- ✅ Sem débito técnico desnecessário introduzido (TODOs vagos, `# FIXME` sem issue, código morto)
- ✅ Domínio correto: código no lugar certo (`core/agents/`, `core/utils/`, `products/<x>/`, etc)
- ✅ Escopo coerente com ROADMAP da funcionalidade — sem extrapolar (ver PO Skill para gold plating)
- ✅ Documentação estrutural (`ARCHITECTURE.md`, specs em `docs/`, `core/docs/`) atualizada se a estrutura mudou

---

## 3. CRITÉRIOS DE REJEIÇÃO

Rejeita **automaticamente** se **qualquer** item ocorrer:

- ❌ Padrão divergente de módulo análogo sem justificativa em commit/doc
- ❌ Decisão arquitetural quebrada (contraria `ARCHITECTURE.md` ou specs)
- ❌ Documentação estrutural desalinhada do código entregue
- ❌ Duplicação de informação entre docs (mesma spec em 2 lugares)
- ❌ Código no domínio errado (ex: lógica de produto em `core/`, util compartilhado em produto específico)
- ❌ Débito introduzido sem registro/justificativa (TODO vago, dependência circular nova, hack temporário)

---

## 4. INPUT ESPERADO

- Branch `feature/X.Y-nome` aprovada por QA
- `current_implementation.md` com `QA ✅`
- ROADMAP da funcionalidade
- `ARCHITECTURE.md` + specs do tema afetado (via `docs/CONTEXT_INDEX.md`)

---

## 5. OUTPUT PRODUZIDO

- ✅ Decisão binária registrada em `current_implementation.md`
- ✅ Lista de pontos verificados (com referência a `ARCHITECTURE.md` / módulos análogos)
- ✅ Em caso de rejeição: lista específica de desvios + arquivo + linha + padrão esperado

---

## 6. INTERAÇÃO COM OUTRAS SKILLS

| Cenário | Próxima ação |
|---------|--------------|
| Aprovou | Fluxo segue para **PO Skill** |
| Rejeitou | Fluxo volta para **Dev** com lista de desvios |
| 3 rejeições consecutivas | Aplicar `docs/process/development/blockers.md` |

TL **não reescreve código**. Aponta padrão correto e devolve.

---

## 7. EXEMPLOS

- [examples/approval-case.md](examples/approval-case.md) — caso de aprovação simples
- [examples/rejection-case.md](examples/rejection-case.md) — caso de rejeição com 2 desvios apontados

---

**Ver também:**
- Prompt operacional → [skill.md](skill.md)
- Padrões arquiteturais → `ARCHITECTURE.md`
- Princípios anti-duplicação → `CONSTITUTION.md` §6 e `.claudecode.md`
- Próximo gate → `core/skills/po/README.md`
