# Validação Manual do Milestone PROTO-WORKFLOW-FILA — fila reativa + chat focado por item + auto-regulação básica + persistência de preferências

> **📌 Público:** dev (revisor da PR final).
> **📌 Arquivo:** `docs/process/current_validation.md` — rotativo, sobrescrito a cada novo milestone (igual a `current_implementation.md`). Histórico fica nas PRs mergeadas.
> **📌 Quando usar:** ao receber notificação da sessão autônoma de "Milestone pronto", rodar este checklist antes de mergear.
> **📌 Princípio anti-viés:** este arquivo valida critérios de aceite do ROADMAP, não a implementação. Dev executa este arquivo sem precisar abrir nenhum `.py`.

---

## Preparação do ambiente

```bash
# 1. Checkout da branch
git fetch origin
git checkout claude/execute-project-workflow-yoTQ7
git pull origin claude/execute-project-workflow-yoTQ7

# 2. Ambiente
source venv/bin/activate              # Linux/Mac
# .\venv\Scripts\Activate.ps1         # Windows
pip install -r requirements-test.txt   # se deps mudaram no milestone
pip install streamlit                  # plataforma usa Streamlit
```

**Pré-condição:** `git fetch origin` funcional (a fila usa `git fetch origin --prune` ao recarregar). `ANTHROPIC_API_KEY` não é exigida pra esta validação — milestone é puramente plataforma + lógica determinística.

---

## Testes unitários (determinísticos)

```bash
pytest tests/tools/workflow_platform/ -v
```

**Esperado:** 120 testes passando, 0 falhas, 0 erros, 0 skips. Se algum falhar, parar e reportar — não seguir para validação manual.

---

## Épico W-PROTO-FILA-1 — Detecção reativa de eventos e shape de item

> Critérios em [`docs/process/workflow/ROADMAP.md`](workflow/ROADMAP.md), seção `#### ÉPICO W-PROTO-FILA-1`.

### 1.1 — Shape mínimo de item de fila

**Critério de aceite:** "Tentar instanciar `QueueItem(type=DISPATCH, source_pointer=BranchPointer(...))` deve falhar via runtime check em `__post_init__` ou validação pydantic-style (não silenciar inconsistência)."

**Gatilho:**
1. Abra o terminal a partir da raiz do repo.
2. Cole exatamente este comando:
   ```bash
   python -c "
   from datetime import datetime
   from tools.workflow_platform.queue.models import (
       QueueItem, ItemType, BranchPointer
   )
   QueueItem(
       id='x', type=ItemType.DISPATCH, title='t', context='c',
       expected_action='a',
       source_pointer=BranchPointer(branch_name='b', last_commit_at=datetime.now(), days_stale=1),
       detected_at=datetime.now(),
   )
   "
   ```

**Resultado esperado:**
- `TypeError: ItemType.DISPATCH expects EpicPointer, got BranchPointer` (ou mensagem equivalente apontando que DISPATCH espera EpicPointer)

**Sinal de falha:**
- Comando termina sem erro, ou erro genérico que não cita o tipo esperado, ou silenciamento da inconsistência.

---

### 1.2 — Detecção dos 5 tipos a partir do estado-do-mundo

**Critério de aceite:** "`detect_dispatch_items(roadmaps)` deve gerar 1 item por milestone com **todos** os épicos em 🔍 e nenhum em 🏗️/🔀/✅; milestones sem milestone_id ou com pelo menos 1 épico em estado de execução não geram item."

**Gatilho:**
1. A partir da raiz do repo, cole:
   ```bash
   pytest tests/tools/workflow_platform/test_queue_detect.py -v
   ```

**Resultado esperado:**
- Saída mostra `25 passed`. Os testes cobrem milestone com todos 🔍 (gera 1 DISPATCH), com 1 em 🏗️ (não gera), com 1 em 🔀 (não gera), com 1 em ✅ (não gera), com 1 pré-🔍 (não gera), épicos sem milestone (skip).

**Sinal de falha:**
- Qualquer teste com `FAILED`, `ERROR` ou `SKIPPED`. Saída de `pytest` lista cada caso por nome.

