# Validação Manual do Milestone PILOTO-WORKFLOW-DISPATCH-EPICO — dispatch/refino por épico + predecessor bloqueante

> **📌 Público:** dev (revisor da PR final).
> **📌 Arquivo:** `docs/process/current_validation.md` — rotativo, sobrescrito a cada novo milestone. Histórico fica nas PRs mergeadas.
> **📌 Quando usar:** ao receber notificação de "Milestone pronto", rodar este checklist antes de mergear.
> **📌 Princípio anti-viés:** valida critérios de aceite do ROADMAP, não a implementação. Dev executa sem precisar abrir nenhum `.py`. Editar um ROADMAP (`.md`) para montar um cenário é entrada de dados da plataforma (markdown é a fonte da verdade), não inspeção de código.

---

## Preparação do ambiente

```bash
# 1. Checkout da branch
git fetch origin
git checkout claude/admiring-ramanujan-2s5tiq
git pull origin claude/admiring-ramanujan-2s5tiq

# 2. Ambiente
source venv/bin/activate              # Linux/Mac
# .\venv\Scripts\Activate.ps1         # Windows
pip install -r requirements.txt        # reflex 0.9.0 já está pinado (nenhuma dep nova neste milestone)
```

**Pré-condição:** `git fetch origin` funcional (a fila usa `git fetch` ao carregar). `ANTHROPIC_API_KEY` não é exigida — milestone é plataforma + lógica determinística.

---

## Testes unitários (determinísticos)

```bash
pytest tests/tools/workflow_platform/ -v
```

**Esperado:** 153 testes passando, 0 falhas, 0 erros, 0 skips. Se algum falhar, parar e reportar — não seguir para a validação manual.

---

## Subir a plataforma

```bash
cd tools/workflow_platform
reflex run
# aguarde "App running at: http://localhost:3001/"
```

Abra `http://localhost:3001/` no navegador. (Portas 3001/8001 coexistem com o Ensaio em 3000/8000.)

---

## Épico W-PILOTO-DISP-1 — Dispatch e refino por épico, com predecessor bloqueante

> Critérios em [`docs/process/workflow/ROADMAP.md`](workflow/ROADMAP.md), seção `#### ÉPICO W-PILOTO-DISP-1`.

### 1.2 / 1.3 — Dispatch por épico (fatias 🔍 de milestone parcial surfaçam)

**Critério de aceite:** "`detect_dispatch`: 1 item por épico em 🔍 cujos predecessores estão **todos ✅**. Épico 🔍 com predecessor não-✅ **não** gera item. (Substitui a lógica atômica por milestone — milestone parcialmente entregue passa a surfaçar as fatias 🔍 restantes.)"

**Gatilho:**
1. Na aba **Fila** (default), localize o cabeçalho **📤 Dispatch**.
2. Selecione (clique) o card **📤 Despachar W-PILOTO-UX-2**.

**Resultado esperado:**
- O grupo **📤 Dispatch** lista **um card por épico 🔍**, não um único card por milestone. Aparecem cards separados para `W-PILOTO-UX-2`, `W-PILOTO-UX-3`, `W-PILOTO-UX-4` e `W-PILOTO-DISP-1` — mesmo o `PILOTO-WORKFLOW-UX` estando **parcialmente entregue** (UX-1 já ✅). Cada card tem título no formato `Despachar <ID>`.
- No painel de detalhe do card selecionado, o bloco "Prompt de dispatch (clipboard-ready)" mostra exatamente: `implementa o épico W-PILOTO-UX-2` (o texto por épico, não `implementa o PILOTO-WORKFLOW-UX`).

**Sinal de falha:**
- Um único card `Despachar PILOTO-WORKFLOW-UX` no lugar dos cards por épico; ou o milestone parcialmente entregue **sumir** por inteiro da Fila; ou o prompt dizer `implementa o PILOTO-WORKFLOW-UX` (nível milestone) em vez de `implementa o épico <ID>`.

---

### 1.1 / 1.4 — Épico bloqueado por predecessor não-✅ some da Fila

**Critério de aceite:** "**Fila:** épico bloqueado **não** aparece como item de ação." · "Registrar os predecessores já existentes na fonte: UX-2, UX-3, UX-4 → `W-PILOTO-UX-1`." · "Campo ausente → lista vazia; presente → IDs parseados (trim + split por vírgula)."

**Gatilho:**
1. No arquivo `docs/process/workflow/ROADMAP.md`, localize o bloco `#### ÉPICO W-PILOTO-UX-2`. Sua linha atual é `**Predecessor bloqueante:** W-PILOTO-UX-1`.
2. Troque temporariamente essa linha por: `**Predecessor bloqueante:** W-PILOTO-UX-3` (UX-3 está em 🔍, **não** ✅ — vira um predecessor não satisfeito).
3. Salve o arquivo, volte ao navegador e clique no botão **🔄 Recarregar** da sidebar.

