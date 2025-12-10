# MIGRATION.md - Reorganização para Monorepo Componentizado

## 1. Visão Geral

### Por que migrar?
- Preparar para super-sistema com múltiplos produtos
- Separar core compartilhado de produtos específicos
- Facilitar evolução independente de componentes

### Escopo da Mudança
- **200 arquivos** de código Python
- **144 arquivos** de documentação
- **348 imports** a ajustar em **151 arquivos**
- **~2000 referências** em documentação

### Estratégia de Execução

**Cursor (rápido):**
- Tarefas simples e mecânicas
- Substituições de imports (find/replace)
- Movimentação de arquivos (`git mv`)
- Validações rápidas (grep, pytest específico)

**Claude Code (complexo):**
- Ajustes de caminhos hardcoded
- Refatorações de lógica
- Validações extensivas (suite completa)
- Pull Requests com scripts de validação

---

## 2. Estado Atual (Antes da Migração)

```
paper-agent/
├── agents/          # Core + produto misturado
├── app/             # Interface web (produto Revelar)
├── cli/             # Interface CLI (ferramenta dev)
├── utils/           # Core + produto misturado
├── config/          # Core
├── tests/           # Core + produto misturado
├── scripts/         # Core + produto misturado
└── docs/            # Core + produto misturado
```

### Dados Reais das Análises

#### Imports
- **232 imports** de `agents/` em **84 arquivos**
- **93 imports** de `utils/` em **55 arquivos**
- **23 imports** de `app/` em **12 arquivos**
- **0 imports relativos** (100% absolutos - ótimo!)
- **Total:** 348 imports em 151 arquivos

#### Estrutura
- **200 arquivos** de código Python
- **144 arquivos** de documentação
- **344 arquivos** totais
- **0 dependências circulares** detectadas

#### Hotspots Críticos (arquivos com mais imports)
1. `agents/orchestrator/nodes.py` (22 imports)
2. `agents/multi_agent_graph.py` (17 imports)
3. `agents/methodologist/nodes.py` (18 imports)
4. `agents/structurer/nodes.py` (17 imports)

#### Arquivos com Caminhos Hardcoded
- `agents/memory/config_loader.py` (linha 16): `CONFIG_DIR = Path(__file__).parent.parent.parent / "config" / "agents"`
- `agents/observer/catalog.py` (linhas 30-31): `DEFAULT_CHROMA_PATH = "./data/chroma"`, `DEFAULT_SQLITE_PATH = "./data/concepts.db"`
- `agents/database/manager.py` (linha 48): `def __init__(self, db_path: str = "data/data.db")`
- **41 arquivos** usam `Path(__file__).parent` (verificar se quebram após migração)

---

## 3. Estado Desejado (Depois da Migração)

```
paper-agent-monorepo/
├── core/
│   ├── agents/
│   ├── prompts/
│   ├── utils/
│   ├── config/
│   ├── tools/cli/
│   └── ROADMAP.md
│
├── products/
│   └── revelar/
│       ├── app/
│       └── ROADMAP.md
│
├── tests/
│   ├── core/
│   │   ├── unit/
│   │   └── integration/
│   │       ├── smoke/
│   │       ├── behavior/
│   │       └── e2e/
│   └── products/
│       └── revelar/
│           └── integration/
│
├── scripts/
│   ├── core/
│   └── revelar/
│
├── docs/
│   ├── core/
│   └── products/
│       └── revelar/
│
├── ROADMAP.md       # Índice
└── MIGRATION.md     # Este arquivo
```

---

## 4. Riscos Críticos

### Arquivos de Alto Risco (revisão obrigatória)

1. **`agents/memory/config_loader.py`** (linha 16)
   - Caminho hardcoded: `Path(__file__).parent.parent.parent / "config" / "agents"`
   - Quebra após mover `config/` → `core/config/`
   - **Ação:** Ajustar para `Path(__file__).parent.parent.parent.parent / "core" / "config" / "agents"`

2. **`agents/observer/catalog.py`** (linhas 30-31)
   - Caminhos de dados: `"./data/chroma"`, `"./data/concepts.db"`
   - Relativos à raiz, podem quebrar se executado de outro diretório
   - **Ação:** Usar `Path(__file__).parent.parent.parent.parent / "data" / ...`

3. **`agents/database/manager.py`** (linha 48)
   - Caminho de DB: `"data/data.db"`
   - Similar ao anterior
   - **Ação:** Usar caminho absoluto baseado em `__file__`

4. **`agents/multi_agent_graph.py`** (17 imports)
   - Arquivo de integração crítica
   - Múltiplos imports de `agents/`, `utils/`
   - **Ação:** Revisar todos os imports após Fase 5

5. **Todos os scripts com `Path(__file__).parent`** (41 arquivos)
   - Podem quebrar após mover diretórios
   - **Ação:** Revisar cada um após mover para nova estrutura

### Validações Obrigatórias

1. **Após Fase 5 (Core completo):** `pytest tests/core/ -v`
2. **Após Fase 7 (App):** `streamlit run products/revelar/app/chat.py`
3. **Após Fase 8 (Testes):** Suite completa
4. **Fase 12 (Final):** Tudo funcionando

---

## 5. Fases da Migração

### Fase 0: Preparação ✅

**Status:** Concluída

- [x] Criar branch `refactor/monorepo-structure`
- [x] Analisar estrutura atual
- [x] Criar análises de impacto
- [x] Criar MIGRATION.md

**Pausa Segura:** ✅ Sim

---

### Fase 1: Estrutura Base

**Objetivo:** Criar diretórios vazios, sem mover código.

#### Fase 1.1: Criar Diretórios Principais

**Cursor (rápido):**
- [x] Criar `core/`
- [x] Criar `core/agents/`
- [x] Criar `core/prompts/`
- [x] Criar `core/utils/`
- [x] Criar `core/config/`
- [x] Criar `core/tools/`
- [x] Criar `core/tools/cli/`
- [x] Criar `products/`
- [x] Criar `products/revelar/`
- [x] Criar `products/revelar/app/`
- [x] Criar `tests/core/`
- [x] Criar `tests/core/unit/`
- [x] Criar `tests/core/integration/`
- [x] Criar `tests/core/integration/smoke/`
- [x] Criar `tests/core/integration/behavior/`
- [x] Criar `tests/core/integration/e2e/`
- [x] Criar `tests/products/`
- [x] Criar `tests/products/revelar/`
- [x] Criar `tests/products/revelar/integration/`
- [x] Criar `scripts/core/`
- [x] Criar `scripts/revelar/`
- [x] Criar `docs/core/`
- [x] Criar `docs/products/`
- [x] Criar `docs/products/revelar/`

