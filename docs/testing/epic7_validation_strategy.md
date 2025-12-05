# ÉPICO 7: Validação de Maturidade do Sistema - Fase Manual

> **Objetivo:** Validar que sistema multi-agente funciona como deveria através de roteiro de cenários críticos executados manualmente.

---

## 📋 Visão Geral

**Problema:**
- Código está implementado (transições, tools, reasoning loop, memória, modelo cognitivo)
- **MAS** não sabemos se está funcionando como deveria na prática

**Solução:**
- Criar roteiro estruturado com 10-15 cenários críticos
- Executar cenários manualmente
- Coletar logs estruturados (EventBus + MultiAgentState)
- Analisar logs e gerar relatório de maturidade

**Resultado Esperado:**
- Confiança de que sistema funciona bem OU
- Lista priorizada de problemas reais a corrigir

---

## 🎯 O Que Validar

### 1. Transições Entre Agentes
**Validar:**
- Orquestrador decide corretamente quando chamar Estruturador/Metodologista
- Router retorna próximo agente correto baseado em `next_step` e `agent_suggestion`
- Transições são automáticas (não pedem permissão)
- Sistema anuncia ação mas não pergunta "Posso chamar X?"

**Cenários:**
- Usuário começa vago → Orquestrador explora → Estruturador organiza
- Usuário fornece hipótese completa → Orquestrador chama Metodologista diretamente
- Metodologista sugere refinamento → Estruturador refina → Volta para Orquestrador

---

### 2. Preservação de Contexto
**Validar:**
- `focal_argument` é atualizado a cada turno pelo Orquestrador
- `messages` preserva histórico completo
- `hypothesis_versions` registra versões refinadas (V1, V2, V3)
- Contexto não se perde entre transições de agentes

**Cenários:**
- Conversa de 5+ turnos → verificar se focal_argument evolui
- Refinamento de hipótese → verificar se versões são registradas
- Mudança de direção → verificar se focal_argument é resetado

---

### 3. Decisões Coerentes
**Validar:**
- Orquestrador classifica contexto corretamente (`next_step`)
- Estruturador organiza ideias de forma coerente
- Metodologista valida com critérios científicos (não arbitrário)
- Decisões têm justificativas claras

**Cenários:**
- Input vago → Orquestrador explora (não estrutura automaticamente)
- Input completo → Orquestrador chama Metodologista (não pede mais contexto)
- Hipótese com gaps → Metodologista sugere refinamento (não rejeita)

---

### 4. Fluidez Conversacional
**Validar:**
- Sistema não pede permissão ("Posso chamar X?")
- Sistema anuncia ação de forma natural
- Transições são fluidas (sem quebras)
- Bastidores mostram raciocínio (transparência)

**Cenários:**
- Transição automática → verificar mensagem ao usuário
- Sistema chama agente → verificar EventBus (agent_started/completed)
- Bastidores → verificar se mostram reasoning

---

### 5. Provocação Socrática
**Validar:**
- Orquestrador identifica assumptions implícitas
- `reflection_prompt` é gerado quando relevante
- Provocação expõe lacunas (não coleta burocrática)
- 5 categorias de assumptions detectadas (métrica vaga, população vaga, baseline ausente, causalidade assumida, generalização excessiva)

**Cenários:**
- Usuário menciona "produtividade" → Sistema provoca sobre COMO medir
- Usuário menciona "equipes" → Sistema provoca sobre QUAL população
- Usuário assume causalidade → Sistema provoca sobre baseline/controle

---

### 6. Reasoning Loop
**Validar:**
- Metodologista faz perguntas quando precisa clarificação
- Loop funciona (analyze → ask_clarification → analyze)
- Limite de iterações é respeitado (`max_iterations`)
- Sistema decide quando tem contexto suficiente

**Cenários:**
- Hipótese vaga → Metodologista pede clarificação → Loop continua
- Clarificação fornecida → Metodologista decide (não fica em loop infinito)
- Limite atingido → Sistema decide com contexto disponível

---

## 📊 Roteiro de Cenários Críticos

### CENÁRIO 1: Usuário Começa Vago → Sistema Estrutura

**Input:** "Observei que LLMs aumentam produtividade"

**Comportamento Esperado:**
- [ ] Orquestrador classifica como vago (`next_step: "explore"`)
- [ ] Sistema pergunta contexto (não estrutura automaticamente)
- [ ] Após usuário responder, Orquestrador chama Estruturador (`next_step: "suggest_agent"`)
- [ ] Estruturador cria V1 com claim correto
- [ ] `focal_argument` é atualizado (intent, subject, population, metrics)