---

### 1.3 — Garantia de determinismo via fixture-snapshot

**Critério de aceite:** "Mudança no código de detecção que altera shape ou regra deve quebrar `test_detect_snapshot` — atualizar snapshot é decisão consciente, não acidental."

**Gatilho:**
1. Cole:
   ```bash
   pytest tests/tools/workflow_platform/test_queue_determinism.py -v
   ```

**Resultado esperado:**
- 3 testes passando (`test_detect_is_deterministic`, `test_detect_snapshot`, `test_snapshot_has_three_items_one_of_each_relevant_type`).
- Snapshot tem exatamente 1 DISPATCH, 1 REVIEW, 1 STALE_BRANCH (REFINE/CLEANUP cobertos pelos testes unitários da 1.2).

**Sinal de falha:**
- Falha em `test_detect_snapshot` ou em `test_detect_is_deterministic`. Diferença entre duas chamadas consecutivas em estado fixo.

---

## Épico W-PROTO-FILA-2 — Exibição da fila + prompt focado por item

> Critérios em [`docs/process/workflow/ROADMAP.md`](workflow/ROADMAP.md), seção `#### ÉPICO W-PROTO-FILA-2`.

### 2.1 — View da fila como tab default

**Critério de aceite:** "App abre com tab '📋 Fila' ativa por default; tab '🗂️ Kanban' continua acessível em segundo plano com renderização inalterada."

**Gatilho:**
1. A partir da raiz do repo:
   ```bash
   streamlit run tools/workflow_platform/app.py
   ```
2. Aguarde o navegador abrir em http://localhost:8501.

**Resultado esperado:**
- Cabeçalho "🧭 Plataforma de Workflow".
- Logo abaixo do cabeçalho aparecem **duas abas**: "📋 Fila" (selecionada/ativa) e "🗂️ Kanban".
- A área visível imediatamente é o conteúdo da tab Fila (cards agrupados por tipo, ou banner "Sem itens na fila").
- Clicar na tab "🗂️ Kanban" mostra o kanban com 8 colunas como antes.

**Sinal de falha:**
- App abre direto no kanban sem tabs visíveis.
- Tab default é Kanban em vez de Fila.
- Tab Kanban não renderiza ou perdeu colunas.

---

**Critério de aceite:** "Cards são agrupados visualmente por `ItemType` com cabeçalho de seção (`st.subheader('📤 Dispatch (N)')`); cada cabeçalho mostra contagem do tipo."

**Gatilho:**
1. (Continua na tab Fila do app rodando.) Aguarde a fila carregar.

**Resultado esperado:**
- Cada bucket presente é precedido por subheader: `📤 Dispatch (N)`, `🔀 Review (N)`, `📐 Refine (N)`, `✅ Cleanup (N)`, `🌱 Stale branches (N)`. Buckets vazios são omitidos.
- N à direita do nome do tipo bate com o número de cards visíveis logo abaixo.

**Sinal de falha:**
- Cards aparecem misturados sem cabeçalhos.
- Contagem entre parênteses não bate com o número de cards do bucket.

---

**Critério de aceite:** "Botão '🔄 Recarregar' (sidebar) limpa state da fila e re-instancia WorldState (incluindo subprocess `git fetch origin --prune`); falha de fetch é exibida em `st.warning` mas não impede renderização."

**Gatilho:**
1. (App rodando na tab Fila.) Na sidebar, clique no botão "🔄 Recarregar".

**Resultado esperado:**
- Página re-renderiza após ~1-3 segundos (delay do `git fetch`).
- Lista de cards permanece visível depois da recarga (mesmo se `git fetch` falhasse, render persiste).

**Sinal de falha:**
- Tela em branco ou traceback após o clique.
- App trava esperando fetch sem timeout.

---

### 2.2 — Builders de prompt por tipo de item

**Critério de aceite:** "Para REVIEW: prompt contém literal `'Revisar PR #<N>: <URL>'` + instrução `'Abra a PR, copie a Seção 🎯 Validação do body, cole no GitHub Copilot, e decida merge.'`"

