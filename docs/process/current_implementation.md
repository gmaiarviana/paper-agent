# Implementação Atual: Milestone PROTO-WORKFLOW-FILA

**Milestone:** PROTO-WORKFLOW-FILA — fila reativa + chat focado por item + auto-regulação básica + persistência de preferências
**Produto:** workflow
**Estágio:** Protótipo
**Branch:** `claude/execute-project-workflow-yoTQ7` (harness-assigned; equivalente a `milestone/proto-workflow-fila` no fluxo manual)
**Modo:** Autônomo
**Dispatch recebido em:** 2026-04-30

---

## Contexto do Milestone

**Objetivo:** plataforma ganha fila reativa de decisões + chat focado por item + auto-regulação básica. Sinais óbvios do repo (épico em 🔍 esperando dispatch, PR de milestone aberta, branch parada) viram itens de fila por regra determinística — sem agente proativo ainda. Operador atende na ordem que escolher; ordenação por recência da detecção. Fonte da verdade: markdown + estado git/GitHub. Sem persistência própria — fila é view derivada, reconstruída do zero a cada render.

**Épicos agrupados:** W-PROTO-FILA-1, W-PROTO-FILA-2, W-PROTO-FILA-3, W-PROTO-FILA-4 (ordem de execução interna conforme dependências declaradas).

