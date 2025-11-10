# Implementação Detalhada: TDD, Validação e Commits

## 2. IMPLEMENTAÇÃO AUTÔNOMA

Para cada tarefa, seguir ciclo:

### A) Decidir sobre Teste

**Escrever teste ANTES (TDD) quando:**
- ✅ Lógica de negócio crítica (cálculos, validações, regras)
- ✅ APIs/endpoints (request/response)
- ✅ Manipulação de dados (CRUD, transformações)
- ✅ Integrações externas (mocks necessários)
- ✅ Funções puras (fáceis de testar)

**Implementar SEM teste (ou teste DEPOIS):**
- ⚠️ UI/componentes visuais simples (testar manualmente)
- ⚠️ Configurações/setup (validar via comportamento)
- ⚠️ Estilização (validar visualmente)

### B) Ciclo de Implementação

**Se TDD aplicável:**
1. Escrever teste que falha (Red)
2. Implementar código mínimo (Green)
3. Refatorar se necessário
4. Validar teste passa

**Se TDD não aplicável:**
1. Implementar código
2. Validar comportamento (rodar app, testar rota, etc)

### C) Validação Obrigatória

Antes de seguir para próxima tarefa:
- ✅ Testes passando (se houver)
- ✅ **Script de validação criado** (scripts/validate_*.py) - **PRÁTICA RECOMENDADA**
- ✅ Aplicação rodando sem erros
- ✅ Comportamento esperado funcionando
- ✅ Documentação da tarefa atualizada (incremental)

**Scripts de Validação (Boa Prática):**

Criar scripts de validação é uma **excelente prática** porque:
- ✅ **Ajuda a entender o módulo**: Rodar o script mostra claramente o que o código faz
- ✅ **Facilita validação manual**: Dev pode testar sem precisar escrever código
- ✅ **Documenta comportamento esperado**: Script serve como documentação viva
- ✅ **Acelera debugging**: Identifica problemas rapidamente

**Quando criar script de validação:**
- Módulos/classes com comportamento não-trivial
- Tools/funções que serão usadas por outros componentes
- Estados complexos (como TypedDicts, Pydantic models)
- Qualquer código onde "ver funcionando" ajuda a entender

**Estrutura recomendada:**
```python
"""
Script de validação manual para [nome do módulo].

Valida que [módulo] foi implementado corretamente com:
- [Característica 1]
- [Característica 2]
- [Característica 3]
"""

import sys
from pathlib import Path

# Adicionar o diretório raiz ao PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Imports do módulo a validar
from module import SomeClass

def validate_module():
    """Valida a implementação do módulo."""
    print("=" * 70)
    print("VALIDAÇÃO DO MÓDULO X")
    print("=" * 70)

    # Teste 1
    print("\n1. Testando característica 1...")
    assert condition, "Erro: descrição"
    print("   ✅ Característica 1 funciona")

    # Teste 2
    print("\n2. Testando característica 2...")
    # ...

    print("\n" + "=" * 70)
    print("TODOS OS TESTES PASSARAM! ✅")
    print("=" * 70)

if __name__ == "__main__":
    try:
        validate_module()
    except AssertionError as e:
        print(f"\n❌ ERRO: {e}")
        sys.exit(1)
```

**Localização:** `scripts/validate_*.py` (ex: `scripts/validate_ask_user.py`)

### D) Commit (Opcional e Estratégico)

Fazer commit quando:
- Tarefa representa marco significativo
- Antes de mudança arriscada (para facilitar restore)
- **Não obrigatório** - use seu julgamento

Formato: `tipo: descrição sucinta - Task N`

---

**Ver também:**
- Para lidar com travamentos → [blockers.md](blockers.md)
- Para finalização e entrega → [delivery.md](delivery.md)
- Para regras de qualidade → [quality_rules.md](quality_rules.md)
