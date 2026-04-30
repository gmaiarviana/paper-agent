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

## Regras Anti-Redundância

**Responsabilidade Única de Cada Documento:**

| Documento | Responsabilidade | O que NÃO deve conter |
|-----------|-----------------|----------------------|
| **README.md** | Getting Started: setup inicial, comandos de validação gerais, referências para docs | ❌ Status de épicos/tasks<br>❌ Estrutura detalhada do projeto<br>❌ Decisões arquiteturais<br>❌ Comandos de validação específicos por task |
| **ROADMAP.md** | Status de épicos/tasks, critérios de aceite | ❌ Instruções de setup geral<br>❌ Arquitetura técnica<br>❌ Comandos de validação (validação é durante sessão de trabalho) |
| **docs/ARCHITECTURE.md** | Estrutura técnica, decisões arquiteturais, organização de código, stack | ❌ Status de implementação<br>❌ Instruções de setup<br>❌ Comandos de validação |
| **docs/process/implementation/** | Processo de trabalho com agentes, regras de qualidade, templates de validação | ❌ Funcionalidades específicas<br>❌ Detalhes de implementação |
| **.github/PULL_REQUEST_TEMPLATE.md** | Template para PRs, preenchido automaticamente pelo GitHub | ❌ Conteúdo específico de tasks<br>❌ Apenas estrutura/template |

**Regras de Ouro:**
- ✅ **Status de funcionalidades**: Vive APENAS no ROADMAP.md
- ✅ **Estrutura do projeto**: Vive APENAS no docs/ARCHITECTURE.md
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

### Template de validação local

> **Fonte canônica.** Outros docs (`docs/process/implementation/delivery.md`,
> `docs/process/autonomous/delivery.md`, `docs/process/implementation/overview.md`)
> referenciam este bloco via `quality_rules.md#template-de-validação-local` em
> vez de duplicar o conteúdo.

```bash
# 0. Fazer checkout da branch (SEMPRE incluir este passo)
git fetch origin
git checkout <branch-name>

# 1. Ativar ambiente virtual (se aplicável)
source .venv/bin/activate              # Linux/Mac
# .\.venv\Scripts\Activate.ps1         # Windows

# 2. Instalar/atualizar dependências (se requirements mudaram)
pip install -r requirements.txt

# 3. Testes unitários
python -m pytest tests/core/unit/ -v

# 4. Validação manual (script - RECOMENDADO!)
python scripts/core/<categoria>/validate_*.py

# 5. (se a branch mexeu em produto) Subir a app
# Stack detectada via products/<produto>/app/ — ver
# .github/copilot-instructions.md §"Stacks por produto" (W-PROTO-14)
```

**Observações:**
- Passo 0 (checkout) é OBRIGATÓRIO - dev precisa baixar a branch para validar
- Passo 1 (venv/ambiente) só se projeto usar ambientes virtuais/isolados; o nome canônico é `.venv/` (ponto), alinhado com `.github/copilot-instructions.md`
- Passo 2 (dependências) só na primeira vez ou se requirements mudaram
- Passo 4 (script de validação) é ALTAMENTE RECOMENDADO - ajuda a entender o módulo
- Passo 5 (subir app) só se a branch tocou produto; a stack vem da tabela em `.github/copilot-instructions.md` (Streamlit / Reflex / etc.) — evita drift quando outros produtos forem adicionados
- ❌ **NÃO usar `PYTHONPATH=...` no Windows** - scripts já adicionam path automaticamente
- ❌ **NÃO salvar comandos de validação no ROADMAP.md** - fornecer apenas na mensagem final ao dev

---

## Exemplo de Fluxo Completo

**Dev:** "Claude, implementa Funcionalidade 3.2: Sistema de Relatórios do roadmap"

**Agente (Claude Code Web):**
```
Lendo contexto...
- ROADMAP.md: Funcionalidade 3.2 descrita
- README.md: Stack Next.js 14 + PostgreSQL, rodar com `npm run dev`
- docs/ARCHITECTURE.md: API em /app/api, componentes em /components

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
   - docs/ARCHITECTURE.md (novos endpoints documentados)
   - ROADMAP.md (3.2 marcado como completo)
✅ Push realizado: milestone/<id-em-caixa-baixa>

🎉 Branch pronta! Você pode criar o PR pela interface do GitHub.
📋 O template de PR será aplicado automaticamente.

📋 Comandos de validação (copie e cole):

# Baixar branch
git fetch origin
git checkout milestone/<id-em-caixa-baixa>

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
- **SEMPRE verificar conflitos antes de editar arquivos críticos**

### Para o Agente (Claude Code Web)
- Seja autônomo mas transparente
- **PARE após 3 tentativas falhas** - não insista infinitamente
- Comandos de validação local são obrigatórios no PR
- Decisões técnicas devem fazer sentido
- Documentação é tão importante quanto código
- PR deve ser auto-explicativo e permitir validação fácil
- **ANTES de editar ROADMAP.md/docs/ARCHITECTURE.md: verificar conflitos com origin/main**

---

**Ver também:**
- Para entender o papel do agente → [overview.md](overview.md)
- Para implementação detalhada → [implementation.md](implementation.md)
- Para finalização e entrega → [delivery.md](delivery.md)