**Gatilho:**
1. Na tab Fila, localize um card sob `🔀 Review (N)` (se houver). Se não houver REVIEW visível, pode pular este item — sem PR aberta no momento, REVIEW não aparece (estado correto da fila).
2. Clique no card. Painel de detalhe abre embaixo com botão `✕ Fechar`.

**Resultado esperado:**
- O bloco "Prompt (clipboard-ready)" mostra **exatamente** o formato:
  ```
  Revisar PR #<N>: <URL>

  Abra a PR, copie a Seção 🎯 Validação do body, cole no GitHub Copilot, e decida merge.
  ```
  (`<N>` e `<URL>` são valores reais).
- O ícone de copiar (canto superior direito do `st.code`) copia o texto para o clipboard.

**Sinal de falha:**
- Texto difere do formato literal acima.
- Aparece `<N>` ou `<URL>` literais (não substituídos).
- Botão de copiar do `st.code` ausente.

---

**Critério de aceite:** "Para STALE_BRANCH: prompt contém literal `'Branch <NAME> parada há <DAYS> dias sem PR aberta.'` + 3 opções enumeradas."

**Gatilho:**
1. Na tab Fila, localize um card sob `🌱 Stale branches (N)`. Se nenhuma branch parada existir, criar artificialmente é fora do escopo — pular.
2. Clique no card.

**Resultado esperado:**
- Bloco "Prompt (clipboard-ready)" mostra:
  ```
  Branch <name> parada há <N> dias sem PR aberta.

  Decida:
  (a) trabalho concluído sem PR — abrir PR via interface do GitHub
  (b) abandonado — `git push origin --delete <name>`
  (c) bloqueado — resgatar contexto e seguir
  ```
- `<name>` e `<N>` substituídos por valores reais.
- Três opções enumeradas `(a)`, `(b)`, `(c)` em linhas separadas.

**Sinal de falha:**
- Faltar uma das 3 opções.
- Comando `git push origin --delete` sem o nome da branch substituído.
- Texto livre em vez de formato enumerado.

---

## Épico W-PROTO-FILA-3 — Auto-regulação básica (alerta visual)

> Critérios em [`docs/process/workflow/ROADMAP.md`](workflow/ROADMAP.md), seção `#### ÉPICO W-PROTO-FILA-3`.

### 3.1 — Badge de contagem na sidebar

**Critério de aceite:** "Sidebar exibe `📋 Fila: <N>/20` com `N = len(detect_all_items(state))`; cor verde se N < 15, amarelo se 15 ≤ N < 20, vermelho se N ≥ 20."

**Gatilho:**
1. (App rodando.) Olhe a sidebar.

**Resultado esperado:**
- Bloco com fundo colorido contendo texto exatamente: `📋 Fila: <N>/20` (ou `📋 Fila: 0/20 — sem itens` quando vazio).
- Cor segue:
  - Fundo **verde claro** (`#d4edda`) se N < 15.
  - Fundo **amarelo claro** (`#fff3cd`) se 15 ≤ N < 20.
  - Fundo **vermelho claro** (`#f8d7da`) se N ≥ 20.
- Bloco aparece tanto na tab Fila quanto na tab Kanban (sidebar é compartilhada).

**Sinal de falha:**
- Bloco ausente.
- N não bate com o total de cards na tab Fila.
- Cor não muda quando N cruza 15 ou 20.

---

### 3.2 — Banner de alerta na tab da fila quando OVER_LIMIT

**Critério de aceite:** "Banner aparece quando `len(items) >= 20`; ausente quando `< 20`."

**Gatilho:**
1. (App rodando.) Verifique se a fila tem ≥ 20 itens (badge da sidebar deve estar vermelho).
2. Se sim, olhe o topo da tab Fila.

**Resultado esperado:**
- Quando N ≥ 20: aparece banner amarelo (Streamlit `st.warning`) **acima** dos cabeçalhos por tipo, com texto exatamente: `⚠️ Fila com <N> itens (limite alvo: 20). Considere fechar itens antes de iniciar novos. No MVP, o proponente vai pausar criação automaticamente.`
- Quando N < 20: banner ausente.
- Tab Kanban **não** mostra o banner (banner é específico da tab Fila).

