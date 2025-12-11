# Bastidores Transparentes (Transparent Backstage)

## Visão Geral

**Bastidores Transparentes** é um diferencial do produto que permite ao usuário ver **como o sistema pensa** e toma decisões. Enquanto a maioria dos sistemas de IA é uma "caixa preta", este sistema oferece transparência opcional sobre seu raciocínio interno.

## Status

⚠️ **CONCEITUAL - NÃO IMPLEMENTADO**

Este documento descreve a visão futura da feature. Atualmente, o sistema opera sem rastreamento de decisões internas.

## Filosofia

### Transparência como Diferencial

**Problema comum em sistemas de IA:**
Usuário: "Por que você disse isso?"
Sistema: [sem resposta, decisões são opacas]
Usuário: [frustrado, não confia no sistema]

**Com Bastidores Transparentes:**
Usuário: "Por que você disse isso?"
Sistema: [mostra exatamente o raciocínio]
├─ Observador detectou mudança de foco
├─ Orquestrador consultou Memory
├─ Memory retornou contexto dos Turnos 1-12
└─ Decisão: sugerir retomar discussão anterior
Usuário: [entende, confia, pode questionar se discordar]

### Princípios

1. **Opt-in, não opt-out**: Transparência não deve distrair usuário por padrão
2. **Resumo primeiro, detalhes depois**: Mostrar essência, permitir aprofundamento
3. **Linguagem natural**: Explicar decisões em português, não JSON técnico
4. **Rastreabilidade completa**: Toda decisão é rastreável até sua origem

## Funcionalidade

### Modo Default (Bastidores Ocultos)
┌────────────────────────────────────────────────┐
│ 💬 Conversa                                     │
├────────────────────────────────────────────────┤
│ Você: E aquela ideia de produtividade?         │
│                                                 │
│ Assistente: Ah, a gente estava explorando como │
│ LLMs poderiam aumentar produtividade em equipes│
│ Python. Você quer retomar essa ideia?          │
│                                                 │
│ [Bastidores ocultos - usuário vê apenas conversa natural]
└────────────────────────────────────────────────┘

### Modo Ativado (Bastidores Visíveis)
┌────────────────────────────────────────────────┐
│ 💬 Conversa                                     │
├────────────────────────────────────────────────┤
│ Você: E aquela ideia de produtividade?         │
│                                                 │
│ 🔍 [Bastidores - clique para expandir] ▼       │
│   ├─ Observador detectou: mudança de foco      │
│   │  └─ Foco anterior: bugs                    │
│   │  └─ Foco novo detectado: produtividade     │
│   ├─ Orquestrador consultou Memory             │
│   │  └─ Query: "discussões sobre produtividade"│
│   │  └─ Latência: 180ms                        │
│   ├─ Memory retornou: Turnos 1-12              │
│   │  └─ Claim em construção: "LLMs aumentam    │
│   │     produtividade"                          │
│   └─ Orquestrador decidiu: sugerir retomar     │
│       discussão anterior                        │
│                                                 │
│ Assistente: Ah, a gente estava explorando como │
│ LLMs poderiam aumentar produtividade em equipes│
│ Python. Você quer retomar essa ideia?          │
└────────────────────────────────────────────────┘

## O que é Rastreado

### 1. Detecções do Observador
```json
{
  "agent": "observador",
  "turn": 15,
  "action": "detectou_incongruencia",
  "context": {
    "turno_atual": "bugs aumentaram",
    "cognitive_model": "baseline_bugs='estável'",
    "tipo": "possivel_contradicao"
  },
  "signal_to": "orquestrador",
  "timestamp": "2024-12-10T14:30:15Z"
}
```

**Exibido ao usuário:**
🔍 Observador detectou possível contradição
├─ Você disse: "bugs aumentaram"
├─ Contexto anterior indicava: "bugs estáveis"
└─ Sinalizado ao Orquestrador para verificar

### 2. Consultas a Memory Agent
```json
{
  "agent": "memory_agent",
  "turn": 15,
  "action": "query",
  "input": {
    "query": "buscar menções a 'bugs' nos últimos 20 turnos",
    "strategy": "superficial_first",
    "requested_by": "orquestrador"
  },
  "output": {
    "layer": "superficial",
    "results": [
      {
        "turn_range": "3-3",
        "summary": "Bugs estáveis há 6 meses",
        "score": 0.89
      },
      {
        "turn_range": "15-15",
        "summary": "Bugs aumentaram 20% no último mês",
        "score": 0.92
      }
    ],
    "latency_ms": 180
  },
  "timestamp": "2024-12-10T14:30:15Z"
}
```

