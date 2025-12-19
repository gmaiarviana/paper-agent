# ARCHITECTURE.md

## Visão Geral

Plataforma colaborativa com agentes de IA para apoiar produção de artigos científicos ponta a ponta. Arquitetura atual: sistema multi-agente conversacional sobre LangGraph com Orquestrador facilitador, Estruturador organizador e Metodologista validador. Sistema mantém diálogo fluido onde usuário e agentes negociam caminho juntos. Interface web conversacional (Streamlit) como principal; CLI mantido para desenvolvimento e automação.

## Entidade Central: Ideia

> **Nota:** Para estrutura de dados completa e ontologia, consulte:
> - `core/docs/architecture/data-models/ontology.md` - O que é Conceito, Ideia, Argumento
> - `core/docs/architecture/data-models/idea_model.md` - Schema técnico de Ideia
> - `core/docs/architecture/data-models/concept_model.md` - Schema técnico de Conceito
> - `core/docs/architecture/data-models/argument_model.md` - Schema técnico de Argumento

O sistema trabalha com a entidade **Ideia**, que representa pensamento articulado que evolui até se tornar argumento sólido.

**Estrutura básica:**
```python
Idea:
  id: UUID
  title: "Cooperação humana via mitos"
  concepts: [concept_ids]      # Conceitos que usa
  arguments: [argument_ids]    # Múltiplos argumentos (lentes)
  context: {source_type, source, ...}
  status: "exploring" | "structured" | "validated"
```

**Ontologia:**
- **Conceito:** Abstração reutilizável (vetor semântico)
- **Ideia:** Território (pensamento articulado)
- **Argumento:** Lente (claim + proposicoes com solidez variável)

**Evolução fluida:** Sistema detecta status automaticamente; usuário pode voltar etapas; múltiplos argumentos por ideia.

## Gestão de Ideias

Sistema gerencia ideias cristalizadas durante conversas com navegação em três espaços distintos (Épico 14):

**Conversas (Sidebar):**
- Últimas 5 conversas recentes com timestamp relativo
- Alternar entre conversas (restaura contexto completo via SqliteSaver)
- Botões para páginas dedicadas: "Meus Pensamentos" e "Catálogo"

**Meus Pensamentos (Página `/pensamentos`):**
- Grid de cards mostrando ideias cristalizadas
- Preview: título, status, # argumentos, # conceitos
- Busca + filtros (status, conceitos)
- Página dedicada da ideia (`/pensamentos/{idea_id}`): argumentos versionados, conceitos usados, conversas relacionadas

**Catálogo (Página `/catalogo`):**
- Biblioteca de conceitos técnicos reutilizáveis
- Busca semântica via embeddings
- Mostra ideias que usam cada conceito

**Filosofia:** Conversas = processo (volátil), Ideias = cristalização (permanente), Conceitos = abstração (biblioteca).

**Persistência Silenciosa:** Sistema avalia a cada mensagem se deve criar/atualizar snapshot do argumento. Para estratégia detalhada, ver `core/docs/architecture/patterns/snapshots.md`.

Ver: `products/revelar/docs/interface/navigation_philosophy.md` para filosofia completa.

## Super-Sistema: Core → Produtos

> **Nota:** Para arquitetura completa, consulte `core/docs/architecture/vision/super_system.md`.

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

**Produtos atuais/futuros:**
- **Revelar:** Clareza de pensamento - estruturar ideias nebulosas em conceitos claros (atual)
- **Prisma Verbal:** Extração de informação - processar literatura e extrair proposições (futuro próximo)
- **Produtor Científico:** Produção de conteúdo - ideia madura → manuscrito/artigo (futuro)

## Escopo Atual

**Sistema Multi-Agente Conversacional:**
- **Orquestrador:** Facilitador conversacional que mantém diálogo, detecta necessidades e sugere agentes
- **Estruturador:** Organiza ideias vagas e refina questões baseado em feedback estruturado
- **Metodologista:** Valida rigor científico em modo colaborativo (approved/needs_refinement/rejected)
- **Interface conversacional:** Web app Streamlit
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

