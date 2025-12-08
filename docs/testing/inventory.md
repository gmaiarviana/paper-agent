# Inventário de Testes

Lista organizada de testes por categoria e propósito.

**Última atualização:** Dezembro 2025  
**Status pós-migração:** ✅ 237 testes, 0 falhas

---

## 📊 Resumo por Categoria

| Categoria | Local | Arquivos | Custo | Quando Rodar |
|-----------|-------|----------|-------|--------------|
| Unit | `tests/unit/` | 21 | $0 | CI (sempre) |
| Smoke | `tests/integration/smoke/` | 3 | ~$0.01 | Manual/CI seletivo |
| Behavior | `tests/integration/behavior/` | 15 | ~$0.02-0.03 | Manual (releases) |
| E2E | `tests/integration/e2e/` | 1 | ~$0.05 | Manual (crítico) |

**Total:** 40 arquivos de teste

---

## 🧪 Unit Tests (tests/unit/)

### agents/ (11 arquivos)
- `orchestrator/` - Testes do orquestrador (modularizados):
  - `test_node.py` - orchestrator_node
  - `test_router.py` - route_from_orchestrator
  - `test_state.py` - MultiAgentState
  - `test_context.py` - _build_context
  - `test_cognitive_model.py` - Validação e fallback do cognitive_model
  - `test_integration.py` - Integração (active_idea_id, snapshots)
- `test_orchestrator_json_extraction.py` - Parsing JSON do orquestrador
- `test_structurer.py` - Lógica do estruturador
- `test_methodologist_state.py` - Estado do metodologista
- `test_methodologist_state_logic.py` - Lógica de criação de estado
- `test_methodologist_graph.py` - Construção do grafo
- `test_methodologist_nodes.py` - Nós do grafo (analyze, ask, decide)
- `test_ask_user_tool.py` - Tool ask_user
- `test_initial_state_human_message.py` - HumanMessage inicial
- `test_multi_agent_state.py` - Estado multi-agente
- `test_multi_agent_state_logic.py` - Lógica do estado multi-agente
- `test_state_syntax.py` - Validação de sintaxe

### models/ (1 arquivo)
- `test_cognitive_model.py` - Modelos Pydantic (CognitiveModel, Contradiction)

### memory/ (3 arquivos)
- `test_config_loader.py` - Carregamento de configs YAML
- `test_execution_tracker.py` - Rastreamento de execuções
- `test_memory_manager.py` - Gerenciamento de memória

### utils/ (5 arquivos)
- `test_cost_tracker.py` - Cálculo de custos
- `test_currency.py` - Conversão de moedas
- `test_event_bus.py` - Publicação/consumo de eventos
- `test_json_extraction.py` - Extração de JSON
- `test_token_extractor.py` - Extração de tokens

### database/ (1 arquivo)
- `test_database_manager.py` - DatabaseManager, CRUD, schema

---

## 🔥 Integration Tests

### smoke/ (3 arquivos)
Validação rápida de componentes principais.

- `test_methodologist_smoke.py` - Smoke test do Metodologista
- `test_multi_agent_smoke.py` - Smoke test do super-grafo
- `test_structurer_smoke.py` - Smoke test do Estruturador

### behavior/ (15 arquivos)
Comportamentos específicos do sistema.

**Conversação:**
- `test_conversation_flow.py` - Fluxo conversacional
- `test_conversation_switching.py` - Alternância de conversas
- `test_conversational_cli.py` - CLI conversacional
- `test_socratic_behavior.py` - Comportamento socrático

**Agentes:**
- `test_orchestrator_integration.py` - Orquestrador (API real)
- `test_structurer_integration.py` - Estruturador (API real)
- `test_multi_agent_flow.py` - Fluxo multi-agente

**Refinamento:**
- `test_refinement_loop.py` - Loop de refinamento
- `test_structurer_refinement.py` - Refinamento do Estruturador

**Cognição:**
- `test_cognitive_evolution.py` - Evolução cognitiva
- `test_build_context.py` - Construção de contexto

**Interface:**
- `test_cli_behavior.py` - CLI do Metodologista
- `test_cli_integration.py` - Integração CLI → EventBus
- `test_dashboard.py` - Dashboard Streamlit

**Infraestrutura:**
- `test_memory_integration.py` - Integração de memória
- `test_real_api_tokens.py` - Tokens reais da API
- `test_token_extraction.py` - Extração de tokens
- `test_system_maturity.py` - Maturidade geral

### e2e/ (1 arquivo)
Cenários completos multi-turn.

- `test_multi_turn_flows.py` - Cenários 3, 6, 7 do Épico 7

---

## 🛠️ Scripts Auxiliares

### debug/
- `check_events.py` - Inspeção de eventos
- `debug_multi_agent.py` - Debug do super-grafo

### health_checks/
- `validate_api.py` - Conexão com API
- `validate_agent_config.py` - Configs de agentes
- `validate_execution_tracker.py` - ExecutionTracker
- `validate_orchestrator_json_parsing.py` - Parsing JSON
- `validate_runtime_config_simple.py` - Runtime config
- `validate_syntax.py` - Sintaxe dos módulos
- `validate_system_prompt.py` - System prompts

### testing/ (Épico 8)
- `execute_scenario.py` - Executa cenários
- `debug_scenario.py` - Debug de cenários
- `replay_session.py` - Replay de sessões
- `collect_scenario_logs.py` - Coleta logs
- `run_scenario.py` - Roda cenário específico
- `run_all_scenarios.py` - Roda todos cenários

---

## 📝 Notas

- **Consulte strategy.md** para detalhes de quando usar cada tipo
- **Consulte structure.md** para estrutura completa de pastas
- **Consulte commands.md** para comandos específicos

**Este é apenas um inventário. Não duplica informações de outros docs.**
