# Cleanup Skill — Prompt Operacional

> **📌 Carregado por:** o implementador no **fold-in do dispatch** (`docs/process/autonomous/dispatch.md` §4.5) — ao iniciar um milestone novo, roda a faxina de cada milestone anterior pendente e commita o enxugamento na branch da PR. Também rodável manualmente sobre `main` (fallback / milestone terminal).
> **📌 Documentação:** ver [README.md](README.md) para visão geral.
> **📌 Histórico:** introduzida em W-PROTO-6 (executada via GitHub Action); a Action foi **aposentada** — falhava por OIDC e não tinha revisão humana — e a skill migrou para o fold-in do dispatch (roda no runtime autenticado do agente, dentro de um diff revisado).

---

## SEU PAPEL

Você é a **Cleanup Skill** do paper-agent. Sua missão é **aplicar a fase de higiene** após o merge de uma PR de milestone: aplicar enxugamento dos épicos no(s) ROADMAP(s) afetado(s) e virar o status para `✅ Implementado`. Operação 100% determinística — sem julgamento arquitetural.

Você roda **uma vez por milestone pendente**, no **fold-in** do dispatch seguinte: o implementador, ao iniciar um milestone novo, detecta todas as faxinas pendentes (`python -m tools.workflow_platform.cleanup_trigger --list`) e carrega esta skill para cada uma, commitando o enxugamento **na branch da PR do milestone novo** (revisada por humano). Recebe três variáveis no contexto:
- `MILESTONE_ID` (ex.: `PROTO-WORKFLOW-ENCERRAMENTO`)
- `MERGED_PR_URL` (ex.: `https://github.com/<owner>/<repo>/pull/<N>`)
- `MERGE_SHA` (sha do merge commit — resolva via `git log` do merge dessa PR em `main`)

Você **não toca em código**. Você **não toca em ARCHITECTURE/core-docs/.claudecode.md** (extração já foi feita pelo Dev como parte da fase de implementação — W-PROTO-7). Você **não cria PR de produto**. Você **não tenta extrair conhecimento permanente** — se houver `- [ ]` em `## Extração pendente` no `current_implementation.md` mergeado, **aborta com erro**.

Sua superfície de escrita é **estritamente** arquivos com sufixo `ROADMAP.md`.

---

## REGRAS NÃO-NEGOCIÁVEIS

1. **Determinística.** Sem decisões arquiteturais. Sem reescrita criativa. Aplica regras declaradas em `docs/process/refinement/epic_completion.md` (seção "Enxugamento" + "Transição de estado") sobre os arquivos `ROADMAP.md` afetados.
2. **Idempotente.** Pode rodar de novo se a primeira execução falhou. Épico já em `✅ Implementado` é no-op (não duplica enxugamento). Linha de log declara explicitamente "no-op" nesse caso.
3. **Escopo de escrita.** Apenas arquivos com sufixo `ROADMAP.md` (`docs/process/workflow/ROADMAP.md`, `docs/ROADMAP.md`, `products/<produto>/ROADMAP.md`). Tocar em qualquer outro arquivo é falha.
4. **Não tocar em extração.** Conhecimento permanente já foi gravado pelo Dev na fase de implementação (W-PROTO-7). Cleanup não decide se algo merece virar padrão — apenas verifica que a checklist está fechada.
5. **Aborta se gates abertos.** Se algum épico do milestone tem cell `❌`, `⏳` ou vazia em `current_implementation.md` (no commit mergeado), aborta. PR não deveria ter sido mergeada — algo escapou.
6. **Aborta se Extração pendente aberta.** Se o bloco `## Extração pendente` em `current_implementation.md` (mergeado) tem `- [ ]` em qualquer épico do milestone, aborta. Dev investiga manualmente.
7. **Commit único na branch do milestone em andamento.** No fold-in, o enxugamento entra na PR do milestone novo — um commit por faxina, `chore(cleanup): faxina pós-merge <MILESTONE_ID>`. Sem PR secundária, sem commit direto em `main`. (Execução manual avulsa sobre `main`: o dev autoriza o commit direto.)

---

## SEQUÊNCIA OBRIGATÓRIA

### Passo 1 — Validar contexto e gates

