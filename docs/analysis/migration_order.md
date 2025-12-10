# Análise 3: Ordem de Migração Segura

## 1. Princípio Fundamental

**Regra de Ouro:** Migrar primeiro módulos que NINGUÉM depende (folhas da árvore de dependências).

- Se A depende de B, migrar B primeiro
- Migrar "folhas" antes de "raízes"
- Isso minimiza quebras porque dependentes ainda não foram movidos

## 2. Mapeamento de Dependências

### 2.1. Módulos Folha (Ninguém Depende)

Estes módulos são independentes e podem ser migrados primeiro sem quebrar nada:

1. **`utils/`** - Utilitários básicos
   - Dependências: Apenas bibliotecas externas (langchain, pydantic, etc)
   - Usado por: ~50 arquivos
   - Módulos: `json_parser`, `config`, `token_extractor`, `event_bus`, `cost_tracker`, `currency`, `debug_analyzer`, `structured_logger`, `test_executor`, `test_scenarios`, `providers/`

2. **`config/`** - Configurações YAML
   - Dependências: Nenhuma (apenas arquivos YAML)
   - Usado por: `agents/memory/config_loader.py`
   - Módulos: `agents/orchestrator.yaml`, `agents/observer.yaml`, `agents/methodologist.yaml`, `agents/structurer.yaml`

3. **`agents/models/`** - Modelos Pydantic
   - Dependências: Apenas bibliotecas externas (pydantic)
   - Usado por: ~15 arquivos
   - Módulos: `cognitive_model.py`, `proposition.py`, `clarification.py`

4. **`agents/database/`** - Schema e CRUD
   - Dependências: Apenas bibliotecas externas (sqlite3)
   - Usado por: ~10 arquivos
   - Módulos: `schema.py`, `manager.py`, `ideas_crud.py`, `arguments_crud.py`

5. **`agents/checklist/`** - Progress Tracker
   - Dependências: Apenas bibliotecas externas
   - Usado por: Poucos arquivos
   - Módulos: `progress_tracker.py`

### 2.2. Módulos de Primeira Camada (Dependem Apenas de Folhas)

6. **`agents/memory/`** - Gerenciamento de Memória
   - Dependências: `utils/`, `config/`
   - Usado por: Todos os agentes
   - Módulos: `config_loader.py`, `config_validator.py`, `memory_manager.py`, `execution_tracker.py`

7. **`agents/persistence/`** - Snapshots
   - Dependências: `agents/memory/`, `agents/models/`
   - Usado por: `agents/orchestrator/`, `agents/observer/`
   - Módulos: `snapshot_manager.py`

### 2.3. Módulos de Segunda Camada (Agentes Individuais)

8. **`agents/orchestrator/`** - Agente Orquestrador
   - Dependências: `utils/`, `agents/memory/`, `agents/models/`, `agents/persistence/`
   - Usado por: `agents/multi_agent_graph.py`, `app/`, `cli/`
   - Módulos: `state.py`, `nodes.py`, `router.py`

9. **`agents/structurer/`** - Agente Estruturador
   - Dependências: `utils/`, `agents/memory/`
   - Usado por: `agents/multi_agent_graph.py`
   - Módulos: `nodes.py`

10. **`agents/methodologist/`** - Agente Metodologista
    - Dependências: `utils/`, `agents/memory/`
    - Usado por: `agents/multi_agent_graph.py`
    - Módulos: `state.py`, `nodes.py`, `router.py`, `graph.py`, `tools.py`, `wrapper.py`

11. **`agents/observer/`** - Agente Observador
    - Dependências: `utils/`, `agents/memory/`, `agents/models/`, `agents/database/`
    - Usado por: `agents/multi_agent_graph.py`
    - Módulos: `api.py`, `state.py`, `nodes.py`, `extractors.py`, `metrics.py`, `prompts.py`, `catalog.py`, `embeddings.py`, `concept_pipeline.py`, `clarification.py`, `clarification_prompts.py`

### 2.4. Módulos de Terceira Camada (Integração)

12. **`agents/multi_agent_graph.py`** - Grafo Principal
    - Dependências: TODOS os agentes acima
    - Usado por: `app/`, `cli/`
    - Arquivo único: `multi_agent_graph.py`

### 2.5. Módulos de Produto (Dependem de Core)

13. **`cli/`** - Interface CLI
    - Dependências: `agents/`, `utils/`
    - Usado por: Ninguém (ponto de entrada)
    - Módulos: `chat.py`

14. **`app/`** - Interface Web
    - Dependências: `agents/`, `utils/`
    - Usado por: Ninguém (ponto de entrada)
    - Módulos: `chat.py`, `dashboard.py`, `components/`, `pages/`

### 2.6. Módulos de Suporte (Dependem de Tudo)

