# Validação Manual do Milestone PROTO-WORKFLOW-PLATAFORMA — Plataforma de Workflow

> **📌 Público:** dev (revisor da PR final).
> **📌 Quando usar:** ao receber notificação da sessão autônoma de "Milestone pronto", rodar este checklist antes de mergear.
> **📌 Princípio anti-viés:** valida critérios de aceite do ROADMAP, não a implementação. Sem instruções de "abrir código", "checar diff" ou "inspecionar log".

---

## Preparação do ambiente

```bash
# 1. Checkout da branch
git fetch origin
git checkout claude/implement-workflow-prototype-BtiaJ
git pull origin claude/implement-workflow-prototype-BtiaJ

# 2. Ambiente
source venv/bin/activate
pip install -r requirements.txt
```

**Pré-condição:** Python 3.11+. Nenhuma chave de API é necessária — a plataforma só lê markdown local.

---

## Testes unitários (determinísticos)

```bash
pytest tests/tools/workflow_platform/ -v
```

**Esperado:** 29 testes passam. Se algum falha, parar e reportar.

---

## Épico W-PROTO-PLAT-1 — Scaffold da plataforma

> Critérios em [docs/process/workflow/ROADMAP.md](ROADMAP.md), seção W-PROTO-PLAT-1.

### 1.1 — App Streamlit com configuração, modelo e parser

**Critério de aceite:** Deve iniciar com `streamlit run tools/workflow_platform/app.py` a partir do repo raiz sem erros.

**Gatilho:**
1. No terminal, a partir do repo raiz, execute:
   ```
   streamlit run tools/workflow_platform/app.py
   ```
2. Abra `http://localhost:8501` no navegador.

**Resultado esperado:**
- Header `🧭 Plataforma de Workflow` aparece no topo da página.
- Sidebar lista exatamente 6 ROADMAPs: `docs/ROADMAP.md`, `docs/process/workflow/ROADMAP.md`, `products/revelar/ROADMAP.md`, `products/ensaio/ROADMAP.md`, `products/prisma-verbal/ROADMAP.md`, `products/produtor-cientifico/ROADMAP.md`.
- Sidebar mostra contagem total `<N> épicos · <M> milestones`.

**Sinal de falha:**
- Stack trace na página, app não carrega, ou contagem total = 0 épicos.

---

**Critério de aceite:** Deve ler ROADMAPs configurados sem travar se algum estiver ausente ou malformado (registra warning no UI e segue).

**Gatilho:**
1. Edite temporariamente `tools/workflow_platform/config.yaml` adicionando uma linha falsa em `roadmaps:`:
   ```
     - docs/ARQUIVO_INEXISTENTE.md
   ```
2. Volte ao navegador, clique em `🔄 Recarregar` na sidebar.
3. Expanda o painel `Avisos do parser` na sidebar.

**Resultado esperado:**
- Painel `Avisos do parser` lista uma entrada contendo `não encontrado` para `ARQUIVO_INEXISTENTE.md`.
- O resto da plataforma continua renderizando normalmente (cards dos demais ROADMAPs visíveis).

**Sinal de falha:**
- Página em branco, stack trace, ou app trava sem renderizar nada.

> Reverter a edição em `config.yaml` antes de seguir.

---

**Critério de aceite:** Parser deve reconhecer os 8 estados via emoji prefix do campo `**Status:** <emoji> ...` e extrair PR URL do estado `🔀 Em revisão — PR #N (URL)`.

**Gatilho:**
1. Na plataforma, role o kanban e localize um card em `🔀 Em revisão`.
2. Clique no card.

**Resultado esperado:**
- Painel de detalhe abre com link clicável para a PR no GitHub (ex.: `https://github.com/gmaiarviana/paper-agent/pull/<N>`).

**Sinal de falha:**
- Aviso `PR não declarada no ROADMAP`, ou link para URL malformada.

---

## Épico W-PROTO-PLAT-2 — Kanban completo

> Critérios em [docs/process/workflow/ROADMAP.md](ROADMAP.md), seção W-PROTO-PLAT-2.

### 2.1 — Kanban de estados por milestone

**Critério de aceite:** Deve exibir todas as 8 colunas na ordem `🌱 → 🧭 → 📐 → 📋 → 🔍 → 🏗️ → 🔀 → ✅`.

**Gatilho:**
1. Abra a página principal da plataforma.

**Resultado esperado:**
- Oito colunas lado a lado, com cabeçalhos exatamente na ordem: `🌱 Visão`, `🧭 Jornada alinhada`, `📐 Esboçados`, `📋 Critérios`, `🔍 Detalhes`, `🏗️ Em andamento`, `🔀 Em revisão`, `✅ Implementado`.