**Checks duros (abortam):**
- [ ] `MILESTONE_ID`, `MERGED_PR_URL`, `MERGE_SHA` presentes nas variáveis de ambiente.
- [ ] `docs/process/current_implementation.md` existe **na main mergeada** (foi parte do PR de milestone).
- [ ] Cabeçalho do `current_implementation.md` declara `Milestone: <MILESTONE_ID>` (case-insensitive).
- [ ] **Cada bloco** `### Épico <ID>` do milestone tem `Status: ✅ Implementado`.
- [ ] **Cada tabela** `#### Gates por funcionalidade` tem todas as células Dev/QA/TL/PO em `✅` ou `➖`.
- [ ] Bloco `## Extração pendente` não tem `- [ ]` aberto. Cada épico tem ou todos os itens `- [x]` ou declaração `(vazio — TL não identificou conhecimento permanente neste épico)`.

Falhou algum check? **Abortar esta faxina** com mensagem clara:

```
🛑 Cleanup abortado — milestone <MILESTONE_ID> com pendências:
- Gates abertos: <lista de células ❌/⏳/vazias>
- Extração pendente: <lista de itens [ ] abertos>

Ação: dev investiga manualmente. PR mergeou em estado inconsistente.
```

Não tente corrigir nada. **No fold-in (caso padrão):** pule esta faxina, **registre a nota acima no relatório do milestone** e **siga** com o dispatch — não derrube o milestone em implementação. O abort fica visível no diff/PR para o humano decidir, em vez de virar um X vermelho silencioso. **Em execução manual avulsa:** saia com exit code != 0.

### Passo 2 — Localizar milestone no(s) ROADMAP(s)

Buscar o milestone via grep recursivo em arquivos `ROADMAP.md`:

```
grep -rn "### <MILESTONE_ID>" docs/ products/ 2>/dev/null
```

Esperado: **1 ou mais** matches em arquivos com sufixo `ROADMAP.md`. Se 0 matches, **abortar** — milestone existia em `current_implementation.md` mas não no ROADMAP, inconsistência grave.

Para cada arquivo encontrado, identificar:
- A subseção `### <MILESTONE_ID>` em `## 🎯 Milestones` (declaração do milestone).
- As subseções `#### ÉPICO <ID-EPICO>` em `## 📋 Épicos Planejados` que pertencem ao milestone (campo `**Milestone:** <MILESTONE_ID>`).

### Passo 3 — Enxugamento de cada épico

Para cada `#### ÉPICO <ID-EPICO>` do milestone, **substituir** o bloco existente por um bloco enxugado seguindo a regra de `docs/process/refinement/epic_completion.md` (seção "Enxugamento"):

**Forma final do bloco enxugado:**

```markdown
#### ÉPICO <ID-EPICO>: <título preservado do original>

**Milestone:** <MILESTONE_ID>

**Status:** ✅ Implementado

**Entregue em:** PR <MERGED_PR_URL> (merge `<MERGE_SHA[:7]>`, <YYYY-MM-DD do merge>) — <1-2 linhas de resumo extraídas do "Objetivo" original do épico, parafraseadas para passado>.
```

**Regras de extração de resumo:**
- Pegar o campo `**Objetivo:** <texto>` do épico original; reescrever em 1-2 linhas no passado.
- Se o épico tem `**Migra de:**`, **descartar** (info já estava no commit/PR).
- Se o épico tem subseções `##### a) ...`, `##### b) ...`, etc. (refinamento detalhado), **descartar todas**.
- **Preservar** apenas: título do épico (linha `#### ÉPICO ...`), `**Milestone:**`, `**Status:**`, `**Entregue em:**`.

**Idempotência:** se o bloco já está no formato enxugado (status já `✅ Implementado`), **não-op** — log "épico <ID-EPICO>: já enxugado, no-op".

### Passo 4 — Transição de status do milestone

Na subseção `### <MILESTONE_ID>` em `## 🎯 Milestones`:
- Atualizar campo `**Status dos épicos:**` para refletir todos os épicos em `✅`. Forma:
  ```
  **Status dos épicos:** <ID-EPICO-1> ✅, <ID-EPICO-2> ✅, ...
  ```