**Exibido ao usuário:**
🔍 Orquestrador consultou Memory
├─ Busca: "menções a 'bugs' nos últimos 20 turnos"
├─ Camada: Superficial (busca rápida)
├─ Encontrado:
│  ├─ Turno 3: "Bugs estáveis há 6 meses"
│  └─ Turno 15: "Bugs aumentaram 20% no último mês"
├─ Conclusão: Períodos diferentes, não contradição
└─ Latência: 180ms

### 3. Decisões do Orquestrador
```json
{
  "agent": "orquestrador",
  "turn": 15,
  "action": "decidiu_next_step",
  "input": {
    "signal_from": "observador",
    "memory_context": {...},
    "cognitive_model": {...}
  },
  "decision": {
    "action": "continuar_sem_perguntar",
    "reasoning": "Contexto recuperado de Memory confirma: períodos diferentes, não contradição",
    "next_step": "processar_turno_normalmente"
  },
  "timestamp": "2024-12-10T14:30:16Z"
}
```

**Exibido ao usuário:**
🔍 Orquestrador decidiu: continuar sem perguntar
├─ Raciocínio: "Períodos diferentes, não contradição"
├─ Ação: processar turno normalmente
└─ Não foi necessário interromper a conversa

### 4. Traduções do Comunicador (Futuro)
```json
{
  "agent": "comunicador",
  "turn": 15,
  "action": "traduziu_decisao",
  "input": {
    "decision_neutra": {
      "action": "recall_context",
      "content": "..."
    },
    "persona": "amigável"
  },
  "output": {
    "resposta": "Ah, a gente estava explorando...",
    "tom_aplicado": "casual, empático",
    "emojis_usados": ["😊"]
  },
  "timestamp": "2024-12-10T14:30:16Z"
}
```

**Exibido ao usuário:**
🔍 Comunicador traduziu para linguagem natural
├─ Decisão neutra recebida do Orquestrador
├─ Persona aplicada: "amigável"
├─ Tom: casual, empático
└─ Resposta gerada com emoji 😊

## Níveis de Detalhamento

### Nível 1: Resumo (Padrão quando ativado)
🔍 [Bastidores]
├─ Observador detectou: mudança de foco
├─ Orquestrador consultou Memory
└─ Memory recuperou: Turnos 1-12

**Características:**
- Linguagem natural
- Uma linha por ação
- Fácil de escanear rapidamente
- Suficiente para 80% dos casos

### Nível 2: Detalhes (Expandível)
🔍 [Bastidores - Detalhes] ▼
├─ Observador detectou: mudança de foco
│  ├─ Foco anterior: bugs
│  ├─ Foco novo: produtividade
│  ├─ Confiança: 0.87
│  └─ Sinalizado ao Orquestrador
│
├─ Orquestrador consultou Memory
│  ├─ Query: "discussões sobre produtividade"
│  ├─ Estratégia: superficial_first
│  ├─ Latência: 180ms
│  └─ Resultados: 3 encontrados
│
└─ Memory retornou: Turnos 1-12
├─ Camada: Superficial
├─ Claim em construção: "LLMs aumentam produtividade"
├─ Proposições: 4 identificadas
└─ Score de relevância: 0.92

**Características:**
- Mais contexto por ação
- Métricas técnicas (latência, scores)
- Estrutura hierárquica
- Para usuários avançados ou debugging

### Nível 3: Técnico (JSON completo)
```json
🔍 [Bastidores - Técnico] ▼

{
  "backstage_trace": [
    {
      "agent": "observador",
      "turn": 15,
      "action": "detectou_mudanca_foco",
      "context": {
        "foco_anterior": "bugs",
        "foco_novo": "produtividade",
        "confianca": 0.87
      },
      "signal_to": "orquestrador",
      "timestamp": "2024-12-10T14:30:15.123Z"
    },
    {
      "agent": "orquestrador",
      "turn": 15,
      "action": "consultou_memory",
      "input": {
        "query": "discussões sobre produtividade",
        "strategy": "superficial_first"
      },
      "latency_ms": 180,
      "timestamp": "2024-12-10T14:30:15.456Z"
    },
    {
      "agent": "memory_agent",
      "turn": 15,
      "action": "query_executed",
      "output": {
        "layer": "superficial",
        "results": [
          {
            "turn_range": "1-12",
            "claim": "LLMs aumentam produtividade",
            "proposicoes": 4,
            "score": 0.92
          }
        ]
      },
      "timestamp": "2024-12-10T14:30:15.636Z"
    }
  ]
}
```

**Características:**
- JSON completo
- Timestamps precisos
- Todos os metadados
- Para desenvolvedores ou auditoria

## Interface do Usuário (Mockup)

