# Comunicador (Interface Linguística)

## Visão Geral

O **Comunicador** é responsável pela interface linguística entre o sistema e o usuário. Separado do Orquestrador para garantir **neutralidade nas decisões** e **customização de personas**.

## Status

⚠️ **CONCEITUAL - NÃO IMPLEMENTADO**

Este documento descreve a visão futura do Comunicador. Atualmente, o Orquestrador acumula responsabilidades de coordenação lógica E comunicação com usuário.

## Filosofia

### Analogia: Área de Broca (Linguagem) vs Córtex Pré-frontal (Decisão)

No cérebro humano:
- **Área de Broca**: produz linguagem, traduz pensamentos em palavras
- **Córtex Pré-frontal**: toma decisões, coordena ações

No sistema:
- **Comunicador** = Área de Broca (traduz decisões em linguagem)
- **Orquestrador** = Córtex Pré-frontal (coordena, decide)

### Problema que Resolve

**Sem separação:**
Orquestrador atual:
├─ Responsabilidade 1: Coordenar agentes (lógica)
├─ Responsabilidade 2: Falar com usuário (linguagem)
└─ Problema: Decisões lógicas misturadas com tom/persona

**Exemplo de viés indesejado:**
```python
# Orquestrador mistura lógica com linguagem
orquestrador.decide(
    action="consultar_memory",
    user_message="E aquela ideia de produtividade?"
)

# Resposta mistura decisão com tom
response = "Ah, claro! 😊 Deixa eu buscar aqui... [consulta Memory]... 
            A gente estava explorando LLMs e produtividade..."
            
# Problema: Tom ("Ah, claro! 😊") está hard-coded na lógica
```

**Com separação:**
```python
# Orquestrador trabalha apenas com fatos neutros
orquestrador.decide(
    action="recall_previous_topic",
    topic="produtividade",
    context_needed=True
)
# Retorna decisão neutra: {"action": "recall", "content": {...}}

# Comunicador traduz para linguagem natural
comunicador.translate(
    decision={"action": "recall", "content": {...}},
    persona="amigável"  # ou "formal", "técnico", etc.
)
# Retorna: "Ah, claro! 😊 A gente estava explorando..."
```

## Responsabilidades

### 1. Receber Mensagem do Usuário
```python
# Interface pública
user_message = "E aquela ideia de produtividade?"

# Comunicador recebe e normaliza
comunicador.receive(user_message)
```

### 2. Traduzir para Contexto Neutro
```python
# Comunicador extrai intent e contexto NEUTRO
contexto_neutro = comunicador.parse_intent(user_message)

# Output:
{
    "intent": "recall_previous_topic",
    "topic": "produtividade",
    "context": {
        "usuario_quer_retomar": True,
        "mencionou_palavra_chave": "ideia"
    },
    "raw_message": "E aquela ideia de produtividade?"  # preserva literal
}
```

**Importante**: Contexto neutro não contém tom, emoção, ou interpretação subjetiva. Apenas fatos objetivos.

### 3. Enviar para Orquestrador
```python
# Comunicador envia contexto neutro para Orquestrador
orquestrador.process(contexto_neutro)
```

### 4. Receber Decisão do Orquestrador
```python
# Orquestrador processa, consulta Memory, decide
decisao = orquestrador.decide(contexto_neutro)

# Output (neutro, sem linguagem):
{
    "action": "recall_context",
    "content": {
        "topic": "produtividade",
        "previous_discussion": {
            "turns": "1-12",
            "claim": "LLMs aumentam produtividade",
            "status": "em construção"
        }
    },
    "next_step": "perguntar_se_quer_retomar"
}
```

### 5. Traduzir para Linguagem Natural
```python
# Comunicador recebe decisão neutra
response = comunicador.translate_to_natural_language(
    decision=decisao,
    persona="amigável",  # configurável
    context=conversa_atual
)

# Output (com linguagem, tom, persona):
"Ah, a gente estava explorando como LLMs poderiam aumentar 
produtividade em equipes Python. Você quer retomar essa ideia 
ou prefere manter foco em bugs?"
```

### 6. Responder ao Usuário
```python
# Comunicador envia resposta formatada
comunicador.send(response, usuario)
```

## Fluxo Completo
┌─────────────────────────────────────────────────┐
│                   USUÁRIO                        │
│  "E aquela ideia de produtividade?"              │
└────────────────┬─────────────────────────────────┘
↓
┌─────────────────────────────────────────────────┐
│                COMUNICADOR                       │
│  1. Recebe mensagem                              │
│  2. Normaliza input                              │
│  3. Extrai intent e contexto NEUTRO              │
│     {                                            │
│       "intent": "recall_previous_topic",         │
│       "topic": "produtividade",                  │
│       "context": {...}                           │
│     }                                            │
└────────────────┬─────────────────────────────────┘
↓
┌─────────────────────────────────────────────────┐
│               ORQUESTRADOR                       │
│  1. Recebe contexto neutro                       │
│  2. Detecta: foco atual = "bugs"                 │
│  3. Observador sinaliza: mudança de tópico       │
│  4. Decide: consultar Memory                     │
│  5. Memory retorna contexto histórico            │
│  6. Decide: next_step = "perguntar_se_quer_retomar" │
│  7. Retorna decisão NEUTRA                       │
│     {                                            │
│       "action": "recall_context",                │
│       "content": {...},                          │
│       "next_step": "perguntar_se_quer_retomar"   │
│     }                                            │
└────────────────┬─────────────────────────────────┘
↓
┌─────────────────────────────────────────────────┐
│                COMUNICADOR                       │
│  1. Recebe decisão neutra                        │
│  2. Aplica persona configurada ("amigável")      │
│  3. Traduz para linguagem natural                │
│     "Ah, a gente estava explorando LLMs..."      │
│  4. Formata resposta                             │
└────────────────┬─────────────────────────────────┘
↓
┌─────────────────────────────────────────────────┐
│                   USUÁRIO                        │
│  Recebe resposta formatada                       │
└─────────────────────────────────────────────────┘

