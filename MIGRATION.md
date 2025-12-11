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

## 2. Resumo do Progresso

### 📈 Progresso Recente (Última Atualização)

**Imports Atualizados:**
- ✅ **Testes:** 100% dos imports atualizados para `from core.` / `from products.revelar.`
- ✅ **Scripts:** 100% dos imports atualizados para `from core.` / `from products.revelar.`
- ✅ **Caminhos hardcoded:** Todos ajustados (config_loader, catalog, database/manager)

**Migração Física:**
- ✅ **tests/:** 100% migrado para `tests/core/` (unit/, integration/smoke/, behavior/, e2e/)
- ✅ **scripts/:** 100% migrado para `scripts/core/` e `scripts/revelar/`
- ✅ **agents/:** Diretório vazio removido (código em core/agents/)

**Documentação:**
- ✅ **core/docs/:** Conteúdo significativo migrado (agents/, architecture/, vision/, tools/)
- ⏳ **docs/ raiz:** Reorganização física pendente

**Próximos Passos:**
1. ✅ ~~Completar ajuste de imports restantes~~ (CONCLUÍDO - Quick win #1)
2. ✅ ~~Mover arquivos fisicamente para nova estrutura~~ (testes, scripts - CONCLUÍDO)
3. Mover 3 arquivos de teste específicos para `tests/products/revelar/` (ajuste de imports)
4. Reorganizar documentação da raiz

### ✅ Fases Concluídas (0-9, 11)

- **Fase 0:** Preparação ✅
- **Fase 1:** Estrutura Base ✅
- **Fase 2:** Core - Folhas ✅
- **Fase 3:** Core - Memória ✅
- **Fase 4:** Core - Agentes ✅
- **Fase 5:** Core - Integração ✅
- **Fase 6:** CLI ✅
- **Fase 7:** Produto Revelar ✅
- **Fase 8:** Testes ✅ (migração física completa para tests/core/)
- **Fase 9:** Scripts ✅ (migração física completa para scripts/core/ e scripts/revelar/)
- **Fase 11:** ROADMAPs ✅

### ⏳ Fases em Progresso

- **Fase 8.4:** Mover 3 arquivos específicos para tests/products/revelar/ (pendente - requer ajuste de imports)
- **Fase 10:** Documentação ⏳ (core/docs/ com conteúdo significativo, reorganização pendente)
- **Fase 12:** Limpeza Final ⏳ (parcial - agents/ removido)

### 📊 Estatísticas

- **Core:** 100% migrado ✅
- **Produto Revelar:** 100% migrado ✅
- **Testes:** 100% migrado fisicamente para tests/core/ ✅ (3 arquivos pendentes para products/revelar/)
- **Scripts:** 100% migrado fisicamente para scripts/core/ e scripts/revelar/ ✅
- **Documentação:** ~60% migrado (core/docs/ com agents/, architecture/, vision/, tools/) ⏳

---

## 3. Estado Atual da Migração

### ✅ Estrutura Já Migrada

```
paper-agent/
├── core/                    # ✅ COMPLETO
│   ├── agents/              # ✅ Todos os agentes migrados
│   ├── prompts/             # ✅ Migrado
│   ├── utils/               # ✅ Migrado
│   ├── config/              # ✅ Migrado
│   ├── tools/cli/           # ✅ CLI migrado
│   ├── docs/               # ✅ Parcial (agents/, architecture/, vision/, tools/)
│   ├── README.md           # ✅ Existe
│   └── ROADMAP.md          # ✅ Existe
│
├── products/
│   └── revelar/            # ✅ PRODUTO MIGRADO
│       ├── app/            # ✅ App migrado
│       ├── docs/          # ✅ Existe
│       ├── README.md      # ✅ Existe
│       └── ROADMAP.md     # ✅ Existe
│
├── tests/
│   ├── core/              # ✅ COMPLETO
│   │   ├── unit/          # ✅ Migrado (43 arquivos)
│   │   └── integration/   # ✅ Migrado
│   │       ├── smoke/     # ✅ Migrado (3 arquivos)
│   │       ├── behavior/  # ✅ Migrado (21 arquivos)
│   │       └── e2e/       # ✅ Migrado (3 arquivos)
│   └── products/revelar/  # ⏳ Estrutura criada (3 arquivos pendentes)
│
└── scripts/
    ├── core/              # ✅ COMPLETO
    │   ├── debug/         # ✅ Migrado
    │   ├── health_checks/ # ✅ Migrado
    │   ├── testing/       # ✅ Migrado
    │   ├── spikes/        # ✅ Migrado
    │   └── state_introspection/ # ✅ Migrado
    └── revelar/           # ✅ Estrutura criada
        └── flows/         # ✅ Migrado
```

### ⚠️ Ainda na Raiz (Pendente)

```
paper-agent/
├── tests/products/revelar/  # ⏳ 3 arquivos pendentes de tests/core/integration/behavior/
│   └── integration/         # test_cli_integration.py, test_dashboard.py, test_conversation_switching_behavior.py
│
└── docs/                    # ⚠️ Não organizado - Fase 10 pendente
    ├── analysis/            # ⚠️ → docs/core/analysis/
    ├── epics/               # ⚠️ → docs/core/epics/
    ├── process/             # ⚠️ → docs/core/process/
    └── testing/             # ⚠️ → docs/core/testing/
```

**Removidos:**
- ✅ `agents/` - removido (código migrado para core/agents/)
- ✅ `app/` - não existia mais
- ✅ `tests/unit/` - migrado para tests/core/unit/
- ✅ `tests/integration/` - migrado para tests/core/integration/
- ✅ `scripts/` subdiretórios - migrados para scripts/core/ e scripts/revelar/

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
- ✅ `core/agents/memory/config_loader.py`: Ajustado (caminho dinâmico + cache)
- ✅ `core/agents/observer/catalog.py`: Ajustado (caminhos dinâmicos)
- ✅ `core/agents/database/manager.py`: Ajustado (caminho dinâmico)
- ⚠️ **Scripts:** Ainda usam `Path(__file__).parent` (revisar após Fase 9)

---

## 4. Estado Final Desejado (Meta da Migração)

```
paper-agent/
├── core/                    # ✅ COMPLETO
│   ├── agents/              # ✅
│   ├── prompts/             # ✅
│   ├── utils/               # ✅
│   ├── config/              # ✅
│   ├── tools/cli/           # ✅
│   ├── docs/                # ⏳ Parcial (agents/, architecture/, vision/, tools/ já existem)
│   ├── README.md            # ✅
│   └── ROADMAP.md           # ✅
│
├── products/
│   └── revelar/             # ✅ COMPLETO
│       ├── app/             # ✅
│       ├── docs/            # ✅
│       ├── README.md        # ✅
│       └── ROADMAP.md       # ✅
│
├── tests/
│   ├── core/                # ⏳ Estrutura criada, aguardando migração
│   │   ├── unit/            # ⏳ Mover tests/unit/ → tests/core/unit/
│   │   └── integration/     # ⏳ Mover tests/integration/ → tests/core/integration/
│   │       ├── smoke/       # ⏳
│   │       ├── behavior/    # ⏳
│   │       └── e2e/         # ⏳
│   └── products/
│       └── revelar/
│           └── integration/ # ⏳ Mover 3 arquivos específicos
│
├── scripts/
│   ├── core/                # ⏳ Mover scripts genéricos
│   │   ├── health_checks/   # ⏳
│   │   ├── debug/           # ⏳
│   │   ├── testing/         # ⏳
│   │   ├── spikes/          # ⏳
│   │   └── state_introspection/ # ⏳
│   └── revelar/             # ⏳ Mover scripts específicos
│       └── flows/           # ⏳
│
├── docs/
│   ├── core/                # ⏳ Mover docs genéricos
│   │   ├── architecture/   # ⏳
│   │   ├── agents/          # ⏳
│   │   ├── testing/         # ⏳
│   │   ├── orchestration/   # ⏳
│   │   ├── process/         # ⏳
│   │   ├── vision/          # ⏳ (parcial já em core/docs/vision/)
│   │   └── analysis/        # ⏳
│   └── products/
│       └── revelar/
│           └── interface/    # ⏳
│
├── ROADMAP.md               # ⏳ Atualizar como índice
└── MIGRATION.md             # Este arquivo
```

---

## 5. Riscos Críticos

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

## 6. Fases da Migração

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
- [x] `git mv agents/memory core/agents/memory`
- [x] Find/Replace: `from agents.memory.` → `from core.agents.memory.`
- [x] Validar: 0 matches de `from agents.memory\.`

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
- [x] `git mv agents/persistence core/agents/persistence`
- [x] Find/Replace: `from agents.persistence.` → `from core.agents.persistence.`
- [x] Validar: 0 matches de `from agents.persistence\.`

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

### Fase 4: Core - Agentes ✅

**Status:** Concluída

**Objetivo:** Mover agentes principais.

#### Fase 4.1: Mover `agents/orchestrator/` → `core/agents/orchestrator/`

**Cursor (rápido):**
- [x] `git mv agents/orchestrator core/agents/orchestrator`
- [x] Find/Replace: `from agents.orchestrator.` → `from core.agents.orchestrator.`
- [x] Validar: 0 matches de `from agents.orchestrator\.`

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
- [x] `git mv agents/structurer core/agents/structurer`
- [x] Find/Replace: `from agents.structurer.` → `from core.agents.structurer.`
- [x] Validar: 0 matches de `from agents.structurer\.`

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
- [x] `git mv agents/methodologist core/agents/methodologist`
- [x] Find/Replace: `from agents.methodologist.` → `from core.agents.methodologist.`
- [x] Validar: 0 matches de `from agents.methodologist\.`

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
- [x] `git mv agents/observer core/agents/observer`
- [x] Find/Replace: `from agents.observer.` → `from core.agents.observer.`
- [x] Validar: 0 matches de `from agents.observer\.`

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

**Pausa Segura:** ✅ Sim

---

#### Fase 4.5: Ajustar `core/agents/observer/catalog.py` (caminhos hardcoded)

**Claude Code (complexo):**
- [x] Ajustar linhas 30-31: `DEFAULT_CHROMA_PATH = "./data/chroma"`, `DEFAULT_SQLITE_PATH = "./data/concepts.db"`
- [x] Usar caminhos absolutos baseados em `__file__` ou raiz do projeto
- [x] Testar: Criar instância e verificar acesso aos dados

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

### Fase 6: CLI ✅

**Status:** Concluida

**Objetivo:** Mover CLI para ferramentas do core.

#### Fase 6.1: Mover `cli/` → `core/tools/cli/`

**Cursor (rapido):**
- [x] `git mv cli/chat.py core/tools/cli/chat.py`
- [x] Atualizar `__init__.py`
- [x] Remover diretorio `cli/` antigo
- [x] Validar: Estrutura preservada

#### Fase 6.2: Ajustar PYTHONPATH e referencias

**Claude Code (complexo):**
- [x] Ajustar PYTHONPATH em chat.py (linha 24): `parent.parent` -> `parent.parent.parent.parent`
- [x] Imports ja estavam corretos (core.agents, core.utils) - Fase 5 ja ajustou
- [x] Atualizar exemplos de uso no argparse
- [x] Atualizar referencias em README.md, ARCHITECTURE.md, .claudecode.md
- [x] Atualizar referencias em testes e docs

**Validacao:**
```powershell
# Testar CLI (PowerShell Windows)
python -m core.tools.cli.chat --help

# Testar integracao
pytest tests/integration/behavior/test_cli_integration.py -v
```

**Pausa Segura:** ✅ Sim (core completo, produto ainda na raiz)

---

### Fase 7: Produto Revelar ✅

**Status:** Concluída

**Objetivo:** Mover app para `products/revelar/`.

#### Fase 7.1: Mover `app/` → `products/revelar/app/` ✅

**Status:** Concluída
- [x] `git mv app products/revelar/app`
- [x] Estrutura preservada

#### Fase 7.2: Ajustar imports em app/ ✅

**Status:** Concluída
- [x] Imports ajustados: `from agents.` → `from core.agents.`
- [x] Imports ajustados: `from utils.` → `from core.utils.`
- [x] Imports ajustados: `from app.` → `from products.revelar.app.`
- [x] Caminhos de `checkpoints.db` ajustados (project_root dinâmico)
- [x] Testes de imports validados
- [x] Commits realizados

**Pausa Segura:** ✅ Sim (core e produto separados, testes ainda na raiz)

---

### Fase 8: Testes ⏳

**Status:** Em Progresso - Imports atualizados, estrutura física pendente

**Objetivo:** Reorganizar testes por core/produto.

**Nota:** 
- A estrutura de diretórios já foi criada na Fase 1
- **164 arquivos** já usam imports `from core.` (95% dos testes)
- Apenas **1 arquivo** ainda usa import antigo (`test_observer_integration.py`)
- Arquivos ainda estão fisicamente na raiz (`tests/unit/`, `tests/integration/`)

#### Fase 8.1: Mover `tests/unit/` → `tests/core/unit/`

**Cursor (rápido):**
- [ ] `git mv tests/unit tests/core/unit`
- [ ] Validar: 43 arquivos movidos corretamente

**Comandos:**
```powershell
git mv tests/unit tests/core/unit
```

**Validação:**
- [ ] Verificar: 43 arquivos movidos (42 *.py + 1 *.md)
- [ ] Verificar: Estrutura preservada (agents/, database/, memory/, models/, utils/)

**Pausa Segura:** ✅ Sim (imports já ajustados nas fases anteriores)

---

#### Fase 8.2: Mover `tests/integration/smoke/` → `tests/core/integration/smoke/` ✅

**Status:** Concluída (Quick win #2)

**Cursor (rápido):**
- [x] `git mv tests/integration/smoke tests/core/integration/smoke`
- [x] Validar: Estrutura preservada

**Comandos:**
```powershell
git mv tests/integration/smoke tests/core/integration/smoke
```

**Validação:**
- [x] Verificar: 3 arquivos movidos (test_methodologist_smoke.py, test_multi_agent_smoke.py, test_structurer_smoke.py)
- [x] Verificar: README.md movido também
- [x] Pytest encontra 11 testes corretamente

**Commit:** `ffed7f4` - Quick win #2

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
- [ ] Verificar: ~20 arquivos movidos (29 *.py + 1 *.md)
- [ ] Verificar: README.md movido também

**Pausa Segura:** ❌ Não (3 arquivos específicos precisam ser movidos depois)

---

#### Fase 8.4: Mover 3 arquivos específicos → `tests/products/revelar/integration/`

**Claude Code (complexo):**
- [ ] `git mv tests/core/integration/behavior/test_cli_integration.py tests/products/revelar/integration/test_cli_integration.py`
- [ ] `git mv tests/core/integration/behavior/test_dashboard.py tests/products/revelar/integration/test_dashboard.py`
- [ ] `git mv tests/core/integration/behavior/test_conversation_switching_behavior.py tests/products/revelar/integration/test_conversation_switching_behavior.py`
- [ ] Ajustar imports: `from app.` → `from products.revelar.app.` nos 3 arquivos movidos
- [ ] Validar: Arquivos movidos e imports ajustados

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
- [ ] Verificar: Imports de `app.` ajustados para `products.revelar.app.` nos arquivos movidos
- [ ] Verificar: `test_system_maturity.py` permanece em `tests/core/integration/behavior/` (é genérico)
- [ ] Testar: `pytest tests/products/revelar/integration/ -v`

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
- [ ] Verificar: README.md movido também

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

### Fase 9: Scripts ⏳

**Status:** Em Progresso - Imports atualizados, estrutura física pendente

**Objetivo:** Categorizar e mover scripts por core/produto.

**Nota:** 
- Estrutura `scripts/core/` e `scripts/revelar/` já foi criada na Fase 1 (parcial)
- **64 arquivos** já usam imports `from core.` (90% dos scripts)
- Apenas **2 arquivos** ainda usam imports antigos (`validate_observer_integration.py`, `analyze_imports.py`)
- Arquivos ainda estão fisicamente na raiz

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

### Fase 10: Documentação ⏳

**Status:** Em Progresso - Conteúdo significativo em core/docs/, reorganização pendente

**Objetivo:** Reorganizar docs por core/produto.

**Nota:** 
- `core/docs/` já contém conteúdo significativo:
  - ✅ `agents/` (7 arquivos)
  - ✅ `architecture/` (32 arquivos - multi_agent/, observer/, orchestrator/, data-models/, infrastructure/, patterns/, vision/)
  - ✅ `vision/` (7 arquivos - cognitive_model/, conversation_mechanics.md, epistemology.md, system_philosophy.md)
  - ✅ `tools/` (2 arquivos - cli.md, conversational_cli.md)
  - ✅ `examples/`, `features/`
- `docs/` na raiz ainda contém: `analysis/`, `epics/`, `interface/`, `process/`, `products/`, `testing/`, `vision/`
- Reorganização física pendente (mover conteúdo da raiz para estrutura final)

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

### Fase 11: ROADMAPs ✅

**Status:** Concluída

**Objetivo:** Criar ROADMAPs separados.

#### Fase 11.1: Criar `core/ROADMAP.md` ✅

**Status:** Concluída
- [x] `core/ROADMAP.md` criado
- [x] Épicos do core extraídos

#### Fase 11.2: Criar `products/revelar/ROADMAP.md` ✅

**Status:** Concluída
- [x] `products/revelar/ROADMAP.md` criado
- [x] Épicos do produto Revelar extraídos

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

### Fase 12: Limpeza Final ⏳

**Status:** Pendente

**Objetivo:** Remover diretórios vazios, ajustar configs finais.

#### Fase 12.1: Remover diretórios vazios da raiz

**Cursor (rápido):**
- [ ] Verificar: `agents/` vazio (apenas __pycache__) - remover
- [ ] Verificar: `app/` vazio (apenas __pycache__) - remover
- [ ] Verificar: `cli/` não existe mais (já removido na Fase 6)
- [ ] Verificar: `utils/` não existe mais (já removido na Fase 2)
- [ ] Verificar: `config/` não existe mais (já removido na Fase 2)
- [ ] Verificar: `tests/integration/` vazio após migração - remover
- [ ] Validar: Apenas diretórios vazios removidos

**Comandos:**
```powershell
# Verificar e remover diretórios vazios (após migração completa)
# Nota: Executar apenas após Fase 8 (testes migrados)
if ((Get-ChildItem agents -ErrorAction SilentlyContinue | Measure-Object).Count -eq 0) { Remove-Item agents -Recurse -Force }
if ((Get-ChildItem app -ErrorAction SilentlyContinue | Measure-Object).Count -eq 0) { Remove-Item app -Recurse -Force }
if ((Get-ChildItem tests/integration -ErrorAction SilentlyContinue | Measure-Object).Count -eq 0) { Remove-Item tests/integration -Recurse -Force }
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

## 7. Checklist de Progresso

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

### Fase 6: CLI ✅
- [x] cli/ movido para core/tools/cli/
- [x] Imports ajustados (project_root path corrigido - 4 níveis para raiz)
- [x] Testes passando (imports validados)
- [x] Commit realizado

### Fase 7: Produto Revelar ✅
- [x] app/ movido para products/revelar/app/
- [x] Imports ajustados (from app. → from products.revelar.app.)
- [x] Caminhos checkpoints.db ajustados (project_root dinâmico)
- [x] Testes de imports ajustados
- [x] Commits realizados

### Fase 8: Testes ⏳
- [x] Imports atualizados para `from core.` (100% - Quick win #1)
- [x] Ajustar último import antigo (`test_observer_integration.py`) ✅
- [x] integration/smoke/ movido fisicamente (3 arquivos + README) ✅ (Quick win #2)
- [ ] unit/ movido fisicamente (43 arquivos)
- [ ] integration/behavior/ movido fisicamente (29 arquivos)
- [ ] 3 arquivos específicos movidos para products/revelar/ (com ajuste de imports)
- [ ] integration/e2e/ movido fisicamente (2 arquivos)
- [ ] Todos passando
- [x] Commits realizados (Quick wins #1 e #2)

### Fase 9: Scripts ⏳
- [x] Imports atualizados para `from core.` (64 arquivos, 90%)
- [ ] Ajustar últimos 2 imports antigos
- [ ] Scripts categorizados
- [ ] Scripts movidos fisicamente
- [ ] Caminhos `Path(__file__).parent` ajustados
- [ ] Scripts testados
- [ ] Commit realizado

### Fase 10: Documentação ⏳
- [x] Conteúdo significativo em `core/docs/` (agents/, architecture/, vision/, tools/)
- [ ] Docs da raiz reorganizados fisicamente
- [ ] Referências atualizadas (~2000)
- [ ] Links validados
- [ ] Commit realizado

### Fase 11: ROADMAPs ✅
- [x] core/ROADMAP.md criado
- [x] products/revelar/ROADMAP.md criado
- [ ] ROADMAP.md raiz atualizado (pendente)
- [ ] Commit realizado

### Fase 12: Limpeza Final
- [ ] Diretórios vazios removidos
- [ ] README.md atualizado
- [ ] ARCHITECTURE.md atualizado
- [ ] Validação final completa
- [ ] Commit final

---

## 8. Troubleshooting

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

## 9. Próximos Passos

Após migração completa:
1. Criar produto **Fichamento** em `products/fichamento/`
2. Evoluir core com novos agentes
3. Criar APIs REST para produtos consumirem core

---

**Versão:** 2.3
**Data:** 2025-12-11
**Status:** Documento mestre - atualizado conforme estado atual do projeto
**Baseado em:** Análises reais de imports, dependências e estrutura atual do projeto
**Última Atualização:**
- Fases 0-9, 11 concluídas ✅
- Fase 8: 100% migrado fisicamente para tests/core/ ✅
- Fase 9: 100% migrado fisicamente para scripts/core/ e scripts/revelar/ ✅
- Fase 10: Conteúdo significativo em core/docs/ (60%), reorganização física pendente ⏳
- Fase 12: Parcial (agents/ removido) ⏳
