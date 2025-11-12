# ARCHITECTURE.md

## Visão Geral

- Plataforma colaborativa com agentes de IA para apoiar produção de artigos científicos ponta a ponta.
- POC atual: validação de hipóteses com Orquestrador + Metodologista rodando sobre LangGraph.
- Interfaces priorizadas: CLI (automação com agentes) e Streamlit opcional para uso humano.

## Escopo Atual (POC)

- Entradas via CLI; respostas estruturadas do Orquestrador.
- Sistema multi-agente com 4 componentes: Orquestrador (roteamento), Estruturador (organização/refinamento), Metodologista (validação colaborativa), force_decision (decisão forçada).
- Loop de refinamento iterativo: até 2 refinamentos automáticos (V1 → V2 → V3).
- Modo colaborativo: Metodologista ajuda a construir hipóteses (3 status: approved, needs_refinement, rejected).
- Estado em memória gerenciado por LangGraph com rastreamento de versões (hypothesis_versions).
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

### Metodologista (`agents/methodologist/`)
Agente especializado em avaliar rigor científico de hipóteses usando LangGraph.
Opera em modo colaborativo: `approved`, `needs_refinement`, `rejected`.

**Arquitetura (Épico 4 - Modo Colaborativo):**
- Estado gerenciado por `MethodologistState` (grafo interno) ou `MultiAgentState` (super-grafo)
- Nós colaborativos: `decide_collaborative`, `force_decision_collaborative`
- Output estruturado com campo `improvements` (aspect, gap, suggestion)
- 3 status: approved (testável), needs_refinement (tem potencial), rejected (sem base científica)
- Usa Claude Sonnet 4 para maior confiabilidade
- Registra versões em `hypothesis_versions`

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
Agente responsável por organizar ideias vagas e refinar questões de pesquisa baseado em feedback.

**Arquitetura (Épico 4 - Refinamento Colaborativo):**
- Nó simples com 2 modos: estruturação inicial (V1) e refinamento (V2/V3)
- `structurer_node`: Detecta modo automaticamente baseado em `methodologist_output`
- **Modo 1 - Estruturação inicial:** Extrai contexto, problema, contribuição; gera questão V1
- **Modo 2 - Refinamento:** Recebe feedback do Metodologista (`improvements`), gera questão refinada V2/V3
- Usa prompt V2 (STRUCTURER_REFINEMENT_PROMPT_V1) para processar feedback
- Mantém essência da ideia original ao refinar
- Registra gaps endereçados (`addressed_gaps`)
- Incrementa `refinement_iteration` a cada refinamento

**Output (Épico 4):**
```python
{
    "structured_question": str,  # Questão de pesquisa estruturada/refinada
    "elements": {
        "context": str,           # Contexto da observação
        "problem": str,           # Problema identificado
        "contribution": str       # Possível contribuição acadêmica
    },
    "version": int,               # V1, V2 ou V3
    "addressed_gaps": list        # Gaps endereçados (apenas refinamento)
}
```

**Status:** Funcionalidades 3.2 e 4.3 implementadas. Loop de refinamento operacional.

**Detalhes:** Ver `docs/orchestration/refinement_loop.md`

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

## Fluxo de Dados (Épico 4 - Loop de Refinamento)

```
Usuário (CLI) → Orquestrador (classifica maturidade) →
  ├─ Input vago → Estruturador (V1) → Metodologista (needs_refinement?)
  │                      ↓ sim (iteration < max)           ↑
  │                      └─ Estruturador (V2) ─────────────┘
  │                                ↓ approved/rejected
  │                                END (resultado com histórico V1→V2)
  │
  └─ Hipótese formada → Metodologista (approved/rejected) → END

Decisão forçada (se iteration >= max_refinements):
  Estruturador (V3) → Metodologista (needs_refinement) → force_decision → END
```

**Cenários (Épico 4):**
1. **Ideia vaga + refinamento:** Orquestrador → Estruturador (V1) → Metodologista (needs_refinement) → Estruturador (V2) → Metodologista (approved) → END
2. **Hipótese direta:** Orquestrador → Metodologista (approved/rejected) → END
3. **Limite atingido:** ... → Metodologista (needs_refinement, iteration=2) → force_decision (approved/rejected) → END
4. **Sem potencial:** Estruturador (V1) → Metodologista (rejected) → END

Logs exibem: decisões, iterações, versões (V1/V2/V3), gaps identificados, refinamentos aplicados.

## Padrões Essenciais

- **Contratos em JSON** entre orquestrador e agentes (status, justificativa, sugestões).
- **Validação** via Pydantic e retries com backoff (até 3 tentativas) para chamadas Anthropic.
- **Transparência**: logs estruturados (`INFO` para decisões, `DEBUG` para reasoning completo).
- **Separação de responsabilidades**: agentes não se conhecem; orquestrador não faz análise científica.

## Decisões Técnicas Atuais

- Prioridade para CLI: permite automação com agentes (Claude Code / Cursor) sem dependência de navegador.
- Sem persistência, Docker ou vector DB durante a POC para acelerar iteração.
- Claude Sonnet 4 usado pelo Metodologista (modo colaborativo) para confiabilidade de JSON estruturado.
- Claude Haiku usado pelo Estruturador (custo-benefício para estruturação/refinamento).
- Loop de refinamento: limite padrão de 2 iterações (V1 → V2 → V3), configurável via `max_refinements`.
- Modo colaborativo: prefere `needs_refinement` ao invés de rejeitar diretamente (construir > criticar).

## Referências

- `README.md`: visão geral e execução.
- `docs/agents/overview.md`: mapa completo de agentes planejados.
- `docs/orchestration/orchestrator.md`: regras de decisão e estado.
- `docs/interface/cli.md`: expectativas de UX e logging.
- `docs/process/planning_guidelines.md`: governança de roadmap e práticas de planejamento.
- `docs/orchestration/refinement_loop.md`: especificação técnica do loop de refinamento colaborativo.

**Versão:** 2.0 (Épico 4 - Loop de Refinamento Colaborativo COMPLETO)
**Data:** 12/11/2025