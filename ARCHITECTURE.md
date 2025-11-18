# ARCHITECTURE.md

## Visão Geral

Plataforma colaborativa com agentes de IA para apoiar produção de artigos científicos ponta a ponta. Arquitetura atual: sistema multi-agente conversacional sobre LangGraph com Orquestrador facilitador, Estruturador organizador e Metodologista validador. Sistema mantém diálogo fluido onde usuário e agentes negociam caminho juntos. Interface web conversacional (Streamlit) como principal; CLI mantido para desenvolvimento e automação.

## Modelo Conceitual: Ontologia (Planejado)

> **Nota:** Para estrutura de dados completa e ontologia, consulte:
> - `docs/architecture/ontology.md` - O que é Conceito, Ideia, Argumento
> - `docs/architecture/idea_model.md` - Schema técnico de Ideia
> - `docs/architecture/concept_model.md` - Schema técnico de Conceito
> - `docs/architecture/argument_model.md` - Schema técnico de Argumento

O sistema está sendo projetado para trabalhar com a entidade **Ideia**, que representa pensamento articulado que evolui até se tornar argumento sólido. **Status atual:** Modelo cognitivo capturado em memória durante conversa. Persistência e gestão de ideias planejadas para Épicos 11-12 (ver `ROADMAP.md`).

**Estrutura planejada:**
```python
Idea:
  id: UUID
  title: "Cooperação humana via mitos"
  concepts: [concept_ids]      # Conceitos que usa (Épico 13)
  arguments: [argument_ids]    # Múltiplos argumentos (Épico 11)
  context: {source_type, source, ...}
  status: "exploring" | "structured" | "validated"
```

**Ontologia conceitual:**
- **Conceito:** Abstração reutilizável (vetor semântico) - Épico 13
- **Ideia:** Território (pensamento articulado) - Épico 12
- **Argumento:** Lente (claim + premises + assumptions) - Épico 11

## Super-Sistema: Core → Produtos

> **Nota:** Para arquitetura completa, consulte `docs/architecture/super_system_vision.md`.

Paper-agent é primeira aplicação de um **super-sistema** com core universal:
```
Core Universal (compartilhado):
  ├─ Ontologia (Conceito, Ideia, Argumento)
  ├─ Modelo Cognitivo (claim → premises)
  ├─ Agentes (Orquestrador, Estruturador, ...)
  └─ Infraestrutura (LangGraph, ChromaDB, SQLite)
            ↓
  ┌─────────┴──────────┬──────────────┐
  ↓                    ↓              ↓
Paper-Agent     Fichamento      Rede Social
(atual)         (futuro)        (futuro)
```

Produtos são **serviços desacoplados** que consomem core via APIs.

## Escopo Atual

**Sistema Multi-Agente Conversacional:**
- **Orquestrador:** Facilitador conversacional que mantém diálogo, detecta necessidades e sugere agentes
- **Estruturador:** Organiza ideias vagas e refina questões baseado em feedback estruturado
- **Metodologista:** Valida rigor científico em modo colaborativo (approved/needs_refinement/rejected)
- **Interface conversacional:** Web app Streamlit (ver `ROADMAP.md` - Épico 9)
- **Interface CLI:** Ferramenta de desenvolvimento (congelada, backend compartilhado)

**Estado compartilhado:**
- MultiAgentState híbrido (campos compartilhados + específicos por agente)
- Rastreamento de iterações de refinamento
- Argumento focal implícito (reconstruído a cada turno via histórico)

**Infraestrutura:**
- Python 3.11+, Anthropic API, LangGraph
- Configuração externa de agentes (YAML)
- EventBus para comunicação CLI ↔ Dashboard
- MemoryManager para registro de metadados

**Detalhes de fluxo:** Ver `docs/orchestration/multi_agent_architecture.md`

---

## Interfaces Mantidas

O sistema oferece **duas interfaces web** com propósitos distintos:

### Chat Web (`app/chat.py`) - Experiência Principal
- Interface conversacional para usuários finais
- Chat fluido + bastidores opcionais (reasoning inline)
- Persistência de sessão via SqliteSaver (checkpoints LangGraph)
- **Porta:** :8501