**Logs Necessários:**
- EventBus: `agent_started` (orchestrator), `agent_completed` (orchestrator)
- EventBus: `agent_started` (structurer), `agent_completed` (structurer)
- MultiAgentState: `focal_argument`, `hypothesis_versions`, `messages`
- Output final: mensagem do sistema ao usuário

**Critérios de Sucesso:**
- ✅ Orquestrador explora (não estrutura automaticamente)
- ✅ Estruturador é chamado automaticamente (sem pedir permissão)
- ✅ Contexto preservado (focal_argument atualizado)
- ✅ Mensagem ao usuário é fluida (não burocrática)

---

### CENÁRIO 2: Usuário Fornece Hipótese Completa

**Input:** "Claude Code reduz tempo de sprint em 30% em equipes de 2-5 devs"

**Comportamento Esperado:**
- [ ] Orquestrador reconhece contexto completo (`next_step: "suggest_agent"`)
- [ ] Sistema chama Metodologista diretamente (não pede mais contexto)
- [ ] Metodologista valida hipótese (approved/needs_refinement/rejected)
- [ ] Sistema apresenta feedback de forma fluida

**Logs Necessários:**
- EventBus: `agent_started` (orchestrator), `agent_completed` (orchestrator)
- EventBus: `agent_started` (methodologist), `agent_completed` (methodologist)
- MultiAgentState: `focal_argument`, `methodologist_output`
- Output final: mensagem do sistema ao usuário

**Critérios de Sucesso:**
- ✅ Orquestrador não explora (contexto já completo)
- ✅ Metodologista é chamado automaticamente
- ✅ Validação usa critérios científicos (não arbitrária)
- ✅ Feedback é apresentado de forma fluida

---

### CENÁRIO 3: Metodologista Sugere Refinamento

**Input:** "Método X melhora desenvolvimento" (vago)

**Comportamento Esperado:**
- [ ] Orquestrador chama Estruturador (V1)
- [ ] Estruturador cria V1 com claim
- [ ] Orquestrador chama Metodologista
- [ ] Metodologista retorna `needs_refinement` com gaps específicos
- [ ] Sistema apresenta feedback ao usuário (não refina automaticamente)
- [ ] Usuário decide refinar ou não
- [ ] Se usuário refinir → Estruturador cria V2

**Logs Necessários:**
- EventBus: sequência completa de agentes
- MultiAgentState: `hypothesis_versions` (V1, V2)
- MethodologistState: `status: "needs_refinement"`, `improvements`

**Critérios de Sucesso:**
- ✅ Sistema não refina automaticamente (aguarda decisão do usuário)
- ✅ Feedback do Metodologista tem gaps específicos
- ✅ Estruturador cria V2 quando usuário decide refinar
- ✅ Versões são registradas (V1 → V2)

---

### CENÁRIO 4: Provocação Socrática - Métrica Vaga

**Input:** "Quero medir produtividade de desenvolvedores"

**Comportamento Esperado:**
- [ ] Orquestrador detecta métrica vaga
- [ ] Sistema gera `reflection_prompt` provocando sobre COMO medir
- [ ] Provocação expõe assumptions (não coleta burocrática)
- [ ] Exemplo: "Produtividade de QUÊ? Linhas de código? Velocidade de entrega? Qualidade?"

**Logs Necessários:**
- MultiAgentState: `reflection_prompt`
- Output: mensagem provocativa ao usuário

**Critérios de Sucesso:**
- ✅ Sistema identifica métrica vaga
- ✅ Provocação expõe assumptions (não pergunta burocrática)
- ✅ Mensagem é socrática (contra-pergunta, não coleta)

---

### CENÁRIO 5: Mudança de Direção

**Input inicial:** "Quero testar hipótese sobre LLMs"
**Input depois:** "Na verdade, quero fazer revisão de literatura"

**Comportamento Esperado:**
- [ ] Sistema aceita mudança sem questionar
- [ ] `focal_argument` é resetado (intent muda de "test_hypothesis" para "review_literature")
- [ ] Sistema adapta fluxo imediatamente
- [ ] Contexto anterior não prende usuário

**Logs Necessários:**
- MultiAgentState: `focal_argument` (antes e depois)
- Output: mensagem de adaptação ao usuário

**Critérios de Sucesso:**
- ✅ Sistema aceita mudança sem questionar
- ✅ `focal_argument` é atualizado
- ✅ Fluxo se adapta imediatamente
- ✅ Mensagem é natural (não reclama)

---

### CENÁRIO 6: Reasoning Loop do Metodologista

**Input:** Hipótese vaga que requer clarificação