**Detalhes de fluxo:** Ver `core/docs/architecture/agents/multi_agent/`

---

## Interfaces Mantidas

O sistema oferece **duas interfaces web** com propósitos distintos:

### Chat Web (`products/revelar/app/chat.py`) - Experiência Principal
- Interface conversacional para usuários finais
- Chat fluido + bastidores opcionais (reasoning inline)
- Sidebar com últimas 5 conversas (SqliteSaver backend)
- Navegação em três espaços: Conversas, Meus Pensamentos, Catálogo (Épico 14)
- Persistência entre visitas (sem autenticação - sessões compartilhadas)
- **Porta:** :8501

### Dashboard (`products/revelar/app/dashboard.py`) - Debug/Monitoring
- Visão global de todas as sessões ativas
- Timeline de eventos por sessão
- Estatísticas agregadas (tokens, custos, agentes)
- Auto-refresh configurável (padrão: 2s)
- **Porta:** :8501 (mesmo Streamlit, apps separados)

### CLI (`core/tools/cli/chat.py`) - Desenvolvimento
- Interface de linha de comando para automacao
- Backend compartilhado (LangGraph + EventBus)
- Funcionalidade congelada (novas features -> web)
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

Facilitador conversacional que mantém diálogo fluido, detecta necessidades, oferece opções ao usuário e adapta-se a mudanças de direção. Extrai e atualiza argumento focal a cada turno, provoca reflexão sobre lacunas e detecta emergência de novo estágio.

**Detalhes:** Ver `core/docs/architecture/agents/orchestrator/conversational/README.md`

## Orquestrador Socrático

Evolução do Orquestrador Conversacional que adiciona capacidade de exposição de suposições implícitas através de contra-perguntas socráticas. Detecta 5 categorias de assumptions (métrica vaga, população vaga, baseline ausente, causalidade assumida, generalização excessiva), escala profundidade de provocação em 3 níveis conforme resistência do usuário, e determina timing apropriado de provocação (quando provocar vs quando apenas explorar).

**Detalhes:** Ver `core/docs/architecture/agents/orchestrator/socratic.md`

**Relacionamento:** Socrático é extensão do Conversacional. Conversacional provê base de análise contextual e argumento focal; Socrático adiciona provocação estruturada sobre assumptions.

## Estado Compartilhado

MultiAgentState híbrido gerencia campos compartilhados (mensagens, argumento focal) e específicos por agente (estruturação, validação). Suporta versionamento de hipóteses (V1 → V2 → V3) e rastreamento de iterações de refinamento.

**Detalhes:** Ver `core/docs/architecture/agents/multi_agent/`

## Modelo Cognitivo

Sistema captura evolução do pensamento do usuário através de modelo cognitivo explícito com campos: `claim`, `premises`, `assumptions`, `open_questions`, `contradictions`, `solid_grounds`, `context`.

**Detalhes completos:** Ver `core/docs/vision/cognitive_model/`

**Responsabilidades:**
- Orquestrador: detecta suposições, extrai claim, atualiza contexto
- Estruturador: organiza premises, torna explícito o implícito
- Metodologista: valida lógica, aponta contradições
- Pesquisador (futuro): transforma dúvidas em evidências

**Implementação:**
- **Schema Pydantic:** `core/agents/models/cognitive_model.py` - CognitiveModel, Contradiction, SolidGround
- **Persistência SQLite:** `core/agents/database/` - DatabaseManager com tabelas ideas e arguments
- **Versionamento:** Auto-incremento de versões (V1, V2, V3...) por idea
- **Maturidade:** `core/agents/persistence/snapshot_manager.py` - Detecção via LLM e snapshots automáticos (ver `core/docs/architecture/patterns/snapshots.md`)
- **Checklist:** `core/agents/checklist/progress_tracker.py` - Rastreamento adaptativo por tipo de artigo
- **Banco de dados:** `data/data.db` - Separado de checkpoints.db (LangGraph)

