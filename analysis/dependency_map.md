# Mapeamento de Dependências (Imports)

Análise completa de todos os imports do projeto.

## 1. Hotspots de Importação (Top 20)

Módulos mais importados no projeto:

| Módulo | Contagem |
|--------|----------|
| `pathlib` | 68 |
| `typing` | 65 |
| `sys` | 55 |
| `logging` | 53 |
| `agents.orchestrator.nodes` | 38 |
| `traceback` | 38 |
| `langchain_core.messages` | 37 |
| `pytest` | 37 |
| `agents.orchestrator.state` | 36 |
| `json` | 31 |
| `agents.multi_agent_graph` | 29 |
| `datetime` | 27 |
| `os` | 27 |
| `agents.observer.clarification` | 26 |
| `dotenv` | 22 |
| `utils.event_bus` | 21 |
| `time` | 16 |
| `unittest.mock` | 16 |
| `streamlit` | 14 |
| `sqlite3` | 12 |

## 2. Dependências por Diretório

Análise de imports cruzados entre diretórios principais:

### `other/` importa de:

| Diretório | Quantidade |
|-----------|------------|
| `agents/` | 232 |
| `utils/` | 93 |
| `app/` | 23 |
| `scripts/` | 12 |

## 3. Dependências Circulares

✅ **Nenhuma dependência circular detectada.**


## 4. Imports Relativos vs Absolutos

| Tipo | Quantidade | Percentual |
|------|------------|------------|
| Relativos (`from .`) | 0 | 0.0% |
| Absolutos (`from agents.`) | 1039 | 100.0% |
| **Total** | **1039** | **100%** |

> ⚠️ **Nota**: Imports relativos podem quebrar após migração de estrutura de diretórios.


## 5. Arquivos com Mais Imports (Top 10)

Arquivos críticos para migração (maior número de dependências):

| Arquivo | Total de Imports |
|---------|------------------|
| `scripts/validate_clarification_questions.py` | 24 |
| `tests/unit/test_clarification.py` | 23 |
| `agents/orchestrator/nodes.py` | 22 |
| `tests/unit/test_observer_orchestrator_integration.py` | 22 |
| `agents/methodologist/nodes.py` | 18 |
| `scripts/validate_observer_integration.py` | 18 |
| `agents/multi_agent_graph.py` | 17 |
| `agents/structurer/nodes.py` | 17 |
| `scripts/debug/debug_multi_agent.py` | 17 |
| `tests/integration/behavior/test_observer_integration.py` | 16 |

## Estatísticas Gerais

- **Total de arquivos Python analisados**: 194

- **Total de imports únicos**: 138

- **Total de imports (com repetição)**: 1039