**Comandos:**
```powershell
# Criar estrutura de diretórios
New-Item -ItemType Directory -Force -Path core/agents, core/prompts, core/utils, core/config, core/tools/cli
New-Item -ItemType Directory -Force -Path products/revelar/app
New-Item -ItemType Directory -Force -Path tests/core/unit, tests/core/integration/smoke, tests/core/integration/behavior, tests/core/integration/e2e
New-Item -ItemType Directory -Force -Path tests/products/revelar/integration
New-Item -ItemType Directory -Force -Path scripts/core, scripts/revelar
New-Item -ItemType Directory -Force -Path docs/core, docs/products/revelar
```

#### Fase 1.2: Criar `__init__.py` Necessários

**Cursor (rápido):**
- [x] Criar `core/__init__.py`
- [x] Criar `core/agents/__init__.py`
- [x] Criar `core/prompts/__init__.py`
- [x] Criar `core/utils/__init__.py`
- [x] Criar `core/config/__init__.py`
- [x] Criar `core/tools/__init__.py`
- [x] Criar `core/tools/cli/__init__.py`
- [x] Criar `products/__init__.py`
- [x] Criar `products/revelar/__init__.py`
- [x] Criar `products/revelar/app/__init__.py`
- [x] Criar `tests/core/__init__.py`
- [x] Criar `tests/core/unit/__init__.py`
- [x] Criar `tests/core/integration/__init__.py`
- [x] Criar `tests/core/integration/smoke/__init__.py`
- [x] Criar `tests/core/integration/behavior/__init__.py`
- [x] Criar `tests/core/integration/e2e/__init__.py`
- [x] Criar `tests/products/__init__.py`
- [x] Criar `tests/products/revelar/__init__.py`
- [x] Criar `tests/products/revelar/integration/__init__.py`
- [x] Criar `scripts/core/__init__.py`
- [x] Criar `scripts/revelar/__init__.py`

**Comandos:**
```powershell
# Criar __init__.py vazios
Get-ChildItem -Recurse -Directory | Where-Object { $_.Name -match '^(core|products|tests|scripts)' } | ForEach-Object { New-Item -ItemType File -Path "$($_.FullName)/__init__.py" -Force }
```

**Validação:**
- [x] Verificar: Testes continuam passando (nada mudou)
- [x] Verificar: Estrutura de diretórios criada corretamente

**Commit:** `refactor(migration): create monorepo directory structure`

**Pausa Segura:** ✅ Sim (sistema funcional, nada mudou)

---

### Fase 2: Core - Folhas (Independentes)

**Objetivo:** Mover módulos independentes do core, começando pelas folhas (sem dependências de outros módulos core).

#### Fase 2.1: Mover `utils/` → `core/utils/` (exceto prompts/)

**⚠️ IMPORTANTE - Ordem de Substituição:**
1. **PRIMEIRO:** Substituir `from utils.prompts.` → `from core.prompts.` (já feito na Fase 2.2, mas verificar antes)
2. **DEPOIS:** Substituir `from utils.` → `from core.utils.`

Se fizer na ordem errada, `from utils.prompts.` vira `from core.utils.prompts.` (incorreto).

**Cursor (rápido):**
- [x] `git mv utils core/utils` (exceto prompts/)
- [x] **PRIMEIRO:** Verificar se `from utils.prompts.` já foi convertido para `from core.prompts.`
- [x] **DEPOIS:** Find/Replace: `from utils.` → `from core.utils.` (excluir prompts/)
- [x] Validar: 0 matches de `from utils\.` (exceto prompts)

**Comandos:**
```powershell
# Mover utils (exceto prompts/)
git mv utils core/utils
# Nota: prompts/ será movido separadamente na Fase 2.2

# Find/Replace no Cursor (ORDEM CRÍTICA):
# 1. PRIMEIRO: Buscar: from utils\.prompts\.
#    Substituir: from core.prompts.
# 2. DEPOIS: Buscar: from utils\.
#    Substituir: from core.utils.
#    Excluir: prompts
```

**Validação Rápida (Cursor):**
```powershell
# Verificar que utils.prompts foi ajustado corretamente (antes de mover utils/)
Get-ChildItem -Recurse -Include *.py | Select-String "from utils\.prompts\." | Measure-Object
# Esperado: 0 matches (deve ter sido convertido para core.prompts)

# Verificar se não sobrou padrão antigo (exceto prompts)
Get-ChildItem -Recurse -Include *.py | Select-String "from utils\." | Where-Object { $_.Line -notmatch "prompts" } | Measure-Object
# Esperado: 0 matches
```

**Validação Completa (Claude Code):**
```powershell
# Rodar testes relacionados
pytest tests/unit/ -k utils -v
```

**Pausa Segura:** ✅ Sim (sistema funcional)

---

#### Fase 2.2: Mover `utils/prompts/` → `core/prompts/`

**Cursor (rápido):**
- [x] `git mv core/utils/prompts/* core/prompts/` (arquivos movidos)
- [x] Find/Replace: `from core.utils.prompts.` → `from core.prompts.`
- [x] Validar: 0 matches de `from utils.prompts\.` e `from core.utils.prompts\.`

**Comandos:**
```powershell
# Mover prompts
git mv utils/prompts core/prompts

# Find/Replace no Cursor:
# Buscar: from utils.prompts.
# Substituir: from core.prompts.
```

**Validação Rápida (Cursor):**
```powershell
Get-ChildItem -Recurse -Include *.py | Select-String "from utils.prompts\." | Measure-Object
# Esperado: 0 matches
```

**Validação Completa (Claude Code):**
```powershell
pytest tests/unit/ -k prompts -v
```

**Pausa Segura:** ✅ Sim

---

#### Fase 2.3: Mover `config/` → `core/config/`

**Cursor (rápido):**
- [x] `git mv config core/config`
- [x] Validar: Estrutura preservada

**Comandos:**
```powershell
git mv config core/config
```

**Validação:**
- [x] Verificar: `core/config/agents/*.yaml` existe

**Pausa Segura:** ✅ Sim (mas config_loader.py ainda não funciona)

---

#### Fase 2.4: Ajustar `agents/memory/config_loader.py` (caminho hardcoded + cache)

**Claude Code (complexo):**
- [x] Ajustar linha 16: `CONFIG_DIR = Path(__file__).parent.parent.parent / "config" / "agents"`
- [x] **Caminho correto:** Implementada função `_get_config_dir()` que detecta automaticamente a estrutura (antiga ou nova)
- [x] **Solução:** Função detecta se está em `core/agents/memory/` ou `agents/memory/` e ajusta o caminho automaticamente
- [x] **Adicionar cache em memória:** Implementado dict `_config_cache: Dict[str, Dict[str, Any]] = {}` que verifica cache antes de ler YAML do disco
- [x] Testar: `python -c "from agents.memory.config_loader import load_agent_config; print(load_agent_config('orchestrator')['model'])"` ✅

