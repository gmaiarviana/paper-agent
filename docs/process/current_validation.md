# Validação Manual do Milestone PROTO-WORKFLOW-COPILOT-STACK — Reflex no fluxo do Copilot

> **📌 Público:** dev (revisor da PR final).
> **📌 Arquivo rotativo:** sobrescrito a cada novo milestone. Histórico fica nas PRs mergeadas.
> **📌 Quando usar:** após receber a notificação "Milestone pronto", antes de mergear.
> **📌 Princípio anti-viés:** este arquivo valida critérios de aceite do ROADMAP via observação direta do arquivo entregue (`.github/copilot-instructions.md`) — **sem instruções de "abrir código-fonte do produto", "rodar app", "checar log de prompt"**. Esta entrega é uma reescrita de doc operacional; a observação se faz lendo a doc resultante e rodando os greps do ROADMAP.

---

## Preparação do ambiente

```bash
# 1. Checkout da branch
git fetch origin
git checkout claude/implement-copilot-stack-gSUxf
git pull origin claude/implement-copilot-stack-gSUxf

# 2. Ambiente (não há mudança de deps neste milestone — opcional)
source .venv/bin/activate              # Linux/Mac
# .\.venv\Scripts\Activate.ps1         # Windows
```

**Pré-condição:** nenhuma. O milestone só edita `.github/copilot-instructions.md` (doc operacional do Copilot). Não há código novo, não há deps novas, não há `.env` a configurar.

---

## Testes unitários (determinísticos)

Não há testes automatizados aplicáveis a este milestone (alteração 100% em doc markdown). A suite continua passando como base; rode se quiser confirmar regressão zero:

```bash
pytest tests/core/unit -q
```

**Esperado:** mesmo resultado que `main` (este milestone não toca `tests/` nem `core/`).

---

## Épico W-PROTO-14 — Operacionalizar Reflex no fluxo de validação do Copilot

> Critérios em [docs/process/workflow/ROADMAP.md](workflow/ROADMAP.md), seção `#### ÉPICO W-PROTO-14`.

### 14.1 — Detecção de stack por produto

**Critério de aceite:** `.github/copilot-instructions.md` ganha tabela explícita produto → stack → entrypoint → comando → portas, posicionada como §"Stacks por produto" entre §"Pré-condição" (linhas 19-31) e §"Fluxo (3 passos)" (linha 35). Detecção pelo diff (`git diff --name-only origin/main | grep products/`) usa essa tabela como fonte. Se o diff toca produto sem entrada na tabela, o agente para e reporta — não improvisa.

**Gatilho:**
1. Abra `.github/copilot-instructions.md` no editor.
2. Role até logo depois da seção "Pré-condição: branch saiu do fluxo autônomo" (linha ~31) e antes da seção "## Fluxo (3 passos)".
3. Rode no terminal:
   ```bash
   grep -n "Stacks por produto" .github/copilot-instructions.md
   ```

**Resultado esperado:**
- Existe uma seção de cabeçalho `## Stacks por produto` posicionada entre §"Pré-condição" e §"Fluxo (3 passos)".
- A seção contém uma tabela com **exatamente** as duas linhas:
  - `| Revelar | products/revelar/app/  | Streamlit | products/revelar/app/chat.py (ou dashboard) | 8501-8503   |`
  - `| Ensaio  | products/ensaio/app/   | Reflex    | products/ensaio/ (reflex run a partir daí) | 3000, 8000  |`
- A seção contém o texto literal: `Se a branch toca produto fora desta tabela, **pare e reporte** — não improvise.`
- Existe instrução explícita para o caso "branch toca mais de um produto" (perguntar ao dev) e o caso "só `core/` ou `docs/`" (pular §3).
- O `grep` retorna pelo menos uma linha mencionando "Stacks por produto".

**Sinal de falha:**
- A seção §"Stacks por produto" não existe, ou aparece em outra posição (antes de §"Pré-condição" ou depois de §"Fluxo").
- A tabela está incompleta (faltam Revelar ou Ensaio) ou tem dados errados (ex.: "Ensaio | Streamlit | 8501").
- Falta a regra "pare e reporte" para produto fora da tabela.

---

### 14.2 — Comando de subida por stack na §3

**Critério de aceite:** §3 "Subir a app afetada" (linhas 68-96 hoje) é reescrita pra ramificar por stack detectada em 14.1. Comando de Reflex é foreground, com log visível, encerramento via Ctrl+C — mesma postura do Streamlit.

**Gatilho:**
1. Abra `.github/copilot-instructions.md` e localize a seção `### 3. Subir a app afetada`.
2. Rode no terminal:
   ```bash
   grep -n "reflex run" .github/copilot-instructions.md
   grep -n "products/ensaio" .github/copilot-instructions.md
   ```

**Resultado esperado:**
- §3 contém **dois** blocos de comando claramente rotulados: `**Streamlit (Revelar):**` e `**Reflex (Ensaio):**`.
- O bloco de Streamlit traz literalmente: `python -m streamlit run <entrypoint>`.
- O bloco de Reflex traz literalmente:
  ```
  cd products/ensaio
  reflex run
  ```
  com comentário indicando portas `backend :8000, frontend :3000`.
