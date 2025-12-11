# Orquestrador

## Visão Geral

O Orquestrador é o **Facilitador Conversacional** do sistema multi-agente. Ele coordena a interação entre o usuário e os agentes especializados, mantendo o fluxo da conversa natural e adaptativo.

**Papel Principal:**
- Analisa input do usuário e decide entre responder diretamente ou delegar para um agente especializado
- Mantém histórico da conversa em memória (via LangGraph) e registra cada decisão
- Facilita diálogo provocativo com exposição de assumptions implícitas
- Negocia caminhos com o usuário (apresenta opções, não decide sozinho)

## Evolução Planejada

⚠️ **VISÃO FUTURA:** O Orquestrador passará por refatoração para separar responsabilidades:

**Hoje (Implementado):**
- Coordenação de agentes ✅
- Comunicação com usuário ✅
- Decisão de next_step ✅

**Futuro (Conceitual):**
- Coordenação de agentes ✅
- Comunicação com usuário → será delegada ao Comunicador
- Decisão de next_step ✅
- Consulta a Memory Agent (novo) ✅

Esta separação visa:
- **Neutralidade:** decisões lógicas sem viés linguístico
- **Customização:** personas aplicadas pelo Comunicador
- **Testabilidade:** lógica pura separada de linguagem

---

## Responsabilidades

### Responsabilidades Principais

- **Facilitar conversação** entre usuário e sistema (não apenas classificar)
- Gerenciar estado da conversa e progresso do artigo
- **Negociar caminhos** com o usuário (apresentar opções, não decidir sozinho)
- Detectar quando há conflito entre agentes
- Apresentar conflitos para o usuário resolver
- Determinar quando o artigo está completo
- **Adaptar fluxo** conforme decisões do usuário
- **Provocar reflexão** sobre aspectos não explorados: "Você assumiu X. Quer examinar?"
- **Consultar Observador** quando incerto (gatilhos naturais)

### Consulta a Memory Agent (Futuro)

Quando necessário, o Orquestrador consultará o Memory Agent para:

- **Validar entendimento** (usuário já definiu baseline?)
- **Resolver incongruências** (Observador detectou contradição)
- **Recall explícito** (usuário pergunta sobre passado)
- **Retomar contexto** (mudança de foco)

**Gatilhos de consulta:**

- Observador sinaliza incongruência
- Orquestrador detecta referência a contexto não presente em CognitiveModel
- Usuário pergunta explicitamente sobre passado
- Mudança de foco detectada (retomar ideia anterior)

**Exemplo:**

```python
# Observador sinaliza incongruência
if observador.detectou_incongruencia:
    # Orquestrador consulta Memory
    contexto = memory_agent.query(
        query="buscar menções a 'baseline'",
        strategy="superficial_first"
    )
    
    # Orquestrador processa resultado
    if contexto:
        orquestrador.resolver_incongruencia(contexto)
    else:
        orquestrador.perguntar_ao_usuario("baseline")
```

---

## O que o Orquestrador PODE fazer

- **Perguntar ao usuário** antes de chamar agentes
- **Apresentar opções** claras e contextuais
- Chamar qualquer agente (após negociação)
- Solicitar re-trabalho de qualquer etapa
- Pedir esclarecimentos ao usuário
- Salvar checkpoints do progresso
- **Adaptar fluxo** quando usuário muda de direção
- Encerrar processo (com aprovação do usuário)
- **Consultar Observador** para insights contextuais
- Usar insights para decisões mais inteligentes

---

## O que o Orquestrador NÃO PODE fazer

- **Decidir sozinho** qual agente chamar (deve negociar)
- **Classificar automaticamente** sem explorar intenção
- Avaliar conteúdo científico
- Escrever ou editar texto
- Tomar decisões sobre metodologia
- Ignorar feedback de agentes especialistas
- **Forçar fluxo rígido** (deve ser adaptativo)
- **Detectar proposições não examinadas** (responsabilidade do Observador)
- **Extrair claims** (responsabilidade do Observador)
- **Atualizar CognitiveModel** (responsabilidade do Observador)

