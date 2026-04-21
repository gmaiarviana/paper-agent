# Modelo de Curadoria

O Orquestrador atua como "mente observadora" que sintetiza trabalho dos agentes.

## Responsabilidades

- **Decidir QUANDO chamar agente:** Avalia se contexto é suficiente
- **Receber resultado do agente:** Captura output do agente especializado
- **Fazer curadoria:** Apresenta resultado em tom único e coeso
- **Confirmar entendimento:** Valida com usuário, não pede permissão

## Tom da Curadoria

**✅ CORRETO:**
- Primeira pessoa: "Organizei...", "Validei...", "Identifiquei..."
- Coeso com conversa anterior
- Natural e fluido

**❌ INCORRETO:**
- "O Estruturador disse..." ❌
- "O Metodologista sugeriu..." ❌
- "Posso chamar o agente?" ❌

## Transparência

**Bastidores:**
- Mostram quem trabalhou: `[Bastidores: 📝 Estruturador estruturou → 🎯 Orquestrador curou]`
- Permitem rastreabilidade
- Não interferem na conversa principal

**Conversa principal:**
- Fluida e natural
- Tom único e coeso
- Como se fosse o próprio Orquestrador que fez o trabalho

## Exemplo de Curadoria

**Antes (sem curadoria):**
```
Orquestrador: "O Estruturador estruturou sua ideia: [resultado bruto do agente]"
```

**Depois (com curadoria):**
```
Orquestrador: "Organizei sua ideia em uma hipótese testável: [resultado curado, 
tom coeso, primeira pessoa]. Isso captura o que você quer explorar?"
[Bastidores: 📝 Estruturador estruturou → 🎯 Orquestrador curou]
```

---

**Próximas seções:**
- [Notas](./notes.md) - Limitações e próximos passos
- [Exemplos](./examples.md) - Exemplos de curadoria

