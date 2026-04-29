# Implementação Atual: Milestone PROTO-WORKFLOW-COPILOT-STACK

**Milestone:** PROTO-WORKFLOW-COPILOT-STACK — alinhar `copilot-instructions.md` à mudança de stack do Ensaio (Streamlit → Reflex, ADR 001)
**Produto:** workflow
**Estágio:** Protótipo
**Branch:** `claude/implement-copilot-stack-gSUxf` (harness-assigned; equivalente a `milestone/proto-workflow-copilot-stack` no fluxo manual)
**Modo:** Autônomo
**Dispatch recebido em:** 2026-04-29

---

## Contexto do Milestone

**Objetivo:** alinhar `copilot-instructions.md` à mudança de stack do Ensaio (Streamlit → Reflex, ADR 001 de 2026-04-25). Ajuste pequeno e operacional — o Copilot hoje manda Streamlit pros dois produtos e a validação de branches do Ensaio quebra ou roda com comando errado.

**Épicos agrupados:** W-PROTO-14

**Dependências de core:** nenhuma. Comandos de Reflex já fixados pelo ADR 001 + `products/ensaio/rxconfig.py` — sem input pendente do dev.

---

## Sizing (EM) — 2026-04-29 15:30

- Milestone: PROTO-WORKFLOW-COPILOT-STACK (Protótipo, workflow)
- Épicos avaliados: 1
- Funcionalidades: 3 (W-PROTO-14: 14.1 + 14.2 + 14.3)
- Fator de risco médio: 1.0 (sem refator declarado, sem integração com sistema existente, sem dependência core não-✅)
- Cálculo: 3 × 200 × 1.0 = **600 LOC estimado**
- Decisão: **FIT** (≤ 3000)
- Linha persistida em `docs/process/sizing/history.jsonl`

---

## Épicos

Um bloco por épico, na ordem de execução.

---

### Épico W-PROTO-14 — Operacionalizar Reflex no fluxo de validação do Copilot

**Status:** ✅ Implementado
**Objetivo:** o Ensaio migrou para Reflex no Protótipo (ADR 001), mas `copilot-instructions.md` ainda manda Streamlit pros dois produtos. Validação de branches do Ensaio quebra ou roda com comando errado.
**Dependências:** ADR 001 (`products/ensaio/docs/adr/001-stack-do-prototipo.md`); `products/ensaio/rxconfig.py`. Coordena com W-PROTO-13.3 (futuro).

#### Funcionalidades

##### 14.1 — Detecção de stack por produto

- **Domain:** docs
- **Estimativa:** ~25 linhas | risco: baixo
- **Arquivos esperados:**
  - modificar: `.github/copilot-instructions.md` (inserir nova §"Stacks por produto" entre linhas 31 e 35)
- **Padrão a seguir:** conteúdo verbatim declarado em W-PROTO-14.1 do ROADMAP.
- **Critérios de aceite cobertos:** [W-PROTO-14.1]
- **Validação:** seção "Stacks por produto" presente; tabela inclui Revelar (Streamlit, 8501-8503) e Ensaio (Reflex, 3000+8000); regra "se branch toca produto fora da tabela, parar e reportar" presente.

##### 14.2 — Comando de subida por stack na §3

- **Domain:** docs
- **Estimativa:** ~30 linhas | risco: baixo
- **Arquivos esperados:**
  - modificar: `.github/copilot-instructions.md` (substituir §3 "Subir a app afetada", linhas 68-96 hoje)
- **Padrão a seguir:** conteúdo verbatim declarado em W-PROTO-14.2 do ROADMAP.
- **Critérios de aceite cobertos:** [W-PROTO-14.2]
- **Validação:** `grep -n "reflex run" .github/copilot-instructions.md` ≥ 1; `grep -n "products/ensaio" .github/copilot-instructions.md` ≥ 1; §3 ramifica visualmente entre Streamlit (Revelar) e Reflex (Ensaio).

##### 14.3 — Liberação de portas por stack

- **Domain:** docs
- **Estimativa:** ~25 linhas | risco: baixo
- **Arquivos esperados:**
  - modificar: `.github/copilot-instructions.md` (substituir bloco de liberação de portas hardcoded em 8501-8503 por bloco que cobre Streamlit e Reflex)
- **Padrão a seguir:** conteúdo verbatim declarado em W-PROTO-14.3 do ROADMAP.
- **Critérios de aceite cobertos:** [W-PROTO-14.3]
- **Validação:** `grep -nE "8501|8502|8503|3000|8000" .github/copilot-instructions.md` retorna linhas em §"Liberação de portas"; bloco menciona Streamlit (8501-8503) e Reflex (3000, 8000) explicitamente.

#### Gates por funcionalidade — Épico W-PROTO-14

| Funcionalidade                                | Dev | QA | TL | PO |
|-----------------------------------------------|:---:|:--:|:--:|:--:|
| 14.1 Detecção de stack por produto            | ✅  | ✅ | ✅ | ✅ |
| 14.2 Comando de subida por stack na §3        | ✅  | ✅ | ✅ | ✅ |
| 14.3 Liberação de portas por stack            | ✅  | ✅ | ✅ | ✅ |

