# ARCHITECTURE.md

## Visão Geral

- Plataforma colaborativa com agentes de IA para apoiar produção de artigos científicos ponta a ponta.
- **Arquitetura atual:** Sistema multi-agente conversacional sobre LangGraph com Orquestrador facilitador, Estruturador organizador e Metodologista validador.
- **Em evolução:** Transição de fluxo determinístico para conversação adaptativa onde sistema e usuário negociam caminho juntos (Épico 7).
- **Interfaces:** CLI para conversação (principal) e Streamlit para visualização de raciocínio em tempo real.

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

**Tipos de artigo suportados:**
1. `empirical` - Testa hipótese com dados coletados
2. `review` - Revisão sistemática/literatura
3. `theoretical` - Propõe framework/teoria
4. `case_study` - Análise de caso(s) específico(s)
5. `meta_analysis` - Análise quantitativa agregada
6. `methodological` - Propõe/valida método/técnica

**Estágios de maturidade:**
- `ideation` - Ideia inicial vaga
- `hypothesis` - Hipótese estruturada
- `methodology` - Metodologia definida
- `research` - Pesquisa em andamento
- `writing` - Escrevendo artigo
- `review` - Revisão final
- `done` - Artigo completo

**Evolução fluida:**
- Sistema detecta `stage` automaticamente (não pergunta diretamente)
- Usuário pode voltar etapas (ex: pesquisa altera metodologia)
- Tipo pode ser inferido ou mudar ao longo da conversa

## Escopo Atual

**Sistema Multi-Agente Conversacional:**
- **Orquestrador:** Classifica maturidade inicial e roteia para agentes (em evolução para facilitador conversacional)
- **Estruturador:** Organiza ideias vagas e refina questões baseado em feedback estruturado
- **Metodologista:** Valida rigor científico em modo colaborativo (approved/needs_refinement/rejected)
- **Interface visual:** Dashboard Streamlit com timeline de eventos em tempo real

**Estado compartilhado:**
- MultiAgentState híbrido (campos compartilhados + específicos por agente)
- Versionamento de hipóteses (V1 → V2 → V3)
- Rastreamento de iterações de refinamento

**Infraestrutura:**
- Python 3.11+, Anthropic API, LangGraph
- Configuração externa de agentes (YAML)
- EventBus para comunicação CLI ↔ Dashboard
- MemoryManager para registro de metadados

**Em desenvolvimento (Épico 7):**
- Orquestrador conversacional que negocia caminho com usuário
- Detecção dinâmica de quando chamar agentes especializados
- Handling de mudança de direção do usuário

## Orquestrador Conversacional (Épico 7)

**Transição arquitetural em andamento:**

### De: Classificador Determinístico
```
Input → Classifica (vague/semi_formed/complete) → Roteia automaticamente
```

### Para: Facilitador Conversacional
```
Input → Conversa → Detecta necessidade → Oferece opções → Usuário decide → Executa
```

**Novo papel do Orquestrador:**
- **Diálogo fluido:** Mantém conversa antes de acionar agentes
- **Negociação:** Oferece opções ("Posso chamar Metodologista?" vs "Vou chamar")
- **Detecção inteligente:** Infere quando agente faz sentido (mas não impõe)
- **Adaptação:** Responde a mudanças de direção do usuário
- **Provocação:** Faz perguntas esclarecedoras que ajudam reflexão

**Progressão POC → MVP:**
- **POC:** Conversação básica + oferece opções + chama sob demanda
- **Protótipo:** Detecção inteligente + provocação + handling de mudança
- **MVP:** Detecção emergente de estágio + reasoning explícito + aprende preferências

**Especificação detalhada:** `docs/orchestration/conversational_orchestrator.md`

## Stack Técnico

- **Runtime:** Python 3.11+
- **Orquestração:** LangGraph, LangChain Anthropic
- **LLM:** Claude 3.5 Haiku (custo-benefício) / Sonnet (tarefas complexas)
- **Validação:** Pydantic, PyYAML para configs
- **Interfaces:** CLI (futura), Streamlit opcional (futura)
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

**Integração runtime (Épico 6.1 - 13/11/2025):**
- `orchestrator_node`: Carrega `config/agents/orchestrator.yaml` ao executar
- `structurer_node`: Carrega `config/agents/structurer.yaml` ao executar (ambos modos: inicial e refinamento)
- `decide_collaborative`: Carrega `config/agents/methodologist.yaml` ao executar
- `force_decision_collaborative`: Carrega `config/agents/methodologist.yaml` ao executar
- `create_multi_agent_graph`: Valida que todos YAMLs obrigatórios existem no bootstrap

**Validação:**
- Script: `scripts/validate_runtime_config_simple.py` - valida carregamento de configs
- Script: `scripts/validate_syntax.py` - valida sintaxe Python dos módulos modificados
- Testes: `tests/unit/test_config_loader.py` - cobertura de config loader

