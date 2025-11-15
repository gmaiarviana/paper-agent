# ARCHITECTURE.md

## Visão Geral

Plataforma colaborativa com agentes de IA para apoiar produção de artigos científicos ponta a ponta. Arquitetura atual: sistema multi-agente conversacional sobre LangGraph com Orquestrador facilitador, Estruturador organizador e Metodologista validador. Sistema mantém diálogo fluido onde usuário e agentes negociam caminho juntos. Interface web conversacional (Streamlit) como principal; CLI mantido para desenvolvimento e automação.

## Entidade Central: Tópico/Ideia

O sistema trabalha com a entidade **Tópico**, que representa uma ideia em evolução até se tornar artigo.

**Modelo conceitual (detalhes em `docs/product/vision.md` - Seção 4):**
```python
Topic:
  id: str              # UUID único
  title: str           # "Impacto de LLMs em produtividade"
  article_type: str    # Ver tipos abaixo
  stage: str           # Ver estágios abaixo
  created_at: datetime
  updated_at: datetime
  artifacts: List[Artifact]  # outline, papers, drafts, decisions
  thread_id: str       # LangGraph thread (para recuperar sessão)
```

**Tipos de artigo suportados:** `empirical`, `review`, `theoretical`, `case_study`, `meta_analysis`, `methodological`

**Estágios de maturidade:** `ideation` → `hypothesis` → `methodology` → `research` → `writing` → `review` → `done`

**Evolução fluida:** Sistema detecta `stage` automaticamente; usuário pode voltar etapas; tipo pode ser inferido ou mudar ao longo da conversa.

## Escopo Atual

**Sistema Multi-Agente Conversacional:**
- **Orquestrador:** Facilitador conversacional que mantém diálogo, detecta necessidades e sugere agentes
- **Estruturador:** Organiza ideias vagas e refina questões baseado em feedback estruturado
- **Metodologista:** Valida rigor científico em modo colaborativo (approved/needs_refinement/rejected)
- **Interface conversacional:** Web app Streamlit (Épico 9)
- **Interface CLI:** Ferramenta de desenvolvimento (congelada, backend compartilhado)

**Estado compartilhado:**
- MultiAgentState híbrido (campos compartilhados + específicos por agente)
- Versionamento de hipóteses (V1 → V2 → V3)
- Rastreamento de iterações de refinamento
- Argumento focal explícito (intent, subject, population, metrics, article_type)

**Infraestrutura:**
- Python 3.11+, Anthropic API, LangGraph
- Configuração externa de agentes (YAML)
- EventBus para comunicação CLI ↔ Dashboard
- MemoryManager para registro de metadados

**Detalhes de fluxo:** Ver `docs/orchestration/multi_agent_architecture.md`

## Orquestrador Conversacional

Facilitador conversacional que mantém diálogo fluido, detecta necessidades, oferece opções ao usuário e adapta-se a mudanças de direção. Extrai e atualiza argumento focal a cada turno, provoca reflexão sobre lacunas e detecta emergência de novo estágio.

**Detalhes:** Ver `docs/orchestration/conversational_orchestrator.md`

## Estado Compartilhado

MultiAgentState híbrido gerencia campos compartilhados (mensagens, argumento focal) e específicos por agente (estruturação, validação). Suporta versionamento de hipóteses (V1 → V2 → V3) e rastreamento de iterações de refinamento.

**Detalhes:** Ver `docs/orchestration/multi_agent_architecture.md`

## Stack Técnico

- **Runtime:** Python 3.11+
- **Orquestração:** LangGraph, LangChain Anthropic
- **LLM:** Claude 3.5 Haiku (custo-benefício) / Sonnet (tarefas complexas)
- **Validação:** Pydantic, PyYAML para configs
- **Interface Web:** Streamlit (ver spec técnica completa em `docs/interface/web.md`)
- **CLI:** Ferramenta de desenvolvimento (backend compartilhado com web)
- **Utilitários:** `colorama` para logging colorido, `python-dotenv` para variáveis

