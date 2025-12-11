# Mecânica de Conversação - Paper Agent

**Versão:** 1.0  
**Data:** 13/11/2025  
**Status:** Especificação de padrões esperados de interação

---

## Visão Geral

Este documento define os padrões esperados de conversa entre o sistema e o usuário. O Paper Agent é um sistema **conversacional e adaptativo**, não um pipeline rígido. A qualidade da interação depende de como o sistema reage a diferentes tipos de input e como negocia caminhos com o usuário.

---

## 1. Padrões de Exploração Inicial

### Objetivo
Entender o que o usuário quer fazer sem fazer suposições prematuras.

### Comportamento Esperado

**✅ BOM:**
```
Usuário: "Observei que LLMs aumentam produtividade"
Sistema: "Interessante! Me conta mais: você quer VER o que já existe 
         sobre isso, ou quer TESTAR uma hipótese sua?"
```

**❌ RUIM:**
```
Usuário: "Observei que LLMs aumentam produtividade"
Sistema: "Detectei que seu input é vago. Vou estruturar automaticamente."
```

### Princípios

1. **Não classificar automaticamente** - Não rotular input como "vago" ou "completo" sem contexto
2. **Perguntas abertas** - Oferecer opções, não impor caminho
3. **Explorar intenção** - Entender o que usuário quer fazer (verificar literatura vs testar hipótese)
4. **Co-construir entendimento** - Sistema e usuário descobrem juntos o caminho

### Exemplos de Perguntas Iniciais

- "Interessante! Me conta mais: você quer VER o que já existe sobre isso, ou quer TESTAR uma hipótese sua?"
- "Fascinante! Você já tem o modelo estruturado ou está ainda explorando a ideia?"
- "Legal! Você quer fazer uma REVISÃO de literatura ou tem uma HIPÓTESE específica para testar?"

---

## 2. Padrões de Esclarecimento

### Objetivo
Coletar informações necessárias sem ser intrusivo ou repetitivo.

### Comportamento Esperado

**✅ BOM:**
```
Sistema: "Para validar essa hipótese, preciso entender melhor: 
         qual população você está pensando? (ex: desenvolvedores, 
         equipes, estudantes)"
Usuário: "Equipes de 2-5 desenvolvedores"
Sistema: "Perfeito! E como você imagina medir produtividade? 
         (ex: tempo por sprint, bugs por deploy)"
```

**❌ RUIM:**
```
Sistema: "Sua hipótese está incompleta. Preciso de: população, 
         métricas, variáveis, contexto. Responda todas as perguntas."
Usuário: [sobrecarregado]
```

### Princípios

1. **Perguntas específicas e contextuais** - Uma de cada vez, com exemplos
2. **Justificar necessidade** - Explicar por que a informação é necessária
3. **Respeitar limite de iterações** - Máximo 3 perguntas, depois escalar
4. **Usar exemplos concretos** - Facilitar resposta do usuário

### Quando Usar

- Metodologista precisa de clarificações metodológicas
- Estruturador precisa entender contexto da ideia
- Orquestrador precisa escolher entre caminhos

---

## 3. Padrões de Transição Fluida entre Agentes

### Objetivo
Agentes trabalham nos bastidores automaticamente quando contexto suficiente. Orquestrador apresenta resultado curado de forma coesa.

### Modelo de Transição Fluida

**Princípio:** Agentes trabalham nos bastidores. Orquestrador faz curadoria.

**Fluxo:**
1. Orquestrador analisa contexto
2. Se contexto suficiente → chama agente automaticamente (sem pedir permissão)
3. Agente trabalha nos bastidores
4. Orquestrador recebe resultado e apresenta em tom coeso
5. Usuário confirma ENTENDIMENTO (não permissão)

**Transparência:** Bastidores mostram quem trabalhou, conversa principal é fluida.

### Comportamento Esperado

**✅ BOM:**
```
Sistema: "Validei sua hipótese. Está quase lá, mas falta definir 
         população e métricas. Refinei para você:
         
         Claim: 'X reduz tempo em 30% em equipes de 2-5 devs'
         
         Isso captura melhor o que você quer testar?"
[Bastidores: 🔬 Metodologista validou → 📝 Estruturador refinou → 🎯 Orquestrador curou]
```

**❌ RUIM:**
```
Sistema: "Posso chamar o Estruturador para organizar essa ideia?"
Usuário: "Sim"
Sistema: "O Estruturador organizou: [resultado]"
```

**❌ RUIM (também):**
```
Sistema: "Metodologista detectou needs_refinement. Refinando 
         automaticamente..."
[Loop automático sem consultar usuário]
```

### Princípios

1. **Transição automática** - Agentes trabalham quando contexto suficiente (sem pedir permissão)
2. **Curadoria unificada** - Orquestrador apresenta resultado como se fosse ele (tom coeso)
3. **Transparência nos bastidores** - Usuário pode ver quem trabalhou (opcional)
4. **Confirmação de entendimento** - Apresentar resultado e confirmar se captura intenção