**Sinal de falha:**
- Colunas em ordem diferente, coluna faltando, ou ordem invertida.

---

**Critério de aceite:** Deve agrupar cards por milestone dentro de cada coluna; épicos com `milestone_id=None` ficam num grupo final "Sem milestone".

**Gatilho:**
1. Inspecione visualmente a coluna `🔍 Detalhes`.

**Resultado esperado:**
- Dentro da coluna, vê-se subgrupo titulado `PROTO-WORKFLOW-PLATAFORMA` contendo `W-PROTO-PLAT-1`, `W-PROTO-PLAT-2`, `W-PROTO-PLAT-3`, `W-PROTO-PLAT-4`.
- Se houver épicos do Revelar (sem campo `**Milestone:**`) em alguma coluna, eles aparecem sob subgrupo `Sem milestone` no fim da coluna.

**Sinal de falha:**
- Cards do mesmo milestone espalhados sem agrupamento, ou ausência da rotulação por milestone.

---

**Critério de aceite:** Cada card deve exibir: `id`, `title`, e `milestone_id` (ou "Sem milestone").

**Gatilho:**
1. Inspecione qualquer card no kanban.

**Resultado esperado:**
- Card exibe (em duas linhas): id em destaque (ex.: `**W-PROTO-PLAT-1**`) e o título do épico (ex.: `Scaffold da plataforma`); o milestone aparece no cabeçalho do subgrupo logo acima do card.

**Sinal de falha:**
- Card sem id, sem título, ou sem indicação de milestone (próprio ou do subgrupo).

---

**Critério de aceite:** Deve consolidar épicos de todos os ROADMAPs configurados numa única view.

**Gatilho:**
1. Procure no kanban por épicos com prefixos diferentes: `W-` (workflow), `E-` (ensaio), `C-ENSAIO-` (core).

**Resultado esperado:**
- Pelo menos um card de cada prefixo aparece em alguma coluna.

**Sinal de falha:**
- Apenas épicos de um único ROADMAP aparecem.

---

**Critério de aceite:** Deve atualizar ao recarregar a página — botão "🔄 Recarregar" na sidebar invalida `st.session_state` e re-parseia.

**Gatilho:**
1. Em outro terminal, edite manualmente `docs/process/workflow/ROADMAP.md`, mude `**Status:**` de qualquer épico em `🔍` para `📋 Critérios definidos`.
2. Salve. Volte ao navegador.
3. Clique no botão `🔄 Recarregar` na sidebar.

**Resultado esperado:**
- O épico editado some da coluna `🔍 Detalhes` e aparece na coluna `📋 Critérios`.

**Sinal de falha:**
- Coluna de origem ainda mostra o épico após o reload.

> Reverter a edição em `ROADMAP.md` antes de seguir.

---

**Critério de aceite:** Card clicado guarda `selected_epic_id` em `st.session_state` e abre painel de detalhe lateral.

**Gatilho:**
1. Clique no card `W-PROTO-PLAT-1`.

**Resultado esperado:**
- **Acima** do kanban (no topo da página, dentro de um container com borda), abre seção com cabeçalho `## W-PROTO-PLAT-1 — Scaffold da plataforma` e legenda `Estado: 🔍 · Milestone: PROTO-WORKFLOW-PLATAFORMA`.

**Sinal de falha:**
- Nada acontece ao clicar, ou painel não traz cabeçalho com id/título/milestone, **ou** o painel só aparece muito abaixo do kanban (deveria aparecer no topo da página, acima do kanban).

---

**Critério de aceite (regressão da plataforma):** o painel de detalhe deve ser visível sem scroll após o clique.

**Gatilho:**
1. Role a página até o topo (Ctrl+Home).
2. Clique em um card qualquer no kanban.

**Resultado esperado:**
- Após o clique, sem scrollar, o painel de detalhe está visível imediatamente acima do kanban (com borda, header `## <ID> — <título>` e botão `✕ Fechar` no canto superior direito).
- Botão `✕ Fechar` limpa a seleção e oculta o painel.

**Sinal de falha:**
- Painel só aparece se o usuário scrollar para baixo (defeito reportado em validação anterior).

---

## Épico W-PROTO-PLAT-3 — Ações de implementação

> Critérios em [docs/process/workflow/ROADMAP.md](ROADMAP.md), seção W-PROTO-PLAT-3.

### 3.1 — Dispatch para épicos em 🔍

**Critério de aceite:** Deve exibir prompt de dispatch clipboard-ready ao selecionar épico em `🔍`. O prompt deve referenciar o `milestone_id` (não o `epic.id`) e usar linguagem natural (ex.: ``"implementa o `<MILESTONE_ID>`"``).

**Gatilho:**
1. Clique no card `W-PROTO-PLAT-1`.

