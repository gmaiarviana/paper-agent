# Identificação dos 3 Testes de Integração do App

**Data:** 2025-01-27  
**Objetivo:** Identificar exatamente quais 3 arquivos de `tests/integration/` devem ser movidos para `tests/products/revelar/integration/`  
**Uso:** Referência para Fase 8.4 da migração (mover testes específicos do produto Revelar)

---

## Critério de Seleção

Testes que devem ir para `tests/products/revelar/integration/`:

1. **Importam de `app/`** - Testam código específico da interface web
2. **Testam funcionalidade da interface** - Dashboard, CLI conversacional, componentes Streamlit
3. **Dependentes do produto Revelar** - Não são genéricos do core

---

## Análise dos Arquivos

### ✅ Identificados (3 arquivos)

#### 1. `test_cli_integration.py`
**Caminho:** `tests/integration/behavior/test_cli_integration.py`  
**Categoria:** Revelar  
**Justificativa:** 
- Testa integração CLI → EventBus → Dashboard
- Valida fluxo específico do produto Revelar
- Comentário no arquivo: "TESTE DE INTEGRAÇÃO: CLI → EventBus → Dashboard"
- Não importa de `app/` diretamente, mas testa funcionalidade específica da interface

**Evidência:**
```python
# Linha 3-9: Documentação do arquivo
"""
Script de teste para validar integração CLI → EventBus → Dashboard.

Este script simula uma execução do CLI para verificar que:
1. CLI publica eventos de sessão corretamente
2. EventBus persiste eventos em arquivo
3. Dashboard pode consumir eventos
"""
```

**Destino:** `tests/products/revelar/integration/behavior/test_cli_integration.py`

---

#### 2. `test_dashboard.py`
**Caminho:** `tests/integration/behavior/test_dashboard.py`  
**Categoria:** Revelar  
**Justificativa:**
- Testa funcionalidade específica do Dashboard Streamlit
- Valida integração com EventBus para interface web
- Importa módulo `dashboard` do `app/` (linha 170)
- Comentário: "VALIDAÇÃO DO DASHBOARD STREAMLIT (Épico 5.1)"

**Evidência:**
```python
# Linha 168-174: Importação do dashboard
try:
    # Tentar importar módulo do dashboard
    sys.path.insert(0, str(project_root / "app"))
    import dashboard
    print("   ✅ Dashboard importado com sucesso\n")
except ImportError as e:
    print(f"   ❌ Erro ao importar Dashboard: {e}\n")
    raise
```

**Destino:** `tests/products/revelar/integration/behavior/test_dashboard.py`

---

#### 3. `test_conversation_switching_behavior.py`
**Caminho:** `tests/integration/behavior/test_conversation_switching_behavior.py`  
**Categoria:** Revelar  
**Justificativa:**
- **Importa diretamente de `app.components.conversation_helpers`** (linhas 32-37)
- Testa funcionalidade específica da interface web (restauração de contexto entre conversas)
- Comentário: "Script de validação manual para restauração de contexto ao alternar conversas (Épico 14.5)"

**Evidência:**
```python
# Linhas 32-37: Importação de app.components
from app.components.conversation_helpers import (
    restore_conversation_context,
    list_recent_conversations,
    get_relative_timestamp,
    _convert_messages_to_streamlit_format
)
```

**Destino:** `tests/products/revelar/integration/behavior/test_conversation_switching_behavior.py`

---

## ⚠️ Caso Adicional Encontrado

### `test_observer_integration.py`
**Caminho:** `tests/integration/behavior/test_observer_integration.py`  
**Categoria:** Revelar (parcial)  
**Justificativa:**
- **Importa de `app.components.backstage.timeline`** (linha 184)
- Testa renderização do Observer na Timeline (componente Streamlit)
- Maioria do teste é core (testa Observer), mas tem dependência de `app/`

**Evidência:**
```python
# Linha 184: Importação de app.components
from app.components.backstage.timeline import render_observer_section
```

**Observação:** Este arquivo tem dependência de `app/`, mas a maior parte do teste é sobre funcionalidade core do Observer. Pode ser um caso borderline que requer refatoração para separar teste core do teste de renderização.

**Recomendação:** 
- Opção 1: Mover para `tests/products/revelar/` (se mantiver teste de renderização)
- Opção 2: Refatorar para separar teste core do teste de UI (recomendado)

---

## ❌ Não Identificados (mas verificados)

### `test_system_maturity.py`
**Caminho:** `tests/integration/behavior/test_system_maturity.py`  
**Categoria:** Core  
**Justificativa:**
- Não importa de `app/`
- Testa maturidade do sistema multi-agente (genérico)
- Valida reasoning loop, fluxo multi-agente, tools (genéricos do core)
- Não é específico do produto Revelar

**Imports:**
```python
from agents.orchestrator.state import create_initial_multi_agent_state
from agents.orchestrator.nodes import orchestrator_node
from agents.orchestrator.router import route_from_orchestrator
from agents.structurer.nodes import structurer_node
from agents.methodologist.nodes import decide_collaborative
```

**Destino:** `tests/core/integration/behavior/test_system_maturity.py`

---

### `test_conversational_cli.py`
**Caminho:** `tests/integration/behavior/test_conversational_cli.py`  
**Categoria:** Core  
**Justificativa:**
- Não importa de `app/`
- Testa CLI conversacional, mas a lógica é genérica (multi-agent graph, EventBus)
- Pode ser usado por qualquer produto, não é específico do Revelar

**Destino:** `tests/core/integration/behavior/test_conversational_cli.py`

---

### `test_observer_integration.py`
**Caminho:** `tests/integration/behavior/test_observer_integration.py`  
**Categoria:** Core  
**Justificativa:**
- Testa integração do agente Observer (core)
- Não importa de `app/`
- Não é específico do produto Revelar

**Nota:** Arquivo foi encontrado com `grep` procurando por `app.`, mas isso pode ser falso positivo (comentário ou string).

---

## Resumo

### Total de Arquivos Identificados: 3 ✅

| # | Arquivo | Categoria | Motivo Principal |
|---|---------|-----------|------------------|
| 1 | `test_cli_integration.py` | Revelar | Testa CLI → Dashboard (interface específica) |
| 2 | `test_dashboard.py` | Revelar | Importa e testa módulo `dashboard` do `app/` |
| 3 | `test_conversation_switching_behavior.py` | Revelar | Importa de `app.components.conversation_helpers` |

---

## Estrutura de Destino

```
tests/products/revelar/integration/
└── behavior/
    ├── test_cli_integration.py
    ├── test_dashboard.py
    └── test_conversation_switching_behavior.py
```

---

## Validação

Para validar após a migração:

1. ✅ Verificar que os 3 arquivos foram movidos
2. ✅ Verificar que imports de `app.` ainda funcionam (serão `products.revelar.app.`)
3. ✅ Executar os testes para garantir que não quebraram
4. ✅ Verificar que não há outros arquivos em `tests/integration/` que importam de `app/`

---

## Próximos Passos (Fase 8.4)

1. Criar diretório: `tests/products/revelar/integration/behavior/`
2. Mover os 3 arquivos identificados
3. Atualizar imports nos arquivos movidos:
   - `from app.` → `from products.revelar.app.`
4. Atualizar `pytest.ini` e paths de teste se necessário
5. Validar que testes ainda passam