**Status de integração (Épico 9):** ✅ Concluído
- ✅ Schema implementado (`CognitiveModel`)
- ✅ SnapshotManager implementado (avalia maturidade via LLM)
- ✅ **Épico 9.1:** Orquestrador atualizar cognitive_model no state a cada turno
- ✅ **Épico 9.2:** Passar active_idea_id via config do LangGraph
- ✅ **Épico 9.3:** Integrar SnapshotManager no fluxo conversacional (persistência automática)
- ✅ **Épico 9.4:** Indicador de solidez no painel Contexto (`calculate_solidez()`)

## Integração Observer (Épico 12)

Observer integrado ao grafo multi-agente via callback assíncrono após execução do Orchestrator.

**Arquitetura:**
- **Callback em background:** Observer processa cada turno em thread daemon após `orchestrator_node` completar
- **Não bloqueante:** Latência do usuário não aumenta (Observer roda em paralelo, <3s)
- **Atualização de state:** `state["cognitive_model"]` atualizado com análise semântica
- **Publicação de eventos:** `CognitiveModelUpdatedEvent` via EventBus para Timeline

**Componentes:**
- **Callback:** `_create_observer_callback()` em `core/agents/multi_agent_graph.py`
- **Contexto:** `_build_cognitive_model_context()` em `core/agents/orchestrator/nodes.py`
- **Timeline:** `render_observer_section()` em `products/revelar/app/components/backstage/timeline.py`

**Fluxo:**
```
User Input → Orchestrator → Response ao usuário
                  ↓
            [Background Thread]
                  ↓
              Observer
                  ↓
         cognitive_model atualizado
                  ↓
         Evento publicado (EventBus)
                  ↓
         Timeline atualizada (próximo render)
```

**Status (Épico 12):** ✅ Concluído
- ✅ **12.1:** Callback assíncrono via threading (daemon)
- ✅ **12.2:** CognitiveModel no prompt do Orquestrador
- ✅ **12.3:** Timeline visual com seção "👁️ Observador"
- ✅ **12.4:** 28 testes passando (unit + integration)

## Stack Técnico

> **Nota:** Para detalhes completos, consulte `core/docs/architecture/infrastructure/tech_stack.md`.

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
- **SQLite customizado:** Entidades de domínio em `data/data.db`:
  - Tabela `ideas`: id, title, status, current_argument_id (FK)
  - Tabela `arguments`: id, idea_id (FK), claim, premises, assumptions, open_questions, contradictions, solid_grounds, context, version
  - Versionamento automático (V1, V2, V3...) via UNIQUE constraint (idea_id, version)
  - Triggers para updated_at automático
  - Views otimizadas para JOIN idea + argumento focal
- **DatabaseManager singleton:** `core/agents/database/manager.py` - Orquestrador que delega para CRUDs especializados
  - `core/agents/database/ideas_crud.py` - CRUD operations para Ideas
  - `core/agents/database/arguments_crud.py` - CRUD operations para Arguments
- **Localização:** Arquivos locais em `./data/`

**Futuro (MVP/Produção):**
- **PostgreSQL:** Migração quando escalar
- **Schema compatível:** Mesmas queries funcionam em ambos
- **Estratégia documentada:** Ver `core/docs/architecture/data-models/persistence.md`

**Decisão:** Começar simples (SQLite) e migrar quando necessário. Evitar over-engineering prematuro.

## Configuração Externa de Agentes

Sistema de configuração dinâmica que permite definir prompts, modelos LLM e limites de contexto via arquivos YAML externos.