**Dependências de core:** nenhuma. PLAT-1..4 e FAXINA já mergeados (PR #93/#117).

---

## Sizing (EM) — 2026-04-30 10:06

- Milestone: PROTO-WORKFLOW-FILA (Protótipo, workflow)
- Épicos avaliados: 4
- Funcionalidades: 10 (FILA-1: 3 + FILA-2: 2 + FILA-3: 2 + FILA-4: 3)
- Fator de risco médio: 1.0 (sem refator declarado, sem integração com sistema externo, sem dependência core não-✅; deps são internas do workflow_platform)
- Cálculo: 10 × 200 × 1.0 = **2000 LOC estimado**
- Decisão: **FIT** (≤ 3000)
- Linha persistida em `docs/process/sizing/history.jsonl` (`session_outcome=pending`)

---

## Ordem de execução interna

1. **W-PROTO-FILA-1** primeiro (modelos `queue/models.py` + detecção `queue/detect.py` + snapshot determinístico — funda a base que todos os outros consomem).
2. **W-PROTO-FILA-2** depois (view e prompts dependem dos modelos e detecção de FILA-1).
3. **W-PROTO-FILA-3** depois (badge e banner consomem `len(items)` da view de FILA-2).
4. **W-PROTO-FILA-4** por último (preferences toca `app.py`, `views/queue.py` e ajusta o threshold de stale_branch — consolida sidebar onde FILA-3.1 plotou badge).

---

## Épicos

Um bloco por épico, na ordem de execução. Cada épico fecha quando todas as suas funcionalidades têm Dev/QA/TL/PO ✅.

---

### Épico W-PROTO-FILA-1 — Detecção reativa de eventos e shape de item

**Status:** ✅ Implementado — em 2026-04-30
**Objetivo:** módulo de detecção lê estado-do-mundo (ROADMAPs parseados + branches do remote) e produz lista determinística de itens de fila por regra fixa. Sem persistência própria — fila é função pura do estado. Cobre 5 tipos no Protótipo: DISPATCH, REVIEW, REFINE, CLEANUP, STALE_BRANCH.
**Dependências:** W-PROTO-PLAT-1 (parser de ROADMAP + Epic/Milestone/ParsedRoadmap) — já mergeado.

#### Funcionalidades

##### 1.1 — Shape mínimo de item de fila

- **Domain:** backend, data
- **Estimativa:** ~150 linhas | risco: baixo
- **Arquivos esperados:**
  - criar: `tools/workflow_platform/queue/__init__.py`
  - criar: `tools/workflow_platform/queue/models.py`
  - criar: `tests/tools/workflow_platform/test_queue_models.py`
- **Padrão a seguir:** `tools/workflow_platform/models.py` (Epic, Milestone, ParsedRoadmap — dataclasses imutáveis)
- **Critérios de aceite cobertos:** [W-PROTO-FILA-1.1.1, 1.1.2, 1.1.3, 1.1.4, 1.1.5]
- **Validação:** `pytest tests/tools/workflow_platform/test_queue_models.py -v` passa.

##### 1.2 — Detecção dos 5 tipos a partir do estado-do-mundo

- **Domain:** backend
- **Estimativa:** ~300 linhas | risco: médio
- **Arquivos esperados:**
  - criar: `tools/workflow_platform/queue/detect.py`
  - criar: `tools/workflow_platform/queue/git_helper.py`
  - criar: `tests/tools/workflow_platform/test_queue_detect.py`
- **Padrão a seguir:** `tools/workflow_platform/prompts/dispatch.py` (helper puro: input dataclass → output tipado, sem side effect)
- **Critérios de aceite cobertos:** [W-PROTO-FILA-1.2.1..1.2.9]
- **Validação:** `pytest tests/tools/workflow_platform/test_queue_detect.py -v` passa.

##### 1.3 — Garantia de determinismo via fixture-snapshot

- **Domain:** tests
- **Estimativa:** ~150 linhas | risco: baixo
- **Arquivos esperados:**
  - criar: `tests/tools/workflow_platform/fixtures/__init__.py`
  - criar: `tests/tools/workflow_platform/fixtures/world_state.py`
  - criar: `tests/tools/workflow_platform/fixtures/expected_queue_snapshot.json`
  - criar: `tests/tools/workflow_platform/test_queue_determinism.py`
- **Padrão a seguir:** snapshot testing convencional via `json.dumps(..., sort_keys=True, indent=2)`
- **Critérios de aceite cobertos:** [W-PROTO-FILA-1.3.1, 1.3.2, 1.3.3, 1.3.4]
- **Validação:** `pytest tests/tools/workflow_platform/test_queue_determinism.py -v` passa.

#### Gates por funcionalidade — Épico W-PROTO-FILA-1

| Funcionalidade | Dev | QA | TL | PO |
|----------------|:---:|:--:|:--:|:--:|
| 1.1 Shape de QueueItem | ✅ | ✅ | ✅ | ✅ |
| 1.2 detect_all_items | ✅ | ✅ | ✅ | ✅ |
| 1.3 Snapshot determinístico | ✅ | ✅ | ✅ | ✅ |

---

### Épico W-PROTO-FILA-2 — Exibição da fila + prompt focado por item

**Status:** ✅ Implementado — em 2026-04-30
**Objetivo:** plataforma ganha tab "📋 Fila" (default) que renderiza os QueueItems detectados em FILA-1 como cards clicáveis. Clicar abre painel de detalhe com prompt clipboard-ready específico do tipo, reusando builders de PLAT-3.1 e PLAT-4.2 e adicionando builders novos para REVIEW, CLEANUP, STALE_BRANCH.
**Dependências:** FILA-1 (modelos+detecção); PLAT-2.1 (tabs/sidebar); PLAT-3.1 (`build_dispatch_prompt`).

#### Funcionalidades

##### 2.1 — View da fila como tab default

- **Domain:** frontend, backend
- **Estimativa:** ~250 linhas | risco: médio
- **Arquivos esperados:**
  - criar: `tools/workflow_platform/views/queue.py`
  - criar: `tests/tools/workflow_platform/test_queue_view.py`
  - modificar: `tools/workflow_platform/app.py` (substituir chamada direta de `render_kanban` por bloco de tabs; adicionar botão recarregar fila; gerenciar `st.session_state.queue_world_state`)
- **Padrão a seguir:** `tools/workflow_platform/views/kanban.py` (uso de st.session_state, padrão render_*)
- **Critérios de aceite cobertos:** [W-PROTO-FILA-2.1.1..2.1.6]
- **Validação:** `pytest tests/tools/workflow_platform/test_queue_view.py -v` passa.

##### 2.2 — Builders de prompt por tipo de item

- **Domain:** backend, frontend
- **Estimativa:** ~200 linhas | risco: baixo
- **Arquivos esperados:**
  - criar: `tools/workflow_platform/prompts/queue_item.py`
  - criar: `tests/tools/workflow_platform/test_queue_item_prompt.py`
  - modificar: `tools/workflow_platform/views/queue.py` (adicionar `render_queue_item_detail`)
- **Padrão a seguir:** `tools/workflow_platform/prompts/dispatch.py` (helper puro retornando string)
- **Critérios de aceite cobertos:** [W-PROTO-FILA-2.2.1..2.2.7]
- **Validação:** `pytest tests/tools/workflow_platform/test_queue_item_prompt.py -v` passa.

#### Gates por funcionalidade — Épico W-PROTO-FILA-2

| Funcionalidade | Dev | QA | TL | PO |
|----------------|:---:|:--:|:--:|:--:|
| 2.1 View tab default | ✅ | ✅ | ✅ | ✅ |
| 2.2 Builders de prompt | ✅ | ✅ | ✅ | ✅ |

---

### Épico W-PROTO-FILA-3 — Auto-regulação básica (alerta visual)

**Status:** ✅ Implementado — em 2026-04-30
**Objetivo:** badge na sidebar mostra `<contagem> / 20 itens` com cor por faixa. Banner adicional na tab da fila quando OVER_LIMIT explica o estado mas não bloqueia ação.
**Dependências:** FILA-2.1 (view e bloco da sidebar existem).

#### Funcionalidades

##### 3.1 — Badge de contagem na sidebar

- **Domain:** frontend, backend
- **Estimativa:** ~80 linhas | risco: baixo
- **Arquivos esperados:**
  - criar: `tools/workflow_platform/queue/load.py`
  - criar: `tests/tools/workflow_platform/test_queue_load.py`
  - modificar: `tools/workflow_platform/app.py` (adicionar render_queue_load_badge na sidebar)
- **Padrão a seguir:** `tools/workflow_platform/views/kanban.py::KANBAN_COLUMN_ORDER` (constantes nomeadas + função pura + dict de mapping)
- **Critérios de aceite cobertos:** [W-PROTO-FILA-3.1.1..3.1.5]
- **Validação:** `pytest tests/tools/workflow_platform/test_queue_load.py -v` passa.

##### 3.2 — Banner de alerta na tab da fila quando OVER_LIMIT

- **Domain:** frontend
- **Estimativa:** ~30 linhas | risco: baixo
- **Arquivos esperados:**
  - modificar: `tools/workflow_platform/views/queue.py` (adicionar `render_over_limit_banner`)
- **Padrão a seguir:** `st.warning(...)` Streamlit nativo
- **Critérios de aceite cobertos:** [W-PROTO-FILA-3.2.1..3.2.5]
- **Validação:** lógica condicional já testada via `compute_load_state` em 3.1; validação manual de fixture com 22 itens.

#### Gates por funcionalidade — Épico W-PROTO-FILA-3

| Funcionalidade | Dev | QA | TL | PO |
|----------------|:---:|:--:|:--:|:--:|
| 3.1 Badge sidebar | ✅ | ✅ | ✅ | ✅ |
| 3.2 Banner OVER_LIMIT | ✅ | ✅ | ✅ | ✅ |

---

### Épico W-PROTO-FILA-4 — Configuração persistente + sidebar como painel

**Status:** 🏗️ Em andamento — desde 2026-04-30
**Objetivo:** plataforma ganha base de preferências persistidas localmente (JSON git-ignored) e a sidebar deixa de ser leitura passiva — vira painel de filtros + status. Threshold de stale_branch passa a vir de `preferences.json`.
**Dependências:** PLAT-1 (PlatformConfig, parse_roadmap); FILA-1 (filtro entra como input do WorldState); FILA-2 (sidebar coordenada com badge/recarregar); FILA-3 (badge integrado).

#### Funcionalidades

##### 4.1 — Persistência de preferências (JSON local)

- **Domain:** backend, data
- **Estimativa:** ~200 linhas | risco: baixo
- **Arquivos esperados:**
  - criar: `tools/workflow_platform/preferences.py`
  - criar: `tests/tools/workflow_platform/test_preferences.py`
  - modificar: `.gitignore` (adicionar `tools/workflow_platform/.preferences.json`)
- **Padrão a seguir:** `tools/workflow_platform/config_loader.py` (dataclass imutável + helper puro com path resolvido)
- **Critérios de aceite cobertos:** [W-PROTO-FILA-4.1.1..4.1.6]
- **Validação:** `pytest tests/tools/workflow_platform/test_preferences.py -v` passa.

##### 4.2 — Filtro por ROADMAP no caller

- **Domain:** backend
- **Estimativa:** ~150 linhas | risco: médio
- **Arquivos esperados:**
  - criar: `tests/tools/workflow_platform/test_visibility_filter.py`
  - modificar: `tools/workflow_platform/preferences.py` (adicionar `apply_visibility_filter`)
  - modificar: `tools/workflow_platform/app.py` (carregar prefs + aplicar filtro)
  - modificar: `tools/workflow_platform/views/queue.py` (build_world_state recebe threshold_days)
- **Padrão a seguir:** `tools/workflow_platform/config_loader.py` (helper puro)
- **Critérios de aceite cobertos:** [W-PROTO-FILA-4.2.1..4.2.6]
- **Validação:** `pytest tests/tools/workflow_platform/test_visibility_filter.py -v` passa.

##### 4.3 — Sidebar como painel de filtros + status

- **Domain:** frontend, backend
- **Estimativa:** ~250 linhas | risco: médio
- **Arquivos esperados:**
  - criar: `tests/tools/workflow_platform/test_sidebar_label.py`
  - modificar: `tools/workflow_platform/app.py` (reescrever `_render_sidebar` + `_label_for_roadmap` + `_render_warnings_dialog`)
- **Padrão a seguir:** `tools/workflow_platform/views/card_detail.py` (st.session_state para painel inline)
- **Critérios de aceite cobertos:** [W-PROTO-FILA-4.3.1..4.3.7]
- **Validação:** `pytest tests/tools/workflow_platform/test_sidebar_label.py -v` passa.

#### Gates por funcionalidade — Épico W-PROTO-FILA-4

| Funcionalidade | Dev | QA | TL | PO |
|----------------|:---:|:--:|:--:|:--:|
| 4.1 preferences.py | ⏳ | ⏳ | ⏳ | ⏳ |
| 4.2 apply_visibility_filter | ⏳ | ⏳ | ⏳ | ⏳ |
| 4.3 Sidebar painel | ⏳ | ⏳ | ⏳ | ⏳ |

---

## Esclarecimentos (resolvidos por consulta)

- ✅ Branch harness-assigned é equivalente funcional a `milestone/proto-workflow-fila` — fonte: precedente do PR #117 (FAXINA usou `claude/proto-workflow-faxina-e4irl` declarado como equivalente).
- ✅ `EpicState` enum existe em `tools/workflow_platform/models.py`; `NEXT_STEP_MAP` existe em `tools/workflow_platform/prompts/refinement.py` — fonte: arquivos lidos antes do plano.
- ✅ `parse_roadmap` retorna `ParsedRoadmap` com `epics` (lista de `Epic`) e `milestones` (lista de `Milestone`) — fonte: `tools/workflow_platform/parser.py:203`.
- ✅ `build_dispatch_prompt(epic, all_epics_in_milestone) -> DispatchPromptResult` (não retorna string direto) — fonte: `tools/workflow_platform/prompts/dispatch.py:36`. FILA-2.2 precisa adaptar shape ao chamar via `build_prompt_for_item`.
- ✅ `build_refinement_prompt(epic) -> str | None` — fonte: `tools/workflow_platform/prompts/refinement.py:79`.
- ✅ Layout de testes: `tests/tools/workflow_platform/test_*.py` — fonte: árvore de `tests/`.

---

## Extração pendente

> Itens identificados pelo TL durante os gates como conhecimento permanente a gravar em docs estruturais.

### Épico W-PROTO-FILA-1
- (vazio — TL não identificou conhecimento permanente neste épico)

### Épico W-PROTO-FILA-2
- [x] `tools/workflow_platform/views/queue.py`: tabs Streamlit usam padrão st.tabs com fila default e estado em st.session_state.queue_world_state. Documentado inline na docstring do módulo. (TL identificou; Dev marcou ao escrever.)

### Épico W-PROTO-FILA-3
- (vazio — TL não identificou conhecimento permanente neste épico)

### Épico W-PROTO-FILA-4
(em aberto — TL preenche durante os gates)

---

## Status dos Gates (nível milestone)

- [x] PM ➖ pulado: todos os épicos em 🔍 no dispatch
- [x] EM (veredicto: FIT)
- [x] Scrum Master (plano para todos os 4 épicos escrito)
- [ ] Loop por épico concluído (todas as tabelas acima com Dev/QA/TL/PO ✅)
- [ ] RTE (no fim do milestone, após o último épico fechar)

### Evidências de carregamento de skill

**Únicas por milestone:**

- [PM] skill pulada: todos os épicos já em 🔍 ➖ 2026-04-30 10:06
- [EM] skill carregada: skills/em/skill.md ✅ 2026-04-30 10:06
- [SCRUM-MASTER] skill carregada: skills/scrum-master/skill.md ✅ 2026-04-30 10:06

**Repetidas por funcionalidade:**

- [QA] skills/qa/skill.md ✅ 2026-04-30 10:10 | épico W-PROTO-FILA-1 | funcionalidade 1.1
- [TL] skills/tl/skill.md ✅ 2026-04-30 10:10 | épico W-PROTO-FILA-1 | funcionalidade 1.1
- [PO] skills/po/skill.md ✅ 2026-04-30 10:10 | épico W-PROTO-FILA-1 | funcionalidade 1.1
- [QA] skills/qa/skill.md ✅ 2026-04-30 10:15 | épico W-PROTO-FILA-1 | funcionalidade 1.2
- [TL] skills/tl/skill.md ✅ 2026-04-30 10:15 | épico W-PROTO-FILA-1 | funcionalidade 1.2
- [PO] skills/po/skill.md ✅ 2026-04-30 10:15 | épico W-PROTO-FILA-1 | funcionalidade 1.2
- [QA] skills/qa/skill.md ✅ 2026-04-30 10:20 | épico W-PROTO-FILA-1 | funcionalidade 1.3
- [TL] skills/tl/skill.md ✅ 2026-04-30 10:20 | épico W-PROTO-FILA-1 | funcionalidade 1.3
- [PO] skills/po/skill.md ✅ 2026-04-30 10:20 | épico W-PROTO-FILA-1 | funcionalidade 1.3
- [QA] skills/qa/skill.md ✅ 2026-04-30 11:05 | épico W-PROTO-FILA-2 | funcionalidade 2.1
- [TL] skills/tl/skill.md ✅ 2026-04-30 11:05 | épico W-PROTO-FILA-2 | funcionalidade 2.1
- [PO] skills/po/skill.md ✅ 2026-04-30 11:05 | épico W-PROTO-FILA-2 | funcionalidade 2.1
- [QA] skills/qa/skill.md ✅ 2026-04-30 11:05 | épico W-PROTO-FILA-2 | funcionalidade 2.2
- [TL] skills/tl/skill.md ✅ 2026-04-30 11:05 | épico W-PROTO-FILA-2 | funcionalidade 2.2
- [PO] skills/po/skill.md ✅ 2026-04-30 11:05 | épico W-PROTO-FILA-2 | funcionalidade 2.2
- [QA] skills/qa/skill.md ✅ 2026-04-30 11:10 | épico W-PROTO-FILA-3 | funcionalidade 3.1
- [TL] skills/tl/skill.md ✅ 2026-04-30 11:10 | épico W-PROTO-FILA-3 | funcionalidade 3.1
- [PO] skills/po/skill.md ✅ 2026-04-30 11:10 | épico W-PROTO-FILA-3 | funcionalidade 3.1
- [QA] skills/qa/skill.md ✅ 2026-04-30 11:10 | épico W-PROTO-FILA-3 | funcionalidade 3.2
- [TL] skills/tl/skill.md ✅ 2026-04-30 11:10 | épico W-PROTO-FILA-3 | funcionalidade 3.2
- [PO] skills/po/skill.md ✅ 2026-04-30 11:10 | épico W-PROTO-FILA-3 | funcionalidade 3.2

---

## Histórico de Reprovações

(vazio até o momento)
