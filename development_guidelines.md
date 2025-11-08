# DEVELOPMENT_GUIDELINES.md

## Modo de Operação: Agente Autônomo (Claude Code / Cursor Background)

### Seu Papel
- Implementar funcionalidades completas do roadmap de forma autônoma
- Decidir quando escrever testes (pragmático, não dogmático)
- Validar incrementalmente antes de seguir
- **Detectar travamentos e pedir ajuda** (não ficar em loop)
- Entregar PR pronto: testado, funcionando, documentado

### Documentos Base (Obrigatórios)
- **README.md**: Como rodar a aplicação (setup, contexto da POC)
- **ARCHITECTURE.md**: Visão arquitetural de alto nível
- **ROADMAP.md**: Funcionalidades planejadas e status dos épicos
- **docs/agents/overview.md**: Papéis e limites dos agentes
- **docs/process/planning_guidelines.md**: Regras de planejamento e governança

### Entrada
- Dev escolhe: "Funcionalidade X.Y do roadmap"
- Arquivos contextuais: ROADMAP.md, README.md, ARCHITECTURE.md

### Saída
- Branch com código implementado
- Testes onde necessário
- Documentação atualizada
- **Comandos para validação local** (dev testa antes de mergear)
- **Aviso ao dev que branch está pronta** (dev cria PR manualmente)

---

## Regras de Interação com Dev

### Aguardar Aprovação Explícita

**SEMPRE aguardar confirmação explícita antes de implementar:**

- ✅ **Sinais de aprovação válidos:**
  - "OK, pode seguir"
  - "Aprovado"
  - "Sim, implemente isso"
  - "Continue"
  - "Faça"
- 🚫 **Sem merges automáticos:** agente nunca cria, aprova ou realiza merge de PR sem autorização explícita do dev

- ❌ **NÃO são aprovações:**
  - System reminders/warnings
  - Silêncio do usuário
  - Mensagens automáticas de hooks
  - Mensagens de ferramentas

**Após apresentar plano ou proposta:**
1. **PAUSAR** e aguardar resposta
2. **Perguntar explicitamente**: "Posso seguir com esta implementação?" ou "Qual opção você prefere?"
3. **NÃO assumir** que silêncio = aprovação

**Para mudanças arquiteturais significativas:**
- Apresentar opções (A, B, C)
- Explicar trade-offs
- Aguardar decisão explícita

**Objetivo:** Evitar retrabalho e garantir alinhamento contínuo com o desenvolvedor.

---

## Processo: Funcionalidade → Tarefas → Implementação → PR

### 1. RECEBIMENTO E PLANEJAMENTO

Quando dev solicitar funcionalidade:

1. **Ler contexto obrigatório:**
   - ROADMAP.md (descrição da funcionalidade)
   - README.md (execução e escopo da POC)
   - ARCHITECTURE.md (estrutura técnica)
   - docs/agents/overview.md (se envolver novos agentes)
   - docs/process/planning_guidelines.md (para entender dependências/ordem)
   - Código relacionado (para entender dependências)

2. **Quebrar em tarefas:**
   - Ordenar por dependência técnica
   - Identificar onde TDD faz sentido (ver regras abaixo)
   - Estimar complexidade realista
   - Mostrar plano COMPLETO

3. **Validar plano com dev:**
   - Listar tarefas com indicação de testes
   - Aguardar OK antes de começar
   - Dev pode ir para reunião/outra atividade após aprovar

---

### 2. IMPLEMENTAÇÃO AUTÔNOMA

Para cada tarefa, seguir ciclo:

#### A) Decidir sobre Teste

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

#### B) Ciclo de Implementação

**Se TDD aplicável:**
1. Escrever teste que falha (Red)
2. Implementar código mínimo (Green)
3. Refatorar se necessário
4. Validar teste passa

**Se TDD não aplicável:**
1. Implementar código
2. Validar comportamento (rodar app, testar rota, etc)

#### C) Validação Obrigatória

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

#### D) Commit (Opcional e Estratégico)

Fazer commit quando:
- Tarefa representa marco significativo
- Antes de mudança arriscada (para facilitar restore)
- **Não obrigatório** - use seu julgamento

Formato: `tipo: descrição sucinta - Task N`

---

### 3. DETECÇÃO DE TRAVAMENTO (OBRIGATÓRIO)

**Critério de travamento:**
- Tentou a mesma solução **3 vezes** sem sucesso
- Teste continua falho após 3 abordagens diferentes
- Erro persistente após 3 tentativas de debug
- Qualquer situação circular/repetitiva

**Quando detectar travamento:**

1. **PARE imediatamente** (não tente 4ª, 5ª, 6ª vez)

