# ARCHITECTURE.md

## Visão Geral

- Plataforma colaborativa com agentes de IA para apoiar produção de artigos científicos ponta a ponta.
- **Arquitetura atual:** Sistema multi-agente conversacional sobre LangGraph com Orquestrador facilitador, Estruturador organizador e Metodologista validador.
- **Conversação adaptativa:** Sistema mantém diálogo fluido onde usuário e agentes negociam caminho juntos (Épico 7 MVP concluído).
- **Interfaces:** Interface web conversacional (Streamlit) como principal; CLI mantido para desenvolvimento e automação.

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
- **Orquestrador:** Facilitador conversacional que mantém diálogo, detecta necessidades e sugere agentes (Épico 7 MVP concluído)
- **Estruturador:** Organiza ideias vagas e refina questões baseado em feedback estruturado
- **Metodologista:** Valida rigor científico em modo colaborativo (approved/needs_refinement/rejected)
- **Interface conversacional:** Web app Streamlit com chat + painel "Bastidores" (reasoning dos agentes)
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

**Funcionalidades conversacionais MVP (Épico 7 - concluído):**
- CLI conversacional contínua com múltiplos turnos
- Detecção inteligente de quando chamar agentes especializados
- Handling de mudança de direção do usuário
- Argumento focal explícito extraído e atualizado a cada turno
- Provocação de reflexão sobre lacunas na conversa
- Detecção emergente de estágio (exploration → hypothesis)

## Orquestrador Conversacional (Épico 7)

**Status:** ✅ MVP Concluído (15/11/2025)

**Transição arquitetural concluída:**

### De: Classificador Determinístico
```
Input → Classifica (vague/semi_formed/complete) → Roteia automaticamente
```

### Para: Facilitador Conversacional (✅ Implementado)
```
Input → Conversa → Detecta necessidade → Oferece opções → Usuário decide → Executa
```

**Papel atual do Orquestrador:**
- **Diálogo fluido:** Mantém conversa antes de acionar agentes
- **Negociação:** Oferece opções ("Posso chamar Metodologista?" vs "Vou chamar")
- **Detecção inteligente:** Infere quando agente faz sentido (mas não impõe)
- **Adaptação:** Responde a mudanças de direção do usuário
- **Provocação:** Faz perguntas esclarecedoras que ajudam reflexão
- **Argumento focal:** Extrai e atualiza explicitamente (intent, subject, population, metrics, article_type)
- **Detecção emergente:** Sugere mudança de estágio quando conversa evolui

**Progressão implementada:**
- ✅ **POC:** Conversação básica + oferece opções + chama sob demanda
- ✅ **Protótipo:** Detecção inteligente + transparência + CLI conversacional
- ✅ **MVP:** Argumento focal explícito + provocação de reflexão + detecção emergente

**Especificação detalhada:** `docs/orchestration/conversational_orchestrator.md`

## Interface Web Conversacional (Épico 9)

**Transição arquitetural: Dashboard → Chat Interativo**

### De: Visualização Passiva
```
Dashboard Streamlit (Épico 5.1) → Apenas visualiza eventos do CLI
```

### Para: Interface Principal
```
Web App Conversacional → Chat + Bastidores + Métricas + Sessões
```

**Papel da Interface Web:**
- **Chat principal:** Input de mensagens, histórico de conversa
- **Bastidores (opcional):** Reasoning dos agentes em tempo real
- **Métricas inline:** Tokens e custo por mensagem (discreto)
- **Sessões:** Sidebar com lista de conversas (não simultâneo)
- **Persistência:** Salvar/retomar conversas entre visitas

**Progressão POC → MVP:**

**POC (chat básico):**
- ✅ Input de texto + enviar mensagem
- ✅ Histórico de conversa visível
- ✅ Métricas inline (custo/tokens discreto)
- ✅ Backend compartilhado (LangGraph + EventBus)

**Protótipo (bastidores):**
- ✅ Painel collapsible "Ver raciocínio"
- ✅ Reasoning resumido (~280 chars) + completo (modal)
- ✅ Timeline de agentes (histórico colapsado)
- ✅ Streaming via SSE (eventos em tempo real)

**MVP (experiência completa):**
- ✅ Sidebar com lista de sessões
- ✅ Persistência básica (SqliteSaver ou localStorage)
- ✅ Métricas consolidadas (total + por agente)

**Especificação detalhada:** `docs/interface/web.md`

---

### Arquitetura da Interface Web

**Stack Técnico:**
- **Framework:** Streamlit
- **Streaming:** SSE (Server-Sent Events) via endpoint `/events`
- **Backend:** LangGraph + EventBus (compartilhado com CLI)
- **Persistência:** SqliteSaver (LangGraph checkpoints) ou localStorage

**Componentes:**

**1. Chat Component**
- Input de texto (field + botão enviar)
- Histórico de mensagens (você/sistema)
- Estado "digitando..." durante processamento
- Métricas inline após cada mensagem

**2. Bastidores Component (Collapsible)**
- Toggle "🔍 Ver raciocínio" (fechado por padrão)
- Agente ativo (Orquestrador/Estruturador/Metodologista)
- Reasoning resumido (~280 chars)
- Botão "Ver completo" (expande modal com JSON)
- Métricas do agente (tempo, tokens, custo)

**3. Timeline Component**
- Histórico de agentes executados
- Colapsado por padrão (expansível)
- Ordenado cronologicamente
- Permite revisitar reasoning de passos anteriores