**Sinal de falha:**
- Banner ausente quando deveria aparecer.
- Banner persiste quando N < 20.
- Banner aparece também no Kanban.

---

## Épico W-PROTO-FILA-4 — Configuração persistente + sidebar como painel

> Critérios em [`docs/process/workflow/ROADMAP.md`](workflow/ROADMAP.md), seção `#### ÉPICO W-PROTO-FILA-4`.

### 4.1 — Persistência de preferências (JSON local)

**Critério de aceite:** "`load_preferences(repo_root: Path) -> Preferences` retorna defaults quando arquivo ausente, **sem warning ou log** (ausência é estado normal)."

**Gatilho:**
1. A partir da raiz do repo:
   ```bash
   ls tools/workflow_platform/.preferences.json 2>&1
   ```
2. Se o arquivo existir, mova-o temporariamente:
   ```bash
   mv tools/workflow_platform/.preferences.json tools/workflow_platform/.preferences.json.bak
   ```
3. Cole:
   ```bash
   python -c "from tools.workflow_platform.preferences import load_preferences; from pathlib import Path; print(load_preferences(Path('.')))"
   ```

**Resultado esperado:**
- Saída exatamente: `Preferences(visible_roadmaps=None, stale_branch_threshold_days=7)`.
- Nenhum warning ou stack trace.

**Sinal de falha:**
- Stack trace ou erro.
- Saída inclui valores diferentes dos defaults.
- Aparece um warning (mesmo silencioso).

---

### 4.2 — Filtro por ROADMAP no caller

**Critério de aceite:** "`apply_visibility_filter(roadmaps, prefs, all_configured_paths)` retorna `roadmaps` inalterada quando `prefs.visible_roadmaps is None`."

**Gatilho:**
1. (App rodando.) Olhe a sidebar — todos os checkboxes "👁️ Visíveis" devem estar marcados (estado default = todos).
2. Verifique se o kanban e a fila mostram itens de todos os ROADMAPs configurados (Core, Workflow, Revelar, Ensaio, Prisma Verbal, Produtor Científico).

**Resultado esperado:**
- 6 checkboxes marcados na sidebar.
- Kanban mostra épicos de múltiplos ROADMAPs (verificável pelos prefixos dos IDs: W-PROTO-, E-POC-, etc.).

**Sinal de falha:**
- Apenas 1 ou alguns checkboxes marcados quando deveria ser todos.
- Kanban filtra prematuramente.

---

**Critério de aceite:** "Lista `prefs.visible_roadmaps` vazia (`[]`) ⇒ retorna `[]` (operador desmarcou tudo; kanban/fila ficam vazios — estado válido, não erro)."

**Gatilho:**
1. (App rodando.) Na sidebar, clique para desmarcar **todos** os checkboxes "👁️ Visíveis".

**Resultado esperado:**
- Após cada desmarcar, a página re-renderiza.
- Após o último desmarcar: kanban fica vazio (8 colunas, todas com "_(vazio)_") e fila mostra "Sem itens na fila — nada esperando ação no momento."
- Nenhum traceback.
- Arquivo `tools/workflow_platform/.preferences.json` agora existe com `"visible_roadmaps": []`.

**Sinal de falha:**
- Erro ao desmarcar último checkbox.
- Estado não persiste em `.preferences.json`.
- Kanban/fila renderizam itens mesmo com tudo desmarcado.

**Ação após validar:** marque ao menos um checkbox de volta antes de continuar.

---

### 4.3 — Sidebar como painel de filtros + status

**Critério de aceite:** "Sidebar mostra um `st.checkbox` por ROADMAP do `config.yaml`, com label retornado por `_label_for_roadmap(path)` (ex.: `products/revelar/ROADMAP.md` → 'Revelar'; `docs/ROADMAP.md` → 'Core'; `docs/process/workflow/ROADMAP.md` → 'Workflow')."

**Gatilho:**
1. (App rodando.) Olhe a sidebar, seção "👁️ Visíveis".

