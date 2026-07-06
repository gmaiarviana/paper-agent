# Implementação Atual: Milestone PILOTO-WORKFLOW-DISPATCH-EPICO

**Milestone:** PILOTO-WORKFLOW-DISPATCH-EPICO — dispatch e refino por épico, com predecessor bloqueante
**Produto:** workflow
**Estágio:** Piloto
**Branch:** `claude/admiring-ramanujan-2s5tiq` (harness-assigned; equivalente a `milestone/piloto-workflow-dispatch-epico` no fluxo manual)
**Modo:** Autônomo
**Dispatch recebido em:** 2026-07-06

> **Escopo desta PR:** o milestone tem **um único épico** — **W-PILOTO-DISP-1**
> (dispatch/refino por épico + predecessor bloqueante), em `🔍`. Dependências
> declaradas (W-PILOTO-UX-1 `✅` mergeada; PROTO-WORKFLOW-FILA) satisfeitas.

---

## Contexto do Milestone

**Objetivo:** tornar dispatch e refino ações **por épico** (não só por milestone) e
introduzir o **predecessor bloqueante** como gate de acionabilidade. Hoje
`detect_dispatch` é atômico por milestone (exige todos os épicos em 🔍) e
`build_dispatch_prompt` bloqueia se qualquer irmão está em 🏗️/🔀/✅ — o que torna
um milestone parcialmente entregue invisível/impossível de continuar pela
plataforma. Depois deste épico, cada épico 🔍 (dispatch) ou pré-🔍 (refino) é ação
própria, e a única coisa que a suprime é um predecessor declarado ainda não `✅`.

**Conceito — predecessor bloqueante:** campo novo opcional no bloco do épico
(`**Predecessor bloqueante:** <IDs>`). Aceita 1+ IDs (épico ou milestone),
separados por vírgula. Satisfeito quando o predecessor está em `✅`; em qualquer
outro estado, o dependente está **bloqueado**. Uma regra compartilhada
(`is_blocked_by_predecessor`) serve dispatch **e** refino.

---

## Épicos

### Épico W-PILOTO-DISP-1 — Dispatch e refino por épico, com predecessor bloqueante

**Status:** ✅ Implementado (código pronto, sob revisão humana na PR)

**Objetivo:** ver contexto acima.

#### Gates por funcionalidade

| Funcionalidade | Dev | QA | TL | PO |
|---|---|---|---|---|
| 1.1 Dado — campo `**Predecessor bloqueante:**` (parser + modelo) | ✅ | ✅ | ✅ | ✅ |
| 1.2 Detecção por épico + gate de predecessor | ✅ | ✅ | ✅ | ✅ |
| 1.3 Prompts por épico | ✅ | ✅ | ✅ | ✅ |
| 1.4 Plataforma — Fila oculta, Kanban comunica | ✅ | ✅ | ✅ | ✅ |

#### Evidências de carregamento (por milestone)

| Skill | Evidência |
|---|---|
| EM (sizing) | FIT — épico único, 4 funcionalidades coesas na mecânica de detecção/dispatch; predecessor é campo + função pura, sem decisão arquitetural nova. Sem OVERFLOW. |
| Scrum Master | Plano = este arquivo; tarefas por funcionalidade na ordem 1.1→1.4 declarada no épico. |
| RTE | Push único da branch + PR aberta com Seção 🎯; `current_validation.md` gerado; DISP-1 → `🔀` no ROADMAP. |

#### Evidências por gate (por funcionalidade)

| Gate | Contexto | Evidência |
|---|---|---|
| Dev | DISP-1 \| func. 1.1 | `models.py` (`Epic.blocking_predecessors` + `is_blocked_by_predecessor`/`blocking_predecessors_of`); `parser.py` (`_PREDECESSOR_FIELD_RE`); `presenters.py` (serialização); ROADMAP UX-2/3/4 → `W-PILOTO-UX-1`. |
| QA | DISP-1 \| func. 1.1 | `test_parser.py` (campo presente/ausente/split por vírgula, sem warning espúrio); suíte verde. |
| TL | DISP-1 \| func. 1.1 | Regra compartilhada em `models.py` (camada base, sem deps de UI); paridade com os campos atuais do épico (unknown → ignorado). |
| PO | DISP-1 \| func. 1.1 | Campo ausente → lista vazia; presente → IDs parseados; UX-2/3/4 registram `W-PILOTO-UX-1`. |
| Dev | DISP-1 \| func. 1.2 | `job_queue/detect.py` — `detect_dispatch_items`/`detect_refine_items` por épico com gate de predecessor. |
| QA | DISP-1 \| func. 1.2 | `test_queue_detect.py` (per-épico, gate de predecessor, milestone parcial surfaça fatias 🔍); snapshot regenerado. |
| TL | DISP-1 \| func. 1.2 | REVIEW/CLEANUP/STALE_BRANCH intocados; ordenação e determinismo preservados. |
| PO | DISP-1 \| func. 1.2 | 1 item por épico 🔍 com predecessores ✅; épico 🔍 com predecessor não-✅ não gera item; refine idem. |
| Dev | DISP-1 \| func. 1.3 | `prompts/dispatch.py` (`build_dispatch_prompt` por épico, motivo de bloqueio); `prompts/queue_item.py`. |
| QA | DISP-1 \| func. 1.3 | `test_dispatch_prompt.py`/`test_queue_item_prompt.py` reescritos para semântica por épico; verde. |
| TL | DISP-1 \| func. 1.3 | Prompt `"implementa o épico <ID>"`; não bloqueia mais por irmão em 🏗️/🔀/✅; refino idem. |
| PO | DISP-1 \| func. 1.3 | Predecessor não-✅ → `blocked=True`, sem prompt, com motivo ("bloqueado por <ID> — precisa estar ✅"). |
| Dev | DISP-1 \| func. 1.4 | `web/state.py` (kind `blocked` + badge), `web/view_models.py`, `web/components/detail.py`, `web/components/kanban.py`. |
| QA | DISP-1 \| func. 1.4 | `test_platform_state.py` (blocked suprime da fila, kanban card badge, painel sem ação); `reflex run` compila. |
| TL | DISP-1 \| func. 1.4 | View-only sobre a regra compartilhada; sem lógica de detecção nova na camada Reflex. |
| PO | DISP-1 \| func. 1.4 | Fila não lista bloqueado; card no Kanban com selo 🔒 + "aguardando <ID>", clicável; painel mostra bloqueio, sem ação. |

#### Extração pendente

(vazio — TL não identificou conhecimento permanente novo a promover a
`ARCHITECTURE.md`/`.claudecode.md`. A regra do predecessor bloqueante vive como
função pura em `models.py` com rationale nos docstrings; o conceito e o shape do
campo estão documentados no próprio bloco do épico no ROADMAP; a gotcha de
"parser ignora fences ``` ao casar campos de épico" está comentada em
`parser.py`. Nada duplicável fora disso — anti-redundância, CONSTITUTION §6.)

---

## Faxina pendente (fold-in do dispatch — §4.5)

- `python -m tools.workflow_platform.cleanup_trigger --list` → **vazio**. Nenhuma
  faxina pendente (o milestone PILOTO-WORKFLOW-UX segue aberto — UX-1 `✅` é janela
  intra-milestone, não gera CLEANUP; UX-2/3/4 em 🔍). Fold-in é no-op.

---

## Resumo Final do Milestone

(a preencher pela RTE)