**Versões atualizadas:**
- Orquestrador v2.0, Estruturador v3.0, Metodologista v3.0, Super-grafo v3.0

## Registro de Memória e Metadados (Épico 6.2)

Sistema de captura e agregação de tokens, custos e metadados de execução por agente.

**Arquitetura:**
- **ExecutionTracker**: `agents/memory/execution_tracker.py` - helper para capturar tokens de AIMessage e registrar no MemoryManager
- **MemoryManager**: `agents/memory/memory_manager.py` - armazena histórico de execuções por sessão e agente
- **CostTracker**: `utils/cost_tracker.py` - calcula custos baseado em tokens e modelo LLM
- **Integração**: Nós do LangGraph recebem config com `memory_manager` e registram após cada invocação LLM

**Funcionalidades (13/11/2025):**
- Captura automática de tokens de respostas LLM (LangChain AIMessage)
- Cálculo de custos integrado (suporta Haiku, Sonnet, Opus)
- Registro de metadados personalizados por agente (classificação, modo, versão, etc)
- Agregação de totais por agente e por sessão
- Export JSON serializável para integração com dashboard (Épico 5)
- Passagem opcional via config - não quebra nós existentes

**Nós instrumentados:**
- `orchestrator_node` (v2.1): Registra classificação de maturidade + tokens
- `structurer_node` (v3.1): Registra estruturação inicial (V1) e refinamentos (V2/V3) + tokens
- `decide_collaborative` (v3.1): Registra decisões colaborativas (approved/needs_refinement/rejected) + tokens
- `force_decision_collaborative` (v3.1): Registra decisões forçadas após limite + tokens

**Validação:**
- Script: `scripts/validate_memory_integration.py` - validação end-to-end do fluxo completo
- Script: `scripts/validate_execution_tracker.py` - validação unitária do helper
- CLI: `cli/chat.py` atualizado para exibir métricas de tokens e custos

**Exemplo de uso:**
```python
from agents.multi_agent_graph import create_multi_agent_graph
from agents.memory.memory_manager import MemoryManager

memory_manager = MemoryManager()
graph = create_multi_agent_graph()

config = {
    "configurable": {
        "thread_id": "session-123",
        "memory_manager": memory_manager  # Opcional (Épico 6.2)
    }
}

result = graph.invoke(state, config=config)

# Obter métricas
totals = memory_manager.get_session_totals("session-123")
print(f"Total: {totals['total']} tokens")
print(f"Orchestrador: {totals['orchestrator']} tokens")
```

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
│   ├── methodologist/     # Agente Metodologista (Épico 2)
│   │   ├── __init__.py
│   │   ├── state.py       # MethodologistState
│   │   ├── nodes.py       # analyze, ask_clarification, decide (v3.0 com config YAML)
│   │   ├── router.py      # route_after_analyze
│   │   ├── graph.py       # Construção do grafo
│   │   └── tools.py       # ask_user tool
│   ├── orchestrator/      # Agente Orquestrador (Épico 3.1)
│   │   ├── __init__.py
│   │   ├── state.py       # MultiAgentState
│   │   ├── nodes.py       # orchestrator_node (v2.0 com config YAML)
│   │   └── router.py      # route_from_orchestrator
│   ├── structurer/        # Agente Estruturador (Épico 3.2)
│   │   ├── __init__.py
│   │   └── nodes.py       # structurer_node (v3.0 com config YAML)
│   ├── memory/            # Sistema de memória e configuração (Épico 6)
│   │   ├── __init__.py
│   │   ├── config_loader.py      # Carregamento de configs YAML
│   │   ├── config_validator.py   # Validação de schema YAML
│   │   └── memory_manager.py     # Gestão de memória por agente
│   ├── multi_agent_graph.py      # Super-grafo (v3.0 com validação de configs)
│   └── methodologist_knowledge.md  # Base de conhecimento micro
│
├── utils/                 # Utilitários e helpers
│   ├── __init__.py
│   ├── prompts.py         # Prompts versionados dos agentes
│   ├── cost_tracker.py    # Cálculo de custos de API
│   ├── event_models.py    # Models Pydantic para eventos (Épico 5.1)
│   └── event_bus.py       # EventBus para Dashboard (Épico 5.1)
│
├── cli/                   # Interface de linha de comando
│   ├── __init__.py
│   └── chat.py            # CLI interativo (integrado com EventBus)
│
├── app/                   # Interface Streamlit (Épico 5.1)
│   ├── __init__.py
│   └── dashboard.py       # Dashboard web com timeline
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
│   │   ├── test_structurer.py           # Testes do Estruturador (Épico 3.2)
│   │   ├── test_event_models.py         # Testes dos models de eventos (Épico 5.1)
│   │   ├── test_event_bus.py            # Testes do EventBus (Épico 5.1)
│   │   └── test_config_loader.py        # Testes do config loader (Épico 6.1)
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
│   ├── validate_cli.py    # Validação do CLI (fluxo completo)
│   ├── validate_dashboard.py     # Validação do Dashboard (Épico 5.1)
│   ├── validate_agent_config.py  # Validação de configs YAML (Épico 6.1)
│   ├── validate_runtime_config.py  # Validação de integração runtime (requer venv)
│   ├── validate_runtime_config_simple.py  # Validação de configs sem deps
│   ├── validate_syntax.py  # Validação de sintaxe Python
│   └── validate_memory_integration.py  # Validação da integração do MemoryManager (Épico 6.2)
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
Agente responsável por facilitar conversa e coordenar chamadas a agentes especializados.

