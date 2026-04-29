# Implementação Atual: Milestone PROTO-WORKFLOW-FAXINA

**Milestone:** PROTO-WORKFLOW-FAXINA — faxina documental do `docs/process/`
**Produto:** workflow
**Estágio:** Protótipo
**Branch:** `claude/proto-workflow-faxina-e4irl` (harness-assigned; equivalente a `milestone/proto-workflow-faxina` no fluxo manual)
**Modo:** Autônomo
**Dispatch recebido em:** 2026-04-29

---

## Contexto do Milestone

**Objetivo:** faxina documental do `docs/process/` — eliminar drift entre cópias da lista de estados de épico, retirar de `quality_rules.md` o que não é regra do fluxo, enxugar `copilot-instructions.md`, descontinuar a dicotomia "fluxo manual (Cursor) vs autônomo" que não reflete o uso real (operador roda 100% via Claude Code Web), e consolidar o template de "comandos de validação local" duplicado em 3 docs. Faz a casa antes de avançar para a fila reativa.

**Épicos agrupados:** W-PROTO-15, W-PROTO-16, W-PROTO-13, W-PROTO-10, W-PROTO-11 (ordem de execução interna).

**Dependências de core:** nenhuma.

---

## Sizing (EM) — 2026-04-29 16:19

- Milestone: PROTO-WORKFLOW-FAXINA (Protótipo, workflow)
- Épicos avaliados: 5
- Funcionalidades: 18 (W-PROTO-15: 8 + W-PROTO-16: 2 + W-PROTO-13: 3 + W-PROTO-10: 2 + W-PROTO-11: 3)
- Fator de risco médio: 1.0 (sem refator declarado, sem integração com sistema existente, sem dependência core não-✅; todas as edições são documentais com conteúdo declarado verbatim no ROADMAP)
- Cálculo: 18 × 200 × 1.0 = **3600 LOC estimado**
- Decisão: **TIGHT** (3000 < 3600 ≤ 6000)
- Alerta registrado: milestone aperta o orçamento por volume (18 funcionalidades), mas escopo cirúrgico por funcionalidade reduz risco real — a maioria são deleções ou substituições com texto verbatim já declarado no ROADMAP. Bootstrap defaults (sem histórico FIT-completed na `history.jsonl`).
- Linha persistida em `docs/process/sizing/history.jsonl`

---

## Ordem de execução interna

1. **W-PROTO-15** primeiro (varre fluxo manual / Cursor / Claude Web do desenho — afeta arquivos que outros tocam).
2. **W-PROTO-16** depois (congela template canônico de validação antes da reorganização do `quality_rules.md`).
3. **W-PROTO-13** independente (toca apenas `.github/copilot-instructions.md`).
4. **W-PROTO-10** depois de 15.1/15.2 (rótulo de `📋` reescrito antes da centralização).
5. **W-PROTO-11** por último (depende de 15.4 + 16 estarem fechados).

---

## Épicos

Um bloco por épico, na ordem de execução.

---

### Épico W-PROTO-15 — Descontinuar fluxo manual / Cursor / Claude Web do desenho

**Status:** ✅ Implementado
**Objetivo:** o desenho atual carrega dicotomia "fluxo manual (Cursor) vs fluxo autônomo (Claude Code Web)" em ~140 menções espalhadas em 16 arquivos. Operador opera 100% via Claude Code Web; Cursor não está instalado; Claude Web persiste como ferramenta secundária de refinamento estratégico. Absorve W-PROTO-12.

#### Funcionalidades

##### 15.1 — Reescrever `autonomous/overview.md` para fluxo único
- **Domain:** docs
- **Arquivos esperados:** modificar `docs/process/autonomous/overview.md`
- **Critério de aceite cobertos:** [W-PROTO-15.1]
- **Validação:** `grep -ni "fluxo manual\|cursor" docs/process/autonomous/overview.md` retorna 0.