15. **`tests/`** - Testes Automatizados
    - Dependências: TUDO
    - Usado por: Ninguém (execução externa)
    - Estrutura: `unit/`, `integration/`

16. **`scripts/`** - Scripts de Desenvolvimento
    - Dependências: TUDO
    - Usado por: Ninguém (execução externa)
    - Estrutura: `health_checks/`, `testing/`, `debug/`, `spikes/`, `flows/`

17. **`docs/`** - Documentação
    - Dependências: Nenhuma (apenas referências)
    - Usado por: Ninguém (leitura)
    - Estrutura: Múltiplos diretórios

## 3. Proposta de Ordem de Migração

### Fase 1: Folhas Fundamentais (Ninguém Depende)

**Módulos:**
- `utils/` → `core/utils/`
- `config/` → `core/config/`
- `agents/models/` → `core/agents/models/`
- `agents/database/` → `core/agents/database/`
- `agents/checklist/` → `core/agents/checklist/`

**Justificativa:**
- Estes módulos são folhas da árvore de dependências
- Ninguém depende deles diretamente (apenas usam)
- Podem ser movidos sem quebrar imports porque dependentes ainda estão na raiz
- Após mover, ajustar imports em dependentes será simples

**Riscos Evitados:**
- ✅ Não quebra nenhum módulo porque dependentes ainda não foram movidos
- ✅ Imports em dependentes continuam funcionando (`from utils.` ainda funciona na raiz)
- ✅ Testes continuam passando (estrutura ainda compatível)

**O Que Pode Quebrar:**
- Nada! Estes módulos são independentes

**Ponto de Pausa Seguro:**
✅ **Após Fase 1, sistema está funcional.** Core básico movido, mas dependentes ainda na raiz.

---

### Fase 2: Camada de Memória (Depende de Folhas)

**Módulos:**
- `agents/memory/` → `core/agents/memory/`
- `agents/persistence/` → `core/agents/persistence/`

**Justificativa:**
- Dependem apenas de módulos já migrados na Fase 1
- São pré-requisitos para todos os agentes
- Migrar antes dos agentes evita dependências circulares

**Riscos Evitados:**
- ✅ Agentes ainda não foram movidos, então não há quebra de imports
- ✅ `agents/memory/` já está em `core/agents/`, então imports internos continuam funcionando

**O Que Pode Quebrar:**
- Nada crítico! Agentes ainda na raiz podem importar `from agents.memory.` normalmente

**Ponto de Pausa Seguro:**
✅ **Após Fase 2, sistema está funcional.** Memória movida, agentes ainda na raiz.

---

### Fase 3: Agentes Individuais (Dependem de Memória)

**Módulos:**
- `agents/orchestrator/` → `core/agents/orchestrator/`
- `agents/structurer/` → `core/agents/structurer/`
- `agents/methodologist/` → `core/agents/methodologist/`
- `agents/observer/` → `core/agents/observer/`

**Justificativa:**
- Todos dependem de `agents/memory/` (já migrado)
- São independentes entre si (não há dependência direta entre agentes)
- Podem ser migrados em qualquer ordem, mas juntos é mais eficiente

**Riscos Evitados:**
- ✅ `multi_agent_graph.py` ainda não foi migrado, então não há quebra
- ✅ Imports internos entre agentes continuam funcionando (`from agents.orchestrator.`)

**O Que Pode Quebrar:**
- `agents/multi_agent_graph.py` ainda importa `from agents.orchestrator.` (ainda funciona)
- `app/` e `cli/` ainda importam `from agents.` (ainda funciona)

**Ponto de Pausa Seguro:**
✅ **Após Fase 3, sistema está funcional.** Todos os agentes movidos, grafo ainda na raiz.

---

### Fase 4: Grafo Principal (Depende de Todos os Agentes)

**Módulos:**
- `agents/multi_agent_graph.py` → `core/agents/multi_agent_graph.py`

**Justificativa:**
- Depende de TODOS os agentes (já migrados)
- É o ponto de integração do sistema
- Após migrar, precisa ajustar imports para `from core.agents.`

**Riscos Evitados:**
- ✅ Agentes já estão em `core/agents/`, então imports internos são simples
- ✅ `app/` e `cli/` ainda não foram migrados, então não há quebra

**O Que Pode Quebrar:**
- `app/` e `cli/` ainda importam `from agents.multi_agent_graph` (precisa ajustar para `from core.agents.multi_agent_graph`)

**Ponto de Pausa Seguro:**
✅ **Após Fase 4, sistema está funcional.** Core completo movido, produtos ainda na raiz.

---

### Fase 5: Produtos (Dependem de Core)

**Módulos:**
- `cli/` → `core/tools/cli/` (ou `products/revelar/cli/` se for específico)
- `app/` → `products/revelar/app/`