---

## Input e Output

### Input esperado

- Do usuário: hipótese inicial, observação, constatação, **decisões sobre caminhos**
- De agentes: outputs validados ou rejeitados

### Output esperado

- **Perguntas e opções** para o usuário
- Comandos para próximo agente (após negociação)
- Resumos de progresso para usuário
- Apresentação de conflitos com argumentos

**Estrutura de decisão:**

```python
{
    "action": "call_agent" | "respond_direct",
    "agent": "methodologist" | null,
    "message": "..."
}
```

**Decisões:**
- `respond_direct`: utilizado para saudações, conversas casuais ou perguntas fora do escopo científico
- `call_agent`: utilizado para hipóteses ou solicitações que demandem avaliação metodológica. Ao escolher esta opção, o Orquestrador chama o agente correspondente e inclui a resposta formatada no retorno ao usuário

---

## Critérios de Qualidade

- **Sempre pergunta antes de agir**
- **Opções claras e contextuais** apresentadas
- Fluxo lógico mantido (mas adaptativo)
- Nenhum agente chamado fora de contexto
- Conflitos sempre escalados para usuário
- Estado sempre consistente
- **Mudanças de direção aceitas sem questionar**

---

## Fluxo de Decisão

### Fluxo Atual

```
Turno atual
     ↓
Orquestrador analisa contexto
     ↓
Orquestrador decide:
├─ explore → Faz perguntas abertas
├─ suggest_agent → Sugere agente com justificativa
└─ clarify → Esclarece ambiguidade
     ↓
Orquestrador fala com usuário
```

### Fluxo com Memory Agent (Futuro)

```
Turno atual
     ↓
Observador processa
     ↓
Observador sinaliza Orquestrador (se necessário)
     ↓
Orquestrador avalia:
├─ Precisa de contexto histórico?
│  ├─ SIM → Consulta Memory Agent
│  │        ↓
│  │   Memory retorna contexto
│  │        ↓
│  │   Orquestrador processa com contexto
│  │
│  └─ NÃO → Decide com CognitiveModel atual
│
↓
Orquestrador decide next_step
     ↓
[HOJE] Orquestrador fala com usuário
[FUTURO] Orquestrador envia decisão neutra → Comunicador traduz → Usuário
```

---

## Fluxos de Conversação

