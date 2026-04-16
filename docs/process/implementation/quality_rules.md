# Regras de Qualidade

## Princípios Gerais

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

---

## Diretrizes Aprendidas em Produção

### Sistemas Conversacionais com LLMs

**Debug estruturado > Testes unitários:**
- SEMPRE crie ferramentas de observabilidade (logs detalhados, rastreamento de decisões) ANTES de escrever testes
- Testes unitários não capturam bugs de fluxo multi-turn
- Ferramentas de debug revelam causa raiz em minutos vs horas

**Orientação > Prescrição em prompts:**
- Prompts com 50+ linhas de regras IF-THEN transformam LLM em script
- PREFIRA: código robusto (tolera variações) + prompt minimalista (1-3 parágrafos)
- EVITE: regras rígidas que eliminam autonomia do LLM
- Para sistemas inteligentes: flexibilidade > determinismo

**Preservação de contexto:**
- Reconheça variações naturais do LLM (`"not operationalized"`, `"undefined"`) como valores vagos
- Não dependa apenas do LLM retornar valores padronizados
- Código deve ser resiliente a variações linguísticas

### Validação e Testes

**Validação incremental:**
- Commits separados (infraestrutura → fix parcial → fix completo) aceleram debug
- Facilita rollback e análise histórica
- Cada commit deve ter descrição clara do que resolve

**Cenários de teste:**
- Escreva cenários baseados em hipótese inicial
- Execute e observe comportamento REAL do sistema
- Ajuste cenários OU sistema conforme necessário
- Não tenha medo de ajustar cenários se comportamento real for razoável

### Arquitetura e Design

**Visão do produto define solução técnica:**
- SEMPRE pergunte: "Essa solução está alinhada com a visão do produto?" ANTES de implementar
- Soluções tecnicamente corretas podem conflitar com experiência desejada
- Exemplo: Regras rígidas vs "facilitador inteligente"

**Quando evitar automação completa:**
- Para análise de qualidade conversacional, humano + LLM > automação
- Automação completa perde contexto e qualidade de insights
- PREFIRA: ferramentas que estruturam dados para análise, não que tomam decisões

---

## Regras Anti-Redundância

**Responsabilidade Única de Cada Documento:**

