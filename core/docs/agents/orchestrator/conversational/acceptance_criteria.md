# Critérios de Aceite POC

## Funcionalidades Mínimas

✅ **Perguntas abertas (não classificação)**
- Orquestrador faz perguntas exploratórias
- Não classifica input como "vague"/"semi_formed"/"complete"
- Explora contexto antes de sugerir direções

✅ **Análise contextual (não garçom)**
- Analisa input + histórico conversacional
- Identifica padrões, lacunas, contradições
- Opina sobre direções possíveis

✅ **Chamada automática de agente**
- Chama agente automaticamente quando contexto suficiente
- Não pede permissão, age proativamente
- Transparência nos bastidores mostra quem trabalhou

✅ **Curadoria da resposta**
- Recebe resultado do agente
- Faz curadoria: apresenta em tom único e coeso
- Primeira pessoa: "Organizei...", "Validei...", "Identifiquei..."
- NÃO menciona agente na conversa principal

✅ **Confirmação de entendimento**
- Confirma entendimento, não pede permissão
- "Isso captura o que você quer?" em vez de "Posso chamar agente?"
- Usuário ajusta se necessário, sistema adapta

✅ **Detecção de mudança via LLM**
- Compara novo input com histórico
- Detecta contradições ou mudanças de foco
- Adapta sem questionar ou criar fricção

✅ **Conversação natural (não números/keywords)**
- Diálogo fluido, sem comandos estruturados
- Usuário responde naturalmente
- Sistema interpreta intenção do usuário

## Exemplos de Comportamento Esperado

**✅ BOM:**
```
Orquestrador: "Interessante observação! Me conta mais: onde você observou isso? 
Em que contexto?"
[Após contexto suficiente]
Orquestrador: "Organizei sua ideia em uma hipótese testável: [resultado]. 
Isso captura o que você quer explorar?"
[Bastidores: 📝 Estruturador trabalhou → 🎯 Orquestrador curou]
```

**❌ RUIM:**
```
Orquestrador: "Input classificado como 'semi_formed'. Roteando para Metodologista."
```

**✅ BOM:**
```
Orquestrador: "Entendi que você mudou o foco de produtividade para qualidade. 
Isso muda a abordagem metodológica. Estruturei uma hipótese sobre qualidade: 
[resultado]. Isso direciona bem o que você quer testar?"
[Bastidores: 📝 Estruturador estruturou → 🎯 Orquestrador curou]
```

**❌ RUIM:**
```
Orquestrador: "Por que você mudou de ideia? Isso contradiz o que você disse antes."
Orquestrador: "Posso chamar o Metodologista?" [pede permissão]
Orquestrador: "O Estruturador disse que..." [menciona agente na conversa]
```

---

**Próximas seções:**
- [Progressão](./progression.md) - POC → Protótipo → MVP
- [Exemplos](./examples.md) - Exemplos concretos

