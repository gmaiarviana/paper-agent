# Review-PR Skill

> **📌 Localização:** `skills/review-pr/`
> **📌 Etapa do fluxo:** **entrada** — quando o operador traz uma PR para avaliar (não é etapa do fluxo autônomo de entrega).
> **📌 Trigger:** gatilho durável em [`CLAUDE.md`](../../CLAUDE.md) — operador cola descrição, link (`.../pull/N`) ou número (`#N`) de PR sem outro pedido.

---

## 1. PAPEL

A Review-PR Skill **produz um parecer técnico** sobre uma PR. Nasceu para dar a opção de revisar PR no próprio Claude Code — **alternativa** ao GitHub Copilot, que segue valendo. Antes, colar a descrição de uma PR não disparava nada: o Claude travava pedindo desambiguação. A skill torna esse fluxo explícito e reproduzível.

Ela **delega às revisoras nativas** (`/review` para PR do GitHub, `/code-review` para diff local) e acrescenta **só o contexto deste repo**: ledger de milestone (`current_implementation.md`), flags de pytest, worktree para rodar testes sem trocar de branch, e o modelo de duas fases da faxina (épico em `🔀 Em revisão` é estado esperado, não defeito).

É **só de leitura/análise** (não commita, não mergeia, não abre PR, não faz push, não toca no template) — mas **antecipa o máximo**: roda todos os testes/greps que der e, em sessão local com veredito ✅, **sobe a própria app** para entregar a demo já no ar. Ao operador sobra só o irredutível: abrir, navegar, observar o valor.

---

## 2. QUANDO USAR

Sempre que o operador trouxer uma PR para avaliar — colando a **descrição**, um **link** ou um **número**. O gatilho em `CLAUDE.md` dispara a invocação automaticamente.

**Não usar se:**
- ❌ O pedido é **implementar/corrigir**, não revisar — aí é fluxo de dispatch/RTE.
- ❌ O texto é genuinamente ambíguo (nem PR, nem branch, nem diff) — perguntar antes.

---

## 3. COMO FUNCIONA

1. **Identificar a entrada** — descrição / link / número → escolher `/review` ou `/code-review`. Nunca travar pedindo desambiguação quando é reconhecível como PR.
2. **Mapear o diff** — `git diff --stat origin/main...<branch>` primeiro, depois o diff completo.
3. **Revisar por camada** — lógica (vs critérios do milestone), testes (cobrem as fronteiras?), docs (consistência interna).
4. **Rodar a suíte relevante num worktree** — `--noconftest --ignore=tests/core/integration`, sem trocar a branch ativa.
5. **Confirmar claims e triar falhas** — regressão (arquivo tocado / passa na main) vs pré-existente (falha idêntica em `origin/main`); path separator no Windows = não-regressão.
6. **Montar o roteiro mínimo de validação de valor** — se a PR muda comportamento observável (UI/UX, CLI, LLM), 2-3 checks do valor central, derivados do `current_validation.md`; senão, uma linha de ausência justificada.
7. **Limpar o worktree** — `git worktree remove --force` + `prune`.
8. **Fechar com veredito** — ressalvas (recomendação → por quê → trade-off) + seção 🧪 roteiro, e um dos dois braços:
   - **✅ Aprovar** → em sessão local, sobe a app (`/run`) e restaura a working tree para entregá-la **já no ar** (headless → comando pronto + oferta de `/run`).
   - **🔧 Mudanças pedidas** → emite o **📮 prompt de retrabalho** (achados bloqueantes, `arquivo:linha`, critério) pro operador colar no agente que implementou. Loop: fix → re-validação (a skill re-roda na branch atualizada).

---

## 4. INPUT ESPERADO

- Descrição de PR colada, **ou** link `https://github.com/<owner>/<repo>/pull/<N>`, **ou** número `#<N>`.

Arquivos lidos (não escritos):
- Diff da branch vs `main`.
- `docs/process/current_implementation.md` (ledger de milestone — critérios de aceite).
- `docs/process/current_validation.md` (seção 🎯 — fonte do roteiro mínimo de valor).
- ROADMAP(s) afetados (consistência de docs).
- `.claudecode.md` (flags de pytest, armadilhas de Windows).

---

## 5. OUTPUT PRODUZIDO

- ✅ **Parecer** (mensagem ao operador): veredito binário + camadas + falhas triadas + ressalvas no formato canônico + **🧪 roteiro mínimo de validação de valor** (ou ausência justificada).
- ✅ **Demo antecipada** (veredito ✅ + árvore ativa já sendo a branch da PR): app já no ar (`http://localhost:3001/`) com os 2-3 passos de navegação — o teste final do operador é só abrir e observar.

**Não produz:**
- ❌ Commit, merge, push, PR nova, comentário via `gh`.
- ❌ Edição do template de PR.
- ❌ Escrita em código/docs versionados. A única mutação é **efêmera** — os arquivos que o `reflex run` gera na demo, restaurados em seguida (`git checkout`).

---

## 6. INTERAÇÃO COM OUTRAS SKILLS

| Cenário | Relação |
|---------|---------|
| PR de milestone do fluxo autônomo | A RTE abre a PR; a Review-PR a avalia. Épicos em `🔀 Em revisão` são esperados — a faxina (`cleanup`) só transita para `✅` pós-merge. |
| Falha de teste na revisão | Triada contra `origin/main` — não bloqueia se for pré-existente ou path separator no Windows. |
| Parecer pede mudanças (🔧) | A skill emite o 📮 prompt de retrabalho; o operador cola no agente implementador → fix → a skill re-valida. A skill nunca escreve nem despacha sozinha. |

---

**Ver também:**
- Prompt operacional → [skill.md](skill.md)
- Gatilho durável → [`CLAUDE.md`](../../CLAUDE.md)
- Flags de pytest e Windows → [`.claudecode.md`](../../.claudecode.md)
- Modelo de duas fases da faxina → [`skills/cleanup/skill.md`](../cleanup/skill.md)