### Toggle de Ativação
┌────────────────────────────────────────────────┐
│ ⚙️ Configurações                                │
├────────────────────────────────────────────────┤
│                                                 │
│ 🔍 Bastidores Transparentes                    │
│                                                 │
│ ○ Desativado (padrão)                          │
│   └─ Conversa limpa, sem distrações            │
│                                                 │
│ ● Ativado - Resumo                             │
│   └─ Mostra decisões principais                │
│                                                 │
│ ○ Ativado - Detalhes                           │
│   └─ Mostra métricas e contexto completo       │
│                                                 │
│ ○ Ativado - Técnico (JSON)                     │
│   └─ Mostra trace completo para debugging      │
│                                                 │
└────────────────────────────────────────────────┘

### Exibição em Conversa
┌────────────────────────────────────────────────┐
│ 💬 Conversa com Assistente                     │
├────────────────────────────────────────────────┤
│                                                 │
│ [Turno 14]                                      │
│ Você: Foco em bugs agora                        │
│                                                 │
│ Assistente: Certo, vamos focar em bugs então.   │
│                                                 │
│ ─────────────────────────────────────────────  │
│                                                 │
│ [Turno 15]                                      │
│ Você: E aquela ideia de produtividade?         │
│                                                 │
│ 🔍 [Bastidores] ▼ (clique para expandir)       │
│                                                 │
│ Assistente: Ah, a gente estava explorando como │
│ LLMs poderiam aumentar produtividade...        │
│                                                 │
│ ─────────────────────────────────────────────  │
│                                                 │
│ [Ícone de bastidores só aparece quando há      │
│  rastreamento relevante para aquele turno]     │
│                                                 │
└────────────────────────────────────────────────┘

### Expansão de Bastidores
┌────────────────────────────────────────────────┐
│ 🔍 [Bastidores - Turno 15] ▲ (clique para colapsar)
├────────────────────────────────────────────────┤
│                                                 │
│ 1️⃣ Observador detectou: mudança de foco        │
│    ├─ Foco anterior: bugs                      │
│    ├─ Foco novo: produtividade                 │
│    └─ Sinalizado ao Orquestrador               │
│                                                 │
│ 2️⃣ Orquestrador consultou Memory               │
│    ├─ Query: "discussões sobre produtividade"  │
│    └─ Latência: 180ms                          │
│                                                 │
│ 3️⃣ Memory retornou contexto                    │
│    ├─ Turnos 1-12 recuperados                  │
│    ├─ Claim: "LLMs aumentam produtividade"     │
│    └─ Status: em construção                    │
│                                                 │
│ 4️⃣ Orquestrador decidiu                        │
│    └─ Ação: sugerir retomar discussão anterior │
│                                                 │
│ 💡 [Ver detalhes técnicos] [Copiar JSON]       │
│                                                 │
└────────────────────────────────────────────────┘

## Benefícios

### 1. Confiança do Usuário

**Sem transparência:**
Usuário: "Por que você está perguntando isso de novo?"
Sistema: [sem resposta]
Usuário: [frustrado, perde confiança]

**Com transparência:**
Usuário: "Por que você está perguntando isso de novo?"
Sistema: [mostra bastidores]
├─ Memory consultado: definição não encontrada
└─ Decisão: perguntar para confirmar
Usuário: "Ah, entendi. Eu havia dito isso no Turno 3."
Sistema: [mostra bastidores do Turno 3]
├─ Você definiu: "Baseline é 45min"
└─ Por algum motivo, não foi armazenado no CognitiveModel
Usuário: [confia que sistema está tentando, não sendo burro]

### 2. Feedback para Melhoria

Usuário pode identificar quando sistema erra:
🔍 Observador detectou: incongruência
├─ Você disse: "população são equipes Python"
├─ CognitiveModel tinha: "população são desenvolvedores"
└─ Sinalizado ao Orquestrador
Usuário: [vê bastidores]
"Não, não é incongruência! Equipes Python SÃO desenvolvedores."
→ Feedback valioso: Observador está detectando falsos positivos
→ Sistema pode melhorar detecção de incongruências

### 3. Educação do Usuário

Usuário aprende como o sistema pensa:
🔍 Memory consultou Camada Superficial primeiro
├─ Encontrou resumo relevante
├─ Não precisou acessar Camada Profunda (mais lenta)
└─ Economia: ~800ms de latência
Usuário: [aprende que sistema tem camadas de memória]
Usuário: [entende por que às vezes é mais rápido, às vezes mais lento]

### 4. Debugging e Desenvolvimento