##### 15.2 — Reescrever §"Otimização do Workflow" em `planning_guidelines.md`
- **Domain:** docs
- **Arquivos esperados:** modificar `docs/process/refinement/planning_guidelines.md`
- **Critério de aceite cobertos:** [W-PROTO-15.2]
- **Validação:** `grep -ni "Otimização do Workflow.*Cursor\|prompts separados para Cursor\|apto ao fluxo manual" docs/process/refinement/planning_guidelines.md` retorna 0.

##### 15.3 — Limpar `CONSTITUTION.md`
- **Domain:** docs
- **Arquivos esperados:** modificar `docs/CONSTITUTION.md`
- **Critério de aceite cobertos:** [W-PROTO-15.3]
- **Validação:** `grep -ni "cursor\|fluxo manual" docs/CONSTITUTION.md` retorna 0.

##### 15.4 — Limpar `implementation/overview.md` e `quality_rules.md` (absorve W-PROTO-12)
- **Domain:** docs
- **Arquivos esperados:** modificar `docs/process/implementation/overview.md`, `docs/process/implementation/quality_rules.md`
- **Critério de aceite cobertos:** [W-PROTO-15.4]
- **Validação:** `grep -ni "Cursor Background\|fluxo manual" docs/process/implementation/overview.md docs/process/implementation/quality_rules.md` retorna 0.

##### 15.5 — Limpar arquivos periféricos
- **Domain:** docs
- **Arquivos esperados:** modificar `docs/process/refinement/starter.md`, `docs/process/refinement/overview.md`, `docs/process/autonomous/delivery.md`, `skills/rte/skill.md`, `skills/rte/templates/delivery-report.md`
- **Critério de aceite cobertos:** [W-PROTO-15.5]
- **Validação:** `grep -ni "fluxo manual\|via Cursor"` nos 5 arquivos retorna 0.

##### 15.6 — Deletar `.cursorrules`
- **Domain:** docs
- **Arquivos esperados:** apagar `.cursorrules`
- **Critério de aceite cobertos:** [W-PROTO-15.6]
- **Validação:** `ls .cursorrules` retorna vazio.

##### 15.7 — Atualizar `CLAUDE.md`, `docs/CONTEXT_INDEX.md`, `README.md`
- **Domain:** docs
- **Arquivos esperados:** modificar `CLAUDE.md`, `docs/CONTEXT_INDEX.md`, `README.md`
- **Critério de aceite cobertos:** [W-PROTO-15.7]
- **Validação:** `grep -ni "cursor" CLAUDE.md docs/CONTEXT_INDEX.md README.md` retorna 0.

##### 15.8 — Varredura final
- **Domain:** docs
- **Arquivos esperados:** nenhum (validação de varredura)
- **Critério de aceite cobertos:** [W-PROTO-15.8]
- **Validação:** `grep -rni "cursor\|fluxo manual"` no escopo declarado retorna 0 menções (com exceções declaradas).

#### Gates por funcionalidade — Épico W-PROTO-15

| Funcionalidade                                                | Dev | QA | TL | PO |
|---------------------------------------------------------------|:---:|:--:|:--:|:--:|
| 15.1 Reescrever `autonomous/overview.md`                      | ✅  | ✅ | ✅ | ✅ |
| 15.2 Reescrever §"Otimização do Workflow"                     | ✅  | ✅ | ✅ | ✅ |
| 15.3 Limpar `CONSTITUTION.md`                                 | ✅  | ✅ | ✅ | ✅ |
| 15.4 Limpar `implementation/overview.md` + `quality_rules.md` | ✅  | ✅ | ✅ | ✅ |
| 15.5 Limpar arquivos periféricos                              | ✅  | ✅ | ✅ | ✅ |
| 15.6 Deletar `.cursorrules`                                   | ✅  | ✅ | ✅ | ✅ |
| 15.7 Atualizar `CLAUDE.md`/CONTEXT_INDEX/README               | ✅  | ✅ | ✅ | ✅ |
| 15.8 Varredura final                                          | ✅  | ✅ | ✅ | ✅ |

