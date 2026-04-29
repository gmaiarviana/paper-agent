# Validação Local — PROTO-WORKFLOW-FAXINA

> **📌 Público:** dev (revisor da PR final).
> **📌 Arquivo rotativo:** sobrescrito a cada novo milestone. Histórico fica nas PRs mergeadas.
> **📌 Quando usar:** opcional, depois que o Copilot rodou na Seção 🎯 do body e você quer fazer uma checagem manual extra antes do merge. A Seção 🎯 da PR é a porta principal de revisão.
> **📌 Princípio anti-viés:** os roteiros abaixo só validam comportamento observável extraído dos critérios de aceite **PO ✅** do ROADMAP. Não há passos que peçam para você abrir código-fonte, rodar `git diff`, ou inspecionar logs internos do agente — esses checks já são feitos pelo Copilot na Seção 🎯 da PR.

---

## Preparação do ambiente

Este milestone é 100% faxina documental. Não há código que rode, não há aplicação para subir e não há testes unitários introduzidos. A "preparação" é só baixar a branch e usar `grep`/editor para inspeção visual.

```bash
# Baixar branch
git fetch origin
git checkout claude/proto-workflow-faxina-e4irl
git pull origin claude/proto-workflow-faxina-e4irl
```

Não há `pip install` nem `pytest` aplicável a este milestone (saldo de testes adicionados = 0).

---

## Testes unitários

Não aplicável — milestone é faxina documental, sem mudança de código.

---

## Épico W-PROTO-15 — Descontinuar fluxo manual / Cursor / Claude Web do desenho

### 15.1 — Reescrever `autonomous/overview.md` para fluxo único

**Critério de aceite:** arquivo descreve **um** fluxo (autônomo via Claude Code Web). Tabela "Fluxo Manual vs Autônomo" some. Seção "Use o Fluxo Manual (Cursor) quando..." some. Intro e §6 deixam de contrastar com fluxo manual. Estado `📋 Critérios definidos` é descrito como "passo intermediário até `🔍`" (não como "apto ao fluxo manual").

**Gatilho:**
```bash
grep -ni "fluxo manual\|cursor" docs/process/autonomous/overview.md
```

**Resultado esperado:** comando não imprime nenhuma linha (exit code não-zero do grep).

**Sinal de falha:** uma ou mais linhas aparecem no output. Cada linha indica menção residual à dicotomia.

### 15.2 — Reescrever §"Otimização do Workflow" em `planning_guidelines.md`

**Critério de aceite:** §"Otimização do Workflow: Usando Cursor para Análises" some; substituída por §"Modalidades de Refinamento" descrevendo três modalidades (Estratégico via Claude Code Web na branch; Estratégico via Claude Web em sessão externa; Tático via PM skill). Pipeline tripartite "Cursor escaneia → Claude Web refina → Cursor executa" desaparece.

**Gatilho:**
```bash
grep -ni "Otimização do Workflow.*Cursor\|prompts separados para Cursor\|apto ao fluxo manual" docs/process/refinement/planning_guidelines.md
grep -n "^### Modalidades de Refinamento" docs/process/refinement/planning_guidelines.md
```

**Resultado esperado:** primeiro comando não imprime linhas. Segundo comando imprime **exatamente uma linha** com `### Modalidades de Refinamento`.

**Sinal de falha:** primeiro comando imprime alguma linha; OU segundo retorna 0 linhas (a seção canônica não existe) ou múltiplas linhas (drift).

### 15.3 — Limpar `CONSTITUTION.md`

**Critério de aceite:** §"Cursor (Atualizador de Documentações)" some; §"Fluxos Disponíveis" reescrita como §"Requisitos de Refinamento". Glossário atualizado. 0 menções a "cursor" ou "fluxo manual" no arquivo.

**Gatilho:**
```bash
grep -ni "cursor\|fluxo manual" docs/CONSTITUTION.md
grep -n "Requisitos de Refinamento" docs/CONSTITUTION.md
```

**Resultado esperado:** primeiro comando não imprime linhas. Segundo imprime pelo menos 1 linha (cabeçalho da nova seção).

**Sinal de falha:** primeiro comando imprime alguma linha; OU segundo retorna 0.

### 15.4 — Limpar `implementation/overview.md` e `quality_rules.md`

