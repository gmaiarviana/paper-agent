# LLM Clients Setup

Scripts pra conectar cada REPL ao OpenWebUI corporativo. Escolha o seu:

| REPL | Caso de uso | Comando |
|---|---|---|
| **OpenCode** (recomendado) | Implementação + refinamento com tool-use nativo | `.\setup-opencode.ps1 && opencode` |
| **Aider** | Refinamento rápido, modo inline | `.\setup-aider.ps1 && aider` |
| **Claude Code** (legado) | Antes do OpenCode; usa proxy LiteLLM | `.\setup-claude-code.ps1 && claude` |

---

## OpenCode (default)

Terminal-first REPL que fala OpenAI direto com o OpenWebUI. Sem tradução
Anthropic↔OpenAI = sem SSE bug.

```powershell
.\setup-opencode.ps1
opencode                                # TUI interativa
opencode run "sua tarefa" --model atlantico/gpt-oss:20b  # headless
opencode models atlantico               # lista modelos
```

Modelos: `gpt-oss:20b` (default), `qwen3.6:35b`, `llama3.2:3b`

---

## Aider

Editor inline com LLM. Também fala OpenAI direto (sem proxy).

```powershell
.\setup-aider.ps1
aider
```

---

## Claude Code

**Legado.** Usa o proxy LiteLLM em `localhost:4000` (requer `start-proxy.ps1`
rodando em outro terminal). Deixar aqui pra referência, mas migração pra
OpenCode é recomendada.

```powershell
.\setup-claude-code.ps1
claude
```

---

## Detalhes de setup

- Cada script carrega `OPENWEBUI_API_KEY` + `OPENWEBUI_BASE_URL` do `.env` da raiz
- Configuração de providers em:
  - OpenCode: [`opencode.json`](../../opencode.json) na raiz
  - Aider/Claude Code: variáveis de env só
- Troubleshooting: ver `infra/litellm-proxy/README.md`