### Fluxo Conversacional Completo (Modelo de Transição Fluida)

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
│ 4. Orquestrador: [analisa + histórico] → continua          │
│    exploração ou sugere próximo passo                       │
└─────────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. [Se contexto suficiente] Orquestrador chama agente       │
│    automaticamente (sem pedir permissão)                    │
│    Ex: Chama Estruturador                                   │
└─────────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────────┐
│ 6. Agente processa e retorna resultado                     │
└─────────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────────┐
│ 7. Orquestrador: [recebe resultado] → faz curadoria →      │
│    apresenta em tom coeso                                   │
│    Ex: "Organizei sua ideia em uma hipótese testável:      │
│        [resultado com população, variáveis, métricas].      │
│        Isso captura o que você quer explorar?"               │
│    [Bastidores: 📝 Estruturador estruturou → 🎯 Orquestrador curou] │
└─────────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────────┐
│ 8. Usuário: confirma entendimento ou ajusta                 │
│    Ex: "Sim, perfeito!" ou "Ajuste X"                       │
└─────────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────────┐
│ 9. [Loop continua]                                          │
│    Se ajuste: Orquestrador explora novamente                │
│    Se confirma: Orquestrador pode chamar próximo agente     │
│    automaticamente quando contexto suficiente                │
└─────────────────────────────────────────────────────────────┘
```

### Características do Fluxo

- ✅ **Conversação natural:** Não usa números/keywords, apenas diálogo
- ✅ **Transição fluida:** Chama agente automaticamente quando contexto suficiente
- ✅ **Curadoria:** Orquestrador apresenta resultado como se fosse ele mesmo
- ✅ **Adaptativo:** Aceita mudanças de direção sem questionar

---

## Mudança de Papel (13/11/2025)

**ANTES (classificador):**
- Orquestrador classificava input automaticamente
- Router decidia próximo agente sem consultar usuário
- Fluxo rígido e determinístico

**AGORA (facilitador):**
- Orquestrador explora intenção com perguntas abertas
- Apresenta opções e negocia caminhos
- Fluxo adaptativo e conversacional
- Usuário mantém controle sobre decisões

**Exemplo de mudança:**
```
❌ ANTES: "Detectei que seu input é vago. Chamando Estruturador automaticamente."
✅ AGORA: "Interessante! Você quer testar uma hipótese ou verificar literatura?"
```

---

## Mitose: Observador Separado (05/12/2025)

**EVOLUÇÃO:**
- Orquestrador tinha 2 responsabilidades conflitantes
- Separamos em 2 agentes especializados:
  - **Orquestrador:** Facilitar conversa, negociar, decidir fluxo
  - **Observador:** Atualizar CognitiveModel, extrair conceitos, calcular métricas

**Como se comunicam:**
- Orquestrador consulta Observador quando incerto (não-determinístico)
- Observador responde com insights, não comandos
- Orquestrador mantém autonomia sobre decisões

**Exemplo de consulta:**
```
Orquestrador detecta mudança de direção
↓
Consulta Observador: "Conceitos anteriores ainda relevantes?"
↓
Observador responde: {relevance: "Parcial", suggestion: "...", confidence: 0.8}
↓
Orquestrador decide baseado em insight + própria análise
```

---

## Separação Orquestrador ↔ Comunicador (Futuro)

### Motivação

Atualmente, o Orquestrador acumula duas responsabilidades:

1. **Coordenação lógica:** decidir next_step, consultar agentes
2. **Comunicação:** falar com usuário, aplicar tom

Essa duplicidade:

- ❌ Mistura decisões lógicas com linguagem natural
- ❌ Dificulta implementação de personas customizáveis
- ❌ Reduz testabilidade (lógica + linguagem juntas)

### Arquitetura Futura

**Orquestrador (Coordenação Lógica):**

- Recebe contexto neutro do Comunicador
- Coordena Observador, Memory Agent, outros agentes
- Decide next_step baseado em lógica pura
- Retorna decisão neutra (JSON, sem linguagem)

**Comunicador (Interface Linguística):**

- Recebe mensagem do usuário
- Extrai intent e contexto neutro
- Envia para Orquestrador
- Recebe decisão neutra do Orquestrador
- Traduz para linguagem natural (aplica persona)
- Responde ao usuário

### Exemplo de Separação

**Hoje (Orquestrador faz tudo):**

```python
def processar_turno(mensagem_usuario):
    # Orquestrador processa E responde
    if "ideia de produtividade" in mensagem_usuario:
        contexto = buscar_em_historico("produtividade")
        return f"Ah, claro! 😊 A gente estava explorando {contexto}..."
        # ↑ Lógica + linguagem misturadas
```

**Futuro (Separado):**

```python
# Comunicador extrai intent
def comunicador_recebe(mensagem_usuario):
    return {
        "intent": "recall_previous_topic",
        "topic": "produtividade"
    }

# Orquestrador decide (neutro, sem linguagem)
def orquestrador_decide(contexto_neutro):
    contexto = memory_agent.query(contexto_neutro["topic"])
    return {
        "action": "recall_context",
        "content": contexto,
        "next_step": "perguntar_se_quer_retomar"
    }

# Comunicador traduz (aplica persona)
def comunicador_traduz(decisao, persona="amigável"):
    if persona == "amigável":
        return f"Ah, claro! 😊 A gente estava explorando {decisao['content']}..."
    elif persona == "formal":
        return f"Certamente. Estávamos discutindo {decisao['content']}..."
