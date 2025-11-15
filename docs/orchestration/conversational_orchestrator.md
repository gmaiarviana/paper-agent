# Orquestrador Conversacional Inteligente (Épico 7)

**Objetivo:** Transformar sistema de "trilho fixo" em diálogo adaptativo onde usuário e sistema decidem caminho juntos através de negociação contínua.

**Status:** 🟡 POC em planejamento

**Dependências:**
- Épico 6.2 concluído (registro de memória)

---

## 1. ARQUITETURA

### Decisão Arquitetural: Substituição Direta

**Abordagem:** Substituir `orchestrator_node` atual diretamente (abordagem ousada).

**Mudanças:**
- ❌ Remove lógica de classificação (`vague`/`semi_formed`/`complete`)
- ✅ Novo comportamento: explorar → analisar → sugerir → negociar
- ✅ Mantém estrutura de `MultiAgentState`
- ✅ Ignora limite de contexto no POC (foco em raciocínio básico)

### Novo Comportamento do Orquestrador

O Orquestrador POC evolui de **classificador determinístico** para **facilitador conversacional**:

```
ANTES (Épico 3):
Input → Classifica (vague/semi_formed/complete) → Roteia automaticamente

DEPOIS (Épico 7 POC):
Input → Conversa → Analisa contexto → Sugere opções → Usuário decide → Executa
```

**Papel do Orquestrador:**
- **Explorar:** Faz perguntas abertas para entender contexto
- **Analisar:** Examina input + histórico conversacional
- **Sugerir:** Opina sobre direções possíveis com justificativa
- **Negociar:** Oferece opções ao usuário antes de chamar agentes

---

## 2. RACIOCÍNIO DO ORQUESTRADOR

### Capacidades do Orquestrador POC

O Orquestrador POC deve:

1. **Explorar com perguntas abertas**
   - Quantas perguntas forem necessárias
   - Não classifica, apenas explora o espaço do problema
   - Exemplo: "Me conta mais sobre essa observação. Onde você viu isso acontecer?"

2. **Analisar contexto do input + histórico**
   - Considera não apenas o input atual, mas toda a conversa
   - Identifica padrões, contradições, lacunas
   - Não é "garçom" (não apenas repassa), mas analisa ativamente

3. **Opinar sobre direções possíveis**
   - Sugere múltiplas direções com justificativa clara
   - Explica por que cada direção faz sentido
   - Não impõe, apenas oferece opções

4. **Detectar mudança de direção**
   - Compara novo input com histórico conversacional
   - Identifica contradições ou mudanças de foco
   - Adapta sem questionar ou criar fricção

### Exemplo de Análise Contextual

**Input do usuário:**
```
"Observei que LLMs aumentam produtividade"
```

**Análise do Orquestrador:**
```
Interessante observação! Estou percebendo que você tem uma crença sobre LLMs, 
mas não mencionou como mediu produtividade ou em que contexto. Isso me sugere 
duas direções:

1. Se você quer VALIDAR essa crença, precisamos transformar em hipótese testável 
   (chamar Metodologista ajuda aqui)

2. Se você quer primeiro ENTENDER o que já existe, podemos fazer revisão de 
   literatura

Me conta mais: essa observação veio de experiência pessoal ou você já tem dados?
```

**Características da análise:**
- ✅ Identifica lacuna (falta de medição/contexto)
- ✅ Oferece múltiplas direções com justificativa
- ✅ Faz pergunta aberta para continuar exploração
- ✅ Não classifica como "vague" ou "complete"

---

## 3. DETECÇÃO DE MUDANÇA DE DIREÇÃO

### Mecanismo de Detecção

**Como funciona:**
- LLM compara novo input com histórico conversacional
- Detecta contradições ou mudanças de foco
- Adapta sem questionar ou criar fricção

**Exemplo:**

**Histórico:**
```
Usuário: "Quero estudar impacto de LLMs em produtividade de desenvolvedores"
Orquestrador: [explora contexto, sugere direções]
Usuário: "Na verdade, quero focar em qualidade de código, não produtividade"
```