**Resultado esperado:**
- Painel de detalhe exibe bloco de código com texto começando exatamente por `implementa o PROTO-WORKFLOW-PLATAFORMA`.
- O bloco tem ícone de cópia no canto superior direito (padrão do `st.code`).

**Sinal de falha:**
- Texto contém o id do épico (`W-PROTO-PLAT-1`), ou bloco de código não aparece.

---

**Critério de aceite:** Se algum épico do mesmo milestone está em `🌱`/`🧭`/`📐`/`📋`, listar esses ids no prompt como "PM skill refinará: <ids>".

**Gatilho:**
1. Edite manualmente `docs/process/workflow/ROADMAP.md` mudando o `**Status:**` de `W-PROTO-PLAT-2` de `🔍 Detalhes definidos` para `📋 Critérios definidos`.
2. Volte ao navegador, clique em `🔄 Recarregar`.
3. Clique no card `W-PROTO-PLAT-1` (ainda em `🔍`).

**Resultado esperado:**
- O bloco de prompt agora inclui uma seção `Nota: PM skill refinará os épicos abaixo (→ 🔍) antes da EM rodar:` seguida de um item `- W-PROTO-PLAT-2`.

**Sinal de falha:**
- Prompt não menciona `PM skill` nem `W-PROTO-PLAT-2`.

> Reverter a edição em `ROADMAP.md` antes de seguir.

---

**Critério de aceite:** Se algum épico do mesmo milestone está em `🏗️`/`🔀`/`✅`, exibir alerta visual e desabilitar botão de copy (sem prompt).

**Gatilho:**
1. Edite `docs/process/workflow/ROADMAP.md` mudando o `**Status:**` de `W-PROTO-PLAT-2` de `🔍` para `🏗️ Em andamento`.
2. Recarregue na plataforma e clique no card `W-PROTO-PLAT-1`.

**Resultado esperado:**
- Painel exibe aviso amarelo (`st.warning`) com texto `milestone em execução/concluído — dispatch não recomendado` e cita `W-PROTO-PLAT-2`.
- Não aparece bloco `st.code` com prompt.

**Sinal de falha:**
- Prompt clipboard-ready ainda aparece para copy, ou não há aviso visível.

> Reverter a edição em `ROADMAP.md` antes de seguir.

---

### 3.2 — Status para 🏗️/🔀/✅

**Critério de aceite:** Para `🏗️`: exibe `epic.branch` como link `https://github.com/<owner>/<repo>/tree/<branch>`.

**Gatilho:**
1. Localize qualquer card em `🏗️ Em andamento` no kanban (se ausente, edite temporariamente um épico para esse estado e adicione campo `**Branch:** milestone/teste`; recarregue).
2. Clique no card.

**Resultado esperado:**
- Painel exibe linha `**Branch em andamento:** milestone/teste` com link clicável para `https://github.com/gmaiarviana/paper-agent/tree/milestone/teste`.

**Sinal de falha:**
- Linha não aparece, ou link aponta para URL diferente.

---

**Critério de aceite:** Para `🔀`: exibe link para `epic.pr_url` (ou monta URL a partir de `epic.pr_number`).

**Gatilho:**
1. Clique em qualquer card em `🔀 Em revisão` no kanban.

**Resultado esperado:**
- Painel exibe linha `**Em revisão:** PR #<N>` com link clicável para `https://github.com/gmaiarviana/paper-agent/pull/<N>`.

**Sinal de falha:**
- Aviso `PR não declarada no ROADMAP` aparecendo num card cujo `**Status:**` traz `PR #N`.

---

**Critério de aceite:** Para `✅`: exibe título e resumo (corpo do bloco do épico no ROADMAP, primeiros 500 chars) sem botões de ação.

**Gatilho:**
1. Clique em qualquer card em `✅ Implementado` (ex.: `W-POC-1`).

**Resultado esperado:**
- Painel exibe ícone de sucesso e bloco `Resumo do bloco:` com texto extraído do ROADMAP.
- Não aparece botão de cópia, prompt clipboard-ready, nem prompt de refinamento.

**Sinal de falha:**
- Botão de dispatch ou refinamento aparece para épico em `✅`.

---

## Épico W-PROTO-PLAT-4 — Direcionamento de refinamento

> Critérios em [docs/process/workflow/ROADMAP.md](ROADMAP.md), seção W-PROTO-PLAT-4.

### 4.1 — Próximo passo por estado pré-execução

**Critério de aceite:** Para `📋`: exibe "Próximo alvo: `🔍 Detalhes definidos` (apto ao fluxo autônomo). Checklist do alvo: [autonomous_readiness.md](../refinement/autonomous_readiness.md)."

