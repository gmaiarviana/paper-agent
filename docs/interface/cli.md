CLI e Interfaces
================

CLI (chat.py)
-------------
- Interface principal para desenvolvimento e testes automatizados.
- Comunicação via stdin/stdout para compatibilidade com Claude Code e Cursor background.
- Funcionalidade básica:
  - Loop contínuo até `exit`/`quit`
  - Logs dos componentes com ícones/cores (via `rich` ou similar)
  - Flag `--verbose` habilita nível `DEBUG` para prompts e respostas completas

Experiência Esperada
--------------------
- Mensagens de decisão do Orquestrador antecedem qualquer chamada de agente (`🎯 Orquestrador decidiu: ...`).
- Quando o Metodologista é chamado, a CLI exibe status e resumo da decisão (`🧪`, `✅`/`❌`).
- Histórico recente permanece visível no terminal para contexto rápido.

Streamlit (Opcional)
--------------------
- `app.py` oferece visualização gráfica local para demonstrações humanas.
- Estrutura sugerida:
  - Painel principal: histórico de mensagens
  - Sidebar: logs em tempo real, incluindo transições do Orquestrador
  - Indicadores visuais (spinner, badges de agente ativo)
- Recomendado rodar apenas após o fluxo CLI estar validado.

Roteiro de Evolução
-------------------
- Adicionar painel de logs enriquecido no terminal (Épico 4.2)
- Avaliar suporte a execução não interativa (`--input "..."`) para testes automatizados
- Documentar aqui quaisquer argumentos novos ou variações de execução

Telemetria em Tempo Real (Épicos 5 e 6)
---------------------------------------
- CLI passa a registrar eventos estruturados em `runtime/streams/<session_id>.jsonl` usando append atômico de JSONL.
- Cada evento enviado para a UI segue o schema abaixo (campos string, números em ponto flutuante, timestamps ISO 8601):

```
{
  "schema_version": 1,
  "event_id": "evt-0001",
  "session_id": "cli-session-<uuid>",
  "agent": "methodologist",
  "action": "invoke" | "interrupt" | "complete" | "error",
  "status": "running" | "done" | "failed",
  "started_at": "2025-11-12T10:35:21.123Z",
  "finished_at": "2025-11-12T10:35:28.456Z",
  "tokens_input": 512,
  "tokens_output": 216,
  "tokens_total": 728,
  "cost": 0.0046,
  "summary": "Resumo curto do raciocínio (<= 280 chars)",
  "payload": {...}  # opcional, usado para detalhes expandíveis na UI
}
```

- Streamlit faz polling a cada 1s com cache incremental por arquivo; `watchdog` será avaliado depois, caso o polling não atenda.
- Identificadores:
  - `session_id`: reutiliza o `thread_id` já gerado pelo CLI (`cli-session-<uuid>`).
  - `event_id`: contador incremental por sessão (`evt-0001`, `evt-0002`, ...).
- UI reconstruirá timeline e custos lendo todo o JSONL; eventos inválidos são ignorados e logados em `warning`.
- CLI continua executando mesmo se a escrita falhar, emitindo aviso em PT-BR.

Contrato de Transporte
----------------------
- Canal base: arquivo JSONL local sob `runtime/streams/`. Mantém setup simples, funciona offline e permite múltiplas interfaces lendo em paralelo.
- Streamlit mantém cache em memória per sessão para evitar releituras completas; quando o arquivo cresce, apenas novas linhas são processadas.
- Evoluções futuras podem adicionar websocket, mas o contrato inicia em arquivo para reduzir dependências.

Versionamento do Contrato
-------------------------
- `schema_version` controla alterações compatíveis; UI e CLI evoluem juntas neste repositório.
- Quebras de contrato exigem incrementar a versão e manter parser retro-compatível até migração completa.
- Caso a CLI não consiga escrever o campo `schema_version`, assume-se `1` por padrão.

