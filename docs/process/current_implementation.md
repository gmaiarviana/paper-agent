# Implementação Atual: Épico 11 - Alinhamento de Ontologia

**Início:** 08/12/2025
**Branch:** `claude/epic-11-continue-01CbHwFD711NynxJQEcWFWng`

## Contexto

Épico 11 migra o sistema de premises/assumptions (strings separadas) para Proposições unificadas com solidez gradual.

### Features Já Concluídas
- ✅ **11.1** Schema Unificado (`agents/models/proposition.py`)
- ❌ **11.2** Adapter de Compatibilidade (CANCELADO - sem dados em produção)
- ✅ **11.3** Migrar CognitiveModel (`agents/models/cognitive_model.py`)
- ✅ **11.4** Migrar Observador (`agents/observer/*.py`)

### Features Restantes
- ⏳ **11.5** Migrar Orchestrator (e componentes relacionados)
- ⏳ **11.6** Migrar Interface
- ⏳ **11.7** Migrar Testes
- ⏳ **11.8** Limpeza Final

---

## Análise de Impacto

### Arquivos com referências a `premises`/`assumptions`:

**Camada Orchestrator (11.5):**
| Arquivo | Referências | Complexidade |
|---------|-------------|--------------|
| `agents/orchestrator/nodes.py` | 6 | Média |
| `agents/checklist/progress_tracker.py` | ~15 | Alta |
| `utils/prompts/orchestrator.py` | ~12 | Alta (prompts LLM) |
| `utils/event_models.py` | 2 | Baixa |
| `utils/event_bus/publishers.py` | 4 | Baixa |

**Camada Interface (11.6):**
| Arquivo | Referências | Complexidade |
|---------|-------------|--------------|
| `app/pages/_ideia_detalhes.py` | 6 | Baixa |
| `app/components/backstage.py` | ~12 | Média |
| `app/components/sidebar/ideas.py` | 2 | Baixa |

**Camada Testes (11.7):**
| Arquivo | Tipo |
|---------|------|
| `tests/unit/agents/test_orchestrator_logic.py` | Unit |
| `tests/integration/behavior/test_socratic_behavior.py` | Integration |
| `tests/integration/behavior/test_system_maturity.py` | Integration |

**Nota:** `agents/structurer/` NÃO tem referências - já está compatível!

---

## Plano de Checkpoints

### Checkpoint 1 (PR #1) - Orchestrator Core
**Features:** 11.5 (parcial)
**Escopo:**
- `agents/orchestrator/nodes.py` → usar `proposicoes`
- `utils/prompts/orchestrator.py` → atualizar prompts para nova estrutura JSON
- `utils/event_models.py` → adaptar para proposições
- `utils/event_bus/publishers.py` → adaptar publishers

**Estimativa:** ~300-400 linhas modificadas
**Risco:** Médio (prompts LLM precisam ser cuidadosamente ajustados)
**Valor:** Orchestrator gera cognitive_model com proposições

**Validação:**
```bash
pytest tests/unit/agents/test_orchestrator_logic.py -v
python -c "from agents.orchestrator.nodes import process_turn; print('OK')"
```

---

### Checkpoint 2 (PR #2) - Checklist + Interface
**Features:** 11.5 (completo) + 11.6
**Escopo:**
- `agents/checklist/progress_tracker.py` → usar proposições para inferir progresso
- `app/pages/_ideia_detalhes.py` → exibir proposições com solidez
- `app/components/backstage.py` → inferir status de proposições
- `app/components/sidebar/ideas.py` → preview de proposições

**Estimativa:** ~400-500 linhas modificadas
**Risco:** Baixo (lógica de UI é direta)
**Valor:** Sistema end-to-end com proposições

**Validação:**
```bash
pytest tests/unit/ -v -k "checklist or backstage"
streamlit run app/main.py  # Testar manualmente
```

---

### Checkpoint 3 (PR #3) - Testes + Limpeza
**Features:** 11.7 + 11.8
**Escopo:**
- `tests/unit/agents/test_orchestrator_logic.py` → usar proposições
- `tests/integration/behavior/test_socratic_behavior.py` → atualizar
- `tests/integration/behavior/test_system_maturity.py` → atualizar
- Buscar e remover qualquer referência residual a premises/assumptions
- Deletar este arquivo (`current_implementation.md`)

**Estimativa:** ~200-300 linhas modificadas
**Risco:** Baixo
**Valor:** Épico 11 completo, código limpo

**Validação:**
```bash
pytest tests/ -v
grep -r "premises\|assumptions" agents/ app/ utils/ --include="*.py"  # Deve retornar vazio
```

---

## Status dos Checkpoints

| Checkpoint | Features | Status | Branch | PR |
|------------|----------|--------|--------|-----|
| 1 | 11.5 (parcial) | ⏳ Pendente | - | - |
| 2 | 11.5 + 11.6 | ⏳ Pendente | - | - |
| 3 | 11.7 + 11.8 | ⏳ Pendente | - | - |

---

## Notas de Implementação

### Mapeamento de Conceitos
| Antigo | Novo |
|--------|------|
| `premises: List[str]` | `proposicoes: List[Proposicao]` onde `solidez >= 0.7` |
| `assumptions: List[str]` | `proposicoes: List[Proposicao]` onde `solidez < 0.7` ou `solidez = None` |
| `len(premises) >= 2` | `len(model.get_solid_propositions()) >= 2` |
| `len(assumptions) <= 2` | `len(model.get_fragile_propositions()) <= 2` |

### Prompts LLM
O formato JSON do cognitive_model nos prompts deve mudar de:
```json
{
  "claim": "...",
  "premises": ["...", "..."],
  "assumptions": ["...", "..."]
}
```
Para:
```json
{
  "claim": "...",
  "proposicoes": [
    {"texto": "...", "solidez": 0.8},
    {"texto": "...", "solidez": null}
  ]
}
```