### Dashboard (`app/dashboard.py`) - Debug/Monitoring
- Visão global de todas as sessões ativas
- Timeline de eventos por sessão
- Estatísticas agregadas (tokens, custos, agentes)
- Auto-refresh configurável (padrão: 2s)
- **Porta:** :8501 (mesmo Streamlit, apps separados)

### CLI (`cli/chat.py`) - Desenvolvimento
- Interface de linha de comando para automação
- Backend compartilhado (LangGraph + EventBus)
- Funcionalidade congelada (novas features → web)
- **Uso:** Testes, debugging, scripts

**Backend Compartilhado:**
- Todas as interfaces usam mesmo LangGraph + EventBus
- Chat e Dashboard consomem mesmos eventos (JSON files)
- CLI publica eventos consumidos pelo Dashboard

**Decisão Arquitetural:**
- Chat: UX rica, foco em uma sessão
- Dashboard: Telemetria, visão global
- CLI: Automação, sem depender de navegador
- Custo de manutenção baixo (EventBus já existe)

---

## Orquestrador Conversacional

Facilitador conversacional que mantém diálogo fluido, detecta necessidades, oferece opções ao usuário e adapta-se a mudanças de direção. Reconstrói argumento focal a cada turno analisando histórico da conversa.

**Detalhes:** Ver `docs/orchestration/conversational_orchestrator.md`

## Orquestrador Socrático

Evolução do Orquestrador Conversacional que adiciona capacidade de exposição de suposições implícitas através de contra-perguntas socráticas.

**Detalhes:** Ver `ROADMAP.md` (Épico 10) e `docs/orchestration/socratic_orchestrator.md`

## Estado Compartilhado

MultiAgentState híbrido gerencia campos compartilhados (mensagens, histórico conversacional) e específicos por agente (estruturação, validação). Rastreia iterações de refinamento durante sessão ativa.

**Detalhes:** Ver `docs/orchestration/multi_agent_architecture.md`

## Modelo Cognitivo

Sistema captura evolução do pensamento do usuário através de modelo cognitivo explícito com campos: `claim`, `premises`, `assumptions`, `open_questions`, `contradictions`, `solid_grounds`, `context`.

**Detalhes completos:** Ver `docs/vision/cognitive_model.md`

**Responsabilidades:**
- Orquestrador: detecta suposições, extrai claim, atualiza contexto
- Estruturador: organiza premises, torna explícito o implícito
- Metodologista: valida lógica, aponta contradições
- Pesquisador (futuro): transforma dúvidas em evidências

**Status atual:** Modelo cognitivo capturado em memória (MultiAgentState) durante conversa. Para evolução planejada (persistência, gestão de ideias), ver `ROADMAP.md` (Épicos 11-12).

## Stack Técnico

> **Nota:** Para detalhes completos, consulte `docs/architecture/tech_stack.md`.

**Resumo:**
- **Runtime:** Python 3.11+
- **Orquestração:** LangGraph, LangChain Anthropic
- **LLM:** Claude 3.5 Haiku/Sonnet
- **Dados estruturados:** SQLite (local) → PostgreSQL (cloud futuro)
- **Vetores semânticos:** ChromaDB (local) → Qdrant (cloud futuro)
- **Embeddings:** sentence-transformers (local, gratuito)
- **Interface Web:** Streamlit

### Persistência

**Atual:**
- **SqliteSaver (LangGraph):** Checkpoints de conversa (arquivo `checkpoints.db`)
- **Localização:** Arquivos locais em `./data/`

**Futuro (MVP/Produção):**
- **PostgreSQL:** Migração quando escalar
- **Schema compatível:** Mesmas queries funcionam em ambos
- **Estratégia documentada:** Ver `docs/architecture/persistence_foundation.md`

**Decisão:** Começar simples (SQLite) e migrar quando necessário. Evitar over-engineering prematuro.

## Configuração Externa de Agentes

Sistema de configuração dinâmica que permite definir prompts, modelos LLM e limites de contexto via arquivos YAML externos.

**Detalhes:** Ver `ROADMAP.md` (Épico 6) para funcionalidades completas.