**Resultado esperado:**
- No grupo **📤 Dispatch** da Fila, o card **Despachar W-PILOTO-UX-2** **desaparece** (bloqueado por UX-3 não-✅). Os cards de `W-PILOTO-UX-3`, `W-PILOTO-UX-4`, `W-PILOTO-DISP-1` continuam presentes.

**Sinal de falha:**
- `Despachar W-PILOTO-UX-2` continua na Fila mesmo após recarregar; ou a Fila fica vazia/quebra (traceback no console do `reflex run`).

**Cleanup:** desfaça a edição do passo 2 (`git checkout -- docs/process/workflow/ROADMAP.md`) antes de mergear.

---

### 1.4 — Kanban mantém o bloqueado visível, com selo, e clicável

**Critério de aceite:** "**Kanban:** o card do bloqueado (na coluna 🔍/📐) exibe selo discreto (🔒 + \"aguardando <ID>\") e **permanece clicável**." · "**Painel de detalhe:** bloqueado → sem botão/prompt de ação; no lugar, \"🔒 Bloqueado por <ID> (precisa estar ✅)\"."

**Gatilho:**
1. Refaça a edição do roteiro anterior (`**Predecessor bloqueante:** W-PILOTO-UX-3` no bloco de `W-PILOTO-UX-2`), salve e clique **🔄 Recarregar**.
2. Vá para a aba **Kanban**. Na coluna **🔍 Detalhes**, localize o card de `W-PILOTO-UX-2`.
3. Clique nesse card.

**Resultado esperado:**
- O card de `W-PILOTO-UX-2` na coluna 🔍 continua **visível** (não some do Kanban), com o rótulo prefixado por `🔒` e, abaixo do botão, a nota `🔒 aguardando W-PILOTO-UX-3`.
- O card responde ao clique (é clicável) e o painel de detalhe abre mostrando o callout `🔒 Bloqueado por W-PILOTO-UX-3 (precisa estar ✅)`, **sem** bloco "Prompt de dispatch" e **sem** botão de ação.

**Sinal de falha:**
- O card some do Kanban; ou não tem o selo 🔒 / a nota "aguardando"; ou não responde ao clique; ou o painel mostra o prompt de dispatch `implementa o épico W-PILOTO-UX-2` em vez do aviso de bloqueio.

**Cleanup:** desfaça a edição (`git checkout -- docs/process/workflow/ROADMAP.md`) antes de mergear.

---

## Comportamentos "não deve" (regressão)

### Não deve: o dispatch bloquear só porque um irmão do milestone está em 🏗️/🔀/✅

**Gatilho:** na aba **Fila**, observe o grupo **📤 Dispatch** com o ROADMAP **sem** edições (estado limpo — rode `git checkout -- docs/process/workflow/ROADMAP.md` se ainda editado, e **🔄 Recarregar**).

**Resultado esperado:**
- `W-PILOTO-UX-2/3/4` aparecem como cards de dispatch **mesmo** com o irmão `W-PILOTO-UX-1` do mesmo milestone já em `✅` — a presença de um irmão concluído/em execução **não** suprime as fatias 🔍 restantes.

**Sinal de falha:**
- Nenhum card de dispatch aparece para os épicos do `PILOTO-WORKFLOW-UX` sob a alegação de "milestone em execução/concluído".

---

### Não deve: REVIEW / CLEANUP / STALE_BRANCH mudarem de comportamento

**Gatilho:** na aba **Fila**, com o ROADMAP limpo, observe os grupos **🔀 Review**, **✅ Cleanup** e **🌱 Stale branches** (os que existirem no estado atual do repo).

**Resultado esperado:**
- Esses grupos seguem detectando por milestone/PR/branch como antes — este milestone só mudou dispatch e refino. Nenhum item REVIEW/CLEANUP/STALE_BRANCH some ou aparece por causa de predecessor.

**Sinal de falha:**
- Um item de REVIEW/CLEANUP/STALE_BRANCH some ou muda de agrupamento após este milestone.

---

## Critérios de aprovação

Aprove o merge quando **todos**:

- [ ] `pytest tests/tools/workflow_platform/ -v` → 153 passando, 0 falha
- [ ] Cada roteiro acima rodou e o **Resultado esperado** foi observado literalmente
- [ ] Nenhum **Sinal de falha** ocorreu
- [ ] Comportamentos "não deve" confirmados (não ocorreram)
- [ ] `docs/process/workflow/ROADMAP.md` voltou ao estado limpo (edições de teste revertidas)
- [ ] Tabela do Copilot na PR (Seção 🎯) sem ❌ sem justificativa

**Se algum critério falhar:** devolver com feedback para nova rodada autônoma (Claude Code Web) ou abrir sessão estratégica externa se exigir decisão arquitetural.

---

**Ver também:**
- Skill da RTE → [skills/rte/skill.md](../../skills/rte/skill.md)
- Validação geral do modo autônomo → [docs/process/autonomous/delivery.md](autonomous/delivery.md)