**Comportamento Esperado:**
- [ ] Metodologista entra em modo `analyze`
- [ ] Detecta que precisa clarificação (`needs_clarification: True`)
- [ ] Router envia para `ask_clarification`
- [ ] Tool `ask_user` é chamada (faz pergunta ao usuário)
- [ ] Usuário responde
- [ ] Loop volta para `analyze` com nova informação
- [ ] Processo se repete até ter contexto suficiente OU atingir limite (`max_iterations`)
- [ ] Metodologista decide quando tem contexto suficiente

**Logs Necessários:**
- MethodologistState: `needs_clarification`, `iterations`, `max_iterations`
- EventBus: `agent_started` (methodologist - múltiplas vezes)
- Messages: perguntas e respostas do loop

**Critérios de Sucesso:**
- ✅ Loop funciona (analyze → ask → analyze)
- ✅ Sistema não fica em loop infinito (respeita limite)
- ✅ Perguntas são específicas (não genéricas)
- ✅ Sistema decide quando tem contexto suficiente

---

### CENÁRIO 7: Preservação de Contexto em Conversa Longa

**Input:** 5+ turnos de conversa explorando diferentes aspectos

**Comportamento Esperado:**
- [ ] `focal_argument` evolui a cada turno
- [ ] `messages` preserva histórico completo
- [ ] Contexto não se perde (agentes têm acesso ao histórico)
- [ ] Sistema referencia informações de turnos anteriores

**Logs Necessários:**
- MultiAgentState: `focal_argument` (evolução ao longo dos turnos)
- MultiAgentState: `messages` (histórico completo)
- Output: mensagens que referenciam turnos anteriores

**Critérios de Sucesso:**
- ✅ `focal_argument` evolui (não fica estático)
- ✅ Histórico é preservado
- ✅ Sistema referencia informações anteriores
- ✅ Contexto não se perde

---

### CENÁRIO 8: Transição Fluida (Sem "Posso Chamar X?")

**Input:** Contexto suficiente para chamar Estruturador

**Comportamento Esperado:**
- [ ] Sistema anuncia ação: "Vou organizar isso em uma questão de pesquisa"
- [ ] Sistema NÃO pergunta: "Posso chamar o Estruturador?"
- [ ] Transição é automática
- [ ] Bastidores mostram qual agente está trabalhando

**Logs Necessários:**
- Output: mensagem de anúncio ao usuário
- EventBus: `agent_started` (structurer)
- Bastidores: reasoning do Estruturador

**Critérios de Sucesso:**
- ✅ Sistema anuncia (não pede permissão)
- ✅ Mensagem é natural e fluida
- ✅ Transição é automática
- ✅ Bastidores mostram transparência

---

### CENÁRIO 9: Validação Científica com Critérios

**Input:** Hipótese estruturada mas com gaps metodológicos

**Comportamento Esperado:**
- [ ] Metodologista valida usando 4 critérios (testabilidade, falseabilidade, especificidade, operacionalização)
- [ ] Retorna `needs_refinement` com gaps específicos
- [ ] Justificativa cita critérios aplicados
- [ ] Sugestões são concretas (não genéricas)

**Logs Necessários:**
- MethodologistState: `status`, `justification`, `improvements`
- Output: feedback estruturado ao usuário

**Critérios de Sucesso:**
- ✅ Validação usa critérios científicos (não arbitrária)
- ✅ Gaps são específicos (não genéricos)
- ✅ Sugestões são concretas e acionáveis
- ✅ Justificativa é clara

---

### CENÁRIO 10: Bastidores Mostra Reasoning

**Input:** Qualquer interação que chame agentes

**Comportamento Esperado:**
- [ ] Painel "Bastidores" mostra qual agente está trabalhando
- [ ] Reasoning do agente é exibido (card de pensamento)
- [ ] Eventos aparecem em timeline
- [ ] Métricas são exibidas (tokens, custo, duração)

**Logs Necessários:**
- EventBus: eventos de agentes
- Interface: painel Bastidores (screenshot ou descrição)

**Critérios de Sucesso:**
- ✅ Bastidores mostra agentes ativos
- ✅ Reasoning é exibido de forma clara
- ✅ Timeline mostra sequência de eventos
- ✅ Métricas são precisas

---

## 📝 Template de Coleta de Logs

Para cada cenário, colete:

### 1. EventBus (JSON)
```json
{
  "session_id": "test-scenario-1",
  "events": [
    {
      "type": "agent_started",
      "agent_name": "orchestrator",
      "timestamp": "2025-12-04T10:00:00Z"
    },
    {
      "type": "agent_completed",
      "agent_name": "orchestrator",
      "summary": "Classificou como vago, pediu mais contexto",
      "tokens_input": 100,
      "tokens_output": 50,
      "tokens_total": 150,
      "cost": 0.0012,
      "duration": 1.2
    }
  ]
}
```

