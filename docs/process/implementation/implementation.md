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

### A.1) Checkpoints: Fluindo entre Funcionalidades

**O que é um checkpoint:**
- Conjunto de funcionalidades relacionadas que juntas agregam valor
- Exemplo: Features 11.1 + 11.2 + 11.3 = 1 checkpoint = 1 PR
- Documentado em `docs/process/current_implementation.md`

**Como trabalhar dentro de um checkpoint:**
1. Implementar TODAS as funcionalidades do checkpoint sem parar
2. Para cada funcionalidade:
   - Planejar tarefas
   - Executar incrementalmente
   - Validar localmente (sintaxe, imports)
3. NÃO parar entre funcionalidades (manter fluxo)
4. **AO FIM DO CHECKPOINT:**
   - Atualizar `current_implementation.md`:
     - Marcar checkpoint como ✅
     - Adicionar info (branch, estimativas realizadas)
   - Fornecer comandos de validação ao dev
   - Commitar código + documentação atualizada

**Exemplo de fluxo:**
```
Checkpoint 1 = Features 11.1 + 11.2

Feature 11.1 (Schema):
  Tarefa 1: Criar Proposicao
  Tarefa 2: Atualizar schema SQL
  ✅ Sintaxe OK

Feature 11.2 (Adapter):
  Tarefa 1: Criar ProposicaoAdapter
  Tarefa 2: Implementar to_legacy()
  ✅ Sintaxe OK

AO FIM:
  Atualizar current_implementation.md (Checkpoint 1 ✅)
  Fornecer comandos de validação
  PARAR e aguardar validação do dev
```

**Finalização do último checkpoint:**
- Implementar checkpoint
- **DELETAR** `docs/process/current_implementation.md`
- Commitar código + remoção do arquivo

**Benefício:**
- ✅ Fluxo contínuo dentro do checkpoint
- ✅ Validação quando há valor real entregue
- ✅ PRs menores e mais coesas
- ✅ Documentação sempre atualizada pós-checkpoint

### A.2) Reflexão Obrigatória Entre Features

**Ao finalizar cada feature dentro do checkpoint:**

1. **Validar feature atual:**
   - ✅ Sintaxe Python OK
   - ✅ Imports funcionando
   - ✅ Buscar impactos em outros módulos

2. **Refletir sobre próxima feature:**
   - 🔍 Ler código atualizado (feature anterior pode ter mudado contexto)
   - 🔍 Avaliar se plano original ainda faz sentido
   - 🔍 Identificar riscos/bloqueios/incertezas
   - 🔍 **Replanejar se necessário** (não seguir cegamente)

3. **Decidir próximo passo:**
   
   **Se tudo claro e sem riscos:**
   - ✅ Seguir para próxima feature (não parar)
   - ✅ Manter fluxo contínuo

   **Se há riscos, bloqueios ou incertezas:**
   - ⚠️ **PARAR e reportar ao dev:**
```
     ⚠️ Reflexão após Feature X.Y:
     
     Identifiquei risco/bloqueio:
     [descrição do problema]
     
     Impacto no plano:
     [como afeta features seguintes]
     
     Opções:
     A) [ajustar abordagem]
     B) [replanejar checkpoint]
     C) [pedir esclarecimento]
     
     Como prefere prosseguir?
```

**Exemplo de fluxo:**
```
Feature 11.1 implementada
  ↓
Reflexão: Tudo OK, próxima feature clara
  ↓
Feature 11.2 (sem parar)
  ↓
Reflexão: ⚠️ Código da 11.2 revelou que 11.3 precisa abordagem diferente
  ↓
PARAR e reportar ao dev
  ↓
Dev ajusta plano ou confirma abordagem
  ↓
Feature 11.3 (com nova abordagem)
```

**Objetivo:**
- ✅ Manter fluxo quando caminho está claro
- ✅ Evitar implementação cega de plano desatualizado
- ✅ Parar apenas quando há dúvida real (não por trivialidades)

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
- ✅ **Script de validação criado** (scripts/<categoria>/validate_*.py) - **PRÁTICA RECOMENDADA**
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

**Estrutura recomendada (padrão de script de validação):**
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

**Localização:** `scripts/<categoria>/validate_*.py` (ex: `scripts/state_introspection/validate_ask_user.py`)

**Idioma e convenções:**
- Nomes de funções, variáveis e arquivos em inglês (`validate_module`, `project_root`), conforme [`language_guidelines.md`](language_guidelines.md)
- Docstrings, prints e mensagens de erro em PT-BR (explicando o que está sendo validado)

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
