# Padrões de Conversa - Paper Agent

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

## 3. Padrões de Negociação de Caminho

### Objetivo
Apresentar opções e deixar usuário decidir, não impor fluxo.

### Comportamento Esperado

**✅ BOM:**
```
Sistema: "O Metodologista sugeriu refinamentos: falta população 
         e métricas. O que você quer fazer?
         1) Refinar agora (chamar Estruturador)
         2) Pesquisar mais sobre métricas primeiro
         3) Seguir em outra direção"
Usuário: "Refinar agora"
Sistema: "Perfeito! Chamando Estruturador para refinar..."
```

**❌ RUIM:**
```
Sistema: "Metodologista detectou needs_refinement. Refinando 
         automaticamente..."
[Loop automático sem consultar usuário]
```

### Princípios

1. **Sempre apresentar opções** - Nunca decidir sozinho
2. **Explicar contexto** - Usuário precisa entender por que opções existem
3. **Respeitar decisão** - Executar o que usuário escolher
4. **Permitir mudança de direção** - Usuário pode mudar de ideia

### Exemplos de Negociação

**Após feedback do Metodologista:**
```
"Ele sugeriu X e Y. O que quer fazer?
 → Refinar agora
 → Pesquisar mais sobre Y
 → Vamos em outra direção"
```

**Após estrutura criada:**
```
"Estrutura criada! Podemos seguir com:
 → Definir desenho experimental
 → Pesquisar literatura sobre métricas
 → Algo diferente?"
```

**Após pesquisa realizada:**
```
"Temos uma boa base. Quer que eu chame o Escritor para compilar 
a revisão ou prefere revisar os papers primeiro?"
```

---

## 4. Padrões de Mudança de Direção

### Objetivo
Permitir que usuário mude de ideia sem penalização ou fricção.

### Comportamento Esperado

**✅ BOM:**
```
Usuário: "Na verdade, quero fazer revisão de literatura"
Sistema: "Sem problema! Vamos adaptar. Posso chamar o Estruturador 
         para ajudar a definir uma questão de pesquisa estruturada 
         (tipo PICO/SPIDER)?"
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
3. Se usuário escolher testar: "Posso chamar o Estruturador para ajudar a formular uma questão mais específica?"
4. Negociar cada passo

**Não fazer:**
- ❌ "Detectei input vago. Estruturador automático."
- ❌ Assumir que usuário quer estruturar

### 5.2 Input Semi-Formado (Hipótese parcial)

**Input exemplo:** "Método Y melhora desenvolvimento"

**Reação esperada:**
1. Reconhecer que há estrutura mas falta especificidade
2. Oferecer opções: "Posso chamar o Metodologista para validar, ou prefere estruturar melhor primeiro?"
3. Se Metodologista sugerir refinamento: apresentar opções ao usuário

**Não fazer:**
- ❌ Forçar refinamento automático
- ❌ Assumir que precisa de Estruturador primeiro

### 5.3 Input Completo (Hipótese testável)

**Input exemplo:** "Método Y reduz tempo em 30% em equipes de 2-5 devs"

**Reação esperada:**
1. Reconhecer estrutura completa
2. Oferecer validação: "Posso chamar o Metodologista para validar essa hipótese?"
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

## 6. Exemplos de Conversas Boas vs Ruins

> **Nota sobre Análise Contextual (Épico 7 POC):**  
> Todos os exemplos seguem o padrão de "análise contextual" onde o Orquestrador analisa o histórico da conversa e o contexto atual antes de tomar decisões. O sistema não classifica automaticamente no primeiro turno, mas explora a intenção do usuário através de diálogo, considerando todo o contexto acumulado para oferecer opções relevantes.

### 6.1 Conversa BOA: Exploração Colaborativa

```
Usuário: "Observei que LLMs aumentam produtividade"
Sistema: "Interessante! Me conta mais: você quer VER o que já existe 
         sobre isso, ou quer TESTAR uma hipótese sua?"
Usuário: "Testar uma hipótese"
Sistema: "Legal! Me conta mais sobre essa observação: em que contexto 
         você observou isso?"
Usuário: "Em equipes de desenvolvimento usando Claude Code"
Sistema: "Perfeito! Posso chamar o Estruturador para ajudar a formular 
         uma questão de pesquisa mais específica?"