**Comando:**
```powershell
# Pedir ao Claude Code:
# "Ajuste o caminho hardcoded em core/agents/memory/config_loader.py linha 16 
#  para funcionar após mover config/ → core/config/"
# 
# Mudança necessária:
# ANTES: Path(__file__).parent.parent.parent / "config" / "agents"
# DEPOIS (opção 1): Path(__file__).parent.parent.parent.parent / "core" / "config" / "agents"
# DEPOIS (opção 2 - mais seguro):
#   project_root = Path(__file__).parent.parent.parent.parent
#   CONFIG_DIR = project_root / "core" / "config" / "agents"
#
# Também adicionar cache em memória:
# - Criar dict _config_cache: Dict[str, Dict[str, Any]] = {} no módulo
# - Em load_agent_config(), verificar cache antes de ler YAML do disco
# - Se não estiver em cache, carregar do disco e armazenar no cache
# - Benefício: elimina I/O repetido (config é carregado 3+ vezes por turno)
```

**Validação:**
```powershell
# Testar carregamento de config
python -c "from agents.memory.config_loader import load_agent_config; print(load_agent_config('orchestrator')['model'])"
```

**Pausa Segura:** ✅ Sim

---

#### Fase 2.5: Mover `agents/models/` → `core/agents/models/`

**Cursor (rápido):**
- [ ] `git mv agents/models core/agents/models`
- [ ] Find/Replace: `from agents.models.` → `from core.agents.models.`
- [ ] Validar: 0 matches de `from agents.models\.`

**Comandos:**
```powershell
git mv agents/models core/agents/models

# Find/Replace no Cursor:
# Buscar: from agents.models.
# Substituir: from core.agents.models.
```

**Validação:**
```powershell
Get-ChildItem -Recurse -Include *.py | Select-String "from agents.models\." | Measure-Object
# Esperado: 0 matches
```

**Pausa Segura:** ✅ Sim

---

#### Fase 2.6: Mover `agents/database/` → `core/agents/database/`

**Cursor (rápido):**
- [ ] `git mv agents/database core/agents/database`
- [ ] Find/Replace: `from agents.database.` → `from core.agents.database.`
- [ ] Validar: 0 matches de `from agents.database\.`

**Comandos:**
```powershell
git mv agents/database core/agents/database

# Find/Replace no Cursor:
# Buscar: from agents.database.
# Substituir: from core.agents.database.
```

**Validação:**
```powershell
Get-ChildItem -Recurse -Include *.py | Select-String "from agents.database\." | Measure-Object
# Esperado: 0 matches
```

**Pausa Segura:** ✅ Sim (mas manager.py ainda tem caminho hardcoded)

---

#### Fase 2.7: Ajustar `agents/database/manager.py` (caminho hardcoded)

**Claude Code (complexo):**
- [ ] Ajustar linha 48: `def __init__(self, db_path: str = "data/data.db")`
- [ ] Usar caminho absoluto baseado em `__file__` ou variável de ambiente
- [ ] Testar: Criar instância e verificar conexão

**Comando:**
```powershell
# Pedir ao Claude Code:
# "Ajuste o caminho hardcoded em agents/database/manager.py linha 48
#  para usar caminho absoluto baseado em __file__ ou raiz do projeto"
```

**Validação:**
```powershell
# Testar conexão com DB
python -c "from agents.database.manager import DatabaseManager; db = DatabaseManager(); print('OK')"
```

**Pausa Segura:** ✅ Sim

---

#### Fase 2.8: Mover `agents/checklist/` → `core/agents/checklist/`

**Cursor (rápido):**
- [ ] `git mv agents/checklist core/agents/checklist`
- [ ] Find/Replace: `from agents.checklist.` → `from core.agents.checklist.`
- [ ] Validar: 0 matches de `from agents.checklist\.`

**Comandos:**
```powershell
git mv agents/checklist core/agents/checklist

# Find/Replace no Cursor:
# Buscar: from agents.checklist.
# Substituir: from core.agents.checklist.
```

**Validação:**
```powershell
Get-ChildItem -Recurse -Include *.py | Select-String "from agents.checklist\." | Measure-Object
# Esperado: 0 matches
```

**Pausa Segura:** ✅ Sim

---

### Fase 3: Core - Memória

**Objetivo:** Mover módulos de memória e persistência.

#### Fase 3.1: Mover `agents/memory/` → `core/agents/memory/`

**Cursor (rápido):**
- [ ] `git mv agents/memory core/agents/memory`
- [ ] Find/Replace: `from agents.memory.` → `from core.agents.memory.`
- [ ] Validar: 0 matches de `from agents.memory\.`

**Comandos:**
```powershell
git mv agents/memory core/agents/memory

# Find/Replace no Cursor:
# Buscar: from agents.memory.
# Substituir: from core.agents.memory.
```

**Validação:**
```powershell
Get-ChildItem -Recurse -Include *.py | Select-String "from agents.memory\." | Measure-Object
# Esperado: 0 matches

# Testar config_loader (já ajustado na Fase 2.4)
python -c "from core.agents.memory.config_loader import load_agent_config; print('OK')"
```

**Pausa Segura:** ✅ Sim

---

#### Fase 3.2: Mover `agents/persistence/` → `core/agents/persistence/`

**Cursor (rápido):**
- [ ] `git mv agents/persistence core/agents/persistence`
- [ ] Find/Replace: `from agents.persistence.` → `from core.agents.persistence.`
- [ ] Validar: 0 matches de `from agents.persistence\.`

**Comandos:**
```powershell
git mv agents/persistence core/agents/persistence

# Find/Replace no Cursor:
# Buscar: from agents.persistence.
# Substituir: from core.agents.persistence.
```

**Validação:**
```powershell
Get-ChildItem -Recurse -Include *.py | Select-String "from agents.persistence\." | Measure-Object
# Esperado: 0 matches
```

**Pausa Segura:** ✅ Sim

---

### Fase 4: Core - Agentes

**Objetivo:** Mover agentes principais.

#### Fase 4.1: Mover `agents/orchestrator/` → `core/agents/orchestrator/`

**Cursor (rápido):**
- [ ] `git mv agents/orchestrator core/agents/orchestrator`
- [ ] Find/Replace: `from agents.orchestrator.` → `from core.agents.orchestrator.`
- [ ] Validar: 0 matches de `from agents.orchestrator\.`

**Comandos:**
```powershell
git mv agents/orchestrator core/agents/orchestrator

# Find/Replace no Cursor:
# Buscar: from agents.orchestrator.
# Substituir: from core.agents.orchestrator.
```

**Validação:**
```powershell
Get-ChildItem -Recurse -Include *.py | Select-String "from agents.orchestrator\." | Measure-Object
# Esperado: 0 matches
```

