# Cleanup Skill

> **📌 Localização:** `skills/cleanup/`
> **📌 Etapa do fluxo:** **após** o merge da PR de um milestone — carregada no **fold-in do dispatch seguinte** (`docs/process/autonomous/dispatch.md` §4.5).
> **📌 Trigger:** o implementador, ao iniciar um milestone novo, detecta faxinas pendentes via `python -m tools.workflow_platform.cleanup_trigger --list` e roda esta skill por milestone. Fallback manual sobre `main` para o milestone terminal.
> **📌 Introduzida em:** W-PROTO-6 (originalmente via GitHub Action, depois aposentada — ver §8).

---

## 1. PAPEL

A Cleanup Skill **aplica a fase de higiene** que segue o merge de uma PR de milestone. Aplica enxugamento dos épicos no(s) `ROADMAP.md` afetado(s) (reduz cada épico a título + status + "Entregue em:") e vira o status para `✅ Implementado`. Determinística — sem julgamento arquitetural. Roda no fold-in do dispatch seguinte, commitando na branch da PR do milestone novo (diff revisado por humano).

Substitui o ritual manual que existia em `docs/process/refinement/epic_completion.md` para os passos **enxugamento** + **transição**. A **extração** de conhecimento permanente já não é parte do rito pós-merge — virou passo do implementador (W-PROTO-7), e a Cleanup confirma que está fechada antes de rodar.

---

## 2. QUANDO USAR

A skill é invocada no **fold-in do dispatch**: ao iniciar um milestone novo, o implementador roda `python -m tools.workflow_platform.cleanup_trigger --list` (detecção determinística que reusa o resolver de W-PROTO-17) e carrega esta skill para cada faxina pendente, commitando o enxugamento na branch da PR em construção. Regra completa em `docs/process/autonomous/dispatch.md` §4.5.

**Invariante que torna a detecção confiável:** um épico em `🔀 Em revisão` presente em `main` implica PR já mergeada (a RTE seta `🔀` dentro da branch, antes do push). Logo varrer `🔀` em `main` lista exatamente as faxinas pendentes — nunca o milestone atual.

**Fallback manual / milestone terminal:** o dev pode carregar a skill em sessão Claude Code Web sobre `main` pós-merge, passando as três variáveis: `MILESTONE_ID`, `MERGED_PR_URL`, `MERGE_SHA`.

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
5. **Commitar** — commit único `chore(cleanup): faxina pós-merge <MILESTONE_ID>` **na branch do milestone em andamento** (entra na PR revisada). Push é único, no fim do milestone (RTE).
6. **Log** — relatório final no relatório do milestone para o dev auditar na PR.

---

## 4. INPUT ESPERADO

Variáveis passadas pelo fold-in (uma linha de `cleanup_trigger --list` por faxina):
- `MILESTONE_ID` — resolvido via ROADMAP (épicos em `🔀` cujo `PR #N` casa).
- `MERGED_PR_URL` — URL da PR mergeada (coluna da saída de `--list`).
- `MERGE_SHA` — sha do merge dessa PR em `main` (`git log`).

Arquivos lidos:
- `docs/process/current_implementation.md` (na main mergeada).
- `docs/process/workflow/ROADMAP.md`, `docs/ROADMAP.md`, `products/<produto>/ROADMAP.md` (cada um pode ou não conter o milestone).
- `docs/process/refinement/epic_completion.md` (regra de enxugamento + transição).

---

## 5. OUTPUT PRODUZIDO

- ✅ Edições em arquivos `ROADMAP.md` (apenas) — épicos enxugados + milestone com status agregado.
- ✅ Commit único `chore(cleanup): faxina pós-merge <MILESTONE_ID>` na branch do milestone (entra na PR).
- ✅ Log estruturado no relatório do milestone (auditável na descrição da PR).

**Não produz:**
- ❌ Edições em código, ARCHITECTURE, core-docs, .claudecode.md (extração já foi feita pelo Dev na fase de implementação).
- ❌ Decisões arquiteturais.
- ❌ Outro PR de produto.

---

## 6. INTERAÇÃO COM OUTRAS SKILLS

| Cenário | Próxima ação |
|---------|--------------|
| Tudo OK | Cleanup completa, commit na branch do milestone, ROADMAP enxuto. Entra na PR para revisão humana. |
| Gates abertos em `current_implementation.md` | Aborta **esta faxina**, registra a nota e segue o milestone. Abort fica visível no diff/PR — dev investiga. |
| Extração pendente aberta | Idem: aborta a faxina, registra a nota, segue. Dev executa os itens manualmente depois. |
| Várias faxinas pendentes | Uma execução (Passos 2-5) por milestone listado em `--list`; um commit por faxina. |

---

## 7. PRÉ-REQUISITO OPERACIONAL

- Nenhum secret de CI. A skill roda no runtime já autenticado do agente implementador (fold-in) ou em sessão Claude Code Web manual. A Action que exigia `ANTHROPIC_API_KEY` foi aposentada (ver §8).

## 8. POR QUE A ACTION FOI APOSENTADA

A skill nasceu (W-PROTO-6) como a **primeira skill executada via GitHub Action** (`.github/workflows/milestone-cleanup.yml`). W-PROTO-17 consertou o trigger (resolver o milestone pelo estado do ROADMAP). Mas no primeiro run real pós-merge o passo executor (`anthropics/claude-code-action@v1`) falhou por falta de `id-token: write` (OIDC), e o desenho — agente commitando em `main` sem revisão — tinha resistência.

Decisão: **aposentar a metade-executora da Action** (não consertar o OIDC). A faxina migrou para o **fold-in do dispatch** — roda no runtime autenticado do agente e entra num diff revisado por humano. O que sobreviveu da Action: o resolver determinístico `tools/workflow_platform/cleanup_trigger.py` (agora também com `--list` para listar todas as faxinas pendentes) e esta skill autocontida.

A observabilidade de custo por run (a Action gravava tokens em `docs/process/workflow/cleanup_runs.jsonl`) foi descontinuada junto com a Action; o JSONL histórico permanece como registro dos runs antigos.

---

**Ver também:**
- Prompt operacional → [skill.md](skill.md)
- Trigger (fold-in) → `docs/process/autonomous/dispatch.md` §4.5
- Detecção determinística → `tools/workflow_platform/cleanup_trigger.py` (`--list`)
- Rito que ela automatiza → `docs/process/refinement/epic_completion.md`
- Visão do "skill em Action" → `docs/process/workflow/vision.md`