**Gatilho:**
1. Clique em qualquer card em `📋 Critérios` (se nenhum visível, navegue por outros ROADMAPs onde houver).

**Resultado esperado:**
- Painel exibe caixa azul (`st.info`) com texto começando por `Próximo alvo: 🔍 Detalhes definidos (apto ao fluxo autônomo). Checklist do alvo: docs/process/refinement/autonomous_readiness.md.`.
- Logo abaixo, link para `docs/process/refinement/autonomous_readiness.md`.

**Sinal de falha:**
- Texto da info-box menciona `📋` como alvo, ou link aponta para outro arquivo.

---

**Critério de aceite:** Não deve listar arquivos para upload manual — refinamento é delegado à PM skill ou sessão estratégica.

**Gatilho:**
1. Inspecione o painel após clicar em qualquer card pré-execução (`🌱`/`🧭`/`📐`/`📋`).

**Resultado esperado:**
- Texto da guidance menciona `PM skill` e/ou `sessão estratégica` como caminho de refinamento.
- Nenhuma lista de arquivos para upload aparece.

**Sinal de falha:**
- Aparece UI tipo "anexar arquivos", "upload", ou lista de paths para o operador subir.

---

### 4.2 — Prompt de refinamento clipboard-ready

**Critério de aceite:** Deve gerar prompt incluindo `epic.id`, `epic.title`, `epic.state.name`, alvo, `epic.roadmap_path` e ponteiros para `planning_guidelines.md` e `starter.md`. Para épico em `📋`: prompt cita explicitamente `autonomous_readiness.md`.

**Gatilho:**
1. Clique em um card em `📋 Critérios` qualquer.

**Resultado esperado:**
- Bloco `st.code` exibe prompt iniciando por `Refinar o épico <ID> ("<título>") até 🔍 Detalhes definidos.` e contendo as três strings: `docs/process/refinement/planning_guidelines.md`, `docs/process/refinement/autonomous_readiness.md`, `docs/process/refinement/starter.md`.

**Sinal de falha:**
- Prompt não menciona `🔍`, ou falta um dos três caminhos.

---

**Critério de aceite:** Para épico em `🌱`/`🧭`/`📐`: prompt **não** menciona `autonomous_readiness.md` (o checklist só vale para o alvo `🔍`, atingido a partir de `📋`).

**Gatilho:**
1. Clique em um card em `📐 Esboçados` qualquer.

**Resultado esperado:**
- Bloco de código com prompt de refinamento, mas **sem** ocorrência de `autonomous_readiness.md`.

**Sinal de falha:**
- Prompt cita `autonomous_readiness.md`.

---

**Critério de aceite:** Para épicos em estados de execução (`🔍`/`🏗️`/`🔀`/`✅`): a UI não exibe o painel de refinamento.

**Gatilho:**
1. Clique em um card em `🔍 Detalhes`.

**Resultado esperado:**
- Aparece prompt de **dispatch** (W-PROTO-PLAT-3.1), não prompt de refinamento. Não há frase "Refinar o épico".

**Sinal de falha:**
- Texto "Refinar o épico" aparece para épico em `🔍`/`🏗️`/`🔀`/`✅`.

---

## Comportamentos "não deve" (regressão)

### Não deve: listar arquivos para upload manual

**Gatilho:** Clique em qualquer card pré-execução.

**Resultado esperado:** Painel só apresenta texto de guidance + prompt copy-paste. Nenhum elemento de upload visível.

**Sinal de falha:** Botão "Upload" ou lista de arquivos para anexar aparecendo no painel.

---

### Não deve: dispachar épico sem milestone

**Gatilho:** Localize um card cujo bloco do ROADMAP não tenha campo `**Milestone:**` (ex.: épicos do Revelar). Clique nele em estado `🔍` (se houver).

**Resultado esperado:** Aviso "épico sem milestone declarado — não pode ser despachado". Sem prompt de dispatch.

**Sinal de falha:** Prompt clipboard-ready aparece mesmo sem milestone declarado.

---

## Critérios de aprovação

Aprove o merge quando **todos**:

- [ ] Cada roteiro acima rodou e o **Resultado esperado** foi observado literalmente
- [ ] Nenhum **Sinal de falha** ocorreu em nenhum roteiro
- [ ] Comportamentos "não deve" do ROADMAP foram confirmados (não ocorreram)
- [ ] Tabela do Copilot na PR (Seção 🎯) sem ❌ sem justificativa

**Se algum critério falhar:** devolver com feedback para nova rodada autônoma ou trazer para fluxo manual.

---

**Ver também:**
- Skill da RTE → [skills/rte/skill.md](../../../skills/rte/skill.md)
- Validação geral do modo autônomo → [docs/process/autonomous/delivery.md](../autonomous/delivery.md)