**Pausa Segura:** ✅ Sim

---

#### Fase 4.2: Mover `agents/structurer/` → `core/agents/structurer/`

**Cursor (rápido):**
- [ ] `git mv agents/structurer core/agents/structurer`
- [ ] Find/Replace: `from agents.structurer.` → `from core.agents.structurer.`
- [ ] Validar: 0 matches de `from agents.structurer\.`

**Comandos:**
```powershell
git mv agents/structurer core/agents/structurer

# Find/Replace no Cursor:
# Buscar: from agents.structurer.
# Substituir: from core.agents.structurer.
```

**Validação:**
```powershell
Get-ChildItem -Recurse -Include *.py | Select-String "from agents.structurer\." | Measure-Object
# Esperado: 0 matches
```

**Pausa Segura:** ✅ Sim

---

#### Fase 4.3: Mover `agents/methodologist/` → `core/agents/methodologist/`

**Cursor (rápido):**
- [ ] `git mv agents/methodologist core/agents/methodologist`
- [ ] Find/Replace: `from agents.methodologist.` → `from core.agents.methodologist.`
- [ ] Validar: 0 matches de `from agents.methodologist\.`

**Comandos:**
```powershell
git mv agents/methodologist core/agents/methodologist

# Find/Replace no Cursor:
# Buscar: from agents.methodologist.
# Substituir: from core.agents.methodologist.
```

**Validação:**
```powershell
Get-ChildItem -Recurse -Include *.py | Select-String "from agents.methodologist\." | Measure-Object
# Esperado: 0 matches
```

**Pausa Segura:** ✅ Sim

---

#### Fase 4.4: Mover `agents/observer/` → `core/agents/observer/`

**Cursor (rápido):**
- [ ] `git mv agents/observer core/agents/observer`
- [ ] Find/Replace: `from agents.observer.` → `from core.agents.observer.`
- [ ] Validar: 0 matches de `from agents.observer\.`

**Comandos:**
```powershell
git mv agents/observer core/agents/observer

# Find/Replace no Cursor:
# Buscar: from agents.observer.
# Substituir: from core.agents.observer.
```

**Validação:**
```powershell
Get-ChildItem -Recurse -Include *.py | Select-String "from agents.observer\." | Measure-Object
# Esperado: 0 matches
```

**Pausa Segura:** ✅ Sim (mas catalog.py ainda tem caminhos hardcoded)

---

#### Fase 4.5: Ajustar `agents/observer/catalog.py` (caminhos hardcoded)

**Claude Code (complexo):**
- [ ] Ajustar linhas 30-31: `DEFAULT_CHROMA_PATH = "./data/chroma"`, `DEFAULT_SQLITE_PATH = "./data/concepts.db"`
- [ ] Usar caminhos absolutos baseados em `__file__` ou raiz do projeto
- [ ] Testar: Criar instância e verificar acesso aos dados

**Comando:**
```powershell
# Pedir ao Claude Code:
# "Ajuste os caminhos hardcoded em agents/observer/catalog.py linhas 30-31
#  para usar caminhos absolutos baseados em __file__ ou raiz do projeto"
```

**Validação:**
```powershell
# Testar acesso ao ChromaDB
python -c "from core.agents.observer.catalog import ConceptCatalog; cat = ConceptCatalog(); print('ChromaDB OK')"

# Testar acesso aos dados
python -c "from core.agents.observer.catalog import ConceptCatalog; cat = ConceptCatalog(); print('OK')"
```

**Pausa Segura:** ✅ Sim

---

### Fase 5: Core - Integração

**Objetivo:** Mover arquivo de integração principal.

#### Fase 5.1: Mover `agents/multi_agent_graph.py` → `core/agents/`

**Cursor (rápido):**
- [ ] `git mv agents/multi_agent_graph.py core/agents/multi_agent_graph.py`
- [ ] Validar: Arquivo movido

**Comandos:**
```powershell
git mv agents/multi_agent_graph.py core/agents/multi_agent_graph.py
```

**Pausa Segura:** ❌ Não (imports ainda quebrados)

---

#### Fase 5.2: Ajustar TODOS os imports em `multi_agent_graph.py` (arquivo crítico)

**Claude Code (complexo):**
- [ ] Ajustar imports de `from agents.` → `from core.agents.`
- [ ] Ajustar imports de `from utils.` → `from core.utils.`
- [ ] **Ajustar linha 450:** `Path("data/checkpoints.db")` → usar caminho absoluto baseado em `__file__` ou raiz do projeto
- [ ] Exemplo: `Path(__file__).parent.parent.parent.parent / "data" / "checkpoints.db"`
- [ ] Revisar TODOS os 17 imports do arquivo
- [ ] Testar: `python -m core.agents.multi_agent_graph`

**Comando:**
```powershell
# Pedir ao Claude Code:
# "Ajuste TODOS os imports em core/agents/multi_agent_graph.py
#  para usar os novos caminhos core.agents e core.utils.
#  Também ajuste linha 450: Path('data/checkpoints.db') para usar
#  caminho absoluto baseado em __file__ ou raiz do projeto"
```

**Validação Completa (Claude Code):**
```powershell
# Rodar suite completa de testes do core
pytest tests/core/ -v

# Testar importação do módulo
python -c "from core.agents.multi_agent_graph import create_multi_agent_graph; print('OK')"
```

**Pausa Segura:** ✅ Sim (core completo e funcional)

---

### Fase 6: CLI

**Objetivo:** Mover CLI para ferramentas do core.

#### Fase 6.1: Mover `cli/` → `core/tools/cli/`

**Cursor (rápido):**
- [ ] `git mv cli core/tools/cli`
- [ ] Validar: Estrutura preservada

**Comandos:**
```powershell
git mv cli core/tools/cli
```

**Pausa Segura:** ❌ Não (imports ainda quebrados)

---

#### Fase 6.2: Ajustar imports em CLI

**Claude Code (complexo):**
- [ ] Ajustar imports de `from agents.` → `from core.agents.`
- [ ] Ajustar imports de `from utils.` → `from core.utils.`
- [ ] Testar: `python -m core.tools.cli.chat`

**Comando:**
```powershell
# Pedir ao Claude Code:
# "Ajuste todos os imports em core/tools/cli/ para usar core.agents e core.utils"
```

**Validação:**
```powershell
# Testar CLI
python -m core.tools.cli.chat --help

# Testar integração
pytest tests/integration/behavior/test_cli_integration.py -v
```

**Pausa Segura:** ✅ Sim (core completo, produto ainda na raiz)

---

### Fase 7: Produto Revelar

**Objetivo:** Mover app para `products/revelar/`.

#### Fase 7.1: Mover `app/` → `products/revelar/app/`

**Cursor (rápido):**
- [ ] `git mv app products/revelar/app`
- [ ] Validar: Estrutura preservada

