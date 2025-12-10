# Análise: Estratégia de Automação para Migração

**Data:** 2025-01-27  
**Contexto:** Identificar o que pode ser automatizado na migração para estrutura monorepo  
**Objetivo:** Reduzir trabalho manual e riscos de erro humano

---

## 📊 Resumo Executivo

**Total de Mudanças Identificadas:**
- **Imports Python:** ~218 linhas (139 `from agents.` + 79 `from utils.`)
- **Referências em Docs:** ~251 referências (196 `agents/` + 55 `utils/`)
- **Arquivos a Mover:** ~100+ arquivos Python + ~50 arquivos de documentação

**Automação Recomendada:**
- ✅ **Substituição de Imports:** 95% automatizável com regex
- ✅ **Movimentação de Arquivos:** 100% automatizável com `git mv`
- ✅ **Atualização de Docs:** 90% automatizável com find/replace
- ⚠️ **Validação:** Requer revisão manual após automação

---

## 1. Substituição de Imports (Regex)

### 1.1. Padrões Identificados

| Padrão Antigo | Padrão Novo | Regex | Arquivos Afetados | Complexidade |
|---------------|-------------|-------|-------------------|--------------|
| `from agents.` | `from core.agents.` | `^from agents\.` | ~82 arquivos (139 linhas) | 🟢 Simples |
| `from utils.` | `from core.utils.` | `^from utils\.` | ~50 arquivos (79 linhas) | 🟢 Simples |
| `from utils.prompts.` | `from core.prompts.` | `^from utils\.prompts\.` | ~20 arquivos | 🟢 Simples |
| `from app.` | `from products.revelar.app.` | `^from app\.` | ~10 arquivos | 🟢 Simples |
| `import agents.` | `import core.agents.` | `^import agents\.` | 0 arquivos | 🟢 Simples |
| `import utils.` | `import core.utils.` | `^import utils\.` | 0 arquivos | 🟢 Simples |

**Total:** ~218 linhas de imports em ~142 arquivos únicos

### 1.2. Regex Patterns Detalhados

#### Padrão 1: `from agents.X` → `from core.agents.X`
```regex
^from agents\.
```
**Substituição:** `from core.agents.`

**Exemplos:**
- `from agents.models.cognitive_model import CognitiveModel` → `from core.agents.models.cognitive_model import CognitiveModel`
- `from agents.orchestrator.state import MultiAgentState` → `from core.agents.orchestrator.state import MultiAgentState`
- `from agents.memory.memory_manager import MemoryManager` → `from core.agents.memory.memory_manager import MemoryManager`

**Cuidados:** Nenhum - padrão simples e seguro.

---

#### Padrão 2: `from utils.X` → `from core.utils.X`
```regex
^from utils\.
```
**Substituição:** `from core.utils.`

**Exemplos:**
- `from utils.cost_tracker import CostTracker` → `from core.utils.cost_tracker import CostTracker`
- `from utils.json_parser import extract_json_from_llm_response` → `from core.utils.json_parser import extract_json_from_llm_response`
- `from utils.config import get_anthropic_model` → `from core.utils.config import get_anthropic_model`

**Cuidados:** Nenhum - padrão simples e seguro.

---

#### Padrão 3: `from utils.prompts.X` → `from core.prompts.X`
```regex
^from utils\.prompts\.
```
**Substituição:** `from core.prompts.`

**Exemplos:**
- `from utils.prompts import METHODOLOGIST_DECIDE_PROMPT_V2` → `from core.prompts import METHODOLOGIST_DECIDE_PROMPT_V2`

**Cuidados:** 
- ⚠️ Este padrão deve ser aplicado **ANTES** do padrão 2 (`from utils.`)
- Caso contrário, `from utils.prompts.` será transformado em `from core.utils.prompts.` (incorreto)

**Ordem de Aplicação:**
1. Primeiro: `from utils.prompts.` → `from core.prompts.`
2. Depois: `from utils.` → `from core.utils.`

---

#### Padrão 4: `from app.X` → `from products.revelar.app.X`
```regex
^from app\.
```
**Substituição:** `from products.revelar.app.`

**Exemplos:**
- `from app.chat import ChatState` → `from products.revelar.app.chat import ChatState`
- `from app.components.sidebar import Sidebar` → `from products.revelar.app.components.sidebar import Sidebar`