| Documento | Responsabilidade | O que NÃO deve conter |
|-----------|-----------------|----------------------|
| **README.md** | Getting Started: setup inicial, comandos de validação gerais, referências para docs | ❌ Status de épicos/tasks<br>❌ Estrutura detalhada do projeto<br>❌ Decisões arquiteturais<br>❌ Comandos de validação específicos por task |
| **ROADMAP.md** | Status de épicos/tasks, critérios de aceite | ❌ Instruções de setup geral<br>❌ Arquitetura técnica<br>❌ Comandos de validação (validação é durante sessão de trabalho) |
| **ARCHITECTURE.md** | Estrutura técnica, decisões arquiteturais, organização de código, stack | ❌ Status de implementação<br>❌ Instruções de setup<br>❌ Comandos de validação |
| **docs/process/implementation/** | Processo de trabalho com agentes, regras de qualidade, templates de validação | ❌ Funcionalidades específicas<br>❌ Detalhes de implementação |
| **.github/PULL_REQUEST_TEMPLATE.md** | Template para PRs, preenchido automaticamente pelo GitHub | ❌ Conteúdo específico de tasks<br>❌ Apenas estrutura/template |

**Regras de Ouro:**
- ✅ **Status de funcionalidades**: Vive APENAS no ROADMAP.md
- ✅ **Estrutura do projeto**: Vive APENAS no ARCHITECTURE.md
- ✅ **Setup e comandos gerais**: Vive APENAS no README.md
- ✅ **Validação de funcionalidades**: Acontece durante a sessão de trabalho via scripts (`scripts/**/validate_*.py`)
- ❌ **NUNCA duplicar informações** entre documentos - sempre referenciar
- ❌ **NUNCA adicionar histórico de validação no ROADMAP** - validação é feita durante implementação

---

## Comandos e Validação

- **PowerShell como padrão**: Dev usa Windows, sempre fornecer comandos em PowerShell
- **Validação durante implementação**: Criar scripts de validação (`scripts/**/validate_*.py`) e executar durante a sessão
- **Validação no PR**: Fornecer comandos de validação na mensagem final ao dev (não no ROADMAP)
- **Checkout de branch obrigatório**: Sempre incluir passos de fetch/checkout nas instruções de validação

**Template de validação (para mensagem final ao dev):**
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
python scripts/<categoria>/validate_*.py

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
- ❌ **NÃO salvar comandos de validação no ROADMAP.md** - fornecer apenas na mensagem final ao dev

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

## Verificação de Conflitos e Prevenção de Perda de Trabalho

### 🚨 Problema Identificado: Sobrescrição de Trabalho

**Cenário:**
- Trabalho em múltiplas frentes (ex: Épico 9 + Funcionalidade 8.1)
- Branch local atrás do origin/main
- Mudanças locais sobrescrevem conteúdo importante de commits anteriores

**Causa Raiz:**
- Edição direta do ROADMAP.md sem verificar commits recentes do origin/main
- Falta de processo de verificação antes de editar arquivos críticos
- Git status não mostra conflitos até tentar push/merge

### ✅ Processo de Verificação Obrigatório

**ANTES de editar arquivos críticos (ROADMAP.md, ARCHITECTURE.md, README.md):**

1. **Verificar status do repositório:**
   ```powershell
   git fetch origin
   git status
   git log --oneline HEAD..origin/main
   ```

2. **Se branch local está atrás:**
   ```powershell
   # Ver diferenças em arquivos críticos
   git diff HEAD origin/main -- ROADMAP.md
   git diff HEAD origin/main -- ARCHITECTURE.md
   git diff HEAD origin/main -- README.md
   ```

3. **Se houver mudanças locais não commitadas:**
   ```powershell
   # Ver o que foi modificado localmente
   git diff -- ROADMAP.md
   git diff -- ARCHITECTURE.md
   ```

4. **Decisão:**
   - **Se origin/main tem conteúdo importante que local não tem:**
     - Fazer merge/rebase ANTES de editar
     - OU criar branch separada para cada frente de trabalho
   - **Se local tem mudanças importantes:**
     - Commitar local primeiro
     - Depois fazer merge/rebase
     - Resolver conflitos preservando ambas as mudanças

### 📋 Checklist Antes de Editar ROADMAP.md

- [ ] `git fetch origin` executado
- [ ] `git status` verificado (branch atrás? mudanças locais?)
- [ ] `git log HEAD..origin/main` revisado (commits importantes?)
- [ ] `git diff HEAD origin/main -- ROADMAP.md` revisado (conteúdo perdido?)
- [ ] Se houver conteúdo importante em origin/main: merge/rebase ANTES de editar
- [ ] Se houver mudanças locais: commitar ANTES de merge/rebase

### 🔍 Verificação de Arquivos Modificados

**Quando há múltiplas frentes de trabalho:**

1. **Listar arquivos modificados:**
   ```powershell
   git status --short
   ```

2. **Para cada arquivo modificado, verificar:**
   ```powershell
   # Ver diferenças locais
   git diff -- <arquivo>
   
   # Ver diferenças com origin/main
   git diff HEAD origin/main -- <arquivo>
   
   # Ver histórico de commits recentes
   git log --oneline -5 -- <arquivo>
   ```

3. **Identificar conflitos potenciais:**
   - Arquivo modificado localmente E em origin/main?
   - Mesmas seções editadas em ambos?
   - Conteúdo complementar ou conflitante?

### 🛡️ Prevenção de Perda de Trabalho

**Estratégias:**

1. **Commits frequentes:**
   - Commitar trabalho parcial antes de mudar de frente
   - Mensagens descritivas: "Épico 9.1: cognitive_model no orchestrator"

2. **Branches separadas:**
   - Uma branch por frente de trabalho
   - Merge apenas quando trabalho estiver completo

3. **Verificação antes de push:**
   ```powershell
   # Sempre verificar antes de push
   git fetch origin
   git log --oneline HEAD..origin/main
   git diff HEAD origin/main -- <arquivos-críticos>
   ```

4. **Documentação de decisões:**
   - Se conteúdo foi removido intencionalmente, documentar por quê
   - Se conteúdo foi perdido acidentalmente, restaurar imediatamente

### 📝 Template de Verificação (Copiar antes de editar ROADMAP.md)

```powershell
# 1. Verificar status
git fetch origin
git status

# 2. Ver commits recentes no origin/main
git log --oneline -10 origin/main

# 3. Ver diferenças em ROADMAP.md
git diff HEAD origin/main -- ROADMAP.md | Select-Object -First 200

# 4. Ver mudanças locais
git diff -- ROADMAP.md | Select-Object -First 200

# 5. Se necessário, ver commits específicos
git show <commit-hash>:ROADMAP.md | Select-Object -First 100
```

### ⚠️ Sinais de Alerta

**Pare e verifique se:**
- Git status mostra "Your branch is behind 'origin/main' by X commits"
- Você está trabalhando em múltiplas frentes simultaneamente
- Arquivo crítico foi editado recentemente (últimos commits)
- Você não tem certeza se mudanças locais conflitam com origin/main

**Ação imediata:**
1. Parar edições
2. Executar checklist de verificação
3. Resolver conflitos antes de continuar

---

## Observações Finais

### Para o Dev
- Sempre valide localmente antes de mergear (use comandos do PR)
- Se algo não estiver claro, pergunte
- Ajuste estas diretrizes conforme o projeto evolui
- **Interrompa o agente se perceber loop** (não deixe rodar infinitamente)
- **SEMPRE verificar conflitos antes de editar arquivos críticos**

### Para o Agente (Claude Code / Cursor Background)
- Seja autônomo mas transparente
- **PARE após 3 tentativas falhas** - não insista infinitamente
- Comandos de validação local são obrigatórios no PR
- Decisões técnicas devem fazer sentido
- Documentação é tão importante quanto código
- PR deve ser auto-explicativo e permitir validação fácil
- **ANTES de editar ROADMAP.md/ARCHITECTURE.md: verificar conflitos com origin/main**

---

**Ver também:**
- Para entender o papel do agente → [overview.md](overview.md)
- Para implementação detalhada → [implementation.md](implementation.md)
- Para finalização e entrega → [delivery.md](delivery.md)
