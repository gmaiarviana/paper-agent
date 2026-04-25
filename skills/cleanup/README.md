# Cleanup Skill

> **📌 Localização:** `skills/cleanup/`
> **📌 Etapa do fluxo:** **após** o merge da PR de milestone — fase de higiene, fora da fase de implementação.
> **📌 Trigger:** GitHub Action `.github/workflows/milestone-cleanup.yml` (não Claude Code Web).
> **📌 Introduzida em:** W-PROTO-6.

---

## 1. PAPEL

A Cleanup Skill **automatiza a fase de higiene** que segue o merge de uma PR de milestone. Aplica enxugamento dos épicos no(s) `ROADMAP.md` afetado(s) (reduz cada épico a título + status + "Entregue em:") e vira o status para `✅ Implementado`. Determinística — sem julgamento arquitetural.

Substitui o ritual manual que existia em `docs/process/refinement/epic_completion.md` para os passos **enxugamento** + **transição**. A **extração** de conhecimento permanente já não é parte do rito pós-merge — virou passo do implementador (W-PROTO-7), e a Cleanup confirma que está fechada antes de rodar.

---

## 2. QUANDO USAR

A skill é invocada **automaticamente** pelo workflow `.github/workflows/milestone-cleanup.yml` quando:
- Uma PR é fechada com `merged == true`.
- A branch de origem da PR começa com `milestone/`.

**Fallback manual:** se a Action falhar (timeout, branch protection inesperada, erro de API), o dev pode carregar a skill em sessão Claude Code Web sobre `main` pós-merge, passando as três variáveis: `MILESTONE_ID`, `MERGED_PR_URL`, `MERGE_SHA`.

**Não usar se:**
- ❌ Há `❌`/`⏳`/célula vazia em `current_implementation.md` — PR não deveria ter sido mergeada; dev investiga.
- ❌ Há `- [ ]` aberto em `## Extração pendente` — Dev esqueceu de executar; dev investiga.

---

## 3. COMO FUNCIONA

A skill executa, em ordem:

1. **Validar contexto** — checa variáveis (`MILESTONE_ID`, `MERGED_PR_URL`, `MERGE_SHA`) + presença e integridade do `current_implementation.md` mergeado.
2. **Localizar milestone** — grep recursivo por `### <MILESTONE_ID>` em arquivos `ROADMAP.md`.
3. **Enxugar cada épico** — substituir o bloco do épico por forma enxugada (título + Milestone + Status `✅ Implementado` + "Entregue em:" com link da PR). Subseções de refinamento detalhado (`##### a)`, `##### b)`, etc.) são descartadas.
4. **Transitar status do milestone** — atualizar `**Status dos épicos:**` na subseção do milestone em `## 🎯 Milestones`; adicionar/atualizar `**Implementado em:**`.
5. **Commitar** — commit único `chore(cleanup): faxina pós-merge <MILESTONE_ID>`. Push direto em main (modo A) ou PR secundária via `peter-evans/create-pull-request` (modo B) conforme branch protection — workflow decide.
6. **Log** — relatório final no stdout do runner para dev auditar.

---

## 4. INPUT ESPERADO

Variáveis passadas pelo workflow:
- `MILESTONE_ID` — extraído de `pull_request.head.ref` (regex `milestone/(.+)` → upper-case).
- `MERGED_PR_URL` — `pull_request.html_url`.
- `MERGE_SHA` — `pull_request.merge_commit_sha`.

Arquivos lidos:
- `docs/process/current_implementation.md` (na main mergeada).
- `docs/process/workflow/ROADMAP.md`, `docs/ROADMAP.md`, `products/<produto>/ROADMAP.md` (cada um pode ou não conter o milestone).
- `docs/process/refinement/epic_completion.md` (regra de enxugamento + transição).

---

## 5. OUTPUT PRODUZIDO

- ✅ Edições em arquivos `ROADMAP.md` (apenas) — épicos enxugados + milestone com status agregado.
- ✅ Commit único `chore(cleanup): faxina pós-merge <MILESTONE_ID>` em main (modo A) ou em PR secundária (modo B).
- ✅ Log estruturado no runner (auditável via Actions UI).

**Não produz:**
- ❌ Edições em código, ARCHITECTURE, core-docs, .claudecode.md (extração já foi feita pelo Dev na fase de implementação).
- ❌ Decisões arquiteturais.
- ❌ Outro PR de produto.

---

## 6. INTERAÇÃO COM OUTRAS SKILLS

| Cenário | Próxima ação |
|---------|--------------|
| Tudo OK | Cleanup completa, commit em main, ROADMAP enxuto. Dev recebe notificação só se quiser auditar. |
| Gates abertos em `current_implementation.md` | Aborta com erro no log. PR não deveria ter sido mergeada — dev investiga manualmente. |
| Extração pendente aberta | Aborta com erro. Dev executa os itens manualmente em main e re-dispara via `workflow_dispatch`. |
| Branch protection bloqueia commit direto | Workflow cai para modo B (PR secundária). Skill não muda — workflow ajusta o staging. |

---

## 7. PRÉ-REQUISITO OPERACIONAL

- Secret `ANTHROPIC_API_KEY` configurado em `Settings → Secrets and variables → Actions` do repo. Sem isso, a Action falha no setup do Claude Code.
- A Action oficial Claude Code da Anthropic precisa estar disponível no marketplace (ver `.github/workflows/milestone-cleanup.yml` para o nome exato em uso).

## 8. OBSERVABILIDADE DE CUSTO

Cada execução da Action grava uma linha em `docs/process/workflow/cleanup_runs.jsonl` com:

```json
{"timestamp": "...", "milestone_id": "...", "pr": "...", "run_id": "...",
 "mode_a_outcome": "success|failure", "input_tokens": N, "output_tokens": N,
 "api_calls": N}
```

A captura é **best-effort**: lê `${{ steps.claude.outputs.execution_file }}`, soma `input_tokens`/`output_tokens` por chamada e faz append no JSONL. Falha de parse não interrompe o cleanup — o run apenas fica sem entrada no log. Custo em USD não é calculado no workflow (preço por modelo muda); cálculo ad-hoc lendo o JSONL com a tabela de pricing corrente da Anthropic.

Análise sugerida quando houver ≥5 runs: `jq` no JSONL para mediana de tokens por milestone, identificar outliers, calibrar expectativa de custo da fase de higiene.

---

## 8. PADRÃO "SKILL EM ACTION"

Esta é a **primeira skill** do paper-agent executada via GitHub Action em vez de Claude Code Web. O padrão emergente:
- Skill é autocontida (mesmo `skill.md` carrega em Action ou em Claude Code Web manualmente).
- Trigger é evento de repositório (merge de PR, push em branch específica, schedule cron).
- Workflow é mínimo: checkout + Claude Code Action + commit/push.

Candidatas futuras: skills agendadas (varredura de débito técnico, atualização de history.jsonl com loc_actual real após merge), skills reativas a issues, etc. Decisão por épico — não generalizar antes de ter sinal.

---

**Ver também:**
- Prompt operacional → [skill.md](skill.md)
- Trigger workflow → `.github/workflows/milestone-cleanup.yml`
- Rito que ela automatiza → `docs/process/refinement/epic_completion.md`
- Visão do "skill em Action" → `docs/process/workflow/vision.md`