**Cuidados:** 
- ⚠️ Aplicar apenas após mover `app/` para `products/revelar/app/`
- Verificar se há imports relativos que precisam de ajuste manual

---

### 1.3. Casos que NÃO Podem Usar Regex Simples

#### ❌ Imports Relativos
```python
# Casos que requerem revisão manual:
from .models import CognitiveModel  # Dentro de agents/
from ..utils import CostTracker     # Dentro de subdiretório
```

**Ação:** Buscar manualmente com `grep -r "from \."` e revisar caso a caso.

---

#### ❌ Strings Literais
```python
# Strings que contêm caminhos (não são imports):
config_path = "agents/orchestrator/config.yaml"
sys.path.insert(0, "agents/")
```

**Ação:** Buscar com `grep -r "agents/"` e `grep -r "utils/"` e revisar manualmente.

---

#### ❌ Comentários e Documentação em Código
```python
# Exemplo: agents/orchestrator/nodes.py
"""
Este módulo usa agents.memory para...
"""
```

**Ação:** Atualizar manualmente ou incluir em substituição de docs (seção 3).

---

#### ❌ Imports Dinâmicos
```python
# Casos raros (verificar se existem):
module = __import__("agents.orchestrator")
importlib.import_module("agents.memory")
```

**Ação:** Buscar com `grep -r "__import__"` e `grep -r "importlib"` e revisar manualmente.

---

### 1.4. Estratégia de Substituição

**Recomendação:** Usar find/replace do IDE (VS Code, PyCharm) com regex:

1. **Fase 1:** Substituir `from utils.prompts.` → `from core.prompts.` (prioridade)
2. **Fase 2:** Substituir `from agents.` → `from core.agents.`
3. **Fase 3:** Substituir `from utils.` → `from core.utils.`
4. **Fase 4:** Substituir `from app.` → `from products.revelar.app.` (após mover app/)

**Validação Pós-Substituição:**
```powershell
# Verificar se não sobrou nenhum padrão antigo
Get-ChildItem -Path . -Recurse -Include *.py | Select-String -Pattern "^from agents\." | Measure-Object
Get-ChildItem -Path . -Recurse -Include *.py | Select-String -Pattern "^from utils\." | Measure-Object
```

---

## 2. Movimentação de Arquivos

### 2.1. Estratégia com `git mv`

**Por que `git mv`?**
- ✅ Preserva histórico do Git
- ✅ Detecta renomeações automaticamente
- ✅ Mantém rastreabilidade de mudanças

**Comando Base:**
```powershell
# PowerShell (Windows)
git mv agents/ core/agents/
git mv utils/ core/utils/
git mv config/ core/config/
git mv cli/ core/tools/cli/
git mv app/ products/revelar/app/
```

### 2.2. Script de Automação (PowerShell)

**Vale a pena criar script?** ✅ **SIM** - Reduz erros e padroniza processo.

**Exemplo de Script:**
```powershell
# scripts/migration/move_files.ps1
# Executa movimentação de arquivos preservando histórico Git

Write-Host "Iniciando movimentação de arquivos..." -ForegroundColor Green

# Core
git mv agents core/agents
git mv utils core/utils
git mv config core/config
git mv cli core/tools/cli

# Prompts (subdiretório especial)
git mv core/utils/prompts core/prompts

# Produto Revelar
git mv app products/revelar/app

Write-Host "Movimentação concluída!" -ForegroundColor Green
Write-Host "Verifique com: git status" -ForegroundColor Yellow
```

**Vantagens:**
- ✅ Execução rápida e consistente
- ✅ Fácil de reverter se necessário
- ✅ Documenta o processo

**Desvantagens:**
- ⚠️ Requer que diretórios destino já existam (Fase 1)
- ⚠️ Pode falhar se houver conflitos (resolver manualmente)

---

### 2.3. Ordem de Movimentação

**Seguir ordem de dependências:**

1. **Primeiro:** `utils/` → `core/utils/` (menos dependências)
2. **Segundo:** `config/` → `core/config/` (usado por agents/)
3. **Terceiro:** `agents/` → `core/agents/` (depende de utils/ e config/)
4. **Quarto:** `utils/prompts/` → `core/prompts/` (após mover utils/)
5. **Quinto:** `cli/` → `core/tools/cli/` (depende de agents/)
6. **Sexto:** `app/` → `products/revelar/app/` (depende de agents/)