**Critério de aceite:** ambos os arquivos perdem o rótulo "Cursor Background" e a contrastação com "fluxo manual". §"Validação Híbrida" do `overview.md` permanece intacta.

**Gatilho:**
```bash
grep -ni "Cursor Background\|fluxo manual" docs/process/implementation/overview.md docs/process/implementation/quality_rules.md
grep -n "Claude Code Web" docs/process/implementation/overview.md docs/process/implementation/quality_rules.md
```

**Resultado esperado:** primeiro comando não imprime linhas. Segundo imprime ≥3 linhas (cabeçalhos atualizados em ambos os arquivos).

**Sinal de falha:** primeiro comando imprime alguma linha.

### 15.5 — Limpar arquivos periféricos

**Critério de aceite:** menções residuais em `refinement/starter.md`, `refinement/overview.md`, `autonomous/delivery.md`, `skills/rte/skill.md`, `skills/rte/templates/delivery-report.md` removidas.

**Gatilho:**
```bash
grep -ni "fluxo manual\|via Cursor" docs/process/refinement/starter.md docs/process/refinement/overview.md docs/process/autonomous/delivery.md skills/rte/skill.md skills/rte/templates/delivery-report.md
```

**Resultado esperado:** comando não imprime nenhuma linha.

**Sinal de falha:** alguma linha aparece.

### 15.6 — Deletar `.cursorrules`

**Critério de aceite:** arquivo `.cursorrules` (60 linhas) apagado integralmente.

**Gatilho:**
```bash
ls .cursorrules
```

**Resultado esperado:** output literal contém `cannot access` ou `No such file or directory` (exit code 2).

**Sinal de falha:** o comando lista o arquivo (`.cursorrules` aparece no output).

### 15.7 — Atualizar `CLAUDE.md`, `docs/CONTEXT_INDEX.md`, `README.md`

**Critério de aceite:** referência cruzada a `.cursorrules` em CLAUDE.md removida; bullet "Fluxo manual (Cursor)" reescrito; CONTEXT_INDEX e README atualizados.

**Gatilho:**
```bash
grep -ni "cursor" CLAUDE.md docs/CONTEXT_INDEX.md README.md
```

**Resultado esperado:** comando não imprime nenhuma linha.

**Sinal de falha:** alguma linha aparece.

### 15.8 — Varredura final

**Critério de aceite:** varredura de todo `docs/`, `skills/`, `products/`, `core/`, `tools/`, `tests/`, `scripts/`, `CLAUDE.md`, `README.md` retorna 0 menções (com exceções: `ROADMAP.md` excluído por flag, `current_implementation.md` artefato de sessão).

**Gatilho:**
```bash
grep -rni "cursor\|fluxo manual" \
  --include="*.md" \
  --exclude-dir=.git \
  --exclude="ROADMAP.md" \
  --exclude="current_implementation.md" \
  docs/ skills/ products/ core/ tools/ tests/ scripts/ \
  CLAUDE.md README.md
```

**Resultado esperado:** comando não imprime nenhuma linha.

**Sinal de falha:** alguma linha fora das exceções declaradas aparece.

---

## Épico W-PROTO-16 — Consolidar template de "comandos de validação local"

### 16.1 — Eleger fonte canônica em `quality_rules.md`

**Critério de aceite:** §"Template de validação local" presente como cabeçalho navegável (`### Template de validação local`) em `quality_rules.md`. Bloco usa `.venv/` (com ponto). Passo 5 referencia `copilot-instructions.md §"Stacks por produto"` em vez de hardcodar `streamlit run`.

**Gatilho:**
```bash
grep -n "^### Template de validação local" docs/process/implementation/quality_rules.md
grep -n "\.venv/" docs/process/implementation/quality_rules.md
grep -n "Stacks por produto\|W-PROTO-14" docs/process/implementation/quality_rules.md
```

**Resultado esperado:** primeiro comando imprime **exatamente uma linha** com o cabeçalho. Segundo imprime ≥1 linha mencionando `.venv/` (passo 1 do template). Terceiro imprime ≥1 linha referenciando o épico W-PROTO-14 ou §"Stacks por produto".

**Sinal de falha:** primeiro retorna 0 ou >1 linha; segundo retorna 0 (template ainda usa `venv/` sem ponto); terceiro retorna 0 (passo 5 não referencia W-PROTO-14).