## Configuração Externa de Agentes (Épico 6.1)

Sistema de configuração dinâmica que permite definir prompts, modelos LLM e limites de contexto via arquivos YAML externos.

**Arquitetura:**
- **Arquivos YAML**: `config/agents/{agent_name}.yaml` - um por agente (orchestrator, structurer, methodologist)
- **Loader**: `agents/memory/config_loader.py` - carrega e valida configs em runtime
- **Validator**: `agents/memory/config_validator.py` - valida schema dos YAMLs
- **Bootstrap**: Validação automática no `create_multi_agent_graph()`

**Funcionalidades:**
- Prompts carregados do YAML substituem prompts hard-coded em `utils/prompts.py`
- Modelos LLM configuráveis por agente (Haiku para performance, Sonnet para precisão)
- Limites de contexto (`max_input_tokens`, `max_output_tokens`, `max_total_tokens`) por agente
- **Fallback automático**: Se YAML falhar, nós usam prompts hard-coded para não quebrar sistema
- **Mensagens em PT-BR**: Todos os erros reportados em português

**Integração runtime:**
- `orchestrator_node`: Carrega `config/agents/orchestrator.yaml` ao executar
- `structurer_node`: Carrega `config/agents/structurer.yaml` ao executar (ambos modos: inicial e refinamento)
- `decide_collaborative` e `force_decision_collaborative`: Carregam `config/agents/methodologist.yaml` ao executar
- `create_multi_agent_graph`: Valida que todos YAMLs obrigatórios existem no bootstrap

## Registro de Memória e Metadados (Épico 6.2)

Sistema de captura e agregação de tokens, custos e metadados de execução por agente.

**Arquitetura:**
- **ExecutionTracker**: `agents/memory/execution_tracker.py` - helper para capturar tokens de AIMessage e registrar no MemoryManager
- **MemoryManager**: `agents/memory/memory_manager.py` - armazena histórico de execuções por sessão e agente
- **CostTracker**: `utils/cost_tracker.py` - calcula custos baseado em tokens e modelo LLM
- **Integração**: Nós do LangGraph recebem config com `memory_manager` e registram após cada invocação LLM

**Funcionalidades:**
- Captura automática de tokens de respostas LLM (LangChain AIMessage)
- Cálculo de custos integrado (suporta Haiku, Sonnet, Opus)
- Registro de metadados personalizados por agente (classificação, modo, versão, etc)
- Agregação de totais por agente e por sessão
- Export JSON serializável para integração com dashboard
- Passagem opcional via config - não quebra nós existentes

