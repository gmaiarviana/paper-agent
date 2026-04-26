# PO Skill (Product Owner)

> **📌 Localização:** `skills/po/`
> **📌 Etapa do fluxo:** quinta (após TL) — `docs/process/autonomous/workflow.md` §5
> **📌 Pré-requisito:** TL Skill aprovou.

---

## 1. PAPEL

A PO Skill é o **gate de produto**. Decide **binariamente** se a entrega cumpre os critérios de aceite do ROADMAP.

**Princípio:** código bom + arquitetura correta não bastam — tem que entregar o que foi pedido. Nem mais, nem menos.

---

## 2. CRITÉRIOS DE APROVAÇÃO

Aprova **APENAS** quando **TODOS** os itens forem verdadeiros:

- ✅ Todos os critérios de aceite do ROADMAP (X.Y) estão atendidos
- ✅ Cada critério tem cobertura observável (teste OU script de validação OU rota/comando manual claro)
- ✅ Comportamentos "não deve" foram validados (não basta o "deve" funcionar)
- ✅ Funcionalidade é utilizável pelo usuário final (não exige etapas escondidas)
- ✅ Sem **gold plating**: nada implementado fora do escopo da X.Y
- ✅ ROADMAP marcado como concluído quando aplicável (✅ + resumo de 1-2 linhas)

---

## 3. CRITÉRIOS DE REJEIÇÃO

Rejeita **automaticamente** se **qualquer** item ocorrer:

- ❌ Critério de aceite não coberto/observável
- ❌ Comportamento "não deve" não foi validado
- ❌ Funcionalidade exige passo manual escondido para funcionar
- ❌ **Gold plating**: implementou comportamento extra fora do escopo (mesmo que "útil")
- ❌ ROADMAP não atualizado (ou atualizado com texto que não reflete entrega)

> **Importante:** rejeição por gap de plano (Scrum Master não previu o critério) volta para **Scrum Master**, não para Dev. Rejeição por gap de implementação volta para **Dev**.

---

## 4. INPUT ESPERADO

- Branch `milestone/<id-em-caixa-baixa>` aprovada por QA + TL
- `current_implementation.md` com `QA ✅` e `TL ✅`
- Mapeamento crítério ↔ task gerado por Scrum Master
- ROADMAP da funcionalidade

---

## 5. OUTPUT PRODUZIDO

- ✅ Decisão binária registrada em `current_implementation.md`
- ✅ Checklist completo no formato [templates/acceptance-criteria.md](templates/acceptance-criteria.md)
- ✅ Em caso de rejeição: lista específica de critérios não atendidos OU itens fora do escopo

---

## 6. INTERAÇÃO COM OUTRAS SKILLS

| Cenário | Próxima ação |
|---------|--------------|
| Aprovou | Fluxo segue para **RTE Skill** |
| Rejeitou (gap de implementação) | Devolve para **Dev** |
| Rejeitou (gap de plano) | Devolve para **Scrum Master** |
| 3 rejeições consecutivas | `docs/process/implementation/blockers.md` |

PO **não negocia critério**. Critério de aceite vem do ROADMAP — se está mal escrito, é problema de refinamento (manual via Claude Web), não da PO Skill.

---

## 7. RELAÇÃO COM TL SKILL

Existe sobreposição aparente sobre "escopo": TL valida escopo **arquitetural** (mexeu em módulo fora do tema?); PO valida escopo **funcional** (entregou comportamento extra fora do critério de aceite?).

Os dois gates podem capturar o mesmo problema por ângulos diferentes — isso é desejável, é redundância intencional.

---

**Ver também:**
- Prompt operacional → [skill.md](skill.md)
- Template do checklist → [templates/acceptance-criteria.md](templates/acceptance-criteria.md)
- Critérios de aceite → ROADMAP da funcionalidade
- Próximo gate → `skills/rte/README.md`