---

### Épico W-PROTO-16 — Consolidar template de "comandos de validação local"

**Status:** ✅ Implementado
**Objetivo:** template "git fetch / checkout / venv / pytest / [run app]" aparece em 4 arquivos com formatos divergentes. Consolida em fonte única (`quality_rules.md`) e substitui as cópias por referência.

#### Funcionalidades

##### 16.1 — Eleger fonte canônica em `quality_rules.md`
- **Domain:** docs
- **Arquivos esperados:** modificar `docs/process/implementation/quality_rules.md`
- **Critério de aceite cobertos:** [W-PROTO-16.1]
- **Validação:** §"Template de validação local" presente como cabeçalho navegável; bloco usa `.venv/`; passo 5 referencia W-PROTO-14.

##### 16.2 — Substituir cópias por referência
- **Domain:** docs
- **Arquivos esperados:** modificar `docs/process/implementation/delivery.md`, `docs/process/autonomous/delivery.md`, `docs/process/implementation/overview.md`
- **Critério de aceite cobertos:** [W-PROTO-16.2]
- **Validação:** os 3 docs apontam para `quality_rules.md#template-de-validação-local`; `git fetch origin` deixa de aparecer em blocos de código nos 3 arquivos (apenas em texto referencial).

#### Gates por funcionalidade — Épico W-PROTO-16

| Funcionalidade                                | Dev | QA | TL | PO |
|-----------------------------------------------|:---:|:--:|:--:|:--:|
| 16.1 Eleger fonte canônica                    | ✅  | ✅ | ✅ | ✅ |
| 16.2 Substituir cópias por referência         | ✅  | ✅ | ✅ | ✅ |

---

### Épico W-PROTO-13 — Faxina do `copilot-instructions.md` (concisão pra agente)

**Status:** ✅ Implementado
**Objetivo:** aplicar princípio "documentação para agente é concisa, não defensiva". Agente trabalha do traceback, não consulta catálogo de erros típicos. 13.1 e 13.2 são **no-ops verificados**; escopo real é 13.3.

#### Funcionalidades

##### 13.1 — §"Erros típicos e orientação" (no-op verificado)
- **Domain:** docs
- **Arquivos esperados:** nenhum (já apagada em refinamento anterior)
- **Critério de aceite cobertos:** [W-PROTO-13.1]
- **Validação:** `grep -c "Erros típicos\|orientação" .github/copilot-instructions.md` retorna 0.

##### 13.2 — §"Checklist mínimo de POC do Ensaio" (no-op verificado)
- **Domain:** docs
- **Arquivos esperados:** nenhum (já apagada em refinamento anterior)
- **Critério de aceite cobertos:** [W-PROTO-13.2]
- **Validação:** `grep -c "Checklist mínimo.*POC\|POC do Ensaio" .github/copilot-instructions.md` retorna 0.

##### 13.3 — Apagar §"Operação Windows / macOS / Linux"
- **Domain:** docs
- **Arquivos esperados:** modificar `.github/copilot-instructions.md`
- **Critério de aceite cobertos:** [W-PROTO-13.3]
- **Validação:** `grep -n "Operação Windows" .github/copilot-instructions.md` retorna 0; §"Quando o dev disser 'deu erro'" intacta.

#### Gates por funcionalidade — Épico W-PROTO-13

| Funcionalidade                                                | Dev | QA | TL | PO |
|---------------------------------------------------------------|:---:|:--:|:--:|:--:|
| 13.1 §"Erros típicos" (no-op)                                 | ➖  | ➖ | ➖ | ➖ |
| 13.2 §"Checklist POC" (no-op)                                 | ➖  | ➖ | ➖ | ➖ |
| 13.3 Apagar §"Operação Windows / macOS / Linux"               | ✅  | ✅ | ✅ | ✅ |

---

### Épico W-PROTO-10 — Centralizar definição dos estados de épico

