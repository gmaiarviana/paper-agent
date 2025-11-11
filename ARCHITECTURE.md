# ARCHITECTURE.md

## Visão Geral

- Plataforma colaborativa com agentes de IA para apoiar produção de artigos científicos ponta a ponta.
- POC atual: validação de hipóteses com Orquestrador + Metodologista rodando sobre LangGraph.
- Interfaces priorizadas: CLI (automação com agentes) e Streamlit opcional para uso humano.

## Escopo Atual (POC)

- Entradas via CLI; respostas estruturadas do Orquestrador.
- Sistema multi-agente com 3 agentes: Orquestrador (roteamento), Estruturador (organização), Metodologista (validação).
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
│   ├── methodologist/     # Agente Metodologista (Épico 2)
│   │   ├── __init__.py
│   │   ├── state.py       # MethodologistState
│   │   ├── nodes.py       # analyze, ask_clarification, decide
│   │   ├── router.py      # route_after_analyze
│   │   ├── graph.py       # Construção do grafo
│   │   └── tools.py       # ask_user tool
│   ├── orchestrator/      # Agente Orquestrador (Épico 3.1)
│   │   ├── __init__.py
│   │   ├── state.py       # MultiAgentState
│   │   ├── nodes.py       # orchestrator_node
│   │   └── router.py      # route_from_orchestrator
│   ├── structurer/        # Agente Estruturador (Épico 3.2)
│   │   ├── __init__.py
│   │   └── nodes.py       # structurer_node
│   └── methodologist_knowledge.md  # Base de conhecimento micro
│
├── utils/                 # Utilitários e helpers
│   ├── __init__.py
│   ├── prompts.py         # Prompts versionados dos agentes
│   └── cost_tracker.py    # Cálculo de custos de API
│
├── cli/                   # Interface de linha de comando
│   ├── __init__.py
│   └── chat.py            # CLI interativo para testar Metodologista
│
├── app/                   # Interface Streamlit (futura)
│   └── __init__.py        # (Futuro: app.py)
│
├── tests/                 # Testes automatizados (pytest)
│   ├── __init__.py
│   ├── unit/              # Testes unitários (mocks, rápidos)
│   │   ├── __init__.py
│   │   ├── test_cost_tracker.py
│   │   ├── test_methodologist_state.py  # Testes do Metodologista
│   │   ├── test_ask_user_tool.py        # Testes da tool ask_user
│   │   ├── test_graph_nodes.py          # Testes dos nós do Metodologista
│   │   ├── test_orchestrator.py         # Testes do Orquestrador (Épico 3.1)
│   │   └── test_structurer.py           # Testes do Estruturador (Épico 3.2)
│   ├── integration/       # Testes de integração (API real)
│   │   └── __init__.py
│   └── conftest.py        # Fixtures compartilhadas (futuro)
│
├── scripts/               # Scripts de validação manual
│   ├── __init__.py
│   ├── validate_api.py    # Health check da API
│   ├── validate_state.py  # Validação do estado do Metodologista
│   ├── validate_ask_user.py  # Validação da tool ask_user
│   ├── validate_graph_nodes.py  # Validação dos nós do Metodologista
│   ├── validate_orchestrator.py  # Validação do Orquestrador (Épico 3.1)
│   ├── validate_structurer.py    # Validação do Estruturador (Épico 3.2)
│   └── validate_cli.py    # Validação do CLI (fluxo completo)
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
Opera em modo colaborativo: `approved`, `needs_refinement` (novo), `rejected`.

**Arquitetura:**
- Estado gerenciado por `MethodologistState` (TypedDict)
- Persistência de sessão via MemorySaver
- 3 nós do grafo: `analyze`, `ask_clarification`, `decide`
- Tool `ask_user` para interação via `interrupt()`
- Knowledge base micro sobre método científico

**Detalhes:** Ver `docs/agents/methodologist.md`

### Orquestrador (`agents/orchestrator/`)
Agente responsável por classificar maturidade de inputs e rotear para agentes especializados.

**Arquitetura (Épico 3.1 - Implementado):**
- Estado compartilhado gerenciado por `MultiAgentState` (TypedDict híbrido)
- Nó de classificação: `orchestrator_node` (usa LLM para detectar maturidade)
- Router condicional: `route_from_orchestrator` (roteia para Estruturador ou Metodologista)
- Classificações: "vague" (→ Estruturador), "semi_formed" (→ Metodologista), "complete" (→ Metodologista)

**Status:** Funcionalidade 3.1 implementada e testada.

**Detalhes:** Ver `docs/orchestration/multi_agent_architecture.md`

### Estruturador (`agents/structurer/`)
Agente responsável por organizar ideias vagas em questões de pesquisa estruturadas.

**Arquitetura (Épico 3.2 - Implementado):**
- Nó simples (não grafo completo nesta versão POC)
- `structurer_node`: Extrai contexto, problema e contribuição potencial de observações vagas
- Gera questão de pesquisa estruturada
- Comportamento colaborativo: não rejeita ideias, apenas organiza
- Não valida rigor científico (responsabilidade do Metodologista)
- Output estruturado em `MultiAgentState.structurer_output`

**Output:**
```python
{
    "structured_question": str,  # Questão de pesquisa estruturada
    "elements": {
        "context": str,           # Contexto da observação
        "problem": str,           # Problema identificado
        "contribution": str       # Possível contribuição acadêmica
    }
}
```

**Status:** Funcionalidade 3.2 implementada e testada. Próximo passo: Super-grafo (3.3)

**Detalhes:** Ver `docs/orchestration/multi_agent_architecture.md`

### CLI (`cli/chat.py`)
Loop interativo minimalista para testar o agente Metodologista.

**Funcionalidades:**
- Loop de entrada/processamento/saída
- Thread ID único por sessão
- Handling de interrupts (perguntas do agente)
- Comando `exit` para encerrar
- Exibição formatada de resultados (status + justificativa)

**Exemplo de uso:**
```bash
python cli/chat.py
```

**Detalhes:** Ver `docs/interface/cli.md` (futuro - melhorias de UX/logging)

### Utilitários (`utils/`)
- `cost_tracker.py`: Cálculo de custos de API
- `prompts.py`: Prompts versionados dos agentes (futuro - Task 2.6)

## Fluxo de Dados (resumo)

```
Usuário (CLI) → Orquestrador (classifica maturidade) →
  ├─ Input vago → Estruturador (organiza) ↔ Metodologista (valida/refina até 2x) → Usuário
  └─ Hipótese formada → Metodologista (valida) → Usuário
```

**Cenários:**
1. **Ideia vaga**: Orquestrador → Estruturador → Metodologista → Resultado
2. **Hipótese parcial/completa**: Orquestrador → Metodologista → Resultado

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
- Épico 4: Loop de refinamento no super-grafo, limite 2 iterações.

## Referências

- `README.md`: visão geral e execução.
- `docs/agents/overview.md`: mapa completo de agentes planejados.
- `docs/orchestration/orchestrator.md`: regras de decisão e estado.
- `docs/interface/cli.md`: expectativas de UX e logging.
- `docs/process/planning_guidelines.md`: governança de roadmap e práticas de planejamento.
- `docs/orchestration/refinement_loop.md`: especificação técnica do loop de refinamento colaborativo.

**Versão:** 1.7 (Épico 4 - Loop de Refinamento)
**Data:** 11/11/2025