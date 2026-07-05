# Validação Manual do Milestone PILOTO-WORKFLOW-UX (fatia W-PILOTO-UX-1 — migração Reflex)

> **📌 Público:** dev (revisor da PR final).
> **📌 Arquivo:** `docs/process/current_validation.md` — rotativo, sobrescrito a cada novo milestone. Histórico fica nas PRs mergeadas.
> **📌 Quando usar:** ao receber notificação de "Milestone pronto", rodar este checklist antes de mergear.
> **📌 Princípio anti-viés:** valida critérios de aceite do ROADMAP, não a implementação. Dev executa sem precisar abrir nenhum `.py`.

---

## Preparação do ambiente

```bash
# 1. Checkout da branch
git fetch origin
git checkout claude/docs-process-workflow-gk9hac
git pull origin claude/docs-process-workflow-gk9hac

# 2. Ambiente
source venv/bin/activate              # Linux/Mac
# .\venv\Scripts\Activate.ps1         # Windows
pip install -r requirements.txt        # reflex 0.9.0 já está pinado (Ensaio + plataforma)
```

**Pré-condição:** `git fetch origin` funcional (a fila usa `git fetch origin --prune` ao carregar). `ANTHROPIC_API_KEY` não é exigida — milestone é plataforma + lógica determinística.

**Mudança de stack:** a plataforma agora roda em **Reflex**, não Streamlit. Não use mais `streamlit run tools/workflow_platform/app.py` (esse arquivo foi removido).

---

## Testes unitários (determinísticos)

```bash
pytest tests/tools/workflow_platform/ -v
```

**Esperado:** 135 testes passando, 0 falhas, 0 erros, 0 skips. Se algum falhar, parar e reportar — não seguir para a validação manual.

---

## Épico W-PILOTO-UX-1 — Migração da plataforma para Reflex

> Critérios em [`docs/process/workflow/ROADMAP.md`](workflow/ROADMAP.md), seção `#### ÉPICO W-PILOTO-UX-1`.

### Subir a plataforma

```bash
cd tools/workflow_platform
reflex run
# aguarde "App running at: http://localhost:3001/"
```

Abra `http://localhost:3001/` no navegador. (Portas 3001/8001 são distintas das do Ensaio, 3000/8000 — as duas apps coexistem.)

> **⚠️ Gotcha de execução — suba SEMPRE com `reflex run` (console script), NÃO com
> `python -m reflex run`.** A partir de `tools/workflow_platform`, `python -m reflex
> run` coloca o cwd em `sys.path[0]`, e o pacote local `queue/` sombreia o módulo
> `queue` da stdlib (que o `multiprocessing` importa) → o compile quebra com
> `ImportError: cannot import name 'Empty' from 'queue'`. O console script `reflex
> run` usa o dir do Scripts como `sys.path[0]` e não sombreia → sobe normal.

> **📝 Nota de operação — `reflex run` muta a working tree.** Ao subir, o reflex
> **remove** o arquivo trackeado `tools/workflow_platform/__init__.py` (warning
> "Removing __init__.py file in the app root directory") e **gera** `.gitignore` e
> `requirements.txt` na pasta do app. Impacto funcional nenhum (namespace packages
> absorvem a ausência do `__init__.py`; a suíte segue verde). Mas deixa a working
> tree suja — depois de rodar, restaure com
> `git checkout tools/workflow_platform/__init__.py` e **não commite** os dois
> arquivos gerados pelo reflex (o `.gitignore` raiz já os ignora).

### 1.1 — Esqueleto Reflex + estado no backend

**Critério:** "Deve subir via `reflex run` carregando `config.yaml`, ROADMAPs e preferences sem erro. O estado da UI (aba, seleção, filtros) deve viver em `rx.State`, não em `st.session_state`."

**Verificar:**
- [ ] `reflex run` sobe sem erro e serve em `http://localhost:3001/`.
- [ ] A página carrega o título "🧭 Plataforma de Workflow", a sidebar de ROADMAPs visíveis e as abas Fila/Kanban.
- [ ] Trocar de aba e selecionar itens não recarrega a página inteira (estado no backend).

### 1.2 — Porte da aba Fila

**Critério:** "Para um mesmo estado-do-mundo, deve listar os mesmos itens da versão Streamlit (mesma saída de `detect_all`). Selecionar um item deve exibir detalhe + ação copiável (prompt clipboard-ready). Deve ser a aba default."

**Verificar:**
- [ ] A aba **Fila** é a default ao abrir.
- [ ] Os itens aparecem agrupados por tipo (Dispatch, Review, Refine, Cleanup, Stale branches) com contagem por grupo.
- [ ] Se houver ≥ 20 itens, aparece o badge de carga vermelho (`n/20`) na sidebar + banner de OVER_LIMIT no topo.
- [ ] Clicar num card abre o painel de detalhe (rodapé) com o ponteiro (PR/Branch/Milestone/Épico) e o **Prompt (clipboard-ready)** + botão "📋 Copiar".
- [ ] O botão "📋 Copiar" copia o prompt para a área de transferência.

### 1.3 — Porte da aba Kanban

**Critério:** "Deve exibir as 8 colunas (🌱→✅) consolidando épicos de todos os ROADMAPs, agrupados por milestone. Selecionar um épico deve exibir o painel com as ações contextuais por estado."