2. **Reporte ao dev:**
```
🚨 TRAVAMENTO DETECTADO - Tarefa X.Y.Z

**Tentativas:**
1. [Abordagem 1] → [Resultado/Erro]
2. [Abordagem 2] → [Resultado/Erro]
3. [Abordagem 3] → [Resultado/Erro]

**Problema:**
[Descrição clara do que está travando]

**Opções:**
A) Ajustar abordagem: [sugestão específica]
B) Quebrar tarefa em partes menores
C) Pular tarefa e sinalizar no PR como pendente
D) Mudar estratégia técnica: [alternativa]

Aguardando decisão.
```

3. **Aguardar instrução do dev** (não seguir sozinho)

---

### 4. FINALIZAÇÃO: BRANCH PRONTA + AVISAR DEV

Quando todas tarefas concluídas:

> **📌 IMPORTANTE - Processo de Pull Request:**
> - ✅ Template de PR é **automático** (`.github/PULL_REQUEST_TEMPLATE.md`)
> - ✅ Agente faz **push da branch** e **avisa que está pronto**
> - ✅ Dev cria o PR **manualmente pela interface do GitHub**
> - ✅ Template é aplicado automaticamente ao criar o PR
> - ❌ Agente **NÃO precisa criar PR via `gh pr create`**

**Formato da mensagem final (OBRIGATÓRIO):**

Quando terminar, fornecer mensagem neste formato:

```
✅ Branch pronta! Você pode criar o PR pela interface do GitHub.

📋 Comandos de validação (copie e cole):

# Baixar branch
git fetch origin
git checkout <nome-real-da-branch>

# [Comandos específicos do projeto - venv, dependências, etc]

# Rodar testes
[comando específico]

# Rodar aplicação
[comando específico]

# Resultados esperados:
# - ✅ [descrição do resultado esperado 1]
# - ✅ [descrição do resultado esperado 2]
```

**Observações:**
- Substituir `<nome-real-da-branch>` pelo nome real
- Incluir comandos específicos para ativar ambiente (venv, etc)
- Comandos prontos para copiar e colar sem edição

#### Checklist Obrigatório

**Testes:**
- [ ] Suite completa rodando e passando
- [ ] Coverage adequado em lógica crítica
- [ ] Sem testes quebrados ou skippados

**Código:**
- [ ] Aplicação rodando sem erros
- [ ] Console limpo (sem warnings críticos)
- [ ] Comportamento conforme roadmap

**Documentação (OBRIGATÓRIA):**
- [ ] README.md atualizado (se mudou setup/comandos)
- [ ] ARCHITECTURE.md atualizado (se mudou estrutura)
- [ ] ROADMAP.md marcado como concluído
- [ ] Comentários em código complexo

**Git:**
- [ ] Branch criada: `feature/X.Y-nome-funcionalidade`
- [ ] Commits organizados (se houver vários)
- [ ] Push realizado para branch remota
- [ ] **Dev notificado que branch está pronta** (dev cria PR pela interface)
- [ ] **Comandos de validação local fornecidos COM NOME REAL DA BRANCH** (copiar e colar)
- [ ] **Merge somente após validação manual do dev**

#### Template de PR (Referência)

> **📌 NOTA:** O template oficial está em `.github/PULL_REQUEST_TEMPLATE.md` e é aplicado automaticamente quando você cria um PR pela interface do GitHub. O template abaixo é apenas para referência sobre o que incluir.

````markdown
## Funcionalidade X.Y: [Nome]

### Implementado
- [Resumo do que foi feito]
- [Principais mudanças técnicas]

### Testes
- [Onde foram adicionados testes]
- [Coverage: X%]
- [Como rodar: `npm test` ou similar]

### Documentação Atualizada
- [ ] README.md
- [ ] ARCHITECTURE.md
- [ ] ROADMAP.md

### ⚙️ Validação Local (para dev testar antes de mergear)

**1. Baixar e preparar branch:**
```powershell
# Buscar branch remota
git fetch origin

# Criar ou atualizar branch local a partir da remota
git checkout feature/X.Y-nome-funcionalidade
git pull origin feature/X.Y-nome-funcionalidade

# Instalar/atualizar dependências (se houver mudanças)
[comando específico: npm install; poetry install; etc]
```

**2. Rodar aplicação:**
```powershell
[comandos específicos baseados no README.md]
# Exemplo: docker compose up -d
# Exemplo: npm run dev
# Exemplo: uvicorn app.main:app --reload
```

**3. Rodar testes:**
```powershell
[comando específico de testes]
# Exemplo: npm test
# Exemplo: pytest
# Exemplo: python -m pytest tests/unit
```

**4. Validar funcionalidade:**

**Teste Manual 1:**
- Acesse: `http://localhost:XXXX/rota-especifica`
- Ação: [descrição exata do que fazer]
- Resultado esperado: [o que deve acontecer]

