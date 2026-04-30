CLI e Interfaces
================

> **📌 Mudança de Papel (15/11/2025):** CLI passou de interface principal para ferramenta de desenvolvimento. Interface web conversacional (Streamlit) é agora a experiência principal do sistema. Ver `products/revelar/docs/interface/` (overview.md, components.md, flows.md) para detalhes.

---

CLI (chat.py)
-------------
- Ferramenta de desenvolvimento para testes automatizados, debugging e scripts
- Funcionalidade congelada (novas features vão para interface web)
- Backend compartilhado com interface web (LangGraph + EventBus)
- Útil para CI/CD, validação rápida de prompts, automação
- Comunicação via stdin/stdout para compatibilidade com agentes (Claude Code Web)
- Funcionalidade básica:
  - Loop contínuo até `exit`/`quit`
  - Logs dos componentes com ícones/cores (via `rich` ou similar)
  - Flag `--verbose` habilita nível `DEBUG` para prompts e respostas completas

## Quando Usar CLI vs Interface Web

### Use CLI quando:
- ✅ **Testes automatizados**: Scripts de validação, CI/CD
- ✅ **Debugging**: Testar prompts rapidamente sem abrir navegador
- ✅ **Automação**: Scripts que invocam o sistema (ex: batch processing)
- ✅ **Desenvolvimento de agentes**: Validar mudanças sem UI

### Use Interface Web quando:
- ✅ **Uso interativo**: Conversar com o sistema naturalmente
- ✅ **Ver bastidores**: Acompanhar reasoning dos agentes em tempo real
- ✅ **Múltiplas sessões**: Gerenciar várias conversas
- ✅ **Persistência**: Pausar e retomar conversas entre visitas
- ✅ **Experiência visual**: Timeline, métricas, interface rica

**Recomendação:** Usuários finais devem preferir interface web. CLI é para desenvolvedores.

Experiência Esperada
--------------------

> **Nota:** CLI oferece experiência minimalista focada em texto. Para interface visual com bastidores e timeline, use o Dashboard (`streamlit run products/revelar/app/dashboard.py`). Interface web conversacional (`products/revelar/app/chat.py`) será implementada no Épico 9.

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

**CLI está congelado para novas features.** Melhorias futuras vão para interface web.

**Manutenção mínima:**
- Bugs críticos serão corrigidos
- Backend compartilhado mantém funcionalidade
- Documentação preservada para referência

**Migração para Web:**
- Novas funcionalidades serão implementadas em `products/revelar/app/chat.py` (Épico 9)
- Bastidores, timeline, sessões → exclusivos da web
- CLI permanece útil para automação e testes

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