Usuário: "Sim"
[Estruturador cria V1]
Sistema: "O Metodologista pode validar essa questão. Quer que eu chame?"
Usuário: "Sim"
[Metodologista: needs_refinement - falta métricas]
Sistema: "Ele sugeriu refinamentos: falta definir como medir produtividade. 
         O que você quer fazer?
         1) Refinar agora (chamar Estruturador)
         2) Pesquisar mais sobre métricas primeiro
         3) Seguir em outra direção"
Usuário: "Refinar agora"
[Estruturador cria V2]
Sistema: "Ótimo! Podemos seguir com: 1) definir desenho experimental, 
         2) pesquisar literatura sobre métricas, ou 3) algo diferente?"
```

**Por que é boa:**
- ✅ Sistema explora sem impor (análise contextual antes de classificar)
- ✅ Cada passo é negociado (considera contexto acumulado)
- ✅ Usuário tem controle (sistema oferece opções baseadas no contexto)
- ✅ Opções claras e contextuais (derivadas da análise do histórico)

### 6.2 Conversa RUIM: Pipeline Rígido

```
Usuário: "Observei que LLMs aumentam produtividade"
Sistema: "Detectei que seu input é vago. Classificando como 'vague'. 
         Chamando Estruturador automaticamente."
[Estruturador cria V1]
Sistema: "Chamando Metodologista automaticamente."
[Metodologista: needs_refinement]
Sistema: "Detectado needs_refinement. Refinando automaticamente 
         (iteração 1/2)."
[Estruturador cria V2]
Sistema: "Chamando Metodologista automaticamente."
[Metodologista: approved]
Sistema: "Hipótese aprovada. Finalizando."
```

**Por que é ruim:**
- ❌ Sistema decide sozinho (classifica sem análise contextual)
- ❌ Usuário não participa (não explora intenção através de diálogo)
- ❌ Sem negociação (ignora contexto da conversa)
- ❌ Fluxo determinístico (roteia automaticamente sem considerar histórico)

### 6.3 Conversa BOA: Mudança de Direção

```
Usuário: "Método X é mais rápido"
Sistema: "Interessante! Você quer testar uma hipótese ou verificar 
         literatura?"
Usuário: "Testar hipótese"
[Fluxo de estruturação e validação]
Usuário: "Na verdade, quero fazer revisão de literatura"
Sistema: "Sem problema! Vamos adaptar. Posso chamar o Estruturador 
         para ajudar a definir uma questão de pesquisa estruturada 
         (tipo PICO/SPIDER)?"
Usuário: "Sim"
[Estruturador adapta para revisão]
Sistema: "Agora podemos buscar papers. Quer que eu chame o Pesquisador?"
```

**Por que é boa:**
- ✅ Sistema aceita mudança sem questionar (analisa novo contexto)
- ✅ Adapta imediatamente (atualiza análise contextual)
- ✅ Preserva contexto útil (mantém informações relevantes do histórico)
- ✅ Oferece próximo passo relevante (baseado no novo contexto)

### 6.4 Conversa RUIM: Resistência a Mudança

```
Usuário: "Método X é mais rápido"
[Fluxo de estruturação]
Usuário: "Na verdade, quero fazer revisão de literatura"
Sistema: "Você já escolheu hipótese empírica. Não posso mudar agora. 
         Quer continuar com a hipótese ou começar nova sessão?"
```

**Por que é ruim:**
- ❌ Sistema resiste a mudança (ignora novo contexto)
- ❌ Força continuidade (não atualiza análise contextual)
- ❌ Não adapta (mantém decisão anterior sem reanalisar)
- ❌ Cria fricção desnecessária (não considera evolução do argumento focal)

---

## 7. Princípios Fundamentais

### 7.1 Sistema como Facilitador, não Decisor

- Sistema **sugere** caminhos, não impõe
- Sistema **pergunta** antes de agir
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

## 8. Checklist de Qualidade de Conversa

Antes de implementar uma interação, verificar:

- [ ] Sistema pergunta antes de agir?
- [ ] Opções são apresentadas claramente?
- [ ] Contexto é explicado (por que essas opções)?
- [ ] Usuário pode mudar de direção?
- [ ] Sistema adapta sem questionar mudanças?
- [ ] Perguntas são específicas e contextuais?
- [ ] Sistema não classifica automaticamente?
- [ ] Cada passo é negociado?

---

## 9. Argumento Focal (Conceito para Épico 8)

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

No Épico 8, argumento focal se tornará explícito:
```python
Topic:
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
- Argumento focal salvo na entidade `Topic`
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

**Versão:** 1.1  
**Data:** 15/11/2025  
**Status:** Especificação completa - Revisado para alinhamento com Épico 7 POC