### 16.2 — Substituir cópias por referência

**Critério de aceite:** `docs/process/implementation/delivery.md` (bloco PowerShell em §"Validação Local"), `docs/process/autonomous/delivery.md` (§3 Comandos), `docs/process/implementation/overview.md` (exemplo simplificado) apontam para `quality_rules.md#template-de-validação-local` via link.

**Gatilho:**
```bash
grep -n "template-de-validação-local\|quality_rules.md#template" docs/process/implementation/delivery.md docs/process/autonomous/delivery.md docs/process/implementation/overview.md
```

**Resultado esperado:** comando imprime **3 linhas ou mais** — uma por arquivo, cada uma com o link para `#template-de-validação-local`.

**Sinal de falha:** retorna 0, 1 ou 2 linhas (algum arquivo não foi atualizado).

---

## Épico W-PROTO-13 — Faxina do `copilot-instructions.md` (concisão pra agente)

### 13.1 — §"Erros típicos e orientação" (no-op verificado)

**Critério de aceite:** seção não existe no arquivo (já apagada em refinamento anterior).

**Gatilho:**
```bash
grep -c "^## Erros típicos\|^### Erros típicos\|Erros típicos.*orientação" .github/copilot-instructions.md
```

**Resultado esperado:** comando imprime `0` (zero ocorrências do título de seção).

**Sinal de falha:** imprime número > 0.

### 13.2 — §"Checklist mínimo de POC do Ensaio" (no-op verificado)

**Critério de aceite:** seção não existe no arquivo.

**Gatilho:**
```bash
grep -c "Checklist mínimo.*POC\|POC do Ensaio" .github/copilot-instructions.md
```

**Resultado esperado:** comando imprime `0`.

**Sinal de falha:** imprime número > 0.

### 13.3 — Apagar §"Operação Windows / macOS / Linux"; manter §"Quando o dev disser 'deu erro'"

**Critério de aceite:** §"Operação Windows / macOS / Linux" apagada; §"Quando o dev disser 'deu erro'" intacta.

**Gatilho:**
```bash
grep -n "Operação Windows" .github/copilot-instructions.md
grep -n "Quando o dev disser" .github/copilot-instructions.md
```

**Resultado esperado:** primeiro comando não imprime linhas. Segundo imprime **exatamente uma linha** com o cabeçalho.

**Sinal de falha:** primeiro imprime alguma linha; OU segundo retorna 0 (seção mantida-por-spec foi acidentalmente apagada) ou múltiplas linhas (duplicada).

---

## Épico W-PROTO-10 — Centralizar definição dos estados de épico

### 10.1 — Bloco canônico único em `planning_guidelines.md`

**Critério de aceite:** uma única seção define os 8 estados (`🌱 Visão`, `🧭 Jornada alinhada`, `📐 Funcionalidades esboçadas`, `📋 Critérios definidos`, `🔍 Detalhes definidos`, `🏗️ Em andamento`, `🔀 Em revisão`, `✅ Implementado`) com nome, descrição curta, gatilho de transição e responsável. As outras duas seções dentro do mesmo arquivo são apagadas; referências internas usam âncora `#estados-de-épico`.

**Gatilho:**
```bash
grep -nE "^## Estados de Épico" docs/process/refinement/planning_guidelines.md
grep -cE '^- \*\*`🌱 Visão`\*\*' docs/process/refinement/planning_guidelines.md
```

**Resultado esperado:** primeiro comando imprime **exatamente uma linha** com `## Estados de Épico`. Segundo imprime `1` (uma única definição canônica de 🌱 Visão; sem duplicatas).

**Sinal de falha:** primeiro retorna 0 ou >1; segundo retorna >1 (drift entre cópias persiste) ou 0 (definição sumiu).

### 10.2 — Limpeza de drift cross-doc

**Critério de aceite:** `docs/CONSTITUTION.md`, `docs/process/refinement/starter.md`, `docs/process/autonomous/workflow.md`, `docs/process/workflow/vision.md`, `skills/pm/README.md` deixam de ter definição dos 8 estados (texto duplicado) e apontam pra fonte canônica via âncora.

**Gatilho:**
```bash
grep -rln "🌱.*🧭.*📐.*📋.*🔍.*🏗\|🌱 Visão.*🧭 Jornada" \
  --include="*.md" \
  --exclude-dir=.git \
  docs/ skills/
```

