# Prompts do Sistema

> **Nota:** Prompts obsoletos (ORCHESTRATOR_CLASSIFICATION_PROMPT, STRUCTER_PROMPT) foram removidos. O sistema agora usa prompts conversacionais carregados de `config/agents/<papel>.yaml` em runtime.

## Prompts Atuais

Os prompts dos agentes são carregados dinamicamente de arquivos YAML:

- `config/agents/orchestrator.yaml` - Orquestrador Socrático
- `config/agents/structurer.yaml` - Estruturador
- `config/agents/methodologist.yaml` - Metodologista
- `config/agents/observer.yaml` - Observador

Os prompts completos também estão disponíveis em `utils/prompts/` (modularizado por agente) para referência.

## Referências

- **Configuração:** [config.md](config.md)
- **Implementação dos nós:** [nodes.md](nodes.md)
- **Prompts completos:** `utils/prompts/` (modularizado por agente)