**Status:** ⏳ Em andamento
**Objetivo:** eliminar drift entre as três cópias da lista canônica dos 8 estados de épico em `planning_guidelines.md`. Drift entre cópias gerou as 3 contradições corrigidas em 2026-04-28.

#### Funcionalidades

##### 10.1 — Bloco canônico único em `planning_guidelines.md`
- **Domain:** docs
- **Arquivos esperados:** modificar `docs/process/refinement/planning_guidelines.md`
- **Critério de aceite cobertos:** [W-PROTO-10.1]
- **Validação:** uma única seção define os 8 estados; `grep -n "🌱 Visão$" docs/process/refinement/planning_guidelines.md` retorna no máximo 1 bloco.

##### 10.2 — Limpeza de drift cross-doc
- **Domain:** docs
- **Arquivos esperados:** modificar `docs/process/refinement/starter.md`, `docs/CONSTITUTION.md`, `docs/process/autonomous/workflow.md`, `docs/process/workflow/vision.md`, `skills/pm/README.md`
- **Critério de aceite cobertos:** [W-PROTO-10.2]
- **Validação:** os arquivos abrem com link pra fonte canônica antes de qualquer menção a estado.

#### Gates por funcionalidade — Épico W-PROTO-10

| Funcionalidade                                | Dev | QA | TL | PO |
|-----------------------------------------------|:---:|:--:|:--:|:--:|
| 10.1 Bloco canônico único                     | ⏳  | ⏳ | ⏳ | ⏳ |
| 10.2 Limpeza de drift cross-doc               | ⏳  | ⏳ | ⏳ | ⏳ |

---

### Épico W-PROTO-11 — Faxina de `quality_rules.md`

**Status:** ⏳ Em andamento
**Objetivo:** tirar de `quality_rules.md` (397 linhas) o que não é regra de processo. Mistura princípios + lessons learned do produto Revelar + tutorial defensivo de git pra Windows. Saída: doc com ~185 linhas focado em princípios + anti-redundância + comandos.

#### Funcionalidades

##### 11.1 — Apagar §"Verificação de Conflitos e Prevenção de Perda de Trabalho"
- **Domain:** docs
- **Arquivos esperados:** modificar `docs/process/implementation/quality_rules.md`
- **Critério de aceite cobertos:** [W-PROTO-11.1]
- **Validação:** `grep -n "Verificação de Conflitos\|Prevenção de Perda" docs/process/implementation/quality_rules.md` retorna 0.

##### 11.2 — Mover §"Diretrizes Aprendidas em Produção" para `products/revelar/docs/`
- **Domain:** docs
- **Arquivos esperados:** modificar `docs/process/implementation/quality_rules.md`; criar `products/revelar/docs/llm_implementation_lessons.md`
- **Critério de aceite cobertos:** [W-PROTO-11.2]
- **Validação:** `grep -n "Diretrizes Aprendidas em Produção\|Sistemas Conversacionais com LLMs" docs/process/implementation/quality_rules.md` retorna 0; `ls products/revelar/docs/llm_implementation_lessons.md` existe com >40 linhas.

##### 11.3 — Reorganizar o que sobra em ordem coerente
- **Domain:** docs
- **Arquivos esperados:** modificar `docs/process/implementation/quality_rules.md` (apenas se 11.1 + 11.2 + 15.4 + 16 deixaram lacunas)
- **Critério de aceite cobertos:** [W-PROTO-11.3]
- **Validação:** `wc -l docs/process/implementation/quality_rules.md` retorna ~180-200 linhas.

#### Gates por funcionalidade — Épico W-PROTO-11

| Funcionalidade                                                | Dev | QA | TL | PO |
|---------------------------------------------------------------|:---:|:--:|:--:|:--:|
| 11.1 Apagar §"Verificação de Conflitos"                       | ⏳  | ⏳ | ⏳ | ⏳ |
| 11.2 Mover §"Diretrizes Aprendidas"                           | ⏳  | ⏳ | ⏳ | ⏳ |
| 11.3 Reorganizar o que sobra                                  | ⏳  | ⏳ | ⏳ | ⏳ |

