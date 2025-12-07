# Análise: Cenário [X] - [Nome do Cenário]

> **Data da Execução:** [A PREENCHER]  
> **Executor:** [A PREENCHER]  
> **Session ID:** [A PREENCHER]

---

## 1. Input Fornecido

```
[Copiar input do epic7_validation_strategy.md ou descrever input real usado]
```

**Input Real Usado:**
```
[Se diferente do esperado, descrever aqui]
```

---

## 2. Comportamento Esperado (Checklist)

### Comportamento Esperado:
- [ ] Critério 1
- [ ] Critério 2
- [ ] Critério 3
- [ ] ...

[Copiar lista completa do epic7_validation_strategy.md]

### Critérios de Sucesso:
- [ ] ✅ Critério de sucesso 1
- [ ] ✅ Critério de sucesso 2
- [ ] ✅ Critério de sucesso 3
- [ ] ...

[Copiar critérios de sucesso do epic7_validation_strategy.md]

---

## 3. Comportamento Observado

### Status:
- [ ] ✅ **Sucesso completo** (todos os critérios atendidos)
- [ ] ⚠️ **Sucesso parcial** (especificar abaixo quais critérios falharam)
- [ ] ❌ **Falha** (especificar abaixo o que não funcionou)

### Detalhes do Comportamento:

<!-- Descrever passo a passo o que aconteceu na prática -->

**Sequência de Eventos:**
1. [Descrever primeiro evento/ação observada]
2. [Descrever segundo evento/ação observada]
3. [Continuar descrevendo...]

**Agentes Chamados:**
- [ ] Orquestrador
- [ ] Estruturador
- [ ] Metodologista
- [ ] Outro: [especificar]

**Transições Observadas:**
- [Descrever transições entre agentes, se houver]

**Output Final ao Usuário:**
```
[Copiar mensagem exibida ao usuário]
```

**Diferenças em Relação ao Esperado:**
- [Listar diferenças encontradas, se houver]

---

## 4. Logs Coletados

### Arquivos Disponíveis:
- [x] **EventBus JSON:** `logs/events.json`
- [ ] **MultiAgentState:** `logs/state.json` (se disponível)
- [x] **Metadata:** `logs/metadata.txt`
- [ ] **Screenshots:** (se houver)

### Resumo dos Logs:

**EventBus - Eventos Registrados:**
- Total de eventos: [número]
- Agentes envolvidos: [lista]
- Tipos de eventos: [lista]

**MultiAgentState - Campos Relevantes:**
- `focal_argument`: [estado observado]
- `hypothesis_versions`: [versões registradas]
- `messages`: [número de mensagens no histórico]
- Outros campos relevantes: [especificar]

**Observações sobre Logs:**
- [Qualquer observação relevante sobre os logs coletados]

---

## 5. Problemas Identificados

### 🔴 Críticos (Bloqueia uso do sistema)

- [ ] **Problema 1:** [Descrição clara e específica]
  - **Onde ocorreu:** [contexto/especificar]
  - **Como reproduzir:** [passos para reproduzir]
  - **Impacto:** [descrição do impacto]

- [ ] **Problema 2:** [Descrição clara e específica]
  - **Onde ocorreu:** [contexto/especificar]
  - **Como reproduzir:** [passos para reproduzir]
  - **Impacto:** [descrição do impacto]

### 🟡 Médios (Degrada experiência mas não bloqueia)

- [ ] **Problema 3:** [Descrição clara e específica]
  - **Onde ocorreu:** [contexto/especificar]
  - **Como reproduzir:** [passos para reproduzir]
  - **Impacto:** [descrição do impacto]

- [ ] **Problema 4:** [Descrição clara e específica]
  - **Onde ocorreu:** [contexto/especificar]
  - **Como reproduzir:** [passos para reproduzir]
  - **Impacto:** [descrição do impacto]

### 🟢 Baixos (Melhorias desejáveis)

- [ ] **Problema 5:** [Descrição clara e específica]
  - **Sugestão de melhoria:** [descrição]

- [ ] **Problema 6:** [Descrição clara e específica]
  - **Sugestão de melhoria:** [descrição]

**Nenhum problema identificado:** [Marcar se não houver problemas]

---

## 6. Observações Adicionais

<!-- Qualquer observação relevante que não se encaixa nas seções acima -->

### Pontos Positivos:
- [Listar aspectos que funcionaram bem]

### Pontos de Atenção:
- [Listar aspectos que merecem atenção, mesmo que não sejam problemas]

### Comportamentos Inesperados:
- [Listar comportamentos que não estavam no comportamento esperado, mas não são necessariamente problemas]

### Sugestões de Melhoria:
- [Sugestões gerais de melhoria para este cenário]

---

## 7. Recomendações

### Correções Prioritárias (Críticas):
1. **Problema [X]:** [Descrição da correção necessária]
   - **Prioridade:** Crítica
   - **Esforço estimado:** [baixo/médio/alto]
   - **Sugestão de implementação:** [breve descrição]

2. **Problema [Y]:** [Descrição da correção necessária]
   - **Prioridade:** Crítica
   - **Esforço estimado:** [baixo/médio/alto]
   - **Sugestão de implementação:** [breve descrição]

### Melhorias Recomendadas (Médias):
1. **Problema [Z]:** [Descrição da melhoria]
   - **Prioridade:** Média
   - **Esforço estimado:** [baixo/médio/alto]
   - **Sugestão de implementação:** [breve descrição]

### Backlog (Baixas):
- [Listar melhorias de baixa prioridade]

---

## 8. Conclusão

### Resumo Executivo:
<!-- Breve resumo (2-3 linhas) do resultado geral do cenário -->

**Status Final:** [✅ Sucesso / ⚠️ Parcial / ❌ Falha]

**Próximos Passos:**
- [ ] [Ação 1]
- [ ] [Ação 2]
- [ ] [Ação 3]

---

**Instruções de Uso:**
1. Copie este template para `docs/testing/epic7_results/{cenario}/analysis.md`
2. Preencha após executar o cenário e coletar logs usando `collect_scenario_logs.py`
3. Seja específico ao descrever problemas (reprodução clara)
4. Priorize problemas por severidade (crítico > médio > baixo)
5. Use checkboxes (- [ ]) para marcar itens completos
6. Adicione screenshots ou logs adicionais em `logs/` se necessário

**Referência:** [Estratégia de Validação do Épico 7](../epic7_validation_strategy.md)

