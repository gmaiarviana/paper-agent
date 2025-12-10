# Categorização Completa de Scripts

Este documento categoriza TODOS os arquivos em `scripts/` para determinar se devem ir para `scripts/core/` ou `scripts/revelar/` na Fase 9.

**Critério**:
- **Core**: Scripts genéricos, reutilizáveis, não específicos de produto
- **Revelar**: Scripts específicos da interface Revelar (app Streamlit)

---

## ✅ scripts/core/ - Scripts Genéricos

### health_checks/ → scripts/core/health_checks/
Todos os scripts de validação genérica:

1. **`scripts/health_checks/validate_agent_config.py`**
   - Valida configurações YAML de agentes
   - ✅ **Core**: Genérico, não específico de produto

2. **`scripts/health_checks/validate_api.py`**
   - Valida conectividade com APIs (Anthropic)
   - ✅ **Core**: Utilitário genérico

3. **`scripts/health_checks/validate_execution_tracker.py`**
   - Valida implementação do ExecutionTracker
   - ✅ **Core**: Testa componente core

4. **`scripts/health_checks/validate_orchestrator_json_parsing.py`**
   - Valida parsing de JSON do Orquestrador
   - ✅ **Core**: Testa componente core

5. **`scripts/health_checks/validate_runtime_config_simple.py`**
   - Valida configurações de runtime
   - ✅ **Core**: Utilitário genérico

6. **`scripts/health_checks/validate_syntax.py`**
   - Valida sintaxe de arquivos Python
   - ✅ **Core**: Utilitário genérico

7. **`scripts/health_checks/validate_system_prompt.py`**
   - Valida system prompts dos agentes
   - ✅ **Core**: Testa componentes core

### debug/ → scripts/core/debug/
Scripts de diagnóstico e depuração:

8. **`scripts/debug/check_events.py`**
   - Diagnóstico do EventBus
   - ✅ **Core**: Utilitário genérico de debug

9. **`scripts/debug/debug_multi_agent.py`**
   - Diagnóstico do super-grafo multi-agente
   - ✅ **Core**: Testa componente core

### spikes/ → scripts/core/spikes/
Spikes experimentais:

10. **`scripts/spikes/validate_cognitive_model_access.py`**
    - Spike: Testa se Claude usa CognitiveModel via prompt
    - ✅ **Core**: Experimentação genérica

11. **`scripts/spikes/validate_langgraph_parallel.py`**
    - Spike: Valida execução paralela no LangGraph
    - ✅ **Core**: Experimentação genérica

### testing/ → scripts/core/testing/
Scripts de teste e cenários:

12. **`scripts/testing/run_scenario.py`**
    - Executa cenário específico de validação multi-turn
    - ✅ **Core**: Utilitário de teste genérico

13. **`scripts/testing/run_all_scenarios.py`**
    - Executa todos os cenários de teste
    - ✅ **Core**: Utilitário de teste genérico

14. **`scripts/testing/replay_session.py`**
    - Reproduz sessão anterior
    - ✅ **Core**: Utilitário de teste genérico

15. **`scripts/testing/execute_scenario.py`**
    - Executa cenário de teste
    - ✅ **Core**: Utilitário de teste genérico

16. **`scripts/testing/debug_scenario.py`**
    - Debug de cenários de teste
    - ✅ **Core**: Utilitário de teste genérico

17. **`scripts/testing/collect_scenario_logs.py`**
    - Coleta logs de cenários
    - ✅ **Core**: Utilitário de teste genérico

### Scripts Raiz → scripts/core/

18. **`scripts/analyze_imports.py`**
    - Analisa imports do projeto e gera relatório de dependências
    - ✅ **Core**: Utilitário de análise genérico

19. **`scripts/analyze_migration_impact.py`**
    - Analisa impacto da migração de cada módulo
    - ✅ **Core**: Utilitário de análise genérico (específico de migração, mas não de produto)