## Separação de Responsabilidades

### ❌ O que Comunicador NÃO faz:

- Não toma decisões sobre next_step
- Não consulta Memory
- Não coordena outros agentes
- Não mantém CognitiveModel
- Não detecta incongruências

### ✅ O que Comunicador FAZ:

- Recebe mensagem do usuário
- Extrai intent e contexto neutro
- Traduz decisões neutras para linguagem natural
- Aplica personas customizáveis
- Formata resposta
- Envia resposta ao usuário

### Comparação: Orquestrador vs Comunicador

| Aspecto | Orquestrador | Comunicador |
|---------|--------------|-------------|
| **Natureza** | Lógica, decisões | Linguística, tradução |
| **Input** | Contexto neutro | Mensagem do usuário |
| **Processamento** | Coordena agentes, decide | Extrai intent, aplica persona |
| **Output** | Decisão neutra (JSON) | Linguagem natural (string) |
| **Depende de** | Observador, Memory | Orquestrador |
| **Tom/Persona** | Nenhum (neutro) | Sim (customizável) |
| **Testabilidade** | Alta (lógica pura) | Moderada (depende de LLM) |

## Benefícios da Separação

### 1. Neutralidade nas Decisões

**Problema sem separação:**
```python
# Orquestrador mistura lógica com linguagem
if usuario_pergunta_sobre_passado:
    resposta = "Ah, você quer saber sobre aquilo? 😊"  # tom hard-coded
    consultar_memory()
```

**Solução com separação:**
```python
# Orquestrador: decisão neutra
if intent == "recall":
    return {"action": "recall", "topic": topic}  # sem tom

# Comunicador: aplica persona
if persona == "amigável":
    return "Ah, você quer saber sobre aquilo? 😊"
elif persona == "formal":
    return "Vejo que você deseja revisar um tópico anterior."
```

### 2. Customização de Personas (Épico 18)
```python
# Configuração de personas
personas = {
    "amigável": {
        "tom": "casual, empático",
        "emojis": True,
        "tratamento": "você",
        "exemplo": "Ah, claro! 😊 A gente estava explorando..."
    },
    "formal": {
        "tom": "profissional, objetivo",
        "emojis": False,
        "tratamento": "senhor/senhora",
        "exemplo": "Certamente. Estávamos discutindo..."
    },
    "técnico": {
        "tom": "preciso, detalhado",
        "emojis": False,
        "tratamento": "você",
        "exemplo": "Contexto recuperado: Turnos 1-12, claim em construção."
    },
    "socrático": {
        "tom": "questionador, provocativo",
        "emojis": False,
        "tratamento": "você",
        "exemplo": "Por que você quer retomar produtividade agora? O que mudou?"
    }
}

# Usuário escolhe persona
usuario.config.persona = "socrático"

# Comunicador aplica automaticamente
comunicador.set_persona(usuario.config.persona)
```

### 3. Rastreabilidade (Bastidores Transparentes)

Com separação, bastidores mostram:
🔍 [Bastidores]
├─ Comunicador recebeu: "E aquela ideia de produtividade?"
├─ Intent extraído: recall_previous_topic
├─ Orquestrador decidiu: consultar Memory
├─ Memory retornou: Turnos 1-12 (LLMs e produtividade)
├─ Orquestrador decidiu: perguntar se quer retomar
└─ Comunicador traduziu para persona "amigável"

**Transparência**: Usuário vê decisões lógicas separadas de tradução linguística.

### 4. Testabilidade

**Testar Orquestrador (lógica pura):**
```python
def test_orquestrador_recall():
    contexto = {
        "intent": "recall_previous_topic",
        "topic": "produtividade"
    }
    
    decisao = orquestrador.process(contexto)
    
    assert decisao["action"] == "recall_context"
    assert decisao["next_step"] == "perguntar_se_quer_retomar"
    # Não precisa testar linguagem, apenas lógica
```

**Testar Comunicador (tradução):**
```python
def test_comunicador_persona_amigavel():
    decisao = {
        "action": "recall_context",
        "content": {"topic": "produtividade"}
    }
    
    resposta = comunicador.translate(decisao, persona="amigável")
    
    assert "😊" in resposta  # emojis esperados
    assert "a gente" in resposta.lower()  # tom casual
```