**Resultado esperado:**
- Labels visíveis incluem **literalmente**: "Core", "Workflow", "Revelar", "Ensaio", "Prisma Verbal", "Produtor Cientifico" (com a contagem de épicos entre parênteses).
- Cada label tem checkbox próprio (6 ao todo).

**Sinal de falha:**
- Algum label vem como path bruto (ex.: `docs/ROADMAP.md`).
- Hífen aparecendo em "Prisma-Verbal" em vez de espaço.
- Nomes em caixa baixa.

---

**Critério de aceite:** "Botão '⚠️ Avisos (N)' abre `st.dialog('Avisos do parser')` com lista de warnings agrupados por arquivo."

**Gatilho:**
1. (App rodando.) Na sidebar, clique no botão "⚠️ Avisos (N)" (rodapé da sidebar).

**Resultado esperado:**
- Modal Streamlit aparece sobre a página com título "Avisos do parser".
- Conteúdo: ou "sem avisos" (caption) ou lista markdown com nome do arquivo + mensagem por linha.
- Botão "Fechar" fecha o modal.

**Sinal de falha:**
- Clique não abre modal (ou abre expander dentro da sidebar — fallback documentado, mas é decisão consciente).
- Modal sem título correto.
- Modal não fecha após clique em "Fechar".

---

## Comportamentos "não deve" (regressão)

### Não deve: chat embutido na plataforma

**Critério (FILA-2 §"Fora do escopo"):** "Chat embutido na plataforma (sessão de Claude Code dentro do app) — escopo MVP."

**Gatilho:** (App rodando.) Clique em qualquer card da fila e verifique o painel de detalhe.

**Resultado esperado:**
- Painel mostra **prompt clipboard-ready** (texto em `st.code`) — copiar para outra ferramenta é o fluxo declarado.
- Não há campo de input de chat, botão "Enviar" para LLM, nem janela de diálogo embutida.

**Sinal de falha:**
- Aparecer interface de chat dentro do app.

---

### Não deve: pausa dura em OVER_LIMIT

**Critério (FILA-3 §"Fora do escopo"):** "Pausa dura (gatilho que impede detecção de novos itens) — escopo MVP quando proponente existe."

**Gatilho:** (App rodando, fila em OVER_LIMIT se possível.) Clique em qualquer card da fila.

**Resultado esperado:**
- Banner OVER_LIMIT aparece (FILA-3.2) mas **não bloqueia** o clique.
- Painel de detalhe abre normalmente.
- Botão de copiar prompt funciona.

**Sinal de falha:**
- Banner desabilita interação.
- Botão de card fica greyed out.

---

### Não deve: edição/cancelamento manual de itens da fila

**Critério (FILA-2 §"Fora do escopo"):** "Edição/cancelamento manual de itens da fila — fila é derivada, mexer no estado-do-mundo (ROADMAP, branch) já basta."

**Gatilho:** (App rodando.) Olhe os cards da fila.

**Resultado esperado:**
- Nenhum card tem botão "✕ Excluir", "Cancelar item" ou "Editar".
- Painel de detalhe tem botão "✕ Fechar" (fecha o painel, não cancela o item).

**Sinal de falha:**
- Aparecer botão de exclusão/edição direto no card.

---

## Critérios de aprovação

Aprove o merge quando **todos**:

- [ ] Cada roteiro acima rodou e o **Resultado esperado** foi observado literalmente
- [ ] Nenhum **Sinal de falha** ocorreu em nenhum roteiro
- [ ] Comportamentos "não deve" do ROADMAP foram confirmados (não ocorreram)
- [ ] `pytest tests/tools/workflow_platform/` retorna 120 passed, 0 failed
- [ ] Tabela do Copilot na PR (Seção 🎯) sem ❌ sem justificativa

**Se algum critério falhar:** devolver com feedback para nova rodada autônoma (Claude Code Web) ou abrir sessão estratégica externa se exigir decisão arquitetural.

---

**Ver também:**
- Skill da RTE → [skills/rte/skill.md](../../skills/rte/skill.md)
- Validação geral do modo autônomo → [docs/process/autonomous/delivery.md](autonomous/delivery.md)