**Arquitetura (em transição - Épico 7):**
- Estado compartilhado gerenciado por `MultiAgentState` (TypedDict híbrido)
- **Atual:** Nó de classificação `orchestrator_node` (classifica maturidade)
- **Futuro:** Facilitador conversacional (negocia caminho com usuário)
- Router condicional: `route_from_orchestrator` (roteia para Estruturador ou Metodologista)

**Classificações atuais (POC):**
- "vague" → Estruturador (ideia não estruturada)
- "semi_formed" → Metodologista (hipótese parcial)
- "complete" → Metodologista (hipótese completa)

**Evolução (Épico 7):**
- Conversação > classificação
- Oferece opções > roteia automaticamente
- Detecta dinamicamente > fluxo fixo
- Adapta a mudanças > fluxo linear

**Status:** Funcionalidade 3.1 implementada (classificação). Épico 7 em planejamento (conversação).

**Detalhes:** Ver `docs/orchestration/conversational_orchestrator.md`

### Detecção de Tipo de Artigo (Épico 7 - Futuro)

**Responsabilidade:** Orquestrador infere tipo de artigo na conversa inicial e adapta fluxo de agentes.

**Estratégia:**
- Perguntas dinâmicas na primeira interação
- Análise de palavras-chave (ex: "testar hipótese" → empírico, "revisão de literatura" → review)
- Permite mudança de tipo ao longo da conversa (começa observacional, vira empírico)

**Adaptação de fluxo:**

| Tipo | Agentes Prioritários | Checkpoints Mínimos |
|------|---------------------|---------------------|
| empirical | Metodologista, Estruturador | Hipótese → Metodologia → Coleta → Análise |
| review | Pesquisador, Estruturador | Questão PICO → Busca → Síntese |
| theoretical | Metodologista, Estruturador | Problema → Argumento → Framework |
| case_study | Metodologista, Estruturador | Caso → Contexto → Análise → Insights |
| meta_analysis | Metodologista, Pesquisador | Questão → Busca → Extração → Análise estatística |
| methodological | Metodologista, Estruturador | Método → Validação → Comparação |

Ver `docs/product/vision.md` (Seções 2 e 3) para fluxos detalhados.

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

### EventBus (`utils/event_bus.py`) - Épico 5.1
Barramento de eventos para comunicação entre CLI/Graph e Dashboard.

**Arquitetura:**
- Publica eventos em arquivos JSON temporários (`/tmp/paper-agent-events/`)
- Cada sessão tem arquivo próprio: `events-{session_id}.json`
- Padrão singleton via `get_event_bus()`

**Tipos de evento:**
- `SessionStartedEvent`: Início de sessão com input do usuário
- `AgentStartedEvent`: Agente inicia execução
- `AgentCompletedEvent`: Agente finaliza com sucesso (inclui tokens e summary)
- `AgentErrorEvent`: Agente falha durante execução
- `SessionCompletedEvent`: Sessão finaliza com status e total de tokens

**Métodos principais:**
- `publish_*()`: Publicar eventos específicos
- `get_session_events()`: Obter timeline de eventos de uma sessão
- `list_active_sessions()`: Listar sessões com arquivos de evento
- `get_session_summary()`: Obter resumo (status, total de eventos, timestamps)

**Integração:**
- CLI publica eventos de sessão (started/completed)
- Graph instrumentado publica eventos de agentes (started/completed/error)
- Dashboard consome eventos em tempo real

**Status:** Funcionalidade 5.1 implementada e testada.

### Dashboard Streamlit (`app/dashboard.py`) - Épico 5.1
Interface web para visualização de sessões e eventos em tempo real.

**Funcionalidades:**
- 📋 Lista de sessões ativas na sidebar
- 🕒 Timeline cronológica de eventos com ícones e cores por agente
- 📊 Status visual (executando, concluído, erro) com indicadores coloridos
- 🔄 Auto-refresh configurável (1-10 segundos, padrão: 2s)
- 📈 Estatísticas: eventos por tipo, agentes executados, total de tokens
- 🗑️ Ações: atualizar manualmente, limpar sessão

