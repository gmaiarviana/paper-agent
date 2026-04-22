# Copilot Instructions — Paper Agent

Guia para GitHub Copilot (no VS Code) quando o dev pede ajuda para **validar uma branch produzida pelo fluxo autônomo do Claude Code Web**.

Se o dev pedir outra coisa (implementar, refatorar, etc.), siga o pedido normalmente — este arquivo é específico para o fluxo de validação.

---

## Princípio

Testes já foram executados **duas vezes** antes da branch chegar pra ser validada:
1. **QA Skill** (Claude Code Web) rodou unit + integration durante a implementação — resultado em `docs/process/current_implementation.md`.
2. **CI** (`.github/workflows/test-unit.yml`) roda unit no push — status no PR.

Portanto **não re-rode testes por padrão**. O valor do passo local é o que CI e QA não conseguem: **ver a app subir sem crashar** e **observar os critérios de aceite visuais**. Só rode testes se o dev pedir explícito ou se algo abaixo indicar regressão.

---

## Fluxo quando o dev disser "valida essa branch X"

### 1. Sincronizar

```bash
git fetch origin
git checkout <branch>
git pull origin <branch>
```

### 2. Checar os sinais que já existem

**a) Gates do fluxo autônomo** — abrir `docs/process/current_implementation.md` e verificar:
- Status dos Gates: QA ✅ / TL ✅ / PO ✅
- Lista de tarefas concluídas (entender o que mudou)
- Critérios de aceite declarados

**b) CI** — verificar pelo PR ou via `gh`:
```bash
gh pr checks <branch>    # se houver PR aberto
# ou
gh run list --branch <branch> --limit 3
```

**Abortar antes de continuar** se:
- Algum gate estiver ❌ ou não preenchido → branch não passou no fluxo autônomo
- CI estiver vermelho → testes unit falhando
- `current_implementation.md` não existir → branch não veio do fluxo autônomo (talvez validação manual seja diferente; perguntar ao dev)

### 3. Checar se deps mudaram

```bash
git diff origin/main -- requirements.txt requirements-test.txt
```

Se mudou, rodar:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

Se `ModuleNotFoundError` aparecer depois em qualquer passo, é aqui que resolve.

### 4. Smoke-check da aplicação

Aplicar **apenas aos entry points afetados pela branch** (usar `git diff --stat origin/main` como guia):

**Streamlit chat (revelar)** — se mexeu em `products/revelar/app/**`:
```bash
timeout 15 streamlit run products/revelar/app/chat.py --server.headless true --server.port 8599 2>&1 | head -40
```
Sucesso: linha "You can now view your Streamlit app" sem traceback.

**Streamlit dashboard** — se mexeu em dashboard:
```bash
timeout 15 streamlit run products/revelar/app/dashboard.py --server.headless true --server.port 8598 2>&1 | head -40
```

**CLI** — se mexeu em `core/tools/cli/**`:
```bash
echo "" | timeout 10 python -m core.tools.cli.chat 2>&1 | head -30
```
Sucesso: CLI inicia e mostra prompt sem traceback.

Se a branch só mexe em `core/agents/**`, `docs/**` ou testes — pular esta etapa.

### 5. Listar critérios de aceite pra inspeção visual

Da seção de critérios em `current_implementation.md` (e/ou ROADMAP linkado), separar:
- **Cobertos por teste** (QA/CI já validaram) → não listar
- **Comportamento observável** (ex: "ao clicar em X, aparece Y") → listar como checkbox pro dev
- **"Não deve"** não coberto por teste → listar como inspeção manual

### 6. Reportar

```
Branch: <nome>
Diff resumido: <N arquivos, áreas principais>

Sinais verdes
  ✅/❌ Gates QA/TL/PO (via current_implementation.md)
  ✅/❌ CI (via gh pr checks)
  ✅/❌ Smoke app: <entry points testados + resultado>

📋 Critérios pendentes de inspeção visual
  - [ ] <critério 1>
  - [ ] <critério 2>

⚠️ Pontos de atenção
  - <se alguma coisa fugiu do esperado>

Recomendação: <aprovar merge | ajustar X | subir a app e inspecionar Y>
```

---

## Quando RE-RODAR testes localmente

Só nesses casos:

- Dev pediu explícito ("roda os testes também")
- Um gate está ❌ em `current_implementation.md` e o dev quer confirmar o problema
- CI vermelho e dev quer reproduzir localmente
- Você detectou regressão de dep no passo 3 e quer validar depois do pip install

Comandos (se precisar):
```bash
pytest tests/core/unit/ -q
pytest tests/core/integration/ -m integration -q --maxfail=1   # só se ANTHROPIC_API_KEY setada
```

Perfis completos em `docs/testing/commands.md`.

---

## Regras

- **Não crie PR nem faça merge.** O dev decide.
- **Não faça push de código novo.** Só validação.
- Preserve o ambiente do dev: não rode `pip uninstall`, não mexa em `.env`.
- Se encontrar problema, **reporte** e pare. Não tente "consertar" sem pedido explícito.

---

## Referências

- Fluxo autônomo completo: `docs/process/autonomous/workflow.md`
- Mensagem final esperada da Validation Skill: `docs/process/autonomous/delivery.md`
- Perfis de teste (se precisar rodar): `docs/testing/commands.md`