**Detecção:**
```
Orquestrador detecta mudança de foco (produtividade → qualidade) e adapta:
"Entendi! Você mudou o foco de produtividade para qualidade de código. 
Isso muda a abordagem metodológica. Posso chamar o Metodologista para 
ajudar a estruturar uma hipótese sobre qualidade?"
```

**Características:**
- ✅ Reconhece mudança explicitamente
- ✅ Não questiona ("por que mudou?")
- ✅ Adapta sugestões ao novo foco
- ✅ Mantém contexto do histórico

### Conceito: "Argumento Focal"

**Definição:**
O sistema está construindo um **"argumento focal"** sobre o que o usuário quer fazer. Esse argumento evolui ao longo da conversa e serve como âncora para detectar contexto e mudanças de direção.

**Conexão com Épico 8:**
No Épico 8, o argumento focal se tornará campo explícito na entidade `Topic`, permitindo persistência e rastreamento formal. No POC, ele é implícito (reconstruído a cada turno via histórico).

**No POC:**
- Detecção simples via comparação LLM (novo input vs histórico)
- Argumento focal é implícito (vive apenas no histórico)
- LLM reconstrói argumento focal a cada turno analisando histórico
- Detecta mudanças óbvias (contradições, mudança de foco)

---

## 4. FLUXO POC