**Comandos:**
```powershell
git mv app products/revelar/app
```

**Pausa Segura:** ❌ Não (imports ainda quebrados)

---

#### Fase 7.2: Ajustar imports em app/

**Claude Code (complexo):**
- [ ] Ajustar imports de `from agents.` → `from core.agents.`
- [ ] Ajustar imports de `from utils.` → `from core.utils.`
- [ ] Ajustar imports de `from app.` → `from products.revelar.app.` (em testes)
- [ ] **Ajustar caminhos de `checkpoints.db` em:**
  - `products/revelar/app/components/conversation_helpers.py` (linha 196)
  - `products/revelar/app/pages/_ideia_detalhes.py` (linha 171)
- [ ] Usar caminho absoluto baseado na raiz do projeto ou variável de ambiente
- [ ] Exemplo: `project_root / "data" / "checkpoints.db"`
- [ ] Testar: `streamlit run products/revelar/app/chat.py`

**Comando:**
```powershell
# Pedir ao Claude Code:
# "Ajuste todos os imports em products/revelar/app/ para usar core.agents e core.utils.
#  Também ajuste caminhos de checkpoints.db em:
#  - products/revelar/app/components/conversation_helpers.py (linha 196)
#  - products/revelar/app/pages/_ideia_detalhes.py (linha 171)
#  Use caminho absoluto baseado na raiz do projeto"
```

**Validação:**
```powershell
# Testar Streamlit
streamlit run products/revelar/app/chat.py

# Testar imports
python -c "from products.revelar.app.chat import main; print('OK')"

# Testar acesso a checkpoints.db
python -c "from pathlib import Path; from products.revelar.app.components.conversation_helpers import *; print('Checkpoints OK')"
```

**Pausa Segura:** ✅ Sim (core e produto separados, testes ainda na raiz)

---

### Fase 8: Testes

**Objetivo:** Reorganizar testes por core/produto.

#### Fase 8.1: Mover `tests/unit/` → `tests/core/unit/`

**Cursor (rápido):**
- [ ] `git mv tests/unit tests/core/unit`
- [ ] Validar: Estrutura preservada

**Comandos:**
```powershell
git mv tests/unit tests/core/unit
```

**Validação:**
- [ ] Verificar: Arquivos movidos corretamente

**Pausa Segura:** ✅ Sim (imports já ajustados nas fases anteriores)

---

#### Fase 8.2: Mover `tests/integration/smoke/` → `tests/core/integration/smoke/`

**Cursor (rápido):**
- [ ] `git mv tests/integration/smoke tests/core/integration/smoke`
- [ ] Validar: Estrutura preservada

**Comandos:**
```powershell
git mv tests/integration/smoke tests/core/integration/smoke
```

**Validação:**
- [ ] Verificar: 3 arquivos movidos (test_methodologist_smoke.py, test_multi_agent_smoke.py, test_structurer_smoke.py)

**Pausa Segura:** ✅ Sim

---

#### Fase 8.3: Mover `tests/integration/behavior/` → `tests/core/integration/behavior/` (maioria)

**Cursor (rápido):**
- [ ] `git mv tests/integration/behavior tests/core/integration/behavior`
- [ ] Validar: Estrutura preservada

**Comandos:**
```powershell
git mv tests/integration/behavior tests/core/integration/behavior
```

**Validação:**
- [ ] Verificar: ~20 arquivos movidos

**Pausa Segura:** ❌ Não (3 arquivos específicos precisam ser movidos depois)

---

#### Fase 8.4: Mover 3 arquivos específicos → `tests/products/revelar/integration/`

**Cursor (rápido):**
- [ ] `git mv tests/core/integration/behavior/test_cli_integration.py tests/products/revelar/integration/test_cli_integration.py`
- [ ] `git mv tests/core/integration/behavior/test_dashboard.py tests/products/revelar/integration/test_dashboard.py`
- [ ] `git mv tests/core/integration/behavior/test_conversation_switching_behavior.py tests/products/revelar/integration/test_conversation_switching_behavior.py`
- [ ] Validar: Arquivos movidos

**Comandos:**
```powershell
# Mover arquivos específicos do produto Revelar
# Nota: test_system_maturity.py permanece em core/ (é genérico, não específico do produto)
git mv tests/core/integration/behavior/test_cli_integration.py tests/products/revelar/integration/test_cli_integration.py
git mv tests/core/integration/behavior/test_dashboard.py tests/products/revelar/integration/test_dashboard.py
git mv tests/core/integration/behavior/test_conversation_switching_behavior.py tests/products/revelar/integration/test_conversation_switching_behavior.py
```

**Validação:**
- [ ] Verificar: 3 arquivos em `tests/products/revelar/integration/`
- [ ] Verificar: Imports de `app.` serão ajustados para `products.revelar.app.` nos arquivos movidos
- [ ] Verificar: `test_system_maturity.py` permanece em `tests/core/integration/behavior/` (é genérico)

**Pausa Segura:** ✅ Sim

---

#### Fase 8.5: Mover `tests/integration/e2e/` → `tests/core/integration/e2e/`

**Cursor (rápido):**
- [ ] `git mv tests/integration/e2e tests/core/integration/e2e`
- [ ] Validar: Estrutura preservada

**Comandos:**
```powershell
git mv tests/integration/e2e tests/core/integration/e2e
```

**Validação:**
- [ ] Verificar: 2 arquivos movidos (test_direction_change.py, test_multi_turn_flows.py)

**Pausa Segura:** ✅ Sim

---

#### Fase 8.6: Validar pytest.ini

**Claude Code (se necessário):**
- [ ] Verificar `pytest.ini` após reorganizar testes
- [ ] Ajustar `testpaths` se necessário
- [ ] Testar: `pytest tests/core/ -v`
- [ ] Testar: `pytest tests/products/revelar/ -v`

**Validação:**
```powershell
# Verificar que pytest encontra testes
pytest tests/core/ -v --collect-only
pytest tests/products/revelar/ -v --collect-only

# Rodar testes para validar
pytest tests/core/ -v
pytest tests/products/revelar/ -v
```

**Pausa Segura:** ✅ Sim

---

### Fase 9: Scripts

**Objetivo:** Categorizar e mover scripts por core/produto.

#### Fase 9.1: Categorizar scripts (core vs revelar)

**Análise necessária:**
- **Scripts genéricos (core):**
  - `health_checks/` → `scripts/core/health_checks/` (7 arquivos)
  - `debug/` → `scripts/core/debug/` (2 arquivos)
  - `testing/` → `scripts/core/testing/` (6 arquivos)
  - `spikes/` → `scripts/core/spikes/` (2 arquivos)
  - `state_introspection/` → `scripts/core/state_introspection/` (1 arquivo)
  - **Raiz:** `analyze_imports.py`, `analyze_migration_impact.py`, `common.py`, `inspect_database.py`, `validate_observer_integration.py`, `validate_clarification_questions.py`, `validate_direction_change.py` → `scripts/core/` (7 arquivos)
  