**Legenda:** ⏳ pendente · ✅ aprovado · ❌ reprovado · ➖ não aplicável

---

## Esclarecimentos (resolvidos por consulta)

(nenhum até o momento — adicionar conforme aparecerem)

---

## Extração pendente

### Épico W-PROTO-15
- (vazio — TL não identificou conhecimento permanente neste épico)

> Faxina documental do desenho — descontinuou dicotomia "fluxo manual (Cursor) vs autônomo" alinhando o desenho ao uso real (operador opera 100% via Claude Code Web). Sem padrão arquitetural novo; o conceito "fluxo único de execução" já está documentado no próprio escopo do épico (CONSTITUTION + autonomous/overview).

### Épico W-PROTO-16
- (vazio — TL não identificou conhecimento permanente neste épico)

> Consolidação de template existente em fonte canônica. A âncora `quality_rules.md#template-de-validação-local` é o padrão para futuras referências; observação operacional, não conhecimento arquitetural.

### Épico W-PROTO-13
- (vazio — TL não identificou conhecimento permanente neste épico)

> Faxina cirúrgica em `.github/copilot-instructions.md`. 13.1 e 13.2 declarados no-ops verificados (seções já apagadas em refinamento anterior); 13.3 removeu seção redundante. Sem padrão arquitetural novo.

### Épico W-PROTO-10
- (a preencher pelo TL)

### Épico W-PROTO-11
- (a preencher pelo TL)

---

## Status dos Gates (nível milestone)

- [x] PM ➖ todos os épicos já em `🔍` no dispatch (2026-04-29 16:19)
- [x] EM ✅ TIGHT — 3600 LOC estimado, 18 funcionalidades em 5 épicos (2026-04-29 16:19)
- [x] Scrum Master ✅ plano para 5 épicos / 18 funcionalidades escrito (2026-04-29 16:19)
- [ ] Loop por épico concluído
- [ ] RTE

### Evidências de carregamento de skill

**Únicas por milestone:**

```
[PM]  skill pulada: todos os épicos já em `🔍` ➖ 2026-04-29 16:19
[EM]  skill carregada: skills/em/skill.md ✅ 2026-04-29 16:19
[SCRUM-MASTER] skill carregada: skills/scrum-master/skill.md ✅ 2026-04-29 16:19
```

**Repetidas por funcionalidade:**

