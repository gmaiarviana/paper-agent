# Orquestrador Socrático

**Versão:** 1.0  
**Data:** 16/11/2025  
**Épico:** 10  
**Status:** Especificação técnica para implementação

---

## Visão Geral

O Orquestrador Socrático transforma conversa de "interrogatório burocrático" para "diálogo provocativo" onde sistema expõe suposições implícitas e provoca reflexão através de contra-perguntas socráticas.

**Problema que resolve:**
Sistema faz perguntas genéricas de coleta de dados ao invés de provocar reflexão sobre assumptions não examinadas.

**Exemplo do problema:**
```
❌ Sistema: "Que tipo de revestimento? Em que tipo de construção?"
```
→ Coleta de dados burocrática

**Solução esperada:**
```
✅ Sistema: "Você falou em medir % de conclusão. Mas % para QUEM? 
           O engenheiro quer saber se está no prazo. 
           O cliente quer saber se vai pagar. 
           São métricas diferentes, não?"
```
→ Provocação que expõe assumption implícita

---

## Conceito: Contra-Pergunta Socrática

Sócrates não respondia perguntas - ele fazia contra-perguntas que expunham contradições e suposições não examinadas.

**Características:**
- Não é coleta de dados ("Que tipo?")
- Não é validação ("Isso está correto?")
- É exposição de assumptions ("Você assumiu X, mas e se Y?")

**Estrutura típica:**
1. **Apontar assumption**: "Você mencionou X..."
2. **Contra-pergunta**: "...mas e Y? Isso importa?"
3. **Consequência** (opcional): "Se não souber Y, como vai validar X?"

---

## 5 Categorias de Assumptions Detectáveis

### 1. Métrica Vaga
**O que é:** Usuário menciona conceito mensurável mas não especifica COMO medir.

**Exemplos de input:**
- "LLMs aumentam produtividade"
- "Método X é mais eficiente"
- "Ferramenta Y melhora qualidade"

**Assumptions implícitas:**
- Produtividade tem definição única e óbvia
- Eficiência é mensurável de forma padrão
- Qualidade tem critérios claros

**Contra-perguntas provocativas:**
- "Você mencionou produtividade, mas produtividade de QUÊ? Linhas de código? Features entregues? Bugs reduzidos? São métricas BEM diferentes."
- "Eficiência para QUEM? Desenvolvedor quer velocidade, gestor quer custo, usuário quer confiabilidade."
- "Qualidade em que DIMENSÃO? Performance? Manutenibilidade? Usabilidade? Trade-offs existem."

### 2. População Vaga
**O que é:** Usuário menciona "pessoas" ou "equipes" sem especificar características.

**Exemplos de input:**
- "Funciona para equipes de desenvolvimento"
- "Desenvolvedores preferem X"
- "Empresas adotam Y"

**Assumptions implícitas:**
- Todas as equipes são iguais
- Desenvolvedores são grupo homogêneo
- Tamanho/contexto da empresa não importa

**Contra-perguntas provocativas:**
- "Equipes de QUANTAS pessoas? 2 desenvolvedores vs 50 são realidades diferentes."
- "Desenvolvedores júnior vs senior? Experiência muda tudo."
- "Startups vs corporações? Contexto importa."

### 3. Baseline Ausente
**O que é:** Usuário faz comparação ("mais rápido", "melhor") sem especificar baseline.

**Exemplos de input:**
- "Método X é mais rápido"
- "Ferramenta Y reduz tempo"
- "Abordagem Z aumenta acurácia"

**Assumptions implícitas:**
- Baseline é óbvio
- Comparação é justa
- Contexto de medição é o mesmo

**Contra-perguntas provocativas:**
- "Mais rápido que O QUÊ? Método manual? Ferramenta concorrente? Versão anterior?"
- "Reduz tempo EM QUANTO? 10%? 50%? Ordem de magnitude?"
- "Aumenta acurácia COMPARADO COM? Baseline importa."

### 4. Causalidade Assumida
**O que é:** Usuário assume que correlação = causalidade sem considerar confundidores.

**Exemplos de input:**
- "X causa Y"
- "Depois de usar X, Y melhorou"
- "X → Y"

**Assumptions implícitas:**
- Relação é causal, não apenas correlação
- Não há variáveis confundidoras
- Direção da causalidade é óbvia