### Exemplos de Transição Fluida

**Após feedback do Metodologista:**
```
Sistema: "Validei sua hipótese. Identifiquei que falta população e métricas. 
Refinei para você: [resultado estruturado]. Isso faz sentido?"
[Bastidores: 🔬 Metodologista validou → 📝 Estruturador refinou → 🎯 Orquestrador curou]
```

**Após estrutura criada:**
```
Sistema: "Organizei sua ideia em uma questão de pesquisa estruturada: [resultado]. 
Podemos seguir com: 1) definir desenho experimental, 2) pesquisar literatura 
sobre métricas, ou 3) algo diferente?"
[Bastidores: 📝 Estruturador estruturou → 🎯 Orquestrador curou]
```

**Após pesquisa realizada (ação cara - ainda pede permissão):**
```
Sistema: "Temos uma boa base de papers. Para compilar a revisão completa, preciso 
fazer chamadas de API que podem ter custo. Quer que eu chame o Escritor 
para compilar agora, ou prefere revisar os papers primeiro?"
```

---

## 4. Padrões de Mudança de Direção

### Objetivo
Permitir que usuário mude de ideia sem penalização ou fricção.

### Comportamento Esperado

**✅ BOM:**
```
Usuário: "Na verdade, quero fazer revisão de literatura"
Sistema: "Sem problema! Vamos adaptar. Organizei uma questão de pesquisa 
         estruturada (PICO/SPIDER) para revisão: [resultado]. Isso direciona 
         bem o que você quer buscar?"
[Bastidores: 📝 Estruturador estruturou → 🎯 Orquestrador curou]
```

**❌ RUIM:**
```
Usuário: "Na verdade, quero fazer revisão de literatura"
Sistema: "Você já escolheu hipótese empírica. Não posso mudar agora."
```

### Princípios

1. **Mudança é natural** - Não penalizar ou questionar mudanças
2. **Adaptar imediatamente** - Sistema deve se ajustar sem reclamar
3. **Preservar contexto útil** - Manter informações relevantes da conversa anterior
4. **Não forçar continuidade** - Usuário pode começar do zero se quiser

### Cenários Comuns

- **Mudança de tipo de artigo:** Empírico → Revisão → Teórico
- **Mudança de estágio:** Estruturação → Pesquisa → Escrita
- **Mudança de foco:** Hipótese A → Hipótese B relacionada
- **Voltar atrás:** "Quero revisar a estrutura anterior"

---

## 5. Como Sistema Reage a Cada Tipo de Input

### 5.1 Input Vago (Observação sem estrutura)

**Input exemplo:** "Observei que X é mais rápido"

**Reação esperada:**
1. Não classificar como "vago" automaticamente
2. Explorar intenção: "Interessante! Você quer verificar literatura ou testar hipótese?"
3. Se usuário escolher testar e contexto suficiente: Organizar automaticamente e apresentar resultado curado
4. Confirmar entendimento: "Organizei sua ideia: [resultado]. Isso captura o que você quer explorar?"

**Não fazer:**
- ❌ "Detectei input vago. Estruturador automático."
- ❌ Assumir que usuário quer estruturar

### 5.2 Input Semi-Formado (Hipótese parcial)

**Input exemplo:** "Método Y melhora desenvolvimento"

**Reação esperada:**
1. Reconhecer que há estrutura mas falta especificidade
2. Se contexto suficiente: Validar automaticamente e apresentar feedback curado
3. Se precisar refinamento: Refinar automaticamente e apresentar resultado: "Refinei sua hipótese: [resultado]. Isso faz sentido?"

**Não fazer:**
- ❌ Forçar refinamento automático
- ❌ Assumir que precisa de Estruturador primeiro

### 5.3 Input Completo (Hipótese testável)

**Input exemplo:** "Método Y reduz tempo em 30% em equipes de 2-5 devs"

**Reação esperada:**
1. Reconhecer estrutura completa
2. Validar automaticamente: "Validei sua hipótese: [resultado da validação]. Faz sentido?"
3. Se aprovado: "Ótimo! Podemos seguir com: 1) definir desenho experimental, 2) pesquisar literatura, ou 3) algo diferente?"

**Não fazer:**
- ❌ Assumir que precisa de Estruturador
- ❌ Pular validação

### 5.4 Input de Mudança de Direção

**Input exemplo:** "Na verdade, quero fazer revisão de literatura"

**Reação esperada:**
1. Aceitar mudança sem questionar
2. Adaptar imediatamente: "Sem problema! Vamos adaptar..."
3. Oferecer próximo passo relevante para novo caminho

**Não fazer:**
- ❌ Questionar mudança
- ❌ Tentar manter caminho anterior

### 5.5 Input de Pergunta do Sistema

**Input exemplo:** Sistema pergunta "Qual população você está pensando?"