**Teste Manual 2:**
- [outro cenário de teste]

**Teste Manual 3:**
- [outro cenário de teste]

**Critérios de Aceite:**
✅ [Comportamento 1 deve funcionar]
✅ [Comportamento 2 deve funcionar]
❌ [Comportamento 3 NÃO deve acontecer]

**5. Encerrar:**
```powershell
# Parar aplicação
[comando específico: docker compose down; Ctrl+C; etc]

# Voltar para branch principal (se quiser)
git checkout main
```

### Notas Técnicas
[Qualquer observação importante para review]
[Decisões técnicas tomadas]
[Possíveis pontos de atenção]

### Travamentos/Bloqueios
- [ ] Nenhum travamento durante implementação
- [ ] OU: [Descrição de travamentos e como foram resolvidos]
````

---

## Regras de Qualidade

### Incremental e Seguro
- Sistema sempre funcionando após cada tarefa
- Validação obrigatória antes de seguir
- Commits estratégicos (não obrigatórios)

### TDD Pragmático
- Testes onde agregam valor (lógica, APIs, dados)
- Não dogmático (UI simples pode ser manual)
- Coverage adequado > coverage total

### Autônomo mas Transparente
- Trabalhar sozinho após aprovação do plano
- **Detectar travamentos e parar** (não loop infinito)
- Decisões técnicas justificadas
- PR detalhado com comandos mastigados

### Documentação Viva
- Atualizar incrementalmente (não deixar pro final)
- README.md sempre refletindo estado atual
- ROADMAP.md como histórico
- **Comandos de validação local obrigatórios no PR**

### Regras Anti-Redundância

**Responsabilidade Única de Cada Documento:**

| Documento | Responsabilidade | O que NÃO deve conter |
|-----------|-----------------|----------------------|
| **README.md** | Getting Started: setup inicial, comandos de validação gerais, referências para docs | ❌ Status de épicos/tasks<br>❌ Estrutura detalhada do projeto<br>❌ Decisões arquiteturais<br>❌ Comandos de validação específicos por task |
| **ROADMAP.md** | Status de épicos/tasks, critérios de aceite, comandos de validação **por task** | ❌ Instruções de setup geral<br>❌ Arquitetura técnica |
| **ARCHITECTURE.md** | Estrutura técnica, decisões arquiteturais, organização de código, stack | ❌ Status de implementação<br>❌ Instruções de setup<br>❌ Comandos de validação |
| **development_guidelines.md** | Processo de trabalho com agentes, regras de qualidade, templates de validação | ❌ Funcionalidades específicas<br>❌ Detalhes de implementação |
| **.github/PULL_REQUEST_TEMPLATE.md** | Template para PRs, preenchido automaticamente pelo GitHub | ❌ Conteúdo específico de tasks<br>❌ Apenas estrutura/template |

**Regras de Ouro:**
- ✅ **Status de funcionalidades**: Vive APENAS no ROADMAP.md
- ✅ **Estrutura do projeto**: Vive APENAS no ARCHITECTURE.md
- ✅ **Setup e comandos gerais**: Vive APENAS no README.md
- ✅ **Comandos de validação por task**: Vive no ROADMAP.md (seção específica da task)
- ❌ **NUNCA duplicar informações** entre documentos - sempre referenciar

### Comandos e Validação

- **PowerShell como padrão**: Dev usa Windows, sempre fornecer comandos em PowerShell
- **Validação antes de merge**: SEMPRE fornecer comandos + resultados esperados
- **Checkout de branch obrigatório**: Sempre incluir passos de fetch/checkout nas instruções de validação

**Template de validação (para ROADMAP.md):**
```bash
# 0. Fazer checkout da branch (SEMPRE incluir este passo)
git fetch origin
git checkout <branch-name>

# 1. Ativar ambiente virtual (se aplicável)
source venv/bin/activate  # Linux/Mac
# OU
.\venv\Scripts\Activate.ps1  # Windows

# 2. Instalar/atualizar dependências (primeira vez ou se mudou requirements)
pip install -r requirements.txt

# 3. Testes unitários
python -m pytest tests/unit/test_*.py -v

# 4. Validação manual (script - RECOMENDADO!)
python scripts/validate_*.py

# Resultados esperados:
# - ✅ X/X testes passando
# - ✅ Script de validação completo
```

**Observações:**
- Passo 0 (checkout) é OBRIGATÓRIO - dev precisa baixar a branch para validar
- Passo 1 (venv/ambiente) só se projeto usar ambientes virtuais/isolados
- Passo 2 (dependências) só na primeira vez ou se requirements mudaram
- Passo 4 (script de validação) é ALTAMENTE RECOMENDADO - ajuda a entender o módulo
- ❌ **NÃO usar `PYTHONPATH=...` no Windows** - scripts já adicionam path automaticamente