**Contra-perguntas provocativas:**
- "Você TEM CERTEZA que X causa Y? Ou X e Y podem ter causa comum Z?"
- "E se Y melhorou por OUTRO motivo que coincidiu com X?"
- "Como você ELIMINARIA explicações alternativas?"

### 5. Generalização Excessiva
**O que é:** Usuário assume que resultado local generaliza para contextos diferentes.

**Exemplos de input:**
- "Funcionou na minha equipe, então funciona"
- "Vi em 3 projetos, é padrão"
- "Todo mundo usa, deve ser bom"

**Assumptions implícitas:**
- Contexto do usuário é representativo
- Amostra pequena é suficiente
- Popularidade = eficácia

**Contra-perguntas provocativas:**
- "Funcionou na SUA equipe. Mas sua equipe tem características ÚNICAS? Tamanho? Senioridade? Stack?"
- "3 projetos é amostra REPRESENTATIVA? Ou pode ser viés de seleção?"
- "Popularidade prova eficácia? Ou só prova marketing?"

---

## Timing de Provocação

### QUANDO PROVOCAR ✅

**Turno 2-4:** Assumption ficou clara mas ainda não foi explorada
- Usuário mencionou conceito vago pela primeira vez
- Momento natural da conversa (não interrompe fluxo)
- Uma provocação por vez (não sobrecarregar)

**Lacuna é relevante:** Afeta qualidade científica da pesquisa
- Métrica vaga compromete testabilidade
- População vaga impede generalização
- Baseline ausente invalida comparação

**Usuário não resistiu:** Não repetiu assumption após provocação anterior
- Se usuário ignorou provocação, não insista
- Se usuário respondeu superficialmente, aprofunde

### QUANDO NÃO PROVOCAR ❌

**Turno 1:** Deixa usuário expressar ideia completa
- Sistema escuta antes de provocar
- Evita interrupção prematura

**Lacuna já foi explorada:** Usuário já respondeu essa provocação
- Não repetir provocações
- Não circular em loop

**Conversa está completa:** Todos aspectos relevantes foram cobertos
- Provocação desnecessária polui conversa
- Sistema reconhece suficiência

**Usuário está respondendo outra pergunta:** Não interrompa
- Respeite fluxo natural
- Aguarde momento apropriado

---

## Profundidade da Provocação

Sistema escala profundidade conforme resistência do usuário.

### Nível 1: Apontar Assumption
**Quando usar:** Primeira vez que assumption aparece

**Formato:**
```
"Você mencionou X, mas percebi que assumiu Y. Correto?"
```

**Exemplo:**
```
Usuário: "Método incremental é mais rápido"
Sistema: "Você mencionou 'mais rápido', mas percebi que assumiu que 
         existe um baseline conhecido. Você tem esse baseline?"
```

### Nível 2: Contra-Pergunta
**Quando usar:** Usuário confirmou assumption mas não explorou

**Formato:**
```
"Você assumiu X. Mas e Y? Isso não importa?"
```

**Exemplo:**
```
Usuário: "Sim, mais rápido que método manual"
Sistema: "Método manual de QUEM? Desenvolvedor júnior vs senior 
         têm velocidades MUITO diferentes. Isso não afeta comparação?"
```

### Nível 3: Consequência
**Quando usar:** Usuário resistiu a explorar assumption 2 vezes

**Formato:**
```
"Se você não souber Y, como vai validar X?"
```

**Exemplo:**
```
Usuário: "Não sei a senioridade, mas vi que funciona"
Sistema: "Se não souber senioridade, como vai SEPARAR efeito da 
         ferramenta do efeito da experiência? Pode ser confundidor."
```

---

## Integração com Argumento Focal

Orquestrador Socrático atualiza `focal_argument` conforme provocações são respondidas:

**Antes da provocação:**
```python
focal_argument: {
  "intent": "test_hypothesis",
  "subject": "incremental method impact on speed",
  "population": "not specified",  # ← assumption detectada
  "metrics": "not specified",     # ← assumption detectada
  "article_type": "empirical"
}
```

**Após provocação respondida:**
```python
focal_argument: {
  "intent": "test_hypothesis",
  "subject": "incremental method impact on development time",
  "population": "teams of 2-5 developers with 2+ years experience",
  "metrics": "time per sprint in days",
  "article_type": "empirical"
}
```

---

## Exemplos Completos

### Exemplo 1: Métrica Vaga

**Turno 1:**
```
Usuário: "Observei que LLMs aumentam produtividade"
Sistema: "Interessante observação! Me conta mais: onde você observou isso?"
```
→ Sistema escuta primeiro (não provoca prematuramente)