## Integração com Épico 18 (Personas)

### Épico 18: Personas Customizáveis

**Objetivo**: Permitir que usuário escolha como o sistema se comunica.

**Personas planejadas:**
1. **Amigável**: casual, empático, usa emojis
2. **Formal**: profissional, objetivo, sem emojis
3. **Técnico**: preciso, detalhado, usa jargão
4. **Socrático**: questionador, provocativo, estimula reflexão
5. **Minimalista**: respostas curtas, direto ao ponto

**Com Comunicador separado, implementar Épico 18 é trivial:**
```python
# Usuário escolhe persona na UI
usuario.config.persona = "socrático"

# Sistema aplica automaticamente
comunicador.set_persona(usuario.config.persona)

# Todas as respostas seguem persona escolhida
# Sem modificar NENHUMA lógica do Orquestrador
```

**Sem Comunicador separado, Épico 18 seria:**
- Modificar Orquestrador para suportar múltiplas personas
- Misturar lógica de decisão com lógica de linguagem
- Alto acoplamento, difícil manutenção

## Implementação Futura

### Tecnologias Candidatas

**LLM para tradução:**
- Claude Haiku (rápido, barato, suficiente para tradução)
- GPT-3.5-turbo (alternativa)
- Llama 3 local (privacy, sem custo de API)

**Templates de Persona:**
- Jinja2: templates estruturados
- Few-shot prompting: exemplos de cada persona
- Chain-of-Thought: raciocínio sobre tom apropriado

**Cache:**
- Redis: cache de traduções frequentes
- Reduz latência de 500ms → 50ms para respostas comuns

### Arquitetura Técnica
```python
class Comunicador:
    def __init__(self, llm_model="claude-haiku", default_persona="amigável"):
        self.llm = llm_model
        self.persona = default_persona
        self.cache = RedisCache()
    
    def receive(self, user_message: str) -> dict:
        """Recebe mensagem, extrai intent neutro"""
        intent = self.extract_intent(user_message)
        return {
            "intent": intent["type"],
            "context": intent["context"],
            "raw_message": user_message
        }
    
    def extract_intent(self, message: str) -> dict:
        """Usa LLM para extrair intent SEM interpretação subjetiva"""
        prompt = f"""
        Extraia o intent OBJETIVO desta mensagem (sem tom ou emoção):
        
        Mensagem: "{message}"
        
        Retorne JSON:
        {{
            "type": "recall" | "clarify" | "continue" | "new_topic",
            "context": {{...dados objetivos...}}
        }}
        """
        return self.llm.complete(prompt, response_format="json")
    
    def translate_to_natural_language(
        self, 
        decision: dict, 
        persona: str
    ) -> str:
        """Traduz decisão neutra para linguagem natural com persona"""
        
        # Check cache
        cache_key = f"{decision['action']}:{persona}"
        if cached := self.cache.get(cache_key):
            return cached
        
        # Generate translation
        persona_config = self.get_persona_config(persona)
        prompt = f"""
        Traduza esta decisão para linguagem natural:
        
        Decisão: {json.dumps(decision)}
        
        Persona: {persona}
        Tom: {persona_config['tom']}
        Emojis: {persona_config['emojis']}
        
        Gere resposta que:
        1. Comunique a decisão claramente
        2. Siga o tom da persona
        3. Seja natural e conversacional
        """
        
        response = self.llm.complete(prompt)
        self.cache.set(cache_key, response, ttl=3600)
        return response
```

### Métricas de Sucesso

- **Consistência de persona**: >95% das respostas seguem tom configurado
- **Latência de tradução**: <200ms (P95) com cache
- **Satisfação do usuário**: >80% preferem persona customizada vs padrão
- **Separação limpa**: 0 referências a "linguagem" no código do Orquestrador

## Migração Gradual

### Fase 1: Comunicador passivo (atual → futuro)
Orquestrador atual:
├─ Coordena agentes
└─ Fala com usuário
Comunicador (novo, passivo):
├─ Recebe decisão do Orquestrador
└─ Apenas formata resposta (sem lógica)

### Fase 2: Comunicador ativo
Orquestrador:
├─ Coordena agentes
└─ Envia decisão neutra ao Comunicador
Comunicador:
├─ Extrai intent do usuário
├─ Envia contexto neutro ao Orquestrador
├─ Recebe decisão neutra
└─ Traduz para linguagem natural

### Fase 3: Personas customizáveis (Épico 18)
Comunicador:
├─ Suporta múltiplas personas
├─ Usuário escolhe via UI
└─ Aplica automaticamente

## Referências

- `docs/agents/orchestrator.md` - Quem coordena, não quem fala
- `docs/features/transparent_backstage.md` - Rastreamento de traduções
- `ROADMAP.md` - Épico 18 (Personas)
- `../architecture/vision/super_system.md` - Separação de responsabilidades

---

**Status**: Conceitual, aguardando implementação
**Prioridade**: Média (após Memory Agent e Épico 13)
**Complexidade**: Média (novo agente, refatoração do Orquestrador)
**Benefício**: Alto (neutralidade, customização, testabilidade)

