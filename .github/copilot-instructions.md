# Copilot Instructions — Paper Agent

Guia para GitHub Copilot (no VS Code) quando o dev pede ajuda para **validar uma branch produzida pelo fluxo autônomo do Claude Code Web**.

Se o dev pedir outra coisa (implementar, refatorar, etc.), siga o pedido normalmente — este arquivo é específico para o fluxo de validação.

---

## Contexto do projeto

- Monorepo com `core/` (runtime) e `products/` (produtos que consomem o core).
- Branches `claude/*` e `feature/*` são produzidas pelo fluxo autônomo descrito em `docs/process/autonomous/`.
- A entrega vem com artefatos fixos: `docs/process/current_implementation.md` (plano + status dos gates) e mensagem final listando comandos + critérios de aceite.
- Dois perfis de teste formalizados em `docs/testing/commands.md`:
  - **Unit (rápido, $0):** `requirements-test.txt` + `pytest tests/core/unit/`
  - **Full Integration (pago, rede):** `requirements.txt` + `ANTHROPIC_API_KEY` + `pytest tests/core/integration/ -m integration`

---

## Fluxo quando o dev disser "valida essa branch X"

Execute em ordem. Pare e reporte ao dev no primeiro erro crítico; se só for warning, continue e inclua no relatório final.

### 1. Sincronizar a branch

```bash
git fetch origin
git checkout <branch>
git pull origin <branch>
```

### 2. Ler o contrato de entrega

Abrir e extrair destes dois arquivos — são a **fonte de verdade** do que foi entregue:

- `docs/process/current_implementation.md`
  - Status dos gates (QA / TL / PO): devem estar marcados como ✅
  - Lista de tarefas concluídas
  - Evidências de carregamento de skill (para auditoria)
- Mensagem final do commit da Validation Skill (normalmente no último commit da branch) — contém:
  - Comandos de validação prontos
  - Critérios de aceite do ROADMAP a observar

Se algum gate estiver como ❌ ou pulado, **avise o dev antes de continuar**.

### 3. Preparar ambiente

```bash
python -m venv venv                 # se ainda não existir
source venv/bin/activate            # Linux/Mac
# .\venv\Scripts\Activate.ps1       # Windows
pip install -r requirements.txt
```

Use `requirements.txt` (completo) por padrão — integration precisa dele. `requirements-test.txt` só se o dev pedir o perfil rápido.

### 4. Rodar testes

**Perfil Unit** (sempre):
```bash
pytest tests/core/unit/ -q
```
Espera-se: 0 falhas. Skips são aceitos (ver `docs/testing/commands.md` para quais).

**Perfil Integration** (se `ANTHROPIC_API_KEY` estiver setada no `.env` ou exportada):
```bash
pytest tests/core/integration/ -m integration -q --maxfail=1
```
Espera-se: 0 falhas. Se cair por falta de API key, reporte ao dev — não pule.

### 5. Smoke-check da aplicação

Se a branch mexeu em `products/revelar/app/**` ou `core/tools/cli/**`, subir e verificar que não crasha:

**Streamlit chat (revelar):**
```bash
timeout 15 streamlit run products/revelar/app/chat.py --server.headless true --server.port 8599 2>&1 | head -40
```
Sucesso: aparece "You can now view your Streamlit app" sem traceback. Se sair antes por erro de import/runtime, reporte o traceback.

**Streamlit dashboard:**
```bash
timeout 15 streamlit run products/revelar/app/dashboard.py --server.headless true --server.port 8598 2>&1 | head -40
```

**CLI:**
```bash
echo "" | timeout 10 python -m core.tools.cli.chat 2>&1 | head -30
```
Sucesso: CLI inicia e mostra prompt sem traceback.

Se mudou nenhuma interface, pular esta etapa.

### 6. Mapear critérios de aceite

Para cada critério listado na mensagem final da branch:

- Se o critério tem teste associado → já coberto pelo passo 4, marcar como ✅
- Se é comportamento observável (ex: "ao clicar em X, aparece Y") → listar para o dev inspecionar visualmente
- Se é "não deve" (ex: "não deve quebrar comportamento anterior") → se houver regressão nos testes, já pegou; senão, listar como inspeção manual

### 7. Reportar ao dev

Formato fixo:

```
Branch: <nome>
Commits novos: <N>

✅ Gates autônomos (via current_implementation.md)
  - QA: <status>
  - TL: <status>
  - PO: <status>

✅ Testes
  - Unit: <passed/failed/skipped>
  - Integration: <passed/failed/skipped> OU "pulado (sem API key)"

✅ Smoke da aplicação
  - <entry point>: <OK | falhou com: <trecho do erro>>

📋 Critérios de aceite pendentes de inspeção visual
  - [ ] <critério 1>
  - [ ] <critério 2>

⚠️ Pontos de atenção
  - <warnings que apareceram>

Recomendação: <aprovar merge | pedir ajuste | aprofundar critério N>
```

---

## Regras

- **Não crie PR nem faça merge.** O dev decide.
- **Não faça push de código novo.** Só validação.
- Se o teste unit falhar, pare e reporte. Não tente "consertar" sem o dev pedir.
- Se faltar dependência (ex: `ModuleNotFoundError`), verifique se `requirements.txt` foi atualizado na branch — se sim, rode `pip install -r requirements.txt` novamente; se não, reporte como regressão.
- Preserve o ambiente do dev: não rode `pip uninstall` sem pedir; não mexa em `.env`.

---

## Referências

- Fluxo autônomo completo: `docs/process/autonomous/workflow.md`
- Mensagem final esperada: `docs/process/autonomous/delivery.md`
- Perfis de teste: `docs/testing/commands.md`
- Layout de testes: `docs/testing/structure.md`