**Arquitetura:**
- **Arquivos YAML**: `core/config/agents/{agent_name}.yaml` - um por agente (orchestrator, structurer, methodologist)
- **Loader**: `core/agents/memory/config_loader.py` - carrega e valida configs em runtime
- **Validator**: `core/agents/memory/config_validator.py` - valida schema dos YAMLs
- **Bootstrap**: Validação automática no `create_multi_agent_graph()`

**Funcionalidades:**
- Prompts carregados do YAML substituem prompts hard-coded em `core/prompts/` (módulo modularizado por agente)
- Modelos LLM configuráveis por agente (Haiku para performance, Sonnet para precisão)
- Limites de contexto (`max_input_tokens`, `max_output_tokens`, `max_total_tokens`) por agente
- **Fallback automático**: Se YAML falhar, nós usam prompts hard-coded para não quebrar sistema
- **Mensagens em PT-BR**: Todos os erros reportados em português

**Integração runtime:**
- `orchestrator_node`: Carrega `core/config/agents/orchestrator.yaml` ao executar
- `structurer_node`: Carrega `core/config/agents/structurer.yaml` ao executar (ambos modos: inicial e refinamento)
- `decide_collaborative` e `force_decision_collaborative`: Carregam `core/config/agents/methodologist.yaml` ao executar
- `create_multi_agent_graph`: Valida que todos YAMLs obrigatórios existem no bootstrap

## Registro de Memória e Metadados

Sistema de captura e agregação de tokens, custos e metadados de execução por agente.

**Arquitetura:**
- **ExecutionTracker**: `core/agents/memory/execution_tracker.py` - helper para capturar tokens de AIMessage e registrar no MemoryManager
- **MemoryManager**: `core/agents/memory/memory_manager.py` - armazena histórico de execuções por sessão e agente
- **CostTracker**: `core/utils/cost_tracker.py` - calcula custos baseado em tokens e modelo LLM
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

## Sistema de Observabilidade (Epic 8.5)

Sistema de logging estruturado para debugging e análise de sessões multi-agente.

**Arquitetura:**
- **StructuredLogger**: `core/utils/structured_logger.py` - Captura eventos em formato JSONL append-only
- **DebugReporter**: `core/utils/debug_reporter.py` - Gera relatórios formatados a partir dos logs
- **Session Replay**: `scripts/core/testing/replay_session.py` - Reproduz sessões passo a passo

**Logs capturados:**
- `agent_started`: Início de execução de agente
- `agent_completed`: Conclusão com métricas (tokens, cost, duration)
- `decision_made`: Decisões tomadas com reasoning completo
- `error`: Erros durante execução

**Schema do log:**
```json
{
  "timestamp": "2025-12-05T18:10:57.331970Z",
  "trace_id": "test-scenario-2-1764958245",
  "agent": "orchestrator",
  "node": "orchestrator_node",
  "event": "decision_made",
  "level": "INFO",
  "message": "orchestrator made decision",
  "metadata": {
    "tokens_input": 8570,
    "tokens_output": 368,
    "tokens_total": 8938,
    "cost": 0.0083,
    "duration_ms": 12545.157,
    "decision": {...},
    "reasoning": "..."
  }
}
```

**Localização:** `logs/structured/{trace_id}.jsonl`

**Ferramentas:**
- Debug detalhado: `python scripts/core/testing/debug_scenario.py --scenario N --level full`
- Replay de sessão: `python scripts/core/testing/replay_session.py {trace_id}`

**Nós instrumentados:**
- `orchestrator_node`: Logs de análise e decisão
- `structurer_node`: Logs de estruturação (V1, V2, V3)
- `decide_collaborative`: Logs de validação metodológica
- `force_decision_collaborative`: Logs de decisão forçada

## Estrutura do Projeto