**Legenda:** ⏳ pendente · ✅ aprovado · ❌ reprovado · ➖ não aplicável

---

## Esclarecimentos (resolvidos por consulta)

- ✅ Posição de §"Liberação de portas" — fonte: ROADMAP W-PROTO-14.2 referencia `(ver §"Stacks por produto" + §"Liberação de portas" abaixo)`. Implementado como sub-seção dentro de §3, imediatamente após o parágrafo de detecção de produto, antes dos blocos Streamlit/Reflex — preserva fluxo "detectar → liberar portas → subir app".
- ✅ Comandos Reflex e portas — fonte: `products/ensaio/rxconfig.py` confirma `frontend_port=3000` e `backend_port=8000`; ADR 001 declara `cd products/ensaio && reflex run`.

---

## Extração pendente

### Épico W-PROTO-14
- (vazio — TL não identificou conhecimento permanente neste épico)

> Épico cirúrgico em arquivo de instruções operacionais; sem padrão arquitetural novo a extrair para `docs/ARCHITECTURE.md` ou similar. ADR 001 já cobre a decisão de stack.

---

## Status dos Gates (nível milestone)

- [x] PM ➖ todos os épicos já em `🔍` no dispatch (2026-04-29 15:30)
- [x] EM ✅ FIT — 600 LOC estimado (2026-04-29 15:30)
- [x] Scrum Master ✅ plano para 1 épico / 3 funcionalidades escrito (2026-04-29 15:32)
- [x] Loop por épico concluído (todas as células Dev/QA/TL/PO ✅)
- [x] RTE ✅ PR aberta (2026-04-29 15:50)

### Evidências de carregamento de skill

**Únicas por milestone:**

```
[PM]  skill pulada: todos os épicos já em `🔍` ➖ 2026-04-29 15:30
[EM]  skill carregada: skills/em/skill.md ✅ 2026-04-29 15:30
[SCRUM-MASTER] skill carregada: skills/scrum-master/skill.md ✅ 2026-04-29 15:32
[RTE] skill carregada: skills/rte/skill.md ✅ 2026-04-29 15:50
```

**Repetidas por funcionalidade:**

```
[QA] skills/qa/skill.md ✅ 2026-04-29 15:38 | épico W-PROTO-14 | funcionalidade 14.1
[TL] skills/tl/skill.md ✅ 2026-04-29 15:39 | épico W-PROTO-14 | funcionalidade 14.1
[PO] skills/po/skill.md ✅ 2026-04-29 15:40 | épico W-PROTO-14 | funcionalidade 14.1
[QA] skills/qa/skill.md ✅ 2026-04-29 15:42 | épico W-PROTO-14 | funcionalidade 14.2
[TL] skills/tl/skill.md ✅ 2026-04-29 15:43 | épico W-PROTO-14 | funcionalidade 14.2
[PO] skills/po/skill.md ✅ 2026-04-29 15:44 | épico W-PROTO-14 | funcionalidade 14.2
[QA] skills/qa/skill.md ✅ 2026-04-29 15:46 | épico W-PROTO-14 | funcionalidade 14.3
[TL] skills/tl/skill.md ✅ 2026-04-29 15:47 | épico W-PROTO-14 | funcionalidade 14.3
[PO] skills/po/skill.md ✅ 2026-04-29 15:48 | épico W-PROTO-14 | funcionalidade 14.3
```

---

## Histórico de Reprovações

(vazio — nenhuma reprovação nesta sessão)

---

## Resumo Final do Milestone

**Identificação:**
- Milestone: PROTO-WORKFLOW-COPILOT-STACK
- Branch: `claude/implement-copilot-stack-gSUxf`
- Data de fechamento: 2026-04-29

**Números reais (decomposição por épico):**

| Métrica                     | W-PROTO-14 | Total milestone |
|-----------------------------|:----------:|:---------------:|
| Funcionalidades aprovadas   | 3          | 3               |
| Arquivos modificados (código/docs) | 1 (docs)   | 1 (1 docs)      |
| Testes adicionados          | 0          | 0               |

**Arquivos modificados (foco do milestone):** `.github/copilot-instructions.md` (escopo declarado do épico). Adicionalmente: `docs/process/current_implementation.md`, `docs/process/current_validation.md`, `docs/process/sizing/history.jsonl`, `docs/process/workflow/ROADMAP.md` (transição para 🔀), `skills/audit_log.jsonl` — gerados/atualizados pelas próprias skills.

**Notas técnicas (TL):** sem observações arquiteturais — escopo cirúrgico em arquivo de instruções operacionais. Referência ao Reflex (e portas 3000/8000) passa a coexistir com Streamlit (e portas 8501-8503) na mesma doc, com ramificação clara por produto.

**Gates: todos ✅** em todas as 3 funcionalidades (Dev/QA/TL/PO).
