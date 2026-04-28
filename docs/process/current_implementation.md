# Current Implementation — PROTO-WORKFLOW-PLATAFORMA

**Milestone:** `PROTO-WORKFLOW-PLATAFORMA`
**Branch:** `claude/implement-workflow-prototype-BtiaJ` (harness-assigned; equivalente a `milestone/proto-workflow-plataforma` no fluxo manual)
**ROADMAP:** [docs/process/workflow/ROADMAP.md](workflow/ROADMAP.md)
**Épicos:** W-PROTO-PLAT-1, W-PROTO-PLAT-2, W-PROTO-PLAT-3, W-PROTO-PLAT-4

---

## Sizing (EM) — 2026-04-28 10:30

- Milestone: PROTO-WORKFLOW-PLATAFORMA (Protótipo, workflow)
- Épicos avaliados: 4
- Funcionalidades: 6 (W-PROTO-PLAT-1: 1; W-PROTO-PLAT-2: 1; W-PROTO-PLAT-3: 2; W-PROTO-PLAT-4: 2)
- Fator de risco médio: 1.0 (sem sinais de risco — top-level novo, sem refator, sem dependência core não-✅)
- LOC estimado: 1200 (6 × 200 × 1.0)
- Decisão: **FIT** (≤ 3000)
- Linha persistida em `docs/process/sizing/history.jsonl`

## Status dos Gates (nível milestone)

- [x] EM ✅ 2026-04-28 10:30
- [x] Scrum Master ✅ 2026-04-28 10:35
- [x] Loop por épico concluído (Dev/QA/TL/PO ✅ em todas as funcionalidades)
- [x] RTE ✅ 2026-04-28 10:55

## Evidências de carregamento de skill

```
[EM]  skill carregada: skills/em/skill.md ✅ 2026-04-28 10:30
[SM]  skill carregada: skills/scrum-master/skill.md ✅ 2026-04-28 10:35
[RTE] skill carregada: skills/rte/skill.md ✅ 2026-04-28 10:55
```

---

## Plano (Scrum Master)

Ordem de execução respeita as dependências declaradas no ROADMAP:

1. **W-PROTO-PLAT-1** — Scaffold (foundation): models, parser, config_loader, app entrypoint
2. **W-PROTO-PLAT-2** — Kanban: 8 colunas por estado, agrupado por milestone
3. **W-PROTO-PLAT-3** — Ações de implementação: dispatch (3.1) + status para 🏗️/🔀/✅ (3.2)
4. **W-PROTO-PLAT-4** — Refinamento: NEXT_STEP_MAP (4.1) + prompt de refinamento (4.2)

---

## Épicos

### Épico W-PROTO-PLAT-1: Scaffold da plataforma — Status: ✅ Implementado

#### Gates por funcionalidade

| Funcionalidade | Dev | QA | TL | PO |
|---|---|---|---|---|
| 1.1 App Streamlit com configuração, modelo e parser | ✅ | ✅ | ✅ | ✅ |

Arquivos esperados (entregues):
- `tools/__init__.py`
- `tools/workflow_platform/__init__.py`
- `tools/workflow_platform/app.py`
- `tools/workflow_platform/config.yaml`
- `tools/workflow_platform/config_loader.py`
- `tools/workflow_platform/models.py`
- `tools/workflow_platform/parser.py`
- `tests/tools/__init__.py`
- `tests/tools/workflow_platform/__init__.py`
- `tests/tools/workflow_platform/test_parser.py`
- `tests/tools/workflow_platform/test_config_loader.py`
- `requirements.txt` (adicionado `pyyaml>=6.0`)

### Épico W-PROTO-PLAT-2: Kanban completo — Status: ✅ Implementado

#### Gates por funcionalidade

| Funcionalidade | Dev | QA | TL | PO |
|---|---|---|---|---|
| 2.1 Kanban de estados por milestone | ✅ | ✅ | ✅ | ✅ |

Arquivos:
- `tools/workflow_platform/views/__init__.py`
- `tools/workflow_platform/views/kanban.py`
- `tests/tools/workflow_platform/test_kanban.py`

### Épico W-PROTO-PLAT-3: Ações de implementação — Status: ✅ Implementado

#### Gates por funcionalidade

| Funcionalidade | Dev | QA | TL | PO |
|---|---|---|---|---|
| 3.1 Dispatch para 🔍 | ✅ | ✅ | ✅ | ✅ |
| 3.2 Status para 🏗️/🔀/✅ | ✅ | ✅ | ✅ | ✅ |

Arquivos:
- `tools/workflow_platform/prompts/__init__.py`
- `tools/workflow_platform/prompts/dispatch.py`
- `tools/workflow_platform/views/card_detail.py`
- `tests/tools/workflow_platform/test_dispatch_prompt.py`

### Épico W-PROTO-PLAT-4: Direcionamento de refinamento — Status: ✅ Implementado

#### Gates por funcionalidade

| Funcionalidade | Dev | QA | TL | PO |
|---|---|---|---|---|
| 4.1 Próximo passo por estado pré-execução | ✅ | ✅ | ✅ | ✅ |
| 4.2 Prompt de refinamento | ✅ | ✅ | ✅ | ✅ |

Arquivos:
- `tools/workflow_platform/prompts/refinement.py`
- `tests/tools/workflow_platform/test_refinement_prompt.py`
- `tools/workflow_platform/views/card_detail.py` (rotas 🌱/🧭/📐/📋)

---

## Extração pendente

- Épico W-PROTO-PLAT-1: (vazio — TL não identificou conhecimento permanente neste épico)
- Épico W-PROTO-PLAT-2: (vazio — TL não identificou conhecimento permanente neste épico)
- Épico W-PROTO-PLAT-3: (vazio — TL não identificou conhecimento permanente neste épico)
- Épico W-PROTO-PLAT-4: (vazio — TL não identificou conhecimento permanente neste épico)

---

## Resumo Final do Milestone

- **Milestone:** PROTO-WORKFLOW-PLATAFORMA — Plataforma de Workflow
- **Estágio:** Protótipo
- **Épicos fechados:** 4 (W-PROTO-PLAT-1, 2, 3, 4)
- **Funcionalidades validadas:** 6
- **Testes novos:** 29 (todos passando)
- **Suite global:** 453 testes passam (`pytest tests/ -m "not integration and not slow" --ignore=tests/core/integration --ignore=tests/products/ensaio`); nenhum teste pré-existente quebrado
- **Arquivos novos:** ~14 em `tools/workflow_platform/` + `tests/tools/workflow_platform/`
- **Arquivos modificados:** `requirements.txt` (+pyyaml), `docs/process/sizing/history.jsonl` (linha de decisão)
- **Stack:** Streamlit (já em requirements.txt), pyyaml (adicionado), regex puro no parser
- **Decisão arquitetural:** plataforma top-level em `tools/workflow_platform/` — fora de `products/` por princípio "workflow é processo, não produto" ([vision.md](workflow/vision.md))
