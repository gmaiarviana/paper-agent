# ARCHITECTURE.md

## Visão Geral

- Plataforma colaborativa com agentes de IA para apoiar produção de artigos científicos ponta a ponta.
- POC atual: validação de hipóteses com Orquestrador + Metodologista rodando sobre LangGraph.
- Interfaces priorizadas: CLI (automação com agentes) e Streamlit opcional para uso humano.

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
│   │   ├── test_structurer.py           # Testes do Estruturador (Épico 3.2)
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
│   ├── validate_agent_config.py  # Validação de configs YAML (Épico 6.1)
│   ├── validate_runtime_config.py  # Validação de integração runtime (requer venv)
│   ├── validate_runtime_config_simple.py  # Validação de configs sem deps
│   └── validate_syntax.py  # Validação de sintaxe Python
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

## Fluxo de Dados (Atualizado - Épico 7)

### Fluxo Base (POC Atual)
```
Usuário (CLI) → Orquestrador (classifica maturidade) →
  ├─ Input vago → Estruturador (V1) → Metodologista (needs_refinement?)
  │                      ↓ sim (iteration < max)           ↑
  │                      └─ Estruturador (V2) ─────────────┘
  │                                ↓ approved/rejected
  │                                END (resultado com histórico V1→V2)
  │
  └─ Hipótese formada → Metodologista (approved/rejected) → END
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