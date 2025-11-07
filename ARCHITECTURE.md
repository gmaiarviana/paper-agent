# ARCHITECTURE.md

## Visão Geral

- Plataforma colaborativa com agentes de IA para apoiar produção de artigos científicos ponta a ponta.
- POC atual: validação de hipóteses com Orquestrador + Metodologista rodando sobre LangGraph.
- Interfaces priorizadas: CLI (automação com agentes) e Streamlit opcional para uso humano.

## Escopo Atual (POC)

- Entradas via CLI; respostas estruturadas do Orquestrador.
- Apenas um agente especialista ativo (Metodologista), documentado em `docs/agents/methodologist.md`.
- Estado em memória gerenciado por LangGraph, sem persistência ou vector DB.
- Infraestrutura mínima: Python 3.11+, Anthropic API, sem Docker ou banco de dados.

## Stack Técnico

- **Runtime:** Python 3.11+
- **Orquestração:** LangGraph, LangChain Anthropic
- **LLM:** Claude Sonnet 4 (Anthropic API)
- **Validação:** Pydantic
- **Interfaces:** CLI (`cli/chat.py`), Streamlit opcional (`app.py`)
- **Utilitários:** `rich` para logging, `python-dotenv` para variáveis

## Estrutura de Pastas (high-level)

```
paper-agent/
├── README.md              # Visão geral + como rodar
├── ROADMAP.md             # Planejamento de funcionalidades
├── ARCHITECTURE.md        # Visão arquitetural (este arquivo)
├── docs/                  # Detalhes por domínio
│   ├── agents/
│   ├── interface/
│   ├── orchestration/
│   └── process/
├── cli/                   # Interface em linha de comando
├── agents/                # Implementações de agentes
├── orchestrator/          # Orquestrador e estado LangGraph
├── utils/                 # Prompts, logging, helpers
└── tests/                 # Scripts de validação manual
```

## Componentes Principais

- **Orquestrador (`orchestrator/`)**: decide próxima ação; detalhes em `docs/orchestration/orchestrator.md`.
- **Metodologista (`agents/methodologist.py`)**: avalia hipóteses; contrato em `docs/agents/methodologist.md`.
- **CLI (`cli/chat.py`)**: loop interativo e logs; UX descrita em `docs/interface/cli.md`.
- **Estado (`orchestrator/state.py`)**: TypedDict versionado; roadmap para LangGraph em `docs/langgraph/examples.md`.
- **Prompts/Logs (`utils/`)**: prompts versionados, logging estruturado e níveis de verbosidade.

## Fluxo de Dados (resumo)

```
Usuário (CLI) → Orquestrador →
  ├─ Responde direto
  └─ Chama Metodologista → JSON estruturado → Orquestrador → Usuário
```

Logs exibem decisões antes das chamadas de agentes; modo `--verbose` mostra prompts e respostas brutas.

## Padrões Essenciais

- **Contratos em JSON** entre orquestrador e agentes (status, justificativa, sugestões).
- **Validação** via Pydantic e retries com backoff (até 3 tentativas) para chamadas Anthropic.
- **Transparência**: logs estruturados (`INFO` para decisões, `DEBUG` para reasoning completo).
- **Separação de responsabilidades**: agentes não se conhecem; orquestrador não faz análise científica.

## Decisões Técnicas Atuais

- Prioridade para CLI: permite automação com agentes (Claude Code / Cursor) sem dependência de navegador.
- Sem persistência, Docker ou vector DB durante a POC para acelerar iteração.
- Claude Sonnet 4 escolhido pelo equilíbrio entre custo e confiabilidade de JSON estruturado.

## Próximas Evoluções Previstas

- Épico 4: logs enriquecidos na CLI e Streamlit como alternativa visual.
- Épico 5: LangGraph assumindo gestão completa do estado (ver `docs/langgraph/examples.md`).
- Futuro: novos agentes (Pesquisador, Estruturador, Escritor, Crítico) documentados em `docs/agents/overview.md`.

## Referências

- `README.md`: visão geral e execução.
- `docs/agents/overview.md`: mapa completo de agentes planejados.
- `docs/orchestration/orchestrator.md`: regras de decisão e estado.
- `docs/interface/cli.md`: expectativas de UX e logging.
- `docs/process/planning_guidelines.md`: governança de roadmap e práticas de planejamento.

**Versão:** 1.1  
**Data:** 07/11/2025  
**Status:** Foco na POC (Orquestrador + Metodologista)