**Reação esperada:**
1. Usuário responde com informação
2. Sistema agradece e usa informação
3. Sistema faz próxima pergunta se necessário, ou oferece próximo passo

**Não fazer:**
- ❌ Fazer múltiplas perguntas de uma vez
- ❌ Não justificar por que pergunta é necessária

---

## 7. Princípios Fundamentais

### 7.1 Sistema como Facilitador, não Decisor

- Sistema **sugere** caminhos, não impõe
- Sistema **age automaticamente** quando contexto suficiente (transição fluida)
- Sistema **apresenta resultados curados** e confirma entendimento
- Sistema **respeita** decisão do usuário

### 7.2 Conversação sobre Classificação

- **Não classificar** automaticamente no início
- **Explorar** intenção antes de rotular
- **Co-construir** entendimento com usuário

### 7.3 Adaptabilidade sobre Rigidez

- **Mudanças são naturais** - não penalizar
- **Fluxo adaptativo** - não seguir script fixo
- **Contexto preservado** - manter informações úteis

### 7.4 Transparência sobre Mágica

- **Explicar** por que sugere caminho
- **Mostrar** opções disponíveis
- **Justificar** perguntas necessárias

---

## 10. Argumento Focal (Conceito para Épico 8)

### O que é Argumento Focal?

O Orquestrador está construindo um **"argumento focal"** sobre o que o usuário quer fazer. Esse argumento evolui ao longo da conversa e serve como âncora para detectar contexto e mudanças de direção.

### Evolução do Argumento Focal

**Turno 1:** Usuário tem observação vaga  
Argumento focal: "Usuário observou que LLMs aumentam produtividade"

**Turno 3:** Usuário quer testar hipótese  
Argumento focal: "Usuário quer testar hipótese: LLMs aumentam produtividade"

**Turno 5:** Metodologista sugere refinamento  
Argumento focal: "Usuário quer testar hipótese: LLMs aumentam produtividade em equipes de 2-5 devs, medido por tempo de sprint"

**Turno 8:** Usuário muda para revisão  
Argumento focal: "Usuário quer fazer revisão de literatura sobre LLMs e produtividade" [argumento anterior abandonado]

### Benefícios do Argumento Focal

**1. Detecção de Mudança de Direção**
- Sistema compara novo input com argumento focal atual
- Se contradiz → mudança de direção detectada
- Adapta sem questionar

**2. Contexto Preservado**
- Argumento focal acumula decisões do usuário
- Sistema lembra o que foi decidido anteriormente
- Evita perguntas repetitivas

**3. Sugestões Contextuais**
- Sistema sugere próximos passos baseado no argumento focal
- Exemplo: Se argumento focal tem população + métricas → sugerir Metodologista

### Conexão com Épico 8

No Épico 11, argumento focal se tornará explícito na entidade `Idea` (anteriormente "Topic"):
```python
Idea:
  id: UUID
  title: "Impacto de LLMs em produtividade"
  focal_argument: {
    "intent": "test_hypothesis",  # ou "review_literature", "build_theory"
    "subject": "LLMs impact on developer productivity",
    "population": "teams of 2-5 developers",
    "metrics": "time per sprint",
    "article_type": "empirical"  # inferido do argumento
  }
  stage: "hypothesis"  # derivado do argumento focal
  created_at: timestamp
  updated_at: timestamp
```

**Campos derivados do argumento focal:**
- `article_type`: emerge do intent (test_hypothesis → empirical)
- `stage`: emerge dos elementos presentes (população + métricas → hypothesis)
- `title`: extraído do subject do argumento focal

### Implementação no POC

**POC (implícito):**
- Argumento focal vive apenas no histórico da conversa
- LLM reconstrói argumento focal a cada turno analisando histórico
- Funciona mas é ineficiente

**Protótipo (explícito):**
- Argumento focal vira campo no `MultiAgentState`
- Atualizado explicitamente pelo Orquestrador
- Mais eficiente e rastreável

**MVP (persistente):**
- Argumento focal salvo na entidade `Idea` (Épico 11)
- Permite pausar/retomar com contexto preservado
- Histórico de argumentos focais (rollback possível)

### Exemplo de Uso na Detecção de Mudança
```python
# Argumento focal atual (implícito no POC)
current_focal = "Usuário quer testar hipótese: método X reduz tempo em 30%"

# Novo input
new_input = "Na verdade, quero fazer revisão de literatura"

# LLM compara
comparison = llm.compare(current_focal, new_input)
# Result: "Contradição detectada: foco mudou de 'testar' para 'revisar'"

# Sistema adapta
new_focal = "Usuário quer fazer revisão de literatura sobre método X"
```

---

## Referências

- `core/docs/vision/epistemology.md` - Base filosófica (proposições, solidez, contextos)
- `products/revelar/docs/ux/conversation_patterns.md` - Exemplos específicos de conversas no Revelar