- §3 instrui subir em **foreground** e parar/reportar se houver traceback no start.
- §3 contém a frase de detecção pelo diff (`git diff --name-only origin/main | grep products/`).
- O `grep -n "reflex run"` retorna pelo menos 1 linha; `grep -n "products/ensaio"` retorna pelo menos 1 linha.

**Sinal de falha:**
- §3 ainda manda Streamlit para Ensaio (ex.: "Ensaio: `python -m streamlit run products/ensaio/...`").
- Falta um dos dois rótulos visuais (Streamlit ou Reflex).
- O comando Reflex está incompleto (sem `cd products/ensaio` ou sem `reflex run`).
- Nenhum dos `grep` retorna resultado.

---

### 14.3 — Liberação de portas por stack

**Critério de aceite:** o bloco de liberação de portas (linhas 70-83 hoje, hardcoded em 8501-8503) é reescrito pra cobrir Streamlit (8501-8503) **e** Reflex (3000, 8000). Detecção da stack reusa 14.1 e libera apenas as portas relevantes — não mata processos em geral.

**Gatilho:**
1. Abra `.github/copilot-instructions.md` e localize a sub-seção §"Liberação de portas" dentro de §3.
2. Rode no terminal:
   ```bash
   grep -nE "8501|8502|8503|3000|8000" .github/copilot-instructions.md
   ```

**Resultado esperado:**
- Existe um cabeçalho/sub-seção que menciona "Liberação de portas".
- O texto literal `Para Streamlit (Revelar): portas 8501-8503.` está presente.
- O texto literal `Para Reflex (Ensaio): portas 3000 (frontend) e 8000 (backend).` está presente.
- O bloco PowerShell traz `$ports = @(8501, 8502, 8503)` (ativo, Streamlit) e `# $ports = @(3000, 8000)` (comentário, Reflex) — comutável pelo agente conforme stack detectada.
- O bloco bash Linux/Mac traz **dois** `pkill`:
  - `pkill -f "streamlit.*products/revelar/app/" 2>/dev/null || true   # Revelar`
  - `pkill -f "reflex.*products/ensaio" 2>/dev/null || true            # Ensaio`
- O `grep -nE "8501|8502|8503|3000|8000"` retorna múltiplas linhas, com pelo menos uma na sub-seção §"Liberação de portas".

**Sinal de falha:**
- Bloco de portas continua hardcoded só em 8501-8503 (sem 3000/8000) ou só em 3000/8000 (sem 8501-8503).
- O `pkill` Linux/Mac mata streamlit em geral (`pkill -f "streamlit.*products/.*/app/"` sem distinção) em vez de filtrar por produto.
- Falta o comutável `$ports` no bloco PowerShell — bloco hardcoded só em uma stack.
- A frase "não mate processos em geral — mate apenas quem está escutando nas portas-alvo" desapareceu.

---

## Comportamentos "não deve" (regressão)

### Não deve: o Copilot mandar Streamlit para uma branch do Ensaio

**Gatilho:** Imagine que o dev pede "valida essa branch" e a branch tocou `products/ensaio/app/...`. Releia §"Stacks por produto" + §3 e simule mentalmente o passo-a-passo do Copilot.

**Resultado esperado:**
- A tabela §"Stacks por produto" mapeia `products/ensaio/app/` → Reflex, portas 3000/8000.
- §3 "Subir a app afetada" tem bloco rotulado `**Reflex (Ensaio):**` com `cd products/ensaio` + `reflex run`.
- §"Liberação de portas" libera 3000/8000 (não 8501-8503) para a stack detectada.

**Sinal de falha:**
- O caminho de leitura do Copilot termina em `python -m streamlit run` quando o produto detectado é Ensaio.
- Conflito entre §"Stacks por produto" e §3 (tabela diz Reflex, comando manda Streamlit).

### Não deve: o Copilot matar processos genéricos quando libera portas

**Gatilho:** Releia §"Liberação de portas".

**Resultado esperado:**
- O bloco PowerShell filtra **por porta** (`Get-NetTCPConnection -LocalPort $port`).
- O bloco Linux/Mac filtra **por entrypoint do projeto** (`pkill -f "streamlit.*products/revelar/app/"` e `pkill -f "reflex.*products/ensaio"`).
- A frase "não mate processos em geral — mate apenas quem está escutando nas portas-alvo" está presente.

**Sinal de falha:**
- O `pkill` ataca todos os processos contendo "python" ou "streamlit" sem caminho do projeto.
- A regra explícita de cirurgia por porta sumiu.

---

## Critérios de aprovação

Aprove o merge quando **todos**:

- [ ] Cada roteiro acima rodou (greps + leitura visual) e o **Resultado esperado** foi observado literalmente.
- [ ] Nenhum **Sinal de falha** ocorreu em nenhum roteiro.
- [ ] Comportamentos "não deve" foram confirmados (não ocorreriam se o Copilot seguisse a doc atualizada).
- [ ] Tabela do Copilot na PR (Seção 🎯) sem ❌ sem justificativa.

**Se algum critério falhar:** devolver com feedback para nova rodada autônoma (Claude Code Web).

---

**Ver também:**
- Skill da RTE → [skills/rte/skill.md](../../skills/rte/skill.md)
- Validação geral do modo autônomo → [docs/process/autonomous/delivery.md](autonomous/delivery.md)
