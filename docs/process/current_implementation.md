# Implementação Atual: Milestone PILOTO-WORKFLOW-UX (fatia W-PILOTO-UX-1)

**Milestone:** PILOTO-WORKFLOW-UX — reconstruir o cockpit em Reflex com o polimento embutido
**Produto:** workflow
**Estágio:** Piloto
**Branch:** `claude/docs-process-workflow-gk9hac` (harness-assigned; equivalente a `milestone/piloto-workflow-ux` no fluxo manual)
**Modo:** Autônomo
**Dispatch recebido em:** 2026-07-04

> **Escopo desta PR:** apenas **W-PILOTO-UX-1** (migração Reflex — fundação).
> Os 4 épicos do milestone estão em `🔍`, mas o ROADMAP declara que **UX-2/3/4
> dependem de UX-1 mergear** (fundação Reflex) antes de implementar. Logo, o
> único pronto para implementar agora é UX-1, entregue aqui como PR própria.
> UX-2/3/4 seguem para um dispatch posterior sobre a fundação já mergeada.

---

## Contexto do Milestone

**Objetivo:** trocar a camada de apresentação da plataforma de Streamlit para
Reflex ([ADR 001](workflow/adr/001-stack-da-plataforma.md)), preservando todo o
miolo stack-independente (`parser`, `models`, `config_loader`, `preferences`,
`queue/*`, `prompts/*`). A primeira fatia entrega esqueleto Reflex + abas
Fila/Kanban funcionais, validando a decisão de stack no uso real; é fundação de
todo o resto do milestone e pré-requisito do `PILOTO-WORKFLOW-CANAL-UNICO`.

**Decisão de stack:** [ADR 001 do workflow](workflow/adr/001-stack-da-plataforma.md)
(Streamlit → Reflex). Spike de viabilidade executado e aprovado no refinamento
a `🔍` (2026-07-04).

---

## Épicos

### Épico W-PILOTO-UX-1 — Migração da plataforma para Reflex (fundação + fatia fina)

**Status:** ✅ Implementado (código pronto, sob revisão humana na PR)

**Objetivo:** substituir o entrypoint Streamlit (`app.py` + `views/*`) por uma
app Reflex (`rxconfig.py` + `web/`) com estado no backend (`rx.State`),
preservando o miolo intocado.

#### Gates por funcionalidade

| Funcionalidade | Dev | QA | TL | PO |
|---|---|---|---|---|
| 1.1 Esqueleto Reflex + estado no backend | ✅ | ✅ | ✅ | ✅ |
| 1.2 Porte da aba Fila | ✅ | ✅ | ✅ | ✅ |
| 1.3 Porte da aba Kanban | ✅ | ✅ | ✅ | ✅ |
| 1.4 Paridade funcional + retirada do Streamlit | ✅ | ✅ | ✅ | ✅ |

#### Evidências de carregamento (por milestone)

| Skill | Evidência |
|---|---|
| EM (sizing) | FIT — migração view-only, miolo intocado; 4 funcionalidades coesas na mesma camada. Sem OVERFLOW. |
| Scrum Master | Plano = este arquivo; tarefas por funcionalidade na ordem 1.1→1.4 declarada no épico. |
| RTE | Push único da branch + PR aberta com Seção 🎯; `current_validation.md` gerado; UX-1 → `🔀` no ROADMAP. |

#### Evidências por gate (por funcionalidade)