- **Scripts específicos (revelar):**
  - `interface/` → `scripts/revelar/interface/` (vazio - preparado para scripts de UI)
  - `flows/` → `scripts/revelar/flows/` (vazio - preparado para fluxos específicos)

**Decisão:**
- [ ] Todos os scripts da raiz vão para `scripts/core/` (são genéricos)
- [ ] `state_introspection/` vai para `scripts/core/` (genérico)
- [ ] `interface/` e `flows/` vão para `scripts/revelar/` (específicos da interface)
- [ ] Documentar decisões

**Pausa Segura:** ✅ Sim (análise apenas)

---

#### Fase 9.2: Mover `scripts/health_checks/` → `scripts/core/`

**Cursor (rápido):**
- [ ] `git mv scripts/health_checks scripts/core/health_checks`
- [ ] Validar: Estrutura preservada

**Comandos:**
```powershell
git mv scripts/health_checks scripts/core/health_checks
```

**Validação:**
- [ ] Verificar: ~8 arquivos movidos

**Pausa Segura:** ✅ Sim

---

#### Fase 9.3: Mover `scripts/debug/` → `scripts/core/`

**Cursor (rápido):**
- [ ] `git mv scripts/debug scripts/core/debug`
- [ ] Validar: Estrutura preservada

**Comandos:**
```powershell
git mv scripts/debug scripts/core/debug
```

**Validação:**
- [ ] Verificar: Arquivos movidos

**Pausa Segura:** ✅ Sim

---

#### Fase 9.4: Mover `scripts/testing/` → `scripts/core/`

**Cursor (rápido):**
- [ ] `git mv scripts/testing scripts/core/testing`
- [ ] Validar: Estrutura preservada

**Comandos:**
```powershell
git mv scripts/testing scripts/core/testing
```

**Validação:**
- [ ] Verificar: ~7 arquivos movidos

**Pausa Segura:** ✅ Sim

---

#### Fase 9.5: Mover `scripts/spikes/` → `scripts/core/`

**Cursor (rápido):**
- [ ] `git mv scripts/spikes scripts/core/spikes`
- [ ] Validar: Estrutura preservada

**Comandos:**
```powershell
git mv scripts/spikes scripts/core/spikes
```

**Validação:**
- [ ] Verificar: Arquivos movidos

**Pausa Segura:** ✅ Sim

---

#### Fase 9.6: Mover `scripts/flows/` → `scripts/revelar/`

**Cursor (rápido):**
- [ ] `git mv scripts/flows scripts/revelar/flows`
- [ ] Validar: Estrutura preservada

**Comandos:**
```powershell
git mv scripts/flows scripts/revelar/flows
```

**Validação:**
- [ ] Verificar: Arquivos movidos

**Pausa Segura:** ✅ Sim

---

#### Fase 9.7: Mover `scripts/state_introspection/` → `scripts/core/`

**Cursor (rápido):**
- [ ] `git mv scripts/state_introspection scripts/core/state_introspection`
- [ ] Validar: Estrutura preservada

**Comandos:**
```powershell
git mv scripts/state_introspection scripts/core/state_introspection
```

**Validação:**
- [ ] Verificar: Arquivos movidos

**Pausa Segura:** ✅ Sim

---

#### Fase 9.8: Mover scripts da raiz → `scripts/core/`

**Cursor (rápido):**
- [ ] `git mv scripts/analyze_imports.py scripts/core/analyze_imports.py`
- [ ] `git mv scripts/analyze_migration_impact.py scripts/core/analyze_migration_impact.py`
- [ ] `git mv scripts/common.py scripts/core/common.py`
- [ ] `git mv scripts/inspect_database.py scripts/core/inspect_database.py`
- [ ] `git mv scripts/validate_observer_integration.py scripts/core/validate_observer_integration.py`
- [ ] `git mv scripts/validate_clarification_questions.py scripts/core/validate_clarification_questions.py`
- [ ] `git mv scripts/validate_direction_change.py scripts/core/validate_direction_change.py`
- [ ] Validar: Estrutura preservada

**Comandos:**
```powershell
# Mover scripts da raiz para scripts/core/
git mv scripts/analyze_imports.py scripts/core/analyze_imports.py
git mv scripts/analyze_migration_impact.py scripts/core/analyze_migration_impact.py
git mv scripts/common.py scripts/core/common.py
git mv scripts/inspect_database.py scripts/core/inspect_database.py
git mv scripts/validate_observer_integration.py scripts/core/validate_observer_integration.py
git mv scripts/validate_clarification_questions.py scripts/core/validate_clarification_questions.py
git mv scripts/validate_direction_change.py scripts/core/validate_direction_change.py
```

**Validação:**
- [ ] Verificar: 7 arquivos movidos

**Pausa Segura:** ✅ Sim

---

#### Fase 9.9: Ajustar imports e `Path(__file__).parent` em scripts

**Claude Code (complexo):**
- [ ] Revisar todos os 41 arquivos com `Path(__file__).parent`
- [ ] Ajustar imports de `from agents.` → `from core.agents.`
- [ ] Ajustar imports de `from utils.` → `from core.utils.`
- [ ] Ajustar caminhos relativos que podem quebrar
- [ ] Testar: Executar scripts principais manualmente

**Comando:**
```powershell
# Pedir ao Claude Code:
# "Revisar e ajustar todos os scripts em scripts/core/ e scripts/revelar/
#  para usar imports corretos (core.agents, core.utils) e ajustar
#  caminhos Path(__file__).parent que podem quebrar"
```

**Validação:**
```powershell
# Testar scripts principais
python scripts/core/health_checks/validate_api.py
python scripts/core/debug/debug_multi_agent.py
```

**Pausa Segura:** ✅ Sim

---

### Fase 10: Documentação

**Objetivo:** Reorganizar docs por core/produto.

#### Fase 10.1: Mover `docs/architecture/` → `docs/core/architecture/`

**Cursor (rápido):**
- [ ] `git mv docs/architecture docs/core/architecture`
- [ ] Validar: Estrutura preservada

**Comandos:**
```powershell
git mv docs/architecture docs/core/architecture
```

**Validação:**
- [ ] Verificar: ~9 arquivos movidos

**Pausa Segura:** ✅ Sim (mas referências ainda quebradas)

---

#### Fase 10.2: Mover `docs/agents/` → `docs/core/agents/`

**Cursor (rápido):**
- [ ] `git mv docs/agents docs/core/agents`
- [ ] Validar: Estrutura preservada