**Validação:**
```powershell
# Verificar se diretórios antigos foram removidos
Test-Path agents/  # Deve retornar False
Test-Path utils/   # Deve retornar False
```

---

## 3. Atualização de Documentação

### 3.1. Padrões em Markdown

| Padrão Antigo | Padrão Novo | Arquivos Afetados |
|---------------|-------------|-------------------|
| `agents/orchestrator/` | `core/agents/orchestrator/` | ~43 arquivos (196 matches) |
| `utils/event_bus/` | `core/utils/event_bus/` | ~21 arquivos (55 matches) |
| `app/chat.py` | `products/revelar/app/chat.py` | ~10 arquivos |
| `config/agents/` | `core/config/agents/` | ~5 arquivos |

**Total:** ~251 referências em ~79 arquivos de documentação

---

### 3.2. Substituição em Massa

**Recomendação:** Usar find/replace do IDE com regex:

**Padrões para Substituir:**
```regex
# Caminhos de diretórios
agents/(orchestrator|observer|methodologist|structurer|memory|database|checklist|persistence|models)
→ core/agents/$1

utils/(event_bus|config|cost_tracker|currency|debug|structured_logger|test_executor|token_extractor|providers|prompts)
→ core/utils/$1

app/
→ products/revelar/app/

config/agents/
→ core/config/agents/
```

**Cuidados:**
- ⚠️ Não substituir em blocos de código que mostram exemplos antigos (comentários históricos)
- ⚠️ Verificar links relativos que podem quebrar
- ⚠️ Atualizar referências em tabelas e listas

---

### 3.3. Validação de Links Quebrados

**Script de Validação:**
```powershell
# scripts/migration/validate_doc_links.ps1
# Verifica links quebrados em documentação

$brokenLinks = @()

Get-ChildItem -Path docs -Recurse -Include *.md | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    $links = [regex]::Matches($content, '\[([^\]]+)\]\(([^\)]+)\)')
    
    foreach ($link in $links) {
        $path = $link.Groups[2].Value
        if ($path -match '^(agents|utils|app|config)/') {
            $brokenLinks += "$($_.FullName): $path"
        }
    }
}

if ($brokenLinks.Count -gt 0) {
    Write-Host "Links quebrados encontrados:" -ForegroundColor Red
    $brokenLinks | ForEach-Object { Write-Host $_ }
} else {
    Write-Host "Nenhum link quebrado encontrado!" -ForegroundColor Green
}
```

---

## 4. Script de Migração Completo

### 4.1. Vale a Pena Criar?

**✅ SIM, mas com ressalvas:**

**Vantagens:**
- ✅ Execução consistente e reproduzível
- ✅ Validação automática de sintaxe Python
- ✅ Relatório detalhado de mudanças
- ✅ Pode ser executado em etapas (dry-run primeiro)

**Desvantagens:**
- ⚠️ Desenvolvimento inicial leva tempo (~2-3h)
- ⚠️ Pode ter bugs que quebram código
- ⚠️ Requer testes extensivos antes de usar

**Recomendação:** 
- **Para migração única:** Use find/replace do IDE + `git mv` manual
- **Para múltiplas migrações futuras:** Vale criar script reutilizável

---

### 4.2. Estrutura do Script (Se Criar)

```python
# scripts/migration/automate_migration.py
"""
Script de automação para migração monorepo.

Uso:
    python scripts/migration/automate_migration.py --dry-run
    python scripts/migration/automate_migration.py --execute
"""

import re
import ast
import subprocess
from pathlib import Path
from typing import List, Dict, Tuple

class MigrationAutomator:
    """Automatiza substituição de imports e validação."""
    
    # Padrões de substituição (ordem importa!)
    REPLACEMENTS = [
        (r'^from utils\.prompts\.', 'from core.prompts.'),
        (r'^from agents\.', 'from core.agents.'),
        (r'^from utils\.', 'from core.utils.'),
        (r'^from app\.', 'from products.revelar.app.'),
    ]
    
    def find_files(self, pattern: str) -> List[Path]:
        """Encontra arquivos Python."""
        # Implementação...
        pass
    
    def replace_imports(self, file_path: Path, dry_run: bool = True) -> Dict:
        """Substitui imports em arquivo."""
        # Implementação...
        pass
    
    def validate_syntax(self, file_path: Path) -> bool:
        """Valida sintaxe Python após mudança."""
        # Implementação...
        pass
    
    def generate_report(self, changes: List[Dict]) -> str:
        """Gera relatório de mudanças."""
        # Implementação...
        pass

if __name__ == '__main__':
    # CLI...
    pass
```