```
paper-agent/
├── .env.example           # Template de variáveis de ambiente
├── requirements.txt       # Dependências Python
├── README.md              # Getting Started
├── core/ROADMAP.md        # Épicos e melhorias do core
└── products/revelar/ROADMAP.md  # Épicos e melhorias do Revelar
├── ARCHITECTURE.md        # Visão arquitetural (este arquivo)
├── development_guidelines.md  # Regras para desenvolvimento com agentes
│
├── core/                  # Core compartilhado
│   ├── config/            # Configurações externas
│   │   └── agents/        # Configs YAML por agente
│   │       ├── orchestrator.yaml    # Prompt, modelo, limites do Orquestrador
│   │       ├── structurer.yaml      # Prompt, modelo, limites do Estruturador
│   │       └── methodologist.yaml   # Prompt, modelo, limites do Metodologista
│   ├── agents/            # Agentes especializados
│   │   ├── __init__.py
│   │   ├── methodologist/     # Agente Metodologista
│   │   │   ├── __init__.py
│   │   │   ├── state.py       # MethodologistState
│   │   │   ├── nodes.py       # analyze, ask_clarification, decide
│   │   │   ├── router.py      # route_after_analyze
│   │   │   ├── graph.py       # Construção do grafo
│   │   │   └── tools.py       # ask_user tool
│   │   ├── orchestrator/      # Agente Orquestrador
│   │   │   ├── __init__.py
│   │   │   ├── state.py       # MultiAgentState
│   │   │   ├── nodes.py       # orchestrator_node
│   │   │   └── router.py      # route_from_orchestrator
│   │   ├── structurer/        # Agente Estruturador
│   │   │   ├── __init__.py
│   │   │   └── nodes.py       # structurer_node
│   │   ├── models/            # Modelos de domínio
│   │   │   ├── __init__.py
│   │   │   └── cognitive_model.py    # CognitiveModel, Contradiction, SolidGround
│   │   ├── database/          # Persistência SQLite
│   │   │   ├── __init__.py
│   │   │   ├── schema.py       # Schema SQL (tabelas, índices, triggers, views)
│   │   │   ├── manager.py      # DatabaseManager (orquestrador singleton)
│   │   │   ├── ideas_crud.py   # CRUD operations para Ideas
│   │   │   └── arguments_crud.py # CRUD operations para Arguments
│   │   ├── persistence/       # Snapshots e maturidade
│   │   │   ├── __init__.py
│   │   │   └── snapshot_manager.py   # SnapshotManager (detecção LLM + snapshot automático)
│   │   ├── checklist/         # Rastreamento de progresso
│   │   │   ├── __init__.py
│   │   │   └── progress_tracker.py   # ProgressTracker (checklist adaptativo)
│   │   ├── memory/            # Sistema de memória e configuração
│   │   │   ├── __init__.py
│   │   │   ├── config_loader.py      # Carregamento de configs YAML
│   │   │   ├── config_validator.py   # Validação de schema YAML
│   │   │   ├── execution_tracker.py   # Helper para captura de tokens
│   │   │   └── memory_manager.py     # Gestão de memória por agente
│   │   └── multi_agent_graph.py      # Super-grafo
│   ├── utils/                 # Utilitários e helpers
│   │   ├── __init__.py
│   │   ├── cost_tracker.py    # Cálculo de custos de API
│   │   ├── event_models.py    # Models Pydantic para eventos
│   │   ├── structured_logger.py  # Logging estruturado
│   │   ├── debug_reporter.py  # Relatórios de debug
│   │   └── event_bus/         # EventBus modularizado para Dashboard
│   │       ├── core.py        # Classe base com persistência
│   │       ├── publishers.py  # Métodos publish_*
│   │       ├── readers.py     # Métodos get_* e list_*
│   │       └── singleton.py   # Classe EventBus completa
│   ├── prompts/               # Prompts dos agentes (modularizado)
│   │   ├── __init__.py
│   │   ├── methodologist.py
│   │   ├── orchestrator.py
│   │   └── structurer.py
│   ├── tools/                 # Ferramentas
│   │   └── cli/               # Interface de linha de comando
│   │       ├── __init__.py
│   │       └── chat.py        # CLI interativo (integrado com EventBus)
│   └── docs/                  # Documentação do core
│       ├── agents/            # Especificações de agentes
│       ├── architecture/      # Decisões técnicas, modelos de dados
│       └── vision/            # Visão do sistema
│
├── products/                  # Produtos específicos
│   └── revelar/              # Produto Revelar (atual)
│       ├── app/               # Interface Web Conversacional
│       │   ├── __init__.py
│       │   ├── dashboard.py   # Dashboard de visualização de eventos
│       │   ├── chat.py        # Chat conversacional principal
│       │   └── components/    # Componentes reutilizáveis
│       │       ├── __init__.py
│       │       ├── chat_input.py     # Input de mensagens
│       │       ├── chat_history.py   # Histórico de conversa
│       │       ├── backstage/        # Painel "Bastidores" (modularizado)
│       │       │   ├── __init__.py
│       │       │   ├── context.py      # Seção "💡 Contexto" (ideia, solidez, custos)
│       │       │   ├── reasoning.py    # Seção "📊 Bastidores" (reasoning dos agentes)
│       │       │   ├── timeline.py     # Histórico de agentes
│       │       │   └── constants.py    # Constantes compartilhadas
│       │       ├── sidebar/          # Sidebar modular (Épico 14.1)
│       │       │   ├── __init__.py
│       │       │   ├── navigation.py    # Navegação principal
│       │       │   ├── conversations.py # Gestão de conversas
│       │       │   └── ideas.py         # Gestão de ideias
│       │       └── storage.py        # Persistência localStorage
│       └── docs/              # Documentação do produto
│
├── tests/                     # Testes automatizados (pytest)
│   ├── __init__.py
│   ├── core/                   # Testes do core
│   │   ├── unit/              # Testes unitários (mocks, rápidos)
│   │   │   ├── __init__.py
│   │   │   ├── test_cost_tracker.py
│   │   │   ├── test_methodologist_state.py
│   │   │   ├── test_ask_user_tool.py
│   │   │   ├── test_graph_nodes.py
│   │   │   ├── test_orchestrator.py
│   │   │   ├── test_structurer.py
│   │   │   ├── test_event_models.py
│   │   │   ├── test_event_bus.py
│   │   │   ├── test_config_loader.py
│   │   │   └── test_memory_manager.py
│   │   └── integration/       # Testes de integração (API real)
│   │       └── __init__.py
│   └── products/              # Testes de produtos
│
├── scripts/                   # Scripts de validação manual
│   ├── __init__.py
│   ├── core/                   # Scripts do core
│   │   ├── health_checks/            # Sanidade de ambiente e configs
│   │   │   ├── validate_api.py
│   │   │   ├── validate_agent_config.py
│   │   │   ├── validate_runtime_config_simple.py
│   │   │   ├── validate_syntax.py
│   │   │   ├── validate_system_prompt.py
│   │   │   ├── validate_execution_tracker.py
│   │   │   └── validate_orchestrator_json_parsing.py
│   │   ├── testing/                 # Testes e debugging
│   │   │   ├── debug_scenario.py
│   │   │   └── replay_session.py
│   │   └── debug/                    # Diagnóstico ad hoc
│   │       ├── debug_multi_agent.py
│   │       └── check_events.py
│   └── revelar/               # Scripts do produto Revelar
│
└── docs/                      # Documentação geral
    ├── analysis/              # Análises técnicas
    ├── process/                # Processos de desenvolvimento
    └── testing/                # Estratégia de testes
```

