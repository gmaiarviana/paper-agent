# ARCHITECTURE.md

## Visão Geral

Plataforma colaborativa com agentes de IA para apoiar produção de artigos científicos ponta a ponta. Arquitetura atual: sistema multi-agente conversacional sobre LangGraph com Orquestrador facilitador, Estruturador organizador e Metodologista validador. Sistema mantém diálogo fluido onde usuário e agentes negociam caminho juntos. Interface web conversacional (Streamlit) como principal; CLI mantido para desenvolvimento e automação.

## Entidade Central: Ideia

> **Nota:** Para estrutura de dados completa e ontologia, consulte:
> - `docs/architecture/ontology.md` - O que é Conceito, Ideia, Argumento
> - `docs/architecture/idea_model.md` - Schema técnico de Ideia
> - `docs/architecture/concept_model.md` - Schema técnico de Conceito
> - `docs/architecture/argument_model.md` - Schema técnico de Argumento

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
- **Argumento:** Lente (claim + premises + assumptions)

**Evolução fluida:** Sistema detecta status automaticamente; usuário pode voltar etapas; múltiplos argumentos por ideia.

## Gestão de Ideias (Épicos 12 + 14 - Concluídos)

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

**Catálogo (Página `/catalogo` - Épico 13):**
- Biblioteca de conceitos técnicos reutilizáveis
- Busca semântica via embeddings
- Mostra ideias que usam cada conceito

**Filosofia:** Conversas = processo (volátil), Ideias = cristalização (permanente), Conceitos = abstração (biblioteca).

Ver: `docs/interface/navigation_philosophy.md` para filosofia completa.

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

---

## Interfaces Mantidas

O sistema oferece **duas interfaces web** com propósitos distintos:

### Chat Web (`app/chat.py`) - Experiência Principal
- Interface conversacional para usuários finais
- Chat fluido + bastidores opcionais (reasoning inline)
- Sidebar com últimas 5 conversas (SqliteSaver backend)
- Navegação em três espaços: Conversas, Meus Pensamentos, Catálogo (Épico 14)
- Persistência entre visitas (sem autenticação - sessões compartilhadas)
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

Facilitador conversacional que mantém diálogo fluido, detecta necessidades, oferece opções ao usuário e adapta-se a mudanças de direção. Extrai e atualiza argumento focal a cada turno, provoca reflexão sobre lacunas e detecta emergência de novo estágio.

**Detalhes:** Ver `docs/orchestration/conversational_orchestrator.md`

## Orquestrador Socrático (Épico 10)

Evolução do Orquestrador Conversacional que adiciona capacidade de exposição de suposições implícitas através de contra-perguntas socráticas. Detecta 5 categorias de assumptions (métrica vaga, população vaga, baseline ausente, causalidade assumida, generalização excessiva), escala profundidade de provocação em 3 níveis conforme resistência do usuário, e determina timing apropriado de provocação (quando provocar vs quando apenas explorar).

**Detalhes:** Ver `docs/orchestration/socratic_orchestrator.md`

**Relacionamento:** Socrático é extensão do Conversacional (Épico 7). Conversacional provê base de análise contextual e argumento focal; Socrático adiciona provocação estruturada sobre assumptions.

## Estado Compartilhado

MultiAgentState híbrido gerencia campos compartilhados (mensagens, argumento focal) e específicos por agente (estruturação, validação). Suporta versionamento de hipóteses (V1 → V2 → V3) e rastreamento de iterações de refinamento.

**Detalhes:** Ver `docs/orchestration/multi_agent_architecture.md`

## Modelo Cognitivo (Épico 11 - Concluído)

Sistema captura evolução do pensamento do usuário através de modelo cognitivo explícito com campos: `claim`, `premises`, `assumptions`, `open_questions`, `contradictions`, `solid_grounds`, `context`.

**Detalhes completos:** Ver `docs/vision/cognitive_model.md`