20. **`scripts/inspect_database.py`**
    - Inspeciona banco de dados do Paper Agent
    - ✅ **Core**: Utilitário genérico (não específico de Revelar)

21. **`scripts/validate_observer_integration.py`**
    - Valida integração do Observer (Épico 12)
    - ✅ **Core**: Testa componente core

22. **`scripts/validate_clarification_questions.py`**
    - Valida perguntas de clarificação
    - ✅ **Core**: Testa componente core

23. **`scripts/validate_direction_change.py`**
    - Valida detecção de mudanças do Observer (Épico 13.6)
    - ✅ **Core**: Testa componente core

24. **`scripts/common.py`**
    - Utilitários comuns para scripts de validação
    - ✅ **Core**: Biblioteca compartilhada

### state_introspection/ → scripts/core/state_introspection/
(Atualmente vazio, apenas `__init__.py`)

25. **`scripts/state_introspection/__init__.py`**
    - Diretório para scripts de introspecção de estado
    - ✅ **Core**: Utilitário genérico

---

## ✅ scripts/revelar/ - Scripts Específicos da Interface Revelar

### interface/ → scripts/revelar/interface/
(Atualmente vazio, apenas `__init__.py`)

26. **`scripts/interface/__init__.py`**
    - Diretório para scripts específicos da interface
    - ✅ **Revelar**: Nome indica scripts de interface (Streamlit)

### flows/ → scripts/revelar/flows/
(Atualmente vazio, apenas `__init__.py`)

27. **`scripts/flows/__init__.py`**
    - Diretório para scripts de fluxos
    - ✅ **Revelar**: Provavelmente fluxos específicos da interface Revelar
    - **Nota**: Confirmar com desenvolvedor se são fluxos de UI ou genéricos

---

## Resumo

| Categoria | Quantidade | Diretórios |
|-----------|------------|------------|
| **Core** | 25 arquivos | health_checks/, debug/, spikes/, testing/, state_introspection/, + 7 na raiz |
| **Revelar** | 2 diretórios vazios | interface/, flows/ |

### Estrutura Proposta para Fase 9

```
scripts/
├── core/
│   ├── health_checks/          (7 arquivos)
│   ├── debug/                  (2 arquivos)
│   ├── spikes/                 (2 arquivos)
│   ├── testing/                (6 arquivos)
│   ├── state_introspection/    (1 arquivo)
│   ├── analyze_imports.py
│   ├── analyze_migration_impact.py
│   ├── inspect_database.py
│   ├── validate_observer_integration.py
│   ├── validate_clarification_questions.py
│   ├── validate_direction_change.py
│   └── common.py
│
└── revelar/
    ├── interface/              (vazio - preparado para scripts de UI)
    └── flows/                  (vazio - preparado para fluxos específicos)
```

---

## Notas e Decisões Pendentes

1. **`scripts/flows/`**: Atualmente vazio. Confirmar se futuros scripts serão específicos da interface Revelar ou genéricos.

2. **`scripts/interface/`**: Atualmente vazio. Nome sugere scripts de interface, então classificado como Revelar.

3. **Scripts de análise**: `analyze_imports.py` e `analyze_migration_impact.py` são genéricos (análise de código), não específicos de produto.

4. **Scripts de validação na raiz**: Todos testam componentes core, não interface Revelar.

---

## Ações para Fase 9

1. Mover `health_checks/` → `scripts/core/health_checks/`
2. Mover `debug/` → `scripts/core/debug/`
3. Mover `spikes/` → `scripts/core/spikes/`
4. Mover `testing/` → `scripts/core/testing/`
5. Mover `state_introspection/` → `scripts/core/state_introspection/`
6. Mover 7 scripts da raiz → `scripts/core/`
7. Mover `interface/` → `scripts/revelar/interface/`
8. Mover `flows/` → `scripts/revelar/flows/`
9. Atualizar todos os imports e paths nos scripts após movimentação
10. Testar cada script após migração

---

**Última atualização**: Gerado automaticamente pela análise do código base