| Gate | Contexto | Evidência |
|---|---|---|
| Dev | épico W-PILOTO-UX-1 \| func. 1.1 | `rxconfig.py`, `web/web.py`, `web/state.py`, `presenters.py`, `world_state.py`. Miolo intocado. |
| QA | épico W-PILOTO-UX-1 \| func. 1.1 | `test_platform_state.py` (6 testes: on_load/select/toggle). Import da `PlatformState` e build de `index()` OK. |
| TL | épico W-PILOTO-UX-1 \| func. 1.1 | Padrão Reflex espelha `products/ensaio/app/`; view models tipados (`web/view_models.py`); `queue/*`, `parser`, `prompts/*` não tocados. |
| PO | épico W-PILOTO-UX-1 \| func. 1.1 | `reflex run` sobe carregando config/ROADMAPs/prefs; estado da UI (aba/seleção/filtros) vive em `rx.State`. Verificado por screenshot. |
| Dev | épico W-PILOTO-UX-1 \| func. 1.2 | `web/components/queue.py` + `web/components/detail.py`; detecção/prompts reusados intactos. |
| QA | épico W-PILOTO-UX-1 \| func. 1.2 | Paridade de `detect_all` por construção (mesma função); `test_queue_view.py`/`test_queue_determinism.py` verdes. |
| TL | épico W-PILOTO-UX-1 \| func. 1.2 | Painel de detalhe portado com paridade de posição (rodapé); reposicionamento fica para UX-2. |
| PO | épico W-PILOTO-UX-1 \| func. 1.2 | Screenshot: 45 itens reais (5 tipos), clique → detalhe + prompt clipboard-ready ("implementa o PILOTO-WORKFLOW-UX"). Aba default = Fila. |
| Dev | épico W-PILOTO-UX-1 \| func. 1.3 | `web/components/kanban.py`; agrupamento reusa `presenters.group_by_milestone`. |
| QA | épico W-PILOTO-UX-1 \| func. 1.3 | `test_kanban.py` verde (import migrado para `presenters`). |
| TL | épico W-PILOTO-UX-1 \| func. 1.3 | Roteamento por estado reusa `build_dispatch_prompt`/`build_refinement_prompt`; sem lógica nova. |
| PO | épico W-PILOTO-UX-1 \| func. 1.3 | Screenshot: 8 colunas 🌱→✅, cards por milestone; coluna 🔍 mostra PILOTO-WORKFLOW-UX. |
| Dev | épico W-PILOTO-UX-1 \| func. 1.4 | `web/components/sidebar.py`; remoção de `app.py` + `views/*`; `.gitignore` + `.web/`. |
| QA | épico W-PILOTO-UX-1 \| func. 1.4 | `grep -rl streamlit tools/workflow_platform/` → vazio; suíte 135 testes verde. |
| TL | épico W-PILOTO-UX-1 \| func. 1.4 | Linha `streamlit>=1.30.0` do `requirements.txt` **mantida** (é do Revelar) — correção do critério 1.4 original registrada no ROADMAP. |
| PO | épico W-PILOTO-UX-1 \| func. 1.4 | Screenshot: sidebar com 6 checkboxes + contagens, badge `45/20` (OVER_LIMIT) + banner, avisos (0). Prefs persistem em `.preferences.json`. |

#### Extração pendente

- [x] Descobertas de Reflex (dataclasses tipados vs `rx.Base` ausente, colisão de
  nome de campo com métodos de `ObjectVar`, `foreach` aninhado exige tipo concreto,
  não concatenar dict-item com `str`, `reflex init` mexe no diretório) registradas
  em [`.claudecode.md`](../../.claudecode.md) §2.6 — conhecimento reusável pelos
  épicos irmãos UX-2/3/4.

(TL: fora isso, nenhum padrão arquitetural novo permanente — a migração espelha o
padrão Reflex já estabelecido pelo Ensaio; nada a promover a `ARCHITECTURE.md`.)

---

## Faxina pendente (fold-in do dispatch — §4.5)

- **PROTO-WORKFLOW-CLEANUP-TRIGGER (PR #123):** faxina **pulada com nota**. O
  `cleanup_trigger --list` detecta W-PROTO-17 em `🔀` na main, mas o
  `current_implementation.md` mergeado documenta **PROTO-WORKFLOW-FILA**, não
  CLEANUP-TRIGGER — o gate-check do Passo 1 da Cleanup skill (cabeçalho declara
  `Milestone: <MILESTONE_ID>`) não passa. Caso previsto no `dispatch.md` §4.5.5:
  registra-se a nota e segue-se. Fechamento manual de W-PROTO-17 fica para o dev
  (a própria PR #123 já anotou essa limitação — sessão manual não gerou
  `current_implementation.md`).

---

## Resumo Final do Milestone (fatia UX-1)

Migração Streamlit → Reflex da plataforma de workflow entregue como fundação do
Piloto. A camada de view foi reescrita em Reflex (`rxconfig.py`, `web/web.py`,
`web/state.py`, `web/view_models.py`, `web/components/*`), com o estado da UI num
único `rx.State` (`PlatformState`). A lógica pura de apresentação e a construção
do WorldState saíram dos módulos Streamlit para `presenters.py` e `world_state.py`
(stack-independent). O miolo (`parser`, `models`, `config_loader`, `preferences`,
`queue/*`, `prompts/*`, `cleanup_trigger`) ficou **intocado**; a paridade de
`detect_all` é garantida por construção. A camada Streamlit (`app.py` + `views/*`)
foi removida; `grep -rl streamlit tools/workflow_platform/` volta vazio.

**Validação:** 135 testes de `tests/tools/workflow_platform/` passam (6 novos em
`test_platform_state.py`; 3 arquivos com imports realocados para `presenters`; 1
teste de integração Streamlit removido). `reflex run` compila (21/21) e sobe;
verificação visual por screenshot confirmou as 3 superfícies (Fila com itens
reais, clique → detalhe com prompt clipboard-ready, Kanban de 8 colunas) e a
sidebar (filtros, badge de carga, avisos).

**Fora do escopo (próximo dispatch, sobre a fundação mergeada):** W-PILOTO-UX-2
(co-visibilidade lista↔detalhe), W-PILOTO-UX-3 (densidade da fila), W-PILOTO-UX-4
(informação por tipo no painel).