**Responsabilidades:**
- Orquestrador: detecta suposições, extrai claim, atualiza contexto
- Estruturador: organiza premises, torna explícito o implícito
- Metodologista: valida lógica, aponta contradições
- Pesquisador (futuro): transforma dúvidas em evidências

**Implementação (Épico 11):**
- **Schema Pydantic:** `agents/models/cognitive_model.py` - CognitiveModel, Contradiction, SolidGround
- **Persistência SQLite:** `agents/database/` - DatabaseManager com tabelas ideas e arguments
- **Versionamento:** Auto-incremento de versões (V1, V2, V3...) por idea
- **Maturidade:** `agents/persistence/snapshot_manager.py` - Detecção via LLM e snapshots automáticos
- **Checklist:** `agents/checklist/progress_tracker.py` - Rastreamento adaptativo por tipo de artigo
- **Banco de dados:** `data/data.db` - Separado de checkpoints.db (LangGraph)

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

**Atual (Épico 11 - Concluído):**
- **SqliteSaver (LangGraph):** Checkpoints de conversa (arquivo `checkpoints.db`)
- **SQLite customizado (Épico 11):** Entidades de domínio em `data/data.db`:
  - Tabela `ideas`: id, title, status, current_argument_id (FK)
  - Tabela `arguments`: id, idea_id (FK), claim, premises, assumptions, open_questions, contradictions, solid_grounds, context, version
  - Versionamento automático (V1, V2, V3...) via UNIQUE constraint (idea_id, version)
  - Triggers para updated_at automático
  - Views otimizadas para JOIN idea + argumento focal
- **DatabaseManager singleton:** `agents/database/manager.py` - CRUD operations
- **Localização:** Arquivos locais em `./data/`

**Futuro (MVP/Produção):**
- **PostgreSQL:** Migração quando escalar
- **Schema compatível:** Mesmas queries funcionam em ambos
- **Estratégia documentada:** Ver `docs/architecture/persistence_foundation.md`

**Decisão:** Começar simples (SQLite) e migrar quando necessário. Evitar over-engineering prematuro.

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
│   ├── models/            # Modelos de domínio (Épico 11)
│   │   ├── __init__.py
│   │   └── cognitive_model.py    # CognitiveModel, Contradiction, SolidGround
│   ├── database/          # Persistência SQLite (Épico 11)
│   │   ├── __init__.py
│   │   ├── schema.py       # Schema SQL (tabelas, índices, triggers, views)
│   │   └── manager.py      # DatabaseManager (singleton CRUD)
│   ├── persistence/       # Snapshots e maturidade (Épico 11)
│   │   ├── __init__.py
│   │   └── snapshot_manager.py   # SnapshotManager (detecção LLM + snapshot automático)
│   ├── checklist/         # Rastreamento de progresso (Épico 11)
│   │   ├── __init__.py
│   │   └── progress_tracker.py   # ProgressTracker (checklist adaptativo)
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
│   ├── validate_cognitive_model.py   # Validação Epic 11 (completo)
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

## Estratégia de Migração

> **Nota:** Para fases detalhadas, consulte `docs/architecture/migration_strategy.md`.

Sistema está migrando de entidade `Topic` para ontologia completa (`Idea`, `Concept`, `Argument`):

**Fases planejadas:**
1. **Épico 11:** ✅ **Concluído** - Abstrair fundação (CognitiveModel + persistência SQLite)
2. **Épico 12:** ✅ **Concluído** - Gestão de ideias (listagem, alternância, busca, criação, explorador de argumentos)
3. **Épico 14:** ✅ **Concluído** - Navegação em Três Espaços (conversas, pensamentos, catálogo) + restauração de contexto
4. **Épico 13:** Criar Concept (vetores semânticos) + busca semântica
5. **Épico 15:** Polimentos de UX (Enter envia, custo em R$, métricas discretas)

**Status:** Épico 14 concluído. Próximo: Épico 13.

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