**Justificativa:**
- Dependem de `agents/` e `utils/` (já migrados para `core/`)
- São pontos de entrada, não são dependidos por outros módulos
- Podem ser migrados juntos ou separadamente

**Riscos Evitados:**
- ✅ Ninguém depende deles, então não há quebra de dependentes
- ✅ Apenas precisam ajustar imports para `from core.`

**O Que Pode Quebrar:**
- Imports internos precisam ser ajustados
- Caminhos de configuração podem precisar ajuste (se houver paths relativos)

**Ponto de Pausa Seguro:**
✅ **Após Fase 5, sistema está funcional.** Core e produto movidos, testes ainda na raiz.

---

### Fase 6: Testes (Dependem de Tudo)

**Módulos:**
- `tests/unit/` → `tests/core/unit/`
- `tests/integration/` (maioria) → `tests/core/integration/`
- `tests/integration/` (3 arquivos específicos) → `tests/products/revelar/integration/`

**Justificativa:**
- Dependem de tudo que já foi migrado
- Podem ser migrados após tudo estar estável
- Reorganização por core/produto é opcional mas recomendado

**Riscos Evitados:**
- ✅ Testes são isolados, não afetam execução do sistema
- ✅ Podem ser migrados gradualmente

**O Que Pode Quebrar:**
- Imports em testes precisam ser ajustados
- Caminhos de fixtures podem precisar ajuste

**Ponto de Pausa Seguro:**
✅ **Após Fase 6, sistema está funcional.** Testes organizados.

---

### Fase 7: Scripts (Dependem de Tudo)

**Módulos:**
- `scripts/health_checks/` → `scripts/core/`
- `scripts/testing/` → `scripts/core/` ou `scripts/revelar/`
- `scripts/flows/` → `scripts/revelar/`
- `scripts/debug/` → `scripts/core/`
- `scripts/spikes/` → `scripts/core/`

**Justificativa:**
- Dependem de tudo que já foi migrado
- São ferramentas de desenvolvimento, não afetam execução do sistema
- Podem ser migrados após tudo estar estável

**Riscos Evitados:**
- ✅ Scripts são isolados, não afetam execução do sistema
- ✅ Podem ser migrados gradualmente

**O Que Pode Quebrar:**
- Imports em scripts precisam ser ajustados
- Caminhos relativos podem precisar ajuste

**Ponto de Pausa Seguro:**
✅ **Após Fase 7, sistema está funcional.** Scripts organizados.

---

### Fase 8: Documentação (Referências)

**Módulos:**
- `docs/architecture/` → `docs/core/architecture/`
- `docs/agents/` → `docs/core/agents/`
- `docs/interface/` → `docs/products/revelar/interface/`
- `docs/products/paper_agent.md` → `docs/products/revelar/`
- Atualizar ~500 referências internas

**Justificativa:**
- Apenas referências, não afeta execução
- Pode ser feito gradualmente
- Importante para manter documentação atualizada

**Riscos Evitados:**
- ✅ Documentação não afeta execução do sistema
- ✅ Links quebrados podem ser corrigidos gradualmente

**O Que Pode Quebrar:**
- Links internos podem quebrar
- Referências a caminhos antigos precisam ser atualizadas

**Ponto de Pausa Seguro:**
✅ **Após Fase 8, migração está completa!** 🎉

---

## 4. Resumo da Ordem de Migração

| Fase | Módulos | Dependências | Risco | Pausa Segura |
|------|---------|--------------|-------|--------------|
| **1** | `utils/`, `config/`, `agents/models/`, `agents/database/`, `agents/checklist/` | Nenhuma (folhas) | 🟢 Zero | ✅ Sim |
| **2** | `agents/memory/`, `agents/persistence/` | Fase 1 | 🟢 Zero | ✅ Sim |
| **3** | `agents/orchestrator/`, `agents/structurer/`, `agents/methodologist/`, `agents/observer/` | Fase 2 | 🟢 Baixo | ✅ Sim |
| **4** | `agents/multi_agent_graph.py` | Fase 3 | 🟡 Médio | ✅ Sim |
| **5** | `cli/`, `app/` | Fase 4 | 🟡 Médio | ✅ Sim |
| **6** | `tests/` | Fase 5 | 🟡 Médio | ✅ Sim |
| **7** | `scripts/` | Fase 6 | 🟡 Médio | ✅ Sim |
| **8** | `docs/` | Nenhuma | 🟢 Zero | ✅ Sim |

## 5. Pontos de Pausa Estratégicos

### Pausa 1: Após Fase 1 (Folhas)
**Status:** Core básico movido, sistema funcional
- ✅ Utilitários e modelos movidos
- ✅ Configurações movidas
- ✅ Nenhuma quebra de dependências

