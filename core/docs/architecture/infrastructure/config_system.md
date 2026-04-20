# Sistema de Configuração e Memória

Mecanismo único que cobre (a) configuração externa dos agentes do core via YAML e (b) registro de memória/metadados de execução por sessão e agente.

Fecha gap previamente listado no `docs/CONTEXT_INDEX.md` (sistema de memória sem doc técnica detalhada).

## Componentes

| Arquivo | Responsabilidade |
|---------|------------------|
| `core/config/agents/<agente>.yaml` | Config externa por agente (`prompt`, `model`, `context_limits`, `metadata`). Um arquivo por agente core (orchestrator, structurer, methodologist, observer, futuros). |
| `core/agents/memory/config_loader.py` | Carrega e resolve YAML em runtime. Retorna estrutura tipada pro nó do LangGraph. |
| `core/agents/memory/config_validator.py` | Valida schema dos YAMLs no bootstrap (`create_multi_agent_graph`). Falha cedo e em PT-BR. |
| `core/agents/memory/memory_manager.py` | Armazena histórico de execuções por `session_id` e `agent`. Agrega tokens, custos, decisões e metadados livres. |
| `core/agents/memory/execution_tracker.py` | Helper que extrai tokens de um `AIMessage` (LangChain) e chama o `MemoryManager`. Usado por cada nó após invocação LLM. |
| `core/utils/cost_tracker.py` | Cálculo de custo por modelo (Haiku/Sonnet/Opus) a partir de tokens. |

## Fluxo no runtime

```
bootstrap (create_multi_agent_graph)
  └─ config_validator valida todos os YAMLs obrigatórios

invocação do nó (ex.: orchestrator_node)
  ├─ config_loader carrega <agente>.yaml
  ├─ monta LLM com model + prompt do YAML
  ├─ chama LLM
  └─ execution_tracker.track_and_record(message, agent, session_id, metadata)
       └─ memory_manager.register(...) com tokens + cost (via cost_tracker)
```

Prompt hard-coded em `core/prompts/<agente>.py` serve como **fallback** se YAML falhar — sistema não quebra.

## Pontos de extensão

- **Novo agente core:** criar `core/config/agents/<agente>.yaml` + entrada no `config_validator` + `core/prompts/<agente>.py` (fallback).
- **Parametrização de contexto de produto** (core C-ENSAIO-1 / Ensaio E-POC-2): nó recebe `product_context` opcional; quando preenchido, o prompt ganha seção `## CONTEXTO DO PRODUTO`. Core continua sem conhecer nomes de produtos — a string vem do YAML do produto (ex.: `products/ensaio/config/product.yaml`) carregado pelo app do produto e injetado via `config` do LangGraph.

## Onde aparece na arquitetura

- Mencionado em `ARCHITECTURE.md` (seções "Configuração Externa de Agentes" e "Registro de Memória e Metadados").
- Integra com observabilidade estruturada (ver `ARCHITECTURE.md` → "Sistema de Observabilidade"): `execution_tracker` alimenta métricas; `structured_logger` persiste eventos.

## Referências

- Código: `core/agents/memory/`, `core/config/agents/`, `core/utils/cost_tracker.py`
- Prompts: `core/prompts/<agente>.py` (fallback)
- Super-sistema e injeção de contexto de produto: `core/docs/architecture/vision/super_system.md`
- Motivação Ensaio: `products/ensaio/ROADMAP.md` (E-POC-2) e `core/ROADMAP.md` (C-ENSAIO-1)
