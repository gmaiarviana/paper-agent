# Inventário de Testes

Este documento lista todos os comportamentos testados pelo sistema.

**IMPORTANTE para Claude Code**: Consulte este inventário ANTES de criar novos testes.

---

## 📊 Resumo

| Tipo | Quantidade | Custo API |
|------|------------|-----------|
| Unit Tests (mocks) | ~14 arquivos | $0 |
| Integration Tests (API real) | 5 arquivos | ~$0.10/execução |
| Behavior Validations (API real) | 10 arquivos | ~$0.15/execução |

---

## 🧪 Testes Unitários (por Componente)

**Diretório**: `tests/unit/`
**Custo**: $0 (usa mocks)
**Quando rodar**: `pytest tests/unit/ -v`

### Orquestrador
| Arquivo | Comportamentos Testados |
|---------|------------------------|
| `test_orchestrator.py` | Classificação input vago/semi/completo, routing, estado inicial, _build_context |
| `test_orchestrator_json_extraction.py` | Parsing JSON do orquestrador, validação de campos |

### Estruturador
| Arquivo | Comportamentos Testados |
|---------|------------------------|
| `test_structurer.py` | Estruturação de questões, refinamento |

### Metodologista
| Arquivo | Comportamentos Testados |
|---------|------------------------|
| `test_methodologist_state.py` | Estado do metodologista |
| `test_ask_user_tool.py` | Ferramenta de perguntas ao usuário |

### Multi-Agente
| Arquivo | Comportamentos Testados |
|---------|------------------------|
| `test_multi_agent_state.py` | Estado compartilhado |
| `test_graph_nodes.py` | Nós do grafo |
| `test_initial_state_human_message.py` | HumanMessage inicial |

### Infraestrutura
| Arquivo | Comportamentos Testados |
|---------|------------------------|
| `test_event_bus.py` | Publicação/consumo de eventos |
| `test_cost_tracker.py` | Cálculo de custos |
| `test_memory_manager.py` | Gerenciamento de memória (lógica complexa: isolamento, cálculos) |
| `test_execution_tracker.py` | Rastreamento de execução |
| `test_config_loader.py` | Carregamento de configs (validação de erros e schema) |
| `test_json_extraction.py` | Extração de JSON |
| `test_database_manager.py` | DatabaseManager, IdeasCRUD, ArgumentsCRUD, schema, versionamento |

---

## 🔗 Testes de Integração (por Componente)

**Diretório**: `tests/integration/`
**Custo**: ~$0.02/teste (usa API real)
**Quando rodar**: `pytest tests/integration/ -m integration -v`

| Arquivo | Comportamentos Testados |
|---------|------------------------|
| `test_multi_agent_smoke.py` | Fluxo completo vague→structured→validated, preservação de contexto |
| `test_methodologist_smoke.py` | Metodologista com API real |
| `test_conversation_switching.py` | Alternância entre conversas |
| `test_real_api_tokens.py` | Tokens reais da API |
| `test_token_extraction.py` | Extração de tokens |

---

## 🎯 Validações Comportamentais (por Behavior)

**Diretório**: `scripts/flows/`
**Custo**: ~$0.02-0.10/script (usa API real)
**Quando rodar**: `python scripts/flows/validate_<nome>.py`

### Conversação
| Arquivo | Behaviors Validados |
|---------|---------------------|
| `validate_conversation_flow.py` | Exploração com perguntas abertas, contexto preservado, sugestão de agentes, mudança de direção, router fallback |
| `validate_conversational_cli.py` | CLI multi-turno, thread_id preservado |

### Comportamento Socrático
| Arquivo | Behaviors Validados |
|---------|---------------------|
| `validate_socratic_behavior.py` | Provocação sobre métricas vagas, timing emergente, escalada natural, parada inteligente, não-repetição |

### Evolução Cognitiva
| Arquivo | Behaviors Validados |
|---------|---------------------|
| `validate_cognitive_evolution.py` | Argumento focal extraído/evolui, provocação de reflexão, detecção de estágio, mudança de direção |

### Multi-Agente
| Arquivo | Behaviors Validados |
|---------|---------------------|
| `validate_multi_agent_flow.py` | Fluxo orquestrador→estruturador→metodologista |
| `validate_refinement_loop.py` | Loop de refinamento |

### Estruturador
| Arquivo | Behaviors Validados |
|---------|---------------------|
| `validate_structurer.py` | Estruturação de questões |
| `validate_structurer_refinement.py` | Refinamento com gaps |
| `validate_build_context.py` | Construção de contexto |

### Interface
| Arquivo | Behaviors Validados |
|---------|---------------------|
| `validate_dashboard.py` | Dashboard Streamlit |
| `validate_cli.py` | CLI do Metodologista |
| `validate_cli_integration.py` | Integração CLI→EventBus→Dashboard |
| `validate_memory_integration.py` | Integração de memória |

---

## ❌ Comportamentos NÃO Cobertos (gaps)

Comportamentos da visão que ainda não têm testes:

- [x] Sistema transiciona automaticamente para agentes sem pedir permissão (Épico 1.1 - transição fluida)
- [ ] Claim evolui para "flecha penetrante" (argumento maduro com evidências)
- [ ] Sistema detecta tipo de artigo emergente (empírico, revisão, teórico)
- [ ] Validação end-to-end com usuário real simulado
- [ ] Métricas de qualidade socrática (score de provocação vs coleta)

---

## 📋 Regras para Claude

### ANTES de criar teste novo:
1. Consulte este inventário
2. Verifique se comportamento já está coberto
3. Se coberto → adicione ao arquivo existente
4. Se não coberto → crie novo arquivo OU adicione a "gaps"

### APÓS criar/modificar teste:
1. Atualize este inventário
2. Rode o teste para validar
3. Commit com mensagem clara

---

**Última atualização**: Dezembro 2025

