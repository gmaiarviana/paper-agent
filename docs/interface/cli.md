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