### Fluxo Conversacional Completo

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Usuário: input inicial                                   │
│    Ex: "Observei que LLMs aumentam produtividade"          │
└─────────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. Orquestrador: [analisa contexto] → faz pergunta aberta  │
│    Ex: "Interessante! Me conta mais: onde você observou    │
│        isso? Em que contexto?"                             │
└─────────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. Usuário: responde                                        │
│    Ex: "Na minha equipe, usando Claude Code"                │
└─────────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. Orquestrador: [analisa + histórico] → sugere opções     │
│    com justificativa                                        │
│    Ex: "Entendi! Vejo duas direções possíveis:             │
│        A) Validar essa observação como hipótese testável   │
│        B) Primeiro entender o que já existe na literatura   │
│        Qual faz mais sentido para você?"                    │
└─────────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. Usuário: escolhe                                         │
│    Ex: "A) Validar"                                          │
└─────────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────────┐
│ 6. Orquestrador: "Posso chamar [Agente]?"                  │
│    [explica por que faz sentido]                            │
│    Ex: "Posso chamar o Metodologista? Ele vai ajudar a     │
│        transformar sua observação em hipótese testável com  │
│        população, variáveis e métricas claras."             │
└─────────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────────┐
│ 7. Usuário: decide                                          │
│    Ex: "Sim, pode chamar"                                    │
└─────────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────────┐
│ 8. [Agente processa]                                        │
│    Metodologista valida/refina hipótese                     │
└─────────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────────┐
│ 9. Orquestrador: [analisa resultado] → apresenta opções   │
│    contextuais                                              │
│    Ex: "O Metodologista sugeriu refinamentos. Você quer:    │
│        A) Refinar a hipótese agora                          │
│        B) Pesquisar literatura primeiro                     │
│        C) Mudar de direção"                                 │
└─────────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────────┐
│ 10. [Loop continua]                                         │
│     Conversação adaptativa até usuário decidir finalizar    │
└─────────────────────────────────────────────────────────────┘
```

### Características do Fluxo

- ✅ **Conversação natural:** Não usa números/keywords, apenas diálogo
- ✅ **Negociação contínua:** Usuário decide a cada passo
- ✅ **Contexto preservado:** Histórico completo considerado
- ✅ **Sugestões justificadas:** Cada opção vem com razão clara
- ✅ **Adaptação dinâmica:** Detecta mudanças e ajusta

---

## 5. CRITÉRIOS DE ACEITE POC

### Funcionalidades Mínimas

✅ **Perguntas abertas (não classificação)**
- Orquestrador faz perguntas exploratórias
- Não classifica input como "vague"/"semi_formed"/"complete"
- Explora contexto antes de sugerir direções

✅ **Análise contextual (não garçom)**
- Analisa input + histórico conversacional
- Identifica padrões, lacunas, contradições
- Opina sobre direções possíveis

✅ **Sugestões com justificativa**
- Oferece múltiplas opções ao usuário
- Cada opção vem com explicação clara do porquê
- Não impõe caminho, apenas sugere

✅ **Detecção de mudança via LLM**
- Compara novo input com histórico
- Detecta contradições ou mudanças de foco
- Adapta sem questionar ou criar fricção

✅ **Conversação natural (não números/keywords)**
- Diálogo fluido, sem comandos estruturados
- Usuário responde naturalmente
- Sistema interpreta intenção do usuário

### Exemplos de Comportamento Esperado

**✅ BOM:**
```
Orquestrador: "Interessante observação! Vejo que você mencionou produtividade, 
mas não especificou como mediu. Isso me sugere duas direções: validar como 
hipótese ou primeiro entender o que já existe. Qual faz mais sentido?"
```

**❌ RUIM:**
```
Orquestrador: "Input classificado como 'semi_formed'. Roteando para Metodologista."
```

**✅ BOM:**
```
Orquestrador: "Entendi que você mudou o foco de produtividade para qualidade. 
Isso muda a abordagem. Posso chamar o Metodologista para estruturar uma 
hipótese sobre qualidade?"
```

**❌ RUIM:**
```
Orquestrador: "Por que você mudou de ideia? Isso contradiz o que você disse antes."
```

---

## 6. PROGRESSÃO

### POC → Protótipo → MVP

A estrutura básica se mantém, mas o raciocínio evolui incrementalmente:

#### POC (primeira entrega - foco mínimo viável)

**Raciocínio:**
- Básico: explora, analisa contexto simples, sugere opções óbvias
- Detecção simples: compara input novo com histórico (mudanças óbvias)

**Funcionalidades:**
- 7.1: Orquestrador mantém diálogo fluido (não apenas roteia)
- 7.2: Oferece opções ao usuário (não impõe caminho)
- 7.3: Chama agentes sob demanda (quando usuário concorda)

**Critérios de aceite:**
- Sistema conversa antes de chamar agente
- Usuário pode escolher entre opções (A, B ou C)
- Agentes só executam após confirmação

#### Protótipo (segunda entrega - inteligência básica)

**Raciocínio:**
- Refinado: análise mais profunda, identifica padrões sutis
- Provocação: faz perguntas que ajudam usuário a refletir

**Funcionalidades:**
- 7.4: Detecção inteligente de quando agente faz sentido
- 7.5: Provocação de reflexão ("Você pensou em X?")
- 7.6: Handling de mudança de direção

**Critérios de aceite:**
- Sistema sugere agente apropriado no momento certo
- Faz perguntas esclarecedoras que ajudam usuário
- Adapta quando usuário muda de ideia

#### MVP (terceira entrega - sistema completo)

**Raciocínio:**
- Argumento focal explícito: extrai e atualiza campo focal_argument no state
- Provocação de reflexão: identifica lacunas na conversa e faz perguntas inteligentes
- Detecção emergente: infere estágio sem classificar explicitamente

**Funcionalidades:**
- 7.8: Argumento Focal Explícito (campo no MultiAgentState)
- 7.9: Provocação de Reflexão (versão simples)
- 7.10: Detecção Emergente de Estágio (exploration → hypothesis)

**Critérios de aceite:**
- Orquestrador extrai e atualiza argumento focal explicitamente (campo focal_argument)
- Identifica lacunas na conversa e faz perguntas que ajudam usuário a refletir
- Sistema detecta quando conversa evoluiu (exploration → hypothesis) e sugere mudança de estágio

---

## 7. IMPLEMENTAÇÃO TÉCNICA

### Mudanças no Código

**Arquivo:** `agents/orchestrator/nodes.py`

**Antes:**
```python
def orchestrator_node(state: MultiAgentState, ...):
    # Classifica: vague/semi_formed/complete
    # Roteia automaticamente
```

**Depois:**
```python
def orchestrator_node(state: MultiAgentState, ...):
    # Analisa contexto (input + histórico)
    # Faz pergunta aberta OU sugere opções
    # Negocia com usuário antes de chamar agentes