**Nós instrumentados:**
- `orchestrator_node` (v2.1): Registra classificação de maturidade + tokens
- `structurer_node` (v3.1): Registra estruturação inicial (V1) e refinamentos (V2/V3) + tokens
- `decide_collaborative` (v3.1): Registra decisões colaborativas (approved/needs_refinement/rejected) + tokens
- `force_decision_collaborative` (v3.1): Registra decisões forçadas após limite + tokens

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
├── config/                # Configurações externas (Épico 6)
│   └── agents/            # Configs YAML por agente
│       ├── orchestrator.yaml    # Prompt, modelo, limites do Orquestrador
│       ├── structurer.yaml      # Prompt, modelo, limites do Estruturador
│       └── methodologist.yaml   # Prompt, modelo, limites do Metodologista
│
├── agents/                # Agentes especializados
│   ├── __init__.py
│   ├── methodologist/     # Agente Metodologista
│   │   ├── __init__.py
│   │   ├── state.py       # MethodologistState
│   │   ├── nodes.py       # analyze, ask_clarification, decide
│   │   ├── router.py      # route_after_analyze
│   │   ├── graph.py       # Construção do grafo
│   │   └── tools.py       # ask_user tool
│   ├── orchestrator/      # Agente Orquestrador
│   │   ├── __init__.py
│   │   ├── state.py       # MultiAgentState
│   │   ├── nodes.py       # orchestrator_node
│   │   └── router.py      # route_from_orchestrator
│   ├── structurer/        # Agente Estruturador
│   │   ├── __init__.py
│   │   └── nodes.py       # structurer_node
│   ├── memory/            # Sistema de memória e configuração
│   │   ├── __init__.py
│   │   ├── config_loader.py      # Carregamento de configs YAML
│   │   ├── config_validator.py   # Validação de schema YAML
│   │   ├── execution_tracker.py   # Helper para captura de tokens
│   │   └── memory_manager.py     # Gestão de memória por agente
│   └── multi_agent_graph.py      # Super-grafo
│
├── utils/                 # Utilitários e helpers
│   ├── __init__.py
│   ├── prompts.py         # Prompts versionados dos agentes
│   ├── cost_tracker.py    # Cálculo de custos de API
│   ├── event_models.py    # Models Pydantic para eventos
│   └── event_bus.py       # EventBus para Dashboard
│
├── cli/                   # Interface de linha de comando
│   ├── __init__.py
│   └── chat.py            # CLI interativo (integrado com EventBus)
│
├── app/                   # Interface Web Conversacional
│   ├── __init__.py
│   ├── dashboard.py       # DEPRECATED: Visualização de eventos
│   ├── chat.py            # Chat conversacional principal
│   ├── components/        # Componentes reutilizáveis
│   │   ├── __init__.py
│   │   ├── chat_input.py     # Input de mensagens
│   │   ├── chat_history.py   # Histórico de conversa
│   │   ├── backstage.py      # Painel "Bastidores"
│   │   ├── timeline.py       # Timeline de agentes
│   │   └── sidebar.py        # Lista de sessões
│   └── sse.py             # Server-Sent Events endpoint
│
├── tests/                 # Testes automatizados (pytest)
│   ├── __init__.py
│   ├── unit/              # Testes unitários (mocks, rápidos)
│   │   ├── __init__.py
│   │   ├── test_cost_tracker.py
│   │   ├── test_methodologist_state.py
│   │   ├── test_ask_user_tool.py
│   │   ├── test_graph_nodes.py
│   │   ├── test_orchestrator.py
│   │   ├── test_structurer.py
│   │   ├── test_event_models.py
│   │   ├── test_event_bus.py
│   │   ├── test_config_loader.py
│   │   └── test_memory_manager.py
│   └── integration/       # Testes de integração (API real)
│       └── __init__.py
│
├── scripts/               # Scripts de validação manual
│   ├── __init__.py
│   ├── health_checks/            # Sanidade de ambiente e configs
│   │   ├── validate_api.py
│   │   ├── validate_agent_config.py
│   │   ├── validate_runtime_config_simple.py
│   │   ├── validate_syntax.py
│   │   ├── validate_system_prompt.py
│   │   ├── validate_execution_tracker.py
│   │   └── validate_orchestrator_json_parsing.py
│   ├── flows/                    # Cenários completos (consomem API)
│   │   ├── validate_cli.py
│   │   ├── validate_cli_integration.py
│   │   ├── validate_dashboard.py
│   │   ├── validate_memory_integration.py
│   │   ├── validate_multi_agent_flow.py
│   │   ├── validate_orchestrator.py
│   │   ├── validate_refinement_loop.py
│   │   ├── validate_structurer.py
│   │   ├── validate_structurer_refinement.py
│   │   └── validate_build_context.py
│   └── debug/                    # Diagnóstico ad hoc
│       ├── debug_multi_agent.py
│       └── check_events.py
│
└── docs/                  # Documentação detalhada por domínio
    ├── agents/            # Especificações de agentes
    │   ├── overview.md
    │   └── methodologist.md
    ├── interface/         # Especificações de interface
    │   ├── cli.md
    │   ├── conversational_cli.md
    │   └── web.md
    ├── orchestration/     # Orquestração e estado
    │   ├── conversational_orchestrator.md
    │   ├── multi_agent_architecture.md
    │   ├── orchestrator.md
    │   └── refinement_loop.md
    └── product/           # Visão de produto
        └── vision.md