### 2. MultiAgentState (Campos Relevantes)
```python
{
  "focal_argument": {
    "intent": "test_hypothesis",
    "subject": "LLMs impact on productivity",
    "population": "not specified",
    "metrics": "not specified",
    "article_type": "empirical"
  },
  "hypothesis_versions": [
    {"version": "V1", "hypothesis": "..."}
  ],
  "messages": [...]  # Histórico completo
}
```

### 3. Output Final
Mensagem exibida ao usuário:
"Interessante! Me conta mais: você quer VER o que já existe sobre isso, ou quer TESTAR uma hipótese sua?"

### 4. Observações
- Comportamento esperado foi atingido? (Sim/Não/Parcial)
- Problemas identificados? (Crítico/Médio/Baixo)
- Notas adicionais

---

## 📊 Template de Relatório de Maturidade

Após executar todos os cenários, gerar relatório estruturado:

### 1. Sumário Executivo
- Sistema está maduro? (Sim/Não/Parcial)
- Resumo de problemas críticos encontrados
- Recomendações principais

### 2. Resultados por Categoria

#### Transições Entre Agentes
- ✅ Funciona bem: [listar o que funciona]
- ❌ Problemas encontrados: [listar problemas]
- Cenários testados: [lista]

#### Preservação de Contexto
- ✅ Funciona bem: [listar o que funciona]
- ❌ Problemas encontrados: [listar problemas]
- Cenários testados: [lista]

#### Decisões Coerentes
- ✅ Funciona bem: [listar o que funciona]
- ❌ Problemas encontrados: [listar problemas]
- Cenários testados: [lista]

#### Fluidez Conversacional
- ✅ Funciona bem: [listar o que funciona]
- ❌ Problemas encontrados: [listar problemas]
- Cenários testados: [lista]

#### Provocação Socrática
- ✅ Funciona bem: [listar o que funciona]
- ❌ Problemas encontrados: [listar problemas]
- Cenários testados: [lista]

#### Reasoning Loop
- ✅ Funciona bem: [listar o que funciona]
- ❌ Problemas encontrados: [listar problemas]
- Cenários testados: [lista]

### 3. Classificação de Problemas

#### Problemas Críticos (Bloqueia uso)
- [ ] Problema 1: Descrição + Cenário onde ocorreu
- [ ] Problema 2: ...

#### Problemas Médios (Degrada experiência)
- [ ] Problema 3: Descrição + Cenário onde ocorreu
- [ ] Problema 4: ...

#### Problemas Baixos (Melhorias)
- [ ] Problema 5: Descrição + Cenário onde ocorreu
- [ ] Problema 6: ...

### 4. Recomendações

#### Correções Prioritárias
1. **Problema Crítico 1**: Descrição da correção necessária
2. **Problema Crítico 2**: ...

#### Melhorias Recomendadas
1. **Problema Médio 1**: Descrição da melhoria
2. **Problema Médio 2**: ...

#### Backlog
- Problema Baixo 1
- Problema Baixo 2

### 5. Próximos Passos

- [ ] Corrigir problemas críticos identificados
- [ ] Implementar Épico 8 (Automação) para prevenir regressões
- [ ] Ou: Sistema maduro, seguir para próximo épico

---

## 🎯 Critérios de Aceite do Épico 7

### 7.1 Roteiro Criado
- [ ] Arquivo `docs/testing/epic7_validation_strategy.md` criado
- [ ] 10-15 cenários críticos definidos
- [ ] Cada cenário especifica: input, comportamento esperado, logs necessários, critérios de sucesso
- [ ] Template de coleta de logs definido
- [ ] Template de relatório de maturidade definido

### 7.2 Cenários Executados
- [ ] Todos os cenários foram executados no sistema real
- [ ] Logs estruturados foram coletados (EventBus + MultiAgentState)
- [ ] Comportamento observado foi anotado (sucesso/falha/parcial)
- [ ] Problemas foram classificados (crítico/médio/baixo)

### 7.3 Relatório Gerado
- [ ] Relatório de maturidade completo
- [ ] Sumário executivo (sistema maduro? O que falta?)
- [ ] Resultados por categoria (6 categorias)
- [ ] Problemas classificados e priorizados
- [ ] Recomendações de correções
- [ ] Próximos passos definidos

---

**Versão:** 1.0  
**Data:** Dezembro 2025  
**Relacionado:** ÉPICO 7 no ROADMAP

