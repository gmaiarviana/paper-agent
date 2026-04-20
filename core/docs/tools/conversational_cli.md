# CLI Conversacional - Especificação Técnica

**Versão:** 1.0  
**Data:** 15/11/2025  
**Status:** Especificação para Protótipo (Épico 7)

## 1. Visão Geral
- CLI com múltiplos turnos de conversa
- Mantém contexto ao longo da sessão
- Substitui modelo "input único → fim" por chat contínuo

## 2. Problema Atual (POC)
**Fluxo atual:**
[CLI inicia]
📝 Digite sua hipótese: tdd reduz bugs
🔬 Analisando hipótese...
Sistema: "Interessante! Me conte mais..."
📝 Digite sua hipótese: <volta pro início, perde contexto>

**Limitações:**
- Cada input é nova sessão
- Contexto não preservado
- Orquestrador pede "me conte mais" mas CLI não permite responder

## 3. Solução Proposta (Protótipo)

**Novo fluxo:**
[CLI inicia]
Sistema: Olá! Me conte sobre sua ideia ou observação.
Você: tdd reduz bugs
Sistema: Interessante! Em que contexto você notou isso?
Você: na minha equipe Python
Sistema: E como mediu redução de bugs?
Você: impressão geral, bugs caíram
Sistema: Vou organizar isso em uma questão de pesquisa estruturada.
[Sistema chama Estruturador automaticamente...]
Sistema: Organizei sua ideia assim: "TDD reduz densidade de bugs em equipes Python?" Isso captura o que você quer?

## 4. Implementação Técnica

### Loop Conversacional

**Código proposto:**
```python
def run_conversational_cli():
    """Loop conversacional contínuo."""
    thread_id = f"cli-session-{uuid.uuid4()}"
    
    print("Sistema: Olá! Me conte sobre sua ideia ou observação.")
    
    while True:
        # Input do usuário
        user_input = input("\nVocê: ").strip()
        
        if user_input.lower() in ['exit', 'sair']:
            print("Sistema: Até logo!")
            break
        
        # Invocar grafo
        result = graph.invoke(
            {"user_input": user_input},
            config={"configurable": {"thread_id": thread_id}}
        )
        
        # Exibir resposta
        orchestrator_output = result.get('orchestrator_output', {})
        message = orchestrator_output.get('message', '')
        next_step = orchestrator_output.get('next_step', '')
        
        # Transparência (opcional)
        if verbose_mode:
            reasoning = orchestrator_output.get('reasoning', '')
            print(f"\n🧠 Raciocínio: {reasoning}")
        
        print(f"\nSistema: {message}")
        
        # Decidir próximo passo
        if next_step == "suggest_agent":
            # Agente trabalhou nos bastidores, Orquestrador apresentou resultado curado
            # Usuário pode confirmar entendimento ou pedir ajustes
            # (Chamada automática já aconteceu no grafo)
            continue
        
        # Se next_step == "explore", loop continua normalmente
```

### Preservação de Contexto

**Thread ID:**
- Gerado uma vez no início da sessão
- Passado em toda invocação do grafo
- LangGraph usa para recuperar histórico completo

**Estado compartilhado:**
- `MultiAgentState` acumula `conversation_history`
- Orquestrador tem acesso a todos os turnos anteriores
- Análise contextual considera histórico completo

## 5. Transparência do Raciocínio

**3 níveis de transparência:**

### Nível 1: CLI Padrão (limpo)
Você: tdd reduz bugs
Sistema: Interessante! Em que contexto você notou isso?

### Nível 2: CLI Verbose (flag `--verbose`)
Você: tdd reduz bugs
🧠 Raciocínio: Input vago sobre TDD. Preciso contexto: onde observou,
como mediu, qual população. Não tenho informação suficiente para
sugerir agente ainda.
Sistema: Interessante! Em que contexto você notou isso?

### Nível 3: Dashboard (sempre disponível)
- EventBus emite eventos com reasoning completo
- Dashboard Streamlit exibe timeline com reasoning de cada turno
- Usa infraestrutura existente do Épico 5

**Implementação:**
```python
# CLI emite evento
event_bus.publish_agent_started(
    session_id=thread_id,
    agent="orchestrator",
    metadata={"reasoning": orchestrator_output['reasoning']}
)

# Dashboard consome
events = event_bus.get_session_events(thread_id)
for event in events:
    if event['agent'] == 'orchestrator':
        st.write(f"🧠 {event['metadata']['reasoning']}")
```

## 6. Detecção de Momento Certo

**Lógica não-determinística:**
- LLM julga se tem informação suficiente
- Não usa checklist rígida de campos obrigatórios
- Considera qualidade e quantidade de contexto

**Prompt do Orquestrador:**
Analise o histórico da conversa. Você tem CONTEXTO SUFICIENTE para
sugerir agente quando:

Conversa acumulou detalhes relevantes (não precisa estar perfeito)
Usuário deu informações que permitem próximo passo útil
Chamar agente agora agregaria valor (não apenas "seguir protocolo")

Use julgamento baseado em contexto, não checklist rígida.
Se contexto suficiente: next_step = "suggest_agent"
Se precisa mais info: next_step = "explore"

## 7. Critérios de Aceite

**Funcionalidade:**
- [x] CLI mantém conversa por N turnos (não volta para prompt inicial)
- [x] Thread ID preservado ao longo da sessão
- [x] Orquestrador acessa histórico completo
- [x] Sistema detecta "momento certo" para sugerir agente
- [x] Usuário pode aceitar ou recusar sugestão de chamar agente

**Transparência:**
- [x] CLI padrão exibe apenas mensagem limpa
- [x] Flag `--verbose` exibe reasoning inline
- [x] EventBus emite eventos com reasoning
- [ ] Dashboard consome e exibe reasoning (validar manualmente)

**Experiência:**
- [x] Conversa flui naturalmente (sem quebras)
- [x] Sistema faz perguntas relevantes (depende do prompt do Orquestrador)
- [x] Sugestões de agentes fazem sentido no contexto (depende do prompt)

**Status:** ✅ Protótipo Implementado (15/11/2025)

## 8. Comandos de Execução
```bash
# Modo padrao (CLI limpa)
python -m core.tools.cli.chat

# Modo verbose (exibe reasoning)
python -m core.tools.cli.chat --verbose

# Dashboard (reasoning sempre visível)
streamlit run products/revelar/app/dashboard.py
```

---

**Referências:**
- `../docs/architecture/agents/orchestrator/conversational/` - Lógica do Orquestrador
- `ROADMAP.md` - Épico 7 Protótipo
- `core/docs/tools/cli.md` - CLI original (antes do Épico 7)