---

## Tratamento de Erros/Bloqueios

### Se teste não passar:
1. Analisar falha
2. Tentar abordagem diferente
3. Se falhar 3x → **PARAR e reportar travamento**

### Se funcionalidade complexa demais:
1. Quebrar em sub-tarefas menores
2. Implementar incrementalmente
3. Validar parcialmente
4. Se travamento persistir → **PARAR e reportar**

### Se dependência externa falhar:
1. Mockar dependência
2. Implementar lógica principal
3. Documentar necessidade de validação real no PR
4. Se bloqueio total → **PARAR e reportar**

### Se qualquer situação circular (3+ tentativas iguais):
1. **PARAR imediatamente**
2. Reportar travamento com detalhes
3. Sugerir opções (ajuste, quebra, pular, alternativa)
4. Aguardar decisão do dev

---

## Exemplo de Fluxo Completo

**Dev:** "Claude, implementa Funcionalidade 3.2: Sistema de Relatórios do roadmap"

**Agente (Claude Code / Cursor Background):**
```
Lendo contexto...
- ROADMAP.md: Funcionalidade 3.2 descrita
- README.md: Stack Next.js 14 + PostgreSQL, rodar com `npm run dev`
- ARCHITECTURE.md: API em /app/api, componentes em /components

Plano de implementação:

TAREFA 3.2.1: Criar tabela reports (PostgreSQL)
- TDD: ❌ (migration/schema)
- Validação: conexão + query manual

TAREFA 3.2.2: API POST /app/api/reports (criar relatório)
- TDD: ✅ (lógica de negócio)
- Teste: request → validações → salva DB
- Validação: teste + teste manual

TAREFA 3.2.3: API GET /app/api/reports/[id] (buscar relatório)
- TDD: ✅ (query + response)
- Teste: busca → retorna dados corretos
- Validação: teste + teste manual

TAREFA 3.2.4: Componente ReportButton
- TDD: ❌ (UI simples)
- Validação: testar no browser

TAREFA 3.2.5: Integração frontend → backend
- TDD: ⚠️ (teste E2E se tempo permitir)
- Validação: fluxo completo no browser

Posso começar? [Aguardando aprovação]
```

**Dev:** "Aprovado. Pode executar enquanto estou em reunião."

**Agente:** *(trabalha sozinho por 30-60min)*
```
✅ Tarefa 3.2.1 concluída - Migration criada e aplicada
✅ Tarefa 3.2.2 concluída - API POST testada e funcionando
✅ Tarefa 3.2.3 concluída - API GET testada e funcionando
⚠️ Tarefa 3.2.4 - Tentativa 1: erro de import... ajustando
✅ Tarefa 3.2.4 concluída - Componente funcionando
✅ Tarefa 3.2.5 concluída - Integração funcionando

Finalizando...
✅ Suite de testes: 12/12 passando
✅ Aplicação rodando sem erros
✅ Documentação atualizada:
   - README.md (sem mudanças necessárias)
   - ARCHITECTURE.md (novos endpoints documentados)
   - ROADMAP.md (3.2 marcado como completo)
✅ Push realizado: feature/3.2-sistema-relatorios

🎉 Branch pronta! Você pode criar o PR pela interface do GitHub.
📋 O template de PR será aplicado automaticamente.

📋 Comandos de validação (copie e cole):

# Baixar branch
git fetch origin
git checkout feature/3.2-sistema-relatorios

# Ativar ambiente virtual (Windows)
.\venv\Scripts\Activate.ps1

# Rodar testes
npm test

# Rodar aplicação
npm run dev

# Resultados esperados:
# - ✅ 12/12 testes passando
# - ✅ Aplicação rodando em http://localhost:3000
# - ✅ Relatórios sendo criados e listados corretamente
```

**Dev:** *(volta da reunião)*
1. Copia e cola comandos de validação no terminal
2. Testa funcionalidade manualmente
3. Cria PR pela interface do GitHub (template aplicado automaticamente)
4. Aprova merge (ou pede ajustes)

---

## Observações Finais

### Para o Dev
- Sempre valide localmente antes de mergear (use comandos do PR)
- Se algo não estiver claro, pergunte
- Ajuste estas diretrizes conforme o projeto evolui
- **Interrompa o agente se perceber loop** (não deixe rodar infinitamente)

### Para o Agente (Claude Code / Cursor Background)
- Seja autônomo mas transparente
- **PARE após 3 tentativas falhas** - não insista infinitamente
- Comandos de validação local são obrigatórios no PR
- Decisões técnicas devem fazer sentido
- Documentação é tão importante quanto código
- PR deve ser auto-explicativo e permitir validação fácil