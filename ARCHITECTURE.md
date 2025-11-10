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
- **LLM:** Claude 3.5 Haiku (custo-benefício) / Sonnet (tarefas complexas)
- **Validação:** Pydantic
- **Interfaces:** CLI (futura), Streamlit opcional (futura)
- **Utilitários:** `colorama` para logging colorido, `python-dotenv` para variáveis

## Estrutura do Projeto

```
paper-agent/
├── .env.example           # Template de variáveis de ambiente
├── requirements.txt       # Dependências Python
├── README.md              # Getting Started
├── ROADMAP.md             # Status de épicos e funcionalidades
├── ARCHITECTURE.md        # Visão arquitetural (este arquivo)
├── development_guidelines.md  # Regras para desenvolvimento com agentes
│
├── agents/                # Agentes especializados
│   ├── __init__.py
│   ├── methodologist.py   # Estado, tools e nós do Metodologista
│   └── methodologist_knowledge.md  # Base de conhecimento micro
│
├── orchestrator/          # Lógica de orquestração e decisão
│   └── __init__.py        # (Futuro: orchestrator.py, state.py)
│
├── utils/                 # Utilitários e helpers
│   ├── __init__.py
│   ├── prompts.py         # Prompts versionados dos agentes
│   └── cost_tracker.py    # Cálculo de custos de API
│
├── app/                   # Interface Streamlit (futura)
│   └── __init__.py        # (Futuro: app.py)
│
├── tests/                 # Testes automatizados (pytest)
│   ├── __init__.py
│   ├── unit/              # Testes unitários (mocks, rápidos)
│   │   ├── __init__.py
│   │   ├── test_cost_tracker.py
│   │   ├── test_methodologist_state.py  # Testes do estado
│   │   ├── test_ask_user_tool.py        # Testes da tool ask_user
│   │   └── test_graph_nodes.py          # Testes dos nós analyze, ask_clarification, decide
│   ├── integration/       # Testes de integração (API real)
│   │   └── __init__.py
│   └── conftest.py        # Fixtures compartilhadas (futuro)
│
├── scripts/               # Scripts de validação manual
│   ├── __init__.py
│   ├── validate_api.py    # Health check da API
│   ├── validate_state.py  # Validação do estado do Metodologista
│   ├── validate_ask_user.py  # Validação da tool ask_user
│   └── validate_graph_nodes.py  # Validação dos nós do grafo
│
└── docs/                  # Documentação detalhada por domínio
    ├── testing_guidelines.md  # Estratégia de testes
    ├── agents/            # Especificações de agentes
    │   ├── overview.md
    │   └── methodologist.md
    ├── interface/         # Especificações de interface
    │   └── cli.md
    ├── orchestration/     # Orquestração e estado
    │   └── orchestrator.md
    ├── langgraph/         # Exemplos e padrões LangGraph
    │   └── examples.md
    └── process/           # Processo e governança
        └── planning_guidelines.md
```

## Componentes Principais

### Metodologista (`agents/methodologist.py`)
Agente especializado em avaliar rigor científico de hipóteses usando LangGraph.

**Arquitetura:**
- Estado gerenciado por `MethodologistState` (TypedDict)
- Persistência de sessão via MemorySaver
- 3 nós do grafo: `analyze`, `ask_clarification`, `decide`
- Tool `ask_user` para interação via `interrupt()`
- Knowledge base micro sobre método científico

**Detalhes:** Ver `docs/agents/methodologist.md`

### Orquestrador (`orchestrator/`)
Decide próxima ação e roteia para agentes especializados.

**Detalhes:** Ver `docs/orchestration/orchestrator.md` (futuro - Épico 3)

### CLI (`cli/chat.py`)
Loop interativo e logs estruturados.

**Detalhes:** Ver `docs/interface/cli.md` (futuro - Épico 2, Task 2.7)

### Utilitários (`utils/`)
- `cost_tracker.py`: Cálculo de custos de API
- `prompts.py`: Prompts versionados dos agentes (futuro - Task 2.6)

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

## Referências

- `README.md`: visão geral e execução.
- `docs/agents/overview.md`: mapa completo de agentes planejados.
- `docs/orchestration/orchestrator.md`: regras de decisão e estado.
- `docs/interface/cli.md`: expectativas de UX e logging.
- `docs/process/planning_guidelines.md`: governança de roadmap e práticas de planejamento.

**Versão:** 1.4
**Data:** 10/11/2025