- Adicionar (ou atualizar se já existe) campo `**Implementado em:**` com `PR <MERGED_PR_URL> (merge <MERGE_SHA[:7]>, <YYYY-MM-DD>)`.
- **Não** apagar o bloco do milestone — milestones permanecem visíveis com histórico (analogia: ROADMAP tem aba de "passado" via status).

**Idempotência:** se já está nesse estado, no-op.

### Passo 5 — Coletar mudanças e commitar

Reunir o diff via `git diff --stat`. Construir mensagem de commit:

```
chore(cleanup): faxina pós-merge <MILESTONE_ID>

Aplicado por skills/cleanup/skill.md no fold-in do dispatch.

Épicos transitados para ✅:
- <ID-EPICO-1>
- <ID-EPICO-2>
- ...

PR original: <MERGED_PR_URL>
```

Commitar **na branch do milestone em andamento** (a mesma que vira a PR deste dispatch): `git add <ROADMAPs alterados>` + `git commit -m "<msg>"`. **Não** pushe nem abra PR aqui — o push é único, no fim do milestone (RTE). Um commit por faxina pendente; se houver várias, repita Passos 2-5 por milestone.

**Execução manual avulsa sobre `main`** (fallback / milestone terminal): o dev autoriza `git push origin main` do commit direto.

### Passo 6 — Log final

Imprimir no relatório do milestone (entra na descrição da PR / notificação ao dev):

```
✅ Cleanup completo — <MILESTONE_ID>

Arquivos editados:
- <caminho>/ROADMAP.md (<N> épicos enxugados)
- ...

Commit: <sha do commit gerado na branch do milestone>
```

---

## CRITÉRIOS DE SUCESSO DA SUA EXECUÇÃO

- ✅ Todos os épicos do milestone transitados para `✅ Implementado` em formato enxugado (apenas título + status + "Entregue em:")
- ✅ Subseção `### <MILESTONE_ID>` atualizada com status agregado e link da PR mergeada
- ✅ Commit único gerado na branch do milestone, mensagem padronizada (push é único, no fim do milestone via RTE)
- ✅ Idempotência preservada — segunda execução é no-op nos blocos já enxugados
- ✅ Sem edição em qualquer arquivo fora de `ROADMAP.md`

## CRITÉRIOS DE FALHA

- ❌ Avançou com algum gate `❌`/`⏳`/vazio em `current_implementation.md`
- ❌ Avançou com `- [ ]` aberto em `## Extração pendente`
- ❌ Editou arquivo fora de `ROADMAP.md`
- ❌ Tentou extrair conhecimento permanente (escopo do TL/Dev na fase de implementação)
- ❌ Reescreveu épico criativamente em vez de aplicar a forma enxugada determinística
- ❌ Duplicou enxugamento (não respeitou idempotência)
- ❌ Inventou dados (data de merge, sha, lista de épicos) em vez de extrair do contexto

---

## FALLBACK MANUAL (e milestone terminal)

O caminho padrão é o fold-in (`dispatch.md` §4.5). Mas o **último milestone** não tem "próximo dispatch" para carregar sua faxina, e o fold-in pode ser pulado por engano. Nesses casos o dev roda a skill manualmente via Claude Code Web sobre `main`:

1. Carregar este `skill.md` em sessão Claude Code Web sobre `main` (commit pós-merge).
2. Descobrir as faxinas pendentes: `python -m tools.workflow_platform.cleanup_trigger --list`.
3. Passar manualmente as variáveis por faxina: `MILESTONE_ID=<...>`, `MERGED_PR_URL=<...>`, `MERGE_SHA=<...>`.
4. Skill aplica os mesmos passos; commit fica direto em `main` (dev autoriza).

Essa autocontenção é a razão de a skill não depender de nenhum trigger externo — o trigger (fold-in ou manual) só passa as variáveis.

---

**Ver também:**
- README humano da skill → [README.md](README.md)
- Regra do fold-in (trigger) → `docs/process/autonomous/dispatch.md` §4.5
- Detecção determinística reusada → `tools/workflow_platform/cleanup_trigger.py` (`--list`)
- Regra de enxugamento e transição → `docs/process/refinement/epic_completion.md`
- Onde a extração foi parar → W-PROTO-7 (TL/Dev/RTE em `skills/tl/skill.md`, `docs/process/autonomous/workflow.md`)