**Comandos:**
```powershell
git mv docs/agents docs/core/agents
```

**Validação:**
- [ ] Verificar: ~7 arquivos movidos

**Pausa Segura:** ✅ Sim (mas referências ainda quebradas)

---

#### Fase 10.3: Mover `docs/testing/` → `docs/core/testing/`

**Cursor (rápido):**
- [ ] `git mv docs/testing docs/core/testing`
- [ ] Validar: Estrutura preservada

**Comandos:**
```powershell
git mv docs/testing docs/core/testing
```

**Validação:**
- [ ] Verificar: ~57 arquivos movidos

**Pausa Segura:** ✅ Sim (mas referências ainda quebradas)

---

#### Fase 10.4: Mover `docs/orchestration/` → `docs/core/orchestration/`

**Cursor (rápido):**
- [ ] `git mv docs/orchestration docs/core/orchestration`
- [ ] Validar: Estrutura preservada

**Comandos:**
```powershell
git mv docs/orchestration docs/core/orchestration
```

**Validação:**
- [ ] Verificar: ~23 arquivos movidos

**Pausa Segura:** ✅ Sim (mas referências ainda quebradas)

---

#### Fase 10.5: Mover `docs/interface/` → `docs/products/revelar/interface/`

**Cursor (rápido):**
- [ ] `git mv docs/interface docs/products/revelar/interface`
- [ ] Validar: Estrutura preservada

**Comandos:**
```powershell
git mv docs/interface docs/products/revelar/interface
```

**Validação:**
- [ ] Verificar: ~6 arquivos movidos

**Pausa Segura:** ✅ Sim (mas referências ainda quebradas)

---

#### Fase 10.6: Mover outros (process/, vision/, analysis/)

**Cursor (rápido):**
- [ ] Decidir: `docs/process/` → `docs/core/process/` ✅ (core - processos de desenvolvimento)
- [ ] Decidir: `docs/vision/` → `docs/core/vision/` ✅ (core - visão do sistema)
- [ ] Decidir: `docs/analysis/` → `docs/core/analysis/` ✅ (análises técnicas são core)
- [ ] Mover conforme decisão acima
- [ ] Validar: Estrutura preservada

**Comandos:**
```powershell
# Decisão: process/, vision/ e analysis/ são core (análises técnicas)
git mv docs/process docs/core/process
git mv docs/vision docs/core/vision
git mv docs/analysis docs/core/analysis
```

**Validação:**
- [ ] Verificar: Arquivos movidos

**Pausa Segura:** ✅ Sim (mas referências ainda quebradas)

---

#### Fase 10.7: Atualizar ~2000 referências internas

**Claude Code (complexo):**
- [ ] Buscar todas as referências a caminhos antigos em `.md`
- [ ] Atualizar referências:
  - `agents/` → `core/agents/`
  - `utils/` → `core/utils/`
  - `app/` → `products/revelar/app/`
  - `docs/architecture/` → `docs/core/architecture/`
  - `docs/agents/` → `docs/core/agents/`
  - `docs/interface/` → `docs/products/revelar/interface/`
- [ ] Validar: Links não quebrados

**Comando:**
```powershell
# Pedir ao Claude Code:
# "Atualizar todas as referências internas em arquivos .md
#  para usar os novos caminhos (core/, products/revelar/, etc)"
```

**Validação:**
```powershell
# Buscar referências antigas
Get-ChildItem -Recurse -Include *.md | Select-String "agents/" | Select-Object -First 10
Get-ChildItem -Recurse -Include *.md | Select-String "app/" | Select-Object -First 10
```

**Pausa Segura:** ✅ Sim

---

### Fase 11: ROADMAPs

**Objetivo:** Criar ROADMAPs separados.

#### Fase 11.1: Criar `core/ROADMAP.md`

**Claude Code (complexo):**
- [ ] Extrair épicos relacionados ao core do `ROADMAP.md` raiz
- [ ] Criar `core/ROADMAP.md` com épicos do core
- [ ] Validar: Conteúdo relevante

**Comando:**
```powershell
# Pedir ao Claude Code:
# "Criar core/ROADMAP.md extraindo épicos relacionados ao core
#  do ROADMAP.md raiz"
```

**Pausa Segura:** ✅ Sim

---

#### Fase 11.2: Criar `products/revelar/ROADMAP.md`

**Claude Code (complexo):**
- [ ] Extrair épicos relacionados ao produto Revelar do `ROADMAP.md` raiz
- [ ] Criar `products/revelar/ROADMAP.md` com épicos do produto
- [ ] Validar: Conteúdo relevante

**Comando:**
```powershell
# Pedir ao Claude Code:
# "Criar products/revelar/ROADMAP.md extraindo épicos relacionados
#  ao produto Revelar do ROADMAP.md raiz"
```

**Pausa Segura:** ✅ Sim

---

#### Fase 11.3: Atualizar root `ROADMAP.md` como índice

**Claude Code (complexo):**
- [ ] Transformar `ROADMAP.md` raiz em índice
- [ ] Referenciar `core/ROADMAP.md` e `products/revelar/ROADMAP.md`
- [ ] Manter apenas épicos gerais/super-sistema
- [ ] Validar: Links funcionam

**Comando:**
```powershell
# Pedir ao Claude Code:
# "Transformar ROADMAP.md raiz em índice que referencia
#  core/ROADMAP.md e products/revelar/ROADMAP.md"
```

**Pausa Segura:** ✅ Sim

---

### Fase 12: Limpeza Final

**Objetivo:** Remover diretórios vazios, ajustar configs finais.

#### Fase 12.1: Remover diretórios vazios da raiz

**Cursor (rápido):**
- [ ] Verificar: `agents/` vazio (remover)
- [ ] Verificar: `app/` vazio (remover)
- [ ] Verificar: `cli/` vazio (remover)
- [ ] Verificar: `utils/` vazio (remover)
- [ ] Verificar: `config/` vazio (remover)
- [ ] Verificar: `tests/integration/` vazio (remover)
- [ ] Validar: Apenas diretórios vazios removidos

**Comandos:**
```powershell
# Verificar e remover diretórios vazios
if ((Get-ChildItem agents -ErrorAction SilentlyContinue | Measure-Object).Count -eq 0) { Remove-Item agents }
if ((Get-ChildItem app -ErrorAction SilentlyContinue | Measure-Object).Count -eq 0) { Remove-Item app }
if ((Get-ChildItem cli -ErrorAction SilentlyContinue | Measure-Object).Count -eq 0) { Remove-Item cli }
if ((Get-ChildItem utils -ErrorAction SilentlyContinue | Measure-Object).Count -eq 0) { Remove-Item utils }
if ((Get-ChildItem config -ErrorAction SilentlyContinue | Measure-Object).Count -eq 0) { Remove-Item config }
if ((Get-ChildItem tests/integration -ErrorAction SilentlyContinue | Measure-Object).Count -eq 0) { Remove-Item tests/integration }
```