```

### Estado (MultiAgentState)

**Mantém:**
- `user_input`: Input atual do usuário
- `conversation_history`: Histórico completo
- `messages`: Mensagens LangGraph

**Remove (POC):**
- `orchestrator_classification`: Não classifica mais
- `current_stage`: Não usa estágios fixos

**Adiciona (futuro - Protótipo/MVP):**
- `orchestrator_suggestions`: Opções oferecidas ao usuário
- `user_choices`: Histórico de decisões do usuário

### Prompt do Sistema (ORCHESTRATOR_CONVERSATIONAL_PROMPT_V1)

### Estrutura do Prompt

O prompt do Orquestrador conversacional deve guiar os seguintes comportamentos:

**1. EXPLORAÇÃO INICIAL**
- Perguntas abertas para entender intenção
- Não classificar automaticamente (vague/completo)
- Oferecer opções claras

**2. ANÁLISE CONTEXTUAL**
- Analisar input + TODO o histórico da conversa
- Identificar o que está claro e o que falta
- Detectar padrões: crença vs observação vs hipótese

**3. SUGESTÃO COM JUSTIFICATIVA**
- Sugerir próximos passos com RAZÃO clara
- Sempre apresentar opções, não decidir sozinho
- Explicar por que agente específico faz sentido

**4. DETECÇÃO DE MUDANÇA**
- Comparar novo input com histórico
- Se detectar contradição ou mudança de foco, adaptar sem questionar
- Atualizar "argumento focal" implícito

**5. CONVERSAÇÃO NATURAL**
- Linguagem clara e acessível
- Evitar jargões desnecessários
- Perguntar quantas vezes precisar (sem limite artificial)

### Agentes Disponíveis
- **Estruturador**: transforma ideias vagas em questões estruturadas
- **Metodologista**: valida rigor científico
- **Pesquisador**: busca literatura
- **Escritor**: compila artigo

### Output Esperado (JSON)
```json
{
  "reasoning": "Análise do contexto e histórico",
  "next_step": "explore" | "suggest_agent" | "clarify",
  "message": "Mensagem ao usuário (pergunta ou sugestão)",
  "agent_suggestion": null | {
    "agent": "nome", 
    "justification": "por que faz sentido"
  }
}
```

### Exemplos de Output

**Exemplo 1: Exploração inicial**
```
Input: "Observei que LLMs aumentam produtividade"

Output:
{
  "reasoning": "Usuário tem observação mas não especificou: contexto, métricas, população. Pode querer testar ou verificar literatura. Preciso explorar intenção.",
  "next_step": "explore",
  "message": "Interessante observação! Me conta mais: você quer VER o que já existe sobre isso, ou quer TESTAR uma hipótese sua?",
  "agent_suggestion": null
}
```

**Exemplo 2: Sugestão de agente com justificativa**
```
Input histórico: [conversa sobre hipótese com população e métricas definidas]
Input: "Sim, quero validar essa hipótese"

Output:
{
  "reasoning": "Usuário definiu hipótese com população (equipes 2-5 devs) e métricas (tempo por sprint). Estrutura testável. Metodologista pode validar rigor científico.",
  "next_step": "suggest_agent",
  "message": "Perfeito! Posso chamar o Metodologista para validar se essa hipótese atende critérios científicos? Ele vai verificar testabilidade, falseabilidade e operacionalização.",
  "agent_suggestion": {
    "agent": "methodologist",
    "justification": "Hipótese estruturada com população e métricas definidas, pronta para validação metodológica"
  }
}
```

**Exemplo 3: Detecção de mudança de direção**
```
Input histórico: [conversa sobre teste de hipótese em andamento]
Input: "Na verdade, quero fazer revisão de literatura"