Desenvolvedores podem ver exatamente o que aconteceu:
Bug reportado: "Sistema não lembrou da definição de baseline"
🔍 Bastidores - Modo Técnico
├─ Turno 3: Observador processou "baseline = 45min"
├─ CognitiveModel atualizado: baseline=45min ✅
├─ Turno 10: Memory armazenou snapshot ✅
├─ Turno 25: Orquestrador consultou Memory
├─ Memory retornou: [VAZIO] ❌ ← BUG IDENTIFICADO
└─ Causa: Query mal formatada ("baselien" em vez de "baseline")
→ Bug encontrado e corrigido rapidamente

## Implementação Futura

### Arquitetura de Rastreamento
```python
class BackstageTracker:
    def __init__(self):
        self.trace = []  # Lista de eventos do turno atual
    
    def track_event(
        self,
        agent: str,
        action: str,
        context: dict,
        output: dict = None,
        reasoning: str = None
    ):
        """Rastreia um evento do sistema"""
        event = {
            "agent": agent,
            "action": action,
            "context": context,
            "output": output,
            "reasoning": reasoning,
            "timestamp": datetime.now().isoformat()
        }
        self.trace.append(event)
    
    def get_summary(self) -> str:
        """Retorna resumo em linguagem natural"""
        summary_lines = []
        for event in self.trace:
            line = self._format_event_summary(event)
            summary_lines.append(line)
        return "\n".join(summary_lines)
    
    def get_detailed(self) -> str:
        """Retorna detalhes expandidos"""
        detailed_lines = []
        for event in self.trace:
            line = self._format_event_detailed(event)
            detailed_lines.append(line)
        return "\n".join(detailed_lines)
    
    def get_json(self) -> dict:
        """Retorna trace completo em JSON"""
        return {"backstage_trace": self.trace}
```

### Integração com Agentes
```python
# Observador rastreia suas detecções
observador.detecta_incongruencia()
backstage.track_event(
    agent="observador",
    action="detectou_incongruencia",
    context={
        "turno_atual": "bugs aumentaram",
        "cognitive_model": "bugs=estável"
    },
    reasoning="Possível contradição detectada"
)

# Orquestrador rastreia consultas
orquestrador.consultar_memory(query)
backstage.track_event(
    agent="orquestrador",
    action="consultou_memory",
    context={"query": query, "strategy": "superficial_first"},
    output={"latency_ms": 180}
)

# Memory rastreia resultados
memory_agent.query(query)
backstage.track_event(
    agent="memory_agent",
    action="query_executed",
    context={"query": query, "layer": "superficial"},
    output={"results": results, "score": 0.92}
)
```

### Persistência
```python
# Salvar trace com turno
conversation.save_turn(
    turn_id=15,
    user_message="...",
    assistant_response="...",
    backstage_trace=backstage.get_json()
)

# Recuperar trace depois
trace = conversation.get_backstage_trace(turn_id=15)
```

## Métricas de Sucesso

- **Adoção**: >30% dos usuários ativam bastidores pelo menos uma vez
- **Retenção**: >60% dos que ativam continuam usando
- **Confiança**: >80% dos usuários reportam maior confiança no sistema
- **Feedback**: >50 bugs/melhorias identificados via análise de traces
- **Educação**: >70% dos usuários entendem melhor como sistema funciona

## Limitações e Considerações

### 1. Overhead de Performance

**Rastreamento adiciona latência:**
- Sem rastreamento: 500ms por turno
- Com rastreamento: 550ms por turno (+10%)

**Mitigação**: Rastreamento assíncrono (não bloqueia resposta)

### 2. Privacidade

**Traces contêm informações sensíveis:**
- Mensagens do usuário
- Decisões internas
- Contexto recuperado

**Mitigação**: 
- Traces são privados (não compartilhados)
- Usuário pode deletar traces
- Opção de desativar permanentemente

### 3. Complexidade para Usuário Leigo

**Usuário não-técnico pode não entender:**
- "Camada Superficial"
- "Score de relevância: 0.92"
- "Latência: 180ms"

**Mitigação**:
- Nível 1 (Resumo) usa linguagem não-técnica
- Níveis 2-3 para usuários avançados
- Tooltips explicam termos técnicos

## Referências

- `core/docs/agents/observer.md` - Rastreamento de detecções
- `core/docs/agents/orchestrator.md` - Rastreamento de decisões
- `core/docs/agents/memory_agent.md` - Rastreamento de consultas
- `core/docs/agents/communicator.md` - Rastreamento de traduções (futuro)
- `core/docs/architecture/data-models/ontology.md` - BackstageContext

---

**Status**: Conceitual, aguardando implementação
**Prioridade**: Média (após Memory Agent)
**Complexidade**: Média (rastreamento + UI)
**Diferencial**: Alto (transparência é rara em sistemas de IA)