**Pausa Segura:** ✅ Sim

---

#### Fase 12.2: Atualizar README.md

**Claude Code (complexo):**
- [ ] Atualizar estrutura de diretórios no README.md
- [ ] Atualizar instruções de instalação/uso
- [ ] Atualizar caminhos de exemplos
- [ ] Validar: README reflete nova estrutura

**Comando:**
```powershell
# Pedir ao Claude Code:
# "Atualizar README.md para refletir a nova estrutura monorepo
#  com core/ e products/revelar/"
```

**Pausa Segura:** ✅ Sim

---

#### Fase 12.3: Atualizar ARCHITECTURE.md

**Claude Code (complexo):**
- [ ] Atualizar diagramas de estrutura
- [ ] Atualizar referências a caminhos
- [ ] Atualizar descrições de componentes
- [ ] Validar: ARCHITECTURE.md reflete nova estrutura

**Comando:**
```powershell
# Pedir ao Claude Code:
# "Atualizar ARCHITECTURE.md para refletir a nova estrutura monorepo"
```

**Pausa Segura:** ✅ Sim

---

#### Fase 12.4: Validação Final Completa

**Claude Code (complexo):**
- [ ] Rodar suite completa de testes: `pytest tests/ -v`
- [ ] Testar CLI: `python -m core.tools.cli.chat --help`
- [ ] Testar Streamlit: `streamlit run products/revelar/app/chat.py`
- [ ] Verificar imports: `python -c "from core.agents.multi_agent_graph import create_multi_agent_graph; print('OK')"`
- [ ] Verificar configs: `python -c "from core.agents.memory.config_loader import load_agent_config; print(load_agent_config('orchestrator')['model'])"`
- [ ] Validar: Tudo funcionando

**Comandos:**
```powershell
# Suite completa
pytest tests/ -v

# Testes específicos
pytest tests/core/ -v
pytest tests/products/revelar/ -v

# Testar CLI
python -m core.tools.cli.chat --help

# Testar Streamlit
streamlit run products/revelar/app/chat.py

# Testar imports críticos
python -c "from core.agents.multi_agent_graph import create_multi_agent_graph; print('OK')"
python -c "from core.agents.memory.config_loader import load_agent_config; print(load_agent_config('orchestrator')['model'])"
```

**Commit:** `refactor(migration): finalize monorepo structure`

**Pausa Segura:** ✅ Sim (Migração completa! 🎉)

---

## 6. Checklist de Progresso

### Fase 0: Preparação
- [x] Branch criada
- [x] Estrutura analisada
- [x] Análises de impacto criadas
- [x] MIGRATION.md criado

### Fase 1: Estrutura Base ✅
- [x] Diretórios vazios criados
- [x] `__init__.py` criados
- [x] Testes continuam passando
- [x] Commit realizado

### Fase 2: Core - Folhas ✅
- [x] utils/ movido (exceto prompts/)
- [x] prompts/ movido
- [x] config/ movido
- [x] config_loader.py ajustado (caminho dinâmico + cache)
- [x] models/ movido
- [x] database/ movido
- [x] database/manager.py ajustado (caminho dinâmico)
- [x] checklist/ movido
- [x] Imports ajustados
- [x] Testes passando

### Fase 3: Core - Memória ✅
- [x] memory/ movido
- [x] persistence/ movido
- [x] Imports ajustados
- [x] Testes passando

### Fase 4: Core - Agentes ✅
- [x] orchestrator/ movido
- [x] structurer/ movido
- [x] methodologist/ movido
- [x] observer/ movido
- [x] observer/catalog.py ajustado (caminho dinâmico)
- [x] Imports ajustados
- [x] Testes passando

### Fase 5: Core - Integração ✅
- [x] multi_agent_graph.py movido
- [x] Imports ajustados
- [x] checkpoints.db caminho dinâmico
- [x] Suite completa passando (1 teste pré-existente falhando - não relacionado à migração)
- [x] Commit realizado

### Fase 6: CLI
- [ ] cli/ movido
- [ ] Imports ajustados
- [ ] Testes passando
- [ ] Commit realizado

### Fase 7: Produto Revelar
- [ ] app/ movido
- [ ] Imports ajustados
- [ ] Streamlit funcionando
- [ ] Commits realizados

### Fase 8: Testes
- [ ] unit/ movido
- [ ] integration/smoke/ movido
- [ ] integration/behavior/ movido (maioria)
- [ ] 3 arquivos específicos movidos para products/revelar/
- [ ] integration/e2e/ movido
- [ ] Todos passando
- [ ] Commit realizado

### Fase 9: Scripts
- [ ] Scripts categorizados
- [ ] Scripts movidos
- [ ] Imports e caminhos ajustados
- [ ] Scripts testados
- [ ] Commit realizado

### Fase 10: Documentação
- [ ] Docs reorganizados
- [ ] Referências atualizadas (~2000)
- [ ] Links validados
- [ ] Commit realizado

### Fase 11: ROADMAPs
- [ ] core/ROADMAP.md criado
- [ ] products/revelar/ROADMAP.md criado
- [ ] ROADMAP.md raiz atualizado
- [ ] Commit realizado

### Fase 12: Limpeza Final
- [ ] Diretórios vazios removidos
- [ ] README.md atualizado
- [ ] ARCHITECTURE.md atualizado
- [ ] Validação final completa
- [ ] Commit final

---

## 7. Troubleshooting

### "Testes quebraram após mover agents/"
- Verifique imports: `from agents.` → `from core.agents.`
- Busque padrão: `Get-ChildItem -Recurse -Include *.py | Select-String "from agents\."`

### "Streamlit não encontra módulos"
- Verifique PYTHONPATH
- Rode da raiz: `streamlit run products/revelar/app/chat.py`

### "Config YAML não encontrado"
- Ajuste caminho em `core/agents/memory/config_loader.py`
- Caminho correto: `core/config/agents/*.yaml`

### "Git não preservou histórico"
- Use `git mv` ao invés de `mv`
- Verifique: `git log --follow <arquivo>`

### "Caminhos hardcoded quebrados"
- Busque: `Get-ChildItem -Recurse -Include *.py | Select-String "Path\(__file__\)\.parent"`
- Revise cada arquivo e ajuste conforme nova estrutura

---

## 8. Próximos Passos

Após migração completa:
1. Criar produto **Fichamento** em `products/fichamento/`
2. Evoluir core com novos agentes
3. Criar APIs REST para produtos consumirem core

---

**Versão:** 2.0
**Data:** 2025-01-XX
**Status:** Documento mestre - atualizar conforme progresso
**Baseado em:** Análises reais de imports, dependências e estrutura
