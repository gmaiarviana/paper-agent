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
- PR criado e pronto para review

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
- ✅ Aplicação rodando sem erros
- ✅ Comportamento esperado funcionando
- ✅ Documentação da tarefa atualizada (incremental)

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

### 4. FINALIZAÇÃO: PR PRONTO + COMANDOS PARA VALIDAÇÃO LOCAL

Quando todas tarefas concluídas:

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
- [ ] PR criado com descrição clara
- [ ] **Comandos de validação local fornecidos**

#### Template de PR
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
```bash
# Buscar branch remota
git fetch origin

# Criar branch local a partir da remota
git checkout -b feature/X.Y-nome-funcionalidade origin/feature/X.Y-nome-funcionalidade

# Instalar dependências (se houver mudanças)
[comando específico: npm install, composer install, etc]
```

**2. Rodar aplicação:**
```bash
[comandos específicos baseados no README.md]
# Exemplo: docker-compose up -d
# Exemplo: npm run dev
# Exemplo: python manage.py runserver
```

**3. Rodar testes:**
```bash
[comando específico de testes]
# Exemplo: npm test
# Exemplo: pytest
# Exemplo: php artisan test
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
```bash
# Parar aplicação
[comando específico: docker-compose down, Ctrl+C, etc]

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
- **Status de épicos**: Vive APENAS no ROADMAP.md (não duplicar no README)
- **Estrutura do projeto**: Vive APENAS no ARCHITECTURE.md (não duplicar no README)
- **README.md**: Foco em "Getting Started" - setup rápido e referências
- **ARCHITECTURE.md**: Foco em estrutura técnica, decisões arquiteturais, organização de código

### Comandos e Validação
- **PowerShell como padrão**: Dev usa Windows, sempre fornecer comandos em PowerShell
- **Validação antes de merge**: SEMPRE fornecer comandos + resultados esperados
- **Template de validação**:
  ```powershell
  # 1. Trocar de branch
  git fetch origin
  git checkout <branch-name>

  # 2. Instalar/atualizar dependências
  <comando específico>

  # 3. Testar funcionalidade
  <comandos de validação>

  # Resultados esperados:
  # - <item 1>
  # - <item 2>
  ```

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

PR criado: feature/3.2-sistema-relatorios
👉 Review: http://github.com/repo/pull/42

📋 Comandos para validação local estão no PR
```

**Dev:** *(volta da reunião)*
1. Lê PR
2. Executa comandos fornecidos para baixar branch
3. Roda aplicação localmente
4. Testa funcionalidade manualmente
5. Aprova merge (ou pede ajustes)

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