# Arquitetura do Orquestrador Conversacional

## Decisão Arquitetural: Substituição Direta

**Abordagem:** Substituir `orchestrator_node` atual diretamente (abordagem ousada).

**Mudanças:**
- ❌ Remove lógica de classificação (`vague`/`semi_formed`/`complete`)
- ✅ Novo comportamento: explorar → analisar → chamar agente automaticamente → curar → confirmar
- ✅ Mantém estrutura de `MultiAgentState`
- ✅ Ignora limite de contexto no POC (foco em raciocínio básico)

## Novo Comportamento do Orquestrador

O Orquestrador POC evolui de **classificador determinístico** para **facilitador conversacional**:

```
ANTES (Épico 3):
Input → Classifica (vague/semi_formed/complete) → Roteia automaticamente

DEPOIS (Épico 7 POC - Transição Fluida):
Input → Conversa → Analisa contexto → Chama agente automaticamente → Curadoria → Confirma entendimento
```

**Papel do Orquestrador:**
- **Explorar:** Faz perguntas abertas para entender contexto
- **Analisar:** Examina input + histórico conversacional
- **Decidir:** Chama agente automaticamente quando contexto suficiente
- **Curar:** Recebe resultado do agente, apresenta em tom coeso e unificado
- **Confirmar:** Valida entendimento com usuário, não pede permissão

---

**Próximas seções:**
- [Raciocínio](./reasoning.md) - Capacidades detalhadas
- [Fluxo](./flow.md) - Fluxo conversacional completo
- [Implementação](./implementation.md) - Mudanças técnicas no código