**Resultado esperado:** comando imprime **exatamente duas linhas** — `docs/process/refinement/planning_guidelines.md` (fonte canônica) e `docs/process/workflow/ROADMAP.md` (estrutura de dado do `EpicState` enum em W-PROTO-PLAT-1.1, exceção declarada).

**Sinal de falha:** retorna mais que 2 arquivos; OU retorna < 2 (a fonte canônica sumiu).

---

## Épico W-PROTO-11 — Faxina de `quality_rules.md`

### 11.1 — Apagar §"Verificação de Conflitos e Prevenção de Perda de Trabalho"

**Critério de aceite:** seção (140 linhas, tutorial defensivo de git pra Windows) apagada de `quality_rules.md`.

**Gatilho:**
```bash
grep -n "Verificação de Conflitos\|Prevenção de Perda" docs/process/implementation/quality_rules.md
```

**Resultado esperado:** comando não imprime nenhuma linha.

**Sinal de falha:** alguma linha aparece.

### 11.2 — Mover §"Diretrizes Aprendidas em Produção" para `products/revelar/docs/`

**Critério de aceite:** §"Diretrizes Aprendidas em Produção" apagada de `quality_rules.md` e migrada para arquivo novo `products/revelar/docs/llm_implementation_lessons.md` com >40 linhas.

**Gatilho:**
```bash
grep -n "Diretrizes Aprendidas em Produção\|Sistemas Conversacionais com LLMs" docs/process/implementation/quality_rules.md
ls -l products/revelar/docs/llm_implementation_lessons.md
wc -l products/revelar/docs/llm_implementation_lessons.md
```

**Resultado esperado:** primeiro comando não imprime linhas. Segundo lista o arquivo (não dá erro). Terceiro imprime número ≥ 40.

**Sinal de falha:** primeiro imprime alguma linha; OU segundo dá erro (`No such file`); OU terceiro retorna < 40.

### 11.3 — Reorganizar o que sobra em ordem coerente

**Critério de aceite:** após 11.1 + 11.2 + 15.4 + 16, `quality_rules.md` lê em ordem coerente (Princípios Gerais → Regras Anti-Redundância → Comandos e Validação → Exemplo de Fluxo Completo → Observações Finais), com ~180-200 linhas (tolerância: ±20).

**Gatilho:**
```bash
wc -l docs/process/implementation/quality_rules.md
grep -nE "^## " docs/process/implementation/quality_rules.md
```

**Resultado esperado:** primeiro comando imprime número entre **160 e 240** (target ~180-200, tolerância ampliada). Segundo imprime 5 linhas (5 cabeçalhos `##`) na ordem `Princípios Gerais → Regras Anti-Redundância → Comandos e Validação → Exemplo de Fluxo Completo → Observações Finais`.

**Sinal de falha:** primeiro retorna < 160 (faxina excessiva, conteúdo importante perdido) ou > 240 (faxina insuficiente); OU segundo retorna ordem diferente da declarada (ex.: "Comandos e Validação" antes de "Regras Anti-Redundância", ou seções extras como "Verificação de Conflitos" reaparecendo).

---

## Critérios de aprovação (checklist agregado)

- [ ] Cada roteiro acima rodou e o **Resultado esperado** foi observado literalmente
- [ ] Nenhum **Sinal de falha** ocorreu em nenhum roteiro
- [ ] Comportamentos "não deve" do ROADMAP foram confirmados (não ocorreram):
  - `.cursorrules` permanece no repo (15.6)
  - duplicação dos 8 estados em texto fora de `planning_guidelines.md` e `ROADMAP.md` (10.1/10.2)
  - bloco bash de validação local duplicado em `delivery.md` (`implementation` ou `autonomous`) — só link pra fonte canônica (16.2)
- [ ] Tabela do Copilot na PR (Seção 🎯) sem ❌ sem justificativa

**Se algum critério falhar:** devolver com feedback para nova rodada autônoma (Claude Code Web) ou abrir sessão estratégica externa (Claude Web) se exigir decisão arquitetural.

---

**Ver também:**
- Relatório completo do milestone → `docs/process/current_implementation.md`
- Como o dev valida (visão geral) → `docs/process/autonomous/delivery.md`