Output:
{
  "reasoning": "Detecto mudança de direção: de teste de hipótese para revisão de literatura. Usuário mudou de ideia. Adaptar sem questionar. Argumento focal anterior (testar hipótese X) → novo argumento focal (revisar literatura sobre X).",
  "next_step": "suggest_agent",
  "message": "Sem problema! Vamos adaptar. Posso chamar o Estruturador para ajudar a definir uma questão de pesquisa estruturada (tipo PICO/SPIDER) para a revisão?",
  "agent_suggestion": {
    "agent": "structurer",
    "justification": "Revisão de literatura precisa de questão estruturada. PICO/SPIDER são frameworks adequados."
  }
}
```

### Implementação
- **Localização futura**: `utils/prompts.py`
- **Constante**: `ORCHESTRATOR_CONVERSATIONAL_PROMPT_V1`
- **Modelo**: Claude Sonnet 4 (para raciocínio complexo)

---

## 8. EXEMPLOS CONCRETOS

### Exemplo 1: Exploração Inicial

**Input:**
```
"LLMs aumentam produtividade"
```

**Orquestrador:**
```
Interessante observação! Para eu entender melhor e sugerir o melhor caminho, 
me conta:

1. Onde você observou isso? (experiência pessoal, estudo, dados?)
2. Como você mediu produtividade? (tempo, qualidade, quantidade?)
3. Em que contexto? (desenvolvimento, pesquisa, escrita?)

Quanto mais contexto você compartilhar, melhor posso ajudar a estruturar 
isso como pesquisa acadêmica.
```

### Exemplo 2: Sugestão de Direções

**Contexto:**
```
Usuário: "Na minha equipe, usando Claude Code, vi que tarefas que levavam 
         2 horas agora levam 30 minutos"
```

**Orquestrador:**
```
Excelente! Agora tenho contexto concreto. Vejo duas direções possíveis:

A) VALIDAR como hipótese testável
   - Transformar sua observação em hipótese formal
   - Definir população, variáveis, métricas
   - O Metodologista pode ajudar aqui
   - Faz sentido se você quer testar isso cientificamente

B) ENTENDER o que já existe
   - Revisar literatura sobre produtividade com LLMs
   - Ver como outros pesquisadores mediram isso
   - O Pesquisador pode ajudar aqui
   - Faz sentido se você quer primeiro entender o estado da arte

Qual direção faz mais sentido para você?
```

### Exemplo 3: Detecção de Mudança

**Histórico:**
```
Usuário: "Quero estudar impacto de LLMs em produtividade"
Orquestrador: [explora, sugere direções]
Usuário: "Na verdade, quero focar em qualidade de código, não produtividade"
```

**Orquestrador:**
```
Entendi! Você mudou o foco de produtividade para qualidade de código. 
Isso muda a abordagem metodológica - qualidade tem métricas diferentes 
(complexidade, bugs, manutenibilidade).

Posso chamar o Metodologista para ajudar a estruturar uma hipótese sobre 
qualidade de código? Ele vai ajudar a definir como medir qualidade e 
quais variáveis considerar.
```

---

## 9. NOTAS DE IMPLEMENTAÇÃO

### Limitações do POC

- **Raciocínio básico:** Análise simples, não profundamente sofisticada
- **Detecção simples:** Apenas mudanças óbvias, não padrões sutis
- **Sem limite de contexto:** Ignora limites no POC (foco em funcionalidade)
- **Sem aprendizado:** Não aprende preferências do usuário ainda

### Próximos Passos (Protótipo)

- Refinar raciocínio (análise mais profunda)
- Adicionar provocação ("Você pensou em X?")
- Melhorar detecção de mudança (padrões sutis)
- Implementar histórico de decisões do usuário

### Conexão com Épico 8

- **Argumento focal:** Conceito documentado mas não implementado no POC
- **Persistência:** Base para persistência de tópicos (Épico 8)
- **Evolução:** POC → Protótipo → MVP mantém estrutura, evolui raciocínio

---

## 10. Protótipo: CLI Conversacional (Épico 7.5-7.7)

### Mudanças Implementadas

**POC → Protótipo:**
- ✅ POC: Backend conversacional implementado (Orquestrador analisa contexto)
- ✅ Protótipo: Frontend conversacional (CLI com múltiplos turnos)

### CLI Conversacional (7.5)

**Problema resolvido:** CLI do POC não mantinha conversa - voltava para "Digite sua hipótese" após cada resposta.

**Solução:**
- Loop conversacional contínuo
- Thread ID preservado ao longo da sessão
- Contexto acumulado via `conversation_history`

**Fluxo implementado:**
Sistema: Olá! Me conte sobre sua ideia.
Você: tdd reduz bugs
Sistema: Em que contexto?
Você: equipe Python
Sistema: Como mediu?
Você: impressão geral
Sistema: Posso chamar Estruturador?
Você: sim
[chama Estruturador...]

**Código:**
```python
thread_id = f"cli-session-{uuid.uuid4()}"
while True:
    user_input = input("Você: ")
    result = graph.invoke(
        {"user_input": user_input},
        config={"configurable": {"thread_id": thread_id}}
    )
    print(f"Sistema: {result['orchestrator_output']['message']}")