**Verificar:**
- [ ] A aba **Kanban** mostra 8 colunas (🌱 Visão → ✅ Implementado) com contagem por coluna.
- [ ] Dentro de cada coluna, os cards estão agrupados por milestone (e "Sem milestone" ao final quando aplicável).
- [ ] Clicar num card 🔍 mostra o prompt de dispatch; num card pré-execução (🌱/🧭/📐/📋) mostra guidance + prompt de refinamento; em 🏗️/🔀 mostra link para branch/PR; em ✅ mostra o resumo.

### 1.4 — Paridade funcional + retirada do Streamlit

**Critério:** "Preferências (`.preferences.json`), filtro por ROADMAP e badge de carga devem ler/gravar e renderizar com paridade. `app.py` e `views/*` Streamlit removidos; `grep -rl streamlit tools/workflow_platform/` → vazio. `.web/` no `.gitignore`."

**Verificar:**
```bash
# nenhum módulo da plataforma IMPORTA Streamlit (grep de import, não substring):
grep -rnE '^\s*(import streamlit|from streamlit)' tools/workflow_platform/   # → vazio

# a linha do Revelar PERMANECE (não é da plataforma):
grep -n "streamlit" requirements.txt            # streamlit>=1.30.0   # Revelar

# build do Reflex ignorado:
git check-ignore tools/workflow_platform/.web
```
- [ ] O grep de import acima não retorna nada. (Menções remanescentes a
  "Streamlit" em `tools/workflow_platform/` são apenas referências históricas em
  docstrings da migração — não são imports.)
- [ ] A linha `streamlit>=1.30.0   # Revelar` **continua** no `requirements.txt` (remover quebraria o Revelar).
- [ ] Na sidebar, marcar/desmarcar um ROADMAP filtra a fila e o kanban; o estado persiste após recarregar a página (gravado em `tools/workflow_platform/.preferences.json`, git-ignored).

---

## 🎯 Validação (copie tudo abaixo e envie ao Copilot)

Você é revisor técnico desta PR. Valide o diff (`main...HEAD`) contra os critérios abaixo. Para cada critério: ✅ (atende), ⚠️ (atende, mas há risco com cenário de falha real identificável — descreva a sessão que quebra), ❌ (não atende — aponte arquivo/linha). Observações de estilo sem cenário de falha → "Riscos adicionais (baixa prioridade)", não ⚠️ na tabela. Reporte em markdown.

### Contexto
- Milestone: PILOTO-WORKFLOW-UX — reconstruir o cockpit em Reflex. **Esta PR entrega só a fatia W-PILOTO-UX-1** (migração Reflex, fundação); UX-2/3/4 dependem desta mergear e vêm depois.
- Decisão de stack: ADR 001 do workflow (Streamlit → Reflex). Miolo stack-independente preservado.

### Critérios de aceite

**1.1 — Esqueleto Reflex + estado no backend:**
1. `reflex run` (de `tools/workflow_platform/`) sobe carregando `config.yaml`, ROADMAPs e preferences sem erro.
2. Estado da UI (aba ativa, seleção, filtros) vive em `rx.State` (`web/state.py::PlatformState`), não em `st.session_state`.
3. O miolo (`parser`, `models`, `config_loader`, `preferences`, `queue/*`, `prompts/*`) é importado **sem modificação de comportamento**. Exceção: `queue/load.py` — atualização de referência em docstring (`views/kanban.py` → `presenters.py`), sem mudança de comportamento.
4. Nenhuma lógica de detecção/parse/prompt nova — só a camada de view/estado migra.

**1.2 — Porte da aba Fila:**
1. A lista renderizada reusa `queue.detect.detect_all_items` (mesma saída da versão Streamlit) — paridade por construção.
2. Selecionar um item exibe detalhe + prompt clipboard-ready via `prompts.queue_item.build_prompt_for_item` (reusado).
3. Fila é a aba default; painel de detalhe no rodapé (paridade de posição — reposicionamento é UX-2).

**1.3 — Porte da aba Kanban:**
1. 8 colunas por estado (🌱→✅), épicos agrupados por milestone via `presenters.group_by_milestone` (reuso).
2. Ações contextuais por estado reusam `build_dispatch_prompt`/`build_refinement_prompt` — sem lógica nova.

**1.4 — Paridade + retirada do Streamlit:**
1. `app.py` e `views/*` Streamlit removidos; nenhum import de Streamlit na plataforma (`grep -rnE '^\s*(import streamlit|from streamlit)' tools/workflow_platform/` → vazio). Menções remanescentes a "Streamlit" são referências históricas em docstrings, não imports.
2. A linha `streamlit>=1.30.0` do `requirements.txt` **permanece** (é do Revelar — removê-la quebraria o Revelar).
3. `tools/workflow_platform/.web/` está no `.gitignore`.
4. Preferências (`.preferences.json`), filtro por ROADMAP e badge de carga (`<n>/20` + banner OVER_LIMIT) com paridade à versão Streamlit.

### Comportamentos "não deve"
- **Não deve** alterar a lógica de detecção/parse/prompt — só a view migra.
- **Não deve** implementar o clique-dispara-execução (é `PILOTO-WORKFLOW-CANAL-UNICO`).
- **Não deve** remover a linha `streamlit` do `requirements.txt` (é do Revelar).

### Formato de retorno esperado
- Tabela `Critério | Status | Observação`
- Seção "Riscos adicionais (baixa prioridade)"
