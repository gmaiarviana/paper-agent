# LiteLLM Proxy

Setup local do proxy [LiteLLM](https://github.com/BerriAI/litellm) que traduz
Anthropic ↔ OpenAI. Necessário **apenas para Claude Code**; os demais clientes
(OpenCode, Aider) falam OpenAI direto e não usam o proxy.

> **Setup de todos os clientes:** ver [`infra/llm-clients/`](../llm-clients/).

> **Heads-up sobre o Claude Code:** o LiteLLM 1.74.x tem bug ao traduzir
> tool-use de modelos não-Anthropic (ex.: `gpt-oss:20b`, `qwen3.6:35b`). Você
> verá `API Error: Content block is not a text block`. Por isso o setup
> recomendado migrou pra **OpenCode**. O proxy segue documentado pra quem
> ainda quer testar o Claude Code.

> **Independente do projeto.** Esta pasta é uma ferramenta de desenvolvimento.
> Pode ser apagada inteira sem quebrar o `paper-agent`.

---

## Pré-requisitos

- Windows + PowerShell 5+
- Python 3.10+ com `venv` criada na raiz do projeto (`.venv`)
- Claude Code instalado (`npm i -g @anthropic-ai/claude-code` ou similar)
- Uma chave do **OpenWebUI** (default) — gerar em
  `https://chat.alia.atlantico.com.br` → Settings → Account → API Keys.
  Alternativamente, chave da Anthropic se trocar o backend no YAML.

---

## Instalação

A partir da **raiz do projeto**:

```powershell
# 1. Ative a venv
.\.venv\Scripts\Activate.ps1

# 2. Instale o LiteLLM (versão pinada — não use `pip install -U litellm`)
pip install -r infra\litellm-proxy\requirements.txt
```

> ⚠️ **Não atualize o LiteLLM para 1.83.x.** Há um bug de loop interno em
> `/v1/messages` no Windows. A versão 1.74.15 está pinada por isso.

### Variáveis de ambiente

No `.env` da raiz (use `.env.example` como base) defina:

```
# Backend OpenWebUI (default)
OPENWEBUI_API_KEY=sk-...                            # chave do OpenWebUI
OPENWEBUI_BASE_URL=https://chat.alia.atlantico.com.br/api

# Opcional: roteia clientes SDK/CLI pro proxy local
ANTHROPIC_BASE_URL=http://localhost:4000
```

A variável `ANTHROPIC_BASE_URL` é **lida apenas por clientes** (SDK Python,
Claude Code). O script `start-proxy.ps1` ignora ela ao iniciar o LiteLLM —
caso contrário, o proxy chamaria a si mesmo em loop.

> Se quiser voltar pro backend Anthropic direto, edite `litellm-config.yaml`
> trocando `model: openai/...` por `model: anthropic/claude-*` e
> `api_key: os.environ/OPENWEBUI_API_KEY` por `os.environ/ANTHROPIC_API_KEY_BACKEND`.

---

## Uso (apenas se usando Claude Code)

### Terminal 1 — Sobe o proxy

```powershell
.\start-proxy.ps1
```

Aguarde a mensagem `Application startup complete` + `Uvicorn running on
http://0.0.0.0:4000`. Mantenha esse terminal aberto.

### Terminal 2 — Valida o proxy

```powershell
.\test-proxy.ps1
```

Esperado: 3 testes verdes (health, `/v1/messages`, wildcard).

### Terminal 3 — Aponta o Claude Code para o proxy

```powershell
..\llm-clients\setup-claude-code.ps1
claude
```

O comando `claude` vai abrir o REPL e responder via proxy. Confirme no log do
Terminal 1: deve aparecer `POST /v1/messages?... 200 OK`.

> Se o Claude Code perguntar `Do you want to use this API key?`, escolha **Yes**.
> Ele detectou a chave que setamos — é o esperado.

> Se aparecer `Auth conflict: Both a token (claude.ai) and an API key`, rode
> `/logout` no REPL pra silenciar — ou ignore, o aviso é cosmético.

---

## Troubleshooting

### "Connection refused" ao chamar /v1/messages
LiteLLM não está rodando. Verifique o Terminal 1.

### Proxy fica em loop, requests ficam em timeout
Você está com **LiteLLM 1.83.x**. Volte para 1.74.15:
```powershell
pip install -r infra\litellm-proxy\requirements.txt --force-reinstall
```

### "UnicodeEncodeError" no startup do LiteLLM
Console do Windows está em CP1252. O `start-proxy.ps1` já força UTF-8, mas se
você invocar `litellm` direto, exporte antes:
```powershell
$env:PYTHONIOENCODING = "utf-8"; $env:PYTHONUTF8 = "1"
```

### "Unauthorized" / 401 / "API key invalid"
A chave em `OPENWEBUI_API_KEY` no `.env` está errada ou expirada. Teste direto
no OpenWebUI:
```powershell
curl https://chat.alia.atlantico.com.br/api/chat/completions `
  -H "Authorization: Bearer sk-..." -H "Content-Type: application/json" `
  -d '{"model":"ministral-3:14b","messages":[{"role":"user","content":"ok"}]}'
```

### Modelo retorna 404 / "model not found"
O nome em `litellm-config.yaml` (`openai/gpt-oss:20b`) precisa
existir em `https://chat.alia.atlantico.com.br/api/models`. Lista atual:
- `llama3.2:3b` (rápido, leve)
- `gpt-oss:20b` (default)
- `qwen3.6:35b`

Compatibilidade: o alias `ollama/qwen3.6:27b` segue aceito no proxy, mas hoje
ele roteia para `qwen3.6:35b` (modelo Qwen ativo no OpenWebUI).

Snapshots locais dessa lista (atualizados manualmente via API):
- `infra/litellm-proxy/openwebui-models.snapshot.json`
- `infra/litellm-proxy/openwebui-models.ids.txt`

### Quero apagar tudo
1. Apague esta pasta `infra/litellm-proxy/`.
2. Remova `OPENWEBUI_API_KEY`, `OPENWEBUI_BASE_URL` e `ANTHROPIC_BASE_URL` do `.env`.
3. `pip uninstall litellm litellm-proxy-extras`

---

## Arquitetura

```
┌──────────────┐  POST /v1/messages         ┌────────────────────┐
│  Claude Code │  x-api-key: sk-litellm-... │   LiteLLM Proxy    │
│              ├──────────────────────────► │   localhost:4000   │
│ ANTHROPIC_   │                            │                    │
│ BASE_URL =   │ ◄──────────────────────────┤ (model_list yaml)  │
│ localhost:   │     resposta Anthropic     │                    │
│ 4000         │                            └─────────┬──────────┘
└──────────────┘                                      │
                                                      │ POST /chat/completions
                                                      │ Authorization: Bearer <chave>
                                                      ▼
                                           ┌────────────────────────────┐
                                           │  chat.alia.atlantico.com.br│
                                           │  /api  (OpenWebUI default) │
                                           │                            │
                                           │  ou api.anthropic.com,     │
                                           │  Azure, Ollama local…      │
                                           └────────────────────────────┘
```

A configuração do roteamento está em [`litellm-config.yaml`](./litellm-config.yaml).
O wildcard `claude-*` casa qualquer model_name que o Claude Code envie e
roteia tudo pro backend único definido lá. Para trocar de backend, edite só
esse arquivo — o Claude Code não precisa saber.

---

## Estrutura desta pasta

| Arquivo | Função |
|---|---|
| `litellm-config.yaml` | Roteamento de modelo → provedor (wildcard `claude-*` → OpenWebUI) |
| `start-proxy.ps1` | Sobe o proxy na porta 4000 |
| `test-proxy.ps1` | Smoke test (3 chamadas) |
| `openwebui-models.snapshot.json` | Snapshot da lista de modelos do OpenWebUI |
| `openwebui-models.ids.txt` | Mesma lista, só IDs |
| `requirements.txt` | Versão pinada do LiteLLM |
| `README.md` | Este arquivo |