```

### Detecção Inteligente (7.6)

**Abordagem não-determinística:**
- LLM julga "momento certo" baseado em contexto
- Não usa checklist rígida de campos obrigatórios
- Considera qualidade e quantidade de informação

**Prompt do Orquestrador (atualizado):**
Analise o histórico completo. Você tem CONTEXTO SUFICIENTE para sugerir
agente quando:

Conversa acumulou detalhes relevantes
Chamar agente agregaria valor real
Não precisa estar perfeito, apenas útil

Use julgamento contextual, não protocolo fixo.
Se contexto suficiente:
next_step = "suggest_agent"
agent_suggestion = {"agent": "nome", "justification": "..."}
Se precisa mais info:
next_step = "explore"
message = "Pergunta esclarecedora específica"

**Output esperado:**
```json
{
  "reasoning": "Análise do contexto acumulado...",
  "next_step": "suggest_agent",
  "message": "Posso chamar o Estruturador para transformar em questão?",
  "agent_suggestion": {
    "agent": "structurer",
    "justification": "Usuário tem observação + contexto, falta estruturação"
  }
}
```

### Transparência do Raciocínio (7.7)

**3 níveis implementados:**

1. **CLI Padrão** (limpo): Apenas mensagem
2. **CLI Verbose** (`--verbose`): Mensagem + reasoning inline
3. **Dashboard** (sempre): Timeline com reasoning completo

**Implementação:**
```python
# CLI
if args.verbose:
    print(f"🧠 {orchestrator_output['reasoning']}")
print(f"Sistema: {orchestrator_output['message']}")

# EventBus
event_bus.publish_agent_completed(
    session_id=thread_id,
    agent="orchestrator",
    summary=orchestrator_output['message'],
    metadata={"reasoning": orchestrator_output['reasoning']}
)
```

**Benefícios:**
- CLI mantém experiência limpa por padrão
- Reasoning disponível sob demanda (verbose)
- Dashboard sempre mostra transparência completa
- Usa infraestrutura existente (Épico 5)

### Diferenças POC → Protótipo

| Aspecto | POC | Protótipo |
|---------|-----|-----------|
| **CLI** | Loop único | Chat contínuo |
| **Contexto** | Não preservado | Preservado via thread_id |
| **Turnos** | 1 (input → fim) | N (conversa fluida) |
| **Detecção** | Básica | Inteligente (LLM julga) |
| **Transparência** | Apenas logs | 3 níveis (CLI/verbose/dashboard) |
| **Experiência** | Quebrada | Fluida e natural |

### Próximos Passos (MVP)

- 7.8: Argumento Focal Explícito (campo no state)
- 7.9: Provocação de Reflexão (versão simples)
- 7.10: Detecção Emergente de Estágio

**Nota:** Funcionalidades 7.12-7.14 foram movidas para outros épicos:
- 7.12: Reasoning Explícito das Decisões → Épico 9.6/9.7 (Interface Web)
- 7.13: Histórico de Decisões → Épico 10.7 (Persistência)
- 7.14: Argumento Focal Persistente → Épico 10.2 (Persistência)

**Especificação técnica completa:** `docs/interface/conversational_cli.md`

---

**Versão:** 1.1 (Protótipo implementado)
**Data:** 15/11/2025
**Status:** Especificação para Protótipo (Épico 7.5-7.7)