## Componentes Principais

### Metodologista (`core/agents/methodologist/`)
Agente especializado em avaliar rigor científico de hipóteses usando LangGraph. Opera em modo colaborativo: `approved`, `needs_refinement`, `rejected`.

**Detalhes:** Ver `core/docs/agents/methodologist.md`

### Orquestrador (`core/agents/orchestrator/`)
Agente responsável por facilitar conversa e coordenar chamadas a agentes especializados. Facilitador conversacional que negocia caminho com usuário.

**Detalhes:** Ver `core/docs/architecture/agents/orchestrator/conversational/README.md`

### Estruturador (`core/agents/structurer/`)
Agente responsável por organizar ideias vagas e refinar questões de pesquisa baseado em feedback. Nó simples com 2 modos: estruturação inicial (V1) e refinamento (V2/V3).

**Detalhes:** Ver `core/docs/architecture/patterns/refinement.md`

### Interface Web (`products/revelar/app/`)
Interface web conversacional (Streamlit) como experiência principal do sistema. Chat fluido com reasoning dos agentes visível ("Bastidores"), métricas inline e streaming de eventos. Componentes: chat, bastidores, timeline, sidebar. Eventos consumidos via polling (POC) ou SSE (MVP).

**Detalhes:** Ver `products/revelar/docs/interface/` (overview.md, components.md, flows.md)