```

### Benefícios da Separação

1. **Neutralidade:** Orquestrador toma decisões sem viés linguístico
2. **Customização:** Comunicador aplica personas facilmente (Épico 18)
3. **Testabilidade:** Testar lógica pura (Orquestrador) vs tradução (Comunicador)
4. **Rastreabilidade:** Bastidores transparentes mostram decisão lógica separada de tradução
5. **Manutenção:** Alterar tom/persona não afeta lógica de decisão

### Status de Implementação

- [ ] Memory Agent criado
- [ ] Comunicador criado
- [ ] Orquestrador refatorado (decisões neutras)
- [ ] Integração Orquestrador ↔ Comunicador
- [ ] Épico 18: Personas customizáveis

**Prioridade:** Após Memory Agent e Épico 13 (Conceitos)

---

## Estado e LangGraph

- O estado da conversa está definido em `orchestrator/state.py` utilizando TypedDict
- Campos principais:
  - `messages`: histórico completo trocado entre usuário, orquestrador e agentes
  - `current_agent`: nome do agente ativo (ou `None`)
  - `last_decision`: registro estruturado da decisão anterior
  - `metadata`: métricas auxiliares (tokens, duração, etc.)
  - `focal_argument`: Argumento focal extraído/atualizado (OBRIGATÓRIO)
  - `cognitive_model`: Modelo cognitivo do argumento (Épico 9.1 - OBRIGATÓRIO)
  - `next_step`: Próxima ação ("explore", "suggest_agent", "clarify")
- LangGraph é responsável por aplicar updates imutáveis ao estado, garantindo consistência

---

## Comportamento Conversacional

O Orquestrador opera em três modos principais:

- **"explore":** Fazer perguntas abertas para entender contexto
- **"suggest_agent":** Sugerir agente específico com justificativa
- **"clarify":** Esclarecer ambiguidade ou contradição detectada

### Exemplo de Uso

```python
>>> state = create_initial_multi_agent_state("Observei que LLMs aumentam produtividade", "session-1")
>>> result = orchestrator_node(state)
>>> result['focal_argument']['intent']
'unclear'
>>> result['focal_argument']['subject']
'LLMs impact on productivity'
>>> result['next_step']
'explore'
```

---

## Logs e Observabilidade

- `INFO`: registra decisões tomadas e agentes acionados
- `DEBUG`: inclui prompts completos e respostas brutas (ativado via flag `--verbose`)
- Estrutura JSON sugerida:

```json
{
  "timestamp": "2025-11-06T10:30:00",
  "level": "INFO",
  "component": "orchestrator",
  "action": "decision",
  "data": {
    "input": "...",
    "decision": "call_agent",
    "agent": "methodologist"
  }
}
```

---

## Tratamento de Erros

- Sempre encapsule falhas de agentes e API em mensagens claras para a CLI
- Utilize retry com backoff exponencial (3 tentativas) para conversas com a API
- Se todas as tentativas falharem, registre em `ERROR` e retorne instruções amigáveis ao usuário para tentar novamente

---

## Referências

- `core/docs/agents/overview.md` - Visão geral do sistema multi-agente
- `core/docs/agents/observer.md` - Sinaliza necessidade de consulta a Memory
- `core/docs/agents/memory_agent.md` - Consultado quando necessário
- `core/docs/agents/communicator.md` - Separação futura
- `../docs/architecture/agents/orchestrator/conversational/` - Documentação completa do Orquestrador Conversacional
- `../docs/architecture/agents/orchestrator/socratic.md` - Orquestrador socrático (evolução)
- `agents/orchestrator/nodes.py` - Implementação do nó principal
- `agents/orchestrator/state.py` - Definição do estado
- `agents/orchestrator/router.py` - Roteamento entre agentes
- `config/agents/orchestrator.yaml` - Configuração e prompts do Orquestrador

---

**Versão:** 2.0  
**Data:** 05/12/2025  
**Status:** Atualizado - Evolução planejada documentada, Memory Agent e separação Comunicador adicionados