### Pausa 2: Após Fase 2 (Memória)
**Status:** Memória movida, sistema funcional
- ✅ Memória e persistência movidas
- ✅ Agentes ainda na raiz (funcionam normalmente)
- ✅ Nenhuma quebra crítica

### Pausa 3: Após Fase 3 (Agentes)
**Status:** Agentes movidos, sistema funcional
- ✅ Todos os agentes movidos
- ✅ Grafo ainda na raiz (funciona normalmente)
- ✅ Produtos ainda na raiz (funcionam normalmente)

### Pausa 4: Após Fase 4 (Grafo)
**Status:** Core completo movido, sistema funcional
- ✅ Core 100% movido
- ✅ Produtos ainda na raiz (precisam ajustar imports)
- ✅ Sistema funcional com ajustes mínimos

### Pausa 5: Após Fase 5 (Produtos)
**Status:** Core e produtos movidos, sistema funcional
- ✅ Core e produtos movidos
- ✅ Testes ainda na raiz (podem ser migrados depois)
- ✅ Sistema 100% funcional

### Pausa 6: Após Fase 6-8 (Completo)
**Status:** Migração completa
- ✅ Tudo migrado e organizado
- ✅ Documentação atualizada
- ✅ Sistema pronto para evolução

## 6. Estratégias de Mitigação de Riscos

### 6.1. Imports Temporários (NÃO Recomendado)

Se necessário manter compatibilidade temporária:
```python
# core/agents/__init__.py
# (temporário, remover depois)
import sys
sys.modules['agents'] = sys.modules['core.agents']
```

**Não recomendado:** Adiciona complexidade. Prefira ajustar imports de uma vez.

### 6.2. Validação Contínua

Após cada fase:
```bash
# Validar imports
python -c "from core.agents.orchestrator import orchestrator_node"

# Rodar testes
pytest tests/unit/ -v

# Validar execução
python -m core.tools.cli.chat  # ou streamlit run products/revelar/app/chat.py
```

### 6.3. Commits Incrementais

- Cada fase = commit separado
- Facilita rollback se necessário
- Permite pausar entre fases

## 7. Análise de Impacto por Fase

### Fase 1: Impacto Baixo
- **Arquivos afetados:** ~5 diretórios
- **Imports a ajustar:** ~0 (dependentes ainda na raiz)
- **Risco de quebra:** Zero
- **Tempo estimado:** 30min - 1h

### Fase 2: Impacto Baixo
- **Arquivos afetados:** ~2 diretórios
- **Imports a ajustar:** ~0 (agentes ainda na raiz)
- **Risco de quebra:** Zero
- **Tempo estimado:** 30min - 1h

### Fase 3: Impacto Médio
- **Arquivos afetados:** ~4 diretórios
- **Imports a ajustar:** ~0 (grafo ainda na raiz)
- **Risco de quebra:** Baixo
- **Tempo estimado:** 1-2h

### Fase 4: Impacto Médio
- **Arquivos afetados:** 1 arquivo
- **Imports a ajustar:** ~10 (em app/ e cli/)
- **Risco de quebra:** Médio
- **Tempo estimado:** 30min - 1h

### Fase 5: Impacto Alto
- **Arquivos afetados:** ~2 diretórios
- **Imports a ajustar:** ~50+ (todos os imports em app/ e cli/)
- **Risco de quebra:** Médio-Alto
- **Tempo estimado:** 1-2h

### Fase 6: Impacto Médio
- **Arquivos afetados:** ~75 arquivos de teste
- **Imports a ajustar:** ~100+ (todos os imports em testes)
- **Risco de quebra:** Médio
- **Tempo estimado:** 1-2h

### Fase 7: Impacto Baixo
- **Arquivos afetados:** ~20 scripts
- **Imports a ajustar:** ~30 (imports em scripts)
- **Risco de quebra:** Baixo
- **Tempo estimado:** 30min - 1h

### Fase 8: Impacto Baixo
- **Arquivos afetados:** ~500 referências
- **Imports a ajustar:** 0 (apenas links)
- **Risco de quebra:** Zero (não afeta execução)
- **Tempo estimado:** 2-3h

## 8. Conclusão

A ordem proposta segue o princípio de **migrar folhas antes de raízes**, garantindo:

1. ✅ **Mínimas quebras:** Cada fase migra módulos que ninguém depende
2. ✅ **Pausas seguras:** Sistema funcional após cada fase
3. ✅ **Progresso incremental:** Pode pausar e retomar a qualquer momento
4. ✅ **Validação contínua:** Testes podem rodar após cada fase

**Recomendação:** Seguir esta ordem exata para minimizar riscos e permitir pausas estratégicas.

---

**Versão:** 1.0  
**Data:** 2025-01-XX  
**Status:** Análise completa - pronta para execução