**Funcionalidades:**
1. ✅ Busca arquivos Python recursivamente
2. ✅ Aplica substituições na ordem correta
3. ✅ Valida sintaxe Python com `ast.parse()`
4. ✅ Gera relatório de mudanças
5. ✅ Suporta `--dry-run` para preview
6. ✅ Cria backup antes de modificar

---

### 4.3. Alternativa Mais Simples: Find/Replace do IDE

**Recomendação Final:** Para esta migração única, use:

1. **VS Code / PyCharm Find/Replace:**
   - ✅ Interface visual e segura
   - ✅ Preview antes de aplicar
   - ✅ Suporta regex
   - ✅ Pode fazer em múltiplos arquivos de uma vez

2. **Processo Manual Controlado:**
   - ✅ Mais seguro (revisão a cada passo)
   - ✅ Permite pausar entre fases
   - ✅ Fácil de reverter se necessário

**Quando Criar Script:**
- Se planejar fazer migrações similares no futuro
- Se o projeto tiver >500 arquivos Python
- Se precisar de automação CI/CD para validação

---

## 5. Checklist de Automação

### Fase 1: Preparação
- [ ] Backup do repositório (`git branch backup/pre-migration`)
- [ ] Criar diretórios destino (Fase 1 do MIGRATION.md)
- [ ] Validar que testes passam antes de começar

### Fase 2: Substituição de Imports
- [ ] Substituir `from utils.prompts.` → `from core.prompts.` (prioridade)
- [ ] Substituir `from agents.` → `from core.agents.`
- [ ] Substituir `from utils.` → `from core.utils.`
- [ ] Validar: `pytest tests/unit/ -v` (deve quebrar - imports não encontrados ainda)

### Fase 3: Movimentação de Arquivos
- [ ] Executar `git mv` para cada diretório (ou script)
- [ ] Validar: `git status` mostra apenas movimentações
- [ ] Validar: `pytest tests/unit/ -v` (deve passar agora)

### Fase 4: Atualização de Docs
- [ ] Substituir referências `agents/` → `core/agents/` em docs/
- [ ] Substituir referências `utils/` → `core/utils/` em docs/
- [ ] Validar links quebrados (script ou manual)

### Fase 5: Validação Final
- [ ] Todos os testes passam
- [ ] Nenhum import antigo restante
- [ ] Documentação atualizada
- [ ] Commit realizado

---

## 6. Riscos e Mitigações

### Risco 1: Regex Substitui Mais do Que Deveria
**Mitigação:**
- Usar regex específicos (`^from agents\.` não `agents\.`)
- Fazer substituição por fases (testar após cada fase)
- Usar find/replace do IDE com preview

### Risco 2: Git mv Perde Histórico
**Mitigação:**
- Sempre usar `git mv` (nunca `mv` ou renomear no explorador)
- Validar com `git log --follow <arquivo>` após mover

### Risco 3: Links Quebrados em Docs
**Mitigação:**
- Executar script de validação após atualizar docs
- Revisar manualmente arquivos críticos (README.md, ARCHITECTURE.md)

### Risco 4: Imports Relativos Quebrados
**Mitigação:**
- Buscar manualmente: `grep -r "from \."`
- Revisar cada caso individualmente

---

## 7. Conclusão

### Automação Recomendada

**✅ AUTOMATIZAR:**
1. Substituição de imports (find/replace IDE com regex)
2. Movimentação de arquivos (script PowerShell simples ou `git mv` manual)
3. Substituição em documentação (find/replace IDE)

**⚠️ REVISAR MANUALMENTE:**
1. Imports relativos (`from .`, `from ..`)
2. Strings literais com caminhos
3. Links em documentação
4. Validação de sintaxe Python após mudanças

**❌ NÃO VALE CRIAR SCRIPT COMPLEXO:**
- Para migração única, find/replace do IDE é mais rápido e seguro
- Script complexo leva tempo para desenvolver e testar
- Processo manual permite revisão incremental

### Próximos Passos

1. Revisar esta análise
2. Decidir: script simples ou find/replace manual
3. Executar automação por fases (conforme MIGRATION.md)
4. Validar após cada fase

---

**Versão:** 1.0  
**Data:** 2025-01-27  
**Status:** Análise completa - pronto para execução