```

## Componentes Principais

### Metodologista (`agents/methodologist/`)
Agente especializado em avaliar rigor científico de hipóteses usando LangGraph. Opera em modo colaborativo: `approved`, `needs_refinement`, `rejected`.

**Detalhes:** Ver `docs/agents/methodologist.md`

### Orquestrador (`agents/orchestrator/`)
Agente responsável por facilitar conversa e coordenar chamadas a agentes especializados. Facilitador conversacional que negocia caminho com usuário.

**Detalhes:** Ver `docs/orchestration/conversational_orchestrator.md`

### Estruturador (`agents/structurer/`)
Agente responsável por organizar ideias vagas e refinar questões de pesquisa baseado em feedback. Nó simples com 2 modos: estruturação inicial (V1) e refinamento (V2/V3).

**Detalhes:** Ver `docs/orchestration/refinement_loop.md`

### Interface Web (`app/`)
Interface web conversacional (Streamlit) como experiência principal do sistema. Chat fluido com reasoning dos agentes visível ("Bastidores"), métricas inline e streaming de eventos. Componentes: chat, bastidores, timeline, sidebar. Eventos consumidos via polling (POC) ou SSE (MVP).

**Detalhes:** Ver `docs/interface/web.md`

### CLI (`cli/chat.py`)
Loop interativo minimalista para desenvolvimento e automação. Backend compartilhado com interface web.

**Detalhes:** Ver `docs/interface/cli.md` e `docs/interface/conversational_cli.md`

## Decisões Técnicas Atuais

- **Prioridade para CLI:** Permite automação com agentes (Claude Code / Cursor) sem dependência de navegador
- **Sem persistência, Docker ou vector DB durante POC:** Para acelerar iteração
- **Claude Sonnet 4 usado pelo Metodologista:** Para confiabilidade de JSON estruturado
- **Claude Haiku usado pelo Estruturador:** Custo-benefício para estruturação/refinamento
- **Refinamento sob demanda:** Loop não é automático; usuário decide quando refinar baseado em feedback do Metodologista. Sem limite fixo de iterações
- **Transição para conversação adaptativa:** Ver `docs/orchestration/conversational_orchestrator.md` para padrões de conversa vs classificação
- **EventBus para visualização:** CLI emite eventos consumidos por Dashboard Streamlit via arquivos JSON temporários
- **Modo colaborativo:** Prefere `needs_refinement` ao invés de rejeitar diretamente (construir > criticar)

## Padrões Essenciais

- **Contratos em JSON** entre orquestrador e agentes (status, justificativa, sugestões)
- **Validação** via Pydantic e retries com backoff (até 3 tentativas) para chamadas Anthropic
- **Transparência:** logs estruturados (`INFO` para decisões, `DEBUG` para reasoning completo)
- **Separação de responsabilidades:** agentes não se conhecem; orquestrador não faz análise científica

## Referências

- `README.md`: visão geral e execução
- `ROADMAP.md`: status de épicos e funcionalidades
- `docs/product/vision.md`: visão de produto, tipos de artigo, jornada do usuário
- `docs/agents/overview.md`: mapa completo de agentes planejados
- `docs/agents/methodologist.md`: especificação do Metodologista
- `docs/orchestration/conversational_orchestrator.md`: especificação do Orquestrador Conversacional
- `docs/orchestration/multi_agent_architecture.md`: arquitetura multi-agente e estado compartilhado
- `docs/orchestration/refinement_loop.md`: especificação técnica do loop de refinamento colaborativo
- `docs/interface/web.md`: especificação da interface web conversacional
- `docs/interface/cli.md`: especificação da CLI
- `docs/interface/conversational_cli.md`: especificação da CLI conversacional
- `planning_guidelines.md`: governança de roadmap e práticas de planejamento