**Arquitetura:**
- **Arquivos YAML**: `config/agents/{agent_name}.yaml` - um por agente
- **Loader**: `agents/memory/config_loader.py` - carrega e valida configs em runtime
- **Integração**: Nós carregam configs YAML ao executar, com fallback para prompts hard-coded

## Registro de Memória e Metadados

Sistema de captura e agregação de tokens, custos e metadados de execução por agente.

**Detalhes:** Ver `ROADMAP.md` (Épico 6) para funcionalidades completas.

**Arquitetura:**
- **ExecutionTracker**: Captura tokens de AIMessage e registra no MemoryManager
- **MemoryManager**: Armazena histórico de execuções por sessão e agente
- **CostTracker**: Calcula custos baseado em tokens e modelo LLM
- **Integração**: Nós do LangGraph registram métricas após cada invocação LLM

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
│   ├── dashboard.py       # Dashboard de visualização de eventos (Épico 5.1)
│   ├── chat.py            # Chat conversacional principal (Épico 9 - scaffold criado)
│   └── components/        # Componentes reutilizáveis (Épico 9)
│       ├── __init__.py
│       ├── chat_input.py     # Input de mensagens (esqueleto)
│       ├── chat_history.py   # Histórico de conversa (esqueleto)
│       ├── backstage.py      # Painel "Bastidores" (esqueleto)
│       ├── sidebar.py        # Lista de sessões (esqueleto)
│       └── storage.py        # Persistência localStorage (funcional - 9.9)
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
    ├── architecture/      # Decisões técnicas, modelos de dados
    ├── interface/         # Especificações de interface
    ├── orchestration/     # Orquestração e estado
    ├── vision/            # Visão de produto
    │   ├── vision.md
    │   ├── cognitive_model.md
    │   ├── conversation_patterns.md
    │   └── agent_personas.md  (Épico 16+)
    ├── products/          # Produtos específicos (paper-agent, fichamento)
    └── process/           # Desenvolvimento, testes
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

## Visão Futura

> **Nota:** Para fases detalhadas de migração, consulte `docs/architecture/migration_strategy.md` e `ROADMAP.md`.

Sistema atual trabalha com modelo cognitivo em memória. Planejado para Épicos 11+:
- **Épico 11:** Modelagem Cognitiva (Argument como entidade persistida)
- **Épico 12:** Gestão de Ideias (múltiplas ideias, sidebar, alternância)
- **Épico 13:** Entidade Concept (vetores semânticos, ChromaDB)
- **Épico 14:** Melhorias de UX (polimento de interface)
- **Épico 15:** Agentes Avançados (Pesquisador, Escritor, Crítico)

**Status:** Épicos 9-10 concluídos. Épicos 11+ planejados (ver `ROADMAP.md` para detalhes).

## Padrões Essenciais

- **Contratos em JSON** entre orquestrador e agentes (status, justificativa, sugestões)
- **Validação** via Pydantic e retries com backoff (até 3 tentativas) para chamadas Anthropic
- **Transparência:** logs estruturados (`INFO` para decisões, `DEBUG` para reasoning completo)
- **Separação de responsabilidades:** agentes não se conhecem; orquestrador não faz análise científica

## Referências

**Arquitetura:**
- `docs/architecture/ontology.md` - Ontologia (Conceito/Ideia/Argumento)
- `docs/architecture/super_system_vision.md` - Super-sistema: Core → Produtos
- `docs/architecture/idea_model.md` - Estrutura de dados Ideia
- `docs/architecture/concept_model.md` - Estrutura de dados Conceito
- `docs/architecture/argument_model.md` - Estrutura de dados Argumento
- `docs/architecture/tech_stack.md` - ChromaDB, SQLite, embeddings
- `docs/architecture/migration_strategy.md` - Fases de migração

**Visão de Produto:**
- `docs/vision/vision.md` - Visão de produto, tipos de artigo
- `docs/vision/cognitive_model.md` - Modelo cognitivo e evolução

**Orquestração:**
- `docs/orchestration/multi_agent_architecture.md` - Arquitetura multi-agente
- `docs/orchestration/conversational_orchestrator.md` - Orquestrador conversacional

**Produtos:**
- `docs/products/paper_agent.md` - Paper-agent (produto atual)
- `docs/products/fichamento.md` - Fichamento (produto futuro)