**4. Sidebar Component**
- Lista de sessões (título, data)
- Botão "Nova conversa"
- Sessão ativa destacada
- Alternância entre sessões

**Fluxo de Dados:**
```
┌──────────────┐
│   Usuário    │
│  (Interface) │
└──────┬───────┘
       │ 1. Envia mensagem
       ▼
┌──────────────┐
│   Streamlit  │
│  (Frontend)  │
└──────┬───────┘
       │ 2. Invoke LangGraph
       ▼
┌──────────────┐
│  LangGraph   │──────┐ 3. Publica eventos
│   Backend    │      │
└──────┬───────┘      │
       │              ▼
       │        ┌──────────────┐
       │        │  EventBus    │
       │        │  (SSE)       │
       │        └──────┬───────┘
       │               │ 4. Stream eventos
       │               ▼
       ▼         ┌──────────────┐
┌──────────────┐ │  Bastidores  │
│   Chat UI    │ │  Component   │
│  (resposta)  │ │  (reasoning) │
└──────────────┘ └──────────────┘
```

**SSE (Server-Sent Events):**
- Endpoint: `/events/<session_id>`
- Eventos: `agent_started`, `agent_completed`, `agent_error`
- Fallback: Polling (2s) se SSE falhar
- Reconnect automático em caso de falha

**Diferencial vs CLI:**
- ✅ Interface visual rica (não só texto)
- ✅ Bastidores inline (não precisa verbose flag)
- ✅ Timeline interativa (não logs lineares)
- ✅ Sessões persistidas (não apenas thread_id)

## Stack Técnico

- **Runtime:** Python 3.11+
- **Orquestração:** LangGraph, LangChain Anthropic
- **LLM:** Claude 3.5 Haiku (custo-benefício) / Sonnet (tarefas complexas)
- **Validação:** Pydantic, PyYAML para configs
- **Interface Web:** Streamlit, SSE (Server-Sent Events), componentes customizados
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
- Script: `scripts/flows/validate_memory_integration.py` - validação end-to-end do fluxo completo
- Script: `scripts/health_checks/validate_execution_tracker.py` - validação unitária do helper
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
├── app/                   # Interface Web Conversacional (Épico 9)
│   ├── __init__.py
│   ├── dashboard.py       # DEPRECATED: Visualização de eventos (Épico 5.1)
│   ├── chat.py            # Chat conversacional principal (Épico 9)
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
│   ├── health_checks/            # Sanidade de ambiente e configs
│   │   ├── validate_api.py
│   │   ├── validate_agent_config.py  # Validação de configs YAML (Épico 6.1)
│   │   ├── validate_runtime_config_simple.py  # Validação de configs sem deps
│   │   ├── validate_syntax.py  # Validação de sintaxe Python
│   │   ├── validate_system_prompt.py
│   │   ├── validate_execution_tracker.py  # Validação unitária do helper
│   │   └── validate_orchestrator_json_parsing.py
│   ├── flows/                    # Cenários completos (consomem API)
│   │   ├── validate_cli.py    # Validação do CLI (fluxo completo)
│   │   ├── validate_cli_integration.py  # Validação de integração CLI
│   │   ├── validate_dashboard.py     # Validação do Dashboard (Épico 5.1)
│   │   ├── validate_memory_integration.py  # Validação da integração do MemoryManager (Épico 6.2)
│   │   ├── validate_multi_agent_flow.py
│   │   ├── validate_orchestrator.py
│   │   ├── validate_refinement_loop.py
│   │   ├── validate_structurer.py    # Validação do Estruturador (Épico 3.2)
│   │   ├── validate_structurer_refinement.py
│   │   └── validate_build_context.py
│   ├── state_introspection/      # Nós isolados e estados
│   │   ├── validate_state.py
│   │   ├── validate_graph.py
│   │   └── validate_ask_user.py
│   └── debug/                    # Diagnóstico ad hoc
│       ├── debug_multi_agent.py
│       └── check_events.py
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

**Arquitetura (Épico 7 MVP - concluído):**
- Estado compartilhado gerenciado por `MultiAgentState` (TypedDict híbrido)
- **Implementado:** Facilitador conversacional que negocia caminho com usuário
- **Campos MVP:** `focal_argument`, `reflection_prompt`, `stage_suggestion`
- Router condicional: `route_from_orchestrator` (roteia para Estruturador ou Metodologista)

**Comportamento conversacional:**
- Mantém diálogo fluido antes de chamar agentes
- Oferece opções ao usuário (não impõe caminho)
- Detecta dinamicamente quando agente faz sentido
- Adapta a mudanças de direção do usuário
- Extrai e atualiza argumento focal a cada turno
- Provoca reflexão sobre lacunas na conversa
- Detecta emergência de novo estágio

**Status:** ✅ Épico 7 MVP concluído (15/11/2025)

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

**Evolução para Telemetria (Épico 8):**
O EventBus foi projetado com campo `metadata: Dict[str, Any]` livre, permitindo extensão sem mudanças estruturais. No Épico 8, este campo é usado para incluir `reasoning` dos agentes, viabilizando transparência completa do sistema. A arquitetura suporta tanto polling (implementado) quanto SSE (planejado para Protótipo 8.3) sem modificações no EventBus core.

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
- **Refinamento sob demanda (Épico 4):** Loop não é automático; usuário decide quando refinar baseado em feedback do Metodologista. Sem limite fixo de iterações.
- **Transição para conversação adaptativa (Épico 7):** Orquestrador evolui de classificador para facilitador que negocia caminho com usuário.
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