**Turno 2:**
```
Usuário: "Na minha equipe de desenvolvimento"
Sistema: "Legal! E quando você diz 'aumentam produtividade', você tá 
         medindo O QUÊ exatamente? Linhas de código? Features entregues? 
         Tempo por tarefa? São métricas bem diferentes."
```
→ Provocação Nível 1 (apontar assumption de métrica vaga)

**Turno 3:**
```
Usuário: "Tempo por tarefa"
Sistema: "Perfeito! E você tem baseline? Quanto tempo levava ANTES?"
```
→ Provocação Nível 1 (apontar assumption de baseline ausente)

### Exemplo 2: População Vaga + Escalada de Profundidade

**Turno 1:**
```
Usuário: "Método ágil funciona melhor para equipes"
Sistema: "Interessante! Me conta: que tipo de equipes você observou?"
```
→ Exploração inicial

**Turno 2:**
```
Usuário: "Equipes de desenvolvimento de software"
Sistema: "Equipes de QUANTAS pessoas? 3 desenvolvedores vs 30 são 
         realidades MUITO diferentes, não?"
```
→ Provocação Nível 2 (contra-pergunta)

**Turno 3:**
```
Usuário: "Ah, não sei exatamente"
Sistema: "Se não souber tamanho da equipe, como vai SEPARAR efeito 
         do método do efeito do tamanho? Pequenas equipes se comunicam 
         melhor naturalmente - pode ser confundidor."
```
→ Provocação Nível 3 (consequência) - usuário resistiu 2x

### Exemplo 3: Levantamento de Obra (Caso Real)

**Turno 1:**
```
Usuário: "Quero avaliar uso de visão computacional para acompanhamento 
         de atividades como revestimento. Ver % de conclusão..."
Sistema: "Interessante! Você mencionou '% de conclusão', mas % para QUEM? 
         O engenheiro quer saber se está no prazo (% físico). 
         O cliente quer saber quanto vai pagar (% financeiro). 
         O auditor quer saber conformidade (% de qualidade). 
         São métricas MUITO diferentes. Qual te interessa?"
```
→ Provocação Nível 2 (contra-pergunta expondo assumption)

**Turno 2:**
```
Usuário: "% físico de conclusão"
Sistema: "OK! E como você vai VALIDAR que a visão computacional está 
         medindo certo? Precisa de baseline - alguém medindo manualmente 
         pra comparar. Você tem isso ou vai precisar coletar?"
```
→ Provocação Nível 1 (apontar assumption de baseline/validação)

---

## Implementação Técnica

### Prompt do Orquestrador

**Arquivo:** `utils/prompts.py`  
**Nome:** `ORCHESTRATOR_SOCRATIC_PROMPT_V1`

**Estrutura do prompt:**
1. **Papel:** Facilitador socrático (não interrogador)
2. **5 Categorias:** Instruções explícitas para detectar cada assumption
3. **Timing:** Quando provocar e quando não provocar
4. **Profundidade:** 3 níveis de provocação
5. **Exemplos:** 3 exemplos completos (métrica vaga, população vaga, escalada)
6. **Output JSON:** focal_argument + reflection_prompt

### Config YAML

**Arquivo:** `config/agents/orchestrator.yaml`

**Mudanças:**
- Remover classificação vague/semi_formed/complete (deprecated)
- Referenciar comportamento socrático
- Modelo: claude-3-5-haiku-20241022 (suficiente para provocações)

### Integração com Estado

**Sem mudanças no MultiAgentState (POC):**
- `focal_argument` já existe (Épico 7.8)
- `reflection_prompt` já existe (Épico 7.9)
- Sistema usa campos existentes

**Mudanças futuras (Épico 11 - Modelagem Cognitiva):**
- `assumptions` será campo explícito
- `open_questions` rastreará lacunas
- Orquestrador populará esses campos

---

## Referências

- `docs/product/vision.md` - Sistema como "mestre socrático"
- `docs/product/cognitive_model.md` - Modelo de assumptions e premises
- `docs/orchestration/conversational_orchestrator.md` - Base conversacional (Épico 7)

---

**Próximos Épicos:**
- Épico 11: Modelagem Cognitiva (rastreamento explícito de assumptions)
- Épico 12: Persistência (salvar modelo cognitivo)
- Épico 13: Múltiplos Tópicos (gerenciar vários argumentos)