### CLI (`core/tools/cli/chat.py`)
Loop interativo minimalista para desenvolvimento e automacao. Backend compartilhado com interface web.

**Detalhes:** Ver `core/docs/tools/cli.md` e `core/docs/tools/conversational_cli.md`

## Decisões Técnicas Atuais

- **Prioridade para CLI:** Permite automação com agentes (Claude Code / Cursor) sem dependência de navegador
- **Sem persistência, Docker ou vector DB durante POC:** Para acelerar iteração
- **Claude Sonnet 4 usado pelo Metodologista:** Para confiabilidade de JSON estruturado
- **Claude Haiku usado pelo Estruturador:** Custo-benefício para estruturação/refinamento
- **Refinamento sob demanda:** Loop não é automático; usuário decide quando refinar baseado em feedback do Metodologista. Sem limite fixo de iterações
- **Transição para conversação adaptativa:** Ver `core/docs/architecture/agents/orchestrator/conversational/` para padrões de conversa vs classificação
- **EventBus para visualização:** CLI emite eventos consumidos por Dashboard Streamlit via arquivos JSON temporários
- **Modo colaborativo:** Prefere `needs_refinement` ao invés de rejeitar diretamente (construir > criticar)

## Padrões Essenciais

- **Contratos em JSON** entre orquestrador e agentes (status, justificativa, sugestões)
- **Validação** via Pydantic e retries com backoff (até 3 tentativas) para chamadas Anthropic
- **Transparência:** logs estruturados (`INFO` para decisões, `DEBUG` para reasoning completo)
- **Separação de responsabilidades:** agentes não se conhecem; orquestrador não faz análise científica

## Referências

**Arquitetura:**
- `core/docs/architecture/data-models/ontology.md` - Ontologia (Conceito/Ideia/Argumento)
- `core/docs/architecture/vision/super_system.md` - Super-sistema: Core → Produtos
- `core/docs/architecture/data-models/idea_model.md` - Estrutura de dados Ideia
- `core/docs/architecture/data-models/concept_model.md` - Estrutura de dados Conceito
- `core/docs/architecture/data-models/argument_model.md` - Estrutura de dados Argumento
- `core/docs/architecture/infrastructure/tech_stack.md` - ChromaDB, SQLite, embeddings
- `core/docs/architecture/patterns/snapshots.md` - Estratégia de persistência de snapshots

**Visão de Produto:**
- `products/produtor-cientifico/docs/vision.md` - Visão de produto, tipos de artigo
- `core/docs/vision/cognitive_model/` - Modelo cognitivo e evolução

**Orquestração:**
- `core/docs/architecture/agents/multi_agent/` - Arquitetura multi-agente
- `core/docs/architecture/agents/orchestrator/conversational/` - Orquestrador conversacional

**Produtos:**
- `products/produtor-cientifico/docs/vision.md` - Produtor Científico (produto atual)
- `products/prisma-verbal/docs/vision.md` - Fichamento (produto futuro)