```
[QA] skills/qa/skill.md ✅ 2026-04-29 16:35 | épico W-PROTO-15 | funcionalidade 15.1
[TL] skills/tl/skill.md ✅ 2026-04-29 16:35 | épico W-PROTO-15 | funcionalidade 15.1
[PO] skills/po/skill.md ✅ 2026-04-29 16:35 | épico W-PROTO-15 | funcionalidade 15.1
[QA] skills/qa/skill.md ✅ 2026-04-29 16:36 | épico W-PROTO-15 | funcionalidade 15.2
[TL] skills/tl/skill.md ✅ 2026-04-29 16:36 | épico W-PROTO-15 | funcionalidade 15.2
[PO] skills/po/skill.md ✅ 2026-04-29 16:36 | épico W-PROTO-15 | funcionalidade 15.2
[QA] skills/qa/skill.md ✅ 2026-04-29 16:38 | épico W-PROTO-15 | funcionalidade 15.3
[TL] skills/tl/skill.md ✅ 2026-04-29 16:38 | épico W-PROTO-15 | funcionalidade 15.3
[PO] skills/po/skill.md ✅ 2026-04-29 16:38 | épico W-PROTO-15 | funcionalidade 15.3
[QA] skills/qa/skill.md ✅ 2026-04-29 16:40 | épico W-PROTO-15 | funcionalidade 15.4
[TL] skills/tl/skill.md ✅ 2026-04-29 16:40 | épico W-PROTO-15 | funcionalidade 15.4
[PO] skills/po/skill.md ✅ 2026-04-29 16:40 | épico W-PROTO-15 | funcionalidade 15.4
[QA] skills/qa/skill.md ✅ 2026-04-29 16:42 | épico W-PROTO-15 | funcionalidade 15.5
[TL] skills/tl/skill.md ✅ 2026-04-29 16:42 | épico W-PROTO-15 | funcionalidade 15.5
[PO] skills/po/skill.md ✅ 2026-04-29 16:42 | épico W-PROTO-15 | funcionalidade 15.5
[QA] skills/qa/skill.md ✅ 2026-04-29 16:43 | épico W-PROTO-15 | funcionalidade 15.6
[TL] skills/tl/skill.md ✅ 2026-04-29 16:43 | épico W-PROTO-15 | funcionalidade 15.6
[PO] skills/po/skill.md ✅ 2026-04-29 16:43 | épico W-PROTO-15 | funcionalidade 15.6
[QA] skills/qa/skill.md ✅ 2026-04-29 16:45 | épico W-PROTO-15 | funcionalidade 15.7
[TL] skills/tl/skill.md ✅ 2026-04-29 16:45 | épico W-PROTO-15 | funcionalidade 15.7
[PO] skills/po/skill.md ✅ 2026-04-29 16:45 | épico W-PROTO-15 | funcionalidade 15.7
[QA] skills/qa/skill.md ✅ 2026-04-29 16:48 | épico W-PROTO-15 | funcionalidade 15.8
[TL] skills/tl/skill.md ✅ 2026-04-29 16:48 | épico W-PROTO-15 | funcionalidade 15.8
[PO] skills/po/skill.md ✅ 2026-04-29 16:48 | épico W-PROTO-15 | funcionalidade 15.8
[QA] skills/qa/skill.md ✅ 2026-04-29 17:02 | épico W-PROTO-16 | funcionalidade 16.1
[TL] skills/tl/skill.md ✅ 2026-04-29 17:02 | épico W-PROTO-16 | funcionalidade 16.1
[PO] skills/po/skill.md ✅ 2026-04-29 17:02 | épico W-PROTO-16 | funcionalidade 16.1
[QA] skills/qa/skill.md ✅ 2026-04-29 17:05 | épico W-PROTO-16 | funcionalidade 16.2
[TL] skills/tl/skill.md ✅ 2026-04-29 17:05 | épico W-PROTO-16 | funcionalidade 16.2
[PO] skills/po/skill.md ✅ 2026-04-29 17:05 | épico W-PROTO-16 | funcionalidade 16.2
[QA] skills/qa/skill.md ➖ 2026-04-29 17:10 | épico W-PROTO-13 | funcionalidade 13.1 (no-op verificado)
[TL] skills/tl/skill.md ➖ 2026-04-29 17:10 | épico W-PROTO-13 | funcionalidade 13.1 (no-op verificado)
[PO] skills/po/skill.md ➖ 2026-04-29 17:10 | épico W-PROTO-13 | funcionalidade 13.1 (no-op verificado)
[QA] skills/qa/skill.md ➖ 2026-04-29 17:10 | épico W-PROTO-13 | funcionalidade 13.2 (no-op verificado)
[TL] skills/tl/skill.md ➖ 2026-04-29 17:10 | épico W-PROTO-13 | funcionalidade 13.2 (no-op verificado)
[PO] skills/po/skill.md ➖ 2026-04-29 17:10 | épico W-PROTO-13 | funcionalidade 13.2 (no-op verificado)
[QA] skills/qa/skill.md ✅ 2026-04-29 17:13 | épico W-PROTO-13 | funcionalidade 13.3
[TL] skills/tl/skill.md ✅ 2026-04-29 17:13 | épico W-PROTO-13 | funcionalidade 13.3
[PO] skills/po/skill.md ✅ 2026-04-29 17:13 | épico W-PROTO-13 | funcionalidade 13.3
```

---

## Histórico de Reprovações

(vazio — nenhuma reprovação até o momento)

---

## Resumo Final do Milestone

(a preencher pela RTE)
