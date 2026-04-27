# LiteLLM Proxy para Claude Code

Setup local opcional que coloca um proxy [LiteLLM](https://github.com/BerriAI/litellm)
entre o **Claude Code** (CLI da Anthropic) e a API real, permitindo:

- Trocar o backend Anthropic por outro provedor compatível (ex: OpenWebUI, Azure
  OpenAI, Ollama) **sem mexer no Claude Code**.
- Logar/auditar todas as requests.
- Cachear, aplicar rate limit, observar uso por modelo.

> **Independente do projeto.** Esta pasta é uma ferramenta de desenvolvimento.
> Pode ser apagada inteira sem quebrar o `paper-agent`.

---

## Pré-requisitos

- Windows + PowerShell 5+
- Python 3.10+ com `venv` criada na raiz do projeto (`.venv`)
- Claude Code instalado (`npm i -g @anthropic-ai/claude-code` ou similar)
- Uma chave válida da Anthropic (ou de qualquer outro backend compatível)

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
ANTHROPIC_API_KEY_BACKEND=sk-ant-api03-...    # chave real do backend
ANTHROPIC_BASE_URL=http://localhost:4000      # opcional, só pra clientes Python
```

A variável `ANTHROPIC_BASE_URL` é **lida apenas por clientes** (SDK Python,
Claude Code). O script `start-proxy.ps1` ignora ela ao iniciar o LiteLLM —
caso contrário, o proxy chamaria a si mesmo em loop.

---

## Uso

### Terminal 1 — Sobe o proxy

```powershell
.\infra\litellm-proxy\start-proxy.ps1
```

Aguarde a mensagem `Application startup complete` + `Uvicorn running on
http://0.0.0.0:4000`. Mantenha esse terminal aberto.

### Terminal 2 — Valida o proxy

```powershell
.\infra\litellm-proxy\test-proxy.ps1
```

Esperado: 3 testes verdes (health, `/v1/messages`, wildcard).

### Terminal 3 — Aponta o Claude Code para o proxy

```powershell
.\infra\litellm-proxy\setup-claude-code.ps1
claude
```

O comando `claude` vai abrir o REPL e responder via proxy. Confirme no log do
Terminal 1: deve aparecer `POST /v1/messages?... 200 OK`.

> Se o Claude Code perguntar `Do you want to use this API key?`, escolha **Yes**.
> Ele detectou a chave dummy que setamos — é o esperado.

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
A chave em `ANTHROPIC_API_KEY_BACKEND` no `.env` está errada ou expirada. Teste
direto com a Anthropic:
```powershell
curl https://api.anthropic.com/v1/messages -H "x-api-key: sk-ant-..." -H "anthropic-version: 2023-06-01" -H "content-type: application/json" -d '{"model":"claude-haiku-4-5-20251001","max_tokens":16,"messages":[{"role":"user","content":"ok"}]}'
```

### Quero apagar tudo
1. Apague esta pasta `infra/litellm-proxy/`.
2. Remova `ANTHROPIC_API_KEY_BACKEND` e `ANTHROPIC_BASE_URL` do `.env`.
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
                                                      │ POST /v1/messages
                                                      │ x-api-key: <chave real>
                                                      ▼
                                           ┌────────────────────┐
                                           │  api.anthropic.com │
                                           │  (ou OpenWebUI,    │
                                           │   Azure, Ollama…)  │
                                           └────────────────────┘
```

A configuração do roteamento está em [`litellm-config.yaml`](./litellm-config.yaml).
O wildcard `claude-*` cobre todos os modelos da família Claude. Para trocar de
backend (ex: OpenWebUI), edite só esse arquivo — o Claude Code não precisa
saber.

---

## Estrutura desta pasta

| Arquivo | Função |
|---|---|
| `litellm-config.yaml` | Roteamento de modelo → provedor |
| `start-proxy.ps1` | Sobe o proxy carregando `.env` da raiz |
| `test-proxy.ps1` | Smoke test (3 chamadas) |
| `setup-claude-code.ps1` | Seta `ANTHROPIC_BASE_URL` na sessão atual |
| `requirements.txt` | Versão pinada do LiteLLM |
| `README.md` | Este arquivo |
