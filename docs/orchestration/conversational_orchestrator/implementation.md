# Implementação Técnica

## Mudanças no Código

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

## Estado (MultiAgentState)

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

## Prompt do Sistema (ORCHESTRATOR_CONVERSATIONAL_PROMPT_V1)

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

**3. CHAMADA AUTOMÁTICA DE AGENTE**
- Quando contexto suficiente, CHAMAR o agente automaticamente
- Não pedir permissão, agir proativamente
- Decidir qual agente chamar baseado no contexto acumulado

**4. CURADORIA DA RESPOSTA**
- Receber resultado do agente
- Fazer curadoria: apresentar resultado como se fosse você, em tom coeso
- Primeira pessoa: "Organizei...", "Validei...", "Identifiquei..."
- NÃO mencionar agente na conversa principal
- Coeso com conversa anterior

**5. CONFIRMAÇÃO DE ENTENDIMENTO**
- Confirmar entendimento: "Isso captura o que você quer?"
- NÃO pedir permissão: "Posso chamar agente?" ❌
- Usuário ajusta se necessário, sistema adapta

**6. DETECÇÃO DE MUDANÇA**
- Comparar novo input com histórico
- Se detectar contradição ou mudança de foco, adaptar sem questionar
- Atualizar "argumento focal" implícito

**7. CONVERSAÇÃO NATURAL**
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
  "next_step": "explore" | "call_agent" | "clarify",
  "message": "Mensagem ao usuário (pergunta ou resultado curado)",
  "agent_call": null | {
    "agent": "nome", 
    "justification": "por que faz sentido"
  }
}
```

**Nota:** `next_step: "call_agent"` significa chamar automaticamente (não sugerir).

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

**Exemplo 2: Transição fluida para agente**
```
Input histórico: [conversa sobre hipótese com população e métricas definidas]
Input: "Sim, quero validar essa hipótese"

Output:
{
  "reasoning": "Usuário definiu hipótese com população (equipes 2-5 devs) e métricas (tempo por sprint). Estrutura testável. Contexto suficiente. Chamando Metodologista automaticamente.",
  "next_step": "call_agent",
  "message": "Validei sua hipótese: ela atende critérios de testabilidade, falseabilidade e operacionalização. Isso captura o que você quer explorar?",
  "agent_call": {
    "agent": "methodologist",
    "justification": "Hipótese estruturada com população e métricas definidas, pronta para validação metodológica"
  }
}
[Bastidores: 🔬 Metodologista validou → 🎯 Orquestrador curou]
```

**Nota:** O `message` é a resposta curada após o agente trabalhar, não uma pergunta de permissão.

**Exemplo 3: Detecção de mudança de direção**
```
Input histórico: [conversa sobre teste de hipótese em andamento]
Input: "Na verdade, quero fazer revisão de literatura"

Output:
{
  "reasoning": "Detecto mudança de direção: de teste de hipótese para revisão de literatura. Usuário mudou de ideia. Adaptar sem questionar. Chamando Estruturador automaticamente para criar questão PICO/SPIDER.",
  "next_step": "call_agent",
  "message": "Sem problema! Vamos adaptar. Organizei uma questão de pesquisa estruturada (PICO/SPIDER) para a revisão: [resultado]. Isso direciona bem o que você quer buscar?",
  "agent_call": {
    "agent": "structurer",
    "justification": "Revisão de literatura precisa de questão estruturada. PICO/SPIDER são frameworks adequados."
  }
}
[Bastidores: 📝 Estruturador estruturou → 🎯 Orquestrador curou]
```

### Implementação
- **Localização futura**: `utils/prompts.py`
- **Constante**: `ORCHESTRATOR_CONVERSATIONAL_PROMPT_V1`
- **Modelo**: Claude Sonnet 4 (para raciocínio complexo)

---

**Próximas seções:**
- [Exemplos](./examples.md) - Exemplos concretos de implementação
- [Curadoria](./curation.md) - Modelo de curadoria