**Componentes:**
- `render_session_selector()`: Seletor de sessões
- `render_session_summary()`: Métricas principais (status, eventos, timestamps)
- `render_timeline()`: Timeline visual com eventos ordenados cronologicamente
- `render_event_stats()`: Estatísticas e gráficos de uso

**Tecnologia:**
- Streamlit para UI
- EventBus para consumo de eventos
- Auto-refresh via `st.rerun()` com timer

**Como executar:**
```bash
streamlit run app/dashboard.py
```

**Status:** Funcionalidade 5.1 implementada e testada.

## Fluxo de Dados (Atualizado - Épico 7)

### Fluxo Atual (Transição)

**Implementado (Épicos 3-4):**
```
Usuário (CLI) → Orquestrador (classifica maturidade) →
  ├─ Input vago → Estruturador (V1) → Metodologista
  │                  ↓ needs_refinement (< max iterations)
  │                  └─ Estruturador (V2) → Metodologista
  │                           ↓ approved/rejected
  │                           END (V1 → V2 com feedback)
  │
  └─ Hipótese formada → Metodologista → END
```

**Em desenvolvimento (Épico 7 POC):**
```
Usuário: "Quero entender X"
  ↓
Orquestrador: [conversa] "Você quer VER literatura ou TESTAR hipótese?"
  ↓
Usuário: "Testar"
  ↓
Orquestrador: "Legal! Me conta mais sobre X..."
  ↓ [conversa até ficar claro]
Orquestrador: "Posso chamar Metodologista para validar?"
  ↓
Usuário: "Sim"
  ↓
[Chama Metodologista] → Feedback
  ↓
Orquestrador: "Ele sugeriu A e B. O que quer fazer?
               1. Refinar agora
               2. Pesquisar sobre B
               3. Mudar direção"
  ↓
Usuário decide → Sistema executa
```

### Fluxo Futuro (Com Tipos de Artigo - Épico 7)
```
Usuário inicia sessão
  ↓
Orquestrador detecta tipo de artigo (empirical, review, theoretical, etc)
  ↓
Sistema adapta fluxo conforme tipo:

EMPÍRICO:
  Estruturador → Metodologista → [Desenho Experimental] → Pesquisador → Escritor → Crítico

REVISÃO:
  Estruturador (protocolo PICO) → Pesquisador (busca) → Escritor (síntese) → Crítico

TEÓRICO:
  Estruturador (argumento) → Metodologista (lógica) → Escritor (framework) → Crítico

[Outros tipos seguem padrão similar]
```

**Persistência entre sessões:**
- Tópico salvo em `/data/topics/{topic_id}/` (SqliteSaver)
- Thread ID vinculado ao tópico (recupera contexto completo)
- Artefatos versionados (V1, V2, V3)

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
- **Transição para conversação adaptativa (Épico 7):** Orquestrador evolui de classificador para facilitador que negocia caminho com usuário.
- **Refinamento sob demanda:** Loop não é mais automático; usuário decide quando refinar baseado em feedback do Metodologista.
- **EventBus para visualização:** CLI emite eventos consumidos por Dashboard Streamlit via arquivos JSON temporários.
- Modo colaborativo: prefere `needs_refinement` ao invés de rejeitar diretamente (construir > criticar).

### Modelo de Dados (Épico 7 - Planejado)

- **Persistência:** SqliteSaver (LangGraph) para início, migração para PostgreSQL quando escalar
- **Estrutura de diretórios:** `/data/topics/{topic_id}/checkpoints.db`
- **Entidade Tópico:** TypedDict/Pydantic com article_type, stage, artifacts
- **Versionamento:** Artefatos rastreados (V1, V2, V3), com opção de rollback futuro
- **Detecção de tipo:** Orquestrador infere tipo automaticamente via LLM (ver vision.md)
- **Estágios:** Detectados automaticamente pelo Orquestrador com base em artefatos presentes

## Referências

- `README.md`: visão geral e execução.
- `docs/product/vision.md`: visão de produto, tipos de artigo, jornada do usuário
- `docs/agents/overview.md`: mapa completo de agentes planejados.
- `docs/orchestration/orchestrator.md`: regras de decisão e estado.
- `docs/interface/cli.md`: expectativas de UX e logging.
- `docs/process/planning_guidelines.md`: governança de roadmap e práticas de planejamento.
- `docs/orchestration/refinement_loop.md`: especificação técnica do loop de refinamento colaborativo.

**Versão:** 2.0 (Épico 4 - Loop de Refinamento Colaborativo COMPLETO)
**Data:** 12/11/2025